import logging
from pathlib import Path
from typing import Dict, List

import yaml

from app.utils.generic_utils import get_method_from_method_path_string


def get_mapping_config_from_yaml_file(filepath: str) -> Dict:
    path = Path(filepath)

    if path.is_file():
        with open(filepath, 'r') as file:
            return yaml.safe_load(file)
    return {}


def flatten_dict(data, parent_key: str = '', sep: str = '__', expand_list: bool = False):
    items = []
    if isinstance(data, dict):
        for k, v in data.items():
            new_key = parent_key + sep + k if parent_key else k
            if isinstance(v, Dict):
                items.extend(flatten_dict(data=v, parent_key=new_key, sep=sep, expand_list=expand_list).items())
            elif expand_list and (isinstance(v, list) or isinstance(v, tuple)):
                for i in range(0, len(v)):
                    items.extend(flatten_dict(data=v[i], parent_key=new_key + f'[{i}]',
                                              sep=sep, expand_list=expand_list).items())
            else:
                items.append((new_key, v))
    elif expand_list and (isinstance(data, list) or isinstance(data, tuple)):
        for i in range(0, len(data)):
            items.extend(flatten_dict(data=data[i], parent_key=parent_key + f'[{i}]', sep=sep,
                                      expand_list=expand_list).items())
    # elif isinstance(d, str) or isinstance(d, int) or isinstance(d, float):
    else:
        items.append((parent_key, data))
    return dict(items)


def map_obj_to_another_obj(obj: Dict, mapping_config: Dict, expand_list: bool = False) -> Dict:
    flat_d = flatten_dict(data=obj, expand_list=expand_list)
    final_map = {}
    for key, value in mapping_config.items():
        final_map[value] = flat_d.get(key)

    return final_map


def map_obj_list_to_another_list(obj_list: List[Dict], mapping_config: Dict, expand_list: bool = False) -> List:
    final_list = []
    for obj in obj_list:
        final_list.append(map_obj_to_another_obj(obj=obj, mapping_config=mapping_config, expand_list=expand_list))
    return final_list


def post_process_obj(obj: Dict, post_process_mapping_config: Dict) -> Dict:
    for key, method_path in post_process_mapping_config.items():
        if key in obj:
            fn = get_method_from_method_path_string(method_path)
            if fn:
                obj[key] = fn(obj[key])
            else:
                logging.warning(f"Not able to find the method: {method_path}")
    return obj


def post_process_obj_list(obj_list: List[Dict], post_process_mapping_config: Dict) -> List:
    final_list = []
    for obj in obj_list:
        final_list.append(post_process_obj(obj=obj, post_process_mapping_config=post_process_mapping_config))
    return final_list
