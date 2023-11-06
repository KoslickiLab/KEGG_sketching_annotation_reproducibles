This experiment uses the same HMP as in part 2. For instructions on how to download the raw data, refer to [this guide](https://github.com/KoslickiLab/KEGG_sketching_annotation_reproducibles/blob/main/part2_analyze_HMP_data/README.md) and follow section 2.1.1 through 2.1.4 to obtain the combined dataframe `remove_low_depth_KO_files_rela_abund_k11.csv`, which is a combined dataframe consisting of functional profiles of HHS, T2D and IBD samples.
For this experiment, we further removed all the IBD samples from this dataframe and kept only the HHS and IBD samples.

## 1. Computing pairwise FunUniFrac
### 1.1 Clone FunUniFrac repo and setup condo environment
```angular2html
cd KEGG_sketching_annotation_reproducibles
git clone https://github.com/KoslickiLab/FunUniFrac.git
conda env update -f environment.yml
conda activate fununifrac
```

### 1.2 Compute pairwise FunUniFrac
```angular2html
python FunUniFrac/fununifrac/compute_fununifrac_combined.py -e part3_FunUniFrac/data/kegg_tree.txt -f part3_FunUniFrac/data/hq_data_t2d_hhs_only.csv -o part3_FunUniFrac/data/output -i pw_fununifrac_hhs_vs_t2d
```
This will produce output files `pw_fununifrac_hhs_vs_t2d.npy` and `pw_fununifrac_hhs_vs_t2d.basis.npy` in the part3_FunUniFrac/data/output folder.

## 2. MDS plot
```angular2html
python part3_FunUniFrac/scripts/plot_mds.py -pd part3_FunUniFrac/data/output/pw_fununifrac_hhs_vs_t2d.npy -l part3_FunUniFrac/data/output/pw_fununifrac_hhs_vs_t2d.basis.npy -o part3_FunUniFrac/data/output/mds_hhs_vs_t2d_fununifrac.pdf -m part3_FunUniFrac/data/metadata_hq_HHS_T2D.tsv
```
This will create a file named `mds_hhs_vs_t2d_fununifrac.pdf` in part3_FunUniFrac/data/output.

## 3. PCoA plot
```angular2html
python part3_FunUniFrac/scripts/plot_pcoa.py -f part3_FunUniFrac/data/hq_data_t2d_hhs_only.csv -m part3_FunUniFrac/data/metadata_hq_HHS_T2D.tsv -o part3_FunUniFrac/data/output/pcoa_hhs_vs_t2d.png -2D
```

