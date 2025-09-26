import socket
import re
import time
from common_ports import ports

class SecurePortScanner:
    def __init__(self, max_ports=50, delay=0.1, timeout=1.0):
        """
        Initialize scanner with security limits
        max_ports: Maximum number of ports to scan in one request
        delay: Delay between port scans (seconds)
        timeout: Socket timeout (seconds)
        """
        self.max_ports = max_ports
        self.delay = delay
        self.timeout = timeout
        
        # Whitelist of allowed targets for public deployment
        self.allowed_targets = [
            'scanme.nmap.org',
            'testphp.vulnweb.com',
            # Add more test targets as needed
        ]
    
    def is_allowed_target(self, target):
        """Check if target is in whitelist"""
        return target in self.allowed_targets
    
    def get_open_ports(self, target, port_range, verbose=False):
        """
        Secure version of port scanner with rate limiting and restrictions
        """
        # Security check for public deployment
        if not self.is_allowed_target(target):
            return "Error: Target not in allowed list for public scanning"
        
        # Limit port range size
        start_port, end_port = port_range
        if end_port - start_port + 1 > self.max_ports:
            return f"Error: Port range too large. Maximum {self.max_ports} ports allowed"
        
        # Validate port range
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            return "Error: Invalid port range"
        
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
        
        # Scan ports with rate limiting
        for port in range(start_port, end_port + 1):
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(self.timeout)
            try:
                result = s.connect_ex((ip, port))
                if result == 0:
                    open_ports.append(port)
            except Exception:
                pass
            finally:
                s.close()
            
            # Rate limiting delay
            time.sleep(self.delay)
        
        if not verbose:
            return open_ports
        
        # Verbose output
        output = f"Open ports for {url} ({ip})\nPORT     SERVICE\n"
        for port in open_ports:
            service = ports.get(port, "unknown")
            output += f"{str(port).ljust(8)}{service}\n"
        
        return output.strip()

# Wrapper function to maintain compatibility
def get_open_ports(target, port_range, verbose=False):
    """Public interface with security restrictions"""
    scanner = SecurePortScanner()
    return scanner.get_open_ports(target, port_range, verbose)