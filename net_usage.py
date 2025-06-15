#!/usr/bin/python3

import json
import sys
import time

iface = "wlo1"

rx_prev = 0
tx_prev = 0

def read_bytes(path):
    try:
        with open(path, 'r') as f:
            return int(f.read().strip())
    except:
        return 0
    

print(json.dumps({"version": 1}))
print("[")
print("[],")

while True:
    line = sys.stdin.readline()
    if not line:
        break

    if line.startswith(","):
        line = line[1:]
    
    try:
        status = json.loads(line)
    except json.JSONDecodeError:
        continue

    rx = read_bytes(f"/sys/class/net/{iface}/statistics/rx_bytes")
    tx = read_bytes(f"/sys/class/net/{iface}/statistics/tx_bytes")

    down_bytes = rx - rx_prev
    up_bytes = tx - tx_prev

    rx_prev = rx
    tx_prev = tx

    format_bytes = lambda b: f"{b / 1024:.2f}KB"

    net_block = {
        "full_text": f"D: {format_bytes(down_bytes)} U: {format_bytes(up_bytes)}",
        "name": "net_usage",
        "color": "#00FF00" if down_bytes < 1024**2 and up_bytes < 1024**2 else "#FF0000",
    }

    if isinstance(status, list):
        status.insert(0, net_block)
        print("," + json.dumps(status))
    else:
        print(line, end="")

    sys.stdout.flush()

    time.sleep(1)  # Update every second