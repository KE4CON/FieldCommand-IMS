#!/usr/bin/env bash
# =========================================================
# FieldCommand EmComm Field Server — Interactive Installer
# Version 1.0  |  For Raspberry Pi 5 (16 GB) / Ubuntu 24
# =========================================================
set -euo pipefail

FC_VERSION="1.0"
FC_USER="fieldcommand"
FC_HOME="/opt/fieldcommand"
FC_DATA="$FC_HOME/data"
FC_PYTHON="$FC_HOME/python"
FC_VENV="$FC_HOME/venv"
FC_WEB="/opt/fieldcommand/html"
FC_LOG="/var/log/fieldcommand-install.log"

AMBER='\033[0;33m'
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'
DIM='\033[2m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Non-interactive / config-file support ──────────────────────────
# The one-command orchestrator (fieldcommand-setup.sh) runs this installer
# unattended on the first boot from the SSD RAID. It passes the operator's
# answers ahead of time so nothing is typed twice. Two ways in:
#   * --config FILE / FC_CONFIG=FILE : a shell file that sets the vars below
#   * --noninteractive / FC_NONINTERACTIVE=1 : never prompt; use presets/defaults
# When neither is used, the installer prompts exactly as it always has.
NONINTERACTIVE="${FC_NONINTERACTIVE:-0}"
FC_CONFIG="${FC_CONFIG:-}"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --config) FC_CONFIG="$2"; shift 2 ;;
        --config=*) FC_CONFIG="${1#*=}"; shift ;;
        --noninteractive|--unattended|-y) NONINTERACTIVE=1; shift ;;
        *) shift ;;
    esac
done
if [[ -n "$FC_CONFIG" ]]; then
    if [[ -f "$FC_CONFIG" ]]; then
        # shellcheck disable=SC1090
        source "$FC_CONFIG"
        NONINTERACTIVE=1   # a config file implies unattended
    else
        echo "Config file not found: $FC_CONFIG" >&2
        exit 1
    fi
fi

# ask VARNAME "prompt text" "default"
# If VARNAME is already set (from config/env) it is kept. In non-interactive
# mode the default is used without prompting. Otherwise it prompts, falling
# back to the default on empty input or EOF (won't abort under `set -e`).
ask() {
    local __v="$1" __p="$2" __d="${3-}" __in=""
    if [[ -n "${!__v-}" ]]; then return 0; fi
    if [[ "$NONINTERACTIVE" == "1" ]]; then printf -v "$__v" '%s' "$__d"; return 0; fi
    read -rp "$__p" __in || __in=""
    printf -v "$__v" '%s' "${__in:-$__d}"
}

# ── Logging ────────────────────────────────────────────────────────
log() { echo -e "$1" | tee -a "$FC_LOG"; }
info()    { log "${CYAN}[INFO]${NC}  $1"; }
success() { log "${GREEN}[OK]${NC}    $1"; }
warn()    { log "${AMBER}[WARN]${NC}  $1"; }
error()   { log "${RED}[ERROR]${NC} $1"; exit 1; }
step()    { log "\n${BOLD}${AMBER}━━━ $1 ━━━${NC}"; }

# ── Root check ─────────────────────────────────────────────────────
if [[ $EUID -ne 0 ]]; then
    echo -e "${RED}This installer must be run as root: sudo bash install.sh${NC}"
    exit 1
fi

# ── Banner ─────────────────────────────────────────────────────────
clear
cat << 'BANNER'

  ███████╗██╗███████╗██╗      ██████╗  ██████╗ ██████╗ ███╗   ███╗███████╗
  ██╔════╝██║██╔════╝██║     ██╔════╝ ██╔═══██╗██╔══██╗████╗ ████║██╔════╝
  █████╗  ██║█████╗  ██║     ██║      ██║   ██║██╔══██╗██╔████╔██║███████╗
  ██╔══╝  ██║██╔══╝  ██║     ██║      ██║   ██║██║  ██║██║╚██╔╝██║╚════██║
  ██║     ██║███████╗███████╗╚██████╗ ╚██████╔╝██████╔╝██║ ╚═╝ ██║███████║
  ╚═╝     ╚═╝╚══════╝╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝

        EmComm Field Server v1.0  —  Raspberry Pi Installer
BANNER
echo ""

# ── Prerequisites check ────────────────────────────────────────────
step "Checking Prerequisites"

OS=$(lsb_release -si 2>/dev/null || echo "Unknown")
VER=$(lsb_release -sr 2>/dev/null || echo "0")
ARCH=$(uname -m)

info "OS: $OS $VER ($ARCH)"
info "Kernel: $(uname -r)"

if [[ "$OS" != "Raspbian" && "$OS" != "Ubuntu" && "$OS" != "Debian" ]]; then
    warn "Unsupported OS detected. Raspbian/Ubuntu/Debian recommended. Continuing anyway."
fi

RAM_KB=$(grep MemTotal /proc/meminfo | awk '{print $2}')
RAM_GB=$(( RAM_KB / 1024 / 1024 ))
if [[ $RAM_KB -lt 1048576 ]]; then
    warn "Less than 1 GB RAM detected (${RAM_KB}KB). 2 GB+ recommended."
else
    info "RAM: ${RAM_GB} GB — OK"
fi

DISK_FREE=$(df -BG / | awk 'NR==2 {print $4}' | tr -d 'G')
if [[ $DISK_FREE -lt 4 ]]; then
    warn "Less than 4 GB free disk space (${DISK_FREE}GB available). 8 GB+ recommended."
else
    info "Disk free: ${DISK_FREE} GB — OK"
fi

mkdir -p "$(dirname $FC_LOG)"
touch "$FC_LOG"

# ── Interactive configuration ──────────────────────────────────────
step "Installation Configuration"

if [[ "$NONINTERACTIVE" != "1" ]]; then
    echo ""
    echo -e "${BOLD}Select installation profile:${NC}"
    echo "  1) Full installation (recommended) — all services, WiFi AP, FCC DB"
    echo "  2) Server only — Python APIs + web, no WiFi AP config"
    echo "  3) Web only — copy HTML files, no Python services"
    echo "  4) Update — update files in existing installation"
    echo ""
fi
ask PROFILE "Profile [1-4, default=1]: " 1

# Callsign is OPTIONAL. Leave it blank for a group with no amateur operators —
# the app then keeps its Amateur Radio features grayed out (see setup wizard /
# index.html gating). A callsign can be added later in the Setup wizard.
echo "" 2>/dev/null || true
ask CALLSIGN "Station callsign — leave blank if no amateur operators (e.g. W8ABC): " ""
CALLSIGN="${CALLSIGN^^}"

