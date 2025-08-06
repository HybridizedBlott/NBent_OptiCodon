import argparse
from Bio import SeqIO
import pandas as pd

parser = argparse.ArgumentParser(description="Merge expression data from multiple files")
parser.add_argument("-f", "--input", type=str, required=True, help="Input Fasta file")
parser.add_argument("-q", "--quant", type=str, required=True, help="Quantification file")
parser.add_argument("-o", "--output", type=str, required=True, help="Output file")

args = parser.parse_args()

fasta_path = args.input 
sequences = {}

for record in SeqIO.parse(fasta_path,"fasta"):
    sequences[record.id] = str(record.seq)


quant_df = pd.read_csv(args.quant, sep='\t')
quant_df['Sequence'] = quant_df['Name'].map(sequences)
result_df = quant_df[['Name','Sequence','TPM']].rename(columns ={'Name':'ids','Sequence':'dna','TPM':'expr'})
result_df.to_csv(args.output, index=False)
