import asyncua as ua
import server.server


def first_callback(node: ua.Node, val, data):
    print("\nFUNGE")


if __name__ == "__main__":
    server.start_server(
        r"/home/max220/programming/opc-sim-venv/opc-ua-simulator/opcua_sim/client/save/10_10_219_65.json",
        {},
    )
