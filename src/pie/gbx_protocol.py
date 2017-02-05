__all__ = ['GbxProtocol']

import asyncio
from xmlrpc.client import dumps, loads, Fault

from .log import logger


class GbxProtocol(asyncio.Protocol):

    def __init__(self, loop, handle_callback):

        self.loop = loop
        self.handle_callback = handle_callback
        self.transport = None

        self.check_connection = True
        self.next_handle = 0x80000000
        self.futures = {}
        self.calls = {}

        self.buffer = b''
        self.read_xml = False
        self.len_xml = 0
        self.handle = 0


    def connection_made(self, transport):

        self.transport = transport
        logger.debug('connection_made .. OK')


    def data_received(self, data):

        #print('Data received: {!r}'.format(data))

        data = self.buffer + data

        if self.check_connection:
            if len(data) >= 15:
                self.connection_check(data[:15])
                data = data[15:]
                self.buffer = b''
            else:
                self.buffer = data
                return


        while len(data):

            if not self.read_xml:

                if len(data) >= 8:
                    self.len_xml = int.from_bytes(data[:3], 'little')
                    self.handle = int.from_bytes(data[4:8], 'little')
                    #print(self.len_xml)
                    #print(self.handle)
                    #print(data)
                    data = data[8:]
                    self.buffer = b''
                    self.read_xml = True

                else:
                    self.buffer = data
                    return

            else:

                if len(data) >= self.len_xml:
                    d = data[:self.len_xml]
                    #print(data)
                    #print(len(data))
                    try:
                        response, methodname = loads(d)
                    except Fault as exception:
                        self.handle_response_exception(self.handle, exception)
                    else:
                        if methodname != None:
                            logger.debug('callback received ' + str((methodname, response)))
                            self.handle_callback(self.handle, (methodname, response))
                        else:
                            self.handle_response(self.handle, (methodname, response))
                    finally:
                        data = data[self.len_xml:]
                        self.buffer = b''
                        self.read_xml = False

                else:
                    self.buffer = data
                    return



    def handle_response(self, handle, response):

        #logger.debug('response to ' + str(self.calls[handle]) + ' is ' + str(response))
        future = self.futures[handle]
        # unpack response
        if len(response[1]) == 1:
            response = response[1][0]
        else:
            response = response[1]
        #logger.debug(response)
        future.set_result(response)
        del self.futures[handle]
        del self.calls[handle]


    def handle_response_exception(self, handle, exception):

        logger.debug('response to ' + str(self.calls[handle]) + ' is ' + str(exception))
        future = self.futures[handle]
        future.set_exception(exception)
        del self.futures[handle]
        del self.calls[handle]


    def connection_lost(self, exc):

        logger.info('The server closed the connection: ' + str(exc))
        logger.info('Stop the event lop')
        self.loop.stop()
        #raise exc


    def connection_check(self, data):

        size = int.from_bytes(data[:3], 'little')
        protocol = data[4:].decode()
        if size != 11 or protocol != 'GBXRemote 2':
            self.loop.stop()
            raise Exception('wrong protocol response')
            logger.error(data)
        logger.debug('connection_check .. OK')
        self.check_connection = False


    def rpc(self, name, params):

        request = dumps(params, name)
        t = request.encode(errors='surrogateescape')
        handle = self.send_request(t)
        future = asyncio.Future(loop=self.loop)
        self.futures[handle] = future
        self.calls[handle] = name, params
        return future


    def send_request(self, request):

        datalen = len(request).to_bytes(4, 'little')
        if self.next_handle == 0xffffffff:
            self.next_handle = 0x80000000
        else:
            self.next_handle = self.next_handle + 1;
        handle = self.next_handle.to_bytes(4, 'little')
        data = datalen + handle + request
        #print(data)
        self.transport.write(data)
        return int.from_bytes(handle, 'little')


    # # only gets called when the attribute is not defined
    # def __getattr__(self, name):
    #     # magic method dispatcher
    #     return _Method(self.rpc, name)
    #     # note: to call a remote object with an non-standard name, use
    #     # result getattr(server, "strange-python-name")(args)