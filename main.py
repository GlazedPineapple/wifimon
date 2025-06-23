#!/bin/env ./.venv/bin/python3

import scapy.all as scapy
import dhcp
import netifaces
from pprint import pprint
import network

global intWAN
#defaults
intWAN = "eth0"
global intLAN
#defaults
intLAN = "wlan1"

network.sniff(intWAN,5)


print("Network interface info:",network.getIntDetail())
intWan = input("Please select an interface for wan: \n")
intLan = input("Please select an interface for Lan: \n")







#starts dhcp server
dhcp.start(intLAN)
dhcp.client(intWAN)

leases = dhcp.leases()
#print(leases)