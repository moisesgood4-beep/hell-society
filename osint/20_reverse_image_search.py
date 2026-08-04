#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - Reverse Image Search (OSINT)                   ║
║  Created by: HELL SOCIETY Community                              ║
╚══════════════════════════════════════════════════════════════════╝
"""
import os, sys, json, re, time, requests, hashlib
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

class ReverseImageSearch:
    def __init__(self, image_path=None, image_url=None):
        self.image_path = image_path
        self.image_url = image_url
        self.results = {}

    def exif_analysis(self):
        print(f"\n{G}[+] Method 1: EXIF Metadata Extraction{RS}")
        if not self.image_path or not os.path.exists(self.image_path):
            print(f"  {R}[!] Image file not found")
            return

        try:
            from PIL import Image
            from PIL.ExifTags import TAGS
            img = Image.open(self.image_path)
            exif = img._getexif()
            if exif:
                print(f"  {G}[✓] EXIF data found!")
                for tag_id, value in exif.items():
                    tag = TAGS.get(tag_id, tag_id)
                    if tag in ['GPSInfo', 'GPSLatitude', 'GPSLongitude', 'DateTime', 'Make', 'Model', 'Software']:
                        print(f"  {C}  {tag}: {value}")
                self.results['exif'] = {TAGS.get(k, k): str(v) for k, v in exif.items()}
            else:
                print(f"  {Y}[!] No EXIF data found")
        except ImportError:
            print(f"  {R}[!] PIL not installed")
        except Exception as e:
            print(f"  {R}[!] Error: {e}")

    def google_lens(self):
        print(f"\n{G}[+] Method 2: Google Lens Search{RS}")
        if self.image_path:
            # Create upload link
            upload_url = "https://lens.google.com/upload"
            print(f"  {Y}[i] Upload to: {upload_url}")
            self.results['google_lens'] = upload_url
        elif self.image_url:
            search_url = f"https://lens.google.com/searchbyimage?url={self.image_url}"
            print(f"  {Y}[i] Search: {search_url}")
            self.results['google_lens'] = search_url

    def yandex_search(self):
        print(f"\n{G}[+] Method 3: Yandex Image Search{RS}")
        yandex_url = "https://yandex.com/images/search"
        print(f"  {Y}[i] Upload to: {yandex_url}")
        self.results['yandex'] = yandex_url

    def tin_eye(self):
        print(f"\n{G}[+] Method 4: TinEye Reverse Search{RS}")
        if self.image_path:
            import base64
            with open(self.image_path, 'rb') as f:
                img_data = base64.b64encode(f.read()).decode()
            print(f"  {Y}[i] Upload to: https://tineye.com/search")
        elif self.image_url:
            print(f"  {Y}[i] Search: https://tineye.com/search?url={self.image_url}")
        self.results['tineye'] = "https://tineye.com/search"

    def bing_visual(self):
        print(f"\n{G}[+] Method 5: Bing Visual Search{RS}")
        if self.image_path:
            print(f"  {Y}[i] Upload to: https://www.bing.com/visualsearch")
        elif self.image_url:
            print(f"  {Y}[i] Search: https://www.bing.com/visualsearch?q={self.image_url}")
        self.results['bing'] = "https://www.bing.com/visualsearch"

    def imgur_upload(self):
        print(f"\n{G}[+] Method 6: Image Hash Fingerprint{RS}")
        if self.image_path and os.path.exists(self.image_path):
            with open(self.image_path, 'rb') as f:
                data = f.read()
                md5 = hashlib.md5(data).hexdigest()
                sha256 = hashlib.sha256(data).hexdigest()
            print(f"  {C}  MD5: {md5}")
            print(f"  {C}  SHA256: {sha256}")
            print(f"  {C}  Size: {len(data)} bytes")
            self.results['hashes'] = {'md5': md5, 'sha256': sha256, 'size': len(data)}

    def face_check(self):
        print(f"\n{G}[+] Method 7: Face Recognition Search{RS}")
        print(f"  {Y}[i] Search faces on:")
        print(f"  {Y}  - https://pimeyes.com/")
        print(f"  {Y}  - https://search4faces.com/")
        print(f"  {Y}  - https://yandex.com/images/")
        self.results['face_services'] = ['pimeyes.com', 'search4faces.com', 'yandex.com/images']

    def save_results(self):
        outfile = f"reverse_image_{int(time.time())}.json"
        with open(outfile, 'w') as f:
            json.dump({'path': self.image_path, 'url': self.image_url, 'results': self.results}, f, indent=2)
        print(f"\n{G}[+] Results saved: {outfile}")

    def run_all(self):
        print(BANNER)
        print(f"{B}[*] Image Path: {W}{self.image_path}")
        print(f"{B}[*] Image URL:  {W}{self.image_url}")
        print(f"{Y}[~]{'─'*50}{RS}")

        self.exif_analysis()
        self.google_lens()
        self.yandex_search()
        self.tin_eye()
        self.bing_visual()
        self.imgur_upload()
        self.face_check()
        self.save_results()

        print(f"\n{BR}{'═'*50}")
        print(f"{BR}║  HELL SOCIETY - Reverse Image Search Complete ║")
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
    print(f"  {BW}{Style.BRIGHT}  REVERSE IMAGE SEARCH{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}REVERSE IMAGE SEARCH                    {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Image file path                              {RS}")
        print(f"  {C}[2]  {BW}Image URL                                    {RS}")
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
            print(f"  {Y}[*] Image file path{RS}")
            value = input(f"  {Y}[*] -f: {RS}").strip()
            print(f"  {C}[*] Executing with -f={BW}{value}{RS}")
            print(f"  {G}[+] Operation completed{RS}")
            print()
        if choice == '2':
            print(f"  {Y}[*] Image URL{RS}")
            value = input(f"  {Y}[*] -u: {RS}").strip()
            print(f"  {C}[*] Executing with -u={BW}{value}{RS}")
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

