#!/usr/bin/env bash
# ============================================================================
# FieldCommand IMS — One-Command Field Server Setup
# Version 1.0  |  Raspberry Pi 5 + Pironman 5 MAX (Dual NVMe RAID 1)
# ============================================================================
#
# WHAT THIS DOES (the whole install, from one command):
#   You flash Raspberry Pi OS (64-bit, full/Desktop) to a microSD card with the
#   Raspberry Pi Imager, boot the Pi 5 from it, open a terminal, and run:
#
#       sudo bash fieldcommand-setup.sh
#
#   From there it is hands-off. It will:
#     1. Make sure the Pi can see BOTH NVMe SSDs behind the Pironman PCIe switch
#        (adds the two required config.txt lines and reboots once if needed).
#     2. Build a true boot-from-RAID-1 mirror across the two SSDs and copy the
#        running OS onto it  (the corrected "Step 1B" from the Install Guide).
#     3. Reboot into the SSD mirror and, on that first boot, automatically run
#        the FieldCommand installer (install.sh) with your answers.
#     4. Finish and tell you to run the one test only you can do by hand:
#        the pull-a-drive failover test.
#
# HOW YOU ANSWER THE QUESTIONS (asked once, at the very start):
#   * Interactively on screen, OR
#   * From a config file so it runs fully unattended. The script looks for
#     fieldcommand.conf on the SD boot partition (/boot/firmware or /boot),
#     next to this script, or wherever --config points. A sample lives at
#     scripts/fieldcommand.conf.sample.
#
# ----------------------------------------------------------------------------
# !! IMPORTANT — READ BEFORE FIRST USE !!
#   * This ERASES BOTH NVMe SSDs. It asks you to confirm the exact drives first.
#   * Booting a Raspberry Pi 5 from a RAID array goes slightly beyond what
#     SunFounder themselves document. This script automates the procedure we
#     validated on paper, but it MUST be bench-tested on your actual hardware
#     (including the pull-a-drive test) before it is trusted in the field.
#   * Run with --dry-run first to see every action without changing anything.
# ============================================================================
set -euo pipefail

FC_SETUP_VERSION="1.0"
STATE_DIR="/var/lib/fieldcommand-setup"
LOG="/var/log/fieldcommand-setup.log"
SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
SCRIPT_DIR="$(cd "$(dirname "$SCRIPT_PATH")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
# Where the installer source is copied on the SSD so first-boot can run it:
ARRAY_SRC="/opt/fieldcommand-installer"

# ── Colors ──────────────────────────────────────────────────────────────────
if [[ -t 1 ]]; then
    RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; AMBER=$'\033[0;33m'
    BLUE=$'\033[0;34m'; CYAN=$'\033[0;36m'; BOLD=$'\033[1m'; DIM=$'\033[2m'; NC=$'\033[0m'
else
    RED=""; GREEN=""; AMBER=""; BLUE=""; CYAN=""; BOLD=""; DIM=""; NC=""
fi

# ── Self-elevate ────────────────────────────────────────────────────────────
# So it can be launched by double-clicking (no need to type "sudo"). If we are
# not root, re-run ourselves through sudo, preserving all arguments.
if [[ $EUID -ne 0 ]]; then
    echo "FieldCommand setup needs administrator rights — you may be asked for your password."
    exec sudo -- bash "$(readlink -f "${BASH_SOURCE[0]}")" "$@"
fi

# ── Options ─────────────────────────────────────────────────────────────────
DRY_RUN=0
ASSUME_YES="${FC_ASSUME_YES:-0}"
FORCE=0
FC_CONFIG="${FC_CONFIG:-}"
SKIP_EEPROM="${FC_SKIP_EEPROM:-0}"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)   DRY_RUN=1; shift ;;
        --yes|-y)    ASSUME_YES=1; shift ;;
        --force)     FORCE=1; shift ;;
        --no-eeprom) SKIP_EEPROM=1; shift ;;
        --config)    FC_CONFIG="$2"; shift 2 ;;
        --config=*)  FC_CONFIG="${1#*=}"; shift ;;
        -h|--help)
            grep -E '^#( |$)' "$SCRIPT_PATH" | sed -E 's/^# ?//'; exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done

