test = False

i = 0

ret = ""

tests = [

    {"input": "desc", "output": "Bad syntax"},
    {"input": "x == 5", "output": "\033[31m[SyntaxError]\033[0m Invalid input."},
    {"input": "x = 22e-+dd5-+", "output": "\033[31m[NameError]\033[0m The variable e is not assigned."},
    {"input": "x = g", "output": "\033[31m[NameError]\033[0m The variable g is not assigned."},
    {"input": "x = 5 = ?", "output": "\033[31m[SyntaxError]\033[0m Invalid input."},
    {"input": "x = 3 + 5 ?", "output": "\033[31m[SyntaxError]\033[0m Invalid input."},
    {"input": "x + 8 = 5", "output": "\033[31m[SyntaxError]\033[0m Invalid input."},
    {"input": "x = 10 / 0", "output": "\033[31m[ComputeError]\033[0m Division by 0."},
    {"input": "x = 5", "output": "5"},
    {"input": "x / 0 = ?", "output": "\033[31m[ComputeError]\033[0m Division by 0."},
    {"input": "x / 0 ?", "output": "\033[31m[SyntaxError]\033[0m Invalid input."},
    {"input": "i = 8", "output": "\033[31m[NameError]\033[0m Can't assign the variable i."},
    {"input": "env", "output": ""},

    {"input": "desc", "output": "Assignation et calculs de réels"},
    {"input": "x = 5", "output": "5"},
    {"input": "x = ?", "output": "5"},
    {"input": "x = 5 + 8 * 2", "output": "21"},
    {"input": "x + 2 = ?", "output": "23"},
    {"input": "y = 10", "output": "10"},
    {"input": "y + x = ?", "output": "31"},
    {"input": "y = y + 2", "output": "12"},
    {"input": "x = ?", "output": "21"},
    {"input": "x = y - 13.80", "output": "-1.8"},
    {"input": "8 + 2 = ?", "output": "10"},
    {"input": "4^2 = ?", "output": "16"},
    {"input": "2 * 5^2 = ?", "output": "50"},
    {"input": "env", "output": ""},

    {"input": "desc", "output": "Assignation et calculs de fonctions"},
    {"input": "funX(x) = 5x^2", "output": "5x^2"},
    {"input": "funX = ?", "output": "5x^2"},
    {"input": "funX(2) = ?", "output": "20"},
    {"input": "x = -3", "output": "-3"},
    {"input": "funX(x) = ?", "output": "45"},
    {"input": "x = -1.8", "output": "-1.8"},
    {"input": "funX(x + 2) = ?", "output": "0.2"},
    {"input": "funX(x) + y = ?", "output": "28.2"},
    {"input": "funY(b)= b + 6", "output": "b + 6"},
    {"input": "funX(2) + funY(5) = ?", "output": "31"},
    {"input": "funA(q) = q + w", "output": "\033[31m[SyntaxError]\033[0m Too many unknown variables."},
    {"input": "z = funX(x) + 7 - funY(3)", "output": "14.2"},
    {"input": "z*2 = ?", "output": "28.4"},
    {"input": "funX(3) = ?", "output": "45"},
    {"input": "env", "output": ""},

    {"input": "desc", "output": "Assignation et calculs de matrices"},
    {"input": "z = [[1,2];[2,3]]", "output": "[ 1, 2 ]\n  [ 2, 3 ]\n  "},
    {"input": "z = ?", "output": "[ 1, 2 ]\n  [ 2, 3 ]\n  "},
    {"input": "z * 2 = ?", "output": "[ 2, 4 ]\n  [ 4, 6 ]\n  "},
    {"input": "v = [[5,12];[50,23]]", "output": "[ 5, 12 ]\n  [ 50, 23 ]\n  "},
    {"input": "v - z + 5 * 2 + v = ?", "output": "\033[31m[ComputeError]\033[0m Can't add a rational to a matrice."},
    {"input": "v * z = ?", "output": "[ 29, 46 ]\n  [ 96, 169 ]\n  "},
    {"input": "v^2 = ?", "output": "[ 625, 336 ]\n  [ 1400, 1129 ]\n  "},
    {"input": "2^v = ?", "output": "\033[31m[ComputeError]\033[0m Can't elevate a rational to a matrice."},
    {"input": "5-z=?", "output": "\033[31m[ComputeError]\033[0m Can't substract a matrice to a rational."},
    {"input": "z%2=?", "output": "[ 1, 0 ]\n  [ 0, 1 ]\n  "},
    {"input": "z^3=?", "output": "[ 21, 34 ]\n  [ 34, 55 ]\n  "},
    {"input": "z^v=?", "output": "\033[31m[ComputeError]\033[0m Can't elevate a matrice to a matrice."},
    {"input": "z/v=?", "output": "\033[31m[ComputeError]\033[0m Can't divide a matrice by a matrice."},
    {"input": "z/2=?", "output": "[ 0.5, 1.0 ]\n  [ 1.0, 1.5 ]\n  "},
    {"input": " a = [[5];[2]]", "output": "[ 5 ]\n  [ 2 ]\n  "},
    {"input": " a * z = ?", "output": "\033[31m[ComputeError]\033[0m Can't resolve m1 * m2 : Number of raws in m1 doesn't match number of columns in m2."},
    {"input": " a = [[5,2]]", "output": "[ 5, 2 ]\n  "},
    {"input": " a * z = ?", "output": "[ 9, 16 ]\n  "},
    {"input": "env", "output": ""},

    {"input": "desc", "output": "Assignation et calcul de complexes"},
    {"input": "c = 5 + 3i", "output": "5 + 3i"},
    {"input": "y = -4i", "output": "-4i"},
    {"input": "c = ?", "output": "5 + 3i"},
    {"input": "c + 5 = ?", "output": "10 + 3i"},
    {"input": "a = c + 5", "output": "10 + 3i"},
    {"input": "a = ?", "output": "10 + 3i"},
    {"input": "a * 5 = ?", "output": "50 + 15i"},
    {"input": "b = a * 5 + 8", "output": "58 + 15i"},
    {"input": "a * b = ?", "output": "535 + 324i"},
    {"input": "a * b = ?", "output": "535 + 324i"},
    {"input": "a = 20 - 4i", "output": "20 -4i"},
    {"input": "b = 3 + 2i", "output": "3 + 2i"},
    {"input": "a / b = ?", "output": "4 -4i"},

    {"input": "env", "output": ""},

    {"input": "desc", "output": "Complex x Matrices"},
    {"input": " a * z = ?", "output": "[ 20 -4i, 40 -8i ]\n  [ 40 -8i, 60 -12i ]\n  "},

    {"input": "desc", "output": "Fonctions x Matrices"},
    {"input": "funX(z)=?", "output": "[ 25, 40 ]\n  [ 40, 65 ]\n  "},
    {"input": "a = funX(z) - funX(2)", "output": "\033[31m[ComputeError]\033[0m Can't substract a rational to a matrice."},
    {"input": "a = funX(z) - z", "output": "[ 24, 38 ]\n  [ 38, 62 ]\n  "},
    {"input": "a = ?", "output": "[ 24, 38 ]\n  [ 38, 62 ]\n  "},
    {"input": "env", "output": ""},

    {"input": "desc", "output": "Fonctions x Complexes"},
    {"input": "funX(c) = ?", "output": "80 + 150i"},
    {"input": "funA(s) = 5+6-8s^2", "output": "5+6-8s^2"},
    {"input": "d = 5+3i", "output": "5 + 3i"},
    {"input": "funA(d) = ?", "output": "-117 -240i"},
    {"input": "env", "output": ""},

]


def test_output(output):

    global tests, test, i, ret

    if tests[i]["output"] == str(output):
        print(ret.ljust(40) + "|    \033[32mOK\033[0m")
    else:
        print(ret.ljust(40) + "|    \033[31mKO\033[0m\n\n>>>>>>>>>>>>>>>>>>>>>")
        print("expected : ")
        print(tests[i]["output"])
        print("output : ")
        print(str(output) + "\n<<<<<<<<<<<<<<<<<<<<\n")
    i += 1

