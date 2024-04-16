import argparse
import datetime
import configparser
import subprocess
import os
import pysam
import pandas as pd
import gzip

# hardcoded items
camisim_path = 'path-to-camisim-repo/metagenomesimulation.py'
kegg_genomes_directory = 'path-to-required-files-from-zenodo/genomes_extracted_from_kegg'
gene_to_ko_mapping_filename = 'path-to-downloaded-files-from-zenodo/present_genes_and_koids.csv'
sample_config_filename = 'path-to-this-repo/sample_config.ini'
metadata_filename = 'path-to-this-repo/metadata.tsv'
genome_to_id_filename = 'path-to-this-repo/genome_to_id.tsv'


def get_kegg_genome_mapping_filename(kegg_genome_name):
    return kegg_genomes_directory + '/' + kegg_genome_name + '/' + kegg_genome_name + '_mapping.csv'

def get_bam_filename(outdir, simulation_directory_name, genome_name):
    return outdir + '/' + simulation_directory_name + '/bam/' + genome_name + '.bam'

def get_fastq_filenames(outdir, simulation_directory_name, genome_name):
    return outdir + '/' + simulation_directory_name + '/reads/' + genome_name + '1.fq.gz', outdir + '/' + simulation_directory_name + '/reads/' + genome_name + '2.fq.gz'

