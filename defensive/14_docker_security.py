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

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Docker Security Auditor')
    args = parser.parse_args()

    auditor = DockerAuditor()
    auditor.audit_all()

if __name__ == "__main__":
    main()