ask STATION_LAT "Station latitude [42.3153]: " 42.3153
ask STATION_LON "Station longitude [-88.4473]: " -88.4473
# NOTE: the Pi does NOT broadcast Wi-Fi — the ASUS router creates EMCOMM-NET.
# These two values are only recorded for the server's own display; set the SAME
# Wi-Fi name and password on the router itself. (See the One-Command Setup
# Quick Start guide.)
if [[ "$NONINTERACTIVE" != "1" ]]; then
    echo -e "  ${DIM}The Pi does NOT create the Wi-Fi — the ASUS router broadcasts EMCOMM-NET.${NC}"
    echo -e "  ${DIM}Enter the same name/password you set (or will set) on the router.${NC}"
fi
ask AP_SSID "Wi-Fi name the ROUTER broadcasts — Pi does NOT create Wi-Fi [EMCOMM-NET]: " EMCOMM-NET
ask AP_PASS "Wi-Fi password (must match the router) [fieldcommand2026]: " fieldcommand2026
ask SERVER_IP "Server IP address [192.168.50.1]: " 192.168.50.1
# Optional third-party case software (only useful on a SunFounder Pironman 5 case).
ask INSTALL_PIRONMAN "Install SunFounder Pironman case software (power button, fan, OLED)? [y/N]: " N

if [[ "$PROFILE" == "1" ]]; then
    ask DO_FCC "Download FCC amateur database? (~600MB) [y/N]: " N
fi

if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    if [[ "$NONINTERACTIVE" != "1" ]]; then
        echo ""
        echo -e "${BOLD}Offline Map Tiles${NC} (served on port 8083)"
        echo -e "  Downloads map tiles for McHenry County so maps work with no internet."
        echo -e "  Tiles are stored as MBTiles SQLite files on the Pi."
        echo ""
        echo -e "  ${GREEN}1 — Essential${NC}   Z8–Z14  ~8 MB   ~2 min    Overview to street level"
        echo -e "  ${AMBER}2 — Standard${NC}    Z8–Z16  ~180 MB ~25 min   Full street + block detail"
        echo -e "  ${CYAN}3 — Full${NC}         Z8–Z17  ~1.6 GB ~4 hr     Building-level detail"
        echo -e "  ${DIM}0 — Skip (maps use online tiles when available)${NC}"
        echo ""
    fi
    ask TILE_PRESET "Map tile preset [0-3, default=1]: " 1
else
    TILE_PRESET=0
fi

if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    if [[ "$NONINTERACTIVE" != "1" ]]; then
        echo ""
        echo -e "${BOLD}Kiwix Offline Library${NC} (served on port 8081)"
        echo -e "  Provides offline reference docs to all devices on EMCOMM-NET."
        echo -e "  Requires internet at install time. Downloads can be resumed."
        echo ""
        echo -e "  ${GREEN}1 — Tier 1 Essential${NC}   ~2.5 GB   WikiMed + Wikipedia Mini + Wikivoyage"
        echo -e "  ${AMBER}2 — Tier 2 Extended${NC}    ~10 GB    + Wikibooks + iFixit repair manuals"
        echo -e "  ${CYAN}3 — Tier 3 Full suite${NC}  ~25 GB    + Medical Wikipedia + Wikiversity + Electronics SE"
        echo -e "  ${DIM}0 — Skip downloads (install Kiwix service only, add ZIMs later)${NC}"
        echo ""
    fi
    ask KIWIX_TIER "Kiwix content tier [0-3, default=1]: " 1
else
    KIWIX_TIER=0
fi

echo ""
echo -e "${BOLD}Configuration summary:${NC}"
echo -e "  Profile:     ${AMBER}$PROFILE${NC}"
if [[ -n "$CALLSIGN" ]]; then
    echo -e "  Callsign:    ${AMBER}$CALLSIGN${NC}"
else
    echo -e "  Callsign:    ${DIM}none — amateur radio features stay disabled${NC}"
fi
echo -e "  Coordinates: ${AMBER}$STATION_LAT, $STATION_LON${NC}"
echo -e "  WiFi name:   ${AMBER}$AP_SSID${NC} ${DIM}(broadcast by the router, not the Pi)${NC}"
echo -e "  Server IP:   ${AMBER}$SERVER_IP${NC}"
if [[ "${KIWIX_TIER:-0}" != "0" ]]; then
    echo -e "  Kiwix tier:  ${AMBER}Tier ${KIWIX_TIER}${NC}"
else
    echo -e "  Kiwix:       ${DIM}service only (no ZIM downloads)${NC}"
fi
if [[ "${TILE_PRESET:-0}" != "0" ]]; then
    echo -e "  Map tiles:   ${AMBER}Preset ${TILE_PRESET} (McHenry County)${NC}"
else
    echo -e "  Map tiles:   ${DIM}online only (no offline download)${NC}"
fi
echo ""
if [[ "$NONINTERACTIVE" == "1" ]]; then
    info "Non-interactive mode — proceeding with the configuration above."
else
    read -rp "Proceed with installation? [Y/n]: " CONFIRM
    CONFIRM=${CONFIRM:-Y}
    [[ "$CONFIRM" =~ ^[Yy] ]] || { echo "Installation cancelled."; exit 0; }
fi

# ── Package installation ───────────────────────────────────────────
step "Installing System Packages"

apt-get update -qq 2>>"$FC_LOG" || warn "apt update had warnings"

PACKAGES=(
    python3 python3-pip python3-venv
    nginx sqlite3
    git curl wget unzip
    gpsd gpsd-clients
    chrony
    # Note: hostapd/dnsmasq NOT installed — Wi-Fi handled by ASUS RT-BE58 Go router
    rsync
)

if [[ "$PROFILE" != "3" ]]; then
    apt-get install -y "${PACKAGES[@]}" 2>>"$FC_LOG" | grep -E "(Inst|already)" || true
    success "System packages installed"
else
    apt-get install -y nginx rsync 2>>"$FC_LOG" | grep -E "(Inst|already)" || true
    success "nginx installed"
fi

# ── System user ────────────────────────────────────────────────────
step "Creating System User"

if ! id "$FC_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$FC_HOME" "$FC_USER"
    success "Created user: $FC_USER"
else
    info "User $FC_USER already exists"
fi

# ── Directory structure ────────────────────────────────────────────
step "Creating Directory Structure"

dirs=(
    "$FC_HOME"
    "$FC_DATA"
    "$FC_DATA/nets"
    "$FC_DATA/forms"
    "$FC_DATA/ics"
    "$FC_PYTHON"
    "$FC_HOME/scripts"
    "$FC_HOME/docs"
)

for d in "${dirs[@]}"; do
    mkdir -p "$d"
    success "Created: $d"
done

# ── Python virtualenv ──────────────────────────────────────────────
if [[ "$PROFILE" != "3" ]]; then
    step "Setting Up Python Environment"
    
    if [[ ! -d "$FC_VENV" ]]; then
        python3 -m venv "$FC_VENV"
        success "Virtual environment created"
    else
        info "Virtual environment exists — updating"
    fi
    
    "$FC_VENV/bin/pip" install --quiet --upgrade pip 2>>"$FC_LOG"
    "$FC_VENV/bin/pip" install --quiet flask flask-cors requests gpsd-py3 reportlab pypdf 2>>"$FC_LOG"
    success "Python packages installed: flask, flask-cors, requests, gpsd-py3"
