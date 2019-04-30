import re
from includes import regex, utils as u
import matplotlib.pyplot as plt                 # used for graphical representation of functions
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
        y = eval(self.formated)
        plt.plot(X, y)
        plt.show()


class Rational:

    def __init__(self, value):
        self.value = value
        self.str = str(u.intFloatCast(str(round(value, 3))))
        self.frac = None

    def print(self, index):
        if index is None:
            u.out((index + " = " if index is not None else "") + self.str)
        else:
            print("  " + (index + " = " if index is not None else "") + (self.str if self.frac is None else self.frac))

    def getType(self):
        return "rational"

    def negate(self):
        return Rational(-self.value)

    def calc(self, operation, obj):
        type = obj.getType()

        if operation == '+':
            if type == "rational":
                return Rational(self.value + obj.value)

            if type == "matrice" or type == "complex":
                return obj.calc('+', self)

        elif operation == '-':
            if type == "rational":
                return Rational(self.value - obj.value)

            elif type == "matrice":
                #TODO checker real - matrice
                u.warn("Can't substract a matrice to a rational.", "ComputeError")

            elif type == "complex":
                ret = obj.negate()
                return ret.calc('+', self)

        elif operation == '*':
            if type == "rational":
                return Rational(self.value * obj.value)

            elif type == "matrice" or type == "complex":
                return obj.calc('*', self)

        elif operation == '/':
            frac = None
            if type == "complex":
                u.warn("Can't divide a rational by a " + type + ".", "ComputeError")
            elif type == "matrice":
                ret = copy.deepcopy(obj)
                ret.array = ret.getInverse(ret.array)
                return ret.calc('*', self)
            if obj.value == 0:
                u.warn("Division by 0.", "ComputeError")
            res = str(self.value / obj.value)
            if '.' in res and '.' not in self.str and '.' not in obj.str:
                cd = u.pgcd(self.value, obj.value)
                frac = str(self.value / cd) + "/" + str(obj.value / cd)
            if frac is not None:
                self.frac = frac
            return Rational(self.value / obj.value)

        elif operation == '%':
            #TODO checker rational % matrice | complexe
            if type != "rational":
                u.warn("Can't modulo a rational by a " + type + ".", "ComputeError")
            return Rational(self.value % obj.value)

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a rational to a " + type + ".", "ComputeError")
            return Rational(self.value ** obj.value)


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

    @staticmethod
    def transpose(m, height, width):
        return [[m[row][col] for row in range(0, height)] for col in range(0, width)]

    @staticmethod
    def getMinor(m, i, j):
        return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]

    def getDeterminant(self, m):
        if len(m) == 2:
            return m[0][0] * m[1][1] - m[0][1] * m[1][0]

        determinant = 0
        for c in range(len(m)):
            determinant += ((-1) ** c) * m[0][c] * self.getDeterminant(self.getMinor(0, c))
        return determinant

    def getInverse(self, m):
        determinant = self.getDeterminant(m)
        if determinant == 0:
            u.warn("Can't compute inverse of matrice, determinant is 0.", "ComputeError")
        if len(m) == 2:
            return [[m[1][1] / determinant, -1 * m[0][1] / determinant],
                    [-1 * m[1][0] / determinant, m[0][0] / determinant]]

        cofactors = []
        for r in range(len(m)):
            cofactorRow = []
            for c in range(len(m)):
                minor = self.getMinor(m, r, c)
                cofactorRow.append(((-1) ** (r + c)) * self.getDeterminant(minor))
            cofactors.append(cofactorRow)
        cofactors = self.transpose(cofactors, len(cofactors), len(cofactors[0]))
        for r in range(len(cofactors)):
            for c in range(len(cofactors)):
                cofactors[r][c] /= determinant
        return cofactors

    def calc(self, operation, obj):
        ret = Matrice()
        new = copy.deepcopy(self.array)
        type = obj.getType()

        if operation == "+":
            if type == "rational" or type == "complex":
                u.warn("Can't add a " + type + " to a matrice.", "ComputeError")
            elif type == "matrice":
                if self.height == obj.height and self.width == obj.width:
                    for i in range(len(new)):
                        for j in range(len(new[i])):
                            new[i][j] = new[i][j].calc('+', obj.array[i][j])
                else:
                    u.warn("Can't add matrices of different dimensions.", "ComputeError")

        elif operation == "-":
            if type == "rational" or type == "complex":
                u.warn("Can't substract a " + type + " to a matrice.", "ComputeError")
            elif type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('-', obj)

            elif type == "matrice" or type == "complex":
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
                if obj.width != obj.height:
                    u.warn("Can't compute the inverse of an unsquare matrice", "ComputeError")
                new = copy.deepcopy(obj.array)
                for i in range(obj.height):
                    for j in range(obj.width):
                        new[i][j] = obj.array[i][j].value
                new = self.getInverse(new)
                for i in range(len(new)):
                    for j in range(len(new)):
                        new[i][j] = Rational(new[i][j])
                ret.array = new
                ret.height = obj.height
                ret.width = obj.width
                ret = self.calc('*', ret)
                return ret

        elif operation == "%":
            if type == "rational":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('%', obj)

            else:
                u.warn("Can't modulo a " + type + " by a matrice", "ComputeError")

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
                u.warn("Can't add a matrice to a complex.", "ComputeError")

        elif operation == "-":
            if type == "rational":
                ret.real -= obj.value

            elif type == "complex":
                ret.real -= obj.real
                ret.imaginary -= obj.imaginary
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "matrice":
                u.warn("Can't substract a matrice to a complex.", "ComputeError")

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
                ret.array = ret.getInverse(obj.array)
                for i in range(ret.height):
                    for j in range(ret.width):
                        ret.array[i][j] = self.calc('*', ret.array[i][j])

        elif operation == "%":
            if type == "rational":
                ret.real %= obj.value
                ret.imaginary %= obj.value
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "complex" or type == "matrice":
                u.warn("Can't modulo a complex by a " + type + ".", "ComputeError")

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
