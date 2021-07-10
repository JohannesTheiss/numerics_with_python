import numpy as np
import sympy as sp

red = '\033[91m'
bold = '\033[1m'
end = '\033[0m'


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
        return np.array([])


def print_heading(text):
    print(bold + red + text +  end)


def print_default(name, new_line=False):
    if new_line:
        print()
    print(f"{name}:")

def print_arr(name, data, new_line=False, prec=8):
    print_default(name, new_line)

    sp.pprint(data)
    print("=")
    data_list = []
    #sp.pprint(sp.nsimplify(data))
    for d in data:
        nsimp = sp.nsimplify(d)
        simp = sp.simplify(d)
        rou = np.round(d, prec)
        #if nsimp == simp:
            #print("smae", nsimp, simp)
        #if simp == rou:
            #print("round", rou)
        eqs = str(nsimp) + " = " + str(simp) + " = " + str(rou) + "\n"
        data_list.append(eqs)
    sp.pprint(data_list)


def print_poly(name, poly, new_line=False):
    print_default(name, new_line)

    #sp.pprint(poly)
    #print("=")
    fac = sp.factor(poly)
    if fac == poly:
        print("same")
        sp.pprint(poly)
    else:
        print("not same")
        sp.pprint(poly)
        sp.pprint(fac)
    #sp.pprint(sp.expand(poly))



def func_max_norm():
    xi = np.linspace(0, 1, 1000000)
    f = lambda x : 24/((1+x)**5)
    fi = np.abs(f(xi))
    #print(fi)
    m = max(fi)
    print(f"max: {m}")
    return m


func_max_norm()




