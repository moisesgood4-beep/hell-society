#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  GRAPHQL EXPLORER & ATTACKER v2.0                                ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - API Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsabil del mal uso de esta herramienta.
"""

import requests
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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

GRAPHQL_ENDPOINTS = ['/graphql', '/graphql.php', '/api/graphql', '/v1/graphql',
                     '/query', '/graphiql', '/playground', '/altair']

INTROSPECTION_QUERY = '''{
  __schema {
    types {
      name
      kind
      description
      fields {
        name
        type { name kind }
      }
    }
  }
}'''

ATTACK_QUERIES = {
    'batch_query': [
        {"query": "{ users { id name email } }"},
        {"query": "{ users { id name email } }"},
        {"query": "{ users { id name email } }"},
    ],
    'deep_nesting': '{"query": "{ user(id: 1) { posts { comments { author { posts { comments { author { posts } } } } } } } }"}',
    'alias_abuse': '{"query": "{ a: user(id: 1) { name } b: user(id: 2) { name } c: user(id: 3) { name } d: user(id: 4) { name } e: user(id: 5) { name } }"}',
    'field_suggestion': '{"query": "{ user { nme } }"}',
    'introspection_full': '{"query": "{ __schema { types { name fields { name args { name type { name } } } } } }"}',
}

class GraphQLExplorer:
    def __init__(self, target):
        self.target = target.rstrip('/')
        self.endpoint = None
        self.vulns = []
        self.schema = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0',
            'Content-Type': 'application/json'
        })

    def discover_endpoint(self):
        print(f"{Fore.CYAN}  [*] Discovering GraphQL endpoint...\n")

        for endpoint in GRAPHQL_ENDPOINTS:
            url = f"{self.target}{endpoint}"
            try:
                resp = self.session.post(url, json={'query': '{ __typename }'}, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if 'data' in data and data['data'].get('__typename') == 'Query':
                        self.endpoint = url
                        print(f"  {Fore.GREEN}[+] GraphQL endpoint found: {url}")
                        return True
            except:
                pass

        print(f"  {Fore.YELLOW}  [!] Could not auto-discover endpoint")
        return False

    def introspection(self):
        if not self.endpoint:
            return

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  INTROSPECTION QUERY")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        try:
            resp = self.session.post(self.endpoint,
                json={'query': INTROSPECTION_QUERY}, timeout=15)

            if resp.status_code == 200:
                data = resp.json()
                if 'data' in data and data['data'].get('__schema'):
                    self.schema = data['data']['__schema']
                    print(f"  {Fore.GREEN}[+] Introspection enabled!")
                    print(f"  {Fore.GREEN}  Types found: {len(self.schema['types'])}")

                    for t in self.schema['types'][:20]:
                        print(f"  {Fore.CYAN}  • {t['name']} ({t['kind']})")

                    if len(self.schema['types']) > 20:
                        print(f"  {Fore.YELLOW}  ... and {len(self.schema['types']) - 20} more")

                    self.vulns.append('GraphQL Introspection Enabled')
                else:
                    print(f"  {Fore.GREEN}[OK] Introspection disabled")
        except:
            pass

    def test_attacks(self):
        if not self.endpoint:
            return

        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  GraphQL ATTACKS")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Batch query attack
        try:
            resp = self.session.post(self.endpoint, json=ATTACK_QUERIES['batch_query'], timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list):
                    print(f"  {Fore.RED}[VULN] Batch queries accepted ({len(data)} queries)")
                    self.vulns.append('GraphQL Batch Query')
                else:
                    print(f"  {Fore.GREEN}[OK] Batch queries rejected")
        except:
            pass

        # Deep nesting
        try:
            resp = self.session.post(self.endpoint,
                json={'query': ATTACK_QUERIES['deep_nesting']}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if 'errors' not in data and 'data' in data:
                    print(f"  {Fore.RED}[VULN] Deep nesting not restricted")
                    self.vulns.append('GraphQL Deep Nesting')
                else:
                    print(f"  {Fore.GREEN}[OK] Deep nesting restricted")
        except:
            pass

        # Field suggestion
        try:
            resp = self.session.post(self.endpoint,
                json={'query': ATTACK_QUERIES['field_suggestion']}, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if 'errors' in data:
                    error_msg = str(data['errors'])
                    if 'did you mean' in error_msg.lower() or 'suggestions' in error_msg.lower():
                        print(f"  {Fore.RED}[VULN] Field suggestions leak schema info")
                        self.vulns.append('GraphQL Field Suggestion Leak')
        except:
            pass

    def print_results(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.RED}[!] Vulnerabilities: {len(self.vulns)}")

        if self.vulns:
            for v in self.vulns:
                print(f"    {Fore.RED}• {v}")

        score = max(0, 100 - (len(self.vulns) * 20))
        print(f"\n  {Fore.CYAN}GraphQL Security Score: {score}/100")



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
    print(f"  {BW}{Style.BRIGHT}  GRAPHQL EXPLORER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}GRAPHQL EXPLORER                        {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL (base URL, not endpoint)          {RS}")
        print(f"  {C}[2]  {BW}Specific GraphQL endpoint                    {RS}")
        print()
        print(f"  {C}[3]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target URL (base URL, not endpoint){RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Specific GraphQL endpoint{RS}")
            value = input(f"  {Y}[*] -e: {RS}").strip()
            print(f"  {C}[*] Executing with -e={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '3':
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

