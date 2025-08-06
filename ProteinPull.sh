#!/bin/bash

file=$1 #newline-delimited text file with list of protein ids used in UniProt database

#for loop that extracts fasta sequences using UniProt REST API

for pro in `cat $file`; 
    do echo "Fetching $pro"
    curl -s "https://rest.uniprot.org/uniprotkb/$pro.fasta" >> uniprot_sequences.fasta
    done


echo "Fasta Retrieval Complete!"

#Python script for automating tblastn operation on Sol Genomics Network Nicotiana database

echo "Sol Genomics Network BLAST Search"
python3 SolGenPull.py -f uniprot_sequences.fasta -o solGenSeqs.fasta -t 4
awk '/^>/ {match($1, /(Niben101Scf[0-9]+)/, arr); print ">" arr[1]} !/^>/ {print}' solGenSeqs.fasta > Sol_Seqs_simple.fasta

echo "NCBI BLAST Search using Sol Genomics Network genome 1.1.0"
bash NCBI_BLAST.sh

echo "Combining Results"
cat Sol_Seqs_simple.fasta >> combined_results.fasta
cat top_hit_cdnas.fasta >> combined_results.fasta

seqkit rmdup -s < combined_results.fasta > combined_results_clean.fasta

echo "Retrieval Job Complete"