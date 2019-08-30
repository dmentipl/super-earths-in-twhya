import numpy as np
import matplotlib.pyplot as plt
from iplot import generate_plot

opts = {"average":      True,
        "axes":         "au",
        "beam":         [48.5,48.5,127],
        "colorbar":     False,
        "contrast":     None,
        "convolve":     True,
        "coronagraph":  None,
        "cut":          True,
        "log":          "x",
        "mask":         None,
        "noise":        [1.2,0],
        "nolabels":     False,
        "normalize":    True,
        "polarization": "Qphi",
        "radius":       [25,200],
        "scalebar":     None,
        "scaling":      2}

if False:

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
    for idx in range(4):
        generate_plot(prefixes=prefixes[idx], opts=opts)

        dat = np.loadtxt('van-boekel-2017-radius-gaia-vs-brightness.txt')
        r = dat[:,0]
        b = dat[:,1]
        rr = r[(r > 25) & (r < 200)]
        bb = b[(r > 25) & (r < 200)]
        plt.plot(rr,bb,color='r',linestyle='-')
        plt.savefig('scattered-intensity-comparison-' + '{:.1f}'.format(masses[idx]) + '.pdf')

if True:

    prefixes = ['twhya-1.6-2018-05-06a',
                'twhya-1.6-2018-05-06b',
                'twhya-1.6-2018-05-06c',
                'twhya-1.6-2018-05-06d']

    generate_plot(prefixes=prefixes, opts=opts)

    dat = np.loadtxt('van-boekel-2017-radius-gaia-vs-brightness.txt')
    r = dat[:,0]
    b = dat[:,1]
    rr = r[(r > 25) & (r < 200)]
    bb = b[(r > 25) & (r < 200)]
    plt.plot(rr,bb,color='r',linestyle='-')
    plt.savefig('scattered-radial-comparison.pdf')

if False:
    plt.show()
