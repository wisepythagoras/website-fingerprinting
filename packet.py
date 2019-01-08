#!/usr/bin/env python

import sys
import dpkt
import datetime

if len(sys.argv) == 1:
    print("An argument is required")
    exit(1)

f = open(sys.argv[1], 'rb')

pcap = dpkt.pcap.Reader(f)
open_time = 0

for ts, buf in pcap:
    if open_time is 0:
        open_time = ts
        print("# The start time was on %s (%s)" % (
            datetime.datetime.fromtimestamp(
                open_time
            ).strftime('%Y-%m-%d %H:%M:%S'),
            open_time,
        ))
        print("timing,bytes")

    print("%s,%s" % (round(ts - open_time, 5), len(buf),))
