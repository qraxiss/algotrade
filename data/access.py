from json import load, dump

config = "data/config.json"

def get_config()->dict:
    with open(config, 'r') as file:
        return load(file)

def set_config(overwrite_json)->None:
    with open(config, 'w') as file:
        dump(overwrite_json, file)

def get_default():
    with open("data/default.json", 'r') as file:
        return load(file)
