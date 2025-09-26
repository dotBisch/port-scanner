import socket
import re
from common_ports import ports

def get_open_ports(target, port_range, verbose=False):
    open_ports = []
    ip = None
    url = None
    # Validate target
    try:
        # Check if it's an IP address
        socket.inet_aton(target)
        ip = target
        try:
            url = socket.gethostbyaddr(ip)[0]
        except Exception:
            url = ip
    except socket.error:
        # Try to resolve as hostname
        try:
            ip = socket.gethostbyname(target)
            url = target
        except socket.gaierror:
            # Invalid hostname
            if re.match(r"^\d+\.\d+\.\d+\.\d+$", target):
                return "Error: Invalid IP address"
            else:
                return "Error: Invalid hostname"
    start_port, end_port = port_range
    for port in range(start_port, end_port + 1):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)
        try:
            result = s.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
        except Exception:
            pass
        finally:
            s.close()
    if not verbose:
        return open_ports
    # Verbose output
    output = f"Open ports for {url} ({ip})\nPORT     SERVICE\n"
    for port in open_ports:
        service = ports.get(port, "unknown")
        output += f"{str(port).ljust(8)}{service}\n"
    return output.strip()
