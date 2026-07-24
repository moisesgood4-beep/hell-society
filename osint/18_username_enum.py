#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Username Enumeration Tool                       ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests
from concurrent.futures import ThreadPoolExecutor, as_completed
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    R,G,Y,B,M,C,W=Fore.RED,Fore.GREEN,Fore.YELLOW,Fore.BLUE,Fore.MAGENTA,Fore.CYAN,Fore.WHITE
    BR,BG,BY=Style.BRIGHT+Fore.RED,Style.BRIGHT+Fore.GREEN,Style.BRIGHT+Fore.YELLOW
    RS=Style.RESET_ALL
except: R=G=Y=B=M=C=W=BR=BG=BY="" ; RS=""

BANNER=f"""{BR}
██╗   ██╗████████╗██╗   ██╗ ██████╗ ██████╗  █████╗ ██╗
██║   ██║╚══██╔══╝╚██╗ ██╔╝██╔═══██╗██╔══██╗██╔══██╗██║
██║   ██║   ██║    ╚████╔╝ ██║   ██║██████╔╝███████║██║
██║   ██║   ██║     ╚██╔╝  ██║   ██║██╔═══╝ ██╔══██║██║
╚██████╔╝   ██║      ██║   ╚██████╔╝██║     ██║  ██║███████╗
 ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝
{Y}  Created by: HELL SOCIETY{RS}
"""

SITES = {
    'GitHub': {'url': 'https://github.com/{}', 'exists': 200},
    'Twitter/X': {'url': 'https://twitter.com/{}', 'exists': 200},
    'Instagram': {'url': 'https://www.instagram.com/{}', 'exists': 200},
    'Facebook': {'url': 'https://www.facebook.com/{}', 'exists': 200},
    'LinkedIn': {'url': 'https://www.linkedin.com/in/{}', 'exists': 200},
    'Reddit': {'url': 'https://www.reddit.com/user/{}', 'exists': 200},
    'TikTok': {'url': 'https://www.tiktok.com/@{}', 'exists': 200},
    'YouTube': {'url': 'https://www.youtube.com/@{}', 'exists': 200},
    'Pinterest': {'url': 'https://www.pinterest.com/{}', 'exists': 200},
    'Twitch': {'url': 'https://www.twitch.tv/{}', 'exists': 200},
    'Medium': {'url': 'https://medium.com/@{}', 'exists': 200},
    'Dev.to': {'url': 'https://dev.to/{}', 'exists': 200},
    'StackOverflow': {'url': 'https://stackoverflow.com/users?tab=users&q={}', 'exists': 200},
    'HackerOne': {'url': 'https://hackerone.com/{}', 'exists': 200},
    'Bitbucket': {'url': 'https://bitbucket.org/{}/', 'exists': 200},
    'GitLab': {'url': 'https://gitlab.com/{}', 'exists': 200},
    'Steam': {'url': 'https://steamcommunity.com/id/{}', 'exists': 200},
    'Keybase': {'url': 'https://keybase.io/{}', 'exists': 200},
    'SoundCloud': {'url': 'https://soundcloud.com/{}', 'exists': 200},
    'Spotify': {'url': 'https://open.spotify.com/user/{}', 'exists': 200},
    'Tumblr': {'url': 'https://{}.tumblr.com/', 'exists': 200},
    'VK': {'url': 'https://vk.com/{}', 'exists': 200},
    'Patreon': {'url': 'https://www.patreon.com/{}', 'exists': 200},
    'WordPress': {'url': 'https://en.gravatar.com/{}', 'exists': 200},
    'Flickr': {'url': 'https://www.flickr.com/people/{}', 'exists': 200},
    'Last.fm': {'url': 'https://www.last.fm/user/{}', 'exists': 200},
    'Slack': {'url': 'https://app.slack.com/{}', 'exists': 200},
    'Trello': {'url': 'https://trello.com/{}', 'exists': 200},
    'Quora': {'url': 'https://www.quora.com/profile/{}', 'exists': 200},
    'TripAdvisor': {'url': 'https://www.tripadvisor.com/Profile/{}', 'exists': 200},
    'About.me': {'url': 'https://about.me/{}', 'exists': 200},
    'Fiverr': {'url': 'https://www.fiverr.com/{}', 'exists': 200},
    'Dribbble': {'url': 'https://dribbble.com/{}', 'exists': 200},
    'Behance': {'url': 'https://www.behance.net/{}', 'exists': 200},
    'Wattpad': {'url': 'https://www.wattpad.com/user/{}', 'exists': 200},
    'Roblox': {'url': 'https://www.roblox.com/user.aspx?username={}', 'exists': 200},
    'Minecraft': {'url': 'https://namemc.com/profile/{}', 'exists': 200},
    'Pypi': {'url': 'https://pypi.org/user/{}/', 'exists': 200},
    'NPM': {'url': 'https://www.npmjs.com/~{}', 'exists': 200},
    'HackerRank': {'url': 'https://www.hackerrank.com/{}', 'exists': 200},
    'LeetCode': {'url': 'https://leetcode.com/{}', 'exists': 200},
    'CodeChef': {'url': 'https://www.codechef.com/users/{}', 'exists': 200},
    'Kaggle': {'url': 'https://www.kaggle.com/{}', 'exists': 200},
    'Imgur': {'url': 'https://imgur.com/user/{}', 'exists': 200},
    '9GAG': {'url': 'https://9gag.com/u/{}', 'exists': 200},
    'Weibo': {'url': 'https://weibo.com/{}', 'exists': 200},
    'Xing': {'url': 'https://www.xing.com/profile/{}', 'exists': 200},
    'Telegram': {'url': 'https://t.me/{}', 'exists': 200},
    'Discord': {'url': 'https://discord.com/invite/{}', 'exists': 200},
    'PayPal': {'url': 'https://www.paypal.me/{}', 'exists': 200},
}

