import numpy as np
import namelist
import wave2d

import matplotlib.pyplot as plt
plt.ion()

param = namelist.Namelist()
param.typewave = 'internal'
param.generation = 'oscillator'
param.omega0 = 6.
param.waveform = 'gaussian'
param.sigma = 0.05*param.Lx/8
param.x0, param.y0 = 1.5, 1. # wavemaker location
param.aspect_ratio = 1.

param.varplot = 'p'

param.nx, param.ny = 128*4, 128*4
param.Lx, param.Ly = 3, 2

param.BVF = 20.

param.tend = 4.
param.tplot = .05
param.plotvector = 'None'
param.vectorscale = 1.
param.dt = 1e-2

param.U = .4
param.alphaU = -30*np.pi/180.

param.cax = np.asarray([-1., 1.])
param.figwidth = 1080

model = wave2d.Wave2d(param)
model.set_fourier_space(param)
model.set_wave_packet(param)
model.run(param)
