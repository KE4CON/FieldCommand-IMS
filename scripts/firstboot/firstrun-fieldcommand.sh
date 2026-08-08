#!/bin/bash
# ============================================================================
# FieldCommand IMS — first-boot hook  (installs the auto-start launcher)
# ============================================================================
# This runs ONCE, automatically, the first time the Pi boots — triggered by a
# systemd.run= entry that the card-prep step adds to cmdline.txt. It runs early
# and offline, so it does NOT run the installer itself. Its only job is to drop
# a desktop auto-start launcher so the FieldCommand setup opens by itself once
# the desktop is up (where there is a network and a real terminal). Then it
# removes its own trigger so it never runs again.
# ============================================================================
set +e

# Where the FieldCommand-IMS folder was copied on the boot partition.
if [ -d /boot/firmware/FieldCommand-IMS ]; then
    BOOTDIR=/boot/firmware
elif [ -d /boot/FieldCommand-IMS ]; then
    BOOTDIR=/boot
else
    BOOTDIR=/boot/firmware
fi
SRC="$BOOTDIR/FieldCommand-IMS"

# Install a desktop auto-start entry for ALL users (system-wide autostart).
mkdir -p /etc/xdg/autostart
cat > /etc/xdg/autostart/fieldcommand-setup.desktop <<EOF
[Desktop Entry]
Type=Application
Name=FieldCommand Setup
Comment=Set up this FieldCommand field server
Exec=x-terminal-emulator -e bash $SRC/scripts/desktop/fc-autostart.sh
Terminal=false
X-GNOME-Autostart-enabled=true
NoDisplay=false
EOF

# Remove our first-boot trigger so this only ever runs once.
rm -f "$BOOTDIR/firstrun-fieldcommand.sh" 2>/dev/null
CMDLINE="$BOOTDIR/cmdline.txt"
if [ -f "$CMDLINE" ]; then
    sed -i \
        -e 's# systemd.run=[^ ]*firstrun-fieldcommand.sh##g' \
        -e 's# systemd.run_success_action=[^ ]*##g' \
        -e 's# systemd.run_failure_action=[^ ]*##g' \
        -e 's# systemd.unit=kernel-command-line.target##g' \
        "$CMDLINE"
fi

exit 0
