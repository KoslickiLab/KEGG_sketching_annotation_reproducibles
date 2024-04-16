import argparse
import subprocess
import multiprocessing

# hardcoded item: 
sourmash_running_script = 'absolute-path-to-this-directory/run_sourmash_wrapper.py'

def execute_command(cmd, is_verbose):
    if is_verbose:
        print(cmd)

    p = subprocess.Popen(cmd, shell=True)
    p.wait()

    return p.returncode

def parse_args():
    parser = argparse.ArgumentParser(description="This script will take a metagenome-list (num of arguments is variable) as input. Then, it will invoke sourmash prefetch for every metagenome in the list, generate list of matched KOs, and record them in individual files. Time and memory for every run will also be recorded separately.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ksize", type=int, help="k size", default=7)
    parser.add_argument("--seed", type=int, help="Random seed", default=0)
    parser.add_argument("--threshold", type=int, help="sourmash gather threshold bp", default=50)
    parser.add_argument("--kosig", type=str, help="Full path to the sketch of the KOs")
    parser.add_argument("--scaled", type=int, help="Scale factor, integer.", default=1000)
    parser.add_argument("--outdir", type=str, help="Full path to the output directory")
    parser.add_argument("--verbose", help="Print verbose output", action="store_true")
    parser.add_argument("files", nargs='+', help="Full path to the metagenome files")

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    args = parse_args()

    # get the arguments, and then call run_sourmash_script.py
    ksize = str(args.ksize)
    threshold_bp = str(args.threshold)
    ko_signature_filename = args.kosig
    scaled = str(args.scaled)
    outdir = args.outdir
    is_verbose = args.verbose
    metagenome_files = args.files

    processes_opened = []
    commands_executed = []

    for metagenome_file in metagenome_files:

        # create the gather filename, output filename, metagenome sketch name, and resource usage filename
        # all these files will be created in the outdir
        metagenome_name = metagenome_file.split('/')[-1]
        gather_output_filename = outdir + '/gather_' + metagenome_name + '_k_' + str(ksize)
        ko_abundance_filename = outdir + '/ko_abundances_' + metagenome_name + '_k_' + str(ksize)
        metagenome_signature_name = metagenome_name + '_sketch' + '_k_' + str(ksize)
        metagenome_signature_file = outdir + '/' + metagenome_signature_name
        resource_usage_filename = outdir + '/' + metagenome_name + '_resource_usage' + '_k_' + str(ksize)

        cmd = '/usr/bin/time -v python ' + sourmash_running_script + ' --ksize ' + ksize + ' --threshold ' + threshold_bp + ' --metagenome ' + metagenome_file + ' --kosig ' + ko_signature_filename + ' --scaled ' + scaled
        cmd += ' --gatherfile ' + gather_output_filename + ' --outfile ' + ko_abundance_filename + ' --metagenome_sketch_name ' + metagenome_signature_file + ' --resource ' + resource_usage_filename

        if is_verbose:
            print(cmd)

        # open a thread for this command
        p = multiprocessing.Process(target=execute_command, args=(cmd, is_verbose))
        p.start()
        processes_opened.append(p)
        commands_executed.append(cmd)

    # wait for all processes to finish
    for p in processes_opened:
        p.join()

    exit_codes = [p.exitcode for p in processes_opened]
    for exit_code, command in zip(exit_codes, commands_executed):
        if exit_code != 0:
            print("Error in running the sourmash script for the command: \n" + command)
            exit(1)

    print("All processes finished!")    