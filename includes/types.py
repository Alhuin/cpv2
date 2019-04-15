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
            u.out(str(self.real) + (" + " if not self.imgIsNeg else "") + str(self.imaginary) + "i")

    def getType(self):
        return "complex"

    def calc(self, operation, obj):
        ret = copy.deepcopy(self)
        type = obj.getType()
        # if operation == "fn":
        if type == "rational":
            if operation == "+":
                ret.real += obj.value
            elif operation == "-":
                ret.real -= obj.value
            elif operation == "*":
                ret.real *= obj.value
                ret.imaginary *= obj.value
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

        ret.imgIsNeg = ret.imaginary < 0
        return ret


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
                    # print(new[i][j])
                    new[i][j] = obj.compute(new[i][j])
                    # print(new[i][j])
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
                    elif operation == "^":
                        new[i][j] **= var
                    else:
                        new[i][j] %= var
        elif type == "matrice":
            if operation == "^":
                u.warn("Can't resolve Matrice ^ Matrice????", "error")
            elif operation == "*" or operation == "/":
                obj.print(None)
                print(obj.height)
                self.print(None)
                print(self.width)
                if obj.width == self.height:
                    # print("main loop")
                    new = []
                    i = 0
                    j = 0
                    m = 0
                    while i < obj.height or j < obj.width:
                        print("main loop")
                        new.append([])
                        j = 0
                        k = 0
                        while k < self.width:
                            print('second loop')
                            j = 0
                            l = 0
                            res = 0
                            while j < obj.width:
                                print('j = ' + str(j) + ' and self.width = ' + str(self.width))
                                print("ret += obj["+str(l)+"]["+str(k)+"] * self["+str(i)+"]["+str(j)+"]")
                                # print("obj[l][k] = " + str(obj[l][k]))
                                # print("arr[i][j] = " + str(self.array[i][j]))
                                res += self.array[l][k] * obj.array[i][j]
                                j += 1
                                l += 1
                            print(str(res))
                            new[m].append(res)
                            print(new[m])
                            k += 1
                        m += 1
                        i += 1
                else:
                    u.warn("Can't resolve m1 * m2 : Number of raws in m1 doesn't match number of columns in m2", "error")
            else:
                m = obj.array
                for i in range(len(new)):
                    for j in range(len(new[i])):
                            if operation == "+":
                                new[i][j] += m[i][j]
                            elif operation == "-":
                                new[i][j] -= m[i][j]
                            else:
                                new[i][j] %= m[i][j]

        else:
            u.warn("complex x matrice", "error")
        print('HUM')
        ret.array = new.copy()
        print('HUM')
        ret.height = self.height
        print('HUM')
        ret.width = self.width
        print('HUM')
        ret.print(None)
        print('HUM')
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
                u.warn("Syntax error", "error")
            for e in elems:
                matrice[height].append(u.intFloatCast(e))
            height += 1
        print(height)
        print(width)
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
