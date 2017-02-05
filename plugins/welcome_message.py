import pie


@pie.eventhandler('pie.PlayerConnect')
async def on_player_connect(server, player):

    server.chat_send('Welcome ' + player.nickname)


@pie.chatcommand('/welcome')
async def cmd_welcome(server, player):

    server.chat_send('Welcome ' + player.nickname, player)
    await server.rpc.sdfsfsdf()


@pie.chatcommand('/muffin')
async def cmd_muffin(server, player, login):

    server.chat_send('Muffin for ' + server.player_from_login(login).nickname)