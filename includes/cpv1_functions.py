from includes import utils as u
import re


def pgcd(a, b):
    if b == 0:
        return a
    else:
        r = a % b
        return pgcd(b, r)

def strIntFloat(param):
    string = str(param)
    strLen = len(string)
    if strLen > 2 and string[strLen - 2:strLen] == ".0":
        return string[:strLen - 2]
    else:
        return string


#   prints irreducitible fraction if necessary

def printSolution(solution, den, div):
    solution = -solution if solution == -0 or solution == -0.0 else solution
    frac = ""
    res = strIntFloat(solution)
    if res == "-0":
        res = "0"
    if '.' in res and '.' not in strIntFloat(den) and '.' not in strIntFloat(div):
        cd = pgcd(den, div)
        frac = strIntFloat(den / cd) + "/" + strIntFloat(div / cd)
    if frac != "":
        res += "   (" + frac + ")"
    u.out(res)


#   Handles natural input

def formatLine(line):

    # replace 6^2 | 6*2 | 6/2 by the result

    match = True
    while match:
        match = re.search("(?:[+-=]|^)\s*((\d+(?:\.\d+)?)\s*[\^*/]\s*(\d+(?:\.\d+)?))\s*(?=[+-=]|$)", line, flags=re.IGNORECASE)
        if match:
            exp = match.group(1).replace('^', '**')
            res = eval(exp)
            line = line.replace(match.group(1), str(res))
    print(line)

    # replace 6x^2 | 6*x^2  by 6 * X^2

    line = re.sub("([\+\-=]|^)\s*(\d+(?:\.\d+)?)\s*\*?\s*X\s*\^\s*(\d+)\s*(?=[\+\-=]|$)", r"\1 \2 * X^\3 ", line, flags=re.IGNORECASE)

    # replace 6x | 6*x      by 6 * X^1

    line = re.sub("(\d+(?:\.\d+)?)\s*\*?\s*X\s*([\+\-=]|$)", r"\1 * X^1 \2", line, flags=re.IGNORECASE)

    # replace X             by 1 * X^1

    line = re.sub("([\+\-=]|^)\s*X\s*(?=[\+\-=]|$)", r"\1 1 * X^1 ", line, flags=re.IGNORECASE)

    # replace X^5           by 1 * X^5

    line = re.sub("([\+\-=]|^)\s*X\s*\^\s*(\d+)\s*(?=[\+\-=]|$)", r"\1 1 * X^\2 ", line, flags=re.IGNORECASE)

    # replace 6             by 6 * X^0

    line = re.sub("(?<![\^\d])\s*(\d+(?:\.\d+)?)\s*(?=[\+\-=]|$)", r" \1 * X^0 ", line, flags=re.IGNORECASE)

    return line
