#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  HELL SOCIETY - Termux Setup Script
#  Compatible with Android / Termux (aarch64, arm, x86_64)
#  Created by: HELL SOCIETY Community
# ============================================================

clear

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║${BOLD}  HELL SOCIETY - Termux Installer                         ${NC}${RED}║${NC}"
echo -e "${RED}║${BOLD}  Created by: HELL SOCIETY Community                      ${NC}${RED}║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}[i] Starting installation...${NC}"
echo -e "${YELLOW}[i] This may take 5-10 minutes. Please wait.${NC}"
echo ""

# ============================================================
# STEP 0: Check if running in Termux
# ============================================================
if [[ "$PREFIX" != *"/data/data/com.termux"* ]]; then
    echo -e "${YELLOW}[!] This script is designed for Termux on Android${NC}"
    echo -e "${YELLOW}[!] For Linux, use install.sh instead${NC}"
    echo -e "${RED}[!] Proceeding anyway...${NC}"
    sleep 2
fi

# ============================================================
# STEP 1: UPDATE PACKAGES
# ============================================================
echo -e "${GREEN}[1/7] Updating package lists...${NC}"
pkg update -y 2>/dev/null || apt-get update -y 2>/dev/null
echo -e "${GREEN}[+] Updated${NC}"
echo ""

# ============================================================
# STEP 2: INSTALL BASE PACKAGES (available in Termux repos)
# ============================================================
echo -e "${GREEN}[2/7] Installing base packages...${NC}"

# These packages are confirmed available in Termux repos
pkg install -y \
    python \
    git \
    nano \
    vim \
    curl \
    wget \
    nmap \
    whois \
    dnsutils \
    openssl \
    openssh \
    termux-api \
    tsu \
    clang \
    make \
    cmake \
    pkg-config \
    net-tools \
    termux-exec \
    libcrypt 2>/dev/null

echo -e "${GREEN}[+] Base packages installed${NC}"
echo ""

# ============================================================
# STEP 3: INSTALL PYTHON NATIVE PACKAGES (via pkg)
# ============================================================
echo -e "${GREEN}[3/7] Installing Python native packages (via pkg)...${NC}"

# These are pre-compiled for Termux - no compilation needed
pkg install -y python-cryptography 2>/dev/null && echo -e "${GREEN}[+] python-cryptography${NC}"
pkg install -y python-numpy 2>/dev/null && echo -e "${GREEN}[+] python-numpy${NC}"
pkg install -y python-lxml 2>/dev/null && echo -e "${GREEN}[+] python-lxml${NC}"

echo -e "${GREEN}[+] Native Python packages done${NC}"
echo ""

# ============================================================
# STEP 4: INSTALL PIP PACKAGES (pure Python)
# ============================================================
echo -e "${GREEN}[4/7] Installing pip packages...${NC}"

# Set environment for Termux compilation
export CFLAGS="-I$PREFIX/include"
export LDFLAGS="-L$PREFIX/lib"
export CPPFLAGS="-I$PREFIX/include"
export LD_LIBRARY_PATH="$PREFIX/lib"

# Install pip packages - using --break-system-packages for newer Python
# These are packages that work on Termux (pure Python or with native support)
for pkg_name in \
    colorama \
    requests \
    beautifulsoup4 \
    soupsieve \
    dnspython \
    paramiko \
    bcrypt \
    pyasn1 \
    pyasn1-modules \
    six \
    cffi \
    pycparser \
    PyNaCl \
    scapy \
    netifaces \
    python-whois \
    lxml \
    Pillow; do

    echo -n "    Installing ${pkg_name}... "
    pip install --break-system-packages "${pkg_name}" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP (may need manual install)${NC}"
    fi
done

# Try pycryptodome with CFLAGS set
echo -n "    Installing pycryptodome... "
CFLAGS="-I$PREFIX/include" LDFLAGS="-L$PREFIX/lib" pip install --break-system-packages pycryptodome 2>/dev/null
if python3 -c "from Crypto.Cipher import AES" 2>/dev/null; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}SKIP (use pkg install python-cryptography instead)${NC}"
fi

