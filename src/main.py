import sys

import pie
import config


def handle_exception(exc_type, exc_value, exc_traceback):
    #if issubclass(exc_type, KeyboardInterrupt):
        #sys.__excepthook__(exc_type, exc_value, exc_traceback)
        #return

    pie.logger.error("uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))


sys.excepthook = handle_exception
sys.path.append('plugins')

import maps

pie.servers = {}

for server in config.servers:
    pie.servers[server.login] = pie.ManiaPlanetServer(server)
    pie.servers[server.login].run_task(pie.servers[server.login].create_connection())

pie.loop.run_forever()
pie.loop.close()
pie.logger.info('pie shutdown')