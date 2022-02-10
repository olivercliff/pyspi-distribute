from pyspi.calculator import Calculator
from pyspi.data import Data

import os
import yaml
import dill
import fileinput
from shutil import copyfile
from copy import deepcopy

basedir = os.path.dirname(os.path.abspath(__file__))

runfile = 'pyspi_run.pbs'
computefile = 'pyspi_compute.py'

pbsfile = basedir + '/' + runfile
pyfile = basedir + '/' + computefile

basecalc = Calculator()

for dirpath, _, filenames in os.walk(os.path.join(basedir,'database')):
    for filename in filenames:
        if filename.endswith('.yaml'):
            doc = os.path.join(dirpath,filename)
            print(f'Loading {doc}...')
            with open(doc) as d:
                yf = yaml.load(d,Loader=yaml.FullLoader)
                try:
                    for config in yf:
                        file = config['file']
                        dim_order = config['dim_order']
                        name = config['name']
                        labels = config['labels']
                        try:
                            data = Data(data=file,dim_order=dim_order,name=name,normalise=True)
                        except ValueError as err:
                            print(f'Issue loading dataset: {err}')
                            continue

                        calc = deepcopy(basecalc)
                        calc.load_dataset(data)
                        calc.name = name
                        calc.labels = labels

                        # Make new directory for calculator
                        path = file[:-4]
                        savefile = path + '/calc.pkl'

                        if os.path.exists(savefile):
                            print(f'File {savefile} already exists. Delete/move if you would like to recompute.')
                            continue
                        
                        try:
                            os.mkdir(path)
                        except OSError as err:
                            print(f'Creation of the directory {path} failed: {err}')
                        else:
                            print(f'Successfully created the directory {path}')
                        
                        # Save calculator in directory
                        print('Saving object to dill database: "{}"'.format(savefile))
                        with open(savefile, 'wb') as f:
                            dill.dump(calc, f)

                        newpbs = path + '/' + runfile
                        copyfile(pbsfile,newpbs)
                        copyfile(pyfile,path + '/' + computefile)

                        with fileinput.FileInput(newpbs,inplace=True) as f:
                            for line in f:
                                print(line.replace('xxNameOfJobxx', name).replace('xxPathxx',path), end='')

                        # Submit the job
                        os.system(f'qsub {newpbs}')
                except (yaml.scanner.ScannerError,TypeError) as err:
                    print(f'YAML-file {doc} failed: {err}')
