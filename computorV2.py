import sys
import re
from includes import utils as u, regex
from includes.types import Matrice, Real, Function

data = {}


def evalMatrice(exp):
    i = 0
    match = True
    matrices = {}
    while match:
        match = re.search("(?:\W|^)(?!mat)([A-za-z]+)", exp)
        if match:
            key = match.group(0).strip()
            if key in data.keys():
                var = data[key]
                if var.getType() == "real":
                    exp = exp.replace(match.group(0), var.str)
                elif var.getType() == "matrice":
                    matrices["mat" + str(i)] = var
                    exp = exp.replace(key, "mat" + str(i))
                    i += 1
    match = True
    while match:
        match = re.search("(\d+|mat\d+)\s*([\*\/\%])\s*(\d+|mat\d+)", exp)
        if match:
            string = match.group(0)
            nb1 = match.group(1)
            ope = match.group(2)
            nb2 = match.group(3)
            if nb1.isnumeric() and nb2.isnumeric():
                exp = exp.replace(string, str(eval(string)))
            else:
                m = Matrice()
                if nb1.isnumeric() and not nb2.isnumeric():
                    if ope == '/' or ope == '%':
                        return u.warn("Can't resolve 'Real " + ope + " Matrice.", "error")
                    if nb2 in matrices.keys():
                        m = matrices[nb2].calc(ope, Real(u.intFloatCast(nb1)))
                        del matrices[nb2]
                elif not nb1.isnumeric() and not nb2.isnumeric():
                    if nb2 in matrices.keys() and nb1 in matrices.keys():
                        m = matrices[nb2].calc(ope, matrices[nb1])
                        del matrices[nb1]
                        del matrices[nb2]
                else:
                    if nb2 in matrices.keys():
                        m = matrices[nb1].calc(ope, Real(u.intFloatCast(nb2)))
                        del matrices[nb1]
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
                    del matrices[nb1]
                    del matrices[nb2]
                elif nb1.isnumeric() and nb2[0:3] == "mat":
                    if ope == '-':
                        return u.warn("Can't resolve 'Real - Matrice.", "error")
                    m = matrices[nb2]
                    matrices["mat" + str(i)] = m.calc('+', Real(u.intFloatCast(nb1)))
                    del matrices[nb2]
                else:
                    m = matrices[nb1]
                    matrices["mat" + str(i)] = m.calc(ope, Real(u.intFloatCast(nb2)))
                    del matrices[nb1]
                exp = exp.replace(string, "mat" + str(i))
                i += 1
        return matrices["mat" + str(i - 1)]


def evalFunction(exp):
    match = re.findall(regex.func, exp)
    if match:
        for m in match:
            fun = m[0]
            param = m[1]
            if fun in data.keys():
                fn = data[fun]
                if param.isnumeric():
                    exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(param)), exp)
                elif param in data.keys():
                    if param.getType() == "real":
                        exp = re.sub(fun + "\(" + param + "\)", str(fn.compute(data[param].value)), exp)
                    else:
                        u.warn("TODO: funX(matrice | complexe | x + 5)", "error")
                else:
                    u.warn("Variable " + param + " is not assigned", "error")
                    return None
    return exp


def evalReals(exp):
    match = re.findall(regex.checkLetter, exp)        # replace X || y by their result
    if match:
        for m in match:
            var = m[0]
            if var in data.keys():
                if data[var].getType() == "real":
                    exp = re.sub(var, str(data[var].str), exp)
    return exp


def evaluate(exp):
    exp = evalFunction(exp)                 # replace funX(y) || funX(5) by their result
    if exp is None:
        return None
    exp = evalReals(exp)                    # replace X || y by their result
    print(exp)
    match = re.match(regex.checkLetter, exp)
    print(match)
    if match:
        return evalMatrice(exp)
    else:
        try:
            res = eval(exp)
            return res
        except ZeroDivisionError:
            u.warn("Division by 0.", "error")
            return None
        except SyntaxError:
            u.warn("Syntax error.", "error")




def parsePut(line):
    lineSplit = line.split('=')
    if len(lineSplit) == 1:
        return u.warn("Syntax : pas de '='", "error")
    key = lineSplit[0].strip()
    exp = lineSplit[1].strip()
    value = ""

    if exp in data.keys():                                            # x = y     => assign x
        value = data[exp]
    else:
        match = re.match(regex.func, key)
        if match:
            value = Function(exp, match.group(2))
            key = match.group(1)[0:4]
        else:
            # print("yo")
            if re.match(regex.checkMatrice, exp):
                mat = Matrice()
                value = Matrice.parse(mat, exp)
                if value is None:
                    return u.warn("Matrice not well formated", "error")
            else:
                newType = u.checkType(exp, data)
                if newType == "real":                                       # x = 3 || x = y + 3 || x = funX(2) etc.
                    value = Real(evaluate(exp))
                elif newType == "matrice":
                    value = evaluate(exp)
                else:
                    u.warn("TODO : gestion des complexes", "error")
    data[key] = value
    data[key].print(None)


def parseGet(get):
    key = get.group(1).strip()
    if key in data.keys():                                                                      # "x = ?"
        data[key].print(None)
    elif re.match(regex.func, key):
        if key[0:4] in data.keys():                                                             # "funX(param) = ?"
            match = re.match(regex.func, key)
            param = match.group(2).strip()
            fn = data[key[0:4]]
            if param.isnumeric():
                u.out(fn.compute(param))
            elif param in data.keys():                                      # "funX(x) = ?"  /!\   gerer funX(x + 5)
                if data[param].getType() == "real":
                    u.out(fn.compute(data[param].value))
                else:
                    u.warn("TODO : fn(complexe | matrice | fn(x + 5)).", "error")
            else:
                u.warn("The variable " + param + " is not assigned.", "error")
        else:
            u.warn("The function " + key[0:4] + " is not defined.", "error")
    elif re.match(regex.checkLetter, key) is None:                                                  # "5 + 5 = ?"
        try:
            res = eval(u.formatLine(get.group(1).strip()))
            u.out(res)
        except SyntaxError:
            u.warn("Bad syntax.", "error")
        except ZeroDivisionError:
            u.warn("Division by zero.", "error")
    else:
        # print("eval")
        res = evaluate(key)
        if res is not None:
            res.print(None)


def main():
    line = ""
    while line is not None:
        try:
            line = u.read_in()
            if line == "":
                u.warn("Empty input.", "error")
            elif line == "env":
                for index, var in enumerate(data):
                    var.print(index)
            elif line == "q" or line == "quit" or line == "exit":
                sys.exit()
            else:
                get = re.match(regex.get, line)
                if get:
                    # print("get")
                    parseGet(get)
                else:
                    # print("put")
                    if re.match(regex.put, line):
                        parsePut(line)
        except KeyboardInterrupt:
            sys.exit()


main()
