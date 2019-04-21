import re
import readline

import tests as t
from includes import regex
from includes.customError import CustomError
import sys
import click

history = []

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
    if category == "error":
        output = ("\033[31m[Error]\033[0m " + message)
    else:
        output = "\033[31m[" + category + "]\033[0m " + message
    if t.test:
        t.test_output(output)
    else:
        print(output)
    raise CustomError


def printEnv(data):
    t.i += 1
    print("\n   ENV")
    for index, var in enumerate(data):
        data[var].print(var)
    print('\n')


def printHistory():
    print("\n  HISTORY")
    for input in history:
        print(input)
    print("\n")

def read_in():
    global history
    if t.test:
        line = test()
    else:
        user_input = input("> ")
        line = user_input.strip()
    if line == "q" or line == "quit" or line == "exit":
        sys.exit()
    if line == "":
        warn("Empty input", "SyntaxError")
    else:
        history.append(line)
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
                # exp = exp.replace(key, data[key].str)

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
