import re
import tests as t
from includes import regex


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
    user_input = input("> ")
    return user_input.strip()


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
    line = re.sub("([\+\-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*\^\s*(\d+)\s*(?=[\+\-\%\*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)
    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*([\+\%\*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)
    line = re.sub("\^", "**", line)

    return line
