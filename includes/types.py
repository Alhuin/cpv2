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
        u.out((index + " = " if index is not None else "") + self.function)

    def getType(self):
        return "function"

    def draw(self, xMin, xMax):
        X = np.array(range(xMin, xMax))
        y = eval(self.function)
        plt.plot(X, y)
        plt.show()

    def compute(self, param):
        try:
            type = param.getType()

            if type == "rational":
                return Rational(eval(self.formated.replace('X', param.str)))

            elif type == "matrice" or type == "complex":
                return param.calc('fn', self)

        except ZeroDivisionError:
            u.warn("Division by 0.", "error")


class Rational:

    def __init__(self, value):
        self.value = value
        self.str = str(value)

    def print(self, index):
        u.out((index + " = " if index is not None else "") + self.str)

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
                u.warn("Can't substract a matrice to a rational.", "error")

            elif type == "complex":
                ret = obj.negate()
                return ret.calc('+', self)

        elif operation == '*':
            if type == "rational":
                return Rational(self.value * obj.value)

            elif type == "matrice" or type == "complex":
                return obj.calc('*', self)

        elif operation == '/':
            #TODO checker rational / matrice | complexe
            if type != "rational":
                u.warn("Can't divide a rational by a " + type + ".", "error")
            return Rational(self.value / obj.value)

        elif operation == '%':
            #TODO checker rational % matrice | complexe
            if type != "rational":
                u.warn("Can't divide a rational by a " + type + ".", "error")
            return Rational(self.value % obj.value)

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a rational to a " + type + ".", "error")
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
                u.warn("Syntax : Matrice not well formated.", "error")
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

        if operation == "fn":
            for i in range(len(new)):
                for j in range(len(new[i])):
                    new[i][j] = obj.compute(new[i][j])

        elif operation == "+":
            if type == "rational" or type == "complex":
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc('+', obj)

            elif type == "matrice":
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc('+', obj.array[i][j])

        elif operation == "-":
            if type == "rational" or type == "complex":
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc('-', obj)

            elif type == "matrice":
                for i in range(len(new)):
                    for j in range(len(new[i])):
                        new[i][j] = new[i][j].calc('-', obj.array[i][j])

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
                           "error")

        elif operation == "/":
            if type == "rational" or type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('/', obj)

            elif type == "matrice":
                #TODO checker divisions de matrices
                u.warn("Can't divide a matrice by a matrice.", "error")

        elif operation == "%":
            if type == "rational" or type == "complex":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('%', obj)

            elif type == "matrice":
                for i in range(self.height):
                    for j in range(self.width):
                        new[i][j] = new[i][j].calc('%', obj.array[i][j])

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a matrice to a " + type + ".", "error")

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
        self.str = exp
        self.real = 0 if match.group(1) is None else u.intFloatCast(match.group(1).replace(" ", ""))
        self.imaginary = u.intFloatCast(match.group(2).replace(" ", ""))
        self.imgIsNeg = self.imaginary < 0
        return self

    def print(self, index):
        if index is None:
            u.out(self.str)

    def getType(self):
        return "complex"

    def negate(self):
        ret = copy.deepcopy(self)
        ret.real = -self.real
        ret.imaginary = -self.imaginary
        ret.imgIsNeg = ret.imaginary < 0
        ret.str = (str(ret.real) + (" + " if not ret.imgIsNeg else " ") if ret.real != 0 else "") + str(ret.imaginary) + "i"
        return ret

    def calc(self, operation, obj):
        ret = copy.deepcopy(self)
        type = obj.getType()
        i = 0

        if operation == "fn":
            datas = {}
            formated = obj.formated
            match = re.search("X\*\*(\d+)", formated)
            if match:
                pow = u.intFloatCast(match.group(1))
                sub = "X"
                for i in range(pow - 1):
                    sub += " * X"
                formated = re.sub("X\*\*\d+", sub, formated)
            while re.search("(?:^| )X(?: |$)", formated):
                key = "com" + str(i)
                i += 1
                formated = formated.replace("X", key, 1)
                datas[key] = self
            match = True
            while match is not None:
                # print(formated)
                match = re.search("(\d+|com\d+)\s*([\*\/\%])\s*(\d+|com\d+)", formated)
                if match:
                  #print(match)
                    string = match.group(0)
                    var1 = match.group(1)
                    ope = match.group(2)
                    var2 = match.group(3)
                    com = 0
                    if var1.isnumeric():
                        var1 = Rational(u.intFloatCast(var1))
                    else:
                        var1 = datas[var1]
                        com += 1
                    if var2.isnumeric():
                        var2 = Rational(u.intFloatCast(var2))
                    else:
                        var2 = datas[var2]
                        com += 1
                    if com > 0:
                        key = "com" + str(i)
                        i += 1
                        datas[key] = var1.calc(ope, var2)
                        formated = formated.replace(string, key, 1)
                      #print(formated)
                    else:
                        # print("in")
                        formated = formated.replace(string, var1.calc(ope, var2).str, 1)
            # print(formated)
            match = True
            while match is not None:
                match = re.match("(\d+|com\d+)\s*([\+\-])\s*(\d+|com\d+)", formated)
                if match:
                    string = match.group(0)
                    var1 = match.group(1)
                    ope = match.group(2)
                    var2 = match.group(3)
                    com = 0
                    if var1.isnumeric():
                        var1 = Rational(u.intFloatCast(var1))
                    else:
                        var1 = datas[var1]
                        com += 1
                    if var2.isnumeric():
                        var2 = Rational(u.intFloatCast(var2))
                    else:
                        var2 = datas[var2]
                        com += 1
                    if com > 0:
                        key = "com" + str(i)
                        i += 1
                        datas[key] = var1.calc(ope, var2)
                        formated = formated.replace(string, key, 1)
                      #print(formated)
                    else:
                        # print("in formated")
                        # print(formated)
                        formated = formated.replace(string, var1.calc(ope, var2).str, 1)
                        # print(formated)
                        # print("out formated")
            # print(formated)
            if formated.strip() in datas.keys():
                return datas[formated.strip()]
            else:
                u.warn("Syntax error.", "error")

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

            elif type == "function":
                u.warn("complexe + fonctions a gerer", "todo")
                # TODO checker si les fonctions sont bien évaluées

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

            elif type == "function":
                # TODO checker si les fonctions sont bien évaluées
                u.warn("complexe - fonctions a gerer", "todo")

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

            elif type == "function":
                u.warn("complexe * fonctions a gerer", "todo")
                # TODO checker si les fonctions sont bien évaluées

        elif operation == "/":
            if type == "rational":
                ret.real /= obj.value
                ret.imaginary /= obj.value
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "complex":
                # TODO checker complexe / complexe
                u.warn("Can't devide a complex by a complex.", "todo")
                # old = ret.real
                # ret.real = ret.real * obj.real - ret.imaginary * obj.imaginary
                # ret.imaginary = old * obj.imaginary + ret.imaginary * obj.real

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('*', obj.array[i][j])

            elif type == "function":
                u.warn("complexe * fonctions a gerer", "todo")
                # TODO checker si les fonctions sont bien évaluées

        elif operation == "%":
            if type == "rational":
                ret.real %= obj.value
                ret.imaginary %= obj.value
                ret.imgIsNeg = ret.imaginary < 0

            elif type == "complex":
                # TODO checker complexe % complexe
                u.warn("Can't modulo a complex by a complex.", "todo")
                # old = ret.real
                # ret.real = ret.real * obj.real - ret.imaginary * obj.imaginary
                # ret.imaginary = old * obj.imaginary + ret.imaginary * obj.real

            elif type == "matrice":
                ret = copy.deepcopy(obj)
                for i in range(obj.height):
                    for j in range(obj.width):
                        ret.array[i][j] = self.calc('%', obj.array[i][j])

            elif type == "function":
                # TODO checker si les fonctions sont bien évaluées
                u.warn("complexe * fonctions a gerer", "todo")

        elif operation == '^':
            if type != "rational":
                u.warn("Can't elevate a complex to a " + type + ".", "error")
            for i in range(obj.value):
                ret *= self.calc('*', self)

        if ret.getType() == "complex":
            ret.imgIsNeg = ret.imaginary < 0
            ret.str = (str(ret.real) + (" + " if not ret.imgIsNeg else " ") if ret.real != 0 else "") + str(ret.imaginary) + "i"
        return ret
