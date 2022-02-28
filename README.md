# Distribute PySPI jobs across a PBS cluster

This repository contains scripts for distributing [PySPI](https://github.com/olivercliff/pyspi) jobs across a PBS-type cluster.
Each job will contain one calculator object that is associated with one multivariate time series (MTS).

The scripts allow the user to specify a directory containing the MTS files, with each sample's time series stored in a separate binary NumPy [(.npy)](https://numpy.org/doc/stable/reference/generated/numpy.save.html) file. Within this directory, the user needs to also include a YAML configuration file like [that included in the repo](https://github.com/olivercliff/pyspi-distribute/blob/main/database/sample.yaml) specifying the relative location of each .npy file (and, optionally, the `name`, `dim_order`, and any relevant `labels`). An R script to automatically populate this configuration file is provided: create_yaml_for_samples.R.


## Usage

1. Follow the [PySPI documentation](https://pyspi-toolkit.readthedocs.io/en/latest/) to install and set up PySPI on your cluster. We recommend installing into a new conda environment.
2. Organize all MTS .npy files into a user-specified data directory. 
3. Either manually create the `sample.yaml` file or automatically populate it using `create_yaml_for_samples.R` (see below for usage).
4. Activate your conda environment where PySPI is installed:
```
conda activate pyspi
```
5. Submit the jobs from the command line using `distribute_jobs.py` (see below for usage).  

`distribute_jobs.py` works by taking in a data directory, compute file, and sample YAML (see below), iterating over each MTS NumPy sample, and submitting a separate pbs job per sample. The pbs file is automatically generated from this script and submitted via `qsub`. `distribute_jobs.py` includes several command-line options for user configuration, all of which are optional:

* `--data_dir`: Data directory in which all samples' MTS NumPy files are stored. If no path is supplied, the default is `./database/` from the directory in which `distribute_jobs.py` is located.
* `--compute_file`: The file path for python script that actually runs pyspi. Default is [pyspi_compute.py](https://github.com/olivercliff/pyspi-distribute/blob/main/pyspi_compute.py) in the directory where this script is located.
* `--sample_yaml`: The file path to the sample YAML configuration file (see below for generation details). The default is `./database/sample.yaml`.
* `--pyspi_config`: If desired, the file path to a user-generated YAML configuration file specifying a subset of SPIs to compute.
* `--walltime_hrs`: Maximum walltime allowed for a given job, in hours. The default is 24.
* `--overwrite_pkl`: Including this flag means that existing pyspi results for a given sample will be overwritten.  
* `--pbs-notify`:  When pbs should email user; a=abort, b=begin, e=end. The default is none.
* `--email`:  Email address when pbs should notify user.


### Accessing results 

The results will be stored in the user-specified data directory under the same name as the numpy files. For example, if you have the file `database/sample1.npy` in your YAML file, then there will be a new folder called `database/sample1` with a `calc.pkl` file inside that contains the calculator.

In order to access the results, load the calculator with dill

```
import dill

with open('calc.pkl','rb') as f:
  calc = dill.load(f)
```

Then you can view the contents as per the standard *PySPI* documentation, e.g.,
```
calc.table
calc.table['cov_EmpiricalCovariance]
```


### Automatically generate sample YAML configuration file

If you have many samples, you may wish to automatically populate your sample YAML configuration file. We have provided the R script `create_yaml_for_samples.R` to accomplish this. This script can be run on the command line with the following arguments:  

* `--data_dir`: [*Required*] Data directory in which all samples' MTS NumPy files are stored (e.g. `database/`)
* `--sample_metadata`: [*Optional*] Path to CSV file containing sample metadata. If supplied, the identifying variable for each sample MTS must be `sampleID`.
* `--label_vars`: [*Optional*] Variable(s) to include in the YAML file from the metadata.
* `--overwrite`: [*Optional flag*] If included, `sample.yaml` will be overwritten if if already exists.  

