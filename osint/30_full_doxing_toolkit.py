#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Full Doxing Toolkit (All-in-One)               ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests, hashlib, socket
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

class FullDoxingToolkit:
    def __init__(self, target):
        self.target = target
        self.all_results = {}

    def determine_type(self):
        if '@' in self.target:
            return 'email'
        elif self.target.replace('+','').isdigit():
            return 'phone'
        elif re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', self.target):
            return 'ip'
        elif '.' in self.target:
            return 'domain'
        else:
            return 'username'

    def full_email_doxxing(self):
        print(f"\n{BR}[EMAIL DOXING]{RS}")
        email = self.target
        user = email.split('@')[0]
        domain = email.split('@')[1]

        # 1. Search everywhere
        print(f"\n{G}[1] Search Engines{RS}")
        print(f"  {C}  Google: \"\\\"{email}\\\"\"")
        print(f"  {C}  Bing: \"{email}\"")
        print(f"  {C}  DuckDuckGo: \"{email}\"")

        # 2. Breach databases
        print(f"\n{G}[2] Data Breaches{RS}")
        breaches = [
            f"https://haveibeenpwned.com/search/{email}",
            f"https://intelx.io/?s={email}",
            f"https://dehashed.com/search?query={email}",
            f"https://snusbase.com/{email}",
            f"https://leakcheck.io/search?query={email}",
        ]
        for b in breaches:
            print(f"  {C}  {b[:60]}")

        # 3. Social media
        print(f"\n{G}[3] Social Media{RS}")
        platforms = ['github', 'twitter', 'instagram', 'facebook', 'linkedin', 'reddit', 'pinterest', 'tiktok']
        for p in platforms:
            print(f"  {C}  {p}: https://{p}.com/{user}")

        # 4. IP extraction from email
        print(f"\n{G}[4] IP Extraction{RS}")
        print(f"  {C}  Gravatar: https://www.gravatar.com/avatar/{hashlib.md5(email.encode()).hexdigest()}")
        print(f"  {C}  Email header analysis tools")

        # 5. Phone correlation
        print(f"\n{G}[5] Phone Association{RS}")
        print(f"  {C}  https://phonebook.cz/api/?email={email}")
        print(f"  {C}  https://www.truecaller.com/")

        self.all_results['email'] = {'email': email, 'type': 'email'}

    def full_username_doxxing(self):
        print(f"\n{BR}[USERNAME DOXING]{RS}")
        user = self.target

        # Check 50+ platforms
        print(f"\n{G}[1] Platform Enumeration{RS}")
        platforms = {
            'GitHub': f'https://github.com/{user}',
            'Twitter': f'https://twitter.com/{user}',
            'Instagram': f'https://www.instagram.com/{user}',
            'Facebook': f'https://www.facebook.com/{user}',
            'LinkedIn': f'https://www.linkedin.com/in/{user}',
            'Reddit': f'https://www.reddit.com/user/{user}',
            'TikTok': f'https://www.tiktok.com/@{user}',
            'YouTube': f'https://www.youtube.com/@{user}',
            'Pinterest': f'https://www.pinterest.com/{user}',
            'Twitch': f'https://www.twitch.tv/{user}',
            'Medium': f'https://medium.com/@{user}',
            'Dev.to': f'https://dev.to/{user}',
            'StackOverflow': f'https://stackoverflow.com/users/?tab=users&q={user}',
            'HackerOne': f'https://hackerone.com/{user}',
            'GitLab': f'https://gitlab.com/{user}',
            'Bitbucket': f'https://bitbucket.org/{user}',
            'Steam': f'https://steamcommunity.com/id/{user}',
            'Keybase': f'https://keybase.io/{user}',
            'SoundCloud': f'https://soundcloud.com/{user}',
            'Spotify': f'https://open.spotify.com/user/{user}',
            'Tumblr': f'https://{user}.tumblr.com',
            'VK': f'https://vk.com/{user}',
            'Patreon': f'https://www.patreon.com/{user}',
            'Flickr': f'https://www.flickr.com/people/{user}',
            'Telegram': f'https://t.me/{user}',
            'WhatsApp': f'https://wa.me/{user}',
            'PayPal': f'https://www.paypal.me/{user}',
            'Fiverr': f'https://www.fiverr.com/{user}',
            'Dribbble': f'https://dribbble.com/{user}',
            'Behance': f'https://www.behance.net/{user}',
        }
        for name, url in platforms.items():
            print(f"  {C}  {name}: {url[:55]}")

        # GitHub API deep recon
        print(f"\n{G}[2] GitHub Deep Recon{RS}")
        try:
            r = requests.get(f"https://api.github.com/users/{user}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {C}  Name: {data.get('name','N/A')}")
                print(f"  {C}  Email: {data.get('email','N/A')}")
                print(f"  {C}  Bio: {data.get('bio','N/A')}")
                print(f"  {C}  Company: {data.get('company','N/A')}")
                print(f"  {C}  Location: {data.get('location','N/A')}")
                print(f"  {C}  Blog: {data.get('blog','N/A')}")
                print(f"  {C}  Twitter: {data.get('twitter_username','N/A')}")
                self.all_results['github'] = data
            else:
                print(f"  {Y}[!] GitHub user not found")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

        # Breach search
        print(f"\n{G}[3] Breach Search{RS}")
        print(f"  {C}  https://intelx.io/?s={user}")
        print(f"  {C}  https://dehashed.com/search?query={user}")
        print(f"  {C}  https://snusbase.com/{user}")

        self.all_results['username'] = {'username': user, 'type': 'username'}

    def full_ip_doxxing(self):
        print(f"\n{BR}[IP DOXING]{RS}")
        ip = self.target

        # Geolocation
        print(f"\n{G}[1] Geolocation{RS}")
        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {C}  Country: {data.get('country','')}")
                print(f"  {C}  Region: {data.get('regionName','')}")
                print(f"  {C}  City: {data.get('city','')}")
                print(f"  {C}  ISP: {data.get('isp','')}")
                print(f"  {C}  Lat/Lon: {data.get('lat','')}, {data.get('lon','')}")
                self.all_results['geo'] = data
        except: pass

        # Shodan
        print(f"\n{G}[2] Shodan{RS}")
        print(f"  {C}  https://www.shodan.io/host/{ip}")
        try:
            r = requests.get(f"https://internetdb.shodan.io/{ip}", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {C}  Ports: {data.get('ports',[])}")
                self.all_results['shodan'] = data
        except: pass

        # Reverse DNS
        print(f"\n{G}[3] Reverse DNS{RS}")
        try:
            hostname, _, _ = socket.gethostbyaddr(ip)
            print(f"  {C}  Hostname: {hostname}")
        except:
            print(f"  {Y}[!] No reverse DNS")

        # Threat intel
        print(f"\n{G}[4] Threat Intelligence{RS}")
        services = [
            f"https://www.abuseipdb.com/check/{ip}",
            f"https://www.virustotal.com/gui/ip-address/{ip}",
            f"https://otx.alienvault.com/indicator/ip/{ip}",
        ]
        for s in services:
            print(f"  {C}  {s[:60]}")

        self.all_results['ip'] = {'ip': ip, 'type': 'ip'}

    def full_phone_doxxing(self):
        print(f"\n{BR}[PHONE DOXING]{RS}")
        phone = self.target.replace(' ','').replace('-','').replace('+','')

        print(f"\n{G}[1] Carrier & Location{RS}")
        print(f"  {C}  Phone: +{phone}")
        print(f"  {C}  https://numverify.com/validate/{phone}")

        print(f"\n{G}[2] Social Media{RS}")
        print(f"  {C}  WhatsApp: https://wa.me/{phone}")
        print(f"  {C}  Telegram: https://t.me/+{phone}")
        print(f"  {C}  Truecaller: https://www.truecaller.com/search/{phone}")

        print(f"\n{G}[3] Reverse Lookup{RS}")
        print(f"  {C}  https://www.411.com/reverse-phone/{phone}")
        print(f"  {C}  https://www.whitepages.com/phone/1-{phone}")

        self.all_results['phone'] = {'phone': phone, 'type': 'phone'}

    def full_domain_doxxing(self):
        print(f"\n{BR}[DOMAIN DOXING]{RS}")
        domain = self.target

        print(f"\n{G}[1] WHOIS{RS}")
        print(f"  {C}  https://whois.domaintools.com/{domain}")
        print(f"  {C}  https://www.whois.com/whois/{domain}")

        print(f"\n{G}[2] DNS{RS}")
        print(f"  {C}  https://dnschecker.org/#A/{domain}")
        print(f"  {C}  https://www.mxtoolbox.com/DNSLookup.aspx?argument={domain}")

        print(f"\n{G}[3] History{RS}")
        print(f"  {C}  https://web.archive.org/web/*/http://{domain}/*")
        print(f"  {C}  https://builtwith.com/{domain}")

        self.all_results['domain'] = {'domain': domain, 'type': 'domain'}

    def generate_full_report(self):
        print(f"\n{BR}[GENERATING FULL REPORT]{RS}")
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║           HELL SOCIETY - FULL DOXING REPORT                 ║
╚══════════════════════════════════════════════════════════════╝

Target: {self.target}
Type:   {self.determine_type()}
Date:   {time.strftime('%Y-%m-%d %H:%M:%S')}
Tool:   Full Doxing Toolkit v1.0

{'='*60}
COLLECTED DATA:
{'='*60}

{json.dumps(self.all_results, indent=2)}

{'='*60}
NEXT STEPS:
{'='*60}
1. Run individual specialized tools for deeper analysis
2. Cross-reference findings across multiple sources
3. Check data breaches for additional information
4. Use social engineering if authorized
5. Document all findings for the report

{'='*60}
DISCLAIMER: This tool is for authorized pentesting only.
HELL SOCIETY assumes no liability for misuse.
{'='*60}
"""
        outfile = f"FULL_DOXING_REPORT_{self.target.replace('@','_').replace('.','_')}.txt"
        with open(outfile, 'w') as f:
            f.write(report)
        print(f"  {G}[✓] Full report saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target: {W}{self.target}")
        print(f"{B}[*] Type:   {W}{self.determine_type()}")
        print(f"{Y}[~]{'─'*50}{RS}")

        target_type = self.determine_type()

        if target_type == 'email':
            self.full_email_doxxing()
        elif target_type == 'username':
            self.full_username_doxxing()
        elif target_type == 'ip':
            self.full_ip_doxxing()
        elif target_type == 'phone':
            self.full_phone_doxxing()
        elif target_type == 'domain':
            self.full_domain_doxxing()

        self.generate_full_report()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Full Doxing Complete          ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--target', required=True, help='Target (email, username, IP, phone, domain)')
    args = parser.parse_args()
    toolkit = FullDoxingToolkit(args.target)
    toolkit.run_all()

if __name__ == "__main__":
    main()
