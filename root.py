import rational

class Root:
    def __init__(self, n, radicand):
        if type(radicand) == Root:
            self.n = n * radicand.n
            self.radicand = radicand.radicand
        else:
            self.n = n
            self.radicand = radicand

    def approximate(self, precision):
        pass

    def __mul__(self, other):
        if type(other) == int or type(other) == Rational:
            return Root(self.n, self.radicand * (other**self.n))
        elif type(other) == Root:
            d = gcd(self.n, other.n)
            return Root((self.n * other.n)//d, self.radicand**(other.n//d) * other.radicand**(self.n//d))
        else:
            raise TypeError("unsupported operand type(s) for *: '{}' and '{}'".format(type(self), type(other)))

    __rmul__ = __mul__

    def __truediv__(self, other):
        if type(other) == int or type(other) == Rational:
            return Root(self.n, self.radicand / (other**self.n))
        elif type(other) == Root:
            d = gcd(self.n, other.n)
            return Root((self.n * other.n)//d, self.radicand**(other.n//d) / other.radicand**(self.n//d))
        else:
            raise TypeError("unsupported operand type(s) for /: '{}' and '{}'".format(type(self), type(other)))

    def __rtruediv__(self, other):
        if type(other) == int or type(other) == Rational:
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
        elif type(other) == Rational:
            power = other * Rational(1, self.n)
            return Root(power.b, self.radicand**power.a)
        else:
            raise TypeError("unsupported operand type(s) for **: '{}' and '{}'".format(type(self), type(other)))

    def __repr__(self):
        return "Root({}, {})".format(self.n, repr(self.radicand))