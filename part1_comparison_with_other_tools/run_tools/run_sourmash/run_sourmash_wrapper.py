import subprocess
import argparse
import time

# sourmash running script: /scratch/mbr5797/run_camisim/run_tools/run_sourmash/run_sourmash_script.py
# in this script, we will run sourmash gather on the metagenome and the KO sketches
# and record resource usages

def parse_args():
    parser = argparse.ArgumentParser(description="This script will take a metagenome as input. Then, it will use exitsing KO sketches (from KEGG database, using FracMinHash) to identify which KO's are found in the metagenome. Mainly, this script is a python wrapper for sourmash gather.",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--ksize", type=int, help="k size", default=7)
    parser.add_argument("--seed", type=int, help="Random seed", default=0)
    parser.add_argument("--threshold", type=int, help="sourmash gather threshold bp", default=50)
    parser.add_argument("--metagenome", type=str, help="Full path to the metagenome")
    parser.add_argument("--kosig", type=str, help="Full path to the sketch of the KOs")
    parser.add_argument("--gatherfile", type=str, help="Full path to the gather output filename")
    parser.add_argument("--outfile", type=str, help="Full path to the output KO abundance filename")
    parser.add_argument("--scaled", type=int, help="Scale factor, integer.", default=1000)
    parser.add_argument("--metagenome_sketch_name", type=str, help="Name of the metagenome sketch file")

    # resource usage filename
    parser.add_argument("--resource", type=str, help="Full path to the resource usage filename")

    args = parser.parse_args()
    return args

if __name__=='__main__':
    args = parse_args()

    # get the arguments, and then call run_sourmash_script.py
    ksize = str(args.ksize)
    threshold_bp = str(args.threshold)
    metagenome_file = args.metagenome
    metagenome_name = metagenome_file.split('/')[-1]
    ko_signature_filename = args.kosig
    gather_output_filename = args.gatherfile
    ko_abundance_filename = args.outfile
    scaled = str(args.scaled)
    metagenome_signature_name = args.metagenome_sketch_name
    metagenome_signature_file = metagenome_signature_name

    sourmash_running_script = '/scratch/mbr5797/run_camisim/run_tools/run_sourmash/run_sourmash_script.py'
    cmd = '/usr/bin/time -v python ' + sourmash_running_script + ' --ksize ' + ksize + ' --threshold ' + threshold_bp + ' --metagenome ' + metagenome_file + ' --kosig ' + ko_signature_filename + ' --gatherfile ' + gather_output_filename + ' --outfile ' + ko_abundance_filename + ' --scaled ' + scaled + ' --metagenome_sketch_name ' + metagenome_signature_name

    start_time = time.time()

    # redirect stderr to STDOUT, and call the cmd using subprocess.check_output
    output = subprocess.check_output(cmd, stderr = subprocess.STDOUT, shell=True)
    output = output.decode("utf-8")
    #print(output)
    output = output.split('\n')

    end_time = time.time()

    # user time is at line 23 from the bottom
    # system time is at line 22 from the bottom
    # maximum resident set size is at line 15 from the bottom
    # average resident set size is at line 14 from the bottom
    # cpu time is the sum of user time and system time
    
    user_time = float(output[-23].split(" ")[-1].strip())
    system_time = float(output[-22].split(" ")[-1].strip())
    cpu_time = user_time + system_time
    max_resident_set_size = float(output[-15].split(" ")[-1].strip())
    avg_resident_set_size = float(output[-14].split(" ")[-1].strip())
    walltime = end_time - start_time

    # write resource usages as comma separated values in the order:
    # wall time, cpu time, max resident set size, avg resident set size
    if args.resource:
        resourceout = open(args.resource, "w")
        resourceout.write(str(walltime) + "," + str(cpu_time) + "," + str(max_resident_set_size) + "," + str(avg_resident_set_size) + "\n")
        resourceout.close()
    else:
        print("Wall time: " + str(walltime))
        print("CPU time: " + str(cpu_time))
        print("Max resident set size: " + str(max_resident_set_size))
        print("Avg resident set size: " + str(avg_resident_set_size))