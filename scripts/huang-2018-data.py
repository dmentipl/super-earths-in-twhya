'''


HACKED FROM iplot.py TO GET WORKING FOR PAPER TO PLOT CO FROM DATA.

Image plot

Make figures from fits files generated by MCFOST, and possibly other sources.

Data can be scattered light, dust thermal emission, and molecular line emission.
It can include polarization and velocity channels. The fits file may be
post-processed by CASA.

Files required are:
    - .fits file(s) containing the image data from MCFOST
    - .json file with plotting options
    - (optional) top_left.txt, top_right.txt, bottom_left.txt, bottom_right.txt
      which contains annotation text for plots

Can be used in an ipython shell, or at the command line.

D. Mentiplay, 2017-2018
'''


# ---------------------------------------------------------------------------- #

import argparse
from argparse import RawTextHelpFormatter
from astropy.io import fits
from astropy import constants
from astropy import units
from cycler import cycler
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.ticker import FuncFormatter
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
from numpy import pi
import os
from os.path import exists
from pprint import pprint
import sys


# ---------------------------------------------------------------------------- #

c = constants.c.cgs.value
h = constants.h.cgs.value
kB = constants.k_B.cgs.value
arcsec = units.arcsec.cgs.scale
mas = units.mas.cgs.scale
Jy = units.Jansky.cgs.scale


# ---------------------------------------------------------------------------- #

# Options.
max_brightness = 60  #None  # 2 for thermal continuum or 60 for CO intensity map
font_family = 'serif'  # 'sans-serif'
minor_ticks = False
add_text = True
Tbrightness = False
integer_ticks_labels = True
xlabel_valign = -0.02
ylabel_halign = 0.08
size_scaling = 2.45  #None  # 2.45 for both sets of ALMA data


# ---------------------------------------------------------------------------- #

# Matplotlib parameters.
mpl.rcParams['axes.prop_cycle'] = cycler('color', ['0.3', '0.3', '0.3', '0.3']) \
                                + cycler('linestyle', ['-', '--', ':', '-.'])
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

