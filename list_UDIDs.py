#!/usr/bin/env python

import sqlite3
import sys

__conn = sqlite3.connect ("./mdm.db")
if not __conn:
    print "Can't connect to database."
    sys.exit (1)

__cursor = __conn.cursor ()
sql = "SELECT UDID FROM mdm_device"
__cursor.execute (sql)
print __cursor.fetchone()
__cursor.close()
__conn.close()

