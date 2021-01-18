import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib
import fourier
font = {'size': 16}

matplotlib.use('TkAgg')
matplotlib.rc('font', **font)


# the backend 'TkAgg' has to be set before pyplot is imported
import matplotlib.pyplot as plt
plt.ion()


class Plotting(object):
    def __init__(self, param):
        list_param = ['Lx', 'Ly', 'cax', 'figwidth',
                      'varplot', 'typewave', 'vectorscale', 'macuser']
        param.copy(self, list_param)
        self.d = 8 # how many points are skept for quiver plot

    def init_figure(self, field2d, u=None, v=None):
        """create the figure
        this is where you adapt the figure to your needs the function
        should return the graphical objects to update
        """
        # best youtube aspect ratio is 16:9
        #fig_size = np.array([1280, 720])
        fig_size = np.array([self.figwidth, self.figwidth//16*9])
        my_dpi = 100
        zoom_factor = 1

        self.title_string = '%s / variable = %s / time = %.2f'

        self.fig = plt.figure(figsize=fig_size/my_dpi, dpi=my_dpi)
        self.fig.clf()

        field_size = np.shape(field2d)
        zoom_factor = (0.8*fig_size[0])//field_size[1]
    #    zoom_factor = (fig_size[0])//field_size[0]
        # print("each grid cell is (%i, %i) pixels" % (zoom_factor, zoom_factor))
        rectangle = [0.1, 0.1,
                     field_size[1]/fig_size[0]*zoom_factor,
                     field_size[0]/fig_size[1]*zoom_factor]
        #ax = plt.axes(rectangle)
        ax = self.fig.add_subplot(1, 1, 1)
        self.ax = ax
        self.im = ax.imshow(field2d, cmap=plt.get_cmap('RdBu_r', lut=21),
                            vmin=self.cax[0], vmax=self.cax[1],
                            extent=[0, self.Lx, 0, self.Ly],
                            origin='lower', interpolation='nearest')

        time = 0.
        self.ti = ax.set_title(self.title_string % (
            self.typewave, self.varplot, time))
        ax.set_xlabel('X')
        if self.typewave == 'internal':
            ax.set_ylabel('Z')
        else:
            ax.set_ylabel('Y')

        divider = make_axes_locatable(ax)
        cbax = divider.append_axes("right", size="3%", pad=0.1)

        if not(u is None) and not(v is None):
            ny, nx = np.shape(field2d)
            self.x, _ = fourier.set_x_and_k(nx, self.Lx)
            self.y, _ = fourier.set_x_and_k(ny, self.Ly)
            maxu = max(np.max(np.abs(u.ravel())), np.max(np.abs(v.ravel())))
            self.quiv = ax.quiver(self.x[::self.d], self.y[::self.d],
                                  u[::self.d, ::self.d], v[::self.d, ::self.d],
                                  scale=maxu*10*self.vectorscale)

    #    pos = [rectangle[0]+rectangle[2]+0.02, rectangle[1], 0.05, rectangle[3]]
        cb = self.fig.colorbar(self.im, cax=cbax)
        cb.formatter.set_powerlimits((-3, 3))
        pos = np.array(cb.ax.get_position().bounds)
        pos[1], pos[3] = rectangle[1], rectangle[3]

        self.fig.tight_layout()
        self.fig.show()
        if self.macuser:
            plt.pause(1e-4)
        else:
            self.fig.canvas.draw()

    def update(self, kt, time, field2d, u=None, v=None):
        """ update the figure during the loop

            read/compute the field before and update the imshow object 'im'
            also update the title object 'ti' with the time """

        self.im.set_array(field2d)
        self.ti.set_text(self.title_string % (
            self.typewave, self.varplot, time))
        if not(u is None) and not(v is None):
            self.quiv.set_UVC(u[::self.d, ::self.d], v[::self.d, ::self.d])
            maxu = max(np.max(np.abs(u.ravel())), np.max(np.abs(v.ravel())))
            maxu = max(np.std(u.ravel()), np.std(v.ravel()))
            self.quiv.scale = maxu*10*self.vectorscale
            
        self.fig.canvas.draw()
        # for macOS comment above and decomment below
        # plt.pause(1e-4)


def plotvar(param, field2d, varname, cax=None):
    param.varplot = varname
    if cax is None:
        maxi = np.max(np.abs(field2d.ravel()))
        param.cax = [-maxi, maxi]
    else:
        param.cax = cax

    fig = Plotting(param)
    fig.init_figure(field2d)
    fig.update(0, 0., field2d)
    return fig.ax
