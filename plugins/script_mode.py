import asyncio
import pie


@pie.chatcommand('/setscript')
async def cmd_setscript(server, player, script):

    try:
        await server.SetScriptName(script)
        server.chat_send('new script: ' + script)
    except pie.XMLRPCError as e:
        pie.logger.debug('catched exception: ' + str(e))
        server.chat_send('could not load script: ' + script)


@asyncio.coroutine
def cc_set_script_settings(self, player, script):

    try:
        yield from pie.server.SetScriptName(script)
        yield from pie.chat_send('new script: ' + script)
    except pie.XMLRPCError as e:
        pie.logger.debug('catched exception: ' + str(e))
        yield from pie.chat_send('could not load script: ' + script)