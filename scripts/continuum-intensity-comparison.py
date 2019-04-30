from astropy import constants
from astropy import units
import numpy as np
import matplotlib.pyplot as plt
from iplot import get_options, generate_plot

# convert to temperature brightness?
Tbrightness = False

# constants
c = constants.c.cgs.value
h = constants.h.cgs.value
kB = constants.k_B.cgs.value
arcsec = units.arcsec.cgs.scale
mas = units.mas.cgs.scale
Jy = units.Jansky.cgs.scale

# get model data
opts = get_options('alma-radial.json')
generate_plot(prefixes=['twhya-alma-2018-03-02b',
                        'twhya-alma-2018-03-12a',
                        'twhya-alma-2018-03-02a',
                        'twhya-alma-2018-03-13a'],
              opts=opts)

# get ALMA data
dat = np.loadtxt('andrews-2016-continuum-brightness.txt')
r = dat[:,0]
b = dat[:,1]

# ---------------------------------------------------------------------------- #

def Tbrightness_to_Flux(T, wl, BMAJ, BMIN):
    '''
    From C. Pinte

    Convert brightness temperature [K] to flux density [mJy]
        T [K]
        wl [cm]
        BMAJ, BMIN in [mas]
        flux [mJy]
    '''

    # Frequency.
    nu = c/wl

    # Calculate flux.
    flux = 2*h*nu**3/(c**2) / (np.exp(h*nu/(kB*T)) - 1)

    # Convert beam to radians.
    BMAJ = BMAJ * mas
    BMIN = BMIN * mas

    # Convert flux to mJy.
    flux = flux / (Jy/1000)
    flux = flux * (BMIN*BMAJ * np.pi/4/np.log(2))

    return flux


# ---------------------------------------------------------------------------- #

if Tbrightness:
    wl = 870 * 1e-4
    BMAJ = 30
    BMIN = 30
    b = Tbrightness_to_Flux(b, wl, BMAJ, BMIN)

rr = r[(r > 10) & (r < 70)]
bb = b[(r > 10) & (r < 70)]
plt.plot(rr,bb,color='r',linestyle='-')
if Tbrightness:
    plt.savefig('dust-thermal-comparison-Tb.pdf')
else:
    plt.savefig('dust-thermal-comparison-Sb.pdf')
plt.show()
