import sys
import re
import tests as t
from includes import utils as u, regex
from includes.types import Matrice, Rational, Function, Complex

data = {}

def evalMatriceComplex(exp):
    i = 0
    j = 0
    match = True
    tmp = {}

    while match:
        match = re.search(regex.checkMatrice, exp)
        if match:
            m = Matrice()
            string = match.group(0)
            key = "mat" + str(i)
            i += 1
            tmp[key] = m.parse(string)
            exp = exp.replace(string, key)

    match = True
    while match:
        match = re.search("(?:\W|^)(?!mat|com)(fun[a-zA-Z]\([a-zA-Z]+\)|[a-zA-Z]+)", exp)
        if match:
            key = match.group(1).strip()
            if key in data.keys():
                var = data[key]
                if var.getType() == "rational":
                    exp = exp.replace(match.group(0), var.str)
                elif var.getType() == "matrice":
                    tmp["mat" + str(i)] = var
                    exp = exp.replace(key, "mat" + str(i), 1)
                    i += 1
                elif var.getType() == "complex":
                    tmp["com" + str(j)] = var
                    exp = exp.replace(key, "com" + str(j), 1)
                    j += 1
            elif key[0:4] in data.keys():
                fn = re.match(regex.evalFunc, key)
                func = data[key[0:4]]
                if fn.group(2).strip() in data.keys():
                    param = data[fn.group(2).strip()]
                    # print(param.getType())
                    if param.getType() == "matrice":
                        # print("ok")
                        tmp["mat" + str(i)] = param.calc("fn", func)
                        exp = exp.replace(key, "mat" + str(i), 1)
                        i += 1
                    elif param.getType() == "complex":
                        # print("ok")
                        tmp["com" + str(j)] = param.calc("fn", func)
                        exp = exp.replace(key, "com" + str(j), 1)
                        j += 1
    # print(exp)
    match = True
    while match:
        match = re.search("(\d+|mat\d+|com\d+)\s*([\*\/\%\^])\s*(\d+|mat\d+|com\d+)", exp)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)), 1)
            else:
                if nb1.isnumeric() and nb2 in tmp.keys():
                    var = tmp[nb2]
                    if var.getType == "matrice":
                        key = "mat" + str(i)
                        i += 1
                    else:
                        key = "com" + str(j)
                        j += 1
                    tmp[key] = Rational(u.intFloatCast(nb1)).calc(ope, var)
                elif nb2 in tmp.keys() and nb1 in tmp.keys():
                    var1 = tmp[nb1]
                    var2 = tmp[nb2]
                    if var1.getType() == "complex" and var2.getType() == "complex":
                        key = "com" + str(j)
                        j += 1
                    else:
                        key = "mat" + str(i)
                        i += 1
                    tmp[key] = var1.calc(ope, var2)
                else:
                    if nb1 in tmp.keys():
                        var = tmp[nb1]
                        if var.getType == "matrice":
                            key = "mat" + str(i)
                            i += 1
                        else:
                            key = "com" + str(j)
                            j += 1
                        tmp[key] = var.calc(ope, Rational(u.intFloatCast(nb2)))
                exp = exp.replace(string, key, 1)
    match = True
    while match:
        match = re.search("(\d+|mat\d+|com\d+)\s*([\+\-])\s*(\d+|mat\d+|com\d+)", exp)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)), 1)
            else:
                # print(nb1)
                # print(ope)
                # print(nb2)
                if nb1 in tmp.keys() and nb2 in tmp.keys():
                    var1 = tmp[nb1]
                    var2 = tmp[nb2]
                    if var1.getType() == "complex" and var2.getType() == "complex":
                        key = "com" + str(j)
                        j += 1
                    else:
                        key = "mat" + str(i)
                        i += 1
                    tmp[key] = var1.calc(ope, var2)
                elif nb1.isnumeric() and nb2 in tmp.keys():
                        var = tmp[nb2]
                        if var.getType() == "complex":
                            key = "com" + str(j)
                            j += 1
                        else:
                            key = "mat" + str(i)
                            i += 1
                        tmp[key] = Rational(u.intFloatCast(nb1)).calc(ope, var)
                else:
                    # print("wtf")
                    if nb1 in tmp.keys():
                        # print("wtf")
                        var = tmp[nb1]
                        if var.getType() == "complex":
                            # print("wtf")
                            key = "com" + str(j)
                            j += 1
                        else:
                            key = "mat" + str(i)
                            i += 1
                            # print("mat0 + 5")
                        # print("wtf")
                        tmp[key] = var.calc(ope, Rational(u.intFloatCast(nb2)))
                exp = exp.replace(string, key, 1)
                i += 1
    if exp.strip() in tmp.keys():
        return tmp[exp.strip()]
    else:
        u.warn("Syntax error.", "error")


