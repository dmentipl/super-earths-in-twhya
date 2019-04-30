# Calculate the minimum planet mass and gap width from Dipierro and Laibe (2017)
# from our TW Hya model.
#
# D. Mentiplay. 2018
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------- #

sun_to_earth = 1.989e33/5.972e27

# ---------------------------------------------------------------------------- #

size = 1
dust_to_gas = 0.05
p = 0.5
q = 0.125
zeta = - (p + q + 3/2)
alphaSS = 1e-3
Rin = 10
Rref = 10
H_Rref = 0.034
sig_norm = 0.265
disc_m = 7.5e-4
sig_dust_norm = 0.017

print('')
print('Dust-to-gas ratio is',dust_to_gas)
print('Grain size is',size,'mm')
print('p is',p)
print('q is',q)
print('zeta is',zeta)
print('alphaSS is',alphaSS)
print('')
print('--------------------------------------------------------------------------------')
print('')

# ---------------------------------------------------------------------------- #

def sigma(R):
    return sig_norm * (R / Rref)**(-p) * (1 - np.sqrt(Rin/R))

def sigmadust(R):
    return sig_dust_norm

def St(R):
    return (0.2/(sigma(R)+1e-6)) * size

def H_R(R):
    return H_Rref * (R / Rref)**(1/2 - q)

def eps(R):
    return sigmadust(R)/sigma(R) / np.sqrt(alphaSS/St(R))

# ---------------------------------------------------------------------------- #

def Mp(R):
    '''
    Minimum planet mass.
    '''
    # 0.8 from stellar mass
    # epsilon = eps(R)
    epsilon = dust_to_gas
    return 0.8*sun_to_earth * 1.38 * (-zeta/(1+epsilon))**(3/2) * St(R)**(-3/2) \
            * (H_R(R))**3

def dgap(R,Mp):
    '''
    Gap width.
    '''
    # epsilon = eps(R)
    epsilon = dust_to_gas
    return 0.87 * (-zeta/(1+epsilon))**(-1/4) * St(R)**(1/4) * (H_R(R))**(-1/2) \
            * (Mp/sun_to_earth)**(1/2)

# ---------------------------------------------------------------------------- #

Rvals = [24,41,94]
for R in Rvals:
    print('R =',R,'au')
    print('H_R =',round(H_R(R),4))
    print('St =',round(St(R),1))
    print('dust-to-gas =',dust_to_gas)
    print('eps = ',round(eps(R),2))
    print('Minimum planet mass at',R,'au is',round(Mp(R),1),'M_E')
    print('')

print('')
print('--------------------------------------------------------------------------------')
print('')

Rvals = [24,41]
Mpvals = [4,8,16,24]
for R in Rvals:
    print('R = ',R,'au')
    print('----------')
    for Mp in Mpvals:
        print('      Gap width for Mp =',Mp,'M_E is  ',round(dgap(R,Mp),3),'au')
        print('total gap width for Mp =',Mp,'M_E is ~',round(4*dgap(R,Mp),3),'au')
        print('')
    print('')

print('NOTE: gap width is distance from planet to outer edge')
print('      this is smaller than total gap width by a factor of a few')

RR = np.linspace(20,60)
plt.plot(RR,eps(RR))
plt.show()
