#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Deep Web & Dark Web Search Tool                ║
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

class DeepWebSearch:
    def __init__(self, query):
        self.query = query
        self.results = {}

    def tor_search_engines(self):
        print(f"\n{G}[+] Method 1: Tor Search Engines{RS}")
        engines = [
            ('Ahmia', 'http://msydqstlz2kzerdg.onion/search/?q='),
            ('Torch', 'http://torchdeedp3i2jigzjdmfpn5ttjhthh5wbmda2rr3jvqjg5p77c54dqd.onion/'),
            ('Haystak', 'http://haystak5njsmn2hqkewecpaxetahtwhsbsa64jom2k22z5afxhnpxfid.onion/'),
            ('Not Evil', 'http://hss3uro2hsxfogfq.onion/'),
            ('Dan', 'http://dancb4v75v7w7s.onion/'),
        ]
        for name, url in engines:
            search_url = f"{url}{self.query}" if '?' in url else url
            print(f"  {Y}[i] {name}: {search_url[:60]}")
        self.results['tor_engines'] = engines

    def pastebin_search(self):
        print(f"\n{G}[+] Method 2: Pastebin & Paste Sites{RS}")
        sites = [
            ('Pastebin', f"https://pastebin.com/search?q={self.query}"),
            ('GhostBin', f"https://ghostbin.com/search?q={self.query}"),
            ('Paste.ee', f"https://paste.ee/search?q={self.query}"),
            ('Pastes.io', f"https://pastes.io/search?q={self.query}"),
            ('ZeroBin', f"https://zerobin.net/search?q={self.query}"),
            ('PrivateBin', f"https://privatebin.net/search?q={self.query}"),
        ]
        for name, url in sites:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['pastebin'] = sites

    def forum_search(self):
        print(f"\n{G}[+] Method 3: Forum & Board Search{RS}")
        forums = [
            ('4chan', f"https://boards.4chan.org/g/search?q={self.query}"),
            ('8kun', f"https://8kun.top/search?q={self.query}"),
            ('Reddit', f"https://www.reddit.com/search?q={self.query}"),
            ('Hacker News', f"https://hn.algolia.com/?dateRange=all&page=0&query={self.query}&type=story"),
            ('Lobsters', f"https://lobste.rs/search?q={self.query}"),
        ]
        for name, url in forums:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['forums'] = forums

    def breach_databases(self):
        print(f"\n{G}[+] Method 4: Breach Database Search{RS}")
        dbs = [
            ('IntelX', f"https://intelx.io/?s={self.query}"),
            ('DeHashed', f"https://dehashed.com/search?query={self.query}"),
            ('Snusbase', f"https://snusbase.com/{self.query}"),
            ('LeakCheck', f"https://leakcheck.io/search?query={self.query}"),
            ('HaveIBeenPwned', f"https://haveibeenpwned.com/search/{self.query}"),
            ('WeLeakInfo', f"https://weleakinfo.com/search?query={self.query}"),
            ('Scylla', f"https://scylla.sh/search?email={self.query}"),
            ('BreachDirectory', f"https://breachdirectory.org/{self.query}"),
        ]
        for name, url in dbs:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['breaches'] = dbs

    def google_dorks(self):
        print(f"\n{G}[+] Method 5: Advanced Google Dorks{RS}")
        dorks = [
            f'"{self.query}" site:pastebin.com',
            f'"{self.query}" site:ghostbin.com',
            f'"{self.query}" site:pastes.io',
            f'"{self.query}" filetype:txt',
            f'"{self.query}" filetype:sql',
            f'"{self.query}" filetype:csv',
            f'"{self.query}" filetype:xls',
            f'"{self.query}" intitle:"index of"',
            f'"{self.query}" inurl:login',
            f'"{self.query}" inurl:admin',
            f'"{self.query}" site:onion.link',
            f'"{self.query}" site:onion.to',
        ]
        for d in dorks:
            print(f"  {C}  {d}")
        self.results['dorks'] = dorks

    def search_api(self):
        print(f"\n{G}[+] Method 6: Search APIs{RS}")
        try:
            # Google Custom Search (requires API key)
            print(f"  {Y}[i] Google CSE: https://developers.google.com/custom-search/v1/overview")
            # Bing API
            print(f"  {Y}[i] Bing API: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api")
            # Shodan
            print(f"  {Y}[i] Shodan: https://www.shodan.io/search?query={self.query}")
            # Censys
            print(f"  {Y}[i] Censys: https://search.censys.io/search?resource=hosts&q={self.query}")
            self.results['apis'] = ['Google CSE', 'Bing API', 'Shodan', 'Censys']
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def save_results(self):
        outfile = f"deepweb_search_{self.query.replace(' ','_')[:30]}.json"
        with open(outfile, 'w') as f:
            json.dump({'query': self.query, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Query: {W}{self.query}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.tor_search_engines()
        self.pastebin_search()
        self.forum_search()
        self.breach_databases()
        self.google_dorks()
        self.search_api()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Deep Web Search Complete      ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', required=True, help='Search query')
    args = parser.parse_args()
    search = DeepWebSearch(args.query)
    search.run_all()

if __name__ == "__main__":
    main()
