#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PEOPLE SEARCH ENGINE v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - People Intelligence                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import re

colorama.init(autoreset=True)

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██████╗ ██╗   ██╗███████╗███╗   ██╗███████╗                         {Fore.MAGENTA}║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔════╝████╗  ██║██╔════╝                         {Fore.MAGENTA}║
║{Fore.CYAN}  ██████╔╝██║   ██║█████╗  ██╔██╗ ██║█████╗                           {Fore.MAGENTA}║
║{Fore.CYAN}  ██╔══██╗██║   ██║██╔══╝  ██║╚██╗██║██╔══╝                           {Fore.MAGENTA}║
║{Fore.CYAN}  ██║  ██║╚██████╔╝███████╗██║ ╚████║██║                             {Fore.MAGENTA}║
║{Fore.CYAN}  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═╝                             {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - People Search Engine v2.0                        {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

class PeopleSearch:
    def __init__(self, name, location=None):
        self.name = name
        self.location = location
        self.results = []

    def generate_search_queries(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  SEARCH QUERIES:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        queries = []

        # Basic name search
        queries.append(f'"{self.name}"')
        queries.append(f'"{self.name}" filetype:pdf')
        queries.append(f'"{self.name}" filetype:doc')

        # With location
        if self.location:
            queries.append(f'"{self.name}" "{self.location}"')
            queries.append(f'"{self.name}" "{self.location}" filetype:pdf')

        # Professional
        queries.append(f'"{self.name}" linkedin')
        queries.append(f'"{self.name}" github')
        queries.append(f'"{self.name}" twitter')

        # Documents & records
        queries.append(f'"{self.name}" intitle:resume')
        queries.append(f'"{self.name}" intitle:cv')
        queries.append(f'"{self.name}" site:linkedin.com')
        queries.append(f'"{self.name}" site:github.com')

        # Social media
        queries.append(f'"{self.name}" site:twitter.com')
        queries.append(f'"{self.name}" site:instagram.com')
        queries.append(f'"{self.name}" site:facebook.com')

        # Data breaches & leaks
        queries.append(f'"{self.name}" email')
        queries.append(f'"{self.name}" breach')

        # Professional records
        queries.append(f'"{self.name}" company')
        queries.append(f'"{self.name}" OR "{self.name.split()[-1]}" email')

        for i, q in enumerate(queries, 1):
            encoded = q.replace(' ', '+').replace('"', '%22')
            url = f"https://www.google.com/search?q={encoded}"
            print(f"  {Fore.WHITE}[{i:02d}] {q}")
            print(f"  {Fore.CYAN}     {url}")
            self.results.append({'query': q, 'url': url})

    def check_databases(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DATABASE CHECKS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        databases = [
            ('HaveIBeenPwned', f'https://haveibeenpwned.com/'),
            ('DeHashed', f'https://dehashed.com/search?query="{self.name}"'),
            ('IntelX', f'https://intelx.io/?s="{self.name}"'),
            ('Pipl', f'https://pipl.com/'),
            ('BeenVerified', f'https://www.beenverified.com/'),
            ('Spokeo', f'https://www.spokeo.com/'),
            ('TruePeopleSearch', f'https://www.truepeoplesearch.com/results?name={self.name}'),
            ('FastPeopleSearch', f'https://www.fastpeoplesearch.com/'),
            ('WebMii', f'https://webmii.com/people?n={self.name}'),
        ]

        for name, url in databases:
            print(f"  {Fore.WHITE}[{name}]")
            print(f"    {Fore.CYAN}{url}")

    def generate_links(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DIRECT LINKS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        links = {
            'LinkedIn': f'https://www.linkedin.com/search/results/all/?keywords={self.name}',
            'GitHub': f'https://github.com/search?q={self.name}',
            'Twitter/X': f'https://twitter.com/search?q={self.name}',
            'Facebook': f'https://www.facebook.com/public/{self.name.replace(" ", "+")}',
            'Instagram': f'https://www.google.com/search?q=site:instagram.com+"{self.name}"',
            'Google Scholar': f'https://scholar.google.com/scholar?q={self.name}',
            'Wayback': f'https://web.archive.org/web/*/{self.name}',
        }

        for platform, url in links.items():
            print(f"  {Fore.WHITE}  {platform}: {url}")

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.name}")
        if self.location:
            print(f"{Fore.CYAN}  [*] Location: {Fore.WHITE}{self.location}")
        print(f"{Fore.CYAN}  [*] Starting people search...\n")

        self.generate_search_queries()
        self.check_databases()
        self.generate_links()

        # Save results
        results_file = f'/tmp/people_search_{self.name.replace(" ", "_")}.json'
        with open(results_file, 'w') as f:
            json.dump({'name': self.name, 'location': self.location, 'queries': self.results}, f, indent=2)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  PEOPLE SEARCH COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"\n  {Fore.YELLOW}[i] Use the generated queries in your browser for results")

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society People Search')
    parser.add_argument('-n', '--name', required=True, help='Target name')
    parser.add_argument('-l', '--location', help='Target location')
    args = parser.parse_args()

    search = PeopleSearch(args.name, args.location)
    search.run()
