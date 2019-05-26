#!/bin/bash

(
  rm /tmp/hctimeloc.log
  /usr/local/lib/astro/hc-time.sh > /tmp/hctimeloc.log
  /usr/local/lib/astro/hc-location-gps.sh >> /tmp/hctimeloc.log
)
