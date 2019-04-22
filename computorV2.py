import sys
import re
import tests as t
from resolve import resolve
from includes import utils as u, regex, cpv1_computor as cpv1
from includes.customError import CustomError
from includes.types import Function


def parsePut(key, exp, data):
    match = re.match(regex.func, key)
    if match:
        exp = u.checkUnknownVars(exp, match.group(2).strip(), data)
        if exp is not None:
            value = Function(exp, match.group(2))
            key = match.group(1)[0:4]
        else:
            u.warn("Too many unknown variables.", "SyntaxError")
    else:
        value = resolve(exp, data)
    data[key] = value
    data[key].print(None)


def compute(line, data):
    get = re.match(regex.get, line)
    put = re.match(regex.put, line)
    if get:
        key = get.group(1).strip()
        if key == "" or '=' in key:
            u.warn("Invalid input.", "SyntaxError")
        res = resolve(key, data)
        res.print(None)
    elif put:
        exp = put.group(2).strip()
        if exp == "" or '=' in exp or '?' in exp:
            u.warn("Invalid input.", "SyntaxError")
        key = put.group(1).strip()
        if key == "i":
            u.warn("Can't assign the variable i.", "NameError")
        parsePut(key, exp, data)
    else:
        split = line.split('=')
        if len(split) != 2 or len(split[0]) == 0 or len(split[1]) == 0 or "?" in split[1]\
                or not re.search("[Xx]", line) or "fun" in line:
            u.warn("Invalid input.", "SyntaxError")
        cpv1.tryPolynomial(line)


def main():
    data = {}
    if len(sys.argv) > 1 and sys.argv[1] == "-test":
        t.test = True

    line = ""
    while line is not None:
        try:
            line = u.read_in(data)
            compute(line, data)
        except KeyboardInterrupt:
            sys.exit('')
        except CustomError:
            pass


main()
