import numpy as np
import sympy as sp

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


