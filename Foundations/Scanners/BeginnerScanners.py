import nmap, requests
from concurrent.futures import ThreadPoolExecutor
from scapy.all import ARP, Ether, srp, ls

# can be used if going to coffee shop or anything to scan surroundin 
class Simple_Host_Scanner():
    def __init__(self, network_range='192.168.1.0/24'):
        self.network_range = network_range
        self.devices = []

    def arp_scan(self):
        print(f"[!] Scanning {self.network_range}...")
        packet = Ether(dst = 'ff:ff:ff:ff:ff:ff') / ARP(pdst='192.168.1.1/24')
        answ, _ = srp(packet, timeout=2, verbose=0)
        self.devices = [{"ip": rcv.psrc, "mac": rcv.hwsrc} for snd, rcv in answ]
        print(f"[+] Found {len(self.devices)} devices.")

    def display_devices(self):
        for device in self.devices:
            print(f"{device['ip']}\t\t{device['mac']}")        


    def get_device_info_nmap(self, device):
        ip_address = device['ip']
        scanner = nmap.PortScanner()
        try:

            # -O: OS detection, -Pn: No ping, -F: Fast port scan, -n: No DNS, -T4: Faster timing
            scan_results = scanner.scan(ip_address, arguments='-O -Pn -F -n -T4')
            os_matches = scan_results['scan'][ip_address].get('osmatch', [])
            if os_matches:
                best_match = max(os_matches, key=lambda x: int(x['accuracy']))
                # print(best_match)
                print(f"{ip_address} - Best Match: {best_match['name']} ({best_match['accuracy']}%)")
            else:
                print("Host is up, but no OS fingerprinting matches were found.")

        except nmap.PortScannerError as e:
            print(f"Nmap Error: {e}.") 
        
    def scan_host_os_info(self, threads=10):
        print(f"[!] Starting OS Fingerprinting (Threads: {threads})")
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(self.get_device_info_nmap, self.devices)


scanner = Simple_Host_Scanner('192.168.1.0/24') # Change to your subnet
scanner.arp_scan()
scanner.scan_host_os_info()