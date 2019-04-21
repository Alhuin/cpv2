import re
from includes.types import Complex, Matrice, Rational
from includes import regex, utils as u


def unknowns(exp, data, i, tmp):
    match = True

    # print("handling complexes")
    while match:                                # find and replace complexes
        match = re.search(regex.complex, exp)
        if match:
            c = Complex()
            string = match.group(0)
            key = "var" + str(i)
            i += 1
            exp = exp.replace(string, key, 1)
            tmp[key] = c.parse(string)
    # print(exp)

    # print("handling matrices")
    match = True
    while match:  # find and replace matrices
        match = re.search(regex.checkMatrice, exp)
        if match:
            m = Matrice()
            string = match.group()
            key = "var" + str(i)
            i += 1
            exp = exp.replace(string, key, 1)
            tmp[key] = m.parse(string)
    # print(exp)

    # print("handling  funcs")
    match = True
    while match:                                                # find and replace functions
        match = re.search("(fun[a-z]\(([a-z\d\s+\-/*%^]+)\))", exp, flags=re.IGNORECASE)
        if match:
            obj = match.group(1)
            if obj[0:4] in data.keys():
                fn = data[obj[0:4]]
                param = u.intFloatCast(match.group(2))
                if param:
                    key = "var" + str(i)
                    i += 1
                    ret = resolve(fn.formated.replace('X', match.group(2)), data)
                    exp = exp.replace(obj, key)
                    tmp[key] = ret
                elif match.group(2) in data.keys():
                    param = data[match.group(2)]
                    ret = resolve(fn.formated.replace('X', param.str), data)
                    key = "var" + str(i)
                    i += 1
                    tmp[key] = ret
                    exp = exp.replace(obj, key)
                else:
                    param = resolve(match.group(2), data)
                    if param:
                        ret = resolve(fn.formated.replace('X', param.str), data)
                        key = "var" + str(i)
                        i += 1
                        tmp[key] = ret
                        exp = exp.replace(obj, key)
            else:
                u.warn("The function " + obj[0:4] + " is not assigned.", "NameError")
    # print(exp)

    # print("handling vars")
    match = True
    while match:
        match = re.search("(?:[^a-z]|^)(?!var)([A-Z])", exp, flags=re.IGNORECASE)
        if match:
            # print(match)
            obj = match.group(1)
            if obj in data.keys():
                key = "var" + str(i)
                i += 1
                tmp[key] = data[obj]
                exp = re.sub("([^a-z]|^)(?!var)([A-Za-z])", r"\1" + key, exp, 1)
                # print(exp)
            else:
                u.warn("The variable " + obj + " is not assigned.", "NameError")
    # print(exp)

    # print("handling -ints")
    match = True
    while match:
        # print(exp)
        match = re.search("(?:[+\-*/%]|^)\s*(-\s*\d+(?:\.\d+)?)", exp)           # find and replace negative rationals
        if match:
            # print("matched = " + match.group(0))
            key = "var" + str(i)
            var = Rational(u.intFloatCast(match.group(1).replace(" ", "")))
            i += 1
            tmp[key] = var
            exp = re.sub("([+\-*/%]|^)\s*(-\s*\d+(?:\.\d+)?)", r"\1 " + key, exp, 1)
    # print(exp)

    # print("handling +ints")
    match = True
    while match:
        # print(exp)
        match = re.search("(?<!var)\d+(?:\.\d+)?", exp)           # find and replace positive rationals
        if match:
            # print("matched = " + match.group(0))
            key = "var" + str(i)
            var = Rational(u.intFloatCast(match.group(0)))
            i += 1
            tmp[key] = var
            exp = re.sub("(?<!var)\d+(?:\.\d+)?", key, exp, 1)
    # print("END = " + exp)

    return {"exp": exp, "index": i, "tmp": tmp}


def compute(exp, i, tmp):

    # print("Computing powers")
    match = True
    while match:
        match = re.search("(var\d+)\s*(?:\*\*|\^)\s*(var\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(2)]
            ret = var1.calc('^', var2)
            key = "var" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(var\d+)\s*(?:\*\*|\^)\s*(var\d+)", key, exp, 1)
    # print(exp)


    # print("Computing mult / div / mod")
    match = True
    while match:
        match = re.search("(var\d+)\s*([*/%])\s*(var\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(3)]
            ope = match.group(2)
            ret = var1.calc(ope, var2)
            key = "var" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(var\d+)\s*([*/%])\s*(var\d+)", key, exp, 1)
    # print(exp)

    # print("Computing add / sub")
    match = True
    while match:
        match = re.search("(var\d+)\s*([+-])\s*(var\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(3)]
            ope = match.group(2)
            ret = var1.calc(ope, var2)
            key = "var" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(var\d+)\s*([+-])\s*(var\d+)", key, exp, 1)
    # print(exp)

    if exp.strip() in tmp.keys():
        return tmp[exp.strip()]
    else:
        match = re.match("^-\s*(var\d+)$", exp.strip())
        # print(match)
        if match and match.group(1) in tmp.keys():
            return tmp[match.group(1)].negate()


def resolve(exp, data):
    i = 0
    tmp = {}
    if exp.strip() in data.keys():
        return data[exp.strip()]
    exp = unknowns(exp, data, i, tmp)
    return compute(exp["exp"], exp["index"], exp["tmp"])


# def main():
#     fn = Function("5x^2", "x")
#     m = Matrice()
#     data = {"x": Rational(5), "y": Rational(2.5), "funX": fn, "z": m.parse("[[5,2];[2,8]]")}
#     exp = "5 *5 + 3i^2"
#     print("resolve : " + exp)
#     resolve(exp, data).print("res")
#
#
# main()
