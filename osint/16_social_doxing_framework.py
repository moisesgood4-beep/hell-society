#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Social Media Doxing Framework                   ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY,BB,BM,BC,BW=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW,Style.BRIGHT+Fore.BLUE,Style.BRIGHT+Fore.MAGENTA,Style.BRIGHT+Fore.CYAN,Style.BRIGHT+Fore.WHITE
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY=BB=BM=BC=BW="" ; RS=""

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
    'github': 'https://api.github.com/users/{}',
    'twitter': 'https://nitter.net/{}',
    'instagram': 'https://www.instagram.com/{}',
    'facebook': 'https://www.facebook.com/{}',
    'linkedin': 'https://www.linkedin.com/in/{}',
    'reddit': 'https://www.reddit.com/user/{}/',
    'pinterest': 'https://www.pinterest.com/{}',
    'tiktok': 'https://www.tiktok.com/@{}',
    'youtube': 'https://www.youtube.com/@{}',
    'spotify': 'https://open.spotify.com/user/{}',
    'twitch': 'https://www.twitch.tv/{}',
    'telegram': 'https://t.me/{}',
    'snapchat': 'https://www.snapchat.com/add/{}',
    'tiktok_api': 'https://www.tiktok.com/api/user/detail?uniqueId={}',
    'medium': 'https://medium.com/@{}',
    'devto': 'https://dev.to/{}',
    'hackerone': 'https://hackerone.com/{}',
    'bitbucket': 'https://bitbucket.org/{}/',
    'gitlab': 'https://gitlab.com/{}',
    'steam': 'https://steamcommunity.com/id/{}',
    'keybase': 'https://keybase.io/{}',
    'pypi': 'https://pypi.org/user/{}/',
    'npm': 'https://www.npmjs.com/~{}',
    'hackernews': 'https://news.ycombinator.com/user?id={}',
    'stackoverflow': 'https://stackoverflow.com/users/?tab=users&q={}',
    'tumblr': 'https://{}.tumblr.com/',
    'vk': 'https://vk.com/{}',
    'whatsapp': 'https://wa.me/{}',
}

class SocialDoxer:
    def __init__(self, username):
        self.username = username
        self.found = []
        self.not_found = []
        self.results = {}

    def check_platform(self, name, url_template):
        url = url_template.format(self.username)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0'}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code in [200, 301, 302]:
                self.found.append(name)
                self.results[name] = {'url': url, 'status': r.status_code, 'found': True}
                print(f"  {G}[✓] {name}: FOUND ({r.status_code})")
                return True
            else:
                self.not_found.append(name)
                self.results[name] = {'url': url, 'status': r.status_code, 'found': False}
                print(f"  {R}[✗] {name}: Not found ({r.status_code})")
                return False
        except:
            print(f"  {Y}[~] {name}: Unreachable")
            self.results[name] = {'url': url, 'found': False, 'error': True}
            return False

    def github_recon(self):
        print(f"\n{G}[+] GitHub Deep Recon{RS}")
        url = f"https://api.github.com/users/{self.username}"
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                info = {}
                info['name'] = data.get('name', 'N/A')
                info['email'] = data.get('email', 'N/A')
                info['bio'] = data.get('bio', 'N/A')
                info['company'] = data.get('company', 'N/A')
                info['location'] = data.get('location', 'N/A')
                info['blog'] = data.get('blog', 'N/A')
                info['twitter'] = data.get('twitter_username', 'N/A')
                info['repos'] = data.get('public_repos', 0)
                info['followers'] = data.get('followers', 0)
                info['avatar'] = data.get('avatar_url', 'N/A')

                for k, v in info.items():
                    if v and v != 'N/A':
                        print(f"  {C}[{k}] {W}{v}")

                self.results['github_detail'] = info

                # Get repos
                repos_url = f"https://api.github.com/users/{self.username}/repos"
                r2 = requests.get(repos_url, timeout=10)
                if r2.status_code == 200:
                    repos = r2.json()
                    print(f"\n  {Y}[i] Repos ({len(repos)}):")
                    for repo in repos[:10]:
                        print(f"  {G}  - {repo['name']} ({repo.get('language','?')})")
                    self.results['repos'] = [r['name'] for r in repos[:10]]
                return info
        except Exception as e:
            print(f"  {R}[!] Error: {e}")
        return None

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target Username: {W}{self.username}")
        print(f"{Y}[~]{'─'*50}{RS}")

        # Phase 1: Check all platforms
        print(f"\n{BR}[PHASE 1] Checking {len(PLATFORMS)} platforms...{RS}")
        for name, url in PLATFORMS.items():
            self.check_platform(name, url)

        # Phase 2: GitHub deep recon
        self.github_recon()

        # Phase 3: Save results
        outfile = f"social_doxing_{self.username}.json"
        with open(outfile, 'w') as f:
            json.dump({
                'username': self.username,
                'found': self.found,
                'not_found': self.not_found,
                'results': self.results
            }, f, indent=2)

        print(f"\n{G}[+] Results saved: {outfile}")
        print(f"{BR}{'═'*50}")
        print(f"{BR}║  Found: {len(self.found)} platforms  ║")
        print(f"{BR}║  Not Found: {len(self.not_found)} platforms  ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Target username')
    args = parser.parse_args()
    doxer = SocialDoxer(args.username)
    doxer.run_all()

if __name__ == "__main__":
    main()