echo ""

# ============================================================
# STEP 5: INSTALL SECURITY TOOLS FROM GITHUB
# ============================================================
echo -e "${GREEN}[5/7] Installing security tools from GitHub...${NC}"

cd ~

# SQLMap
echo -n "    [*] sqlmap... "
if ! command -v sqlmap &>/dev/null; then
    git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git ~/sqlmap-dev 2>/dev/null
    if [ -f ~/sqlmap-dev/sqlmap.py ]; then
        ln -sf ~/sqlmap-dev/sqlmap.py $PREFIX/bin/sqlmap 2>/dev/null
        chmod +x $PREFIX/bin/sqlmap 2>/dev/null
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

# WhatWeb
echo -n "    [*] whatweb... "
if ! command -v whatweb &>/dev/null; then
    git clone --depth 1 https://github.com/urbanadventurer/WhatWeb.git ~/WhatWeb 2>/dev/null
    if [ -d ~/WhatWeb ]; then
        ln -sf ~/WhatWeb/whatweb $PREFIX/bin/whatweb 2>/dev/null
        chmod +x $PREFIX/bin/whatweb 2>/dev/null
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

# Sublist3r
echo -n "    [*] sublist3r... "
if ! command -v sublist3r &>/dev/null; then
    git clone --depth 1 https://github.com/aboul3la/Sublist3r.git ~/Sublist3r 2>/dev/null
    if [ -d ~/Sublist3r ]; then
        pip install --break-system-packages -r ~/Sublist3r/requirements.txt 2>/dev/null || true
        ln -sf ~/Sublist3r/sublist3r.py $PREFIX/bin/sublist3r 2>/dev/null
        chmod +x $PREFIX/bin/sublist3r 2>/dev/null
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

