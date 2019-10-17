import numpy as np
import matplotlib.pyplot as plt
from iplot import generate_plot

opts = {"average":      True,
        "axes":         "au",
        "beam":         False,
        "colorbar":     False,
        "contrast":     None,
        "convolve":     [139,131,-74.9],
        "coronagraph":  None,
        "cut":          True,
        "distance":     59.5,
        "log":          None,
        "mask":         None,
        "noise":        None,
        "nolabels":     False,
        "normalize":    True,
        "polarization": None,
        "radius":       [30,200],
        "scalebar":     None,
        "scaling":      None}


prefixes = ['twhya-CO-2018-05-06a',
            'twhya-CO-2018-05-06b',
            'twhya-CO-2018-05-06c',
            'twhya-CO-2018-05-06d']
generate_plot(prefixes=prefixes, opts=opts)

dat = np.loadtxt('./CO-radial.txt')
r = dat[:,0]
b = dat[:,1]
if True:
    rr = r[(r > 30) & (r < 200)]
    bb = b[(r > 30) & (r < 200)]
    bb = bb / np.max(bb)
else:
    rr = r
    bb = b
plt.plot(rr,bb,color='r',linestyle='-')
plt.savefig('huang-CO-comparison.pdf', bbox_inches='tight')
if False:
    plt.show()
