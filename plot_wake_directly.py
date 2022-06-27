"""It is possible to compute the ship wake pattern directly, thanks
to a beautiful mathematical trick found in a Pierre Gilles de Gennes
paper (French 1991 Nobel Prize). See the fourier.py module. """

# to activate it, copy-paste this script in your Ipython window, after
# you've run the main wave2d script
#
# The wake tip starts at param.x0
#
# to have a good rendering -> param.x0 = 1.5
#


import plotting as pt
fig = pt.Plotting(param)
# epsilon controls the wake extension (larger epsilon->shorter wake)
p = model.fspace.compute_balanced_wake(model.hphi0, param.U, epsilon=0.8)
fig.init_figure(p)
