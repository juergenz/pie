"""Logging configuration."""

__all__ = ['logger']

import logging
import datetime

loglevel = logging.DEBUG

now = datetime.datetime.now().strftime('%Y-%m-%d %X')
logging.basicConfig(filename='logs/' + now + '.log', level=loglevel, format='%(asctime)s %(name)s:%(filename)s - %(levelname)s: %(message)s')

# define a Handler which writes to the sys.stderr
console = logging.StreamHandler()
console.setLevel(loglevel)

# set a format which is simpler for console use
formatter = logging.Formatter('%(name)s:%(filename)s - %(levelname)s: %(message)s')

# tell the handler to use this format
console.setFormatter(formatter)
# add the handler to the root logger
logging.getLogger('').addHandler(console)

# Name the logger after the package.
logger = logging.getLogger(__package__)