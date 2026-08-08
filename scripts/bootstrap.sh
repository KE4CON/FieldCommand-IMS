#!/usr/bin/env bash
# ============================================================================
# FieldCommand IMS — bootstrap
# ============================================================================
# Downloads FieldCommand IMS onto a freshly-imaged Raspberry Pi and launches
# the one-command field-server setup. This is the CONVENIENCE method — it needs
# internet on the Pi and a PUBLIC repo. The offline / no-typing method is to
# copy the FieldCommand-IMS folder onto the SD card boot partition instead
# (see the Install Guide).
#
# Usage (on the Pi, after first boot):
#   curl -fsSL https://raw.githubusercontent.com/KE4CON/FieldCommand-IMS/main/scripts/bootstrap.sh | sudo bash
#
# Pass setup options through after a --, e.g. a dry run:
#   curl -fsSL .../bootstrap.sh | sudo bash -s -- --dry-run
# ============================================================================
set -euo pipefail

REPO_URL="https://github.com/KE4CON/FieldCommand-IMS.git"
DEST="/opt/fieldcommand-installer"
BRANCH="main"

if [[ $EUID -ne 0 ]]; then
    echo "Run as root:  curl -fsSL <url> | sudo bash" >&2
    exit 1
fi

echo "==> Installing git (if needed)…"
if ! command -v git >/dev/null 2>&1; then
    apt-get update -qq
    apt-get install -y git
fi

if [[ -d "$DEST/.git" ]]; then
    echo "==> Updating existing copy in $DEST…"
    git -C "$DEST" fetch --depth 1 origin "$BRANCH"
    git -C "$DEST" reset --hard "origin/$BRANCH"
else
    echo "==> Cloning FieldCommand IMS to $DEST…"
    rm -rf "$DEST"
    git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$DEST"
fi

echo "==> Launching field-server setup…"
exec bash "$DEST/scripts/fieldcommand-setup.sh" "$@"
