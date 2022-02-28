library(tidyverse)
library(argparse)
library(tools)

parser <- ArgumentParser(description='Automatically generate sample YAML file for pyspi-distribute.')

parser$add_argument("--data_dir", help="Directory containing samples' .npy files.")
parser$add_argument("--sample_metadata", help="OPTIONAL: CSV file containing sample metadata info.")
parser$add_argument("--label_vars", help="OPTIONAL: columns in metadata to use as labels for YAML.")
parser$add_argument("--overwrite", help="Should sample.yaml be overwritten if it already exists? Default is F.",
                    action="store_true", default=FALSE)

# Parse arguments
args <- parser$parse_args()
data_dir <- args$data_dir
metadata <- args$sample_metadata
meta_vars <- args$label_vars
overwrite <- args$overwrite

npy_files <- list.files(data_dir, pattern="*.npy")
yaml_file <- paste0(data_dir, "sample.yaml")

if (!is.null(metadata) & !is.null(meta_vars)) {
  metadata_data <- read.csv(metadata)
}

if (!file.exists(yaml_file) | overwrite) {
  file.create(yaml_file)
  yaml_string <- "- {file: %s, name: %s, dim_order: sp, labels: [%s] }\n"
  for (npy in npy_files) {
    sample_ID <- tools::file_path_sans_ext(npy)
    if (!is.null(metadata) & !is.null(meta_vars)) {
      sample_data <- metadata_data %>%
        dplyr::filter(sampleID == sample_ID) %>%
        dplyr::select(meta_vars)
      sample_data_vector <- paste(as.vector(sample_data[1,]), collapse=",")
    } else{
      sample_data_vector <- character()
    }
    
    sample_string <- sprintf(yaml_string, 
                           paste0(data_dir, npy),
                           sample_ID,
                           sample_data_vector)
    write_file(sample_string, yaml_file, append=T)
  }
}

