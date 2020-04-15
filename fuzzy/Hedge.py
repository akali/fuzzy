import copy
import math
from dataclasses import dataclass
from typing import Callable, List


def default_modifier(x):
    return x


@dataclass
class Hedge:
    name: str = ''
    modifier: Callable = lambda _: _

    def __and__(self, other):
        return Hedge(f"{self.name} and {other.name}", modifier=lambda x: min(self.modifier(x), other.modifier(x)))

    def __or__(self, other):
        return Hedge(f"{self.name} and {other.name}", modifier=lambda x: max(self.modifier(x), other.modifier(x)))

    def __call__(self, other):
        if isinstance(other, Hedge):
            return Hedge(f"{self.name} {other.name}", modifier=lambda x: self.modifier(other.modifier(x)))
        return self.modifier(other)

    def __init__(self, name, modifier: Callable = None):
        self.name = name
        if modifier is None:
            modifier = default_modifier
        self.modifier = modifier


def dict_hedges():
    return dict([(hedge.name, hedge) for hedge in list_hedges()])


def list_hedges():
    x = Hedge("x", modifier=lambda x: x)
    plus = Hedge("plus", modifier=lambda x: math.pow(x, 1.25))
    minus = Hedge("minus", modifier=lambda x: math.pow(x, 0.75))

    not_h = Hedge("not", modifier=lambda x: 1.0 - x)

    more_or_less = Hedge("more-or-less", modifier=lambda x: math.sqrt(x))
    somewhat = Hedge("somewhat", modifier=lambda x: math.sqrt(x))

    very = Hedge("very", modifier=lambda x: x * x)
    extremely = Hedge("extremely", modifier=lambda x: x * x * x)

    quite = Hedge("quite", modifier=lambda x: pow(x, 1.7))
    fairly = Hedge("fairly", modifier=lambda x: math.sqrt(x))

    indeed = Hedge("indeed", modifier=lambda x: 2 * x * x if x <= 0.5 else 1 - 2 * (1 - x) ** 2)

    highly = Hedge("highly", modifier=(plus(very(x))).modifier)
    slightly = Hedge("slightly", modifier=(x and not_h(very)).modifier)
    sort_of = Hedge("sort_of", modifier=(more_or_less and not_h(very)).modifier)

    return [x, very, not_h, more_or_less, extremely, quite, fairly, highly, slightly, sort_of, indeed, somewhat,
            plus, minus]
