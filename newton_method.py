import numpy as np
import sympy as sp

DELIMITER = "-----------------------------------------"


def print_with_start_vec(F, var, start_vec):
    print("=")
    print("print with start vec:")
    if len(var) != len(start_vec):
        print("ERROR print_with_start_vec")
        return

    f = F
    for i in range(len(var)):
        f = f.subs(var[i], start_vec[i])

    sp.pprint(f)

# THE ORDER OF THE xis is IMPORTANT for derivation !!!!
def newton_method(F, xis, start_vec):
    print("####### NEWTON METHOD ####### ")
    print("F(x):")
    sp.pprint(F)
    print_with_start_vec(F, xis, start_vec)

    # culc. F'
    Fd1 = sp.Matrix()
    for var in xis:
        fd1 = F.diff(var)
        Fd1 = Fd1.row_join(fd1)

    shape = sp.shape(Fd1)
    print(f"\nF'(x): ∊ {shape[0]}x{shape[1]}")
    sp.pprint(Fd1)
    print_with_start_vec(Fd1, xis, start_vec)

    #str_fd1 = sp.pretty(Fd1)
    #print("hasd", str_fd1)

    # if Fd1 is n x n
    if shape[0] == shape[1]:
        if shape[0] <= 2:
            print(DELIMITER)
            print("culc with: d^(k) = -[F'(x^(k))]^-1 * F(x^(x))")
            # culc det()
            det = Fd1.det()
            print("det(F'(x)) = ")
            sp.pprint(det)
            print_with_start_vec(det, xis, start_vec)

            print()
            if det != 0:
                # culc F'.inv
                Fd1_inv = Fd1.inv()
                print("[F'(x^(k))]^-1 = F'.inv")
                sp.pprint(Fd1_inv)
                print_with_start_vec(Fd1_inv, xis, start_vec)

                print(DELIMITER)
                # culc d
                print("d = ")
                d = (Fd1_inv * F)
                sp.pprint(d)
                d = sp.simplify(d)
                print("=")
                sp.pprint(d)
                print_with_start_vec(d, xis, start_vec)

                # culc φ 
                phi = sp.Matrix(xis) - d
                print("\n", sp.pretty(sp.symbols("phi")), " = ")
                sp.pprint(phi)
                phi = sp.simplify(phi)
                print("=")
                sp.pprint(phi)
                print_with_start_vec(d, xis, start_vec)

                return phi

            else:
                print("ERROR: newton_method.py: F'(x^(k)) is singular <=> det(F'(x^(k))) = 0")
                return None
        else:
            # culc with 3x3
            print(DELIMITER)
            print("culc with:  = [F'(x^(k))] * d^(k) = -F(x^(x))  ---> LGS")

            # culc. F'(x^(0)) and
            # culc. -F(x^(0))
            #Fd1x0 = Fd1
            #mFx0 = F
            #for i in range(len(xis)):
                #Fd1x0 = Fd1x0.subs(xis[i], start_vec[i])
                #mFx0 = mFx0.subs(xis[i], start_vec[i])

            #mFx0 = -mFx0

            #print(f"F'({start_vec})")
            #sp.pprint(Fd1x0)

            #print(f"-F({start_vec})")
            #sp.pprint(mFx0)

            #d1, d2, d3 = sp.symbols("d1, d2, d3")
            #solved_lgs = sp.linsolve([Fd1x0, mFx0], (d1, d2, d3))
            #d = sp.Matrix([list(solved_lgs)[0]]).T

            solved_lgs = sp.linsolve([Fd1, -F])
            sp.pprint(solved_lgs)
            d = sp.Matrix([list(solved_lgs)[0]]).T

            print(f"d = ")
            sp.pprint(d)
            print_with_start_vec(d, xis, start_vec)


            # culc φ 
            phi = sp.Matrix(xis) + d
            print("\n", sp.pretty(sp.symbols("phi")), " = ")
            sp.pprint(phi)
            phi = sp.simplify(phi)
            print("=")
            sp.pprint(phi)
            print_with_start_vec(d, xis, start_vec)

            return phi

    else:
        return None



def newton_method_iteration(phi, xis, number_of_iterations, start_vec_inter):
    print("####### NEWTON METHOD ITERATION ####### ")
    print(xis)
    print(start_vec_inter)
    #print(start_vec_inter.ndim)

    xk = phi
    xis_len = len(xis)

    # check if start point x^(0) given
    #if start_vec_inter.ndim == 1:
    iteration_steps = [start_vec_inter]
    for iteration in range(number_of_iterations):
        curr_phi = phi # get phi
        curr_approx = iteration_steps[-1]

        for i in range(xis_len):
            curr_phi = curr_phi.subs(xis[i], curr_approx[i])

        print(f"\nx^({iteration+1}) = φ(x^({iteration}))")
        sp.pprint(curr_phi)
        iteration_steps.append(curr_phi)

    #else:
        # TODO
        # interval is given
        # so check if all the point in start_vec_inter conv.
        #pass



# numpy datatype: float64
dt = np.dtype('f8')

# define variables and the order of derivation
#xis =[x1, x2] = sp.symbols("x1, x2")
#xis =[x, y, z] = sp.symbols("x, y, z")

# define Function
# ⎡  3     3    ⎤
# ⎢x₁  + x₂  - 4⎥
# ⎢             ⎥
# ⎢    3     3  ⎥
# ⎣  x₁  - x₂   ⎦
# line 1
#f1 = (x1**3) + (x2**3) - 4
# line 2
#f2 = (x1**3) - (x2**3)
#F = sp.Matrix([[f1], [f2]])

xis =[x, y, z] = sp.symbols("x, y, z")
f1 = 2*x**2 - z
f2 = 1 + (y**2)*x
f3 = x**2 + z**2 - 1
F = sp.Matrix([[f1], [f2], [f3]])
start_vec = [1, 1, 0]



# define the number of iterations the newton_method should do
number_of_iterations = 1

#define the start_vec of the interation
#strt_vec = [1, 1]


# bsp: x**2 = 0
# start: x0 = 1
#x1 = sp.symbols("x1")
#xis = [x1]
#f1 = x1**2
#F = sp.Matrix([[f1]])
#start_vec = [1]


phi = newton_method(F, xis, start_vec)
if phi != None:
    ite = newton_method_iteration(phi, xis, number_of_iterations, start_vec)



#### OLD CODE ####
#dim = 2
#fixed_point = sp.zeros(dim, 1) # 0 vector
#steps_in_inter = 5
#x1_inter = np.linspace(1, 2, steps_in_inter)  # [1, 2]
#x2_inter = np.linspace(1, 2, steps_in_inter) # [1, 2]
#start_vec_inter = np.matrix([x1_inter, x2_inter], dtype=dt) # [1, 2] x [1, 2]
#start_vec_inter = np.array([1, 1], dtype=dt)


