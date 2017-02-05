__all__ = ['eventhandler', 'send_event', '_connect_event']

import asyncio
import functools
import inspect

from .asyncio_loop import loop
from .log import logger

_registered_events = {}  # dict of all registered events


# @evenhandler decorator
def eventhandler(event):

    def eventhandler_decorator(func):

        if inspect.ismethod(func):
            print('2')

        _connect_event(event, func)
        module = inspect.getmodule(func)
        logger.debug('event ' + "'" + event + "' connected to " + str(func) + ' in module ' + str(module))

        @functools.wraps(func)
        def func_wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return func_wrapper

    return eventhandler_decorator


def send_event(server, event, data=None):

    #logger.debug('send_event ' + event)

    if event in _registered_events:
        for e in _registered_events[event]:
            try:
                if asyncio.iscoroutinefunction(e):
                    if data:
                        task = loop.create_task(e(server, data))
                    else:
                        task = loop.create_task(e(server))
                    task.add_done_callback(server.handle_done_task)
                else:
                    if data:
                        r = e(data)
                    else:
                        r = e()
                    #logger.debug('event finished ' + str(e) + ' result=' + str(r))
            except Exception as exp:
                #TODO delete fault event
                logger.error(str(exp))
                server.chat_send_error(str(exp))


def _connect_event(event, function):

    if event in _registered_events:
        # event already exists

        if function in _registered_events[event]:
            raise Exception('function already registered')

        _registered_events[event].append(function)

    else:
        # new event
        _registered_events[event] = [function]
