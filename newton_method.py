import numpy as np
import sympy as sp

DELIMITER = "-----------------------------------------"

# THE ORDER OF THE xis is IMPORTANT for derivation !!!!
def newton_method(F, xis):
    print("####### NEWTON METHOD ####### ")
    print("F(x):")
    sp.pprint(F)

    Fd1 = sp.Matrix()
    for var in xis:
        fd1 = F.diff(var)
        Fd1 = Fd1.row_join(fd1)

    shape = sp.shape(Fd1)
    print(f"\nF'(x): ∊ {shape[0]}x{shape[1]}")
    sp.pprint(Fd1)
    #str_fd1 = sp.pretty(Fd1)
    #print("hasd", str_fd1)

    # if Fd1 is n x n
    if shape[0] == shape[1]:
        print(DELIMITER)
        print("culc with: d^(k) = -[F'(x^(k))]^-1 * F(x^(x))")
        # culc det()
        det = Fd1.det()

        print("det(F'(x)) = ")
        sp.pprint(det)

        print()
        if det != 0:
            Fd1_inv = Fd1.inv()
            print("[F'(x^(k))]^-1 = F'.inv")
            sp.pprint(Fd1_inv)

            print(DELIMITER)
            # culc d
            print("d = ")
            d = (Fd1_inv * F)
            sp.pprint(d)
            d = sp.simplify(d)
            print("=")
            sp.pprint(d)

            # culc φ 
            phi = sp.Matrix(xis) - d
            print("\n", sp.pretty(sp.symbols("phi")), " = ")
            sp.pprint(phi)
            phi = sp.simplify(phi)
            print("=")
            sp.pprint(phi)

            return phi


        else:
            print("ERROR: newton_method.py: F'(x^(k)) is singular <=> det(F'(x^(k))) = 0")
            return None

    else:
        return None



def newton_method_iteration(phi, xis, number_of_iterations, fixed_point, start_vec_inter):
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

        print(f"x^({iteration+1})")
        sp.pprint(curr_phi)
        iteration_steps.append(curr_phi)

    #else:
        # TODO
        # interval is given
        # so check if all the point in start_vec_inter conv.
        #pass



dt = np.dtype('f8')

dim = 2
# define Function
xis =[x1, x2] = sp.symbols("x1, x2")
f1 = (x1**3) + (x2**3) - 4
f2 = (x1**3) - (x2**3)
F = sp.Matrix([[f1], [f2]])

number_of_iterations = 5

# define order of derivation
#xis = [x1, x2, z]

fixed_point = sp.zeros(dim, 1) # 0 vector

steps_in_inter = 5
x1_inter = np.linspace(1, 2, steps_in_inter)  # [1, 2]
x2_inter = np.linspace(1, 2, steps_in_inter) # [1, 2]
#start_vec_inter = np.matrix([x1_inter, x2_inter], dtype=dt) # [1, 2] x [1, 2]

#start_vec_inter = np.array([1, 1], dtype=dt)
start_vec_inter = [1, 1]


phi = newton_method(F, xis)
if phi != None:
    ite = newton_method_iteration(phi, xis, number_of_iterations, fixed_point, start_vec_inter)


