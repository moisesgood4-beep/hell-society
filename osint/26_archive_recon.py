#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Web Archive Recon & Deleted Content Recovery   ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests
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

class ArchiveRecon:
    def __init__(self, domain):
        self.domain = domain
        self.results = {}

    def wayback_machine(self):
        print(f"\n{G}[+] Method 1: Wayback Machine{RS}")
        try:
            url = f"https://web.archive.org/cdx/search/cdx?url=*.{self.domain}&output=json&limit=100"
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and r.json():
                data = r.json()
                headers = data[0]
                entries = data[1:]
                print(f"  {G}[✓] {len(entries)} archived URLs found")
                for entry in entries[:30]:
                    print(f"  {C}  {entry[headers.index('url')]} ({entry[headers.index('timestamp')][:8]})")
                self.results['wayback'] = entries[:100]
            else:
                print(f"  {Y}[!] No archives found or API unavailable")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def google_cache(self):
        print(f"\n{G}[+] Method 2: Google Cache Search{RS}")
        print(f"  {Y}[i] cache:{self.domain}")
        print(f"  {Y}[i] site:{self.domain} -inurl:login")
        print(f"  {Y}[i] site:{self.domain} inurl:admin")
        print(f"  {Y}[i] site:{self.domain} filetype:pdf")
        print(f"  {Y}[i] site:{self.domain} filetype:xls")
        self.results['cache_queries'] = [f"site:{self.domain}"]

    def archive_today(self):
        print(f"\n{G}[+] Method 3: Archive.today{RS}")
        print(f"  {Y}[i] https://archive.org/wayback/available?url={self.domain}")
        try:
            r = requests.get(f"https://archive.org/wayback/available?url={self.domain}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                if 'archived_snapshots' in data and data['archived_snapshots']:
                    closest = data['archived_snapshots'].get('closest', {})
                    print(f"  {G}[✓] Latest snapshot: {closest.get('url', 'N/A')}")
                    self.results['archive_today'] = closest
                else:
                    print(f"  {Y}[!] No recent snapshots")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def recover_deleted(self):
        print(f"\n{G}[+] Method 4: Deleted Content Recovery{RS}")
        # Search for deleted pages
        print(f"  {Y}[i] Search Wayback Machine for deleted pages:")
        print(f"  {Y}[i] https://web.archive.org/web/*/http://{self.domain}/*")
        print(f"\n  {Y}[i] Check for removed directories:")
        paths = ['/admin', '/backup', '/config', '/.env', '/wp-config.php',
                 '/phpmyadmin', '/.git/config', '/api/v1', '/graphql', '/.htaccess']
        for p in paths:
            wb_url = f"https://web.archive.org/web/*/http://{self.domain}{p}"
            print(f"  {C}  {wb_url[:60]}")
        self.results['deleted_check'] = paths

    def extract_emails(self):
        print(f"\n{G}[+] Method 5: Extract Emails from Archives{RS}")
        try:
            url = f"https://web.archive.org/cdx/search/cdx?url=www.{self.domain}/*&output=text&fl=original&limit=50"
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and r.text.strip():
                urls = r.text.strip().split('\n')
                print(f"  {G}[✓] {len(urls)} archived URLs to scan")
                # Search each for emails
                emails = set()
                for archived_url in urls[:20]:
                    try:
                        wb = f"https://web.archive.org/web/2024/{archived_url}"
                        resp = requests.get(wb, timeout=10)
                        if resp.status_code == 200:
                            found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', resp.text)
                            for e in found:
                                if self.domain.split('.')[-2] in e:
                                    emails.add(e)
                    except:
                        pass
                if emails:
                    print(f"  {G}[✓] Emails found: {emails}")
                    self.results['emails'] = list(emails)
                else:
                    print(f"  {Y}[!] No emails found in archives")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def technology_detection(self):
        print(f"\n{G}[+] Method 6: Historical Technology Detection{RS}")
        try:
            url = f"https://web.archive.org/cdx/search/cdx?url={self.domain}&output=json&filter=statuscode:200&limit=10"
            r = requests.get(url, timeout=15)
            if r.status_code == 200 and r.json():
                print(f"  {Y}[i] Check archived versions for technology changes")
                print(f"  {Y}[i] https://web.archive.org/web/2024/https://{self.domain}")
        except: pass

    def save_results(self):
        outfile = f"archive_recon_{self.domain}.json"
        with open(outfile, 'w') as f:
            json.dump({'domain': self.domain, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target Domain: {W}{self.domain}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.wayback_machine()
        self.google_cache()
        self.archive_today()
        self.recover_deleted()
        self.extract_emails()
        self.technology_detection()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Archive Recon Complete        ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help='Target domain')
    args = parser.parse_args()
    recon = ArchiveRecon(args.domain)
    recon.run_all()

if __name__ == "__main__":
    main()
