import json
import os
import sys
import time
from os import path
from urllib import request

URL = "https://tuna.thesaurus.com/pageData/{}"


def get_thesaurus_data(word):
    url_word = word
    url_word = url_word.replace('_', '%20')

    url = URL.format(url_word)

    response = request.urlopen(url)
    return json.loads(response.read())


def main(args):
    dir = "thesaurus"

    print(dir)

    if not path.exists(dir):
        os.mkdir(dir)
    else:
        assert path.isdir(dir), f'not dir {dir} already exists'

    for word in args:
        data = get_thesaurus_data(word)
        output = open(f"{dir}/{word}.json", "w")
        json.dump(data, output)
        output.close()

        print(f"{word} done")
        time.sleep(1)


if __name__ == '__main__':
    main(sys.argv[1:])
