from random import randint
import json


def random_exclude(_from, to, exclude_list):
    result = None
    while result in exclude_list or result is None:
        result = randint(_from, to)

    return result


def generate_config():
    r1 = randint(0, 10)
    r2 = r1 + 5

    d = []
    c = []
    while True:
        if len(d) <= 3:
            d.append(random_exclude(1, 16, d))
        elif len(d) == 8:
            break
        elif len(d) > 3:
            d.append(randint(1, 16))

    while True:
        if len(c) <= 2:
            c.append(random_exclude(1, 50, c))
        elif len(c) == 4:
            break
        elif len(c) > 2:
            c.append(randint(1, 50))

    config = json.load(open('config.json', 'r', encoding='UTF-8'))
    config['task']['r'] = [r1, r2]
    config['task']['d'] = d
    config['task']['c'] = c

    with open('config.json', 'w', encoding='UTF-8') as f:
        f.write(json.dumps(config))