def get_data(prefix, opts):

    # Open fits file.
    filename = prefix+'.fits'
    if exists(filename):
        print('\nGetting data from ' + filename)
        hdulist = fits.open(filename)
        hdu = hdulist[0]
    else:
        print('Data file \'' + filename + '\' does not exist')
        sys.exit(1)

    # Get info from header.
    crpixx = hdu.header.get('CRPIX1')
    crpixy = hdu.header.get('CRPIX2')
    width_in_pixel = hdu.header.get('NAXIS1')
    arcsec_per_pixel = abs(hdu.header.get('CDELT1')) * 3600
    pixel_per_arcsec = 1/arcsec_per_pixel
    width_in_arcsec = arcsec_per_pixel * width_in_pixel
    middle_in_pixel = width_in_pixel/2

    # Beam unit.
    bunit = hdu.header.get('BUNIT')
    if bunit == 'Jy/beam':
        flux_unit = 'Jy'
        pixel_unit = 'beam'
    elif bunit == 'JY/PIXEL':
        flux_unit = 'Jy'
        pixel_unit = 'pixel'
    elif bunit == 'W.m-2.pixel-1':
        flux_unit = 'W.m-2'
        pixel_unit = 'pixel'

    # Beam in arcsec. PA in degrees.
    BMAJ = hdu.header.get('BMAJ')
    BMIN = hdu.header.get('BMIN')
    BPA  = hdu.header.get('BPA')
    if BMAJ is not None:
        BMAJ = BMAJ * 3600
        BMIN = BMIN * 3600
    if opts['convolve'] is not None:
        if BMAJ is not None:
            print('Attempting to convolve already convolved data')
            sys.exit(1)
        else:
            BMAJ = opts['convolve'][0] / 1000
            BMIN = opts['convolve'][1] / 1000
            BPA  = opts['convolve'][2]

    # Distance scaling.
    if opts['distance'] is not None:
        width_in_au = width_in_arcsec * opts['distance']
        pixel_per_au = width_in_pixel / width_in_au
    else:
        width_in_au = None
        pixel_per_au = None

    # Frequency and wavelength.
    if hdu.header.get('CTYPE3') == 'FREQ    ':
        freq_Hz = hdu.header.get('CRVAL3')
        if freq_Hz is not None:
            wl_micron = c/freq_Hz * 1e4
        else:
            wl_micron = None
    else:
        wl_micron = None

    # Make image tighter.
    if size_scaling is not None:
        fac = size_scaling
        leftpix = round(0.5*(1-1/fac)*width_in_pixel)
        rightpix = width_in_pixel-round(0.5*(1-1/fac)*width_in_pixel)
        width_in_arcsec = width_in_arcsec / fac
        width_in_pixel = width_in_pixel / fac
        middle_in_pixel = middle_in_pixel / fac

    # Squeeze arrays.
    data = np.squeeze(hdu.data)

    # Remove nan.
    if np.isnan(data).any():
        data = np.nan_to_num(data)

    # Check for type of image data.
    if np.ndim(data) > 2:
        if np.amin(data.shape) == 4:
            dtype = 'polarized'
        else:
            dtype = 'line'
    else:
        dtype = 'continuum'

    # Continuum emission.
    if dtype == 'continuum':
        img = data

    # Polarized scattered light.
    elif dtype == 'polarized':
        if opts['polarization'] is None:
            img = data[0]
        else:
            Q = data[1]
            U = data[2]
            V = data[3]
            print('Polarization: ' + opts['polarization'])
            if opts['polarization']=='Q':
                img = Q
            elif opts['polarization']=='Qphi':
                px = np.linspace(0,width_in_pixel-1,width_in_pixel)
                mx, my = np.meshgrid(px,px)
                phi = np.arctan2(mx-crpixx,my-crpixy)
                Qphi = -(Q * np.cos(2*phi) + U * np.sin(2*phi))
                img = Qphi
            elif opts['polarization']=='U':
                img = U
            elif opts['polarization']=='V':
                img = V
            else:
                print('Polarization is either Q, Qphi, U, or V')
                sys.exit(1)

    # Line emission.
    elif dtype == 'line':
        print('For now, can only plot integrated intensity for line emission')
        if hdu.header.get('CTYPE3') == 'VELO-LSR':
            # From MCFOST.
            delta_V = hdu.header.get('CDELT3')
        else:
            # From ALMA data.
            delta_V = 1e-5 * c * np.abs(hdu.header.get('CDELT3')/hdu.header.get('CRVAL3'))
        data[data < 3*1.7e-3] = 0
        img = np.sum(data, axis=0) * delta_V

    # Re-scale.
    if size_scaling is not None:
        img = img[leftpix:rightpix,leftpix:rightpix]

    # Package data.
    dat = {'BMAJ': BMAJ,
           'BMIN': BMIN,
           'BPA': BPA,
           'crpixx': crpixx,
           'crpixy': crpixy,
           'dtype': dtype,
           'flux_unit': flux_unit,
           'middle_in_pixel': middle_in_pixel,
           'pixel_per_au': pixel_per_au,
           'pixel_per_arcsec': pixel_per_arcsec,
           'pixel_unit': pixel_unit,
           'width_in_arcsec': width_in_arcsec,
           'width_in_au': width_in_au,
           'width_in_pixel': width_in_pixel,
           'wl_micron': wl_micron}

    return img, dat


# ---------------------------------------------------------------------------- #

