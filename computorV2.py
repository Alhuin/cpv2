import sys
import re
import tests as t
from resolve import resolve
from includes import utils as u, regex
from includes.types import Matrice, Rational, Function, Complex

data = {}


def checkUnknownVars(exp, param):
    count = 0
    buff = ""

    match = re.findall(regex.checkLetter, exp)
    for m in match:
        key = m.strip()
        if key not in data.keys():
            if key != "i" and m not in buff:
                buff += m
                count += 1
        elif param != key:
            exp = exp.replace(key, data[key].str)
    if count < 2:
        return exp
    else:
        return None


def parsePut(key, exp):
    match = re.match(regex.func, key)
    if match:
        exp = checkUnknownVars(exp, match.group(2).strip())
        if exp is not None:
            value = Function(exp, match.group(2))
            key = match.group(1)[0:4]
        else:
            u.warn("Too many unknown variables.", "SyntaxError")
    else:
        value = resolve(exp, data)
    data[key] = value
    data[key].print(None)


def compute(line):
    get = re.match(regex.get, line)
    put = re.match(regex.put, line)
    if get:
        key = get.group(1).strip()
        if key == "" or '=' in key:
            u.warn("Invalid input.", "SyntaxError")                            #TODO Custom Error
        res = resolve(key, data)
        res.print(None)
    elif put:
        exp = put.group(2).strip()
        if exp == "" or '=' in exp or '?' in exp:
            u.warn("Invalid input.", "SyntaxError")
        key = put.group(1).strip()
        if key == "i":
            u.warn("Can't assign the variable i.", "NameError")
        parsePut(key, exp)
    else:
        u.warn("Invalid input.", "SyntaxError")


def main():

    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        t.test = True

    line = ""
    while line is not None:
        try:
            line = u.read_in(data)
            if line == "env":
                u.printEnv(data)
                continue
            compute(line)
        except KeyboardInterrupt:
            sys.exit('')
        except Exception:
            pass


main()
