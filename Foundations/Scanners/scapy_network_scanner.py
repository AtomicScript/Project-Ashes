from scapy.all import ARP, Ether, srp, ls
import nmap


def info_():
    # creates an arp packet
    request = ARP()
    # status of the packet created
    print(request.summary())
    # more details on the packet 
    print(request.show())
    # Fields can be filled and expected input 
    print(ls(ARP()))

'''
Steps for creating Network Scanner -

'''

def arp_scanner():
    # 1. Create an ARP packet using ARP() method
    request = ARP()
    # 2. Set the network range using variable.
    # pdst       : MultipleTypeField (IPField, IP6Field, StrFixedLenField) = '0.0.0.0'       ('None')
    request.pdst = '192.168.1.1/24'
    # 3. Create an Ethernet packet using Ether() method.
    broadcast = Ether()
    # 4. Set the destination to broadcast using variable hwdst.
    broadcast.dest = 'ff:ff:ff:ff:ff:ff'
    # 5. Combine ARP request packet and Ethernet frame using '/'.
    packet = broadcast / request
    # 6. Send this to your network and capture the response from different devices.
    clients = srp(packet, timeout=3, verbose=False)[0]
    #7 . Print the IP and MAC address from the response packets. 
    for sent, received in clients:
        print(f"IP: {received.psrc}, MAC: {received.hwsrc}")


def devices_arp_scanner():
    request = ARP(pdst='192.168.1.1/24')
    broadcast = Ether(dst = 'ff:ff:ff:ff:ff:ff')
    packet = broadcast / request
    answ, unansw = srp(packet, timeout=3, verbose=0)

    devices = []
    for sent, received in answ:
        devices.append({"ip": received.psrc, "mac": received.hwsrc})

    return devices



def get_device_info_nmap(ip_address):
    scanner = nmap.PortScanner()
    try:
        # add -F if you want it to be faster
        scan_results = scanner.scan(ip_address, arguments='-O -Pn')
        os_matches = scan_results['scan'][ip_address].get('osmatch', [])
        if os_matches:
            best_match = max(os_matches, key=lambda x: int(x['accuracy']))
            # print(best_match)
            print(f"Best Match: {best_match['name']} ({best_match['accuracy']}%)")
        
        else:
            print("Host is up, but no OS fingerprinting matches were found.")


    except nmap.PortScannerError as e:
        print(f"Nmap Error: {e}.")



active_devices = devices_arp_scanner()
for device in active_devices:
    print(f"{device['ip']}\t\t{device['mac']}")
    get_device_info_nmap(device['ip'])
    

# get_device_info_nmap(active_devices[1]['ip'])
# 