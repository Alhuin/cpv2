test = False

i = 0

tests = [

    {"input": "desc", "output": "Bad syntax"},
    {"input": "x == 5", "output": "\033[31m[Error]\033[0m Syntax error."},
    {"input": "x = 5 = ?", "output": "\033[31m[Error]\033[0m Syntax error."},
    {"input": "x = 3 + 5 ?", "output": "\033[31m[Error]\033[0m Syntax error."},
    {"input": "x + 8 = 5", "output": "\033[31m[Error]\033[0m Syntax error."},
    {"input": "x = 10 / 0", "output": "\033[31m[Error]\033[0m Division by 0."},
    {"input": "x = 5", "output": "5"},
    {"input": "x / 0 = ?", "output": "\033[31m[Error]\033[0m Division by 0."},
    {"input": "x / 0 ?", "output": "\033[31m[Error]\033[0m Syntax error."},

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

    {"input": "desc", "output": "Assignation et calculs de fonctions"},
    {"input": "funX(x) = 5x^2", "output": "5x^2"},
    {"input": "funX = ?", "output": "5x^2"},
    {"input": "funX(2) = ?", "output": "20"},
    {"input": "funX(x) = ?", "output": "-16.2"},
    {"input": "funX(x + 2) = ?", "output": "0.2"},
    {"input": "funX(x) + y = ?", "output": "-4.2"},
    {"input": "funY(y)= y + 6", "output": "y + 6"},
    {"input": "funX(2) + funY(5) = ?", "output": "31"},
    {"input": "funA(z) = z + w", "output": "\033[31m[Error]\033[0m Too many unknown variables."},
    {"input": "z = funX(x) + 7 - funY(3)", "output": "-18.2"},
    {"input": "z*2 = ?", "output": "-36.4"},

    {"input": "desc", "output": "Assignation et calculs de matrices"},
    {"input": "z = [[1,2];[2,3]]", "output": "[ 1, 2 ]\n  [ 2, 3 ]\n  "},
    {"input": "z = ?", "output": "[ 1, 2 ]\n  [ 2, 3 ]\n  "},
    {"input": "z * 2 = ?", "output": "[ 2, 4 ]\n  [ 4, 6 ]\n  "},
    {"input": "v = [[5,12];[50,23]]", "output": "[ 5, 12 ]\n  [ 50, 23 ]\n  "},
    {"input": "v - z + 5 * 2 + v = ?", "output": "[ 19, 32 ]\n  [ 108, 53 ]\n  "},
    {"input": "v * z = ?", "output": "[ 5, 24 ]\n  [ 100, 69 ]\n  "},
    {"input": "v^2 = ?", "output": "[ 25, 144 ]\n  [ 2500, 529 ]\n  "},
    {"input": "2^v = ?", "output": "\033[31m[Error]\033[0m Can't resolve Rational ^ Matrice."},
    {"input": "5-z=?", "output": "\033[31m[Error]\033[0m Can't resolve Rational - Matrice."},
    {"input": "z%2=?", "output": "[ 1, 0 ]\n  [ 0, 1 ]\n  "},
    {"input": "z^2=?", "output": "[ 1, 4 ]\n  [ 4, 9 ]\n  "},
    {"input": "z^v=?", "output": "\033[31m[Error]\033[0m Can't resolve Matrice ^ Matrice."},

    {"input": "desc", "output": "Fonctions x Matrices"},
    {"input": "funX(z)=?", "output": "[ 5, 20 ]\n  [ 20, 45 ]\n  "},
    {"input": "a = funX(z) - funX(2)", "output": "[ -15, 0 ]\n  [ 0, 25 ]\n  "},
    {"input": "a = ?", "output": "[ -15, 0 ]\n  [ 0, 25 ]\n  "},

    {"input": "desc", "output": "Assignation et calcul de complexes"},
    {"input": "c = 5 + 3i", "output": "5 + 3i"},
    {"input": "c = ?", "output": "5 + 3i"},
    {"input": "c + 5 = ?", "output": "10 + 3i"},
    {"input": "a = c + 5", "output": "10 + 3i"},
    {"input": "a = ?", "output": "10 + 3i"},
    {"input": "a * 5 = ?", "output": "50 + 15i"},
    {"input": "b = a * 5 + 8", "output": "58 + 15i"},
    {"input": "a * b = ?", "output": "535 + 324i"},

]

category = ""

ret = ""

warn = False

def test_output(output):

    global tests, test, i, ret, warn

    if tests[i]["output"] == str(output):
        print(ret.ljust(40) + "|    \033[32mOK\033[0m")
    else:
        print(ret.ljust(40) + "|    \033[31mKO\033[0m\n\n>>>>>>>>>>>>>>>>>>>>>")
        print("expected : ")
        print(tests[i]["output"])
        print("output : ")
        print(str(output) + "\n<<<<<<<<<<<<<<<<<<<<\n")
    i += 1

