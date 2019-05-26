#!/bin/sh -e

cd /usr/local/lib/astro
/usr/bin/python3 gps3_info.py &
cd -

exit 0