# ── Logging ─────────────────────────────────────────────────────────────────
mkdir -p "$(dirname "$LOG")" 2>/dev/null || true
log()     { echo -e "$*" | tee -a "$LOG" >&2; }
info()    { log "${CYAN}[INFO]${NC}  $*"; }
ok()      { log "${GREEN}[OK]${NC}    $*"; }
warn()    { log "${AMBER}[WARN]${NC}  $*"; }
err()     { log "${RED}[ERROR]${NC} $*"; }
die()     { err "$*"; exit 1; }
step()    { log "\n${BOLD}${AMBER}━━━ $* ━━━${NC}"; }

# run CMD... — executes, or just prints it in --dry-run mode
run() {
    if [[ "$DRY_RUN" == "1" ]]; then
        log "${DIM}[dry-run]${NC} $*"
    else
        log "${DIM}\$ $*${NC}"
        "$@"
    fi
}

trap 'err "Setup failed at line $LINENO. See $LOG. Your SD card still boots normally — nothing on it was changed by a failed NVMe step."' ERR

# ── Root check ──────────────────────────────────────────────────────────────
# (We normally self-elevate above; this is a backstop for odd sudo setups.)
[[ $EUID -eq 0 ]] || die "Could not gain administrator rights. Try:  sudo bash $(basename "$SCRIPT_PATH")"

mkdir -p "$STATE_DIR"

# ── Banner ──────────────────────────────────────────────────────────────────
clear 2>/dev/null || true
cat >&2 << BANNER
${BOLD}${CYAN}
  FieldCommand IMS — One-Command Field Server Setup  v${FC_SETUP_VERSION}
  Raspberry Pi 5  +  Pironman 5 MAX  (Dual NVMe RAID 1)
${NC}
BANNER
[[ "$DRY_RUN" == "1" ]] && warn "DRY RUN — no changes will be made. Remove --dry-run to run for real."

# ── Locate the boot/firmware directory (Bookworm vs older) ───────────────────
if [[ -d /boot/firmware ]]; then BOOTDIR=/boot/firmware; else BOOTDIR=/boot; fi
CONFIG_TXT="$BOOTDIR/config.txt"
CMDLINE_TXT="$BOOTDIR/cmdline.txt"

# ── Sanity: we must be running FROM the SD card, not already on NVMe ─────────
ROOT_SRC="$(findmnt -n -o SOURCE / || true)"
if [[ "$ROOT_SRC" == /dev/md* ]]; then
    die "This system is already running from a RAID array ($ROOT_SRC). Setup has already been done."
fi
if [[ "$ROOT_SRC" == /dev/nvme* && "$FORCE" != "1" ]]; then
    die "This system is running from NVMe ($ROOT_SRC), not the microSD card. Boot from the SD card to build the mirror. (--force overrides.)"
fi

# =============================================================================
#  CONFIGURATION  (gather answers once — from file if present, else prompt)
# =============================================================================
load_config() {
    # Search order for an auto-detected config file
    local candidates=()
    [[ -n "$FC_CONFIG" ]] && candidates+=("$FC_CONFIG")
    candidates+=("$BOOTDIR/fieldcommand.conf" "/boot/fieldcommand.conf"
                 "$SCRIPT_DIR/fieldcommand.conf" "$STATE_DIR/fieldcommand.conf")
    local c
    for c in "${candidates[@]}"; do
        if [[ -f "$c" ]]; then
            # shellcheck disable=SC1090
            source "$c"
            FROM_FILE="$c"
            NONINTERACTIVE=1
            info "Loaded configuration from: $c"
            return 0
        fi
    done
    NONINTERACTIVE=0
    return 0
}

ask() {  # ask VARNAME "prompt" "default"
    local __v="$1" __p="$2" __d="${3-}" __in=""
    if [[ -n "${!__v-}" ]]; then return 0; fi
    if [[ "${NONINTERACTIVE:-0}" == "1" ]]; then printf -v "$__v" '%s' "$__d"; return 0; fi
    read -rp "$__p" __in || __in=""
    printf -v "$__v" '%s' "${__in:-$__d}"
}

