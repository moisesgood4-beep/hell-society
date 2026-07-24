#!/data/data/com.termux/files/usr/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HELL SOCIETY - TERMUX SETUP                                    ║
# ║  Created by: HELL SOCIETY Community                              ║
# ║  Auto-setup for Android Termux environment                       ║
# ║  Tested: Termux 0.118+ / Android 12+ / aarch64                  ║
# ╚══════════════════════════════════════════════════════════════════╝

clear

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║   ██╗  ██╗ ██████╗ ███╗   ███╗███████╗                           ║"
echo "║   ██║  ██║██╔═══██╗████╗ ████║██╔════╝                           ║"
echo "║   ███████║██║   ██║██╔████╔██║███████╗                           ║"
echo "║   ██╔══██║██║   ██║██║╚██╔╝██║╚════██║                           ║"
echo "║   ██║  ██║╚██████╔╝██║ ╚═╝ ██║███████║                           ║"
echo "║   ╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝                           ║"
echo "╠══════════════════════════════════════════════════════════════════╣"
echo "║  HELL SOCIETY - Termux Setup Wizard                              ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if running on Termux
if [[ "$(uname)" != *"Android"* ]] && [[ "$PREFIX" != *"/data/data/com.termux"* ]]; then
    echo "[!] This script is designed for Termux on Android"
    echo "[!] For Linux, use install.sh instead"
    exit 1
fi

# ──────────────────────────────────────────────────────────────────
# STEP 1: UPDATE & UPGRADE
# ──────────────────────────────────────────────────────────────────
echo "[1/7] Updating Termux packages..."
pkg update -y 2>/dev/null
pkg upgrade -y 2>/dev/null
echo "[+] Termux updated"
echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 2: INSTALL CORE PACKAGES
# ──────────────────────────────────────────────────────────────────
echo "[2/7] Installing core packages..."
pkg install -y \
    python \
    python-pip \
    python-numpy \
    git \
    nano \
    vim \
    curl \
    wget \
    net-tools \
    nmap \
    whois \
    dnsutils \
    openssh \
    termux-api \
    tsu \
    clang \
    make \
    cmake \
    pkg-config \
    openssl-dev \
    libffi \
    libgmp \
    libxml2 \
    libxslt
echo "[+] Core packages installed"
echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 3: INSTALL SECURITY TOOLS (from source/git)
# ──────────────────────────────────────────────────────────────────
echo "[3/7] Installing security tools..."

# SQLMap - install from git
echo "    [*] Installing SQLmap..."
cd ~
git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git sqlmap-dev 2>/dev/null
if [ -f ~/sqlmap-dev/sqlmap.py ]; then
    # Create symlink
    ln -sf ~/sqlmap-dev/sqlmap.py ~/../usr/bin/sqlmap
    chmod +x ~/sqlmap-dev/sqlmap.py
    echo "    [+] SQLmap installed"
else
    echo "    [!] SQLmap install skipped (offline?)"
fi

# Hydra - install from source
echo "    [*] Installing Hydra..."
cd /tmp
git clone --depth 1 https://github.com/vanhauser-thc/thc-hydra.git 2>/dev/null
cd /tmp/thc-hydra
./configure 2>/dev/null && make 2>/dev/null && make install 2>/dev/null
if command -v hydra &>/dev/null; then
    echo "    [+] Hydra installed"
else
    echo "    [i] Hydra needs compilation, trying alternative..."
    pkg install -y hydra 2>/dev/null
    if command -v hydra &>/dev/null; then
        echo "    [+] Hydra installed via pkg"
    else
        echo "    [!] Hydra install skipped"
    fi
fi
cd ~

# TCPDump - use Termux's version
echo "    [*] Installing tcpdump..."
pkg install -y tcpdump 2>/dev/null
if command -v tcpdump &>/dev/null; then
    echo "    [+] tcpdump installed"
else
    echo "    [i] tcpdump not available in repos, using alternatives"
fi

echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 4: INSTALL PYTHON PACKAGES (NO PIP UPGRADE)
# ──────────────────────────────────────────────────────────────────
echo "[4/7] Installing Python packages..."

# Install cryptography from pkg (avoids Rust compilation error)
echo "    [*] Installing cryptography from pkg..."
pkg install -y python-cryptography 2>/dev/null
echo "    [+] cryptography installed"

