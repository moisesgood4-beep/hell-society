#!/usr/bin/env python3
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HACKING TOOL - HELL SOCIETY                                    ║
# ║  Created by: HELL SOCIETY Community                              ║
# ║  Professional Pentesting Framework                               ║
# ╚══════════════════════════════════════════════════════════════════╝

import os
import sys
import subprocess
import platform

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
except ImportError:
    os.system("pip3 install colorama 2>/dev/null || pip install colorama 2>/dev/null")
    from colorama import init, Fore, Back, Style
    init(autoreset=True)

# ──────────────────────────────────────────────────────────────────
# COLORS
# ──────────────────────────────────────────────────────────────────
R  = Fore.RED
G  = Fore.GREEN
Y  = Fore.YELLOW
B  = Fore.BLUE
M  = Fore.MAGENTA
C  = Fore.CYAN
W  = Fore.WHITE
BR = Style.BRIGHT + Fore.RED
BG = Style.BRIGHT + Fore.GREEN
BY = Style.BRIGHT + Fore.YELLOW
BB = Style.BRIGHT + Fore.BLUE
BM = Style.BRIGHT + Fore.MAGENTA
BC = Style.BRIGHT + Fore.CYAN
BW = Style.BRIGHT + Fore.WHITE
RS = Style.RESET_ALL

# ──────────────────────────────────────────────────────────────────
# ASCII ART
# ──────────────────────────────────────────────────────────────────
BANNER = f"""{BR}
 ██╗  ██╗ ██████╗ ███╗   ███╗███████╗██████╗  █████╗ ██╗    ██╗███╗   ██╗
 ██║  ██║██╔═══██╗████╗ ████║██╔════╝██╔══██╗██╔══██╗██║    ██║████╗  ██║
 ███████║██║   ██║██╔████╔██║███████╗██████╔╝███████║██║ █╗ ██║██╔██╗ ██║
 ██╔══██║██║   ██║██║╚██╔╝██║╚════██║██╔══██╗██╔══██║██║███╗██║██║╚██╗██║
 ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████║██║  ██║██║  ██║╚███╔███╔╝██║ ╚████║
 ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝{RS}
"""

SUB_BANNER = f"""{BW}
 ██████╗ ██╗   ██╗███████╗██████╗     ██████╗  █████╗ ████████╗ █████╗
 ██╔══██╗██║   ██║██╔════╝██╔══██╗    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗
 ██║  ██║██║   ██║█████╗  ██████╔╝    ██████╔╝███████║   ██║   ███████║
 ██║  ██║╚██╗ ██╔╝██╔══╝  ██╔══██╗    ██╔══██╗██╔══██║   ██║   ██╔══██║
 ██████╔╝ ╚████╔╝ ███████╗██║  ██║    ██████╔╝██║  ██║   ██║   ██║  ██║
 ╚═════╝   ╚═══╝  ╚══════╝╚═╝  ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝{RS}
"""

SKULL = f"""{BR}
           {BR}   .---.   {RS}
          {BR}  /     \\  {RS}
         {BR}  |  O O  | {RS}
         {BR}  |   ▽   | {RS}
          {BR}  \\  --- /{RS}
           {BR}  '---'  {RS}
  {R}H E L L   S O C I E T Y{RS}"""

