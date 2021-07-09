import numpy as np
import sympy as sp


def lms(xi, fi, poly_degree):
    print("############## Least-Mean-Squares-Algorithmus ############## ")
    x = sp.symbols("x")
    y_vec = []
    n = xi.size
    ret_f = 0

    # make phis and y_vec
    phis = []
    for j in range(poly_degree):
        #if j % 2 != 0:
            #continue
        phi = x**(j)
        phis.append(phi)

        yi = sp.symbols(f"y{j}")
        y_vec.append(yi)

        ret_f += yi*phi

    #sp.pprint(phis)
    print(f"φ_j = {phis}")
    print(f"y_ve = {y_vec}")
    print(f"ret_f = {ret_f}")
    print(f"fi = {fi}")

    # culc. A
    A = sp.Matrix()
    for i in range(len(phis)):
        phi = phis[i]
        phi_y = None
        if phi == 1:
            phi_y = sp.ones(n, 1)
        else:
            phi_func = sp.lambdify(x, phi)
            phi_y = sp.Matrix([phi_func(xi)]).T

        if phi_y == None:
            print("ERROR: lms.py: phi_y = None")
            return None

        #sp.pprint(phi_y)
        A = A.row_join(phi_y)

    print("A = ")
    sp.pprint(A)

    # culc ATA 
    AT = A.T
    ATA = AT * A
    print("\nAT = ")
    sp.pprint(AT)
    print("\nATA = ")
    sp.pprint(ATA)

    # ATA * y
    print("\nATA * y = ")
    ATAy = ATA*sp.Matrix([y_vec]).T
    sp.pprint(ATAy)

    f = sp.Matrix([fi]).T
    ATf = AT * f
    print("\nATf = ")
    sp.pprint(ATf)

    # option #1 to solve the lgs 
    #lgs = sp.Eq(ATA, ATf)
    #sp.pprint(lgs)
    #solved_lgs = sp.linsolve((ATA, ATf), y_vec)

    # option #2
    lgs = sp.Eq(ATAy,  ATf)
    solved_lgs = sp.solve(lgs)

    print("\nLGS: ATA * y = ATf <=> ")
    sp.pprint(lgs)
    print("==>")
    sp.pprint(solved_lgs)
    print("=")
    sp.pprint(sp.nsimplify(solved_lgs))

    for var, value  in solved_lgs.items():
        #print(sp.nsimplify(value))
        #print(float(value))
        ret_f = ret_f.subs(var, value)

    print("\nfa(x) = ret_f(x) =")
    sp.pprint(ret_f)
    print("=")
    simp = sp.nsimplify(ret_f)
    sp.pprint(simp)

    return simp

