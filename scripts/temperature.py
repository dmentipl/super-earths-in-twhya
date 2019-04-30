'''
temperature.py

For TW Hya paper.

Daniel Mentiplay
'''

# ---------------------------------------------------------------------------- #

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

mpl.rcParams['font.size']        = 13.0
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

plot = 'T'
# plot = 'H_R'

save_figure = True
# save_figure = False

linestyle = 'solid'
color = '0.4'
linewidth = 1.2

# ---------------------------------------------------------------------------- #

R_ref = 10
T_ref = 30
q = 0.125

R_snow = 19
T_snow = 20
H_R_ref = 0.034
H_R_snow = H_R_ref * (R_snow/R_ref)**(1/2-q)

# ---------------------------------------------------------------------------- #

R = np.linspace(10,200)
T = T_snow * (R/R_snow)**(-2*q)
H_R = H_R_ref * (R/R_ref)**(1/2-q)

if plot is 'T':

    plt.plot(R,T,linestyle=linestyle,color=color,linewidth=linewidth)
    plt.plot(R_snow,T_snow,marker='o',color=color)
    plt.xlabel('R [au]')
    plt.ylabel('T [K]')
    filename = 'temperature.pdf'

elif plot is 'H_R':

    plt.plot(R,H_R,linestyle=linestyle,color=color,linewidth=linewidth)
    plt.plot(R_snow,H_R_snow,marker='o',color=color)
    plt.xlabel('R [au]')
    plt.ylabel('H/R')
    filename = 'H_R.pdf'

if save_figure is True:
    plt.savefig(filename)
    os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))
else:
    plt.show()
