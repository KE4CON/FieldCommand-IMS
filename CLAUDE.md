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

**Incident data is permanent — save everything.** Every incident is a durable record: **all** data an incident generates (nets, logs, ICS forms, T-cards, IAP, cost, resources, roster snapshots, attachments — *everything*) is saved on the server, **backed up to an external drive (the LaCie)**, and **archived**. Nothing an incident produces is treated as throwaway or session-only. When building or changing any incident feature, the default is *persist it and make sure it lands in the archive/backup path* — never in-memory-only or localStorage-only for incident data. (This is the opposite of the sibling Activation Planner, which is deliberately stateless.)

**Two editions — ESV vs. World.** Every user-facing doc (manual, user guide, install guide, BOM) has, or should have, two variants that differ ONLY by:
- **ESV edition** — keeps org names (McHenry County ESV / K9ESV / MCESV / MCEMA), names the specific gear (**InstyConnect** cellular primary, **Starlink** fallback), and calls the public-safety side **Starcom**. Operator workstations are the **Raspberry Pi 500+** (16 GB, 256 GB NVMe, mechanical keyboard) — matches the ESV BOM.
- **World edition** — strips all org names, drops the InstyConnect/Starlink specifics (say generic "cellular primary / satellite fallback"), and refers to the public-safety side generically as **"public service communications"** (never "Starcom"). Operator workstations stay on the plainer **Raspberry Pi 500** (cheaper baseline) — do **not** bump the World docs to 500+.

(Both editions run the same **servers**: two Raspberry Pi 5 (16 GB) units — the FieldCommand app server and the 44Net gateway. The Pi 500/500+ distinction is only the operator *workstations*.)

Current state — the dual-edition pipeline is mostly built (one source → both editions via edition tokens):
- **Complete Manual: done** — `manual_build.py` emits both from one source. `FieldCommand_Complete_User_Manual_v1.0.pdf` = **World** (generic; org/Starcom/ESV-isms stripped); `FieldCommand_Complete_User_Manual_ESV_v1.0.pdf` = **ESV** (names McHenry County ESV, served agency **MCEMA**, Starcom, ESV member-ID/club-callsign examples). Edition tokens live in `manual_framework._ED_DEFAULTS`; World overrides in `manual_build.MANUAL_EDITIONS`. The one residual "starcom" in the World manual is the literal `starcom.html` **page URL** (a real filename in the code) — fully removing it needs the app page renamed, an app change.
- **BOM: done** — `bom_build.py` emits both (`FieldCommand_BOM.pdf` = ESV, `FieldCommand_BOM_World.pdf` = World).
- **Install guides:** both editions exist (ESV on Pi 500+, World on Pi 500).
- **One-command field-server setup — DONE.** `scripts/fieldcommand-setup.sh` automates the whole build from a single command: it detects both NVMe SSDs behind the Pironman PCIe switch (adds the two `dtparam=pciex1` lines + reboots once if needed), builds the boot-from-RAID-1 mirror and copies the OS (the corrected Section 1B), sets NVMe boot order, then a one-shot `fc-firstboot.service` runs `install.sh --config …` unattended on the first SSD boot. Answers come from prompts OR a `fieldcommand.conf` (sample in `scripts/`); `install.sh` gained a non-interactive/`--config` mode. The disk erase ALWAYS needs an explicit typed `YES` (never auto-confirmed across the PCIe reboot). Has `--dry-run`. Primary delivery = copy the 7 MB repo folder onto the SD `bootfs` partition during imaging (offline, no auth); `scripts/bootstrap.sh` is the public-repo `curl|sudo bash` alternative. **Boot-from-RAID on Pi 5 goes beyond SunFounder's docs — bench-test incl. pull-a-drive before field use.**
- **Callsign is OPTIONAL / amateur features gated — DONE.** Groups with no licensed operators leave the callsign blank; the app then keeps the whole **Amateur Radio** mode grayed out. Gating lives in `index.html` (reads `/api/config` callsign + `active_modules`; only gates once `setup_complete`, so an unconfigured Pi still shows everything). `setup.html` makes callsign optional, blocks enabling any ham module (`amateur/winlink/aprs/44net`) without a callsign, and carries the strong wording that these features legally require a properly licensed operator with privileges on the bands/modes used. `install.sh` no longer forces a `W8ABC` default.
- **User Guide: done** — `gen_user_guide.py` now emits both via an edition `transform()` (applied in the `P()` helper + the canvas draw methods, so it catches paragraph AND canvas text). ESV = `McHenry_County_RACES_ARES_Starcom_FieldCommand_User_Guide.pdf` (McHenry County ESV, served agency MCEMA on the cover, Starcom kept); World = `FieldCommand_RACES_ARES_PublicService_User_Guide.pdf` (generic "your county/organization" placeholders, Starcom → Public Service; only the literal `starcom.html` URL remains).
- Author copyright (James Rospopo KE4CON) intentionally stays in BOTH editions of every doc (authorship / license requirement) — only deploying-org branding differs.

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

