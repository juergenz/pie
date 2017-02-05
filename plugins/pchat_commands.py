import pie

@pie.chatcommand('/rpc')
async def chat_command_rpc(server, player, cmd):

    methodname = cmd[:cmd.find('(')]
    params = cmd[cmd.find('('):]
    params = params.strip('()')
    params = params.split(',')

    for i in range(len(params)):
        if params[i].isdecimal():
            params[i] = int(params[i])
        elif params[i] == 'true':
            params[i] = True
        elif params[i] == 'false':
            params[i] = False

    r = await getattr(server.rpc, methodname)(*params)
    server.chat_send(str(r), player)

"""
class chat_commands(pie.Plugin):

    def __init__(self):

        super().__init__()


    @asyncio.coroutine
    def on_load(self):

        self.register_chat_command('/loadmatchsettings', self.cc_load_matchsettings)
        self.register_chat_command('/pm', self.chat_command_pm)
        self.register_chat_command('/rpc', self.chat_command_rpc)
        self.register_chat_command('/hide', self.chat_command_hide)
        self.register_chat_command('/shutdown', self.chat_command_shutdown)
        self.register_chat_command('/endround', self.chat_command_endround)
        self.register_chat_command('/rules', self.chat_command_rules)
        self.register_chat_command('/votecancel', self.chat_command_votecancel)
        self.register_chat_command('/setpassword', self.chat_command_setpassword)
        self.register_chat_command('/setservername', self.cc_setservername)


    @asyncio.coroutine
    def cc_load_matchsettings(self, player):

        yield from pie.LoadMatchSettings()
        yield from pie.chat_send('load default matchsettings', player)


    @asyncio.coroutine
    def chat_command_pm(self, player, to, text):

        #yield from pie.chat_send('[' + login + ']' + ' » ' + text, to)
        yield from pie.server.ChatSendServerMessageToLogin('$z[' + player.login + '] » ' + text, to)





    @asyncio.coroutine
    def chat_command_hide(self, player=None):

        if player is None:
            yield from pie.server.SendHideManialinkPage()

        yield from pie.server.SendHideManialinkPageToLogin(player.login)


    @asyncio.coroutine
    def chat_command_endround(self, player):

        yield from pie.chat_send('Forcing end round!')
        yield from pie.server.ForceEndRound()


    @asyncio.coroutine
    def chat_command_rules(self, player):

        yield from pie.chat_send('$f00Rules of Chase mode: $fffTo score one $f00point$fff the $f00last$fff player of a team passing a checkpoint must be the $f00first$fff at the next one.')


    @asyncio.coroutine
    def chat_command_shutdown(self, player):

        yield from pie.server.SendHideManialinkPage()
        pie.loop.stop()


    @asyncio.coroutine
    def chat_command_votecancel(self, player):


        yield from pie.server.CancelVote()
        yield from pie.chat_send('Vote canceled!')


    @asyncio.coroutine
    #@pie.chat_command('setpassword')
    def chat_command_setpassword(self, player, s):

        yield from pie.server.SetServerPassword(s)


    @asyncio.coroutine
    def cc_setservername(self, player, s):

        yield from pie.server.SetServerName(s)
        yield from pie.chat_send('new servername: ' + s)
"""


