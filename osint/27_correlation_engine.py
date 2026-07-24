#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Data Correlation Engine                        ║
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

class CorrelationEngine:
    def __init__(self, target):
        self.target = target
        self.correlations = []
        self.results = {}

    def email_correlation(self):
        print(f"\n{G}[+] Method 1: Email Correlation{RS}")
        user = self.target.split('@')[0]
        domain = self.target.split('@')[1]

        # Find other emails with same domain
        patterns = [
            f"{user}@{domain}",
            f"{user}.backup@{domain}",
            f"{user}.old@{domain}",
            f"{user}@{domain.split('.')[0]}.com",
            f"{user}2@{domain}",
        ]
        for p in patterns:
            print(f"  {Y}[~] {p}")
        self.results['email_patterns'] = patterns

        # Search for other emails with same username
        print(f"\n  {Y}[i] Search: \"{user}\" email on Google")
        print(f"  {Y}[i] Search: site:pastebin.com \"{user}\"")

    def username_correlation(self):
        print(f"\n{G}[+] Method 2: Username Correlation{RS}")
        user = self.target.split('@')[0] if '@' in self.target else self.target
        platforms = [
            'github', 'twitter', 'instagram', 'facebook', 'linkedin',
            'reddit', 'tiktok', 'youtube', 'pinterest', 'twitch',
            'medium', 'dev.to', 'hackerone', 'gitlab', 'bitbucket',
            'steam', 'keybase', 'telegram', 'spotify', 'tumblr'
        ]
        found = []
        for p in platforms:
            print(f"  {Y}[i] {p}: https://{p}.com/{user}")
        self.results['username_platforms'] = platforms

    def phone_correlation(self):
        print(f"\n{G}[+] Method 3: Phone Number Correlation{RS}")
        phone = self.target.replace(' ', '').replace('-', '')
        formats = [
            f"+{phone}",
            f"{phone[:3]}-{phone[3:6]}-{phone[6:]}" if len(phone) >= 10 else phone,
            f"({phone[:3]}) {phone[3:6]}-{phone[6:]}" if len(phone) >= 10 else phone,
        ]
        for f in formats:
            print(f"  {Y}[~] Format: {f}")
        self.results['phone_formats'] = formats

    def name_correlation(self):
        print(f"\n{G}[+] Method 4: Name Correlation{RS}")
        name = self.target
        parts = name.split()
        if len(parts) >= 2:
            first, last = parts[0], parts[1]
            combinations = [
                f"{first}{last}",
                f"{first}.{last}",
                f"{first}_{last}",
                f"{first}-{last}",
                f"{first[0]}{last}",
                f"{first}{last[0]}",
                f"{last}{first}",
                f"{first.lower()}.{last.lower()}",
                f"{first.capitalize()}{last.capitalize()}",
            ]
            print(f"  {Y}[i] Username combinations:")
            for c in combinations:
                print(f"  {C}  - {c}")
            self.results['name_combinations'] = combinations

    def cross_reference(self):
        print(f"\n{G}[+] Method 5: Cross-Reference Sources{RS}")
        sources = [
            ('HaveIBeenPwned', f"https://haveibeenpwned.com/search/{self.target}"),
            ('IntelX', f"https://intelx.io/?s={self.target}"),
            ('DeHashed', f"https://dehashed.com/search?query={self.target}"),
            ('Snusbase', f"https://snusbase.com/{self.target}"),
            ('Google', f"https://www.google.com/search?q=%22{self.target}%22"),
            ('DuckDuckGo', f"https://duckduckgo.com/?q=%22{self.target}%22"),
            ('Bing', f"https://www.bing.com/search?q=%22{self.target}%22"),
        ]
        for name, url in sources:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['cross_ref'] = sources

    def generate_report(self):
        print(f"\n{G}[+] Method 6: Generate Correlation Report{RS}")
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           HELL SOCIETY - CORRELATION REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

Target: {self.target}
Date:   {time.strftime('%Y-%m-%d %H:%M:%S')}

{'='*60}
FINDED CORRELATIONS:
{'='*60}

{json.dumps(self.results, indent=2)}

{'='*60}
RECOMMENDED NEXT STEPS:
{'='*60}
1. Search target on all social media platforms
2. Check data breaches for associated information
3. Use reverse image search on profile pictures
4. Search Google Dorks for additional exposure
5. Check public records and directories

{'='*60}
"""
        outfile = f"correlation_report_{self.target.replace('@','_').replace(' ','_')}.txt"
        with open(outfile, 'w') as f:
            f.write(report)
        print(f"  {G}[✓] Report saved: {outfile}")

    def save_results(self):
        outfile = f"correlation_{self.target.replace('@','_')}.json"
        with open(outfile, 'w') as f:
            json.dump({'target': self.target, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target: {W}{self.target}")
        print(f"{Y}[~]{'─'*50}{RS}")

        if '@' in self.target:
            self.email_correlation()
        elif self.target.replace('+','').isdigit():
            self.phone_correlation()
        else:
            self.username_correlation()
            self.name_correlation()

        self.cross_reference()
        self.generate_report()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Correlation Engine Complete   ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='Target (email, username, phone, name)')
    args = parser.parse_args()
    engine = CorrelationEngine(args.target)
    engine.run_all()

if __name__ == "__main__":
    main()
