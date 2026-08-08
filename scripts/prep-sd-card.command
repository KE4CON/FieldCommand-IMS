#!/bin/bash
# ============================================================================
# FieldCommand IMS — SD card prep (macOS)
# ============================================================================
# Run this AFTER you flash Raspberry Pi OS (64-bit, Desktop) with Raspberry Pi
# Imager. It makes the card "insert and go":
#   * copies the FieldCommand-IMS folder onto the card's boot partition, and
#   * wires up a one-time first-boot hook so the setup opens by itself when the
#     Pi boots — no command line, no digging through folders on the Pi.
#
# Easiest way to run it: double-click this file in Finder (it opens Terminal
# and runs). If macOS blocks it ("unidentified developer"), right-click it →
# Open → Open. If double-click does nothing, it may need the run permission:
# open Terminal and run:  chmod +x "<path to this file>"  then try again.
#
# It only writes to the removable "bootfs" volume — never your Mac's disk.
# ============================================================================
set -u

say()  { printf '  %s\n' "$1"; }
ok()   { printf '\033[32m[OK]\033[0m  %s\n' "$1"; }
warn() { printf '\033[33m[!]\033[0m   %s\n' "$1"; }
errx() { printf '\033[31m[ERR]\033[0m %s\n' "$1"; }

printf '\n\033[36mFieldCommand IMS — SD card prep (macOS)\033[0m\n'
printf -- '----------------------------------------\n'

# ── Locate the repo root (this script lives in <repo>/scripts) ───────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ ! -f "$REPO_ROOT/scripts/fieldcommand-setup.sh" ]; then
    errx "Can't find the FieldCommand files. Run this from inside the FieldCommand-IMS/scripts folder."
    read -r -p "Press Enter to close… " _; exit 1
fi

# ── Find the card's boot partition under /Volumes ────────────────────────────
candidates=()
for v in /Volumes/*; do
    [ -d "$v" ] || continue
    if [ -f "$v/cmdline.txt" ] && [ -f "$v/config.txt" ]; then
        candidates+=("$v")
    fi
done

if [ "${#candidates[@]}" -eq 0 ]; then
    errx "Couldn't find the Pi boot partition (a volume with cmdline.txt + config.txt)."
    say "Make sure the freshly-imaged card is inserted. It usually mounts as /Volumes/bootfs."
    read -r -p "Press Enter to close… " _; exit 1
fi

boot="${candidates[0]}"
if [ "${#candidates[@]}" -gt 1 ]; then
    warn "More than one boot partition found:"
    i=0; for c in "${candidates[@]}"; do echo "   [$i] $c"; i=$((i+1)); done
    read -r -p "Which one is your FieldCommand card? Enter the number: " sel
    boot="${candidates[$sel]}"
fi

echo ""
warn "This will copy files to and edit the first-boot settings on:  $boot"
read -r -p "Is that the correct card? Type YES to continue: " ans
if [ "$ans" != "YES" ]; then say "Cancelled — nothing changed."; read -r -p "Press Enter to close… " _; exit 0; fi

# ── 1. Copy the FieldCommand-IMS folder onto the card ────────────────────────
dest="$boot/FieldCommand-IMS"
say "Copying FieldCommand-IMS to $dest ..."
rm -rf "$dest"
mkdir -p "$dest"
rsync -a --exclude='.git' "$REPO_ROOT/" "$dest/"
ok "Software copied."

# ── 2. Put the first-boot hook on the boot partition ─────────────────────────
cp "$REPO_ROOT/scripts/firstboot/firstrun-fieldcommand.sh" "$boot/firstrun-fieldcommand.sh"
ok "First-boot hook installed."

# ── 3. Wire the hook into first boot ─────────────────────────────────────────
cmdline="$boot/cmdline.txt"
imager_firstrun="$boot/firstrun.sh"   # created by Imager's own customization

# Back up cmdline.txt once
[ -f "$boot/cmdline.txt.fieldcommand-backup" ] || cp "$cmdline" "$boot/cmdline.txt.fieldcommand-backup"

if [ -f "$imager_firstrun" ]; then
    # Raspberry Pi Imager customization is in use — prepend our autostart-install
    # step into Imager's firstrun.sh so both run.
    if ! grep -q 'fieldcommand-setup.desktop' "$imager_firstrun"; then
        inject="$(cat <<'FCINJ'
# --- FieldCommand: install the setup auto-start launcher (added by prep) ---
mkdir -p /etc/xdg/autostart
cat > /etc/xdg/autostart/fieldcommand-setup.desktop <<'FCDESK'
[Desktop Entry]
Type=Application
Name=FieldCommand Setup
Exec=x-terminal-emulator -e bash /boot/firmware/FieldCommand-IMS/scripts/desktop/fc-autostart.sh
Terminal=false
X-GNOME-Autostart-enabled=true
FCDESK
# --- end FieldCommand ---
FCINJ
)"
        tmp="$(mktemp)"
        { head -n 1 "$imager_firstrun"; printf '%s\n' "$inject"; tail -n +2 "$imager_firstrun"; } > "$tmp"
        cp "$tmp" "$imager_firstrun"; rm -f "$tmp"
        ok "Hooked into Raspberry Pi Imager's first-boot setup (coexisting)."
    else
        ok "Imager first-boot already carries the FieldCommand step."
    fi
else
    # No Imager customization — add our own systemd.run trigger to cmdline.txt.
    if ! grep -q 'firstrun-fieldcommand.sh' "$cmdline"; then
        content="$(tr -d '\r\n' < "$cmdline")"
        printf '%s%s\n' "$content" ' systemd.run=/boot/firmware/firstrun-fieldcommand.sh systemd.run_success_action=reboot systemd.run_failure_action=none systemd.unit=kernel-command-line.target' > "$cmdline"
        ok "First-boot trigger added to cmdline.txt."
    else
        ok "First-boot trigger already present in cmdline.txt."
    fi
fi

echo ""
ok "Card is ready. Eject it, put it in the Pi 5 (with both SSDs installed), and power on."
say "The FieldCommand setup will open by itself. Just answer the questions and type YES to confirm."
echo ""
# Best-effort eject so it's safe to pull
diskutil eject "$boot" >/dev/null 2>&1 && say "Card ejected — safe to remove." || true
read -r -p "Press Enter to close… " _
