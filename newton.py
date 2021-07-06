import numpy as np
import math

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

def newton(xi, fi, x=None, debug=True):
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

        coefs.append(p[0])

    coefs_number = len(coefs)
    var_x = sp.symbols("x")
    newton_poly = coefs[coefs_number-1]
    for i in range(coefs_number-2, -1, -1):
        newton_poly *= (var_x - xi[i])
        newton_poly += coefs[i]

    px = None
    if x != None:
        px = newton_poly.subs(var_x, x)

    # prints
    print(f"coefs: {coefs}")
    print(f"p({x}) = {px}")
    print("newton poly:")
    sp.pprint(newton_poly)
    print("=")
    sp.pprint(sp.simplify(newton_poly))

    return newton_poly, px



# example call
#print(newton(np.array([1,2,3]), np.array([3,4,5]), 2))
#print(newton(np.array([-2,-0.5,0.5,1,1.5]), np.array([-4,0.5,3.5,5,6.5]), 2))

