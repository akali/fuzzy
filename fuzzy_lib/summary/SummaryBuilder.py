from typing import Dict, Any, Union

import pandas as pd
import numpy as np
from pandas import DataFrame, Series

from fuzzy_lib.Hedge import dict_hedges
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

    def get_summary(self, thresholds: Dict[str, float]) -> Summary:
        numeric_columns = self.df.select_dtypes(include=np.number).columns.tolist()
        category_columns = self.df.select_dtypes(include='category').columns.tolist()

        for column_name in category_columns:
            column = self.df[column_name]

            print(column_name, get_categories(column))

            for category_name in get_categories(column):
                print(column_name, category_name, len(column[column == category_name]))

        for column_name in numeric_columns:
            column = self.df[column_name]

            qs = QuantifierSet(column.min(), column.max())

            def run(membership_function, name):
                l, r = membership_function.extract_range(0.5)
                print(column_name, f'{name}: ', l, r, f'range: {column.min()} {column.max()}')

            for (i, fuzzy_set) in enumerate(self.fuzzy_sets[column_name]):
                very = dict_hedges()["very"]
                run(fuzzy_set, i)

            # run(qs.almost_none(), 'Almost none')
            # run(qs.few(), 'Few')
            # run(qs.many(), 'Many')
            # run(qs.most(), 'Most')
            # run(qs.some(), 'Some')

        return Summary()
