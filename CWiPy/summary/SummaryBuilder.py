from dataclasses import dataclass, field
from functools import reduce
from typing import Dict, Any, Union, List

import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from CWiPy.Modifier import dict_modifiers, Modifier, default_modifier
from CWiPy.MembershipFunction import MembershipFunction
from CWiPy.Syntax import FuzzyQuery
from CWiPy.summary.Quantifier import QuantifierSetOnParams, QuantifierSet


@dataclass
class Summarizer:
    membership_function: MembershipFunction
    modifier: Modifier
    attribute: str

    def name(self):
        return f'{self.modifier.name} {self.membership_function.name} {self.attribute}'

    def __call__(self, x):
        return self.modifier(self.membership_function(x))


class Summary:
    truth: float

    quantifier: MembershipFunction
    summarizer: Summarizer

    def __init__(self, truth, quantifier, summarizer):
        self.truth = truth
        self.quantifier = quantifier
        self.summarizer = summarizer

    def get_statement(self):
        return f'{self.quantifier.name} of the records are {self.summarizer.name()} with truth value = {self.truth}. '


class SummarySet:
    summaries: List[Summary]

    def __init__(self):
        self.summaries = []

    def add_summary(self, summary):
        self.summaries.append(summary)

    def get_statement(self, limit=0):
        if limit == 0:
            limit = len(self.summaries)
        result = ""
        for summary in sorted(self.summaries, key=lambda x: x.truth)[-limit:]:
            result += summary.get_statement() + "\n"
        return result


def get_categories(column):
    return column.cat.categories.tolist()


class SummaryBuilder:
    def __init__(self, df: pd.DataFrame, fuzzy_sets):
        self.df = df
        self.fuzzy_sets = fuzzy_sets

    def set_dataframe(self, df: pd.DataFrame):
        self.df = df

    def set_fuzzy_sets(self, fuzzy_sets):
        self.fuzzy_sets = fuzzy_sets

    class ModifierGenerator:
        current_modifier = Modifier('')
        yielded_empty = False

        def generate(self, iterations_left):
            if not self.yielded_empty:
                yield self.current_modifier
                self.yielded_empty = True
            if iterations_left == 0:
                yield self.current_modifier
                return
            modifiers = dict_modifiers()

            for modifier_name in modifiers:
                modifier = modifiers[modifier_name]
                tmp = self.current_modifier
                self.current_modifier = self.current_modifier(modifier)
                yield from self.generate(iterations_left - 1)
                self.current_modifier = tmp
            if self.current_modifier.modifier != default_modifier:
                yield self.current_modifier

    def list_summarizers(self, attribute, modifier_size=1):
        for combined_modifier in self.ModifierGenerator().generate(modifier_size):
            for membership_function_name in self.fuzzy_sets[attribute].keys():
                summarizer = Summarizer(self.fuzzy_sets[attribute][membership_function_name], combined_modifier,
                                        attribute)

                yield summarizer

    def get_summary_attr(self, attributes: List[str]) -> SummarySet:
        """
        Summaries based on some exactly attribute
        :param attributes: column_names
        :return: SummarySet
        """
        summary_set = SummarySet()

        for attribute in attributes:
            for summarizer in self.list_summarizers(attribute):
                qs = QuantifierSet.dict_quantifiers()

                for quantifier in qs:
                    quantifier_mf = qs[quantifier]

                    truth = quantifier_mf(self.df[attribute].map(lambda x: summarizer(x)).sum() * 1.0 / len(self.df))
                    summary = Summary(truth, quantifier_mf, summarizer)

                    summary_set.add_summary(summary)
                    # print(summary.get_statement())

        return summary_set
