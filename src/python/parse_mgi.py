"""
Parse a MGI_features file and get gene symbols from it
Ouput those genes to an output file

Author: Ramon Reilman
Version: 1
data: 01-10-2024
"""

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
    parser.add_argument(
        "--output_file", type=str, help="Path and name of the output file"
    )
    args = parser.parse_args()

    return args


def read_input(path):
    """
    Read the input file, a MGI_features file.

    PARAMETERS
    ----------
    path, a path to the input file

    RETURNS
    -------
    gene_symbol_list, list with all gene symbols
    """

    gene_symbol_list = []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("Type"):
                    continue

                line_list = line.split()
                if line_list[2] == "gene":
                    gene_symbol_list.append(line_list[4])

    except FileNotFoundError:
        print(f"Input file at {path} not found")
        return None
    return gene_symbol_list


def output_file(args, genes_list):
    """
    Writes the gene symbols to an output file

    PARAMETERS
    ----------
    args, object that contains users CLI arguments
    genes_list, list with all gene symbols
    """

    if args.output_file is None:
        input_file_list = args.input_file.split("/")
        args.output_file = args.input_file.replace(input_file_list[-1], "output.txt")

    with open(args.output_file, "w", encoding="utf-8") as output:
        for gene in genes_list:
            output.write(f"{gene}\n")


def main():
    """
    One main to rule them all
    """

    args = process_cli()
    gene_symbols = read_input(args.input_file)
    if gene_symbols is None:
        return 1
    output_file(args, gene_symbols)
    return 0


if __name__ == "__main__":
    main()
