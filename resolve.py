import re
from includes.types import Complex, Matrice, Rational
from includes import regex, utils as u


def findBrackets(exp):
    bracket = 0
    first = True
    fun = False

    for index, char in enumerate(exp):
        if char == "(":
            if exp[index - 4:index - 1] == "fun":
                fun = True
            else:
                if first:
                    first = False
                    begin = index + 1
                bracket += 1
        elif char == ")":
            if fun:
                fun = False
            else:
                bracket -= 1
                if bracket == 0 and not first:
                    return exp[begin:index]
    return None


def parse(exp, data, i, tmp):
    match = True

    # handling brackets
    brackets = findBrackets(exp)
    if brackets is not None:
        ret = resolve(brackets, data)
        key = "el" + str(i)
        tmp[key] = ret
        i += 1
        exp = exp.replace("(" + brackets + ")", key, 1)
        # print("brackets new exp = " + exp )

    # print("handling complexes")
    while match:                                # find and replace complexes
        match = re.search(regex.complex, exp)
        if match:
            c = Complex()
            string = match.group(0)
            key = "el" + str(i)
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
            key = "el" + str(i)
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
                    key = "el" + str(i)
                    i += 1
                    ret = resolve(fn.formated.replace('X', match.group(2)), data)
                    exp = exp.replace(obj, key)
                    tmp[key] = ret
                elif match.group(2) in data.keys():
                    param = data[match.group(2)]
                    ret = resolve(fn.formated.replace('X', param.str), data)
                    key = "el" + str(i)
                    i += 1
                    tmp[key] = ret
                    exp = exp.replace(obj, key)
                else:
                    param = resolve(match.group(2), data)
                    if param:
                        ret = resolve(fn.formated.replace('X', param.str), data)
                        key = "el" + str(i)
                        i += 1
                        tmp[key] = ret
                        exp = exp.replace(obj, key)
            else:
                u.warn("The function " + obj[0:4] + " is not assigned.", "NameError")
    # print(exp)

    # print("handling vars")
    match = True
    while match:
        match = re.search("(?:[^a-z]|^)(?!el)([A-Z]+)", exp, flags=re.IGNORECASE)
        if match:
            # print(match)
            obj = match.group(1)
            if obj in data.keys():
                key = "el" + str(i)
                i += 1
                tmp[key] = data[obj]
                exp = re.sub("([^a-z]|^)(?!el)([A-Za-z]+)", r"\1" + key, exp, 1)
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
            key = "el" + str(i)
            var = Rational(u.intFloatCast(match.group(1).replace(" ", "")))
            i += 1
            tmp[key] = var
            exp = re.sub("([+\-*/%]|^)\s*(-\s*\d+(?:\.\d+)?)", r"\1 " + key, exp, 1)
    # print(exp)

    # print("handling +ints")
    match = True
    while match:
        # print(exp)
        match = re.search("(?<!el)\d+(?:\.\d+)?", exp)           # find and replace positive rationals
        if match:
            # print("matched = " + match.group(0))
            key = "el" + str(i)
            var = Rational(u.intFloatCast(match.group(0)))
            i += 1
            tmp[key] = var
            exp = re.sub("(?<!el)\d+(?:\.\d+)?", key, exp, 1)
    # print("END = " + exp)

    return {"exp": exp, "index": i, "tmp": tmp}


def compute(parsed):

    i = parsed["index"]
    exp = parsed["exp"]
    tmp = parsed["tmp"]

    # print("begin " + exp)
    # print("Computing powers")
    match = True
    while match:
        match = re.search("(el\d+)\s*(?:\*\*|\^)\s*(el\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(2)]
            ret = var1.calc('^', var2)
            key = "el" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(el\d+)\s*(?:\*\*|\^)\s*(el\d+)", key, exp, 1)
    # print(exp)


    # print("Computing mult / div / mod")
    match = True
    while match:
        match = re.search("(el\d+)\s*([*/%])\s*(el\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(3)]
            ope = match.group(2)
            ret = var1.calc(ope, var2)
            key = "el" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(el\d+)\s*([*/%])\s*(el\d+)", key, exp, 1)
            # print(exp)

    # print("Computing add / sub")
    match = True
    while match:
        match = re.search("(el\d+)\s*([+-])\s*(el\d+)", exp)
        if match:
            var1 = tmp[match.group(1)]
            var2 = tmp[match.group(3)]
            ope = match.group(2)
            ret = var1.calc(ope, var2)
            key = "el" + str(i)
            i += 1
            tmp[key] = ret
            exp = re.sub("(el\d+)\s*([+-])\s*(el\d+)", key, exp, 1)
    # print(exp)
    if exp.strip() in tmp.keys():
        return tmp[exp.strip()]
    else:
        match = re.match("^-\s*(el\d+)$", exp.strip())
        # print(match)
        if match and match.group(1) in tmp.keys():
            return tmp[match.group(1)].negate()
        elif "i" in exp.strip():
            c = Complex()
            return c.parse(exp.strip())
        else:
            u.warn("Invalid input.", "SyntaxError")


def resolve(exp, data):
    i = 0
    tmp = {}
    # print(exp)
    exp = re.sub("(\d+(?:\.\d+)?)([A-Z]+)", r"\1 * \2", exp, flags=re.IGNORECASE)
    # print(exp)
    if exp.strip() in data.keys():
        return data[exp.strip()]
    # if not re.search("[A-Za-z\[\]]", exp.strip()):
    #     try:
    #         exp = re.sub("(-?\s*\d+(?:\.\d+)?)\s*(?:\*\*|\^)\s*(\d+(?:\.\d+)?)", r"(\1)**\2", exp)
    #         # print("ici?")
    #         var = round(eval(exp), 2)
    #         return Rational(var)
    #     except ZeroDivisionError:
    #         u.warn("Division by 0.", "ComputeError")
    #     except SyntaxError:
    #         u.warn("Invalid input", "SyntaxError")

    parsed = parse(exp, data, i, tmp)
    return compute(parsed)

#
# def main():
#     m = Matrice()
#     data = {"x": Rational(5), "y": Rational(2.5), "z": m.parse("[[5,2];[2,8]]")}
#     exp = "5 *5 + 3i^2"
#     brackets = findBrackets("funX(p - g) + 5-2*(( c - d )/2)")
#     if brackets is not None:
#         print(brackets)
#         # for b in brackets:
#         #     print(b)
#     # print("resolve : " + exp)
#     # resolve(exp, data).print("res")
#
#
# main()
