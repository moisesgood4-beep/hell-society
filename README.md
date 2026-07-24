# Hell Society Cyber Toolkit v2.0

```
╔══════════════════════════════════════════════════════════════════╗
║   ██╗  ██╗ ██████╗ ███╗   ███╗███████╗                           ║
║   ██║  ██║██╔═══██╗████╗ ████║██╔════╝                           ║
║   ███████║██║   ██║██╔████╔██║███████╗                           ║
║   ██╔══██║██║   ██║██║╚██╔╝██║╚════██║                           ║
║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████║                           ║
║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝                           ║
╠══════════════════════════════════════════════════════════════════╣
║        77 Profesional Security Tools for Pentesting              ║
║        Compatible: Linux (Debian/Ubuntu/Kali) + Termux           ║
║                  Created by: HELL SOCIETY                        ║
╚══════════════════════════════════════════════════════════════════╝
```

---

## ADVERTENCIA LEGAL

> Este toolkit fue desarrollado por la comunidad **Hell Society** exclusivamente para fines de **pentesting ético**, investigación de seguridad y educación. Los autores **no se hacen responsables** del mal uso de estas herramientas. El uso no autorizado de herramientas de seguridad contra sistemas, redes o datos sin consentimiento explícito del propietario es **ilegal** en la mayoría de jurisdicciones.

---

## Contenido

| Categoría | Cantidad | Directorio |
|-----------|----------|------------|
| Ofensivos (Pentesting Web/Apps) | 33 | `/offensive/` |
| Defensivos (Protección/Detección) | 30 | `/defensive/` |
| OSINT & Doxing | 14 | `/osint/` |
| **Total** | **77** | |

---

## Instalación

### Linux (Debian/Ubuntu/Kali)

```bash
# Clonar o extraer el toolkit
cd cybertoolkit/

# Instalar todo
chmod +x install.sh && ./install.sh

# O manualmente:
sudo apt-get update && sudo apt-get install -y python3 python3-pip git nmap whois dnsutils
sudo pip3 install colorama requests beautifulsoup4 pillow pycryptodome scapy python-whois dnspython paramiko
sudo apt-get install -y hydra sqlmap tcpdump sslscan

# Ejecutar
python3 launcher.py
# O rápido:
./run.sh
```

### Termux (Android)

```bash
# Clonar o extraer el toolkit
cd cybertoolkit/

# Instalar todo automáticamente
chmod +x termux_setup.sh && bash termux_setup.sh

# O paso a paso:
pkg update -y
pkg install -y python python-pip git nmap whois dnsutils termux-api
pip install colorama requests beautifulsoup4 pillow pycryptodome scapy dnspython paramiko
pkg install -y hydra sqlmap tcpdump openssl

# Ejecutar
python3 launcher.py
# O rápido:
./run.sh
# O desde cualquier directorio:
~/hell-society/run
```

---

## Scripts Ofensivos (Pentesting Web & Aplicaciones)

