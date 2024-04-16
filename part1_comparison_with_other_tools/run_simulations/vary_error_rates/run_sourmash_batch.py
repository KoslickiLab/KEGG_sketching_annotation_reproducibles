import subprocess
import time

def main():
    error_rates = [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]
    num_runs = 30

    for error_rate in error_rates:
        # generate all metagenome filenames
        metagenome_files = [ "metagenomes/metagenome_"+str(error_rate)+"_seed_"+str(seed)+".fastq" for seed in range(2, num_runs+2) ]
        
        # run sourmash batch for all these metagenems, using k = 11 and 15
        # command: python ../../run_tools/run_sourmash/run_sourmash_batch_wrapper.py --ksize <k> --threshold 50 --kosig /scratch/mbr5797/KOs_sketched/KOs_sbt_scaled_1000_k_<ksize>.sbt.zip --scaled 1000 --outdir sourmash_batch_output --verbose <metagenomes>
        # also, record time and memory

        start_time = time.time()

        cmd = "/usr/bin/time -v python ../../run_tools/run_sourmash/run_sourmash_batch_wrapper.py --ksize 11 --threshold 50 --kosig /scratch/mbr5797/KOs_sketched/KOs_sbt_scaled_1000_k_11.sbt.zip --scaled 1000 --outdir sourmash_batch_output " + " ".join(metagenome_files)
        print(cmd)
        output = subprocess.check_output(cmd, stderr = subprocess.STDOUT, shell=True)
        output = output.decode("utf-8")
        output = output.split('\n')

        end_time = time.time()
        
        user_time, system_time, max_resident_set_size, avg_resident_set_size = 0, 0, 0, 0
        # iterate the lines in reverse order
        for line in output[::-1]:
            if 'User time' in line:
                user_time = float(line.split(" ")[-1].strip())
                break
            if 'System time' in line:
                system_time = float(line.split(" ")[-1].strip())
            if 'Maximum resident set size' in line:
                max_resident_set_size = float(line.split(" ")[-1].strip())
            if 'Average resident set size' in line:
                avg_resident_set_size = float(line.split(" ")[-1].strip())
        walltime = end_time - start_time
        cpu_time = user_time + system_time

        # write to file: single row: walltime,cputime,maxresident,avgresident
        with open("sourmash_batch_output/sourmash_resource_usage_" + str(error_rate) + "_ksize_11.txt", "w") as f:
            f.write(str(walltime) + "," + str(cpu_time) + "," + str(max_resident_set_size) + "," + str(avg_resident_set_size))

        start_time = time.time()

        cmd = "/usr/bin/time -v python ../../run_tools/run_sourmash/run_sourmash_batch_wrapper.py --ksize 15 --threshold 50 --kosig /scratch/mbr5797/KOs_sketched/KOs_sbt_scaled_1000_k_15.sbt.zip --scaled 1000 --outdir sourmash_batch_output --verbose " + " ".join(metagenome_files)
        print(cmd)
        output = subprocess.check_output(cmd, stderr = subprocess.STDOUT, shell=True)
        output = output.decode("utf-8")

        end_time = time.time()

        print (output)

        user_time, system_time, max_resident_set_size, avg_resident_set_size = 0, 0, 0, 0
        # iterate the lines in reverse order
        for line in output[::-1]:
            if 'User time' in line:
                user_time = float(line.split(" ")[-1].strip())
                break
            if 'System time' in line:
                system_time = float(line.split(" ")[-1].strip())
            if 'Maximum resident set size' in line:
                max_resident_set_size = float(line.split(" ")[-1].strip())
            if 'Average resident set size' in line:
                avg_resident_set_size = float(line.split(" ")[-1].strip())
        walltime = end_time - start_time
        cpu_time = user_time + system_time

        # write to file: single row: walltime,cputime,maxresident,avgresident
        with open("sourmash_batch_output/sourmash_resource_usage_" + str(error_rate) + "_ksize_15.txt", "w") as f:
            f.write(str(walltime) + "," + str(cpu_time) + "," + str(max_resident_set_size) + "," + str(avg_resident_set_size))


        print("Finished error rate: ", error_rate)

if __name__ == '__main__':
    main()