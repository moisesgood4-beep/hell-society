#!/usr/bin/env python3
"""Crypto Wallet Tracker - Track cryptocurrency wallet addresses and transactions."""
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

WALLET_EXPLORERS = {
    "BTC": "https://blockchain.com/btc/address/{addr}",
    "ETH": "https://etherscan.io/address/{addr}",
    "BNB": "https://bscscan.com/address/{addr}",
    "SOL": "https://solscan.io/account/{addr}",
    "ADA": "https://cardanoscan.io/address/{addr}",
    "DOT": "https://polkascan.io/polkadot/account/{addr}",
    "MATIC": "https://polygonscan.com/address/{addr}",
    "AVAX": "https://snowtrace.io/address/{addr}",
}

def detect_chain(addr):
    if addr.startswith("1") or addr.startswith("3") or addr.startswith("bc1"): return "BTC"
    if addr.startswith("0x") and len(addr) == 42: return "ETH"
    if len(addr) == 44: return "SOL"
    return "UNKNOWN"

def check_wallet(addr):
    chain = detect_chain(addr)
    print(f"\n{Y}[+] Detected chain: {BW}{chain}{RS}")
    print(f"\n{Y}[+] Wallet explorers:{RS}")
    
    for name, template in WALLET_EXPLORERS.items():
        url = template.format(addr=addr)
        print(f"  {G}[+] {BW}{name:10}{RS} {url}")
    
    # Try blockchain.info API for BTC
    if chain == "BTC":
        try:
            r = requests.get(f"https://blockchain.info/rawaddr/{addr}?limit=5", timeout=10)
            if r.status_code == 200:
                data = r.json()
                print(f"\n  {G}[+] Balance: {data.get('final_balance', 0) / 1e8} BTC{RS}")
                print(f"  {G}[+] Transactions: {data.get('n_tx', 0)}{RS}")
                for tx in data.get('txs', [])[:3]:
                    print(f"  {C}├─ TX: {tx.get('hash','?')[:30]}...{RS}")
        except: print(f"\n  {R}[!] API lookup failed{RS}")
    elif chain == "ETH":
        try:
            r = requests.get(f"https://api.etherscan.io/api?module=account&action=balance&address={addr}&tag=latest", timeout=10)
            if r.status_code == 200:
                data = r.json()
                if data.get('status') == '1':
                    print(f"\n  {G}[+] Balance: {int(data.get('result', 0)) / 1e18} ETH{RS}")
        except: print(f"\n  {R}[!] API lookup failed{RS}")

def main():
    clear(); print(BANNER); print(); print(DISCLAIMER); print()
    print(f"{BG}[+] {BW}Crypto Wallet Tracker{RS}")
    print(f"{Y}{'─'*55}{RS}")
    addr = input(f"\n{C}[*] Enter wallet address: {RS}").strip()
    if not addr: sys.exit(1)
    check_wallet(addr)
    print(f"\n{BW}{R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"{BW}{R}║  HELL SOCIETY - NO LIABILITY FOR MISUSE                        ║{RS}")
    print(f"{BW}{R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    input(f"\n{Y}[i] Press Enter to exit...{RS}")

if __name__ == "__main__": main()
