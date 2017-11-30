#!/bin/bash

if [[ $# -eq 0 ]]; then
    echo "Usage:   script.sh <domain> <?source>"
    echo "Example: script.sh jjay.cuny.edu lynx"
    exit 1
fi

# Create the directory if it does not already exist.
[ -d ./pcaps/$1 ] || mkdir -pv ./pcaps/$1

# Create the file name.
fname="$1-$(date +'%m-%d-%y_%T')"

if [ ! -z "$2" ]; then
    fname="$fname-$2"
    echo "PCAPs in ./pcaps/$1: " $(ls -ltr ~/pcaps/$1/ | grep "$2.pcap$" | wc -l)
else
    echo "PCAPs in ./pcaps/$1: " $(ls -ltr ~/pcaps/$1/ | grep ".pcap$" wc -l)
fi

sudo tcpdump -vv -x -X -i eth0 -A tcp and port not 22 -w ./pcaps/$1/$fname.pcap
