import json
import os

base_path = os.path.dirname(__file__)
config_path = os.path.join(base_path, "sanic_config.json")

if os.path.exists(config_path):
    with open(config_path) as handle:
        configs = json.load(handle)
else:
    configs = {}


def get_configs():
    return configs