def process_image(img, opts, dat):

    # Unpack dat structure.
    BMAJ = dat['BMAJ']
    BMIN = dat['BMIN']
    BPA  = dat['BPA']
    crpixx = dat['crpixx']
    crpixy = dat['crpixy']
    flux_unit = dat['flux_unit']
    pixel_per_arcsec = dat['pixel_per_arcsec']
    pixel_unit = dat['pixel_unit']
    width_in_pixel = dat['width_in_pixel']
    wl_micron = dat['wl_micron']

    # Convert from SI or Jy to mJy.
    if wl_micron is None:
        print('No wavelength in fits header, assuming CO J=3--2 with lambda = 345 GHz')
        nu = 345e9
        wl_cm = c/nu
    else:
        wl_cm = wl_micron / 1e4
    if flux_unit == 'W.m-2':
        img = SI_to_mJy(img, wl_cm)
        dat['flux_unit'] = 'mJy'
    if flux_unit == 'Jy':
        img = 1000*img
        dat['flux_unit'] = 'mJy'

    # Add noise.
    if opts['noise'] is not None:
        gain = opts['noise'][0]
        fixed = opts['noise'][1]
        print('Noise: (gain,fixed) = (' + str(gain) + ',' + str(fixed) + ')')
        noise1 = 1 + gain  * np.random.randn(width_in_pixel,width_in_pixel)
        noise2 = np.abs(fixed * img * np.random.randn(width_in_pixel,width_in_pixel))
        img   = noise1 * img + noise2

    # Convolve with PSF.
    if opts['convolve'] is not None:
        # Smooth to beam.
        BMAJ_in_pixels = BMAJ * pixel_per_arcsec
        BMIN_in_pixels = BMIN * pixel_per_arcsec
        print('Convolve with beam with FWHM of (' + str(BMAJ*1000) +
              ',' + str(BMIN*1000) + ') mas at PA = ' + str(BPA))
        sigma_x = BMAJ_in_pixels / (2.*np.sqrt(2.*np.log(2)))
        sigma_y = BMIN_in_pixels / (2.*np.sqrt(2.*np.log(2)))
        psf = gauss_kernel2(int(max(sigma_x,sigma_y))*5,sigma_x,sigma_y,90.+BPA)
        img = convol2df(img,psf)
        # Pixel to beam in units.
        if pixel_unit == 'pixel':
            img = pixel_to_beam(img, BMAJ, BMIN, 1/pixel_per_arcsec)
            dat['pixel_unit'] = 'beam'

    # Scale by R^p.
    if opts['scaling'] is not None:
        print('Scaling by R^p where p = '+str(opts['scaling']))
        p = opts['scaling']
        px = np.linspace(0,width_in_pixel-1,width_in_pixel)
        mx, my = np.meshgrid(px,px)
        Rscaled_pix = abs(mx-crpixx+1)**p + abs(my-crpixy+1)**p
        Rscaled = Rscaled_pix/Rscaled_pix.max()
        img = Rscaled*img

    # Coronagraph.
    if opts['coronagraph']:
        print('Adding coronagraph of radius '+str(opts['coronagraph'])+' mas')
        px = np.linspace(0,width_in_pixel-1,width_in_pixel)
        mx, my = np.meshgrid(px,px)
        R_pix = np.sqrt((mx-crpixx+1)**2 + (my-crpixy+1)**2)
        R_arcsec = R_pix / pixel_per_arcsec
        img[R_arcsec<opts['coronagraph']/1000] = 0.
    else:
        img[img==img.max()] = 0.

    return img, dat


# ---------------------------------------------------------------------------- #

def set_plot(img, opts, dat):

    # Unpack dat structure.
    crpixx = dat['crpixx']
    crpixy = dat['crpixy']
    dtype = dat['dtype']
    flux_unit = dat['flux_unit']
    middle_in_pixel = dat['middle_in_pixel']
    pixel_per_arcsec = dat['pixel_per_arcsec']
    pixel_per_au = dat['pixel_per_au']
    pixel_unit = dat['pixel_unit']
    width_in_arcsec = dat['width_in_arcsec']
    width_in_au = dat['width_in_au']
    width_in_pixel = dat['width_in_pixel']

    # Axis tick labels.
    # Adjust manually depending on angular width of image.
    if opts['axes'] == 'arcsec':
        half_width = width_in_arcsec/2
        if half_width < 0.5:
            num_tick = 5
            max_tick = 0.4
        elif half_width < 1:
            num_tick = 3
            max_tick = 0.5
        elif half_width < 2:
            num_tick = 5
            max_tick = 1.
        elif half_width < 3.:
            num_tick = 5
            max_tick = 2.
        elif half_width < 4.:
            num_tick = 7
            max_tick = 3.
        else:
            num_tick = 5
            max_tick = 4.
        ticks = np.linspace(-max_tick,max_tick,num_tick)
        tick_labels = ["{:.1f}".format(tick) for tick in ticks]
        if integer_ticks_labels:
            if max_tick/(int(num_tick/2)) < 1:
                print('You probably don\'t want to set integer_ticks_labels')
            tick_labels = ["{0:.0f}".format(tick) for tick in ticks]
        ticks = middle_in_pixel + pixel_per_arcsec * ticks
        xticks = np.flip(ticks, 0)
        yticks = np.flip(ticks, 0)
    elif opts['axes'] == 'au':
        half_width = width_in_au/2
        if half_width < 50:
            num_tick = 5
            max_tick = 25
        elif half_width < 75:
            num_tick = 5
            max_tick = 50
        elif half_width < 100:
            num_tick = 7
            max_tick = 75
        elif half_width < 150:
            num_tick = 7
            max_tick = 100
        elif half_width < 200:
            num_tick = 7
            max_tick = 150
        else:
            num_tick = 7
            max_tick = 200
        ticks = np.linspace(-max_tick,max_tick,num_tick)
        tick_labels = ["{0:.0f}".format(tick) for tick in ticks]
        ticks = middle_in_pixel + pixel_per_au * ticks
        xticks = ticks
        yticks = np.flip(xticks,0)

    # Set units for colorbar label.
    unit_label = 'brightness ' + '[' + flux_unit + '/' + pixel_unit
    if dtype == 'line':
        unit_label = unit_label + ' km/s]'
    else:
        unit_label = unit_label + ']'

    # Change image contrast or set max brightness.
    scale = 1.0
    if opts['contrast'] is not None:
        scale = opts['contrast']
    if max_brightness is not None:
        print('Setting vmax to max_brightness = ' + str(max_brightness))
        vmax = max_brightness
    else:
        vmax = scale*img.max()

    # Normalize. Overrides scaling.
    if opts['normalize']:
        img = img/np.max(img)
        unit_label = 'normalized brightness'
        vmax = 1.

    # Azimuthally average image.
    if not opts['cut'] and opts['average']:
        print('Taking azimuthal average')
        radial_brightness = radial_profile(img, (crpixx,crpixy))
        for mx in range(width_in_pixel):
            for my in range(width_in_pixel):
                R_pix = np.sqrt((mx-crpixx+1)**2 + (my-crpixy+1)**2)
                img[mx,my] = radial_brightness[int(R_pix)]

    # Set color map.
    if dtype == 'line':
        cmap = 'Blues_r'
    elif dtype == 'polarized':
        cmap = 'gist_heat'
    elif dtype == 'continuum':
        cmap = 'inferno'

    # Plot options.
    plot = {'cmap': cmap,
            'xticks': xticks,
            'yticks': yticks,
            'tick_labels': tick_labels,
            'unit_label': unit_label,
            'vmax': vmax}

    return img, plot


