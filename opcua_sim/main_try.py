import struct_converter.struct_converter as sc
import client.client as c
import server.server as s

if __name__ == "__main__":
    data_path = r"opcua_sim/struct_converter/config.json"
    # sc.convert_for_ignition(data_path)
    # c.test()
    s.start_server(
        "/home/max220/programming/opc-sim-venv/opc-ua-simulator/opcua_sim/test_project/struct/10_10_219_65.json",
        {},
    )
