# KEGG-sketch-each-KO
This repository gives instructions on how to reproduce the results for the comparison of sourmash with KofamScan and Diamond.

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

## Downloading resource
Because github has a limit on the file size, we have put some files on Zenodo. Plese use the following steps to obtain these files:
1. Protein reference database:
1. List of genes present in the KEGG database, and their KOIDs:
1. Sequence bloom tree of the KO sketches:

## How to run?
After installing, we need to do the following:
1. `cd manuscript_experiment`
1. Edit the file named `snakefile` and write the full path to all resources that have been downloaded/installed
1. `snakemake create_all_metagenomes -j <num_cores_to_use>`
1. `snakemake create_all_ko_ground_truths -j <num_cores_to_use>`
1. `snakemake all_kofam -j <num_cores_to_use>`
1. `snakemake all -j <num_cores_to_use>`


## Plotting
Gather all statistics from all these runs using the following:
```
python aggregate_large_MG_results.py
python aggregate_small_MG_results.py
```

These statistics were plotted using `plotter.m`