# ---------------------------------------------------------------------------- #

def plot_image(img, fig, ax, idx, opts, dat, plot):

    # Unpack dat structure.
    BMAJ = dat['BMAJ']
    BMIN = dat['BMIN']
    BPA  = dat['BPA']
    pixel_per_au = dat['pixel_per_au']
    pixel_per_arcsec = dat['pixel_per_arcsec']
    width_in_pixel = dat['width_in_pixel']

    # Unpack plot options.
    cmap = plot['cmap']
    tick_labels = plot['tick_labels']
    unit_label = plot['unit_label']
    vmax = plot['vmax']
    xticks = plot['xticks']
    yticks = plot['yticks']

    # Plot.
    im = ax.imshow(img,cmap=cmap,vmin=0.0,vmax=vmax)

    # Axis tick labels.
    if idx == 0:
        labelleft = 'on'
    else:
        labelleft = 'off'
    ax.set_xticks(xticks)
    ax.set_yticks(yticks)
    ax.set_xticklabels(tick_labels)
    ax.set_yticklabels(tick_labels)
    if not opts['nolabels']:
        ax.tick_params(axis='both',
                       which='both',
                       color='white',
                       bottom='on',
                       top='on',
                       left='on',
                       right='on',
                       labelbottom='on',
                       labelleft=labelleft,
                       direction='in')
    else:
        ax.tick_params(axis='both',
                       which='both',
                       bottom='off',
                       top='off',
                       left='off',
                       right='off',
                       labelbottom='off',
                       labelleft='off')

    # Scale bar.
    if opts['scalebar'] is not None:
        scalebar_in_au = int(opts['scalebar'])
        scalebar_width = scalebar_in_au * pixel_per_au
        posx = 0.05*width_in_pixel
        posy = 0.05*width_in_pixel
        offsetx = scalebar_width/2
        offsety = 1.1*posy
        ax.plot((posx,posx+scalebar_width),(posy,posy),color='white',linewidth=2.0)
        ax.text(posx+offsetx,posy+offsety,str(scalebar_in_au)+' au',
                 horizontalalignment='center',color='white')

    # Add misc text.
    if add_text:
        text_files = ['top_left.txt', 'top_right.txt', 'bottom_left.txt', 'bottom_right.txt']
        posx = np.array([0.05, 0.95, 0.05, 0.95])*width_in_pixel
        posy = np.array([0.10, 0.10, 0.90, 0.90])*width_in_pixel
        ha = ['left', 'right', 'left', 'right']
        for indx, text_file in enumerate(text_files):
            if exists(text_file):
                with open(text_file) as f:
                    text_to_add = f.readlines()
                text_to_add = [x.strip() for x in text_to_add]
                if idx + 1 > len(text_to_add):
                    print('Not enough lines in ' + str(text_file))
                    sys.exit(1)
                text = text_to_add[idx]
                ax.text(posx[indx], posy[indx], text, ha=ha[indx], color='white')

    # Beam size.
    if opts['beam']:
        if BMAJ is not None:
            print('Plotting beam ellipse')
            BMAJ_in_pixels = BMAJ * pixel_per_arcsec
            BMIN_in_pixels = BMIN * pixel_per_arcsec
            posx = 0.05*width_in_pixel
            posy = 0.95*width_in_pixel
            ellipse1=Ellipse((posx,posy),width=BMAJ_in_pixels,
                                         height=BMIN_in_pixels,
                                         angle=90.-BPA,
                                         color='white',
                                         linewidth=1.0,
                                         fill=False)
            ax.add_artist(ellipse1)
        else:
            print('Can\'t find beam to plot: set convolve in options file')

    # Mask.
    if opts['mask'] is not None:
        mask_width_in_pixels = 2 * pixel_per_au * opts['mask']
        posx = 0.5*width_in_pixel
        posy = 0.5*width_in_pixel
        ellipse2=Ellipse((posx,posy),width=mask_width_in_pixels,
                                     height=mask_width_in_pixels,
                                     angle=0.,
                                     color='grey',
                                     linewidth=1.5,
                                     fill=True)
        ax.add_artist(ellipse2)

    # Legend, i.e. colorbar.
    if opts['colorbar'] and colorbar_per_axis:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes('right', size='5%', pad=0.05)
        fig.colorbar(im, cax=cax, orientation='vertical', label=unit_label)

    return im

