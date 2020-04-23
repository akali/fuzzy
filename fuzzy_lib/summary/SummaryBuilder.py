from typing import Dict, Any, Union

import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from fuzzy_lib.Hedge import dict_hedges
from fuzzy_lib.MembershipFunction import MembershipFunction
from fuzzy_lib.Syntax import FuzzyQuery
from fuzzy_lib.summary.Quantifier import QuantifierSet


class Summary:
    def __init__(self):
        pass

    def __str__(self):
        pass

    pass


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

    class HedgeGenerator:
        current_hedges = []
        yielded_empty = False

        def generate(self, iterations_left):
            if not self.yielded_empty:
                yield []
                self.yielded_empty = True
            if iterations_left == 0:
                yield self.current_hedges
                return
            hedges = dict_hedges()

            for hedge in hedges:
                self.current_hedges.append(hedge)
                yield from self.generate(iterations_left - 1)
                self.current_hedges.pop()
            if len(self.current_hedges) > 0:
                yield self.current_hedges

    def get_summary(self, thresholds: Dict[str, Dict[str, MembershipFunction]]) -> Summary:
        numeric_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        category_columns = self.df.select_dtypes(include='category').columns.tolist()

        # print(numeric_columns, category_columns)

        for combined_hedge in self.HedgeGenerator().generate(2):
            hedges_str = ""
            for hedge in combined_hedge:
                hedges_str += f'{hedge} '
            hedges_str = hedges_str[:-1]

            for column_name in numeric_columns:
                for membership_function_name in thresholds[column_name].keys():
                    query = f'{hedges_str} {membership_function_name} {column_name}'
                    fuzzy_query = FuzzyQuery(query, thresholds)
                    matching = fuzzy_query.matching(self.df)

                    qs = QuantifierSet(0, len(self.df))
                    for quantifier_name in qs.dict_quantifiers():

                        # TODO: REMOVE
                        if quantifier_name == "almost_none":
                            continue

                        quantifier = qs.dict_quantifiers()[quantifier_name]

                        l, r = quantifier.extract_range(0.5)

                        if l <= len(self.df[matching]) & len(self.df[matching]) <= r:
                            print(f"{quantifier_name} of the records matches query {query}")

                    qs = QuantifierSet(0, len(matching))
                    for quantifier_name in qs.dict_quantifiers():

                        # TODO: REMOVE
                        if quantifier_name == "almost_none":
                            continue
                        quantifier = qs.dict_quantifiers()[quantifier_name]

                        for category_column_name in category_columns:
                            category_column = self.df[category_column_name]
                            for category in get_categories(category_column):
                                query = f'{hedges_str} {membership_function_name} {column_name} are {category}'
                                matching_with_category = matching & (self.df[category_column_name] == category)

                                l, r = quantifier.extract_range(0.5)

                                if l <= len(self.df[matching_with_category]) & len(
                                        self.df[matching_with_category]) <= r:
                                    print(f"{quantifier_name} of the records with {query}")

        return Summary()
