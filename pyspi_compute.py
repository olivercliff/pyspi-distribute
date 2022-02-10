# Loads the local calculator from calc.pkl, run compute, and save back to file
import dill
import os

fname = os.path.dirname(os.path.realpath(__file__)) + '/calc.pkl'
print(f'Attempting to open: {fname}')

with open('calc.pkl', 'rb') as f:
    calc = dill.load(f)
print(f'Done. Computing...')

calc.compute()

print(f'Saving back to {fname}.')
with open('calc.pkl', 'wb') as f:
    dill.dump(calc,f)
print('Done.')