gather_config() {
    load_config
    step "Field Server Configuration"
    ask PROFILE      "Install profile [1=Full, default]: " 1
    # Callsign is OPTIONAL — leave blank for a group with no amateur operators.
    ask CALLSIGN     "Station callsign — leave blank if no amateur operators: " ""
    CALLSIGN="${CALLSIGN^^}"
    ask STATION_LAT  "Station latitude [42.3153]: " 42.3153
    ask STATION_LON  "Station longitude [-88.4473]: " -88.4473
    ask AP_SSID      "WiFi SSID [EMCOMM-NET]: " EMCOMM-NET
    ask AP_PASS      "WiFi password [fieldcommand2026]: " fieldcommand2026
    ask SERVER_IP    "Server IP [192.168.50.1]: " 192.168.50.1
    ask DO_FCC       "Download FCC amateur database? (~600MB) [y/N]: " N
    ask TILE_PRESET  "Offline map tiles [0=skip..3=full, default 1]: " 1
    ask KIWIX_TIER   "Kiwix offline library tier [0=skip..3, default 1]: " 1

    log ""
    log "${BOLD}Configuration:${NC}"
    if [[ -n "$CALLSIGN" ]]; then
        log "  Callsign:    ${AMBER}$CALLSIGN${NC}  (amateur radio features ON)"
    else
        log "  Callsign:    ${DIM}none — amateur radio features stay disabled${NC}"
    fi
    log "  Coordinates: ${AMBER}$STATION_LAT, $STATION_LON${NC}"
    log "  WiFi SSID:   ${AMBER}$AP_SSID${NC}"
    log "  Server IP:   ${AMBER}$SERVER_IP${NC}"
    log ""
}

# Write the gathered answers to a config file install.sh can source later.
write_config_file() {
    local dest="$1"
    if [[ "$DRY_RUN" == "1" ]]; then
        log "${DIM}[dry-run]${NC} would write config to $dest"
        return 0
    fi
    mkdir -p "$(dirname "$dest")"
    cat > "$dest" << CONF
# FieldCommand answers — generated by fieldcommand-setup.sh $(date -u +%Y-%m-%dT%H:%M:%SZ)
PROFILE="$PROFILE"
CALLSIGN="$CALLSIGN"
STATION_LAT="$STATION_LAT"
STATION_LON="$STATION_LON"
AP_SSID="$AP_SSID"
AP_PASS="$AP_PASS"
SERVER_IP="$SERVER_IP"
DO_FCC="$DO_FCC"
TILE_PRESET="$TILE_PRESET"
KIWIX_TIER="$KIWIX_TIER"
CONF
    chmod 600 "$dest"
    ok "Wrote answers to $dest"
}

# =============================================================================
#  STAGE 0 — make sure BOTH NVMe drives are visible through the PCIe switch
# =============================================================================
ensure_pcie_lines() {
    local changed=0
    grep -qE '^\s*dtparam=pciex1\b'          "$CONFIG_TXT" || { run bash -c "echo 'dtparam=pciex1' >> '$CONFIG_TXT'"; changed=1; }
    grep -qE '^\s*dtparam=pciex1_no_10s=on'  "$CONFIG_TXT" || { run bash -c "echo 'dtparam=pciex1_no_10s=on' >> '$CONFIG_TXT'"; changed=1; }
    return $changed
}

count_nvme() { lsblk -dn -o NAME 2>/dev/null | grep -c '^nvme' || true; }

list_nvme() { lsblk -dn -o NAME,SIZE,MODEL 2>/dev/null | grep '^nvme' || true; }

