#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HACKING TOOL - HELL SOCIETY                                    ║
# ║  Created by: HELL SOCIETY Community                              ║
# ║  Professional Pentesting Framework                               ║
# ╚══════════════════════════════════════════════════════════════════╝

import os, sys, json
try:
    from colorama import init, Fore, Style; init(autoreset=True)
except: os.system("pip3 install colorama 2>/dev/null"); from colorama import init, Fore, Style; init(autoreset=True)

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN; M = Fore.MAGENTA; BW = Style.BRIGHT+Fore.WHITE
BR = Style.BRIGHT+Fore.RED; BG = Style.BRIGHT+Fore.GREEN; BY = Style.BRIGHT+Fore.YELLOW; BC = Style.BRIGHT+Fore.CYAN
RS = Style.RESET_ALL

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

DISCLAIMER = f"""{R}╔══════════════════════════════════════════════════════════════════╗
║ {BW}DISCLAIMER: Developers assume no liability and are not            ║
║ {BW}responsible for any misuse or damage caused.                      ║
║ {BW}Only use for educational purposes!!                               ║
║ {BG}Attacking targets without mutual consent is illegal!!{RS}  {R}║
╚══════════════════════════════════════════════════════════════════╝{RS}"""

def clear(): os.system('clear' if os.name != 'nt' else 'cls')

OUI_DB = {
    "00:0C:29": "VMware", "00:50:56": "VMware", "08:00:27": "Oracle/VirtualBox",
    "52:54:00": "QEMU/KVM", "00:16:3E": "Xen", "00:03:FF": "Microsoft Virtual PC",
    "AA:BB:CC": "Custom/Randomized", "00:11:22": "Custom/Randomized",
    "D0:81:7A": "ASRock", "74:D4:35": "ASUS", "C8:60:00": "ASUS",
    "3C:D9:2B": "ASUS", "A4:83:E7": "Razer", "98:22:6E": "Intel",
    "B0:6E:BF": "Intel", "00:1B:63": "Intel", "AC:B5:7D": "Wacom",
    "20:68:9D": "TP-Link", "50:91:E3": "TP-Link", "10:27:F5": "TP-Link",
    "7C:10:C9": "ASUS", "F0:18:98": "Apple", "DC:A6:32": "Apple",
    "A8:60:B6": "Apple", "F8:FF:C2": "Apple", "48:D7:05": "Apple",
    "A4:5E:60": "Apple", "D0:03:4B": "Apple", "C8:1E:8E": "Samsung",
    "94:D9:B3": "Samsung", "5C:CB:99": "Samsung", "00:26:B0": "Samsung",
    "F0:9F:C2": "Huawei", "30:87:30": "Huawei", "14:75:90": "TP-Link",
    "00:50:B6": "Nokia", "00:23:CD": "Apple", "34:23:BA": "Apple",
}

def lookup_mac(mac):
    mac = mac.replace("-", ":").replace(".", ":").upper()
    parts = mac.split(":")
    if len(parts) < 3: return {"error": "Invalid MAC format"}
    oui = ":".join(parts[:3])
    vendor = OUI_DB.get(oui, "Unknown/Private")
    is_local = (int(parts[0], 16) & 0x02) != 0
    is_unicast = (int(parts[0], 16) & 0x01) == 0
    return {
        "mac": mac, "oui": oui, "vendor": vendor,
        "is_local_assigned": is_local, "is_unicast": is_unicast,
        "is_virtual": vendor in ["VMware", "Oracle/VirtualBox", "QEMU/KVM", "Xen", "Microsoft Virtual PC"],
        "is_mobile": vendor in ["Apple", "Samsung", "Huawei", "Nokia", "Xiaomi"],
        "is_router": vendor in ["TP-Link", "ASUS", "ASRock", "Intel"],
    }

def mac_randomize(mac):
    import random
    parts = mac.split(":")
    octet0 = (int(parts[0], 16) & 0xFC) | 0x02
    return f"{octet0:02X}:" + ":".join(f"{random.randint(0,255):02X}" for _ in range(5))

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}MAC Address Lookup Tool{RS}")
    print(f"{Y}{'─'*55}{RS}")
    mac = input(f"\n{C}[*] Enter MAC address: {RS}").strip()
    if not mac:
        print(f"{R}[!] No MAC provided{RS}")
        sys.exit(1)
    result = lookup_mac(mac)
    print(f"\n{Y}[+] {BW}Results:{RS}")
    for k, v in result.items():
        color = G if k == "vendor" and v != "Unknown/Private" else R if "error" in k else Y
        print(f"  {C}{k:25}{RS}: {color}{v}{RS}")
    if result.get("is_virtual"):
        print(f"\n{R}[!] Virtual machine detected!{RS}")
    if result.get("is_mobile"):
        print(f"\n{M}[!] Mobile device detected!{RS}")
    print(f"\n{G}[*] Randomized MAC: {mac_randomize(mac)}{RS}")
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