# SecLists wordlists
echo -n "    [*] SecLists... "
if [ ! -d ~/SecLists ]; then
    git clone --depth 1 https://github.com/danielmiessler/SecLists.git ~/SecLists 2>/dev/null
    if [ -d ~/SecLists ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

# Hydra (try from pkg first, then from source)
echo -n "    [*] hydra... "
if ! command -v hydra &>/dev/null; then
    pkg install -y hydra 2>/dev/null
    if ! command -v hydra &>/dev/null; then
        cd /tmp
        git clone --depth 1 https://github.com/vanhauser-thc/thc-hydra.git 2>/dev/null
        cd /tmp/thc-hydra 2>/dev/null
        ./configure --prefix=$PREFIX 2>/dev/null && make -j$(nproc) 2>/dev/null && make install 2>/dev/null
        cd ~
    fi
    if command -v hydra &>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP (compile from source manually if needed)${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

echo ""

# ============================================================
# STEP 6: ADD SECURITY REPO (i-Haklab)
# ============================================================
echo -e "${GREEN}[6/7] Adding security tools repository...${NC}"

mkdir -p $PREFIX/etc/apt/sources.list.d 2>/dev/null

# Download repo list
wget -q -O $PREFIX/etc/apt/sources.list.d/ivam3-termux-packages.list \
    https://raw.githubusercontent.com/ivam3/termux-packages/gh-pages/ivam3-termux-packages.list 2>/dev/null || true

# Download GPG key
curl -fsSL "https://raw.githubusercontent.com/ivam3/termux-packages/gh-pages/dists/stable/public_key.gpg" | \
    gpg --dearmor 2>/dev/null | \
    tee "$PREFIX/etc/apt/trusted.gpg.d/ivam3.gpg" >/dev/null 2>&1 || true

# Update with new repo
apt update 2>/dev/null || true

# Install tools from the repo if available
pkg install -y nikto hashcat 2>/dev/null || true

echo -e "${GREEN}[+] Security repo configured${NC}"
echo ""

# ============================================================
# STEP 7: SETUP WORKSPACE
# ============================================================
echo -e "${GREEN}[7/7] Setting up workspace...${NC}"

# Create directories
mkdir -p ~/hell-society/data 2>/dev/null
mkdir -p ~/hell-society/output 2>/dev/null
mkdir -p ~/hell-society/reports 2>/dev/null
mkdir -p ~/hell-society/wordlists 2>/dev/null

# Copy wordlists
if [ -d ~/SecLists ]; then
    ln -sf ~/SecLists ~/hell-society/wordlists/seclists 2>/dev/null
fi

# Setup storage access for Termux
termux-setup-storage 2>/dev/null || true

# Set permissions
cd "$(dirname "$0")" 2>/dev/null || cd ~/hell-society 2>/dev/null
find . -name "*.py" -exec chmod +x {} \; 2>/dev/null
find . -name "*.sh" -exec chmod +x {} \; 2>/dev/null

echo -e "${GREEN}[+] Workspace ready${NC}"
echo ""

# ============================================================
# FINAL MESSAGE
# ============================================================
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${BOLD}  INSTALLATION COMPLETE!                                   ${NC}${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}  How to launch:${NC}"
echo -e "  ${YELLOW}cd ~/hell-society && python3 launcher.py${NC}"
echo -e "  ${YELLOW}OR: ./run${NC}"
echo ""
echo -e "${CYAN}  Installed:${NC}"
echo -e "  ${GREEN}[+] Python 3 + pip${NC}"
echo -e "  ${GREEN}[+] nmap, whois, dnsutils${NC}"
echo -e "  ${GREEN}[+] openssl, curl, wget${NC}"
echo -e "  ${GREEN}[+] clang, make, cmake${NC}"
echo -e "  ${GREEN}[+] sqlmap${NC}"
echo -e "  ${GREEN}[+] whatweb${NC}"
echo -e "  ${GREEN}[+] sublist3r${NC}"
echo -e "  ${GREEN}[+] SecLists wordlists${NC}"
echo -e "  ${GREEN}[+] colorama, requests, bs4${NC}"
echo -e "  ${GREEN}[+] scapy, paramiko, dnspython${NC}"
echo -e "  ${GREEN}[+] cryptography (via pkg)${NC}"
echo -e "  ${GREEN}[+] pycryptodome${NC}"
echo ""
echo -e "${RED}  HELL SOCIETY - NO LIABILITY FOR MISUSE${NC}"
echo ""
echo -e "${YELLOW}  Press Enter to continue...${NC}"
read

# Verify installation
echo ""
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"
echo -e "${CYAN}  VERIFICATION:${NC}"
echo -e "${CYAN}═══════════════════════════════════════════════════════════════════${NC}"

python3 -c "import colorama; print('  [OK] colorama')" 2>/dev/null || echo "  [!!] colorama MISSING"
python3 -c "import requests; print('  [OK] requests')" 2>/dev/null || echo "  [!!] requests MISSING"
python3 -c "import bs4; print('  [OK] beautifulsoup4')" 2>/dev/null || echo "  [!!] beautifulsoup4 MISSING"
python3 -c "import scapy; print('  [OK] scapy')" 2>/dev/null || echo "  [!!] scapy MISSING"
python3 -c "import paramiko; print('  [OK] paramiko')" 2>/dev/null || echo "  [!!] paramiko MISSING"
python3 -c "import Crypto; print('  [OK] pycryptodome')" 2>/dev/null || echo "  [i]  pycryptodome (use cryptography instead)"
python3 -c "import cryptography; print('  [OK] cryptography')" 2>/dev/null || echo "  [!!] cryptography MISSING"
python3 -c "import dns; print('  [OK] dnspython')" 2>/dev/null || echo "  [!!] dnspython MISSING"
command -v nmap &>/dev/null && echo "  [OK] nmap" || echo "  [!!] nmap MISSING"
command -v whois &>/dev/null && echo "  [OK] whois" || echo "  [!!] whois MISSING"
command -v sqlmap &>/dev/null && echo "  [OK] sqlmap" || echo "  [i]  sqlmap in ~/sqlmap-dev/"
command -v hydra &>/dev/null && echo "  [OK] hydra" || echo "  [i]  hydra not installed"

echo ""
echo -e "${GREEN}  Done! Ready to use.${NC}"