# ──────────────────────────────────────────────────────────────────
# TOOLS DATABASE
# ──────────────────────────────────────────────────────────────────
OFFENSIVE_TOOLS = [
    ("01", "SQL Injection Scanner",       "offensive/01_sql_injection_scanner.py"),
    ("02", "XSS Scanner",                 "offensive/02_xss_scanner.py"),
    ("03", "Directory Fuzzer",            "offensive/03_directory_fuzzer.py"),
    ("04", "Subdomain Enumeration",       "offensive/04_subdomain_enum.py"),
    ("05", "Port Scanner",                "offensive/05_port_scanner.py"),
    ("06", "Hash Cracker",                "offensive/06_hash_cracker.py"),
    ("07", "HTTP Header Analyzer",        "offensive/07_header_analyzer.py"),
    ("08", "Web Crawler",                 "offensive/08_web_crawler.py"),
    ("09", "SSL/TLS Analyzer",            "offensive/09_ssl_analyzer.py"),
    ("10", "CMS Scanner",                 "offensive/10_cms_scanner.py"),
    ("11", "API Security Scanner",        "offensive/11_api_scanner.py"),
    ("12", "Phishing Framework",          "offensive/12_phishing_framework.py"),
    ("13", "Reverse Shell Generator",     "offensive/13_reverse_shell.py"),
    ("14", "LFI/RFI Scanner",             "offensive/14_lfi_scanner.py"),
    ("15", "CSRF Scanner",                "offensive/15_csrf_scanner.py"),
    ("16", "IDOR Scanner",                "offensive/16_idor_scanner.py"),
    ("17", "SSRF Scanner",                "offensive/17_ssrf_scanner.py"),
    ("18", "Command Injection",           "offensive/18_command_injection.py"),
    ("19", "Web Vuln Scanner",            "offensive/19_web_vuln_scanner.py"),
    ("20", "Password Brute Force",        "offensive/20_password_bruteforce.py"),
    ("21", "Wireless Sniffer",            "offensive/21_wireless_sniffer.py"),
    ("22", "JWT Token Attacker",          "offensive/22_jwt_attacker.py"),
    ("23", "XXE Scanner",                 "offensive/23_xxe_scanner.py"),
    ("24", "SSTI Scanner",                "offensive/24_ssti_scanner.py"),
    ("25", "Dorker",                      "offensive/25_dorker.py"),
    ("26", "WebSocket Interceptor",       "offensive/26_websocket_interceptor.py"),
    ("27", "GraphQL Explorer",            "offensive/27_graphql_explorer.py"),
    ("28", "API Fuzzer",                  "offensive/28_api_fuzzer.py"),
    ("29", "Session Hijacker",            "offensive/29_session_hijacker.py"),
    ("30", "Email Spoofer",               "offensive/30_email_spoofer.py"),
    ("31", "Web Defacement Tester",       "offensive/31_web_defacement_tester.py"),
    ("32", "Database Extractor",          "offensive/32_database_extractor.py"),
    ("33", "Database Dumper",             "offensive/33_database_dumper.py"),
    ("34", "ExitTool (BlackEye Phishing)", "offensive/34_exittool.py"),
]

DEFENSIVE_TOOLS = [
    ("01", "System Hardening",            "defensive/01_system_hardening.py"),
    ("02", "Log Analyzer",                "defensive/02_log_analyzer.py"),
    ("03", "Network Monitor",             "defensive/03_network_monitor.py"),
    ("04", "Vulnerability Scanner",       "defensive/04_vulnerability_scanner.py"),
    ("05", "IDS/IPS Detector",            "defensive/05_ids_ips_detector.py"),
    ("06", "Malware Scanner",             "defensive/06_malware_scanner.py"),
    ("07", "WAF Configurator",            "defensive/07_waf_configurator.py"),
    ("08", "Certificate Monitor",         "defensive/08_certificate_monitor.py"),
    ("09", "Brute Force Detector",        "defensive/09_brute_force_detector.py"),
    ("10", "Traffic Analyzer",            "defensive/10_traffic_analyzer.py"),
    ("11", "File Integrity Checker",      "defensive/11_file_integrity_checker.py"),
    ("12", "Firewall Analyzer",           "defensive/12_firewall_analyzer.py"),
    ("13", "Password Policy Checker",     "defensive/13_password_policy_checker.py"),
    ("14", "Docker Security",             "defensive/14_docker_security.py"),
    ("15", "Web App Security Scanner",    "defensive/15_web_app_scanner.py"),
    ("16", "Incident Responder",          "defensive/16_incident_responder.py"),
    ("17", "Backup Validator",            "defensive/17_backup_validator.py"),
    ("18", "Encryption Tool",             "defensive/18_encryption_tool.py"),
    ("19", "Honeypot",                    "defensive/19_honeypot.py"),
    ("20", "Ransomware Detector",         "defensive/20_ransomware_detector.py"),
    ("21", "API Security Checker",        "defensive/21_api_security_checker.py"),
    ("22", "CVE Checker",                 "defensive/22_cve_checker.py"),
    ("23", "Network Segmentation",        "defensive/23_network_segmentation.py"),
    ("24", "Zero-Day Detector",           "defensive/24_zero_day_detector.py"),
    ("25", "Privilege Escalation Detect", "defensive/25_privilege_escalation_detector.py"),
    ("26", "DLP Scanner",                 "defensive/26_dlp_scanner.py"),
    ("27", "Email Header Analyzer",       "defensive/27_email_header_analyzer.py"),
    ("28", "SSL Pinning Checker",         "defensive/28_ssl_pinning_checker.py"),
    ("29", "Threat Intel Feed",           "defensive/29_threat_intel_feed.py"),
    ("30", "Audit Compliance",            "defensive/30_audit_compliance.py"),
]

