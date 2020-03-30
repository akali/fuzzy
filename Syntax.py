import json

import settings
from Hedge import dict_hedges


def get_synonyms(word):
    """
    :param word:
    :return: list of objects containing term and similarity from -100 to 100
    :raises: IOException: when not found, you should load words first
    """
    data_file = f"{settings.BASE_DIR}/{settings.STATIC_DIR}/thesaurus/{word}.json"

    result = []

    with open(data_file) as f:
        thesaurus_data = json.load(f)
        for entry in thesaurus_data["data"]["definitionData"]["definitions"]["synonyms"]:
            result.append({
                'term': entry['term'],
                'similarity': int(entry['similarity']),
            })
        f.close()

    return result


def get_hedges():
    """
    :return: list of hedges(names only)
    """
    return dict_hedges().keys()


def get_hedges_synonyms(limit):
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


def to_sql(fuzzy_query, fields, limit=100):
    """
    TODO: Implement query parse
    Converts fuzzy query to sql query
    :param fields: dict of querying numerical fields: {name, membership_function}
    :param limit: similarity limit for synonyms
    :param fuzzy_query: fuzzy query
    :return: sql query
    :raises: SyntaxException: syntax error
    """

    if fuzzy_query == "":
        raise SyntaxException("Empty query")

    return ""
