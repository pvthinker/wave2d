"""It is possible to compute the ship wake pattern directly, thanks
to a beautiful mathematical trick found in a Pierre Gilles de Gennes
paper (French 1991 Nobel Prize). See the fourier.py module. """

# to activate it, copy-paste this script in your Ipython window, after
# you've run the main wave2d script

import plotting as pt
fig = pt.Plotting(param)
p = model.fspace.compute_balanced_wake(model.hphi0, param.U)
fig.init_figure(p)
