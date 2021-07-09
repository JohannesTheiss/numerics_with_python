import numpy as np
import sympy as sp
import util


prec = 7

def neville(xi, fi, x, debug=True):
    print(f"NEVILLE: (prec. = {prec})")
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
            print(f"P {j},{new_k} = ({x} - {xi[j]})* {p[j+1]} \t- ({x} - {xi[new_k]})* {p[j]} \t/ ({xi[new_k]} - {xi[j]}) \t = {pjk} = {np.round(pjk, prec)} = {sp.nsimplify(pjk)}")

            # update the value in the array
            p[j] = pjk


    print(f"P 0,{n-1} = p({x}) = {p[0]}")
    print("=")
    sp.pprint(sp.nsimplify(p[0]))
    return p[0]


# example call
#print(neville(np.array([1,2,3]), np.array([3,4,5]), np.array([2])))

