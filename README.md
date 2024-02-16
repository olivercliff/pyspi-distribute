# Distribute _pyspi_ jobs across a PBS cluster

This repository contains scripts for distributing [pyspi](https://github.com/DynamicsAndNeuralSystems/pyspi) jobs across a PBS-type cluster.
Each job will contain one `Calculator` object that is associated with one multivariate time series (MTS).

The scripts allow the user to specify a directory containing the MTS files, with each sample's time series stored in a separate binary NumPy [(.npy)](https://numpy.org/doc/stable/reference/generated/numpy.save.html) file (as shown in [`simple_demo.ipynb`](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/simple_demo.ipynb)). Within this directory, the user needs to also include a YAML configuration file like [that included in the repo](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/example/sample.yaml) specifying the relative location of each .npy file (and, optionally, the `name`, `dim_order`, and any relevant `labels`). See [`simple_demo.ipynb`](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/simple_demo.ipynb) for code to automatically populate a `sample.yaml` file.


## Usage

1. Follow the [_pyspi_ documentation](https://time-series-features.gitbook.io/pyspi/) to install and set up _pyspi_ on your cluster. We recommend installing into a [new conda environment](https://time-series-features.gitbook.io/pyspi/installation/installing-pyspi#recommended-create-a-conda-environment).
2. Organize all MTS .npy files into a user-specified data directory. 
3. Create the `sample.yaml` file and store it in the same user-specified data directory as your MTS .npy files.
4. Activate your conda environment where _pyspi_ is installed:

```
conda activate pyspi_environment
```
5. Submit the jobs from the command line using [`distribute_jobs.py`](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/distribute_jobs.py) (see below for usage).  

`distribute_jobs.py` works by taking in a data directory, compute file, and sample YAML (see below), iterating over each MTS NumPy array, and submitting a separate pbs job per sample. 
The pbs file is automatically generated from this script and submitted via `qsub`. 
`distribute_jobs.py` includes several command-line options for user configuration, all of which are optional:

* `--data_dir`: Data directory in which all samples' MTS NumPy files are stored.
* `--calc_file_name`: Name of the `.pkl` output file for each sample. The default is `calc.pkl`.
* `--compute_file`: The file path for python script that actually runs _pyspi_. Default is [pyspi_compute.py](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/pyspi_compute.py) in the directory where this script is located.
* `--sample_yaml`: The file path to the sample YAML configuration file (see below for generation details). The default is `sample.yaml`.
* `--pyspi_config`: If desired, the file path to a user-generated YAML configuration file specifying a subset of SPIs to compute. Omitting this argument computes all 283 SPIs.
* `--walltime_hrs`: Maximum walltime allowed for a given job, in hours. The default is 6.
* `--cpu`: The number of CPUs requested per job. The default is 2.
* `--mem`: The amount of memory requested per job, in GB. The default is 20.
* `--overwrite_pkl`: Including this flag means that existing _pyspi_ results for a given sample will be overwritten if found.  
* `--pbs-notify`:  When pbs should email user; a=abort, b=begin, e=end. The default is 'a'.
* `--user_email`:  Email address where pbs should notify user.
* `--table_only`: Optional flag to only save the `calc.table` results for each sample rather than the full `Calculator` object.


### Accessing results 

The results will be stored in the user-specified data directory under the same name as the numpy files; e.g., if you have the file `example_data/Dataset_0.npy` in your YAML file, then there will be a new folder called `example_data/Dataset_0` with a `calc.pkl` file inside that contains the calculator (or the SPI results table).

You can access the results using the `dill` package:

```
import dill

with open('calc.pkl','rb') as f:
  calc = dill.load(f)
```

Then you can view the contents as per the standard _pyspi_ documentation, e.g.,
```
calc.table
calc.table['cov_EmpiricalCovariance]
```

Check out [`simple_demo.ipynb`](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/simple_demo.ipynb) for a more in-depth walkthrough of this process.

### Automatically generate sample YAML configuration file

If you have many samples, you may wish to automatically populate your sample YAML configuration file. As shown in [`simple_demo.ipynb`](https://github.com/DynamicsAndNeuralSystems/pyspi-distribute/blob/main/simple_demo.ipynb), if you have a dictionary containing your MTS where each key is the name of the dataset and the value is the MTS array, you can automatically populate your `sample.yaml` file as follows:

```
# Define the YAML file
yaml_file = "example_data/sample.yaml"

# Use ps dimension order to indicate that processes are the rows while timepoints are the columns
dim_order = "ps"

# Iterate over the keys and values of the dictionary
for key, value in MTS_datasets.items():
    # Define template string and fill in variables
    yaml_string = "{{file: example_data/{key}.npy, name: {key}, dim_order: {dim_order}, labels: [{key}]}}\n"
    yaml_string_formatted = f"{yaml_string.format(key=key, dim_order=dim_order)}"

    # Append line to file
    with open(yaml_file, "a") as f:
        f.write(yaml_string_formatted)
```
