__all__ = ['load_plugin']


import importlib

from .log import logger
from .chat_commands import chatcommand

_plugins = {}


async def load_plugin(server, name):

    importlib.invalidate_caches()

    if name in _plugins:
        m = importlib.reload(_plugins[name])
        logger.info('reload plugin ' + name)
        server.chat_send('reload plugin ' + name)
    else:
        m = importlib.import_module(name)
        logger.info('load plugin ' + name)
        server.chat_send('load plugin ' + name)

    _plugins[name] = m


@chatcommand('/loadplugin')
async def cmd_loadplugin(server, player, name):

    await load_plugin(server, name)

