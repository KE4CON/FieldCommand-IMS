#!/usr/bin/env bash
# ============================================================================
# FieldCommand IMS — reset the two SSDs  (FOR TESTING / RE-RUNS)
# ============================================================================
# Wipes the RAID mirror and all partitions off both NVMe SSDs so you can run
# the setup again from scratch. Use this when re-testing the installer.
#
#   sudo bash fc-reset-drives.sh            # wipe (asks you to type YES)
#   sudo bash fc-reset-drives.sh --dry-run  # show what it would do, change nothing
#
# IMPORTANT: run this from the microSD card boot — NOT from the SSD system you
# are wiping (you cannot erase the disk you are running on). If your Pi now
# boots the SSDs first, boot back to the SD first:
#   sudo rpi-eeprom-config --edit   # set  BOOT_ORDER=0xf461  (SD first), save, reboot
# ============================================================================
set -euo pipefail

DRY_RUN=0
FORCE=0
for a in "$@"; do
    case "$a" in
        --dry-run) DRY_RUN=1 ;;
        --force)   FORCE=1 ;;
        -h|--help) grep -E '^#( |$)' "$0" | sed -E 's/^# ?//'; exit 0 ;;
    esac
done

if [[ -t 1 ]]; then
    RED=$'\033[0;31m'; GREEN=$'\033[0;32m'; AMBER=$'\033[0;33m'; CYAN=$'\033[0;36m'; BOLD=$'\033[1m'; NC=$'\033[0m'
else RED=""; GREEN=""; AMBER=""; CYAN=""; BOLD=""; NC=""; fi

info(){ echo -e "${CYAN}[INFO]${NC} $*"; }
ok(){   echo -e "${GREEN}[OK]${NC}   $*"; }
warn(){ echo -e "${AMBER}[!]${NC}   $*"; }
die(){  echo -e "${RED}[ERR]${NC}  $*" >&2; exit 1; }
run(){ if [[ "$DRY_RUN" == 1 ]]; then echo -e "  [dry-run] $*"; else echo -e "  \$ $*"; "$@"; fi; }

# Self-elevate
if [[ $EUID -ne 0 ]]; then exec sudo -- bash "$(readlink -f "$0")" "$@"; fi

# Safety: never wipe the disk we are running from.
ROOTSRC="$(findmnt -n -o SOURCE / || true)"
case "$ROOTSRC" in
    /dev/md*|/dev/nvme*)
        [[ "$FORCE" == 1 ]] || die "This system is running from $ROOTSRC — you can't wipe the drive you're booted from. Boot from the microSD card first (see the note at the top of this script)."
        ;;
esac

mapfile -t DISKS < <(lsblk -dn -o NAME | grep '^nvme' | sed 's,^,/dev/,')
[[ "${#DISKS[@]}" -gt 0 ]] || die "No NVMe drives found."

echo ""
warn "The following drives will be COMPLETELY ERASED (RAID + all partitions):"
lsblk -o NAME,SIZE,MODEL,SERIAL "${DISKS[@]}"
echo ""
if [[ "$DRY_RUN" != 1 ]]; then
    read -rp "Type ${BOLD}YES${NC} to erase them: " reply
    [[ "$reply" == "YES" ]] || die "Not confirmed. Nothing changed."
fi

# Stop any assembled arrays
for md in /dev/md*; do
    [[ -b "$md" ]] || continue
    info "Stopping array $md"
    run mdadm --stop "$md" || true
done

for d in "${DISKS[@]}"; do
    info "Wiping $d"
    # Clear RAID superblocks on any member partitions
    for p in "${d}"p*; do
        [[ -b "$p" ]] || continue
        run mdadm --zero-superblock "$p" || true
    done
    # Clear filesystem/partition signatures and the GPT (primary + backup)
    run wipefs -a "$d" || true
    if command -v sgdisk >/dev/null 2>&1; then
        run sgdisk --zap-all "$d" || true
    else
        # Zero the first 20 MB and the last 20 MB (GPT backup lives at the end)
        run dd if=/dev/zero of="$d" bs=1M count=20 conv=fsync || true
        SZ=$(blockdev --getsz "$d" 2>/dev/null || echo 0)
        if [[ "$SZ" -gt 40960 ]]; then
            run dd if=/dev/zero of="$d" bs=512 seek=$((SZ-40960)) count=40960 conv=fsync || true
        fi
    fi
done

# Clear the setup's saved state so a re-run starts clean
run rm -rf /var/lib/fieldcommand-setup

run partprobe || true
echo ""
ok "Both SSDs are wiped and setup state is cleared."
info "You can now run the FieldCommand setup again for a fresh install."
