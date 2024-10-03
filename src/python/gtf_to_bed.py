"""
Reads GTF file, extracts gene names, chromosome number, start - stop from exons

Author: Ramon Reilman
Version: 1
data: 03-10-2024
"""

import sys
import argparse
import polars as pl
from gtfparse import read_gtf


def process_cli():
    """
    Parses command line arguments

    RETURNS
    -------
    args, object that contains users CLI arguments
    """

    parser = argparse.ArgumentParser(description="Get BED file from GTF File")

    parser.add_argument("input_file", type=str, help="Path of the input file")
    parser.add_argument(
        "--output_file", type=str, help="Path and name of the output file"
    )
    args = parser.parse_args()

    return args


def process_input(path):
    """
    Read the input file, a GTF file

    PARAMETERS
    ----------
    path, a path to the input file

    RETURNS
    -------
    df_voor_bed, polars dataframe that contains the bed file data
    """


    try:
        gtf_data = read_gtf(path)
        exon_data = gtf_data.filter(pl.col('feature') == 'exon')
        df_voor_bed = exon_data.select(['seqname', 'start', 'end', 'gene_name'])

        # Account for bed index at 0, while gtf starts at 1.
        df_voor_bed = df_voor_bed.with_columns((pl.col("start")-1).alias("start"))

        return df_voor_bed
    except FileNotFoundError:
        print("Input file not found, maybe check permissions?")
        return None


def output_file(args, bed_df):
    """
    Writes the .bed data to a .bed file

    PARAMETERS
    ----------
    args, object that contains users CLI arguments
    bed_df, polars dataframe that contains the bed file data
    """
    if args.output_file is None:
        input_file_list = args.input_file.split("/")
        args.output_file = args.input_file.replace(input_file_list[-1], "output.bed")

    bed_df.write_csv(args.output_file, separator="\t")

def main():

    """
    One main to rule them all
    """
    args = process_cli()
    bed_df = process_input(args.input_file)
    if bed_df is None:
        sys.exit(1)
    output_file(args, bed_df)



if __name__ == "__main__":
    main()
