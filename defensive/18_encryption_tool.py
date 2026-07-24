#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  FILE ENCRYPTION/DECRYPTION TOOL v2.0                            ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Defensive - Data Protection                           ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import colorama
from colorama import Fore, Back, Style
import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

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

class Encryptor:
    def __init__(self, password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'hellsociety',
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)

    def encrypt_file(self, filepath, output_path=None):
        if not output_path:
            output_path = filepath + '.enc'

        with open(filepath, 'rb') as f:
            data = f.read()

        encrypted = self.cipher.encrypt(data)

        with open(output_path, 'wb') as f:
            f.write(encrypted)

        print(f"  {Fore.GREEN}[+] Encrypted: {filepath} -> {output_path}")
        print(f"  {Fore.GREEN}[+] Original size: {len(data)} bytes")
        print(f"  {Fore.GREEN}[+] Encrypted size: {len(encrypted)} bytes")

    def decrypt_file(self, filepath, output_path=None):
        if not output_path:
            output_path = filepath.replace('.enc', '')

        with open(filepath, 'rb') as f:
            data = f.read()

        decrypted = self.cipher.decrypt(data)

        with open(output_path, 'wb') as f:
            f.write(decrypted)

        print(f"  {Fore.GREEN}[+] Decrypted: {filepath} -> {output_path}")
        print(f"  {Fore.GREEN}[+] Size: {len(decrypted)} bytes")

    def encrypt_directory(self, dirpath, password):
        for root, dirs, files in os.walk(dirpath):
            for filename in files:
                if not filename.endswith('.enc'):
                    filepath = os.path.join(root, filename)
                    self.encrypt_file(filepath)

    def encrypt_string(self, text):
        encrypted = self.cipher.encrypt(text.encode())
        print(f"  {Fore.GREEN}[+] Encrypted: {encrypted.decode()}")
        return encrypted

    def decrypt_string(self, token):
        decrypted = self.cipher.decrypt(token.encode())
        print(f"  {Fore.GREEN}[+] Decrypted: {decrypted.decode()}")
        return decrypted

def main():
    print(BANNER)

    parser = argparse.ArgumentParser(description='Hell Society Encryption Tool')
    parser.add_argument('--encrypt', metavar='FILE', help='Encrypt file')
    parser.add_argument('--decrypt', metavar='FILE', help='Decrypt file')
    parser.add_argument('--encrypt-dir', metavar='DIR', help='Encrypt directory')
    parser.add_argument('--decrypt-string', metavar='TOKEN', help='Decrypt string')
    parser.add_argument('--encrypt-string', metavar='TEXT', help='Encrypt string')
    parser.add_argument('-p', '--password', required=True, help='Password')
    parser.add_argument('-o', '--output', help='Output path')
    args = parser.parse_args()

    encryptor = Encryptor(args.password)

    if args.encrypt:
        encryptor.encrypt_file(args.encrypt, args.output)
    elif args.decrypt:
        encryptor.decrypt_file(args.decrypt, args.output)
    elif args.encrypt_dir:
        encryptor.encrypt_directory(args.encrypt_dir, args.password)
        print(f"\n  {Fore.GREEN}[OK] Directory encrypted")
    elif args.encrypt_string:
        encryptor.encrypt_string(args.encrypt_string)
    elif args.decrypt_string:
        encryptor.decrypt_string(args.decrypt_string)
    else:
        print(f"  {Fore.YELLOW}Usage examples:")
        print(f"  {Fore.CYAN}  --encrypt file.txt -p password123")
        print(f"  {Fore.CYAN}  --decrypt file.txt.enc -p password123")
        print(f"  {Fore.CYAN}  --encrypt-dir /path/to/dir -p password123")
        print(f"  {Fore.CYAN}  --encrypt-string 'secret text' -p password123")

if __name__ == "__main__":
    main()