fi

# ── Copy Python files ──────────────────────────────────────────────
if [[ "$PROFILE" != "3" ]]; then
    step "Installing Python Services"
    
    PY_FILES=(
        db.py
        fcc_lookup_server.py
        build_fcc_db.py
        health_monitor.py
        deadmans.py
        ics_platform_server.py
        reference_server.py
        gen_operator_cards.py
        tile_server.py
        amprgate_poll.py
        wan_monitor.py
        ics_pdf_downloader.py
        apply_theme.py
        iap_pdf.py
        nims_definitions.py
        nims_resource_types.py
    )
    
    if [[ -f "$SCRIPT_DIR/../python/wan_config_defaults.json" ]]; then
        cp "$SCRIPT_DIR/../python/wan_config_defaults.json" "$FC_PYTHON/wan_config_defaults.json"
        success "Installed: wan_config_defaults.json"
    fi

    for f in "${PY_FILES[@]}"; do
        if [[ -f "$SCRIPT_DIR/../python/$f" ]]; then
            cp "$SCRIPT_DIR/../python/$f" "$FC_PYTHON/$f"
            chmod 755 "$FC_PYTHON/$f"
            success "Installed: $f"
        else
            warn "Not found (skipping): python/$f"
        fi
    done

    # Drop-in template packs (JSON) — db.py seeds these as protected built-ins.
    if [[ -d "$SCRIPT_DIR/../python/seed_templates" ]]; then
        mkdir -p "$FC_PYTHON/seed_templates"
        rsync -a "$SCRIPT_DIR/../python/seed_templates/" "$FC_PYTHON/seed_templates/" 2>>"$FC_LOG" \
            || cp -r "$SCRIPT_DIR/../python/seed_templates/." "$FC_PYTHON/seed_templates/"
        success "Installed: seed_templates/ (drop-in template packs)"
    fi
fi

# ── Copy web files ─────────────────────────────────────────────────
step "Installing Web Frontend"

if [[ -d "$SCRIPT_DIR/../html" ]]; then
    rsync -a --delete "$SCRIPT_DIR/../html/" "$FC_WEB/" 2>>"$FC_LOG"
    success "HTML files deployed to $FC_WEB"
else
    error "html/ directory not found in $SCRIPT_DIR"
fi

# Patch station config into HTML files
info "Patching station configuration into HTML files..."
find "$FC_WEB" -name "*.html" | while read -r f; do
    sed -i "s/STATION_LAT *= *42\.3153/STATION_LAT = $STATION_LAT/g" "$f"
    sed -i "s/STATION_LON *= *-88\.4473/STATION_LON = $STATION_LON/g" "$f"
    # Only substitute the callsign placeholder when a callsign was provided.
    # Blank = a non-amateur group; leave the placeholder so nothing renders empty
    # (the UI reads the live callsign from /api/config and gates amateur features).
    [[ -n "$CALLSIGN" ]] && sed -i "s/W8ABC/$CALLSIGN/g" "$f"
done
if [[ -n "$CALLSIGN" ]]; then
    success "Station configuration patched (callsign: $CALLSIGN, lat/lon: $STATION_LAT/$STATION_LON)"
else
    success "Station configuration patched (no callsign — amateur features disabled; lat/lon: $STATION_LAT/$STATION_LON)"
fi

# ── Systemd services ───────────────────────────────────────────────
if [[ "$PROFILE" != "3" ]]; then
    step "Installing Systemd Services"
    
    SERVICES=(
        fcc-lookup.service
        health-monitor.service
        deadmans.service
        ics-platform.service
        fcc-refresh.service
        fcc-refresh.timer
        fieldcommand-backup@.service
        fieldcommand-refs.service
        pat.service
        amprgate-poll.service
        wan-monitor.service
    )
    
    for f in "${SERVICES[@]}"; do
        if [[ -f "$SCRIPT_DIR/../systemd/$f" ]]; then
            cp "$SCRIPT_DIR/../systemd/$f" "/etc/systemd/system/$f"
            success "Installed: $f"
        else
            warn "Not found (skipping): systemd/$f"
        fi
    done
    
    systemctl daemon-reload
    
    for svc in fcc-lookup health-monitor deadmans ics-platform fieldcommand-refs amprgate-poll wan-monitor; do
        systemctl enable "$svc.service" 2>>"$FC_LOG" && success "Enabled: $svc"
    done
    
    systemctl enable fcc-refresh.timer 2>>"$FC_LOG" && success "Enabled: fcc-refresh.timer"
fi

# ── nginx configuration ────────────────────────────────────────────
step "Configuring Firewall (ufw)"
if command -v ufw &>/dev/null; then
    ufw allow 22/tcp    comment "SSH"        2>>"$FC_LOG" || true
    ufw allow 80/tcp    comment "nginx HTTP (redirects to HTTPS)" 2>>"$FC_LOG" || true
    ufw allow 443/tcp   comment "nginx HTTPS" 2>>"$FC_LOG" || true
    # Core API services (5050 FCC, 5051 Health, 5055 ICS, 5056 Refs) are bound to
    # 127.0.0.1 and reached ONLY through nginx (/svc/<port>) over HTTPS. They are
    # deliberately NOT opened on the LAN, so operator PII is never on the wire in
    # cleartext. (Do not re-add ufw allow rules for 5050/5051/5055/5056.)
    ufw allow 8000/tcp  comment "Direwolf AGWPE TNC"  2>>"$FC_LOG" || true
    ufw allow 8001/tcp  comment "Direwolf KISS TNC"   2>>"$FC_LOG" || true
    ufw allow 8081/tcp  comment "Kiwix Library"     2>>"$FC_LOG" || true
    ufw allow 8083/tcp  comment "Tile Server"       2>>"$FC_LOG" || true
    ufw allow 8090/tcp  comment "Pat Winlink"       2>>"$FC_LOG" || true
    ufw --force enable  2>>"$FC_LOG" && success "Firewall configured (80/443 web; core APIs localhost-only)" || warn "ufw enable failed"
else
    warn "ufw not found — ports may be blocked. Install with: sudo apt-get install ufw"
fi

step "Generating TLS certificate (HTTPS)"
# nginx serves the dashboard over HTTPS. On this closed LAN (no public domain) we
# create our own certificate: a private local Certificate Authority by default
# (install its root on devices once for a warning-free padlock), or a single
# self-signed cert if TLS_SELF_SIGNED=1. Must exist before 'nginx -t' below.
command -v openssl >/dev/null 2>&1 || apt-get install -y openssl 2>>"$FC_LOG" || true
CERT_ARGS="--ip ${SERVER_IP:-192.168.50.1}"
[[ "${TLS_SELF_SIGNED:-0}" == "1" ]] && CERT_ARGS="$CERT_ARGS --self-signed"
if bash "$SCRIPT_DIR/fc-gen-cert.sh" $CERT_ARGS 2>>"$FC_LOG"; then
    if [[ "${TLS_SELF_SIGNED:-0}" == "1" ]]; then
        success "TLS certificate ready (self-signed — devices show a one-time warning)"
    else
        success "TLS certificate ready (local CA — install /opt/fieldcommand/html/fieldcommand-ca.crt on devices for a clean padlock)"
    fi
