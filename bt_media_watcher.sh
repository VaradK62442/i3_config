#!/bin/bash

connected_flag=0
echo "started" > ~/.bt_log

dbus-monitor --system "type='signal',interface='org.freedesktop.DBus.Properties'" |
while read -r line; do
    if echo "$line" | grep -q "Connected"; then
        echo "connected" >> ~/.bt_log
        connected_flag=1
    elif [[ $connected_flag -eq 1 ]] && echo "$line" | grep -q "boolean false"; then
        echo "bool false" >> ~/.bt_log
        playerctl pause
        connected_flag=0
    elif [[ $connected_flag -eq 1 ]] && echo "$line" | grep -q "boolean true"; then
        echo "bool true" >> ~/.bt_log
        playerctl play
        connected_flag=0
    fi
done