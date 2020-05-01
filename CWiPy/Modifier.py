import math
from dataclasses import dataclass
from typing import Callable


def default_modifier(x):
    return x


@dataclass
class Modifier:
    name: str = ''
    modifier: Callable = lambda _: _

    def __and__(self, other):
        return Modifier(f"{self.name} and {other.name}", modifier=lambda x: min(self.modifier(x), other.modifier(x)))

    def __or__(self, other):
        return Modifier(f"{self.name} or {other.name}", modifier=lambda x: max(self.modifier(x), other.modifier(x)))

    def __call__(self, other):
        if isinstance(other, Modifier):
            name = f'{self.name} {other.name}'
            if self.name is None or len(self.name) == 0:
                name = f'{other.name}'
            return Modifier(f"{name}", modifier=lambda x: self.modifier(other.modifier(x)))
        return self.modifier(other)

    def __init__(self, name, modifier: Callable = None):
        self.name = name
        if modifier is None:
            modifier = default_modifier
        self.modifier = modifier


def dict_modifiers():
    return dict([(modifier.name, modifier) for modifier in list_modifiers()])


def list_modifiers():
    x = Modifier("x", modifier=lambda x: x)
    plus = Modifier("plus", modifier=lambda x: math.pow(x, 1.25))
    minus = Modifier("minus", modifier=lambda x: math.pow(x, 0.75))

    not_h = Modifier("not", modifier=lambda x: 1.0 - x)

    more_or_less = Modifier("more-or-less", modifier=lambda x: math.sqrt(x))
    somewhat = Modifier("somewhat", modifier=lambda x: math.sqrt(x))

    very = Modifier("very", modifier=lambda x: x * x)
    extremely = Modifier("extremely", modifier=lambda x: x * x * x)

    quite = Modifier("quite", modifier=lambda x: pow(x, 1.7))
    fairly = Modifier("fairly", modifier=lambda x: math.sqrt(x))

    indeed = Modifier("indeed", modifier=lambda x: 2 * x * x if x <= 0.5 else 1 - 2 * (1 - x) ** 2)

    highly = Modifier("highly", modifier=(plus(very(x))).modifier)
    slightly = Modifier("slightly", modifier=(x and not_h(very)).modifier)
    sort_of = Modifier("sort_of", modifier=(more_or_less and not_h(very)).modifier)

    return [very, not_h, more_or_less, extremely, quite, fairly, highly, slightly, sort_of, indeed, somewhat]
