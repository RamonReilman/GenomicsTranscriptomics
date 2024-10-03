import polars as pl
import argparse
from gtfparse import read_gtf
# /students/2024-2025/Thema05/BlaasKanker/etc/gencode.vM35.annotation.gtf
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
    try:
        gtf_data = read_gtf(path)
        exon_data = gtf_data.filter(pl.col('feature') == 'exon')
        df_voor_bed = exon_data.select(['seqname', 'start', 'end', 'gene_name'])
        df_voor_bed = df_voor_bed.with_columns((pl.col("start")-1).alias("start"))

        return df_voor_bed
    except FileNotFoundError:
        print("Input file not found, maybe check permissions?")
        return None


def output_file(args, bed_df):
    if args.output_file is None:
        input_file_list = args.input_file.split("/")
        args.output_file = args.input_file.replace(input_file_list[-1], "output.bed")

    bed_df.write_csv(args.output_file, separator="\t")

def main():
    args = process_cli()
    bed_df = process_input(args.input_file)
    if bed_df is None:
        return 1
    output_file(args, bed_df)


if __name__ == "__main__":
    main()