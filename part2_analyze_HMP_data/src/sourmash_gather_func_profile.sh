date
out_dir=$1
single_sig_dir=$2
KEGG_protein_sig=$3


cd ${out_dir}

### scan HMP on KEGG by sourmash gather
run_sourmash_gather() {
 query_file=$1
 ref_db=$2
 k_value=$3
 echo ${query_file}
 
 # pick name
 filename=$(echo ${query_file##*/})
 out_name=$(echo ${filename} | cut -d"_" -f 1-3)
 
 # run gather with time command
 /usr/bin/time -av -o runlog_scale1000_sourmash_gather_k_${k_value}_${out_name}.txt \
  sourmash gather -k ${k_value} -o sourmash_gather_out_scale1000_k_${k_value}_${out_name}.csv \
  -q --protein --threshold-bp 500  ${query_file} ${ref_db}
 unset query_file ref_db k_value filename out_name
}

export -f run_sourmash_gather

for k_value in 11; do
 readlink -f ${single_sig_dir}/*zip | parallel -j 10 run_sourmash_gather {} ${KEGG_protein_sig} ${k_value}
done


mkdir -p single_gather_out
mkdir -p runlog_single_gather
mv runlog_scale1000_sourmash_gather_k_*.txt ./runlog_single_gather
mv sourmash_gather_out_scale1000_k_*.csv ./single_gather_out

date
echo "done"

