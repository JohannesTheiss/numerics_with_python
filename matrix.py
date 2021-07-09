import numpy as np
import sympy as sp
import math

def ppMatrix(A):
    shape = A.shape
    new_ATA = sp.Matrix([])
    for i in range(shape[0]):
        curr_list = []
        for j in range(shape[1]):
            curr_list.append(sp.nsimplify(A[i,j]))
        new_ATA = new_ATA.row_join(sp.Matrix(curr_list))

    sp.pprint(new_ATA.T)
    return new_ATA



########### DEF... ###############
dt = np.dtype('f8')
pi = math.pi
e = math.e
prec = 7


######### inputs ###############
lx = np.array([(-3 + i) for i in range(0, 7)], dtype=dt)
fxi = lambda xk : np.abs(xk)
xi = fxi(lx)
print(xi)

# build Matrix
# ROUND CARE !!!!! UHHH
f1 = lambda xk : [np.round(math.sin(v * (pi/3)), prec) for v in xk]
f2 = lambda xk : [np.round(math.cos(v * (pi/3)), prec) for v in xk]
#f1 = lambda xk : [math.sin(v * (pi/3)) for v in xk]
#f2 = lambda xk : [math.cos(v * (pi/3)) for v in xk]

# rows | lines
line1 = sp.ones(1, 7).T
line2 = sp.Matrix([f1(xi)]).T
line3 = sp.Matrix([f2(xi)]).T
m = [line1, line2, line3]


if False:
    # print lines
    for i in range(len(m)):
        print(f"line{i}:")
        sp.pprint(m[i])

# make A
A = sp.Matrix([m])
simp_A = sp.simplify(A)

print("A")
sp.pprint(A)
print("=")
sp.pprint(simp_A)
print("=")
sp.pprint(sp.nsimplify(A))
print("=")
ppMatrix(A)


# AT
AT = A.T
print("AT:")
sp.pprint(AT)

# ATA 
ATA = AT * A
print("ATA:")
sp.pprint(ATA)
print("=")
ppMatrix(ATA)




