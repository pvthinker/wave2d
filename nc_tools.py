import numpy as np
from netCDF4 import Dataset

class NcTools(object):
    def __init__(self, variables, sizes, attrs, ncfilename="history.nc"):
        self.attrs = attrs
        self.variables = variables
        self.sizes = sizes
        self.ncfilename = ncfilename

    def createhisfile(self):
        with Dataset(self.ncfilename, "w") as nc:
            nc.setncatts(self.attrs)
            nc.createDimension("time")
            for dim, size in self.sizes.items():
                nc.createDimension(f"{dim}", size)
            #
            for var in self.variables:
                shortn = var["short"]
                longn  = var["long"]
                units = var["units"]
                dims = var["dims"]

                v = nc.createVariable(shortn, float, dims)
                v.long_name = longn
                v.units = units

if __name__ == "__main__":
    nx, ny = 100, 50
    shape = (ny, nx)

    attrs = {"model": "wave2d",
             "wave": "gwlong"}

    sizes = {"y": ny, "x": nx}

    variables = [{"short": "time",
                  "long": "time",
                  "units": "s",
                  "dims": ("time")},
                 {"short": "p",
                  "long": "pressure anomaly",
                  "units": "m s^-1",
                  "dims": ("time", "y", "x")}]
    
    nct = NcTools(variables, sizes, attrs)
    nct.createhisfile()

    dt = 0.1
    p0 = np.random.uniform(size=shape)
    with Dataset(nct.ncfilename, "r+") as nc:
        for kt in range(50):
            t = kt*dt
            nc.variables["time"][kt] = t
            dx = 4*t
            dy = 10*np.sin(t/2)
            p = np.roll(np.roll(p0, int(dy), axis=0), int(dx), axis=1)
            nc.variables["p"][kt,:,:] = p
