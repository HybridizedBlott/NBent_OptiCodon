input_file = 'nbent_cdna.fa' 
output_file = 'nbent_cdna_clean.fa' 

with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for line in infile:
        if line.startswith('>'):
            parts = line.split()
            parts[0] = parts[0].split('.')[0]
            new_header = " ".join(parts)
            outfile.write(new_header + "\n")
        else:
            outfile.write(line)