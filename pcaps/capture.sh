#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Usage:   script.sh <interface> <domain>      <?source>"
    echo "Example: script.sh eth0        jjay.cuny.edu lynx"
    exit 1
fi

# Create the directory if it does not already exist.
[ -d ./pcaps/$2 ] || mkdir -pv ./pcaps/$2

# Create the file name.
fname="$2-$(date +'%m-%d-%y_%T')"

if [ ! -z "$3" ]; then
    fname="$fname-$3"
    echo "PCAPs in ./pcaps/$2: " $(ls -ltr ./pcaps/$2/ | grep "$3.pcap$" | wc -l)
else
    echo "PCAPs in ./pcaps/$2: " $(ls -ltr ./pcaps/$2/ | grep ".pcap$" wc -l)
fi

sudo tcpdump -vv -x -X -i $1 -A tcp and port not 22 -w ./pcaps/$2/$fname.pcap
