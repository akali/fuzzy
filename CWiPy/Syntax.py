import json
from copy import deepcopy

import numpy as np
import pandas as pd

from CWiPy import settings
from CWiPy.MembershipFunction import MembershipFunction
from CWiPy.Modifier import dict_modifiers


def get_synonyms(word):
    """
    :param word:
    :return: list of objects containing term and similarity from -100 to 100
    :raises: IOException: when not found, you should load words first
    """

    word = word.replace('-', '_')

    data_file = \
        f"{settings.BASE_DIR}/{settings.STATIC_DIR}/thesaurus/{word}.json"

    result = []

    with open(data_file) as f:
        thesaurus_data = json.load(f)
        # print(thesaurus_data['data']['definitionData']['definitions'])
        for entry in thesaurus_data["data"]["definitionData"]["definitions"]:
            for synonym in entry["synonyms"]:
                result.append({
                    'term': synonym['term'],
                    'similarity': int(synonym['similarity']),
                })
        f.close()

    return result


def get_modifiers_synonyms(limit=100):
    """
    :param limit: similarity limit
    :return: dict of synonym modifiers: {synonym: modifier}
    """
    result = {}
    for modifier in dict_modifiers().keys():
        for synonym in get_synonyms(modifier):
            if synonym['similarity'] < limit:
                continue
            term = synonym['term']
            if term not in result:
                result[term] = set()
            result[term].add(modifier)
    return result


class SyntaxException(BaseException):
    pass


class FuzzyQuery:
    def __init__(self, fuzzy_query, fields, limit=None, alpha_cut=None,
                 modifiers_included=None, round_values=None):
        """
        Args:
            fuzzy_query: fuzzy query string
            fields: dict of querying numerical fields: {field_name, {membership_function_name: membership_function}}
            limit: similarity limit for synonyms
            alpha_cut: alpha cut applied for range filtering
            modifiers_included: are modifiers included in query
            round_values: round returning query values

        Raises:
            SyntaxException: on syntax error
        """
        if limit is None:
            limit = 100
        if alpha_cut is None:
            alpha_cut = 0.5
        if modifiers_included is None:
            modifiers_included = True
        if round_values is None:
            round_values = False

        self.fuzzy_query = fuzzy_query
        self.fields = fields
        self.limit = limit
        self.alpha_cut = alpha_cut
        self.round_values = round_values
        self.modifiers_included = modifiers_included

    def extract_crisp_parameters(self):
        """
        Converts fuzzy_query to crisp query parameters.
        Fuzzy expression structure:
        [composite modifier] [summarizer] [field] [connector]
        [composite modifier] [summarizer] [field] [connector]
        [composite modifier] [summarizer] [field] [connector] ...
        [composite modifier] [summarizer] [field]

        example fuzzy_query: middle age and very high salary

        [connector] = {and, or, but}

        Returns:
            dict[field, [lower bound, upper bound, connector]]
        """

        EOQ_TOKEN = "~~~END_TOKEN~~~"

        if self.fuzzy_query == "":
            raise SyntaxException("Empty query")

        tokens = list(
            filter(lambda x: len(x) > 0, self.fuzzy_query.split(' ')))

        tokens.append(EOQ_TOKEN)

        modifiers_synonyms = get_modifiers_synonyms(self.limit)
        modifiers = dict_modifiers()

        connectors = ["and", "or", "", "but", EOQ_TOKEN]
        connector_sql = {
            "and": "and",
            "or": "or",
            "but": "and",
            EOQ_TOKEN: "",
        }

        expression = []

        result = []

        for token in tokens:
            if token in connectors:
                token = connector_sql[token]
                if self.modifiers_included and len(expression) < 2:
                    raise SyntaxException(
                        f"Empty or incorrect expression {expression}")
                original_expression = expression
                expression.reverse()
                if expression[0] not in self.fields.keys():
                    raise SyntaxException(
                        f"Unknown field {expression[0]} in expression "
                        f"{original_expression}")
                field = expression.pop(0)

                mf_name = expression[0]

                if mf_name not in self.fields[field].keys():
                    raise SyntaxException(
                        f"Unknown membership function {mf_name} in expression "
                        f"{original_expression}")

                mf: MembershipFunction = deepcopy(self.fields[field][mf_name])
                expression.pop(0)

                while len(expression) > 0:
                    if expression[0] not in modifiers and expression[0] \
                            not in modifiers_synonyms:
                        raise SyntaxException(
                            f"Unknown modifier {expression[0]} in expression "
                            f"{original_expression}")

                    if expression[0] in modifiers.keys():
                        mf.set_modifier(modifiers[expression[0]](mf.modifier))
                    else:
                        mf.set_modifier(
                            modifiers_synonyms[expression[0]][0](mf.modifier))
                    expression.pop(0)

                l, r = mf.extract_range(self.alpha_cut)
                result.append([field, l, r, token])
            else:
                expression.append(token)

        return result

    def to_sql(self):
        """

        Returns:
            Constructed SQL where clause
        """
        crisp_query = ""
        params = self.extract_crisp_parameters()
        for (field, l, r, token) in params:
            if self.round_values:
                l, r = int(l), int(r)
            crisp_query += f" {l} <= {field} and {field} <= {r} {token} "

        return crisp_query

    def matching(self, df: pd.DataFrame) -> pd.Series:
        """
        Args:
            df: Querying pandas dataframe

        Returns:
            Series matching fuzzy query
        """

        params = self.extract_crisp_parameters()
        result_series = pd.Series(np.ones(len(df), dtype=bool))

        connector = ""

        for (field, left, right, next_connector) in params:
            if self.round_values:
                left, right = int(left), int(right)

            matching_series = (left <= df[field]) & (df[field] <= right)

            if connector == "":
                result_series = matching_series
            elif connector == "or":
                result_series = result_series | matching_series
            else:  # and
                result_series = result_series & matching_series

            connector = next_connector

        return result_series
