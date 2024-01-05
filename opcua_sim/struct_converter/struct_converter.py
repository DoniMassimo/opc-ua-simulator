from typing import Dict, List
from utils import global_const as gc
from utils import utils as utils
import os
from pprint import pprint


def get_entry_sub_struct(struct: Dict, entry_index: str) -> Dict:
    entry_structs: List[Dict] = []
    def recursive_get_entry_struct(rel_structr: Dict):
        for key in rel_structr.keys():
            if str(key) == entry_index:
                entry_structs.append(rel_structr)
                return True
            else:
                res = recursive_get_entry_struct(rel_structr[key][gc.Struct.CHILDREN])
                if res == True:
                    return res
    recursive_get_entry_struct(struct[list(struct.keys())[0]])
    return entry_structs

def get_ignition_data_type(type_: str) -> str:
    if type_ == 'integer' or type_ == 'uinteger':
        return 'int'
    elif type_ == 'float' or type_ == 'double' or type_ == 'decimal':
        return 'Float4'
    elif type_ == 'string':
        return 'String'
    else:
        return None

def convert(struct: Dict, opc_server: str) -> Dict:
    def recursive_conversion(rel_struct: Dict):
        data = []
        for key in rel_struct.keys():
            rel_conversion = {gc.Ignition.NAME:rel_struct[key][gc.Struct.BROWSE_NAME]}
            if rel_struct[key][gc.Struct.CHILDREN]:
                rel_conversion[gc.Ignition.TAG_TYPE] = 'Folder'
                rel_conversion[gc.Ignition.TAGS] = []
                rel_conversion[gc.Ignition.TAGS] = recursive_conversion(rel_struct[key][gc.Struct.CHILDREN])
            else:
                rel_conversion[gc.Ignition.VALUE_SOURCE] = 'opc'
                rel_conversion[gc.Ignition.OPC_ITEM_PATH] = rel_struct[key][gc.Struct.NODE_ID]                
                type_ = get_ignition_data_type(rel_struct[key][gc.Struct.DATA_TYPE])
                rel_conversion[gc.Ignition.DATA_TYPE] = type_
                rel_conversion[gc.Ignition.TAG_GROUP] = 'Erogatore_5'
                rel_conversion[gc.Ignition.OPC_SERVER] = 'Erogatore_5'
                rel_conversion[gc.Ignition.TAG_TYPE] = 'AtomicTag'
            data.append(rel_conversion)
        return data
    ret = recursive_conversion(struct)
    return ret

def start_conversion(struct: Dict, entry_index: List[str]):
    sub_struct = get_entry_sub_struct(struct, entry_index)
    data = convert(sub_struct[0], '')
    utils.save_structure(data, r'C:\Users\mdoni\Desktop\MAX\Project\Python\opc-ua-simulator\opcua_sim\Client\save\data.json')

def convert_for_ignition(config_path):
    config = utils.load_config(config_path)
    structs_to_convert: List[Dict] = []
    for settings in config[gc.Struct.SETTINGS]:
        struct = utils.load_config(settings[gc.Struct.STRUCT_PATH])
        entry_index = settings[gc.Struct.UDT_ENTRY_INDEX]
        start_conversion(struct, entry_index)