else
    warn "TLS certificate generation failed — HTTPS will not start until it exists (see $FC_LOG)"
fi

step "Configuring nginx"

if [[ -f "$SCRIPT_DIR/../udev/nginx-fieldcommand.conf" ]]; then
    cp "$SCRIPT_DIR/../udev/nginx-fieldcommand.conf" /etc/nginx/sites-available/fieldcommand
    ln -sf /etc/nginx/sites-available/fieldcommand /etc/nginx/sites-enabled/fieldcommand
    rm -f /etc/nginx/sites-enabled/default
    nginx -t 2>>"$FC_LOG" && success "nginx config valid" || warn "nginx config test failed — check manually"
    systemctl enable nginx 2>>"$FC_LOG"
    systemctl restart nginx 2>>"$FC_LOG" && success "nginx restarted"
else
    warn "nginx config not found — using defaults"
    systemctl enable nginx 2>>"$FC_LOG"
fi

# ── WiFi AP configuration ──────────────────────────────────────────
if [[ "$PROFILE" == "1" ]]; then
    step "Configuring Pi 5 Static IP (NetworkManager)"
    info "Wi-Fi is provided by the ASUS RT-BE58 Go router — Pi does NOT run hostapd"
    
    # Find the Ethernet connection name
    ETH_CON=$(nmcli -t -f NAME,TYPE con show | grep ethernet | head -1 | cut -d: -f1)
    if [[ -z "$ETH_CON" ]]; then
        ETH_CON="Wired connection 1"
        warn "Could not detect Ethernet connection name — defaulting to: $ETH_CON"
    fi
    
    info "Setting static IP $SERVER_IP/24 on: $ETH_CON"
    nmcli con mod "$ETH_CON"         ipv4.addresses "$SERVER_IP/24"         ipv4.method manual 2>>"$FC_LOG"         && success "Static IP configured: $SERVER_IP/24 on $ETH_CON"         || warn "nmcli failed — set static IP manually after reboot (see manual Chapter 34.5)"
    
    # Also install the NetworkManager config file for reference
    if [[ -f "$SCRIPT_DIR/../udev/NetworkManager-static-ip.conf" ]]; then
        cp "$SCRIPT_DIR/../udev/NetworkManager-static-ip.conf"            /opt/fieldcommand/docs/NetworkManager-static-ip.conf
    fi
fi

# ── udev USB backup rule ───────────────────────────────────────────
if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    step "Installing USB Backup Trigger"
    
    if [[ -f "$SCRIPT_DIR/../udev/99-fieldcommand-backup.rules" ]]; then
        cp "$SCRIPT_DIR/../udev/99-fieldcommand-backup.rules" /etc/udev/rules.d/
        udevadm control --reload-rules 2>>"$FC_LOG" && success "udev USB backup rule installed"
    fi

    # Install TNC udev rules (Digirig, SignaLink, etc.)
    if [[ -f "$SCRIPT_DIR/../udev/99-fieldcommand-tnc.rules" ]]; then
        cp "$SCRIPT_DIR/../udev/99-fieldcommand-tnc.rules" /etc/udev/rules.d/
        udevadm control --reload-rules 2>>"$FC_LOG" && success "udev TNC rules installed — /dev/tnc0 symlink will auto-create on plug-in"
    fi
fi

# ── Kiwix offline library ──────────────────────────────────────────
if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    step "Installing Kiwix Offline Library"

    KIWIX_TIER="${KIWIX_TIER:-0}"

    # Copy kiwix.service unit
    if [[ -f "$SCRIPT_DIR/../systemd/kiwix.service" ]]; then
        cp "$SCRIPT_DIR/../systemd/kiwix.service" /etc/systemd/system/kiwix.service
        success "Installed kiwix.service"
    fi

    # Copy the kiwix_setup script to the Pi
    if [[ -f "$SCRIPT_DIR/kiwix_setup.sh" ]]; then
        cp "$SCRIPT_DIR/kiwix_setup.sh" /opt/fieldcommand/scripts/kiwix_setup.sh
        chmod +x /opt/fieldcommand/scripts/kiwix_setup.sh
        success "Installed kiwix_setup.sh → /opt/fieldcommand/scripts/"
    fi

    # Run kiwix setup (install packages, create user/dirs, write service)
    # Pass --tier with --no-prompt so it handles everything non-interactively
    if [[ -f "/opt/fieldcommand/scripts/kiwix_setup.sh" ]]; then
        if [[ "$KIWIX_TIER" != "0" ]]; then
            info "Running Kiwix setup with Tier ${KIWIX_TIER} content…"
            info "This will download up to $([ "$KIWIX_TIER" -eq 1 ] && echo "~2.5 GB" || [ "$KIWIX_TIER" -eq 2 ] && echo "~10 GB" || echo "~25 GB") of ZIM files."
            info "Large downloads may take 30–120 minutes depending on your connection."
            info "If interrupted, re-run: sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh --tier ${KIWIX_TIER}"
            echo ""
            bash /opt/fieldcommand/scripts/kiwix_setup.sh --tier "$KIWIX_TIER" --no-prompt \
                2>>"$FC_LOG" && success "Kiwix setup complete" || \
                warn "Kiwix setup had errors — check $FC_LOG and re-run kiwix_setup.sh"
        else
            # Install service and packages only, no downloads
            info "Installing Kiwix service (no ZIM downloads — run kiwix_setup.sh later)"
            bash /opt/fieldcommand/scripts/kiwix_setup.sh --tier 0 --no-prompt \
                2>>"$FC_LOG" && success "Kiwix service installed" || \
                warn "Kiwix service install had issues — check $FC_LOG"
        fi
    else
        warn "kiwix_setup.sh not found — install Kiwix manually"
        info "Download ZIMs later: sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh"
    fi
fi

