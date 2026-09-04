"""Custom complex numbers, with some more support than the native complex type, especially for swapping between
representations, i.e. between cartesian? and polar"""
import math
from typing import Union, Tuple, Any


class C:
    real: float
    imaginary: float

    @staticmethod
    def __to_c(x: Union["C", tuple, int, float, "C._Polar"]) -> "C":
        if x.__class__ == C:
            return x
        elif x.__class__ == tuple:
            if len(x) > 2:
                raise ValueError("Too many values to unpack")

            return C(*x[:2])
        elif x.__class__ in (int, float):
            return C(x)
        elif x.__class__ == C._Polar:
            raise NotImplementedError()
        else:
            raise ValueError(f"Cannot convert {x} of type {x.__class__} to a complex number")

    def __init__(self, real=0.0, imaginary=0.0):
        self.real = float(real)
        self.imaginary = float(imaginary)

    def compute_func(self, other: Any, func):
        return func(self, C.__to_c(other))

    @staticmethod
    def __add(a: "C", b: "C") -> Tuple[float, float]:
        return a.real + b.real, a.imaginary + b.imaginary

    def __add__(self, other) -> "C":
        return C(*self.compute_func(other, C.__add))

    def __iadd__(self, other):
        self.real, self.imaginary = self.compute_func(other, C.__add)

    @staticmethod
    def __sub(a: "C", b: "C") -> Tuple[float, float]:
        return a.real - b.real, a.imaginary - b.imaginary

    def __sub__(self, other) -> "C":
        return C(*self.compute_func(other, C.__sub))

    def __isub__(self, other):
        self.real, self.imaginary = self.compute_func(other, C.__sub)

    @staticmethod
    def __mul(a: "C", b: "C") -> Tuple[float, float]:
        return a.real * b.real - a.imaginary * b.imaginary, \
               a.real * b.imaginary + b.real * a.imaginary

    def __mul__(self, other) -> "C":
        return C(*self.compute_func(other, C.__mul))

    def __imul__(self, other):
        self.real, self.imaginary = self.compute_func(other, C.__mul)

    @staticmethod
    def __truediv(a: "C", b: "C") -> Tuple[float, float]:
        """a / b"""
        # This calculates (a / b) * (c / c) where c = b.conjugate()
        # We are allowed to expand the function like this because c / c = 1 and multiplying by 1 is fine
        # This can be rewritten as (a * c) / (b * c), which can then be calculated
        # The trick is that b * b.conjugated() is the same as |b|
        x: "C" = a * b.conjugate()
        y: float = len(b)
        return x.real / y, x.imaginary / y

    def __truediv__(self, other) -> "C":
        return C(*self.compute_func(other, C.__truediv))

    def __itruediv__(self, other):
        self.real, self.imaginary = self.compute_func(other, C.__truediv)

    def conjugate(self) -> "C":
        """Returns a new instance without altering this one"""
        return C(self.real, -self.imaginary)

    def __invert__(self) -> "C":
        """Same as conjugate, but alters and returns this instance"""
        self.imaginary = -self.imaginary
        return self

    def __len__(self) -> float:
        """|b|"""
        return self.real ** 2 + self.imaginary ** 2

    def __repr__(self) -> str:
        return "(%g %c %gi)" % (self.real, '+' if self.imaginary >= 0 else '-', self.imaginary)

    def __to_polar(self):
        return C._Polar(self)

    class _Polar:
        """Complex number in representation r * cos(phi) + r * i * sin(phi) = r * (cos(phi) + i * sin(phi))"""
        r: float
        phi: float

        def __init__(self, c: Union["C", Tuple[float, float]]):
            if c.__class__ == C:
                self.r = len(c)
                self.phi = (c.imaginary >= 0) * math.acos(c.real / self.r)
            else:
                # c is a tuple
                self.r, self.phi = c

        def __repr__(self) -> str:
            return "(%g, %g pi)" % (self.r, self.phi / math.pi)

        def __pow__(self, power: Union[float, int], modulo=None) -> "C._Polar":
            if modulo:
                raise ValueError("Can't mod a complex number")

            return C._Polar((self.r ** power, self.phi * power))

        def __ipow__(self, power: Union[float, int]):
            self.r **= power
            phi = self.phi * power
            if phi >= 0:
                self.phi = phi % (2 * math.pi)
            else:
                phi = "TODO"  # TODO
            self.phi *= power

