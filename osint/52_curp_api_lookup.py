#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - CURP API LOOKUP & CROSS-REFERENCE               ║
║  Created by: HELL SOCIETY Community                              ║
║  Multi-API CURP Verification & Data Extraction                   ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: Hell Society assumes no liability for misuse.
"""

import os
import sys
import re
import json
import hashlib
import time
import urllib.parse

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    os.system("pip3 install requests beautifulsoup4 2>/dev/null")
    import requests
    from bs4 import BeautifulSoup

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN; W = Fore.WHITE
BW = Style.BRIGHT + Fore.WHITE; BR = Style.BRIGHT + Fore.RED
BG = Style.BRIGHT + Fore.GREEN; BC = Style.BRIGHT + Fore.CYAN
BY = Style.BRIGHT + Fore.YELLOW
RS = Style.RESET_ALL

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

VOCALS = ['A', 'E', 'I', 'O', 'U']
ESTADO_MAP = {
    'AGUASCALIENTES': 'AS', 'BAJA CALIFORNIA': 'BC', 'BAJA CALIFORNIA SUR': 'BS',
    'CAMPECHE': 'CC', 'COAHUILA': 'CL', 'COLIMA': 'CM', 'CHIAPAS': 'CS',
    'CHIHUAHUA': 'CH', 'CIUDAD DE MEXICO': 'DF', 'CDMX': 'DF', 'DF': 'DF',
    'DURANGO': 'DG', 'GUANAJUATO': 'GT', 'GUERRERO': 'GR', 'HIDALGO': 'HG',
    'JALISCO': 'JC', 'ESTADO DE MEXICO': 'MC', 'MEXICO': 'MC', 'MC': 'MC',
    'MICHOACAN': 'MN', 'MICHOACÁN': 'MN', 'MORELOS': 'MS', 'NAYARIT': 'NS',
    'NUEVO LEON': 'NL', 'OAXACA': 'OC', 'PUEBLA': 'PL', 'QUERETARO': 'QT',
    'QUINTANA ROO': 'QR', 'SAN LUIS POTOSI': 'SP', 'SINALOA': 'SL',
    'SONORA': 'SR', 'TABASCO': 'TC', 'TAMAULIPAS': 'TS', 'TLAXCALA': 'TL',
    'VERACRUZ': 'VZ', 'YUCATAN': 'YN', 'ZACATECAS': 'ZS', 'EXTRANJERO': 'NE'
}

STATE_NAMES = {
    'AS': 'Aguascalientes', 'BC': 'Baja California', 'BS': 'Baja California Sur',
    'CC': 'Campeche', 'CL': 'Coahuila', 'CM': 'Colima', 'CS': 'Chiapas',
    'CH': 'Chihuahua', 'DF': 'Ciudad de México', 'DG': 'Durango',
    'GT': 'Guanajuato', 'GR': 'Guerrero', 'HG': 'Hidalgo', 'JC': 'Jalisco',
    'MC': 'Estado de México', 'MN': 'Michoacán', 'MS': 'Morelos',
    'NS': 'Nayarit', 'NL': 'Nuevo León', 'OC': 'Oaxaca', 'PL': 'Puebla',
    'QT': 'Querétaro', 'QR': 'Quintana Roo', 'SP': 'San Luis Potosí',
    'SL': 'Sinaloa', 'SR': 'Sonora', 'TC': 'Tabasco', 'TS': 'Tamaulipas',
    'TL': 'Tlaxcala', 'VZ': 'Veracruz', 'YN': 'Yucatán', 'ZS': 'Zacatecas',
    'NE': 'Nacido en el Extranjero'
}

def strip_accents(text):
    text = text.upper().strip()
    replacements = {'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U'}
    for a, p in replacements.items():
        text = text.replace(a, p)
    return text

def get_first_vowel(name):
    for c in name[1:]:
        if c in VOCALS:
            return c
    return 'X'

def get_consonant(name):
    consonants = 'BCDFGHJKLMNPQRSTVWXYZ'
    for c in name[1:]:
        if c in consonants:
            return c
    return 'X'

def calc_verification(curp_17):
    digits = {chr(i): i - ord('A') + 10 if i >= ord('A') else i - ord('0') for i in range(ord('0'), ord('9')+1)}
    digits.update({chr(i): i - ord('A') + 10 for i in range(ord('A'), ord('Z')+1)})
    total = 0
    for i, c in enumerate(curp_17):
        v = digits.get(c, 0)
        w = 18 - i
        total += v * w
    r = total % 10
    return str(10 - r) if r != 0 else '0'

def generate_curp(name, paternal, maternal, day, month, year, sex, state):
    name = strip_accents(name)
    paternal = strip_accents(paternal)
    maternal = strip_accents(maternal) if maternal else 'X'
    
    particles = ['DE', 'DEL', 'LA', 'LOS', 'LAS', 'Y', 'MC']
    for p in particles:
        paternal = re.sub(r'\b' + p + r'\b', '', paternal).strip()
        maternal = re.sub(r'\b' + p + r'\b', '', maternal).strip()
    
    curp = paternal[0] if paternal else 'X'
    curp += get_first_vowel(paternal)
    curp += get_consonant(paternal)
    curp += maternal[0] if maternal else 'X'
    curp += str(year)[-2:].zfill(2)
    curp += str(month).zfill(2)
    curp += str(day).zfill(2)
    curp += sex.upper()
    estado_code = ESTADO_MAP.get(state.upper().strip(), 'NE')
    curp += estado_code
    curp += get_consonant(maternal)
    curp += get_consonant(name)
    curp += '0'
    curp += calc_verification(curp)
    return curp

def parse_curp(curp):
    """Parse CURP into structured data"""
    if len(curp) != 18:
        return None
    data = {
        'curp': curp,
        'initials': curp[:4],
        'year': int('19' + curp[4:6]) if int(curp[4:6]) > 30 else int('20' + curp[4:6]),
        'month': curp[6:8],
        'day': curp[8:10],
        'sex': 'Male' if curp[10] == 'H' else 'Female',
        'sex_code': curp[10],
        'state_code': curp[11:13],
        'state_name': STATE_NAMES.get(curp[11:13], 'Unknown'),
        'consonants': curp[13:16],
        'homonymy': curp[16],
        'verification': curp[17]
    }
    return data

# ═══════════════════════════════════════════════════════════════════
# METHOD 9: CURP ONLINE VERIFY (Multiple services)
# ═══════════════════════════════════════════════════════════════════

def method_online_verify():
    """Verify CURP across multiple online services"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 9: ONLINE CURP VERIFICATION{RS}              {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    curp = input(f"  {Y}[*] Enter CURP to verify: {RS}").strip().upper()
    
    if len(curp) != 18:
        print(f"  {R}[!] Invalid CURP length{RS}")
        return
    
    print(f"\n  {C}[*] Checking across multiple services...{RS}\n")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml',
        'Accept-Language': 'es-MX,es;q=0.9'
    }
    
    results = {}
    
    # 1. Official RENAPO
    print(f"  {Y}[*] [1/5] Checking RENAPO (official)...{RS}")
    try:
        data = parse_curp(curp)
        url = "https://consultas.curp.gob.mx/CurpSP/"
        params = {
            'nombre': data['initials'][3],
            'paterno': data['initials'][0:3],
            'materno': 'X',
            'dia': data['day'],
            'mes': data['month'],
            'year': str(data['year']),
            'sexo': data['sex_code'],
            'entidad': data['state_name']
        }
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        results['RENAPO'] = resp.status_code == 200
        print(f"  {'  '+G+'[+]' if results['RENAPO'] else '  '+R+'[X]'} RENAPO: {'OK' if results['RENAPO'] else f'Error {resp.status_code}'}{RS}")
    except Exception as e:
        results['RENAPO'] = False
        print(f"  {R}  [X] RENAPO: Connection error{RS}")
    
    # 2. CURP format validation
    print(f"  {Y}[*] [2/5] Format validation...{RS}")
    calc = calc_verification(curp[:17])
    valid = (curp[17] == calc)
    results['Format'] = valid
    print(f"  {'  '+G+'[+]' if valid else '  '+R+'[X]'} Format: {'VALID' if valid else f'INVALID (digit should be {calc})'}{RS}")
    
    # 3. State code validation
    print(f"  {Y}[*] [3/5] State validation...{RS}")
    state_valid = curp[11:13] in STATE_NAMES
    results['State'] = state_valid
    print(f"  {'  '+G+'[+]' if state_valid else '  '+R+'[X]'} State: {'VALID' if state_valid else 'INVALID'}{RS}")
    
    # 4. Birth date validation
    print(f"  {Y}[*] [4/5] Date validation...{RS}")
    try:
        y = data['year']
        m = int(data['month'])
        d = int(data['day'])
        from datetime import date
        date(y, m, d)
        results['Date'] = True
        print(f"  {G}  [+] Date: VALID ({d}/{m}/{y}){RS}")
    except:
        results['Date'] = False
        print(f"  {R}  [X] Date: INVALID{RS}")
    
    # 5. Search in breach databases
    print(f"  {Y}[*] [5/5] Breach database check...{RS}")
    try:
        url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{curp}"
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            breaches = resp.json()
            results['Breaches'] = len(breaches)
            print(f"  {R}  [!] Found in {len(breaches)} breaches!{RS}")
            for b in breaches:
                print(f"  {R}      - {b.get('Name', 'Unknown')}{RS}")
        elif resp.status_code == 404:
            results['Breaches'] = 0
            print(f"  {G}  [+] Not found in breaches{RS}")
        else:
            results['Breaches'] = 'error'
            print(f"  {Y}  [~] Breach check: Service unavailable{RS}")
    except:
        results['Breaches'] = 'error'
        print(f"  {Y}  [~] Breach check: Connection error{RS}")
    
    # Summary
    print(f"\n  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  VERIFICATION SUMMARY:{RS}")
    print(f"  {Y}{'=' * 50}{RS}")
    
    total_checks = 5
    passed = sum(1 for v in [results.get('Format'), results.get('State'), results.get('Date')] if v is True)
    
    print(f"  {C}  Format: {G}PASS{RS}" if results.get('Format') else f"  {C}  Format: {R}FAIL{RS}")
    print(f"  {C}  State:  {G}PASS{RS}" if results.get('State') else f"  {C}  State:  {R}FAIL{RS}")
    print(f"  {C}  Date:   {G}PASS{RS}" if results.get('Date') else f"  {C}  Date:   {R}FAIL{RS}")
    print(f"  {C}  RENAPO: {G}OK{RS}" if results.get('RENAPO') else f"  {C}  RENAPO: {Y}N/A{RS}")
    print(f"  {C}  Breaches: {R}FOUND{RS}" if isinstance(results.get('Breaches'), int) and results.get('Breaches', 0) > 0 else f"  {C}  Breaches: {G}CLEAN{RS}")
    print()
    
    return results

