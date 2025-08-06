import sys

# Usage: python map_blast_to_genes.py tblastn_hits.tsv Data/Niben101_annotation.gene_models.gff > top_gene_ids.txt

def parse_gff(gff_file):
    genes = []
    with open(gff_file) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split('\t')
            if len(parts) < 9:
                continue
            if parts[2] != "gene":
                continue
            chrom = parts[0]
            start = int(parts[3])
            end = int(parts[4])
            info = parts[8]
            # Extract gene ID (adjust regex if needed)
            gene_id = None
            for field in info.split(';'):
                if field.startswith("ID="):
                    gene_id = field.split('=')[1]
                    break
            if gene_id:
                genes.append((chrom, start, end, gene_id))
    return genes

def find_gene(chrom, pos, genes):
    for g_chrom, g_start, g_end, g_id in genes:
        if g_chrom == chrom and g_start <= pos <= g_end:
            return g_id
    return None

def main():
    tblastn_file = sys.argv[1]
    gff_file = sys.argv[2]
    genes = parse_gff(gff_file)
    found_ids = set()
    with open(tblastn_file) as f:
        for line in f:
            if line.startswith("#") or not line.strip():
                continue
            parts = line.strip().split('\t')
            if len(parts) < 10:
                continue
            chrom = parts[1]
            sstart = int(parts[8])
            send = int(parts[9])
            # Use midpoint of hit for mapping
            mid = (sstart + send) // 2
            gene_id = find_gene(chrom, mid, genes)
            if gene_id:
                found_ids.add(gene_id)
    for gid in sorted(found_ids):
        print(gid)

if __name__ == "__main__":
    main()