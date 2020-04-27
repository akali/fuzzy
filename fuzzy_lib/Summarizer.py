from dataclasses import dataclass

from fuzzy_lib.MembershipFunction import MembershipFunction
from fuzzy_lib.Modifier import Modifier


@dataclass
class Summarizer:
    membership_function: MembershipFunction
    modifier: Modifier
    attribute: str

    def name(self):
        return f'{self.modifier.name} {self.membership_function.name} {self.attribute}'

    def __call__(self, x):
        return self.modifier(self.membership_function(x))
