#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEB DIRECTORY FUZZER v2.0                                       ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Web Pentesting                            ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import requests
import sys
import time
import colorama
from colorama import Fore, Back, Style
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import threading

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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

WORDLIST = [
    "admin", "administrator", "login", "logout", "signin", "signout",
    "register", "signup", "dashboard", "panel", "console", "manage",
    "manager", "config", "configuration", "settings", "setup",
    "install", "upgrade", "update", "backup", "db", "database",
    "mysql", "phpmyadmin", "wp-admin", "wp-login", "wp-content",
    "wp-includes", "wp-config", "api", "api/v1", "api/v2",
    "graphql", "rest", "swagger", "docs", "documentation",
    "test", "testing", "dev", "development", "staging", "prod",
    "production", "debug", "error", "logs", "log", "tmp", "temp",
    "cache", "session", "sessions", "upload", "uploads", "download",
    "downloads", "files", "file", "images", "img", "css", "js",
    "scripts", "includes", "lib", "library", "vendor", "node_modules",
    "assets", "static", "public", "private", "secret", "hidden",
    "robots.txt", "sitemap.xml", "favicon.ico", ".htaccess",
    ".git", ".svn", ".env", ".gitignore", ".htpasswd",
    "phpinfo.php", "info.php", "test.php", "index.php", "index.html",
    "index.php.bak", "index.html.bak", ".DS_Store",
    "server-status", "server-info", "status", "health",
    "healthcheck", "ping", "version", "changelog",
    "readme", "README", "README.md", "CHANGELOG",
    "LICENSE", "CONTRIBUTING", "docker-compose.yml",
    "Dockerfile", "Makefile", "requirements.txt",
    "package.json", "composer.json", "Gemfile",
    "cgi-bin", "bin", "sbin", "etc", "var", "opt",
    "proc", "sys", "dev", "root", "home", "user",
    "ftp", "ssh", "telnet", "smtp", "dns",
    "php-fpm", "nginx", "apache", "tomcat", "jboss",
    "jenkins", "gitlab", "github", "bitbucket",
    "phpinfo", "phpMyAdmin", "cpanel", "webmail",
    "phpmyadmin", "myadmin", "adminer",
    "old", "new", "old_site", "backup_site",
    "archive", "archives", "data", "csv", "xml", "json",
    "export", "import", "migrate", "migration",
    "password", "reset", "forgot", "recover",
    "user", "users", "profile", "account", "accounts",
    "search", "query", "results", "filter", "sort",
    "print", "pdf", "report", "reports", "stats",
    "analytics", "tracking", "cookie", "session",
    "auth", "authentication", "authorization", "oauth",
    "token", "tokens", "keys", "secrets", "credentials",
]

EXTENSIONS = [".php", ".html", ".htm", ".asp", ".aspx", ".jsp",
              ".js", ".json", ".xml", ".txt", ".bak", ".old",
              ".log", ".conf", ".cfg", ".ini", ".env", ".yml", ".yaml"]

class DirectoryFuzzer:
    def __init__(self, target, threads=20, timeout=5):
        self.target = target.rstrip('/')
        self.threads = threads
        self.timeout = timeout
        self.results = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) HellSociety/2.0'
        })

    def test_path(self, path):
        url = f"{self.target}/{path}"
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=False)

            if response.status_code not in [404, 403]:
                result = {
                    'path': path,
                    'status_code': response.status_code,
                    'size': len(response.text),
                    'redirect': response.headers.get('Location', ''),
                    'content_type': response.headers.get('Content-Type', '')
                }
                with self.lock:
                    self.results.append(result)
                    status_color = Fore.GREEN if response.status_code == 200 else Fore.YELLOW
                    print(f"  {status_color}[{response.status_code}] {Fore.WHITE}{path} {Fore.CYAN}({len(response.text)} bytes)")

            return True
        except requests.exceptions.Timeout:
            return False
        except requests.exceptions.RequestException:
            return False

    def fuzz(self):
        targets = []

        for word in WORDLIST:
            targets.append(word)
            for ext in EXTENSIONS:
                targets.append(f"{word}{ext}")

        total = len(targets)
        print(f"{Fore.CYAN}  [*] Testing {total} paths with {self.threads} threads\n")

        completed = 0
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.test_path, path): path for path in targets}

            for future in as_completed(futures):
                completed += 1
                progress = (completed / total) * 100
                bar_length = 40
                filled = int(bar_length * completed / total)
                bar = f"{Fore.GREEN}█{Style.RESET_ALL}" * filled + f"{Fore.RED}░{Style.RESET_ALL}" * (bar_length - filled)
                print(f"\r{Fore.CYAN}  [{bar}] {progress:.1f}% - Found: {len(self.results)}", end="", flush=True)

    def print_results(self):
        if not self.results:
            print(f"\n\n{Fore.YELLOW}  [!] No interesting paths found")
            return

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  SCAN COMPLETE - {len(self.results)} PATHS FOUND  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        self.results.sort(key=lambda x: x['status_code'])

        for r in self.results:
            status_color = Fore.GREEN if r['status_code'] == 200 else Fore.YELLOW
            print(f"  {status_color}[{r['status_code']}] {Fore.WHITE}/{r['path']}")
            if r['redirect']:
                print(f"           {Fore.YELLOW}Redirect: {r['redirect']}")
            print(f"           {Fore.CYAN}Size: {r['size']} bytes | Content-Type: {r['content_type']}")



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
    print(f"  {BW}{Style.BRIGHT}  DIRECTORY FUZZER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}DIRECTORY FUZZER                        {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Target URL                                   {RS}")
        print(f"  {C}[2]  {BW}Number of threads                            {RS}")
        print()
        print(f"  {C}[3]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Target URL{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Number of threads{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '3':
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

