__all__ = []

import sqlite3

_conn = sqlite3.connect('pie.db')
_c = _conn.cursor()
