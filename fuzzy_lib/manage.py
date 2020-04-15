#!/bin/python3

import json
import time

from fuzzy_lib import settings
from fuzzy_lib.scripts.load_synonyms_antonyms import get_thesaurus_data


def load_thesaurus():
    words = ["somewhat", "very",
             "extremely",
             "quite",
             "fairly",
             "indeed",
             "highly",
             "slightly",
             "sort_of", "more_or_less", "not"]

    for word in words:
        data = get_thesaurus_data(word)
        dir = f"{settings.BASE_DIR}/{settings.STATIC_DIR}/thesaurus"

        output = open(f"{dir}/{word}.json", "w")
        json.dump(data, output)
        output.close()

        print(f"{word} done")
        time.sleep(1)


def main(args):
    if len(args) > 1 and args[1] == 'thesaurus':
        load_thesaurus()
        return


if __name__ == '__main__':
    import sys

    main(sys.argv)
