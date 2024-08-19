# Methods_PPINs_GRNs_nets

## Introduction to Gene Regulatory Networks and Protein-Protein Networks

### Gene Regulatory Networks (GRNs)

Gene Regulatory Networks (GRNs) are complex networks that depict the regulatory relationships between genes and the proteins they encode. These networks illustrate how genes interact with each other and with various molecular signals to control gene expression. In a GRN, nodes represent genes, while edges indicate regulatory interactions, such as activation or repression.

### Protein-Protein Networks (PPNs)

Protein-Protein Networks (PPNs) focus on the interactions between proteins within a cell. These networks are essential for understanding cellular functions, as proteins often work together in complexes to perform biological tasks. In a PPN, nodes represent proteins, and edges denote physical or functional interactions between them. Analyzing PPNs helps researchers identify key protein interactions contributing to various cellular processes, including signaling pathways, metabolic processes, and disease mechanisms.

GRNs.py

Overview
GRNs.py script is designed for analyzing protein-protein associations in a dataset of NCI, AD, carriers and non-carriers of allele 4 of ApoE gene. It employs statistical methods, including bootstrap sampling to identify significant associations between proteins in patients.

Dependencies
This script requires the following Python libraries:
pandas
numpy
scipy
statsmodels

Make sure to install these libraries before running the script.

Input Data

The script reads data from CSV files. The main input file is:
valores_concatenados_apoe_carriers.csv: Contains protein association data for carriers.
Additionally, it utilizes another CSV file for AD individuals:
df_frecuencias_iteraciones-bootstrap_non-carriers.csv: Contains protein association data for non-carriers.

Script Workflow

Data Loading: The script begins by loading the CSV file containing the data for carriers into a pandas DataFrame.
Association Extraction: It extracts all unique protein-protein associations from the DataFrame.
A new DataFrame is created to indicate the presence (1) or absence (0) of each association across different samples.
Bootstrap Sampling:
The script performs bootstrap sampling to estimate the frequency of each association.
It iteratively selects random samples and counts how often each association appears, storing results in a DataFrame.
Chi-Square Testing:
After calculating frequencies, the script prepares data for chi-square tests to compare associations between sick and healthy individuals.
It creates contingency tables and performs chi-square tests to identify significant differences in associations.
Multiple Testing Correction:
The script applies corrections for multiple testing (e.g., Bonferroni correction) to control the false discovery rate.
Output:
Results, including significant associations and their corrected p-values, are saved to CSV files for further analysis.
Usage
To run the script, ensure that the required CSV files are in the specified paths. Execute the script using Python:
bash
python Nuevo_GRNs_carriers_enfermos_CHIsquare.py

Output Files
The script generates the following output files:
df_frecuencias_iteraciones-bootstrap_carriers.csv: Contains the bootstrap frequencies for associations in sick carriers.
asociaciones_significativas_fdr.csv: Lists significant associations after applying FDR correction.
asociaciones_significativas_fdr-CHIsquare.csv: Contains significant associations with chi-square statistics and corrected p-values.
Conclusion
This script provides a comprehensive analysis of protein associations in a dataset of carriers and non-carriers, utilizing statistical methods to identify significant differences. It is a valuable tool for researchers studying the implications of protein interactions in health and disease.

PPNs-AJM_NCI-AD.py
Overview
The Nuevo_PPNs-AJM_NCI-AD.py script is designed for the analysis of protein-protein networks in patients with Alzheimer's Disease (AD) and controls. It processes interaction data, performs bootstrap sampling, and identifies significant protein associations, providing insights into the underlying biological mechanisms of the disease.
Dependencies
This script requires the following Python libraries:
pandas
numpy
re
glob
Ensure these libraries are installed in your Python environment before executing the script.
Input Data
The script expects the following input files:
ROSMAP-Trait_ordenado.txt: Contains patient traits, including specimenID, cogdx, and apoe_genotype.
CSV files containing protein interaction data, named in the format red_pp_{specimenID}_*_expscore_01-dbscore01.csv, located in a specified directory.
Script Workflow
Data Preparation:
Load the ROSMAP-Trait_ordenado.txt file into a pandas DataFrame.
Extract specimenID and cogdx values into separate lists for patients diagnosed with NCI (cogdx = 1.0) and AD (cogdx = 4.0).
File Loading:
Use the extracted specimenID to recursively load relevant protein interaction CSV files from a specified directory.
Data Concatenation:
Create DataFrames to concatenate protein interaction data for both NCI and AD patients.
Protein Association Extraction:
Identify all unique protein associations from the concatenated DataFrames for both groups.
Create a new DataFrame to indicate the presence (1) or absence (0) of each association across samples.
Bootstrap Sampling:
Perform bootstrap sampling on the DataFrames for both patient groups to estimate the frequency of protein associations.
Each bootstrap sample consists of randomly selecting a specified number of samples with replacement.
Frequency Calculation:
Calculate the frequency of each protein association across bootstrap samples.
Identify associations that appear in at least 80% of the bootstrap samples as significant.
Output:
Save the concatenated DataFrames and significant associations to CSV files for further analysis.
Usage
To run the script, ensure that the input files are in the specified paths. Execute the script using Python:
bash
python Nuevo_PPNs-AJM_NCI-AD.py

Output Files
The script generates the following output files:
valores_concatenados_NCI.csv: Contains concatenated protein interaction data for NCI patients.
valores_concatenados_AD.csv: Contains concatenated protein interaction data for AD patients.
Additional files may be generated based on the bootstrap sampling results.
Conclusion
This script is a powerful tool for analyzing protein-protein interactions in Alzheimer's Disease research. By leveraging bootstrap sampling and frequency analysis, it helps identify key protein associations that may play a role in the disease's pathology.
can you give me an idea of what is a Gene regulatory network and protein-protein network for the introduccion of this readme?
Fuentes
