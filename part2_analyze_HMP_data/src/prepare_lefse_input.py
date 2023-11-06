### this is Py script
import sys
import pandas as pd
import re

input_df = sys.argv[1]
df = pd.read_csv(input_df, header=0, index_col=0)

# add row for study name
t_df = df.transpose()
t_df['study'] = [re.sub(r'f[0-9]{1,4}_(ihmp|HMP)_','', x) for x in t_df.index]
df = t_df.transpose()
df = df.reindex(['study'] + df.index[:-1].tolist())
del t_df

# split to 2 KO contrast files: T2D vs HHS, and IBD vs HHS
t2d_columns = df.columns[df.loc['study'] != "IBD"]
out_t2d = df[t2d_columns]
out_t2d.to_csv("compare_T2D_HHS_KO.tsv", header=True, index=True, sep="\t")

ibd_columns = df.columns[df.loc['study'] != "T2D"]
out_ibd = df[ibd_columns]
out_ibd.to_csv("compare_IBD_HHS_KO.tsv", header=True, index=True, sep="\t")


# aggregate this KO profile into pathway profile by the simplifed map
df_map = pd.read_csv("subset_ko_map.tsv", sep="\t", header=None, names=['ko','map'])
map_set = set(df_map['map'])
dict_map_ko = {}
## build a dict for map:{ko} relation for fast retrive
for item in map_set:
 dict_map_ko[item] = set(df_map[df_map.iloc[:, 1] == item]['ko'])
## aggregate df
aggr_list = []
index_list = []
aggr_list.append(df.columns)
index_list.append('name')
aggr_list.append(df.loc['study',:])
index_list.append('study')
for item in dict_map_ko:
 sub_df = df.loc[df.index.isin(dict_map_ko[item])]
 aggr_list.append(sub_df.sum(axis=0))
 index_list.append(item)

df_aggr = pd.DataFrame(aggr_list)
df_aggr.index = index_list
df_aggr.to_csv("map_aggr_by_KO_matrix_k11_rela_abund.tsv", sep="\t", header=False, index=True)

# split to 2 map contrast files: T2D vs HHS, and IBD vs HHS
t2d_columns = df_aggr.columns[df_aggr.loc['study'] != "IBD"]
out_t2d = df_aggr[t2d_columns]
out_t2d.to_csv("compare_T2D_HHS_maps.tsv", header=False, index=True, sep="\t")

ibd_columns = df_aggr.columns[df_aggr.loc['study'] != "T2D"]
out_ibd = df_aggr[ibd_columns]
out_ibd.to_csv("compare_IBD_HHS_maps.tsv", header=False, index=True, sep="\t")
