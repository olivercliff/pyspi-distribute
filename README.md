# Distribute PySPI jobs across a PBS cluster

This repository contains scripts for distributing [PySPI](https://github.com/olivercliff/pyspi) jobs across a PBS-type cluster.
Each job will contain one calculator object that is associated with one multivariate time series (MTS).

The scripts assume the directory structure that is already set up in this repo: there is a [database directory](https://github.com/olivercliff/pyspi-distribute/tree/main/database) (`database`) that contains all MTS files, along with a [YAML configuration file](https://github.com/olivercliff/pyspi-distribute/blob/main/database/sample.yaml) (`sample.yaml`) that specifies the relative location of each file (and, optionally, their `name`, `dim_order`, and any relevant `labels`).

## Usage

1. Follow the [PySPI documentation](https://pyspi-toolkit.readthedocs.io/en/latest/) to install and set-up PySPI on your cluster
2. Ensure that any relevant initialization procedures (for setting up conda or anything else) is contained in the [PBS script](https://github.com/olivercliff/pyspi-distribute/blob/main/pyspi_run.pbs).
3. Copy all MTS (as numpy files) to the `database` folder, and update the `sample.yaml` file accordingly.
4. activate your conda environment:
```
conda activate pyspi
```
5. Submit the jobs:
```
python distribute_jobs.py
```

The results will be stored in the `database` under the same name as the numpy files. For example, if you have the file `database/sample1.npy` in your YAML file, then there will be a new folder called `database/sample1` with a `calc.pkl` file inside that contains the calculator.

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
