import numpy as np
import sympy as sp
import enum

class SPLINE_TYPE(enum.Enum):
     natural = 0
     complete = 1
     periodic = 2

def append_equations(lgs, eqs, PRINT=True):
    for lhs, rhs in eqs:
        eq = sp.Eq(lhs, rhs)
        lgs.append(eq)
        if PRINT:
            sp.pprint(eq)

def cubic_spline(xi, fi, spline_type, f=None, fd1=None):
    print("######## CUBIC SPLINE ########")

    n = xi.size
    x = sp.symbols("x")
    inter = []
    for i in range(xi.size-1):
        inter.append((xi[i], xi[i+1]))

    print(f"Interval: {inter}")

    inter_len = len(inter)
    Si = ["DUMMY_FUNC"]
    var_vector = []
    print("Si:")
    for i in range(inter_len):
        left_outer = inter[i][0] # the left outer point of the interval
        a, b, c, d = sp.symbols(f"a{i+1},b{i+1},c{i+1},d{i+1}")
        si = a + b*(x-left_outer) + c*((x-left_outer)**2) + d*((x-left_outer)**3)
        Si.append(si)
        var_vector.extend([a,b,c,d])
        print(f"\ns{i+1}(x):")
        sp.pprint(si)
    print()

    Sil = len(Si)
    SiD1 = ["DUMMY_FUNC"]
    SiD2 = ["DUMMY_FUNC"]
    print("derivative:")
    for i in range(1, Sil):
        d1 = sp.diff(Si[i], x)
        d2 = sp.diff(d1, x)
        SiD1.append(d1)
        SiD2.append(d2)
        print(f"\ns{i}'(x)")
        #print(f"s{i}'= {d1} \t\t s{i}'' = {d2}")
        sp.pprint(sp.expand(d1))
        print(f"\ns{i}''(x)")
        sp.pprint(d2)

    print("\nconditions:")
    inter_points = xi[1:n-1]
    ipl = len(inter_points)
    lgs = []
    # Stetigkeitsbedingung
    # for x1,...,xn-1
    for i in range(ipl):
        # Si'(xi) = Si+1'(xi)
        si1d1 = SiD1[i+1].subs(x, inter_points[i])
        si2d1 = SiD1[i+2].subs(x, inter_points[i])
        a1 = sp.Eq(si1d1, si2d1)

        # Si''(xi) = Si+1''(xi)
        si1d2 = SiD2[i+1].subs(x, inter_points[i])
        si2d2 = SiD2[i+2].subs(x, inter_points[i])
        a2 = sp.Eq(si1d2, si2d2)

        lgs.extend([a1, a2])
        sp.pprint(a1, wrap_line=False)
        sp.pprint(a2)

    # Interpolationsbedingungen
    for i in range(1, n):
        sim1 = Si[i].subs(x, xi[i-1])
        si = Si[i].subs(x, xi[i])

        b1 = sp.Eq(sim1, fi[i-1])
        b2 = sp.Eq(si, fi[i])

        lgs.extend([b1, b2])
        sp.pprint(b1)
        sp.pprint(b2)

    print()

    if spline_type == SPLINE_TYPE.natural:
        # natuerlicher spline
        print("natural spline")
        s1 = SiD2[1].subs(x, xi[0])
        sn = SiD2[n-1].subs(x, xi[n-1])

        append_equations(lgs, [(s1, 0), (sn, 0)])

    elif spline_type == SPLINE_TYPE.complete:
        # vollstaendiger spline 
        print("complete spline")
        if fd1 == None:
            print(f"ERROR: cubic_spline.py no func given")
            return None

        s1d1x0 = SiD1[1].subs(x, xi[0])
        snd1xn = SiD1[n-1].subs(x, xi[n-1])

        # fd1 = sp.diff(func, x)
        #fd1x0 = fd1.subs(x, xi[0])
        #fd1xn = fd1.subs(x, xi[n-1])
        #sp.pprint(fd1)
        #sp.pprint(fd1x0)
        #sp.pprint(fd1xn)

        fd1x0 = fd1(xi[0])
        fd1xn = fd1(xi[n-1])

        append_equations(lgs, [(s1d1x0, fd1x0), (snd1xn, fd1xn)])

    elif spline_type == SPLINE_TYPE.periodic:
        print("periodic spline")
        if f == None:
            print(f"ERROR: cubic_spline.py no func given")
            return None
        # check if periodic spline is possible
        if np.round(f(xi[0]), 6) != np.round(f(xi[n-1]), 6):
            print(f"ERROR: cubic_spline.py periodic spline is not possible f(x0) != f(xn)")
            return None

        s1d1x0 = SiD1[1].subs(x, xi[0])
        snd1xn = SiD1[n-1].subs(x, xi[n-1])

        s1d2x0 = SiD2[1].subs(x, xi[0])
        snd2xn = SiD2[n-1].subs(x, xi[n-1])

        append_equations(lgs, [(s1d1x0, snd1xn), (s1d2x0, snd2xn)])


    if len(lgs) != (4*inter_len):
        print(f"error: length of the LGS is wrong: {len(lgs)} != {(4*inter_len)}")

    # results
    print("\nRESULTS:")

    solved_lgs = sp.solve(lgs, var_vector)
    # print lgs
    print("LGS:")
    for g in lgs:
        sp.pprint(g)

    print("\nsolved LGS:")
    sp.pprint(solved_lgs)
    print("=")
    sp.pprint(sp.nsimplify(solved_lgs))

    sx = []
    for i in range(1, Sil):
        # get free_symbols and the value from the solved_lgs
        fs = list(Si[i].free_symbols)
        values_by_fs = []
        for s in fs:
            values_by_fs.append(solved_lgs.get(s))

        # map free_symbols and solved_lgs values
        sxi = Si[i]
        for j in range(len(fs)):
            if values_by_fs[j] != None:
                sxi = sxi.subs(fs[j], values_by_fs[j])

        sx.append((sxi, inter[i-1]))

        # print solved si
        print(f"\nS{i}: interval: {inter[i-1]}")
        sp.pprint(sxi)
        print("=")
        simp = sp.simplify(sxi)
        sp.pprint(simp)
        print("=")
        sp.pprint(sp.nsimplify(simp))

    ## return all si (functions)
    return sx

