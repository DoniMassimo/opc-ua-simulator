import asyncio
from typing import List, Dict, Tuple
import logging
import os
import json
import socket
from pprint import pprint
import asyncua as ua
from asyncua import ua as u 
from asyncua.common import xmlimporter
import opcua_constant as oc

async def get_node_attrs(node, default_value=True):
    attrs = await node.read_attributes([u.AttributeIds.DisplayName, 
                                        u.AttributeIds.BrowseName, 
                                        u.AttributeIds.NodeId,
                                        u.AttributeIds.NodeClass,
                                        u.AttributeIds.Value])
    display_name = attrs[0].Value.Value.Text
    browse_name = attrs[1].Value.Value.Name
    node_id = f'ns={attrs[2].Value.Value.NamespaceIndex};i={attrs[2].Value.Value.Identifier}'
    node_class = attrs[3].Value.Value
    value = attrs[4].Value.Value
    if default_value:
        if value is str:
            value = '' 
        elif value is int:
            value = 0
        elif value is float:
            value = 0.0
    attrs_dict = {node_id:{oc.BROWSE_NAME:browse_name,
                           oc.NODE_ID:node_id,
                           oc.NODE_CLASS:node_class,
                           oc.VALUE:value,
                           oc.DISPLAY_NAME:display_name}}
    return attrs_dict, node_id

async def get_node_children_id(node: ua.Node) -> List[str]:
    node_children: List[ua.Node] = await node.get_children()
    node_children_id = [] 
    for child in node_children:
        node_id = (await get_node_attrs(child))[1]
        node_children_id.append(node_id)
    return node_children_id

async def create_node(node_attrs: Dict[str, str], parent_node: ua.Node):
    new_node: ua.Node
    if node_attrs[oc.NODE_CLASS] == 1:
        new_node = await parent_node.add_object(node_attrs[oc.NODE_ID],
                                     node_attrs[oc.DISPLAY_NAME])
    else:
        new_node = await parent_node.add_variable(node_attrs[oc.NODE_ID],
                                                  node_attrs[oc.DISPLAY_NAME], node_attrs[oc.VALUE])
        await new_node.set_writable()
    return new_node

async def create_node_from_struct(rel_server_struct: Dict, current_node: ua.Node, server: ua.Server):
    struct_id = list(rel_server_struct.keys())[0]
    rel_struct_attrs = rel_server_struct[struct_id]
    if rel_struct_attrs[oc.CHILDREN]:
        current_childer_id = await get_node_children_id(current_node)
        for child_id, child_attrs in rel_struct_attrs[oc.CHILDREN].items():
            if child_id not in current_childer_id:
                await create_node(child_attrs, current_node)
            child_node = server.get_node(child_id)
            await create_node_from_struct({child_id:child_attrs}, child_node, server)

def get_ip() -> str:
    host_name = socket.gethostname()
    ip_address = socket.gethostbyname(host_name)
    return ip_address

def get_struct_and_endpoint(struct_path: str) -> Tuple[Dict, str]:
    all_structs: Dict = {}
    with open(struct_path, 'r') as all_structs_file:
        json_all_structs = all_structs_file.read()
        all_structs = json.loads(json_all_structs)
    current_ip = get_ip()
    struct: Dict = {}
    endpoint = ''
    for key, value in all_structs.items():
        if current_ip in str(key):
            endpoint = key
            struct = all_structs[key]
    return struct, endpoint

async def main():
    save_file_path = './'
    server = ua.Server()
    await server.init()
    uri = "http://examples.freeopcua.github.io"
    p = os.path.join(save_file_path, 'server_struct.json')
    server_structure, server_endpoint = get_struct_and_endpoint(p)
    server.set_endpoint(server_endpoint)
    root_node = server.get_root_node()
    await create_node_from_struct(server_structure, root_node, server)
    async with server:
        while True:
            await asyncio.sleep(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
