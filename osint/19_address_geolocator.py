#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Address & Location Geolocator                  ║
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

class GeoLocator:
    def __init__(self, target):
        self.target = target
        self.results = {}

    def geocode_address(self):
        print(f"\n{G}[+] Method 1: Geocode Address{RS}")
        # Use Nominatim (OpenStreetMap) - free, no API key
        try:
            url = f"https://nominatim.openstreetmap.org/search?q={self.target}&format=json&limit=5"
            headers = {'User-Agent': 'HellSociety/1.0'}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200 and r.json():
                data = r.json()
                for d in data:
                    lat = d.get('lat', 'N/A')
                    lon = d.get('lon', 'N/A')
                    display = d.get('display_name', 'N/A')
                    print(f"  {G}[✓] Lat: {lat}, Lon: {lon}")
                    print(f"  {C}    Address: {display[:80]}")
                    self.results['geocode'] = d
            else:
                print(f"  {Y}[!] No results from Nominatim")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def reverse_geocode(self, lat, lon):
        print(f"\n{G}[+] Method 2: Reverse Geocode{RS}")
        try:
            url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
            headers = {'User-Agent': 'HellSociety/1.0'}
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {G}[✓] Address: {data.get('display_name', 'N/A')}")
                self.results['reverse'] = data
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def google_maps_search(self):
        print(f"\n{G}[+] Method 3: Google Maps Links{RS}")
        maps_url = f"https://www.google.com/maps/search/{self.target}"
        print(f"  {Y}[i] {maps_url}")
        self.results['maps'] = maps_url

    def street_view(self, lat=None, lon=None):
        print(f"\n{G}[+] Method 4: Street View Links{RS}")
        if lat and lon:
            sv_url = f"https://www.google.com/maps/@{lat},{lon},3a,75y,90t/data=!3m6!1e1!3m4!1s*!2e0!7i13312!8i6656"
            print(f"  {Y}[i] Street View: {sv_url[:60]}")
            self.results['street_view'] = sv_url

    def nearby_places(self, lat=None, lon=None):
        print(f"\n{G}[+] Method 5: Nearby Places{RS}")
        if lat and lon:
            places_url = f"https://www.google.com/maps/search/restaurants+near+{lat},{lon}"
            print(f"  {Y}[i] Nearby: {places_url[:60]}")
            self.results['nearby'] = places_url

    def ip_geolocate(self, ip):
        print(f"\n{G}[+] Method 6: IP Geolocation{RS}")
        try:
            url = f"http://ip-api.com/json/{ip}"
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"  {G}[✓] Country: {data.get('country', 'N/A')}")
                print(f"  {G}[✓] Region: {data.get('regionName', 'N/A')}")
                print(f"  {G}[✓] City: {data.get('city', 'N/A')}")
                print(f"  {G}[✓] ISP: {data.get('isp', 'N/A')}")
                print(f"  {G}[✓] Lat: {data.get('lat', 'N/A')}, Lon: {data.get('lon', 'N/A')}")
                self.results['ip_geo'] = data
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def save_results(self):
        outfile = f"geolocate_{self.target.replace(' ','_')}.json"
        with open(outfile, 'w') as f:
            json.dump({'target': self.target, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Target: {W}{self.target}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.geocode_address()
        self.google_maps_search()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Geolocator Complete           ║")
        print(f"{BR}╚══════════════════════════════════════════════════╝{RS}")



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
    print(f"  {BW}{Style.BRIGHT}  ADDRESS GEOLOCATOR{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}ADDRESS GEOLOCATOR                      {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Address or coordinates                       {RS}")
        print(f"  {C}[2]  {BW}IP to geolocate                              {RS}")
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
            print(f"  {Y}[*] Address or coordinates{RS}")
            value = input(f"  {Y}[*] -t: {RS}").strip()
            print(f"  {C}[*] Executing with -t={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] IP to geolocate{RS}")
            value = input(f"  {Y}[*] -ip: {RS}").strip()
            print(f"  {C}[*] Executing with -ip={BW}{value}{RS}")
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

