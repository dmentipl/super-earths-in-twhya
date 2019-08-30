'''
sigma-init-final.py

for TW Hya paper (adapted from pplot.py)

Daniel Mentiplay
'''

# ---------------------------------------------------------------------------- #

import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

mpl.rcParams['font.size']        = 9.0
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

linewidth = 1.0
linestyles = ['solid']
colors = ['0.4','0.0']

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
filenames = ['angm00000', 'angm00125']

# Radius.
tmp = np.loadtxt(filenames[0])
Rg_min = 10
Rg_max = 200
Rd_min = 10
Rd_max = 80
Rg_min_idx = min(np.where(tmp[:,0] > Rg_min)[0])
Rg_max_idx = max(np.where(tmp[:,0] < Rg_max)[0])
Rd_min_idx = min(np.where(tmp[:,0] > Rd_min)[0])
Rd_max_idx = max(np.where(tmp[:,0] < Rd_max)[0])
Rg = tmp[Rg_min_idx:Rg_max_idx,0]
Rd = tmp[Rd_min_idx:Rd_max_idx,0]
nRg = len(Rg)
nRd = len(Rd)

# Aspect ratio.
aspect_ratio = 0.75

# Initialize figure.
fig, (ax1,ax2) = plt.subplots(2, figsize=(5,5/aspect_ratio))

# Initialize arrays.
data = np.zeros((2,500,14))
sig_g = np.zeros((2,nRg))
sig_d = np.zeros((2,nRd))

# Loop over files. Get data and plot.
for idx, file in enumerate(filenames):

    data[idx] = np.loadtxt(file)
    sig_g[idx] = code_units_to_g_per_cm_2 * data[idx,Rg_min_idx:Rg_max_idx,1]
    sig_d[idx] = code_units_to_g_per_cm_2 * data[idx,Rd_min_idx:Rd_max_idx,2]
    color = colors[np.mod(idx,len(colors))]
    linestyle = linestyles[np.mod(idx,len(linestyles))]
    ax1.plot(Rg, sig_g[idx], linewidth=linewidth, linestyle=linestyle, color=color)
    ax2.plot(Rd, sig_d[idx], linewidth=linewidth, linestyle=linestyle, color=color)

# Aspect ratio.
ax1.set_aspect(1.0/ax1.get_data_ratio()*aspect_ratio)
ax2.set_aspect(1.0/ax2.get_data_ratio()*aspect_ratio)

# Axis labels.
fig.text(0.5, 0.05, '$\mathrm{radius\;[au]}$', ha='center')
fig.text(0.08, 0.5, '$\mathrm{surface\ density\ [g\;cm^{-2}]}$',
                    va='center', rotation='vertical')

# Add arrows.
arrowprops=dict(facecolor='black', arrowstyle='->')
ax1.annotate('Saturn-mass planet', xy=(94, 0.045), xytext=(94, 0.02),
             fontstyle='italic', horizontalalignment='center',
             arrowprops=arrowprops,)
ax2.annotate('Super-Earth', xy=(24, 0.025), xytext=(24+5, 0.038),
             fontstyle='italic', horizontalalignment='center',
             arrowprops=arrowprops,)
ax2.annotate('Super-Earth', xy=(41, 0.02), xytext=(41+5, 0.033),
             fontstyle='italic', horizontalalignment='center',
             arrowprops=arrowprops,)

# Add text.
bbox_props = dict(boxstyle='round', fc='none', lw=0.8)
ax1.annotate('gas',  xy=(200, 0.065), horizontalalignment='right', bbox=bbox_props)
ax2.annotate('dust', xy=(80, 0.04),   horizontalalignment='right', bbox=bbox_props)

# Save figures to file.
if save_format is not None:
    print('')
    print('Saving figure as ' + save_format)
    filename = 'sigma-init-final.' + save_format
    plt.savefig(filename)
    if save_format == 'pdf':
        os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))

# Or plot to screen.
else:
    plt.show()
