import numpy as np
import namelist
import wave2d

import matplotlib.pyplot as plt
plt.ion()

# to get the list of all parameters and their available values
# use param.manall() in your IPython console or in your Jupyter notebook

param = namelist.Namelist()
param.typewave = 'gwshort'  # 'gwshort', 'inertiagravity', 'internal', 'rossby'
param.generation = 'initial'
param.omega0 = 5.
param.waveform = 'gaussian'

param.sigma = 0.02*param.Lx
param.aspect_ratio = 1.

param.varplot = 'p'

param.nx, param.ny = 128*2, 128
param.Lx, param.Ly = 4, 2
param.x0, param.y0 = 1., 1.0

param.g = 1.
param.H = 1.
param.f0 = 20.
param.beta = 500.
param.Rd = 0.05
cg = 1.0
param.beta = cg/param.Rd**2
param.BVF = 20.

param.tend = 2.
param.tplot = .02
param.plotvector = 'None'
param.vectorscale = 10. # larger 'vectorscale' makes the arrows shorter
param.dt = 1e-2

param.netcdf = True # set it to True to save the NetCDF file

param.U = .6
param.alphaU = 0*np.pi/180.

param.cax = np.asarray([-1., 1.])
param.figwidth = 1080

model = wave2d.Wave2d(param)
model.set_fourier_space(param)
model.set_wave_packet(param)
model.run(param)

#plt.figure(2)
#plt.plot(model.energy)
