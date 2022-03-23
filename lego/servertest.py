import asyncio
from time import sleep

from calculus.expression import Expression


class EchoServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        self.loop = asyncio.get_event_loop()

    def data_received(self, data):
        expr = Expression(data)
        print('Expression: {}'.format(expr))
        # self.loop.create_task(self.send_progress())

        for x in range(50, 255):
            byte = (x).to_bytes(1, 'big', signed=False)
            self.transport.write(byte)
            sleep(1)

        print('Close the client socket')
        self.transport.close()
    
    async def send_progress(self):
        for x in range(255):
            byte = (x).to_bytes(1, 'big', signed=False)
            self.transport.write(byte)
            print(byte)
            await asyncio.sleep(0.1)



async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: EchoServerProtocol(),
        '0.0.0.0', 64010)

    async with server:
        await server.serve_forever()


asyncio.run(main())