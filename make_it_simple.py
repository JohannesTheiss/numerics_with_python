import numpy as np
import sympy as sp

SIMPLE_PRITNS = False
DERIVATIVE_PRINTS = True


############ INPUT ############# 
# define your vars like:
# x, y, z = sp.symbols("x,y,z")
x = sp.symbols("x")

# define your expression like:
exp = (-1*(x+1)) * ((x-1)/(-3)) * ((x-3)/(-5))


# choose some simplify function
simple_exp = sp.simplify(exp)
expand_exp = sp.expand(exp)
#trig_exp = sp.trigsimp(exp) # (for trigonometric expressions) 
#expand_exp1 = sp.expand(exp, trig=True)

#factor_exp = sp.factor(exp)

#pow_simp = sp.powsimp(exp) #(simplification of exponents)
#log_simp = sp.logcombine(exp)
#rad_simp = sp.radsimp(exp)


############# PRINT ############# 
if SIMPLE_PRITNS:
    print("INPUT EXPRESSION")
    sp.pprint(exp)

    print("\nSIMPLIFY")
    sp.pprint(simple_exp)

    print("\nEXPAND")
    sp.pprint(expand_exp)
    #sp.pprint(trig_exp)
    #sp.pprint(factor_exp)
    #sp.pprint(pow_simp)
    #sp.pprint(log_simp)
    #sp.pprint(rad_simp)

if DERIVATIVE_PRINTS:
    x = sp.symbols("x")
    f = x *  sp.sin(x) + sp.exp(x)

    I = sp.integrate(f, x)
    Iab = float(I.subs(x, sp.pi/2) - I.subs(x, 0))

    fd1 = f.diff(x)
    fd2 = fd1.diff(x)

    sp.pprint(f)
    sp.pprint(fd1)
    sp.pprint(fd2)

    xi = sp.pi/4
    error = (-1/24) * (sp.pi **3) * fd2

    mr = float((sp.pi/2) * f.subs(x, xi))

    sp.pprint(error)
    res = sp.simplify(error.subs(x, xi))
    print(f"{Iab} - {mr}")
    r1 = sp.Abs(Iab - mr)

    print(f"res = {r1} * 10^-2")







