#!/usr/bin/env python
import argparse
import os
import sys
from os.path import exists
import pathlib
from os import listdir
from os.path import isfile, join
import subprocess
import re
import numpy as np
from collections import Counter
import warnings
import pandas as pd
# for relative imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from src.HelperFuncs import make_sketches, run_sourmash_gather, check_extension, \
     build_diamond_db, run_diamond_blastx, parse_diamond_results


def main():
    parser = argparse.ArgumentParser(description="This script will use Diamond to classify a metagenome and report statistics on it.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-r', '--reference_file', type=str, help="The reference file (fna or faa) that you want to compare against.")
    parser.add_argument('-m', '--metagenome', type=str, help="The simulated metagenome.")
    parser.add_argument('-o', '--out_dir', type=str, help="The output directory.")
    parser.add_argument('-d', '--diamond_file', type=str, help="The output diamond file.")
    parser.add_argument('-k', '--ko_file', type=str, help="The final ko abudnance file.")
    parser.add_argument('-p', '--present_genes', type=str, help='file containing list of present genes and KO ids. Generated by main.py of the repo: https://github.com/mahmudhera/extract-kegg-organisms')
    parser.add_argument('-t', '--pident_threshold', type=float, default=0.1, help='pident threshold value. all reads mapped with pident value smaller than this will be dropped.')
    parser.add_argument('-T', '--num_threads', type=int, default=128, help='Number of threads to use when invoking Diamond.')

    # parse the args
    args = parser.parse_args()
    reference_file = args.reference_file
    metagenome_file = args.metagenome
    out_dir = args.out_dir
    diamond_file = args.diamond_file
    ko_file = args.ko_file
    present_genes_filename = args.present_genes
    pident_threshold = args.pident_threshold
    num_threads = args.num_threads

    # load gene to ko info
    gene_koid_df = pd.read_csv(present_genes_filename)
    gene_ids = gene_koid_df['gene_id'].tolist()
    ko_ids = gene_koid_df['ko_id'].tolist()

    gene_id_to_ko_id = {}
    for gene_id, ko_id in list( zip(gene_ids, ko_ids) ):
        gene_id_to_ko_id[gene_id] = ko_id

    # check args
    if not exists(out_dir):
        os.makedirs(out_dir)
    if not exists(metagenome_file):
        raise Exception(f"Input metagenome {metagenome_file} does not appear to exist")
    # Check if the reference database has been built, and build it if it hasn't
    ref_db = os.path.join(out_dir, os.path.basename(f"{reference_file}.dmnd"))
    if not exists(ref_db):
        warnings.warn(f"Diamond database {ref_db} does not appear to exist. Making it now. This may take some time.")
        build_diamond_db(reference_file, ref_db)
    # Do the alignment
    out_file = diamond_file
    if out_file is None:
        out_file = os.path.join(out_dir, f"{os.path.basename(metagenome_file)}_{os.path.basename(ref_db)}_matches.csv")
    run_diamond_blastx(metagenome_file, ref_db, out_file, num_threads = num_threads)

    diamond_results = parse_diamond_results(diamond_file, pident_threshold+1)
    gene_names = diamond_results['name'].tolist()
    num_reads_for_genes = diamond_results['num_reads'].tolist()
    gene_lengths = diamond_results['gene_length'].tolist()
    ave_bit_scores = diamond_results['ave_bit_score'].tolist()

    total_num_reads = sum(num_reads_for_genes)
    ko_abundances = {}
    for (gene_name, num_reads_mapped, length, avg_bit_score) in list( zip(gene_names, num_reads_for_genes, gene_lengths, ave_bit_scores) ):
        ko_id = gene_id_to_ko_id[gene_name]
        if ko_id not in ko_abundances.keys():
            ko_abundances[ko_id] = 1.0*num_reads_mapped/total_num_reads
        else:
            ko_abundances[ko_id] += 1.0*num_reads_mapped/total_num_reads

    out_list = []
    for ko_id in ko_abundances.keys():
        out_list.append( (ko_id, ko_abundances[ko_id]) )

    out_df = pd.DataFrame(out_list, columns=['ko_id', 'abundance'])
    out_df.to_csv( ko_file )


if __name__ == "__main__":
    main()