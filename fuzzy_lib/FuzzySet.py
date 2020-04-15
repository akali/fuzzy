from dataclasses import dataclass, field
from typing import List, Callable

from fuzzy_lib.Exception import IncorrectBoundException
from fuzzy_lib.MembershipFunction import MembershipFunction


@dataclass
class Bounds:
    min: int
    max: int


@dataclass
class FuzzySet(Bounds, Callable):
    mfs: List[MembershipFunction] = field(default_factory=list)

    def add_mf(self, mf: MembershipFunction):
        self.mfs.append(mf)

    def __call__(self, x):
        if min > x or x > max:
            raise IncorrectBoundException('Expected min <= x <= max')
        for mf in self.mfs:
            if mf.includes(x):
                return mf(x)
        return 0

    def extract_ranges(self, alpha_cut) -> List[(int, int)]:
        result: List[(int, int)] = []
        for mf in self.mfs:
            rng = mf.extract_range(alpha_cut)
            result.append(rng)
        return result