| # | Herramienta | Descripción |
|---|-------------|-------------|
| 01 | SQL Injection Scanner | Escaneo y detección de SQLi en formularios web |
| 02 | XSS Scanner | Detección de Cross-Site Scripting (Reflected, Stored, DOM) |
| 03 | Directory Fuzzer | Fuzzing de directorios y archivos web |
| 04 | Subdomain Enumeration | Enumeración de subdominios |
| 05 | Port Scanner | Escaneo de puertos TCP/UDP |
| 06 | Hash Cracker | Cracking de hashes (MD5, SHA, NTLM, etc.) |
| 07 | HTTP Header Analyzer | Análisis de headers HTTP para vulnerabilidades |
| 08 | Web Crawler | Spider web para mapeo de aplicaciones |
| 09 | SSL/TLS Analyzer | Análisis de configuración SSL/TLS |
| 10 | CMS Scanner | Escaneo de vulnerabilidades en WordPress, Joomla, Drupal |
| 11 | API Scanner | Escaneo de seguridad de APIs REST |
| 12 | Phishing Framework | Framework de phishing autorizado |
| 13 | Reverse Shell Generator | Generador de reverse shells multiplataforma |
| 14 | LFI/RFI Scanner | Escaneo de Local/Remote File Inclusion |
| 15 | CSRF Scanner | Detección de Cross-Site Request Forgery |
| 16 | IDOR Scanner | Escaneo de Insecure Direct Object References |
| 17 | SSRF Scanner | Detección de Server-Side Request Forgery |
| 18 | Command Injection | Detección de inyección de comandos OS |
| 19 | Web Vuln Scanner | Escáner multi-vulnerabilidad web |
| 20 | Password Brute Force | Fuerza bruta de contraseñas multi-protocolo |
| 21 | Wireless Sniffer | Captura y análisis de tráfico WiFi |
| 22 | JWT Attacker | Ataque a tokens JWT (none, weak secret) |
| 23 | XXE Scanner | Detección de XML External Entity injection |
| 24 | SSTI Scanner | Detección de Server-Side Template Injection |
| 25 | Dorker | Motor de Google Dorking automatizado |
| 26 | WebSocket Interceptor | Interceptación y manipulación de WebSocket |
| 27 | GraphQL Explorer | Exploración y ataque a endpoints GraphQL |
| 28 | API Fuzzer | Fuzzing de parámetros y endpoints API |
| 29 | Session Hijacker | Robo y manipulación de sesiones web |
| 30 | Email Spoofer | Análisis y spoofing de headers de email |
| 31 | Web Defacement Tester | Test de vulnerabilidades de defacement |
| 32 | Database Extractor | Extracción de DB vía SQL Injection |
| 33 | Database Dumper | Volcado completo de bases de datos |

---

## Scripts Defensivos (Protección & Detección)

| # | Herramienta | Descripción |
|---|-------------|-------------|
| 01 | System Hardening | Hardening de sistema Linux |
| 02 | Log Analyzer | Análisis de logs para amenazas |
| 03 | Network Monitor | Monitorización de red en tiempo real |
| 04 | Vulnerability Scanner | Escaneo de vulnerabilidades del sistema |
| 05 | IDS/IPS Detector | Sistema de detección/prevención de intrusiones |
| 06 | Malware Scanner | Escaneo de malware y firmas conocidas |
| 07 | WAF Configurator | Configuración de Web Application Firewall |
| 08 | Certificate Monitor | Monitorización de certificados SSL |
| 09 | Brute Force Detector | Detección de ataques de fuerza bruta |
| 10 | Traffic Analyzer | Análisis de tráfico de red |
| 11 | File Integrity Checker | Verificación de integridad de archivos |
| 12 | Firewall Analyzer | Análisis de reglas de firewall |
| 13 | Password Policy Checker | Verificación de políticas de contraseñas |
| 14 | Docker Security | Auditoría de seguridad de contenedores Docker |
| 15 | Web App Security Scanner | Escaneo de seguridad de aplicaciones web |
| 16 | Incident Responder | Herramienta de respuesta a incidentes |
| 17 | Backup Validator | Validación de backups y recuperación |
| 18 | Encryption Tool | Herramientas de cifrado/descifrado |
| 19 | Honeypot | Despliegue de honeypots para detección |
| 20 | Ransomware Detector | Detección de comportamiento ransomware |
| 21 | API Security Checker | Auditoría de seguridad de APIs |
| 22 | CVE Checker | Verificación de CVEs conocidos en el sistema |
| 23 | Network Segmentation | Análisis de segmentación de red |
| 24 | Zero-Day Detector | Detección de indicadores de zero-days |
| 25 | Privilege Escalation Detector | Detección de vectores de escalada de privilegios |
| 26 | DLP Scanner | Prevención de pérdida de datos |
| 27 | Email Header Analyzer | Análisis de headers de email contra spoofing |
| 28 | SSL Pinning Checker | Verificación de configuración SSL |
| 29 | Threat Intel Feed | Integración con feeds de inteligencia de amenazas |
| 30 | Audit Compliance | Auditoría de cumplimiento de seguridad |

