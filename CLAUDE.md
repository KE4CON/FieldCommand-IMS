# FieldCommand IMS — Project Context

## ⛔ THE ONE RULE (read first)

**Never consider a change "done" until `python scripts/preflight_check.py` passes.**
This project is browser-loaded and never compiled, so syntax errors hide until a page is opened. A duplicated server file and eight page-killing JavaScript syntax errors once shipped to `main` this way. The preflight (and the matching GitHub Action, `.github/workflows/ci.yml`) compile every `.py`, `bash -n` every `.sh`, validate JSON, scan for the duplication signature, and run `node --check` on every HTML `<script>` block.

- Run the preflight after **every** edit session, before handing back.
- **Never let an AI (or a bulk find-replace) rewrite a whole file unreviewed.** The corruption that started all this came from exactly that. Prefer small, anchored edits; diff before saving.
- CI runs on every push. A red check means a real syntax/corruption problem — fix it, don't merge past it.

## Project Identity
Name: **FieldCommand IMS** (Incident Management System)
Author: Jim, KE4CON — for **McHenry County Emergency Services Volunteers (K9ESV)** / MCEMA (RACES / ARES / Starcom)
Language/stack: **Python 3 (standard library only)** backends + **plain HTML/CSS/JS** front end (no framework, no build step)
Platform: **Raspberry Pi 5**, offline-first, self-contained (its own Wi-Fi via an external ASUS router)
License: **AGPLv3** (software) · **CC BY-SA 4.0** (docs)

## Vision & Scope (why this exists)
FieldCommand started as a **communications** app (the legacy "FieldComms" brand — now purged) and grew into a **complete ICS/NIMS all-hazards incident management system**. Its thesis: **communications is inseparable from running an incident.** So it marries comms with the full development and running of the ICS **Incident Action Plan (IAP)**.

- Day to day, an incident uses **public-safety comms** (Starcom).
- In a **total-infrastructure disaster**, that side is likely gone — so the app deliberately puts **amateur radio in front of emergency managers as the backup that survives**, because it may be all that's left.
- **Offline-first:** the full tool set works with **zero internet**. Internet-dependent features (NEXRAD radar, some lookups) light up automatically when a WAN is present.
- Any smartphone/tablet/laptop joins **EMCOMM-NET** Wi-Fi and reaches the whole dashboard at `http://192.168.50.1` — **no app install, no login, any OS.** Multi-user: every operator sees live data.

Two BOMs live in `docs/`: one for **ESV** (the club) and one for **anyone else** who deploys it (e.g., GitHub downloaders).

## Related Programs — Do Not Merge
- **APRS Command** — separate C#/Avalonia desktop APRS client (Jim's). Planned integration: it can replace YAAC as FieldCommand's APRS client/feed (see "Radio direction" below). No shared code; data integration only.
- **IcomRigControl** — separate in-the-moment rig control / QSO logging. FieldCommand does **not** do CAT rig control or contest/award logging.
- Keep FieldCommand the **incident-management + comms picture**, not a rig controller or a logger.

## Architecture (never mix concerns)
Several **small, single-purpose Python `http.server` backends**, one per concern, each a systemd service, fronted by **nginx** on port 80. **SQLite** (`python/db.py`, WAL) is the datastore.

| Service (systemd) | File | Port | Role |
|---|---|---|---|
| `fcc-lookup` | `fcc_lookup_server.py` | 5050 | Core API — FCC callsign lookup, nets/roster, GPS/DMS, hospitals, preflight |
| `health-monitor` | `health_monitor.py` | 5051 | CPU/mem/disk, service states, internet/GPS/WAN/44Net roll-up |
| `ics-platform` | `ics_platform_server.py` | 5055 | ICS/incident platform — incidents, ICS forms, T-cards, IAP, FEMA cost |
| `fieldcommand-refs` | `reference_server.py` | 5056 | Offline reference library (renders PDFs) |
| `fieldcommand-tiles` | `tile_server.py` (Flask) | 8083 | Offline MBTiles map server |
| `deadmans` | `deadmans.py` | — | Dead-man's-switch monitor (net inactivity) |
| `pat` | (Pat Winlink) | 8090 | Winlink over radio |
| gateway Pi (`192.168.50.2`) | `amprgate_*` | 9000/9001 | 44Net/AMPRNet WireGuard gateway (separate host) |

**The ICS API is on port 5055.** `5051` is the health monitor — do not point `/api/ics/*` calls at 5051.

Front end: `html/*.html` (one page per tool), inline `<style>`/`<script>`, **Leaflet** for maps, UI state in **`localStorage`**, shared helpers only in `html/lib/identity.js` and `html/lib/tiles.js`. Theme is 14 CSS custom properties enforced by `python/apply_theme.py`.

