date

single_file_dir=$1
target_dir=$2
cd ${target_dir}

###### 1658 tar file: files inside are *.fastq.gz and *.txt.bz2 files. We need to untar first and merge into one file to create single signatures
# besides, gz files have just 2 lines but bz2 files have 3 lines (1st line is ./) so need to truncate it

process_only_tar_sourmash ()
{
 tar_file=$1
 scaleFactor=$2
 filename=$(echo ${tar_file##*/})
 out_name=$(echo ${filename} | cut -d"_" -f 1-3)
 tar -xvf ${tar_file} > temp_file_${out_name}.txt
 # delete row with "./"
 grep -v "^./$" temp_file_${out_name}.txt > temp_${out_name} && mv temp_${out_name} temp_file_${out_name}.txt
 # there are 2 files: either fastq.gz or txt.bz2
 format=$(head -1 temp_file_${out_name}.txt | rev | cut -d"." -f 1 | rev)
 for file in $(cat temp_file_${out_name}.txt); do
  cat ${file} >> merged_${out_name}.${format}
  rm ${file}
 done
 # run sourmash
 /usr/bin/time -av -o runlog_scale_${scaleFactor}_${filename}.txt sourmash sketch translate -p protein,k=11,abund,scaled=${scaleFactor} -o ${out_name}_scale_${scaleFactor}.sig.zip merged_${out_name}.${format}
 # clean temp files
 rm merged_${out_name}.${format} temp_file_${out_name}.txt
 unset tar_file filename out_name format 
}

export -f process_only_tar_sourmash

ls ${single_file_dir}/*.tar && readlink -f ${single_file_dir}/*.tar | parallel -P 10 process_only_tar_sourmash {} 1000



########### 562 tar.bz2 file: files inside are stored in a folder
echo "tar.bz2 records" > file_note_all_bz2.txt
echo -e "f_id\tfolder_name" > error_records.txt

process_tarbz_sourmash ()
{
 tar_bz_file=$1
 scaleFactor=$2
 filename=$(echo ${tar_bz_file##*/})
 out_name=$(echo ${filename} | cut -d"_" -f 1-3)
 tar -xvf ${tar_bz_file} > temp_file_${out_name}.txt
 # 1st line is folder
 format=$(sed -n '2p' temp_file_${out_name}.txt | rev | cut -d"." -f 1 | rev)
 # merge reads into 1 file
 for file in $(sed '1d' temp_file_${out_name}.txt); do
   cat ${file} >> merged_${out_name}.${format}
   rm ${file}
 done
 # check if folder become empty after merging
 dirname=$(sed -n '1p' temp_file_${out_name}.txt)
 rmdir ${dirname} || echo -e "${out_name}\t${dirname}" >> error_records.txt  
 # run sourmash
 /usr/bin/time -av -o runlog_scale_${scaleFactor}_${filename}.txt sourmash sketch translate -p protein,k=11,abund,scaled=${scaleFactor} -o ${out_name}_scale_${scaleFactor}.sig.zip merged_${out_name}.${format}
 # clean temp files
 echo ${out_name} >> file_note_all_bz2.txt
 cat temp_file_${out_name}.txt >> file_note_all_bz2.txt
 rm temp_file_${out_name}.txt merged_${out_name}.${format}
 unset tar_bz_file scaleFactor filename out_name dirname format
}

export -f process_tarbz_sourmash

# we can optimize the function by fixing the scalefactor into it. So don't need to generate merged data twice. Keep current we in case we need more scaleFactor
ls ${single_file_dir}/*.tar.bz2 && readlink -f ${single_file_dir}/*.tar.bz2 | parallel -P 10 process_tarbz_sourmash {} 1000






############# 300 fastq.gz file
process_fqgz_sourmash ()
{
 fq_gz_file=$1
 scaleFactor=$2
 filename=$(echo ${fq_gz_file##*/})
 out_name=$(echo ${filename} | cut -d"_" -f 1-3)
 /usr/bin/time -av -o runlog_scale_${scaleFactor}_${filename}.txt sourmash sketch translate -p protein,k=11,abund,scaled=${scaleFactor} -o ${out_name}_scale_${scaleFactor}.sig.zip ${fq_gz_file}
 unset fq_gz_file filename out_name
}

export -f process_fqgz_sourmash

ls ${single_file_dir}/*.fastq.gz && readlink -f ${single_file_dir}/*.fastq.gz | parallel -P 10 process_fqgz_sourmash {} 1000



############# remove data in trouble: failed sketching
mkdir failed_sketch

for file in $(grep exit runlog*.txt); do
 name=$(echo ${file} | cut -d"_" -f 4-6)
 mv ${file} ./failed_sketch
 mv ${name}*.zip ./failed_sketch
done


mkdir -p scale_1000_protein
mv *_scale_1000.sig.zip ./scale_1000_protein
mv runlog_scale_1000*.txt ./scale_1000_protein


date
echo "skeching step done"


