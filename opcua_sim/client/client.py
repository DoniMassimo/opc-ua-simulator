import asyncio
from typing import Dict, List
import asyncua as ua
import os
from utils.global_const import Config as cnc
from . import node_manger as nm
import utils.utils as utils


async def build_structure(
    udt_entry_index: List[str], client: ua.Client, default_values: bool
) -> Dict:
    udt_to_leaf_struct = []
    for udt_index in udt_entry_index:
        udt_node = client.get_node(udt_index)
        nm.nodes_children_scan.def_value = default_values
        struct, node_id = await nm.nodes_children_scan(udt_node, client)
        udt_to_leaf_struct.append(struct)
    server_structure = await nm.create_root_to_udt_struct(
        udt_entry_index, client, udt_to_leaf_struct
    )
    return server_structure


def start_client(project_path: str):
    config_path = os.path.join(project_path, "client/config.json")
    save_dir = os.path.join(project_path, "struct")
    config = utils.load_config(config_path)
    asyncio.run(main(config, save_dir))


async def main(config: Dict, save_dir: str):
    for settings in config[cnc.OPC_SETTINGS]:
        server_structure = {}
        if not settings[cnc.ENABLED]:
            continue
        save_file_name = settings[cnc.SAVE_FILE_NAME]
        url = settings[cnc.END_POINT_TO_SCAN]
        udt_entry_path = settings[cnc.UDT_ENTRY_INDEX]
        default_value = settings[cnc.DEFAULT_VALUE]
        async with ua.Client(url=url) as client:
            await client.connect()
            current_server_structure = await build_structure(
                udt_entry_path, client, default_value
            )
            server_structure[url] = current_server_structure
        utils.save_structure(server_structure, os.path.join(save_dir, save_file_name))


def test():
    project_dir = os.path.normpath(
        "/home/max220/programming/opc-sim-venv/opc-ua-simulator/opcua_sim/test_project"
    )
    start_client(
        project_dir,
    )
