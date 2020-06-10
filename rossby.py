import numpy as np
import namelist
import wave2d

import matplotlib.pyplot as plt
plt.ion()

# to get the list of all parameters and their available values
# use param.manall() in your IPython console or in your Jupyter notebook

param = namelist.Namelist()
param.typewave = 'rossby'
param.generation = 'initial'
param.waveform = 'gaussian'

param.sigma = 0.05*param.Lx
param.aspect_ratio = 1.

param.varplot = 'p'

param.nx, param.ny = 128*4, 128*4
param.Lx, param.Ly = 3, 2
param.x0, param.y0 = 1., 1.0

param.g = 20.
param.H = .01
param.beta = 1.
param.Rd = 0.0001
cg = 1.0
param.beta = cg/param.Rd**2
param.omega0 = 5.

param.tend = 3.
param.tplot = .1
param.ageos = False
param.plotvector = 'None'  # 'velocity'
param.vectorscale = 10.
param.dt = 1e-2

param.U = .6
param.alphaU = 0*np.pi/180.

param.cax = np.asarray([-1., 1.])*5e-3
param.figwidth = 1080

model = wave2d.Wave2d(param)
model.set_fourier_space(param)
model.set_wave_packet(param)
model.run(param)
