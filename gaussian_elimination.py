import numpy as np
import sympy as sp

class LGS:
    def __init__(self, A, b):
        self.dim, n = A.shape
        if self.dim != n:
            print(f"ERROR: LGS: i need a nxn Matrix but got: {self.dim}x{n}")
            return None
        if self.dim != b.shape[0]:
            print(f"ERROR: LGS: f vector need to be in same dim as A: (f is {b.shape[1]})")
            return None

        self.A = A
        self.b = b

    def print(self, new_line=False):
        for i in range(self.dim):
            #line = str(self.A[i, :]) + "\t| " + str(self.b[i, :])
            line = []
            for j in range(self.dim):
                line.append(str(self.A[i,j]))

            line.append("|")
            line.append(str(b[i]))
            print("\t".join(line))

        if new_line:
            print()



def gauss(lgs):
    # !!! geht nicht wenn erste spalte eine Null-spalte !!!!!
    print("############## Gaussian Elimination ##############")
    #sp.pprint(A)
    #sp.pprint(b)
    lgs.print(True)
    A = lgs.A
    b = lgs.b
    n = lgs.dim


    for ii in range(n):
        aii = A[ii, ii]
        for row_i in range(n-1, ii, -1):
            if A[row_i, ii] == 0:
                continue
            lam = -A[row_i, ii] / aii
            print(f"row_{row_i} * {lam}")

            for col_i in range(n):
                print(f"({A[ii, col_i]} * {lam}) + {A[row_i, col_i]}", end=" = ")
                A[row_i, col_i] = A[row_i, col_i] + (A[ii, col_i] * lam)
                print(A[row_i, col_i])
                lgs.print(True)

            print(f"{b[0, 0]} * {lam} + {b[row_i, 0]}", end=" = ")
            b[row_i, 0] = b[row_i, 0] + (b[0, 0] * lam)
            print(b[row_i, 0])
            lgs.print(True)

            print()


#Al = [[7, 0, -1], [0, 3, 0], [-1, 0, 4]]
#bl = [12, 0, -7]
Al = [[2, 1, -1], [-3, -1, 2], [-2, 1, 2]]
bl = [8, -11, -3]

#Al = [[2, -3, 1], [1, -1, 2], [3, 1, -1]]
#bl = [-1, -3, 9]

A = sp.Matrix(Al)
b = sp.Matrix(bl)

lgs = LGS(A, b)
gauss(lgs)


