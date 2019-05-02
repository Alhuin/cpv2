import re
from includes.types import Complex, Matrice, Rational
from includes import regex, utils as u


def parse(exp, data, i, tmp):
    """
    Replace all the elements in the string by a key and stores the object in the dictionary tmp with the same key.

    :param
        exp : the expression to evaluate
        data : the program dictionary, containing all the assigned variables so far
        i : the index to make the key to store elements in the dictionnary (key = "el" + str(i))
        tmp : the temporary dictinnary where we store all the parsed elements

    :order
        - find and evaluate brackets
        - parse Complexes
        - parse Matrices
        - parse Variables
        - parse negative Rationals
        - parse positive Rationals

    :return
        obj{exp, index, tmp}:
            exp : the formated expression
            index : the key index, to be used by compute
            tmp : the tmp dictionary filled with the parsed objects

    :e.g.
        parse("5 - [[1,2];[2,3]] * 5 + 3i")
        return:
            exp = "el0 - el1 * el2"
            index = 3
            tmp = {"el0": Rational(5), "el1": Matrice([[1,2];[2,3]]), "el2": Complex(5 + 3i)}
    """
    match = True

    # handling brackets
    brackets = u.findBrackets(exp)
    if brackets is not None:
        ret = resolve(brackets, data)
        key = "el" + str(i)
        tmp[key] = ret
        i += 1
        exp = re.sub("(\d+(?:\.\d+)?|[A-Za-z])\s*\(" + brackets + "\)", r"\1 * (" + brackets + ")", exp)
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
    """
    Replace the calculations by a key and stores the object in the tmp dictionary with the same key.

    :param:
        obj{exp, index, tmp}
        exp : the parsed expression to evaluate
        index : the index to make the key to store elements in the dictionnary (key = "el" + str(i))
        tmp : the temporary dictinnary where we store all the parsed elements

    :order:
        - evaluate powers
        - evaluate * / %
        - evaluate + -

    :return:
        The last object in exp:
            exp should now contain only one key as "el7" if True, then return the corresponding object from tmp
    """
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
