#!/usr/bin/env python3
"""Social Media Link Finder - Discover all social media accounts for a username."""
import os, sys
try:
    from colorama import init, Fore, Style; init(autoreset=True)
except: os.system("pip3 install colorama 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True)

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;M=Fore.MAGENTA;BW=Style.BRIGHT+Fore.WHITE
BR=Style.BRIGHT+Fore.RED;BG=Style.BRIGHT+Fore.GREEN;BC=Style.BRIGHT+Fore.CYAN;RS=Style.RESET_ALL

BANNER = f"""{BR}⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄{RS}
  {Y}  Created by: HELL SOCIETY{RS}"""

DISCLAIMER = f"{R}╔══════════════════════════════════════════════════════════════════╗\n║ {BW}DISCLAIMER: Developers assume no liability and are not            ║\n║ {BW}responsible for any misuse or damage caused.                      ║\n║ {BW}Only use for educational purposes!!                               ║\n║ {BG}Attacking targets without mutual consent is illegal!!{RS}  {R}║\n╚══════════════════════════════════════════════════════════════════╝{RS}"

def clear(): os.system('clear' if os.name!='nt' else 'cls')

PLATFORMS = {
    "Instagram": "https://instagram.com/{u}", "Facebook": "https://facebook.com/{u}",
    "Twitter/X": "https://x.com/{u}", "TikTok": "https://tiktok.com/@{u}",
    "YouTube": "https://youtube.com/@{u}", "LinkedIn": "https://linkedin.com/in/{u}",
    "GitHub": "https://github.com/{u}", "Reddit": "https://reddit.com/user/{u}",
    "Pinterest": "https://pinterest.com/{u}", "Twitch": "https://twitch.tv/{u}",
    "Discord": "https://discord.com/users/{u}", "Snapchat": "https://snapchat.com/add/{u}",
    "Spotify": "https://open.spotify.com/user/{u}", "Steam": "https://steamcommunity.com/id/{u}",
    "Telegram": "https://t.me/{u}", "WhatsApp": "https://wa.me/{u}",
    "Medium": "https://medium.com/@{u}", "Tumblr": "https://{u}.tumblr.com",
    "Vimeo": "https://vimeo.com/{u}", "SoundCloud": "https://soundcloud.com/{u}",
    "Flickr": "https://flickr.com/people/{u}", "Dribbble": "https://dribbble.com/{u}",
    "Behance": "https://behance.net/{u}", "DeviantArt": "https://{u}.deviantart.com",
    "Kickstarter": "https://kickstarter.com/profile/{u}", "Patreon": "https://patreon.com/{u}",
    "OnlyFans": "https://onlyfans.com/{u}", "Gravatar": "https://gravatar.com/{u}",
    "Keybase": "https://keybase.io/{u}", "GitLab": "https://gitlab.com/{u}",
    "Bitbucket": "https://bitbucket.org/{u}", "CodePen": "https://codepen.io/{u}",
    "HackerRank": "https://hackerrank.com/{u}", "StackOverflow": "https://stackoverflow.com/users/{u}",
    "Wikipedia": "https://en.wikipedia.org/wiki/User:{u}", "Quora": "https://quora.com/profile/{u}",
    "Goodreads": "https://goodreads.com/{u}", "LastFM": "https://last.fm/user/{u}",
    "Mixcloud": "https://mixcloud.com/{u}", "Foursquare": "https://foursquare.com/{u}",
    "TripAdvisor": "https://tripadvisor.com/members/{u}", "Amazon": "https://amazon.com/gp/profile/{u}",
    "eBay": "https://ebay.com/usr/{u}", "PayPal": "https://paypal.me/{u}",
    "Venmo": "https://venmo.com/{u}", "CashApp": "https://cash.app/${u}",
    "Crypto": "https://etherscan.io/address/{u}", "Google+": "https://plus.google.com/{u}",
}

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Social Media Link Finder{RS}")
    print(f"{Y}{'─'*55}{RS}")
    username = input(f"\n{C}[*] Enter username: {RS}").strip()
    if not username: print(f"{R}[!] No username{RS}"); sys.exit(1)
    
    print(f"\n{Y}[+] Searching for: {BW}{username}{RS}\n")
    count = 0
    for platform, url_template in sorted(PLATFORMS.items()):
        url = url_template.format(u=username)
        color = G if count % 2 == 0 else C
        print(f"  {color}[+] {BW}{platform:20}{RS} {url}")
        count += 1
    
    print(f"\n{BG}[*] Total platforms: {count}{RS}")
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
