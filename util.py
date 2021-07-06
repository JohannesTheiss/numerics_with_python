import numpy as np
import sympy as sp



# func(x)
def evalFunc(func, start, end, num_of_point):
    if func != None:
        # build fx
        fx = []
        xi = np.linspace(start, end, num_of_point)

        if len(func.free_symbols) > 1:
            print("ERROR: util.py: more then one var in func")
            return None

        x = sp.symbols("x")
        lambda_fun = sp.lambdify(x, func)
        fx_xi = np.array(lambda_fun(xi))

        return fx_xi
    else:
        return None