OSINT_TOOLS = [
    ("01", "Email OSINT",                 "osint/01_email_osint.py"),
    ("02", "Username Recon",              "osint/02_username_recon.py"),
    ("03", "IP Geolocation",              "osint/03_ip_geolocation.py"),
    ("04", "Domain Recon",                "osint/04_domain_recon.py"),
    ("05", "Phone Recon",                 "osint/05_phone_recon.py"),
    ("06", "Social Media Scraper",        "osint/06_social_media_scraper.py"),
    ("07", "Web Archive Recon",           "osint/07_web_archive_recon.py"),
    ("08", "Dork Engine",                 "osint/08_dork_engine.py"),
    ("09", "People Search",               "osint/09_people_search.py"),
    ("10", "EXIF Metadata",               "osint/10_exif_metadata.py"),
    ("11", "IP Extractor Advanced",       "osint/11_ip_extractor.py"),
    ("12", "Profile Data Extractor",      "osint/12_profile_data_extractor.py"),
    ("13", "Data Breach Finder",          "osint/13_data_breach_finder.py"),
    ("14", "Geo Tracker Advanced",        "osint/14_geo_tracker.py"),
    ("15", "Email to Phone",              "osint/15_email_to_phone.py"),
    ("16", "Social Doxing Framework",     "osint/16_social_doxing_framework.py"),
    ("17", "Phone OSINT",                 "osint/17_phone_osint.py"),
    ("18", "Username Enumeration",        "osint/18_username_enum.py"),
    ("19", "Address Geolocator",          "osint/19_address_geolocator.py"),
    ("20", "Reverse Image Search",        "osint/20_reverse_image_search.py"),
    ("21", "WHOIS Deep Recon",            "osint/21_whois_deep_recon.py"),
    ("22", "Password Breach Check",       "osint/22_password_breach_check.py"),
    ("23", "WiFi Network Scanner",        "osint/23_wifi_scanner.py"),
    ("24", "IP Intelligence",             "osint/24_ip_intelligence.py"),
    ("25", "Social Engineering Toolkit",  "osint/25_social_engineering.py"),
    ("26", "Archive Recon",               "osint/26_archive_recon.py"),
    ("27", "Correlation Engine",          "osint/27_correlation_engine.py"),
    ("28", "Vehicle Lookup",              "osint/28_vehicle_lookup.py"),
    ("29", "Deep Web Search",             "osint/29_deepweb_search.py"),
    ("30", "Full Doxing Toolkit",         "osint/30_full_doxing_toolkit.py"),
]

ALL_TOOLS = OFFENSIVE_TOOLS + DEFENSIVE_TOOLS + OSINT_TOOLS

TOOL_LOOKUP = {}
for num, name, path in ALL_TOOLS:
    TOOL_LOOKUP[num] = (name, path)

# ──────────────────────────────────────────────────────────────────
# DISPLAY FUNCTIONS
# ──────────────────────────────────────────────────────────────────
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(BANNER)
    print(SUB_BANNER)
    print(f"  {R}╔══════════════════════════════════════════════════════════════════╗{RS}")
    print(f"  {R}║ :: {BW}{BR}Disclaimer: Developers assume no liability and are not    {RS}{R} ::{RS}")
    print(f"  {R}║ :: {BW}{BR}responsible for any misuse or damage caused.            {RS}{R} ::{RS}")
    print(f"  {R}║ :: {BW}{BR}Only use for educational purposes!!                     {RS}{R} ::{RS}")
    print(f"  {R}║ ::                                                                  {RS}")
    print(f"  {R}║ :: {BG}Attacking targets without mutual consent is illegal!!{RS} {R} ::{RS}")
    print(f"  {R}╚══════════════════════════════════════════════════════════════════╝{RS}")
    print()

def print_tools_in_columns(tools, category_color, category_name, columns=3):
    print(f"  {category_color}[ {BW}{BR}{category_name}{RS} {category_color}]{RS}")
    print(f"  {'─' * 58}")

    rows = (len(tools) + columns - 1) // columns

    for row in range(rows):
        line = "  "
        for col in range(columns):
            idx = row + col * rows
            if idx < len(tools):
                num, name, _ = tools[idx]
                n = int(num)
                if n <= 10:
                    num_color = BR
                elif n <= 20:
                    num_color = BY
                elif n <= 30:
                    num_color = BG
                else:
                    num_color = BM
                line += f"{num_color}[{num}] {BW}{name}{RS}"
                if col < columns - 1:
                    line += "   "
        print(line)
    print()

def print_skull():
    print(f"  {SKULL}")
    print()

def print_stats():
    off = len(OFFENSIVE_TOOLS)
    defn = len(DEFENSIVE_TOOLS)
    osin = len(OSINT_TOOLS)
    total = off + defn + osin
    print(f"  {BG}┌─────────────────────────────────────────────────────┐{RS}")
    print(f"  {BG}│  {BW}TOTAL TOOLS: {BR}{total}{BW}  |  OFF: {BR}{off}{BW}  |  DEF: {BR}{defn}{BW}  |  OSINT: {BR}{osin}{BW}    {BG}│{RS}")
    print(f"  {BG}└─────────────────────────────────────────────────────┘{RS}")
    print()

