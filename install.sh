#!/bin/bash
# ╔══════════════════════════════════════════════════════════════════╗
# ║  HELL SOCIETY CYBER TOOLKIT - UNIVERSAL INSTALLER               ║
# ║  Created by: HELL SOCIETY Community                              ║
# ║  Compatible: Linux (Debian/Ubuntu/Kali) + Termux (Android)       ║
# ╚══════════════════════════════════════════════════════════════════╝

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  HELL SOCIETY - Cyber Toolkit Installer v2.0                     ║"
echo "║  Compatible: Linux + Termux                                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Detect platform
if [[ "$(uname)" == *"Android"* ]] || [[ "$PREFIX" == *"/data/data/com.termux"* ]]; then
    echo "[*] Platform detected: TERMUX (Android)"
    PLATFORM="termux"
else
    echo "[*] Platform detected: LINUX ($(uname -a))"
    PLATFORM="linux"
fi

echo ""

# ──────────────────────────────────────────────────────────────
# PYTHON DEPENDENCIES (Both platforms)
# ──────────────────────────────────────────────────────────────
echo "[*] Installing Python dependencies..."

if [ "$PLATFORM" == "termux" ]; then
    echo "[*] Termux: Installing packages via pkg..."
    pkg update -y
    pkg install -y python python-pip git nmap whois dnsutils net-tools openssh curl wget
    pip install --upgrade pip
    pip install colorama requests beautifulsoup4 pillow pycryptodome
    echo "[+] Termux Python dependencies installed"
else
    echo "[*] Linux: Installing packages via apt..."
    sudo apt-get update -y
    sudo apt-get install -y python3 python3-pip git nmap whois dnsutils net-tools openssh-client curl wget
    sudo pip3 install --upgrade pip
    sudo pip3 install colorama requests beautifulsoup4 pillow pycryptodome scapy python-whois dnspython paramiko
    echo "[+] Linux Python dependencies installed"
fi

echo ""

# ──────────────────────────────────────────────────────────────
# PLATFORM-SPECIFIC TOOLS
# ──────────────────────────────────────────────────────────────
if [ "$PLATFORM" == "termux" ]; then
    echo "[*] Installing Termux-specific tools..."

    # Install additional Termux packages
    pkg install -y hydra sqlmap tcpdump termux-api tsu

    # Make scripts executable
    chmod +x launcher.py
    chmod +x install.sh

    # Create Termux-specific launcher
    cat > run.sh << 'TERMUX_EOF'
#!/data/data/com.termux/files/usr/bin/bash
# HELL SOCIETY - Termux Launcher
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  HELL SOCIETY - Termux Launcher                                  ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

if [ -z "$1" ]; then
    python3 launcher.py
else
    python3 "$1"
fi
TERMUX_EOF
    chmod +x run.sh

    echo "[+] Termux tools installed"
    echo "[+] run.sh created for quick launch"

else
    echo "[*] Installing Linux-specific tools..."

    # Install additional Linux security tools
    sudo apt-get install -y hydra sqlmap tcpdump tcpdump sslscan nikto gobuster dirb wfuzz
    sudo apt-get install -y sslh openvpn

    # Make scripts executable
    chmod +x launcher.py
    chmod +x install.sh

    echo "[+] Linux tools installed"
fi

echo ""

# ──────────────────────────────────────────────────────────────
# SET PERMISSIONS
# ──────────────────────────────────────────────────────────────
echo "[*] Setting permissions..."
find . -name "*.py" -exec chmod +x {} \;
find . -name "*.sh" -exec chmod +x {} \;

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  INSTALLATION COMPLETE!                                          ║"
echo "║                                                                  ║"
if [ "$PLATFORM" == "termux" ]; then
    echo "║  RUN: ./run.sh               (Termux menu)                   ║"
    echo "║  RUN: python3 launcher.py    (Full menu)                     ║"
    echo "║  RUN: bash run.sh script.py  (Single script)                 ║"
else
    echo "║  RUN: python3 launcher.py    (Full menu)                     ║"
    echo "║  RUN: ./run.sh               (Quick launcher)                ║"
    echo "║  RUN: python3 script.py      (Single script)                 ║"
fi
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Display compatibility info
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║  PLATFORM: $PLATFORM                                                ║"
if [ "$PLATFORM" == "termux" ]; then
    echo "║  PYTHON: $(which python3 || which python)                     ║"
    echo "║  PREFIX: $PREFIX                                               ║"
else
    echo "║  PYTHON: $(which python3)                                    ║"
    echo "║  OS: $(cat /etc/os-release 2>/dev/null | grep PRETTY_NAME)   ║"
fi
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
