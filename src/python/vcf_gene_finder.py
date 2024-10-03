"""
Finds the genes that user gives via file input in a vcf file.

Author: Ramon Reilman
Version: 1
data: 03-10-2024
"""

import sys
import argparse

def process_cli():
    """
    Parses command line arguments

    RETURNS
    -------
    args, object that contains users CLI arguments
    """


    parser = argparse.ArgumentParser(description="Get Gene symbols from MGI file")

    parser.add_argument("input_file", type=str, help="Path of the input file")
    parser.add_argument("gene_file", 
                        type=str, 
                        help="Path of the file that contains the wanted genes")

    parser.add_argument(
        "--output_file", type=str, help="Path and name of the output file"
    )
    args = parser.parse_args()

    return args


def get_genes(args):
    """
    Gets a list of genes from a gene.txt file

    PARAMETERS
    ----------
    args, object that contains users CLI arguments

    RETURNS
    -------
    list_genes, list of genes that the user wants to find
    """
    list_genes = []
    try:
        with open(args.gene_file, 'r', encoding='utf-8') as gene_file:
            for line in gene_file:
                list_genes.append(line.strip())
        return list_genes
    except FileNotFoundError:
        print("Gene file not found, maybe check permission?")
        sys.exit(1)


def process_input(args, wanted_genes):
    """
    Reads input file, and finds the users given genes
    
    PARAMETERS
    ----------
    args, object that contains users CLI arguments
    wanted_genes, list of genes that the user wants to find

    RETURNS
    -------
    wanted_genes_lines, string with all the lines that contain the user's gene
    """


    wanted_genes_lines = ""

    try:
        with open(args.input_file, 'r', encoding='utf-8') as input_file:
            for line in input_file:
                if line.startswith("#CHROM"):
                    wanted_genes_lines += line

                line_split = line.split("\t")
                for gene in wanted_genes:
                    if gene in line_split[-1].split("|"):
                        wanted_genes_lines += line
        return wanted_genes_lines
    except FileNotFoundError:
        print("Input file not found, maybe check permission?")
        sys.exit(1)


def process_output(args, filtered_vcf):
    """
    Write the lines with the user's wanted genes to a vcf file
    
    PARAMETERS
    ----------
    args, object that contains users CLI arguments
    filtered_vcf, string with all the lines that contain the user's gene
    """


    if args.output_file is None:
        print("Output not given, putting it in the input folder")
        input_file_list = args.input_file.split("/")
        args.output_file = args.input_file.replace(input_file_list[-1], "output.vcf")

    try:
        with open(args.output_file, 'w', encoding='utf-8') as output_file:
            for line in filtered_vcf:
                output_file.write(line)
    except FileNotFoundError:
        print("Output dir not found, check permission")


def main():
    """
    One main to rule them all
    """
    args = process_cli()
    list_genes = get_genes(args)
    filtered_vcf = process_input(args, list_genes)
    process_output(args, filtered_vcf)


if __name__ == "__main__":
    main()
