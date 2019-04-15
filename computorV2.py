import sys
import re
import tests as t
from includes import utils as u, regex
from includes.types import Matrice, Rational, Function, Complex

data = {}


def evalComplex(exp):
    i = 0
    match = True
    complexes = {}
    while match:
        # print(exp)
        match = re.search("(?:\W|^)(?!com)(fun[a-zA-Z]\([a-zA-Z]+\)|[a-zA-Z]+)", exp)
        # print(match)
        if match:
            # print(match)
            key = match.group(1).strip()
            # print(key)
            if key in data.keys():
                var = data[key]
                if var.getType() == "rational":
                    exp = exp.replace(match.group(0), var.str)
                elif var.getType() == "complex":
                    complexes["com" + str(i)] = var
                    exp = exp.replace(key, "com" + str(i), 1)
                    i += 1
            elif key[0:4] in data.keys():
                fn = re.match(regex.evalFunc, key)
                func = data[key[0:4]]
                if fn.group(2).strip() in data.keys():
                    c = data[fn.group(2).strip()]
                    complexes["com" + str(i)] = c.calc("fn", func)
                    exp = exp.replace(key, "com" + str(i), 1)
                    i += 1
    # print(exp)
    match = True
    while match:
        match = re.search("(\d+|com\d+)\s*([\*\/\%\^])\s*(\d+|com\d+)", exp)
        # print(match)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            # print(nb1)
            # print(ope)
            # print(nb2)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)))
            else:
                c = Complex()
                if nb1.isnumeric() and not nb2.isnumeric():
                    if ope == '/' or ope == '%' or ope == '^':
                        u.warn("Can't resolve Rational " + ope + " Complex.", "error")
                    if nb2 in complexes.keys():
                        c = complexes[nb2].calc(ope, Rational(u.intFloatCast(nb1)))
                elif not nb1.isnumeric() and not nb2.isnumeric():
                    if nb2 in complexes.keys() and nb1 in complexes.keys():
                        c = complexes[nb2].calc(ope, complexes[nb1])
                else:
                    if nb1 in complexes.keys():
                        c = complexes[nb1].calc(ope, Rational(u.intFloatCast(nb2)))
                        complexes["com" + str(i)] = c
                exp = exp.replace(string, "com" + str(i), 1)
                complexes["com" + str(i)] = c
                i += 1
    match = True
    # print(exp)
    while match:
        match = re.search("(\d+|com\d+)\s*([\+\-])\s*(\d+|com\d+)", exp)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)))
            else:
                if nb1[0:3] == "com" and nb2[0:3] == "com":
                    c = complexes[nb1]
                    d = complexes[nb2]
                    complexes["com" + str(i)] = c.calc(ope, d)
                elif nb1.isnumeric() and nb2[0:3] == "com":
                    c = complexes[nb2]
                    complexes["mat" + str(i)] = c.calc(ope, Rational(u.intFloatCast(nb1)))
                else:
                    c = complexes[nb1]
                    complexes["com" + str(i)] = c.calc(ope, Rational(u.intFloatCast(nb2)))
                exp = exp.replace(string, "com" + str(i))
                i += 1
    return complexes["com" + str(i - 1)]


def evalMatrice(exp):
    i = 0
    match = True
    matrices = {}
    while match:
        # print(exp)
        match = re.search("(?:\W|^)(?!mat)(fun[a-zA-Z]\([a-zA-Z]+\)|[a-zA-Z]+)", exp)
        # print(match)
        if match:
            # print(match)
            key = match.group(1).strip()
            # print(key)
            if key in data.keys():
                var = data[key]
                if var.getType() == "rational":
                    exp = exp.replace(match.group(0), var.str)
                elif var.getType() == "matrice":
                    matrices["mat" + str(i)] = var
                    exp = exp.replace(key, "mat" + str(i), 1)
                    i += 1
            elif key[0:4] in data.keys():
                fn = re.match(regex.evalFunc, key)
                func = data[key[0:4]]
                if fn.group(2).strip() in data.keys():
                    m = data[fn.group(2).strip()]
                    matrices["mat" + str(i)] = m.calc("fn", func)
                    exp = exp.replace(key, "mat" + str(i), 1)
                    i += 1
    # print(exp)
    match = True
    while match:
        match = re.search("(\d+|mat\d+)\s*([\*\/\%\^])\s*(\d+|mat\d+)", exp)
        # print(match)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            # print(nb1)
            # print(ope)
            # print(nb2)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)))
            else:
                m = Matrice()
                if nb1.isnumeric() and not nb2.isnumeric():
                    if ope == '/' or ope == '%' or ope == '^':
                        u.warn("Can't resolve Rational " + ope + " Matrice.", "error")
                    if nb2 in matrices.keys():
                        m = matrices[nb2].calc(ope, Rational(u.intFloatCast(nb1)))
                elif not nb1.isnumeric() and not nb2.isnumeric():
                    if nb2 in matrices.keys() and nb1 in matrices.keys():
                        print("calc")
                        m = matrices[nb2].calc(ope, matrices[nb1])
                        print("end calc")
                else:
                    if nb1 in matrices.keys():
                        m = matrices[nb1].calc(ope, Rational(u.intFloatCast(nb2)))
                exp = exp.replace(string, "mat" + str(i))
                matrices["mat" + str(i)] = m
                i += 1
    match = True
    while match:
        match = re.search("(\d+|mat\d+)\s*([\+\-])\s*(\d+|mat\d+)", exp)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)))
            else:
                if nb1[0:3] == "mat" and nb2[0:3] == "mat":
                    m = matrices[nb1]
                    n = matrices[nb2]
                    matrices["mat" + str(i)] = m.calc(ope, n)
                elif nb1.isnumeric() and nb2[0:3] == "mat":
                    m = matrices[nb2]
                    matrices["mat" + str(i)] = m.calc(ope , Rational(u.intFloatCast(nb1)))
                else:
                    m = matrices[nb1]
                    matrices["mat" + str(i)] = m.calc(ope, Rational(u.intFloatCast(nb2)))
                exp = exp.replace(string, "mat" + str(i))
                i += 1
    return matrices["mat" + str(i - 1)]


