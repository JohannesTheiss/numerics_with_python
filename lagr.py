import numpy as np

import scipy as sci
import scipy.interpolate as sciint

import sympy as sp

import matplotlib.pyplot as plt
import math
import enum

class LINE_TYPE(enum.Enum):
    no_type = 0
    line = 1
    dotted = 2
    dashed = 3
    line_dotted = 4

class PlotFunc:
    def __init__(self, x, y, line_type=LINE_TYPE.no_type, color="", name=""):
        self.x = x
        self.y = y
        self.line_type = line_type
        self.color = color
        self.name = name

    def __iter__(self):
        return iter((self.x, self.y, self.line_type, self.color, self.name))


# args:
# functions: [PlotFunc,...]
def plot_funcs(functions):
    i = 0
    for (x_values, y_values, line_type, color, name) in functions:
        lt = 'o-' # default: dotted with line
        if LINE_TYPE.line == line_type:
            lt = '-'
        elif LINE_TYPE.dotted == line_type:
            lt = ':'
        elif LINE_TYPE.dashed == line_type:
            lt = '--'
        elif LINE_TYPE.line_dotted == line_type:
            lt = 'o:'

        # if color == "red" than use "r"
        if len(color) > 1: color = color[0]

        fmt = f"{lt}{color}"
        lbl = name if name != "" else f"line{i}"

        #plt.plot(x_values, y_values, marker='o', label=f"line{i}")
        plt.plot(x_values, y_values, fmt, label=lbl)

        i += 1

    plt.legend()
    plt.grid()
    plt.show()


def lagr(xi, fi, X=np.array([]), debug=True, prec=4):
    poly = lagrange(xi, fi)
    coef = Polynomial(poly).coef
    res = None

    if X.size != 0:
        res = np.round(np.polyval(coef, X), prec)

    if debug:
        print("p(x):")
        print(poly)
        print(f"coef: {np.round(coef, prec)}")
        if res.size != 0 and res.size == X.size:
            for i in range(res.size):
                print(f"p({X[i]})\t: {res[i]}")

    return coef, res


def neville(xi, fi, x, debug=True):
    print("NEVILLE:")
    if xi.size != fi.size:
        print("xi and yi must have same first dimension")
        return None

    p = np.copy(fi)
    n = xi.size
    for k in range(1, n):
        for j in range(0, n-k):
            # k+j is das eig. k was man will
            new_k = k+j
            pjk = (((x-xi[j])*p[j+1]) - ((x-xi[new_k])*p[j])) / (xi[new_k] - xi[j])

            # print
            print(f"P {j},{new_k} = ({x} - {xi[j]})* {p[j+1]} \t- ({x} - {xi[new_k]})* {p[j]} \t/ ({xi[new_k]} - {xi[j]}) \t = {pjk}")

            # update the value in the array
            p[j] = pjk


    print(f"P 0,{n-1} = p({x}) = {p[0]}")
    return p[0]


def newton(xi, fi, x, debug=True):
    print("NEWTON:")
    if xi.size != fi.size:
        print("xi and yi must have same first dimension")
        return None

    p = np.copy(fi)
    n = xi.size
    coefs = [p[0]]
    for k in range(1, n):
        for j in range(0, n-k):
            # k+j is das eig. k was man will
            new_k = k+j
            pjk = (p[j+1] - p[j]) / (xi[new_k] - xi[j])

            # print
            print(f"P {j},{new_k} =\t {p[j+1]} - {p[j]}      \t/ ({xi[new_k]} - {xi[j]}) \t = {pjk}")

            # update the value in the array
            p[j] = pjk

        print()
        coefs.append(p[0])


    print(coefs)
    coefs_number = len(coefs)
    px = coefs[coefs_number-1]
    px_poly = ["("*(math.ceil(coefs_number-1)) ,f"({px})"]
    for i in range(coefs_number-2, -1, -1):
        px_poly.append(f"*(x-({xi[i]}))+({coefs[i]}))")
        px *= (x - xi[i])
        px += coefs[i]

    print(px)
    px_str = "".join(px_poly)
    print(px_str)

    # das ist nicht gesund...
    func = lambda x : eval(px_str) # ACHTUNG ACHTUNG BITTE HELFEN SIE MIR

    print(f"P 0,{n-1} = p({x}) = {p[0]}")
    return func, p[0]


class SPLINE_TYPE(enum.Enum):
     natural = 0
     complete = 1
     periodic = 2


