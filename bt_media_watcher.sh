#!/bin/bash

dbus-monitor --system "type='signal',interface='org.freedesktop.DBus.Properties" |
while read -r line; do
    if echo "$line" | grep -q "$buds" && echo "$line" | grep -q "Connected" && echo "$line" | grep -q "boolean false"; then
        playerctl pause
    fi
done