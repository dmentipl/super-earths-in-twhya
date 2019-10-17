'''
van-boekel2017.py

Plot van Boekel et al. (2017) SPHERE 1.6 micron image.

Daniel Mentiplay
'''
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import os

mpl.rcParams['font.size']        = 20.0
mpl.rcParams['font.family']      = 'serif'
mpl.rcParams['font.serif']       = 'Times New Roman'
mpl.rcParams['mathtext.fontset'] = 'custom'
mpl.rcParams['mathtext.cal']     = 'cursive'
mpl.rcParams['mathtext.rm']      = 'serif'
mpl.rcParams['mathtext.tt']      = 'monospace'
mpl.rcParams['mathtext.it']      = 'serif:italic'
mpl.rcParams['mathtext.bf']      = 'serif:bold'
mpl.rcParams['mathtext.sf']      = 'sans'

# Options.
save_format = 'pdf'
plot_to_screen = False
scalebar = False
arrow = False
text = False
integer_ticks_labels = True

# Read png.
image = plt.imread('huang-2018.png', format='png')
width_in_pixel = image.shape[0]
width_in_arcsec = 8.98
middle_in_pixel = int(width_in_pixel/2)
pixel_per_arcsec = width_in_pixel/width_in_arcsec

# Plot image.
fig, ax = plt.subplots()
im = ax.imshow(image)

# Ticks.
half_width = width_in_arcsec/2
num_tick = 5
max_tick = 4.
ticks = np.linspace(-max_tick,max_tick,num_tick)
tick_labels = ticks
if integer_ticks_labels:
    tick_labels = ticks.astype(int)
ticks = middle_in_pixel + pixel_per_arcsec * ticks
xticks = np.flip(ticks, 0)
yticks = np.flip(ticks, 0)
ax.set_xticks(xticks)
ax.set_yticks(yticks)
ax.set_xticklabels(tick_labels)
ax.set_yticklabels(tick_labels)
ax.tick_params(axis='both',
               which='both',
               color='white',
               bottom='on',
               top='on',
               left='on',
               right='on',
               labelbottom='on',
               labelleft='on',
               direction='in')
ax.set_xlabel(r'$\mathrm{\Delta\alpha\ [arcsec]}$')
ax.set_ylabel(r'$\mathrm{\Delta\delta\ [arcsec]}$')

# Plot scalebar.
if scalebar:
    width_in_AU = 380
    scalebar_in_AU = 50
    pixel_per_AU = width_in_pixel / width_in_AU
    scalebar_width = scalebar_in_AU * pixel_per_AU
    posx = 0.05*width_in_pixel
    posy = 0.05*width_in_pixel
    offsetx = 0.2*posx
    offsety = 1.1*posy
    plt.plot((posx,posx+scalebar_width),(posy,posy),color='white',linewidth=2.0)
    plt.text(posx+offsetx,posy+offsety,'50 au',color='white')

# Add arrows.
if arrow:
    arrowprops=dict(color='white', arrowstyle='->')
    parrow = (0.83*width_in_pixel, 0.28*width_in_pixel)
    ptext  = (0.80*width_in_pixel, 0.10*width_in_pixel)
    ax.annotate('Spiral arm?', xy=parrow, xytext=ptext,
                color='white', horizontalalignment='center', fontsize=18,
                arrowprops=arrowprops,)

if text:
    text = 'SPHERE 1.6 $\mu$m DPI'
    posx = 0.05*width_in_pixel
    posy = 0.10*width_in_pixel
    ax.text(posx, posy, text, ha='left', color='white')

# Save figure.
if save_format is not None:
    filename = 'huang-2018-modified.' + save_format
    plt.savefig(filename, bbox_inches='tight')
    if save_format == 'pdf':
        os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))

# Plot to screen.
if plot_to_screen:
    plt.show()
