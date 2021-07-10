import numpy as np
import sympy as sp
import math


def euler(etha_i, h, xi, yd1, vs):
    # build interval
    #t = [x for x in range(0, xi, h)]
    t = np.arange(0, xi, h)
    print(t)
    #f = yd1.subs(vs[0], )

    #next_etha = etha_i + (h * yd1.subs())




############ INPUTS ############ 
vs = x, y = sp.symbols("x, y")

# Entwicklungsstelle
xi = 1

# Schrittweite
h = 1/2

# y'(x)
yd1 = x*y

# y(x)
y = sp.exp((x**2)/2)

# y(0) the start value
y0 = 1

# print the inputs
print(f"y'({vs}) =")
sp.pprint(yd1)
print(f"y(x) =")
sp.pprint(y)
print(f"y(0) = {y0}")


yh = euler(y0, h, xi, yd1, vs)





