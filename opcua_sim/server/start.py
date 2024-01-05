import server as server
import asyncua as ua

def first_callback(node: ua.Node, val, data):
    print('\nFUNGE')


if __name__ == "__main__":
    server.start_server(r'C:\Users\mdoni\Desktop\MAX\Project\Python\opc-ua-simulator\opcua_sim\Client\save\10_10_219_65.json', {})