# ── GPS configuration ──────────────────────────────────────────────
if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    step "Configuring GPS (gpsd)"

    # Install gpsd udev rules for common GPS devices
    if [[ -f "$SCRIPT_DIR/../udev/99-fieldcommand-gps.rules" ]]; then
        cp "$SCRIPT_DIR/../udev/99-fieldcommand-gps.rules" \
           /etc/udev/rules.d/99-fieldcommand-gps.rules
        udevadm control --reload-rules 2>>"$FC_LOG"
        success "GPS udev rules installed — /dev/gps0 symlink will auto-create on plug-in"
    fi

    # Write gpsd default config
    if [[ -f "$SCRIPT_DIR/../udev/gpsd.conf" ]]; then
        cp "$SCRIPT_DIR/../udev/gpsd.conf" /etc/default/gpsd
        success "gpsd config written: /etc/default/gpsd"
    fi

    # Detect if a GPS is already connected
    GPS_DEVICE=""
    for dev in /dev/ttyUSB0 /dev/ttyUSB1 /dev/ttyACM0 /dev/ttyACM1 /dev/ttyAMA0; do
        if [[ -e "$dev" ]]; then
            info "Detected serial device: $dev (may be GPS)"
            GPS_DEVICE="$dev"
            break
        fi
    done

    if [[ -n "$GPS_DEVICE" ]]; then
        info "Configuring gpsd to use: $GPS_DEVICE"
        sed -i "s|DEVICES=\"/dev/gps0\"|DEVICES=\"$GPS_DEVICE\"|" /etc/default/gpsd
        # Also create the symlink manually if udev hasn't yet
        ln -sf "$GPS_DEVICE" /dev/gps0 2>/dev/null || true
    else
        info "No GPS device detected yet."
        info "Plug in your USB GPS receiver — it will be auto-detected via udev."
        info "Supported: GlobalSat BU-353, u-blox NEO-6/7/8, Adafruit Ultimate GPS, VK-162"
    fi

    # Write station config with installer-provided coordinates as fallback
    STATION_CONFIG_DIR="$FC_DATA"
    mkdir -p "$STATION_CONFIG_DIR"
    cat > "$STATION_CONFIG_DIR/station_config.json" << SCONF
{
  "callsign": "$CALLSIGN",
  "lat": $STATION_LAT,
  "lon": $STATION_LON,
  "gps_enabled": true,
  "gps_device": "${GPS_DEVICE:-/dev/gps0}",
  "configured_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
SCONF
    success "Station config written: $STATION_CONFIG_DIR/station_config.json"

    # Enable and start gpsd
    systemctl enable gpsd 2>>"$FC_LOG" && success "gpsd enabled"
    systemctl restart gpsd 2>>"$FC_LOG" || warn "gpsd restart failed — attach GPS and restart: sudo systemctl restart gpsd"

    # Test gpsd connection
    sleep 1
    if timeout 3 bash -c 'echo "?WATCH={\"enable\":true}" | nc -q1 127.0.0.1 2947' \
       &>/dev/null 2>&1; then
        success "gpsd is responding on port 2947"
    else
        info "gpsd not yet responding (normal if no GPS attached)"
        info "Once GPS is connected: sudo systemctl restart gpsd"
        info "Test with: gpspipe -w -n 5"
    fi
fi

# ── Time sync (chrony + GPS as an offline clock) ───────────────────
if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    step "Configuring time sync (chrony + GPS)"

    # Install the GPS refclock drop-in so the Pi can hold accurate UTC with no
    # internet — gpsd feeds GPS time into chrony via shared memory.
    if [[ -f "$SCRIPT_DIR/../udev/chrony-gps.conf" ]]; then
        mkdir -p /etc/chrony/conf.d
        cp "$SCRIPT_DIR/../udev/chrony-gps.conf" /etc/chrony/conf.d/fieldcommand-gps.conf
        success "GPS refclock config written: /etc/chrony/conf.d/fieldcommand-gps.conf"
        # Older chrony.conf files may not include the conf.d directory — add it once.
        if [[ -f /etc/chrony/chrony.conf ]] && ! grep -q 'conf.d' /etc/chrony/chrony.conf; then
            echo 'confdir /etc/chrony/conf.d' >> /etc/chrony/chrony.conf
            info "Added 'confdir /etc/chrony/conf.d' to chrony.conf"
        fi
    fi

    # chrony and systemd-timesyncd cannot both run — hand timekeeping to chrony.
    systemctl disable --now systemd-timesyncd 2>>"$FC_LOG" || true

    systemctl enable chrony 2>>"$FC_LOG" && success "chrony enabled"
    systemctl restart chrony 2>>"$FC_LOG" || warn "chrony restart failed — check: sudo systemctl status chrony"

    # Best-effort: show chrony's sources (GPS shows as #* / #? once it has a fix).
    sleep 1
    if command -v chronyc >/dev/null 2>&1; then
        chronyc sources 2>>"$FC_LOG" | grep -iE 'NMEA|PPS' >/dev/null 2>&1 \
            && success "GPS reference clock is registered with chrony" \
            || info "GPS refclock will engage once the GPS has a fix (needs sky view)."
    fi
    info "Offline, the Pi keeps UTC from GPS; with a WAN it also uses internet time."
fi

# ── Offline map tiles ──────────────────────────────────────────────
if [[ "$PROFILE" == "1" || "$PROFILE" == "2" ]]; then
    step "Installing Offline Map Tile System"

    TILE_PRESET="${TILE_PRESET:-0}"

    # Copy tile server Python script
    cp "$SCRIPT_DIR/../python/tile_server.py" "$FC_PYTHON/tile_server.py"
    chmod 755 "$FC_PYTHON/tile_server.py"
    success "Installed: tile_server.py"

    # Copy tile download script
    if [[ -f "$SCRIPT_DIR/download_tiles.sh" ]]; then
        cp "$SCRIPT_DIR/download_tiles.sh" "$FC_HOME/scripts/download_tiles.sh"
        chmod +x "$FC_HOME/scripts/download_tiles.sh"
        success "Installed: download_tiles.sh"
    fi

    # Copy lib/ files to web lib directory (belt-and-suspenders — rsync above should cover it
    # but explicit copies ensure these critical shared files are never missing)
    mkdir -p "$FC_WEB/lib"
    if [[ -f "$SCRIPT_DIR/../html/lib/tiles.js" ]]; then
        cp "$SCRIPT_DIR/../html/lib/tiles.js" "$FC_WEB/lib/tiles.js"
        success "Installed: lib/tiles.js"
    fi
    if [[ -f "$SCRIPT_DIR/../html/lib/identity.js" ]]; then
        cp "$SCRIPT_DIR/../html/lib/identity.js" "$FC_WEB/lib/identity.js"
        success "Installed: lib/identity.js"
    fi

    # Create tile storage directory
    mkdir -p "$FC_HOME/tiles"
    chown "${FC_USER}:${FC_USER}" "$FC_HOME/tiles"
    success "Created: $FC_HOME/tiles/"

    # Install systemd service
    if [[ -f "$SCRIPT_DIR/../systemd/fieldcommand-tiles.service" ]]; then
        cp "$SCRIPT_DIR/../systemd/fieldcommand-tiles.service" \
           /etc/systemd/system/fieldcommand-tiles.service
        systemctl daemon-reload
        systemctl enable fieldcommand-tiles 2>>"$FC_LOG"
        success "Installed: fieldcommand-tiles.service (port 8083)"
    fi

    # Download tiles if requested
    if [[ "$TILE_PRESET" != "0" ]]; then
        case "$TILE_PRESET" in
            1) TILE_FLAGS="--mchenry-essential" ;;
            2) TILE_FLAGS="--mchenry-standard" ;;
            3) TILE_FLAGS="--area county_mchenry --zoom 8-17 --sources usgs_topo,esri_street,esri_imagery" ;;
        esac

        info "Downloading McHenry County map tiles (Preset ${TILE_PRESET})…"
        info "If interrupted, re-run: sudo bash $FC_HOME/scripts/download_tiles.sh"

        # Run as fieldcommand user can't write to tile dir yet — run as root
        bash "$FC_HOME/scripts/download_tiles.sh" $TILE_FLAGS --no-prompt \
            2>>"$FC_LOG" && success "Map tiles downloaded" || \
            warn "Tile download had issues — re-run download_tiles.sh to retry"
    else
        info "Skipping tile download — maps will use online sources when available"
        info "Download tiles later: sudo bash $FC_HOME/scripts/download_tiles.sh"
    fi
