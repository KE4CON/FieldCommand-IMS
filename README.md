# FieldCommand IMS

**Full ICS/NIMS all-hazards incident management that works when everything else fails.**

FieldCommand IMS is a complete offline incident management platform built on a Raspberry Pi. It runs its own Wi-Fi network, requires no internet connection, and provides the full suite of ICS/NIMS tools accessible from any browser on the network — including every form needed to build a complete Incident Action Plan.

> *The cell towers are down, the internet is gone, and you're running on a generator in a parking lot. That's exactly when you need incident management software most — and that's exactly when everything else fails.*

---

## Get Started

New here? This is the whole path from nothing to a running field server.

**1. Get the hardware.** At minimum, a **Raspberry Pi 5 (16 GB)** with a **Pironman 5 MAX** carrying **two NVMe SSDs** (mirrored for reliability), a microSD card for the initial flash, and a monitor + keyboard. The full recommended kit — router, switch, radios, cases — is in [Hardware](#hardware) below and priced out in the Bill of Materials PDFs in [`docs/`](docs/).

> ⚠️ **Install BOTH NVMe SSDs in the Pironman before you start.** The setup builds a RAID 1 mirror across the two drives and will stop if it finds only one. Seat both SSDs and the SunFounder FFC ribbon cable firmly.

**2. Get the software.** Download this repository — click **Code → Download ZIP** on GitHub, or clone it:
```bash
git clone https://github.com/KE4CON/FieldCommand-IMS.git
```
It's about 7 MB. Everything you need is inside.

> 📁 **A GitHub ZIP unzips to a folder named `FieldCommand-IMS-main`.** The prep tool in Step 4 handles that name automatically. (Only if you skip the prep tool and copy the folder onto the card by hand do you need to rename it to `FieldCommand-IMS`.)

**3. Flash Raspberry Pi OS.** With the [Raspberry Pi Imager](https://www.raspberrypi.com/software/), flash **Raspberry Pi OS (64-bit, Desktop)** to the microSD card. Set the username to `fieldcommand` in the Imager's advanced options.

> 💾 **About `bootfs`:** flashing creates two partitions on the SD card — **`bootfs`** (a small FAT boot partition, which shows up as a drive on your computer) and `rootfs` (the large Linux partition, which Windows/Mac can't read). You interact with **`bootfs`**; once the card is in the Pi it's mounted at `/boot/firmware`. **On Windows**, if a "You need to format the disk" popup appears, that's it seeing the `rootfs` it can't read — click **Cancel**, do *not* format.

**4. Make the card "insert-and-go" (one double-click on your computer).** After imaging, a small drive named **`bootfs`** appears on your computer. Open the downloaded `FieldCommand-IMS` folder, go into **`scripts`**, and double-click the prep tool for your computer:
> - **Windows:** `prep-sd-card.bat`
> - **Mac:** `prep-sd-card.command` *(if macOS blocks it the first time, right-click it → Open → Open)*
>
> It copies the software onto the card and sets it to run the setup automatically on first boot. That's the only "computer" step — no command line, no editing files by hand.

> *Prefer to do it by hand instead of the prep tool? Just copy the whole `FieldCommand-IMS` folder onto the `bootfs` drive. You'll then start the setup on the Pi from the desktop icon (File Manager → `FieldCommand-IMS` → `scripts` → `desktop` → double-click "1. Preview" then "2. Install"), or from a terminal with `bash /boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh`.*

**5. Insert and go.** Put the card in the Pi 5 (**both SSDs installed**), connect a monitor and keyboard, and power on. The FieldCommand setup **opens by itself**. Answer a few short questions on screen, and type **`YES`** once to confirm erasing the two SSDs. From there it's hands-off — it builds the mirrored RAID 1 storage, copies the OS, reboots, and installs and configures FieldCommand automatically.

**6. Open it.** When it finishes, from any device on the FieldCommand Wi-Fi network, browse to **http://192.168.50.1/**.

> **Do you need an amateur radio callsign?** No. If your group has no licensed amateur radio operators, **leave the callsign blank** during setup — the incident-management and public-safety features all work fully, and the amateur radio tools simply stay grayed out. Enter a callsign only if you have a properly licensed operator with privileges on the bands and modes you intend to use. You can add one later at any time.

📖 **Full details, wiring, and the manual partitioning fallback:** [`docs/guides/FieldCommand_Installation_Guide.pdf`](docs/guides/FieldCommand_Installation_Guide.pdf) and the [Complete User Manual](docs/guides/FieldCommand_Complete_User_Manual_v1.0.pdf).

---

## Vision & Scope

FieldCommand IMS is a **complete ICS/NIMS all-hazards incident management system** — not just an EMCOMM tool. It is designed to manage the full lifecycle of any incident from initial response through demobilization, using standard ICS forms and workflows, while adding a native amateur radio and public safety communications capability that no other ICS platform provides.

It is the offline-first, field-deployable alternative to cloud-dependent platforms like WebEOC, E-Team, and NIMSIAP — all of which fail when infrastructure goes down. FieldCommand IMS is designed specifically for the moment when everything else fails.

**Comparable to:** WebEOC · E-Team · NIMSIAP · NIMS Logic · E-iSuite  
**Unique advantages:** Fully offline · Pi-deployable · Native EMCOMM · Open source · Free forever

---

## What it does — Complete Feature Set

### ICS / NIMS All-Hazards Incident Management
- **Organization setup wizard** — agency name, callsign, logo, default form variant (FEMA/USCG/NWCG)
- **Incident setup** — name, type, location, operational period, agency, form variant override
- **Full IAP form set** — every ICS form needed to build a complete Incident Action Plan:
  - ICS-201 Incident Briefing
  - ICS-202 Incident Objectives
  - ICS-203 Organization Assignment List
  - ICS-204 Assignment List (FEMA + NWCG variants)
  - ICS-205 Radio Communications Plan
  - ICS-205A Communications List
  - ICS-206 Medical Plan
  - ICS-207 Incident Organization Chart
  - ICS-208 Safety Message/Plan
  - ICS-209 Incident Status Summary
  - ICS-210 Resource Status Change
  - ICS-211 Check-In List (covered by net loggers)
  - ICS-213 General Message ✓ Built
  - ICS-213RR Resource Request Message
  - ICS-214 Activity Log ✓ Built
  - ICS-215 Operational Planning Worksheet (Fire + Non-Fire)
  - ICS-215A IAP Safety Analysis
  - ICS-219 Resource Status Cards (T-Cards)
  - ICS-220 Air Operations Summary
  - ICS-221 Demobilization Check-Out
  - ICS-309 Communications Log ✓ Built (via net logger export)
- **Form variant selection** — FEMA / USCG / NWCG selectable per form at time of use; mix and match on same incident
- **Logo support** — agency/IMT logo on all printed forms and IAP documents
- **IAP assembly** — combine all completed forms into single printable PDF with cover page
- **Weather auto-population** — sunrise/sunset/timezone/NWS data from incident location
- **Operational period tracking** — all forms tied to operational period
- **ICS section navigation** — Command · Operations · Planning · Logistics · Finance/Admin · Communications

### Amateur Radio EMCOMM
- Amateur net logger with FCC callsign validation and EMA ID lookup ✓ Built
- Net open/close timestamps, per-entry checkout, duration tracking ✓ Built
- APRS tactical map (Leaflet.js, offline tiles) ✓ Built
- Winlink/PAT integration ✓ Built
- 44Net/AMPRNet gateway node (192.168.50.2) ✓ Built

### Public Safety Communications
- Starcom net logger with Radio ID auth and EMA ID lookup ✓ Built
- ICS-309 Communications Log export with Duration and EMA ID columns ✓ Built
- Drill/exercise mode with watermark ✓ Built

### Tactical Operations
- Offline tactical map with APRS overlay ✓ Built
- Resource tracking and facilities management ✓ Built
- Planning-P workflow ✓ Partial
- NWS NEXRAD animated radar (WAN-dependent) ✓ Built
- HF propagation tool ✓ Built

### Infrastructure
- Offline-first — full functionality with no internet
- Runs on EMCOMM-NET Wi-Fi (SSID: EMCOMM-NET, IP: 192.168.50.1)
- WAN monitoring — cellular (InstyConnect) + satellite (Starlink) failover ✓ Built
- AMPRNet/44Net status monitoring ✓ Built
- Dead man's switch ✓ Built
- Automated backup to USB drive ✓ Built
- FCC ULS database (offline callsign lookup) ✓ Built

### Future / Horizon
- WordPress plugin — Starcom + amateur net logger for mchenryesv.org
- AI node — dedicated Pi 5 at 192.168.50.4, Ollama, offline inference
- Resource import — from InciNet, E-iSuite, IROC

---

## Hardware

| Component | Spec |
|---|---|
| FieldCommand Server | Raspberry Pi 5 16GB + Pironman MAX 5 (dual 1TB NVMe RAID 1) |
| 44Net Gateway | Raspberry Pi 5 16GB + Argon NEO 5 |
| Primary Router | ASUS RT-BE58 Go Wi-Fi 7 + 2× AiMesh nodes |
| Switch | UniFi Switch Lite 16 PoE |
| Cellular WAN | InstyConnect Drum (T-Mobile + Verizon 5G) |
| Satellite WAN | Starlink Standard Gen 3 |
| Workstations | 4× Raspberry Pi 500+ Desktop Kit + 4× Pi Monitor 15.6" |
| HF Radio | Icom IC-7300MK2 + SCS PXdragon DR-9400-BTWF PACTOR modem |
| VHF/UHF Radio | Yaesu FTM-510DR + Comet CA-2X4SRNMO + Digirig + Mobilinkd TNC4 |
| Field Antenna | Chameleon MPAS 2.0 + CHA URT1 remote tuner |
| Transport | 6× Harbor Freight Apache 4800 XL (IP65) |

---

## Network Architecture

```
192.168.50.1  — FieldCommand Pi (primary server, all web services)
192.168.50.2  — 44Net Gateway Pi (AMPRNet/44Net, amateur net logger)
192.168.50.4  — AI Node Pi (future — Ollama inference)
192.168.50.254 — ASUS RT-BE58 Go (primary router)
44.x.x.x/29  — AMPRNet allocation (pending portal.ampr.org)
```

---

## License

- **Software:** GNU Affero General Public License v3.0 (AGPLv3) — see [LICENSE](LICENSE)
- **Documentation:** Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) — see [LICENSE-DOCS](LICENSE-DOCS)

## Author

Copyright (C) 2026 James Rospopo KE4CON  
Developed for McHenry County Emergency Services Volunteers (K9ESV)  
https://github.com/KE4CON/FieldCommand-IMS
