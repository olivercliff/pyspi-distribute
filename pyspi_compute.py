# Loads the local calculator from calc.pkl, run compute, and save back to file
import dill
import os
import sys

fname=sys.argv[1]
table_only=sys.argv[2]
print(f'Attempting to open: {fname}')

with open (fname, "rb") as f:
    calc = dill.load(f)
print(f'Done. Computing...')

calc.compute()

print(f'Saving back to {fname}.')
with open(fname, 'wb') as f:
    if table_only:
        dill.dump(calc.table, f)
    else:
        dill.dump(calc,f)
print('Done.')
