import numpy as np
import sympy as sp

# local Modules
import plot_func as pf
import lagrange as lagr
import neville as nevi
import newton as newt
import cubic_spline as cubsp


################## SETTINGS ################### 
dt = np.dtype('f8')
spline_type = cubsp.SPLINE_TYPE.natural


################## TEST FUNCTIONS ################### 
def print_error(func, expected, value):
    print(f"ERROR {func}: expected: {expected} but is was {value}")

def lagrange_test(xi, fi, X, expected):
    lagr_coef, lagr_values = lagr.lagr(xi, fi, X)
    b = lagr_values[0] == expected
    if not b:
        print_error("lagrange", expected, lagr_values)
    return b

def neville_test(xi, fi, x, expected):
    neville_value = nevi.neville(xi, fi, x)
    b = np.round(neville_value, 6) == expected
    if not b:
        print_error("neville", expected, neville_value)
    return b

def newton_test(xi, fi, x, expected):
    newton_poly, newton_value = newt.newton(xi, fi, x)
    b = newton_value == expected
    if not b:
        print_error("newton", expected, newton_value)
    return b

def cubic_spline_test(xi, fi, x, spline_type, expected):
    cspline = cubsp.cubic_spline(xi, fi, spline_type)
    var_x = sp.symbols("x")
    fx = None
    for func, inter in cspline:
        if inter[0] <= x and x <= inter[1]:
            fx = func.subs(var_x, x)
    b = fx == expected
    if not b:
        print_error("cubic_spline", expected, fx)
    return b



############# TEST DATA ############# 
# Auswertungspunkte
X = np.array([2])
x = X[0]

lx1 = np.array([-2, -1, 1, 3], dtype=dt)
ly1 = np.array([8, 0, 2, -12], dtype=dt)
exp1 = 0.0

lx2 = np.array([-2, -1, 1, 3, 0], dtype=dt)
ly2 = np.array([8, 0, 2, -12, 1], dtype=dt)
exp2 = -2.0

lx3 = np.array([-2, -0.5, 0.5, 1, 1.5], dtype=dt)
ly3 = np.array([-4, 0.5, 3.5, 5, 6.5], dtype=dt)
exp3 = 8

#lx4 = np.array([-2, -1, 0, 1, 2], dtype=dt)
#f = lambda x : abs(x)
#lf1 = f(lx4)
#fi = np.array(ly1, dtype=dt)

# create test lists
list_of_xis = [lx1, lx2, lx3]
list_of_fis = [ly1, ly2, ly3]
expected_values = [exp1, exp2, exp3]


if len(expected_values) != len(list_of_xis) or len(list_of_xis) != len(list_of_fis):
    print("your list lengths dosnt match!")
    exit()

list_of_checks = []
for i in range(len(list_of_xis)):
    xi = list_of_xis[i]
    fi = list_of_fis[i]
    exv = expected_values[i]

    list_of_checks.append(lagrange_test(xi, fi, X, exv))
    list_of_checks.append(neville_test(xi, fi, x, exv))
    list_of_checks.append(newton_test(xi, fi, x, exv))
    #list_of_checks.append(cubic_spline_test(xi, fi, x, spline_type, exv))


print(list_of_checks)

