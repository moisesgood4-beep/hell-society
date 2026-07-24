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

def main():
    print(BANNER)
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--plate', help='License plate number')
    parser.add_argument('-v', '--vin', help='Vehicle VIN (17 chars)')
    args = parser.parse_args()
    lookup = VehicleLookup(args.plate, args.vin)
    lookup.run_all()

if __name__ == "__main__":
    main()
