import numpy as np

from scipy.interpolate import lagrange
from numpy.polynomial.polynomial import Polynomial

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


# example call
#print(lagr(np.array([1,2,3]), np.array([3,4,5]), np.array([2])))

