from typing import Any
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sys, csv, os, argparse, re, glob
sys.setrecursionlimit(1000000)  # to avoid max recur for k=7 matrix



def parse_metadata(file_metadata, subset: list = None, exclude: list = None):
	"""
	Parse the input metadata which has a fixed composition and is tab delimited
	:param file_metadata: path to metadata file
	:param subset: subset of files to keep
	:param exclude: list of files to exclude, e.g. ['f259']
	:return: a dataframe
	"""

	temp_df = pd.read_csv(file_metadata, sep='\t')
	temp_df = temp_df[['f_uid', 'size', 'sample_id', 'subject_id', 'subject_gender', 'subject_race', 'study_full_name']]

	# exclude row records by f_uid
	if exclude:
		temp_df = temp_df[~temp_df['f_uid'].isin(exclude)]

	# subset
	if subset:
		temp_df = temp_df[temp_df['f_uid'].isin(subset)]

	# output
	print('Parsed {} records'.format(len(temp_df)))
	return temp_df


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="HMP Cluster analysis",
									 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('-m', '--metafile', help="Path to metadata")
	parser.add_argument('-i', '--input_folder', help="Path to folder that stores all single gather out", default='.')
	parser.add_argument('-o', '--output_prefix', help="Give a name to output file(s)", default="filtered_data")
	parser.add_argument('-k', '--klist', help="List of k values to check, sep by comma", default="11,11")
	parser.add_argument('-s', '--subset_list', help="Path to 1 col file with subset f_uids", default=None)
	parser.add_argument('-d', '--merged_data', help="Path to merged data so don't need to merge again", default=None)
	parser.add_argument('-f', '--field', help="Which field of gather output to use", default='f_unique_weighted')
	
	

	args = parser.parse_args()
	metafile = os.path.abspath(args.metafile)
	df_meta = parse_metadata(metafile)
	input_folder = os.path.abspath(args.input_folder)
	out_name = args.output_prefix
	# used to work with multiple k values, but now we only need one; though still keep the previous code
	k_list = [int(x) for x in args.klist.split(',')]
	use_field = args.field

	# check if sub list exist
	if args.subset_list:
		sub_file = os.path.abspath(args.subset_list)
		temp_sub_df = pd.read_csv(sub_file, header=None)
		sub_list = set(temp_sub_df[0])
		del temp_sub_df
	else:
		sub_list = set()

	


	# run a merged file or merge by ourself
	if args.merged_data:
		data_df = pd.read_csv(args.merged_data, index_col='name')
		# transfer to row: data, col: KO; and fill NA with 0
		data_df = data_df.transpose()
		data_df.fillna(0, inplace=True)
		# add color map from metadata
		sub_df_meta = df_meta[df_meta['f_uid'].isin(list(data_df.index))]
		sub_df_meta['binary_size'] = np.where(sub_df_meta['size'] > 200 * 1024 * 1024, 'GT_200M', 'LT_200M')
		# build color dict
		color_map_dict = dict()
		for col_name in ['subject_id', 'subject_gender', 'subject_race', 'study_full_name', 'binary_size']:
			temp_distinct_category = sub_df_meta[col_name].unique()
			lut = dict(zip(temp_distinct_category, sns.color_palette("hls", len(temp_distinct_category))))
			# need to get a group information in the same order as the matrix go
			records_in_sim_matrix = []
			for item in list(data_df.index):
				records_in_sim_matrix.append(sub_df_meta.loc[sub_df_meta['f_uid'] == item, col_name].values[0])
			color_map_dict[col_name] = pd.Series(records_in_sim_matrix, index=list(data_df.index), name=col_name).map(lut)
		color_map_df = pd.DataFrame(color_map_dict)
		
		# generate clustermap
		fig = sns.clustermap(data_df, figsize=(20, 16), cmap="Greens", row_colors=color_map_df,
		                     col_cluster=False, metric="cosine")
		fig.fig.suptitle("Corr_" + out_name)
		fig.savefig("KEGG_clustermap_corrlation_" + out_name + ".png", dpi=300)
		del fig
		
		
		# make a binary table
		binary_data_df=data_df.copy()
		binary_data_df[binary_data_df!=0] = 1
		fig = sns.clustermap(binary_data_df, figsize=(20, 16), cmap="Greens", row_colors=color_map_df,
		                     col_cluster=False, metric="cosine")
		fig.fig.suptitle("Corr_" + out_name)
		fig.savefig("Fig4a_KEGG_clustermap_binary_funiquq_corrlation_" + out_name + ".png", dpi=300)
		del fig
	else:
		# generate merged KO table
		for k_value in k_list:
			gather_profile_dict = {}
			for sub_file in glob.glob(input_folder + '/sourmash_gather_out_scale1000_k_' + str(k_value) + '*.csv'):
				filename = re.sub("(.csv)|(sourmash_gather_out_scale1000_k_)" + str(k_value) + "_", "",
				                  os.path.basename(sub_file))
				# check if we need subset
				if len(sub_list) > 0:
					if filename in sub_list:
						temp_df = pd.read_csv(sub_file, header=0, index_col='name',
						                      usecols=['name', use_field])
						temp_df.columns = [filename]
						gather_profile_dict[filename] = temp_df
				else:
					temp_df = pd.read_csv(sub_file, header=0, index_col='name',
					                      usecols=['name', use_field])
					temp_df.columns = [filename]
					gather_profile_dict[filename] = temp_df
			# merge dataframes by "KO" column
			out_df = pd.concat(gather_profile_dict.values(), axis=1, join='outer', sort=True)

			# filter low depth files (<200M or data with <1000KO)
			small_file_list = df_meta[df_meta['size'] < 200*1024*1024]['f_uid'].to_list()
			sub_df = out_df.drop(columns=list(set(small_file_list) & set(out_df.columns)))
			binary_sub_df = sub_df.copy()
			binary_sub_df[binary_sub_df!=0] = 1
			column_sums = binary_sub_df.sum(axis=0)
			columns_to_delete = column_sums[column_sums < 1000].index.tolist()
			sub_df.drop(columns=columns_to_delete, inplace=True)
			sub_df.to_csv("remove_low_depth_KO_files_rela_abund_k11.csv")

			# plot KO occurrance
			binary_sub_df = sub_df.copy()
			binary_sub_df[binary_sub_df!=0] = 1
			values: Any = binary_sub_df.sum(axis=1)
			fig, axs = plt.subplots(figsize=(10,10))
			sns.histplot(values, bins=50, edgecolor='black', ax=axs)
			plt.yscale('log')
			plt.ylabel('Frequency')
			plt.xlabel('KO occurrence')
			plt.title('Histogram of KO occurrence')
			fig.savefig("Fig4b_hist_KO_occurrence.png", dpi=300)
	
	

