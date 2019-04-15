import re
from includes import regex, utils as u
import matplotlib.pyplot as plt
import numpy as np
import copy


class Complex:

    def __init__(self, value):
        self.str = value
        self.real = 0
        self.imaginary = 0

    def getType(self):
        return "complex"



class Rational:

    def __init__(self, value):
        self.value = value
        self.str = str(value)

    def getType(self):
        return "rational"

    def print(self, index):
        u.out((index + " = " if index is not None else "") + self.str)


class Function:

    def __init__(self, function, param):
        self.function = function
        self.formated = u.formatLine(function)
        self.param = param

    def compute(self, param):
        try:
            res = eval(self.formated.replace('X', str(param)))
        except ZeroDivisionError:
            res = u.warn("Division by 0.", "error")
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
            for i in range(len(new)):
                for j in range(len(new[i])):
                    if operation == "+":
                        new[i][j] += var
                    elif operation == "*":
                        new[i][j] *= var
                    elif operation == "/":
                        new[i][j] /= var
                    elif operation == "-":
                        new[i][j] -= var
                    elif operation == '^':
                        new[i][j] **= var
                    else:
                        new[i][j] %= var
        elif type == "matrice":
            if obj.height == self.height and obj.width == self.width:
                m = obj.array
                for i in range(len(new)):
                    for j in range(len(new[i])):
                            if operation == "+":
                                new[i][j] += m[i][j]
                            elif operation == "*":
                                new[i][j] *= m[i][j]
                            elif operation == "/":
                                new[i][j] /= m[i][j]
                            elif operation == "-":
                                new[i][j] -= m[i][j]
                            else:
                                new[i][j] %= m[i][j]
            else:
                u.warn("Impossible d'effectuer un calcul matriciel avec deux matrices de tailles différentes.", "error")
                return None
        else:
            u.warn("complex or funx ope with matrice", "error")
            return None
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
                return None
            for e in elems:
                matrice[height].append(u.intFloatCast(e))
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
                output += str(e)
                first = False
            output += ' ]\n  '
        u.out(output)

    def getType(self):
        return("matrice")
