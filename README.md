# FieldCommand IMS

**Full ICS/NIMS all-hazards incident management that works when everything else fails.**

FieldCommand IMS is a complete offline incident management platform built on a Raspberry Pi. It runs its own Wi-Fi network, requires no internet connection, and provides a full suite of ICS/NIMS tools accessible from any browser on the network.

> *The cell towers are down, the internet is gone, and you're running on a generator in a parking lot. That's exactly when you need incident management software most — and that's exactly when everything else fails.*

## What it does

- **Complete ICS/NIMS all-hazards incident management** — full IAP form set (ICS-201 through ICS-221), FEMA / USCG / NWCG form variants selectable per form
- **Amateur radio EMCOMM** — net logging with FCC callsign validation, APRS tactical map, Winlink integration
- **Public safety communications** — Starcom net logging with EMA ID lookup, ICS-309 communications log
- **Tactical operations** — Leaflet.js offline map, resource tracking, facilities management
- **Offline-first** — runs on EMCOMM-NET Wi-Fi (192.168.50.1), no internet required, full functionality on battery or generator power
- **44Net / AMPRNet gateway** — optional internet-connected node for AMPRNet reachability

## Hardware

- Raspberry Pi 5 16GB + Pironman MAX 5 (dual NVMe RAID 1)
- ASUS RT-BE58 Go Wi-Fi 7 router (primary + 2× AiMesh nodes)
- UniFi Switch Lite 16 PoE
- InstyConnect Drum (5G cellular WAN) + Starlink (satellite failover)
- Yaesu FTM-510DR + Icom IC-7300MK2 + SCS PXdragon DR-9400 PACTOR modem

## License

- Software: GNU Affero General Public License v3.0 (AGPLv3) — see [LICENSE](LICENSE)
- Documentation: Creative Commons Attribution-ShareAlike 4.0 (CC BY-SA 4.0) — see [LICENSE-DOCS](LICENSE-DOCS)

## Author

Copyright (C) 2026 James Rospopo KE4CON  
Developed for McHenry County Emergency Services Volunteers (K9ESV)  
https://github.com/KE4CON/FieldCommand-IMS
