'''
planet-mass-comparison.py

for TW Hya paper (adapted from pplot.py)

Daniel Mentiplay
'''

# ---------------------------------------------------------------------------- #

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

mpl.rcParams['font.size']        = 8.0
mpl.rcParams['font.family']      = 'serif'
mpl.rcParams['font.serif']       = 'Times New Roman'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal']     = 'cursive'
mpl.rcParams['mathtext.rm']      = 'serif'
mpl.rcParams['mathtext.tt']      = 'monospace'
mpl.rcParams['mathtext.it']      = 'serif:italic'
mpl.rcParams['mathtext.bf']      = 'serif:bold'
mpl.rcParams['mathtext.sf']      = 'sans'

# ---------------------------------------------------------------------------- #

# accretion_unit = 'sun'
accretion_unit = 'earth'

display_title = False
display_legend = False

linewidth = 0.8
linestyles = ['solid','dashed','dotted','dashdot']
colors = ['0.3']

save_format = 'pdf'
# save_format = None

# ---------------------------------------------------------------------------- #

au = 1.496e13
M_sun = 1.99e33
M_earth = 5.97219e27
mass_sun_to_earth = M_sun / M_earth
code_units_to_g_per_cm_2 = M_sun / au**2

# ---------------------------------------------------------------------------- #

# Filenames.
filenames = ['angm-04_100', 'angm-08_100', 'angm-16_100', 'angm-24_100',
             'angm-04_1',   'angm-08_1',   'angm-16_1',   'angm-24_1']
nfiles = len(filenames)
figN = [0, 0, 0, 0, 1, 1, 1, 1]

# Radius.
tmp = np.loadtxt(filenames[0])
R_min = [16, 34]
R_max = [33, 49]
R_min_idx = [0, 0]
R_max_idx = [0, 0]
for i in range(2):
    R_min_idx[i] = min(np.where(tmp[:,0] > R_min[i])[0])
    R_max_idx[i] = max(np.where(tmp[:,0] < R_max[i])[0])
R1 = tmp[R_min_idx[0]:R_max_idx[0],0]
R2 = tmp[R_min_idx[1]:R_max_idx[1],0]
nR1 = len(R1)
nR2 = len(R2)

# Initialize figure.
fig, axarr = plt.subplots(2, 2, sharex='col', sharey='row')

# Initialize arrays.
data = np.zeros((nfiles,500,14))
sigmadust1 = np.zeros((nfiles,nR1))
sigmadust2 = np.zeros((nfiles,nR2))

# Loop over files. Get data and plot.
for idx, file in enumerate(filenames):

    data[idx] = np.loadtxt(file)
    sigmadust1[idx] = code_units_to_g_per_cm_2 * data[idx,R_min_idx[0]:R_max_idx[0],2]
    sigmadust2[idx] = code_units_to_g_per_cm_2 * data[idx,R_min_idx[1]:R_max_idx[1],2]
    color = colors[np.mod(idx,len(colors))]
    linestyle = linestyles[np.mod(idx,len(linestyles))]
    axarr[figN[idx],0].plot(R1, sigmadust1[idx], linewidth=linewidth, linestyle=linestyle, color=color)
    axarr[figN[idx],1].plot(R2, sigmadust2[idx], linewidth=linewidth, linestyle=linestyle, color=color)

# Axis labels.
fig.text(0.55, 0.03, '$\mathrm{radius\;[au]}$', ha='center')
fig.text(0.03, 0.55, '$\mathrm{surface\ density\ [g\;cm^{-2}]}$', va='center', rotation='vertical')

# Make layout tighter.
fig.tight_layout(rect=[0.06, 0.03, 1, 1])

# Tick spacing on axes.
tick_spacing = 3
axarr[0,0].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
axarr[0,1].xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))

# Add labels for plots.
bbox_props = dict(boxstyle='round', fc='none', lw=0.8)
fig.text(0.5,  0.92, '$100\;\mu$m', ha='right', bbox=bbox_props)
fig.text(0.95, 0.92, '$100\;\mu$m', ha='right', bbox=bbox_props)
fig.text(0.5,  0.46, '1 mm', ha='right', bbox=bbox_props)
fig.text(0.95, 0.46, '1 mm', ha='right', bbox=bbox_props)

# Save figures to file.
if save_format is not None:
    print('')
    print('Saving figure as ' + save_format)
    filename = 'planet-mass-comparison.' + save_format
    plt.savefig(filename)
    if save_format == 'pdf':
        os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))

# Or plot to screen.
else:
    plt.show()