---

## Scripts OSINT & Doxing

| # | Herramienta | Descripción |
|---|-------------|-------------|
| 01 | Email OSINT | Reconocimiento de emails (breaches, Gravatar, social) |
| 02 | Username Recon | Búsqueda de username en 20+ plataformas |
| 03 | IP Geolocation | Geolocalización y recon de IPs |
| 04 | Domain Recon | Inteligencia de dominios (DNS, WHOIS, tech stack) |
| 05 | Phone Recon | Reconocimiento de números telefónicos |
| 06 | Social Media Scraper | Extracción de datos de redes sociales |
| 07 | Web Archive Recon | Investigación en Wayback Machine |
| 08 | Dork Engine | Generador de Google Dorks automatizado |
| 09 | People Search | Búsqueda de personas y datos asociados |
| 10 | EXIF Metadata | Extracción de metadata EXIF de imágenes |
| 11 | IP Extractor Advanced | Extracción de IP por 10 métodos diferentes |
| 12 | Profile Data Extractor | Extracción masiva de datos de perfiles |
| 13 | Data Breach Finder | Búsqueda de datos en leaks/breaches |
| 14 | Geo Tracker Advanced | Geolocalización avanzada y traceroute |

---

## Uso de Ejemplos

```bash
# ===== LINUX =====
# Ofensivo - SQL Injection Scanner
python3 offensive/01_sql_injection_scanner.py -u http://target.com/login.php -l passwords.txt

# Ofensivo - Database Extractor
python3 offensive/32_database_extractor.py -u http://target.com/page.php -p id

# Ofensivo - Database Dumper
python3 offensive/33_database_dumper.py -u http://target.com -m all

# Defensivo - Log Analyzer
python3 defensive/02_log_analyzer.py -l /var/log/auth.log

# OSINT - IP Extractor (10 métodos)
python3 osint/11_ip_extractor.py -t target_username

# OSINT - Profile Extractor
python3 osint/12_profile_data_extractor.py -u target_username

# OSINT - Data Breach Finder
python3 osint/13_data_breach_finder.py -t target@email.com

# ===== TERMUX =====
# Mismos comandos pero sin sudo:
python3 osint/11_ip_extractor.py -t target_username

# Usar run.sh para lanzar cualquier script:
./run.sh osint/14_geo_tracker.py -t 8.8.8.8
```

---

## Menú Principal

```bash
# Linux y Termux
python3 launcher.py
# O
./run.sh
```

---

## Compatibilidad

| Característica | Linux | Termux |
|----------------|-------|--------|
| Python 3 | Nativo | pkg install python |
| colorama | pip install | pip install |
| nmap | apt install | pkg install |
| whois | apt install | pkg install |
| hydra | apt install | pkg install |
| sqlmap | apt install | pip install |
| tcpdump | apt install | pkg install |
| scapy | pip install | pip install |
| sudo | Disponible | No (usa termux-sudo) |
| /tmp/ | Disponible | ~/hell-society/data/ |

---

## Notas Termux

1. **Storage**: Ejecutar `termux-setup-storage` para acceso a archivos del teléfono
2. **Root**: Si necesitas root, usa `tsu` en vez de `sudo`
3. **Red**: Algunas herramientas de red necesitan root (tcpdump, nmap scan)
4. **Python**: Usar siempre `python3` en vez de `python`
5. **Permisos**: Los scripts ya tienen permisos de ejecución configurados

---

## Créditos

**Desarrollado por la comunidad Hell Society**

Todas las herramientas incluyen paneles visuales coloridos con estilo profesional/hacker.

---

## Nota

Este toolkit es una herramienta profesional de seguridad. Úselo de manera responsable y siempre con autorización del propietario del sistema objetivo.
