This file gives instructions on how to generate the plots in **Section 3.1** and **Section 3.2**.

## Step 1: download resources
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

## Step 2: set up environment
1. Clone the camisim repository from here: https://github.com/CAMI-challenge/CAMISIM
1. Change the hardcoded items in `run_camisim.py`. Every path must be absolute path
1. Change the hardcoded items in `run_tools/run_sourmash/run_sourmash_batch.py`
1. Change the hardcoded items in `run_simulations/run_sourmash.py`

## Step 3: run camisim to generate the simulated metagenomes
```
cd run_simulations/vary_error_rates
python run_simulation.py
bash run_simulation.sh
```

## Step 4: run diamond
```
cd run_simulations/vary_error_rates
python run_diamond_batch.py
bash run_diamond_batch.sh
```

## Step 5: run fmh-funprofiler
```
cd run_simulations/vary_error_rates
python run_sourmash_batch.py
bash run_sourmash_batch.sh
```

## Step 6: aggregate all results
```
cd run_simulations/vary_error_rates
python compute_performance_metrics.py
python summarize_all_results_batch.py
```

## Step 7: plot
```
cd run_simulations/vary_error_rates
python plot_results.py
python plot_perf_metrics.py
```

