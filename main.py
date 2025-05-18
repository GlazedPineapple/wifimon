#!/bin/env ./bin/python3

import scapy.all as scapy
import dhcp

packets = scapy.sniff(iface="eth0", count=10)
print(packets)
dhcp.start()

leases = dhcp.leases()
print(leases)