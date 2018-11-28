from utilities import gcd
import root

class Rational:
    def __init__(self, a=0, b=1, string=None):
        if string is not None:
            if string[0] == "-":
                sign = -1
                string = string[1:]
            else:
                sign = 1
            if "." in string:
                i = len(string) - string.index(".") - 1
            else:
                i = 0
            a = sign*int(string.replace(".", ""))
            b = 10**i
        else:
            if b < 0:
                a = -1*a
                b = -1*b

        self.a = a
        self._b = b
        self.reduce()

    def reduce(self):
        d = gcd(self.a, self.b)

        self.a = self.a//d
        self.b = self.b//d

    def approximate(self, precision):
        approx = Rational(string=self.as_string(precision))
        factor = 10**precision // approx.b
        approx.a *= factor
        approx.b *= factor

        return approx

    def as_string(self, precision):
        res = "" if self.a > 0 else "-"
        remainder = abs(self.a)
        res += str(remainder // self.b)
        remainder %= self.b
        if remainder != 0:
            res += "."
        while remainder > 0 and precision > 0:
            remainder *= 10
            res += str(remainder // self.b)
            remainder %= self.b
            precision -= 1
        return res

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, b):
        if b == 0:
            raise ZeroDivisionError("Division by zero")
        if b < 0:
            b = -b
            self.a = -self.a
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
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if type(other) == int:
            return Rational(self.b * other, self.a)
        elif type(other) == Rational:
            return Rational(self.b*other.a, self.a * other.b)
        else:
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self), type(other)))

    def __floordiv__(self, other):
        if type(other) == int:
            return self.a // (self.b * other)
        elif type(other) == Rational:
            return (self.a*other.b) // (self.b * other.a)
        else:
            raise TypeError("unsupported operand type(s) for //: '{}' and '{}'".format(type(self), type(other)))

    def __rfloordiv__(self, other):
        if type(other) == int:
            return (self.b * other) // self.a
        elif type(other) == Rational:
            return (self.b*other.a) // (self.a * other.b)
        else:
            raise TypeError("unsupported operand type(s) for //: '{}' and '{}'".format(type(self), type(other)))

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -other + self

    def __pow__(self, other, mod=None):
        if type(other) == int:
            if other >= 0:
                mult = self % mod
            else:
                mult = (1/self) % mod

            res = Rational(1)
            while other > 0:
                if other%2 == 0:
                    mult = (mult * mult) % mod
                    other //= 2
                else:
                    res = (res * mult) % mod
                    other -= 1

            return res
        elif type(other) == Rational:
            if other.b == 1:
                return self**other.a
            else:
                return root.Root(other.b, self**other.a)
        else:
            raise TypeError("unsupported operand type(s) for **: '{}' and '{}'".format(type(self), type(other)))

    def __mod__(self, other):
        if other is None:
            return self
        return (self - ((self//other) * other))

    def __pos__(self):
        return Rational(self.a, self.b)

    def __neg__(self):
        return Rational(-self.a, self.b)

    def __abs__(self):
        if self.a > 0:
            return +self
        else:
            return -self

    def __trunc__(self):
        return self.a // self.b
    __floor__ = __trunc__

    def __ceil__(self):
        if self.b == 1:
            return self.a
        else:
            return (self.a // self.b) + 1

    def __int__(self):
        return self.a // self.b

    def __float__(self):
        return self.a / self.b

    def __complex__(self):
        return complex(self.a/self.b)

    def __eq__(self, other):
        if type(other) == int:
            return self.b == 1 and self.a == other
        elif type(other) == Rational:
            return self.a == other.a and self.b == other.b
        else:
            return False

    def __ne__(self, other):
        if type(other) == int:
            return self.b != 1 or self.a != other
        elif type(other) == Rational:
            return self.a != other.a or self.b != other.b
        else:
            return True

    def __le__(self, other):
        if type(other) == Rational:
            return self.a * other.b <= other.a * self.b
        elif type(other) == int:
            return self.a <= other*self.b
        else:
            return TypeError("Could not compare {} and {}".format(type(self), type(other)))

    def __lt__(self, other):
        if type(other) == Rational:
            return self.a * other.b < other.a * self.b
        elif type(other) == int:
            return self.a < other*self.b
        else:
            return TypeError("Could not compare {} and {}".format(type(self), type(other)))

    def __ge__(self, other):
        if type(other) == Rational:
            return other.a * self.b <= self.a * other.b
        elif type(other) == int:
            return other*self.b <= self.a
        else:
            return TypeError("Could not compare {} and {}".format(type(self), type(other)))

    def __gt__(self, other):
        if type(other) == Rational:
            return other.a * self.b < self.a * other.b
        elif type(other) == int:
            return other*self.b < self.a
        else:
            return TypeError("Could not compare {} and {}".format(type(self), type(other)))

    def __hash__(self):
        if self.b == 1:
            return hash(self.a)
        else:
            return hash((self.a, self._b))

    def __str__(self):
        return self.as_string(precision=3)

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
        res = self.as_string(precision)
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