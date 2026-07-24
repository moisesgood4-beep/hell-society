#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Domain WHOIS Deep Recon                        ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, socket, subprocess, requests
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

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

class WHOISRecon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}

    def whois_lookup(self):
        print(f"\n{G}[+] Method 1: WHOIS Lookup{RS}")
        try:
            result = subprocess.run(['whois', self.domain], capture_output=True, text=True, timeout=15)
            if result.stdout:
                whois_data = result.stdout
                # Extract key fields
                patterns = {
                    'registrar': r'Registrar:\s*(.+)',
                    'creation': r'Creation Date:\s*(.+)',
                    'expiry': r'Expiry Date:\s*(.+)',
                    'name_servers': r'Name Server:\s*(.+)',
                    'registrant_name': r'Registrant Name:\s*(.+)',
                    'registrant_email': r'Registrant Email:\s*(.+)',
                    'registrant_phone': r'Registrant Phone:\s*(.+)',
                    'admin_email': r'Admin Email:\s*(.+)',
                    'tech_email': r'Tech Email:\s*(.+)',
                }
                extracted = {}
                for key, pattern in patterns.items():
                    match = re.search(pattern, whois_data, re.IGNORECASE)
                    if match:
                        extracted[key] = match.group(1).strip()
                        print(f"  {C}[{key}] {W}{extracted[key]}")
                self.results['whois'] = extracted
            else:
                print(f"  {R}[!] No WHOIS data returned")
        except FileNotFoundError:
            print(f"  {R}[!] whois not installed. Run: apt install whois")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def dns_records(self):
        print(f"\n{G}[+] Method 2: DNS Records{RS}")
        records = ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA']
        for rec_type in records:
            try:
                result = subprocess.run(['dig', '+short', self.domain, rec_type],
                                       capture_output=True, text=True, timeout=10)
                if result.stdout.strip():
                    values = result.stdout.strip().split('\n')
                    print(f"  {C}[{rec_type}] {W}{', '.join(values[:5])}")
                    self.results[f'dns_{rec_type}'] = values
                else:
                    print(f"  {Y}[{rec_type}] No records")
            except FileNotFoundError:
                print(f"  {R}[!] dig not installed")
                break
            except Exception as e:
                print(f"  {R}[!] Error: {e}")

    def subdomain_brute(self):
        print(f"\n{G}[+] Method 3: Subdomain Discovery{RS}")
        subs = ['www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
                'blog', 'shop', 'app', 'db', 'vpn', 'portal', 'login', 'panel']
        found = []
        for sub in subs:
            full = f"{sub}.{self.domain}"
            try:
                ip = socket.gethostbyname(full)
                found.append({'sub': full, 'ip': ip})
                print(f"  {G}[✓] {full} → {ip}")
            except:
                print(f"  {R}[✗] {full}")
        self.results['subdomains'] = found

    def ssl_certificate(self):
        print(f"\n{G}[+] Method 4: SSL Certificate Info{RS}")
        try:
            result = subprocess.run(
                ['openssl', 's_client', '-connect', f'{self.domain}:443', '-servername', self.domain],
                capture_output=True, text=True, timeout=10,
                input='\n'
            )
            cert = result.stdout
            # Extract key info
            subject = re.search(r'subject:?\s*(.+)', cert)
            issuer = re.search(r'issuer:?\s*(.+)', cert)
            dates = re.findall(r'not(Before|After)=(.+)', cert)

            if subject:
                print(f"  {C}[Subject] {W}{subject.group(1).strip()}")
            if issuer:
                print(f"  {C}[Issuer] {W}{issuer.group(1).strip()}")
            for d_type, d_val in dates:
                print(f"  {C}[{d_type}] {W}{d_val.strip()}")

            self.results['ssl'] = {'subject': subject.group(1) if subject else None, 'issuer': issuer.group(1) if issuer else None}
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def http_headers(self):
        print(f"\n{G}[+] Method 5: HTTP Headers{RS}")
        for proto in ['https', 'http']:
            try:
                r = requests.head(f"{proto}://{self.domain}", timeout=10, allow_redirects=True, verify=False)
                print(f"\n  {Y}--- {proto.upper()} ---")
                for header, value in r.headers.items():
                    print(f"  {C}  {header}: {W}{value}")
                self.results['headers'] = dict(r.headers)
                break
            except:
                continue

    def save_results(self):
        outfile = f"whois_recon_{self.domain}.json"
        with open(outfile, 'w') as f:
            json.dump({'domain': self.domain, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Domain: {W}{self.domain}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.whois_lookup()
        self.dns_records()
        self.subdomain_brute()
        self.ssl_certificate()
        self.http_headers()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - WHOIS Deep Recon Complete     ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()
    recon = WHOISRecon(args.domain)
    recon.run_all()

if __name__ == "__main__":
    main()
