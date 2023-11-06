import pandas as pd
import numpy as np
import os, re
import matplotlib.pyplot as plt
import seaborn as sns
import argparse

def local_variable():
    input_file = os.path.abspath("./lefse_output/output_compare_T2D_HHS_KO.tsv.res")
    out_name = "T2D_KO"

    input_file = os.path.abspath("./lefse_output/output_compare_T2D_HHS_maps.tsv.res")
    out_name = "T2D_map"

    num_hits = 10
    lda_cutoff = 2

def barplot_lefse_output(df1, df2, conditions, out_name):
    """
    Make stacked barplots for LEFSE output (similar to standard, but need to tune parameters)
    :param df1: pre-sorted condition 1 (left panal)
    :param df2: pre-sorted condition 2 (right panal)
    :param conditions: 2 conditions for label
    :param out_name: output name
    :return:
    """

    ### build a merged df
    # df1 -> negative values
    temp_1 = df1.copy()
    temp_1['LDA'] = temp_1['LDA'] * -1
    temp_1['group'] = conditions[0]
    # change df2 to ascending order for better view
    temp_2 = df2.copy()
    temp_2 = temp_2.sort_values(by='LDA', ascending=True)
    temp_2['group'] = conditions[1]
    merged_df = pd.concat([temp_1, temp_2], ignore_index=True)

    ### make fig
    fig, ax = plt.subplots(figsize=(10, 12))
    sns.set_color_codes("pastel")
    sns.barplot(x="LDA", y="feature", data=merged_df, hue="group", palette='bright', ax=ax)
    ax.legend(ncol=2, loc='upper right', frameon=True)
    ax.set(xlim=(-5, 5), ylabel="", xlabel="LDA score (log10)")
    sns.despine(left=True, bottom=True)
    # Add vertical lines at -2, 0, and 2
    plt.axvline(x=-2, color='gray', linestyle='--', label='-2', alpha=0.5)
    plt.axvline(x=0, color='gray', linestyle='--', label='0', alpha=0.5)
    plt.axvline(x=2, color='gray', linestyle='--', label='2', alpha=0.5)
    plt.axvline(x=4, color='gray', linestyle='--', label='4', alpha=0.5)
    plt.axvline(x=-4, color='gray', linestyle='--', label='-4', alpha=0.5)
    fig.savefig("Fig5_" +out_name + ".png", dpi=300)
    del fig

def barplot_lefse_with_annotation(df1, df2, conditions, out_name, annotation_df, col_2_use,
                                  sup_title="Differential analysis"):
    """
    Make stacked barplots for LEFSE output (similar to standard, but need to tune parameters)
    :param df1: pre-sorted condition 1 (left panal)
    :param df2: pre-sorted condition 2 (right panal)
    :param conditions: 2 conditions for label
    :param out_name: output name
    :param annotation_df: switch ko/maps to description of itself
    :return:
    """

    ### build a merged df
    # df1 -> negative values
    temp_1 = df1.copy()
    temp_1['LDA'] = temp_1['LDA'] * -1
    temp_1['group'] = conditions[0]
    # change df2 to ascending order for better view
    temp_2 = df2.copy()
    temp_2 = temp_2.sort_values(by='LDA', ascending=True)
    temp_2['group'] = conditions[1]
    merged_df = pd.concat([temp_1, temp_2], ignore_index=True)

    # replace the feature col with new description: original Kxxx - new Kxxx:function
    keys_2_replace = merged_df['feature']
    sub_anno_df = annotation_df[annotation_df[col_2_use].isin(keys_2_replace)]
    dict_replace = dict(zip(sub_anno_df[col_2_use], sub_anno_df['new_desc']))
    # update merged df to plot
    merged_df.replace(dict_replace, inplace=True)

    ### make fig
    fig, ax = plt.subplots(figsize=(20, 12))
    sns.set_color_codes("pastel")
    sns.barplot(x="LDA", y="feature", data=merged_df, hue="group", palette='bright', ax=ax)
    ax.legend(ncol=1, loc='upper right', frameon=True)
    ax.set(xlim=(-5, 5), ylabel="", xlabel="LDA score (log10)")
    sns.despine(left=True, bottom=True)
    # Add vertical lines at -2, 0, and 2
    plt.axvline(x=-2, color='gray', linestyle='--', label='-2', alpha=0.5)
    plt.axvline(x=0, color='gray', linestyle='--', label='0', alpha=0.5)
    plt.axvline(x=2, color='gray', linestyle='--', label='2', alpha=0.5)
    plt.axvline(x=4, color='gray', linestyle='--', label='4', alpha=0.5)
    plt.axvline(x=-4, color='gray', linestyle='--', label='-4', alpha=0.5)
    plt.subplots_adjust(left=0.55, right=0.95, top=0.9, bottom=0.1)
    plt.suptitle(sup_title, y=0.95, fontweight='bold')
    fig.savefig("Fig5_" + out_name + ".png", dpi=300)
    del fig


