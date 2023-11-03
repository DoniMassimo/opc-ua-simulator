import server as server
import asyncua as ua

def first_callback(node: ua.Node, val, data):
    print('\nFUNGE')


if __name__ == "__main__":
    server.start_server('../server_data/server_struct.json', {'ns=2;i=2': first_callback})


