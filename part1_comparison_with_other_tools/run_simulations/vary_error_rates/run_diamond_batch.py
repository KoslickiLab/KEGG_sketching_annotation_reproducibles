import subprocess
import time

def main():
    error_rates = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
    num_runs = 30

    for error_rate in error_rates:
        # generate all metagenome filenames
        metagenome_files = [ "metagenomes/metagenome_"+str(error_rate)+"_seed_"+str(seed)+".fastq" for seed in range(2, num_runs+2) ]
        
        # run diamond batch for all these metagenems
        # command: python ../../run_tools/run_diamond/run_diamond_batch.py --threads 128 --diamond_script ../../run_tools/run_diamond/run_diamond.py --output_dir diamond_fast_batch_output <metagenomes>
        # also, record time and memory

        start_time = time.time()

        cmd = "/usr/bin/time -v python ../../run_tools/run_diamond/run_diamond_batch.py --threads 128 --diamond_script ../../run_tools/run_diamond/run_diamond.py --output_dir diamond_fast_batch_output " + " ".join(metagenome_files)
        output = subprocess.check_output(cmd, stderr = subprocess.STDOUT, shell=True)
        output = output.decode("utf-8")
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

        # write to file: single row: walltime,cputime,maxresident,avgresident
        with open("diamond_fast_batch_output/diamond_resource_usage_" + str(error_rate) + ".txt", "w") as f:
            f.write(str(walltime) + "," + str(cpu_time) + "," + str(max_resident_set_size) + "," + str(avg_resident_set_size))

if __name__ == '__main__':
    main()