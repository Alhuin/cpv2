import sys
import re
import tests as t
from includes import utils as u, regex
from includes.types import Matrice, Rational, Function, Complex

data = {}


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
                        del matrices[nb2]
                elif not nb1.isnumeric() and not nb2.isnumeric():
                    if nb2 in matrices.keys() and nb1 in matrices.keys():
                        m = matrices[nb2].calc(ope, matrices[nb1])
                        del matrices[nb1]
                        del matrices[nb2]
                else:
                    if nb1 in matrices.keys():
                        m = matrices[nb1].calc(ope, Rational(u.intFloatCast(nb2)))
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
                        u.warn("Can't resolve Rational - Matrice.", "error")           # sûr ? genre   -M+1 != 1-M    ?
                    m = matrices[nb2]
                    matrices["mat" + str(i)] = m.calc('+', Rational(u.intFloatCast(nb1)))
                    del matrices[nb2]
                else:
                    m = matrices[nb1]
                    matrices["mat" + str(i)] = m.calc(ope, Rational(u.intFloatCast(nb2)))
                    del matrices[nb1]
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
                    elif type == "matrice":
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


def evaluate(exp):
    exp = evalFunction(exp)                 # replace funX(y) || funX(5) by their result
    # print(exp)
    if exp is None:
        return None
    exp = evalRationals(exp)                    # replace X || y by their result
    # print(exp)
    match = re.search(regex.checkLetter, exp)
    # print(match)
    if match:
        # print(exp)
        res = evalMatrice(exp)
        return(res)
        # res.print(None)
    else:
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
            # print(u.countUnknownVars(exp))
            if u.countUnknownVars(exp) == 1:
                value = Function(exp, match.group(2))
                key = match.group(1)[0:4]
            else:
                u.warn("Too many unknown variables.", "error")
        else:
            # print("yo")
            if re.match(regex.checkMatrice, exp):
                mat = Matrice()
                value = Matrice.parse(mat, exp)
                if value is None:
                    return u.warn("Matrice not well formated", "error")
            else:
                newType = u.checkType(exp, data)
                if newType == "rational":                                       # x = 3 || x = y + 3 || x = funX(2) etc.
                    value = evaluate(exp) if value is not None else None
                elif newType == "matrice":
                   value = evaluate(exp)
                else:
                    u.warn("TODO : gestion des complexes", "error")
    if value is not None:
        data[key] = value
        data[key].print(None)


def parseGet(key):
    if key in data.keys():                                                                      # "x = ?"
        data[key].print(None)
    elif re.search(regex.checkLetter, key):
        res = evaluate(key)
        res.print(None)
    else:                                                  # "5 + 5 = ?"
        try:
            res = eval(u.formatLine(key))
            u.out(res)
        except ZeroDivisionError:
            u.warn("Division by zero.", "error")
        except SyntaxError:
            u.warn("Syntax error.", "error")


def compute(line):
    get = re.match(regex.get, line)
    put = re.match(regex.put, line)
    if get:
        # print("get")
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
        if exp == "" or '=' in exp:
            u.warn("Syntax error.", "error")
        key = put.group(1).strip()
        parsePut(key, exp)
    else:
        u.warn("Syntax error.", "error")


def test():
    if t.i < len(t.tests):
        if t.tests[t.i]["input"] == "desc":
            print("---------------------------------------------\n  " +
                  t.tests[t.i]["output"]
                  + "\n---------------------------------------------")
            t.i += 1
        t.ret = ("\"" + t.tests[t.i]["input"] + "\"")
        return t.tests[t.i]["input"]
    else:
        exit()


def main():

    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        t.test = True

    line = ""
    while line is not None:
        try:
            if t.test:
                line = test()
            else:
                line = u.read_in()
            if line == "":
                u.warn("Empty input.", "error")
            elif line == "env":
                for index, var in enumerate(data):
                    var.print(index)
            elif line == "q" or line == "quit" or line == "exit":
                sys.exit()
            else:
                try:
                    compute(line)
                except Exception:
                    pass
        except KeyboardInterrupt:
            sys.exit('')


main()
