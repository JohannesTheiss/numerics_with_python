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
LAGRAGE = True
NEVILLE = True
NEWTON = True
SPLINE = True
spline_type = cubsp.SPLINE_TYPE.natural


################### INPUTS ################### 
# Stuetzstellen
xi = np.array([-2, -1, 1, 3])
#xi = np.array([-2, -0.5, 0.5, 1, 1.5])
#xi = np.array([-1, 0, 1])
#xi = np.linspace(-1, 1, 3)
#xi = np.array([0,1,2,3,4])

# Stuetzwerte
fi = np.array([8, 0, 2, -12])
#fi = np.array([-4, 0.5, 3.5, 5, 6.5])
#f = lambda x : abs(x)
#fi = np.array(f(xi))

# Auswertungspunkte
#X = np.arange(-10, 10)
X = np.array([2])
x = X[0]

# functions to plot
funcs = [pf.PlotFunc(xi, fi, pf.LINE_TYPE.line, color="r", name="input_func")]

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
    horner_schema, newton_value = newt.newton(xi, fi, x)
    newton_y = horner_schema(new_X)

    if horner_schema != None:
        funcs.append(pf.PlotFunc(new_X, newton_y, name="newton_poly"))
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
            funcs.append(pf.PlotFunc(cubic_new_x_scale, cubic_spline_func, line_type=pf.LINE_TYPE.dashed, name=f"cubic_spline({spline_type}), n={xi.size}"))



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


