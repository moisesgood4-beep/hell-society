#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - CURP WEB EXTRACTOR v1.0                         ║
║  Created by: HELL SOCIETY Community                              ║
║  Extract CURPs from websites, PDFs, and documents                ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: Hell Society assumes no liability for misuse.
"""

import os, sys, re, json, time, hashlib, urllib.parse
from datetime import datetime

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except:
    os.system("pip3 install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import requests
    from bs4 import BeautifulSoup
except:
    os.system("pip3 install requests beautifulsoup4 2>/dev/null")
    import requests
    from bs4 import BeautifulSoup

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN; W = Fore.WHITE
BW = Style.BRIGHT + Fore.WHITE; RS = Style.RESET_ALL

BANNER = f"""{R}⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡄{RS}"""

CURP_PATTERN = r'[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d'
RFC_PATTERN = r'[A-Z&Ñ]{4}\d{6}[A-Z\d]{3}'

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'es-MX,es;q=0.9'
}

# ═══════════════════════════════════════════════════════════════════
# METHOD 1: WEB SCRAPE CURP
# ═══════════════════════════════════════════════════════════════════

def method_web_scrape():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 1: WEB SCRAPE CURP{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    
    url = input(f"  {Y}[*] Target URL: {RS}").strip()
    depth = int(input(f"  {Y}[*] Max depth (1-5): {RS}").strip() or "1")
    
    print(f"\n  {C}[*] Scraping CURPs from {url}...{RS}\n")
    
    found = set()
    visited = set()
    to_visit = [url]
    
    while to_visit and len(visited) < depth * 50:
        current = to_visit.pop(0)
        if current in visited:
            continue
        visited.add(current)
        
        try:
            resp = requests.get(current, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                # Extract CURPs
                matches = re.findall(CURP_PATTERN, resp.text)
                for m in matches:
                    found.add(m)
                
                # Extract RFCs
                rfcs = re.findall(RFC_PATTERN, resp.text)
                for r in rfcs:
                    found.add(f"RFC:{r}")
                
                print(f"  {G}[+] {current}: {len(matches)} CURPs, {len(rfcs)} RFCs{RS}")
                
                # Find more links
                if len(visited) < depth * 50:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if href.startswith('http'):
                            to_visit.append(href)
            
            time.sleep(0.5)
        except Exception as e:
            print(f"  {R}[!] Error on {current}: {e}{RS}")
    
    print(f"\n  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  FOUND: {len(found)} CURPs/RFCs{RS}")
    print(f"  {Y}{'=' * 50}{RS}\n")
    
    for item in sorted(found):
        if item.startswith('RFC:'):
            print(f"  {Y}  {item}{RS}")
        else:
            print(f"  {C}  {item}{RS}")
    
    # Save
    with open('curp_web_results.txt', 'w') as f:
        for item in sorted(found):
            f.write(item + '\n')
    print(f"\n  {G}[+] Saved to: curp_web_results.txt{RS}")

# ═══════════════════════════════════════════════════════════════════
# METHOD 2: PASTEBIN SCANNER
# ═══════════════════════════════════════════════════════════════════

def method_pastebin():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 2: PASTEBIN CURP SCANNER{RS}                 {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    
    keyword = input(f"  {Y}[*] Search keyword (CURP/name/keyword): {RS}").strip()
    
    print(f"\n  {C}[*] Searching Pastebin for CURPs...{RS}\n")
    
    # Pastebin dorks
    searches = [
        f"https://site:pastebin.com/search?q={urllib.parse.quote(keyword+' CURP')}",
        f"https://site:pastebin.com/search?q={urllib.parse.quote(keyword+' RFC')}",
        f"https://site:pastebin.com/search?q={urllib.parse.quote(keyword+' CURP RFC')}",
        f"https://site:pastebin.com/search?q={urllib.parse.quote(keyword+' NOMINA')}",
        f"https://site:pastebin.com/search?q={urllib.parse.quote(keyword+' EMPLEADO')}",
    ]
    
    print(f"  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  PASTEBIN SEARCH LINKS:{RS}")
    print(f"  {Y}{'=' * 50}{RS}\n")
    
    for i, s in enumerate(searches, 1):
        print(f"  {C}[{i:02d}] {BW}{s}{RS}")
        print()
    
    # Also search public pastebin API
    print(f"  {Y}[*] Checking public Pastebin API...{RS}")
    try:
        # Search for recent pastes
        url = f"https://psbdmp.ws/api/v3/search/{urllib.parse.quote(keyword)}"
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            dumps = data.get('dumps', [])
            print(f"  {G}[+] Found {len(dumps)} dumps mentioning '{keyword}'{RS}")
            for d in dumps[:10]:
                print(f"  {C}    - {d.get('title','?')} ({d.get('id','?')}){RS}")
                print(f"  {G}      https://psbdmp.ws/{d.get('id','')}{RS}")
        else:
            print(f"  {Y}[~] API returned {resp.status_code}{RS}")
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")
    
    print(f"\n  {Y}[~] Open the links and search for CURPs manually{RS}")

# ═══════════════════════════════════════════════════════════════════
# METHOD 3: PDF/DOCUMENT EXTRACTOR
# ═══════════════════════════════════════════════════════════════════

def method_document():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 3: DOCUMENT EXTRACTOR{RS}                    {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    
    filepath = input(f"  {Y}[*] File path (TXT/PDF/HTML): {RS}").strip()
    
    if not os.path.isfile(filepath):
        print(f"  {R}[!] File not found{RS}")
        return
    
    print(f"\n  {C}[*] Extracting CURPs from document...{RS}\n")
    
    ext = filepath.lower().split('.')[-1]
    text = ''
    
    if ext == 'txt':
        with open(filepath, 'r', errors='ignore') as f:
            text = f.read()
    elif ext == 'pdf':
        try:
            import subprocess
            result = subprocess.run(['pdftotext', filepath, '-'], capture_output=True, text=True)
            text = result.stdout
        except:
            print(f"  {R}[!] Install pdftotext: pkg install poppler{RS}")
            return
    elif ext in ['html', 'htm']:
        with open(filepath, 'r', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
            text = soup.get_text()
    elif ext in ['csv', 'json', 'xml']:
        with open(filepath, 'r', errors='ignore') as f:
            text = f.read()
    else:
        # Try reading as text
        try:
            with open(filepath, 'r', errors='ignore') as f:
                text = f.read()
        except:
            print(f"  {R}[!] Cannot read file type: {ext}{RS}")
            return
    
    # Extract CURPs
    curps = re.findall(CURP_PATTERN, text)
    rfcs = re.findall(RFC_PATTERN, text)
    
    print(f"  {G}[+] Found {len(curps)} CURPs{RS}")
    print(f"  {G}[+] Found {len(rfcs)} RFCs{RS}")
    
    if curps:
        print(f"\n  {Y}{'=' * 40}{RS}")
        print(f"  {BW}  CURPs:{RS}")
        print(f"  {Y}{'=' * 40}{RS}\n")
        for c in set(curps):
            print(f"  {C}  {c}{RS}")
    
    if rfcs:
        print(f"\n  {Y}{'=' * 40}{RS}")
        print(f"  {BW}  RFCs:{RS}")
        print(f"  {Y}{'=' * 40}{RS}\n")
        for r in set(rfcs):
            print(f"  {Y}  {r}{RS}")
    
    # Save
    with open('curp_doc_results.txt', 'w') as f:
        for c in set(curps): f.write(c + '\n')
        for r in set(rfcs): f.write('RFC:' + r + '\n')
    print(f"\n  {G}[+] Saved to: curp_doc_results.txt{RS}")

# ═══════════════════════════════════════════════════════════════════
# METHOD 4: API ENDPOINT SCANNER
# ═══════════════════════════════════════════════════════════════════

def method_api():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 4: CURP API LOOKUP{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    
    print(f"  {C}Available free CURP APIs:{RS}")
    print()
    print(f"  {C}[1] RENAPO (official){RS}")
    print(f"  {C}[2] Google (dork search){RS}")
    print(f"  {C}[3] Custom endpoint{RS}")
    print()
    
    choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
    
    if choice == '1':
        name = input(f"  {Y}[*] Name: {RS}").strip().upper()
        paternal = input(f"  {Y}[*] Paternal: {RS}").strip().upper()
        maternal = input(f"  {Y}[*] Maternal: {RS}").strip().upper()
        d = input(f"  {Y}[*] Day: {RS}").strip()
        m = input(f"  {Y}[*] Month: {RS}").strip()
        y = input(f"  {Y}[*] Year: {RS}").strip()
        s = input(f"  {Y}[*] Sex (H/M): {RS}").strip().upper()
        st = input(f"  {Y}[*] State: {RS}").strip()
        
        print(f"\n  {C}[*] Querying RENAPO...{RS}")
        try:
            url = "https://consultas.curp.gob.mx/CurpSP/"
            params = {'nombre':name,'paterno':paternal,'materno':maternal,'dia':d,'mes':m,'year':y,'sexo':s,'entidad':st}
            resp = requests.get(url, params=params, headers=HEADERS, timeout=15)
            if resp.status_code == 200:
                matches = re.findall(CURP_PATTERN, resp.text)
                if matches:
                    print(f"  {G}[+] CURP: {BW}{matches[0]}{RS}")
                else:
                    print(f"  {Y}[~] No CURP in response{RS}")
                    print(f"  {C}[*] Generating locally...{RS}")
                    # Generate locally
                    vocals = ['A','E','I','O','U']
                    cons = 'BCDFGHJKLMNPQRSTVWXYZ'
                    state_map = {'AGUASCALIENTES':'AS','BAJA CALIFORNIA':'BC','BAJA CALIFORNIA SUR':'BS','CAMPECHE':'CC','COAHUILA':'CL','COLIMA':'CM','CHIAPAS':'CS','CHIHUAHUA':'CH','CDMX':'DF','DF':'DF','CIUDAD DE MEXICO':'DF','DURANGO':'DG','GUANAJUATO':'GT','GUERRERO':'GR','HIDALGO':'HG','JALISCO':'JC','MEXICO':'MC','ESTADO DE MEXICO':'MC','MC':'MC','MICHOACAN':'MN','MORELOS':'MS','NAYARIT':'NS','NUEVO LEON':'NL','OAXACA':'OC','PUEBLA':'PL','QUERETARO':'QT','QUINTANA ROO':'QR','SAN LUIS POTOSI':'SP','SINALOA':'SL','SONORA':'SR','TABASCO':'TC','TAMAULIPAS':'TS','TLAXCALA':'TL','VERACRUZ':'VZ','YUCATAN':'YN','ZACATECAS':'ZS'}
                    sc = state_map.get(st.upper().strip(),'NE')
                    p = paternal[0]
                    fv = next((c for c in paternal[1:] if c in vocals),'X')
                    fc = next((c for c in paternal[1:] if c in cons),'X')
                    mc = maternal[0] if maternal else 'X'
                    c = p+fv+fc+mc+y[-2:]+m.zfill(2)+d.zfill(2)+s+sc
                    if maternal:
                        mc2 = next((c for c in maternal[1:] if c in cons),'X')
                        c += mc2
                    else:
                        c += 'X'
                    nc = next((c for c in name[1:] if c in cons),'X')
                    c += nc + '0'
                    # Calc verification
                    digits = {chr(i):i-ord('A')+10 if i>=ord('A') else i-ord('0') for i in range(ord('0'),ord('Z')+1)}
                    total = sum(digits.get(c2,0)*(18-i) for i,c2 in enumerate(c))
                    r = total%10
                    c += str(10-r) if r!=0 else '0'
                    print(f"  {G}[+] Generated: {BW}{c}{RS}")
            else:
                print(f"  {R}[!] RENAPO returned {resp.status_code}{RS}")
        except Exception as e:
            print(f"  {R}[!] Error: {e}{RS}")
    
    elif choice == '2':
        search = input(f"  {Y}[*] Search term: {RS}").strip()
        print(f"\n  {C}[*] Google dork links:{RS}")
        for q in [f'"CURP" "{search}"',f'"{search}" "CURP" "RFC"',f'"{search}" "CURP" filetype:csv']:
            url = f"https://www.google.com/search?q={urllib.parse.quote(q)}"
            print(f"  {C}  {url}{RS}")
    
    elif choice == '3':
        endpoint = input(f"  {Y}[*] API endpoint URL: {RS}").strip()
        method = input(f"  {Y}[*] Method (GET/POST): {RS}").strip().upper()
        if method == 'POST':
            data_str = input(f"  {Y}[*] JSON body: {RS}").strip()
            try:
                data = json.loads(data_str)
                resp = requests.post(endpoint, json=data, headers=HEADERS, timeout=15)
            except:
                resp = requests.post(endpoint, data=data_str, headers=HEADERS, timeout=15)
        else:
            resp = requests.get(endpoint, headers=HEADERS, timeout=15)
        
        if resp.status_code == 200:
            curps = re.findall(CURP_PATTERN, resp.text)
            if curps:
                print(f"\n  {G}[+] Found {len(curps)} CURPs:{RS}")
                for c in set(curps): print(f"  {C}  {c}{RS}")
            else:
                print(f"  {Y}[~] No CURPs found in response{RS}")
                print(f"  {W}    Response: {resp.text[:500]}{RS}")
        else:
            print(f"  {R}[!] Error: {resp.status_code}{RS}")

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    os.system('clear' if os.name!='nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - CURP WEB EXTRACTOR v1.0{RS}")
    print(f"  {Y}{Style.BRIGHT}  Extract CURPs from web, documents & APIs{RS}")
    print()
    
    while True:
        print(f"  {G}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {G}║  {BW}HELL SOCIETY CURP EXTRACTOR{RS}                      {G}║{RS}")
        print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[1] {BW}Web Scraper{RS}")
        print(f"  {C}[2] {BW}Pastebin Scanner{RS}")
        print(f"  {C}[3] {BW}Document Extractor{RS}")
        print(f"  {C}[4] {BW}API Endpoint Lookup{RS}")
        print()
        print(f"  {R}[0] {BW}Exit{RS}")
        print()
        
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Y}[*] Goodbye...{RS}")
            sys.exit(0)
        
        if choice == '1': method_web_scrape()
        elif choice == '2': method_pastebin()
        elif choice == '3': method_document()
        elif choice == '4': method_api()
        elif choice == '0':
            print(f"\n  {Y}[*] Goodbye from Hell Society...{RS}")
            sys.exit(0)
        else:
            print(f"  {R}[!] Invalid option{RS}")
        
        print()
        input(f"  {C}[*] Press ENTER to continue...{RS}")
        os.system('clear' if os.name!='nt' else 'cls')
        print(BANNER)
        print()

if __name__ == "__main__":
    main()
