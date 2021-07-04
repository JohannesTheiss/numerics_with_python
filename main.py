import numpy as np

#import scipy as sci
#import scipy.interpolate as sciint

import sympy as sp

import matplotlib.pyplot as plt
import math

# local Modules
import plot_func as pf
import lagrange as lagr
import neville as nevi
import newton as newt
import cubic_spline as cubsp


################## SETTINGS ################### 
LAGRAGE = False
NEVILLE = False
NEWTON = True
SPLINE = True
spline_type = cubsp.SPLINE_TYPE.natural

dt = np.dtype('f8')


################### INPUTS ################### 
# Stuetzstellen
# list of x values
lx1 = [-2, -1, 1, 3]
lx2 = [-2, -1, 1, 3]
lx3 = [-2, -1, 1, 3]
lx4 = [-2, -1, 0, 1, 3]
lx4 = [-2, -1, 1, 3, 0]
lx4 = [-2, -0.5, 0.5, 1, 1.5]
lx4 = [-1, 0, 1]

#xi = np.linspace(-1, 1, 3, dtype=dt)
xi = np.array(lx1, dtype=dt)

# Stuetzwerte
# list of f(x) values
ly1 = [8, 0, 2, -12]
ly2 = [7, 0, 1, 2, -12]
ly3 = [8, 0, 2, -12, 1]
ly4 = [-4, 0.5, 3.5, 5, 6.5]

# define own function
f = lambda x : abs(x)
lf1 = f(xi)
fi = np.array(ly1, dtype=dt)

# Auswertungspunkte
#X = np.arange(-10, 10)
X = np.array([2])
x = X[0]

# functions to plot
funcs = [pf.PlotFunc(xi, fi, pf.LINE_TYPE.line, color="red", name="input_func")]

xi_max = math.ceil(xi.max())
xi_min = math.ceil(xi.min())
new_X = np.linspace(xi_min, xi_max)

################### Interpolation ################### 
if LAGRAGE:
    # lagrange call
    lagr_coef, lagr_values = lagr.lagr(xi, fi, X)

    # plot the lagr poly as a function
    lagr_Y = np.polyval(lagr_coef, new_X)

    if lagr_Y.size != 0:
        funcs.append(pf.PlotFunc(new_X, lagr_Y, name="lagrange_poly"))
    if lagr_values != None:
        funcs.append(pf.PlotFunc(X, lagr_values, name="lagrange_values"))

# NEVILLE call
if NEVILLE:
    neville_value = None
    neville_value = nevi.neville(xi, fi, x)

    if neville_value != None:
        funcs.append(pf.PlotFunc(x, neville_value, name="neville_value"))

# NEWTON call
if NEWTON:
    newton_value = None
    newton_poly, newton_value = newt.newton(xi, fi, x)

    var_x = sp.symbols("x")
    npoly_func = sp.lambdify(var_x, newton_poly)
    newton_y = npoly_func(new_X)

    if newton_poly != None:
        funcs.append(pf.PlotFunc(new_X, newton_y, name="newton_poly", color="green"))
    if newton_value != None:
        funcs.append(pf.PlotFunc(x, newton_value, name="newton_value"))

if SPLINE:
    cspline = cubsp.cubic_spline(xi, fi, spline_type)

    if cspline != None:
        # build fx
        cp_fx = []
        num_of_point = 500
        for cp in cspline:
            inter_start = cp[1][0]
            inter_end = cp[1][1]
            cp_xi = np.linspace(inter_start, inter_end, num_of_point)

            x = sp.symbols("x")
            cp_solved_func = sp.lambdify(x, cp[0])
            cp_fx_xi = cp_solved_func(cp_xi)

            cp_fx.extend(cp_fx_xi)

        cubic_spline_func = np.array(cp_fx)
        cubic_new_x_scale = np.linspace(xi[0], xi[xi.size-1], num_of_point*len(cspline))
        if cubic_spline_func.size != 0:
            funcs.append(pf.PlotFunc(cubic_new_x_scale, cubic_spline_func, line_type=pf.LINE_TYPE.dashed, color="blue" ,name=f"cubic_spline({spline_type}), n={xi.size}"))



############ ERROR ##################
#error = False
#er = []
#for i in range(len(newton_y)):
#    er.append(np.round(abs(newton_y[i] - lagr_Y[i]), 9))
#    if er[i] > 0.0001:
#        error = True

#print(error)
#print(er)


################### PLOTTING ################### 
pf.plot_funcs(funcs)

