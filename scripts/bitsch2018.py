import numpy as np

alpha = 0.001
p = 0.5
q = 0.125
H_Rref = 0.034
Rin = 10
Rref = 10
dlnP_dlnR = p + q + 3/2
sig_norm = 0.265

def H_R(R):
    return H_Rref * (R / Rref)**(1/2 - q)

def sigma(R):
    return sig_norm * (R / Rref)**(-p) * (1 - np.sqrt(Rin/R))


R = 94

sizes = [0.1,1,10]
for size in sizes:
    print('size =',size)
    def St(R):
        return (0.2/(sigma(R)+1e-6)) * size

    f_fit = (H_R(R)/0.05)**3 * (0.34 * (np.log(0.001)/np.log(alpha))**4 + 0.66) * (1 - (dlnP_dlnR + 2.5)/6)
    M_iso = 25 * f_fit
    print('M_iso withou diffusion = ',M_iso)

    M_iso = 25 * f_fit * (1 + alpha/(2*St(R)*0.00476))
    print('M_iso with diffusion = ',M_iso)
