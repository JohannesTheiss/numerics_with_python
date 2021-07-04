import sympy as sp
import enum

class SPLINE_TYPE(enum.Enum):
     natural = 0
     complete = 1
     periodic = 2


def cubic_spline(xi, fi, spline_type, func=None):
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
        print(f"\ns{i+1}'(x)")
        #print(f"s{i}'= {d1} \t\t s{i}'' = {d2}")
        sp.pprint(d1)
        print(f"\ns{i+1}''(x)")
        sp.pprint(d2)

    print("\nconditions:")
    inter_points = xi[1:n-1]
    ipl = len(inter_points)
    lgs = []
    for i in range(ipl):
        si1d1 = SiD1[i+1].subs(x, inter_points[i])
        si2d1 = SiD1[i+2].subs(x, inter_points[i])
        a1 = sp.Eq(si1d1, si2d1)

        si1d2 = SiD2[i+1].subs(x, inter_points[i])
        si2d2 = SiD2[i+2].subs(x, inter_points[i])
        a2 = sp.Eq(si1d2, si2d2)

        lgs.extend([a1, a2])
        sp.pprint(a1)
        sp.pprint(a2)


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
        eq1 = sp.Eq(s1, 0)
        eq2 = sp.Eq(sn, 0)

        lgs.extend([eq1, eq2])
        sp.pprint(eq1)
        sp.pprint(eq2)

    elif spline_type == SPLINE_TYPE.complete:
        # vollstaendiger spline 
        pass


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
        sp.pprint(sp.simplify(sxi))

    ## return all si (functions)
    return sx

