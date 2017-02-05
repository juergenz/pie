__all__ = ['chatcommand', 'execute_chat_command', 'save_matchsettings', '_register_chat_command']

import functools
import inspect

from .events import eventhandler, send_event
from .log import logger
from .asyncio_loop import loop


_registered_chat_commands = {}  # dict of all registered chat commands


async def execute_chat_command(server, player, cmd):

    #if not player.is_admin():
        #r = check_rights(player)


    args = cmd.split(' ')
    if args[len(args) - 1] is '':
        del args[len(args) - 1]

    if args[0] in _registered_chat_commands:

        try:

            if len(args) == 1:
                server.run_task(_registered_chat_commands[args[0]](server, player))
            else:
                server.run_task(_registered_chat_commands[args[0]](server, player, *args[1:]))

        except Exception as exp:
            server.chat_send_error('fault use of chat command: ' + args[0], player)
            server.chat_send_error(str(exp), player)
            server.chat_send('use /help to see available chat commands', player)
            raise

    else:
        server.chat_send_error('unknown chat command: ' + args[0], player)
        server.chat_send('use /help to see available chat commands', player)


def _register_chat_command(chat_command, function):

    if chat_command not in _registered_chat_commands:
        _registered_chat_commands[chat_command] = function
    else:
        logger.error('chatcommand ' + "'" + chat_command + "'" + ' already registered to ' + str(function))
        return False


def _unregister_chat_command(chat_command):

    if chat_command not in _registered_chat_commands:
        raise 'chat command not registered'
    else:
        del _registered_chat_commands[chat_command]


# @chatcommand decorator
def chatcommand(cmd):

    def chatcommand_decorator(func):

        if _register_chat_command(cmd, func) is False:
            return

        module = inspect.getmodule(func)
        logger.debug('chatcommand ' + "'" + cmd + "' connected to " + str(func) + ' in module ' + str(module))

        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return func_wrapper

    return chatcommand_decorator


@eventhandler('ManiaPlanet.PlayerChat')
async def _on_player_chat(server, callback):

    p = server.player_from_login(callback.login)

    # ignore normal chat
    if not callback.isCommand:
        if p is not None:
            send_event(server, 'pie.PlayerChat', p)
        return

    server.run_task(execute_chat_command(server, p, callback.text))


@chatcommand('/help')
async def cmd_help(server, player):

    """list all chat commands"""

    server.chat_send('help:', player)

    for cmd in _registered_chat_commands:
        if _registered_chat_commands[cmd].__doc__ is None:
            docstr = 'no description set'
        else:
            docstr = _registered_chat_commands[cmd].__doc__

        server.chat_send(cmd + ' - ' + docstr, player)


async def save_matchsettings(server, filename = None):

    await server.rpc.SaveMatchSettings('MatchSettings\\' + server.config.matchsettings)


@chatcommand('/savematchsettings')
async def cmd_savematchsettings(server, player):

    await save_matchsettings(server)
    server.chat_send('matchsettings saved: ' + server.config.matchsettings)


@chatcommand('/shutdown')
async def cmd_shutdown(server, player):

    await server.chat_send_wait('pie shutdown')
    loop.stop()


@chatcommand('/players')
async def cmd_players(server, player):

    for player in server.players:
        server.chat_send(server.players[player].nickname)