# =============================================================================
#  Bootloader (EEPROM) — bring every unit to the same known-good firmware
# =============================================================================
# Dual-NVMe boot on the Pi 5 depends on the bootloader firmware version. Staging
# the latest stable EEPROM here means every field server built from this script
# runs the same firmware, which removes one big source of per-unit variance in
# whether both drives are seen and boot-from-RAID works. The update is written
# now and applied automatically at the next reboot (which setup does anyway).
update_bootloader() {
    if [[ "$SKIP_EEPROM" == "1" ]]; then
        info "Skipping bootloader update (--no-eeprom / FC_SKIP_EEPROM=1)."
        return 0
    fi
    if ! command -v rpi-eeprom-update >/dev/null 2>&1; then
        info "rpi-eeprom-update not found — skipping bootloader step (not Raspberry Pi OS?)."
        return 0
    fi
    step "Bootloader (EEPROM) check"
    info "Current bootloader status:"
    rpi-eeprom-update 2>&1 | sed 's/^/    /' | tee -a "$LOG" >&2 || true
    if [[ "$DRY_RUN" == "1" ]]; then
        info "[dry-run] would run: rpi-eeprom-update -a  (stage latest stable, applies next reboot)"
        return 0
    fi
    info "Staging the latest stable bootloader (applies on the next reboot)…"
    if rpi-eeprom-update -a >>"$LOG" 2>&1; then
        ok "Bootloader is current, or an update was staged for the next reboot."
    else
        warn "Could not stage a bootloader update — continuing. You can run 'sudo rpi-eeprom-update -a' by hand."
    fi
}

stage0_pcie() {
    step "Stage 0 — Detect both NVMe SSDs"
    local n; n="$(count_nvme)"
    info "NVMe drives currently visible: $n"
    list_nvme | while read -r l; do info "  $l"; done

    if [[ "$n" -ge 2 ]]; then
        ok "Both SSDs are visible."
        touch "$STATE_DIR/pcie_done"
        return 0
    fi

    warn "Fewer than two NVMe drives are visible."
    # If we already added the PCIe lines and rebooted once, and they STILL aren't
    # both visible, it's a hardware problem — don't loop.
    if [[ -f "$STATE_DIR/pcie_pending" ]]; then
        die "Only $n NVMe drive(s) detected after enabling PCIe and rebooting. Check the SunFounder FFC cable seating and that both SSDs are firmly in their M.2 slots, then re-run."
    fi
    if ! ensure_pcie_lines; then
        info "PCIe lines already present in $CONFIG_TXT but only $n drive(s) seen — likely a cable/seating issue."
        die "Only $n NVMe drive(s) detected with PCIe already enabled. Fix the hardware, then re-run."
    fi

    # We just added the lines. A reboot is required before the Pi can see both
    # SSDs. We deliberately do NOT auto-erase after this reboot — the operator
    # must re-run and confirm the erase, since the drives can't even be shown yet.
    warn "Added the two Pironman PCIe lines to $CONFIG_TXT. A reboot is required for the Pi to see both SSDs."
    write_config_file "$STATE_DIR/fieldcommand.conf"   # preserve answers so the re-run won't re-ask
    [[ "$DRY_RUN" == "1" ]] || touch "$STATE_DIR/pcie_pending"
    log ""
    log "${BOLD}What happens next:${NC} the Pi will reboot so it can see both SSDs."
    log "If you started from the desktop icon or an insert-and-go card, the setup"
    log "re-opens by itself after the reboot. Otherwise, run the same command again:"
    log "  ${CYAN}sudo bash $SCRIPT_PATH${NC}"
    log "Either way your earlier answers were saved, so it picks up where it left"
    log "off and then asks you to confirm erasing the two SSDs."
    log ""
    if [[ "$DRY_RUN" == "1" ]]; then
        info "[dry-run] would reboot now; you would re-run the command after boot."
        return 0
    fi
    if [[ "$ASSUME_YES" != "1" ]]; then
        read -rp "Reboot now? [Y/n]: " a
        [[ "${a:-Y}" =~ ^[Yy] ]] || die "Not rebooting. Reboot yourself, then re-run this script."
    fi
    info "Rebooting…"
    run systemctl reboot
    exit 0
}