# ---------------------------------------------------------------------------- #

def plot_profile(img, ax, opts, dat, plot):

    # Unpack dat.
    BMAJ = dat['BMAJ']
    BMIN = dat['BMIN']
    crpixx = dat['crpixx']
    crpixy = dat['crpixy']
    middle_in_pixel = dat['middle_in_pixel']
    wl_micron = dat['wl_micron']
    width_in_arcsec = dat['width_in_arcsec']
    width_in_au = dat['width_in_au']
    width_in_pixel = dat['width_in_pixel']

    # Azimuthally average radial cut.
    if opts['average']:
        print('Taking azimuthal average')
        brightness = radial_profile(img, (crpixx,crpixy))
        brightness = brightness[0:int(width_in_pixel/2)]
        if Tbrightness:
            print('Converting to brightness temperature')
            wl_cm = wl_micron / 1e4
            brightness = Flux_to_Tbrightness(brightness,wl_cm,BMAJ,BMIN)
        if opts['axes'] == 'arcsec':
            radius = np.linspace(0,width_in_arcsec/2,len(brightness))
        elif opts['axes'] == 'au':
            radius = np.linspace(0,width_in_au/2,len(brightness))
    else:
        brightness = img[int(middle_in_pixel)]

    # Radius range.
    if opts['radius'] is not None:
        R_min_idx = min(np.where(radius > opts['radius'][0])[0])
        R_max_idx = max(np.where(radius < opts['radius'][1])[0])
        radius = radius[R_min_idx:R_max_idx]
        brightness = brightness[R_min_idx:R_max_idx]

    # Unpack plot options.
    unit_label = plot['unit_label']

    # Normalize.
    if opts['normalize']:
        brightness = brightness/np.max(brightness)
        unit_label = 'normalized brightness'

    # Brightness temperature.
    if Tbrightness:
        unit_label = 'brightness temperature [K]'

    # Plot.
    if opts['log'] is None:
        ax.plot(radius,brightness)
    elif opts['log'] == 'x':
        ax.semilogx(radius,brightness)
    elif opts['log'] == 'y':
        ax.semilogy(radius,brightness)
    elif opts['log'] == 'xy':
        ax.loglog(radius,brightness)

    # Axis tick labels.
    if not opts['nolabels']:
        if opts['log'] is not None:
            formatter = FuncFormatter(lambda y, _: '{:.16g}'.format(y))
            ax.xaxis.set_major_formatter(formatter)
            if minor_ticks:
                ax.xaxis.set_minor_formatter(formatter)
            else:
                ax.tick_params(axis='x', which='minor', labelbottom='off')
        if opts['axes'] == 'arcsec':
            ax.set_xlabel(r'$\Delta\alpha$ [arcsec]')
        elif opts['axes'] == 'au':
            ax.set_xlabel('radius [au]')
        ax.set_ylabel(unit_label)


# ---------------------------------------------------------------------------- #

