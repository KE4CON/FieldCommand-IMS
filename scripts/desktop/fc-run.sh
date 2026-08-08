#!/usr/bin/env bash
# Wrapper used by the desktop launcher icons. Finds the setup script wherever
# the FieldCommand-IMS folder was copied (Bookworm /boot/firmware or older
# /boot), runs it with whatever arguments the icon passed, and keeps the
# terminal window open at the end so you can read the result.
set -u

for base in /boot/firmware/FieldCommand-IMS /boot/FieldCommand-IMS \
            /opt/fieldcommand-installer; do
    if [[ -f "$base/scripts/fieldcommand-setup.sh" ]]; then
        SETUP="$base/scripts/fieldcommand-setup.sh"
        break
    fi
done

if [[ -z "${SETUP:-}" ]]; then
    echo "Could not find fieldcommand-setup.sh. Is the FieldCommand-IMS folder on the SD card's boot drive?"
else
    bash "$SETUP" "$@"
fi

echo
read -rp "Press Enter to close this window… " _