def evalFunction(exp):
    # print("evalfunc")
    match = re.findall(regex.evalFunc, exp)
    # print("MAAAAAAAATTTTTTCHCHHCHH")
    if match:
        for m in match:
            # print("match")
            # print(m)
            fun = m[0]
            param = m[1]
            # print(param)
            if fun in data.keys():
                fn = data[fun]
                if param.isnumeric():
                    # print("param isnum")
                    exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(param)), exp)
                elif param in data.keys():
                    type = data[param].getType()
                    # print("param in keys")
                    if type == "rational":
                        exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(data[param].value)), exp)
                    elif type == "matrice" or type == "complex":
                        continue
                    else:
                        u.warn("TODO: funX(matrice | complexe | x + 5)", "error")
                else:
                    obj = evaluate(param)
                    # print(obj.value)
                    # obj.print(None)
                    if obj.getType() == "rational":
                        exp = exp.replace(fun + "(" + param + ")", str(round(fn.compute(obj.value), 2)))
                        # print(exp)
                    else:
                        u.warn("The variable " + param + " is not assigned.", "error")
            else:
                u.warn("The function " + fun + " is not assigned.", "error")
    # print(exp)
    return exp


def evalRationals(exp):
    match = re.findall(regex.checkLetter, exp)        # replace X || y by their result
    if match:
        for m in match:
            var = m[0]
            if var in data.keys():
                if data[var].getType() == "rational":
                    exp = re.sub(var, str(data[var].str), exp)
    return exp


def unknownTypes(exp):
    # print("UK")
    match = re.findall("(?:\W|^)(?!mat)(?!fun[A-Za-z])([a-zA-Z]+)", exp)
    saved = None
    # print(match)
    if match:
        for m in match:
            # print(m)
            if m in data.keys():
                type = data[m].getType()
                if type != saved and type != 'rational':
                    if saved is None:
                        saved = type
                    else:
                        return "mixed"
    # print(saved)
    return saved

def evaluate(exp):
    exp = evalFunction(exp)                 # replace funX(y) || funX(5) by their result
    # print(exp)
    exp = evalRationals(exp)                    # replace X || y by their result
    # print(exp)
    types = unknownTypes(exp)
    # print(types)
    # match = re.search(regex.checkLetter, exp)
    # print(match)
    # print("wtf")
    if types is not None:
        # print(types)
        # print(exp)
        # print(exp)
        if types == 'matrice':
            return evalMatrice(exp)
        elif types == 'complex':
            # u.warn("evalComplex", "error")
            return evalComplex(exp)
        elif types == 'mixed':
            u.warn("Can't compute mixed Matrices and Complexes", "error")
        # res.print(None)
    else:
        # print('YP')
        # print(exp)
        try:
            res = eval(exp)
            # print(round(res, 2))
            return Rational(round(res, 2))
        except ZeroDivisionError:
            u.warn("Division by 0.", "error")
        except SyntaxError:
            u.warn("Syntax error.", "error")


def parsePut(key, exp):
    value = ""
    if exp in data.keys():                                            # x = y     => assign x
        value = data[exp]
    else:
        match = re.match(regex.func, key)
        if match:
            if u.countUnknownVars(exp) == 1:
                value = Function(exp, match.group(2))
                key = match.group(1)[0:4]
            else:
                u.warn("Too many unknown variables.", "error")
        else:
            if re.match(regex.checkMatrice, exp):
                mat = Matrice()
                value = Matrice.parse(mat, exp)
            elif re.match(regex.complex, exp):
                # print('complex detected')
                z = Complex()
                value = Complex.parse(z, exp)
            else:
                # newType = u.checkType(exp, data)
                # if newType == "rational" or newType == "matrice":                                       # x = 3 || x = y + 3 || x = funX(2) etc.
                value = evaluate(exp)
                # else:
                #     u.warn("TODO : gestion des complexes", "error")
    # if value is not None:
    data[key] = value
    data[key].print(None)


def parseGet(key):
    if key in data.keys():                                                                      # "x = ?"
        data[key].print(None)
    elif re.search(regex.checkLetter, key):
        # print("eval")
        res = evaluate(key)
        # print("YO")
        # print("print")
        res.print(None)
    else:                                                  # "5 + 5 = ?"
        try:
            res = eval(u.formatLine(key))
            u.out(res)
        except ZeroDivisionError:
            u.warn("Division by 0.", "error")
        except SyntaxError:
            u.warn("Syntax error.", "error")


def compute(line):
    get = re.match(regex.get, line)
    put = re.match(regex.put, line)
    if get:
        print("get")
        # print(get)
        key = get.group(1).strip()
        if key == "" or '=' in key:
            u.warn("Syntax error.", "error")
        parseGet(key)
    elif put:
        # print("put")
        # print(put)
        exp = put.group(2).strip()
        # print(exp)
        if exp == "" or '=' in exp or '?' in exp:
            u.warn("Syntax error.", "error")
        key = put.group(1).strip()
        parsePut(key, exp)
    else:
        u.warn("Syntax error.", "error")


def main():

    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        t.test = True

    line = ""
    while line is not None:
        try:
            line = u.read_in()
            if line == "env":
                for index, var in enumerate(data):
                    var.print(index)
            else:
                try:
                    compute(line)
                except Exception:
                    pass
        except KeyboardInterrupt:
            sys.exit('')


main()