def generate_plot(prefixes, opts):

    # Set up figure and axes.
    nfiles = len(prefixes)
    global colorbar_per_axis
    if nfiles > 1:
        colorbar_per_axis = False
    else:
        colorbar_per_axis = True
    if opts['cut'] or nfiles == 1:
        fig, ax = plt.subplots()
        axes = [ax for number in range(nfiles)]
    else:
        w, h = plt.figaspect(nfiles)
        fig, axes = plt.subplots(1, nfiles, figsize=(h,w))
        fig.subplots_adjust(wspace=0.0)

    for idx, prefix in enumerate(prefixes):

        # Get image data and header info.
        img, dat = get_data(prefix, opts)

        # Process image.
        img, dat = process_image(img, opts, dat)

        # Set plot options.
        img, plot = set_plot(img, opts, dat)

        # Plot image or radial profile.
        if not opts['cut']:

            # Plot image.
            im = plot_image(img, fig, axes[idx], idx, opts, dat, plot)

        else:

            # Plot radial profile.
            plot_profile(img, axes[idx], opts, dat, plot)

    # Axis labels.
    # For subplots may need to adjust manually:
    #   see xlabel_valign, ylabel_halign above.
    if not opts['nolabels'] and not opts['cut']:
        if nfiles > 1:
            if opts['axes'] == 'arcsec':
                fig.text(0.5, xlabel_valign, r'$\mathrm{\Delta\alpha\ [arcsec]}$',
                         ha='center')
                fig.text(ylabel_halign, 0.5, r'$\mathrm{\Delta\delta\ [arcsec]}$',
                         va='center', rotation='vertical')
            elif opts['axes'] == 'au':
                fig.text(0.5, xlabel_valign, 'radius [au]', ha='center')
                fig.text(ylabel_halign, 0.5, 'radius [au]',
                         va='center', rotation='vertical')

        else:
            if opts['axes'] == 'arcsec':
                ax.set_xlabel(r'$\mathrm{\Delta\alpha\ [arcsec]}$')
                ax.set_ylabel(r'$\mathrm{\Delta\delta\ [arcsec]}$')
            elif opts['axes'] == 'au':
                ax.set_xlabel('radius [au]')
                ax.set_ylabel('radius [au]')

    if opts['colorbar'] and not colorbar_per_axis:
        fig.subplots_adjust(right=0.9)
        cbar_ax = fig.add_axes([0.91, 0.11, 0.01, 0.77])
        fig.colorbar(im, cax=cbar_ax, orientation='vertical', label=plot['unit_label'])

# ---------------------------------------------------------------------------- #

def get_command_line_opts():

    # Read command line args.
    description, epilog = options_help()
    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description=description,
                                     epilog=epilog)
    parser.add_argument('-o', '--options',
                        help='options filename (without .json extension)',
                        required=False)
    parser.add_argument('-p', '--prefix',
                        nargs='+',
                        help='prefix(es) for data (without .fits extension)',
                        required=True)
    parser.add_argument('-s', '--save',
                        help='save as [pdf|png|jpeg]',
                        required=False)
    args = parser.parse_args()

    # Check if data files are available.
    prefixes = args.prefix
    for prefix in prefixes:
        if not exists(prefix + '.fits'):
            print('Data file \'' + prefix + '.fits' + '\' does not exist')
            sys.exit(1)

    # Get options.
    if args.options is not None:
        filename = args.options + '.json'
    else:
        filename = args.options
    opts = get_options(filename)

    # Set save option.
    if args.save is not None:
        tmp, ext = os.path.splitext(args.save)
        if ext == '':
            save_format = tmp
        else:
            save_format = ext[1:]
        if save_format not in ('pdf', 'png', 'jpeg'):
            print('Save format should be pdf, png, or jpeg')
            sys.exit(1)
        else:
            save_format = args.save
    else:
        save_format = None

    # Print out options used.
    print('\nCurrent options:')
    pprint(opts)
    print('')

    # Return.
    return prefixes, save_format, opts


# ---------------------------------------------------------------------------- #

def check_options(opts):

    print('Checking options for consistency')
    print('And rewriting if necessary')

    for key, value in opts.items():
        if key in ('average', 'colorbar', 'cut', 'nolabels', 'normalize'):
            if opts[key] is None:
                opts[key] = False

    if opts['axes'] is None:
        opts['axes'] = 'arcsec'
        print('Using default axes [arcsec]')
    else:
        if opts['axes'] not in ('au', 'arcsec'):
            print('Axes is either au or arcsec')
            sys.exit(1)
        if opts['axes'] == 'au' and opts['distance'] is None:
            print('Must specify a distance if using axes in au')
            sys.exit(1)

    if opts['mask'] is not None and opts['distance'] is None:
        print('Can\'t have a mask (defined in au) without a distance')
        sys.exit(1)

    if opts['scalebar'] is not None and opts['distance'] is None:
        print('Can\'t have a scalebar without a distance')
        sys.exit(1)

    if opts['radius'] is not None:
        if opts['axes'] == 'arcsec':
            print('Cannnot use arcsec axes with radius range')
            sys.exit(1)

    return opts


