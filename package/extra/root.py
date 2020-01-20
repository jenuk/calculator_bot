from . import rational
from .utilities import gcd

class Root:
    def __init__(self, n, radicand):
        if type(n) != int:
            raise TypeError("unsupported type '{}' for root".format(type(n)))
        if type(radicand) == Root:
            self.n = n * radicand.n
            self.radicand = radicand.radicand
        else:
            self.n = n
            self.radicand = radicand

    def approximate(self, precision):
        if type(self.radicand) == int:
            initial = rational.Rational(self.radicand, 1)
            initial.a *= 10**(self.n*precision)
            initial.b *= 10**(self.n*precision)
        else:
            initial = self.radicand.approximate(precision*self.n)

        upper, lower = 10**(len(str(initial.a))), 0
        while upper - lower > 1:
            curr = (upper+lower)//2
            pot = curr**self.n
            if pot == initial.a:
                upper, lower = curr, curr
            elif pot > initial.a:
                upper = curr
            else:
                lower = curr

        res = rational.Rational(lower, 10**precision)

        return res

    def __mul__(self, other):
        if type(other) == int or type(other) == rational.Rational:
            return Root(self.n, self.radicand * (other**self.n))
        elif type(other) == Root:
            d = gcd(self.n, other.n)
            return Root((self.n * other.n)//d, self.radicand**(other.n//d) * other.radicand**(self.n//d))
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if type(other) == int or type(other) == rational.Rational:
            return Root(self.n, self.radicand / (other**self.n))
        elif type(other) == Root:
            d = gcd(self.n, other.n)
            return Root((self.n * other.n)//d, self.radicand**(other.n//d) / other.radicand**(self.n//d))
        else:
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if type(other) == int or type(other) == rational.Rational:
            return Root(self.n, (other**self.n) / self.radicand)
        elif type(other) == Root:
            d = gcd(self.n, other.n)
            return Root((self.n * other.n)//d,  other.radicand**(self.n//d) / self.radicand**(other.n//d))
        else:
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self), type(other)))

    def __pow__(self, other):
        if type(other) == int:
            d = gcd(self.n, other)
            return Root(self.n // d, self.radicand**(other // d))
        elif type(other) == rational.Rational:
            power = other * Rational(1, self.n)
            return Root(power.b, self.radicand**power.a)
        else:
            raise TypeError("unsupported operand type(s) for **: '{}' and '{}'".format(type(self), type(other)))

    def __str__(self):
        return str(self.approximate(3))

    def __repr__(self):
        return "Root({}, {})".format(self.n, repr(self.radicand))

    def __format__(self, spec):
        if "." not in spec:
            return self.approximate(3).__format__(spec)

        i = spec.index(".")
        for k in range(i+1, len(spec)):
            if not spec[k].isdigit():
                break
        else:
            k = len(spec)

        prec = int(spec[i+1:k])
        return self.approximate(prec).__format__(spec)