#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - CURP GENERATOR v2.0                             ║
║  Created by: HELL SOCIETY Community                              ║
║  Multi-Method CURP Generation & Extraction                       ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: Hell Society assumes no liability for misuse.
"""

import os
import sys
import re
import json
import string
import hashlib
import time
import random
import urllib.parse
import subprocess
from datetime import datetime, date

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import requests
except ImportError:
    os.system("pip3 install requests 2>/dev/null")
    import requests

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

# ═══════════════════════════════════════════════════════════════════
# MÉXICO - VOCALS AND CONSONANTS
# ═══════════════════════════════════════════════════════════════════
VOCALS = ['A', 'E', 'I', 'O', 'U']
FIRST_INTERNAL_CONSONANT = 'X'
LAST_INTERNAL_CONSONANT = 'X'
HOMONYMY = 0
VERIFICATION_DIGIT = 0

# ── VOCAL POSITION MAP ──
VOCAL_POSITION = {
    'A': 0, 'E': 5, 'I': 10, 'O': 14, 'U': 17,
    'B': 1, 'C': 2, 'D': 3, 'F': 4, 'G': 5,
    'H': 6, 'J': 7, 'K': 8, 'L': 9, 'M': 10,
    'N': 11, 'Ñ': 12, 'P': 13, 'Q': 14, 'R': 15,
    'S': 16, 'T': 17, 'V': 18, 'W': 19, 'X': 20,
    'Y': 21, 'Z': 22
}

# ── ESTADO MAP (ENTIDAD FEDERATIVA) ──
ESTADO_MAP = {
    'AGUASCALIENTES': 'AS', 'AGUASCALIENTE': 'AS', 'AS': 'AS',
    'BAJA CALIFORNIA': 'BC', 'BC': 'BC',
    'BAJA CALIFORNIA SUR': 'BS', 'BS': 'BS',
    'CAMPECHE': 'CC', 'CC': 'CC',
    'COAHUILA': 'CL', 'CL': 'CL', 'COAHUILA DE ZARAGOZA': 'CL',
    'COLIMA': 'CM', 'CM': 'CM',
    'CHIAPAS': 'CS', 'CS': 'CS',
    'CHIHUAHUA': 'CH', 'CH': 'CH',
    'CIUDAD DE MEXICO': 'DF', 'CDMX': 'DF', 'DF': 'DF',
    'DISTRITO FEDERAL': 'DF',
    'DURANGO': 'DG', 'DG': 'DG',
    'GUANAJUATO': 'GT', 'GT': 'GT',
    'GUERRERO': 'GR', 'GR': 'GR',
    'HIDALGO': 'HG', 'HG': 'HG',
    'JALISCO': 'JC', 'JC': 'JC',
    'ESTADO DE MEXICO': 'MC', 'MEXICO': 'MC',
    'ESTADO DE MÉXICO': 'MC', 'MÉXICO': 'MC', 'MC': 'MC',
    'MICHOACAN': 'MN', 'MICHOACÁN': 'MN', 'MICHOACAN DE OCAMPO': 'MN', 'MN': 'MN',
    'MORELOS': 'MS', 'MS': 'MS',
    'NAYARIT': 'NS', 'NS': 'NS',
    'NUEVO LEON': 'NL', 'NUEVO LEÓN': 'NL', 'NL': 'NL',
    'OAXACA': 'OC', 'OC': 'OC',
    'PUEBLA': 'PL', 'PL': 'PL',
    'QUERETARO': 'QT', 'QUERÉTARO': 'QT', 'QT': 'QT',
    'QUINTANA ROO': 'QR', 'QR': 'QR',
    'SAN LUIS POTOSI': 'SP', 'SAN LUIS POTOSÍ': 'SP', 'SP': 'SP',
    'SINALOA': 'SL', 'SL': 'SL',
    'SONORA': 'SR', 'SR': 'SR',
    'TABASCO': 'TC', 'TC': 'TC',
    'TAMAULIPAS': 'TS', 'TS': 'TS',
    'TLAXCALA': 'TL', 'TL': 'TL',
    'VERACRUZ': 'VZ', 'VERACRUZ DE IGNACIO DE LA LLAVE': 'VZ', 'VZ': 'VZ',
    'YUCATAN': 'YN', 'YUCATÁN': 'YN', 'YN': 'YN',
    'ZACATECAS': 'ZS', 'ZS': 'ZS',
    'NACIDO EN EL EXTRANJERO': 'NE', 'EXTRANJERO': 'NE', 'NE': 'NE',
    'MEXICANA': 'NE', 'MEXICANO': 'NE'
}

# ── MONTH MAP ──
MONTH_MAP = {
    'ENERO': '01', 'ENERO': '01', 'ENE': '01', '1': '01', '01': '01',
    'FEBRERO': '02', 'FEB': '02', '2': '02', '02': '02',
    'MARZO': '03', 'MAR': '03', '3': '03', '03': '03',
    'ABRIL': '04', 'ABR': '04', '4': '04', '04': '04',
    'MAYO': '05', 'MAY': '05', '5': '05', '05': '05',
    'JUNIO': '06', 'JUN': '06', '6': '06', '06': '06',
    'JULIO': '07', 'JUL': '07', '7': '07', '07': '07',
    'AGOSTO': '08', 'AGO': '08', '8': '08', '08': '08',
    'SEPTIEMBRE': '09', 'SEP': '09', 'SEPT': '09', '9': '09', '09': '09',
    'OCTUBRE': '10', 'OCT': '10', '10': '10',
    'NOVIEMBRE': '11', 'NOV': '11', '11': '11',
    'DICIEMBRE': '12', 'DIC': '12', '12': '12'
}

# ── CONSONANT MAP ──
CONSONANT_MAP = {
    'B': 'B', 'C': 'C', 'CH': 'X', 'D': 'D', 'F': 'F',
    'G': 'G', 'H': 'H', 'J': 'J', 'K': 'K', 'L': 'L',
    'LL': 'L', 'M': 'M', 'N': 'N', 'Ñ': 'X', 'P': 'P',
    'Q': 'Q', 'R': 'R', 'S': 'S', 'T': 'T', 'V': 'V',
    'W': 'W', 'X': 'X', 'Y': 'Y', 'Z': 'Z'
}

# ═══════════════════════════════════════════════════════════════════
# CURP CALCULATION
# ═══════════════════════════════════════════════════════════════════

def strip_accents(text):
    """Remove accents from text"""
    text = text.upper().strip()
    replacements = {
        'Á': 'A', 'É': 'E', 'Í': 'I', 'Ó': 'O', 'Ú': 'U', 'Ü': 'U',
        'Ñ': 'Ñ'
    }
    for accent, plain in replacements.items():
        text = text.replace(accent, plain)
    return text

def get_first_vowel(name):
    """Get first internal vowel from name"""
    for char in name[1:]:
        if char in VOCALS:
            return char
    return 'X'

def get_consonant(name):
    """Get first internal consonant from name"""
    consonants = ['B', 'C', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
                  'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'X', 'Y', 'Z']
    for char in name[1:]:
        if char in consonants:
            return char
    return 'X'

def calculate_verification_digit(curp_17):
    """Calculate the verification digit for CURP"""
    digits = {
        '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
        '7': 7, '8': 8, '9': 9,
        'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15,
        'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21,
        'M': 22, 'N': 23, 'Ñ': 24, 'O': 25, 'P': 26, 'Q': 27,
        'R': 28, 'S': 29, 'T': 30, 'U': 31, 'V': 32, 'W': 33,
        'X': 34, 'Y': 35, 'Z': 36
    }
    
    total = 0
    for i, char in enumerate(curp_17):
        value = digits.get(char, 0)
        weight = 18 - i
        total += value * weight
    
    remainder = total % 10
    verification = (10 - remainder) if remainder != 0 else 0
    
    return str(verification) if verification < 10 else 'X'

def generate_curp(name, paternal, maternal, day, month, year, sex, state):
    """Generate CURP from personal data"""
    # Clean inputs
    name = strip_accents(name)
    paternal = strip_accents(paternal)
    maternal = strip_accents(maternal) if maternal else 'X'
    
    # Remove special particles
    particles = ['DE', 'DEL', 'LA', 'LOS', 'LAS', 'Y', 'MC', 'VAN', 'VON']
    for p in particles:
        paternal = re.sub(r'\b' + p + r'\b', '', paternal).strip()
        maternal = re.sub(r'\b' + p + r'\b', '', maternal).strip()
        name = re.sub(r'\b' + p + r'\b', '', name).strip()
    
    # 1. First letter of paternal surname
    curp = paternal[0] if paternal else 'X'
    
    # 2. First vowel of paternal surname
    curp += get_first_vowel(paternal)
    
    # 3. First consonant of paternal surname
    curp += get_consonant(paternal)
    
    # 4. First letter of maternal surname
    curp += maternal[0] if maternal else 'X'
    
    # 5-6. Birth year (2 digits)
    curp += str(year)[-2:].zfill(2)
    
    # 7-8. Birth month
    curp += str(month).zfill(2)
    
    # 9-10. Birth day
    curp += str(day).zfill(2)
    
    # 11. Sex (H/M)
    curp += sex.upper()
    
    # 12-13. State code
    state_upper = state.upper().strip()
    estado_code = ESTADO_MAP.get(state_upper, 'NE')
    curp += estado_code
    
    # 14. First consonant of maternal surname
    curp += get_consonant(maternal)
    
    # 15. First consonant of name
    curp += get_consonant(name)
    
    # 16. Homonymy (default 0)
    curp += '0'
    
    # 17. Verification digit
    curp += calculate_verification_digit(curp)
    
    return curp

# ═══════════════════════════════════════════════════════════════════
# METHOD 1: GENERATOR BY PERSONAL DATA
# ═══════════════════════════════════════════════════════════════════

def method_generator():
    """Generate CURP from personal data input"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 1: GENERATOR BY PERSONAL DATA{RS}              {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    name = input(f"  {Y}[*] Name (given name): {RS}").strip().upper()
    paternal = input(f"  {Y}[*] Paternal surname: {RS}").strip().upper()
    maternal = input(f"  {Y}[*] Maternal surname (X if none): {RS}").strip().upper() or 'X'
    
    print(f"\n  {C}[+] Birth date:{RS}")
    day = input(f"  {Y}    Day: {RS}").strip()
    month_input = input(f"  {Y}    Month (number or name): {RS}").strip().upper()
    year = input(f"  {Y}    Year: {RS}").strip()
    
    sex = input(f"\n  {Y}[*] Sex (H=Male, M=Female): {RS}").strip().upper()
    
    state = input(f"  {Y}[*] State of birth: {RS}").strip().upper()
    
    # Generate CURP
    curp = generate_curp(name, paternal, maternal, day, month_input, year, sex, state)
    
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║                                                       {RS}")
    print(f"  {G}║  {BW}CURP GENERATED:{RS}                                     {RS}")
    print(f"  {G}║  {Y}{Style.BRIGHT}{curp}{RS}                                    {RS}")
    print(f"  {G}║                                                       {RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    return curp

# ═══════════════════════════════════════════════════════════════════
# METHOD 2: RENAPO SEARCH (GOVERNMENT API)
# ═══════════════════════════════════════════════════════════════════

def method_renapo():
    """Search CURP in RENAPO government system"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 2: RENAPO SEARCH (GOVERNMENT){RS}            {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    name = input(f"  {Y}[*] Name: {RS}").strip().upper()
    paternal = input(f"  {Y}[*] Paternal surname: {RS}").strip().upper()
    maternal = input(f"  {Y}[*] Maternal surname: {RS}").strip().upper()
    
    print(f"\n  {C}[+] Birth date:{RS}")
    day = input(f"  {Y}    Day: {RS}").strip()
    month = input(f"  {Y}    Month: {RS}").strip()
    year = input(f"  {Y}    Year: {RS}").strip()
    
    sex = input(f"\n  {Y}[*] Sex (H/M): {RS}").strip().upper()
    state = input(f"  {Y}[*] State: {RS}").strip().upper()
    
    print(f"\n  {Y}[*] Searching in RENAPO...{RS}")
    
    # RENAPO URL
    url = "https://consultas.curp.gob.mx/CurpSP/"
    
    params = {
        'nombre': name,
        'paterno': paternal,
        'materno': maternal,
        'dia': day,
        'mes': month,
        'year': year,
        'sexo': sex,
        'entidad': state
    }
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml',
            'Accept-Language': 'es-MX,es;q=0.9'
        }
        
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            # Try to extract CURP from response
            curp_pattern = r'[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d'
            matches = re.findall(curp_pattern, content)
            
            if matches:
                print(f"\n  {G}[+] CURP found in RENAPO:{RS}")
                for c in matches:
                    print(f"  {Y}{Style.BRIGHT}    {c}{RS}")
                return matches[0]
            else:
                print(f"  {Y}[~] No CURP found in response{RS}")
                print(f"  {C}[*] Try generating with Method 1{RS}")
        else:
            print(f"  {R}[!] Server returned {response.status_code}{RS}")
            print(f"  {Y}[~] Use Method 1 to generate CURP{RS}")
    except Exception as e:
        print(f"  {R}[!] Connection error: {e}{RS}")
        print(f"  {Y}[~] Use Method 1 to generate CURP{RS}")
    
    return None

# ═══════════════════════════════════════════════════════════════════
# METHOD 3: BULK GENERATOR (RANDOM)
# ═══════════════════════════════════════════════════════════════════

def method_bulk_generator():
    """Generate multiple CURPs with random data"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 3: BULK CURP GENERATOR{RS}                   {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    count = input(f"  {Y}[*] How many CURPs to generate: {RS}").strip()
    try:
        count = int(count)
    except:
        count = 10
    
    estado_keys = list(ESTADO_MAP.keys())
    
    names_m = ['JUAN', 'CARLOS', 'JOSE', 'MIGUEL', 'ANTONIO', 'PEDRO', 
               'LUIS', 'FRANCISCO', 'RAFAEL', 'ANDRES', 'DAVID', 'DANIEL']
    names_f = ['MARIA', 'ANA', 'GUADALUPE', 'JUANA', 'MARGARITA', 'VERONICA',
               'PATRICIA', 'ROSARIO', 'TERESA', 'ISABEL', 'CARMEN', 'ELENA']
    
    surnames = ['GARCIA', 'RODRIGUEZ', 'MARTINEZ', 'LOPEZ', 'GONZALEZ',
                'HERNANDEZ', 'PEREZ', 'SANCHEZ', 'RAMIREZ', 'TORRES',
                'FLORES', 'RIVERA', 'GOMEZ', 'DIAZ', 'CRUZ', 'MORALES',
                'REYES', 'GUTIERREZ', 'ORTIZ', 'RAMOS', 'VARGAS', 'CASTRO']
    
    states = ['CDMX', 'JALISCO', 'NUEVO LEON', 'GUANAJUATO', 'PUEBLA',
              'VERACRUZ', 'OAXACA', 'CHIAPAS', 'MICHOACAN', 'GUERRERO']
    
    print(f"\n  {C}[*] Generating {count} CURPs...{RS}\n")
    
    results = []
    for i in range(count):
        name = random.choice(names_m + names_f)
        paternal = random.choice(surnames)
        maternal = random.choice(surnames)
        day = str(random.randint(1, 28)).zfill(2)
        month = str(random.randint(1, 12)).zfill(2)
        year = str(random.randint(1940, 2005))
        sex = random.choice(['H', 'M'])
        state = random.choice(states)
        
        curp = generate_curp(name, paternal, maternal, day, month, year, sex, state)
        results.append(curp)
        
        # Print in batches
        if (i + 1) % 5 == 0 or i == count - 1:
            print(f"  {G}[+] Generated {i+1}/{count}{RS}")
    
    print(f"\n  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  GENERATED CURPs:{RS}")
    print(f"  {Y}{'=' * 50}{RS}\n")
    
    for curp in results:
        print(f"  {C}{curp}{RS}")
    
    # Save to file
    output_file = "curp_bulk_results.txt"
    with open(output_file, 'w') as f:
        for curp in results:
            f.write(curp + "\n")
    
    print(f"\n  {G}[+] Saved to: {output_file}{RS}")
    return results

# ═══════════════════════════════════════════════════════════════════
# METHOD 4: CURP VALIDATOR
# ═══════════════════════════════════════════════════════════════════

def method_validator():
    """Validate a CURP"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 4: CURP VALIDATOR{RS}                        {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    curp = input(f"  {Y}[*] Enter CURP to validate: {RS}").strip().upper()
    
    if len(curp) != 18:
        print(f"  {R}[!] CURP must be 18 characters (got {len(curp)}){RS}")
        return
    
    print(f"\n  {C}[*] Validating: {curp}{RS}")
    print()
    
    # Validate structure
    errors = []
    
    # Chars 1-4: Letters
    for i, c in enumerate(curp[:4]):
        if c not in string.ascii_uppercase:
            errors.append(f"  Position {i+1}: '{c}' is not a letter")
    
    # Chars 5-10: Numbers (YYMMDD)
    for i, c in enumerate(curp[4:10]):
        if c not in '0123456789':
            errors.append(f"  Position {i+5}: '{c}' is not a number")
    
    # Char 11: H or M
    if curp[10] not in 'HM':
        errors.append(f"  Position 11: '{curp[10]}' must be H or M")
    
    # Chars 12-13: State code
    state_code = curp[11:13]
    valid_states = list(set(ESTADO_MAP.values()))
    if state_code not in valid_states:
        errors.append(f"  Position 12-13: '{state_code}' is not a valid state code")
    
    # Chars 14-16: Consonants
    for i, c in enumerate(curp[13:16]):
        if c not in string.ascii_uppercase:
            errors.append(f"  Position {i+14}: '{c}' is not a letter")
    
    # Char 17: Homonymy (0-9)
    if curp[16] not in '0123456789':
        errors.append(f"  Position 17: '{curp[16]}' must be 0-9")
    
    # Char 18: Verification digit
    calc_digit = calculate_verification_digit(curp[:17])
    if curp[17] != calc_digit:
        errors.append(f"  Position 18: Verification digit '{curp[17]}' should be '{calc_digit}'")
    
    # Print results
    if errors:
        print(f"  {R}[X] CURP IS INVALID:{RS}")
        for err in errors:
            print(f"  {R}    {err}{RS}")
    else:
        print(f"  {G}[+] CURP IS VALID!{RS}")
    
    # Parse data
    print(f"\n  {Y}{'=' * 40}{RS}")
    print(f"  {BW}  PARSED DATA:{RS}")
    print(f"  {Y}{'=' * 40}{RS}")
    
    print(f"  {C}Initials: {curp[:4]}{RS}")
    print(f"  {C}Birth date: {curp[4:6]}-{curp[6:8]}-{curp[8:10]}{RS}")
    print(f"  {C}Sex: {'Male' if curp[10] == 'H' else 'Female'}{RS}")
    
    # Find state name
    for state_name, state_code in ESTADO_MAP.items():
        if state_code == curp[11:13]:
            print(f"  {C}State: {state_name}{RS}")
            break
    
    print(f"  {C}Internal consonants: {curp[13:16]}{RS}")
    print(f"  {C}Homonymy: {curp[16]}{RS}")
    print(f"  {C}Verification: {curp[17]}{RS}")
    
    return len(errors) == 0

# ═══════════════════════════════════════════════════════════════════
# METHOD 5: CURP BRUTE FORCE (Partial)
# ═══════════════════════════════════════════════════════════════════

def method_bruteforce():
    """Brute force missing CURP characters"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 5: CURP BRUTE FORCE (PARTIAL){RS}            {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    curp_partial = input(f"  {Y}[*] Enter partial CURP (use ? for unknown): {RS}").strip().upper()
    
    if '?' not in curp_partial:
        print(f"  {Y}[~] No unknown characters found. Use ? for missing positions{RS}")
        return
    
    unknown_positions = [i for i, c in enumerate(curp_partial) if c == '?']
    print(f"  {C}[+] Found {len(unknown_positions)} unknown positions: {unknown_positions}{RS}")
    
    # Generate possible values for each position
    charset = string.ascii_uppercase + '0123456789'
    
    if len(unknown_positions) > 3:
        print(f"  {R}[!] Too many unknown positions (>3). This would take too long.{RS}")
        print(f"  {Y}[~] Try with fewer unknown positions{RS}")
        return
    
    results = []
    chars = list(curp_partial)
    
    def generate_combinations(pos_idx):
        if pos_idx == len(unknown_positions):
            curp_candidate = ''.join(chars)
            # Validate
            if len(curp_candidate) == 18:
                calc = calculate_verification_digit(curp_candidate[:17])
                if curp_candidate[17] == calc:
                    results.append(curp_candidate)
            return
        
        pos = unknown_positions[pos_idx]
        for char in charset:
            chars[pos] = char
            generate_combinations(pos_idx + 1)
    
    print(f"\n  {Y}[*] Generating combinations...{RS}")
    generate_combinations(0)
    
    print(f"\n  {G}[+] Found {len(results)} valid CURPs:{RS}\n")
    for r in results:
        print(f"  {C}{r}{RS}")
    
    return results

# ═══════════════════════════════════════════════════════════════════
# METHOD 6: CURP DATABASE DORKER
# ═══════════════════════════════════════════════════════════════════

def method_dorker():
    """Search for CURPs in leaked databases via dorks"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 6: CURP DATABASE SEARCH{RS}                    {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    search_type = input(f"  {Y}[*] Search type (name/curp/domain): {RS}").strip().upper()
    search_value = input(f"  {Y}[*] Search value: {RS}").strip()
    
    print(f"\n  {C}[*] Generating search links...{RS}\n")
    
    dorks = []
    
    if search_type == 'CURP' or search_type == 'CURP':
        dorks = [
            f'"CURP" "{search_value}" filetype:csv',
            f'"CURP" "{search_value}" filetype:xls',
            f'"CURP" "{search_value}" filetype:xlsx',
            f'"CURP" "{search_value}" site:pastebin.com',
            f'"{search_value}" "CURP" "RFC"',
            f'"{search_value}" "CURP" "NOMBRE"',
            f'inurl:"curp" "{search_value}"',
            f'"{search_value}" ext:csv',
            f'"{search_value}" ext:xlsx "CURP"',
            f'"{search_value}" ext:sql "CURP"',
        ]
    
    elif search_type == 'NAME' or search_type == 'NOMBRE':
        dorks = [
            f'"CURP" "{search_value}"',
            f'"CURP" "RFC" "{search_value}"',
            f'"CURP" "NOMBRE" "{search_value}" filetype:csv',
            f'"CURP" "NOMBRE" "{search_value}" filetype:xlsx',
            f'"{search_value}" "CURP" site:pastebin.com',
        ]
    
    else:
        dorks = [
            f'"CURP" "RFC" site:{search_value}',
            f'CURP filetype:csv site:{search_value}',
            f'CURP filetype:xlsx site:{search_value}',
        ]
    
    print(f"  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  SEARCH LINKS:{RS}")
    print(f"  {Y}{'=' * 50}{RS}\n")
    
    for i, dork in enumerate(dorks, 1):
        url = f"https://www.google.com/search?q={urllib.parse.quote(dork)}"
        print(f"  {C}[{i:02d}] {BW}{dork}{RS}")
        print(f"  {G}     Link: {url}{RS}")
        print()
    
    print(f"  {Y}[~] Copy the links and search manually{RS}")
    return dorks

# ═══════════════════════════════════════════════════════════════════
# METHOD 7: RFC TO CURP (EXTRACTION)
# ═══════════════════════════════════════════════════════════════════

def method_rfc_to_curp():
    """Extract CURP from RFC"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 7: RFC TO CURP EXTRACTION{RS}                {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    rfc = input(f"  {Y}[*] Enter RFC (13 chars): {RS}").strip().upper()
    
    if len(rfc) != 13:
        print(f"  {R}[!] RFC must be 13 characters (got {len(rfc)}){RS}")
        return
    
    # RFC structure: AAAA YYMMDD HXX (where XXX are homoclave)
    initial = rfc[:4]
    birth_date = rfc[4:10]
    homoclave = rfc[10:13]
    
    print(f"\n  {C}[*] Extracted from RFC:{RS}")
    print(f"  {C}    Initials: {initial}{RS}")
    print(f"  {C}    Birth date: {birth_date[0:2]}-{birth_date[2:4]}-{birth_date[4:6]}{RS}")
    print(f"  {C}    Homoclave: {homoclave}{RS}")
    print()
    
    # Generate possible CURPs
    print(f"  {Y}[*] Possible CURPs (first 10 chars from RFC):{RS}")
    print(f"  {C}    {initial}{birth_date}{'HM'}XX{'X'*3}0X{RS}")
    print()
    
    print(f"  {Y}[~] The RFC contains the CURP initials and birth date{RS}")
    print(f"  {Y}[~] Use Method 1 with extracted data for full CURP{RS}")
    
    return {
        'initials': initial,
        'birth_date': birth_date,
        'homoclave': homoclave,
        'curp_start': initial + birth_date
    }

# ═══════════════════════════════════════════════════════════════════
# METHOD 8: CURP FORMAT CONVERTER
# ═══════════════════════════════════════════════════════════════════

def method_converter():
    """Convert between CURP formats"""
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 8: CURP FORMAT CONVERTER{RS}                 {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
    print()
    
    curp = input(f"  {Y}[*] Enter CURP: {RS}").strip().upper()
    
    if len(curp) != 18:
        print(f"  {R}[!] CURP must be 18 characters{RS}")
        return
    
    print(f"\n  {Y}{'=' * 50}{RS}")
    print(f"  {BW}  FORMATS:{RS}")
    print(f"  {Y}{'=' * 50}{RS}\n")
    
    # With dashes
    with_dashes = f"{curp[:4]}-{curp[4:10]}-{curp[10]}-{curp[11:13]}-{curp[13:16]}-{curp[16:18]}"
    print(f"  {C}[+] With dashes: {BW}{with_dashes}{RS}")
    
    # Without dashes
    print(f"  {C}[+] Without dashes: {BW}{curp}{RS}")
    
    # Lowercase
    print(f"  {C}[+] Lowercase: {BW}{curp.lower()}{RS}")
    
    # RFC format
    rfc = curp[:10] + "XXX"
    print(f"  {C}[+] RFC format: {BW}{rfc}{RS}")
    
    # JSON
    data = {
        'curp': curp,
        'initials': curp[:4],
        'birth_date': f"{curp[4:6]}-{curp[6:8]}-{curp[8:10]}",
        'sex': 'Male' if curp[10] == 'H' else 'Female',
        'state': curp[11:13],
        'consonants': curp[13:16],
        'homonymy': curp[16],
        'verification': curp[17]
    }
    print(f"  {C}[+] JSON: {BW}{json.dumps(data, indent=2)}{RS}")
    
    return curp

# ═══════════════════════════════════════════════════════════════════
# MAIN MENU
# ═══════════════════════════════════════════════════════════════════

def main():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - CURP TOOLS v2.0{RS}")
    print(f"  {Y}{Style.BRIGHT}  8 Methods for CURP Generation & Extraction{RS}")
    print()
    print(f"  {R}[!] This tool is for authorized testing only{RS}")
    print()
    
    while True:
        print(f"  {G}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {G}║  {BW}HELL SOCIETY CURP TOOLS{RS}                        {G}║{RS}")
        print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[1]  {BW}CURP Generator (Personal Data){RS}")
        print(f"  {C}[2]  {BW}RENAPO Search (Government){RS}")
        print(f"  {C}[3]  {BW}Bulk CURP Generator{RS}")
        print(f"  {C}[4]  {BW}CURP Validator{RS}")
        print(f"  {C}[5]  {BW}CURP Brute Force (Partial){RS}")
        print(f"  {C}[6]  {BW}CURP Database Search (Dorks){RS}")
        print(f"  {C}[7]  {BW}RFC to CURP Extraction{RS}")
        print(f"  {C}[8]  {BW}CURP Format Converter{RS}")
        print()
        print(f"  {R}[0]  {BW}Exit{RS}")
        print()
        
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {R}[*] Goodbye...{RS}")
            sys.exit(0)
        
        if choice == '1':
            method_generator()
        elif choice == '2':
            method_renapo()
        elif choice == '3':
            method_bulk_generator()
        elif choice == '4':
            method_validator()
        elif choice == '5':
            method_bruteforce()
        elif choice == '6':
            method_dorker()
        elif choice == '7':
            method_rfc_to_curp()
        elif choice == '8':
            method_converter()
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
