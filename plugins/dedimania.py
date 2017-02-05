import pie
import aiohttp
import zlib
from xmlrpc.client import dumps, loads, Fault

class DediProtocol():

    def __init__(self):

        self._dediurl = 'http://dedimania.net:8081/Dedimania'
        self._dedicode = 'fe080daeb3'
        self.headers = {'Content-Type': 'text/xml; charset=UTF-8', 'Keep-Alive': 'timeout=600, max=2000', 'Connection': 'Keep-Alive'}#, 'Content-Encoding': 'deflate'}
        self.session = self.session = aiohttp.ClientSession(connector=aiohttp.TCPConnector(keepalive_timeout=2000), headers=self.headers)
        pie._connect_event('pie.connection_made', self._init)
        pie._register_chat_command('/dedis', self.get_dedis)


    #@pie.eventhandler('pie.connection_made')
    async def _init(self, server):

        r1 = await server.GetDetailedPlayerInfo(server.login)
        r2 = await server.GetVersion()

        params = ({'Game':'TM2', 'Login':server.login, 'Code':self._dedicode, 'Path':r1['Path'], 'Packmask':'Valley', 'ServerVersion':r2['Version'], 'ServerBuild':r2['Build'], 'Tool':'pieIsToShort', 'Version':'dev'},)
        request = dumps(params, 'dedimania.OpenSession')
        t = request.encode(errors='surrogateescape')
        #t = zlib.compress(t)
        r = await self.session.post(self._dediurl, data=t)
        rr = await r.text()
        response, methodname = loads(rr)

        response = response[0]
        params = (response['SessionId'],)
        request = dumps(params, 'dedimania.CheckSession')
        t = request.encode(errors='surrogateescape')
        #t = zlib.compress(t)
        r = await self.session.post(self._dediurl, data=t)
        rr = await r.text()
        response, methodname = loads(rr)

        b = 1
        #dedimania.WarningsAndTTR2


    async def get_dedis(self, server, player):

        pass


dedi_conn = DediProtocol()




