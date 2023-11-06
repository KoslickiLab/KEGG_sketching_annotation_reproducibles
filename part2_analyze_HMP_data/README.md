This file gives instructions on how to reproduce the results for the analysis of HMP datasets in **Section 3.2**.

</br>



### Download resources

---

1. raw data: download information and metadata files were retrived from the HMP database in 2023.1. They also come with this repository in the `data_file` folder with md5:

   ```
   3756e6536c1895a580558d670eb68738  hmp_manifest_160bdc491e.tsv
   bbb3a27faa1b634c51c9c412cbde7376  hmp_manifest_metadata_1ccd2b6917.tsv
   ```

2. KEGG reference data:

   ```
   wget https://zenodo.org/records/10055954/files/KOs_sbt_scaled_1000_k_11.sbt.zip
   ```

3. Merged table containing the functional profiles (relative abundances of KOs) of filtered HMP samples: this is the result from **part2.1**, which is time consuming and computational expensive. For the convenience, you may download this file for downstream analysis. 

   ```
   wget <to add link here>
   ```



</br>

### Part2.1, generate functional profiles of HMP data

---

**Caution**: This step involves downloading and processing a substantial 4.6TB of raw data. We strongly recommend having a minimum of 50GB of memory (for those large samples) available and be prepared for the jobs to run for several days to completion. If you're not using some task management system (e.g. Slurm), it's recommented to use `nohup` for all tasks here. 

</br>

#### 2.1.1, download HMP data (~4.6TB)

```
cd ./part2_analyze_HMP_data

mkdir -p raw_data
target_dir=$(readlink -f raw_data)
manifest=$(readlink -f ./data_file/hmp_manifest_160bdc491e.tsv)
metadata=$(readlink -f ./data_file/hmp_manifest_metadata_1ccd2b6917.tsv)

# use 10 rows to test command
# head ${manifest} > temp_manifest && manifest=$(readlink -f temp_manifest)
# head ${metadata} > temp_metadata && metadata=$(readlink -f temp_metadata)

# download
bash ./src/download_hmp_data.sh ${target_dir} ${manifest} ${metadata}
```

</br>

#### 2.1.2, build FracMinHash sketches by sourmash

```
# assume we are still in the "part2_analyze_HMP_data" folder

mkdir -p single_FMH_sketch
target_dir=$(readlink -f single_FMH_sketch)
single_file_dir=$(readlink -f ./raw_data/download/checked_fq_files)

# build FracMinHash sketch
bash ./src/build_sourmash_sketch.sh ${single_file_dir} ${target_dir}
```

</br>

#### 2.1.3, get functional profiles

```
# assume we are still in the "part2_analyze_HMP_data" folder

mkdir -p functional_profile
target_dir=$(readlink -f functional_profile)
query_sketch_dir=$(readlink -f ./single_FMH_sketch/scale_1000_protein/)
ref_db=$(readlink -f KOs_sbt_scaled_1000_k_11.sbt.zip)

# generate functional profiles
bash ./src/sourmash_gather_func_profile.sh ${target_dir} ${query_sketch_dir} ${ref_db}
```

</br>

#### 2.1.4, merge all results and generate the heatmap (Fig 4)

```
# assume we are still in the "part2_analyze_HMP_data" folder

# this is the edited metafile with f_uid for each sample
curated_metafile=$(readlink -f ./raw_data/all_data_cleaned_metadata.tsv)
single_gather_dir=$(readlink -f ./functional_profile/single_gather_out/)
mkdir -p merged_df_and_heatmap
cd merged_df_and_heatmap

# merge df
python ../src/merge_df_and_heatmap.py -m ${curated_metafile} -i ${single_gather_dir}

# generate heatmap
python ../src/merge_df_and_heatmap.py -m ${curated_metafile} -d remove_low_depth_KO_files_rela_abund_k11.csv
```

</br>

### Part 2.2, downstream analysis

---

Now we have performed functional profiles for all HMP data using FracMinHash sketches. You may also skip part 2.1 and download the `remove_low_depth_KO_files_rela_abund_k11.csv` file [here](Add link). 






