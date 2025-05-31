#!/bin/env ./.venv/bin/python3

import scapy.all as scapy
import dhcp
import netifaces
from pprint import pprint


global intWAN
intWAN = "eth0"
global intLAN
intLAN = "wlan1"


""" packets = scapy.sniff(iface="eth0", count=10)
print(packets) """


# Gets available network interfaces 
#netifaces.interfaces()
#for i in netifaces.interfaces():
#    pprint(netifaces.ifaddresses(i))


#starts dhcp server
dhcp.start(intLAN)
dhcp.client(intWAN)

leases = dhcp.leases()
#print(leases)