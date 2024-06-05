from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import numpy as np
import os
import pandas as pd
from pandas.plotting import register_matplotlib_converters
import sys
import xarray as xr

#excel_filename = 'syn_obs_20240604.xlsx'

def new_obs_plot(excel_filename):
   df = pd.read_excel(os.path.join('data', 'excel', excel_filename))
   time = np.arange(6, 15, 1)
   vars = ['T_omniport', 'RH_omniport', 'p_vaisala']
   label = ['T (Omniport) $^{\\circ} C$', 'RH (Omniport) %', 'p (Vaisala) hPa']

   ds = xr.Dataset.from_dataframe(df[vars])
   ds['time'] = time   


   fig, ax = plt.subplots(3, sharex=True)

   ax[0].plot(ds['time'], ds['T_omniport'][1:], label='T (Omniport) $^{\\circ} C$')
   ax[1].plot(ds['time'], ds['RH_omniport'][1:], label='RH (Omniport) $%$')
   ax[2].plot(ds['time'], ds['p_vaisala'][1:], label='p (Vaisala) hPa')
   ax[2].set_xlabel('Time (UTC)')
   for i in range(len(vars)):
      ax[i].set_ylabel(label[i])
      ax[i].grid()
      ax[i].locator_params(axis='y', nbins=5) 

   print(f'Saving figure: {os.path.join('figures', 'lineplot_new.png')}')
   plt.savefig(os.path.join('figures', 'lineplot_new.png'))




