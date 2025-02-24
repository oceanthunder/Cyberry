import subprocess
import psutil
import datetime

def get_system_info():
    """Fetches system information with cybersecurity metrics"""
    info = {}
    
    try:
        # Basic System Metrics
        info["cpu_temp"] = subprocess.getoutput("vcgencmd measure_temp | cut -d '=' -f 2")
        info["cpu_usage"] = f"{psutil.cpu_percent(interval=1)}%"
        info["load_avg"] = subprocess.getoutput("cat /proc/loadavg | awk '{print $1, $2, $3}'")
        
        # Memory Metrics
        memory = psutil.virtual_memory()
        info["memory_usage"] = (f"{memory.used / (1024 ** 2):.2f} MB / "
                                f"{memory.total / (1024 ** 2):.2f} MB ({memory.percent}%)")

        # Storage Security
        disk = psutil.disk_usage('/')
        info["disk_usage"] = (f"{disk.used / (1024 ** 3):.2f} GB / "
                             f"{disk.total / (1024 ** 3):.2f} GB ({disk.percent}%)")

        # Network Security Metrics
        net = psutil.net_io_counters()
        info["network_sent"] = f"{net.bytes_sent / (1024 ** 2):.2f} MB"
        info["network_recv"] = f"{net.bytes_recv / (1024 ** 2):.2f} MB"
        
        # Cybersecurity-specific metrics
        info["open_ports"] = subprocess.getoutput("ss -tuln | awk 'NR>1 {print $5}' | cut -d':' -f2 | sort -u")
        info["failed_logins"] = subprocess.getoutput("grep 'Failed password' /var/log/auth.log | wc -l") + " attempts"
        info["ssh_logins"] = subprocess.getoutput("who | awk '{print $1,$5}' | sort -u")
        info["rootkit_check"] = subprocess.getoutput("rkhunter --quick --nocolors 2>/dev/null | grep -i 'warning\|infected'") or "No suspicious files found"
        info["sudo_attempts"] = subprocess.getoutput("grep 'sudo:' /var/log/auth.log | wc -l") + " commands"
        info["firewall_status"] = subprocess.getoutput("sudo ufw status | grep -i active")
        info["usb_devices"] = subprocess.getoutput("lsusb | awk '{print $7,$8,$9}'")

        # System Uptime
        info["uptime"] = subprocess.getoutput("uptime -p")
        info["last_security_update"] = subprocess.getoutput("stat -c %y /var/log/apt/history.log | cut -d' ' -f1")

    except Exception as e:
        info["error"] = f"Monitoring error: {str(e)}"

    return info