## Radio direction
- **Graywolf → Direwolf — DONE (Pi side).** Direwolf is the RF TNC now (KISS :8001 / AGW :8000, no HTTP). `install.sh` apt-installs it, writes a starter `/etc/direwolf.conf`, enables `direwolf.service`; `update.sh`, nginx (the dead `/aprs/` :8080 proxy is gone), `health_monitor`, the `fcc_lookup` preflight, and `preflight.html` all reference `direwolf`; docs regenerated. Because Direwolf has no HTTP, the tactical map + dashboard no longer poll a local APRS server — they read a **configurable RF-source host:port** (Tactical → Settings → APRS Sources), defaulting to `localhost:8080`.
- **YAAC → APRS Command — DONE in code (#16).** APRS Command (separate repo, `C:\Dev\APRS-Command`) now has a **FieldCommand LAN feed** mode: its `MobileCompanionServer` can run tokenless on a fixed port (8080) with wildcard CORS, serving the existing `/api/stations` etc. Start it from APRS Command's **View → "FieldCommand Tactical-Map Feed (LAN)"** menu item (`DesktopRuntime.StartFieldCommandFeed`). FieldCommand's `tactical.html` normalizes APRS Command's JSON (`callsign/lat/lng/comment/symbol/lastHeard/speed(knots)/course`). **Deploy wiring (operator, needs hardware):** (1) in APRS Command, connect its TNC to the Pi's Direwolf (KISS TCP `<pi-ip>:8001` or AGW `:8000`); (2) start the LAN feed menu item; (3) on the tactical map, set Settings → APRS Sources → RF source host = laptop IP, port = 8080. Pi-standalone alternative: a tiny KISS→`/api/stations` bridge on localhost:8080. End-to-end (radio→Direwolf→APRS Command→map) is untested pending hardware.

## Two different maps — do not conflate
FieldCommand has **two** separate map displays with different data sources. They never cross:
- **Tactical APRS Map (`tactical.html`)** — the **amateur / RF** big-screen situational-awareness display (a tablet, laptop, or Pi driving a large monitor to show the tactical picture in the area of interest). Fed by **live APRS off the air**: Direwolf decodes it, APRS Command (or a Pi KISS bridge) serves it, the map polls the configurable RF-source host:port. This is the ONLY map the Direwolf / APRS Command feed touches.
- **Starcom Resource Map (`resmap.html`)** — the **public-service (Starcom)** side. Objects are **hand-entered** on the map by the operator: "+ Add Unit" (with *Pick on Map*), "Draw Zone" (click corners), edit/remove — persisted server-side via `/api/resmap` (port 5050). It is **not** fed by APRS/RF and must never be wired to Direwolf. (`APRS Command mobile companion note`: APRS Command's own `MobileCompanionServer` already serves `/api/stations` etc., but behind a per-session token on a random port — see #16.)

## Known issues / consciously deferred
Real but low-priority; listed so they aren't "rediscovered" as new bugs. See `docs/internal/AUDIT_FINDINGS.md` for the full audit (local/private — `docs/internal/` is gitignored, not published).
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
**Docs layout:** `docs/guides/` (public end-user: install guides, World user manual/guide, quick ref, overview), `docs/hardware/` (BOMs), `docs/beta/` (public beta package), and **`docs/internal/` (gitignored, NOT published)** for org-specific ESV editions, business/financial docs (grant, price, tax), and dev docs (audit, testing runbook, remaining-work). Generators route World/generic output to the public subfolders and ESV/business/dev output to `docs/internal/`.
Full audit: `docs/internal/AUDIT_FINDINGS.md`. Vision/feature detail: the FieldCommand PDFs under `docs/guides/`.

---

## Documentation & Installer Standards

These apply to **every** user-facing document (installation guide, user manual, programming guide, README) and **every** installer / setup script in this repo. Locked house standards.

### Audience & voice
- Assume a **lazy, non-technical reader**: does the least effort, won't read ahead, copy-pastes literally.
- **Plain, simple, layman's language**; short sentences. Detailed but easy to follow.
- **Spell out every step and click**; name the exact button/menu/field label. Say **what the reader will see** after each action.
- **Front-load a short "In a nutshell" / "Quick version" summary** at the top of each document and each chapter, so a skimmer still succeeds.
- **Define every acronym in full on first use** — e.g. "Application Programming Interface (API)" — then use the short form.
- **Never use a placeholder a reader might type literally** (e.g. `SERVER-IP`). Tell them to substitute their real value and give a concrete example.
- **Anticipate common errors** and say exactly what to do about each.
- **Length is not a concern — thoroughness is.** Never trade completeness for brevity.
- **American English spelling** (color, center, meters).

### User manuals — depth standard (the APRS-Command User Manual is the benchmark)
- Roughly **1,500–1,800 words and ~33 content blocks per chapter**.
- **Name every UI element exactly**; **tabulate every field / column / option** with a plain-language "what it means".
- Use sub-sections for variations/edge cases; **end every feature chapter with a Troubleshooting section** (symptom → fix).
- Include dedicated **reference chapters**: Troubleshooting & FAQ, Glossary, Keyboard Shortcuts, Menu/Navigation Reference (and Licenses & Credits where relevant).
- **Ground every step in the real application UI / source** — read the actual screens; never guess a label.

### Installation guides — standard (the OpenTrack Installation Guide is the model)
- Lead with a short **"In a nutshell"** summary of the whole install (download → run → answer prompts → done).
- **Spell out every click**, name exact buttons/menus, and say **what the reader will see** after each step.
- **Automate first:** the primary path is a **one-command setup script** with **interactive prompts** (Enter accepts each default); keep by-hand steps only as a clearly-marked fallback.
- Never use a literal placeholder (e.g. `SERVER-IP`) in a step — tell the reader to use their real value with a concrete example (`http://192.168.1.50:5035`).
- Remove tricks that cause failures (e.g. "drag the folder into the window" instead of typing a path); use the real folder/file names.
- Cover **every operating system** the product supports (e.g. Windows and macOS), each spelled out.
- End with a **Troubleshooting** section (symptom → fix) and a backups / keeping-it-running note where relevant.

### Programming guides — standard (the APRS-Command / OpenTrack Programming Guide is the model)
- A developer / maintainer book that explains **how AND why** the code works — plain enough for a curious non-programmer to follow, deep enough for a maintainer.
- Every section answers **What it does → Why it was built this way → How it works**.
- **Define jargon inline** with a "Jargon, in plain words" callout; open each chapter with a "What This Is / What It Is For" and a one-sentence-version callout; close with "Why It Matters / Design Takeaways" and a **maintainer's rule** callout.
- **Ground every claim in the real source** — read the actual files and quote exact code excerpts; never invent class names, methods, or paths.
- Built on the same per-chapter-JSON pipeline (Markdown is the living source of truth). No screenshots — it is a code book.

### Installers / setup
- **Automate as much as possible**: a **one-command setup script** with **interactive prompts** whose defaults are accepted by pressing **Enter**. The fewer chances to fail installing, the better.

### House doc pipeline
- Navy + gold python-docx house style (`style.py`). **Markdown is the living source of truth**; the styled `.docx` / PDF is generated from **per-chapter JSON** (`chapters/*.json` + a `build.py`) — the same pipeline as the APRS-Command manual and the OpenTrack guides.
- Each project ships three core documents: **Installation Guide, User Manual, Programming Guide.**
