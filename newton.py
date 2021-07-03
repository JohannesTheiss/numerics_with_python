import numpy as np
import math

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


# example call
#print(newton(np.array([1,2,3]), np.array([3,4,5]), 2))



