import asyncio
import aiohttp
import pie
import time


class Map:

    def __init__(self, Author, Environnement, FileName, Name):

        self.Author = Author
        self.Environnement = Environnement
        self.FileName = FileName
        self.Name = Name


async def on_load(self):

    await update_map_list()


@pie.chatcommand('/add')
async def chat_command_add(server, player, mxid, insert = True):

    """add a map with mxid example: /addmap 3"""

    url = 'https://tm.mania-exchange.com/tracks/download/' + mxid

    t0 = time.perf_counter()

    try:
        r = await asyncio.wait_for(aiohttp.request('GET', url), 45)
    except asyncio.TimeoutError:
        server.chat_send('$f23MX not responding', player.login)
        return

    t1 = time.perf_counter()
    print(t1 - t0)


    if r.status != 200:
        server.chat_send('$f23HTTP status not ok', player.login)
        return


    map = await r.read()
    header = r.headers['Content-Disposition']
    searchstr = 'filename="'
    filename = header[header.find(searchstr) + len(searchstr):len(header) - 1]
    filename = mxid + '_' + filename

    mapsdir = await server.rpc.GetMapsDirectory()
    mapsdir = mapsdir + server.config.login + '/'

    t0 = time.perf_counter()
    with open(mapsdir + filename, 'wb') as file:
        file.write(map)
    t1 = time.perf_counter()
    print(t1 - t0)

    try:
        if insert:
            await server.rpc.InsertMap(mapsdir + filename)
            await server.rpc.ChooseNextMap(mapsdir + filename)
        else:
            await server.rpc.AddMap(mapsdir + filename)
    except pie.XMLRPCError as e:
        pie.logger.debug('catched exception: ' + str(e))
        server.chat_send('$fff' + filename + '$z already added')
        return

    #pie.ChooseNextMap(filename)
    #await self.update_map_list()
    r = await server.rpc.GetMapInfo(mapsdir + filename)
    #server.chat_send('$fff' + r['Name'] + '$z added & jukeboxed')
    server.chat_send(pie.mpstr(r['Name']) + ' added')


@pie.chatcommand('/remove')
async def chat_command_remove(server, player):

    r = await server.rpc.GetCurrentMapInfo()
    await server.rpc.RemoveMap(r['FileName'])
    server.chat_send(pie.mpstr(r['FileName']) + ' removed', player.login)
    pie.logger.info(player.login + ' removed map ' + pie.mpstr(r['FileName']))


@pie.chatcommand('/skip')
async def chat_command_skip(server, player):

    server.chat_send('Changing to next map!')
    await server.rpc.NextMap()


@pie.chatcommand('/restart')
async def chat_command_restart(server, player):

    server.chat_send('Map restart!')
    await server.rpc.RestartMap()


@pie.chatcommand('/replay')
async def chat_command_replay(server, player):

    r = await server.rpc.GetCurrentMapInfo()
    await server.rpc.ChooseNextMap(r['FileName'])
    server.chat_send('Map will be replayed!')


async def GetMapList(server):

    maplist = []
    i = 0

    try:
        while True:

            ml = await server.rpc.GetMapList(self._READMAPS, i)
            i = i + self._READMAPS
            maplist.extend(ml)

    except pie.XMLRPCError as e:
        pie.logger.debug('catched exception: ' + str(e))
        pass # no more maps

    return maplist


async def update_map_list(server):

    self.maplist.clear()
    t0 = time.perf_counter()
    mlist = await self.GetMapList()
    t1 = time.perf_counter()
    print(t1 - t0)
    for map in mlist:
        self.maplist.append(Map(map['Author'], map['Environnement'], map['FileName'], map['Name']))


@asyncio.coroutine
def chat_command_list(self, player):

    for i, map in enumerate(self.maplist):
        #server.chat_send(str(i) + self.GetMapString(map), player.login)
        pie.execute_task(server.chat_send(str(i) + self.GetMapString(map), player))


def GetMapString(self, map):

    return ' - $fff' + map.Name + '$z (' + '$s$fff' + map.Environnement + '$z' + ') ' + 'by $s$fff' + map.Author



async def on_map_list_modified(self, callback):

    await pie.SaveMatchSettings()