def cubic_spline(xi, fi, spline_type, func=None):
    print("######## CUBIC SPLINE ########")

    n = xi.size
    x = sp.symbols("x")
    inter = []
    for i in range(xi.size-1):
        inter.append((xi[i], xi[i+1]))

    print(f"Interval: {inter}")

    inter_len = len(inter)
    Si = ["DUMMY_FUNC"]
    var_vector = []
    print("Si:")
    for i in range(inter_len):
        left_outer = inter[i][0] # the left outer point of the interval
        a, b, c, d = sp.symbols(f"a{i+1},b{i+1},c{i+1},d{i+1}")
        si = a + b*(x-left_outer) + c*((x-left_outer)**2) + d*((x-left_outer)**3)
        Si.append(si)
        var_vector.extend([a,b,c,d])
        print(f"s{i+1} = {si}")
    print()

    Sil = len(Si)
    SiD1 = ["DUMMY_FUNC"]
    SiD2 = ["DUMMY_FUNC"]
    print("derivative:")
    for i in range(1, Sil):
        d1 = sp.diff(Si[i], x)
        d2 = sp.diff(d1, x)
        SiD1.append(d1)
        SiD2.append(d2)
        print(f"s{i}'= {d1} \t\t s{i}'' = {d2}")

    print("\nconditions:")
    inter_points = xi[1:n-1]
    ipl = len(inter_points)
    lgs = []
    for i in range(ipl):
        si1d1 = SiD1[i+1].subs(x, inter_points[i])
        si2d1 = SiD1[i+2].subs(x, inter_points[i])
        a1 = sp.Eq(si1d1, si2d1)

        si1d2 = SiD2[i+1].subs(x, inter_points[i])
        si2d2 = SiD2[i+2].subs(x, inter_points[i])
        a2 = sp.Eq(si1d2, si2d2)

        lgs.extend([a1, a2])
        sp.pprint(a1)
        sp.pprint(a2)


    for i in range(1, n):
        sim1 = Si[i].subs(x, xi[i-1])
        si = Si[i].subs(x, xi[i])

        b1 = sp.Eq(sim1, fi[i-1])
        b2 = sp.Eq(si, fi[i])

        lgs.extend([b1, b2])
        sp.pprint(b1)
        sp.pprint(b2)

    print()

    if spline_type == SPLINE_TYPE.natural:
        # natuerlicher spline
        print("natural spline")
        s1 = SiD2[1].subs(x, xi[0])
        sn = SiD2[n-1].subs(x, xi[n-1])
        eq1 = sp.Eq(s1, 0)
        eq2 = sp.Eq(sn, 0)

        lgs.extend([eq1, eq2])
        sp.pprint(eq1)
        sp.pprint(eq2)

    elif spline_type == SPLINE_TYPE.complete:
        # vollstaendiger spline 
        pass



    if len(lgs) != (4*inter_len):
        print(f"error: length of the LGS is wrong: {len(lgs)} != {(4*inter_len)}")


    # results
    print("\nRESULTS:")

    solved_lgs = sp.solve(lgs, var_vector)
    sp.pprint(lgs)
    sp.pprint(solved_lgs)


    sx = []
    for i in range(1, Sil):
        # get free_symbols and the value from the solved_lgs
        fs = list(Si[i].free_symbols)
        values_by_fs = []
        for s in fs:
            values_by_fs.append(solved_lgs.get(s))

        # map free_symbols and solved_lgs values
        sxi = Si[i]
        for j in range(len(fs)):
            if values_by_fs[j] != None:
                sxi = sxi.subs(fs[j], values_by_fs[j])

        sx.append((sxi, inter[i-1]))
        sp.pprint(sp.simplify(sxi))

    return sx






################## SETTINGS ################### 
LAGRAGE = False
NEVILLE = False
NEWTON = False
SPLINE = True
spline_type = SPLINE_TYPE.natural


################### INPUTS ################### 
# Stuetzstellen
#xi = np.array([-2, -1, 1, 3])
#xi = np.array([-2, -0.5, 0.5, 1, 1.5])
xi = np.array([-1, 0, 1])
#xi = np.linspace(-1, 1, 3)
#xi = np.array([0,1,2,3,4])

# Stuetzwerte
#fi = np.array([8, 0, 2, -12])
#fi = np.array([-4, 0.5, 3.5, 5, 6.5])
f = lambda x : abs(x)
fi = np.array(f(xi))

# Auswertungspunkte
#X = np.arange(-10, 10)
X = np.array([2])
x = X[0]

# functions to plot
funcs = [PlotFunc(xi, fi, LINE_TYPE.line, color="r", name="input_func")]

xi_max = math.ceil(xi.max())
xi_min = math.ceil(xi.min())
new_X = np.linspace(xi_min, xi_max)

################### Interpolation ################### 
if LAGRAGE:
    # lagrange call
    lagr_coef, lagr_values = lagr(xi, fi, X)

    # plot the lagr poly as a function
    lagr_Y = np.polyval(lagr_coef, new_X)

    if lagr_Y.size != 0:
        funcs.append(PlotFunc(new_X, lagr_Y, name="lagrange_poly"))
    if lagr_values != None:
        funcs.append(PlotFunc(X, lagr_values, name="lagrange_values"))

# NEVILLE call
if NEVILLE:
    neville_value = None
    neville_value = neville(xi, fi, x)

    if neville_value != None:
        funcs.append(PlotFunc(x, neville_value, name="neville_value"))

# NEWTON call
if NEWTON:
    newton_value = None
    horner_schema, newton_value = newton(xi, fi, x)
    newton_y = horner_schema(new_X)

    if horner_schema != None:
        funcs.append(PlotFunc(new_X, newton_y, name="newton_poly"))
    if newton_value != None:
        funcs.append(PlotFunc(x, newton_value, name="newton_value"))

if SPLINE:
    cspline = cubic_spline(xi, fi, spline_type, f)

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
            funcs.append(PlotFunc(cubic_new_x_scale, cubic_spline_func, line_type=LINE_TYPE.dashed, name=f"cubic_spline({spline_type}), n={xi.size}"))



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


plot_funcs(funcs)


