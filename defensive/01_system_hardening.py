#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  LINUX SYSTEM HARDENING v2.0                                     ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - System Security                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import subprocess
import os
import sys
import colorama
from colorama import Fore, Back, Style
import argparse

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

class SystemHardener:
    def __init__(self):
        self.applied = 0
        self.failed = 0
        self.skipped = 0

    def run_cmd(self, cmd, description):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                self.applied += 1
                print(f"  {Fore.GREEN}[OK] {Fore.WHITE}{description}")
                return True
            else:
                self.failed += 1
                print(f"  {Fore.RED}[FAIL] {Fore.WHITE}{description}")
                print(f"  {Fore.YELLOW}  {result.stderr.strip()[:100]}")
                return False
        except subprocess.TimeoutExpired:
            self.failed += 1
            print(f"  {Fore.RED}[TIMEOUT] {description}")
            return False
        except Exception as e:
            self.skipped += 1
            print(f"  {Fore.YELLOW}[SKIP] {Fore.WHITE}{description} - {str(e)[:50]}")
            return False

    def harden_ssh(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}SSH HARDENING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        ssh_config = "/etc/ssh/sshd_config"
        if not os.path.exists(ssh_config):
            print(f"  {Fore.YELLOW}[SKIP] sshd_config not found")
            return

        # Backup
        self.run_cmd(f"cp {ssh_config} {ssh_config}.bak.$(date +%Y%m%d)", "Backup SSH config")

        # Harden SSH
        hardening_rules = [
            (f"sed -i 's/^#*PermitRootLogin.*/PermitRootLogin no/' {ssh_config}", "Disable root login"),
            (f"sed -i 's/^#*PasswordAuthentication.*/PasswordAuthentication no/' {ssh_config}", "Disable password auth"),
            (f"sed -i 's/^#*PubkeyAuthentication.*/PubkeyAuthentication yes/' {ssh_config}", "Enable key auth"),
            (f"sed -i 's/^#*PermitEmptyPasswords.*/PermitEmptyPasswords no/' {ssh_config}", "Disable empty passwords"),
            (f"sed -i 's/^#*X11Forwarding.*/X11Forwarding no/' {ssh_config}", "Disable X11 forwarding"),
            (f"sed -i 's/^#*MaxAuthTries.*/MaxAuthTries 3/' {ssh_config}", "Limit auth attempts"),
            (f"sed -i 's/^#*LoginGraceTime.*/LoginGraceTime 60/' {ssh_config}", "Set login grace time"),
            (f"sed -i 's/^#*ClientAliveInterval.*/ClientAliveInterval 300/' {ssh_config}", "Set alive interval"),
            (f"sed -i 's/^#*ClientAliveCountMax.*/ClientAliveCountMax 2/' {ssh_config}", "Set alive count max"),
            (f"sed -i 's/^#*UsePAM.*/UsePAM yes/' {ssh_config}", "Enable PAM"),
            (f"sed -i 's/^#*Protocol.*/Protocol 2/' {ssh_config}", "Force SSHv2"),
        ]

        for cmd, desc in hardening_rules:
            self.run_cmd(cmd, desc)

    def harden_firewall(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}FIREWALL HARDENING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        rules = [
            ("ufw enable", "Enable UFW"),
            ("ufw default deny incoming", "Default deny incoming"),
            ("ufw default allow outgoing", "Default allow outgoing"),
            ("ufw allow 22/tcp", "Allow SSH"),
            ("ufw allow 80/tcp", "Allow HTTP"),
            ("ufw allow 443/tcp", "Allow HTTPS"),
            ("ufw logging on", "Enable logging"),
        ]

        for cmd, desc in rules:
            self.run_cmd(cmd, desc)

    def harden_permissions(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}FILE PERMISSIONS HARDENING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        rules = [
            ("chmod 700 /tmp", "Secure /tmp"),
            ("chmod 1777 /tmp", "Sticky bit /tmp"),
            ("chmod 644 /etc/passwd", "Secure passwd"),
            ("chmod 644 /etc/group", "Secure group"),
            ("chmod 600 /etc/shadow", "Secure shadow"),
            ("chmod 600 /etc/gshadow", "Secure gshadow"),
            ("chmod 600 /etc/ssh/sshd_config", "Secure SSH config"),
        ]

        for cmd, desc in rules:
            self.run_cmd(cmd, desc)

    def harden_sysctl(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}KERNEL HARDENING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        sysctl_file = "/etc/sysctl.d/99-hellsociety-hardening.conf"

        sysctl_rules = """
# Network hardening
net.ipv4.ip_forward = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.all.accept_source_route = 0
net.ipv4.conf.all.log_martians = 1
net.ipv4.tcp_syncookies = 1
net.ipv4.conf.all.rp_filter = 1
net.ipv6.conf.all.accept_ra = 0
net.ipv6.conf.all.accept_redirects = 0

# Kernel hardening
kernel.randomize_va_space = 2
kernel.dmesg_restrict = 1
kernel.perf_event_paranoid = 3
fs.suid_dumpable = 0
"""

        self.run_cmd(f"echo '{sysctl_rules}' > {sysctl_file}", "Create sysctl hardening")
        self.run_cmd(f"sysctl -p {sysctl_file}", "Apply sysctl rules")

    def harden_accounts(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}ACCOUNT HARDENING")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        rules = [
            ("chage -M 90 root", "Force password change 90 days"),
            ("chage -m 7 root", "Min days between changes: 7"),
            ("chage -W 14 root", "Warning 14 days before expiry"),
        ]

        for cmd, desc in rules:
            self.run_cmd(cmd, desc)

    def audit(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}SECURITY AUDIT")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check SUID files
        self.run_cmd("find / -perm -4000 -type f 2>/dev/null | head -20", "List SUID files")

        # Check world-writable
        self.run_cmd("find / -perm -o+w -type f 2>/dev/null | head -20", "List world-writable files")

        # Check listening ports
        self.run_cmd("ss -tlnp 2>/dev/null | head -20", "List listening ports")

    def apply_all(self):
        print(f"{Fore.CYAN}  [*] Starting system hardening...\n")
        print(f"{Fore.CYAN}  [!] Requires ROOT privileges\n")

        self.harden_ssh()
        self.harden_firewall()
        self.harden_permissions()
        self.harden_sysctl()
        self.harden_accounts()
        self.audit()

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  HARDENING COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.GREEN}[OK] Applied: {self.applied}")
        print(f"  {Fore.RED}[FAIL] Failed: {self.failed}")
        print(f"  {Fore.YELLOW}[SKIP] Skipped: {self.skipped}")
        print(f"\n  {Fore.CYAN}System Security Score: {min(100, self.applied * 3)}/100")

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society System Hardening')
    parser.add_argument('--apply', action='store_true', help='Apply hardening')
    parser.add_argument('--audit', action='store_true', help='Only audit')
    args = parser.parse_args()

    hardener = SystemHardener()

    if args.apply:
        hardener.apply_all()
    elif args.audit:
        hardener.audit()
    else:
        print(f"  {Fore.CYAN}  Usage: sudo python3 01_system_hardening.py --apply")
        print(f"  {Fore.CYAN}  Usage: python3 01_system_hardening.py --audit")

if __name__ == "__main__":
    main()
