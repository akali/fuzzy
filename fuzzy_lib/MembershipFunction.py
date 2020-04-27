from typing import Callable

import pandas as pd

from fuzzy_lib.Exception import IncorrectBoundException
from fuzzy_lib.Modifier import Modifier, DEFAULT_MODIFIER

_EPS = 1E-9


class MembershipFunction(Callable):
    name: str
    func: Callable
    modifier: Modifier

    def __init__(self, func=None, modifier=None, name=None):
        if func is None:
            func = lambda x: x
        if modifier is None:
            modifier = Modifier('', lambda x: x)
        if name is None:
            name = ''
        self.func = func
        self.modifier = modifier
        self.name = name

    def __call__(self, X):
        def _(x):
            if self.func is None:
                return x
            return self.func(x)

        return self.modifier(_(X))

    def __and__(self, other):
        return MembershipFunction(func=lambda x: min(self(x), other(x)))

    def __or__(self, other):
        return MembershipFunction(func=lambda x: max(self(x), other(x)))

    def includes(self, x):
        return True

    def extract_range(self, alpha_cut, modifier=None) -> (float, float):
        raise Exception('Can\'t extract range for an arbitrary function')


class TriangularMembershipFunction(MembershipFunction):
    a: float
    b: float
    c: float

    def __init__(self, a, b, c, modifier=None):
        super().__init__(modifier=modifier)
        self.a = a
        self.b = b
        self.c = c
        if self.a > self.b or self.b > self.c:
            raise IncorrectBoundException('Expected a <= b <= c')

    def includes(self, x) -> bool:
        return self.a <= x <= self.c

    def __call__(self, X, modifier=None):
        if modifier is None:
            modifier = DEFAULT_MODIFIER

        def _(x):
            if abs(self.b - x) < _EPS:
                return 1
            if self.a < x < self.b:
                return (x - self.a) / float(self.b - self.a)
            if self.b < x < self.c:
                return (self.c - x) / float(self.c - self.b)
            return 0

        return modifier(_(X))

    def extract_range(self, alpha_cut, modifier=None) -> (float, float):
        if modifier is None:
            modifier = DEFAULT_MODIFIER
        return self._extract_left(alpha_cut, modifier), self._extract_right(alpha_cut, modifier)

    def _extract_left(self, alpha_cut, modifier=None):
        if modifier is None:
            modifier = DEFAULT_MODIFIER
        left = self.a
        right = self.b
        for _ in range(100):
            m = (left + right) / 2
            if self(m, modifier) + _EPS <= alpha_cut:
                left = m
            else:
                right = m

        return left

    def _extract_right(self, alpha_cut, modifier=None):
        if modifier is None:
            modifier = DEFAULT_MODIFIER
        left = self.b
        right = self.c
        for _ in range(100):
            m = (left + right) / 2
            if self(m, modifier) + _EPS <= alpha_cut:
                right = m
            else:
                left = m

        return right


class TrapezoidMembershipFunction(MembershipFunction):
    a: float
    b: float
    c: float
    d: float

    left: TriangularMembershipFunction
    right: TriangularMembershipFunction

    def __init__(self, a, b, c, d, modifier=None):
        super().__init__(modifier=modifier)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        if self.a > self.b or self.b > self.c or self.c > self.d:
            raise IncorrectBoundException('Expected a <= b <= c <= d')
        self.left = TriangularMembershipFunction(a=self.a, b=self.b, c=self.b)
        self.right = TriangularMembershipFunction(a=self.c, b=self.c, c=self.d)

    def includes(self, x) -> bool:
        return self.a <= x <= self.d

    def __call__(self, x, modifier=None):
        if modifier is None:
            modifier = DEFAULT_MODIFIER
        if self.b <= x <= self.c:
            return modifier(1)
        if self.left.includes(x):
            return self.left(x, modifier)
        if self.right.includes(x):
            return self.right(x, modifier)
        return modifier(0)

    def extract_range(self, alpha_cut, modifier=None) -> (float, float):
        if modifier is None:
            modifier = DEFAULT_MODIFIER
        l, _ = self.left.extract_range(alpha_cut, modifier)
        _, r = self.right.extract_range(alpha_cut, modifier)
        return l, r
