from __future__ import print_function
import numpy as np

import plotting
import fourier
import wavepackets as wp
import nc_tools as nct
from netCDF4 import Dataset

import matplotlib.pyplot as plt
plt.ion()


class Wave2d(object):
    def __init__(self, param):
        param.checkall()
        self.set_fourier_space(param)
        self.set_wave_packet(param)

    def set_fourier_space(self, param):
        fspace = fourier.Fourier(param)
        self.fspace = fspace

    def set_wave_packet(self, param, heading=None):
        if heading is None:
            alphaU = param.alphaU
        else:
            alphaU = heading
        sigma = param.sigma
        aspect_ratio = param.aspect_ratio
        x0, y0 = param.x0, param.y0
        xx, yy = self.fspace.xx, self.fspace.yy
        z = (xx-x0) + 1j*(yy-y0)
        z = z*np.exp(-1j*alphaU)

        if param.waveform == 'gaussian':
            d2 = np.real(z)**2 + (aspect_ratio*np.imag(z))**2
            phi0 = np.exp(-d2/(2*sigma**2))

        elif param.waveform == 'triangle':
            phi0 = wp.triangle(np.real(z), aspect_ratio *
                               np.imag(z), param.sigma)

        elif param.waveform == 'square':
            phi0 = wp.square(np.real(z), aspect_ratio*np.imag(z), param.sigma)

        elif param.waveform == 'packet':
            kxx = self.fspace.kxx
            kyy = self.fspace.kyy

            Lx = param.Lx
            k0x = self.fspace.kx[60]
            k0y = self.fspace.kx[30]
            sigma = 10.

            d2 = ((kxx-k0x)*k0x+(kyy-k0y)*k0y)**2
            d2 += 20*((kxx-k0x)*k0y-(kyy-k0y)*k0x)**2
            d2 /= (k0x**2+k0y**2)

            hphi = np.exp(-d2/(2*sigma**2)) * np.exp(1j*(kxx*x0+kyy*y0))

            hphi *= np.sqrt(param.nx*param.ny)
            self.hphi0 = hphi

            phi0 = np.real(np.fft.ifft2(hphi))

        self.phi0 = phi0
        if param.waveform != 'packet':
            self.hphi0 = np.fft.fft2(self.phi0)
        self.boat = self.hphi0

    def run(self, param, anim=True):

        if param.generation in ['wake', 'oscillator']:
            hphi = self.hphi0.copy()*0

        else:
            hphi = self.hphi0.copy()

        if anim:
            self.plot = plotting.Plotting(param)
            var = self.fspace.compute_all_variables(hphi)
            if param.plotvector == 'velocity':
                self.plot.init_figure(self.phi0, u=var['u'], v=var['v'])

            elif param.plotvector == 'energyflux':
                self.plot.init_figure(self.phi0, u=var['up'], v=var['vp'])

            else:
                self.plot.init_figure(self.phi0)

        tend = param.tend
        dt = param.dt
        nt = int(tend/dt)
        kxx, kyy = self.fspace.kxx, self.fspace.kyy
        omega = self.fspace.omega
        propagator = np.exp(-1j*omega*dt)

        sigma = param.sigma
        aspect_ratio = param.aspect_ratio
        x0, y0 = param.x0, param.y0
        xx, yy = self.fspace.xx, self.fspace.yy

        time = 0.
        kplot = np.ceil(param.tplot/dt)
        xb, yb = param.x0+param.Lx/2, param.y0+param.Ly/2
        xb, yb = 0, 0  # param.x0, param.y0
        energy = np.zeros((nt,))
        if param.netcdf:
            attrs = {"model": "wave2d",
                     "wave": param.typewave}

            sizes = {"y": param.ny, "x": param.nx}

            variables = [{"short": "time",
                          "long": "time",
                          "units": "s",
                          "dims": ("time")},
                         {"short": "p",
                          "long": "pressure anomaly",
                          "units": "m^2 s^-2",
                          "dims": ("time", "y", "x")},
                         {"short": "u",
                          "long": "velocity x-component",
                          "units": "m s^-1",
                          "dims": ("time", "y", "x")},
                         {"short": "v",
                          "long": "velocity y-component (or z-)",
                          "units": "m s^-1",
                          "dims": ("time", "y", "x")},
                         {"short": "up",
                          "long": "up flux x-component",
                          "units": "m^3 s^-3",
                          "dims": ("time", "y", "x")},
                         {"short": "vp",
                          "long": "vp flux y-component",
                          "units": "m^3 s^-3",
                          "dims": ("time", "y", "x")}
                         ]

            fid = nct.NcTools(variables, sizes, attrs,
                              ncfilename=param.filename)
            fid.createhisfile()
            ktio = 0

        for kt in range(nt):
            energy[kt] = 0.5*np.mean(np.abs(hphi.ravel())**2)
            hphi = hphi*propagator

            if param.generation == 'wake':

                if hasattr(self, "traj"):

                    xb, yb = self.traj.get_position(time)
                    vx, vy = self.traj.get_velocity(time)

                    kalpha = vx*kxx+vy*kyy
                    # recompute self.boat (complex Fourier amplitude)
                    # to account for the new heading
                    heading = np.angle(vx+1j*vy)
                    self.set_wave_packet(param, heading)
                    # shift the source at the boat location (xb,yb)
                    shift = np.exp(-1j*(kxx*xb+kyy*yb))
                    # add the source term to hphi
                    hphi -= 1j*dt*self.boat*kalpha*shift
                else:
                    if kt == 0:
                        kalpha = np.cos(param.alphaU)*kxx + \
                            np.sin(param.alphaU)*kyy
                    hphi -= (1j*1e2*dt*self.boat*param.U*kalpha) * \
                        np.exp(-1j*(kxx*xb+kyy*yb))
                    xb += dt*param.U*np.cos(param.alphaU)
                    yb += dt*param.U*np.sin(param.alphaU)

            elif param.generation == 'oscillator':
                hphi += (1e2*dt*self.boat)*np.exp(-1j*time*param.omega0)

            kt += 1
            time += dt

            if anim:
                if (kt % kplot == 0):
                    var = self.fspace.compute_all_variables(hphi)
                    z2d = var[param.varplot]
                    self.var = var
                    if param.plotvector == 'velocity':
                        self.plot.update(kt, time, z2d, u=var['u'], v=var['v'])
                    elif param.plotvector == 'energyflux':
                        self.plot.update(
                            kt, time, z2d, u=var['up'], v=var['vp'])
                    else:
                        self.plot.update(kt, time, z2d)

                    if param.netcdf:
                        with Dataset(param.filename, "r+") as nc:
                            nc.variables["time"][ktio] = time
                            nc.variables["p"][ktio, :, :] = z2d
                            for v in ["u", "v", "up", "vp"]:
                                nc.variables[v][ktio, :, :] = var[v]

                            ktio += 1
            else:
                print('\rkt=%i / %i' % (kt, nt), end='')

        var = self.fspace.compute_all_variables(hphi)
        self.energy = energy
        self.var = var