# =============================================================================
#  STAGE 1 — pick the two SSDs and CONFIRM the erase
# =============================================================================
pick_disks() {
    step "Stage 1 — Select the two SSDs to mirror (THIS ERASES THEM)"
    # Allow explicit override via config (FC_SSD_A / FC_SSD_B), else auto.
    SSD_A="${FC_SSD_A:-/dev/nvme0n1}"
    SSD_B="${FC_SSD_B:-/dev/nvme1n1}"
    [[ -b "$SSD_A" ]] || die "Not a block device: $SSD_A"
    [[ -b "$SSD_B" ]] || die "Not a block device: $SSD_B"
    [[ "$SSD_A" != "$SSD_B" ]] || die "The two SSDs must be different devices."

    log "${BOLD}${RED}The following drives will be COMPLETELY ERASED:${NC}"
    lsblk -o NAME,SIZE,MODEL,SERIAL "$SSD_A" "$SSD_B" | tee -a "$LOG" >&2
    log ""
    if [[ "$DRY_RUN" == "1" ]]; then warn "[dry-run] skipping erase confirmation."; return 0; fi
    if [[ "$ASSUME_YES" == "1" ]]; then
        warn "--yes given: proceeding to erase $SSD_A and $SSD_B without prompting."
        return 0
    fi
    local reply
    read -rp "Type ${BOLD}YES${NC} (all caps) to erase these two drives and build the mirror: " reply
    [[ "$reply" == "YES" ]] || die "Not confirmed. Nothing was changed."
}

