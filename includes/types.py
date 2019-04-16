import re
from includes import regex, utils as u
import matplotlib.pyplot as plt
import numpy as np
import copy


class Complex:

    def __init__(self):
        self.str = ""
        self.real = 0
        self.imaginary = 0
        self.imgIsNeg = False

    def parse(self, exp):
        match = re.search(regex.complex, exp)
        self.str = exp
        self.real = u.intFloatCast(match.group(1).replace(" ", ""))
        self.imaginary = u.intFloatCast(match.group(2).replace(" ", ""))
        self.imgIsNeg = self.imaginary < 0
        return self

    def print(self, index):
        if index is None:
            u.out(self.str)

    def getType(self):
        return "complex"

    def calc(self, operation, obj):
        ret = copy.deepcopy(self)
        type = obj.getType()
        if operation == "fn":

        if type == "rational":
            if operation == "+":
                ret.real += obj.value
            elif operation == "-":
                ret.real -= obj.value
            elif operation == "*":
                ret.real *= obj.value
                ret.imaginary *= obj.value
            elif operation == "%":
                ret.real %= obj.value
                ret.imaginary %= obj.value

        elif type == "complex":
            if operation == "+":
                ret.real += obj.real
                ret.imaginary += obj.imaginary
            elif operation == "-":
                ret.real -= obj.real
                ret.imaginary -= obj.imaginary
            elif operation == "*":
                old = ret.real
                ret.real = ret.real * obj.real - ret.imaginary * obj.imaginary
                ret.imaginary = old * obj.imaginary + ret.imaginary * obj.real

        elif type == "matrice":
            if operation != '*':
                u.warn("Can't resolve complex " + operation + " matrice", "error")
            else:
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        # print(obj.array[i][j])
                        ret.array[i][j] = self.calc('*', obj.array[i][j])
                        # print(ret.array[i][j].str)

        if ret.getType() == "complex":
            ret.imgIsNeg = ret.imaginary < 0
            ret.str = (str(ret.real) + (" + " if not ret.imgIsNeg else " ") if ret.real != 0 else "") + str(ret.imaginary) + "i"
        return ret


class Rational:

    def __init__(self, value):
        self.value = value
        self.str = str(value)

    def getType(self):
        return "rational"

    def print(self, index):
        u.out((index + " = " if index is not None else "") + self.str)

    def calc(self, operation, obj):
        type = obj.getType()
        if operation == '^':
            if type == "complex" or type == "matrice":
                u.warn("Can't resolve rational ^ " + type + ".", "error")
            return Rational(self.value ** obj.value)
        elif operation == '-':
            if type == "matrice":
                u.warn("Can't substract a matrice to a rational.", "error")
            return Rational(self.value - obj.value)
        elif operation == '*':
            if type == "matrice":
              # print("test")
                return(obj.calc('*', self))
            return Rational(self.value * obj.value)
        elif operation == '/':
            return Rational(self.value / obj.value)
        elif operation == '+':
            if type == "matrice":
              # print("test")
                return(obj.calc('+', self))
            return Rational(self.value + obj.value)
        elif operation == '%':
            return Rational(self.value % obj.value)


class Function:

    def __init__(self, function, param):
        self.function = function
        self.formated = u.formatLine(function)
        self.param = param

    def compute(self, param):
        try:
            # print(param.getType())
            type = param.getType()
            # print(type)
            if type == "rational":
                res = Rational(eval(self.formated.replace('X', param.str)))
            elif type == "matrice":
                return param.calc('fn', self.function)
        except ZeroDivisionError:
            u.warn("Division by 0.", "error")
        return res

    def draw(self, xMin, xMax):
        X = np.array(range(xMin, xMax))
        y = eval(self.function)
        plt.plot(X, y)
        plt.show()

    def getType(self):
        return ("fn")

    def print(self, index):
        u.out((index + " = " if index is not None else "") + self.function)


class Matrice:

    def __init__(self):
        self.array = None
        self.height = 0
        self.width = 0

    def calc(self, operation, obj):
        ret = Matrice()
        new = copy.deepcopy(self.array)
        type = obj.getType()

        if operation == "fn":
            for i in range(len(new)):
                for j in range(len(new[i])):
                    new[i][j] = obj.compute(new[i][j])
        elif type == "rational":
            var = obj.value
            if operation == '^':
                tmp = copy.deepcopy(self)
                for i in range(obj.value - 1):
                    tmp = tmp.calc('*', self)
                new = tmp.array
            else:
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc(operation, obj)
        elif type == "matrice":
            if operation == "^":
                u.warn("Can't elevate a Matrice to a Matrice.", "error")
            elif operation == "/":
                u.warn("Can't devide a Matrice by a Matrice.", "error")
            elif operation == "*":
                if self.width == obj.height:
                    new = []
                    i = j = m = 0
                    while i < self.height or j < self.width:
                        new.append([])
                        j = k = 0
                        while k < obj.width:
                            j = l = 0
                            res = 0
                            while j < self.width:
                                res += obj.array[l][k].calc('*', self.array[i][j]).value
                                j += 1
                                l += 1
                            new[m].append(Rational(res))
                            k += 1
                        m += 1
                        i += 1
                else:
                    u.warn("Can't resolve m1 * m2 : Number of raws in m1 doesn't match number of columns in m2.", "error")
            else:
                m = obj.array
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc(operation, m[i][j])

        else:
            u.warn("complex x matrice", "error")
        ret.array = new.copy()
        ret.height = self.height
        ret.width = self.width
        return ret

    def parse(self, exp):
        width = None
        height = 0
        match = re.findall(regex.parseMatrice, exp)
        matrice = [[] for _ in range(len(match))]
        for m in match:
            elems = m.split(',')
            if width is None:
                width = len(elems)
            elif width != len(elems):
                u.warn("Syntax : Matrice not well formated.", "error")
            for e in elems:
                matrice[height].append(Rational(u.intFloatCast(e)))
            height += 1
        self.height = height
        self.width = width
        self.array = matrice
        return self

    def print(self, index):
        output = ""
        if index is not None:
            u.out(index + " = ")
        for m in self.array:
            first = True
            output += '[ '
            for e in m:
                if not first:
                    output += ", "
                output += e.str
                first = False
            output += ' ]\n  '
        u.out(output)

    def getType(self):
        return("matrice")
