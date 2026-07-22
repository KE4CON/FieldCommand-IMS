# FieldCommand IMS

**Full ICS/NIMS all-hazards incident management that works when everything else fails.**

FieldCommand IMS is a complete offline incident management platform built on a Raspberry Pi. It runs its own Wi-Fi network, requires no internet connection, and provides the full suite of ICS/NIMS tools accessible from any browser on the network — including every form needed to build a complete Incident Action Plan.

> *The cell towers are down, the internet is gone, and you're running on a generator in a parking lot. That's exactly when you need incident management software most — and that's exactly when everything else fails.*

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
