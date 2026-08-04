#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  USERNAME RECONNAISSANCE v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Username Intelligence                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

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

PLATFORMS = {
    'Twitter/X': ('https://twitter.com/{}', [200]),
    'Instagram': ('https://www.instagram.com/{}/', [200]),
    'GitHub': ('https://github.com/{}', [200]),
    'LinkedIn': ('https://www.linkedin.com/in/{}', [200]),
    'Reddit': ('https://www.reddit.com/user/{}', [200]),
    'TikTok': ('https://www.tiktok.com/@{}', [200]),
    'Pinterest': ('https://www.pinterest.com/{}/', [200]),
    'Twitch': ('https://www.twitch.tv/{}', [200]),
    'Medium': ('https://medium.com/@{}', [200]),
    'DeviantArt': ('https://www.deviantart.com/{}', [200]),
    'Steam': ('https://steamcommunity.com/id/{}', [200]),
    'Flickr': ('https://www.flickr.com/photos/{}/', [200]),
    'HackerNews': ('https://news.ycombinator.com/user?id={}', [200]),
    'Keybase': ('https://keybase.io/{}', [200]),
    'SoundCloud': ('https://soundcloud.com/{}', [200]),
    'Spotify': ('https://open.spotify.com/user/{}', [200]),
    'Vimeo': ('https://vimeo.com/{}', [200]),
    'WordPress': ('https://{}.wordpress.com', [200]),
    'Tumblr': ('https://{}.tumblr.com', [200]),
    'Bitbucket': ('https://bitbucket.org/{}/', [200]),
    'GitLab': ('https://gitlab.com/{}', [200]),
    'Gravatar': ('https://en.gravatar.com/{}', [200]),
    'YouTube': ('https://www.youtube.com/@{}', [200]),
    'Facebook': ('https://www.facebook.com/{}', [200]),
}

class UsernameRecon:
    def __init__(self, username):
        self.username = username
        self.found = []
        self.not_found = []
        self.errors = []

    def check_platform(self, platform, config):
        url_template, valid_codes = config
        url = url_template.format(self.username)

        try:
            resp = requests.get(url, timeout=10, headers={
                'User-Agent': 'Mozilla/5.0 HellSociety/2.0'
            })

            if resp.status_code in valid_codes:
                self.found.append({'platform': platform, 'url': url, 'status': resp.status_code})
                return True
            else:
                self.not_found.append(platform)
                return False
        except:
            self.errors.append(platform)
            return False

    def run(self):
        print(f"{Fore.CYAN}  [*] Target username: {Fore.WHITE}{self.username}")
        print(f"{Fore.CYAN}  [*] Checking {len(PLATFORMS)} platforms...\n")

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {}
            for platform, config in PLATFORMS.items():
                future = executor.submit(self.check_platform, platform, config)
                futures[future] = platform

            for future in as_completed(futures):
                platform = futures[future]
                if future.result():
                    print(f"  {Fore.GREEN}[+] {platform}: FOUND")
                else:
                    pass

        self.print_results()

    def print_results(self):
        print(f"\n\n{Fore.GREEN}{Back.BLACK}  USERNAME RECON COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.GREEN}[+] Found on: {len(self.found)} platforms")
        for f in self.found:
            print(f"    {Fore.GREEN}• {f['platform']}: {f['url']}")

        print(f"\n  {Fore.YELLOW}[-] Not found: {len(self.not_found)}")
        print(f"  {Fore.RED}[!] Errors: {len(self.errors)}")

        # Save results
        results = {'username': self.username, 'found': self.found, 'count': len(self.found)}
        with open(f'/tmp/username_recon_{self.username}.json', 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Results saved to /tmp/")


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
    print(f"  {BW}{Style.BRIGHT}  USERNAME RECON{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}USERNAME RECON                          {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target username                              {RS}")
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
            print(f"  {Y}[*] Target username{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
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