class UsernameEnum:
    def __init__(self, username, threads=20):
        self.username = username
        self.threads = threads
        self.found = []
        self.not_found = []
        self.results = {}

    def check_site(self, name, config):
        url = config['url'].format(self.username)
        try:
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0'}
            r = requests.get(url, headers=headers, timeout=10, allow_redirects=False)
            if r.status_code == config['exists']:
                self.found.append(name)
                self.results[name] = {'url': url, 'status': r.status_code, 'found': True}
                return f"  {G}[✓] {name}: FOUND ({r.status_code}) {url[:50]}"
            else:
                self.not_found.append(name)
                self.results[name] = {'url': url, 'status': r.status_code, 'found': False}
                return f"  {R}[✗] {name}: Not found ({r.status_code})"
        except:
            self.not_found.append(name)
            return f"  {Y}[~] {name}: Timeout/Error"

    def run(self):
        print(BANNER)
        print(f"{B}[*] Target: {W}{self.username}")
        print(f"{B}[*] Sites: {W}{len(SITES)}")
        print(f"{Y}[~]{'─'*50}{RS}")
        print(f"\n{BR}[SCANNING...]{RS}\n")

        with ThreadPoolExecutor(max_workers=self.threads) as pool:
            futures = {pool.submit(self.check_site, name, config): name for name, config in SITES.items()}
            for future in as_completed(futures):
                print(future.result())

        # Save results
        outfile = f"username_enum_{self.username}.json"
        with open(outfile, 'w') as f:
            json.dump({
                'username': self.username,
                'found': self.found,
                'not_found': self.not_found,
                'results': self.results
            }, f, indent=2)

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Username Enumeration Complete ║")
        print(f"{BR}║  Found: {len(self.found)} sites                   ║")
        print(f"{BR}║  Not Found: {len(self.not_found)} sites             ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

        print(f"\n{G}[+] Results saved: {outfile}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username', required=True, help='Target username')
    parser.add_argument('-t', '--threads', type=int, default=20, help='Threads (default: 20)')
    args = parser.parse_args()
    enum = UsernameEnum(args.username, args.threads)
    enum.run()

if __name__ == "__main__":
    main()