fi

# ── Pat Winlink ────────────────────────────────────────────────────
step "Installing Pat Winlink (backup Winlink client on port 8090)"
info "Pat is the browser-based Winlink backup client. Primary Winlink = Winlink Express on Windows."

PAT_VER="1.0.0"
ARCH=$(dpkg --print-architecture 2>/dev/null || uname -m)
case "$ARCH" in
    arm64|aarch64) PAT_DEB="pat_${PAT_VER}_linux_arm64.deb" ;;
    armhf|armv7l)  PAT_DEB="pat_${PAT_VER}_linux_armhf.deb" ;;
    amd64|x86_64)  PAT_DEB="pat_${PAT_VER}_linux_amd64.deb" ;;
    *)             PAT_DEB="pat_${PAT_VER}_linux_arm64.deb"
                   warn "Unknown arch $ARCH — defaulting to arm64 .deb" ;;
esac

PAT_URL="https://github.com/la5nta/pat/releases/download/v${PAT_VER}/${PAT_DEB}"
PAT_TMP="/tmp/${PAT_DEB}"

info "Downloading Pat v${PAT_VER} (${ARCH})..."
if wget -q --show-progress -O "$PAT_TMP" "$PAT_URL" 2>>"$FC_LOG"; then
    if dpkg -i "$PAT_TMP" 2>>"$FC_LOG"; then
        success "Pat installed: $(pat --version 2>/dev/null | head -1)"
        rm -f "$PAT_TMP"

        # Write Pat config — fieldcommand user's home is /opt/fieldcommand (not /home/fieldcommand)
        PAT_CFG_DIR="$FC_HOME/.config/pat"
        mkdir -p "$PAT_CFG_DIR"
        if [[ ! -f "$PAT_CFG_DIR/config.json" ]]; then
            cat > "$PAT_CFG_DIR/config.json" << PATCFG
{
  "mycall": "${CALLSIGN}",
  "secure_login_password": "",
  "locator": "",
  "http_addr": "0.0.0.0:8090",
  "motd": ["Incident Management EmComm Server — K9ESV"],
  "connect_aliases": {},
  "listen": ["http"],
  "ax25": {"port": ""},
  "serial_tnc": {"path": "", "baudrate": 0},
  "vara": {"host": "localhost", "cmdPort": 8300, "dataPort": 8301},
  "gpsd": {"enable_auto_locator": false, "addr": "localhost:2947"}
}
PATCFG
            chown -R "$FC_USER:$FC_USER" "$PAT_CFG_DIR"
            success "Pat config written ($PAT_CFG_DIR, callsign: $CALLSIGN)"
        else
            info "Pat config already exists — skipping"
        fi

        # Install and enable pat.service
        if [[ -f "$SCRIPT_DIR/../systemd/pat.service" ]]; then
            cp "$SCRIPT_DIR/../systemd/pat.service" /etc/systemd/system/pat.service
            systemctl daemon-reload
            systemctl enable pat.service 2>>"$FC_LOG" && success "pat.service enabled"
        else
            warn "pat.service not found in systemd/ — Pat will not start automatically"
        fi
    else
        warn "Pat .deb install failed — Pat will not be available. Try manually: dpkg -i $PAT_TMP"
    fi
else
    warn "Could not download Pat (needs internet). Install manually after deployment:"
    warn "  wget $PAT_URL && sudo dpkg -i ${PAT_DEB}"
fi

# ── CUPS Print Server ──────────────────────────────────────────────────────
if [[ "${SKIP_CUPS:-0}" != "1" ]]; then
    step "Installing CUPS Print Server"
    info "CUPS allows a USB printer on the Pi to be shared across EMCOMM-NET"
    info "Skip with SKIP_CUPS=1 if printing is not needed"

    if apt-get install -y cups cups-bsd cups-client \
        printer-driver-gutenprint avahi-daemon 2>>"$FC_LOG"; then
        success "CUPS and printer drivers installed"

        # Add fieldcommand user and www-data to lpadmin group
        usermod -aG lpadmin "$FC_USER" 2>>"$FC_LOG" || true
        usermod -aG lpadmin www-data 2>>"$FC_LOG" || true

        # Allow CUPS to be managed remotely from EMCOMM-NET (192.168.50.x)
        # Listen on all interfaces so field devices can reach the web UI
        if [[ -f /etc/cups/cupsd.conf ]]; then
            # Back up original
            cp /etc/cups/cupsd.conf /etc/cups/cupsd.conf.bak

            # Allow remote access from EMCOMM-NET subnet
            python3 - << 'CUPSPY'
import re

with open('/etc/cups/cupsd.conf', 'r') as f:
    cfg = f.read()

# Listen on all interfaces (not just localhost)
cfg = re.sub(r'Listen localhost:631', 'Listen 0.0.0.0:631', cfg)
cfg = re.sub(r'Port 631\nListen /var/run/cups/cups.sock',
             'Port 631\nListen /var/run/cups/cups.sock', cfg)

# Add EMCOMM-NET access to server policy if not present
if '192.168.50.' not in cfg:
    cfg = cfg.replace(
        '<Location />\n  Order allow,deny\n</Location>',
        '<Location />\n  Order allow,deny\n  Allow from 127.0.0.1\n  Allow from 192.168.50.*\n</Location>'
    )
    cfg = cfg.replace(
        '<Location /admin>\n  Order allow,deny\n</Location>',
        '<Location /admin>\n  Order allow,deny\n  Allow from 127.0.0.1\n  Allow from 192.168.50.*\n</Location>'
    )

with open('/etc/cups/cupsd.conf', 'w') as f:
    f.write(cfg)
