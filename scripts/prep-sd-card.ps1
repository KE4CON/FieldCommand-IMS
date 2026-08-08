# ============================================================================
# FieldCommand IMS - SD card prep (Windows)
# ============================================================================
# Run this AFTER you flash Raspberry Pi OS (64-bit, Desktop) with Raspberry Pi
# Imager. It turns the card into an "insert and go" FieldCommand card:
#   * copies the FieldCommand-IMS folder onto the card's boot partition, and
#   * wires up a one-time first-boot hook so the setup opens by itself when the
#     Pi boots (no command line, no file-manager digging).
#
# You do not need to type anything on the Pi afterward except the answers to a
# few questions and typing YES to confirm erasing the two SSDs.
#
# Easiest way to run it: double-click  prep-sd-card.bat  (it calls this file).
# It only writes to the small removable "bootfs" drive - never your PC's disks.
#
# NOTE: this file is intentionally ASCII-only so Windows PowerShell 5.1 reads
# it correctly regardless of the system code page. Do not add accented or
# box-drawing characters.
# ============================================================================
$ErrorActionPreference = 'Stop'

function Write-Info($m){ Write-Host "  $m" }
function Write-OK($m){ Write-Host "[OK]  $m" -ForegroundColor Green }
function Write-Warn2($m){ Write-Host "[!]   $m" -ForegroundColor Yellow }
function Write-Err2($m){ Write-Host "[ERR] $m" -ForegroundColor Red }

Write-Host ""
Write-Host "FieldCommand IMS - SD card prep" -ForegroundColor Cyan
Write-Host "-------------------------------"

# Locate the repo root (this script lives in <repo>\scripts)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot  = Split-Path -Parent $ScriptDir
if (-not (Test-Path (Join-Path $RepoRoot 'scripts\fieldcommand-setup.sh'))) {
    Write-Err2 "Can't find the FieldCommand files. Run this from inside the FieldCommand-IMS\scripts folder."
    Read-Host "Press Enter to close"; exit 1
}

# Find the card's boot partition (the FAT drive that has cmdline.txt + config.txt)
$candidates = @()
foreach ($d in (Get-PSDrive -PSProvider FileSystem)) {
    $root = $d.Root
    if ((Test-Path (Join-Path $root 'cmdline.txt')) -and (Test-Path (Join-Path $root 'config.txt'))) {
        $candidates += $root
    }
}

if ($candidates.Count -eq 0) {
    Write-Err2 "Couldn't find the Pi boot partition (a drive with cmdline.txt + config.txt)."
    Write-Info "Make sure the freshly-imaged card is inserted. On Windows it appears as a drive named 'bootfs'."
    Read-Host "Press Enter to close"; exit 1
}

$boot = $candidates[0]
if ($candidates.Count -gt 1) {
    Write-Warn2 "More than one boot partition found:"
    for ($i=0; $i -lt $candidates.Count; $i++){ Write-Host "   [$i] $($candidates[$i])" }
    $sel = Read-Host "Which one is your FieldCommand card? Enter the number"
    $boot = $candidates[[int]$sel]
}

Write-Host ""
Write-Warn2 "This will copy files to and edit the first-boot settings on:  $boot"
$ans = Read-Host "Is that the correct card? Type YES to continue"
if ($ans -ne 'YES') { Write-Info "Cancelled - nothing changed."; Read-Host "Press Enter to close"; exit 0 }

# 1. Copy the FieldCommand-IMS folder onto the card
$dest = Join-Path $boot 'FieldCommand-IMS'
Write-Info "Copying FieldCommand-IMS to $dest ..."
if (Test-Path $dest) { Remove-Item -Recurse -Force $dest }
New-Item -ItemType Directory -Path $dest | Out-Null
Get-ChildItem -Path $RepoRoot -Force | Where-Object { $_.Name -ne '.git' } | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $dest -Recurse -Force
}
Write-OK "Software copied."

# 2. Put the first-boot hook on the boot partition (write with LF endings)
$hookSrc = Join-Path $RepoRoot 'scripts\firstboot\firstrun-fieldcommand.sh'
$hookDst = Join-Path $boot 'firstrun-fieldcommand.sh'
$hookText = (Get-Content -Raw $hookSrc) -replace "`r`n","`n"
[System.IO.File]::WriteAllText($hookDst, $hookText, (New-Object System.Text.UTF8Encoding($false)))
Write-OK "First-boot hook installed."

# 3. Wire the hook into first boot
$cmdlinePath = Join-Path $boot 'cmdline.txt'
$imagerFirstrun = Join-Path $boot 'firstrun.sh'   # created by Imager's own customization

$backup = Join-Path $boot 'cmdline.txt.fieldcommand-backup'
if (-not (Test-Path $backup)) { Copy-Item $cmdlinePath $backup }

if (Test-Path $imagerFirstrun) {
    # Raspberry Pi Imager customization is in use. Prepend our autostart-install
    # step into Imager's firstrun.sh so both run.
    $fr = (Get-Content -Raw $imagerFirstrun) -replace "`r`n","`n"
    if ($fr -notmatch 'fieldcommand-setup\.desktop') {
        $nl = "`n"
        $inject = "# --- FieldCommand: install the setup auto-start launcher (added by prep-sd-card) ---" + $nl
        $inject += "mkdir -p /etc/xdg/autostart" + $nl
        $inject += "cat > /etc/xdg/autostart/fieldcommand-setup.desktop <<'FCDESK'" + $nl
        $inject += "[Desktop Entry]" + $nl
        $inject += "Type=Application" + $nl
        $inject += "Name=FieldCommand Setup" + $nl
        $inject += "Exec=x-terminal-emulator -e bash /boot/firmware/FieldCommand-IMS/scripts/desktop/fc-autostart.sh" + $nl
        $inject += "Terminal=false" + $nl
        $inject += "X-GNOME-Autostart-enabled=true" + $nl
        $inject += "FCDESK" + $nl
        $inject += "# --- end FieldCommand ---" + $nl
        $parts = $fr -split "`n", 2
        $fr = $parts[0] + $nl + $inject + $parts[1]
        [System.IO.File]::WriteAllText($imagerFirstrun, $fr, (New-Object System.Text.UTF8Encoding($false)))
        Write-OK "Hooked into Raspberry Pi Imager's first-boot setup (coexisting)."
    } else {
        Write-OK "Imager first-boot already carries the FieldCommand step."
    }
} else {
    # No Imager customization - add our own systemd.run trigger to cmdline.txt.
    $cmd = (Get-Content -Raw $cmdlinePath) -replace "`r","" -replace "`n",""
    if ($cmd -notmatch 'firstrun-fieldcommand\.sh') {
        $cmd = $cmd.TrimEnd() + ' systemd.run=/boot/firmware/firstrun-fieldcommand.sh systemd.run_success_action=reboot systemd.run_failure_action=none systemd.unit=kernel-command-line.target'
        [System.IO.File]::WriteAllText($cmdlinePath, $cmd + "`n", (New-Object System.Text.UTF8Encoding($false)))
        Write-OK "First-boot trigger added to cmdline.txt."
    } else {
        Write-OK "First-boot trigger already present in cmdline.txt."
    }
}

Write-Host ""
Write-OK "Card is ready. Safely eject it, put it in the Pi 5 (with both SSDs installed), and power on."
Write-Info "The FieldCommand setup will open by itself. Just answer the questions and type YES to confirm."
Write-Host ""
Read-Host "Press Enter to close"