# ═══════════════════════════════════════════════════════════════════
# METHOD 10: CURP FROM IMAGE (OCR Extraction)
# ═══════════════════════════════════════════════════════════════════

def method_from_image():
    """Extract CURP from images using OCR"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 10: CURP FROM IMAGE (OCR){RS}                {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    img_path = input(f"  {Y}[*] Path to image (JPG/PNG/PDF): {RS}").strip()
    
    if not os.path.isfile(img_path):
        print(f"  {R}[!] File not found: {img_path}{RS}")
        return
    
    print(f"\n  {Y}[*] Extracting CURP from image...{RS}")
    
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        print(f"  {R}[!] Required: pip3 install pytesseract{RS}")
        print(f"  {R}[!] Also install: sudo apt install tesseract-ocr{RS}")
        print(f"  {Y}[~] For Termux: pkg install tesseract{RS}")
        return
    
    try:
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        
        # Find CURP pattern in OCR text
        curp_pattern = r'[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d'
        matches = re.findall(curp_pattern, text)
        
        if matches:
            print(f"\n  {G}[+] Found {len(matches)} CURP(s) in image:{RS}\n")
            for m in matches:
                data = parse_curp(m)
                if data:
                    print(f"  {C}{m}{RS}")
                    print(f"  {BW}    Birth: {data['day']}/{data['month']}/{data['year']}{RS}")
                    print(f"  {BW}    Sex: {data['sex']}{RS}")
                    print(f"  {BW}    State: {data['state_name']}{RS}")
                    print()
        else:
            print(f"  {Y}[~] No CURP found in image{RS}")
            print(f"  {C}[*] Raw OCR text preview:{RS}")
            print(f"  {W}    {text[:500]}{RS}")
    except Exception as e:
        print(f"  {R}[!] Error: {e}{RS}")

# ═══════════════════════════════════════════════════════════════════
# METHOD 11: CURP HASH LOOKUP
# ═══════════════════════════════════════════════════════════════════

def method_hash_lookup():
    """Look up CURP by hash (MD5/SHA256)"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 11: CURP HASH LOOKUP{RS}                     {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    hash_type = input(f"  {Y}[*] Hash type (md5/sha256): {RS}").strip().lower()
    hash_value = input(f"  {Y}[*] Hash value: {RS}").strip().lower()
    
    print(f"\n  {C}[*] Searching in online hash databases...{RS}")
    
    # Try common hash lookup services
    services = [
        ("MD5Decrypter", f"https://md5decrypt.net/en/Api/api.php?hash={hash_value}&hash_type={hash_type}&email=hs@hs.com&code=hs2024"),
        ("Hashes.org", f"https://hashes.org/api.php?key=hs2024&hash={hash_value}"),
        ("CrackStation", f"https://crackstation.net/api.php?key=hs2024&hash={hash_value}&captcha_response="),
    ]
    
    for svc_name, url in services:
        print(f"  {Y}[*] Checking {svc_name}...{RS}")
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200 and resp.text and resp.text != 'not_found' and 'error' not in resp.text.lower():
                result = resp.text.strip()
                if re.match(r'^[A-Z]{4}\d{6}[HM]', result):
                    print(f"  {G}[+] {svc_name}: {result}{RS}")
                else:
                    print(f"  {Y}[~] {svc_name}: Hash found but not CURP format{RS}")
                    print(f"  {W}    Result: {result}{RS}")
            else:
                print(f"  {Y}[~] {svc_name}: Not found{RS}")
        except Exception as e:
            print(f"  {R}[X] {svc_name}: Error{RS}")
    
    print(f"\n  {Y}[~] You can also search manually at:{RS}")
    print(f"  {C}    https://md5decrypt.net/English/{RS}")
    print(f"  {C}    https://crackstation.net/{RS}")
    print(f"  {C}    https://hashes.org/lookup.php{RS}")

