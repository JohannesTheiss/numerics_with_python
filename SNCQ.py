import numpy as np
import sympy as sp

import util

dt = np.dtype('f8')


def get_weights(m):
    w = []
    if m == 0:
        w = [1]
        util.print_heading("Mittelpunks-R")
    elif m == 1:
        w = [0.5, 0.5]
        util.print_heading("Trapez-R")
    elif m == 2:
        w = [1/6, 2/3, 1/6]
        util.print_heading("Simpson-R")
    elif m == 3:
        w = [1/8, 3/8, 3/8, 1/8]
        util.print_heading("3/8 -R")
    elif m == 4:
        w = [7/90, 32/90, 12/90, 32/90, 7/90]
        util.print_heading("Milne-R")
    return np.array(w, dtype=dt)


def NCQF(func, a, b, m):
    x = sp.symbols("x")
    h = b - a # length of the interval
    for mi in m:
        print("__________________")
        weights = get_weights(mi)

        xi = [] # grid points
        print(f"m = {mi}")
        if mi == 0:
            xk = a+(h/2)
            print(f"x{0} = a + (h / 2) = {a} + ({h} / 2) = {xk} = {sp.nsimplify(xk)}")
            xi.append(xk)
        else:
            for i in range(mi+1):
                xk = a+((i*h)/mi)
                print(f"x{i} = a + (i * h / m{mi}) = {a} + ({i} * {h} / {mi}) = {xk} = {sp.nsimplify(xk)}")
                xi.append(xk)

        Im = 0
        print("SUM:")
        for i in range(mi+1):
            func_xi = func.subs(x, xi[i])
            next_value = (h * weights[i] * func_xi)
            Im += next_value
            print(f"h * {sp.nsimplify(weights[i])} * {func}")
            print(f"=> {h} * {sp.nsimplify(weights[i])} * {sp.nsimplify(func_xi)} = {next_value} = {sp.nsimplify(next_value)}\n")


        print(f"I_{mi}")
        print(f"{Im} = {sp.nsimplify(Im)}")



x = sp.symbols("x")
func = 1/(1+x)
a = 0
b = 1
m = [0, 1, 2, 3, 4]

res = NCQF(func, a, b, m)
print(f"res: {res}")



