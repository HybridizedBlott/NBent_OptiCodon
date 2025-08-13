# **Optimizing _Nicotiana Benthamiana_ DNA Sequences using Deep Learning**
## Instructions: 
- Create a conda environment using the requirement.txt file:
```
$conda create --name <env_name> --file requirements.txt
```

- Create a text file containing a list of protein id's in the following format:
```
A0A140G1S3
A0A1S3YWG7
A0A140G1S2
```
- Clone repository into your local machine or HPC
- Download **Model** and **Data** folders from [google drive](https://drive.google.com/drive/folders/1bi0z-Ul7bAslzKo4Xs5GWwKgWmphY9Pp?usp=sharing) and move them into cloned repository
- Download the reference _Nicotiana Benthamiana_ genome from the [Sol Genomics Network database version 1.0.1](https://solgenomics.net/ftp/genomes/Nicotiana_benthamiana/assemblies/) into the Data folder.
- Execute the data retrieval script using:
`$bash ProteinPull.sh <protein list file>`

- Quantify and merge the expression rate of sequence with nucleotide sequences:
```
$salmon index -t <location of retrieved nucleotide fasta file> -i <name for index output>
```
```
$salmon index quant -i <index> --validateMappings -l A -1 Data/SRR5691046_1.fastq -2 Data/SRR5691046_2.fastq -o <output name>
```
```
$python expressionMerger.py --input <retrived nucleotide fasta file> --quant <location of quant file> --output <name of expression csv>
```

- For data preprocessing, follow the instructions in the `Model/source/data_preprocessing/README.md` directory
- For model training run the train.sh script: `$bash train_model.sh`, ensure that configurations are set with the deisred hyperparameters
  The config files used for this project can be found in the `Model/configs/win_configs/win75` directory.
- For model evaluation run: `$bash mod_eval.sh`

## Acknowledgments 
I would like to thank [Sidi _et al_, 2024](https://www.pnas.org/doi/10.1073/pnas.2410003121) for providing access to their model for usage in this project. The codebase is accessible from their [repository](https://github.com/siditom-cs/ReverTra/).  
  
I would like to thank the JGM lab for providing the proteomic dataset used for the cururation of the protein list, which was a part of the following [study](https://onlinelibrary.wiley.com/doi/10.1111/pbi.14342). The data is accessible through the [PRIDE database](https://www.ebi.ac.uk/pride/archive/projects/PXD042916).

I would like to thank [Grosse-Holz _et al_ (2018)](https://pubmed.ncbi.nlm.nih.gov/29055088/) for providing accessibility to their RNA-seq fastq data, which was used for sequence quantification.

I would like to thank Plant Form for their collaboration in developing the idea behind this research project. 

Finally, I greatly appreciate the mentorship and support provided by my advisors Ashley Meyers, Dr. Doug Cossar, Dr. Stefen C. Kremer, and Dr. Jennifer Geddes-McAlister. 
## References:
Sidi, T., Bahiri-Elitzur, S., Tuller, T., and Kolodny, R. (2024). Predicting gene sequences with AI to study codon usage patterns. Proceedings of the National Academy of Sciences 122. https://doi.org/10.1073/pnas.2410003121.  
  
Prudhomme, N., Pastora, R., Thomson, S., Zheng, E., Sproule, A., Krieger, J.R., Murphy, J.P., Overy, D.P., Cossar, D., McLean, M.D., et al. (2024). Bacterial growth‐mediated systems remodelling of Nicotiana benthamiana defines unique signatures of target protein production in molecular pharming. Plant Biotechnology Journal 22, 2248–2266. https://doi.org/10.1111/pbi.14342.  

automate web application actions using python — splinter v0.1 documentation https://splinter.readthedocs.io/en/0.1/index.html.  

Python Testing with Selenium SpringerLink. https://link.springer.com/book/10.1007/978-1-4842-6249-8.  

Patro, R., Duggal, G., Love, M.I., Irizarry, R.A., and Kingsford, C. (2017). Salmon provides fast and bias-aware quantification of transcript expression. Nature Methods 14, 417–419. https://doi.org/10.1038/nmeth.4197.

Grosse‐Holz, F., Kelly, S., Blaskowski, S., Kaschani, F., Kaiser, M., and Van Der Hoorn, R.A.L. (2017). The transcriptome, extracellular proteome and active secretome of agroinfiltrated Nicotiana benthamiana uncover a large, diverse protease repertoire. Plant Biotechnology Journal 16, 1068–1084. https://doi.org/10.1111/pbi.12852.