print("cupsd.conf updated")
CUPSPY
        fi

        # Enable Bonjour/mDNS printer sharing (for automatic discovery)
        cupsctl --share-printers --remote-printers 2>>"$FC_LOG" || true

        # Open CUPS web admin port in firewall
        ufw allow 631/tcp comment "CUPS printer admin" 2>>"$FC_LOG" || true

        # Enable and start CUPS + Avahi
        systemctl enable cups avahi-daemon 2>>"$FC_LOG"
        systemctl restart cups avahi-daemon 2>>"$FC_LOG" \
            && success "CUPS started — admin UI at http://192.168.50.1:631" \
            || warn "CUPS start failed — check: journalctl -u cups"

        info "After connecting a USB printer, add it at: http://192.168.50.1:631"
        info "Then share it so all EMCOMM-NET devices can print to it"
    else
        warn "CUPS install failed — printing will not be available via the Pi"
    fi
else
    info "Skipping CUPS installation (SKIP_CUPS=1)"
    info "Install manually: sudo apt install cups cups-bsd printer-driver-gutenprint avahi-daemon"
fi

# ── APRS — Direwolf TNC (RF) → APRS Command ───────────────────────────────
if [[ "${SKIP_APRS:-0}" != "1" ]]; then
    step "Installing APRS (Direwolf TNC)"
    info "Optional — skip with SKIP_APRS=1 if APRS is not needed"
    info "The tactical map's RF stations are served by APRS Command (run on a"
    info "laptop) or a small KISS bridge reading Direwolf — no on-Pi APRS client."

    # ── Direwolf — RF KISS/AGW TNC ──────────────────────────────────────────
    # Direwolf is a software TNC that decodes APRS off the radio and exposes a
    # KISS (8001) and AGWPE (8000) TCP interface. Unlike the old Graywolf, it has
    # NO HTTP/REST API — the "serve stations to the tactical map" job now belongs
    # to APRS Command (Windows laptop) or a Pi-side KISS bridge that connects to
    # these ports. Direwolf itself is receive-only here unless PTT is configured.
    info "Installing Direwolf software TNC..."
    if apt-get install -y direwolf 2>>"$FC_LOG"; then
        success "Direwolf installed: $(direwolf -h 2>&1 | head -1 || echo direwolf)"
    else
        warn "Direwolf install failed — RF APRS will not decode. Install manually: apt install direwolf"
    fi

    # Write a starter Direwolf config if one is not already present.
    if [[ ! -f /etc/direwolf.conf ]]; then
        info "Writing starter /etc/direwolf.conf (edit ADEVICE and MYCALL before use)..."
        cat > /etc/direwolf.conf << 'DWCONF'
# FieldCommand IMS — Direwolf starter config.
# EDIT the two marked lines for your station, then: systemctl restart direwolf
#
# 1) Audio input device — run `arecord -l` and set the card,device (e.g. plughw:1,0).
ADEVICE  plughw:1,0
ACHANNELS 1
CHANNEL 0
# 2) Your station callsign-SSID (used only if you enable transmit/beacon).
MYCALL   N0CALL
MODEM 1200
# Client interfaces for APRS Command / KISS bridge (listen on the LAN):
AGWPORT 8000
KISSPORT 8001
# Receive-only by default. To transmit (iGate/digipeat), configure PTT below, e.g.:
#   PTT GPIO 23        (or)   PTT CM108
# and add IGSERVER / IGLOGIN for iGate. Leave commented for a listen-only TNC.
DWCONF
        chown "$FC_USER:$FC_USER" /etc/direwolf.conf 2>/dev/null || true
        success "Wrote /etc/direwolf.conf (starter — edit ADEVICE + MYCALL)"
    else
        info "/etc/direwolf.conf already present — leaving it unchanged"
    fi

    # Write and enable direwolf.service (prefers the repo copy if present).
    if [[ -f "$SCRIPT_DIR/../systemd/direwolf.service" ]]; then
        cp "$SCRIPT_DIR/../systemd/direwolf.service" /etc/systemd/system/direwolf.service
    else
        cat > /etc/systemd/system/direwolf.service << 'DWSVC'
[Unit]
Description=Direwolf APRS KISS/AGW software TNC
After=sound.target network.target

[Service]
Type=simple
User=fieldcommand
Group=fieldcommand
ExecStart=/usr/bin/direwolf -t 0 -c /etc/direwolf.conf
Restart=always
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=direwolf

[Install]
WantedBy=multi-user.target
DWSVC
    fi
    systemctl daemon-reload
    systemctl enable direwolf.service 2>>"$FC_LOG" \
        && success "direwolf.service created and enabled" \
        || warn "direwolf.service enable failed — enable manually: systemctl enable direwolf"

else
    info "Skipping APRS installation (SKIP_APRS=1)"
    info "Install manually later:"
    info "  Direwolf TNC:  sudo apt install direwolf   (edit /etc/direwolf.conf, then systemctl enable direwolf)"
    info "  APRS stations reach the tactical map from APRS Command (laptop) or a KISS bridge — nothing to install on the Pi."
fi

# ── Set permissions ────────────────────────────────────────────────
step "Setting Permissions"

chown -R "$FC_USER:$FC_USER" "$FC_HOME"
chown -R www-data:www-data "$FC_WEB"
chmod -R 755 "$FC_WEB"
chmod -R 770 "$FC_DATA"
usermod -aG "$FC_USER" www-data 2>>/dev/null || true
success "Permissions set"

# ── ICS PDF forms download ─────────────────────────────────────────────────
if [[ "${SKIP_ICS_PDF:-0}" != "1" ]]; then
    step "Downloading FEMA ICS Forms PDFs"
    info "Downloads 22 official FEMA ICS forms — requires internet connection"
    info "Skip with:  SKIP_ICS_PDF=1 bash install.sh"
    mkdir -p "$FC_DATA/ics_forms"
    if "$FC_HOME/venv/bin/python" "$FC_HOME/python/ics_pdf_downloader.py" \
        --output "$FC_DATA/ics_forms" >> "$FC_LOG" 2>&1; then
        success "ICS forms downloaded to $FC_DATA/ics_forms/"
    else
        warn "Some ICS forms failed — run manually after deployment:"
        warn "  python3 $FC_HOME/python/ics_pdf_downloader.py"
    fi
else
    info "Skipping ICS PDF download (SKIP_ICS_PDF=1)"
fi

# ── Theme consistency check ────────────────────────────────────────────────
step "Verifying HTML Theme Consistency"
if "$FC_HOME/venv/bin/python" "$FC_HOME/python/apply_theme.py" \
    --dir "$FC_WEB" --check >> "$FC_LOG" 2>&1; then
    success "All HTML files have correct theme variables"
else
    info "Applying theme fixes..."
    "$FC_HOME/venv/bin/python" "$FC_HOME/python/apply_theme.py" \
        --dir "$FC_WEB" --apply >> "$FC_LOG" 2>&1
    success "Theme variables applied"
fi

