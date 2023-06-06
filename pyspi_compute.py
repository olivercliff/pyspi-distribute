# Loads the local calculator from calc.pkl, run compute, and save back to file
import dill
import os
import sys
import random
import pandas as pd

fname=sys.argv[1]
table_only=sys.argv[2]

# # Set the seed manually
# random.seed(127)

print(f'Attempting to open: {fname}')

with open (fname, "rb") as f:
    calc = dill.load(f)
print(f'Done. Computing...')

calc.compute()

print(f'Saving back to {fname}.')
with open(fname, 'wb') as f:
    if table_only:
        SPI_res = calc.table
        # Iterate over each SPI
        SPI_res.columns = SPI_res.columns.to_flat_index()
        
        # Convert index to column
        SPI_res.reset_index(level=0, inplace=True)
        
        # Rename index as first brain region
        SPI_res = SPI_res.rename(columns={"index": "brain_region_from"})

        # Pivot data from wide to long
        SPI_res_long = pd.melt(SPI_res, id_vars="brain_region_from")
        SPI_res_long['SPI'], SPI_res_long['brain_region_to'] = SPI_res_long.variable.str
        
        # Remove variable column
        SPI_res_long = SPI_res_long.drop("variable", 1)

        dill.dump(SPI_res_long, f)
    else:
        dill.dump(calc,f)
print('Done.')
