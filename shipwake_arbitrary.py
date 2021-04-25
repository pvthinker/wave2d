import numpy as np
import namelist
import wave2d
import pickle

import matplotlib.pyplot as plt
plt.ion()

param = namelist.Namelist()
param.typewave = 'gwshort'


param.nx, param.ny = 128*4, 128*2
param.Lx, param.Ly = 2, 1
param.g = 1.
param.H = .1
param.sigma = 0.005*param.Lx  # ship length
param.tend = 4*np.pi
param.tplot = .1
param.dt = 10e-3
param.x0 = 1.

param.alphaU = 30*np.pi/180.

param.cax = np.asarray([-1., 1.])
param.figwidth = 1080

param.aspect_ratio = 4.  # for the ship, between x and y lengths
param.U = 0.15
param.r = 0.3

param.motion = "circular_uniform"


class Trajectory(object):
    def __init__(self, param):
        self.param = param
        self.dt = 1e-6
        self.omega = param.U/param.r

    def get_position(self, time):
        if self.param.motion == "circular_uniform":
            theta = self.omega*time
            x = self.param.r * np.cos(theta)
            y = self.param.r * np.sin(theta)
        elif self.param.motion == "rect_uniform":
            theta = self.param.alphaU
            x = self.param.U*np.cos(theta)*time
            y = self.param.U*np.sin(theta)*time
        elif self.param.motion == "wavy":
            theta = self.omega*time*2
            x = self.param.U*time
            y = self.param.U/10*np.sin(theta)*time
        else:
            raise ValueError(f"{param.motion} is not defined")
        # add you own motion here !
        return (x, y)

    def get_velocity(self, time):
        x1, y1 = self.get_position(time+self.dt)
        x0, y0 = self.get_position(time-self.dt)
        vx = (x1-x0)/(2*self.dt)
        vy = (y1-y0)/(2*self.dt)
        return (vx, vy)


model = wave2d.Wave2d(param)
model.traj = Trajectory(param)
model.run(param, anim=True)

# dt = param.dt
# en = model.energy
# time = np.arange(0, len(en))*dt
# drag = np.mean(np.diff(en)[-50:]/dt) / param.U
# print('Estimated drag: %.3g / U = %.2f' % (drag, param.U))
