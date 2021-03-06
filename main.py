import numpy as np
import sympy as sp

#import matplotlib.pyplot as plt
import math

# local Modules
import plot_func as pf
import util as util
import lagrange as lagr
import neville as nevi
import newton as newt
import cubic_spline as cubsp
import lms as equalizing



################## SETTINGS ################### 
PLOTTING = True

LAGRAGE = True
NEVILLE = True
NEWTON = True

# spline settings
SPLINE = True
spline_types = [cubsp.SPLINE_TYPE.natural, \
                cubsp.SPLINE_TYPE.complete, cubsp.SPLINE_TYPE.periodic]

# LMS settings
LMS = False # or balancing functions LAP
# poly_degree=2 => φ_1(x)=1, φ_2(x)=x^1
poly_degree = 2 # or k


# NUMPY SETTINGS
# numpy array data type: float64
dt = np.dtype('f8')


################### INPUTS ################### 
# evaluation points 
#X = np.arange(-10, 10)
X = np.array([0])
x = X[0]

#lx1 = [-1, 0, 1, 2] # starting points
#lf1 = [ 3, 1, 2, 1] # starting values

lx1 = [-4, -3, -1,  0, 2, 4, 6] # starting points
lf1 = [ 3,  0, -1, -1, 1, 2, 4] # starting values


# only needed for the SPLINE_TYPE.periodic
# if you want to define your own function
# define x values
lx4 = np.array([-1, 0, 1], dtype=dt)
f = lambda x : abs(x)       # f(x) = |x|
fd1 = lambda x : x/abs(x)   # f'(x) = x/|x|
lf4 = f(lx4) # Stuetzwerte



# define x and f(x) data
xi = np.array(lx1, dtype=dt)
fi = np.array(lf1, dtype=dt)
#xi = np.array(lx4, dtype=dt)
#fi = np.array(lf4, dtype=dt)

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
        # if you want to plot the lagrange value
        #funcs.append(pf.PlotFunc(X, lagr_values, name="lagrange_values"))
        pass

# NEVILLE call
if NEVILLE:
    neville_value = None
    neville_value = nevi.neville(xi, fi, x)

    if neville_value != None:
        funcs.append(pf.PlotFunc(x, neville_value, name="neville_value"))
        pass

# NEWTON call
if NEWTON:
    newton_value = None
    newton_poly, newton_value = newt.newton(xi, fi, x)

    var_x = sp.symbols("x")
    npoly_func = sp.lambdify(var_x, newton_poly)
    newton_y = npoly_func(new_X)

    if newton_poly != None:
        funcs.append(pf.PlotFunc(new_X, newton_y, name="newton_poly", color="cyan"))
    if newton_value != None:
        #funcs.append(pf.PlotFunc(x, newton_value, name="newton_value"))
        pass

if SPLINE:
    spline_colors = ["orange", "violet", "lime","mediumspringgreen"]
    for i in range(len(spline_types)):
        spline_type = spline_types[i]
        cspline = cubsp.cubic_spline(xi, fi, spline_type, f, fd1)

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

                fs = cp[0].free_symbols
                if len(fs) > 1:
                    print(f"ERROR: The si got more the one variable, {fs}")
                    exit()

            cubic_spline_func = np.array(cp_fx)
            cubic_new_x_scale = np.linspace(xi[0], xi[xi.size-1], num_of_point*len(cspline))
            if cubic_spline_func.size != 0:
                funcs.append(pf.PlotFunc(cubic_new_x_scale, cubic_spline_func, line_type=pf.LINE_TYPE.dashed, color=spline_colors[i] ,name=f"cubic_spline({spline_type}), n={xi.size}"))


if LMS:

    #lms = equalizing.lms(xi, lf11, poly_degree)
    lms = equalizing.lms(xi, fi, poly_degree)
    start = xi[0]
    end = xi[xi.size-1]
    num_of_point = 500
    fx_xi = util.evalFunc(lms, start, end, num_of_point)

    if fx_xi.size > 0:
        lms_new_x_scale = np.linspace(start, end, num_of_point)
        if fx_xi.size != 0:
            funcs.append(pf.PlotFunc(lms_new_x_scale, fx_xi, line_type=pf.LINE_TYPE.dashed, color="snow", \
                                     name=f"LMS poly_degree={poly_degree}"))




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
if PLOTTING:
    pf.plot_funcs(funcs)

