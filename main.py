from typing import List

import math


class Trapezoid:
    a, b, c, d = 0, 0, 0, 0
    a_val, b_val, c_val, d_val = 0, 0, 0, 0

    def __init__(self, **kwargs):
        self.a = kwargs['a']
        self.b = kwargs['b']
        self.c = kwargs['c']
        self.d = kwargs['d']

        self.a_val = kwargs['a_val']
        self.b_val = kwargs['b_val']
        self.c_val = kwargs['c_val']
        self.d_val = kwargs['d_val']


class BoundsException(Exception):
    def __init__(self):
        super(BoundsException, self).__init__('Bounds exception')


class Vector:
    # x, y
    # x2, y2
    def __init__(self, **kwargs):
        self.x, self.y = kwargs['x2'] - kwargs['x'], kwargs['y2'] - kwargs['y']
        self.sx, self.sy = kwargs['x'], kwargs['y']

    def __len__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def orig(self):
        return {
            'x': self.x + self.sx,
            'y': self.y + self.sy,
        }

    def __mul__(self, other):
        self.x *= other
        self.y *= other
        return self

    def norm(self):
        length = len(self)
        self.x /= length
        self.y /= length

    pass


def calc_value(x, y, x2, y2, value):
    length = x2 - x
    pos = value - x
    coef = 1.0 * pos / length
    return (Vector(x=x, y=y, sx=x2, sy=y2) * coef).orig()['y']


class FuzzySet:
    L: int = 0
    R: int = 0
    default_value = 0

    traps: List[Trapezoid]

    def __init__(self, **kwargs):
        self.L = kwargs['L']
        self.R = kwargs['R']
        self.traps = kwargs['traps']
        self.default_value = kwargs['default_value']

    def test(self, x: int, modifier: None) -> float:
        if self.traps is None:
            return self.default_value
        if self.L > x or self.R < x:
            raise BoundsException()
        if modifier is None:
            modifier = lambda _: _
        for trap in self.traps:
            if trap.a <= x <= trap.b:
                return modifier(calc_value(x=trap.a, y=trap.a_val, x2=trap.b, y2=trap.b_val, value=x))
            if trap.b <= x <= trap.c:
                return modifier(trap.b_val)
            if trap.c <= x <= trap.d:
                return modifier(calc_value(x=trap.c, y=trap.c_val, x2=trap.d, y2=trap.d_val, value=x))
        return self.default_value


class Hedge:
    name: str = ''
    modifier = lambda _: _

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.modifier = kwargs['modifier']

    def apply(self, fs: FuzzySet):
        result = fs.copy()
        result.test = self.modifier(fs.test)
        return result


def main():
    pass


if __name__ == '__main__':
    main()
