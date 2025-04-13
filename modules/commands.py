import subprocess

def run_command(cmd):
    try:
        output = subprocess.check_output(
            cmd, shell=True, stderr=subprocess.STDOUT, text=True, timeout=15
        )
        return output
    except subprocess.CalledProcessError as e:
        return e.output
    except Exception as ex:
        return f"[!] Unexpected error: {str(ex)}"

def get_info():
    import platform, socket, getpass
    try:
        return (
            f"User: {getpass.getuser()}\n"
            f"Hostname: {socket.gethostname()}\n"
            f"IP: {socket.gethostbyname(socket.gethostname())}\n"
            f"OS: {platform.system()} {platform.release()}\n"
            f"Platform: {platform.platform()}"
        )
    except Exception as e:
        return f"[!] Failed to gather info: {e}"
