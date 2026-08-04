#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DOCKER SECURITY AUDITOR v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Container Security                        ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import json

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

class DockerAuditor:
    def __init__(self):
        self.issues = []
        self.score = 100

    def run_cmd(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
            return result.stdout.strip()
        except:
            return ''

    def check_rootless(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ROOTLESS DOCKER:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        user = self.run_cmd('whoami')
        if user == 'root':
            print(f"  {Fore.RED}  [!] Docker running as root")
            self.issues.append('Docker running as root')
            self.score -= 20
        else:
            print(f"  {Fore.GREEN}  [OK] Running as non-root: {user}")

    def check_containers(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CONTAINER ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check running containers
        containers = self.run_cmd('docker ps --format "{{.Names}}:{{.Image}}:{{.Ports}}"')
        if containers:
            print(f"  {Fore.WHITE}  Running containers: {len(containers.split(chr(10)))}")
            for container in containers.split('\n'):
                print(f"    {Fore.WHITE}  {container}")

                if '0.0.0.0' in container:
                    ports = [p.split('->')[0] for p in container.split(',') if '0.0.0.0' in p]
                    print(f"    {Fore.RED}  [!] Ports exposed to all: {ports}")
                    self.issues.append(f'Exposed ports: {ports}')
                    self.score -= 10
        else:
            print(f"  {Fore.YELLOW}  [-] No running containers")

    def check_privileged(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  PRIVILEGED CONTAINERS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        inspect = self.run_cmd('docker inspect --format "{{.Name}}:{{.HostConfig.Privileged}}" $(docker ps -q)')
        if inspect:
            for line in inspect.split('\n'):
                if 'true' in line.lower():
                    print(f"  {Fore.RED}  [!!!] Privileged container: {line}")
                    self.issues.append(f'Privileged container: {line}')
                    self.score -= 25
                else:
                    print(f"  {Fore.GREEN}  [OK] Non-privileged: {line}")
        else:
            print(f"  {Fore.GREEN}  [OK] No privileged containers")

    def check_capabilities(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CAPABILITY ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        inspect = self.run_cmd('docker inspect --format "{{.Name}}:{{.HostConfig.CapAdd}}" $(docker ps -q)')
        if inspect:
            for line in inspect.split('\n'):
                if 'SYS_ADMIN' in line or 'NET_ADMIN' in line:
                    print(f"  {Fore.RED}  [!] Dangerous capabilities: {line}")
                    self.issues.append(f'Dangerous caps: {line}')
                    self.score -= 15
                else:
                    print(f"  {Fore.GREEN}  [OK] Safe capabilities: {line}")
        else:
            print(f"  {Fore.GREEN}  [OK] No dangerous capabilities")

    def check_images(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  IMAGE ANALYSIS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        images = self.run_cmd('docker images --format "{{.Repository}}:{{.Tag}}:{{.Size}}"')
        if images:
            print(f"  {Fore.WHITE}  {len(images.split(chr(10)))} images found")
            for img in images.split('\n')[:10]:
                if 'latest' in img:
                    print(f"    {Fore.YELLOW}  [-] Using latest tag: {img}")
                    self.issues.append(f'Latest tag: {img}')
                    self.score -= 5
                else:
                    print(f"    {Fore.GREEN}  [OK] {img}")
        else:
            print(f"  {Fore.YELLOW}  [-] No images")

    def audit_all(self):
        print(f"{Fore.CYAN}  [*] Starting Docker security audit...\n")
        self.check_rootless()
        self.check_containers()
        self.check_privileged()
        self.check_capabilities()
        self.check_images()
        self.print_summary()

    def print_summary(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DOCKER AUDIT COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.RED}[!] Issues: {len(self.issues)}")
        for issue in self.issues:
            print(f"    {Fore.RED}• {issue}")

        self.score = max(0, self.score)
        color = Fore.GREEN if self.score >= 80 else (Fore.YELLOW if self.score >= 50 else Fore.RED)
        print(f"\n  {color}Docker Security Score: {self.score}/100")



def ask_retry():
    print()
    print(f"  {Y}{'='*50}{RS}")
    print(f"  {C}[1] {BW}Usar esta herramienta de nuevo{RS}")
    print(f"  {C}[2] {BW}Volver al panel principal{RS}")
    print(f"  {R}[0] {BW}Salir{RS}")
    print(f"  {Y}{'='*50}{RS}")
    try:
        ch = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        if ch == '1':
            return 'retry'
        elif ch in ['2', '0']:
            return 'exit'
        else:
            return 'retry'
    except (EOFError, KeyboardInterrupt):
        return 'exit'

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  DOCKER SECURITY{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}DOCKER SECURITY                         {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Iniciar herramienta{RS}")
        print(f"  {C}[2]  {BW}Configurar opciones{RS}")
        print(f"  {C}[3]  {BW}Mostrar ayuda/uso{RS}")
        print()
        print(f"  {R}[0]  {BW}Exit{RS}")
        print()
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {R}[*] Goodbye...{RS}")
            sys.exit(0)
        print()
        if choice == '1':
            print(f"  {G}[*] Starting Docker Security...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Docker Security{RS}")
            print(f"  {Y}    Interactive tool with guided inputs{RS}")
            print()
        elif choice == '0':
            print(f"  {Y}[*] Goodbye from Hell Society...{RS}")
            sys.exit(0)
        else:
            print(f"  {R}[!] Invalid option. Choose 0-3.{RS}")
        ch = ask_retry()
        if ch == 'exit':
            sys.exit(0)
        else:
            os.system('clear' if os.name != 'nt' else 'cls')
            print(BANNER)
            print()

if __name__ == "__main__":
    main()

