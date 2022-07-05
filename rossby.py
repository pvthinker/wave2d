"""Rossby waves

The deformation radius param.Rd is chosen such that the initial wave
packet width is in the short wavelength regime

\omega \sim -\frac{\beta k_x}{k_x^2 + k_y^2}

in which waves are dispersive.

TODO:

  1) run the code as is and observe the banana shape pattern

  2) set param.plotvector = 'velocity' and rerun. The velocity is along
    the isobares.

  3) set param.plotvector = 'velocity' and param.ageostrophic =
    True. Observe the difference

  4) set param.plotvector = 'energyflux' and param.ageostrophic =
  False. Observe that there is no energy flux! How's that possible?...

  5) set param.plotvector = 'energyflux' and param.ageostrophic =
  True. Now you see the energy flux! and it is ... eastward because it
  is the short wave regime.

"""
import numpy as np
import namelist
import wave2d


param = namelist.Namelist()
param.typewave = 'rossby'
param.generation = 'initial'
param.waveform = 'gaussian'

param.sigma = 0.05*param.Lx
param.aspect_ratio = 1.

param.varplot = 'p'

param.nx, param.ny = 128*4, 128*2
param.Lx, param.Ly = 4, 2
param.x0, param.y0 = 2., 1.0

param.g = 20.
param.H = .01
param.beta = 1.
param.Rd = .1
cg = 1.0
param.beta = cg/param.Rd**2
param.omega0 = 5.

param.tend = 3.
param.tplot = .05

param.plotvector = 'None'  # 'energyflux' , 'velocity'  , 'None'

# False -> geostrophic velocity
# True -> ageostrophic velocity
param.ageos = False

param.vectorscale = 10.
param.dt = 1e-2

param.U = .6
param.alphaU = 0*np.pi/180.

param.cax = np.asarray([-1., 1.])*2e-1
param.figwidth = 1080

model = wave2d.Wave2d(param)
model.set_fourier_space(param)
model.set_wave_packet(param)
model.run(param)
