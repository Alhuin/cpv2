import re
import tests as t
from includes import regex
from includes.customError import CustomError
import sys

history = []


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)


def findBrackets(exp):
    """
    Search for the first brackets pair in the expression

    :param
        exp: The expression to search in

    :return
        The matched expression, or None if no brackets where found

    :e.g.
        findBrackets("5 + 2 *(3 + 8 *(5 - c))") = "3 + 8 *(5 - c)"
    """
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


def out(output):
    if t.test:
        t.test_output(output)
    else:
        print("  " + str(output))


def intFloatCast(exp):
    try:
        match = re.match("\s*[-+]?\s*\d+\.(\d+)", exp)
        if match:
            if match.group(1) != '0':
                return float(exp)
            else:
                return int(float(exp))
        elif re.match("\s*[-+]?\s*\d+", exp):
            return int(exp)
        else:
            return None
    except ValueError:
        return None


def warn(message, category):
    global history
    history[len(history) - 1] = "\033[31m" + history[len(history) - 1] + "\033[0m"
    if category == "error":
        output = ("\033[31m[Error]\033[0m " + message)
    else:
        output = "\033[31m[" + category + "]\033[0m " + message
    if t.test:
        t.test_output(output)
    else:
        print(output)
    raise CustomError

def printHelp():
    print("\nThis program is a \033[33mscientific calculator\033[0m. \n")
    print("\033[33mRequirements :\033[0m (brew is needed)")
    print("- Automated installation: `./install.sh`")
    print("- Manual Installation :")
    print("     Install python3 `brew install python3`")
    print("     Replace python3 path in the shebang of computorV2 line 0 : `#![which python3]`")
    print("     Install Numpy (used for graphic rendering of functions) `pip3 install numpy`\n")
    print("\033[32mRules :\033[0m")
    print("- The variable 'i' can't be assigned.")
    print("- Variable name can't contain numbers.\n")
    print("\033[32mHandled types :\033[0m")
    print("- Rationals (including natural integers) :")
    print("\"x = 5\" or \"y = 5/2\"\n")
    print("- Functions with one unknown variable:")
    print("\"funX(a) = 5a + 2\" or \"funA(c) = c * 2 + x (if x is defined)\"\n")
    print("- Matrices :")
    print("\" m = [[1,2];[3,8]]\" or \"n = 8 * [[11,20];[6,9]]\"\n")
    print("- Complexes :")
    print("\"c = 5 + 4i\" or \"d = 12 + 7 - 2i\"\n")
    print("\033[32mGetting a value :\033[0m")
    print("\"c = ?\" or \"funX = ?\"\n")
    print("\033[32mComputing :\033[0m")
    print("- Preset variables and Rationals :")
    print("\"(5 + 8) * 4^2 = ?\" or \"c + 8 = ?\" or \"funX(2) = ?\" or \"funX(c * x) + 2 = ?\"\n")
    print("- Polynomial functions :")
    print("\"x^2 + 2x - 5 = 7\" or \"x + 8 = 3\"\n")
    print("\033[31mForbidden operations :\033[0m")
    print("- Rational [+-] Matrice")
    print("- Rational / Complex")
    print("- Anything % Matrice or Complex")
    print("- Anything ^ Matrice or Complex\n")
    print("\033[32mFeatures :\033[0m")
    print("- \"reset [all|varName]\" : reset the variable value (all of them if 'all' is specified)")
    print("- \"env\" : Print all assigned variables so far")
    print("- \"history\" : Print all inputs so far")
    print("- \"help\" : Print help")
    print("- \"draw funX\" (if funX is defined) : Draw a graphic representation of the function")
    print("- \"q\" or \"quit\" or \"exit\" : Exit program\n")



def printEnv(data):
    t.i += 1
    print("\n       \033[32m[ENV]\033[0m")
    if not data:
        print("No assigned variable.")
    else:
        for index, var in enumerate(data):
            data[var].print(var)
    print('\n')


def printHistory():
    print("\n       \033[32m[HISTORY]\033[0m")
    for input in history:
        print(input)
    print("\n")


def read_in(data):
    global history
    if t.test:
        line = test()
    else:
        user_input = input("> ")
        line = user_input.strip()
    draw = re.match(regex.draw, line)
    if line == "":
        warn("Empty input", "SyntaxError")
    else:
        history.append(line)
    if line == "q" or line == "quit" or line == "exit":
        sys.exit()
    elif draw:
        fn = draw.group(1)
        if fn in data.keys():
            data[fn].draw(-100, 100)
            raise CustomError
        else:
            warn("The function " + fn + " is not assigned.", "NameError")
    elif line == "env":
        printEnv(data)
        raise CustomError
    elif line == "help":
        printHelp()
        raise CustomError
    elif line == "history":
        printHistory()
        raise CustomError
    return line


def checkUnknownVars(exp, param, data):

    match = re.findall(regex.checkLetter, exp)
    for m in match:
        key = m.strip()
        if key != param:
            if key not in data.keys():
                return None
            else:
                exp = re.sub("(\d)" + key, r"\1 * " + key, exp, 1)
                exp = exp.replace(key, data[key].str)

    return exp


def formatLine(line):
    line = re.sub(regex.checkLetter, "X", line)
    line = re.sub("([\-+*%/=])\s*(\d)", r"\1 \2", line, flags=re.IGNORECASE)
    line = re.sub("(\d)\s*([\-+*%/=])", r"\1 \2", line, flags=re.IGNORECASE)
    line = re.sub("([+-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-HJ-Z]\s*\^\s*(\d+)\s*(?=[+\-%*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)
    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-HJ-Z]\s*([+%*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)
    line = re.sub("(\d+)\s*\*?\s*i", r"\1 * i", line, flags=re.IGNORECASE)
    line = re.sub("\^", "**", line)
    return line


