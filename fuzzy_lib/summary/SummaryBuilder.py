from dataclasses import dataclass, field
from typing import Dict, Any, Union, List

import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from fuzzy_lib.Modifier import dict_modifiers
from fuzzy_lib.MembershipFunction import MembershipFunction
from fuzzy_lib.Syntax import FuzzyQuery
from fuzzy_lib.summary.Quantifier import QuantifierSet


# @dataclass
# class Summarizer:
#     pass


class Summary:
    truth: float
    fuzziness: float
    covering: float
    appropriateness: float

    quantifier: MembershipFunction
    summarizer: MembershipFunction


class SummarySet:
    summaries: List[Summary] = field(default=[])

    def add_summary(self, summary):
        self.summaries.append(summary)


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
        current_modifier = []
        yielded_empty = False

        def generate(self, iterations_left):
            if not self.yielded_empty:
                yield []
                self.yielded_empty = True
            if iterations_left == 0:
                yield self.current_modifier
                return
            modifiers = dict_modifiers()

            for modifier in modifiers:
                self.current_modifier.append(modifier)
                yield from self.generate(iterations_left - 1)
                self.current_modifier.pop()
            if len(self.current_modifier) > 0:
                yield self.current_modifier

    def list_summarizers(self, attribute, modifier_size=1):
        for combined_modifier in self.ModifierGenerator().generate(modifier_size):
            modifiers_str = ""
            for modifier in combined_modifier:
                modifiers_str += f'{modifier} '
            modifiers_str = modifiers_str[:-1]

            for membership_function_name in self.fuzzy_sets[attribute].keys():
                return f'{modifiers_str} {membership_function_name} {attribute}'

    def get_summary_attr(self, attribute: str) -> SummarySet:
        """
        Summaries based on some exacty attribute
        :param attribute: column_name
        :return:
        """
        for summarizer in self.list_summarizers(attribute):
            qs = QuantifierSet(0, len(self.df)).dict_quantifiers()

            for quantifier in qs:
                quantifier_mf = qs[quantifier]

                fuzzy_query = FuzzyQuery(summarizer, self.fuzzy_sets)
                matching = fuzzy_query.matching(self.df)
        return SummarySet()

    def get_summary(self, thresholds: Dict[str, Dict[str, MembershipFunction]]) -> SummarySet:

        summary_set = SummarySet()

        numeric_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        category_columns = self.df.select_dtypes(include='category').columns.tolist()
        # Day of the week, Hour of day, day time[Evening, Morning, Afternoon]

        # print(numeric_columns, category_columns)

        for combined_modifier in self.ModifierGenerator().generate(2):
            modifier_str = ""
            for modifier in combined_modifier:
                modifier_str += f'{modifier} '
            modifier_str = modifier_str[:-1]

            for column_name in numeric_columns:
                for membership_function_name in thresholds[column_name].keys():
                    query = f'{modifier_str} {membership_function_name} {column_name}'
                    fuzzy_query = FuzzyQuery(query, thresholds)
                    matching = fuzzy_query.matching(self.df)

                    qs = QuantifierSet(0, len(self.df))
                    for quantifier_name in qs.dict_quantifiers():

                        quantifier = qs.dict_quantifiers()[quantifier_name]

                        l, r = quantifier.extract_range(0.5)  # TODO: get from parameters

                        if l <= len(self.df[matching]) & len(self.df[matching]) <= r:
                            print(f"{quantifier_name} of the records matches query {query}")
                            # summary_set.add_sentence(f"{quantifier_name} of the records matches query {query}")

                    qs = QuantifierSet(0, len(matching))
                    for quantifier_name in qs.dict_quantifiers():

                        quantifier = qs.dict_quantifiers()[quantifier_name]

                        for category_column_name in category_columns:
                            category_column = self.df[category_column_name]
                            for category in get_categories(category_column):
                                query = f'{modifier_str} {membership_function_name} {column_name} are {category}'
                                matching_with_category = matching & (self.df[category_column_name] == category)

                                l, r = quantifier.extract_range(0.5)

                                if l <= len(self.df[matching_with_category]) & len(
                                        self.df[matching_with_category]) <= r:
                                    # summary_set.add_sentence(f"{quantifier_name} of the records with {query}")
                                    print(f"{quantifier_name} of the records with {query}")

        return summary_set