# ---------------------------------------------------------------------------- #

def get_options(options_file):

    # Check if options_file is available.
    print('')
    if options_file is not None:
        if exists(options_file):
            # Use options from json file.
            print('Using options file: \''+options_file+'\'')
            with open(options_file) as data_file:
                opts = json.load(data_file)
        else:
            print('Options file \'' + options_file + '\' does not exist')
            print('Check your files')
            sys.exit(1)
    else:
        # No options file available.
        opts = {'average':      False,
                'axes':         'arcsec',
                'beam':         False,
                'colorbar':     False,
                'contrast':     None,
                'convolve':     None,
                'coronagraph':  None,
                'cut':          False,
                'distance':     None,
                'log':          None,
                'mask':         None,
                'nolabels':     False,
                'noise':        None,
                'normalize':    False,
                'polarization': None,
                'radius':       None,
                'scalebar':     None,
                'scaling':      None}
        print('No options.json file specified')
        text = input('Would you like a default .json file? [y|n] ')
        if text == 'y':
            # Write default options file.
            print('Writing default options json file')
            set_options(opts, 'default')
            sys.exit(1)
        elif text == 'n':
            # Continue with default options.
            print('Using default options')
            opts = check_options(opts)
        else:
            print('Must answer with y or n')
            sys.exit(1)

    # Check consistency.
    opts = check_options(opts)

    return opts


# ---------------------------------------------------------------------------- #

def set_options(opts, filename):

    filename = filename + '.json'
    print('Writing current options to file: ' + filename)
    with open(filename, 'w') as fp:
        json.dump(opts, fp, sort_keys=True, indent=4)


# ---------------------------------------------------------------------------- #

def options_help():

    description = 'iplot = [i]mage [plot]'
    epilog = '''
options available in options file:

  average        azimuthally average                    T/F
  axes           axes units                             'au', 'arcsec'
  beam           plot beam                              T/F
  colorbar       add colorbar to plot                   T/F
  convolve       convolve with beam (BMAJ,BMIN,BPA)     [BMAJ,BMIN,BPA] (mas & deg.)
  contrast       scale intensity: vmax = con*max(img)   contrast (dimensionless)
  coronagraph    add coronagraph                        radius (in mas)
  cut            make a radial cut                      T/F
  distance       distance to object                     distance (in au)
  log            log plot                               'x', 'y', 'xy'
  mask           mask inner region                      radius (in au)
  nolabels       do not show axis labels                T/F
  noise          add noise                              [gain,fixed]
  normalize      normalize brightness                   T/F
  polarization   for scattered light images             'Q', 'Qphi', 'U', 'V'
  radius         minimum and maximum radius             [min,max] (in au)
  scalebar       add scalebar                           length (in au)
  scaling        scale intensity by R^p                 p
'''

    return description, epilog


# ---------------------------------------------------------------------------- #

def pixel_to_beam(flux, BMAJ, BMIN, pixel_size):
    '''
    Convert flux from unit per pixel to unit per beam
        flux
        BMAJ, BMIN [arcsec]
        pixel_size [arcsec]
    '''

    # Convert beam to radians.
    BMAJ = BMAJ * arcsec
    BMIN = BMIN * arcsec

    # Pixel to beam.
    flux = flux / (BMIN*BMAJ / pixel_size**2 * np.pi/4/np.log(2))

    return flux


# ---------------------------------------------------------------------------- #

def SI_to_mJy(flux, wl):
    '''
    Convert flux from W.m-2 per pixel (or beam) to mJy per pixel (or beam)
        flux [W.m-2]
        wl [cm]
        BMAJ, BMIN in [arcsec]
    '''

    # W.m-2/beam to W.m-2.Hz-1/beam.
    nu = c/wl
    flux = flux / nu

    # W.m-2.Hz-1/beam to mJy/beam.
    flux = flux / (Jy/1000)

    return flux


# ---------------------------------------------------------------------------- #

def Flux_to_Tbrightness(flux, wl, BMAJ, BMIN):
    '''
    From C. Pinte

    Convert flux [mJy] to brightness temperature [K]
        flux [mJy]
        wl [cm]
        BMAJ, BMIN in [arcsec]
        T [K]
    '''

    # Frequency.
    nu = c/wl

    # Convert beam to radians.
    BMAJ = BMAJ * arcsec
    BMIN = BMIN * arcsec

    # Convert flux to cgs.
    flux = flux * (Jy/1000)
    flux = flux / (BMIN*BMAJ * np.pi/4/np.log(2))

    # Check for bad values.
    flux[(flux < 0)] = np.min(flux[(flux > 0)])

    # Calculate temperature using Planck.
    exp_m1 = 2*h*nu**3/(flux*c**2)
    exp_m1[(exp_m1 < 1e-10)] = 1e-10
    hnu_kT = np.log(exp_m1 + 1)
    T = h*nu / (hnu_kT*kB)

    return T