def main():
    # parse arguments
    description = """
    This script runs camisim with the given number of genomes, 
    and then converts the bam files to ground truth files. Finally,
    it merges the fastq files into a single file.
    Inputs: \n
    - number of genomes to simulate (int) \n
    - config file (will be written by this script, and used by camisim) (str) \n
    - seed for simulations (int) \n
    - output directory for camisim (str) \n
    - size of the file in Gbp (float) \n
    - gene ground truth filename (str) \n
    - ko ground truth filename (str) \n
    - merged metagenome filename (str) \n
    - genome coverage filename (str) \n
    Usage example: python run_camisim.py 10 --config config_seed_0_size_0.1.ini --seed 0 --outdir ./out_seed_0_size_0.1 --size 0.1 --gene_g_t gene_ground_truth_seed_0_size_0.1.csv --ko_g_t ko_ground_truth_seed_0_size_0.1.csv --metagenome_filename metagenome_seed_0_size_0.1.fastq --genome_cov_file genome_coverages_seed_0_size_0.1.csv"""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('number_of_genomes', type=int, help='Number of genomes')
    parser.add_argument('--config', type=str, help='Config file (output of this script)', default='./config.ini')
    parser.add_argument('--seed', type=int, help='Seed used in simulation', default=0)
    parser.add_argument('--outdir', type=str, help='Output directory for camisim', default='./out')
    parser.add_argument('--size', type=float, help='Size of the file in Gbp', default=0.1)
    parser.add_argument('--gene_g_t', type=str, help='Ground truth file (Output)', default='./gene_ground_truth.csv')
    parser.add_argument('--ko_g_t', type=str, help='Ground truth file (Output)', default='./ko_ground_truth.csv')
    parser.add_argument('--metagenome_filename', type=str, help='Metagenome filename (Output)', default='./metagenome.fastq')
    parser.add_argument('--genome_cov_file', help='file where the genome coverages are written (Output)', default='./genome_coverages.csv')
    parser.add_argument('-t', '--max_proc', type=int, help='Maximum number of processes to use', default=128)
    parser.add_argument('-e', '--error_rate', type=float, help='Error rate to use in the simulation', default=0.00)
    parser.add_argument('-n', '--type_name', type=str, help='Name type of read simulator', default='ART-Illumina')
    parser.add_argument('-v', '--num_novel', type=int, help='Number of novel genomes to add', default=0)
    args = parser.parse_args()

    # read the arguments
    number_of_genomes = args.number_of_genomes
    number_of_novel_genomes = args.num_novel
    number_of_real_genomes = max(number_of_genomes - number_of_novel_genomes, 0)
    if args.config:
        config_filename = args.config
    else:
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        config_filename = 'config_' + timestamp + '.ini'
    seed = args.seed
    outdir = args.outdir
    size = args.size
    gene_ground_truth_filename = args.gene_g_t
    ko_ground_truth_filename = args.ko_g_t
    max_processors = args.max_proc
    error_rate = args.error_rate
    type_name = args.type_name

    # read the sample config file
    config = configparser.ConfigParser()
    config.read(sample_config_filename)

    # update the num_genomes field with the command line argument
    # section: Main
    config.set('Main', 'seed', str(seed))
    config.set('Main', 'output_directory', outdir)
    config.set('Main', 'max_processors', str(max_processors))

    # section: ReadSimulator
    config.set('ReadSimulator', 'size', "{:1.11f}".format(size))
    if type_name == 'wgsim':
        config.set('ReadSimulator', 'type', 'wgsim')
        config.set('ReadSimulator', 'profile', str(error_rate))
        config.set('ReadSimulator', 'readsim', '/home/grads/mbr5797/camisim/CAMISIM-1.3/tools/wgsim/wgsim')

    # section: community0
    config.set('community0', 'genomes_total', str(number_of_genomes))
    config.set('community0', 'genomes_real', str(number_of_real_genomes))
    config.set('community0', 'metadata', metadata_filename)
    config.set('community0', 'id_to_genome_file', genome_to_id_filename)

    # write the updated config to the config filename
    with open(config_filename, 'w') as config_file:
        config.write(config_file)

    # run camisim
    subprocess.run(['rm', '-rf', outdir])
    subprocess.run(['mkdir', outdir])
    cmd = f'python {camisim_path} -seed {seed} -id KL -p 4 {config_filename}'
    print(cmd)
    subprocess.run(cmd.split(' '))

    # find the simulation directory name
    for directory in os.listdir(outdir):
        if 'sample' in directory:
            simulation_directory_name = directory
            break

    ######################################################################
    # locate the bam files, then convert to a ground truth at gene level #
    ######################################################################
    # find the genomes that have been used in the simulation
    source_genomes_directory = outdir + '/source_genomes'
    genome_names_used_in_simulation = []
    filenames = os.listdir(source_genomes_directory)
    for filename in filenames:
        if filename.endswith('.fasta') or filename.endswith('.fna'):
            genome_names_used_in_simulation.append(filename.split('.')[0])

    # records to keep for each gene
    # gene name, and num of reads that mapped to it
    gene_name_to_num_reads_dict = {}
    gene_name_mean_coverage_dict = {}
    gene_name_to_median_coverage_dict = {}
    gene_name_to_num_nucleotides_covered_dict = {}

    # go into the kegg genomes directory and ensure that mapping files exist for all the genomes used in the simulation
    for used_genome_name in genome_names_used_in_simulation:
        # get the file names
        mapping_filename = get_kegg_genome_mapping_filename(used_genome_name)
        bam_filename = get_bam_filename(outdir, simulation_directory_name, used_genome_name)
        
        # check that the files exist
        assert os.path.exists(mapping_filename)
        assert os.path.exists(bam_filename)
    
    # go into the kegg genomes directory and find the corresponding mapping files
    for used_genome_name in genome_names_used_in_simulation:
        # get the file names
        mapping_filename = get_kegg_genome_mapping_filename(used_genome_name)
        bam_filename = get_bam_filename(outdir, simulation_directory_name, used_genome_name)

        # read the bam file using pysam
        bamfile = pysam.AlignmentFile(bam_filename, "rb")

        # read the mapping file as a pandas dataframe
        mapping_df = pd.read_csv(mapping_filename)
        
        # iterate over gene_name, contig_id, start and end positions
        gene_name_list = mapping_df['gene_name'].tolist()
        contig_id_list = mapping_df['contig_id'].tolist()
        start_position_list = mapping_df['start_position'].tolist()
        end_position_list = mapping_df['end_position'].tolist()
        
        for gene_name, contig_id, start_position, end_position in zip(gene_name_list, contig_id_list, start_position_list, end_position_list):
            # for each gene, query the bam file using these intervals and the contig id
            list_of_matches = list(bamfile.fetch(contig_id, start_position, end_position))
            
            # record the matches that have been found in the bam file
            num_reads_in_this_gene = len(list_of_matches)
            if num_reads_in_this_gene == 0:
                continue
            gene_name_to_num_reads_dict[gene_name] = num_reads_in_this_gene

            # record the mean and coverage of this gene
            coverage_list = [ pileupcolumn.n for pileupcolumn in bamfile.pileup(contig_id, start_position, end_position) ]
            num_nucleotides_covered = len(coverage_list)

            # calculate num zeros: gene length - num nucleotides covered
            gene_length = end_position - start_position + 1
            if gene_length < 0:
                gene_length = -gene_length
            num_zeros = gene_length - num_nucleotides_covered
            
            # add zeros to the coverage list
            coverage_list += [0] * num_zeros
            
            gene_name_mean_coverage_dict[gene_name] = sum(coverage_list) / len(coverage_list)
            gene_name_to_median_coverage_dict[gene_name] = sorted(coverage_list)[len(coverage_list) // 2]
            gene_name_to_num_nucleotides_covered_dict[gene_name] = num_nucleotides_covered

    # convert the gene level ground truth to relative abundance
    total_num_reads = sum(gene_name_to_num_reads_dict.values())
    total_num_nts_in_reads = sum(gene_name_to_num_nucleotides_covered_dict.values())
    total_mean_cov = sum(gene_name_mean_coverage_dict.values())
    total_med_cov = sum(gene_name_to_median_coverage_dict.values())

    gene_name_to_rel_abund_by_num_reads_dict = {}
    gene_name_to_rel_abund_by_num_nts_dict = {}
    gene_name_to_rel_abund_by_mean_cov_dict = {}
    gene_name_to_rel_abund_by_med_cov_dict = {}

    for gene_name in gene_name_to_num_reads_dict.keys():
        gene_name_to_rel_abund_by_num_reads_dict[gene_name] = gene_name_to_num_reads_dict[gene_name] / (1.0*total_num_reads)
        gene_name_to_rel_abund_by_num_nts_dict[gene_name] = gene_name_to_num_nucleotides_covered_dict[gene_name] / (1.0*total_num_nts_in_reads)
        gene_name_to_rel_abund_by_mean_cov_dict[gene_name] = gene_name_mean_coverage_dict[gene_name] / (1.0*total_mean_cov)
        gene_name_to_rel_abund_by_med_cov_dict[gene_name] = gene_name_to_median_coverage_dict[gene_name] / (1.0*total_med_cov)

    # store the gene level information as ground truth
    with open(gene_ground_truth_filename, 'w') as ground_truth_file:
        ground_truth_file.write('gene_name,mean_coverage,median_coverage,num_nts_covered,num_reads_in_gene\n')
        for gene_name in gene_name_to_num_reads_dict.keys():
            ground_truth_file.write(f'{gene_name},{gene_name_to_rel_abund_by_mean_cov_dict[gene_name]},{gene_name_to_rel_abund_by_mean_cov_dict[gene_name]},{gene_name_to_rel_abund_by_num_nts_dict[gene_name]},{gene_name_to_rel_abund_by_num_reads_dict[gene_name]}\n')
    
    ###########################################################
    # use gene to ko mapping to get the ko level ground truth #
    ###########################################################
            
    # read the gene to ko mapping file
    genes_to_kos_df = pd.read_csv(gene_to_ko_mapping_filename)
    gene_name_to_ko_id_dict = {}
    gene_name_list = genes_to_kos_df['gene_id'].tolist()
    ko_id_list = genes_to_kos_df['ko_id'].tolist()
    for gene_name, ko_id in zip(gene_name_list, ko_id_list):
        gene_name_to_ko_id_dict[gene_name] = ko_id
    
    ko_abundances_by_num_reads = {}
    ko_abundances_by_num_nts_in_reads = {}
    ko_abundances_by_mean_cov = {}
    ko_abundances_by_med_cov = {}

    # iterate over the genes
    for gene_name in gene_name_to_num_reads_dict.keys():
        koid = gene_name_to_ko_id_dict[gene_name]
        num_reads = gene_name_to_num_reads_dict[gene_name]
        num_nts_in_reads = gene_name_to_num_nucleotides_covered_dict[gene_name]
        mean_cov = gene_name_mean_coverage_dict[gene_name]
        med_cov = gene_name_to_median_coverage_dict[gene_name]

        # update the ko abundances
        if koid not in ko_abundances_by_num_reads:
            ko_abundances_by_num_reads[koid] = 0
        ko_abundances_by_num_reads[koid] += num_reads

        if koid not in ko_abundances_by_num_nts_in_reads:
            ko_abundances_by_num_nts_in_reads[koid] = 0
        ko_abundances_by_num_nts_in_reads[koid] += num_nts_in_reads

        if koid not in ko_abundances_by_mean_cov:
            ko_abundances_by_mean_cov[koid] = 0
        ko_abundances_by_mean_cov[koid] += mean_cov

        if koid not in ko_abundances_by_med_cov:
            ko_abundances_by_med_cov[koid] = 0
        ko_abundances_by_med_cov[koid] += med_cov

    # convert to relative abundance
    total_num_reads = sum(ko_abundances_by_num_reads.values())
    total_num_nts_in_reads = sum(ko_abundances_by_num_nts_in_reads.values())
    total_mean_cov = sum(ko_abundances_by_mean_cov.values())
    total_med_cov = sum(ko_abundances_by_med_cov.values())

    for koid in ko_abundances_by_num_reads.keys():
        ko_abundances_by_num_reads[koid] /= (1.0*total_num_reads)
        ko_abundances_by_num_nts_in_reads[koid] /= (1.0*total_num_nts_in_reads)
        ko_abundances_by_mean_cov[koid] /= (1.0*total_mean_cov)
        ko_abundances_by_med_cov[koid] /= (1.0*total_med_cov)

    # write the ko level ground truth
    with open(ko_ground_truth_filename, 'w') as ground_truth_file:
        ground_truth_file.write('ko_id,abund_by_num_reads,abund_by_num_nts,abund_by_mean_cov,abund_by_med_cov\n')
        for koid in ko_abundances_by_num_reads.keys():
            ground_truth_file.write(f'{koid},{ko_abundances_by_num_reads[koid]},{ko_abundances_by_num_nts_in_reads[koid]},{ko_abundances_by_mean_cov[koid]},{ko_abundances_by_med_cov[koid]}\n')
    
    # write the metagenome file by merging the fq.gz files in the reads directory under the simulation directory
    # get the filenames
    fastq_filenames = []
    for genome_name in genome_names_used_in_simulation:
        names = get_fastq_filenames(outdir, simulation_directory_name, genome_name)
        fastq_filenames.append(names[0])
        fastq_filenames.append(names[1])

    # merge the files
    with open(args.metagenome_filename, 'w') as outfile:
        for fname in fastq_filenames:
            # open the gzipped file, read all the lines, and write to the outfile
            with gzip.open(fname, 'r') as infile:
                for line in infile:
                    outfile.write(line.decode('ascii'))

    # go into bam directory, open bam files, calculate coverages, and write to a csv file
    with open(args.genome_cov_file, 'w') as genome_cov_file:
        genome_cov_file.write('genome_name,mean_coverage,median_coverage\n')
        for genome_name in genome_names_used_in_simulation:
            bam_filename = get_bam_filename(outdir, simulation_directory_name, genome_name)
            bamfile = pysam.AlignmentFile(bam_filename, "rb")

            # get coverage list
            coverage_list = [ pileupcolumn.n for pileupcolumn in bamfile.pileup() ]

            # get reference names
            reference_names = bamfile.references

            # calculate total genome length by adding all reference lengths
            genome_length = 0
            for reference_name in reference_names:
                genome_length += bamfile.get_reference_length(reference_name)

            # calculate num zeros: genome length - num nucleotides covered
            num_nucleotides_covered = sum(coverage_list)
            num_zeros = genome_length - num_nucleotides_covered

            # add zeros to the coverage list
            coverage_list += [0] * num_zeros

            genome_cov_file.write(f'{genome_name},{sum(coverage_list) / len(coverage_list)},{sorted(coverage_list)[len(coverage_list) // 2]}\n')

if __name__ == '__main__':
    main()