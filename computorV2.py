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
            u.warn("Too many unknown variables.", "error")
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
            u.warn("Syntax error.", "error")
        res = resolve(key, data)
        res.print(None)
        # parseGet(key)
    elif put:
        exp = put.group(2).strip()
        if exp == "" or '=' in exp or '?' in exp:
            u.warn("Syntax error.", "error")
        key = put.group(1).strip()
        if key == "i":
            u.warn("Can't assign the variable i.", "error")
        parsePut(key, exp)
    else:
        u.warn("Syntax error.", "error")


def main():

    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        t.test = True

    line = ""
    while line is not None:
        try:
            line = u.read_in()
            if line == "":
                print("\033[31m[Error]\033[0m Empty input.")
                continue
            elif line == "env":
                t.i += 1
                print("\n   ENV")
                for index, var in enumerate(data):
                    data[var].print(var)
                print('\n')
                continue
            else:
                try:
                    compute(line)
                except Exception:
                    pass
        except KeyboardInterrupt:
            sys.exit('')


main()
