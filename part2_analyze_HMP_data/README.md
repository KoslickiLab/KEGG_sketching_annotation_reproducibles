This file gives instructions on how to reproduce the results for the analysis of HMP datasets in **Section 3.2**.

</br>

<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [Download resources](#download-resources)
- [Part2.1, generate functional profiles of HMP data](#part21-generate-functional-profiles-of-hmp-data)
  * [2.1.1, download HMP data (~4.6TB)](#211-download-hmp-data-46tb)
  * [2.1.2, build FracMinHash sketches by sourmash](#212-build-fracminhash-sketches-by-sourmash)
  * [2.1.3, get functional profiles](#213-get-functional-profiles)
  * [2.1.4, merge all results and generate the heatmap (Fig 4)](#214-merge-all-results-and-generate-the-heatmap-fig-4)
- [Part 2.2, downstream analysis](#part-22-downstream-analysis)
  * [2.2.1, prepare data to fit LEfSe format](#221-prepare-data-to-fit-lefse-format)
  * [2.2.2, run LEfSe and generate figures with annotation](#222-run-lefse-and-generate-figures-with-annotation)

<!-- TOC end -->



<!-- TOC --><a name="download-resources"></a>

### Download resources

---

```
cd ./part2_analyze_HMP_data

# download KEGG KO reference
wget https://zenodo.org/records/10055954/files/KOs_sbt_scaled_1000_k_11.sbt.zip

# you pay skip part2.1 by using this merged functional profiles directly
gunzip ./data_file/remove_low_depth_KO_files_rela_abund_k11.csv.gz
```

</br>

<!-- TOC --><a name="part21-generate-functional-profiles-of-hmp-data"></a>

### Part2.1, generate functional profiles of HMP data

---

**Caution**: **This step takes a long time to finish.** This step involves downloading and processing a substantial 4.6TB of raw data. We strongly recommend having a minimum of 10 threads and 50GB MEM (for those large samples) and be prepared for the jobs to **run for several days** to completion. If you're not using some task management system (e.g. Slurm), it's recommented to use `nohup` for all tasks here. 

<!-- TOC --><a name="211-download-hmp-data-46tb"></a>

#### 2.1.1, download HMP data (~4.6TB)

```
mkdir -p raw_data
target_dir=$(readlink -f raw_data)
manifest=$(readlink -f ./data_file/hmp_manifest_160bdc491e.tsv)
metadata=$(readlink -f ./data_file/hmp_manifest_metadata_1ccd2b6917.tsv)

# download
bash ./src/download_hmp_data.sh ${target_dir} ${manifest} ${metadata}
```

</br>

<!-- TOC --><a name="212-build-fracminhash-sketches-by-sourmash"></a>

#### 2.1.2, build FracMinHash sketches by sourmash

```
mkdir -p single_FMH_sketch
target_dir=$(readlink -f single_FMH_sketch)
single_file_dir=$(readlink -f ./raw_data/download/checked_fq_files)

# build FracMinHash sketch
bash ./src/build_sourmash_sketch.sh ${single_file_dir} ${target_dir}
```

</br>

<!-- TOC --><a name="213-get-functional-profiles"></a>

#### 2.1.3, get functional profiles

```
mkdir -p functional_profile
target_dir=$(readlink -f functional_profile)
query_sketch_dir=$(readlink -f ./single_FMH_sketch/scale_1000_protein/)
ref_db=$(readlink -f KOs_sbt_scaled_1000_k_11.sbt.zip)

# generate functional profiles
bash ./src/sourmash_gather_func_profile.sh ${target_dir} ${query_sketch_dir} ${ref_db}
```

</br>

<!-- TOC --><a name="214-merge-all-results-and-generate-the-heatmap-fig-4"></a>

#### 2.1.4, merge all results and generate the heatmap (Fig 4)

```
# this is the edited metafile with f_uid for each sample
curated_metafile=$(readlink -f ./raw_data/all_data_cleaned_metadata.tsv)
single_gather_dir=$(readlink -f ./functional_profile/single_gather_out/)
mkdir -p merged_df_and_heatmap
cd merged_df_and_heatmap

# merge df
python ../src/merge_df_and_heatmap.py -m ${curated_metafile} -i ${single_gather_dir}

# generate heatmap
python ../src/merge_df_and_heatmap.py -m ${curated_metafile} -d remove_low_depth_KO_files_rela_abund_k11.csv
cd ..
```

</br>

<!-- TOC --><a name="part-22-downstream-analysis"></a>

### Part 2.2, downstream analysis

---

Now we have performed functional profiles for all HMP data using FracMinHash sketches. You may also skip part 2.1 and use the merged results in the `data_file` folder.

<!-- TOC --><a name="221-prepare-data-to-fit-lefse-format"></a>

#### 2.2.1, prepare data to fit LEfSe format

```
# this ko-pathway relation file is obtained from KEGG database
ko_pathway_map_file=$(readlink -f ./data_file/link_pathway_to_ko.txt)

# merged data file
# if you are using the file in this repo
# input_file=$(readlink -f ./data_file/remove_low_depth_KO_files_rela_abund_k11.csv)

input_file=$(readlink -f ./merged_df_and_heatmap/remove_low_depth_KO_files_rela_abund_k11.csv)
mkdir -p lefse
cd lefse

# clean and subset ko-pathway map file for faster process
cut -f 1-2 ${ko_pathway_map_file} | sed '1d' | sed 's/ko://g' | sed 's/path://g' > temp_simplified_ko_map.tsv
cut -d"," -f 1 ${input_file} | sed '1d' > temp_ko_list.txt
grep -w -f temp_ko_list.txt temp_simplified_ko_map.tsv > subset_ko_map.tsv
rm temp_ko_list.txt temp_simplified_ko_map.tsv

# split merged df by condition: IBD/T2D vs HHS for KO and Pathway
python ../src/prepare_lefse_input.py ${input_file}
```

</br>

<!-- TOC --><a name="222-run-lefse-and-generate-figures-with-annotation"></a>

#### 2.2.2, run LEfSe and generate figures with annotation

```
# assume we are still in ./part2_analyze_HMP_data/lefse folder

# there are 4 compare tsv files for KO- and pathway-level differential analysis in IBD vs HHS and T2D vs HHs
for input_tsv in $(ls -1 compare*.tsv); do
 ### format
 lefse_format_input.py ${input_tsv} format_${input_tsv}.in -c 2 -u 1 -o 1000000
 ### run: time consuming
 /usr/bin/time -av -o runlog_lefse lefse_run.py format_${input_tsv}.in output_${input_tsv}.res
 ### visualize
 lefse_plot_res.py output_${input_tsv}.res barplot_${input_tsv}.png
done

# Since the default figure generated by LEfSe is not easy to interpret, we added KO/map annotation to the top hits and visulize them as follows:

# Fig5: the annotation files are also in the data_file folder
python ../src/plot_lefse_top_hits.py -i output_compare_T2D_HHS_KO.tsv.res -x ../data_file/kegg_koids.txt -o "T2D_KO"
python ../src/plot_lefse_top_hits.py -i output_compare_T2D_HHS_maps.tsv.res -y ../data_file/pathway.list -o "T2D_pathway"
```