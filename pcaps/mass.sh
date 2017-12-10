#!/bin/bash

for i in `seq 1 2`; do
    echo "[$i][$(date)] Capturing..."

    # Start capturing.
    ./capture.sh eff.org lynx &

    # Start a lynx session over torsocks.
    torsocks timeout 20 lynx https://eff.org/ &

    sleep 21

    # Kill the tcpdump session.
    tcpdump_pid=$(ps axf | grep tcpdump | grep -v grep | awk '{ print $1 }')

    if [[ ! -z $tcpdump_pid ]]; then
        echo "Killing $tcpdump_pid"
        sudo kill -15 $tcpdump_pid
    fi

    # If lynx is still running it needs to be terminated.
    lynx_pid=$(pidof lynx)

    if [[ ! -z $lynx_pid ]]; then
        kill -9 $lynx_pid
    fi
done

