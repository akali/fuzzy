from dataclasses import dataclass, field
from typing import Callable

from Exception import IncorrectBoundException


@dataclass
class MembershipFunction(Callable):
    func: Callable

    def __call__(self, x):
        if self.func is None:
            return x
        return self.func(x)

    def __and__(self, other):
        return MembershipFunction(lambda x: min(self(x), other(x)))

    def __or__(self, other):
        return MembershipFunction(lambda x: max(self(x), other(x)))

    def includes(self, x):
        return True


@dataclass
class TriangularMembershipFunction(MembershipFunction):
    a: int
    b: int
    c: int

    def __post_init__(self):
        if self.a > self.b or self.b > self.c:
            raise IncorrectBoundException('Expected a <= b <= c')
        pass

    def includes(self, x) -> bool:
        return self.a <= x <= self.c

    def __call__(self, x):
        if self.b == x:
            return 1
        if self.a < x < self.b:
            return (x - self.a) / float(self.b - self.a)
        if self.b < x < self.c:
            return (self.c - x) / float(self.c - self.b)
        return 0


@dataclass
class TrapezoidMembershipFunction(MembershipFunction):
    a: int
    b: int
    c: int
    d: int

    left: TriangularMembershipFunction
    right: TriangularMembershipFunction

    def __post_init__(self):
        if self.a > self.b or self.b > self.c or self.c > self.d:
            raise IncorrectBoundException('Expected a <= b <= c <= d')
        self.left = TriangularMembershipFunction(a=self.a, b=self.b, c=self.b)
        self.right = TriangularMembershipFunction(a=self.c, b=self.c, c=self.d)

    def includes(self, x) -> bool:
        return self.a <= x <= self.d

    def __call__(self, x):
        if self.b <= x <= self.c:
            return 1
        if self.left.includes(x):
            return self.left(x)
        if self.right.includes(x):
            return self.right(x)
        return 0
