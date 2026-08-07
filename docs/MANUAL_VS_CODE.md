# FieldCommand IMS — Manual vs. Code Reconciliation

**Date:** 2026-08-07
**Method:** The Complete User Manual's authoritative content (its generator source `docs_generators/manual_ch_*.py`, cross-checked against the extracted PDF text) was verified chapter-by-chapter against the actual page + server code by four independent readers.
**Scope note:** the app has two backends — **`fcc_lookup_server.py` (port 5050)** = main API (config, roster, nets, FCC, hospitals, repeaters, resource types, DMS, preflight); **`ics_platform_server.py` (port 5055)** = ICS platform (incidents, forms, T-cards, IAP, FEMA cost, templates, archive). Several manual/code mismatches trace to confusion between these two.

## How to use this
Findings are sorted into three buckets:
- **🔴 Bucket 1 — Code bugs / broken behavior.** The code is genuinely wrong (dead endpoints, data silently not saved). **Fix the code.** These are the priority.
- **🟠 Bucket 2 — Documented features not built.** The manual promises a capability the code doesn't have. **Decide per item: build it, or remove the promise from the manual.**
- **🟡 Bucket 3 — Manual overstates / mislabels.** The code is fine; the manual's wording is wrong (wrong data source, wrong port, wrong page URL, wrong button label). **Fix the manual.**

The recurring theme: the manual was written to an intended design; the code often implemented it differently or partially. So for Buckets 2 & 3 the decision is *code-to-match-manual* vs *manual-to-match-code*.

---

# 🔴 Bucket 1 — Code bugs (fix the code)

