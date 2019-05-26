#!/usr/bin/env python

import os
import time
import datetime
import subprocess
 
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
from gps3.agps3threaded import AGPS3mechanism
from gps3.misc import satellites_used
 
# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)
 
# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)
 
# Clear display.
disp.fill(0)
disp.show()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)
font = ImageFont.load("./fonts/6x9.pil");

# First define some constants to allow easy resizing of shapes.
padding = 0
top = padding
bottom = height-padding

agps_thread = AGPS3mechanism()  # Instantiate AGPS3 Mechanisms
agps_thread.stream_data()  # From localhost (), or other hosts, by example, (host='gps.ddns.net')
agps_thread.run_thread()  # Throttle time to sleep after an empty lookup, default '()' 0.2 
datetime.time(15, 8, 24, 78915)

def dms(deg):
    m = (abs(deg) - int(abs(deg))) * 60.0
    s = (abs(m) - int(abs(m))) * 60.0
    return (int(deg), int(m), s)

def stats():
    # use custom font
    systimes = format(datetime.datetime.now().time())
    gpstimes = format(agps_thread.data_stream.time[0:19] \
                      + agps_thread.data_stream.time[23:24])
    lats = format(agps_thread.data_stream.lat)
    if lats != 'n/a':
        latdeg, latmin, latsec = dms(float(lats))
        if latdeg < 0:
            lats = 'S{: >3}'.format(-latdeg)
        else:
            lats = 'N{: >3}'.format(latdeg)
        lats = lats + 'º {: >2}'.format(latmin) + "' " \
                    + '{:5.2f}"'.format(latsec)
    lons = format(agps_thread.data_stream.lon)
    if lons != 'n/a':
        londeg, lonmin, lonsec = dms(float(lons))
        if londeg < 0:
            lons = 'W{: >3}'.format(-londeg)
        else:
            lons = 'E{: >3}'.format(londeg)
        lons = lons + 'º {: >2}'.format(lonmin) + "' " \
                    + '{:5.2f}"'.format(lonsec)
    alts = format(agps_thread.data_stream.alt)
    gpsmodes = format(agps_thread.data_stream.mode)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    draw.text((0, top+0), gpstimes, font=font, fill=255)
    draw.text((0, top+8), "Lat: " + lats, font=font, fill=255)
    draw.text((0, top+16), "Lon: " + lons, font=font, fill=255)
    if os.path.isfile('/tmp/setting'):
        draw.text((0, top+24), "Setting HC time/loc...", font=font, \
                  fill=255)
    else:
        draw.text((0, top+24), "Alt: " + alts, font=font, fill=255)
        if (gpsmodes == "3"):
            satInfo = satellites_used(agps_thread.data_stream.satellites)
            draw.text((80, top+24), "Sats: " + "{0}".format(satInfo[1]), \
                      font=font, fill=255)
        else:
            draw.text((80, top+24), "Mode: " + gpsmodes, font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.show()

def main():
    while True:
        stats()
        time.sleep(1)

if __name__ == "__main__":
    try:
        """
        serial = i2c(port=1, address=0x3C)
        device = sh1306(serial, rotate=2)
        """
        main()
    except KeyboardInterrupt:
        pass

