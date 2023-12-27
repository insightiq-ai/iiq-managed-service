from pathlib import Path
from typing import Dict, List

import yaml


def get_mapping_config_from_yaml_file(filepath: str) -> Dict:
    path = Path(filepath)

    if path.is_file():
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
    return {}


def flatten_dict(d, parent_key='', sep='__'):
    items = []
    if isinstance(d, dict):
        for k, v in d.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, Dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list) or isinstance(v, tuple):
                for i in range(0, len(v)):
                    items.extend(flatten_dict(v[i], new_key + f'[{i}]', sep=sep).items())
            else:
                items.append((new_key, v))
    elif isinstance(d, list) or isinstance(d, tuple):
        for i in range(0, len(d)):
            items.extend(flatten_dict(d[i], parent_key + f'[{i}]', sep=sep).items())
    elif isinstance(d, str):
        items.append((parent_key, d))
    return dict(items)


def map_obj_to_another_obj(obj: Dict, mapping_config: Dict) -> Dict:
    flat_d = flatten_dict(obj)
    final_map = {}
    for key, value in mapping_config.items():
        final_map[value] = flat_d.get(key)

    return final_map


def map_obj_list_to_another_list(obj_list: List[Dict], mapping_config: Dict):
    final_list = []
    for obj in obj_list:
        final_list.append(map_obj_to_another_obj(obj, mapping_config))
    return final_list
