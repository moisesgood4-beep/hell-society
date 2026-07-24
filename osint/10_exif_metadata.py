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

BANNER = f"""
{Fore.MAGENTA}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ███████╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗               {Fore.MAGENTA}║
║{Fore.CYAN}  ██╔════╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║               {Fore.MAGENTA}║
║{Fore.CYAN}  ███████╗ ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║               {Fore.MAGENTA}║
║{Fore.CYAN}  ╚════██║  ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║               {Fore.MAGENTA}║
║{Fore.CYAN}  ███████║   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║               {Fore.MAGENTA}║
║{Fore.CYAN}  ╚══════╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝               {Fore.MAGENTA}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - EXIF Metadata Extractor v2.0                     {Fore.MAGENTA}║
╚══════════════════════════════════════════════════════════════════╝
"""

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

if __name__ == "__main__":
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society EXIF Extractor')
    parser.add_argument('-p', '--path', required=True, help='File or directory to scan')
    args = parser.parse_args()

    extractor = EXIFExtractor(args.path)
    extractor.run()