Docs: **ReportLab** generators in `docs_generators/` produce the PDFs in `docs/`.

## Coding Standards
- **Python: standard library only** in the runtime servers (the only third-party deps are `flask`/`flask-cors` for the tile server and `reportlab`/`pypdf` for doc/PDF generation — all installed by `scripts/install.sh`). Don't add dependencies without updating the installer's `pip install` line.
- **No front-end framework, no build step.** Plain HTML/JS; deploy by copying files. Keep it that way — it's why this survives in the field.
- Parameterize **all** SQL (`?` placeholders). Never interpolate untrusted values or **column identifiers** into SQL — filter identifiers with `.isidentifier()` (see `_safe_insert_parts` in `ics_platform_server.py`).
- Every state-mutating request path should tolerate malformed input (guard `int()`/`json.loads`).
- **American English** and **plain, layman's language** in all user-facing text and docs (define jargon; hams and EMs won't read a manual).
- `write` state files atomically (temp + `os.replace`) — several services read the same `data/*.json` concurrently.

## Security posture (by design — know the trade-offs)
FieldCommand is deliberately a **no-login, open-LAN** tool ("any device, no login" is a feature). That means:
- The Python APIs have **no auth** and **wildcard CORS**, and bind `0.0.0.0`. Safe **only** because EMCOMM-NET is isolated. Do not expose these ports to an untrusted network.
- If auth is ever added, it must not break the "no login" field UX — discuss before adding.
- Fixed so far: SQL-identifier injection (reference library + archive restore), forgeable `X-Forwarded-For` in the 44Net log, and the committed default Wi-Fi PSK (now a placeholder in `udev/hostapd.conf`).

## Radio direction (planned, not yet done)
- **Graywolf → Direwolf** as the RF TNC. Direwolf is a KISS/AGW TNC only (no HTTP `/api/stations`), so the "serve stations to the tactical map" job moves off Graywolf.
- **YAAC → APRS Command** as the operator's APRS client on a Windows laptop (also runs Winlink). APRS Command connects to Direwolf and can serve the tactical map's station feed. For Pi-standalone resilience, consider a tiny Pi-side KISS→`/api/stations` bridge so the map works without the laptop.

## Known issues / consciously deferred
Real but low-priority; listed so they aren't "rediscovered" as new bugs. See `docs/AUDIT_FINDINGS.md` for the full audit.
- **Concurrency:** the Python servers are single-threaded `HTTPServer`; a slow request (e.g. a cold `/api/health`, RadioReference lookup) blocks other clients. Revisit `ThreadingHTTPServer` if it bites.
- **`health_monitor.get_internet`** mutates the global socket default timeout (`socket.setdefaulttimeout`) — minor.
- **udev:** an FTDI TNC (`0403:6001`) can collide with the GPS rule and not get `/dev/tnc0` — disambiguate by product string if it happens.
- **44Net gateway sudoers** grants `NOPASSWD` `wg-quick`, which can run arbitrary `PostUp` — tighten if the gateway ever leaves a controlled environment.
- **Doc generators** hardcode a sandbox output path (`/mnt/user-data/outputs`) and are copy-pasted (only `manual_*` shares a framework); `docs_generators/ardc_proposal.py` is a 0-byte stub.
- **Manual TOC/numbering drift (known, needs a focused pass):** `manual_build.py`'s hand-maintained `CHAPTERS` list (used only for the printed Table of Contents) is out of sync with the actual chapter bodies from chapter 3 on — titles mislabel real chapters — and several `manual_ch_19_36.py` subsection labels lag the chapter number by 1 (e.g. "Chapter 22 … 21.1"). The chapter *content* renders fine; only the TOC list and subsection labels are stale. Fix by rebuilding the TOC from the real `chapter()` titles (the unused `register_section`/`SECTIONS` machinery in `manual_framework.py` is the intended mechanism) rather than the hand list.
- **observer.html** can get stuck showing an error after a transient API failure (its error handler replaces the elements the refresh loop expects); reloads recover it.
- Duplicate/near-duplicate HTML pages exist (`resmap`/`resource_map`, `incident`/`incident_mgmt`, `wan_settings`/`wan-status`) — canonicalize when convenient.

## What NOT to do
- Do not let an AI rewrite whole files unreviewed, and do not skip the preflight.
- Do not add a front-end framework or a build step.
- Do not add rig control / QSO logging (that's IcomRigControl) or turn this into a non-incident tool.
- Do not add Python runtime dependencies without updating `scripts/install.sh`.
- Do not point ICS UI calls at port 5051 (that's the health monitor; ICS is 5055).

## Reference
Full audit: `docs/AUDIT_FINDINGS.md`. Vision/feature detail: the FieldCommand PDFs in `docs/` (User Manual, Installation Guide, Overview, the two BOMs).
