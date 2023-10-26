import argparse
from collections import Counter
import re
import pandas as pd

def parse_args():
    parser = argparse.ArgumentParser(description="This script will take one kofamscan outfput filename as input, and generate the KOs present and their abudnances, write it to an output file.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument("kofam_filename", type=str, help="kofamscan filename.")
    parser.add_argument("output_filename", type=str, help="The full path to the KO and abundance filename.")
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_args()
    kofam_filename = args.kofam_filename
    output_filename = args.output_filename

    f = open(kofam_filename, 'r')
    lines = f.readlines()
    f.close()
    stripped_lines = [ line.strip() for line in lines[2:] ]
    kos = [ re.split(r'\s+', stripped_line)[1] for stripped_line in stripped_lines ]
    count_all = len(kos)
    dict = Counter(kos)
    out_list = []
    for ko_id in dict.keys():
        out_list.append( (f'ko:{ko_id}', 1.0*dict[ko_id]/count_all) )

    out_df = pd.DataFrame(out_list, columns=['ko_id', 'abundance'])
    out_df.to_csv( output_filename )
