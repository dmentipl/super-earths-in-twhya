import numpy as np
import matplotlib.pyplot as plt
from iplot import generate_plot

opts_radial = {"average":      True,
               "axes":         "au",
               "beam":         [56,48,127],
               "colorbar":     False,
               "contrast":     None,
               "convolve":     True,
               "coronagraph":  None,
               "cut":          True,
               "log":          "x",
               "mask":         None,
               "noise":        None,
               "nolabels":     False,
               "normalize":    True,
               "polarization": "Qphi",
               "radius":       [25,200],
               "scalebar":     None,
               "scaling":      2}

opts_image = {"average":      False,
              "axes":         "arcsec",
              "beam":         [56,48,127],
              "colorbar":     False,
              "contrast":     None,
              "convolve":     True,
              "coronagraph":  None,
              "cut":          False,
              "log":          None,
              "mask":         None,
              "noise":        None,
              "nolabels":     False,
              "normalize":    True,
              "polarization": "Qphi",
              "radius":       None,
              "scalebar":     None,
              "scaling":      2}

prefixes = [['010/twhya-1.6-2018-05-06a',
             '032/twhya-1.6-2018-05-06a',
             '100/twhya-1.6-2018-05-06a'],
            ['010/twhya-1.6-2018-05-06b',
             '032/twhya-1.6-2018-05-06b',
             '100/twhya-1.6-2018-05-06b'],
            ['010/twhya-1.6-2018-05-06c',
             '032/twhya-1.6-2018-05-06c',
             '100/twhya-1.6-2018-05-06c'],
            ['010/twhya-1.6-2018-05-06d',
             '032/twhya-1.6-2018-05-06d',
             '100/twhya-1.6-2018-05-06d']]

masses = [0.1, 0.3, 1, 2]

dat = np.loadtxt('van-boekel-2017-radius-gaia-vs-brightness.txt')
r = dat[:,0]
b = dat[:,1]
rr = r[(r > 25) & (r < 200)]
bb = b[(r > 25) & (r < 200)]

for idx in range(len(masses)):
    generate_plot(prefixes=prefixes[idx], opts=opts_image)
    plt.savefig('scattered-image-' + '{:.1f}'.format(masses[idx]) + '.pdf')

for idx in range(len(masses)):
    generate_plot(prefixes=prefixes[idx], opts=opts_radial)
    plt.plot(rr,bb,color='r',linestyle='-')
    plt.savefig('scattered-radial-' + '{:.1f}'.format(masses[idx]) + '.pdf')
