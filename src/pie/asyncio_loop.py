__all__ = ['loop']

import asyncio

loop = asyncio.get_event_loop()
#loop.set_debug(True)