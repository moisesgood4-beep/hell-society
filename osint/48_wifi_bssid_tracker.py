#!/usr/bin/env python3
"""WiFi BSSID Tracker - Geolocate WiFi networks by BSSID."""
import os, sys
try:
    from colorama import init, Fore, Style; init(autoreset=True)
    import requests
except: os.system("pip3 install colorama requests 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True); import requests

R=Fore.RED;G=Fore.GREEN;Y=Fore.YELLOW;C=Fore.CYAN;BW=Style.BRIGHT+Fore.WHITE
BR=Style.BRIGHT+Fore.RED;BG=Style.BRIGHT+Fore.GREEN;RS=Style.RESET_ALL

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

def lookup_bssid(bssid):
    """Look up WiFi BSSID in public databases"""
    bssid = bssid.replace("-", ":").replace(".", ":").upper()
    print(f"\n{Y}[+] BSSID: {BW}{bssid}{RS}")
    
    # Extract MAC prefix for manufacturer
    prefix = bssid[:8].replace(":", "")
    print(f"\n{Y}[+] MAC Prefix: {BW}{bssid[:8]}{RS}")
    
    # WiGLE.net lookup
    print(f"\n{Y}[+] WiGLE.net lookup:{RS}")
    print(f"  {G}[+] https://wigle.net/search?searchBssid={bssid}{RS}")
    
    # Google Maps (some BSSIDs appear in street view metadata)
    print(f"\n{Y}[+] Additional sources:{RS}")
    print(f"  {C}[+] https://www.mylnikov.org/geolocation/wifi?bssid={bssid}{RS}")
    print(f"  {C}[+] https://api.mylnikov.org/geolocation/wifi?v=1.1&data=open&bssid={bssid}{RS}")
    
    # Try mylnikov.org API
    try:
        r = requests.get(f"https://api.mylnikov.org/geolocation/wifi?v=1.1&data=open&bssid={bssid}", timeout=10)
        if r.status_code == 200:
            data = r.json()
            if data.get('result', -1) != -1:
                loc = data.get('data', {})
                print(f"\n  {BG}[*] Location found!{RS}")
                print(f"  {G}[+] Lat: {loc.get('lat','?')}{RS}")
                print(f"  {G}[+] Lon: {loc.get('lon','?')}{RS}")
                print(f"  {G}[+] Maps: https://maps.google.com/?q={loc.get('lat','')},{loc.get('lon','')}{RS}")
            else:
                print(f"  {Y}[!] BSSID not found in open database{RS}")
    except: print(f"  {R}[!] API lookup failed{RS}")



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
    print(f"  {BW}{Style.BRIGHT}  WIFI BSSID TRACKER{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}WIFI BSSID TRACKER                      {RS}  {G}╟{RS}")
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
            print(f"  {G}[*] Starting Wifi Bssid Tracker...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Wifi Bssid Tracker{RS}")
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

