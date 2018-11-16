class Number:
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
            return Number(self.a * other, self.b)
        elif type(other) == Number:
            return Number(self.a * other.a, self.b * other.b)
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

    def __add__(self, other):
        if type(other) == int:
            return Number(self.a + other*self.b, self.b)
        elif type(other) == Number:
            return Number(self.a*other.b + other.a*self.b, self.b * other.b)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    __rmul__ = __mul__
    __radd__ = __add__

    def __truediv__(self, other):
        if type(other) == int:
            return Number(self.a, self.b * other)
        elif type(other) == Number:
            return Number(self.a*other.b, self.b * other.a)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if type(other) == int:
            return Number(self.b * other, self.a)
        elif type(other) == Number:
            return Number(self.b*other.a, self.a * other.b)
        else:
            raise TypeError("unsupported operand type(s) for +: '{}' and '{}'".format(type(self), type(other)))

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -other + self

    def __neg__(self):
        return Number(-self.a, self.b)

    def __str__(self):
        return long_division(self.a, self.b, precision=3)

    def __repr__(self):
        return "Number({}, {})".format(self.a, self.b)

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