# Install Python packages (skip pycryptodome if it fails)
echo "    [*] Installing pure-Python packages..."
pip install \
    colorama \
    requests \
    beautifulsoup4 \
    pillow \
    dnspython \
    paramiko
echo "    [+] Python packages installed"

# Try pycryptodome (may need clang)
echo "    [*] Trying pycryptodome..."
export CFLAGS="-I$PREFIX/include"
export LDFLAGS="-L$PREFIX/lib"
pip install pycryptodome 2>/dev/null
if python3 -c "import Crypto" 2>/dev/null; then
    echo "    [+] pycryptodome installed"
else
    echo "    [i] pycryptodome skipped (not critical for most tools)"
    echo "    [i] Install manually: pkg install python-cryptography"
fi

echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 5: CONFIGURE STORAGE
# ──────────────────────────────────────────────────────────────────
echo "[5/7] Setting up storage access..."
mkdir -p ~/hell-society/data 2>/dev/null
mkdir -p ~/hell-society/results 2>/dev/null
mkdir -p ~/hell-society/wordlists 2>/dev/null
echo "[+] Data directories created"
echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 6: SET PERMISSIONS
# ──────────────────────────────────────────────────────────────────
echo "[6/7] Setting permissions..."
cd "$(dirname "$0")"
find . -name "*.py" -exec chmod +x {} \;
find . -name "*.sh" -exec chmod +x {} \;
echo "[+] All scripts are executable"
echo ""

# ──────────────────────────────────────────────────────────────────
# STEP 7: CREATE QUICK LAUNCHER
# ──────────────────────────────────────────────────────────────────
echo "[7/7] Creating launcher..."

# Create run script
cat > ./run << 'EOF'
#!/data/data/com.termux/files/usr/bin/bash
cd "$(dirname "$0")"
clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════╗"
echo "  ║  HELL SOCIETY - Quick Launcher                           ║"
echo "  ╚══════════════════════════════════════════════════════════╝"
echo ""

if [ -z "$1" ]; then
    python3 launcher.py
else
    python3 "$1" "$@"
fi
EOF
chmod +x ./run

# Create alias for global access
TOOLKIT_DIR="$(pwd)"
cat > ~/hell-society/run << EOF
#!/data/data/com.termux/files/usr/bin/bash
cd "$TOOLKIT_DIR"
clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════╗"
echo "  ║  HELL SOCIETY - Quick Launcher                           ║"
echo "  ╚══════════════════════════════════════════════════════════╝"
echo ""

if [ -z "\$1" ]; then
    python3 launcher.py
else
    python3 "\$1" "\$@"
fi
EOF
chmod +x ~/hell-society/run

echo "[+] Launcher created"
echo ""

# ──────────────────────────────────────────────────────────────────
# FINAL
# ──────────────────────────────────────────────────────────────────
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  TERMUX SETUP COMPLETE!                                          ║"
echo "║                                                                  ║"
echo "║  Quick Launch: ./run                                             ║"
echo "║  Full Menu:    python3 launcher.py                               ║"
echo "║  Single Tool:  python3 offensive/01_sql_injection_scanner.py     ║"
echo "║                                                                  ║"
echo "║  Data: ~/hell-society/data/                                      ║"
echo "║  Results: ~/hell-society/results/                                ║"
echo "║  Wordlists: ~/hell-society/wordlists/                            ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Show system info
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  SYSTEM INFO:                                                    ║"
echo "║  Android: $(getprop ro.build.version.release 2>/dev/null || echo 'N/A')"
echo "║  Termux:  $TERMUX_VERSION"
echo "║  Python:  $(python3 --version 2>/dev/null || echo 'N/A')"
echo "║  Arch:    $(uname -m)"
echo "║  SQLmap:  $(command -v sqlmap 2>/dev/null || echo 'Installed in ~/sqlmap-dev')"
echo "║  Hydra:   $(command -v hydra 2>/dev/null || echo 'N/A')"
echo "║  Nmap:    $(command -v nmap 2>/dev/null || echo 'N/A')"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

echo "[+] Ready to hack! Welcome to Hell Society."
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  ADVERTENCIA: Hell Society NO se hace responsable               ║"
echo "║  del mal uso de estas herramientas.                             ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
