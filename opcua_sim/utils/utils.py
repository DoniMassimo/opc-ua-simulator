from typing import Dict
import json

def save_structure(server_structure: Dict, save_path: str):
    js_server_structure = json.dumps(server_structure, indent=4)
    with open(save_path, 'w') as server_struct_file:
        server_struct_file.write(js_server_structure)

def load_config(config_file_path) -> Dict:
    config = {}
    with open(config_file_path, 'r') as config_file:
        config = config_file.read()
        config = json.loads(config)
    return config

def get_default_from_type(type_: str):
    if type_ == 'integer' or type_ == 'uinteger':
        return 0
    elif type_ == 'float' or type_ == 'double' or type_ == 'decimal':
        return 0.0
    elif type_ == 'string':
        return ''
    else:
        return None