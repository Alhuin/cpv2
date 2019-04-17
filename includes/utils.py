import re
import tests as t
from includes import regex
import sys


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


def countUnknownVars(exp):
    match = re.findall(regex.checkLetter, exp)
    saved = ""
    for m in match:
        if m not in saved:
            saved += m
    return len(saved)


def out(output):
    if t.test:
        t.test_output(output)
    else:
        print("  " + str(output))


def intFloatCast(exp):
    if re.match("\d+\.\d+", exp):
        return float(exp)
    else:
        return int(exp)


def warn(message, category):
    if category == "error":
        output = ("\033[31m[Error]\033[0m " + message)
        if t.test:
            t.test_output(output)
        else:
            print(output)
    raise Exception


def read_in():
    global history
    if t.test:
        line = test()
    else:
        user_input = input("> ")
        line = user_input.strip()
    if line == "q" or line == "quit" or line == "exit":
        sys.exit()
    return line


def checkType(str, data):
    if 'i' in str:
        return "complex"
    else:
        match = re.findall("\W(?!fun[A-Z])([A-Za-z])", str)
        for m in match :
            if m in data.keys():
                if data[m].getType() == "matrice":
                    return "matrice"
        return "rational"


def formatLine(line):
    line = re.sub(regex.checkLetter, "X", line)
    line = re.sub("([\-+*%/=])\s*(\d)", r"\1 \2", line, flags=re.IGNORECASE)
    line = re.sub("(\d)\s*([\-+*%/=])", r"\1 \2", line, flags=re.IGNORECASE)
    line = re.sub("([+-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*\^\s*(\d+)\s*(?=[+\-%*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)
    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*([+%*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)
    line = re.sub("\^", "**", line)

    return line
