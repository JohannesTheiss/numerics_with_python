import numpy as np
import sympy as sp
import math

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


def NCQF(func, I, a, b, mi):
    print("================================================")
    h = b - a # length of the interval
    util.print_heading(f"NCQF: ({sp.nsimplify(a)}, {sp.nsimplify(b)}) h = {sp.nsimplify(h)}")
    x = sp.symbols("x")
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
        print(f"h * {sp.nsimplify(weights[i])} * ({func})")
        print(f"=> {h} * {sp.nsimplify(weights[i])} * {sp.nsimplify(func_xi)} = {next_value} = {sp.nsimplify(next_value)}\n")


    # print Im
    print(f"I_{mi} =")
    print(f"{Im} = {sp.nsimplify(Im)}")

    # print error
    error = abs(float(I) - Im)
    print(f"|Im - I(f)| = {error}")
    #print(f"Em = |c| * h^P = {abs(I - Im)}")

    return (Im, error)


def SNCQF(func, I, a, b, m, N):
    etha = (b - a) / N
    sum_Im = []
    for k in range(1, N+1):
        inter_start = a + ((k-1) * etha)
        inter_end = a + (k * etha)
        #print(pi_start, pi_end)
        Im, error = NCQF(func, I, inter_start, inter_end, m)

        sum_Im.append(Im)

    print("=======================================")
    util.print_heading("Summed up NCQF:")
    s = 0
    for i in sum_Im:
        print(f"{sp.nsimplify(i)}", end=" + ")
        s += i

    print(f"\n=> {s} = {sp.nsimplify(s)}")



### Interval
a = 0 # start
b = sp.pi # end
mi = [0, 1, 2, 3, 4]
m = 2

# number of partial intervals
#N = 3


### function
x = sp.symbols("x")
#func = 1/(1+x)
func = sp.sin(x)

# integrated function
I = sp.integrate(func, (x, a, b))
I_value = float(I)


# print functions
print("f(x):")
sp.pprint(func)
print("I:")
sp.pprint(I)
print(f"= {I_value}")


#for i in mi:
#    NCQF(func, I, a, b, i)

NCQF(func, I, a, b, m)

#SNCQF(func, I, a, b, m, N)


