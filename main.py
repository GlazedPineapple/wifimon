#!/bin/env ./.venv/bin/python3

import scapy.all as scapy
import dhcp
import netifaces
from pprint import pprint

global wan
wan = "eth0"
global lan
lan = "wlan1"


""" packets = scapy.sniff(iface="eth0", count=10)
print(packets) """


# Gets available network interfaces 
netifaces.interfaces()
for i in netifaces.interfaces():
    pprint(netifaces.ifaddresses(i))



#starts dhcp server
dhcp.start()

leases = dhcp.leases()
#print(leases)