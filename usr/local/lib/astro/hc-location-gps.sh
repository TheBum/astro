#!/bin/bash

echo none | sudo tee /sys/class/leds/led0/trigger
echo 1 | sudo tee /sys/class/leds/led0/brightness

echo "Getting GPS location..."
location=$(/usr/local/lib/astro/get-gps-loc.py)

if [ ${?} != 0 ]; then exit; fi

HEX="\\\\x%02X"
unset FORMAT
for i in {1..8}; do
  FORMAT="${FORMAT}${HEX}"
done

echo "Location: '${location}'"
hex_text="$(printf "W${FORMAT}" ${location})"

echo "Writing location to HC: '${hex_text}'"
#echo -ne "${hex_text}" > ${serial}
##
exec 3<>/dev/tcp/localhost/12345
printf "showshortport 4030\r\n" >&3
result=$(timeout 1 cat <&3)
if [[ "x$result" == *"waiting"* ]]; then
  printf "setportenable 4030 off\r\n" >&3
  timeout 1 cat <&3
  printf "disconnect 4030\r\n" >&3
  timeout 2 cat <&3
fi
printf "setportenable 4030 raw\r\n" >&3
timeout 1 cat <&3
exec 3<&-
exec 3>&-
##
exec 4<>/dev/tcp/localhost/4030
#sleep 1
echo -ne "${hex_text}" >&4
timeout 1 cat <&4
exec 4<&-
exec 4>&-

echo 0 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 1 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 0 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 1 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 0 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 1 | sudo tee /sys/class/leds/led0/brightness
sleep 1
echo 0 | sudo tee /sys/class/leds/led0/brightness
echo mmc0 | sudo tee /sys/class/leds/led0/trigger
