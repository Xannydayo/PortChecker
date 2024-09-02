import socket
import itertools
import threading
import time
from urllib.parse import urlparse
from tqdm import tqdm

def get_ip_and_ports(url):
    try:
        parsed_url = urlparse(url)
        hostname = parsed_url.hostname
        if not hostname:
            raise ValueError("Invalid URL. Please enter a valid URL.")
        
        ip_address = socket.gethostbyname(hostname)
        print(f"IP Address: {ip_address}")
        
        print("Scanning ports may take some time. Please wait...")
        
        def loading_animation():
            for c in itertools.cycle(['|', '/', '-', '\\']):
                if done:
                    break
                print(f'\rScanning ports {c}', end='', flush=True)
                time.sleep(0.1)
            print('\rScanning ports... Done!', flush=True)
        
        done = False
        t = threading.Thread(target=loading_animation)
        t.start()
        
        try:
            open_ports = []
            for port in tqdm(range(1, 1025), desc="Scanning ports", unit="port"):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)  # Reduce timeout to make scanning faster
                result = sock.connect_ex((ip_address, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
        except KeyboardInterrupt:
            done = True  # Stop the loading animation
            print("\nScanning interrupted.")
        finally:
            done = True  # Ensure the loading animation stops
            t.join()  # Wait for the thread to finish
        
        if open_ports:
            for port in open_ports:
                print(f"Port {port}: Open")
        else:
            print("No open ports found.")
    except (socket.gaierror, ValueError) as e:
        print(e)

if __name__ == "__main__":
    try:
        url = input("Enter URL: ")
        get_ip_and_ports(url)
    except EOFError:
        print("Error: No input provided. Please enter a valid URL.")
    print("\nCreated by Xannydayo")
