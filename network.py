import scapy.all as scapy
import time

#Just shows interface names
def getIntBR():
    return scapy.conf.iface

# Shows a lot more detail about interfaces
def getIntDetail():
    return scapy.conf.ifaces

#starts a sniff on given interface over a set period of time and returns the resulting packets
def sniff(interface, wait):
    pcap = scapy.sniff(iface=interface)
    time.sleep(wait)
    return pcap.summary()
    exit()

