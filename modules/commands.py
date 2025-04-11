import subprocess
import platform
import socket

def run_command(cmd):
    try:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT)
        return output.decode()
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def get_info():
    info = {
        "hostname": socket.gethostname(),
        "ip": socket.gethostbyname(socket.gethostname()),
        "platform": platform.system(),
        "release": platform.release(),
        "user": platform.node()
    }
    return "\n".join(f"{k}: {v}" for k, v in info.items())
