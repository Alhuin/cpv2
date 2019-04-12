import sys
import re
from includes import regex
global data


def out(output):
    print("  " + str(output))


def intFloatCast(exp):
    if re.match("\d+\.\d+", exp):
        return float(exp)
    else:
        return int(exp)


def warn(message, category):
    if category == "error":
        print("\033[0;31m[Error]\033[0m " + message)


def read_flags():
    global details
    nbArgs = len(sys.argv)
    if nbArgs > 1 and sys.argv[1] == "-d":
        details = True


def read_in():
    global history
    user_input = input("> ")
    return user_input.strip()


def checkType(str, data):
    if 'i' in str:
        return "complex"
    else:
        match = re.findall(regex.checkLetter, str)
        for m in match :
            if m in data.keys():
                if data[m].getType() == "matrice":
                    # print("mat")
                    return "matrice"
        return "real"


def formatLine(line):
    line = re.sub(regex.checkLetter, "X", line)
    line = re.sub("([\+\-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*\^\s*(\d+)\s*(?=[\+\-\%\*=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)
    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*[A-Z]\s*([\+\%\*\-=]|$)", r"\1 * X \2", line, flags=re.IGNORECASE)
    line = re.sub("\^", "**", line)

    return line