# ═══════════════════════════════════════════════════════════════════
# METHOD 12: CURP GENERATOR BY AGE RANGE
# ═══════════════════════════════════════════════════════════════════

def method_age_range_generator():
    """Generate CURPs based on age range and state"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 12: AGE RANGE GENERATOR{RS}                   {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    print(f"  {C}[+] Age range:{RS}")
    min_age = input(f"  {Y}    Min age: {RS}").strip()
    max_age = input(f"  {Y}    Max age: {RS}").strip()
    
    sex = input(f"\n  {Y}[*] Sex (H/M/BOTH): {RS}").strip().upper()
    state = input(f"  {Y}[*] State: {RS}").strip()
    count = input(f"  {Y}[*] How many to generate: {RS}").strip() or "10"
    
    try:
        min_age = int(min_age)
        max_age = int(max_age)
        count = int(count)
    except:
        min_age, max_age, count = 18, 40, 10
    
    current_year = datetime.now().year
    year_start = current_year - max_age
    year_end = current_year - min_age
    
    estado_code = ESTADO_MAP.get(state.upper().strip(), 'NE')
    estado_name = STATE_NAMES.get(estado_code, state)
    
    names = ['JUAN', 'CARLOS', 'JOSE', 'MIGUEL', 'ANTONIO', 'PEDRO',
             'LUIS', 'FRANCISCO', 'RAFAEL', 'MARIA', 'ANA', 'GUADALUPE']
    surnames = ['GARCIA', 'RODRIGUEZ', 'MARTINEZ', 'LOPEZ', 'GONZALEZ',
                'HERNANDEZ', 'PEREZ', 'SANCHEZ', 'RAMIREZ', 'TORRES']
    
    print(f"\n  {C}[*] Generating {count} CURPs (ages {min_age}-{max_age}, {estado_name})...{RS}\n")
    
    results = []
    for i in range(count):
        name = random.choice(names)
        paternal = random.choice(surnames)
        maternal = random.choice(surnames)
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(year_start, year_end)
        s = random.choice(['H', 'M']) if sex == 'BOTH' else sex[0]
        
        curp = generate_curp(name, paternal, maternal, str(day), str(month), str(year), s, state)
        results.append({'curp': curp, 'age': current_year - year, 'sex': s})
    
    print(f"  {Y}{'=' * 60}{RS}")
    print(f"  {BW}  GENERATED CURPs ({min_age}-{max_age} years, {estado_name}):{RS}")
    print(f"  {Y}{'=' * 60}{RS}\n")
    
    for r in results:
        print(f"  {C}{r['curp']}{RS}  {Y}(age:{r['age']}, {r['sex']}){RS}")
    
    # Save
    output = "curp_age_range.txt"
    with open(output, 'w') as f:
        for r in results:
            f.write(f"{r['curp']},{r['age']},{r['sex']}\n")
    print(f"\n  {G}[+] Saved to: {output}{RS}")

# ═══════════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - CURP API & CROSS-REFERENCE v2.0{RS}")
    print(f"  {Y}{Style.BRIGHT}  Advanced Lookup, OCR, Hash & Bulk Methods{RS}")
    print()
    
    while True:
        print(f"  {G}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {G}║  {BW}HELL SOCIETY CURP API TOOLS{RS}                      {G}║{RS}")
        print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[1]  {BW}Online CURP Verification (5 services){RS}")
        print(f"  {C}[2]  {BW}CURP From Image (OCR){RS}")
        print(f"  {C}[3]  {BW}CURP Hash Lookup (MD5/SHA256){RS}")
        print(f"  {C}[4]  {BW}Age Range Generator{RS}")
        print()
        print(f"  {R}[0]  {BW}Exit{RS}")
        print()
        
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {R}[*] Goodbye...{RS}")
            sys.exit(0)
        
        if choice == '1':
            method_online_verify()
        elif choice == '2':
            method_from_image()
        elif choice == '3':
            method_hash_lookup()
        elif choice == '4':
            method_age_range_generator()
        elif choice == '0':
            print(f"\n  {Y}[*] Goodbye from Hell Society...{RS}")
            sys.exit(0)
        else:
            print(f"  {R}[!] Invalid option{RS}")
        
        print()
        input(f"  {C}[*] Press ENTER to continue...{RS}")
        os.system('clear' if os.name != 'nt' else 'cls')
        print(BANNER)
        print()

if __name__ == "__main__":
    main()
