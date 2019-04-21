import re
from includes import regex, utils as u
import matplotlib.pyplot as plt
import numpy as np
import copy


class Function:

    def __init__(self, function, param):
        self.function = function
        self.formated = u.formatLine(function)
        self.param = param

    def print(self, index):
        if index is None:
            u.out(self.function)
        else:
            print("  " + index + " = " + self.function)

    def getType(self):
        return "function"

    def draw(self, xMin, xMax):
        X = np.array(range(xMin, xMax))
        y = eval(self.function)
        plt.plot(X, y)
        plt.show()


class Rational:

    def __init__(self, value):
        self.value = value
        self.str = str(value)

    def print(self, index):
        if index is None:
            u.out((index + " = " if index is not None else "") + self.str)
        else:
            print("  " + (index + " = " if index is not None else "") + self.str)

    def getType(self):
        return "rational"

    def negate(self):
        return Rational(-self.value)

    def calc(self, operation, obj):
        type = obj.getType()

        if operation == '+':
            if type == "rational":
                return Rational(round(self.value + obj.value, 2))

            if type == "matrice" or type == "complex":
                return obj.calc('+', self)

        elif operation == '-':
            if type == "rational":
                return Rational(round(self.value - obj.value, 2))

            elif type == "matrice":
                #TODO checker real - matrice
                u.warn("Can't substract a matrice to a rational.", "ComputeError")

            elif type == "complex":
                ret = obj.negate()
                return ret.calc('+', self)

        elif operation == '*':
            if type == "rational":
                return Rational(round(self.value * obj.value, 2))

            elif type == "matrice" or type == "complex":
                return obj.calc('*', self)

        elif operation == '/':
            #TODO checker rational / matrice | complexe
            if type != "rational":
                u.warn("Can't divide a rational by a " + type + ".", "ComputeError")
            if obj.value == 0:
                u.warn("Division by 0.", "ComputeError")
            return Rational(round(self.value / obj.value, 2))

        elif operation == '%':
            #TODO checker rational % matrice | complexe
            if type != "rational":
                u.warn("Can't divide a rational by a " + type + ".", "ComputeError")
            return Rational(round(self.value % obj.value, 2))

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a rational to a " + type + ".", "ComputeError")
            return Rational(round(self.value ** obj.value, 2))


class Matrice:

    def __init__(self):
        self.array = None
        self.height = 0
        self.width = 0
        self.str = ""

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
                u.warn("Matrice not well formated.", "syntaxError")
            for e in elems:
                matrice[height].append(Rational(u.intFloatCast(e)))
            height += 1
        self.height = height
        self.width = width
        self.array = matrice
        self.str = exp
        return self

    def print(self, index):
        output = ""
        if index is not None:
            print("  " + index + " = " + self.str)
        else:
            for m in self.array:
                first = True
                output += '[ '
                for e in m:
                    if not first:
                        output += ", "
                    output += e.str
                    first = False
                output += ' ]\n  '
            else:
                u.out(output)

    def getType(self):
        return "matrice"

    def negate(self):

        ret = copy.deepcopy(self)
        for i in range(ret.height):
            for j in range(ret.width):
                ret.array[i][j] = ret.array[i][j].negate()

    def calc(self, operation, obj):
        ret = Matrice()
        new = copy.deepcopy(self.array)
        type = obj.getType()

        if operation == "+":
            if type == "rational" or type == "complex":
                u.warn("Can't add a rational to a matrice.", "ComputeError")

            elif type == "matrice":
                if self.height == obj.height and self.width == obj.width:
                    for i in range(len(new)):
                        for j in range(len(new[i])):
                            new[i][j] = new[i][j].calc('+', obj.array[i][j])
                else:
                    u.warn("Can't add matrices of different dimensions.", "ComputeError")

        elif operation == "-":
            if type == "rational":
                u.warn("Can't substract a rational to a matrice.", "ComputeError")
            elif type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('-', obj)

            elif type == "matrice":
                if self.height == obj.height and self.width == obj.width:
                    for i in range(len(new)):
                        for j in range(len(new[i])):
                            new[i][j] = new[i][j].calc('-', obj.array[i][j])
                else:
                    u.warn("Can't substract matrices of different dimensions.", "ComputeError")

        elif operation == "*":
            if type == "rational" or type == "complex":
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc('*', obj)

            elif type == "matrice":
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
                    u.warn("Can't resolve m1 * m2 : Number of raws in m1 doesn't match number of columns in m2.",
                           "ComputeError")

        elif operation == "/":
            if type == "rational" or type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('/', obj)

            elif type == "matrice":
                u.warn("Can't divide a matrice by a matrice.", "ComputeError")

        elif operation == "%":
            if type == "rational" or type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('%', obj)

            elif type == "matrice":
                u.warn("Can't modulo a matrice by a matrice", "ComputeError")

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a matrice to a " + type + ".", "ComputeError")
            tmp = copy.deepcopy(self)
            for i in range(obj.value - 1):
                tmp = tmp.calc('*', self)
            new = tmp.array

        ret.array = new.copy()
        ret.height = self.height
        ret.width = self.width
        ret.str = "["
        firstRaw = True
        for i in range(self.height):
            if firstRaw:
                firstRaw = False
            else:
                ret.str += ';'
            ret.str += '['
            first = True
            for j in range(self.width):
                if first:
                    first = False
                else:
                    ret.str += ","
                ret.str += ret.array[i][j].str
            ret.str += ']'
        ret.str += ']'
        return ret


