"""
In this script, we will run diamond in batch mode.
This involves taking many files as argument, and then
invoking run_diamond.py on each of them.

This script will take all arguments that are taken by run_diamond.py
Except for the input file, which will be taken from the list of files.
Additionally, it will take an output directory, where the output files
will be stored.

Also, this script will take a number of threads to run on, and will
run every diamond job using that many threads.
"""

import os
import sys
import subprocess
import argparse
import logging
import time
import shutil

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run diamond in batch. Database here: /scratch/mbr5797/diamond_protein_ref_index/dmnd_ref_db.dmnd")
    parser.add_argument("--algo", help="The algorithm to use. (0=double-indexed/1=query-indexed)", type=int, default=0)
    parser.add_argument("--threads", help="The number of threads to use.", type=int, default=128)
    parser.add_argument("--evalue", help="The evalue to use.", type=float, default=0.001)
    parser.add_argument("--outfmt", help="The output format to use.", type=int, default=6)
    parser.add_argument("--verbose", help="Print more information.", action="store_true")
    parser.add_argument("--sensitive", help="Use sensitive mode.", action="store_true")
    parser.add_argument("--postprocess_only", help="Only postprocess the diamond output.", action="store_true")
    parser.add_argument("--diamond_script", help="The script that runs diamond.", required=True)
    parser.add_argument("--output_dir", help="The output directory.", required=True)
    parser.add_argument("files", help="The files to run diamond on.", nargs='+')
    args = parser.parse_args()

    # iterate over all input files
    for file in args.files:
        # create diamond output file name
        diamond_output_filename = "diamond_output_" + os.path.basename(file)
        output_file = os.path.join(args.output_dir, diamond_output_filename)

        # create gene results filename
        gene_results_filename = "diamond_gene_results_" + os.path.basename(file)
        gene_results_file = os.path.join(args.output_dir, gene_results_filename)

        # create ko results filename
        ko_results_filename = "diamond_ko_results_" + os.path.basename(file)
        ko_results_file = os.path.join(args.output_dir, ko_results_filename)

        # create resource usage filename
        resource_usage_filename = "diamond_resource_usage_" + os.path.basename(file)
        resource_usage_file = os.path.join(args.output_dir, resource_usage_filename)

        # create the command
        command = ["python", args.diamond_script, "--algo", str(args.algo), "--threads", str(args.threads), "--evalue", str(args.evalue), "--outfmt", str(args.outfmt), file, output_file, gene_results_file, ko_results_file, resource_usage_file]
        if args.verbose:
            command.append("--verbose")
        if args.sensitive:
            command.append("--sensitive")
        if args.postprocess_only:
            command.append("--postprocess_only")

        # run the command
        try:
            res = subprocess.run(command) 
        except subprocess.CalledProcessError as e:
            logging.error("Failed to run diamond on file: " + file)
            logging.error("Command: " + " ".join(command))
            output = e.output.decode("utf-8").split('\n')
            logging.error("Error: " + output)
            continue

        # check that the process completed successfully
        if res.returncode != 0:
            logging.error("Failed to run diamond on file: " + file)
            logging.error("Command: " + " ".join(command))
            logging.error("Output:\n" + res.stdout)