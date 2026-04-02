import socket
import threading
from queue import Queue

# Common ports with service names
common_ports = {
    21: "FTP",
    22: "SSH",
    23: "TELNET",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-ALT"
}

# Get target
target = input("Enter target IP or domain: ")
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid target")
    exit()

print(f"\nScanning target: {target} ({target_ip})\n")

# Queue for ports
queue = Queue()
open_ports = []

# Function to scan a port
def scan_port(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(0.5)
    result = s.connect_ex((target_ip, port))
    if result == 0:
        service = common_ports.get(port, "Unknown")
        print(f"[+] Port {port} ({service}) is OPEN")
        open_ports.append(port)
    s.close()

# Thread worker
def worker():
    while not queue.empty():
        port = queue.get()
        scan_port(port)
        queue.task_done()

# Fill queue with ports
for port in range(1, 1025):
    queue.put(port)

# Create threads
thread_count = 50
for _ in range(thread_count):
    t = threading.Thread(target=worker)
    t.start()

# Wait for completion
queue.join()

# Final output
print("\nScan Completed!")
print(f"Open Ports: {open_ports}")
