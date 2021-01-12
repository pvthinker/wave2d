import xarray as xr

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation    

file = 'history.nc'
variable = 'p'
xmin, xmax = 0, 4
ymin, ymax = 0, 2

ds = xr.open_dataset(file)

# This part is a fast adaptation of the window shape
ny, nx = ds[variable][0].shape
if nx == ny:
    shape_window = (8,8)
else:
    shape_window = (12,5)
 
fps = 10 #Set up the number of image / second (animation speed)
snapshots = ds[variable]

# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure( figsize=shape_window )
a = snapshots[0]
im = plt.imshow(a.T, cmap='coolwarm', extent=[xmin,xmax,ymin,ymax]) 
plt.xlabel('X')
plt.ylabel('Y')
plt.clim(-1,1) #Set up here the limits of colorbar
plt.colorbar(label=variable)

def animate_func(i):
    if i % fps == 0:
        print( '.', end ='' )

    im.set_array(snapshots[i])
    return [im]

anim = animation.FuncAnimation(
                               fig, 
                               animate_func, 
                               frames = len(ds[variable]),
                               interval = 1000 / fps, # in ms
                               )
anim.save('animation.gif', writer='PillowWriter')

print('Done!')