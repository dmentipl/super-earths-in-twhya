'''
CO.py

for TW Hya paper (adapted from pplot.py)

Daniel Mentiplay
'''

# ---------------------------------------------------------------------------- #

from astropy.io import fits
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

mpl.rcParams['font.size']        = 12.0
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
display_axis_labels = True
display_ticks = True
display_colorbar = True

linewidth = 1.0
linestyles = ['solid']
colors = ['0.4','0.0']

# save_format = 'pdf'
save_format = None

# ---------------------------------------------------------------------------- #

# Load data.
hdulist = fits.open('lines.fits')
hdu = hdulist[0]
dat = hdu.data[0,0,0]
data = np.sum(dat, axis=0)

# Get parameters for plotting.
width_in_pixel = hdu.header['NAXIS1']
distance_in_pc = 59.5
width_in_arcsec = abs(hdu.header['CDELT1']) * 3600 * width_in_pixel
width_in_AU = width_in_arcsec * distance_in_pc
pixel_per_arcsec = width_in_pixel / width_in_arcsec
middle_in_pixel = width_in_pixel/2

# Plot.
fig, ax = plt.subplots()
im = ax.imshow(data)
if display_axis_labels is True:
    plt.xlabel(r'$\Delta\alpha$ [arcseconds]')
    plt.ylabel(r'$\Delta\delta$ [arcseconds]')

# Axis tick labels.
# Adjust manually depending on angular width of image.
if display_ticks:
    half_width = width_in_arcsec/2
    if half_width < 1:
        num_tick = 3
        max_tick = 0.5
    elif half_width < 2:
        num_tick = 5
        max_tick = 1.
    elif half_width < 3.:
        num_tick = 5
        max_tick = 2.
    else:
        num_tick = 7
        max_tick = 3.
    ticks = np.linspace(-max_tick,max_tick,num_tick)
    tick_labels = np.flip(ticks,0)
    ticks = middle_in_pixel + pixel_per_arcsec * ticks
    plt.xticks(ticks,tick_labels)
    plt.yticks(ticks,tick_labels)
else:
    ax.axis('off')

# Legend.
if display_colorbar is True:
    fig.colorbar(im, label='intensity [W.m-2/pixel]')

# Save as figure as pdf.
if save_format is not None:
    filename = 'CO.' + save_format
    plt.savefig(filename)
    if save_format == 'pdf':
        os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))

# Show figure.
else:
    plt.show()
