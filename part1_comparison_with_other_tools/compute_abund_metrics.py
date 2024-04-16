"""
In this script, we will compute the abundance metrics for a generated KO list.
Inputs:
    - KO ground truth
    - KO predictions by some method (DIAMOND, MMSeqs2, sourmash, etc.)
    - Output file name
Outputs:
    - Pearson correlation coefficient
"""

import pandas as pd
import numpy as np
import argparse

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Compute pearson correlation coefficient for KO predictions')
    parser.add_argument('ground_truth', type=str, help='Path to KO ground truth')
    parser.add_argument('predictions', type=str, help='Path to KO predictions')
    parser.add_argument('output', type=str, help='Path to output file')
    parser.add_argument('--toolname', type=str, help='Name of tool used to generate predictions', default='diamond')
    args = parser.parse_args()

    # Read in the KO ground truth, headers: ko_id,abund_by_num_reads,abund_by_num_nts,abund_by_mean_cov,abund_by_med_cov
    ground_truth = pd.read_csv(args.ground_truth, sep=',')
    ground_truth_kos = set(ground_truth['ko_id'])

    # Read in the KO predictions, ko_id,num_reads,num_nucleotides_covered,relative_abundance_by_num_reads,relative_abundance_by_nucleotides_covered
    predictions = pd.read_csv(args.predictions, sep=',')
    predicted_kos = predictions['ko_id'].tolist()
    if args.toolname == 'sourmash':
        colname = 'abundance'
    if args.toolname == 'diamond':
        colname = 'relative_abundance_by_num_reads'
    relative_abundances = predictions[colname].tolist()

    # make set of all KOs (ground truth and predictions)
    all_kos = set(ground_truth_kos)
    all_kos.update(set(predicted_kos))

    # for all KOs, get abundance from (a) ground truth and (b) predictions
    # if a KO is not in the ground truth, set its abundance to 0
    # if a KO is not in the predictions, set its abundance to 0
    ground_truth_abundances = []
    predicted_abundances = []
    for ko in all_kos:
        if ko in ground_truth_kos:
            ground_truth_abundances.append(ground_truth[ground_truth['ko_id'] == ko]['abund_by_num_reads'].values[0])
        else:
            ground_truth_abundances.append(0)
        if ko in predicted_kos:
            predicted_abundances.append(predictions[predictions['ko_id'] == ko][colname].values[0])
        else:
            predicted_abundances.append(0)

    # compute pearson correlation coefficient between ground truth and predictions
    pearson_corr = np.corrcoef(ground_truth_abundances, predicted_abundances)[0]

    # write pearson correlation coefficient to output file
    with open(args.output, 'w') as f:
        f.write(str(pearson_corr) + '\n')

    