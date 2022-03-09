# Loads the local calculator from calc.pkl, run compute, and save back to file
import dill
import os
import sys

fname=sys.argv[1]
print(f'Attempting to open: {fname}')

with open (fname, "rb") as f:
    calc = dill.load(f)
print(f'Done. Computing...')

calc.compute()

print(f'Saving back to {fname}.')
with open(fname, 'wb') as f:
    dill.dump(calc,f)
print('Done.')
