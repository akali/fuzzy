import copy
import math
from dataclasses import dataclass
from typing import Callable, List


def default_modifier_func(x):
    return x


class Modifier:
    name: str
    func: Callable
    parent_modifier: 'Modifier'

    # Lose parent modifier
    def __and__(self, other):
        return Modifier(f"{self.name} and {other.name}", func=lambda x: min(self.func(x), other.modifier(x)))

    # Lose parent modifier
    def __or__(self, other):
        return Modifier(f"{self.name} or {other.name}", func=lambda x: max(self.func(x), other.modifier(x)))

    def __call__(self, other):
        if isinstance(other, Modifier):
            name = f'{self.name} {other.name}'
            if self.name is None or len(self.name) == 0:
                name = f'{other.name}'
            return Modifier(f"{name}", func=other.func, parent_modifier=self)
        if self.parent_modifier is None:
            return self.func(other)
        return self.parent_modifier(self.func(other))

    def __init__(self, name, func: Callable = None, parent_modifier: 'Modifier' = None):
        self.name = name
        if func is None:
            func = default_modifier_func
        self.func = func
        self.parent_modifier = parent_modifier


def dict_modifiers():
    return dict([(modifier.name, modifier) for modifier in list_modifiers()])


def list_modifiers():
    x = Modifier("x", func=lambda x: x)
    plus = Modifier("plus", func=lambda x: math.pow(x, 1.25))
    minus = Modifier("minus", func=lambda x: math.pow(x, 0.75))

    not_h = Modifier("not", func=lambda x: 1.0 - x)

    more_or_less = Modifier("more-or-less", func=lambda x: math.sqrt(x))
    somewhat = Modifier("somewhat", func=lambda x: math.sqrt(x))

    very = Modifier("very", func=lambda x: x * x)
    extremely = Modifier("extremely", func=lambda x: x * x * x)

    quite = Modifier("quite", func=lambda x: pow(x, 1.7))
    fairly = Modifier("fairly", func=lambda x: math.sqrt(x))

    indeed = Modifier("indeed", func=lambda x: 2 * x * x if x <= 0.5 else 1 - 2 * (1 - x) ** 2)

    highly = Modifier("highly", func=(plus(very(x))).func)
    slightly = Modifier("slightly", func=(x and not_h(very)).func)
    sort_of = Modifier("sort_of", func=(more_or_less and not_h(very)).func)

    return [very, not_h, more_or_less, extremely, quite, fairly, highly, slightly, sort_of, indeed, somewhat]


DEFAULT_MODIFIER = Modifier('', func=default_modifier_func)