> **STATUS 2026-08-07: ALL FIXED (B1–B11).** Verified via preflight. Plus the ICS-309 export
> was reworked on `netcontrol.html` + `starcom.html` to (a) show Frequency/Mode, (b) download a
> saved file, and (c) actually carry the **message traffic** (a Communications Log), with the
> station check-in list kept as a secondary table. Open follow-up (needs Jim's decision):
> **T-card auto-populate from ICS-211 sign-in** — see note at the bottom of this file.

| # | Where | Bug | Impact |
|---|---|---|---|
| B1 | `callsign.html` (Ch 11) | The dedicated lookup page calls `GET :5050/fcc/<CALL>` and Advanced Search calls `:5050/fcc/search`, but the server only has `/api/fcc?call=` and `/api/fcc/status`. Both hit the 404 branch. Field names also differ (`license_class`/`grid_square`/`frn` vs server's `license_status`/`operator_class`). | **HIGH** — the entire dedicated callsign-lookup page + advanced search return "not found" for every callsign. (Net Control's inline lookup uses the correct URL and works.) |
| B2 | `deadmans.html` (Ch 12) | `renderNets()` iterates `dmsState.nets` as an object, but `GET :5050/api/dms` returns a single global row with `armed_nets` as a **list** and no `nets` object → grid always shows "No active nets." `armNet()` posts `{net_id, threshold}` but the server reads `nets`/`threshold_min` → arming never populates `armed_nets`. | **HIGH** — the Dead Man's Switch UI cannot arm/monitor per-net as shown. (The server-side `dms_monitor` on 5050 does still track `last_activity`.) |
| B3 | `fema_costs.html` (Ch 18) | Incident dropdown calls `GET :5050/api/incidents`, which doesn't exist (incidents live on 5055 `/api/ics/incidents`). Empty catch, no fallback. | **HIGH** — can't select an incident on the FEMA cost page except via a `localStorage` value set elsewhere. |
| B4 | `resources.html` (Ch 16) | Calls `:5050/resources` for load/save, but the server route is `/api/resources`. Sync fails silently → localStorage-only. | **MEDIUM** — the flat Resource Board never syncs to the server. |
| B5 | `roster.html` (Ch 4) | Certifications & Equipment use HTML keys like `"ICS-100"`/`"HF"`, but server columns are `ics100`/`hf`; Roles are sent as `roles[]` but the server stores a single `role`. | **MEDIUM (data loss)** — operators fill in certs/equipment/roles and they don't save. |
| B6 | `roster.html` (Ch 4) | CSV re-import assigns a **new random id to every row** and upserts on `id` only, so re-importing the same CSV **duplicates** members instead of updating them. Manual says "existing IDs updated." | **MEDIUM** — roster fills with duplicates on re-import. |
| B7 | `netcontrol.html` (Ch 7) | `logTraffic()` posts `to`/`type`/`note`, but the server's `net_traffic` columns are `to_call`/`text` → those fields are silently dropped. | **MEDIUM (data loss)** — traffic-log destination/notes not saved. |
| B8 | `scan_checkin.html` (Ch 10/11) | `/api/barcode_lookup` searches only the roster table, never `fcc.db`. Manual says a scanned **callsign** fills the name from FCC. | **MEDIUM** — scanning a non-roster callsign yields no FCC name. |
| B9 | `incident.html` (Ch 5) | "Operational Period Duration" (`period_hours`) is collected but never persisted; server hard-codes period 1. | **MEDIUM** — chosen OP duration is lost. |
| B10 | `event_templates.html` / server `do_DELETE` (Ch 6) | No `is_builtin` guard — built-in templates **can** be deleted (set `enabled=0`), despite the manual's "built-in templates cannot be deleted." | **LOW-MED** — built-ins can be removed accidentally. |
| B11 | `ics/operations.html` server (Ch 16) | T-card save writes neither `daily_cost` nor an operational-period column, though the manual documents both as T-card fields. | **MEDIUM** — documented T-card cost/OP data has nowhere to go. |

---

# 🟠 Bucket 2 — Documented features not built (build, or drop from manual)

**Setup & incidents**
- **Setup (Ch 3):** 5 of 8 documented fields don't exist — **grid square (Maidenhead), default incident name, Wi-Fi SSID, server address, time zone.** (Setup uses decimal lat/lon and a hardcoded server URL.)
- **Incident (Ch 5):** no **incident number** field; **IC is free text**, not a roster picker.
- **Net logger (Ch 7):** no **mode dropdown** (SSB/FM/Digital/Other), no **open date/time** entry, no **live elapsed timer**, no **Enter-key** check-in.

**ICS forms & Winlink**
- **ICS-213 (Ch 22):** no **outbound "Send via Winlink"/export**; no **"Reply Requested" checkbox**; no **callsign→FCC auto-fill** on the From field. (Only inbound Winlink import exists.)
- **ICS-214 (Ch 23):** no **"Export to FEMA Labor"** button; no **"resources involved"** entry field.
- **Signatures (Ch 17/22/23):** signature capture exists in the main ICS form engine (`ics-form.html`) but **not on the standalone `ics213.html`/`ics214.html` pages**, despite the "platform-wide signatures" claim. (Stylus **pressure** is not implemented anywhere — mouse/touch only.)

**Maps, radar, accountability, repeaters**
- **Radar (Ch 25):** no **NEXRAD station selector**; offline mode shows a banner instead of the promised **last-frame cache + 30-second WAN re-poll**.
- **Tactical map (Ch 13):** **SARTopo GeoJSON overlay is not wired into `tactical.html`** (the standalone `sartopo_import.html` page exists but nothing renders its overlay on the tactical map).
- **Accountability (Ch 21):** no **"Check All Out"** mass-checkout control (per-row only).
- **Repeaters (Ch 31):** the entire **"+ Add Repeater" manual-entry workflow is missing** (page only ingests CSV/JSON/server/demo); the **"Map View" button is unreachable** (map is fully coded but no toolbar control launches it).
- **NTS (Ch 30):** the **25-word maximum is not enforced** (count shown, never capped).
- **AMPRNet (Ch 28):** status page doesn't show the promised **connected-peers list** or **access-log** display.
- **Facilities (Ch 33):** no server sync (localStorage only) so no ICS-205/T-card linkage; no **"supply depot"** facility type.
- **Hospitals (Ch 33):** single phone field (manual promises switchboard **+ emergency-department** numbers).

---

# 🟡 Bucket 3 — Manual overstates / mislabels (fix the manual)

**Wrong data source**
- Radar (Ch 25) is **RadrView / IEM WMS**, not "NWS RIDGE II."
- HF Propagation (Ch 26) is **HamQSL (N0NBH)**, not "SWPC/NOAA."
- Both "shows last data when offline" claims are false (they show N/A / a model estimate).

**Wrong port / page / count**
- **Appendix A.2 port table:** lists ICS platform on **5051** — it's **5055**; and omits **5056** (reference library). Also `/api/hospitals`, `/api/repeaters`, `/api/resource_types` are on **5050**, not 5055.
- **Ch 16 points to `resources.html`** for the Operations T-card board — the real board is **`ics/operations.html`**.
- **Ch 23** says ICS-309 is auto-generated on `ics309.html` "select the net to reference" — the auto-from-net-log ICS-309 actually lives on **`netcontrol.html`**; `ics309.html` is manual-entry.
- FEMA (Ch 19): "**44** built-in rates" — the seed has **45**.

**Wrong label / behavior wording**
- Mode names (Ch 2): "All-Hazards ICS / Amateur EMCOMM / Public Safety" → actual "Amateur Radio / Starcom / ICS".
- WAN status is a **card in each mode**, not a **top status bar** (Ch 2).
- Incident types (Ch 5): "**six** types" → a **~32-option** dropdown (named six mostly don't match; "Mass Gathering" absent).
- Net logger buttons (Ch 7): "Open Net"/"Check In" → **"Create Net"/"LOG ENTRY"**; ICS-309 "Export/download" → opens a **print** window; the ICS-309 output **omits frequency/mode**.
- Templates (Ch 6): the six built-in **names differ**; the edit modal is **sections, not four tabs**; "taken directly to the new incident" → shows success **links** (no auto-nav).
- QR codes (Ch 4): online path uses the **deprecated Google Charts API** (may not render).
- IAP variant (Ch 17): "full/command/logistics" → actual **FEMA/USCG/NWCG**.
- Cost projection (Ch 20): uses **fixed horizons** (12/24/72 hr, 7 d), not "daily burn × remaining op periods."
- Radar (Ch 25): speed is **Slow/Med/Fast** (not 0.5×/1×/2×/4×); palettes **Default/Dark/NOAA** (not Standard/Dual-pol/Enhanced).
- Print Center (Ch 34.5): claims **CUPS/remote** printing; actually **local browser** print.
- Channel Library (Ch 32): "agency assignment" field is actually **"Division / Group."**
- Cheat Sheets (Ch 34.2): "NIMS resource typing" is a **separate page** (`resource_types.html`), not a cheat-sheet tab.
- AMPRNet (Ch 28): endpoint is **`amprgw.ampr.org:51820`**, not "connect.44net.cloud."
- Observer (Ch 9): header does **not** show frequency/mode/elapsed time.
- FCC lookup (Ch 11): "results as you type" → fires on **Enter/button**; "updated quarterly" vs page's "weekly."
- "Offline, no CDN dependency" (Ch 13, others): **Leaflet and some tiles/QR load from CDNs** and won't work without a WAN — a real gap between the offline-first promise and several pages.

---

## Recommended order of attack
1. **Bucket 1 (B1–B11)** — real bugs; fix regardless of manual. B1/B2/B3 (dead callsign page, dead-man's-switch arming, FEMA-costs incident picker) are the loudest.
2. **The two systemic manual errors** — the appendix **port table (5051→5055, add 5056)** and the **Ch 16 page URL (`resources.html`→`ics/operations.html`)** — these mislead readers about the whole system.
3. **Decide the "offline vs CDN" policy** (Ch 13) — either vendor Leaflet/tiles locally to honor the offline-first promise, or soften the claim.
4. **Bucket 2** — per feature, choose build-vs-descope, ideally aligning both manuals afterward.
5. Regenerate the manuals once the wording decisions are made.

---

## T-card auto-populate from ICS-211 — BUILT 2026-08-07

`checkin.html` promises *"Your check-in goes to the ICS-211 roster **and T-card board** at the ICP."*
This is now implemented (needs on-Pi testing — nothing is deployed yet):
- **Server:** `POST /api/ics/checkin` now also creates/refreshes a T-card in `ics_tcards`, keyed
  `tc-ci-<checkin_id>` so a re-check-in updates rather than duplicates, and any board movement
  (status/assignment) already made is preserved. New cards start in **Available**.
- **Board (`ics/operations.html`):** now loads its cards from **`/api/ics/tcards`** (the same store it
  writes drags/personnel to) instead of `/api/ics/resources`, with a translation layer between the
  server card shape and the board's status/type keys. So a 211 sign-in shows up on the board.
- **"Add Resource"** on the board was **localStorage-only** — it now also POSTs to `/api/ics/tcards`,
  so manually-added resources persist server-side and across devices (per the CLAUDE.md
  "incident data is permanent" rule).

**Historical note (for the record):** the T-card board previously had *three* disconnected stores —
localStorage (Add Resource), `/api/ics/resources` (load), and `/api/ics/tcards` (drag/personnel
writes). It is now unified on `/api/ics/tcards`.

<details><summary>Original finding (before the fix)</summary>

`checkin.html` tells the user *"Your check-in goes to the ICS-211 roster **and T-card board** at the ICP."*
Today that second half is **not built**:
- A 211 self-check-in (`POST /api/ics/checkin`) writes only to `checkin_entries`. **No T-card is created.**
- The `ics/operations.html` T-card board **reads from `:5050/resources`** (the flat Resource Board, `fcc_lookup_server`) but **writes card moves to `:5055/api/ics/tcards`** (`ics_platform_server`). So the board's read store and the T-card store are two different places — a server-side auto-created T-card on 5055 would not even show on the board until that data-source split is reconciled.

**To honor the promise, two things are needed:** (1) create/refresh a T-card when a 211 check-in arrives (idempotent, keyed to the check-in id so re-check-in updates rather than duplicates), and (2) make the operations board load T-cards from `/api/ics/tcards` (5055) so those cards actually render. Recommend doing both together. *(Server-side T-card save was already hardened — it's now a field-preserving partial upsert with a `period` column and cost fields, so a status-only move no longer wipes leader/contact/cost.)*

</details>
