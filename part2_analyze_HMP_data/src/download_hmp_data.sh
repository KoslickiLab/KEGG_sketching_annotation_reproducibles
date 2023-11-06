date
echo "Start downloading files"

target_dir=$1
manifest=$2
metadata=$3

cd ${target_dir}
mkdir -p download
cd download

# merge metadata
paste ${manifest} ${metadata} > ../merged_metadata.tsv

# remove all private records: Private: Data not accessible via the HMP DACC.
echo "Count private data......"
grep "Data not accessible"  ../merged_metadata.tsv | wc -l  # 185
# remove scaffold files (correspond to a fastq file)
echo "Count scaffold data......"
grep '.scaffolds.fa.bz2' ../merged_metadata.tsv | wc -l # 148

# keep files with all depth for now, and check this in data analysis step
grep -v "Data not accessible" ../merged_metadata.tsv  | grep -v '.scaffolds.fa.bz2' | cut -f 3 > ../all_data_file_size_list.txt

# filter data
grep -v "Data not accessible"  ../merged_metadata.tsv  | grep -v '.scaffolds.fa.bz2' > ../hmp_download_list.tsv
echo "validate sample-id match in merged metadata"
awk '$5 != $6' ../hmp_download_list.tsv 

# race dist
cut -f 12 ../hmp_download_list.tsv | sed '1d' | sort | uniq -c | awk '{print $2"\t"$1}' | sort -k2,2rn > ../all_data_race_dist.csv

# subject -> file
# cut -f 8 ../hmp_download_list.tsv | sed '1d' | sort | uniq -c | awk '{print $2"\t"$1}' | sort -k2,2rn | less
# subject -> sample
# cut -f 5,8 ../hmp_download_list.tsv | sed '1d' | sort | uniq -u | cut -f 2 | sort | uniq -c | awk '{print $2"\t"$1}' | sort -k2,2rn | less 
# sample -> file
# cut -f 1,5 ../hmp_download_list.tsv | sed '1d' | sort | uniq -u | cut -f 2 | sort | uniq -c | awk '{print $2"\t"$1}' | sort -k2,2rn | less 


# clean metadata and make a new name for files (too messy)
sed 's/[)(]//g' ../hmp_download_list.tsv | cut -f -5,7,10- | awk -F"\t" 'NR==1{print "f_uid""\t"$0}; NR>1{
 gsub("Healthy Human Subjects","HHS",$10);
 gsub("Inflammatory Bowel Disease Multi-omics Database IBDMDB","IBD",$10);
 gsub("prediabetes","T2D",$10);
 gsub("Human Microbiome Project HMP","HMP",$11);
 gsub("Integrative Human Microbiome Project","ihmp",$11);
print "f"NR-1"_"$11"_"$10"\t"$0}' OFS="\t"  > ../all_data_cleaned_metadata.tsv


# may encounter failed urls, so add this extra step to check
sed 1d ../all_data_cleaned_metadata.tsv | cut -f 1,3,5  > file_2_download.tsv 
input_file=file_2_download.tsv 

date
time_tag=$(date +%h%d_%H%M)
echo -e "f_id\tmd5\tlink" > error_record_${time_tag}.tsv

cat ${input_file} | while read line; do
  # echo "$line"
  file_id=$(echo ${line} | awk '{print $1}')
  md5=$(echo ${line} | awk '{print $2}')
  link=$(echo ${line} | awk '{print $3}' | cut -d"," -f 1)
  default_name=$(echo ${link##*/})
  
  # download
  wget -nv -O ${file_id}_${default_name} ${link}
  
  if [[ "$?" != 0 ]]; then
   echo "Error downloading file"
   rm ${file_id}_${default_name}
   echo -e "${line}\tFailed_download" >>  error_record_${time_tag}.tsv
  fi
done 

rm file_2_download.tsv 
mv error_record_${time_tag}.tsv ../failed_download_record.tsv

# check md5 for all downloaded files
echo -e "f_id\tmeta_md5\tfile_md5" > ../md5_not_match_record.tsv
for file in $(ls -1 ); do
 echo $file
 f_id=$(echo $file | cut -d"_" -f 1-3)
 meta_md5=$(grep $f_id ../all_data_cleaned_metadata.tsv | cut -f 3)
 file_md5=$(md5sum $file | awk '{print $1}')
 [ "$meta_md5" != "$file_md5" ] && echo -e "${file}\t${meta_md5}\t${file_md5}" >> ../md5_not_match_record.tsv
done

# make 2 folders
mkdir md5_not_match
sed '1d' ../md5_not_match_record.tsv | cut -f 1 | xargs mv -t ./md5_not_match

mkdir checked_fq_files
mv f* ./checked_fq_files


echo "Finish downloading"
echo "start time is ${time_tag} (hd_HM)"
echo "end time is: $(date +%h%d_%H%M)"
date

