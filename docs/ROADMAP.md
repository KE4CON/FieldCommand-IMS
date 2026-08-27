# FieldCommand IMS — Roadmap

Post-v1.0 planned work. Items here are **not** in v1.0 scope; they are recorded so they are not lost.

---

## Transport Security (HTTPS) — ✅ IMPLEMENTED (2026-08-13)

**Shipped:** the app now serves over HTTPS with an HTTP→HTTPS redirect. The four core
services (5050/5051/5055/5056) are bound to `127.0.0.1` and reached same-origin through
nginx at `/svc/<port>` — so operator PII (roster, check-ins, ICS forms, FEMA costs) is no
longer on the wire in cleartext, and camera/GPS/PWA secure-context features are unlocked.
Certificate is generated at install by `scripts/fc-gen-cert.sh` — a private local CA by
default (install `fieldcommand-ca.crt` on devices for a clean padlock), or `--self-signed`
(`TLS_SELF_SIGNED=1`). See `udev/nginx-fieldcommand.conf`.

**Remaining follow-ups (smaller):**
- **Live APRS tactical feed** — ✅ done. nginx now reverse-proxies the APRS RF source (APRS Command,
  port 8080) at `/aprs-gw/` with WebSocket upgrade, so the tactical map
  fetches same-origin and opens `wss://` over TLS. `tactical.html` auto-selects the proxy under
  HTTPS and the direct host:port under plain http. Upstreams default to this server; if the APRS
  gateway runs on another host (e.g. the ops laptop), point the `/aprs-gw/` `proxy_pass` line at it.
- **Other direct-port services** still served over plain HTTP on their own ports: Pat Winlink
  (8090), Kiwix (8081), tiles (8083, also proxied at `/tiles`). Non-PII; optionally bind-localhost
  + proxy them later.
- **Gateway FCC lookup** (`amprgate_status.py`) calls the server over HTTPS with certificate
  verification disabled (public data, graceful fallback). Tighten to verify the local CA if the
  root is distributed to the gateway Pi.

---

## (historical) v1.5 / v2.0 — Transport Security (HTTPS)  ·  the original plan

**Why this is on the near track:** served agencies (county emergency management, public
safety) increasingly expect a secure ("padlock") system and may formally vet it before
approving use. Today FieldCommand serves everything over plain HTTP on the closed
EMCOMM-NET LAN, which has two consequences worth fixing sooner than later.

### What's wrong today
1. **Sensitive data crosses the Wi-Fi in cleartext.** Roster names/phones/emails/certifications,
   check-ins, Incident Command System (ICS) forms, and Federal Emergency Management Agency (FEMA)
   cost data are all sent unencrypted. Anyone associated to EMCOMM-NET (the password is shared) —
   or on a rogue/evil-twin access point — can passively read all of it.
2. **Browser features that require a "secure context" are blocked.** Browsers only allow the
   camera (`getUserMedia`), browser GPS/geolocation, and installable Progressive Web App (PWA)
   behavior over HTTPS (or `localhost`). This is why the live camera QR check-in does not work
   over the network today (see the v1.0 mitigation below).

### The constraint that shapes the fix
FieldCommand runs on a private IP (`192.168.50.1`) on an offline island network with **no public
domain name**, so a normal public Certificate Authority (CA) certificate (e.g. Let's Encrypt) is
not possible. That leaves two honest options:

| Option | User experience | Effort |
| --- | --- | --- |
| **Self-signed certificate** | Every device shows a one-time "Not secure / your connection is not private" warning the user must accept; some browsers keep a muted "Not secure" label. | Low |
| **Local CA (recommended)** | Generate a private root certificate once; pre-install it on the imaged Raspberry Pi 500/500+ workstations so they show a clean padlock with no warning. Personal phones either accept the one-time warning or install a small trust profile. | Medium |

### Planned work (when scheduled)
1. **Cert generation at install time** — create a long-dated (e.g. 10-year) certificate whose
   Subject Alternative Name (SAN) includes the server IP `192.168.50.1`. Prefer the local-CA
   approach with the root pre-trusted on imaged workstations.
2. **nginx `:443` server block** — mirror the existing port-80 site over Transport Layer Security
   (TLS); offer an **optional** (not forced) HTTP→HTTPS redirect so everyday HTTP use keeps working
   while camera/GPS/PWA get a secure context.
3. **Route the front-end API calls same-origin through nginx** — today ~65 base-URL constants
   across ~50 pages point directly at `http://192.168.50.1:<port>` (ports 5050 main, 5055 ICS,
   5056 refs, 5051 health). Under HTTPS those become blocked "mixed content." Change them to
   same-origin relative prefixes proxied by nginx to the local ports (backends stay plain-HTTP on
   `127.0.0.1`, never exposed). The constants are consistent and centralized, so this is mechanical.
4. **Docs** — Installation Guide: add the cert step and the one-time "accept the warning / install
   the root" instruction per device. User Manual: note the padlock and the camera unlock.

### v1.0 mitigation already shipped (so this is not urgent-blocking)
Phone QR check-in works **today over plain HTTP** without any of the above, via two paths added to
`html/scan_checkin.html`:
- **Take Photo of QR** — snapping a still photo uses the operating-system camera through a file
  input (no secure context needed) and decodes it with `BarcodeDetector`. (Requires a browser that
  has `BarcodeDetector` — Chrome/Chromium/Edge on Android and the workstations; not iOS Safari.)
- **Hardware barcode/QR scanner** — a Universal Serial Bus (USB) or Bluetooth "keyboard wedge"
  scanner types the decoded value and presses Enter into the auto-focused manual-entry box. Uses no
  camera and no secure context, so it works on **every** device including iPhones, and is the most
  robust option for a fixed check-in station. A 2-dimensional (2D) imager is required to read QR
  codes (a 1D-only scanner reads linear barcodes only).

---

## Other post-v1.0 candidates

- **Public-safety branding is hardcoded to "Starcom" in the UI** (found 2026-08-13 during the
  Programming Guide pass). `html/index.html` and related pages hardcode "Starcom" / "Starcom Net
  Logger" / the `starcom` mode instead of deriving the label from the configured public-safety
  system name (`station_config.ps_system_name`). A non-Starcom agency (World edition) still sees
  "Starcom" everywhere. Fix: drive the public-safety label from config so it's truly agency-neutral.
  (The User Manual accurately describes the current hardcoded UI, so it should be updated together
  with this change.)
- **Two dead-man's-switch monitors can disagree** (found 2026-08-13). `python/deadmans.py` (a
  standalone service watching `dms_state.json`, `armed_nets` as a JSON *list* with one global
  threshold) and the `dms_monitor()` inside `fcc_lookup_server.py` (watching the `dms_state` SQLite
  table, `armed_nets` as a *dict* with per-net thresholds) implement the same feature two ways with
  different state shapes/stores. They can hold conflicting state. Consolidate onto one (the
  table-based monitor with the arm/reset/disarm endpoints is the canonical one).
- **`theme.css` `@import`s a Google Font** (Oswald) — a single online dependency in an otherwise
  offline-first front end; bundle the font locally so the theme renders fully offline.

_(add more here as they come up)_
