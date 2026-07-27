#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════╗
║  HELL SOCIETY - CURP ULTIMATE TOOLKIT v1.0                      ║
║  Created by: HELL SOCIETY Community                              ║
║  Ultimate CURP generation, extraction & analysis                 ║
╚══════════════════════════════════════════════════════════════════╝

DISCLAIMER: Hell Society assumes no liability for misuse.
"""

import os, sys, re, json, time, random, string, csv, hashlib, urllib.parse, subprocess
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

# ═══════════════════════════════════════════════════════════════════
# CURP CORE
# ═══════════════════════════════════════════════════════════════════
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
STATE_IN = {v:k for k,v in STATE_MAP.items()}
STATE_IN.update({
    'AGUASCALIENTES':'AS','BAJA CALIFORNIA':'BC','BAJA CALIFORNIA SUR':'BS',
    'CAMPECHE':'CC','COAHUILA':'CL','COLIMA':'CM','CHIAPAS':'CS',
    'CHIHUAHUA':'CH','CDMX':'DF','CIUDAD DE MEXICO':'DF','DISTRITO FEDERAL':'DF','DF':'DF',
    'DURANGO':'DG','GUANAJUATO':'GT','GUERRERO':'GR','HIDALGO':'HG',
    'JALISCO':'JC','MEXICO':'MC','ESTADO DE MEXICO':'MC','ESTADO DE MÉXICO':'MC','MC':'MC',
    'MICHOACAN':'MN','MICHOACÁN':'MN','MORELOS':'MS','NAYARIT':'NS',
    'NUEVO LEON':'NL','NUEVO LEÓN':'NL','OAXACA':'OC','PUEBLA':'PL',
    'QUERETARO':'QT','QUERÉTARO':'QT','QUINTANA ROO':'QR',
    'SAN LUIS POTOSI':'SP','SAN LUIS POTOSÍ':'SP','SINALOA':'SL',
    'SONORA':'SR','TABASCO':'TC','TAMAULIPAS':'TS','TLAXCALA':'TL',
    'VERACRUZ':'VZ','YUCATAN':'YN','YUCATÁN':'YN','ZACATECAS':'ZS','EXTRANJERO':'NE'
})

def clean(t):
    t = t.upper().strip()
    for a,p in [('Á','A'),('É','E'),('Í','I'),('Ó','O'),('Ú','U'),('Ü','U')]: t = t.replace(a,p)
    return t

def fv(n):
    for c in n[1:]:
        if c in VOCALS: return c
    return 'X'

def fc(n):
    cs = 'BCDFGHJKLMNPQRSTVWXYZ'
    for c in n[1:]:
        if c in cs: return c
    return 'X'

def calcv(c17):
    d = {chr(i):i-ord('A')+10 if i>=ord('A') else i-ord('0') for i in range(ord('0'),ord('Z')+1)}
    t = sum(d.get(c,0)*(18-i) for i,c in enumerate(c17))
    r = t%10
    return str(10-r) if r else '0'

def mk_curp(name,pat,mat,day,mon,year,sex,state):
    name,clean(pat),clean(mat if mat else 'X')
    name=clean(name); pat=clean(pat); mat=clean(mat) if mat else 'X'
    for p in ['DE','DEL','LA','LOS','LAS','Y','MC','VAN','VON']:
        pat=re.sub(r'\b'+p+r'\b','',pat).strip()
        mat=re.sub(r'\b'+p+r'\b','',mat).strip()
    c=pat[0:1]+fv(pat)+fc(pat)+mat[0:1]
    c+=str(year)[-2:].zfill(2)+str(mon).zfill(2)+str(day).zfill(2)
    c+=sex.upper()
    c+=STATE_IN.get(state.upper().strip(),'NE')
    c+=fc(mat)+fc(name)+'0'
    c+=calcv(c)
    return c

def parse(c):
    if len(c)!=18: return None
    y=int(c[4:6]); yr=1900+y if y>30 else 2000+y
    return {'curp':c,'ini':c[:4],'year':yr,'month':c[6:8],'day':c[8:10],
            'sex':'Male' if c[10]=='H' else 'Female','state_code':c[11:13],
            'state':STATE_MAP.get(c[11:13],'Unknown'),'cons':c[13:16],'hom':c[16],'ver':c[17]}

# ═══════════════════════════════════════════════════════════════════
# METHODS
# ═══════════════════════════════════════════════════════════════════

def m1_generator():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 1: CURP GENERATOR{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    n=input(f"  {Y}[*] Name: {RS}").strip().upper()
    p=input(f"  {Y}[*] Paternal: {RS}").strip().upper()
    m=input(f"  {Y}[*] Maternal: {RS}").strip().upper() or 'X'
    d=input(f"  {Y}[*] Day: {RS}").strip()
    mo=input(f"  {Y}[*] Month: {RS}").strip()
    y=input(f"  {Y}[*] Year: {RS}").strip()
    s=input(f"  {Y}[*] Sex(H/M): {RS}").strip().upper()
    st=input(f"  {Y}[*] State: {RS}").strip()
    curp=mk_curp(n,p,m,d,mo,y,s,st)
    data=parse(curp)
    print(f"\n  {G}[+] CURP: {BW}{curp}{RS}")
    if data: print(f"  {C}    {data['ini']} | {data['day']}/{data['month']}/{data['year']} | {data['sex']} | {data['state']}{RS}")

def m2_batch():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 2: BATCH GENERATOR{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    cnt=int(input(f"  {Y}[*] Count: {RS}").strip() or "100")
    st=input(f"  {Y}[*] State: {RS}").strip() or 'DF'
    age_min=int(input(f"  {Y}[*] Min age: {RS}").strip() or "18")
    age_max=int(input(f"  {Y}[*] Max age: {RS}").strip() or "50")
    cy=datetime.now().year
    names=['JUAN','CARLOS','JOSE','MIGUEL','ANTONIO','PEDRO','LUIS','MARIA','ANA','GUADALUPE','TERESA','PATRICIA','DAVID','DANIEL','FRANCISCO']
    surnames=['GARCIA','RODRIGUEZ','MARTINEZ','LOPEZ','GONZALEZ','HERNANDEZ','PEREZ','SANCHEZ','RAMIREZ','TORRES','FLORES','RIVERA','GOMEZ','DIAZ','CRUZ','MORALES','REYES','GUTIERREZ','ORTIZ','VARGAS']
    results=[]
    for i in range(cnt):
        s=random.choice(['H','M'])
        c=mk_curp(random.choice(names),random.choice(surnames),random.choice(surnames),random.randint(1,28),random.randint(1,12),random.randint(cy-age_max,cy-age_min),s,st)
        results.append(c)
    print(f"\n  {G}[+] Generated {cnt} CURPs{RS}")
    with open('curp_batch.txt','w') as f:
        for c in results: f.write(c+'\n')
    print(f"  {G}[+] Saved: curp_batch.txt{RS}")
    # Show first 20
    for c in results[:20]: print(f"  {C}  {c}{RS}")

def m3_validate():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 3: VALIDATOR{RS}                            {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    curp=input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(curp)!=18: print(f"  {R}[!] Must be 18 chars{RS}"); return
    errs=[]
    for i,c in enumerate(curp[:4]):
        if c not in string.ascii_uppercase: errs.append(f"Pos{i+1}:not letter")
    for i,c in enumerate(curp[4:10]):
        if c not in '0123456789': errs.append(f"Pos{i+5}:not digit")
    if curp[10] not in 'HM': errs.append("Pos11:not H/M")
    if curp[11:13] not in STATE_MAP: errs.append("Pos12-13:bad state")
    if curp[17]!=calcv(curp[:17]): errs.append(f"Pos18:should be {calcv(curp[:17])}")
    if errs:
        print(f"  {R}[X] INVALID:{RS}")
        for e in errs: print(f"  {R}    {e}{RS}")
    else:
        print(f"  {G}[+] VALID!{RS}")
        d=parse(curp)
        if d: print(f"  {C}    {d['ini']}|{d['day']}/{d['month']}/{d['year']}|{d['sex']}|{d['state']}{RS}")

def m4_brute():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 4: BRUTE FORCE{RS}                          {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    partial=input(f"  {Y}[*] Partial(?=unknown): {RS}").strip().upper()
    if '?' not in partial: print(f"  {Y}[~] Use ? for unknown positions{RS}"); return
    positions=[i for i,c in enumerate(partial) if c=='?']
    if len(positions)>3: print(f"  {R}[!] Max 3 unknowns{RS}"); return
    results=[]; chars=list(partial); cs=string.ascii_uppercase+'0123456789'
    def gen(idx):
        if idx==len(positions):
            c=''.join(chars)
            if len(c)==18 and c[17]==calcv(c[:17]): results.append(c)
            return
        for ch in cs: chars[positions[idx]]=ch; gen(idx+1)
    print(f"  {Y}[*] Brute forcing...{RS}")
    gen(0)
    print(f"\n  {G}[+] Found {len(results)} valid:{RS}")
    for r in results: print(f"  {C}    {r}{RS}")

def m5_csv_import():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 5: CSV IMPORT & GENERATE{RS}                  {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    fp=input(f"  {Y}[*] CSV (name,pat,mat,day,month,year,sex,state): {RS}").strip()
    if not os.path.isfile(fp): print(f"  {R}[!] Not found{RS}"); return
    results=[]
    with open(fp) as f:
        for row in csv.reader(f):
            if len(row)>=8:
                try: results.append(mk_curp(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
                except: pass
    print(f"  {G}[+] Generated {len(results)} CURPs{RS}")
    with open('curp_csv_out.txt','w') as f:
        for c in results: f.write(c+'\n')

def m6_extract_rfc():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 6: RFC EXTRACTOR{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    rfc=input(f"  {Y}[*] RFC(13): {RS}").strip().upper()
    if len(rfc)!=13: print(f"  {R}[!] Must be 13 chars{RS}"); return
    print(f"\n  {C}[*] Extracted:{RS}")
    print(f"  {C}  Initials: {rfc[:4]}{RS}")
    print(f"  {C}  DOB: {rfc[4:6]}-{rfc[6:8]}-{rfc[8:10]}{RS}")
    print(f"  {C}  CURP base: {rfc[:10]}{RS}")
    print(f"  {Y}[~] Use Method 1 with this data{RS}")

def m7_formats():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 7: FORMAT CONVERTER{RS}                     {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    c=input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(c)!=18: print(f"  {R}[!] 18 chars{RS}"); return
    d=parse(c)
    print(f"\n  {C}  Dashed: {BW}{c[:4]}-{c[4:10]}-{c[10]}-{c[11:13]}-{c[13:16]}-{c[16:18]}{RS}")
    print(f"  {C}  Clean: {BW}{c}{RS}")
    print(f"  {C}  Lower: {BW}{c.lower()}{RS}")
    print(f"  {C}  RFC: {BW}{c[:10]}XXX{RS}")
    if d: print(f"  {C}  JSON: {BW}{json.dumps(d,indent=2)}{RS}")

def m8_online():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 8: ONLINE VERIFY{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    c=input(f"  {Y}[*] CURP: {RS}").strip().upper()
    if len(c)!=18: print(f"  {R}[!] 18 chars{RS}"); return
    print(f"\n  {C}[*] Checking...{RS}")
    v=calcv(c[:17]); fv_ok=c[17]==v; st_ok=c[11:13] in STATE_MAP
    print(f"  {G if fv_ok else R}[{'+' if fv_ok else '!'}] Format: {'OK' if fv_ok else 'BAD'}{RS}")
    print(f"  {G if st_ok else R}[{'+' if st_ok else '!'}] State: {'OK' if st_ok else 'BAD'}{RS}")
    d=parse(c)
    if d:
        print(f"  {C}  Name: {d['ini']} | DOB: {d['day']}/{d['month']}/{d['year']} | {d['sex']} | {d['state']}{RS}")

def m9_dorks():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 9: DORK SEARCH{RS}                         {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    s=input(f"  {Y}[*] Search: {RS}").strip()
    dorks=[f'"CURP" "{s}" filetype:csv',f'"CURP" "{s}" filetype:xlsx',f'"{s}" "CURP" "RFC" "NOMBRE"',f'"{s}" "CURP" site:pastebin.com',f'"{s}" ext:csv "CURP" "RFC"',f'"CURP" "{s}" ext:sql',f'inurl:"curp" "{s}"',f'"{s}" "CURP" "DIRECCION" "TELEFONO"',f'"{s}" "CURP" "IMSS"',f'"{s}" "CURP" "NSS"']
    print(f"\n  {Y}{'='*50}{RS}")
    print(f"  {BW}  DORKS:{RS}")
    print(f"  {Y}{'='*50}{RS}\n")
    for i,d in enumerate(dorks,1):
        u=f"https://www.google.com/search?q={urllib.parse.quote(d)}"
        print(f"  {C}[{i:02d}] {BW}{d}{RS}\n  {G}     {u}{RS}\n")

def m10_api():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 10: RENAPO API{RS}                         {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    n=input(f"  {Y}[*] Name: {RS}").strip().upper()
    p=input(f"  {Y}[*] Paternal: {RS}").strip().upper()
    m=input(f"  {Y}[*] Maternal: {RS}").strip().upper()
    d=input(f"  {Y}[*] Day: {RS}").strip(); mo=input(f"  {Y}[*] Month: {RS}").strip(); y=input(f"  {Y}[*] Year: {RS}").strip()
    s=input(f"  {Y}[*] Sex: {RS}").strip().upper(); st=input(f"  {Y}[*] State: {RS}").strip()
    print(f"\n  {C}[*] Querying RENAPO...{RS}")
    try:
        headers={'User-Agent':'Mozilla/5.0 (Linux; Android 13) Chrome/120.0.0.0 Mobile Safari/537.36'}
        resp=requests.get("https://consultas.curp.gob.mx/CurpSP/",params={'nombre':n,'paterno':p,'materno':m,'dia':d,'mes':mo,'year':y,'sexo':s,'entidad':st},headers=headers,timeout=15)
        if resp.status_code==200:
            matches=re.findall(r'[A-Z]{4}\d{6}[HM][A-Z]{2}[B-DF-HJ-NP-TV-Z]{3}[A-Z\d]\d',resp.text)
            if matches: print(f"  {G}[+] CURP: {BW}{matches[0]}{RS}")
            else:
                print(f"  {Y}[~] Not in RENAPO, generating locally...{RS}")
                curp=mk_curp(n,p,m,d,mo,y,s,st)
                print(f"  {G}[+] Generated: {BW}{curp}{RS}")
        else: print(f"  {R}[!] Status {resp.status_code}{RS}")
    except Exception as e: print(f"  {R}[!] Error: {e}{RS}")

def m11_hash():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 11: HASH LOOKUP{RS}                        {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    ht=input(f"  {Y}[*] Type(md5/sha256): {RS}").strip().lower()
    hv=input(f"  {Y}[*] Hash: {RS}").strip().lower()
    print(f"\n  {C}[*] Searching...{RS}")
    try:
        r=requests.get(f"https://md5decrypt.net/en/Api/api.php?hash={hv}&hash_type={ht}&email=hs@hs.com&code=hs2024",timeout=10)
        if r.text and 'not_found' not in r.text: print(f"  {G}[+] MD5Decrypter: {r.text.strip()}{RS}")
        else: print(f"  {Y}[~] Not found{RS}")
    except: print(f"  {R}[!] Error{RS}")

def m12_age():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 12: AGE RANGE{RS}                          {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    ma=int(input(f"  {Y}[*] Min age: {RS}").strip() or "18")
    xa=int(input(f"  {Y}[*] Max age: {RS}").strip() or "40")
    sex=input(f"  {Y}[*] Sex(H/M/BOTH): {RS}").strip().upper() or 'BOTH'
    st=input(f"  {Y}[*] State: {RS}").strip()
    cnt=int(input(f"  {Y}[*] Count: {RS}").strip() or "20")
    cy=datetime.now().year
    names=['JUAN','CARLOS','JOSE','MARIA','ANA','GUADALUPE','TERESA']
    surnames=['GARCIA','RODRIGUEZ','MARTINEZ','LOPEZ','GONZALEZ','HERNANDEZ']
    results=[]
    for i in range(cnt):
        s=random.choice(['H','M']) if sex=='BOTH' else sex[0]
        results.append(mk_curp(random.choice(names),random.choice(surnames),random.choice(surnames),random.randint(1,28),random.randint(1,12),random.randint(cy-xa,cy-ma),s,st))
    print(f"\n  {G}[+] {cnt} CURPs:{RS}")
    for r in results: print(f"  {C}    {r}{RS}")

def m13_breach():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 13: BREACH CHECK{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    c=input(f"  {Y}[*] CURP: {RS}").strip().upper()
    print(f"\n  {C}[*] Checking HIBP...{RS}")
    try:
        r=requests.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{c}",headers={'User-Agent':'HS/1.0'},timeout=10)
        if r.status_code==200:
            bs=r.json(); print(f"  {R}[!] {len(bs)} breaches:{RS}")
            for b in bs: print(f"  {R}    - {b.get('Name','?')}{RS}")
        elif r.status_code==404: print(f"  {G}[+] Clean{RS}")
        else: print(f"  {Y}[~] Status {r.status_code}{RS}")
    except: print(f"  {Y}[~] Connection error{RS}")

def m14_search():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 14: MULTI SEARCH{RS}                       {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    c=input(f"  {Y}[*] CURP: {RS}").strip().upper()
    print(f"\n  {C}[*] Search links:{RS}\n")
    for name,url in [('Google',f"https://www.google.com/search?q=%22{urllib.parse.quote(c)}%22"),('DuckDuckGo',f"https://duckduckgo.com/?q=%22{urllib.parse.quote(c)}%22"),('HIBP',f"https://haveibeenpwned.com/unifiedsearch/{urllib.parse.quote(c)}"),('IntelX',f"https://intelx.io/?s={urllib.parse.quote(c)}"),('DeHashed',f"https://dehashed.com/search?query={urllib.parse.quote(c)}")]:
        print(f"  {C}[{name:12s}] {BW}{url}{RS}")

def m15_export():
    print(f"\n  {G}╔═══════════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  {BW}METHOD 15: EXPORT/IMPORT{RS}                      {G}║{RS}")
    print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}\n")
    print(f"  {C}[1] Import file{RS}")
    print(f"  {C}[2] Export CSV{RS}")
    print(f"  {C}[3] Export JSON{RS}")
    print(f"  {C}[4] Deduplicate{RS}")
    c=input(f"\n  {G}root@hellsociety{C}~{RS}# ").strip()
    if c=='1':
        fp=input(f"  {Y}[*] File: {RS}").strip()
        if os.path.isfile(fp):
            lines=[l.strip().upper() for l in open(fp) if len(l.strip())==18]
            print(f"  {G}[+] {len(lines)} imported{RS}")
            with open('curp_import.txt','w') as f:
                for l in lines: f.write(l+'\n')
    elif c=='2':
        fp=input(f"  {Y}[*] CURP file: {RS}").strip()
        if os.path.isfile(fp):
            curps=[l.strip().upper() for l in open(fp) if len(l.strip())>=18]
            with open('curp.csv','w',newline='') as f:
                w=csv.writer(f); w.writerow(['CURP','Initials','DOB','Sex','State'])
                for cp in curps:
                    d=parse(cp)
                    if d: w.writerow([cp,d['ini'],f"{d['day']}/{d['month']}/{d['year']}",d['sex'],d['state']])
            print(f"  {G}[+] Exported {len(curps)} to curp.csv{RS}")
    elif c=='3':
        fp=input(f"  {Y}[*] CURP file: {RS}").strip()
        if os.path.isfile(fp):
            data=[parse(l.strip().upper()) for l in open(fp) if len(l.strip())>=18 and parse(l.strip().upper())]
            with open('curp.json','w') as f: json.dump(data,f,indent=2)
            print(f"  {G}[+] Exported {len(data)} to curp.json{RS}")
    elif c=='4':
        fp=input(f"  {Y}[*] File: {RS}").strip()
        if os.path.isfile(fp):
            unique=list(set(l.strip().upper() for l in open(fp) if len(l.strip())>=18))
            print(f"  {G}[+] {len(unique)} unique{RS}")
            with open('curp_unique.txt','w') as f:
                for u in unique: f.write(u+'\n')

# ═══════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════

def main():
    os.system('clear' if os.name!='nt' else 'cls')
    print(BANNER)
    print()
    print(f"  {BW}{Style.BRIGHT}  HELL SOCIETY - CURP ULTIMATE TOOLKIT v1.0{RS}")
    print(f"  {Y}{Style.BRIGHT}  15 Professional Methods{RS}")
    print()
    
    while True:
        print(f"  {G}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {G}║  {BW}HELL SOCIETY CURP ULTIMATE{RS}                     {G}║{RS}")
        print(f"  {G}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[01] {BW}Generator{RS}")
        print(f"  {C}[02] {BW}Batch Generator{RS}")
        print(f"  {C}[03] {BW}Validator{RS}")
        print(f"  {C}[04] {BW}Brute Force{RS}")
        print(f"  {C}[05] {BW}CSV Import & Generate{RS}")
        print(f"  {C}[06] {BW}RFC Extractor{RS}")
        print(f"  {C}[07] {BW}Format Converter{RS}")
        print(f"  {C}[08] {BW}Online Verify{RS}")
        print(f"  {C}[09] {BW}Dork Search{RS}")
        print(f"  {C}[10] {BW}RENAPO API{RS}")
        print(f"  {C}[11] {BW}Hash Lookup{RS}")
        print(f"  {C}[12] {BW}Age Range{RS}")
        print(f"  {C}[13] {BW}Breach Check{RS}")
        print(f"  {C}[14] {BW}Multi Search{RS}")
        print(f"  {C}[15] {BW}Export/Import{RS}")
        print()
        print(f"  {R}[00] {BW}Exit{RS}")
        print()
        
        try:
            ch=input(f"  {G}root@hellsociety{C}~{RS}# ").strip()
        except (EOFError,KeyboardInterrupt):
            print(f"\n  {Y}[*] Goodbye...{RS}"); sys.exit(0)
        
        ms={'1':m1_generator,'2':m2_batch,'3':m3_validate,'4':m4_brute,'5':m5_csv_import,'6':m6_extract_rfc,'7':m7_formats,'8':m8_online,'9':m9_dorks,'10':m10_api,'11':m11_hash,'12':m12_age,'13':m13_breach,'14':m14_search,'15':m15_export,'0':None,'00':None}
        
        if ch in ms and ms[ch]: ms[ch]()
        elif ch in ['0','00']: print(f"\n  {Y}[*] Goodbye from Hell Society...{RS}"); sys.exit(0)
        else: print(f"  {R}[!] Invalid{RS}")
        
        print()
        input(f"  {C}[*] Press ENTER...{RS}")
        os.system('clear' if os.name!='nt' else 'cls')
        print(BANNER)
        print()

if __name__ == "__main__":
    main()