# ── FCC database download ──────────────────────────────────────────
if [[ "${DO_FCC:-N}" =~ ^[Yy] ]]; then
    step "Downloading FCC Amateur Database"
    info "This will download ~600MB from FCC.gov and build the SQLite database."
    info "This may take 10–20 minutes on a Raspberry Pi."
    
    if sudo -u "$FC_USER" "$FC_VENV/bin/python" "$FC_PYTHON/build_fcc_db.py" 2>>"$FC_LOG"; then
        success "FCC database built: $FC_DATA/fcc.db"
    else
        warn "FCC database build failed. Run manually: sudo -u fieldcommand $FC_VENV/bin/python $FC_PYTHON/build_fcc_db.py"
    fi
fi

# ── Start services ─────────────────────────────────────────────────
if [[ "$PROFILE" != "3" ]]; then
    step "Starting Services"
    
    for svc in fcc-lookup health-monitor deadmans ics-platform fieldcommand-tiles fieldcommand-refs amprgate-poll wan-monitor; do
        if systemctl start "$svc.service" 2>>"$FC_LOG"; then
            success "Started: $svc"
        else
            warn "Failed to start $svc — check: journalctl -u $svc"
        fi
    done
    
    systemctl start fcc-refresh.timer 2>>"$FC_LOG" && success "Started: fcc-refresh.timer"
fi

# ── Optional: SunFounder Pironman case software (power button, fan, OLED) ──
# Third-party, opt-in. Off by default. Only useful on a SunFounder Pironman 5
# case. Runs SunFounder's own installer non-interactively (--variant max) and
# sets the Pi 5 to fully cut power on halt. Never fatal — the FieldCommand
# install still succeeds if this step can't complete.
if [[ "${INSTALL_PIRONMAN:-N}" =~ ^[Yy] ]]; then
    step "Installing Pironman case software (SunFounder, optional)"
    info "Third-party software from SunFounder for the Pironman 5 case."

    # Make a Pi 5 halt actually cut power, so shutdown and the button power it off.
    if command -v rpi-eeprom-config >/dev/null 2>&1; then
        _pm_tmp="$(mktemp)"
        rpi-eeprom-config > "$_pm_tmp" 2>/dev/null || true
        if grep -q '^POWER_OFF_ON_HALT=' "$_pm_tmp"; then
            sed -i 's/^POWER_OFF_ON_HALT=.*/POWER_OFF_ON_HALT=1/' "$_pm_tmp"
        else
            echo 'POWER_OFF_ON_HALT=1' >> "$_pm_tmp"
        fi
        rpi-eeprom-config --apply "$_pm_tmp" >>"$FC_LOG" 2>&1 \
            && success "Set POWER_OFF_ON_HALT=1 (full power off on shutdown)" \
            || warn "Could not set POWER_OFF_ON_HALT — set it via: sudo raspi-config → Advanced → Shutdown Behaviour → Full Power Off"
        rm -f "$_pm_tmp"
    fi

    _pm_cmd='curl -sSL "https://raw.githubusercontent.com/sunfounder/pironman5/v1/install.sh" | sudo bash -s -- --variant max'
    if curl -fsSL -m 30 "https://raw.githubusercontent.com/sunfounder/pironman5/v1/install.sh" -o /tmp/pironman5_install.sh 2>>"$FC_LOG"; then
        if timeout 900 bash /tmp/pironman5_install.sh --variant max --no-autologin </dev/null >>"$FC_LOG" 2>&1; then
            success "Pironman software installed — reboot to activate the OLED, fan, and power button."
        else
            warn "Pironman auto-install did not finish. Run it by hand on the Pi: $_pm_cmd"
        fi
        rm -f /tmp/pironman5_install.sh
    else
        warn "No internet (or download failed) — skipped Pironman software. Install later: $_pm_cmd"
    fi
fi

# ── Done ───────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}${BOLD}╔══════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}${BOLD}║           FieldCommand Installation Complete!              ║${NC}"
echo -e "${GREEN}${BOLD}╚══════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BOLD}Access the dashboard:${NC}"
echo -e "  Local:    ${CYAN}http://localhost/${NC}"
echo -e "  Network:  ${CYAN}http://$SERVER_IP/${NC}"
if [[ "$PROFILE" == "1" ]]; then
    echo -e "  WiFi:     Connect to ${CYAN}$AP_SSID${NC} (password: $AP_PASS)"
    echo -e "            Then browse to ${CYAN}http://$SERVER_IP/${NC}"
fi
echo ""
echo -e "${BOLD}Service status:${NC}"
echo -e "  ${CYAN}systemctl status fcc-lookup health-monitor deadmans ics-platform${NC}"
echo ""
echo -e "${BOLD}Logs:${NC}"
echo -e "  ${CYAN}journalctl -fu fcc-lookup${NC}"
echo -e "  ${CYAN}journalctl -fu ics-platform${NC}"
echo -e "  Install log: ${CYAN}$FC_LOG${NC}"
echo ""
echo -e "${BOLD}AMPRNet / 44Net Gateway:${NC}"
echo -e "  Gateway Pi:   ${CYAN}http://192.168.50.2:9000${NC}  (configure separately)"
echo -e "  This Pi:      ${CYAN}http://$SERVER_IP/amprgate.html${NC}"
echo -e "  Setup guide:  ${CYAN}sudo bash scripts/setup_44net.sh${NC}  (run on gateway Pi)"
echo -e "  See Installation Guide Step 11 for complete setup instructions."
echo ""
echo -e "${BOLD}FCC Database (if not downloaded):${NC}"
echo -e "  ${CYAN}sudo -u fieldcommand $FC_VENV/bin/python $FC_PYTHON/build_fcc_db.py${NC}"
echo ""
echo -e "${BOLD}Offline Map Tiles (port 8083):${NC}"
if [[ "${TILE_PRESET:-0}" != "0" ]]; then
    echo -e "  ${GREEN}✓${NC} McHenry County tiles downloaded — ${CYAN}http://$SERVER_IP:8083/${NC}"
else
    echo -e "  ${AMBER}No tiles downloaded. Maps use online tiles when available.${NC}"
fi
echo -e "  Download tiles: ${CYAN}sudo bash /opt/fieldcommand/scripts/download_tiles.sh${NC}"
echo -e "  List options:   ${CYAN}sudo bash /opt/fieldcommand/scripts/download_tiles.sh --list${NC}"
echo ""
if [[ "${KIWIX_TIER:-0}" != "0" ]]; then
    echo -e "  ${GREEN}✓${NC} Tier ${KIWIX_TIER} ZIMs installed — ${CYAN}http://$SERVER_IP:8081${NC}"
else
    echo -e "  ${AMBER}Service installed, no ZIMs downloaded yet.${NC}"
fi
echo -e "  Add/update ZIMs: ${CYAN}sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh${NC}"
echo -e "  List available:  ${CYAN}sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh --list${NC}"
echo ""
if [[ "$PROFILE" == "1" ]]; then
    echo -e "${AMBER}Reboot recommended to activate WiFi AP and all services.${NC}"
    read -rp "Reboot now? [y/N]: " DO_REBOOT
    [[ "$DO_REBOOT" =~ ^[Yy] ]] && reboot
fi

exit 0
