import numpy as np
import warnings

warnings.filterwarnings("ignore")


class Fourier(object):
    def __init__(self, param):
        list_param = ['Lx', 'Ly', 'nx', 'ny',
                      'typewave', 'g', 'H', 'BVF',
                      'beta', 'Rd', 'f0', 'ageos',
                      'gammarho']
        param.copy(self, list_param)

        self.x, self.kx = set_x_and_k(self.nx, self.Lx)
        self.y, self.ky = set_x_and_k(self.ny, self.Ly)

        self.xx, self.yy = np.meshgrid(self.x, self.y)
        self.kxx, self.kyy = np.meshgrid(self.kx, self.ky)
        self.ktot = np.sqrt(self.kxx**2+self.kyy**2)

        if self.typewave == 'gw':
            self.omega = np.sqrt(self.g*self.ktot*np.tanh(self.H*self.ktot))
            self.p2u = self.kxx/self.omega
            self.p2v = self.kyy/self.omega
            self.p2u[self.omega == 0] = 0.
            self.p2v[self.omega == 0] = 0.

        if self.typewave == 'gwshort':
            self.omega = np.sqrt(self.g*self.ktot)
            self.p2u = self.kxx/self.omega
            self.p2v = self.kyy/self.omega
            self.p2u[self.omega == 0] = 0.
            self.p2v[self.omega == 0] = 0.

        if self.typewave == 'capillary':
            self.omega = np.sqrt(self.g*self.ktot+self.gammarho*self.ktot**3)
            self.p2u = self.kxx/self.omega
            self.p2v = self.kyy/self.omega
            self.p2u[self.omega == 0] = 0.
            self.p2v[self.omega == 0] = 0.

        if self.typewave == 'gwlong':
            self.omega = np.sqrt(self.g*self.H)*self.ktot
            self.p2u = self.kxx/self.omega
            self.p2v = self.kyy/self.omega
            self.p2u[self.omega == 0] = 0.
            self.p2v[self.omega == 0] = 0.

        if self.typewave == 'inertiagravity':
            self.omega = np.sqrt(self.f0**2 + self.g*self.H*self.ktot**2)
            self.p2u = (self.omega*self.kxx+1j*self.f0*self.kyy) / (self.g*self.H*self.ktot**2)
            self.p2v = (self.omega*self.kyy-1j*self.f0*self.kxx) / (self.g*self.H*self.ktot**2)
            self.p2u[self.ktot == 0] = 0.
            self.p2v[self.ktot == 0] = 0.

        if self.typewave == 'internal':
            self.omega = self.BVF*np.abs(self.kxx)/self.ktot
            self.omega[self.ktot == 0] = 0.
            self.p2u = self.kxx/self.omega
            self.p2v = self.kyy/(self.omega-self.BVF**2/self.omega)
            self.p2u[self.omega == 0] = 0
            self.p2v[self.omega == 0] = 0
            self.p2v[self.omega == self.BVF] = 0

        if self.typewave == 'rossby':
            self.omega = -self.beta*self.kxx/(self.ktot**2+self.Rd**-2)
            self.p2u = +1j*self.kyy/self.f0
            self.p2v = -1j*self.kxx/self.f0
            if self.ageos:
                pp2u = -1j*self.p2v*self.omega/self.f0
                self.p2v = +1j*self.p2u*self.omega/self.f0
                self.p2u = pp2u

    def compute_all_variables(self, hphi):
        var = {}
        if self.typewave in ['gw', 'gwshort', 'gwlong', 'internal', 'rossby', 'inertiagravity']:
            pp = np.fft.ifft2(hphi)
            p = np.real(pp)
            amp = np.abs(pp)
            u = np.real(np.fft.ifft2(hphi*self.p2u))
            v = np.real(np.fft.ifft2(hphi*self.p2v))
            var['p'] = p
            var['abs'] = amp
            var['u'] = u
            var['v'] = v
            var['up'] = u*p
            var['vp'] = v*p

        return var

    def compute_balanced_wake(self, hphi, U, epsilon=0.3):
        """ ref: Raphael and de Gennes, PRE 1996 """
        ktot = self.ktot
        omega = self.omega
        kxx = self.kxx

        def zeta_epsilon(hphi, eps0):
            den = omega**2-(U*kxx)**2 - 2*1j*eps0*U*kxx
            hzeta = hphi*ktot/den
            hzeta[den == 0] = 0.
            return -np.real(np.fft.ifft2(hzeta))

        zeta1 = zeta_epsilon(hphi, epsilon*1.01)
        zeta0 = zeta_epsilon(hphi, epsilon*0.99)
        return (zeta1 - zeta0)/(0.02*epsilon)


def set_x_and_k(n, L):
    k = ((n//2+np.arange(n)) % n) - n//2
    return (np.arange(n)+0.5)*L/n, 2*np.pi*k/L
