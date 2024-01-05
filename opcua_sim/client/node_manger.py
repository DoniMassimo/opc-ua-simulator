from typing import Dict, List, Tuple
import asyncua as ua
from asyncua import ua as u
import utils.utils as utils
from utils.global_const import Struct as stc
from . import struct_manager as sm


async def nodes_children_scan(node: ua.Node, client: ua.Client, default_value=True) -> Tuple[Dict, str]:
    async def recursive_children_scan(node: ua.Node) -> Tuple[Dict, str]:         
        node_struct, node_id = await get_node_attrs(node, client, default_value)
        node_struct[node_id][stc.CHILDREN] = {}
        sub_nodes = await node.get_children()
        if sub_nodes:
            for node in sub_nodes:            
                child_node_attrs, child_node_id = await recursive_children_scan(node=node)
                node_struct[node_id][stc.CHILDREN][child_node_id] = child_node_attrs[child_node_id]
        return node_struct, node_id
    return (await recursive_children_scan(node))

async def nodes_parent_scan(node: ua.Node, client: ua.Client, default_value=True):
    async def recursive_parent_scan(node: ua.Node, child_node_attrs: Dict = {}, 
                                child_node_id: str = '') -> Tuple[Dict, str]:    
        node_struct, node_id = await get_node_attrs(node, client, default_value)
        if child_node_attrs:
            node_struct[node_id][stc.CHILDREN] = {child_node_id:child_node_attrs[child_node_id]}
        else:
            node_struct[node_id][stc.CHILDREN] = {} 
        parent_node = await node.get_parent()
        if parent_node:
            parent_node_attrs, parent_node_id = await recursive_parent_scan(parent_node, 
                                                                        node_struct, node_id)
            return parent_node_attrs, parent_node_id
        return node_struct, node_id 
    return (await recursive_parent_scan(node))

async def get_base_datatype(data_type_node: ua.Node) -> str:    
    while True:
        display_name = await data_type_node.read_attribute(u.AttributeIds.DisplayName)
        display_name = display_name.Value.Value.Text
        if display_name == 'BaseDataType' or display_name == 'Number':
            return True        
        else:
            parent_node_type = await data_type_node.get_parent()
            res = await get_base_datatype(parent_node_type)
            if res == True:
                return display_name.lower()
            else:
                return res

async def create_root_to_udt_struct(udt_entry_index: List[str], client: ua.Client, udt_structs: List[Dict]):
    nodes_struct = []
    for udt_index in udt_entry_index:
        udt_node = client.get_node(udt_index)
        root_to_udt_struct, root_node_id = await nodes_parent_scan(udt_node, client)
        nodes_struct.append(root_to_udt_struct)
    merged_node_struct = sm.merge_nodes_struct(nodes_struct, udt_structs)
    return merged_node_struct

async def get_node_attrs(node: ua.Node, client: ua.Client, default_value=False):
    attrs = await node.read_attributes([u.AttributeIds.DisplayName, 
                                        u.AttributeIds.BrowseName, 
                                        u.AttributeIds.NodeId,
                                        u.AttributeIds.NodeClass,
                                        u.AttributeIds.Value,
                                        u.AttributeIds.DataType])
    display_name = attrs[0].Value.Value.Text
    browse_name = attrs[1].Value.Value.Name
    node_id = f'ns={attrs[2].Value.Value.NamespaceIndex};i={attrs[2].Value.Value.Identifier}'
    node_class = attrs[3].Value.Value
    data_type_id = attrs[5].Value.Value
    if data_type_id:
        data_type_node = client.get_node(data_type_id)
        data_type = await get_base_datatype(data_type_node)
    else:
        data_type = None
    if default_value and data_type:
        value = utils.get_default_from_type(data_type)
    else:
        value = attrs[4].Value.Value
    attrs_dict = {node_id:{stc.BROWSE_NAME:browse_name,
                           stc.NODE_ID:node_id,
                           stc.NODE_CLASS:node_class,
                           stc.VALUE:value,
                           stc.DISPLAY_NAME:display_name,
                           stc.DATA_TYPE:data_type
                           }}
    return attrs_dict, node_id
