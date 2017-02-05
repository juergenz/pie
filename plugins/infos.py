import asyncio
import pie


class infos(pie.Plugin):

    def __init__(self):

        super().__init__()
        self.index = 0
        self.infos = ['This mode needs minimum 4 players.',
                      'You can cast votes in "Esc -> Manage Server" menu.',
                      'The Warm Up will be skiped if everyone presses "Give Up".',
                      'If you have a good map for this mode tell MakeLove.',
                       'Please change to Spectator when going AFK!']


    @asyncio.coroutine
    def on_load(self):

        self.connect_event('ManiaPlanet.EndMatch', self.print_next_info)


    @asyncio.coroutine
    def print_next_info(self, callback):

        #yield from pie.server.AutoTeamBalance()
        yield from pie.chat_send('$<$f00Info:$> ' + self.nextInfo())


    def nextInfo(self):

        t = self.infos[self.index]
        if self.index == len(self.infos) - 1:
            self.index = 0
        else:
            self.index = self.index + 1
        return t



