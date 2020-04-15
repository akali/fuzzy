from typing import Callable

from fuzzy_lib.Exception import IncorrectBoundException
from fuzzy_lib.Hedge import Hedge

_EPS = 1E-9


class MembershipFunction(Callable):
    func: Callable
    hedge: Hedge

    def __init__(self, func=None, hedge=None):
        if func is None:
            func = lambda x: x
        if hedge is None:
            hedge = Hedge('', lambda x: x)
        self.func = func
        self.hedge = hedge

    def __call__(self, X):
        def _(x):
            if self.func is None:
                return x
            return self.func(x)

        return self.hedge(_(X))

    def __and__(self, other):
        return MembershipFunction(func=lambda x: min(self(x), other(x)))

    def __or__(self, other):
        return MembershipFunction(func=lambda x: max(self(x), other(x)))

    def includes(self, x):
        return True

    def extract_range(self, alpha_cut) -> (float, float):
        raise Exception('Can\'t extract range for an arbitrary function')

    def set_hedge(self, hedge):
        self.hedge = hedge


class TriangularMembershipFunction(MembershipFunction):
    a: float
    b: float
    c: float

    def __init__(self, a, b, c, hedge=None):
        super().__init__(hedge=hedge)
        self.a = a
        self.b = b
        self.c = c
        if self.a > self.b or self.b > self.c:
            raise IncorrectBoundException('Expected a <= b <= c')

    def includes(self, x) -> bool:
        return self.a <= x <= self.c

    def __call__(self, X):
        def _(x):
            if abs(self.b - x) < _EPS:
                return 1
            if self.a < x < self.b:
                return (x - self.a) / float(self.b - self.a)
            if self.b < x < self.c:
                return (self.c - x) / float(self.c - self.b)
            return 0

        return self.hedge(_(X))

    def extract_range(self, alpha_cut) -> (float, float):
        return self._extract_left(alpha_cut), self._extract_right(alpha_cut)

    def _extract_left(self, alpha_cut):
        left = self.a
        right = self.b
        for _ in range(100):
            m = (left + right) / 2
            if self(m) + _EPS <= alpha_cut:
                left = m
            else:
                right = m

        return left

    def _extract_right(self, alpha_cut):
        left = self.b
        right = self.c
        for _ in range(100):
            m = (left + right) / 2
            if self(m) + _EPS <= alpha_cut:
                right = m
            else:
                left = m

        return right

    def set_hedge(self, hedge):
        if hedge is None:
            hedge = Hedge('', lambda x: x)
        self.hedge = hedge


class TrapezoidMembershipFunction(MembershipFunction):
    a: float
    b: float
    c: float
    d: float

    left: TriangularMembershipFunction
    right: TriangularMembershipFunction

    def __init__(self, a, b, c, d, hedge=None):
        super().__init__(hedge=hedge)
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        if self.a > self.b or self.b > self.c or self.c > self.d:
            raise IncorrectBoundException('Expected a <= b <= c <= d')
        self.left = TriangularMembershipFunction(a=self.a, b=self.b, c=self.b)
        self.right = TriangularMembershipFunction(a=self.c, b=self.c, c=self.d)

    def set_hedge(self, hedge):
        if hedge is None:
            hedge = Hedge('', lambda x: x)
        self.hedge = hedge
        self.left.set_hedge(hedge)
        self.right.set_hedge(hedge)

    def includes(self, x) -> bool:
        return self.a <= x <= self.d

    def __call__(self, x):
        h = self.hedge
        if self.b <= x <= self.c:
            return h(1)
        if self.left.includes(x):
            return self.left(x)
        if self.right.includes(x):
            return self.right(x)
        return h(0)

    def extract_range(self, alpha_cut) -> (float, float):
        l, _ = self.left.extract_range(alpha_cut)
        _, r = self.right.extract_range(alpha_cut)
        return l, r
