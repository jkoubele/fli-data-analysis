#!/bin/bash
FASTQ_DATA_FOLDER="/cellfile/datapublic/jkoubele/leibniz_institute_data/FASTQ/20201014_582_KLR/GEX"
OUTPUT_DATA_FOLDER="/cellfile/datapublic/jkoubele/leibniz_institute_data/aligned/20201014_582_KLR/GEX"

for value in O_AL O_DR O_ND O_NR Y_AL Y_DR
do
   mkdir --parents ${OUTPUT_DATA_FOLDER}"/${value}"
   /cellfile/datapublic/jkoubele/STAR_2.7.11a/Linux_x86_64/STAR \
  --runThreadN 16 \
  --soloType CB_UMI_Simple \
  --genomeDir /cellfile/datapublic/jkoubele/STAR_2.7.11a/reference_genomes/GRCm38/STAR_generated_genome \
  --soloCBwhitelist /cellfile/datapublic/jkoubele/STAR_2.7.11a/barcode_white_lists/737K2-orion-dev.txt \
  --soloUMIlen 12 \
  --readFilesIn ${FASTQ_DATA_FOLDER}"/${value}_HSC_RNA_R2.fastq.gz" ${FASTQ_DATA_FOLDER}"/${value}_HSC_RNA_R1.fastq.gz" \
  --readFilesCommand zcat \
  --outFileNamePrefix ${OUTPUT_DATA_FOLDER}"/${value}/" \
  --outSAMtype BAM SortedByCoordinate \
  --outSAMattributes CB UB GX GN \
  --soloUMIfiltering MultiGeneUMI \
  --soloCBmatchWLtype 1MM_multi_pseudocounts \
  --soloFeatures GeneFull
done
