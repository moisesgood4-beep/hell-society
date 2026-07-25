#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
#  HELL SOCIETY - Termux Setup Script v3
#  Compatible with Android / Termux (aarch64, arm, x86_64)
#  Created by: HELL SOCIETY Community
#  Tested: Python 3.13 on Termux / aarch64
# ============================================================

clear

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

echo -e "${RED}╔══════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${RED}║${BOLD}  HELL SOCIETY - Termux Installer v3                      ${NC}${RED}║${NC}"
echo -e "${RED}║${BOLD}  Created by: HELL SOCIETY Community                      ${NC}${RED}║${NC}"
echo -e "${RED}╚══════════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${YELLOW}[i] Starting installation...${NC}"
echo -e "${YELLOW}[i] This may take 5-10 minutes. Please wait.${NC}"
echo ""

# ============================================================
# STEP 1: UPDATE PACKAGES
# ============================================================
echo -e "${GREEN}[1/8] Updating package lists...${NC}"
pkg update -y 2>/dev/null || apt-get update -y 2>/dev/null
pkg upgrade -y 2>/dev/null
echo -e "${GREEN}[+] Updated${NC}"
echo ""

# ============================================================
# STEP 2: INSTALL BASE PACKAGES
# ============================================================
echo -e "${GREEN}[2/8] Installing base packages...${NC}"

pkg install -y \
    python \
    python-pip \
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
    libcrypt \
    libffi \
    libgmp \
    libjpeg-turbo \
    libpng \
    zlib \
    freetype \
    libxml2 \
    libxslt \
    readline \
    libsqlite \
    ncurses 2>/dev/null

echo -e "${GREEN}[+] Base packages installed${NC}"
echo ""

# ============================================================
# STEP 3: INSTALL PYTHON NATIVE PACKAGES (via pkg - PRE-COMPILED)
# ============================================================
echo -e "${GREEN}[3/8] Installing pre-compiled Python packages...${NC}"

# These are pre-compiled binaries - NO compilation needed
pkg install -y python-cryptography 2>/dev/null && echo -e "    ${GREEN}[+] python-cryptography${NC}"
pkg install -y python-numpy 2>/dev/null && echo -e "    ${GREEN}[+] python-numpy${NC}"
pkg install -y python-lxml 2>/dev/null && echo -e "    ${GREEN}[+] python-lxml${NC}"
pkg install -y python-pillow 2>/dev/null && echo -e "    ${GREEN}[+] python-pillow${NC}"
pkg install -y python-pandas 2>/dev/null && echo -e "    ${GREEN}[+] python-pandas${NC}"
pkg install -y python-scipy 2>/dev/null && echo -e "    ${GREEN}[+] python-scipy${NC}"

echo -e "${GREEN}[+] Pre-compiled packages done${NC}"
echo ""

# ============================================================
# STEP 4: INSTALL PIP PACKAGES (NO BUILD NEEDED)
# ============================================================
echo -e "${GREEN}[4/8] Installing pip packages...${NC}"

# Set CFLAGS for Termux
export CFLAGS="-I$PREFIX/include"
export LDFLAGS="-L$PREFIX/lib"
export CPPFLAGS="-I$PREFIX/include"
export LD_LIBRARY_PATH="$PREFIX/lib"

# Install pure Python packages that DON'T need compilation
for pkg_name in \
    colorama \
    requests \
    beautifulsoup4 \
    soupsieve \
    dnspython \
    pyasn1 \
    pyasn1-modules \
    six \
    pycparser \
    scapy \
    netifaces \
    python-whois \
    lxml \
    chardet \
    idna \
    urllib3 \
    certifi \
    typing-extensions; do

    echo -n "    Installing ${pkg_name}... "
    pip install --break-system-packages "${pkg_name}" 2>/dev/null 1>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
done

# Install paramiko (depends on bcrypt + pynacl)
echo -n "    Installing paramiko... "
pip install --break-system-packages paramiko 2>/dev/null 1>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}SKIP (bcrypt/pynacl may fail)${NC}"
fi

# Try bcrypt separately (needs compilation)
echo -n "    Installing bcrypt... "
pkg install -y python-bcrypt 2>/dev/null
if python3 -c "import bcrypt" 2>/dev/null; then
    echo -e "${GREEN}OK (via pkg)${NC}"
else
    pip install --break-system-packages bcrypt 2>/dev/null 1>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK (via pip)${NC}"
    else
        echo -e "${YELLOW}SKIP (not critical)${NC}"
    fi
fi

# Try pynacl separately
echo -n "    Installing PyNaCl... "
pip install --break-system-packages PyNaCl 2>/dev/null 1>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}SKIP (not critical)${NC}"
fi

# pycryptodome
echo -n "    Installing pycryptodome... "
pkg install -y python-pycryptodome 2>/dev/null
if python3 -c "from Crypto.Cipher import AES" 2>/dev/null; then
    echo -e "${GREEN}OK (via pkg)${NC}"
else
    pip install --break-system-packages pycryptodome 2>/dev/null 1>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}OK (via pip)${NC}"
    else
        echo -e "${YELLOW}SKIP (use cryptography instead)${NC}"
    fi
fi

echo ""

