#!/usr/bin/env python3
"""Car/Vehicle Lookup - VIN decoder and license plate analysis."""
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

WMI_CODES = {
    "1": "USA", "2": "Canada", "3": "Mexico", "J": "Japan", "K": "Korea",
    "L": "China", "S": "UK", "V": "France", "W": "Germany", "Z": "Italy",
    "Y": "Sweden", "9": "Brazil",
}
MANUFACTURERS = {
    "1G": "Chevrolet (USA)", "1F": "Ford (USA)", "2T": "Toyota (Canada)",
    "3VW": "VW (Mexico)", "JTD": "Toyota (Japan)", "KMH": "Hyundai (Korea)",
    "WAU": "Audi (Germany)", "WBA": "BMW (Germany)", "WDB": "Mercedes (Germany)",
    "SAJ": "Jaguar (UK)", "VF1": "Renault (France)", "ZFF": "Ferrari (Italy)",
    "YV1": "Volvo (Sweden)", "9BW": "VW (Brazil)", "1GC": "Chevrolet Truck",
    "5YJ": "Tesla (USA)", "1C4": "Chrysler", "2HG": "Honda (Canada)",
    "JMZ": "Mazda (Japan)", "KNM": "Kia (Korea)",
}

def decode_vin(vin):
    if len(vin) != 17: return {"error": "VIN must be 17 characters"}
    result = {
        "vin": vin, "wmi": vin[:3], "year_code": vin[9],
        "serial": vin[10:], "check_digit": vin[8],
    }
    wmi_first = vin[0]
    result["country"] = WMI_CODES.get(wmi_first, "Unknown")
    for code, mfr in MANUFACTURERS.items():
        if vin[:len(code)] == code:
            result["manufacturer"] = mfr
            break
    result.setdefault("manufacturer", "Unknown")
    years = "0123456789ABCDEFGHJKLMNPRSTUVWXYZ"
    year_map = dict(zip(years, range(1980, 2041)))
    result["year"] = year_map.get(vin[9], "Unknown")
    return result

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Vehicle / VIN Lookup{RS}")
    print(f"{Y}{'─'*55}{RS}")
    
    print(f"\n  {R}[1] {BW}VIN Decoder{RS}")
    print(f"  {G}[2] {BW}License Plate Search{RS}")
    print(f"  {C}[0] {BW}Exit{RS}")
    
    choice = input(f"\n  {BG}root{RS}@{BR}hellsociety{RS}:{BG}~{RS}$ {BW}")
    
    if choice == "1":
        vin = input(f"  {C}[*] Enter VIN: {RS}").strip().upper()
        if len(vin) == 17:
            result = decode_vin(vin)
            print(f"\n  {Y}[+] VIN Decode Results:{RS}")
            for k, v in result.items():
                print(f"    {C}{k:15}: {BW}{v}{RS}")
            print(f"\n  {G}[+] Search on: https://www.vehiclehistory.com/vin-decode/{vin}{RS}")
        else:
            print(f"  {R}[!] Invalid VIN length{RS}")
    elif choice == "2":
        plate = input(f"  {C}[*] Enter plate number: {RS}").strip()
        state = input(f"  {C}[*] Enter state/country: {RS}").strip()
        print(f"\n  {Y}[+] Check on:{RS}")
        print(f"  {G}[+] https://www.vehiclehistory.com/plate-lookup/{state}/{plate}{RS}")
        print(f"  {G}[+] https://www.nhtsa.gov/plate-lookup/{plate}{RS}")
    else:
        print(f"  {R}[!] Invalid option{RS}")
    
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
