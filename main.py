#!/bin/env ./.venv/bin/python3

import scapy.all as scapy
import dhcp
import socket


""" packets = scapy.sniff(iface="eth0", count=10)
print(packets) """


# Gets avalible network interfaces 

print(socket.if_nameindex())


#starts dhcp server
dhcp.start()

leases = dhcp.leases()
#print(leases)