#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - CURP FULL FRAMEWORK v3.0                        ║
║  Created by: HELL SOCIETY Community                              ║
║  15 Methods: Generator, Scanner, Brute, OSINT, Database, OCR    ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: Hell Society assumes no liability for misuse.
"""

import os, sys, re, json, hashlib, time, random, string, urllib.parse, csv
from datetime import datetime, date

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except:
    os.system("pip3 install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

try:
    import requests
except:
    os.system("pip3 install requests 2>/dev/null")
    import requests

R = Fore.RED; G = Fore.GREEN; Y = Fore.YELLOW; C = Fore.CYAN; W = Fore.WHITE
BW = Style.BRIGHT + Fore.WHITE; BR = Style.BRIGHT + Fore.RED
BG = Style.BRIGHT + Fore.GREEN; BC = Style.BRIGHT + Fore.CYAN
BY = Style.BRIGHT + Fore.YELLOW; RS = Style.RESET_ALL

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

VOCALS = ['A','E','I','O','U']
STATE_MAP = {
    'AS':'Aguascalientes','BC':'Baja California','BS':'Baja California Sur',
    'CC':'Campeche','CL':'Coahuila','CM':'Colima','CS':'Chiapas',
    'CH':'Chihuahua','DF':'Ciudad de México','DG':'Durango',
    'GT':'Guanajuato','GR':'Guerrero','HG':'Hidalgo','JC':'Jalisco',
    'MC':'Estado de México','MN':'Michoacán','MS':'Morelos',
    'NS':'Nayarit','NL':'Nuevo León','OC':'Oaxaca','PL':'Puebla',
    'QT':'Querétaro','QR':'Quintana Roo','SP':'San Luis Potosí',
    'SL':'Sinaloa','SR':'Sonora','TC':'Tabasco','TS':'Tamaulipas',
    'TL':'Tlaxcala','VZ':'Veracruz','YN':'Yucatán','ZS':'Zacatecas','NE':'Extranjero'
}
STATE_INPUT = {
    'AGUASCALIENTES':'AS','BAJA CALIFORNIA':'BC','BAJA CALIFORNIA SUR':'BS',
    'CAMPECHE':'CC','COAHUILA':'CL','COLIMA':'CM','CHIAPAS':'CS',
    'CHIHUAHUA':'CH','CIUDAD DE MEXICO':'DF','CDMX':'DF','DF':'DF',
    'DURANGO':'DG','GUANAJUATO':'GT','GUERRERO':'GR','HIDALGO':'HG',
    'JALISCO':'JC','ESTADO DE MEXICO':'MC','MEXICO':'MC','MC':'MC',
    'MICHOACAN':'MN','MICHOACÁN':'MN','MORELOS':'MS','NAYARIT':'NS',
    'NUEVO LEON':'NL','OAXACA':'OC','PUEBLA':'PL','QUERETARO':'QT',
    'QUINTANA ROO':'QR','SAN LUIS POTOSI':'SP','SINALOA':'SL',
    'SONORA':'SR','TABASCO':'TC','TAMAULIPAS':'TS','TLAXCALA':'TL',
    'VERACRUZ':'VZ','YUCATAN':'YN','ZACATECAS':'ZS','EXTRANJERO':'NE'
}

def strip_accents(t):
    t = t.upper().strip()
    for a,p in [('Á','A'),('É','E'),('Í','I'),('Ó','O'),('Ú','U'),('Ü','U')]:
        t = t.replace(a,p)
    return t

def get_first_vowel(name):
    for c in name[1:]:
        if c in VOCALS: return c
    return 'X'

def get_consonant(name):
    cons = 'BCDFGHJKLMNPQRSTVWXYZ'
    for c in name[1:]:
        if c in cons: return c
    return 'X'

def calc_ver(curp17):
    d = {chr(i):i-ord('A')+10 if i>=ord('A') else i-ord('0') for i in range(ord('0'),ord('Z')+1)}
    total = sum(d.get(c,0)*(18-i) for i,c in enumerate(curp17))
    r = total % 10
    return str(10-r) if r!=0 else '0'

def gen_curp(name,paternal,maternal,day,month,year,sex,state):
    name = strip_accents(name)
    paternal = strip_accents(paternal)
    maternal = strip_accents(maternal) if maternal else 'X'
    for p in ['DE','DEL','LA','LOS','LAS','Y','MC','VAN','VON']:
        paternal = re.sub(r'\b'+p+r'\b','',paternal).strip()
        maternal = re.sub(r'\b'+p+r'\b','',maternal).strip()
    c = paternal[0:1]+get_first_vowel(paternal)+get_consonant(paternal)+maternal[0:1]
    c += str(year)[-2:].zfill(2)+str(month).zfill(2)+str(day).zfill(2)
    c += sex.upper()
    sc = STATE_INPUT.get(state.upper().strip(),'NE')
    c += sc+get_consonant(maternal)+get_consonant(name)+'0'
    c += calc_ver(c)
    return c

def parse_curp(c):
    if len(c)!=18: return None
    y = int(c[4:6])
    yr = 1900+y if y>30 else 2000+y
    return {'curp':c,'initials':c[:4],'year':yr,'month':c[6:8],'day':c[8:10],
            'sex':'Male' if c[10]=='H' else 'Female','sex_code':c[10],
            'state_code':c[11:13],'state_name':STATE_MAP.get(c[11:13],'Unknown'),
            'consonants':c[13:16],'homonymy':c[16],'verification':c[17]}

# ═══════════════════════════════════════════════════════════════════
# 15 METHODS
# ═══════════════════════════════════════════════════════════════════

def m1_manual():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 1: MANUAL CURP GENERATOR{RS}                  {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    name = input(f"  {Y}[*] Name: {RS}").strip().upper()
    paternal = input(f"  {Y}[*] Paternal: {RS}").strip().upper()
    maternal = input(f"  {Y}[*] Maternal: {RS}").strip().upper() or 'X'
    d = input(f"  {Y}[*] Day: {RS}").strip()
    m = input(f"  {Y}[*] Month: {RS}").strip()
    y = input(f"  {Y}[*] Year: {RS}").strip()
    s = input(f"  {Y}[*] Sex (H/M): {RS}").strip().upper()
    st = input(f"  {Y}[*] State: {RS}").strip()
    curp = gen_curp(name,paternal,maternal,d,m,y,s,st)
    data = parse_curp(curp)
    print(f"\n  {G}[+] CURP: {BW}{curp}{RS}")
    if data:
        print(f"  {C}    Name: {data['initials']} | Birth: {data['day']}/{data['month']}/{data['year']}")
        print(f"  {C}    Sex: {data['sex']} | State: {data['state_name']}{RS}")

def m2_auto():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 2: AUTO GENERATE FROM DATA FILE{RS}            {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    filepath = input(f"  {Y}[*] CSV file path (name,paternal,maternal,day,month,year,sex,state): {RS}").strip()
    if not os.path.isfile(filepath):
        print(f"  {R}[!] File not found{RS}")
        return
    results = []
    with open(filepath,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row)>=8:
                curp = gen_curp(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7])
                results.append(curp)
    print(f"\n  {G}[+] Generated {len(results)} CURPs{RS}")
    out = "curp_auto_results.txt"
    with open(out,'w') as f:
        for c in results: f.write(c+'\n')
    print(f"  {G}[+] Saved to: {out}{RS}")

def m3_validate():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 3: CURP VALIDATOR{RS}                         {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp = input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(curp)!=18:
        print(f"  {R}[!] Must be 18 chars (got {len(curp)}){RS}")
        return
    errors = []
    for i,c in enumerate(curp[:4]):
        if c not in string.ascii_uppercase: errors.append(f"Pos {i+1}: not letter")
    for i,c in enumerate(curp[4:10]):
        if c not in '0123456789': errors.append(f"Pos {i+5}: not digit")
    if curp[10] not in 'HM': errors.append("Pos 11: must be H or M")
    if curp[11:13] not in STATE_MAP: errors.append("Pos 12-13: invalid state")
    calc = calc_ver(curp[:17])
    if curp[17]!=calc: errors.append(f"Pos 18: should be {calc}")
    if errors:
        print(f"  {R}[X] INVALID:{RS}")
        for e in errors: print(f"  {R}    {e}{RS}")
    else:
        print(f"  {G}[+] VALID!{RS}")
        data = parse_curp(curp)
        if data:
            print(f"  {C}    Name: {data['initials']} | DOB: {data['day']}/{data['month']}/{data['year']}")
            print(f"  {C}    Sex: {data['sex']} | State: {data['state_name']}{RS}")

def m4_brute():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 4: PARTIAL BRUTE FORCE{RS}                    {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    partial = input(f"  {Y}[*] Partial CURP (? for unknown): {RS}").strip().upper()
    if '?' not in partial:
        print(f"  {Y}[~] No ? found. Use ? for missing positions{RS}")
        return
    positions = [i for i,c in enumerate(partial) if c=='?']
    if len(positions)>3:
        print(f"  {R}[!] Too many unknowns (max 3){RS}")
        return
    results = []
    chars = list(partial)
    cs = string.ascii_uppercase+'0123456789'
    def gen(idx):
        if idx==len(positions):
            c = ''.join(chars)
            if len(c)==18 and c[17]==calc_ver(c[:17]):
                results.append(c)
            return
        for ch in cs:
            chars[positions[idx]] = ch
            gen(idx+1)
    print(f"  {Y}[*] Brute forcing {len(positions)} positions...{RS}")
    gen(0)
    print(f"\n  {G}[+] Found {len(results)} valid CURPs:{RS}")
    for r in results: print(f"  {C}    {r}{RS}")

def m5_bulk():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 5: BULK RANDOM GENERATOR{RS}                  {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    count = int(input(f"  {Y}[*] Count: {RS}").strip() or "50")
    names_m = ['JUAN','CARLOS','JOSE','MIGUEL','ANTONIO','PEDRO','LUIS','FRANCISCO','RAFAEL','DAVID']
    names_f = ['MARIA','ANA','GUADALUPE','JUANA','MARGARITA','VERONICA','PATRICIA','TERESA','ISABEL']
    surnames = ['GARCIA','RODRIGUEZ','MARTINEZ','LOPEZ','GONZALEZ','HERNANDEZ','PEREZ','SANCHEZ','RAMIREZ','TORRES','FLORES','RIVERA','GOMEZ','DIAZ','CRUZ','MORALES','REYES','ORTIZ','VARGAS','CASTRO']
    states = list(STATE_MAP.values())
    results = []
    for i in range(count):
        n = random.choice(names_m+names_f)
        p = random.choice(surnames)
        mt = random.choice(surnames)
        curp = gen_curp(n,p,mt,random.randint(1,28),random.randint(1,12),random.randint(1940,2005),random.choice(['H','M']),random.choice(states))
        results.append(curp)
    print(f"\n  {G}[+] Generated {count} CURPs{RS}")
    with open('curp_bulk.txt','w') as f:
        for c in results: f.write(c+'\n')
    print(f"  {G}[+] Saved to: curp_bulk.txt{RS}")

def m6_dorks():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 6: DATABASE DORKER{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    search = input(f"  {Y}[*] Search (name or CURP): {RS}").strip()
    dorks = [
        f'"CURP" "{search}" filetype:csv',
        f'"CURP" "{search}" filetype:xlsx',
        f'"CURP" "{search}" filetype:sql',
        f'"{search}" "CURP" "RFC" "NOMBRE"',
        f'"{search}" "CURP" site:pastebin.com',
        f'"{search}" ext:csv "CURP"',
        f'"CURP" "{search}" ext:xls',
        f'"{search}" "CURP" "RFC" ext:txt',
        f'inurl:"curp" "{search}"',
        f'"{search}" "CURP" "DIRECCION"',
    ]
    print(f"\n  {Y}{'='*50}{RS}")
    print(f"  {BW}  DORKS:{RS}")
    print(f"  {Y}{'='*50}{RS}\n")
    for i,d in enumerate(dorks,1):
        url = f"https://www.google.com/search?q={urllib.parse.quote(d)}"
        print(f"  {C}[{i:02d}] {BW}{d}{RS}")
        print(f"  {G}     {url}{RS}\n")

def m7_rfc():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 7: RFC TO CURP EXTRACTOR{RS}                  {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    rfc = input(f"  {Y}[*] RFC (13 chars): {RS}").strip().upper()
    if len(rfc)!=13:
        print(f"  {R}[!] RFC must be 13 chars{RS}")
        return
    print(f"\n  {C}[*] Extracted:{RS}")
    print(f"  {C}    Initials: {rfc[:4]}{RS}")
    print(f"  {C}    Birth: {rfc[4:6]}-{rfc[6:8]}-{rfc[8:10]}{RS}")
    print(f"  {C}    CURP start: {rfc[:10]}{RS}")
    print(f"  {Y}[~] Use Method 1 with this data for full CURP{RS}")

def m8_converter():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 8: FORMAT CONVERTER{RS}                      {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp = input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(curp)!=18:
        print(f"  {R}[!] Must be 18 chars{RS}")
        return
    data = parse_curp(curp)
    print(f"\n  {Y}{'='*50}{RS}")
    print(f"  {BW}  FORMATS:{RS}")
    print(f"  {Y}{'='*50}{RS}")
    print(f"  {C}  With dashes: {BW}{curp[:4]}-{curp[4:10]}-{curp[10]}-{curp[11:13]}-{curp[13:16]}-{curp[16:18]}{RS}")
    print(f"  {C}  Clean: {BW}{curp}{RS}")
    print(f"  {C}  Lower: {BW}{curp.lower()}{RS}")
    print(f"  {C}  RFC: {BW}{curp[:10]}XXX{RS}")
    print(f"  {C}  JSON: {BW}{json.dumps(data,indent=2)}{RS}")

def m9_online():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 9: ONLINE VERIFICATION{RS}                    {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp = input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(curp)!=18:
        print(f"  {R}[!] Invalid{RS}")
        return
    print(f"\n  {C}[*] Checking services...{RS}")
    calc = calc_ver(curp[:17])
    fmt_ok = (curp[17]==calc)
    state_ok = curp[11:13] in STATE_MAP
    print(f"  {G if fmt_ok else R}[{'+' if fmt_ok else '!'}] Format: {'VALID' if fmt_ok else 'INVALID'}{RS}")
    print(f"  {G if state_ok else R}[{'+' if state_ok else '!'}] State: {'VALID' if state_ok else 'INVALID'}{RS}")
    try:
        data = parse_curp(curp)
        headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile Safari/537.36'}
        url = f"https://consultas.curp.gob.mx/CurpSP/"
        params = {'nombre':data['initials'][3],'paterno':data['initials'][0:3],'materno':'X','dia':data['day'],'mes':data['month'],'year':str(data['year']),'sexo':data['sex_code'],'entidad':data['state_name']}
        resp = requests.get(url,params=params,headers=headers,timeout=15)
        print(f"  {G if resp.status_code==200 else R}[{'+' if resp.status_code==200 else '!'}] RENAPO: {'OK' if resp.status_code==200 else f'Error {resp.status_code}'}{RS}")
    except:
        print(f"  {Y}[~] RENAPO: Connection error{RS}")

def m10_ocr():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 10: CURP FROM IMAGE (OCR){RS}                {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    img_path = input(f"  {Y}[*] Image path: {RS}").strip()
    if not os.path.isfile(img_path):
        print(f"  {R}[!] File not found{RS}")
        return
    try:
        from PIL import Image
        import pytesseract
        img = Image.open(img_path)
        text = pytesseract.image_to_string(img)
        matches = re.findall(r'[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d',text)
        if matches:
            print(f"\n  {G}[+] Found {len(matches)} CURP(s):{RS}")
            for m in matches:
                d = parse_curp(m)
                print(f"  {C}    {m} | {d['sex']} | {d['state_name']}{RS}" if d else f"  {C}    {m}{RS}")
        else:
            print(f"  {Y}[~] No CURP found{RS}")
    except ImportError:
        print(f"  {R}[!] Install: pip3 install pytesseract && pkg install tesseract{RS}")

def m11_hash():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 11: HASH LOOKUP{RS}                         {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    htype = input(f"  {Y}[*] Type (md5/sha256): {RS}").strip().lower()
    hval = input(f"  {Y}[*] Hash: {RS}").strip().lower()
    print(f"\n  {C}[*] Searching hash databases...{RS}")
    for svc,url in [("MD5Decrypter",f"https://md5decrypt.net/en/Api/api.php?hash={hval}&hash_type={htype}&email=hs@hs.com&code=hs2024"),("CrackStation",f"https://crackstation.net/api.php?key=hs2024&hash={hval}")]:
        try:
            resp = requests.get(url,timeout=10)
            if resp.text and 'not_found' not in resp.text:
                print(f"  {G}[+] {svc}: {resp.text.strip()}{RS}")
            else:
                print(f"  {Y}[~] {svc}: Not found{RS}")
        except:
            print(f"  {R}[X] {svc}: Error{RS}")

def m12_age():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 12: AGE RANGE GENERATOR{RS}                  {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    ma = int(input(f"  {Y}[*] Min age: {RS}").strip() or "18")
    xa = int(input(f"  {Y}[*] Max age: {RS}").strip() or "40")
    sex = input(f"  {Y}[*] Sex (H/M/BOTH): {RS}").strip().upper() or 'BOTH'
    state = input(f"  {Y}[*] State: {RS}").strip()
    count = int(input(f"  {Y}[*] Count: {RS}").strip() or "20")
    cy = datetime.now().year
    names = ['JUAN','CARLOS','JOSE','MIGUEL','MARIA','ANA','GUADALUPE','TERESA']
    surnames = ['GARCIA','RODRIGUEZ','MARTINEZ','LOPEZ','GONZALEZ','HERNANDEZ','PEREZ','SANCHEZ']
    results = []
    for i in range(count):
        s = random.choice(['H','M']) if sex=='BOTH' else sex[0]
        curp = gen_curp(random.choice(names),random.choice(surnames),random.choice(surnames),random.randint(1,28),random.randint(1,12),random.randint(cy-xa,cy-ma),s,state)
        results.append(curp)
    print(f"\n  {G}[+] Generated {count} CURPs:{RS}")
    for r in results: print(f"  {C}    {r}{RS}")
    with open('curp_age.txt','w') as f:
        for r in results: f.write(r+'\n')

def m13_breaches():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 13: BREACH CHECKER{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp = input(f"  {Y}[*] CURP: {RS}").strip().upper()
    print(f"\n  {C}[*] Checking breach databases...{RS}")
    # HIBP
    try:
        headers = {'User-Agent':'HS-Tool/1.0'}
        resp = requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{curp}",headers=headers,timeout=10)
        if resp.status_code==200:
            breaches = resp.json()
            print(f"  {R}[!] Found in {len(breaches)} breaches:{RS}")
            for b in breaches: print(f"  {R}    - {b.get('Name','?')}{RS}")
        elif resp.status_code==404:
            print(f"  {G}[+] Not found in HIBP{RS}")
        else:
            print(f"  {Y}[~] HIBP: Status {resp.status_code}{RS}")
    except:
        print(f"  {Y}[~] HIBP: Connection error{RS}")

def m14_search():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 14: MULTI-PLATFORM SEARCH{RS}                 {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp = input(f"  {Y}[*] CURP to search: {RS}").strip().upper()
    print(f"\n  {C}[*] Searching across platforms...{RS}\n")
    platforms = {
        'Google': f"https://www.google.com/search?q=%22{urllib.parse.quote(curp)}%22",
        'DuckDuckGo': f"https://duckduckgo.com/?q=%22{urllib.parse.quote(curp)}%22",
        'Pastebin': f"https://site:pastebin.com/search?q={urllib.parse.quote(curp)}",
        'HaveIBeenPwned': f"https://haveibeenpwned.com/unifiedsearch/{urllib.parse.quote(curp)}",
        'Scylla': f"https://scylla.sh/search?q=CURP:{curp}&size=10",
        'IntelX': f"https://intelx.io/?s={urllib.parse.quote(curp)}",
        'DeHashed': f"https://dehashed.com/search?query={urllib.parse.quote(curp)}",
    }
    for name,url in platforms.items():
        print(f"  {C}[{name:20s}] {BW}{url}{RS}")
    print(f"\n  {Y}[~] Open links to search manually{RS}")

def m15_export():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 15: DATABASE EXPORT/IMPORT{RS}                {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    print(f"  {C}[1] Import CURP list{RS}")
    print(f"  {C}[2] Export to CSV{RS}")
    print(f"  {C}[3] Export to JSON{RS}")
    print(f"  {C}[4] Deduplicate{RS}")
    print()
    c = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
    
    if c == '1':
        fp = input(f"  {Y}[*] File path: {RS}").strip()
        if os.path.isfile(fp):
            with open(fp) as f:
                lines = [l.strip().upper() for l in f if len(l.strip())==18]
            print(f"  {G}[+] Imported {len(lines)} CURPs{RS}")
            with open('curp_imported.txt','w') as f:
                for l in lines: f.write(l+'\n')
            print(f"  {G}[+] Saved to: curp_imported.txt{RS}")
    elif c == '2':
        fp = input(f"  {Y}[*] CURP file: {RS}").strip()
        if os.path.isfile(fp):
            with open(fp) as f:
                curps = [l.strip().upper() for l in f if len(l.strip())>=18]
            with open('curp_export.csv','w',newline='') as f:
                w = csv.writer(f)
                w.writerow(['CURP','Initials','DOB','Sex','State'])
                for cp in curps:
                    d = parse_curp(cp)
                    if d: w.writerow([cp,d['initials'],f"{d['day']}/{d['month']}/{d['year']}",d['sex'],d['state_name']])
            print(f"  {G}[+] Exported {len(curps)} to curp_export.csv{RS}")
    elif c == '3':
        fp = input(f"  {Y}[*] CURP file: {RS}").strip()
        if os.path.isfile(fp):
            with open(fp) as f:
                curps = [l.strip().upper() for l in f if len(l.strip())>=18]
            data = []
            for cp in curps:
                d = parse_curp(cp)
                if d: data.append(d)
            with open('curp_export.json','w') as f:
                json.dump(data,f,indent=2)
            print(f"  {G}[+] Exported {len(data)} to curp_export.json{RS}")
    elif c == '4':
        fp = input(f"  {Y}[*] File: {RS}").strip()
        if os.path.isfile(fp):
            with open(fp) as f:
                lines = list(set(l.strip().upper() for l in f if len(l.strip())>=18))
            print(f"  {G}[+] {len(lines)} unique CURPs{RS}")
            with open('curp_unique.txt','w') as f:
                for l in lines: f.write(l+'\n')

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    os.system('clear' if os.name!='nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - CURP FULL FRAMEWORK v3.0{RS}")
    print(f"  {Y}{Style.BRIGHT}  15 Methods for CURP Generation & Extraction{RS}")
    print()
    print(f"  {R}[!] This tool is for authorized testing only{RS}")
    print()
    
    while True:
        print(f"  {G}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {G}║  {BW}HELL SOCIETY CURP FRAMEWORK{RS}                      {G}║{RS}")
        print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[01] {BW}Manual CURP Generator{RS}")
        print(f"  {C}[02] {BW}Auto Generate from CSV{RS}")
        print(f"  {C}[03] {BW}CURP Validator{RS}")
        print(f"  {C}[04] {BW}Partial Brute Force{RS}")
        print(f"  {C}[05] {BW}Bulk Random Generator{RS}")
        print(f"  {C}[06] {BW}Database Dorker{RS}")
        print(f"  {C}[07] {BW}RFC to CURP Extractor{RS}")
        print(f"  {C}[08] {BW}Format Converter{RS}")
        print(f"  {C}[09] {BW}Online Verification{RS}")
        print(f"  {C}[10] {BW}CURP from Image (OCR){RS}")
        print(f"  {C}[11] {BW}Hash Lookup (MD5/SHA256){RS}")
        print(f"  {C}[12] {BW}Age Range Generator{RS}")
        print(f"  {C}[13] {BW}Breach Checker{RS}")
        print(f"  {C}[14] {BW}Multi-Platform Search{RS}")
        print(f"  {C}[15] {BW}Database Export/Import{RS}")
        print()
        print(f"  {R}[00] {BW}Exit{RS}")
        print()
        
        try:
            choice = input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Y}[*] Goodbye...{RS}")
            sys.exit(0)
        
        methods = {
            '1':m1_manual,'2':m2_auto,'3':m3_validate,'4':m4_brute,
            '5':m5_bulk,'6':m6_dorks,'7':m7_rfc,'8':m8_converter,
            '9':m9_online,'10':m10_ocr,'11':m11_hash,'12':m12_age,
            '13':m13_breaches,'14':m14_search,'15':m15_export,'0':None,'00':None
        }
        
        if choice in methods and methods[choice]:
            methods[choice]()
        elif choice in ['0','00']:
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
