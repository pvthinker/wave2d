import numpy as np
import namelist
import wave2d

#import matplotlib.pyplot as plt
#plt.ion()

# to get the list of all parameters and their available values
# use param.manall() in your IPython console or in your Jupyter notebook

param = namelist.Namelist()
param.typewave = 'gwlong'
param.generation = 'initial'
param.omega0 = 40.
param.waveform = 'gaussian'

param.sigma = 0.02*param.Lx
param.aspect_ratio = 1.

param.varplot = 'p'

param.nx, param.ny = 128*4, 128*2
param.Lx, param.Ly = 4, 2
param.x0, param.y0 = 2., 1.

param.g = 1.
param.H = 1.
param.beta = 500.
param.Rd = 0.05
cg = 1.0
param.beta = cg/param.Rd**2
param.BVF = 20.

param.tend = 1.5
param.tplot = .04  # smaller 'tplot' makes the animation smoother
param.plotvector = 'None'  # 'velocity'
param.vectorscale = 20.  # larger 'vectorscale' makes the arrows shorter
param.dt = 0.02
param.macuser = False # <- try True if the animation does not work

param.U = .2
param.alphaU = 0*np.pi/180.

param.cax = np.asarray([-1., 1.])*.25
param.figwidth = 1080

model = wave2d.Wave2d(param)
model.set_fourier_space(param)
model.set_wave_packet(param)
model.run(param)

