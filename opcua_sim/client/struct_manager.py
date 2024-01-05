from typing import Dict, List
from utils.global_const import Struct as stc

def merge_nodes_struct(structs_rel_to_udt: List[Dict], udt_structs: List[Dict]) -> Dict:
    rel_struct = {}
    structs_sub_to_udt = []
    for struct in structs_rel_to_udt:
        rel_struct_id = list(struct.keys())[0]
        sub_struct = struct[rel_struct_id][stc.CHILDREN]
        if sub_struct:
            structs_sub_to_udt.append(sub_struct)
    for struct in structs_rel_to_udt:
        rel_struct_id = list(struct.keys())[0]
        rel_struct[rel_struct_id] = {}
        rs_browse_name = struct[rel_struct_id][stc.BROWSE_NAME]
        rs_display_name = struct[rel_struct_id][stc.DISPLAY_NAME]
        rs_node_class = struct[rel_struct_id][stc.NODE_CLASS]
        rs_node_id = struct[rel_struct_id][stc.NODE_ID]
        rs_value = struct[rel_struct_id][stc.VALUE]
        if structs_sub_to_udt:
            rel_struct[rel_struct_id][stc.CHILDREN] = merge_nodes_struct(structs_sub_to_udt, udt_structs)
        else:
            rel_struct[rel_struct_id][stc.CHILDREN] = {}
            for struct in udt_structs:
                struct_id = list(struct.keys())[0]
                if rs_node_id == struct_id:                    
                    rel_struct[rel_struct_id] = struct[struct_id]
        rel_struct[rel_struct_id][stc.BROWSE_NAME] = rs_browse_name
        rel_struct[rel_struct_id][stc.DISPLAY_NAME] = rs_display_name
        rel_struct[rel_struct_id][stc.NODE_CLASS] = rs_node_class
        rel_struct[rel_struct_id][stc.NODE_ID] = rs_node_id
        rel_struct[rel_struct_id][stc.VALUE] = rs_value
    return rel_struct