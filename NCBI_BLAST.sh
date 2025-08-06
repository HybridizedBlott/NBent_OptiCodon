#!/bin/bash

#makeblastdb -in Genome_dump/Niben101_clean.fasta -dbtype nucl -out Genome_dump/nbent_db

tblastn -query solGenSeqs.fasta -db nbent_db -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore' -max_target_seqs 1 -evalue 1e-10 -out Genome_dump/tblastn_hits.tsv

gffread -w Data/nbent_cdna.fa -g Data/Niben101_clean.fasta Data/Niben101_annotation.gene_models.gff

python map_blast_to_genes.py tblastn_hits.tsv Data/Niben101_annotation.gene_models.gff > top_gene_ids.txt

seqtk subseq Data/nbent_cdna_simple.fa Data/top_genes.txt > Data/top_hit_cdnas.fa