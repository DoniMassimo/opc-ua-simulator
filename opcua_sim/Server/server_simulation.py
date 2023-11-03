import asyncio
import logging
import asyncua as ua
from asyncua import ua as u
from asyncua.common.methods import uamethod
import random as ran
import string

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(ran.choice(chars) for _ in range(size))

async def generate_sim_server(node: ua.Node, idx, node_code: str = '1', level=0):
    for i in range(ran.randint(1, 4)):
        rv = ran.randint(1, 3)
        value = None
        if rv == 1:
            value = ran.randint(0, 100)
        elif rv == 2:
            value = ran.uniform(0.0, 100.0)
        elif rv == 3:
            value = id_generator(size=ran.randint(1, 5))
        if level > 1:
            r = ran.randint(1, 2)
            if r == 1:
                await node.add_variable(idx, f'var{node_code}{str(i)}', value)
                return
        sub_obj = await node.add_object(idx, f'obj{node_code}{str(i)}')
        await generate_sim_server(sub_obj, idx, f'{node_code}{str(i)}', level=level+1)

async def main():
    server = ua.Server()
    await server.init()
    
    endp = "opc.tcp://10.10.1.26:4840/server"
    server.set_endpoint(endp)
    
    # set up our own namespace, not really necessary but should as spec
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)
    # await generate_sim_server(root, idx)
    myobj = await server.nodes.objects.add_object(idx, "MyObject")
    myvar = await myobj.add_variable(idx, "MyVariable", 6.7)
    a = await myobj.add_variable(idx, "var1", 6.7)
    b = await myobj.add_variable(idx, "var2", 6.7)
    c = await myobj.add_variable(idx, "var3", 6.7)
    second = await server.nodes.objects.add_object(idx, "second")
    await second.add_variable(idx, 'var4', 'ciao')
    await second.add_variable(idx, 'var5', 'ciao')
    await second.add_variable(idx, 'var6', 'ciao')
    await myvar.set_writable()
    async with server:
        while True:
            await asyncio.sleep(1)
            # new_val = await myvar.get_value() + 0.1
                # _logger.info("Set value of %s to %.1f", myvar, new_val)
            # await myvar.write_value(new_val)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main(), debug=True)