def print_system_info():
    pyver = platform.python_version()
    ostype = platform.system()
    arch = platform.machine()
    termux = "TERMUX" if ("Android" in ostype or os.environ.get("PREFIX", "").startswith("/data/data/com.termux")) else "LINUX"
    print(f"  {BC}┌──────────────────────────────────────────────────────────┐{RS}")
    print(f"  {BC}│  {BW}OS: {BY}{termux} {BW}| Python: {BG}{pyver} {BW}| Arch: {BC}{arch}{BC}{' ' * max(0, 50 - len(str(arch)) - 25)}│{RS}")
    print(f"  {BC}└──────────────────────────────────────────────────────────┘{RS}")
    print()

def print_menu():
    print_banner()
    print_skull()
    print_stats()
    print_system_info()

    print_tools_in_columns(OFFENSIVE_TOOLS, R, "OFFENSIVE TOOLS", columns=3)
    print_tools_in_columns(DEFENSIVE_TOOLS, C, "DEFENSIVE TOOLS", columns=3)
    print_tools_in_columns(OSINT_TOOLS, G, "OSINT & DOXING TOOLS", columns=3)

    print(f"  {M}[98] {BW}{BM}Check Dependencies{RS}")
    print(f"  {M}[99] {BW}{BM}Exit{RS}")
    print()

    print(f"  {BR}┌──────────────────────────────────────────────────────────┐{RS}")
    print(f"  {BR}│  {BW}[{BY}!{BW}] {BR}Choose an option:{RS}                                   {BR}│{RS}")
    print(f"  {BR}└──────────────────────────────────────────────────────────┘{RS}")
    print()

def launch_tool(tool_path, tool_name=""):
    toolkit_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(toolkit_dir, tool_path)

    print()
    print(f"  {BG}[*] Launching: {BW}{tool_name}{RS}")
    print(f"  {BC}[*] Path: {full_path}{RS}")
    print(f"  {Y}[*] {'─' * 40}")
    print()

    if not os.path.isfile(full_path):
        print(f"  {R}[!] Tool file not found: {tool_path}")
        print(f"  {Y}[i] Run: python3 {full_path}")
        input(f"\n  {Y}[i] Press Enter to return...")
        return

    try:
        subprocess.run([sys.executable, full_path])
    except KeyboardInterrupt:
        print(f"\n  {Y}[!] Tool interrupted")
    except Exception as e:
        print(f"  {R}[!] Error: {e}")

    print()
    input(f"  {Y}[i] Press Enter to return to menu...")

# ──────────────────────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────────────────────
def main():
    while True:
        print_menu()

        try:
            choice = input(f"  {BG}root{RS}@{BR}hellsociety{RS}:{BG}~{RS}$ {BW}")
        except (EOFError, KeyboardInterrupt):
            print(f"\n  {Y}[!] Goodbye!")
            break

        choice = choice.strip()

        if choice == "99" or choice.lower() in ("exit", "quit"):
            print()
            print(f"  {BR}╔══════════════════════════════════════════════════════════════════╗{RS}")
            print(f"  {BR}║  {BW}HACKING TOOL - HELL SOCIETY{RS}                             {RS}{BR}║{RS}")
            print(f"  {BR}║  {BW}Stay dangerous. Stay anonymous.{RS}                          {RS}{BR}║{RS}")
            print(f"  {BR}╚══════════════════════════════════════════════════════════════════╝{RS}")
            print()
            break

        elif choice == "98":
            print()
            print(f"  {BG}[*] Checking dependencies...{RS}")
            deps = ["colorama", "requests", "beautifulsoup4", "pillow", "dnspython", "paramiko"]
            for dep in deps:
                try:
                    __import__(dep)
                    print(f"  {BG}[+]{RS} {BW}{dep}{RS}")
                except ImportError:
                    print(f"  {R}[-]{RS} {BW}{dep}{RS} {Y}- missing{RS}")
            print()
            print(f"  {BG}[*] Install missing: pip3 install colorama requests beautifulsoup4 pillow dnspython paramiko")
            input(f"\n  {Y}[i] Press Enter to return...")
            continue

        elif choice in TOOL_LOOKUP:
            name, path = TOOL_LOOKUP[choice]
            launch_tool(path, name)
        else:
            print(f"  {R}[!] Invalid option: {choice}")
            print(f"  {Y}[i] Enter: 01-34 (offensive) | 01-30 (defensive) | 01-30 (osint)")
            input(f"  {Y}[i] Press Enter to continue...")

if __name__ == "__main__":
    main()
