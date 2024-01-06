from string import ascii_letters, digits
from itertools import permutations
from random import randint
import json

all_permutations = permutations(ascii_letters + digits, r=2)
all_permutations_list = list(all_permutations)[:100]

data = {}


def get_random_besides(_from, to, besides) -> int:
    while True:
        res = randint(_from, to)
        if res in besides:
            continue

        return res


for i in all_permutations_list:
    answer = randint(0, 500000)
    fa1 = get_random_besides(0, 500000, [answer])
    fa2 = get_random_besides(0, 500000, [answer, fa1])
    fa3 = get_random_besides(0, 500000, [answer, fa1, fa2])

    data[''.join(i)] = {
        'answer': answer,
        'fakes': [fa1, fa2, fa3]
    }

open('questions.json', 'w', encoding='UTF-8').write(json.dumps(data))