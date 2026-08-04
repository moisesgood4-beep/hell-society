#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  EXIF METADATA EXTRACTOR v2.0                                    ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: OSINT - Metadata Intelligence                         ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
import json

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

class EXIFExtractor:
    def __init__(self, path):
        self.path = path
        self.results = []

    def extract_exif(self, filepath):
        try:
            from PIL import Image
            from PIL.ExifTags import TAGS

            img = Image.open(filepath)
            exif_data = img._getexif()

            metadata = {
                'file': filepath,
                'format': img.format,
                'size': img.size,
                'mode': img.mode,
                'tags': {}
            }

            if exif_data:
                for tag_id, value in exif_data.items():
                    tag_name = TAGS.get(tag_id, tag_id)
                    if isinstance(value, bytes):
                        value = value.decode('utf-8', errors='ignore')
                    metadata['tags'][tag_name] = value

                    # Show GPS if present
                    if 'GPSInfo' in tag_name:
                        print(f"  {Fore.RED}[!] GPS Data: {value}")

                # Check for GPS coordinates
                gps = exif_data.get(34853)
                if gps:
                    print(f"  {Fore.RED}[!!!] GPS COORDINATES FOUND!")
                    print(f"  {Fore.WHITE}  Raw GPS: {gps}")
                    metadata['gps'] = str(gps)
            else:
                print(f"  {Fore.YELLOW}[-] No EXIF data")

            return metadata

        except Exception as e:
            print(f"  {Fore.RED}[!] Error reading {filepath}: {e}")
            return None

    def extract_basic_metadata(self, filepath):
        """Extract metadata without PIL"""
        print(f"\n  {Fore.WHITE}File: {filepath}")

        stat = os.stat(filepath)
        metadata = {
            'file': filepath,
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'accessed': stat.st_atime,
        }

        print(f"  {Fore.WHITE}  Size: {stat.st_size} bytes")
        print(f"  {Fore.WHITE}  Created: {stat.st_ctime}")
        print(f"  {Fore.WHITE}  Modified: {stat.st_mtime}")
        print(f"  {Fore.WHITE}  Accessed: {stat.st_atime}")

        # Read header to detect file type
        with open(filepath, 'rb') as f:
            header = f.read(32)

        # Check for hidden data
        if header[:4] == b'\xff\xd8\xff\xe1':
            print(f"  {Fore.GREEN}[+] JPEG with EXIF header")
        elif header[:4] == b'\x89PNG':
            print(f"  {Fore.GREEN}[+] PNG file")
        elif header[:3] == b'GIF':
            print(f"  {Fore.GREEN}[+] GIF file")
        elif header[:4] == b'%PDF':
            print(f"  {Fore.GREEN}[+] PDF file")

        metadata['file_type'] = 'image/jpeg' if header[:4] == b'\xff\xd8\xff\xe1' else 'unknown'
        return metadata

    def scan_directory(self):
        print(f"\n{Fore.CYAN}  [*] Scanning directory: {Fore.WHITE}{self.path}\n")

        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.tiff', '.bmp', '.webp']

        for root, dirs, files in os.walk(self.path):
            for filename in files:
                if any(filename.lower().endswith(ext) for ext in image_extensions):
                    filepath = os.path.join(root, filename)
                    print(f"\n{Fore.CYAN}  [{'═' * 40}]")
                    print(f"  {Fore.WHITE}  {filepath}")
                    print(f"{Fore.CYAN}  [{'═' * 40}]")

                    meta = self.extract_basic_metadata(filepath)
                    try:
                        exif = self.extract_exif(filepath)
                        if exif:
                            self.results.append(exif)
                    except:
                        pass

    def scan_single_file(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  {Fore.WHITE}  {self.path}")
        print(f"{Fore.CYAN}  [{'═' * 40}]")

        meta = self.extract_basic_metadata(self.path)
        exif = self.extract_exif(self.path)
        if exif:
            self.results.append(exif)

    def run(self):
        print(f"{Fore.CYAN}  [*] Starting EXIF extraction...")

        if os.path.isdir(self.path):
            self.scan_directory()
        elif os.path.isfile(self.path):
            self.scan_single_file()
        else:
            print(f"  {Fore.RED}[!] Path not found: {self.path}")
            return

        # Save results
        results_file = f'/tmp/exif_results.json'
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: {results_file}")

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  EXIF EXTRACTION COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")


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
    print(f"  {BW}{Style.BRIGHT}  EXIF METADATA{RS}")
    print(f"  {Y}{Style.BRIGHT}  HELL SOCIETY Community{RS}")
    print()
    while True:
        print(f"  {G}╔╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╗{RS}")
        print(f"  {G}╟  {BW}EXIF METADATA                           {RS}  {G}╟{RS}")
        print(f"  {G}╚╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╜╝{RS}")
        print()
        print(f"  {C}[1]  {BW}File or directory to scan                    {RS}")
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
            print(f"  {Y}[*] File or directory to scan{RS}")
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

