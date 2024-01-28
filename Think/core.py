import json
from generate_config import generate_config

config = json.load(open('config.json', 'r', encoding='UTF-8'))
if not config['task']['r']:
    generate_config()
    config = json.load(open('config.json', 'r', encoding='UTF-8'))

flag_config = config['flag']
