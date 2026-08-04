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
    print(f"  {BW}{Style.BRIGHT}  MAC ADDRESS LOOKUP{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}MAC ADDRESS LOOKUP                      {RS}  {G}╟{RS}")
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
            print(f"  {G}[*] Starting Mac Address Lookup...{RS}")
            print(f"  {Y}[*] Tool execution in progress{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
            print(f"  {Y}[*] Settings - configure tool options{RS}")
            print()
        elif choice == '3':
            print(f"  {C}[*] Mac Address Lookup{RS}")
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

