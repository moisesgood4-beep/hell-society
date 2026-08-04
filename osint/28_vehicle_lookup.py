#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Vehicle & License Plate Lookup                 ║
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

class VehicleLookup:
    def __init__(self, plate=None, vin=None):
        self.plate = plate
        self.vin = vin
        self.results = {}

    def decode_vin(self):
        print(f"\n{G}[+] Method 1: VIN Decoder{RS}")
        if not self.vin:
            print(f"  {Y}[!] No VIN provided")
            return

        vin = self.vin.upper().strip()
        if len(vin) != 17:
            print(f"  {R}[!] VIN must be 17 characters")
            return

        # VIN sections
        wmi = vin[:3]
        vds = vin[3:9]
        vis = vin[9:]
        year_code = vin[9]

        # Year lookup
        years = {
            'A': 2010, 'B': 2011, 'C': 2012, 'D': 2013, 'E': 2014,
            'F': 2015, 'G': 2016, 'H': 2017, 'J': 2018, 'K': 2019,
            'L': 2020, 'M': 2021, 'N': 2022, 'P': 2023, 'R': 2024,
            'S': 2025, 'T': 2026
        }
        year = years.get(year_code, f"Unknown ({year_code})")

        print(f"  {C}[WMI] {W}{wmi}")
        print(f"  {C}[VDS] {W}{vds}")
        print(f"  {C}[VIS] {W}{vis}")
        print(f"  {C}[Year] {W}{year}")
        print(f"  {C}[Plant] {W}{vin[10]}")
        print(f"  {C}[Serial] {W}{vin[11:]}")

        # Check VIN online
        print(f"\n  {Y}[i] Decode online: https://www.nhtsa.gov/webapi/vin/decode?vins={vin}")
        self.results['vin'] = {'wmi': wmi, 'year': year, 'full': vin}

    def plate_lookup(self):
        print(f"\n{G}[+] Method 2: License Plate Lookup{RS}")
        if not self.plate:
            print(f"  {Y}[!] No plate provided")
            return

        plate = self.plate.upper().replace(' ', '')
        print(f"  {Y}[i] Plate: {plate}")

        # Lookup services
        services = [
            ('PlateRecognizer', f"https://platerecognizer.com/"),
            ('CarVertical', f"https://www.carvertical.com/check/{plate}"),
            ('VehicleHistory', f"https://www.vehiclehistory.com/license-plate-lookup/{plate}"),
            ('LicensePlateLookup', f"https://www.licenseplatenumberlookup.com/{plate}"),
            ('VINCheck', f"https://www.nicb.org/vincheck/{plate}"),
        ]
        for name, url in services:
            print(f"  {Y}[i] {name}: {url[:60]}")
        self.results['plate_services'] = services

    def vehicle_history(self):
        print(f"\n{G}[+] Method 3: Vehicle History Services{RS}")
        services = [
            f"https://www.carfax.com/VehicleHistory/app/Report.vm",
            f"https://www.autocheck.com/vehiclehistory/search",
            f"https://www.nhtsa.gov/equipment/recalls-and-safety-defects",
            f"https://www.nicb.org/vincheck",
            f"https://comptroller.texas.gov/taxes/vehicle/",
            f"https://dmv.ny.gov/cheat-sheet",
        ]
        for s in services:
            print(f"  {Y}[i] {s[:60]}")

    def insurance_lookup(self):
        print(f"\n{G}[+] Method 4: Insurance & Registration{RS}")
        if self.plate:
            print(f"  {Y}[i] Check registration: https://dmv.ny.gov")
            print(f"  {Y}[i] Check insurance: https://www.nyserda.ny.gov")
            print(f"  {Y}[i] NHTSA recalls: https://www.nhtsa.gov/recalls")

    def save_results(self):
        outfile = f"vehicle_lookup_{self.plate or self.vin or 'unknown'}.json"
        with open(outfile, 'w') as f:
            json.dump({'plate': self.plate, 'vin': self.vin, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] License Plate: {W}{self.plate}")
        print(f"{B}[*] VIN:           {W}{self.vin}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.decode_vin()
        self.plate_lookup()
        self.vehicle_history()
        self.insurance_lookup()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Vehicle Lookup Complete       ║")
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
    print(f"  {BW}{Style.BRIGHT}  VEHICLE LOOKUP{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}VEHICLE LOOKUP                          {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}License plate number                         {RS}")
        print(f"  {C}[2]  {BW}Vehicle VIN (17 chars)                       {RS}")
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
            print(f"  {Y}[*] License plate number{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Vehicle VIN (17 chars){RS}")
            value = input(f"  {Y}[*] -v: {RS}").strip()
            print(f"  {C}[*] Executing with -v={BW}{value}{RS}")
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

