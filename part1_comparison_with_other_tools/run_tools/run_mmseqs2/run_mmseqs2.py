"""
Created the database for the mmseqs2 using the following command:
mmseqs createdb protein_ref_db_giant.faa mmseqdb

Resource usages:
Command being timed: "mmseqs createdb protein_ref_db_giant.faa mmseqdb"
        User time (seconds): 99.52
        System time (seconds): 13.71
        Percent of CPU this job got: 407%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:27.75
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 1676084
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 124
        Minor (reclaiming a frame) page faults: 833659
        Voluntary context switches: 4491
        Involuntary context switches: 946
        Swaps: 0
        File system inputs: 32
        File system outputs: 16574928
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0

Then, created an index of this database using the following command:
Command being timed: "mmseqs createindex mmseqdb tmp"
        User time (seconds): 3961.60
        System time (seconds): 346.19
        Percent of CPU this job got: 11313%
        Elapsed (wall clock) time (h:mm:ss or m:ss): 0:38.07
        Average shared text size (kbytes): 0
        Average unshared data size (kbytes): 0
        Average stack size (kbytes): 0
        Average total size (kbytes): 0
        Maximum resident set size (kbytes): 20571516
        Average resident set size (kbytes): 0
        Major (requiring I/O) page faults: 370
        Minor (reclaiming a frame) page faults: 8455078
        Voluntary context switches: 69934
        Involuntary context switches: 42475
        Swaps: 0
        File system inputs: 0
        File system outputs: 46582584
        Socket messages sent: 0
        Socket messages received: 0
        Signals delivered: 0
        Page size (bytes): 4096
        Exit status: 0


Command using which we can run mmseqs2 (on an already created database) for a metagenome:
1. create a db for the metagenome
command:
mmseqs createdb <metagenome_name> <metagenome_db_name>

2. run mmseqs2 search against the database
command:
mmseqs search <metagenome_db_name> <mmseqdb> <output_name> tmp --threads 64

if we want sensitive mode, then "-s 7.0"
if we want non-sensitive fast mode, then "-s 1.0"

the output format we need to use:
--format-output "TODO"
"""