# ---------------------------------------------------------------------------- #

def Tbrightness_to_Flux(T, wl, BMAJ, BMIN):
    '''
    From C. Pinte

    Convert brightness temperature [K] to flux density [mJy]
        T [K]
        wl [cm]
        BMAJ, BMIN in [arcsec]
        flux [mJy]
    '''

    # Frequency.
    nu = c/wl

    # Calculate flux.
    flux = 2*h*nu**3/(c**2) / (np.exp(h*nu/(kB*T)) - 1)

    # Convert beam to radians.
    BMAJ = BMAJ * arcsec
    BMIN = BMIN * arcsec

    # Convert flux to mJy.
    flux = flux / (Jy/1000)
    flux = flux * (BMIN*BMAJ * np.pi/4/np.log(2))

    return flux


# ---------------------------------------------------------------------------- #

def gauss_kernel2(npix,sigma_x,sigma_y,PA):
    '''
    From C Pinte.

    gauss_kernel2(npix,sigma_x,sigma_y,PA)
    sigma_x et y en pix PA en degres
    PA defini depuis la direction verticale dans le sens horaire
    Cree un noyau gaussien dont l'intégrale vaut 1
    Marche pour npix pair et impair
    SEE ALSO:
    '''

    if (sigma_x < 1.0e-30):
        sigma_x = 1.0e-30
    if (sigma_y < 1.0e-30):
        sigma_y = 1.0e-30

    PA = PA * pi / 180.

    centre = npix/2. - 0.5

    px = np.linspace(0,npix-1,npix)
    mx, my = np.meshgrid(px,px)
    mx = mx - centre
    my = my - centre

    x = mx * np.cos(PA) - my * np.sin(PA)
    y = mx * np.sin(PA) + my * np.cos(PA)

    x = x / sigma_x
    y = y / sigma_y

    dist2 = x**2 + y**2

    tmp = np.exp(-0.5*dist2)

    return tmp/sum(sum(tmp))


# ---------------------------------------------------------------------------- #

def convol2df(im,psf):
    '''
    From C Pinte.
    '''

    psf2 = im * 0.

    dx=im.shape[0]
    dy=im.shape[1]

    dx2=psf.shape[0]
    dy2=psf.shape[0]

    startx = int((dx-dx2)/2)
    starty = int((dy-dy2)/2)

    psf2[startx:startx+dx2,starty:starty+dy2] = psf

    fim = np.fft.fft2(im)
    fpsf = np.fft.fft2(psf2)

    fim = fim * fpsf

    im = np.fft.ifft2(fim)
    im = np.roll(im,(int(dx/2),int(dy/2)),(0,1))
    im = abs(im) / (dx*dy)

    return im


# ---------------------------------------------------------------------------- #

def radial_profile(data, center):

    y, x = np.indices((data.shape))
    r = np.sqrt((x - center[0])**2 + (y - center[1])**2)
    r = r.astype(np.int)

    tbin = np.bincount(r.ravel(), data.ravel())
    nr = np.bincount(r.ravel())
    radialprofile = tbin / nr

    return radialprofile


# ---------------------------------------------------------------------------- #

def save_figure(prefixes, opts, save_format='pdf'):

    # Generate figure.
    plt.close()
    generate_plot(prefixes, opts)

    # Save figure.
    filename, ext = os.path.splitext(save_format)
    if ext == '':
        save_format = filename
        filename = 'iplot'
    else:
        save_format = ext[1:]
    if save_format in ('pdf', 'png', 'jpeg'):
        filename = filename + '.' + save_format
        print('\nSaving plot as ' + filename)
        plt.savefig(filename, bbox_inches='tight')
        if save_format == 'pdf':
            os.system('pdfcrop %s %s &> /dev/null &' % (filename, filename))
    else:
        print('Save format should be pdf, png, or jpeg')


# ---------------------------------------------------------------------------- #

if __name__ == '__main__':

    # Get options.
    prefix, save_format, opts = get_command_line_opts()

    # Plot to screen or save figure.
    if save_format is not None:
        save_figure(prefix, opts, save_format)
    else:
        generate_plot(prefix, opts)
        plt.show()
