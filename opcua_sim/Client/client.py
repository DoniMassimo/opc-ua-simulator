import asyncio
from typing import Dict, List, Tuple
import asyncua as ua
from asyncua import ua as u, common
from asyncua.common import xmlexporter
from pprint import pprint
import asyncua
import json
import os
import opcua_constant as oc

async def nodes_children_scan(node: ua.Node) -> Tuple[Dict, str]:
    node_struct, node_id = await get_node_attrs(node)
    node_struct[node_id][oc.CHILDREN] = {}
    sub_nodes = await node.get_children()
    if sub_nodes:
        for node in sub_nodes:
            child_node_attrs, child_node_id = await nodes_children_scan(node=node)
            node_struct[node_id][oc.CHILDREN][child_node_id] = child_node_attrs[child_node_id]
    return node_struct, node_id

async def nodes_parent_scan(node: ua.Node, child_node_attrs: Dict = {}, 
                            child_node_id: str = '') -> Tuple[Dict, str]:
    node_struct, node_id = await get_node_attrs(node)
    if child_node_attrs:
        node_struct[node_id][oc.CHILDREN] = {child_node_id:child_node_attrs[child_node_id]}
    else:
        node_struct[node_id][oc.CHILDREN] = {} 
    parent_node = await node.get_parent()
    if parent_node:
        parent_node_attrs, parent_node_id = await nodes_parent_scan(parent_node, 
                                                                    node_struct, node_id)
        return parent_node_attrs, parent_node_id
    return node_struct, node_id 

def merge_nodes_struct(structs_rel_to_udt: List[Dict], udt_structs: List[Dict]) -> Dict:
    rel_struct = {}
    structs_sub_to_udt = []
    for struct in structs_rel_to_udt:
        rel_struct_id = list(struct.keys())[0]
        sub_struct = struct[rel_struct_id][oc.CHILDREN]
        if sub_struct:
            structs_sub_to_udt.append(sub_struct)
    for struct in structs_rel_to_udt:
        rel_struct_id = list(struct.keys())[0]
        rel_struct[rel_struct_id] = {}
        rs_browse_name = struct[rel_struct_id][oc.BROWSE_NAME]
        rs_display_name = struct[rel_struct_id][oc.DISPLAY_NAME]
        rs_node_class = struct[rel_struct_id][oc.NODE_CLASS]
        rs_node_id = struct[rel_struct_id][oc.NODE_ID]
        rs_value = struct[rel_struct_id][oc.VALUE]
        if structs_sub_to_udt:
            rel_struct[rel_struct_id][oc.CHILDREN] = merge_nodes_struct(structs_sub_to_udt, udt_structs)
        else:
            rel_struct[rel_struct_id][oc.CHILDREN] = {}
            for struct in udt_structs:
                struct_id = list(struct.keys())[0]
                if rs_node_id == struct_id:
                    pass
                    rel_struct[rel_struct_id] = struct[struct_id]
        rel_struct[rel_struct_id][oc.BROWSE_NAME] = rs_browse_name
        rel_struct[rel_struct_id][oc.DISPLAY_NAME] = rs_display_name
        rel_struct[rel_struct_id][oc.NODE_CLASS] = rs_node_class
        rel_struct[rel_struct_id][oc.NODE_ID] = rs_node_id
        rel_struct[rel_struct_id][oc.VALUE] = rs_value
    return rel_struct

async def create_root_to_udt_struct(udt_entry_index: List[str], client: ua.Client, udt_structs: List[Dict]):
    nodes_struct = []
    for udt_index in udt_entry_index:
        udt_node = client.get_node(udt_index)
        root_to_udt_struct, root_node_id = await nodes_parent_scan(udt_node)
        nodes_struct.append(root_to_udt_struct)
    merged_node_struct = merge_nodes_struct(nodes_struct, udt_structs)
    return merged_node_struct

async def get_node_attrs(node):
    attrs = await node.read_attributes([u.AttributeIds.DisplayName, 
                                        u.AttributeIds.BrowseName, 
                                        u.AttributeIds.NodeId,
                                        u.AttributeIds.NodeClass,
                                        u.AttributeIds.Value,])
                                        
    display_name = attrs[0].Value.Value.Text
    browse_name = attrs[1].Value.Value.Name
    node_id = f'ns={attrs[2].Value.Value.NamespaceIndex};i={attrs[2].Value.Value.Identifier}'
    node_class = attrs[3].Value.Value
    value = attrs[4].Value.Value
    attrs_dict = {node_id:{oc.BROWSE_NAME:browse_name,
                           oc.NODE_ID:node_id,
                           oc.NODE_CLASS:node_class,
                           oc.VALUE:value,
                           oc.DISPLAY_NAME:display_name,}}
    return attrs_dict, node_id

async def build_structure(udt_entry_index: List[str], client: ua.Client) -> Dict:
    udt_to_leaf_struct = []
    for udt_index in udt_entry_index:
        udt_node = client.get_node(udt_index)
        struct, node_id = await nodes_children_scan(udt_node)
        udt_to_leaf_struct.append(struct)
    server_structure = await create_root_to_udt_struct(udt_entry_index, client, udt_to_leaf_struct) 
    return server_structure

def save_structure(server_structure: Dict, save_path: str):
    js_server_structure = json.dumps(server_structure, indent=4)
    with open(save_path, 'w') as server_struct_file:
        server_struct_file.write(js_server_structure)

def load_config(config_file_path = './config.json') -> Dict:
    config = {}
    with open(config_file_path, 'r') as config_file:
        config = config_file.read()
        config = json.loads(config)
    return config

def start_client(config_files_name: List[str], save_path: str):
    for config_name in config_files_name:
        config = load_config(f'./{config_name}')
        asyncio.run(main(config, save_path))
        
async def main(config: Dict, save_path: str):
    server_structure = {}
    for settings in config[oc.OPC_SETTINGS]:
        url = settings[oc.END_POINT]
        udt_entry_path = settings[oc.UDT_ENTRY_INDEX]
        async with ua.Client(url=url) as client:
            await client.connect()       
            current_server_structure = await build_structure(udt_entry_path, client)
            server_structure[url] = current_server_structure
    save_structure(server_structure, save_path)

if __name__ == "__main__":
    start_client(['config.json'], '../server_struct/test.json') 
