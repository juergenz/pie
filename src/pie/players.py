__all__ = []

import asyncio

from .log import logger
from .events import send_event, eventhandler
from .common import mpstr
from .exceptions import XMLRPCError

_MAXREADLIST = 300

class Player():

    def __init__(self, server, login, is_spectator, nickname):

        self.server = server
        self.login = login
        self.is_spectator = is_spectator
        self.nickname = nickname


    async def forcespec(self, mode = 3):
        await self.server.ForceSpectator(self.login, mode)

    async def kick(self):
        await self.server.Kick(self.login, '')

    async def mute(self):
        await self.server.Ignore(self.login)

    async def unmute(self):
        await self.server.UnIgnore(self.login)

    async def is_admin(self):
         pass


# @asyncio.coroutine
# def chat_command_forcespec(login, logintoforce, mode = 3):
#
#     p = _player_list[logintoforce]
#     chat_send(p.nickname + ' forced to Spectator!')
#     await p.forcespec(mode)
#
#
# @asyncio.coroutine
# def chat_command_kick(login, logintokick):
#
#     p = _player_list[logintokick]
#     chat_send(p.nickname + ' kicked!')
#     await p.kick()
#
#
# @asyncio.coroutine
# def chat_command_mute(login, logintomute):
#
#     p = _player_list[logintomute]
#     chat_send(p.nickname + ' muted!')
#     await p.mute()
#
#
# @asyncio.coroutine
# def chat_command_unmute(login, logintounmute):
#
#     p = _player_list[logintounmute]
#     chat_send(p.nickname + ' unmuted!')
#     await p.unmute()


@eventhandler('pie.connection_made')
async def _init(server):

    list = await _get_player_list(server)
    for p in list:
        if p['Login'] == server.config.login:
            continue
        p = Player(server, p['Login'], False, mpstr(p['NickName']))
        server.players[p.login] = p
        send_event(server, 'pie.PlayerConnect', p)


async def _get_player_list(server):

    list = []
    i = 0

    try:
        while True:

            r = await server.rpc.GetPlayerList(_MAXREADLIST, i)
            i = i + _MAXREADLIST
            list.extend(r)

    except XMLRPCError as e:
        logger.debug('catched exception: ' + str(e))
        pass # no more _player_list

    return list


@eventhandler('ManiaPlanet.PlayerConnect')
async def _on_player_connect(server, callback):


    r = await server.rpc.GetPlayerInfo(callback.login)
    p = Player(server, callback.login, callback.isSpectator, mpstr(r['NickName']))
    send_event(server, 'pie.PlayerConnect', p)
    server.players[callback.login] = p


@eventhandler('ManiaPlanet.PlayerDisconnect')
async def _on_player_disconnect(server, callback):

    if callback.login == server.config.login:
        return
    p = server.players[callback.login]
    send_event(server, 'pie.PlayerDisconnect', (p, callback.DisconnectionReason))
    server.chat_send('Disconnect: ' + p.nickname)
    del server.players[callback.login]