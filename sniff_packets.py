#PACKET SNIFFING SCRIPT
from scapy.all import sniff, Dot11

def packet_handler(packet):
    if packet.haslayer(Dot11):
        print(f"[+] Packet: {packet.summary()}")

# Replace 'wlan0mon' with your actual monitor interface
sniff(iface='wlan0mon', prn=packet_handler, store=0)
