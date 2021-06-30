import numpy as np
from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial
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


################### INPUTS ################### 
# Stuetzstellen
xi = np.array([-2, -1, 1, 3])
#xi = np.array([-2, -0.5, 0.5, 1, 1.5])

# Stuetzwerte
fi = np.array([8, 0, 2, -12])
#fi = np.array([-4, 0.5, 3.5, 5, 6.5])

# Auswertungspunkte
#X = np.arange(-10, 10)
X = np.array([2])
x = X[0]


################### Interpolation ################### 
# lagrange call
lagr_coef, lagr_values = lagr(xi, fi, X)

# plot the lagr poly as a function
xi_max = math.ceil(xi.max())
xi_min = math.ceil(xi.min())
lagr_X = np.linspace(xi_min, xi_max)
lagr_Y = np.polyval(lagr_coef, lagr_X)

# NEVILLE call
neville_value = None
neville_value = neville(xi, fi, x)

# NEWTON call
newton_value = None
horner_schema, newton_value = newton(xi, fi, x)


################### PLOTTING ################### 
funcs = [PlotFunc(xi, fi, LINE_TYPE.line, color="r", name="input_func")]

if lagr_Y.size != 0:
    funcs.append(PlotFunc(lagr_X, lagr_Y, name="lagrange_poly"))
if lagr_values != None:
    funcs.append(PlotFunc(X, lagr_values, name="lagrange_values"))
if newton_value != None:
    funcs.append(PlotFunc(x, newton_value, name="newton_value"))
if neville_value != None:
    funcs.append(PlotFunc(x, neville_value, name="neville_value"))


plot_funcs(funcs)


