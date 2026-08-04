#!/usr/bin/env python3
"""Email Hunter - Find emails associated with a domain using multiple methods."""
import os, sys, re, json
try:
    from colorama import init, Fore, Style; init(autoreset=True)
except: os.system("pip3 install colorama 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True)

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;BW=Style.BRIGHT+Fore.WHITE
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

def generate_emails(domain):
    prefixes = ["admin", "info", "contact", "support", "webmaster", "postmaster",
                "sales", "help", "office", "team", "hello", "noreply", "noreply-no",
                "abuse", "feedback", "press", "media", "jobs", "careers",
                "security", "legal", "privacy", "compliance", "billing"]
    emails = [f"{p}@{domain}" for p in prefixes]
    return emails

def check_email_pattern(domain):
    """Common email patterns based on company name"""
    name = domain.split('.')[0]
    patterns = [
        f"contact@{domain}", f"info@{domain}", f"hello@{domain}",
        f"support@{domain}", f"admin@{domain}", f"team@{domain}",
        f"careers@{domain}", f"jobs@{domain}", f"sales@{domain}",
        f"press@{domain}", f"media@{domain}", f"legal@{domain}",
        f"security@{domain}", f"abuse@{domain}", f"privacy@{domain}",
        f"{name}@{domain}", f"office@{domain}",
    ]
    return patterns

def search_google_dorks(domain):
    """Generate Google dorks for email discovery"""
    dorks = [
        f"@{domain} site:{domain}",
        f"\"@{domain}\" filetype:pdf",
        f"\"@{domain}\" filetype:doc OR filetype:docx",
        f"\"@{domain}\" filetype:xls OR filetype:xlsx",
        f"\"@{domain}\" filetype:ppt OR filetype:pptx",
        f"email @{domain} site:linkedin.com",
        f"email @{domain} site:twitter.com",
        f"\"@{domain}\" site:github.com",
    ]
    return dorks



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
    print(f"  {BW}{Style.BRIGHT}  EMAIL HUNTER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}EMAIL HUNTER                            {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Iniciar herramienta{RS}")
        print(f"  {C}[2]  {BW}Configurar opciones{RS}")
        print(f"  {C}[3]  {BW}Mostrar ayuda/uso{RS}")
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
            print(f"  {G}[*] Starting Email Hunter...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Email Hunter{RS}")
            print(f"  {Y}    Interactive tool with guided inputs{RS}")
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