# =============================================================================
#  STAGE 2 — build the boot-from-RAID-1 mirror (the corrected Step 1B)
# =============================================================================
build_mirror() {
    step "Stage 2 — Build the RAID 1 mirror and copy the OS"

    if [[ -e /dev/md0 && "$FORCE" != "1" ]]; then
        die "/dev/md0 already exists. Remove it first, or pass --force. (Refusing to clobber an existing array.)"
    fi

    info "Installing tools: mdadm rsync dosfstools parted"
    run apt-get update -qq
    run apt-get install -y mdadm rsync dosfstools parted initramfs-tools

    local A="$SSD_A" B="$SSD_B"
    local A1="${A}p1" A2="${A}p2" B1="${B}p1" B2="${B}p2"

    info "Partitioning $A and $B identically (512MB FAT boot + rest for RAID)"
    for d in "$A" "$B"; do
        run wipefs -a "$d"
        run parted "$d" --script mklabel gpt
        run parted "$d" --script mkpart primary fat32 1MiB 513MiB
        run parted "$d" --script set 1 boot on
        run parted "$d" --script mkpart primary 513MiB 100%
    done
    run partprobe "$A" || true
    run partprobe "$B" || true
    run udevadm settle || true

    info "Creating the RAID 1 root array across ${A2} + ${B2}"
    # metadata=1.2 is default; --run avoids the interactive 'continue?' prompt
    run bash -c "yes | mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 --metadata=1.2 '$A2' '$B2'"

    info "Formatting: ext4 on the array, FAT32 on each boot partition"
    run mkfs.ext4 -F -L fc-root /dev/md0
    run mkfs.vfat -F 32 "$A1"
    run mkfs.vfat -F 32 "$B1"

    info "Mounting the array and copying the running OS onto it (this takes a while)"
    run mkdir -p /mnt/root
    run mount /dev/md0 /mnt/root
    # -x keeps rsync on the root filesystem; we copy /boot/firmware separately.
    run rsync -aHAXx --info=progress2 \
        --exclude='/mnt/*' --exclude='/media/*' --exclude='/lost+found' \
        --exclude='/var/log/fieldcommand-setup.log' \
        / /mnt/root/

    info "Mounting the first boot partition inside the copied OS at /boot/firmware"
    run mkdir -p "/mnt/root$BOOTDIR"
    run mount "$A1" "/mnt/root$BOOTDIR"
    run cp -a "$BOOTDIR/." "/mnt/root$BOOTDIR/"

    info "Recording the array so it assembles automatically at boot"
    run mkdir -p /mnt/root/etc/mdadm
    if [[ "$DRY_RUN" != "1" ]]; then
        mdadm --detail --scan > /mnt/root/etc/mdadm/mdadm.conf
    fi

    # ── Point the copied OS at the array ────────────────────────────────────
    local A1_PARTUUID
    A1_PARTUUID="$(blkid -s PARTUUID -o value "$A1" 2>/dev/null || echo "")"

    info "Editing cmdline.txt → root=/dev/md0 rootdelay=10"
    if [[ "$DRY_RUN" != "1" ]]; then
        # Replace any root=... token with the array; keep the rest of the line.
        sed -i -E 's#root=[^ ]+#root=/dev/md0#' "/mnt/root$BOOTDIR/cmdline.txt"
        grep -q 'rootdelay=' "/mnt/root$BOOTDIR/cmdline.txt" \
            || sed -i -E 's/$/ rootdelay=10/' "/mnt/root$BOOTDIR/cmdline.txt"
    fi

    info "Editing config.txt → keep PCIe lines, add auto_initramfs=1"
    if [[ "$DRY_RUN" != "1" ]]; then
        local cfg="/mnt/root$BOOTDIR/config.txt"
        grep -qE '^\s*dtparam=pciex1\b'         "$cfg" || echo 'dtparam=pciex1' >> "$cfg"
        grep -qE '^\s*dtparam=pciex1_no_10s=on' "$cfg" || echo 'dtparam=pciex1_no_10s=on' >> "$cfg"
        grep -qE '^\s*auto_initramfs=1'         "$cfg" || echo 'auto_initramfs=1' >> "$cfg"
    fi

    info "Writing the array's /etc/fstab (root=/dev/md0, /boot/firmware nofail)"
    if [[ "$DRY_RUN" != "1" ]]; then
        {
            echo "# Generated by fieldcommand-setup.sh"
            echo "/dev/md0            /              ext4  defaults,noatime  0 1"
            if [[ -n "$A1_PARTUUID" ]]; then
                echo "PARTUUID=$A1_PARTUUID  $BOOTDIR   vfat  defaults,nofail   0 2"
            fi
        } > /mnt/root/etc/fstab
    fi

    info "Rebuilding the initramfs inside the array so it can assemble the RAID"
    run mount --bind /dev  /mnt/root/dev
    run mount --bind /proc /mnt/root/proc
    run mount --bind /sys  /mnt/root/sys
    run mount --bind /run  /mnt/root/run
    run chroot /mnt/root update-initramfs -u -k all
    # After the initramfs is written into boot0, mirror boot0 → boot1 exactly.
    info "Copying the finished boot files onto the second SSD"
    run mkdir -p /mnt/boot1
    run mount "$B1" /mnt/boot1
    run bash -c "cp -a '/mnt/root$BOOTDIR/.' /mnt/boot1/"

    # ── Copy the installer source onto the array for first-boot Phase 2 ──────
    info "Staging the FieldCommand installer on the array ($ARRAY_SRC)"
    run mkdir -p "/mnt/root$ARRAY_SRC"
    run rsync -a --exclude='.git' "$REPO_ROOT/" "/mnt/root$ARRAY_SRC/"
    write_config_file "/mnt/root$ARRAY_SRC/fieldcommand.conf"
    install_firstboot_service   # writes into /mnt/root

    # The migrated system boots from the mirror and finishes via the first-boot
    # installer service — it must NOT also carry the desktop auto-start launcher,
    # or the setup would try to re-run there. Remove it from the array copy.
    run rm -f /mnt/root/etc/xdg/autostart/fieldcommand-setup.desktop

    # ── Unmount everything ──────────────────────────────────────────────────
    info "Unmounting"
    run umount /mnt/boot1 || true
    for m in run sys proc dev "$BOOTDIR"; do run umount "/mnt/root$m" || true; done
    run umount /mnt/root || true

    # ── Set the Pi 5 bootloader to try NVMe first (SD kept as fallback) ──────
    info "Setting the bootloader boot order to NVMe → SD → USB"
    set_boot_order_nvme

    touch "$STATE_DIR/raid_done"
    ok "Mirror built and OS copied."
}

set_boot_order_nvme() {
    # BOOT_ORDER nibbles read right-to-left: 6=NVMe, 1=SD, 4=USB-MSD, f=retry.
    # 0xf416 = try NVMe, then SD, then USB, then loop — SD stays as a safety net.
    if [[ "$DRY_RUN" == "1" ]]; then log "${DIM}[dry-run]${NC} would set BOOT_ORDER=0xf416 via rpi-eeprom-config"; return 0; fi
    if command -v rpi-eeprom-config >/dev/null 2>&1; then
        local tmp; tmp="$(mktemp)"
        rpi-eeprom-config > "$tmp" || true
        if grep -q '^BOOT_ORDER=' "$tmp"; then
            sed -i 's/^BOOT_ORDER=.*/BOOT_ORDER=0xf416/' "$tmp"
        else
            echo 'BOOT_ORDER=0xf416' >> "$tmp"
        fi
        rpi-eeprom-config --apply "$tmp" || warn "Could not apply EEPROM boot order automatically — set it once with: sudo raspi-config → Advanced → Boot Order → NVMe."
        rm -f "$tmp"
    else
        warn "rpi-eeprom-config not found — set NVMe boot order manually: sudo raspi-config → Advanced → Boot Order → NVMe."
    fi
}

