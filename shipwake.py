import numpy as np
import namelist
import wave2d
import pickle

import matplotlib.pyplot as plt
plt.ion()

param = namelist.Namelist()
param.typewave = 'gwlong'


param.nx, param.ny = 128*8, 128*4
param.Lx, param.Ly = 2, 1
param.g = 1.
param.H = .1
param.sigma = 0.01*param.Lx  # ship length
param.tend = 2.5
param.tplot = .1
param.dt = 1e-2

param.alphaU = 0*np.pi/180.

param.cax = np.asarray([-1., 1.])*5
param.figwidth = 1080

param.aspect_ratio = 4.  # for the ship, between x and y lengths
param.U = 0.3

model = wave2d.Wave2d(param)
model.run(param, anim=True)

dt = param.dt
en = model.energy
time = np.arange(0, len(en))*dt
drag = np.mean(np.diff(en)[-50:]/dt) / param.U
print('Estimated drag: %.3g / U = %.2f' % (drag, param.U))
