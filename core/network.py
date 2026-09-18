import socket
import subprocess
import re

def get_local_ips():
    """
    Discovers all IPv4 addresses for local network adapters
    (Hotspot, Wi-Fi LAN, Ethernet, etc.) excluding localhost.
    """
    ips = []
    
    # 1. Primary route check via UDP dummy connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(('8.8.8.8', 80))
        primary_ip = s.getsockname()[0]
        s.close()
        if primary_ip and not primary_ip.startswith('127.') and primary_ip not in ips:
            ips.append(primary_ip)
    except Exception:
        pass

    # 2. Query hostname interfaces
    try:
        hostname = socket.gethostname()
        for ip in socket.gethostbyname_ex(hostname)[2]:
            if ip and not ip.startswith('127.') and ip not in ips:
                ips.append(ip)
    except Exception:
        pass

    # 3. Windows Mobile Hotspot adapter check (default is typically 192.168.137.1)
    if '192.168.137.1' not in ips:
        try:
            # Check if ipconfig shows 192.168.137.1
            output = subprocess.check_output('ipconfig', shell=True, text=True, timeout=2)
            for line in output.splitlines():
                if 'IPv4 Address' in line or 'IPv4-Adresse' in line or 'Dirección IPv4' in line:
                    match = re.search(r'(\d+\.\d+\.\d+\.\d+)', line)
                    if match:
                        found_ip = match.group(1)
                        if found_ip not in ips and not found_ip.startswith('127.'):
                            ips.append(found_ip)
        except Exception:
            pass

    if not ips:
        ips.append('127.0.0.1')
        
    return ips
