import json
from copy import deepcopy

from fuzzy_lib import settings
from fuzzy_lib.Hedge import dict_hedges
from fuzzy_lib.MembershipFunction import MembershipFunction


def get_synonyms(word):
    """
    :param word:
    :return: list of objects containing term and similarity from -100 to 100
    :raises: IOException: when not found, you should load words first
    """

    word = word.replace('-', '_')

    data_file = f"{settings.BASE_DIR}/{settings.STATIC_DIR}/thesaurus/{word}.json"

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


def get_hedges():
    """
    :return: list of hedges(names only)
    """
    hedges = set(dict_hedges().keys())
    hedges.remove("x")
    hedges.remove("plus")
    hedges.remove("minus")
    return hedges


def get_hedges_synonyms(limit=100):
    """

    :param limit: similarity limit
    :return: dict of synonym hedges: {synonym: hedge}
    """
    result = {}
    for hedge in get_hedges():
        for synonym in get_synonyms(hedge):
            if synonym['similarity'] < limit:
                continue
            term = synonym['term']
            if term not in result:
                result[term] = set()
            result[term].add(hedge)
    return result


class SyntaxException(BaseException):
    pass


def to_sql(fuzzy_query: str, fields, limit=100, alpha_cut=0.5):
    """
    Converts fuzzy_lib where clause query to sql where clause query.
    Fuzzy expression structure:
    [hedge] [hedge] [hedge] ... [hedge] [membership function] [field] [connector]
    [hedge] [hedge] [hedge] ... [hedge] [membership function] [field] [connector]
    [hedge] [hedge] [hedge] ... [hedge] [membership function] [field] [connector] ...
    [hedge] [hedge] [hedge] ... [hedge] [membership function] [field]

    example fuzzy_query: middle age and very high salary

    [connector] = {and, or, but}

    :param fuzzy_query: fuzzy_lib query
    :param fields: dict of querying numerical fields: {field_name, {membership_function_name: membership_function}}
    :param limit: similarity limit for synonyms
    :param alpha_cut:
    :return: sql query
    :raises: SyntaxException: syntax error
    """

    EOQ_TOKEN = "~~~END_TOKEN~~~"

    if fuzzy_query == "":
        raise SyntaxException("Empty query")

    tokens = fuzzy_query.split(' ')

    tokens.append(EOQ_TOKEN)

    crisp_query = ""

    hedges_synonyms = get_hedges_synonyms(limit)
    hedges = dict_hedges()

    connectors = ["and", "or", "", "but", EOQ_TOKEN]
    connector_sql = {
        "and": "and",
        "or": "or",
        "": "and",
        "but": "and",
        EOQ_TOKEN: "",
    }

    default_mfs = {
        "low": {},
        "middle": {},
        "high": {},
    }

    expression = []

    for token in tokens:
        if token in connectors:
            token = connector_sql[token]
            if len(expression) < 2:
                raise SyntaxException(f"Empty or incorrect expression {expression}")
            original_expression = expression
            expression.reverse()
            if expression[0] not in fields.keys():
                raise SyntaxException(f"Unknown field {expression[0]} in expression {original_expression}")
            field = expression.pop(0)

            mf_name = expression[0]

            if mf_name not in default_mfs.keys() and mf_name not in fields[field].keys():
                raise SyntaxException(f"Unknown membership function {mf_name} in expression {original_expression}")

            if mf_name in fields[field].keys():
                mf: MembershipFunction = deepcopy(fields[field][mf_name])
            else:
                mf: MembershipFunction = deepcopy(default_mfs[field])
            expression.pop(0)

            while len(expression) > 0:
                if expression[0] not in hedges and expression[0] not in hedges_synonyms:
                    raise SyntaxException(f"Unknown hedge {expression[0]} in expression {original_expression}")

                if expression[0] in hedges.keys():
                    mf.set_hedge(hedges[expression[0]](mf.hedge))
                else:
                    mf.set_hedge(hedges_synonyms[expression[0]][0](mf.hedge))
                expression.pop(0)

            l, r = mf.extract_range(alpha_cut)
            crisp_query += f" {l} <= {field} and {field} <= {r} {token} "
        else:
            expression.append(token)

    return crisp_query
