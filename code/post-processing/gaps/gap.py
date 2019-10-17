from cycler import cycler
from glob import glob
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

# ---------------------------------------------------------------------------- #

# Matplotlib parameters.
mpl.rcParams['axes.prop_cycle'] = cycler('color', ['0.3', '0.3', '0.3', '0.3']) \
                                + cycler('linestyle', ['-', '--', ':', '-.'])
font_family = 'serif'
mpl.rcParams['font.size']   = 18.0
mpl.rcParams['font.family'] = font_family
mpl.rcParams['font.serif']  = 'Times New Roman'
if font_family == 'serif':
    mpl.rcParams['mathtext.fontset'] = 'custom'
    mpl.rcParams['mathtext.cal']     = 'cursive'
    mpl.rcParams['mathtext.rm']      = 'serif'
    mpl.rcParams['mathtext.tt']      = 'monospace'
    mpl.rcParams['mathtext.it']      = 'serif:italic'
    mpl.rcParams['mathtext.bf']      = 'serif:bold'
    mpl.rcParams['mathtext.sf']      = 'sans'


# ---------------------------------------------------------------------------- #

M_sun = 1.99e33
au = 1.496e13
code_units_to_g_per_cm_2 = M_sun / au**2

# normalize = True
normalize = False

# fnames = glob('angm*')
fnames = ['angm00400','angm00600','angm00800','angm01000']
for f in fnames:

    dat = np.loadtxt(f)
    x = dat[:,0]
    y = dat[:,1] * code_units_to_g_per_cm_2

    if normalize:
        y = y / np.max(y)

    plt.plot(x,y)

plt.xlabel('radius [au]')
if normalize:
    plt.ylabel('normalized surface density')
else:
    plt.ylabel('surface density [g/cm${}^2$]')

filename = 'gap.pdf'
plt.savefig(filename, bbox_inches='tight')
os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))
plt.show()
