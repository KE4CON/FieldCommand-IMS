# FieldCommand IMS — Full Source-Code Audit Findings

**Date:** 2026-08-07
**Scope:** every source file in the repository (135 text/source files) — all Python, all HTML/JS, all shell/systemd/udev, all doc generators.
**Method:** (1) deterministic pass — `py_compile` on every `.py`, `bash -n` on every `.sh`, JSON validation, and a whole-file duplication/corruption scan; (2) deep line-by-line semantic review by seven parallel readers; (3) every **Critical** item re-verified by hand against the exact source line.

## How to read this

Each finding is `path:line — Severity — defect — failure scenario`. Severities:

- **Critical** — a whole page or service is non-functional.
- **High** — a major feature on an otherwise-working page/service is broken.
- **Medium** — wrong behavior in specific cases.
- **Low** — edge cases, latent risks, cosmetics.

## Root cause

The overwhelming majority of the Critical/High defects are **mechanical editing scars** — the same fingerprint as the duplicated `ics_platform_server.py`: escaped backticks (`` \` ``) pasted into template strings, a stray `────────` box-drawing line dropped into code, doubled keywords (`async async`), `<script src>` tags with an inline body glued on, `await` in a non-`async` function, live code stranded *after* `</html>`, a double comma. **None of these could survive a compiler.** They are cheap to fix individually; the risk was never architectural.

## The single most important prevention

Add a **CI gate** (or a pre-commit hook) that, on every change, runs `python -m compileall` on all `.py`, `bash -n` on all `.sh`, and a lightweight JS/HTML syntax check (e.g. `node --check` on extracted `<script>` blocks, or a headless page-load smoke test). This one gate would have caught essentially every Critical finding below before it ever landed.

---

# 🔴 Critical

## Page-killing JavaScript syntax errors (whole page dead)
A single syntax error aborts the entire inline `<script>`, so **every** handler on the page becomes undefined.

| File | Line | Defect |
|---|---|---|
| `html/index.html` | 1459 | A bare `────────` box-drawing line sits as code between two functions → the entire dashboard script (clock, health poll, weather, APRS table, `setMode`) never runs. **This is the main landing page.** |
| `html/setup.html` | 494–531 | Orphaned `try{ … await … }` whose owning `async function` header was deleted, plus an unmatched extra `}` at 531 → the first-run setup wizard script fails to parse (`saveConfig`, `loadConfig`, `selectVariant`, `toggleModule` all undefined). |
| `html/ics-form.html` | 2710–2742 | `tr.innerHTML = \`…\`` uses literal backslash-escaped backticks and `\${…}` → the whole form engine script (283–9437) fails to parse; page stuck on "Loading form…". |
| `html/netcontrol.html` | 588 | `async async function promoteToRoster(...)` (doubled `async`) → whole Net Control script aborts; `loadNets()` never runs. |
| `html/netcontrol.html` | 616/620 | `await fetch(...)` inside `function removeEntry(...)` (non-`async`) → independently kills the same script block. |
| `html/starcom.html` | 618–627, 651–654 | Escaped backticks/placeholders (`` \` ``, `\${`) inside template literals → whole Starcom Net Control script fails to parse. |
| `html/printcenter.html` | 389 | A literal `</script>` sits inside a `w.document.write(\`…\`)` template string → the browser ends the inline script early, leaving the template literal unterminated; Preview/Generate/Print/Clear all throw, and trailing code renders as visible garbage. Fix: `<\/script>`. |
| `html/position_checklists.html` | 1492 | `id:'GIS',, abbr:'GIS'` — double comma → the `POSITIONS` array and whole script fail to parse; sidebar empty. |

## Dead features via `<script src>` + inline body
When a `<script>` tag has `src`, its inline body is **ignored** — so glued-on code never runs.

| File | Line | Defect |
|---|---|---|
| `html/repeaters.html` | 1054 | `<script src="/lib/identity.js">` with an inline body (1055–1230) → `updateMapBtn`, `openMapModal`, `addRepToChannelLibrary` never defined; `showData()` throws → the repeater table never renders on any load path. |
| `html/tactical.html` | 1435 | Same pattern (body 1436–1523) → the entire repeater-overlay feature is dead; the "📡 Repeaters" button throws `ReferenceError` on every click. |

## Other Critical
| File | Line | Defect |
|---|---|---|
| `html/wan-status.html` | 407 (+529) | `.then(d => …)` handler reads `data.config` instead of `d.config` → throws → `.catch()` always fires → page **permanently shows "Cannot reach FieldCommand health API"** even when healthy. Compounded by `let _wanConfig = null;` stranded *after* `</html>` (line 529, inert). |
| `python/ics_platform_server.py` | 1623 | **File is duplicated** (two full copies, ~3083 lines) and **fails to parse** (`serve_forever()import json`). The ICS platform API (port 5055) cannot start. |
| `python/ics_platform_server.py` | 709–1420 | A large block of **write endpoints is pasted inside `do_GET`** but references `body`/`now` which exist only in `do_POST`. Result: the **entire data-entry half of the ICS platform cannot save** — T-card personnel, PAR accountability, FEMA labor/equipment/materials, remote check-in save/checkout/sync, general-info save, template create/import, channel-library save, resource GPS, incident archive/restore/delete/reset. (`do_POST` only implements incidents, forms, tcards, resources, meetings.) A GET to these paths → `NameError` 500; a POST → 404. |
| `scripts/install.sh` | 135 (also 152,170,175) | `$DIM` is used but never defined; under `set -u` this aborts the installer at the config screen in every profile. |
| `scripts/install.sh` | 13 vs `udev/nginx-fieldcommand.conf:13` | Web-root mismatch: install deploys HTML to `/var/www/html`; nginx serves `/opt/fieldcommand/html` (never populated on a clean install) → `http://<ip>/` returns 404. |
| `scripts/install.sh` | 267,280–284,317,356,393,399,633,761 | ~half the `$SCRIPT_DIR/...` references omit `../` and point into a non-existent `scripts/<subdir>/` → html/, python service files, systemd units, nginx config, udev rules, pat.service, yaac.service all silently skipped (or a hard exit at 280). |
| `scripts/install.sh` | 419 (also 532, 385) | `cp` into `/opt/fieldcommand/scripts/`, which the `dirs` array never creates → under `set -e` the installer aborts. |

---

# 🟠 High

## Python
| File | Line | Defect |
|---|---|---|
| `python/ics_platform_server.py` | 1624–1632 | `HAS_PDF`/`compile_iap`/`IAP_FORM_ORDER` are defined at module top level **after** the `__main__` block whose `serve_forever()` blocks forever → when run as main, `HAS_PDF` is never assigned → `/api/ics/iap_status` and `/api/ics/iap_compile` throw `NameError: HAS_PDF`. |
| `python/fcc_lookup_server.py` | 561 | `POST /api/hospitals` branches on `if hid:` but `hid` is never assigned → any hospital add/edit → `NameError` 500. |
| `python/fcc_lookup_server.py` | 944 | `_preflight_check()` runs `SELECT COUNT(*) FROM channels`, but the table is `channel_library` → `GET /api/preflight` → `OperationalError: no such table: channels` 500. The whole readiness page fails. |
| `python/reference_server.py` | 277–278 | **SQL injection** in `do_PUT`: `sets=",".join(f"{k}=?" …)` interpolates raw JSON object keys into `UPDATE ref_documents SET {k}=?`. Unauthenticated, bound to the LAN. |
| `python/reference_server.py` | 213, 260, 285 | **Unauthenticated** file **upload / metadata overwrite / hard-delete** (incl. `p.unlink`) bound to `0.0.0.0:5056` with `Access-Control-Allow-Origin: *` → arbitrary remote file write/delete on the Pi. |
| `python/manual_build.py` | 120 | Duplicate chapter number: line 117 and line 120 are both `(34, …)` → two "34" rows in the TOC. |
| `python/manual_build.py` | 127 | `CHAPTER_FUNCS` = `ch1…ch34, ch_appendix, ch_appendix` → **ch35 (JS8Call) never rendered**, **ch36 (Planning-P) missing**, appendix printed **twice**, TOC/body mismatch. |

## HTML/JS
| File | Line | Defect |
|---|---|---|
| `html/ics-form.html` | 603 (+~16 more) | `markDirty()` called ~17× but never defined → signatures, 204 rows, 230 meetings, channel select, 211 pulls all throw. |
| `html/ics-form.html` | 6987 | T-card modal fields emit only `data-key=` (no `id=`), but `saveTCard219`/`addTCardFromNIMS` read `getElementById('tc_name').value` → Save T-Card / Add from NIMS throw null-property errors. |
| `html/ics-form.html` | 8487 | `pull211Remote` calls `FORMS['211']._ciRow(i)`, which is never defined → "Pull Remote Check-Ins" throws. |
| `html/incident.html` | 419 | `renderWorkspace()` uses `incId`/`period` which aren't in scope (function has `inc`,`curPeriod`) → workspace fails to render when the ICS API is up. |
| `html/incident.html` | 402 | "✏ Edit" calls `editIncident(...)`, defined nowhere → ReferenceError. |
| `html/index.html` | 1473 | `setMode()` toggles class `visible`, but CSS reveals panels via `.active` → switching modes shows nothing (a second, independent defect from line 1459). |
| `html/ics/operations.html` | 707 | `ICS_API` used in `loadPersonnel`/`addPersonnel`/`removePersonnel` but only declared function-local in two other functions → Personnel tab shows "Error: ICS_API is not defined". |
| `html/ics/operations.html` | 756 | `addPersonnel` sets `incident_id: incId` — `incId` never exists → throws before the fetch. |
| `html/ics/operations.html` | 736 | `renderPersonnel` calls `esc(...)`, not defined here (the shared `esc` is private inside `identity.js`) → personnel list can't render. |
| `html/wan-status.html` | 529 | `let _wanConfig = null;` declared *after* `</html>` → inert; reads in `setHero`/`load` would throw even after the 407 fix. |
| `html/wan-status.html` | 462 | `getElementById('sl-badge')` targets an element that doesn't exist (only `cell-badge` exists) → `TypeError` once the page runs. |
| `html/grid.html` | 392 vs 406 | `canvas.addEventListener(...)` runs at line 392, but `const canvas` isn't declared until 406 (temporal dead zone) → ReferenceError aborts the rest of the script; map never draws, clicks/resizes do nothing. |

## Shell / systemd
| File | Line | Defect |
|---|---|---|
| `scripts/install.sh` | 327 vs 910 | `fieldcommand-refs.service` is copied and **started** but never **enabled** → the Reference Library API (5056) does not survive a reboot. |
| `scripts/install.sh` | 870, 883 | Runs `ics_pdf_downloader.py` and `apply_theme.py` from `$FC_HOME/python/`, but neither is in the `PY_FILES` copy list (251–264) → both invocations fail. (`update.sh` *does* include them, confirming they're required.) |
| `scripts/update.sh` | 13 | Option 7 rsyncs web files to `/opt/fieldcommand/html` (matches nginx) — contradicts install.sh's `/var/www/html`; the two scripts disagree about the web root. |

---

# 🟡 Medium

| File | Line | Defect |
|---|---|---|
| `python/ics_platform_server.py` | 391, 397 | `/api/ics/incidents/archived` and `/incidents/lacie` are shadowed by the generic `startswith("/api/ics/incidents/")` at 97 → always 404; the archived-incident list never works. |
| `python/ics_platform_server.py` | 1018–1056 | Incident **restore** builds dynamic SQL from JSON object keys (`cols=",".join(inc.keys())`) → identifier injection / `no such column` from a corrupt or malicious USB archive; no per-row try/except for incidents/forms loops. (Latent — endpoint currently unreachable.) |
| `python/ics_platform_server.py` | 168,209,260,364,681,692 | Unvalidated `int(qs.get(...))` → `ValueError` 500 on non-numeric `period`/`limit`. Same pattern in `fcc_lookup_server.py`. |
| `python/reference_server.py` | 106–108, 264 | `do_PUT` calls `read_json()` (no try/except) → a malformed PUT body → uncaught 500. |
| `python/deadmans.py` | 39–40 | `dms_state.json` written non-atomically (`write_text`) while `health_monitor` reads it every ~10 s → a mid-write read gets truncated JSON and silently falls back to "disarmed" — the dashboard can show the dead-man's switch as disarmed while it's actually triggered. (Siblings `wan_monitor`/`amprgate_poll` use the correct tmp+`replace()` pattern.) |
| `python/deadmans.py` | 86–87 | A net-entry timestamp without `Z`/offset yields a naive datetime; subtracting from an aware `datetime.now(timezone.utc)` → `TypeError`, swallowed by the outer print-only try → **the dead-man's switch silently stops advancing to "triggered"** (safety-relevant). |
| `python/health_monitor.py` | 239–264 | `collect_health` shells out sequentially (13× `systemctl is-active` @3 s + 0.5 s GPS + 4 s HTTP) on a single-threaded server → a cold-cache `/api/health` can appear to hang for tens of seconds. |
| `python/amprgate_status.py` | 357–362 | Trusts client-supplied `X-Forwarded-For` (no reverse proxy in front) → the Part-97 station-ID access log can be written with a forged IP. |
| `python/gen_operator_cards.py` | 33–37 | Hard `import reportlab` at module top; **reportlab is not in the installer's `pip install`** (`flask flask-cors requests gpsd-py3`) → `ModuleNotFoundError`. |
| `python/iap_pdf.py` | 181, 198 | `render_ics202` does `d.get('objectives','').split('\n')` / `textwrap.wrap(safety,100)`; `.get(k,'')` returns `None` for a present-but-null key → crash, swallowed → the **entire ICS-202 is silently dropped** from the compiled IAP. (ICS-204 guards this; 202 doesn't.) |
| `python/overview_build.py` / `overview_build_v2.py` | 557 / 151 | Both write the same `IncidentManagement_Overview.pdf` → whichever runs second overwrites the other. |
| `html/ics/operations.html` | 341 | `syncTCardTo204`/`sync204ToTCards` hardcode `ICS_API='...:5051'` while the rest of the file uses `:5055` — an in-file contradiction (5051 is the health monitor). |
| `html/index.html` | 1075 | `updateClock()` reads `currentMode` (only an implicit global set later in `setMode`) → ReferenceError on the first tick (parse-time). |
| `html/ics/planningp.html` | 423 | Loads `/lib/identity.js` (absolute) while siblings use `../lib/identity.js` → 404 unless the doc root is exactly `html/`. |
| `html/checkin.html` | 398 | `e.name.replace(/'/g,"\'")` — in a double-quoted string `"\'"` is just `'` (a no-op) → names with apostrophes (O'Brien) break the `checkOut(...)` onclick. |
| `html/accountability.html` | 468,469,524,563,564 | `esc()` doesn't escape `'`, but its output is injected into single-quoted onclick args → apostrophe names break Location / Check-Out buttons (a personnel-accountability tool). |
| `html/resources.html` | 577 | Misplaced paren in the CSV column-mapping `<option>` builder → when a field is NOT auto-detected, the option renders malformed (no `>`, no label, no `</option>`), corrupting the select. |
| `html/netcontrol.html` / `starcom.html` | 192 | `oninput="updateICS211Link()"` but `updateICS211Link` is defined nowhere → ReferenceError while typing the Incident ID. |
| `html/tactical.html` | 756 | `normalizeGW` passes camelCase `r.symbolTable/symbolCode` to `stationTypeFromSymbol`, but GW records are snake_case → all Graywolf stations misclassify as MOBILE (the type filter breaks). |
| `html/resource_map.html` | 403 | `allTCards.find(c => c.id === cardId)` — strict `===` against a string arg; if DB ids are numeric, `42==='42'` is false → clicking any resource silently does nothing. Same unguarded pattern in `fema_costs.html` (646/710/768). |
| `scripts/install.sh` (udev) | `99-fieldcommand-gps.rules` / `-tnc.rules` | FTDI `0403:6001` matched by three overlapping rules with no product filter → an FTDI TNC gets `/dev/gps_ftdi`+`/dev/tnc_ftdi` and never `/dev/tnc0` (contradicts the installer's promise). |
| `udev/hostapd.conf` | 15 (+ install.sh:116) | Committed default Wi-Fi PSK `fieldcommand2026`. (Note: install.sh's `AP_PASS` is prompted/echoed but never written anywhere — hostapd/dnsmasq aren't installed; the ASUS router handles Wi-Fi.) |
| `scripts/setup_44net.sh` | 491 | `amprgate ALL=(ALL) NOPASSWD: /usr/bin/wg, /usr/bin/wg-quick` — `wg-quick up <path>` runs arbitrary `PostUp` shell from any config file → a compromise of the network-facing Flask app (9000/9001) becomes full root. |
| `scripts/install.sh` | 110 | Longitude default drops the sign: prompt shows `[-88.4473]` but defaults to `88.4473` (positive) → accepting the default places the station in the eastern hemisphere. |

---

# ⚪ Low

| File | Line | Defect |
|---|---|---|
| `html/ics-form.html` | 9794 | Document unterminated — ends at `</script>` with no `</body></html>` (browsers auto-close; still invalid). |
| `html/ics214.html` | 367 | `JSON.parse(last)` on restore has no try/catch (siblings use `||'[]'`) → a corrupt `fc_ics214_last` aborts init. |
| `html/iap.html` | 411 | `exportIAP()` calls `printWin.document.write(...)` with no null check → a popup blocker → uncaught `TypeError`, no feedback. |
| `html/general_info.html` | 582 | `calcSunrise()` guard `if(!lat||!lon)` rejects a valid coordinate of exactly `0`. |
| `html/hospitals.html` | 394–395 (676–677) | `parseFloat(...) || null` collapses a legitimate `0` coordinate to null. |
| `html/ics/finance.html` | 82 | Nav bar omits the Planning-P link present on the other six `ics/` pages. |
| `html/ics/finance.html` | 307 | `statusColor` key `'returned / closed'` never matches the value `returned` → those rows always fall back to muted color. |
| `html/ics/operations.html` | 713 | `fetch(\`${API}/api/roster\`)` with `API=…:5055/api/ics` → double `/api` (`.../api/ics/api/roster`) → roster autocomplete never loads. |
| `html/winlink-import.html` | 354 | Fetches incidents from `:5055/api/ics/incidents`, unlike every sibling page (`:5050/api/incidents`) — endpoint inconsistency. |
| `html/repeaters.html` | 1146 | Popup button calls `addRepToChannelLib(...)`; function is `addRepToChannelLibrary` (typo; moot while 1054 kills the block). |
| `html/deadmans.html` | 388 | `resetPoll()` starts a new 1 s `setInterval` each call but only clears `pollTimer` → interval leak on every "Save Defaults". |
| `html/observer.html` | 141–143 | The "Cannot reach API" error sets `innerHTML` but never `display`, so on a `display:none` picker the error is invisible. |
| `python/health_monitor.py` | 168 | `socket.setdefaulttimeout(3)` mutates the process-global default and is never reset. |
| `python/wan_monitor.py` | 302–303 | `src_list[0]["id"]` → `KeyError` if a configured WAN source omits `id` (kills that poll cycle). |
| `python/tile_server.py` / `reference_server.py` | 56 / 23 | `logging.FileHandler('/var/log/…')` opened at import with no guard → module raises on import if `/var/log` isn't writable. |
| `python/iap_pdf.py` | 325 | `is_placeholder = rid.endswith('+')` — dead (unused) and a latent crash if `rid` isn't a string (caught → form dropped). |
| `python/fetch_repeaters.py` | 203/212, 106–107 | Rate-limit sleep skipped on consecutive failures; a single bad coordinate aborts a whole state/band batch. |
| `python/build_fcc_db.py` | 27–28 | `ZeroDivisionError` in the progress callback when the server sends no Content-Length (`total=0`). |
| `python/deadmans.py` | 110–131 | `DmsHandler` HTTP class defined but never bound to a socket — dead code. |
| `python/reference_server.py` | 62, 224 | Upload is silently truncated (not rejected) at the size cap, and a full 200 MB upload is buffered entirely in RAM (heavy for a Pi). |
| `python/gen_operator_cards.py` | 63 | Leftover dev-sandbox logo path `/home/claude/esv-logo.png` (guarded, harmless). |
| `python/amprgate_status.py` | 118–129 | Auth degrades to "any well-formed callsign" when the FCC DB is unreachable (intentional fallback — flag the risk). |
| `docs_generators/*.py` | — | All hardcode `/mnt/user-data/outputs/…` (build-host paths that don't exist on a clean checkout); `gen_esv_install_guide.py:3` has a copy-pasted wrong docstring; `overview_build.py:128` has a latent invalid-color (dead) helper. |
| `docs_generators/ardc_proposal.py` | — | 0-byte stub — produces no proposal. |
| `systemd/fieldcommand-backup@.service` | 8 | Backs up `fieldcommand.db`, but the installer only builds `fcc.db`; if the app hasn't created `fieldcommand.db`, the `sqlite3 .backup` step fails. |
| `scripts/update.sh` | 125 | "Backup" writes to `/tmp`, which is cleared on reboot. |
| `systemd/fieldcomms-*` , `udev/99-fieldcomms-*`, `*.old` | — | Half-finished `fieldcommand`→`fieldcomms` rename; dormant (nothing installs them) but would all fail if used. Brand drift + duplication. |

---

# Verified NOT bugs (so they aren't re-reported)

- **JS bracket-balance flags** in `channel_library`, `checkin`, `deadmans`, `fema_costs`, `grid`, `hospitals`, `iap_compile`, `resources`, `setup`(*), `tactical`, `wan_settings`, `lib/identity.js` were **false positives** from a crude scanner tripping on template literals / regexes — **except** `setup.html` (a real orphan-`try` error, listed above) and `printcenter`/`repeaters` (real `</script>`/`src`-body errors, listed above).
- **7 of 8** doubled-`<!DOCTYPE>` HTML files (`iap`, `ics/planningp`, `meetings`, `netcontrol`, `printcenter`, `roster`, `starcom`) are legitimate print/export templates in JS strings — **not** duplication. Only `ics-form.html` (missing closing tags) was real.
- `iap_pdf.py` `IAP_FORM_ORDER` types without a `RENDERERS` entry correctly fall through to `render_generic` — no KeyError.
- `db.py._alter_existing_tables()` creates the accountability/GPS/archive/barcode columns, so the endpoints reading them do **not** crash on "missing column".
- nginx `proxy_pass` ports all match their service units.
- Subprocess calls (`ping`, `systemctl`, `wg`, `pdftoppm`) use list-args with timeouts — no command injection.

---

# Open question that needs your input — the ICS API port

The pages disagree with the server about which port serves the ICS API. **`ics_platform_server.py` binds `5055`**; **`5051` is the health monitor**. Yet the root `html/*.html` pages hardcode **`:5051`** for `/api/ics/*`, the `html/ics/*` subfolder uses **`:5055`**, and `operations.html` uses both. As written, the root pages would hit the health monitor and 404. This is systemic and can't be resolved from code alone — **which port does the ICS API actually run on in your deployment?** The answer decides whether this is a few fixes or a sweep.
