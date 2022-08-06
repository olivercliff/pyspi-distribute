# Load libraries
import pandas as pd
import argparse
import os

# Command-line arguments to parse
parser = argparse.ArgumentParser(description='Create YAML file for pyspi samples to process.')
parser.add_argument('--data_dir', dest='data_dir')
parser.add_argument('--sample_metadata', dest='sample_metadata')
parser.add_argument('--ID_var', dest='ID_var')
parser.add_argument('--label_vars', dest='label_vars')
parser.add_argument('--dim_order', dest='dim_order')
parser.add_argument('--overwrite', dest='overwrite', action="store_true", default=FALSE)
parser.add_argument('--yaml_file', dest='yaml_file')

# Parse arguments
args = parser.parse_args()
data_dir = args.data_dir
sample_metadata = args.sample_metadata
ID_var = args.ID_var
label_vars = args.label_vars
dim_order = args.dim_order
overwrite = args.overwrite
yaml_file = args.yaml_file