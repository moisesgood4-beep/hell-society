#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HACKING TOOL - HELL SOCIETY v6                                ║
# ║  Created by: HELL SOCIETY Community                              ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import sys
import time
import signal

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null")
    try:
        from colorama import init, Fore, Back, Style
        init(autoreset=True)
    except:
        class Fore:
            RED='\033[31m'; GREEN='\033[32m'; YELLOW='\033[33m'
            CYAN='\033[36m'; WHITE='\033[37m'
        class Style:
            BRIGHT='\033[1m'; RESET_ALL='\033[0m'
        def init(**kw): pass

R  = Fore.RED; G  = Fore.GREEN; Y  = Fore.YELLOW
C  = Fore.CYAN; W  = Fore.WHITE
BR = Style.BRIGHT + Fore.RED; BG = Style.BRIGHT + Fore.GREEN
BY = Style.BRIGHT + Fore.YELLOW; BC = Style.BRIGHT + Fore.CYAN
BW = Style.BRIGHT + Fore.WHITE
RS = Style.RESET_ALL

TOOL_BASE = os.path.dirname(os.path.abspath(__file__))
VERSION = "v6.0"

# ═══════════════════════════════════════════════════════════════════
# BANNER BRAILLE - HELL SOCIETY
# ═══════════════════════════════════════════════════════════════════
BRB = f"""{R}⠉⠉⠉⠉⠁⠀⠀⠀⠀⠒⠂⠰⠤⢤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
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
# ANDROID ICON
# ═══════════════════════════════════════════════════════════════════
ANDROID_ICON = f"""
  {G}   ┌───────────────────┐{RS}
  {G}   │  ┌─────────────┐  │{RS}
  {G}   │  │  ┌──────┐   │  │{RS}
  {G}   │  │  │ {Y}▓▓▓▓{G} │   │  │{RS}
  {G}   │  │  │ {Y}▓▓▓▓{G} │   │  │{RS}
  {G}   │  │  └──────┘   │  │{RS}
  {G}   │  │  {G}┌────────┐  │  │{RS}
  {G}   │  │  │{Y} HELL  {G}│  │  │{RS}
  {G}   │  │  │{Y}SOCIETY{G}│  │  │{RS}
  {G}   │  │  └────────┘  │  │{RS}
  {G}   │  └─────────────┘  │{RS}
  {G}   │   ┌─┐       ┌─┐   │{RS}
  {G}   └───┤ ├───────┤ ├───┘{RS}
  {G}       └─┘       └─┘{RS}"""

# ═══════════════════════════════════════════════════════════════════
# ALL 118 TOOLS
# ═══════════════════════════════════════════════════════════════════
ALL_TOOLS = [
    # ── OFFENSIVE 1-38 ──
    (1,   "SQL Injection Scanner",        "offensive/01_sql_injection_scanner.py"),
    (2,   "XSS Scanner",                  "offensive/02_xss_scanner.py"),
    (3,   "Directory Fuzzer",             "offensive/03_directory_fuzzer.py"),
    (4,   "Subdomain Enumeration",        "offensive/04_subdomain_enum.py"),
    (5,   "Port Scanner",                 "offensive/05_port_scanner.py"),
    (6,   "Hash Cracker",                 "offensive/06_hash_cracker.py"),
    (7,   "HTTP Header Analyzer",         "offensive/07_header_analyzer.py"),
    (8,   "Web Crawler",                  "offensive/08_web_crawler.py"),
    (9,   "SSL/TLS Analyzer",             "offensive/09_ssl_analyzer.py"),
    (10,  "CMS Scanner",                  "offensive/10_cms_scanner.py"),
    (11,  "API Security Scanner",         "offensive/11_api_scanner.py"),
    (12,  "Phishing Framework",           "offensive/12_phishing_framework.py"),
    (13,  "Reverse Shell Generator",      "offensive/13_reverse_shell.py"),
    (14,  "LFI/RFI Scanner",              "offensive/14_lfi_scanner.py"),
    (15,  "CSRF Scanner",                 "offensive/15_csrf_scanner.py"),
    (16,  "IDOR Scanner",                 "offensive/16_idor_scanner.py"),
    (17,  "SSRF Scanner",                 "offensive/17_ssrf_scanner.py"),
    (18,  "Command Injection",            "offensive/18_command_injection.py"),
    (19,  "Web Vuln Scanner",             "offensive/19_web_vuln_scanner.py"),
    (20,  "Password Brute Force",         "offensive/20_password_bruteforce.py"),
    (21,  "Wireless Sniffer",             "offensive/21_wireless_sniffer.py"),
    (22,  "JWT Token Attacker",           "offensive/22_jwt_attacker.py"),
    (23,  "XXE Scanner",                  "offensive/23_xxe_scanner.py"),
    (24,  "SSTI Scanner",                 "offensive/24_ssti_scanner.py"),
    (25,  "Dorker",                       "offensive/25_dorker.py"),
    (26,  "WebSocket Interceptor",        "offensive/26_websocket_interceptor.py"),
    (27,  "GraphQL Explorer",             "offensive/27_graphql_explorer.py"),
    (28,  "API Fuzzer",                   "offensive/28_api_fuzzer.py"),
    (29,  "Session Hijacker",             "offensive/29_session_hijacker.py"),
    (30,  "Email Spoofer",                "offensive/30_email_spoofer.py"),
    (31,  "Web Defacement Tester",        "offensive/31_web_defacement_tester.py"),
    (32,  "Database Extractor",           "offensive/32_database_extractor.py"),
    (33,  "Database Dumper",              "offensive/33_database_dumper.py"),
    (34,  "ExitTool (BlackEye)",          "offensive/34_exittool.py"),
    (35,  "RAT Framework (Server)",       "offensive/rat_framework/rat_server.py"),
    (36,  "RAT Framework (Client)",       "offensive/rat_framework/rat_client.py"),
    (37,  "Payload & Steganography",      "offensive/35_payload_generator.py"),
    (38,  "Advanced Tools (Keylogger)",   "offensive/36_advanced_tools.py"),
    # ── DEFENSIVE 39-68 ──
    (39,  "System Hardening",             "defensive/01_system_hardening.py"),
    (40,  "Log Analyzer",                 "defensive/02_log_analyzer.py"),
    (41,  "Network Monitor",              "defensive/03_network_monitor.py"),
    (42,  "Vulnerability Scanner",        "defensive/04_vulnerability_scanner.py"),
    (43,  "IDS/IPS Detector",             "defensive/05_ids_ips_detector.py"),
    (44,  "Malware Scanner",              "defensive/06_malware_scanner.py"),
    (45,  "WAF Configurator",             "defensive/07_waf_configurator.py"),
    (46,  "Certificate Monitor",          "defensive/08_certificate_monitor.py"),
    (47,  "Brute Force Detector",         "defensive/09_brute_force_detector.py"),
    (48,  "Traffic Analyzer",             "defensive/10_traffic_analyzer.py"),
    (49,  "File Integrity Checker",       "defensive/11_file_integrity_checker.py"),
    (50,  "Firewall Analyzer",            "defensive/12_firewall_analyzer.py"),
    (51,  "Password Policy Checker",      "defensive/13_password_policy_checker.py"),
    (52,  "Docker Security",              "defensive/14_docker_security.py"),
    (53,  "Web App Security Scanner",     "defensive/15_web_app_scanner.py"),
    (54,  "Incident Responder",           "defensive/16_incident_responder.py"),
    (55,  "Backup Validator",             "defensive/17_backup_validator.py"),
    (56,  "Encryption Tool",              "defensive/18_encryption_tool.py"),
    (57,  "Honeypot",                     "defensive/19_honeypot.py"),
    (58,  "Ransomware Detector",          "defensive/20_ransomware_detector.py"),
    (59,  "API Security Checker",         "defensive/21_api_security_checker.py"),
    (60,  "CVE Checker",                  "defensive/22_cve_checker.py"),
    (61,  "Network Segmentation",         "defensive/23_network_segmentation.py"),
    (62,  "Zero-Day Detector",            "defensive/24_zero_day_detector.py"),
    (63,  "Privilege Escalation Detect",  "defensive/25_privilege_escalation_detector.py"),
    (64,  "DLP Scanner",                  "defensive/26_dlp_scanner.py"),
    (65,  "Email Header Analyzer",        "defensive/27_email_header_analyzer.py"),
    (66,  "SSL Pinning Checker",          "defensive/28_ssl_pinning_checker.py"),
    (67,  "Threat Intel Feed",            "defensive/29_threat_intel_feed.py"),
    (68,  "Audit Compliance",             "defensive/30_audit_compliance.py"),
    # ── OSINT & DOXING 69-118 ──
    (69,  "Email OSINT",                  "osint/01_email_osint.py"),
    (70,  "Username Recon",               "osint/02_username_recon.py"),
    (71,  "IP Geolocation",               "osint/03_ip_geolocation.py"),
    (72,  "Domain Recon",                 "osint/04_domain_recon.py"),
    (73,  "Phone Recon",                  "osint/05_phone_recon.py"),
    (74,  "Social Media Scraper",         "osint/06_social_media_scraper.py"),
    (75,  "Web Archive Recon",            "osint/07_web_archive_recon.py"),
    (76,  "Dork Engine",                  "osint/08_dork_engine.py"),
    (77,  "People Search",                "osint/09_people_search.py"),
    (78,  "EXIF Metadata",                "osint/10_exif_metadata.py"),
    (79,  "IP Extractor Advanced",        "osint/11_ip_extractor.py"),
    (80,  "Profile Data Extractor",       "osint/12_profile_data_extractor.py"),
    (81,  "Data Breach Finder",           "osint/13_data_breach_finder.py"),
    (82,  "Geo Tracker Advanced",         "osint/14_geo_tracker.py"),
    (83,  "Email to Phone",               "osint/15_email_to_phone.py"),
    (84,  "Social Doxing Framework",      "osint/16_social_doxing_framework.py"),
    (85,  "Phone OSINT",                  "osint/17_phone_osint.py"),
    (86,  "Username Enumeration",         "osint/18_username_enum.py"),
    (87,  "Address Geolocator",           "osint/19_address_geolocator.py"),
    (88,  "Reverse Image Search",         "osint/20_reverse_image_search.py"),
    (89,  "WHOIS Deep Recon",             "osint/21_whois_deep_recon.py"),
    (90,  "Password Breach Check",        "osint/22_password_breach_check.py"),
    (91,  "WiFi Network Scanner",         "osint/23_wifi_scanner.py"),
    (92,  "IP Intelligence",              "osint/24_ip_intelligence.py"),
    (93,  "Social Engineering Toolkit",   "osint/25_social_engineering.py"),
    (94,  "Archive Recon",                "osint/26_archive_recon.py"),
    (95,  "Correlation Engine",           "osint/27_correlation_engine.py"),
    (96,  "Vehicle Lookup",               "osint/28_vehicle_lookup.py"),
    (97,  "Deep Web Search",              "osint/29_deepweb_search.py"),
    (98,  "Full Doxing Toolkit",          "osint/30_full_doxing_toolkit.py"),
    (99,  "MAC Address Lookup",           "osint/31_mac_address_lookup.py"),
    (100, "Email Hunter",                 "osint/32_email_hunter.py"),
    (101, "Social Media Link Finder",     "osint/33_social_media_link_finder.py"),
    (102, "GitHub OSINT",                 "osint/34_github_osint.py"),
    (103, "LinkedIn Scraper",             "osint/35_linkedin_scraper.py"),
    (104, "CCTV Locator",                 "osint/36_cctv_locator.py"),
    (105, "Pastebin Monitor",             "osint/37_pastebin_monitor.py"),
    (106, "Dark Web Search",              "osint/38_tor_dorker.py"),
    (107, "Document Leak Finder",         "osint/39_document_leak_finder.py"),
    (108, "Ultimate Doxing Framework",    "osint/40_ultimate_doxer.py"),
    (109, "Domain Crawler",               "osint/41_domain_crawler.py"),
    (110, "Credential Stuffing Checker",  "osint/42_credential_stuffing_checker.py"),
    (111, "IP History",                   "osint/43_ip_history.py"),
    (112, "OSINT Framework",              "osint/44_osint_framework.py"),
    (113, "Car Plate Lookup",             "osint/45_car_plate_lookup.py"),
    (114, "Flight Tracker",               "osint/46_flight_tracker.py"),
    (115, "Crypto Wallet Tracker",        "osint/47_crypto_wallet_tracker.py"),
    (116, "WiFi BSSID Tracker",           "osint/48_wifi_bssid_tracker.py"),
    (117, "Business Intelligence",        "osint/49_business_intel.py"),
    (118, "Mega OSINT Suite",             "osint/50_mega_osint_suite.py"),
]

TOTAL = len(ALL_TOOLS)
TOOL_MAP = {t[0]: (t[1], t[2]) for t in ALL_TOOLS}

# ═══════════════════════════════════════════════════════════════════
# STATUS CHECKS
# ═══════════════════════════════════════════════════════════════════
def check_tool_status(num, name, path):
    """Check if tool file exists and is executable"""
    full_path = os.path.join(TOOL_BASE, path)
    if os.path.isfile(full_path):
        return f"{G}[+]{RS}"  # Green = OK
    else:
        return f"{R}[X]{RS}"  # Red = Missing

# ═══════════════════════════════════════════════════════════════════
# CLEAR SCREEN
# ═══════════════════════════════════════════════════════════════════
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# ═══════════════════════════════════════════════════════════════════
# LOADING ANIMATION
# ═══════════════════════════════════════════════════════════════════
def loading_animation():
    """Show loading bar animation"""
    print()
    bar_len = 30
    for i in range(bar_len + 1):
        filled = int(i / bar_len * bar_len)
        bar = f"{G}{'█' * filled}{R}{'░' * (bar_len - filled)}{RS}"
        pct = int(i / bar_len * 100)
        sys.stdout.write(f"\r  {C}[*]{RS} Loading Hell Society Toolkit... {bar} {G}{pct}%{RS}")
        sys.stdout.flush()
        time.sleep(0.03)
    print()
    print(f"  {G}[*] Loaded {BW}{TOTAL}{RS}{G} tools successfully!{RS}")
    print()

# ═══════════════════════════════════════════════════════════════════
# MAIN MENU DISPLAY
# ═══════════════════════════════════════════════════════════════════
def show_menu():
    clear()
    
    # Banner
    print(BRB)
    print()
    
    # Android icon + Info
    print(ANDROID_ICON)
    print()
    print(f"  {BC}• WELCOME TO MY TOOLS!  {R}#ERROR#{RS}")
    print()
    
    # Tools Installer Info
    print(f"  {G}[+] {BW}TOOLS INSTALLER{RS}")
    print(f"  {C}    {BY}Author{RS}: {W}{Style.BRIGHT}@hellsociety{RS}")
    print(f"  {C}    {BY}Telegram{RS}: {W}t.me/termuxhacking{RS}")
    print(f"  {C}    {BY}Github{RS}: {W}hellsociety/hs-tools{RS}")
    print()
    
    # Subscribe bar
    print(f"  {G}●●●●●●{RS}")
    print(f"  {BW}Subscribe !!  {G}HACKING CYBER ARMY{RS}")
    print(f"  {C}[ Version: {VERSION}  ]{RS}")
    print()
    print(f"  {Y}████████████████████████████████████████████{RS}")
    print()
    
    # Status header
    print(f"  {BW}{Style.BRIGHT}  MENU TOOLS{RS}         {G}[+]{RS}    {Y}[~]{RS}    {R}[X]{RS}    {BW}{Style.BRIGHT}STATUS{RS}")
    print(f"  {'  ' + '─' * 48}")
    print()
    
    # Tools list - 2 columns
    tools_per_page = 20
    page = 0
    total_pages = (TOTAL + tools_per_page - 1) // tools_per_page
    
    for page in range(total_pages):
        start = page * tools_per_page
        end = min(start + tools_per_page, TOTAL)
        
        for idx in range(start, end):
            num, name, path = ALL_TOOLS[idx]
            status = check_tool_status(num, name, path)
            
            # Color by category
            if num <= 38:
                cat_color = R  # Red = offensive
            elif num <= 68:
                cat_color = G  # Green = defensive
            else:
                cat_color = C  # Cyan = OSINT
            
            print(f"  {Y}[{num:03d}]. {cat_color}{Style.BRIGHT}{name:<35s}{RS}  {status}")
        
        if page < total_pages - 1:
            print()
            ch = input(f"\n  {G}[+] {BW}Press ENTER for more tools...{RS}")
            if ch == "q" or ch == "Q":
                return

# ═══════════════════════════════════════════════════════════════════
# RUN TOOL - DIRECT EXECUTION WITH os.execvp
# ═══════════════════════════════════════════════════════════════════
def run_tool(num, name, path):
    """Launch tool directly using os.execvp for full interactive support"""
    clear()
    
    full_path = os.path.join(TOOL_BASE, path)
    
    if not os.path.isfile(full_path):
        print(f"  {R}[X] Tool file not found: {path}{RS}")
        print(f"  {Y}[~] Try: python3 {full_path}{RS}")
        print()
        input(f"  {C}[*] Press ENTER to return to menu...{RS}")
        return
    
    # Show tool banner
    print(BRB)
    print()
    print(f"  {G}[+] {BW}WELCOME TO MY TOOLS!  {R}#ERROR#{RS}")
    print()
    print(f"  {Y}████████████████████████████████████████████{RS}")
    print()
    
    # Tool header
    print(f"  {R}[+] {BW}RUNNING TOOL #{num:03d}{RS}")
    print(f"  {BW}  Name: {Y}{name}{RS}")
    print(f"  {BW}  Path: {C}{path}{RS}")
    print()
    print(f"  {Y}[*] Starting tool now...{RS}")
    print(f"  {Y}[*] After tool finishes, you'll be asked to continue.{RS}")
    print()
    print(f"  {G}╔══════════════════════════════════════════════════╗{RS}")
    print(f"  {G}║  TOOL IS RUNNING - Use it normally              ║{RS}")
    print(f"  {G}║  When done, come back here                       ║{RS}")
    print(f"  {G}╚══════════════════════════════════════════════════╝{RS}")
    print()
    
    try:
        # Use os.execvp to replace current process with the tool
        # This gives FULL interactive support (input, output, etc.)
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        os.execvp(sys.executable, [sys.executable, full_path])
    except SystemExit:
        pass
    except Exception as e:
        print(f"  {R}[X] Error: {e}{RS}")
        print(f"  {Y}[~] Try running manually: python3 {full_path}{RS}")
        input(f"  {C}[*] Press ENTER to return...{RS}")

# ═══════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════
def main():
    # Loading animation
    loading_animation()
    time.sleep(1)
    
    while True:
        show_menu()
        
        print()
        print(f"  {BW}{Style.BRIGHT}  Select tool number or EXIT to quit{RS}")
        print()
        
        try:
            choice = input(f"  {G}[+] {RS}root@hellsociety{C}~{RS}# ").strip().upper()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {R}[*] Goodbye from Hell Society...{RS}")
            sys.exit(0)
        
        if choice == "EXIT" or choice == "0" or choice == "000" or choice == "Q":
            print()
            print(f"  {R}╔═══════════════════════════════════════════════════════════╗{RS}")
            print(f"  {R}║  {BW}HACKING TOOL - HELL SOCIETY{RS}                      {RS}{R}║{RS}")
            print(f"  {R}║  {BW}Stay dangerous. Stay anonymous.{RS}                    {RS}{R}║{RS}")
            print(f"  {R}╚═══════════════════════════════════════════════════════════╝{RS}")
            print()
            sys.exit(0)
        
        if choice == "UPDATE" or choice == "U":
            print(f"  {Y}[*] Updating from GitHub...{RS}")
            os.system("cd " + TOOL_BASE + " && git pull")
            input(f"  {C}[*] Press ENTER to continue...{RS}")
            continue
        
        # Parse number
        try:
            num = int(choice)
        except ValueError:
            print(f"  {R}[X] Invalid input. Enter a number 1-{TOTAL}{RS}")
            time.sleep(1.5)
            continue
        
        if num < 1 or num > TOTAL:
            print(f"  {R}[X] Invalid number. Enter 1-{TOTAL}{RS}")
            time.sleep(1.5)
            continue
        
        # Get tool info
        if num in TOOL_MAP:
            name, path = TOOL_MAP[num]
            run_tool(num, name, path)
        else:
            print(f"  {R}[X] Tool not found{RS}")
            time.sleep(1)

if __name__ == "__main__":
    main()