class Complex:

    def __init__(self):
        self.str = ""
        self.real = 0
        self.imaginary = 0
        self.imgIsNeg = False

    def parse(self, exp):
        match = re.search(regex.complex, exp)
        self.real = 0 if match.group(1) is None else u.intFloatCast(match.group(1).replace(" ", ""))
        self.imaginary = u.intFloatCast(match.group(2).replace(" ", ""))
        self.imgIsNeg = self.imaginary < 0
        self.str = (str(self.real) + (
            " + " if not self.imgIsNeg and self.imaginary != 0 else " ") if self.real != 0 else "") + (
                      (str(self.imaginary) + "i") if self.imaginary != 0 else "")

        return self

    def print(self, index):
        if index is None:
            u.out(self.str)
        else:
            print("  " + index + " = " + self.str)

    def getType(self):
        return "complex"

    def negate(self):
        ret = copy.deepcopy(self)
        ret.real = -self.real
        ret.imaginary = -self.imaginary
        ret.imgIsNeg = ret.imaginary < 0
        ret.str = (str(ret.real) + (
            " + " if not ret.imgIsNeg and ret.imaginary != 0 else " ") if ret.real != 0 else "") + (
                      (str(ret.imaginary) + "i") if ret.imaginary != 0 else "")
        return ret

    def calc(self, operation, obj):
        ret = copy.deepcopy(self)
        type = obj.getType()

        if operation == "+":
            if type == "rational":
                ret.real += obj.value

            elif type == "complex":
                ret.real += obj.real
                ret.imaginary += obj.imaginary
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('+', obj.array[i][j])

        elif operation == "-":
            if type == "rational":
                ret.real -= obj.value

            elif type == "complex":
                ret.real -= obj.real
                ret.imaginary -= obj.imaginary
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('-', obj.array[i][j])

        elif operation == "*":
            if type == "rational":
                ret.real *= obj.value
                ret.imaginary *= obj.value
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "complex":
                old = ret.real
                ret.real = ret.real * obj.real - ret.imaginary * obj.imaginary
                ret.imaginary = old * obj.imaginary + ret.imaginary * obj.real

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('*', obj.array[i][j])

        elif operation == "/":
            if type == "rational":
                ret.real = ret.real / obj.value
                ret.imaginary = ret.imaginary / obj.value

            elif type == "complex":
                div = Rational(obj.real**2 + obj.imaginary**2)
                conj = copy.deepcopy(obj)
                conj.imaginary = -conj.imaginary
                ret = self.calc('*', conj)
                ret = ret.calc('/', div)

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('*', obj.array[i][j])

        elif operation == "%":
            if type == "rational":
                ret.real %= obj.value
                ret.imaginary %= obj.value
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "complex":
                # TODO checker complexe % complexe
                u.warn("Can't modulo a complex by a complex.", "todo")

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('%', obj.array[i][j])

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a complex to a " + type + ".", "ComputeError")
            for i in range(obj.value):
                ret = copy.deepcopy(self)
                for i in range(obj.value - 1):
                    ret = ret.calc('*', self)

        if ret.getType() == "complex":
            ret.real = u.intFloatCast(str(ret.real))
            ret.imaginary = u.intFloatCast(str(ret.imaginary))
            ret.imgIsNeg = ret.imaginary < 0
            ret.str = (str(ret.real) + (" + " if not ret.imgIsNeg and ret.imaginary != 0 else " ") if ret.real != 0 else "") + ((str(ret.imaginary) + "i") if ret.imaginary != 0 else "")
        return ret