# ============================================================
# STEP 5: INSTALL SECURITY TOOLS FROM GITHUB
# ============================================================
echo -e "${GREEN}[5/8] Installing security tools...${NC}"

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
        pip install --break-system-packages -r ~/Sublist3r/requirements.txt 2>/dev/null 1>/dev/null || true
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

# Hydra
echo -n "    [*] hydra... "
if ! command -v hydra &>/dev/null; then
    # Try pkg first
    pkg install -y hydra 2>/dev/null
    if ! command -v hydra &>/dev/null; then
        # Try from source
        cd /tmp
        rm -rf thc-hydra 2>/dev/null
        git clone --depth 1 https://github.com/vanhauser-thc/thc-hydra.git 2>/dev/null
        if [ -d /tmp/thc-hydra ]; then
            cd /tmp/thc-hydra
            ./configure --prefix=$PREFIX 2>/dev/null && make -j$(nproc) 2>/dev/null && make install 2>/dev/null
        fi
        cd ~
    fi
    if command -v hydra &>/dev/null; then
        echo -e "${GREEN}OK${NC}"
    else
        echo -e "${YELLOW}SKIP${NC}"
    fi
else
    echo -e "${GREEN}ALREADY INSTALLED${NC}"
fi

echo ""

# ============================================================
# STEP 6: ADD SECURITY REPO (i-Haklab)
# ============================================================
echo -e "${GREEN}[6/8] Adding security tools repository...${NC}"

mkdir -p $PREFIX/etc/apt/sources.list.d 2>/dev/null

wget -q -O $PREFIX/etc/apt/sources.list.d/ivam3-termux-packages.list \
    https://raw.githubusercontent.com/ivam3/termux-packages/gh-pages/ivam3-termux-packages.list 2>/dev/null || true

curl -fsSL "https://raw.githubusercontent.com/ivam3/termux-packages/gh-pages/dists/stable/public_key.gpg" | \
    gpg --dearmor 2>/dev/null | \
    tee "$PREFIX/etc/apt/trusted.gpg.d/ivam3.gpg" >/dev/null 2>&1 || true

apt update 2>/dev/null || true
pkg install -y nikto hashcat 2>/dev/null || true

echo -e "${GREEN}[+] Security repo configured${NC}"
echo ""

# ============================================================
# STEP 7: SETUP WORKSPACE
# ============================================================
echo -e "${GREEN}[7/8] Setting up workspace...${NC}"

mkdir -p ~/hell-society/data 2>/dev/null
mkdir -p ~/hell-society/output 2>/dev/null
mkdir -p ~/hell-society/reports 2>/dev/null
mkdir -p ~/hell-society/wordlists 2>/dev/null

if [ -d ~/SecLists ]; then
    ln -sf ~/SecLists ~/hell-society/wordlists/seclists 2>/dev/null
fi

termux-setup-storage 2>/dev/null || true

cd "$(dirname "$0")" 2>/dev/null || cd ~/hell-society 2>/dev/null
find . -name "*.py" -exec chmod +x {} \; 2>/dev/null
find . -name "*.sh" -exec chmod +x {} \; 2>/dev/null

echo -e "${GREEN}[+] Workspace ready${NC}"
echo ""

# ============================================================
# STEP 8: VERIFICATION
# ============================================================
echo -e "${GREEN}[8/8] Verifying installation...${NC}"
echo ""

echo -e "${CYAN}  ┌─────────────────────────────────────────────┐${NC}"
echo -e "${CYAN}  │ VERIFICATION RESULTS                        │${NC}"
echo -e "${CYAN}  └─────────────────────────────────────────────┘${NC}"
echo ""

PASS=0
FAIL=0

check_py() {
    if python3 -c "import $1" 2>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} $1"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}[!!]${NC} $1 MISSING"
        FAIL=$((FAIL + 1))
    fi
}

check_cmd() {
    if command -v "$1" &>/dev/null; then
        echo -e "  ${GREEN}[OK]${NC} $1"
        PASS=$((PASS + 1))
    else
        echo -e "  ${RED}[!!]${NC} $1 MISSING"
        FAIL=$((FAIL + 1))
    fi
}

# Check Python packages
check_py colorama
check_py requests
check_py bs4
check_py scapy
check_py paramiko
check_py Crypto
check_py cryptography
check_py dns
check_py PIL
check_py dnspython
check_py lxml

# Check system tools
check_cmd nmap
check_cmd whois
check_cmd sqlmap
check_cmd hydra
check_cmd openssl
check_cmd git

echo ""
echo -e "  ${GREEN}PASSED: ${PASS} | FAILED: ${FAIL}${NC}"
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
echo -e "${CYAN}  System info:${NC}"
echo -e "  Android: $(getprop ro.build.version.release 2>/dev/null || echo 'N/A')"
echo -e "  Termux:  $TERMUX_VERSION"
echo -e "  Python:  $(python3 --version 2>/dev/null || echo 'N/A')"
echo -e "  Arch:    $(uname -m)"
echo ""
echo -e "${RED}  HELL SOCIETY - NO LIABILITY FOR MISUSE${NC}"
echo ""
echo -e "${YELLOW}  Press Enter to continue...${NC}"
read
