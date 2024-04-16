# a python wrapper to run diamond, and to record time and memory usage

"""
Diamond ref db was built using the following command:
"diamond makedb --in ../protein_ref_db_giant.faa -d dmnd_ref_db"
Following are the resource usages
	User time (seconds): 964.38
	System time (seconds): 11.57
	Percent of CPU this job got: 4209%
	Elapsed (wall clock) time (h:mm:ss or m:ss): 0:23.18
	Maximum resident set size (kbytes): 1804148
	Minor (reclaiming a frame) page faults: 2226155
	Voluntary context switches: 13003
	Involuntary context switches: 34664
	File system inputs: 6653008
	File system outputs: 6901656
"""

# now, on the GPU machine, the diamond ref db is here:
# /scratch/mbr5797/diamond_protein_ref_index/dmnd_ref_db.dmnd

# diamond running command:
# diamond blastx -q metagenome_1_seed_1.fastq -d /scratch/mbr5797/diamond_protein_ref_index/dmnd_ref_db.dmnd -o test -p 128 --algo 0 --k 1


import subprocess
import argparse
import pandas as pd
import time

def run_diamond(query, db, out, verbose, num_threads = 128, outfmt = 6, algo = 0, evalue = 0.001, sensitive = False, resourceout = None):
    """
    Run diamond with the given parameters. Capture time and memory usages. Return the resource usages.
    """
    cmd = ["/usr/bin/time", "-v", "diamond", "blastx", "-q", query, "-d", db, "-o", out, "-p", str(num_threads), "-e", str(evalue), "--algo", str(algo), '-k', '1']
    if outfmt == 6:
        cmd.append("--outfmt")
        cmd.append("6")
        cmd = cmd + "qseqid qlen sseqid slen bitscore pident nident mismatch".split(" ")
    if sensitive:
        cmd.append("--sensitive")
    if verbose:
        print("Running command: " + " ".join(cmd))
    
    start_time = time.time()

    # check subprocess output
    cmd = " ".join(cmd)
    print(cmd)
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

    # write resource usages as comma separated values in the order:
    # wall time, cpu time, max resident set size, avg resident set size
    if resourceout:
        resourceout = open(resourceout, "w")
        resourceout.write(str(walltime) + "," + str(cpu_time) + "," + str(max_resident_set_size) + "," + str(avg_resident_set_size) + "\n")
        resourceout.close()
    else:
        print("Wall time: " + str(walltime))
        print("CPU time: " + str(cpu_time))
        print("Max resident set size: " + str(max_resident_set_size))
        print("Avg resident set size: " + str(avg_resident_set_size))

    return walltime, cpu_time, max_resident_set_size, avg_resident_set_size



