import argparse
import socket
import threading


class StorePortScanner:

    def __init__(self, public_ip):
        self.public_ip = public_ip
        # lock thread during print so we get cleaner outputs
        self.print_lock = threading.Lock()
        self.open_ports = []

    def scan_port(self, port):
        try:
            sock = None
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((self.public_ip, int(port)))
            self.open_ports.append(port)
        except socket.error as e:
            Exception(str(e))

    def run_port_scan(self, ports_to_scan):
        try:
            thread_list = []
            port_list = ports_to_scan.split(",")

            for port_to_scan in port_list:
                thread_list.append(threading.Thread(target=self.scan_port, args=(port_to_scan,)))

            for thread in thread_list:
                thread.start()

            for thread in thread_list:
                thread.join()

        except Exception as e:
            Exception(str(e))

        return self.open_ports

parser = argparse.ArgumentParser(description='IPv4 socket TCP port scanner')
parser.add_argument("--i", default=None, help="Public IPv4 address.")
parser.add_argument("--p", default=None, help="Ports to scan. Please provide as comma separated values.")

args = parser.parse_args()
ip_address = args.i
ports_to_scan = args.p
try:
    if not ip_address:
        raise Exception('Please provide an valid IPv4 address.')
    if not ports_to_scan:
        raise Exception('Please provide ports as comma separated values.')     
    scanner = StorePortScanner(public_ip=str(ip_address))
    open_ports = scanner.run_port_scan(ports_to_scan=ports_to_scan)
    print('Open ports for ip address {}: {}'.format(ip_address, open_ports))
except Exception as e:
    print('The following error occured: {}'.format(str(e)))