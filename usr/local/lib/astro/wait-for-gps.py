#!/usr/bin/python3

import sys
import time
from gps3 import gps3

gpsd_socket = gps3.GPSDSocket()
gpsd_socket.connect(host='127.0.0.1', port=2947)
gpsd_socket.watch()
data_stream = gps3.DataStream()

def getgps():
   for new_data in gpsd_socket:
       if new_data:
            data_stream.unpack(new_data)
       if data_stream.TPV['mode'] != 'n/a':
            break

getgps()
time.sleep(10)
