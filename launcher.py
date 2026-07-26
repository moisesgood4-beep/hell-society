#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HACKING TOOL - HELL SOCIETY v3                                ║
# ║  Created by: HELL SOCIETY Community                              ║
# ║  Flow: Select tool -> Use it -> 1=Again 2=Menu                 ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import sys
import subprocess
import time

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
BW = Style.BRIGHT + Fore.WHITE; BM = Style.BRIGHT + (getattr(Fore, 'MAGENTA', '\033[35m'))
RS = Style.RESET_ALL

TOOL_BASE = os.path.dirname(os.path.abspath(__file__))

# ═══════════════════════════════════════════════════════════════════
# BANNER BRAILLE
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
# ALL 114 TOOLS - Numbered 1 to 114
# ═══════════════════════════════════════════════════════════════════
ALL_TOOLS = [
    # ── OFFENSIVE 1-34 ──
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
    (38,  "Advanced Tools (Keylogger/Injector)", "offensive/36_advanced_tools.py"),
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
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear()
    print(BRB)
    print()
    print(f"  {BW}{Style.BRIGHT}  HACKING TOOL{RS}")
    print(f"  {BR}{Style.BRIGHT}  HELL SOCIETY{RS}")
    print()
    print(f"  {W}{Back.RED} :: Disclaimer: Developers assume no liability and are not  :: {RS}")
    print(f"  {W}{Back.RED} :: responsible for any misuse or damage caused.           :: {RS}")
    print(f"  {W}{Back.RED} :: Only use for educational purposes!!                     :: {RS}")
    print()
    print(f"  {W}{Back.RED} :: Attacking targets without mutual consent is illegal!!   :: {RS}")
    print()
    # Stats
    print(f"  {BC}┌──────────────────────────────────────────────────┐")
    print(f"  {BC}│  {BW}TOTAL: {BR}{TOTAL}{BW} | OFF: {BR}34{BW} | DEF: {BR}30{BW} | OSINT: {BR}50{BW}    {BC}│{RS}")
    print(f"  {BC}└──────────────────────────────────────────────────┘")
    print()

def print_offensive_list():
    print(f"  {R}{Style.BRIGHT}[ OFFENSIVE TOOLS ]{RS}")
    print(f"  {'─' * 72}")
    for i in range(0, 34, 3):
        line = "  "
        for j in range(3):
            idx = i + j
            if idx < 34:
                num = ALL_TOOLS[idx][0]
                name = ALL_TOOLS[idx][1][:20]
                num_s = f"{num:03d}"
                line += f"{Y}[{num_s}] {R}{name}{RS}"
                if j < 2:
                    line += "   "
        print(line)
    print()

def print_defensive_list():
    print(f"  {G}{Style.BRIGHT}[ DEFENSIVE TOOLS ]{RS}")
    print(f"  {'─' * 72}")
    for i in range(34, 64, 3):
        line = "  "
        for j in range(3):
            idx = i + j
            if idx < 64:
                num = ALL_TOOLS[idx][0]
                name = ALL_TOOLS[idx][1][:20]
                num_s = f"{num:03d}"
                line += f"{Y}[{num_s}] {G}{name}{RS}"
                if j < 2:
                    line += "   "
        print(line)
    print()

def print_osint_list():
    print(f"  {C}{Style.BRIGHT}[ OSINT & DOXING TOOLS ]{RS}")
    print(f"  {'─' * 72}")
    for i in range(64, TOTAL, 3):
        line = "  "
        for j in range(3):
            idx = i + j
            if idx < TOTAL:
                num = ALL_TOOLS[idx][0]
                name = ALL_TOOLS[idx][1][:20]
                num_s = f"{num:03d}"
                line += f"{Y}[{num_s}] {C}{name}{RS}"
                if j < 2:
                    line += "   "
        print(line)
    print()

def print_main_menu():
    print_banner()
    print_offensive_list()
    print_defensive_list()
    print_osint_list()
    print(f"  {Y}[{Style.BRIGHT}000{RS}{Y}] {BR}EXIT / QUIT{RS}")
    print()
    print(f"  {BC}{'═' * 72}{RS}")
    print(f"  {BW}{Style.BRIGHT}  Enter tool number (001-{TOTAL:03d}) or 000 to exit{RS}")
    print()

# ═══════════════════════════════════════════════════════════════════
# LAUNCH TOOL
# ═══════════════════════════════════════════════════════════════════
def run_tool(num, name, path):
    """Launch tool and handle 1=repeat 2=menu"""
    while True:
        clear()
        # Mini banner
        print(BRB)
        print()
        print(f"  {BW}{Style.BRIGHT}  HACKING TOOL{RS}")
        print(f"  {BR}{Style.BRIGHT}  HELL SOCIETY{RS}")
        print()

        # Tool header
        print(f"  {Y}{Style.BRIGHT}╔═══════════════════════════════════════════════════════╗{RS}")
        print(f"  {Y}{Style.BRIGHT}║  TOOL #{num:03d} - {name:<36s} {RS}{Y}{Style.BRIGHT}║{RS}")
        print(f"  {Y}{Style.BRIGHT}╚═══════════════════════════════════════════════════════╝{RS}")
        print()
        print(f"  {C}[*] Starting tool...{RS}")
        print(f"  {C}[*] Follow the instructions of the tool.{RS}")
        print()

        # Full path
        full_path = os.path.join(TOOL_BASE, path)

        if not os.path.isfile(full_path):
            print(f"  {R}[!] Tool file not found: {path}{RS}")
            print(f"  {Y}[i] Run manually: python3 {full_path}{RS}")
            print()
            print(f"  {Y}[1] {BW}Use this tool again{RS}")
            print(f"  {Y}[2] {BW}Return to main menu{RS}")
            print()
            ch = input(f"  {G}root@hellsociety{RS}:{C}~{RS}# ").strip()
            if ch == "1":
                continue
            else:
                return

        try:
            # Run the tool
            subprocess.run([sys.executable, full_path], cwd=TOOL_BASE)
        except KeyboardInterrupt:
            print(f"\n  {Y}[!] Tool interrupted by user{RS}")
        except Exception as e:
            print(f"\n  {R}[!] Error running tool: {e}{RS}")

        # After tool finishes -> options
        print()
        print(f"  {BC}{'═' * 72}{RS}")
        print()
        print(f"  {BW}{Style.BRIGHT}  Tool execution completed.{RS}")
        print()
        print(f"  {G}[1] {BW}{Style.BRIGHT}Use this tool again{RS}")
        print(f"  {Y}[2] {BW}{Style.BRIGHT}Return to main menu{RS}")
        print(f"  {R}[0] {BW}{Style.BRIGHT}Exit{RS}")
        print()

        ch = input(f"  {G}root@hellsociety{RS}:{C}~{RS}# ").strip()

        if ch == "1":
            continue       # Re-use same tool
        elif ch == "0":
            sys.exit(0)
        else:
            return         # Back to main menu (2 or anything else)

# ═══════════════════════════════════════════════════════════════════
# MAIN LOOP
# ═══════════════════════════════════════════════════════════════════
def main():
    while True:
        print_main_menu()

        try:
            choice = input(f"  {G}root@hellsociety{RS}:{C}~{RS}# ").strip()
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Y}[!] Goodbye from Hell Society...{RS}")
            sys.exit(0)

        if choice == "0" or choice == "000":
            print()
            print(f"  {BR}╔══════════════════════════════════════════════════════════════════╗{RS}")
            print(f"  {BR}║  {BW}HACKING TOOL - HELL SOCIETY{RS}                             {RS}{BR}║{RS}")
            print(f"  {BR}║  {BW}Stay dangerous. Stay anonymous.{RS}                          {RS}{BR}║{RS}")
            print(f"  {BR}╚══════════════════════════════════════════════════════════════════╝{RS}")
            print()
            sys.exit(0)

        # Parse number
        try:
            num = int(choice)
        except ValueError:
            print(f"  {R}[!] Invalid input. Enter a number 1-{TOTAL}{RS}")
            time.sleep(1.5)
            continue

        if num < 1 or num > TOTAL:
            print(f"  {R}[!] Invalid number. Enter 1-{TOTAL}{RS}")
            time.sleep(1.5)
            continue

        # Get tool info
        if num in TOOL_MAP:
            name, path = TOOL_MAP[num]
            run_tool(num, name, path)
        else:
            print(f"  {R}[!] Tool not found.{RS}")
            time.sleep(1)

if __name__ == "__main__":
    main()
