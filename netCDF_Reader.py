import xarray as xr

import numpy as np

import matplotlib
import matplotlib.pyplot as plt

import matplotlib.animation as animation    


class Wave:
    
    """
    A class to represent a wave builded with wave2d

    ...

    Attributes
    ----------
    data : str
        data extracted from netCDF file

    Methods
    -------
    variable_list(self):
        Print the list of available variables
        
    animate(self, variable, args):
        Build an animation of a given variable
    """
    
    def __init__(self, data=None,
                 **kwargs):
        self.data = data
        
    def variable_list(self):
        
        """
        Print the list of available variables
        
        """
        print(self.data.data_vars)
        
    def animate(self, variable, fps=10, xmin=0, xmax=4, ymin=0, ymax=2, cmap='coolwarm', cmin=-1, cmax=1, output='animation', figsize=(12,5), save=True):
        
        """
        Build an animation
        
        Parameters
        ----------
        variable: str
            Variable to display
            
        fps: int, default=10
            Number of images per second
            
        xmin, xmax, ymin, ymax: 4* float, default= 0, 4, 0, 2
            Limits of the domain
            
        cmap: str, default='coolwarm'
            Colormap to use
            
        cmin, cmax: 2* float, default=-1, 1
            Limits of colorbar
            
        output: str, default='animation'
            Name of the output saved file
            
        figsize: tuple, default=(12,5)
            Size of the figure
            
        save: boolean, default=True,
            Is the animation has to be saved?

        Returns
        -------
        Animation
        Saved it into a gif if save==True
        
        """
         
        snapshots = self.data[variable]
        
        # First set up the figure, the axis, and the plot element we want to animate
        fig = plt.figure( figsize=figsize)
        a = snapshots[0]
        im = plt.imshow(a.T, cmap=cmap, extent=[xmin,xmax,ymin,ymax]) 
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.clim(cmin,cmax) #Set up here the limits of colorbar
        plt.colorbar(label=variable)
        
        def animate_func(i):
            if i % int(fps) == 0:
                print( '.', end ='' )
        
            im.set_array(snapshots[i])
            return [im]
        
        anim = animation.FuncAnimation(
                                       fig, 
                                       animate_func, 
                                       frames = len(self.data[variable]),
                                       interval = 1000 / int(fps), # in ms
                                       )
        if save == True:
            anim.save(output+'.gif', writer='PillowWriter')
        
        print('Done!')
        
        
def import_Wave(file):
    
    """
        Build a Wave object
        
        Parameters
        ----------
        file: str
            File to read
  
        Returns
        -------
        Wave Object
        
        """

    ds = xr.open_dataset(file)

    return Wave(ds)


