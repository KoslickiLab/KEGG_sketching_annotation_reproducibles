This file gives instructions on how to reproduce the results for the comparison of sourmash with KofamScan and Diamond.

## Installation

### Installing python dependencies
```
conda create -y --name annotate_ko
conda install -y --name annotate_ko -c conda-forge -c bioconda --file requirements.txt
conda activate annotate_ko
```

### Installing KofamScan
To install KofamScan, please follow the instructions from here:
```
https://www.genome.jp/ftp/tools/kofam_scan/INSTALL
```
After installing KofamScan, we need to know:
1. Location of the executable: this is the path to the exec_annotation file
1. Location of the KofamScan config file

### Installing Diamond
Diamond comes pre-built with the repository (designed for a linux system).

## Downloading resources
Because github has a limit on the file size, we have put some files on Zenodo. Plese use the following steps to obtain these files:
```
mkdir required_files
cd required_files
wget https://zenodo.org/records/10055954/files/genomes_extracted_from_kegg.zip?download=1
wget https://zenodo.org/records/10055954/files/KOs_sbt_scaled_1000_k_11.sbt.zip?download=1
wget https://zenodo.org/records/10055954/files/KOs_sbt_scaled_1000_k_15.sbt.zip?download=1
wget https://zenodo.org/records/10055954/files/KOs_sbt_scaled_1000_k_7.sbt.zip?download=1
wget https://zenodo.org/records/10055954/files/present_genes_and_koids.csv?download=1
wget https://zenodo.org/records/10055954/files/protein_ref_db_giant.faa?download=1
unzip genomes_extracted_from_kegg.zip
```

## How to run?
After installing, we need to do the following:
1. `cd manuscript_experiment`
1. Edit the file named `snakefile` and write the full path to KofamScan locations. Also, add the path where required files have been downloaded.
1. Run the following code:
```
snakemake create_all_metagenomes -j <num_cores_to_use>
snakemake create_all_ko_ground_truths -j <num_cores_to_use>
snakemake all_kofam -j <num_cores_to_use>
snakemake all -j <num_cores_to_use>
```


## Plotting
Gather all statistics from all these runs using the following:
```
python aggregate_large_MG_results.py
python aggregate_small_MG_results.py
```

These statistics were plotted using `plotter.m`
