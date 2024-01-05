
class Ignition():
    NAME = "name"
    TAG_TYPE = "tagType"
    TAGS = "tags"
    VALUE_SOURCE = "valueSource"
    OPC_ITEM_PATH = "opcItemPath"
    DATA_TYPE = "dataType"
    TAG_GROUP = "tagGroup"
    TAG_TYPE = "tagType"
    OPC_SERVER = "opcServer"

class Config():
    OPC_SETTINGS: str = 'opc_settings'
    SAVE_FILE_NAME: str = 'save_file_name'
    END_POINT_TO_SCAN: str = 'opc_endpoint_to_scan'
    UDT_ENTRY_INDEX: str = 'udt_entry_index'
    DEFAULT_VALUE: str = 'default_value'

class Struct():
    CHILDREN: str = 'children'
    BROWSE_NAME: str = 'browse_name' 
    DISPLAY_NAME: str = 'display_name'
    NODE_ID: str = 'node_id'
    NODE_CLASS: str = 'node_class'
    ROOT: str = 'root'
    VALUE: str = 'value'
    DATA_TYPE: str = 'data_type'
    
    STRUCT_PATH: str = 'struct_path'
    END_POINT: str = 'opc_endpoint_to_scan' 
    STRUCT_FILE: str = 'save_dir'
    SETTINGS: str = 'settings'
    DEFAULT_VALUE: str = 'default_value'
    STRUCT_NAME: str = 'save_file_name'
    UDT_ENTRY_INDEX: str = 'udt_entry_index'