def postprocess(diamond_output, gene_output, ko_output):
    """
    Postprocess the diamond output to get gene and KO relative abudnaces.
    """
    # open gene to ko maping file, store that information in a dictionary
    gene_to_ko_mapping_file = '/scratch/mbr5797/genomes_extracted_from_kegg/present_genes_and_koids.csv'
    gene_to_ko_mapping = pd.read_csv(gene_to_ko_mapping_file, index_col = 0)
    gene_ids = gene_to_ko_mapping['gene_id'].tolist()
    ko_ids = gene_to_ko_mapping['ko_id'].tolist()
    gene_to_ko = dict(zip(gene_ids, ko_ids))
    
    # open diamond output file, get the list of genes, their counts, and the number of nucleotides covered
    # diamond output file is tab separated, with the following columns:
    # qseqid qlen sseqid slen bitscore pident nident mismatch
    # we only need sseqid
    # sseqid format: genome_id:gene_id|genome_id:gene_id|genome_id_sequence_id|sequence_id|gene_start|gene_end
    # we need to extract the gene id
    diamond_output = pd.read_csv(diamond_output, sep = "\t", header = None)
    read_id_list = diamond_output[0].tolist()

    # get the unique read ids
    read_id_list = list(set(read_id_list))

    gene_id_to_num_reads = {}
    gene_id_to_num_nucleotides_covered = {}
    
    read_id_to_bitscore = {}
    read_id_to_pident = {}

    # iterate over all rows in the dataframe
    for _, row in diamond_output.iterrows():
        # get the gene id
        gene_id = row[2].split("|")[0]
        num_matches = row[6]
        bitscore = row[4]
        pident = row[5]
        read_id = row[0]

        if read_id in read_id_to_bitscore.keys():
            if bitscore <= read_id_to_bitscore[read_id]:
                continue
            if pident <= read_id_to_pident[read_id]:
                continue

        read_id_to_bitscore[read_id] = bitscore
        read_id_to_pident[read_id] = pident

        # update the gene id to num reads and num nucleotides covered
        if gene_id not in gene_id_to_num_reads.keys():
            gene_id_to_num_reads[gene_id] = 0
            gene_id_to_num_nucleotides_covered[gene_id] = 0
            
        gene_id_to_num_reads[gene_id] += 1
        gene_id_to_num_nucleotides_covered[gene_id] += num_matches

    # convert number of reads and number of nucleotides covered to relative abundances
    total_reads = sum(gene_id_to_num_reads.values())
    total_nucleotides_covered = sum(gene_id_to_num_nucleotides_covered.values())
    gene_id_to_relative_abundance_by_num_reads = {}
    gene_id_to_relative_abundance_by_nucleotides_covered = {}
    for gene_id in gene_id_to_num_reads.keys():
        gene_id_to_relative_abundance_by_num_reads[gene_id] = gene_id_to_num_reads[gene_id] / total_reads
        gene_id_to_relative_abundance_by_nucleotides_covered[gene_id] = gene_id_to_num_nucleotides_covered[gene_id] / total_nucleotides_covered

    # write gene relative abundances to file
    # header: gene_id, num_reads, num_nucleotides_covered, relative_abundance_by_num_reads, relative_abundance_by_nucleotides_covered
    gene_output = open(gene_output, "w")
    gene_output.write("gene_id,num_reads,num_nucleotides_covered,relative_abundance_by_num_reads,relative_abundance_by_nucleotides_covered\n")
    for gene_id in gene_id_to_num_reads.keys():
        gene_output.write(gene_id + "," + str(gene_id_to_num_reads[gene_id]) + "," + str(gene_id_to_num_nucleotides_covered[gene_id]) + "," + str(gene_id_to_relative_abundance_by_num_reads[gene_id]) + "," + str(gene_id_to_relative_abundance_by_nucleotides_covered[gene_id]) + "\n")    

    # using gene to KO mapping, covert gene relative abundances to KO relative abundances
    ko_to_num_reads = {}
    ko_to_num_nucleotides_covered = {}
    for gene_id in gene_id_to_num_reads.keys():
        ko_id = gene_to_ko[gene_id]
        if ko_id not in ko_to_num_reads.keys():
            ko_to_num_reads[ko_id] = 0
            ko_to_num_nucleotides_covered[ko_id] = 0
        ko_to_num_reads[ko_id] += gene_id_to_num_reads[gene_id]
        ko_to_num_nucleotides_covered[ko_id] += gene_id_to_num_nucleotides_covered[gene_id]

    # convert number of reads and number of nucleotides covered to relative abundances
    total_reads = sum(ko_to_num_reads.values())
    total_nucleotides_covered = sum(ko_to_num_nucleotides_covered.values())
    ko_id_to_relative_abundance_by_num_reads = {}
    ko_id_to_relative_abundance_by_nucleotides_covered = {}
    for ko_id in ko_to_num_reads.keys():
        ko_id_to_relative_abundance_by_num_reads[ko_id] = ko_to_num_reads[ko_id] / total_reads
        ko_id_to_relative_abundance_by_nucleotides_covered[ko_id] = ko_to_num_nucleotides_covered[ko_id] / total_nucleotides_covered

    # store KO rel abundances to files
    # header: ko_id, num_reads, num_nucleotides_covered, relative_abundance_by_num_reads, relative_abundance_by_nucleotides_covered
    ko_output = open(ko_output, "w")
    ko_output.write("ko_id,num_reads,num_nucleotides_covered,relative_abundance_by_num_reads,relative_abundance_by_nucleotides_covered\n")
    for ko_id in ko_to_num_reads.keys():
        ko_output.write(ko_id + "," + str(ko_to_num_reads[ko_id]) + "," + str(ko_to_num_nucleotides_covered[ko_id]) + "," + str(ko_id_to_relative_abundance_by_num_reads[ko_id]) + "," + str(ko_id_to_relative_abundance_by_nucleotides_covered[ko_id]) + "\n")
    

def main():
    parser = argparse.ArgumentParser(description="Run diamond with the given parameters. Database here: /scratch/mbr5797/diamond_protein_ref_index/dmnd_ref_db.dmnd")
    parser.add_argument("query", help="The query file.")
    parser.add_argument("diamondout", help="The output file.")
    parser.add_argument("geneout", help="The gene relative abundance output file.")
    parser.add_argument("koout", help="The KO relative abundance output file.")
    parser.add_argument("resourceout", help="The resource usage output file.")
    parser.add_argument("--algo", help="The algorithm to use. (0=double-indexed/1=query-indexed)", type=int, default=0)
    parser.add_argument("--threads", help="The number of threads to use.", type=int, default=128)
    parser.add_argument("--evalue", help="The evalue to use.", type=float, default=0.001)
    parser.add_argument("--outfmt", help="The output format to use.", type=int, default=6)
    parser.add_argument("--verbose", help="Print more information.", action="store_true")
    parser.add_argument("--sensitive", help="Use sensitive mode.", action="store_true")
    parser.add_argument("--postprocess_only", help="Only postprocess the diamond output.", action="store_true")
    args = parser.parse_args()

    if args.postprocess_only:
        postprocess(args.diamondout, args.geneout, args.koout)
        return

    # run diamond and store resource usages
    db = "/scratch/mbr5797/diamond_protein_ref_index/dmnd_ref_db.dmnd"
    run_diamond(args.query, db, args.diamondout, args.verbose, args.threads, args.outfmt, evalue = args.evalue, sensitive=args.sensitive, resourceout = args.resourceout)
    
    # postprocess the diamond output for gene and ko relative abundances
    postprocess(args.diamondout, args.geneout, args.koout)

if __name__ == "__main__":
    main()