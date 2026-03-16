import socket, time
from threading import Thread

# SOCK_STREAM -> TCP
# SOCK_DGRAM -> UDP

# NOTE: Note a stealth scanner; fully logged
def full_TCP_connect_scan(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(3)
        try:
            result = s.connect_ex((host, port))
            if result == 0: 
                print(f"[+] Port {port} is open")
                # NOTE: sending can probe a response 
                # FIXME: specific ports will have a specific probe 
                if port in [80, 445, 8080]:
                    s.send(b"GET / HTTP/1.1\r\n\r\n")
                    banner = s.recv(1024).decode(errors='ignore').strip()
                    print(f"[+][Banner]: {banner[:50]}")
        
        except TimeoutError as e:
            print(f"[-] Error: {e}")

        except socket.error as e:
            print(f"[-] Error: {e}")


common_ports = [20, 21, 22, 23, 25, 80, 111, 443, 445, 631, 993, 995, 135, 137, 138, 139, 548, 8080]
threads = []

start_time = time.time()
for port in range(1, 1025):
    t = Thread(target=full_TCP_connect_scan, args=("216.239.38.120", int(port)))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

end_time = time.time()
elapsed_time = end_time - start_time
print("\nScan complete.")
print(f"Elapsed time: {elapsed_time:.2f} seconds") # Format to 2 decimal places

# TODO: using scapy for Stealth (Half-Open) Scan 
# TODO: NMAP Scanner 