def local_variable():
    input_file = os.path.abspath("lefse_output/output_compare_T2D_HHS_KO.tsv.res")
    input_file = os.path.abspath("lefse_output/output_compare_T2D_HHS_maps.tsv.res")
    out_name = 'temp'
    num_hits = 10
    lda_cutoff = 2
    desc_ko = os.path.abspath("./lefse_output/kegg_koids.txt") # from KEGG FTP, and further cleaned
    desc_map = os.path.abspath("./lefse_output/pathway.list")  # obtained from KEGG FTB

def local_bash_code():
    print("hello")
    print("python ../src/plot_lefse_top_hits.py -i output_compare_T2D_HHS_KO.tsv.res -x kegg_koids.txt -o T2D_KO")
    print("python ../src/plot_lefse_top_hits.py -i output_compare_T2D_HHS_maps.tsv.res -y pathway.list -o T2D_map")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot LEFSE results",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-i', '--input_file', help="Path to lefse output file", required=True)
    parser.add_argument('-x', '--desc_ko', help="Path to KO description file", default=None)
    parser.add_argument('-y', '--desc_map', help="Path to Pathway description file", default=None)
    parser.add_argument('-o', '--output_prefix', help="Give a name to output file(s)", default="temp")
    parser.add_argument('-n', '--num', type=int, help="Number of features to plot", default=10)
    parser.add_argument('-l', '--lda_cutoff', type=int, help="LDA cutoff", default=2)

    args = parser.parse_args()
    input_file = args.input_file
    out_name = args.output_prefix
    num_hits = args.num
    lda_cutoff = args.lda_cutoff
    desc_ko = args.desc_ko
    desc_map = args.desc_map

    # load data
    df_result = pd.read_csv(input_file, sep="\t", header=None, names=['feature', 'normalized_mean_in_high_group', 'group', 'LDA', 'pvalue'])
    sub_df = df_result[df_result['LDA'] > lda_cutoff]

    # get descrtiptino data
    if desc_ko:
        df_ko = pd.read_csv(desc_ko, sep="\t")
        # remove the prefix xxxx; (names, but not description)
        # there is 1 record has no other name, so can't use [x.split(";")[1] for x in df_ko['desc']] (index error)
        remove_prefix = [re.sub('.*; ', '', x) for x in df_ko['desc']]
        # remove the trailing [xxx.xx.x]
        remove_suffix = [re.sub(' \[.*\]', '', x) for x in remove_prefix]
        df_ko['new_desc'] = [f"{x}: {y}" for x, y in zip(df_ko['kegg_ko_id'], remove_suffix)]
        anno_df = df_ko
        col2use = 'kegg_ko_id'
        sup_title = 'Differential analysis: KO'
    elif desc_map:
        df_map = pd.read_csv(desc_map, sep="\t", header=None, comment="#", names=['map_id', 'desc'],
                             dtype={'map_id': 'string', 'desc': 'string'})
        df_map['map_id'] = ["map" + x for x in df_map['map_id']]
        df_map['new_desc'] = [f"{x}: {y}" for x, y in zip(df_map['map_id'], df_map['desc'])]
        anno_df = df_map
        col2use = 'map_id'
        sup_title = "Differential analysis: pathway"
    else:
        raise Exception("You must provide one description file for either KO or MAP")

    conditions = sorted(set(sub_df['group']))
    if len(conditions) != 2:
        raise Exception("There are NOT 2 conditions, please double check input")

    df1 = sub_df[sub_df['group'] == conditions[0]].sort_values(by='LDA', ascending=False)
    df1 = df1[['feature', 'LDA']].iloc[:num_hits]
    df2 = sub_df[sub_df['group'] == conditions[1]].sort_values(by='LDA', ascending=False)
    df2 = df2[['feature', 'LDA']].iloc[:num_hits]

    # make bar plot
    sns.set(font_scale=2)
    # barplot_lefse_output(df1, df2, conditions=conditions, out_name=out_name)
    barplot_lefse_with_annotation(df1, df2, conditions=conditions, out_name=out_name,
                                  annotation_df=anno_df, col_2_use=col2use,
                                  sup_title=sup_title)



