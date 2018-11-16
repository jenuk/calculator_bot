class Rational:
    def __init__(self, a=0, b=1, string=None):
        if string is not None:
            if string[0] == "-":
                sign = -1
                string = string[1:]
            else:
                sign = 1
            if "." in string:
                i = string.index(".")
            else:
                i = 0
            a = sign*int(string.replace(".", ""))
            b = 10**i
        else:
            if b == 0:
                raise ZeroDivisionError("Division by zero")
            elif b < 0:
                a = -1*a
                b = -1*b

        d = gcd(a, b)
        self.a = a//d
        self._b = b//d

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        self._b = b

    def __mul__(self, other):
        if type(other) == int:
            return Rational(self.a * other, self.b)
        elif type(other) == Rational:
            return Rational(self.a * other.a, self.b * other.b)
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

    def __add__(self, other):
        if type(other) == int:
            return Rational(self.a + other*self.b, self.b)
        elif type(other) == Rational:
            return Rational(self.a*other.b + other.a*self.b, self.b * other.b)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    __rmul__ = __mul__
    __radd__ = __add__

    def __truediv__(self, other):
        if type(other) == int:
            return Rational(self.a, self.b * other)
        elif type(other) == Rational:
            return Rational(self.a*other.b, self.b * other.a)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if type(other) == int:
            return Rational(self.b * other, self.a)
        elif type(other) == Rational:
            return Rational(self.b*other.a, self.a * other.b)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -other + self

    def __neg__(self):
        return Rational(-self.a, self.b)

    def __str__(self):
        return long_division(self.a, self.b, precision=3)

    def __repr__(self):
        return "Rational({}, {})".format(self.a, self.b)

    def __format__(self, spec):
        # default values
        fill = " "
        align = ">"
        width = 0
        sign = "-"
        grouping = ""
        alternate = False
        precision = 3
        kind = "f"

        # evaluating the format specifier
        if len(spec) > 1 and spec[1] in "<=>^":
            fill = spec[0]
            align = spec[1]
            spec = spec[2:]

        if len(spec) != 0 and spec[0] in "+- ":
            sign = spec[0]
            spec = spec[1:]

        if len(spec) != 0 and spec[0] == "#":
            alternate = True
            spec = spec[1:]

        if len(spec) != 0 and spec[0] == "0":
            fill = "0"
            align = "="

        if len(spec) != 0 and spec[0].isdigit():
            for k, ch in enumerate(spec):
                if not ch.isdigit():
                    break
            width = int(spec[:k])
            spec = spec[k:]

        if len(spec) != 0 and spec[0] in ",_'":
            grouping = spec[0]
            spec = spec[1:]

        if len(spec) > 1 and spec[0] == ".":
            for k, ch in enumerate(spec[1:]):
                if not ch.isdigit():
                    break
            else:
                k = len(spec)-1
            precision = int(spec[1:k+1])
            spec = spec[k+1:]

        if len(spec) != 0 and spec[0] in "fF":
            kind = spec[0]
            spec = spec[1:]

        if len(spec) > 0:
            raise ValueError("Unknown format code '{}' for object of type 'float'".format(spec[0]))

        # formatting the Rational
        res = long_division(self.a, self.b, precision)
        if alternate and "." not in res:
            res += "."

        if grouping != "":
            pos = res.index(".") if "." in res else len(res)
            for k in range(pos-3, 0, -3):
                res = res[:k] + grouping + res[k:]

        if sign != "-" and res[0] != "-":
            res = sign + res

        if len(res) < width:
            l = width-len(res)
            if align == ">":
                res = fill*l + res
            elif align == "<":
                res = res + fill*l
            elif align == "=":
                if res[0].isdigit():
                    res = fill*l + res
                else:
                    res = res[0] + fill*l + res[1:]
            elif align == "^":
                res = fill*(l//2) + res + fill*(l - l//2)

        return res


def gcd(a, b):
        while b != 0:
            a, b = b, a%b
        return a

def long_division(a, b, precision=2):
    res = "" if a > 0 else "-"
    remainder = abs(a)
    res += str(remainder // b)
    remainder %= b
    if remainder != 0:
        res += "."
    while remainder > 0 and precision > 0:
        remainder *= 10
        res += str(remainder // b)
        remainder %= b
        precision -= 1
    return res