def evalFunction(exp):
    match = re.findall(regex.evalFunc, exp)

    if match:
        for m in match:
            fun = m[0]
            param = m[1]

            if fun in data.keys():
                fn = data[fun]
                if param.isnumeric():
                    exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(Rational(param)).value), exp)
                elif param in data.keys():
                    type = data[param].getType()
                    if type == "rational":
                        exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(data[param]).value), exp)
                    elif type == "matrice" or type == "complex":
                        continue
                else:
                    obj = evaluate(param)
                    if obj.getType() == "rational":
                        exp = exp.replace(fun + "(" + param + ")", str(round(fn.compute(obj).value, 2)))
                    else:
                        u.warn("The variable " + param + " is not assigned.", "error")
            else:
                u.warn("The function " + fun + " is not assigned.", "error")
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
    match = re.findall("(?:\W|^)(?!mat)(?!fun[A-Za-z])([a-zA-Z]+)", exp)
    saved = None
    if match:
        for m in match:
            if m in data.keys():
                type = data[m].getType()
                if type != saved and type != 'rational':
                    if saved is None:
                        saved = type
                    else:
                        return "mixed"
            else:
                u.warn("The variable " + m + " is not assigned.", "error")
    return saved


def evaluate(exp):
    exp = evalFunction(exp)                 # replace funX(y) || funX(5) by their result
    exp = evalRationals(exp)               # replace X || y by their result
    types = unknownTypes(exp)
    # print(exp)
    # print(re.match(regex.checkMatrice, exp))
    if types is not None or re.search(regex.checkMatrice, exp):
        # print("goEval")
        # print(exp)
        return evalMatriceComplex(exp)
       # print("stopEval")
    elif not re.match(regex.checkLetter, exp):
        # print("test")
        try:
            res = eval(exp)
            # print("ici?")
            return Rational(round(res, 2))
        except ZeroDivisionError:
            u.warn("Division by 0.", "error")
        except SyntaxError:
            u.warn("Syntax error.", "error")


def countUnknownVars(exp):
    match = True
    count = 0

    match = re.findall(regex.checkLetter, exp)
    for m in match:
        key = m.strip()
        if key in data.keys():
            exp = exp.replace(key, data[key].str)
        else:
            count += 1
    if count > 1:
        return None
    else:
        return exp

def parsePut(key, exp):
    value = ""
    if exp in data.keys():                                            # x = y     => assign x
        value = data[exp]
    else:
        match = re.match(regex.func, key)
        if match:
            exp = countUnknownVars(exp)
            if exp is not None:
                value = Function(exp, match.group(2))
                key = match.group(1)[0:4]
            else:
                u.warn("Too many unknown variables.", "error")
        else:
            if re.match(regex.checkMatrice, exp):
                mat = Matrice()
                value = Matrice.parse(mat, exp)
            elif re.match(regex.complex, exp):
                z = Complex()
                value = Complex.parse(z, exp)
            else:                            # x = 3 || x = y + 3 || x = funX(2) etc.
                value = evaluate(exp)
    data[key] = value
    data[key].print(None)


def parseGet(key):
    if key in data.keys():                                                                      # "x = ?"
        data[key].print(None)
    elif re.search(regex.checkLetter, key):
       # print("eval")
        res = evaluate(key)
        # print(res.getType())
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
        key = get.group(1).strip()
        if key == "" or '=' in key:
            u.warn("Syntax error.", "error")
       # print("get")
        parseGet(key)
    elif put:
        exp = put.group(2).strip()
        if exp == "" or '=' in exp or '?' in exp:
            u.warn("Syntax error.", "error")
        key = put.group(1).strip()
        if key == "i":
            u.warn("Can't assign the variable i.", "error")
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
            if line == "":
                print("\033[31m[Error]\033[0m Empty input.")
                continue
            elif line == "env":
                for index, var in enumerate(data):
                    var.print(index)
            else:
                try:
                   # print(line)
                    compute(line)
                except Exception:
                    pass
        except KeyboardInterrupt:
            sys.exit('')


main()
