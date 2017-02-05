__all__ = ['ManiaPlanetServer']

from xmlrpc.client import _Method
from .gbx_protocol import GbxProtocol
from .asyncio_loop import loop
from .log import logger
from .callbacks import Callback, ModeScriptCallback
from .events import send_event

class RPC:

    def __init__(self, protocol):

        self.protocol = protocol


     # only gets called when the attribute is not defined eg. when a server rpc happens
    def __getattr__(self, name):
        # magic method dispatcher
        return _Method(self.protocol.rpc, name)
        # note: to call a remote object with an non-standard name, use
        # result getattr(server, "strange-python-name")(args)


class ManiaPlanetServer:

    def __init__(self, config):

        self.config = config
        self.rpc = None
        self.players = {}
        self._protocol = None
        self._transport = None
        self._connected = False


    def chat_send(self, text, player=None):

        if player is None:
            self.run_task(self.chat_send_wait(text))
        else:
            self.run_task(self.chat_send_wait(text, player))


    def chat_send_error(self, text, player=None):

        if player is None:
            self.run_task(self.chat_send_error_wait(text))
        else:
            self.run_task(self.chat_send_error_wait(text, player))


    async def chat_send_wait(self, text, player=None):

        if player is None:
            await self.rpc.ChatSendServerMessage('$z' + text)
        else:
            await self.rpc.ChatSendServerMessageToLogin('$z» ' + text, player.login)


    async def chat_send_error_wait(self, text, player=None):

        if player is None:
            await self.rpc.ChatSendServerMessage('$z$f00' + text)
        else:
            await self.rpc.ChatSendServerMessageToLogin('$z$f00» ' + text, player.login)


    def player_from_login(self, login):
        if login == self.config.login:
            return None
        return self.players[login]


    def handle_done_task(self, future):

        try:
            future.result() # raise Exception if one occurred
        except Exception as exp:
            self.chat_send_error(str(future))
            logger.error(str(future))
            raise
        else:
            logger.debug(future)


    def run_task(self, coro, done_callback=None):

        task = loop.create_task(coro)
        if done_callback is None:
            task.add_done_callback(self.handle_done_task)
        else:
            task.add_done_callback(done_callback)

    ### MAKE THIS FAIL SAFE
    def _handle_callback(self, handle, rawcallback):

        #try:

        callback = Callback(rawcallback[0], rawcallback[1])

        # special handling for ModeScriptCallbackArray so it is possible to catch a specific ModeScriptCallback by his name
        # still sending the 'ManiaPlanet.ModeScriptCallbackArray' event anyway
        if callback.name == 'ManiaPlanet.ModeScriptCallbackArray':
            modescript_callback = ModeScriptCallback(rawcallback[0], rawcallback[1])
            send_event(modescript_callback.name, modescript_callback)

        send_event(self, callback.name, callback)


    async def create_connection(self):

        if self._connected:
            logger.error('connection is already established')
            raise 'connection is already established'
            return

        gbxprotocol = GbxProtocol(loop, self._handle_callback)

        try:
            self._transport, self._protocol = await loop.create_connection(lambda: gbxprotocol, self.config.host, self.config.port)
        except ConnectionRefusedError:
            loop.stop()
            raise

        self.rpc = RPC(self._protocol)
        logger.info('connection established to maniaplanet server ' + self.config.host + ':' + str(self.config.port))
        await self.rpc.SetApiVersion('2013-04-16')
        await self.rpc.Authenticate(self.config.user, self.config.password)
        await self.rpc.SendHideManialinkPage()
        await self.rpc.EnableCallbacks(True)
        send_event(self, 'pie.connection_made')
        self._connected = True
        self.chat_send('pie started')






