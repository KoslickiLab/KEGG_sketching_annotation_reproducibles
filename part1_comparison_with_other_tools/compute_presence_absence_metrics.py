"""
In this script, we will compute the presence-absence metrics for a generated KO list.
Inputs:
    - KO ground truth
    - KO predictions by some method (DIAMOND, MMSeqs2, sourmash, etc.)
    - Output file name
Outputs:
    - Precision
    - Recall

Workflow:
    1. Read in the KO ground truth and KO predictions
    2. Filter KO predictions so that the filtered KOs make up top 90%, 95%, or 100% of predictions
    3. Compute precision and recall for each filtered set of KOs
    4. Write precision and recall to output file (three lines, one for each filter level, 100% first, 95% second, 90% last)
"""

import pandas as pd
import numpy as np
import argparse
from scipy.stats import kendalltau
from scipy.special import rel_entr
from scipy.spatial.distance import braycurtis

def main():
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Compute precision and recall for KO predictions')
    parser.add_argument('ground_truth', type=str, help='Path to KO ground truth')
    parser.add_argument('predictions', type=str, help='Path to KO predictions')
    parser.add_argument('output', type=str, help='Path to output file')
    parser.add_argument('--toolname', type=str, help='Name of tool used to generate predictions', default='diamond')
    args = parser.parse_args()

    # Read in the KO ground truth, headers: ko_id,abund_by_num_reads,abund_by_num_nts,abund_by_mean_cov,abund_by_med_cov
    ground_truth = pd.read_csv(args.ground_truth, sep=',')
    ground_truth_kos_set = set(ground_truth['ko_id'])
    ground_truth_kos_list = ground_truth['ko_id'].tolist()
    #ground_truth_abundances = ground_truth['abund_by_num_reads'].tolist()
    ground_truth_abundances = ground_truth['abund_by_num_nts'].tolist()

    gt_ko_to_abund = dict(zip(ground_truth_kos_list, ground_truth_abundances))

    # Sort the KO ground truth by abundance (highest to lowest)
    sorted_indices = np.argsort(ground_truth_abundances)[::-1]
    sorted_kos_ground_truth = [ground_truth_kos_list[i] for i in sorted_indices]

    # Read in the KO predictions: ko_id,num_reads,num_nucleotides_covered,relative_abundance_by_num_reads,relative_abundance_by_nucleotides_covered
    predictions = pd.read_csv(args.predictions, sep=',')
    predicted_kos = predictions['ko_id'].tolist()
    if args.toolname == 'sourmash':
        colname = 'abundance'
    if args.toolname == 'diamond':
        colname = 'relative_abundance_by_nucleotides_covered'
    relative_abundances = predictions[colname].tolist()

    pred_ko_to_abund = dict(zip(predicted_kos, relative_abundances))

    # Sort the KO predictions by relative abundance (highest to lowest)
    sorted_indices = np.argsort(relative_abundances)[::-1]
    sorted_kos_predictions = [predicted_kos[i] for i in sorted_indices]
    predicted_kos_set = set(sorted_kos_predictions)

    # Compute precision and recall
    true_positives = len(ground_truth_kos_set.intersection(predicted_kos_set))
    false_positives = len(predicted_kos_set) - true_positives
    false_negatives = len(ground_truth_kos_set) - true_positives
    precision = true_positives / (true_positives + false_positives)
    recall = true_positives / (true_positives + false_negatives)

    # get the common kos between ground truth and predictions
    common_kos = ground_truth_kos_set.intersection(predicted_kos_set)

    # get the sorted order of these commons kos in the ground truth
    common_kos_sorted_indices = [sorted_kos_ground_truth.index(ko) for ko in common_kos]
    common_kos_sorted_indices_gt = list(common_kos_sorted_indices)
    # sort common_kos_sorted_indices_gt from small to large
    common_kos_sorted_indices_gt.sort()
    common_kos_sorted_gt = [sorted_kos_ground_truth[i] for i in common_kos_sorted_indices_gt]

    # get the sorted order of these commons kos in the predictions
    common_kos_sorted_indices = [sorted_kos_predictions.index(ko) for ko in common_kos]
    common_kos_sorted_indices_pred = list(common_kos_sorted_indices)
    # sort common_kos_sorted_indices_pred from small to large
    common_kos_sorted_indices_pred.sort()
    common_kos_sorted_pred = [sorted_kos_predictions[i] for i in common_kos_sorted_indices_pred]


    # debug
    #print(common_kos_sorted_gt[:10])
    #print(common_kos_sorted_pred[:10])

    #print(sorted_kos_ground_truth[:10])
    #print(sorted_kos_predictions[:10])

    #print(common_kos_sorted_indices_pred[:10])
    #print(common_kos_sorted_indices_gt[:10])

    # compute kendall tau using sorted_kos_ground_truth and most_abundant_kos_list
    tau, p_value = kendalltau(common_kos_sorted_gt, common_kos_sorted_pred)

    # compute the pearson correlation of the ground truth and predictions for common kos
    abund_of_common_kos_in_gt = [gt_ko_to_abund[ko] for ko in common_kos_sorted_gt]
    abund_of_common_kos_in_pred = [pred_ko_to_abund[ko] for ko in common_kos_sorted_pred]
    pearson_corr = np.corrcoef(abund_of_common_kos_in_gt, abund_of_common_kos_in_pred)[0, 1]

    # normalize the abundances of the common kos in the ground truth and predictions
    abund_of_common_kos_in_gt = np.array(abund_of_common_kos_in_gt) / sum(abund_of_common_kos_in_gt)
    abund_of_common_kos_in_pred = np.array(abund_of_common_kos_in_pred) / sum(abund_of_common_kos_in_pred)

    # compute bray-curtis distance of the ground truth and predictions for common kos
    bray_curtis_common = braycurtis(abund_of_common_kos_in_gt, abund_of_common_kos_in_pred)

    # compute the kl divergence of the ground truth and predictions for common kos using scipy.special.rel_entr
    kl_div_common_gt_to_pred = sum( rel_entr(abund_of_common_kos_in_gt, abund_of_common_kos_in_pred) )
    kl_div_common_pred_to_gt = sum( rel_entr(abund_of_common_kos_in_pred, abund_of_common_kos_in_gt) )
    

    # compute what percentage of the ground truth kos are in the predictions using ground truth abundances
    percent_of_gt_in_pred = 0.0
    for ko in ground_truth_kos_set:
        if ko in predicted_kos_set:
            #percent_of_gt_in_pred += min( ground_truth_abundances[ground_truth_kos_list.index(ko)], relative_abundances[sorted_kos_predictions.index(ko)] )
            percent_of_gt_in_pred += ground_truth_abundances[ground_truth_kos_list.index(ko)]

    # compute what percentage of the predictions are in the ground truth using predicted abundances
    percent_of_pred_in_gt = 0.0
    for ko in predicted_kos_set:
        if ko in ground_truth_kos_set:
            #percent_of_pred_in_gt += min( ground_truth_abundances[ground_truth_kos_list.index(ko)], relative_abundances[sorted_kos_predictions.index(ko)] )
            percent_of_pred_in_gt += relative_abundances[sorted_kos_predictions.index(ko)]

    # create a set of all kos in the ground truth and predictions
    all_kos_union = ground_truth_kos_set.union(predicted_kos_set)

    # create a list of abundances for all kos in the ground truth and predictions
    all_kos_abundances_gt = []
    all_kos_abundances_pred = []
    for ko in all_kos_union:
        if ko in ground_truth_kos_set:
            all_kos_abundances_gt.append(gt_ko_to_abund[ko])
        else:
            all_kos_abundances_gt.append(0)
        if ko in predicted_kos_set:
            all_kos_abundances_pred.append(pred_ko_to_abund[ko])
        else:
            all_kos_abundances_pred.append(0)

    # compute pearson corr coeff of these abundances
    pearson_corr_all = np.corrcoef(all_kos_abundances_gt, all_kos_abundances_pred)[0, 1]

    # write as completeness and purity
    completeness = recall
    purity = precision
    weighted_completeness = percent_of_gt_in_pred
    weighted_purity = percent_of_pred_in_gt

    # compute weighted jaccard index
    kos_all = ground_truth_kos_set.union(predicted_kos_set)
    
    value1, value2 = 0.0, 0.0
    for ko in kos_all:
        try:
            v1 = gt_ko_to_abund[ko]
        except:
            v1 = 0

        try:
            v2 = pred_ko_to_abund[ko]
        except:
            v2 = 0

        value1 += min(v1, v2)
        value2 += max(v1, v2)

    weighted_jaccard = value1 / value2

    # compute completeness by limiting ground truth to top 95% abundant KOs
    top_95_kos = set()
    top_abundance_seen = 0.0
    for ko in sorted_kos_ground_truth:
        top_95_kos.add(ko)
        top_abundance_seen += gt_ko_to_abund[ko]
        if top_abundance_seen >= 0.95:
            break

    completeness_top_95 = len(top_95_kos.intersection(predicted_kos_set)) / len(top_95_kos)

    # write headers to output file
    with open(args.output, 'w') as f:
        f.write('purity,completeness,kendalltau,pearsonr_common,pearsonr_all,wt_purity,wt_completeness,kl_div_common_gt_to_pred,kl_div_common_pred_to_gt,bray_curtis,weighted_jaccard,completeness_top_95\n')

    # Write precision, recall, and tau to output file
    with open(args.output, 'a') as f:
        f.write(f'{purity},{completeness},{tau},{pearson_corr},{pearson_corr_all},{weighted_purity},{weighted_completeness},{kl_div_common_gt_to_pred},{kl_div_common_pred_to_gt},{bray_curtis_common},{weighted_jaccard},{completeness_top_95}\n')

if __name__ == '__main__':
    main()