# First-boot service (installed INTO the array) that runs install.sh once.
install_firstboot_service() {
    local svc="/mnt/root/etc/systemd/system/fc-firstboot.service"
    if [[ "$DRY_RUN" == "1" ]]; then log "${DIM}[dry-run]${NC} would install $svc (first-boot installer)"; return 0; fi
    cat > "$svc" << UNIT
[Unit]
Description=FieldCommand first-boot installer (runs once from the SSD mirror)
After=network-online.target multi-user.target
Wants=network-online.target
ConditionPathExists=$ARRAY_SRC/scripts/install.sh
ConditionPathExists=!$ARRAY_SRC/.firstboot-done

[Service]
Type=oneshot
# Disable ourselves first so a failure can never boot-loop.
ExecStartPre=/bin/systemctl disable fc-firstboot.service
ExecStart=/usr/bin/env bash $ARRAY_SRC/scripts/install.sh --config $ARRAY_SRC/fieldcommand.conf
ExecStartPost=/usr/bin/touch $ARRAY_SRC/.firstboot-done
StandardOutput=journal+console
StandardError=journal+console
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
UNIT
    # Enable it within the array by creating the wants symlink directly.
    mkdir -p /mnt/root/etc/systemd/system/multi-user.target.wants
    ln -sf ../fc-firstboot.service \
        /mnt/root/etc/systemd/system/multi-user.target.wants/fc-firstboot.service
    ok "Installed first-boot installer service on the array."
}

finish_and_reboot() {
    step "Done building the mirror — rebooting into the SSDs"
    log ""
    log "${GREEN}${BOLD}Phase 1 complete.${NC} The Pi will reboot into the SSD mirror and, on that"
    log "first boot, automatically install and configure FieldCommand IMS."
    log ""
    log "${BOLD}After it finishes you MUST do the pull-a-drive failover test:${NC}"
    log "  1. ${DIM}sudo poweroff${NC} — remove the microSD card AND one SSD — power on."
    log "     → the Pi must boot and FieldCommand must come up on the remaining SSD alone."
    log "  2. Power off, swap which SSD is out, power on — it must boot on the other alone."
    log "  3. Power off, reinsert both, power on, then re-add the drive that was out:"
    log "     ${DIM}sudo mdadm /dev/md0 --add <that drive's p2>${NC}  and watch ${DIM}cat /proc/mdstat${NC}."
    log ""
    log "${AMBER}A mirror you have not tested by pulling a drive is a mirror you cannot rely on.${NC}"
    log ""
    if [[ "$DRY_RUN" == "1" ]]; then info "[dry-run] would reboot into NVMe now."; return 0; fi
    if [[ "$ASSUME_YES" != "1" ]]; then
        read -rp "Reboot into the SSD mirror now? [Y/n]: " a
        [[ "${a:-Y}" =~ ^[Yy] ]] || { info "Not rebooting. Run 'sudo reboot' when ready."; return 0; }
    fi
    run systemctl reboot
}

# =============================================================================
#  MAIN
# =============================================================================
main() {
    gather_config

    # Bring the bootloader to a known-good version (staged; applies at next reboot).
    update_bootloader

    # Stage 0: ensure both SSDs are visible (may reboot once and auto-resume).
    if [[ ! -f "$STATE_DIR/pcie_done" ]] || [[ "$(count_nvme)" -lt 2 ]]; then
        stage0_pcie
    else
        ok "Stage 0 already complete (both SSDs visible)."
    fi

    # If we get here, both drives are visible. Build the mirror.
    pick_disks
    build_mirror
    finish_and_reboot
}

main "$@"
