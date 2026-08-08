#!/usr/bin/env bash
# ============================================================================
# FieldCommand IMS — auto-start launcher (runs at desktop login)
# ============================================================================
# Installed by the first-boot hook into /etc/xdg/autostart. It opens the
# FieldCommand setup automatically so the operator never touches the command
# line. It is safe to run at every login:
#   * If the system is already running from the SSD mirror (setup finished, or
#     we've migrated), it removes itself and exits — no window, no re-run.
#   * Otherwise it launches the setup. The setup itself reboots the SD system
#     a couple of times during the build; this launcher simply re-opens it
#     after each of those reboots until the mirror is built — so the operator
#     just answers the questions and confirms the wipe once.
# ============================================================================
set -u

# Already on the RAID/NVMe root? Setup is done — clean up and go away quietly.
ROOTSRC="$(findmnt -n -o SOURCE / 2>/dev/null || echo '')"
case "$ROOTSRC" in
    /dev/md*|/dev/nvme*)
        rm -f /etc/xdg/autostart/fieldcommand-setup.desktop 2>/dev/null \
            || sudo -n rm -f /etc/xdg/autostart/fieldcommand-setup.desktop 2>/dev/null || true
        exit 0
        ;;
esac

# Locate the setup wrapper and run it (it self-elevates for the privileged work).
for base in /boot/firmware/FieldCommand-IMS /boot/FieldCommand-IMS /opt/fieldcommand-installer; do
    if [ -f "$base/scripts/desktop/fc-run.sh" ]; then
        exec bash "$base/scripts/desktop/fc-run.sh"
    fi
done

echo "FieldCommand setup files not found on the boot partition."
read -rp "Press Enter to close… " _
