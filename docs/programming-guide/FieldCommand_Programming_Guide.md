# FieldCommand IMS — Programming Guide

*How the code works, and why — plain enough to follow, deep enough to maintain.*

*Generated August 26, 2026 · Markdown is the living source of truth.*


---


# 1. Introduction — What FieldCommand Is and How This Book Works

*FieldCommand IMS is an offline-first incident-management server that runs on a single Raspberry Pi and is used from an ordinary web browser. This chapter explains what the platform is, the small and deliberate technology stack it is built on, how to read this book, and where every part of the code lives.*

> **IN ONE SENTENCE** — FieldCommand IMS is a self-contained incident-management server — a Raspberry Pi running *nginx* in front of a few small Python programs and one *SQLite* database file — that any browser on its own Wi-Fi network can use with no internet, no login, and no app to install.


## What This Is / What It Is For

FieldCommand IMS is a complete Incident Command System / National Incident Management System (ICS/NIMS) incident-management platform that keeps working when the internet, the cell network, and commercial power are all gone. It runs on a single **Raspberry Pi 5** — a small, inexpensive single-board computer — which also broadcasts its own Wi-Fi network. Any phone, tablet, or laptop that joins that network opens a web browser, goes to `http://192.168.50.1`, and has the full suite of ICS tools: the net loggers, the resource and facility tracking, the tactical map, and every form needed to build a complete Incident Action Plan (IAP).

The thesis behind the whole product is that **communications is inseparable from running an incident**. Cloud incident-management platforms — WebEOC, E-Team, NIMSIAP — all stop working the moment the infrastructure they depend on goes down, which is exactly the moment an emergency manager needs them most. FieldCommand is the offline-first answer to that: it is designed specifically for the moment when everything else fails. It adds a native amateur-radio and public-safety communications capability that no other ICS platform provides, and it deliberately puts amateur radio in front of emergency managers as the backup that survives a total-infrastructure disaster.

> **JARGON, IN PLAIN WORDS** — **Incident Command System / National Incident Management System (ICS/NIMS)** is the standard, nationwide way United States responders organize and document an emergency — the roles, the forms, and the workflow. **Incident Action Plan (IAP)** is the packet of standard forms that describes what an incident is doing during one work shift. **Offline-first** means the software is built to run with no internet at all; anything that needs the internet is an optional extra that lights up only when a connection happens to be present.

One rule frames everything about the data side of the system: **incident data is permanent — save everything.** Every net, log, ICS form, T-card, cost record, resource, and roster snapshot an incident produces is written to the server, backed up to an external drive, and archived. Nothing an incident generates is treated as throwaway or session-only. (This is the deliberate opposite of the sibling project, Activation Planner, which is intentionally stateless.) When you work on any incident feature, the default is always *persist it and make sure it reaches the backup and archive path.*


## The Whole Stack in One View

FieldCommand's technology stack is intentionally tiny. The entire system is four kinds of thing, and you can hold all of them in your head at once:

| Layer | What it is | Why it's here |
| --- | --- | --- |
| **nginx** | A web server that answers the browser on the standard ports (80 and 443), serves the static pages, terminates the encryption (TLS), and forwards Application Programming Interface (API) calls to the right Python service. | One front door for everything, so the browser only ever talks to one place over one secure connection. |
| **Python services** | Several small, single-purpose programs, each built on Python's own `http.server` from the **standard library only** — no web framework. | Each concern (the core API, health, the ICS platform, the reference library) is its own independent process that can crash, restart, or be worked on alone. |
| **SQLite** | One database file on disk (`fieldcommand.db`), reached through `python/db.py`. | All incident data in a single file with no database server to install or babysit — backing it up is copying a file. |
| **Static HTML/JS** | Plain HyperText Markup Language (HTML) pages with inline CSS and JavaScript in `html/` — one page per tool. No framework, no build step. | Deploy by copying files. Nothing to compile means nothing in the build chain to break in the field. |

That is the whole picture. A browser asks nginx for a page or an API call; nginx serves the page from a folder or hands the API call to one of the Python programs; that program reads or writes the one SQLite file and answers. There is no application server, no container runtime, no message queue, and — importantly — **no build step**. What is in the `html/` folder is exactly what the browser runs, and what is in the `python/` folder is exactly what the server runs.

> **WHY 'NO BUILD STEP' IS A FEATURE, NOT A SHORTCUT** — There is deliberately nothing to compile, bundle, or transpile. That is what lets the software survive in the field: an operator can copy files onto a Raspberry Pi and it runs. The flip side is that syntax errors do not surface until a page is opened in a browser or a service is started. That is why the project's one hard rule is that no change is 'done' until `python scripts/preflight_check.py` passes — it compiles every Python file, syntax-checks every shell script, validates the JSON, and runs a syntax check on every `<script>` block in every HTML page.

The only third-party Python packages anywhere in the running system are `flask`/`flask-cors` (used by the offline map-tile server) and `reportlab`/`pypdf` (used only by the document generators that build the PDFs, not by the field server). Every other runtime service is pure Python standard library. That constraint is a promise: a maintainer never has to chase a dependency tree to keep the field server alive.


## How to Read This Book

This is a **maintainer's code book**, not a user manual. Its job is to explain how the code works and — just as important — *why it was built the way it was*, so that the next person to touch it makes changes that fit. It is written to be plain enough for a curious non-programmer to follow and deep enough for a maintainer to rely on. Every chapter follows the same three-part shape:

- *What it does* — a plain-language description of the piece and the job it performs.
- *Why it was built this way* — the reasoning and the trade-offs behind the design, so you understand the constraints before you change anything.
- *How it works* — the mechanics, grounded in the real source with exact code quoted from the files.

Two kinds of callout recur throughout. A **JARGON, IN PLAIN WORDS** note stops to define any technical term the moment it first appears, in everyday language. A **MAINTAINER'S RULE** at the end of each chapter states the one thing you must not get wrong when you work on that piece of the system. Every acronym is spelled out in full the first time it is used — like Transport Layer Security (TLS) — and then shortened.

> **JARGON, IN PLAIN WORDS** — **Grounded in the source** means every claim in this book is checked against the actual files in the repository, and the code you see quoted is copied from those files rather than invented. When this book shows a code block, it is real code you can go read yourself at the path named nearby.

Because the code is the living source of truth and this book is generated from per-chapter files, the fastest way to trust any statement here is to open the file it names and read the surrounding lines. Every chapter points at real paths under `python/`, `html/`, `scripts/`, `udev/`, and `systemd/`.


## A Map of the Codebase

The repository is organized by *kind of thing*, not by feature. Once you know these five folders, you can find anything:

| Folder | What lives here | Examples |
| --- | --- | --- |
| `python/` | Every backend service and helper — the code that runs on the server. About nineteen files. | `fcc_lookup_server.py` (core API, port 5050), `ics_platform_server.py` (ICS platform, 5055), `health_monitor.py` (5051), `reference_server.py` (5056), `tile_server.py` (8083), `db.py` (the one data layer). |
| `html/` | The web front end — one self-contained page per tool, with its CSS and JavaScript inline. About forty-nine pages, plus a tiny shared `lib/`. | `index.html` (the dashboard), `netcontrol.html`, `tactical.html`, `iap.html`, `theme.css`, and the two shared helpers `lib/identity.js` and `lib/tiles.js`. |
| `scripts/` | Installation, setup, and maintenance shell scripts — how the Pi is turned into a FieldCommand server. | `fieldcommand-setup.sh` (one-command build), `install.sh`, `update.sh`, `fc-gen-cert.sh` (TLS cert), `preflight_check.py` (the mandatory syntax gate). |
| `udev/` | System configuration files copied into place on the Pi — the operating-system-level glue. | `nginx-fieldcommand.conf` (the web front-end config), `hostapd.conf` (Wi-Fi), `dnsmasq-fieldcommand.conf`, and the device rules for the Global Positioning System (GPS) and radio hardware. |
| `systemd/` | The service definitions that tell the Raspberry Pi's operating system how to start, stop, and auto-restart each Python program at boot. | `fcc-lookup.service`, `ics-platform.service`, `health-monitor.service`, `fieldcommand-refs.service`, `fieldcommand-tiles.service`, `deadmans.service`. |

The documents you are reading now (the Installation Guide, the User Manual, and this Programming Guide) live under `docs/`, built by generators in `docs_generators/`. Those are tooling, not part of the running field server.

> **JARGON, IN PLAIN WORDS** — **systemd** is the part of Linux that starts programs at boot and restarts them if they die. A **service** (a `.service` file) is a small text file telling systemd what to run and under what conditions. **udev** is the Linux part that reacts to hardware being plugged in — for example, giving a specific GPS receiver a fixed device name every time.


## Who This Book Is For

This book is for the person who has to keep FieldCommand working and safely change it — the maintainer. That might be a volunteer coordinator, a hobbyist programmer, or the next author who inherits the project. It assumes you can read code but does not assume you already know this codebase or every technology in it, which is why jargon is defined as it appears and the reasoning is spelled out alongside the mechanics. If you are a curious non-programmer, you can still follow the What and the Why of every chapter; the How sections are where the code lives when you need them.


## Why It Matters / Design Takeaways

- *Small on purpose.* The entire stack is nginx + a few standard-library Python programs + one SQLite file + static HTML. You can hold the whole architecture in your head, and that is the point.
- *Offline-first is the north star.* Every design decision — SQLite over a database server, no build step, its own Wi-Fi — exists to make the system survive with zero internet on a single Raspberry Pi.
- *The code is the source of truth.* This book explains and quotes the real files; when in doubt, open the path named in the chapter and read the surrounding lines.
- *Every chapter answers What, Why, and How.* Read the Why before you change the How — the constraints are the reason the code looks the way it does.

> **MAINTAINER'S RULE** — Protect the two things that make FieldCommand survivable: **no build step** and **standard library only** in the runtime servers. Deploy by copying files; never introduce a compile/bundle step or a front-end framework, and never add a Python runtime dependency without updating `scripts/install.sh`. And whatever you change, it is not done until `python scripts/preflight_check.py` passes.


# 2. System Architecture — The Big Picture

*This chapter traces a single request from a browser all the way to the database and back, lays out the service-and-port map, and explains why FieldCommand is shaped as a set of small independent processes behind one nginx front door — and where every piece of state lives.*

> **IN ONE SENTENCE** — A browser talks only to *nginx* over one encrypted connection; nginx serves the static pages and forwards each Application Programming Interface (API) call — using a same-origin `/svc/<port>/` address — to the matching small Python service, which reads or writes the one *SQLite* file and answers.


## What This Is / What It Is For

FieldCommand is not one big program. It is a handful of **small, single-purpose Python backends**, each doing one job, all sitting behind a single web server (**nginx**) that faces the browser. The architecture's job is to make that collection of parts behave, to the operator, like one seamless website — while keeping the parts genuinely independent underneath, so any one of them can be restarted or worked on without taking down the rest.

This chapter is the map you keep open while reading the rest of the book. Every later chapter is about the inside of one of these boxes; this chapter is about how the boxes connect, which port each one listens on, and how a click in a browser becomes a row in the database.

> **JARGON, IN PLAIN WORDS** — **nginx** (pronounced 'engine-x') is a fast web server that answers browsers, serves files, and can act as a **reverse proxy** — meaning it takes a request meant for a program running behind it and forwards it on, then relays the answer back. A **port** is a numbered doorway on a computer; different programs listen on different port numbers so requests reach the right one. **Same-origin** means every request goes to the same address (same name, same port, same encryption), which browsers treat as safe and simple.


## How It Works — The Request Path

Follow one API call from a page. Every request, whether for a page or for data, arrives at nginx first — nothing else is exposed to the browser. Here is the whole path:

1. A device on the FieldCommand Wi-Fi opens a page and the page's JavaScript makes a call — for example, the dashboard fetching the station configuration.
2. That call goes to nginx over Hypertext Transfer Protocol Secure (HTTPS) on port 443. nginx terminates the Transport Layer Security (TLS) encryption here — it is the only place encryption is handled.
3. nginx looks at the address. If it is a file (a page, an image, a stylesheet), nginx serves it straight from the `html/` folder on disk. If it starts with `/svc/<port>/`, nginx forwards it to the Python service listening on that port on the same machine.
4. The Python service handles the request — reading or writing the SQLite database through `python/db.py` — and returns JavaScript Object Notation (JSON).
5. nginx relays that answer back to the browser over the same encrypted connection. The page updates.

The front-end code shows how simple the browser's side of this is. The shared identity helper, and every page, calls the core API through a fixed same-origin base — there is no host or port in the address the browser ever sees:

```
const API       = '/svc/5050';
```

And a real call from the dashboard (`html/index.html`) looks like this — just a path, no scheme and no host:

```
const r = await fetch('/svc/5050/api/config');
```

On the nginx side, the matching rule forwards that `/svc/5050/` address to the core service on the local machine. The comment in the real config file explains the one subtle mechanic — the **trailing slash** on `proxy_pass` strips the `/svc/5050/` prefix, so the Python service sees exactly the path it always expected (`/api/config`), unaware that nginx is in front of it:

```
# /svc/<port>/<path>  ->  http://127.0.0.1:<port>/<path>
# The trailing slash on proxy_pass strips the /svc/<port>/ prefix, so the
# backend sees exactly the path the front end used to call directly.
location /svc/5050/ {   # main API / FCC lookup / QR / ID cards
    proxy_pass         http://127.0.0.1:5050/;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_read_timeout 60;
    client_max_body_size 20M;   # member photos, logos
}
```

> **JARGON, IN PLAIN WORDS** — **HTTPS** is ordinary web traffic (HTTP) wrapped in encryption so it cannot be read in transit. **TLS (Transport Layer Security)** is that encryption. **Terminate TLS** means nginx is where the encryption is unwrapped; everything past nginx, on the same machine, is plain unencrypted traffic to `127.0.0.1` (the machine talking to itself). **`proxy_pass`** is the nginx instruction that forwards a request to a program behind it.


## How It Works — The Service and Port Map

Each concern is its own process listening on its own port. This is the complete map, taken from the real `udev/nginx-fieldcommand.conf` and the systemd service files. The first four are the **core services**; the rest are supporting servers proxied by nginx under friendly paths.

| Port | Service (file) | Role | nginx path |
| --- | --- | --- | --- |
| 5050 | `fcc_lookup_server.py` | Core API — Federal Communications Commission (FCC) callsign lookup, nets/roster, GPS position, hospitals, preflight, ID cards. | `/svc/5050/` |
| 5051 | `health_monitor.py` | Health monitor — CPU/memory/disk, service states, internet/GPS/Wide-Area-Network (WAN)/44Net roll-up. | `/svc/5051/` |
| 5055 | `ics_platform_server.py` | ICS platform — incidents, ICS forms, Resource Status Cards (T-cards), the IAP, and Federal Emergency Management Agency (FEMA) cost tracking. | `/svc/5055/` |
| 5056 | `reference_server.py` | Offline reference library — stores and renders reference Portable Document Format (PDF) files; large uploads. | `/svc/5056/` |
| 8081 | Kiwix | Offline knowledge library (for example, an offline copy of reference wikis). | `/kiwix/` |
| 8083 | `tile_server.py` (Flask) | Offline map tiles — serves the map imagery for the tactical and resource maps with no internet. | `/tiles/` |
| 8090 | Pat (Winlink) | Winlink backup email over radio. | `/winlink/` |

Two more nginx paths, `/aprs-gw/` and `/aprs-yc/`, exist to relay the live Automatic Packet Reporting System (APRS) tactical feed — including WebSocket upgrades — from a radio gateway, so the browser can reach that feed same-origin over TLS as well. They point by default at the APRS gateway on this machine and can be repointed at another host if the gateway runs elsewhere.

> **DO NOT POINT ICS CALLS AT 5051** — The ICS platform is on port **5055**. Port **5051** is the health monitor. These are easy to transpose and the mistake is silent — an ICS API call sent to 5051 simply will not find its route. When you add or move an ICS endpoint, confirm the front end calls `/svc/5055/`.


## Why It's Shaped This Way — Localhost-Only Core Services

The four core services (5050, 5051, 5055, 5056) each **bind to `127.0.0.1` only** — the loopback address, meaning they accept connections from the same machine and nothing else. They are never reachable directly from the network; the only way in is through nginx over HTTPS. You can see this at the bottom of each server's `main()`. In the core API server (`fcc_lookup_server.py`):

```
log.info("FCC Lookup API server on port 5050")
# Bind localhost only: the front end reaches this via nginx at /svc/5050 over
# HTTPS; the service is not exposed on the network directly.
HTTPServer(("127.0.0.1", 5050), Handler).serve_forever()
```

And identically in the ICS platform server (`ics_platform_server.py`):

```
log.info("ICS Platform API on port 5055")
# Localhost only — reached via nginx at /svc/5055 over HTTPS.
HTTPServer(("127.0.0.1", 5055), ICSHandler).serve_forever()
```

This is a **recent, deliberate security change**, and it matters for maintenance. Earlier, the front end called services directly at `http://host:<port>`, which meant those ports had to be open on the network and pages mixed encrypted and unencrypted traffic. Now there is exactly one door (nginx, TLS) and one address style (`/svc/<port>/`), and the same page works identically over plain HTTP in development and HTTPS in production with no mixed-content problems. The config file states this intent directly:

```
# The four core services (5050 main/FCC, 5051 health, 5055 ICS, 5056 refs) are
# reached same-origin at /svc/<port>/... so the app works identically over http
# (dev) and https (production) with no mixed-content. The front end no longer
# calls http://host:<port> directly.
```

> **WHY THERE IS DELIBERATELY NO HSTS** — The nginx config intentionally omits the HTTP Strict-Transport-Security (HSTS) header. FieldCommand uses a self-signed or local-Certificate-Authority (CA) certificate on a closed Local Area Network (LAN) with no public domain, so the browser shows a one-time trust prompt. HSTS would forbid that click-through and lock operators out of their own appliance. Leave it off — it is a considered choice, noted in the config, not an oversight.

The supporting servers (tiles on 8083, and the others) are a slightly different case: the tile server binds `0.0.0.0` (all interfaces) by design, but is still reached through nginx's `/tiles/` path in normal use. The security posture across the whole appliance rests on one fact: **the network itself is isolated.** FieldCommand is a no-login, open-LAN tool on purpose — 'any device, no login' is a feature — which is safe only because the EMCOMM-NET Wi-Fi is a closed network. These ports must never be exposed to an untrusted network.


## Why It's Shaped This Way — Independent Processes, One File

Two design choices define the whole architecture, and both trace straight back to running in a field with no internet and no database expert on hand.

**First: many small independent processes instead of one framework.** Each service is built on Python's own `http.server` from the standard library — no Django, no Flask (except the tile server), no application framework at all. Each one is its own systemd service, so it starts at boot, restarts automatically if it crashes, and can be updated or restarted without touching the others. If the reference library server has a bad day, net logging and the ICS platform keep running. The cost of this independence is that these are simple single-threaded servers; a slow request in one process can block other clients of *that* process, which is a known, consciously-deferred trade-off rather than a bug.

**Second: one SQLite file instead of a database server.** All incident data lives in a single file reached through `python/db.py`. There is no database server to install, secure, start at boot, or troubleshoot at two in the morning in a shelter. Backing up the entire system's data is copying a file. The data layer chapter covers how `db.py` makes concurrent access from several processes safe; here the point is architectural — the shared state of the whole platform is one file on one disk.

> **JARGON, IN PLAIN WORDS** — A **process** is one running program with its own memory. **Single-threaded** means a process handles one request at a time, start to finish, before the next. **Binding to `0.0.0.0`** means listening on every network connection the machine has; **binding to `127.0.0.1`** means listening only to the machine itself. **systemd** is the Linux part that launches these processes at boot and restarts them if they die.


## How It Works — Where State Lives

It helps to know exactly where every kind of state is kept, because that tells you what survives a reboot, what gets backed up, and what does not:

| State | Where it lives | Survives a reboot? |
| --- | --- | --- |
| All incident data (nets, logs, ICS forms, T-cards, IAP, cost, resources, roster, station config) | The one SQLite file, via `python/db.py`. Backed up to an external drive and archived. | Yes — this is the permanent record. |
| Uploaded files (member photos, logos, reference PDFs, map tiles) | Files on disk under `/opt/fieldcommand/data/` and the tile store. | Yes. |
| Per-operator UI state (which identity is selected, panel choices) | The browser's `localStorage` on each device — never on the server. | Only on that device; it is not incident data and is not archived. |
| Live status (CPU, service health, internet/GPS/WAN) | Computed on demand by the health monitor; not stored. | No — it is a snapshot of right now. |

The dividing line is simple and important: **incident data is server-side and permanent; interface preferences are browser-side and disposable.** When you build a feature, anything an incident produces must be persisted through `db.py` so it reaches the backup and archive path — never left in memory or in `localStorage` alone.


## Why It Matters / Design Takeaways

- *One front door.* Every request goes through nginx over one TLS connection; the browser only ever uses same-origin `/svc/<port>/` addresses, so development and production behave identically with no mixed-content.
- *Locked-down core.* The four core services bind `127.0.0.1` and are unreachable except through nginx — a recent, deliberate security tightening. The whole no-login model is safe only because the LAN is isolated.
- *Independent by design.* Each concern is its own standard-library Python process and its own systemd service, so one can fail or be updated without taking down the rest.
- *State has a clear home.* Incident data is one SQLite file (permanent, backed up); interface preferences live in the browser (disposable). Know which is which before you store anything.

> **MAINTAINER'S RULE** — Respect the one-front-door shape. The browser must reach services only through nginx's `/svc/<port>/` paths — never wire a page to `http://host:<port>` directly, and keep the core services bound to `127.0.0.1`. When you add a service, add its nginx `location` block and a systemd unit, keep it localhost-only unless there is a specific reason not to, and confirm the whole thing still passes `python scripts/preflight_check.py`.


# 3. The Web Front End — Static HTML/JS, No Framework

*Every screen a FieldCommand operator touches is a plain HTML file with its own inline JavaScript, styled by one shared theme.css and served straight off disk. There is no build step, no bundler, and no framework — you edit a file and reload the page.*

> **IN ONE SENTENCE** — FieldCommand's user interface is roughly 56 hand-written HTML pages that share one `theme.css` and a couple of small `lib/*.js` includes, each page carrying its own inline `<script>` that fetches data from the back end over same-origin `/svc/<port>/...` URLs — no framework, no build step, edit-and-reload.


## What This Is / What It Is For

The FieldCommand front end is the collection of screens in `/opt/fieldcommand/html`: the station dashboard (`index.html`), the roster, net control, the Incident Command System (ICS) forms, the resource and cost pages, the tactical map, setup, and about fifty more. Each screen is a **single, self-contained HTML file**. Open `roster.html` in an editor and you see the whole page — its markup, a `<style>` block for anything page-specific, and one `<script>` block with all of that page's behavior. There is no separate JavaScript project, no compiled bundle, and nothing to `npm install`. The browser loads the file nginx hands it and runs it as-is.

This is a deliberate design choice, not a shortcut. FieldCommand runs on a Raspberry Pi in a field, a shelter, or an Emergency Operations Center (EOC) with no internet and, frequently, no one on site who can rebuild a JavaScript project. The front end has to be something a volunteer can open, read, fix, and reload with nothing but a text editor and a browser. Plain HTML and plain JavaScript are exactly that: what you see in the file is what runs, and a reload is the entire deploy process.

> **JARGON, IN PLAIN WORDS** — A **framework** (React, Vue, Angular) is a large JavaScript library you build your app on top of; it usually needs a **build step** — a program that bundles and transforms your source into files the browser can run. A **bundler** (webpack, Vite) is that program. FieldCommand uses none of them: the files you write are the files the browser runs.


## Why No Build Step — the 'Why' Behind the Choice

A modern JavaScript build pipeline buys you convenience — typed code, module bundling, minification, hot reload — at the cost of a toolchain that must be installed, kept up to date, and re-run every time you change a line. On a purpose-built offline appliance that cost is the wrong trade. If the interface only ran after a successful `npm run build`, then a broken dependency, a missing Node version, or a corrupt `node_modules` on the Pi would mean no dashboard during an actual incident. Removing the build step removes that entire class of failure.

The offline-first, edit-and-reload model has three concrete payoffs. **First, transparency:** a maintainer can read any screen top to bottom in one file and see exactly what it does. **Second, resilience:** there is nothing to compile, so nothing about the interface can fail to compile in the field. **Third, longevity:** plain HTML and JavaScript from today will still open and run in a browser years from now, with no framework version to chase. The price paid for those wins is covered honestly in the trade-offs section below — this is a real engineering decision with two sides, not a free lunch.


## How It Works — the Anatomy of One Page

Every page follows the same simple skeleton. It links the one shared stylesheet, adds only the styles unique to that page, writes its markup, and then includes its shared libraries and its own inline script at the bottom. Here is the top of a real page, `roster.html` — note the single shared `theme.css` link:

```
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Incident Management — Station Dashboard</title>
<link rel="stylesheet" href="theme.css">
<style>
/* only the styles unique to THIS page live here */
</style>
```

At the **bottom** of the same page come the shared includes and the page's own logic. The shared library is pulled in with an ordinary `<script src>` — no import system, no module resolver — and the page's behavior follows in a second inline `<script>`:

```
<script src="/lib/identity.js"></script>
<script>
const API = "/svc/5050";
// ... this page's own functions: loadRoster(), filterMembers(), ...
</script>
```

That is the whole pattern, repeated across all ~56 pages: **shared look** from `theme.css`, **shared cross-page behavior** from `lib/*.js`, and **per-page behavior** in an inline `<script>`. There is no shared application shell and no router — each page is its own small program, and navigation between pages is ordinary links to other `.html` files.


## How It Works — the Shared theme.css

The one thing every page truly shares is its appearance, and that lives entirely in `theme.css`. The file opens by declaring a set of **design tokens** — Cascading Style Sheets (CSS) custom properties on `:root` — so that colors, fonts, spacing, and shadows are defined once and referenced everywhere. A page never hard-codes the EOC navy; it uses the variable:

```
:root {
  --bg:     #f0f4f8;   /* page background — cool grey     */
  --panel:  #ffffff;   /* card surface                    */
  --line:   #c8d8e8;   /* borders                         */
  --txt:    #1a2535;   /* primary text — deep navy        */
  --muted:  #4a5e78;   /* secondary text                  */
  --eoc:    #1a3a6b;   /* primary brand — FEMA ICS blue   */
  --accent: #d97706;   /* gold accent for badges          */
  --font-ui:  -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  --font-hd:  'Oswald', 'Arial Narrow', Arial, sans-serif;
  --shadow-sm: 0 1px 3px rgba(26,58,107,0.08), 0 1px 2px rgba(26,58,107,0.05);
}
```

Because these tokens are plain CSS variables, the same values are reachable from inline styles in JavaScript too — the identity badge, for example, falls back gracefully with `var(--eoc,#1a3a6b)` so it looks right even on a page that somehow loaded without the stylesheet. `theme.css` also defines the shared components every page reuses — `.section-card`, `.btn` and its color variants (`.btn-primary`, `.btn-success`, `.btn-danger`), badges, tables — plus a full print stylesheet, so the ICS forms print cleanly. The file's own header states the rule plainly: *all shared components defined here — no more inline duplication*.

> **JARGON, IN PLAIN WORDS** — A **CSS custom property** (or **design token**) is a named value like `--eoc: #1a3a6b` you set once and reuse with `var(--eoc)`. Change the definition and every element using it updates at once. The `var(--eoc, #1a3a6b)` form supplies a fallback color to use if the variable is not defined.

> **ONE ONLINE DEPENDENCY LIVES IN theme.css** — The very top of `theme.css` has an `@import url('https://fonts.googleapis.com/...Oswald...')` for the heading font. On a truly offline LAN that import simply fails and the browser falls back to the next font in `--font-hd` ('Arial Narrow'), so nothing breaks — but be aware it is the one place the otherwise offline-first front end reaches for the public internet. If you want zero external calls, host the font locally and change this line.


## How It Works — the Shared lib Includes

Only two behaviors are genuinely common across many pages, so only two shared scripts exist in `html/lib/`. Each is written as an **Immediately Invoked Function Expression (IIFE)** that exposes a single global object — `FC_ID` and `FC_TILES` — and nothing else, so pages get a clean, small public interface with no globals leaking out.

| Shared library | Global it exposes | What it does |
| --- | --- | --- |
| `lib/identity.js` | `FC_ID` | Remembers who the operator is (callsign / member ID / radio ID) in the browser's `localStorage`, renders the 'On as:' header badge, and pops the 'Identify Yourself' picker. Every page that logs an action asks `FC_ID` who did it. |
| `lib/tiles.js` | `FC_TILES` | Builds the map's base-layer control for any Leaflet page: it probes the offline tile server first, falls back to online sources when the internet is reachable, and picks the best default basemap. |

`identity.js` is a good example of why sharing it matters: identity is needed on the roster, net control, the ICS logs, and more, and it must behave identically on all of them. It stores one object under a versioned key and offers a tiny read-only Application Programming Interface (API) the pages call:

```
const STORE_KEY = 'fc_operator_identity_v3';
const API       = '/svc/5050';
// ...
return {
    init, showPicker,
    getCallsign:  () => _id?.callsign  || '',
    getDisplayId: () => bestId(_id || {}),   // callsign → radio_id → member_id → name
    isVisitor:    () => ['visitor','mutual_aid'].includes(_id?.member_type),
    // ...
};
```

Note that even a shared library talks to the back end the same same-origin way a page does — `const API = '/svc/5050'`. `tiles.js` follows the identical convention for the map tile server, with `const TILE_SERVER = ''` and URLs built as `/tiles/{z}/{x}/{y}.png`, all same-origin. That consistency is the whole point of the next section.


## How It Works — Talking to the Back End (Same-Origin /svc)

Every page needs data, and every page gets it the same way: a `fetch()` to a **same-origin** path that begins with `/svc/<port>/`. The page declares one constant naming the service it uses, then builds all its calls from it. From `roster.html`:

```
const API = "/svc/5050";

async function loadRoster() {
  try {
    const r = await fetch(`${API}/api/roster`);
    const data = await r.json();
    allMembers  = data.members || [];
    activations = data.activations || [];
    filterMembers();
  } catch(e) {
    document.getElementById("memberList").innerHTML =
      '<div style="color:var(--red)">Cannot reach API</div>';
  }
}
```

Writes look the same, just with a method and a body — the standard `fetch` shape used everywhere in the code:

```
await fetch(`${API}/api/roster/members`, {
  method:  "POST",
  headers: { "Content-Type": "application/json" },
  body:    JSON.stringify(m)
});
```

The `/svc/<port>/` prefix is not a real folder on disk — it is a routing convention. nginx sees a request for `/svc/5050/api/roster`, strips the `/svc/5050/` part, and forwards `/api/roster` to the Python service listening on `127.0.0.1:5050`. The next chapter walks that proxy configuration in detail. For the front end, the important fact is that **`5050` is the main API / Federal Communications Commission (FCC) service, `5051` is the health monitor, `5055` is the ICS platform, and `5056` is the reference library** — and a page selects which back end it wants simply by which port it names in its `API` constant. You can see that in the earlier grep of every page: `roster.html`, `netcontrol.html`, and `starcom.html` name `/svc/5050`; `channel_library.html` names `/svc/5055`; `wan-status.html` names `/svc/5051`; `refs.html` names `/svc/5056`.

> **JARGON, IN PLAIN WORDS** — **Same-origin** means a request goes to the exact same protocol, host, and port the page itself was loaded from. Because `/svc/5050/...` has no `http://` and no host in it, the browser sends it back to wherever the page came from. That sidesteps browser cross-origin (CORS) restrictions and, crucially, mixed-content blocking on an HTTPS page.


## Why It Was Migrated Off Absolute host:port URLs

The front end did not always call `/svc/<port>`. Earlier, pages fetched the back end directly at an absolute address like `http://192.168.50.1:5050/api/roster`. That worked over plain HTTP, but it broke the moment the dashboard was served over HTTPS: a secure page is not allowed to fetch an insecure `http://...:5050` resource, so the browser blocks it as **mixed content**. Hard-coding the host also meant the interface only worked when it was reached at that one address.

Switching every call to the relative `/svc/<port>/` form fixes both problems at once. The nginx configuration file states the goal in its own header comment: the services are *reached same-origin at /svc/<port>/... so the app works identically over http (dev) and https (production) with no mixed-content. The front end no longer calls http://host:<port> directly.* Because the calls are now relative, the same HTML works whether you open it at `http://localhost`, `https://192.168.50.1`, or `https://fieldcommand.local` — the browser always sends the request back to the same origin, and nginx routes it onward.

> **WHY THIS IS A ONE-WAY DOOR** — Never reintroduce an absolute `http://host:port` fetch in a page, even 'just for a quick test.' A single absolute-URL call will silently fail under HTTPS with a mixed-content error that is easy to misdiagnose as a dead back end. If a new page needs a service, copy the `const API = '/svc/<port>'` pattern from an existing page — do not invent a new addressing scheme.


## The Trade-Offs, Stated Honestly

This approach is simple and transparent, and it is offline-proof. Those are exactly the properties an emergency appliance needs, and they are real, earned wins — but they come with real costs a maintainer should know going in:

| What you gain | What you give up |
| --- | --- |
| No build step — edit a file, reload the browser, done. Nothing to compile in the field. | No bundling or minification — each page ships its full source, and shared code that is not in a `lib/` file gets copy-pasted between pages. |
| Full transparency — the whole screen is readable in one file with a plain text editor. | No type checking — a typo in a property name is only caught at runtime, in the browser, on that page. |
| Offline-proof — no toolchain, no `node_modules`, nothing that can fail to install on the Pi. | No shared component system — a change to a repeated markup pattern may need editing in several pages by hand. |
| Longevity — plain HTML/JS keeps working with no framework version to upgrade. | Manual consistency — the discipline of always using `theme.css` tokens and the `/svc` convention is enforced by convention, not by a compiler. |

The honest summary: FieldCommand trades developer conveniences (types, bundling, hot module reload) for operational guarantees (nothing to build, nothing to install, everything readable). For a device that must come up and stay up in an emergency with no internet and no build server, that trade is the right one — but it means the shared conventions in this chapter are the only thing keeping ~56 independent pages coherent, so they must be honored every time.


## Why It Matters / Design Takeaways

- *No build step is a feature, not a gap.* Edit-and-reload means the interface can never fail to compile in the field, and any volunteer with a text editor can read and fix a screen.
- *One stylesheet, two libraries, many pages.* Shared look lives in `theme.css` design tokens; shared behavior lives in `FC_ID` and `FC_TILES`; everything else is a page's own inline script.
- *Same-origin `/svc/<port>` is the one way pages reach the back end.* It works identically over HTTP and HTTPS, avoids mixed-content blocking, and lets a page pick its back end just by naming a port.
- *The conventions are the architecture.* With no framework to enforce structure, the `theme.css` tokens and the `/svc` addressing pattern are what keep 56 hand-written pages consistent.

> **MAINTAINER'S RULE** — When you add or change a page: keep it a single self-contained HTML file; link the shared `theme.css` and use its `var(--...)` tokens rather than hard-coding colors; put cross-page behavior in a `lib/*.js` include, not copy-pasted script; and reach the back end only through a `const API = '/svc/<port>'` same-origin `fetch`. Never hard-code an absolute `http://host:port` URL — it will break the page the instant the dashboard is served over HTTPS.


# 4. The nginx Reverse Proxy and HTTPS

*One nginx configuration file is FieldCommand's single front door. It serves the static HTML, terminates HTTPS, and reverse-proxies every Python service and background helper behind one address and one port — so the browser only ever talks to one place.*

> **IN ONE SENTENCE** — `udev/nginx-fieldcommand.conf` makes nginx the one address a browser talks to: it redirects plain HTTP to HTTPS, serves the static `html` root, and reverse-proxies each Python service under a same-origin `/svc/<port>/` path — with the proxy's trailing slash quietly stripping that prefix so the back end sees the original path.


## What This Is / What It Is For

FieldCommand is not one program — it is a static web front end plus several independent Python services (the main / Federal Communications Commission (FCC) server on port 5050, the health monitor on 5051, the Incident Command System (ICS) platform on 5055, the reference library on 5056) and a handful of background helpers (the offline tile server, a Pat Winlink client, a Kiwix library, the live Automatic Packet Reporting System (APRS) feeds). If a browser had to reach each of those on its own host and port, the front end would be a tangle of cross-origin calls, and none of it would work over a single secure connection.

The **reverse proxy** solves that. nginx sits in front of everything as the single front door. The browser only ever connects to nginx — one host, one port (443), one certificate. nginx decides, per request path, whether to hand back a static file from disk or to forward the request to one of the local services and relay the answer. The whole policy for that lives in one file, [udev/nginx-fieldcommand.conf](udev/nginx-fieldcommand.conf), and the file's own header explains the intent: the four core services are *reached same-origin at /svc/<port>/... so the app works identically over http (dev) and https (production) with no mixed-content.*

> **JARGON, IN PLAIN WORDS** — A **reverse proxy** is a server that receives requests from the outside and quietly forwards them to other programs running behind it, then passes their answers back — so the outside world sees one server instead of many. **TLS** (Transport Layer Security) is what puts the padlock in the browser; 'terminating TLS' means nginx handles the encryption so the services behind it can speak plain HTTP locally.


## How It Works — Redirect Everything to HTTPS

The file opens with a tiny first server block whose only job is to make sure nothing ever stays on plain HTTP. Anything that arrives on port 80 is answered with a permanent redirect to the same URL on HTTPS:

```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    # Everything is served over TLS; send all plain-HTTP traffic to HTTPS.
    return 301 https://$host$request_uri;
}
```

`server_name _;` is a catch-all — it matches any hostname, which is exactly right for an appliance reached by bare IP address (`https://192.168.50.1`) or by a local name (`https://fieldcommand.local`). `$host$request_uri` preserves whatever the operator typed, so a link to a deep page still lands on that page, just over HTTPS. The `listen [::]:80` line adds the same behavior for Internet Protocol version 6 (IPv6).


## How It Works — the TLS Server and the Static Root

The second, main server block listens on 443 with TLS. It points at the certificate pair generated by the cert script (covered below), pins modern protocol versions, and then does the simplest of its jobs — serving the front end straight off disk from `/opt/fieldcommand/html`:

```
server {
    listen 443 ssl default_server;
    listen [::]:443 ssl default_server;
    server_name _;

    ssl_certificate     /etc/fieldcommand/tls/server.crt;
    ssl_certificate_key /etc/fieldcommand/tls/server.key;
    ssl_protocols       TLSv1.2 TLSv1.3;
    ssl_ciphers         HIGH:!aNULL:!MD5;

    root  /opt/fieldcommand/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
        add_header Cache-Control "no-store, no-cache, must-revalidate";
    }
}
```

`try_files $uri $uri/ =404` tells nginx to look for the requested file, then a directory, then give up with a clean 404 — the standard, safe way to serve static files. The `no-store` cache header on the HTML pages means an operator always gets the current version of a screen after an update (important when the whole deploy process is 'edit the file'), while a separate rule below it lets genuine assets — CSS, JavaScript, images, fonts — cache for an hour so the interface still feels quick.


## How It Works — the /svc/<port>/ Proxies and the Trailing Slash

This is the heart of the file and the mechanism the front end depends on. Each core service gets a `location /svc/<port>/` block that forwards to that service on localhost. The single most important detail is the **trailing slash on `proxy_pass`**, and the config comments it explicitly:

```
# /svc/<port>/<path>  ->  http://127.0.0.1:<port>/<path>
# The trailing slash on proxy_pass strips the /svc/<port>/ prefix, so the
# backend sees exactly the path the front end used to call directly.
location /svc/5050/ {   # main API / FCC lookup / QR / ID cards
    proxy_pass         http://127.0.0.1:5050/;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_read_timeout 60;
    client_max_body_size 20M;   # member photos, logos
}
```

Here is the rule that makes it work, spelled out. When `proxy_pass` has a **Uniform Resource Identifier (URI) part** — even just a `/` — nginx replaces the matched `location` prefix with that URI. So the matched prefix `/svc/5050/` is swapped for `/`. A browser request for `/svc/5050/api/roster` becomes `http://127.0.0.1:5050/api/roster` at the service. The Python service therefore sees `/api/roster` — exactly the path the front end used to call when it hit `host:5050` directly, which is precisely why the migration to `/svc` (from the previous chapter) required no back-end changes at all.

> **THE TRAILING SLASH IS LOAD-BEARING — DO NOT DROP IT** — `proxy_pass http://127.0.0.1:5050/;` (with slash) strips the `/svc/5050/` prefix. `proxy_pass http://127.0.0.1:5050;` (no slash) does NOT — the backend would receive `/svc/5050/api/roster` and answer 404 for every call. This one character is the difference between a working service and a dead one. If you add a new `/svc/<port>/` block, copy an existing one exactly, slash included.

The other lines are per-service tuning. `proxy_set_header Host $host` and `X-Real-IP` pass the real hostname and client address through so the service can log and build correct links. The timeouts and body-size limits differ by service on purpose — 5050 allows 20 megabytes (MB) for member photos and logos, while the reference library on 5056 allows 200 MB and a longer 120-second read timeout for large document uploads, and the health monitor on 5051 gets a short 10-second timeout because it should always answer instantly:

```
location /svc/5056/ {   # reference library (large uploads)
    proxy_pass            http://127.0.0.1:5056/;
    proxy_set_header      Host $host;
    proxy_read_timeout    120;
    client_max_body_size  200M;
}
```


## How It Works — the /tiles/ Exception (No Slash on Purpose)

Not every proxy wants the prefix stripped, and the offline map tile server is the deliberate exception. Its `proxy_pass` has **no trailing slash**, so the full original path is preserved and forwarded unchanged — because that is the path shape the tile server actually serves:

```
# No trailing slash on proxy_pass: preserve the full /tiles/<set>/<z>/<x>/<y>
# path, which is what the tile server serves.
location /tiles/ {
    proxy_pass         http://127.0.0.1:8083;
    proxy_set_header   Host $host;
    proxy_read_timeout 10;
    add_header Cache-Control "public, max-age=86400";
}
```

This is the same rule as before, used the other way around: **slash strips the prefix, no slash keeps it.** The tile server expects requests like `/tiles/usgs_topo/12/1050/1520.png` verbatim, so nginx must forward the whole thing. The day-long cache header (`max-age=86400`) suits map tiles, which effectively never change. This pairing of the two behaviors — strip for the `/svc` services, keep for `/tiles` — is worth internalizing, because getting it backward on a new proxy is the most common way to break one.


## How It Works — WebSocket Proxies for the Live APRS Feed

The tactical map shows a live APRS feed, which needs a **WebSocket** — a connection that stays open and streams both ways, rather than one request and one answer. Proxying a WebSocket requires nginx to pass the HTTP `Upgrade` handshake through, and the file sets that up with a small `map` at the very top:

```
# WebSocket upgrade helper (used by the live APRS feed proxies below).
map $http_upgrade $connection_upgrade {
    default upgrade;
    ''      close;
}
```

That `map` reads the incoming `Upgrade` header and produces the right `Connection` header to send onward: `upgrade` when the client is asking to switch to a WebSocket, `close` otherwise. The APRS proxies then use it, along with `proxy_http_version 1.1` (WebSockets require HTTP/1.1) and a very long read timeout so the stream is not cut off:

```
location /aprs-gw/ {
    proxy_pass         http://127.0.0.1:8080/;
    proxy_http_version 1.1;
    proxy_set_header   Upgrade $http_upgrade;
    proxy_set_header   Connection $connection_upgrade;
    proxy_set_header   Host $host;
    proxy_read_timeout 3600s;
}
```

There are two of these — `/aprs-gw/` to the Radio Frequency (RF) gateway on 8080 and `/aprs-yc/` to YAAC on 8082. The payoff is the same same-origin, single-front-door story as the rest of the file: the browser opens a secure `wss://` connection to nginx, nginx terminates the TLS and makes the plain, local `ws` hop to the APRS gateway itself. The config notes that if the APRS gateway runs on a different host (say the operations laptop), you change the `127.0.0.1` here to that host's address — the browser side never changes. The file also notes one thing it deliberately does **not** proxy: the 44Net gateway tunnel control on port 9001 is intentionally localhost-only on a different device and is left unexposed.

> **JARGON, IN PLAIN WORDS** — A **WebSocket** is a network connection that stays open so a server can keep pushing new data (here, live radio positions) without the page asking again each time. The `wss://` scheme is a WebSocket over TLS — the secure version — just as `https://` is HTTP over TLS.


## Why There Is Deliberately No HSTS

A production HTTPS site would normally send an HTTP Strict Transport Security (HSTS) header, which tells browsers 'only ever talk to this site over HTTPS, and refuse if the certificate is not trusted.' FieldCommand deliberately omits it, and the config says so directly at the point where it would go:

```
# NOTE: deliberately NO Strict-Transport-Security (HSTS). With a self-signed
# or local-CA certificate, HSTS would prevent the browser's one-time
# click-through and lock operators out of the LAN appliance.
```

The reasoning is specific to this environment. FieldCommand runs on a closed local-area network (LAN) with no public domain name, so it cannot obtain a certificate from a public Certificate Authority — it uses a private local Certificate Authority (CA) or a self-signed certificate. Browsers show a one-time trust prompt for those, which an operator clicks through. HSTS would turn that solvable prompt into a **hard block** with no click-through, locking every operator out of the appliance during an incident. Omitting HSTS is therefore the safe choice here, precisely the opposite of the public-internet default. The file still sends the sensible non-HSTS security headers — `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, and `Referrer-Policy: no-referrer`.

> **DO NOT 'HARDEN' THIS BY ADDING HSTS** — Adding an HSTS header would look like a security improvement in a checklist and would in fact brick the appliance for anyone using the self-signed path. The absence of HSTS is a correctness requirement for a local-CA / self-signed LAN device, not an oversight. Leave it out unless FieldCommand ever gains a real public-CA certificate.


## How It Works — the TLS Certificate (fc-gen-cert.sh)

nginx points at `/etc/fieldcommand/tls/server.crt` and `server.key`, and those are produced by [scripts/fc-gen-cert.sh](scripts/fc-gen-cert.sh). Because there is no public domain, the script builds the certificate locally in one of two modes. The default is a **local CA**: it creates a private root certificate authority once, then issues a server certificate signed by it. Install that root on each device a single time and the browser shows a clean padlock with no warning. The alternative, `--self-signed`, skips the root and issues a single self-signed certificate — nothing to distribute, but every device shows a one-time 'not secure' warning to accept.

The one detail that makes either certificate valid for an appliance reached by IP address is the **Subject Alternative Name (SAN)**, which lists the server's IP so modern browsers accept `https://192.168.50.1`:

```
SAN="subjectAltName=IP:${IP},IP:127.0.0.1,DNS:${HOST},DNS:localhost"

# self-signed mode: one X.509 cert carrying that SAN
openssl req -x509 -newkey rsa:2048 -nodes \
    -keyout "$SRV_KEY" -out "$SRV_CRT" -days "$DAYS" \
    -subj "/O=FieldCommand IMS/CN=${HOST}" \
    -addext "$SAN" \
    -addext "extendedKeyUsage=serverAuth"
```

In local-CA mode the script generates the root, then a server key and signing request, signs the leaf with the CA (carrying the same SAN), and concatenates the leaf and the CA into one file — because *nginx wants leaf + issuer chain in one file*. It then publishes the CA root into the web root so operators can download and install it straight from the appliance:

```
cat "$TLS_DIR/server.leaf.crt" "$CA_CRT" > "$SRV_CRT"
# ...
cp "$CA_CRT" "$PUB_DIR/fieldcommand-ca.crt"
#   (also reachable at https://${IP}/fieldcommand-ca.crt once HTTPS is up)
```

A few deliberate touches make this field-appropriate. Certificates are issued for `DAYS=3650` (about ten years) *so field units never silently expire*. The script refuses to overwrite an existing certificate unless you pass `--force`, and it warns that forcing *invalidates any already-installed trust* — regenerating means every device that trusted the old root must trust the new one again. And when it reuses an existing CA it keeps devices that already trust it valid. The keys are written with tight permissions (`chmod 600`) and the certificates world-readable (`chmod 644`).

> **JARGON, IN PLAIN WORDS** — A **Certificate Authority (CA)** is the entity that signs certificates so a browser trusts them; a **local CA** is your own private one, trusted only by devices you install its root on. A **Subject Alternative Name (SAN)** is the list of names and IP addresses a certificate is valid for — modern browsers ignore the old 'Common Name' and check the SAN, which is why the server IP must be listed there.


## Why It Matters / Design Takeaways

- *One front door.* nginx is the single host and port the browser talks to; it serves the static files and proxies every service behind it, so the front end stays same-origin and works identically over HTTP and HTTPS.
- *The trailing slash is the whole trick.* A slash on `proxy_pass` strips the `/svc/<port>/` prefix so the back end sees its own path; no slash (as with `/tiles/`) preserves the path. Getting this backward is the classic way to break a proxy.
- *WebSockets need the upgrade map.* The `$http_upgrade`→`$connection_upgrade` map plus `proxy_http_version 1.1` and a long timeout are what let the live APRS feed stream over a same-origin `wss://` connection.
- *No HSTS is intentional.* On a self-signed / local-CA LAN appliance, HSTS would lock operators out; its absence is a correctness requirement, not a gap.
- *The certificate is built for the field.* `fc-gen-cert.sh` offers a trust-once local CA or a warning-each-time self-signed cert, both with an IP SAN and a ten-year life so units never silently expire.

> **MAINTAINER'S RULE** — This one file is the whole edge configuration — change it here and nowhere else. To expose a new service, copy an existing `/svc/<port>/` block verbatim (trailing slash included) and adjust only the port, timeout, and body-size limit. Never remove the trailing slash from a `/svc` proxy, never add it to `/tiles`, and never add an HSTS header while the appliance uses a self-signed or local-CA certificate. After any edit, run `sudo nginx -t` and `sudo systemctl reload nginx` before you consider it done.


# 5. The Data Layer — SQLite and db.py

*One small Python file, python/db.py, is the single front door to all of FieldCommand's saved data. It owns the database file, the connection handling, the schema, the migrations, and the one-time import of the old JSON files. Every service goes through it.*

> **IN ONE SENTENCE** — `python/db.py` gives every FieldCommand service a thread-safe SQLite connection, creates and upgrades the schema on startup, and migrates any old JSON files in once — so the rest of the code just calls `db()` and writes SQL.


## What This Is / What It Is For

FieldCommand keeps everything an incident produces — nets, check-ins, the roster, ICS forms, resources, costs, map state, the station's own configuration — in **one** database file on the server. The data layer is the single piece of code that owns that file. It is [python/db.py](python/db.py), and it is deliberately small and boring: it opens the database, hands out connections, defines the tables, upgrades them when the code changes, and imports any legacy data left over from the old JSON-file days. Nothing else in the system talks to the database file directly; everything goes through here.

Three separate service processes (the main / Federal Communications Commission (FCC) lookup server, the Incident Command System (ICS) platform server, and the health monitor) all `import db`. Because they share this one module, they share one schema, one set of helpers, and one set of rules about how the database is opened. That is the whole point of having a data layer: the decisions about *how* data is stored live in exactly one place.

> **JARGON, IN PLAIN WORDS** — **SQLite** is a database that is just a single file on disk — there is no separate database server program to install, start, or log into. Your code opens the file and reads and writes it directly. **Schema** means the shape of the data: the list of tables and the columns in each. **Migration** means changing that shape safely after there is already real data in the file.


## Why SQLite — the 'Why' Behind the Choice

FieldCommand runs on a Raspberry Pi in a field with no internet and, often, no one who knows databases. A traditional database server (PostgreSQL, MySQL) would mean another service to install, secure, start at boot, back up, and troubleshoot at 2 a.m. in a shelter. SQLite removes all of that: the entire database is the file `/opt/fieldcommand/data/fieldcommand.db`. Backing it up is copying a file. There is no port, no password, no server process that can crash independently.

The trade-off is that SQLite is a library inside each process rather than a shared server, so the data layer has to be careful about **concurrency** — several service processes and several threads all touching the same file at once. The rest of this chapter is mostly about how `db.py` makes that safe. The paths are fixed at the top of the file, and the directories are created on import so a fresh install never fails for a missing folder:

```
BASE      = Path("/opt/fieldcommand")
DATA      = BASE / "data"
DB_PATH   = DATA / "fieldcommand.db"

for _d in [DATA, DATA / "nets", DATA / "forms", DATA / "ics" / "forms",
           REFS_DIR, FILES_DIR, THUMB_DIR]:
    _d.mkdir(parents=True, exist_ok=True)
```

> **WHY fcc.db IS KEPT SEPARATE** — The ~800,000-record FCC license database lives in its own file (`fcc.db`), not in `fieldcommand.db`. The file's own comment explains why: it is huge (~600 MB), it is rebuild-only, and the application never writes to it. Keeping it out of the main database keeps backups of live incident data small and fast.


## How It Works — One Connection Per Thread

Each service runs a **single-threaded** HTTP server (Python's `HTTPServer`), so within one process requests are handled one at a time. Even so, `db.py` gives **each thread its own connection** using Python's `threading.local()` and opens it with `check_same_thread=False`. This is defensive: any background thread (for example the dead-man's-switch monitor) — or a future switch to a threaded server — then never shares a SQLite connection unsafely, because SQLite connection objects are not meant to be passed between threads carelessly. The first time a given thread asks for a connection, one is created and tuned; after that, the same thread gets the same connection back:

```
_local = threading.local()

def get_conn() -> sqlite3.Connection:
    """Return a thread-local connection to fieldcommand.db."""
    if not hasattr(_local, "conn") or _local.conn is None:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA cache_size=-8000")   # 8 MB per thread
        conn.execute("PRAGMA temp_store=MEMORY")
        _local.conn = conn
    return _local.conn
```

Each setting is a deliberate choice, so here is what each one buys you:

| Setting | What it does | Why it's set this way |
| --- | --- | --- |
| `row_factory = sqlite3.Row` | Makes query results behave like dictionaries (`row['name']`) as well as tuples. | Every helper can turn a row straight into a dict for JSON responses — no column-order bugs. |
| `journal_mode=WAL` | Write-Ahead Logging: readers don't block the writer and the writer doesn't block readers. | The dashboard is constantly reading while net control is writing. WAL keeps both smooth on one file. |
| `synchronous=NORMAL` | Slightly relaxes how often SQLite forces data to disk. | A good safety/speed balance for a Pi with an SSD; still crash-safe under WAL. |
| `foreign_keys=ON` | Enforces the table relationships (e.g. deleting an incident cascades to its forms). | SQLite leaves this OFF by default; the schema relies on it, so it must be turned on per connection. |
| `cache_size=-8000` | Gives each connection an 8 megabyte (MB) page cache. | Speeds up repeated reads without using much of the Pi's memory. |
| `temp_store=MEMORY` | Keeps temporary tables/sorts in memory instead of on disk. | Faster sorts and joins; less SSD wear. |

> **JARGON, IN PLAIN WORDS** — **Thread-local** means each thread gets its own private copy of something. **Write-Ahead Logging (WAL)** is a way SQLite records changes to a side file first, so that reading and writing can happen at the same time without one freezing the other. **PRAGMA** is just SQLite's keyword for 'set an option on this connection.'

Two short aliases keep the calling code readable — services call `db()` everywhere rather than the longer name:

```
def db() -> sqlite3.Connection:
    """Shorthand for get_conn()."""
    return get_conn()
```


## How It Works — Creating and Upgrading the Schema

All the tables are defined as one big block of SQL in the `SCHEMA` string, and every table uses `CREATE TABLE IF NOT EXISTS`. That single word — `IF NOT EXISTS` — is what makes `init_db()` safe to call on **every** startup: if the table is already there, nothing happens; if it isn't, it's created. `init_db()` runs the whole schema in one call:

```
def init_db():
    """Create all tables and indexes. Safe to call multiple times."""
    conn = db()
    conn.executescript(SCHEMA)
```

But `CREATE TABLE IF NOT EXISTS` has a limit: it will **not** add a new column to a table that already exists from an older install. When a later version of FieldCommand needs a new column, the table is already there with real data in it, so the create statement does nothing. That is what the **migrations** list solves. It is a plain list of `ALTER TABLE ... ADD COLUMN` statements, run one at a time, each wrapped so that an 'already exists' error is simply ignored:

```
    migrations = [
        "ALTER TABLE nets ADD COLUMN net_opened TEXT",
        "ALTER TABLE station_config ADD COLUMN wifi_ssid TEXT DEFAULT 'EMCOMM-NET'",
        # ... dozens more, one per column added over the project's life
    ]
    for sql in migrations:
        try:
            conn.execute(sql)
        except Exception:
            pass  # column already exists
```

> **WHY THE BARE except IS INTENTIONAL HERE** — Swallowing every exception is normally a bad habit, and FieldCommand's own rules forbid it in general. This one spot is the deliberate exception: on a database that already has the column, `ADD COLUMN` throws, and that specific throw is the *expected, correct* outcome. The pattern is idempotent — running it a hundred times leaves the schema identical. When you add a column, append a new line here; never edit or reorder the existing lines, because field databases at every past version must all upgrade cleanly.

After the tables exist, `init_db()` seeds the reference data that a brand-new database needs to be useful — example radio channels, the National Incident Management System (NIMS) resource-typing library, hospitals, incident templates, and the Federal Emergency Management Agency (FEMA) equipment rates. Each seeder checks whether its table is already populated and does nothing if so, so seeding also runs safely on every boot:

```
    seed_hospitals(conn)
    seed_resource_types(conn)
    seed_channel_library(conn)
    seed_incident_templates(conn)
    seed_fema_equipment_rates(conn)
```

> **SEEDED DATA IS EXAMPLE DATA, NOT LOCKED DATA** — The seeded channels and similar defaults are McHenry County, Illinois examples on purpose — the seeder even says so in a comment. They are all fully editable and deletable from the app. Never treat seeded rows as system-owned; an agency is expected to replace them with their own.


## How It Works — Drop-In Template Packs

Beyond the built-in incident templates that `seed_incident_templates()` installs, a maintainer can ship additional templates without editing any Python. This is how a template an operator suggested — via the Event Templates page's 'Export Update Candidates' button — reaches a future release. `load_template_packs()` runs on every boot, right after the built-in seed:

```
    seed_incident_templates(conn)
    load_template_packs(conn)      # drop-in packs from python/seed_templates/
    seed_fema_equipment_rates(conn)
```

It reads every `*.json` file in `python/seed_templates/`. Each file is one template object, or an array of them, in the same shape the Event Templates page exports. For each one it inserts the row only when that `id` is not already present, marks it a protected built-in, and strips the operator-only `propose_upstream` flag. A malformed file is logged and skipped — never fatal:

```
TEMPLATE_PACK_DIR = Path(__file__).resolve().parent / 'seed_templates'

def load_template_packs(conn):
    if not TEMPLATE_PACK_DIR.is_dir():
        return
    for f in sorted(TEMPLATE_PACK_DIR.glob('*.json')):
        # ... parse f; skip and log if malformed ...
        for t in items:
            tid = str(t.get('id') or '').strip()
            if not tid or conn.execute(
                'SELECT 1 FROM incident_templates WHERE id=?', (tid,)).fetchone():
                continue          # new ids only — never clobber a local edit
            conn.execute('INSERT INTO incident_templates (...) VALUES (... is_builtin=1 ...)')
```

> **NEW IDS ONLY — WHY IT NEVER OVERWRITES** — The loader runs on every startup, not just first run, so a template file added in a new release also reaches already-deployed servers on their next update. Because it inserts only ids that are not already in the table, it can never overwrite a built-in an operator edited or a template a group customized. If you must push a corrected version of an already-shipped template, give it a NEW id — that is a deliberate change, not an accident waiting to happen.

> **THE MAINTAINER WORKFLOW, END TO END** — An operator flags a template and clicks Export Update Candidates on the Event Templates page, producing a JSON file, and sends it to you. You review it, give it a clear name (for example wildland-fire.json), and drop it into python/seed_templates/. install.sh and update.sh copy that folder onto the server, and load_template_packs() seeds it on the next database init — no BUILTIN_TEMPLATES edit and no schema change. The folder's own python/seed_templates/README.md has the drop-a-file steps.


## How It Works — The One-Time JSON Migration

Early versions of FieldCommand stored data in JSON files (a `nets/` folder, `roster.json`, `resources.json`, and so on). `migrate_from_json()` imports all of that into SQLite exactly once. The trick that makes it 'exactly once' is simple: after a file is successfully imported, it is **renamed** with a `.migrated` suffix, so the next boot no longer finds it. The generic helper shows the pattern:

```
def _migrate_json_file(path: Path, label: str, fn):
    """Load a JSON file, call fn(data), rename file to .migrated."""
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
        count = fn(data)
        path.rename(path.with_suffix(".migrated"))
        return count
    except Exception as e:
        log.warning(f"  Migration error for {label}: {e}")
        return 0
```

Every insert during migration uses `INSERT OR IGNORE`, so even if a migration were somehow run twice against the same data, duplicate primary keys are silently skipped rather than crashing. On a fresh install with no legacy files, all of this simply finds nothing and returns immediately — it costs nothing.


## The Shared Helpers

The rest of `db.py` is a handful of tiny helpers that every service uses so that time-stamping and JSON handling are done the same way everywhere:

| Helper | What it returns |
| --- | --- |
| `utcnow()` | The current time as a Coordinated Universal Time (UTC) string like `2026-08-12T14:30:00Z`. Every timestamp in the database is written with this, so logs and forms are consistent. |
| `jdump(obj)` | A JSON string for storing a list/object in a text column (used for things like a net's roster chips or a form's full data blob). |
| `jload(s, default)` | The reverse — parses a JSON text column back into Python, returning `default` if the column is empty or unparseable (never throws). |
| `row_to_dict(row)` / `rows_to_list(rows)` | Turn SQLite rows into plain dicts/lists, ready to hand straight to `json.dumps` for an Application Programming Interface (API) response. |

These look trivial, but they are why every service produces identical timestamp formats and stores JSON columns the same way. If you ever need to change how time is stamped or how JSON is stored, you change it here, once.


## Why It Matters / Design Takeaways

- *One front door.* Because all data access goes through `db.py`, the hard decisions (concurrency, WAL, foreign keys, timestamp format) are made once and shared by every service.
- *Safe to run on every boot.* `init_db()` uses `CREATE TABLE IF NOT EXISTS`, an idempotent migration list, and check-first seeders, so starting the app never damages an existing database — it only ever brings the schema forward.
- *Field-appropriate.* SQLite means the whole database is one file with no server to babysit; backups are a file copy; WAL keeps reads and writes smooth on a single Pi.
- *Forward-only migrations.* New columns are added by appending to the migrations list, never by editing the schema of a table that already ships — so a database created by any past version upgrades cleanly.

> **MAINTAINER'S RULE** — To change the stored data, change it in `db.py` and nowhere else. Add a table by extending the `SCHEMA` string; add a column by **appending** one `ALTER TABLE ... ADD COLUMN` line to the migrations list (never editing existing lines or the shipped `CREATE`); add starter data with a check-first seeder. Then confirm `init_db()` still runs cleanly against both a brand-new database and a copy of an old one before you consider the change done.


# 6. The Main API Server — fcc_lookup_server.py

*One Python file, python/fcc_lookup_server.py, is the main back end for the whole web interface. It listens on port 5050, serves station configuration, the roster and member photos, barcode/QR check-in lookups, offline QR images, printable ID cards, Federal Communications Commission (FCC) callsign lookups, and much more. Every page you see in the browser is talking to this one server.*

> **IN ONE SENTENCE** — `python/fcc_lookup_server.py` is a single-file Application Programming Interface (API) server on port 5050 that routes every browser request by its Uniform Resource Locator (URL) path to a block of code, reads or writes the database through `db.py`, and answers with either JSON or raw bytes — all bound to localhost and reached through nginx over Hypertext Transfer Protocol Secure (HTTPS).


## What This Is / What It Is For

If [python/db.py](python/db.py) is FieldCommand's data layer — the one front door to saved data — then [python/fcc_lookup_server.py](python/fcc_lookup_server.py) is the **main API server**: the program the web pages actually talk to. When an operator opens the roster page, checks someone in by scanning a barcode, saves the station's configuration, or prints member identification (ID) cards, the browser sends a request to this server and this server answers. Its file header states its job plainly: it is the *FieldCommand EmComm Main API Server — Port 5050*, with all runtime data stored in `fieldcommand.db` through `db.py`, and the separate read-only `fcc.db` used for FCC callsign lookups.

The name is historical — it began life as just an FCC callsign lookup — but it has grown into the primary service. In one file it serves station configuration, the member roster and each member's photo, the barcode and Quick Response (QR) code check-in lookup, an offline QR-code image generator, printable ID cards as a Portable Document Format (PDF) file, hospital and facility directories, the National Incident Management System (NIMS) resource-typing library, repeaters, nets and net traffic, map state, Incident Command System (ICS) forms, the dead-man's-switch state, and a pre-flight readiness check. This chapter does not tour every endpoint — it shows the shape of the file so any endpoint is easy to find and safe to change.

> **JARGON, IN PLAIN WORDS** — An **API** (Application Programming Interface) is just a set of URLs a program answers — the web page asks a question at a URL and gets data back. An **endpoint** is one of those URLs, like `/api/roster`. A **request handler** is the code that receives a request and decides what to do with it. **JSON** (JavaScript Object Notation) is the plain-text format the answers are written in.


## Why It Is Bound to Localhost — the 'Why' Behind the Address

The very last lines of the file are the most important lines for security, so they are worth reading first. The server binds to `127.0.0.1` — localhost — and not to the Pi's real network address:

```
if __name__ == "__main__":
    db.startup()
    threading.Thread(target=dms_monitor, daemon=True).start()
    log.info("FCC Lookup API server on port 5050")
    # Bind localhost only: the front end reaches this via nginx at /svc/5050 over
    # HTTPS, so the API is never exposed in cleartext on the LAN.
    HTTPServer(("127.0.0.1", 5050), Handler).serve_forever()
```

Binding to `127.0.0.1` means the operating system will only accept connections that come from the Pi itself. A laptop or phone on the field network **cannot** reach port 5050 directly. Instead, the browser talks to nginx (the web server) over HTTPS, and nginx forwards the request internally to `127.0.0.1:5050` at the path `/svc/5050`. That single decision does two jobs at once: it keeps the API off the local area network (LAN) in cleartext, and it puts nginx in front as the one place where HTTPS, and therefore the encryption that protects **personally identifiable information (PII)** like member names, phones, and photos, is handled. The API server itself never has to speak HTTPS — it trusts that anything reaching it already came through nginx.

> **NEVER MOVE THIS OFF LOCALHOST** — Do not change `127.0.0.1` to `0.0.0.0` to 'make it reachable.' That would expose the entire API — roster PII, photos, config, everything — as unencrypted plain Hypertext Transfer Protocol (HTTP) on the field network. The correct way to reach it from another device is always through nginx over HTTPS. If a page cannot reach an endpoint, fix the nginx route, not the bind address.

Two more things happen at startup, in order. First `db.startup()` runs — that is the data layer creating and upgrading the schema and importing any legacy JSON, covered in the previous chapter. Then a background thread starts running `dms_monitor()`, the per-net dead-man's-switch watcher, as a **daemon** thread so it dies automatically when the server stops. Only after both are set up does the server begin serving requests.


## How It Works — One Handler, Routed by Path

All the request handling lives in one class, `Handler`, which extends Python's built-in `BaseHTTPRequestHandler`. The base class calls a method named after the Hypertext Transfer Protocol (HTTP) method of each request: a browser GET calls `do_GET`, a save calls `do_POST`, a delete calls `do_DELETE`, and a browser pre-check calls `do_OPTIONS`. Inside each of those methods, the code is one long `if / elif` chain that compares the request's URL path against known endpoints and runs the matching block. The GET method sets this pattern up at the top:

```
def do_GET(self):
    parsed = urlparse(self.path)
    path   = parsed.path.rstrip("/")
    qs     = parse_qs(parsed.query)
    c      = get_conn()

    if path == "/api/fcc":
        call = qs.get("call",[""])[0]
        if not call: return self.send_json({"error":"Missing call"},400)
        r = fcc_lookup(call)
        return self.send_json(r) if r else self.send_json({"error":"Not found"},404)
```

Three habits in that opening repeat in every handler and are worth naming. The path is normalized with `.rstrip("/")` so `/api/roster` and `/api/roster/` are treated the same. The query string is parsed once into `qs`, and because `parse_qs` returns a list for every parameter, values are pulled out with the `qs.get("call",[""])[0]` idiom — 'give me the first value, or empty string if it is missing.' And a thread-local database connection `c` is fetched once at the top with `get_conn()`, so the whole handler shares one connection. Some endpoints match on an exact path; others, like the per-net routes, match with `path.startswith("/api/nets/")` and then split the path to pull out an identifier:

```
elif path.startswith("/api/nets/"):
    parts  = path.split("/"); net_id = parts[3] if len(parts)>3 else ""
    sub    = "/".join(parts[4:]) if len(parts)>4 else ""
```

> **JARGON, IN PLAIN WORDS** — A **query string** is the part of a URL after the `?`, like `?call=W8EOC`. A **path parameter** is an identifier baked into the path itself, like the `net-123` in `/api/nets/net-123`. **CORS** (Cross-Origin Resource Sharing) is the browser's rule about which pages may call which servers; the `cors()` helper adds the headers that tell the browser 'this is allowed.'


## How It Works — The Two Reply Helpers

Almost every endpoint ends by calling one of two helpers. `send_json` is the workhorse: it serializes a Python object to JSON, sets the content type and length, adds the CORS headers, and writes the body. The `default=str` argument means any value JSON does not natively understand (a date, for example) is turned into a string instead of crashing the response:

```
def send_json(self, obj, code=200):
    body = json.dumps(obj, default=str).encode()
    self.send_response(code)
    self.send_header("Content-Type","application/json")
    self.send_header("Content-Length",len(body))
    self.cors(); self.end_headers(); self.wfile.write(body)
```

The second helper, `send_bytes`, exists because not everything the server returns is JSON. QR images, member photos, and the ID-card PDF are raw binary. `send_bytes` takes the bytes and a content type, allows extra headers (used for caching and file-download names), and — importantly — wraps the actual write in a `try/except` so that a browser hanging up mid-download does not throw an unhandled error:

```
def send_bytes(self, data, content_type, code=200, extra=None):
    self.send_response(code)
    self.send_header("Content-Type", content_type)
    self.send_header("Content-Length", len(data))
    if extra:
        for k, v in extra.items():
            self.send_header(k, v)
    self.cors(); self.end_headers()
    try:
        self.wfile.write(data)
    except Exception:
        pass
```

Because these two helpers do all the response plumbing, the endpoint code stays short: fetch or write data, then hand a Python object to `send_json` or raw bytes to `send_bytes`. That is why a 1,300-line file with dozens of endpoints is still readable — every endpoint follows the same tiny shape.


## How It Works — The Roster, Labels, and the Hidden Photo

The roster is the richest example of the server doing real translation between what the database stores and what the web page wants. The database stores certifications and equipment as separate yes/no columns, but the roster page speaks in human labels like `ICS-100` and `VARA HF`. Two lists and two label maps at the top of the file are the single source of truth for that translation:

```
CERT_COLS  = ["ics100","ics200","ics300","ics400","ics700","ics800",
              "emcomm1","emcomm2","cpr","first_aid","cert"]
EQUIP_COLS = ["hf","vhf","digital","packet","pactor","vara_hf","vara_fm",
              "aprs","winlink","go_box","generator","battery","vehicle"]
CERT_LABELS  = {"ics100":"ICS-100", ... "cert":"CERT"}
EQUIP_LABELS = {"hf":"HF", ... "vehicle":"Vehicle"}
```

The function `member_to_dict` turns one database row into the object the page receives. It does three jobs worth calling out. First, it **never ships the photo blob** in list or detail JSON — photos can be large, so it replaces the raw image with a simple `has_photo` boolean flag and drops the blob and its mime type entirely. Second, it rebuilds the `certifications` and `equipment` objects using the label maps, so the page gets `{"ICS-100": true, ...}` instead of raw column names. Third, it computes a `display_id` with a clear priority — callsign, then radio identifier, then member identifier:

```
def member_to_dict(row):
    if row is None: return None
    d = dict(row)
    # Photos can be large; never ship the Base64 blob in list/detail JSON.
    # Expose only a flag — the actual image is served by GET /api/roster/photo.
    d["has_photo"] = bool(d.get("photo_data"))
    d.pop("photo_data", None); d.pop("photo_mime", None)
    d["certifications"] = {CERT_LABELS[c]:  bool(d.pop(f"cert_{c}", 0))  for c in CERT_COLS}
    d["equipment"]      = {EQUIP_LABELS[e]: bool(d.pop(f"equip_{e}", 0)) for e in EQUIP_COLS}
    d["display_id"] = (d.get("callsign") or d.get("radio_id") or
                       d.get("member_id") or d.get("id",""))
```

The reverse direction — saving a member — is handled by `member_upsert_sql` and `member_vals`, which accept **either** the database key (`ics100`) **or** the label (`ICS-100`) for each flag, so a page can post in whichever form it has. Normalizing at this API boundary is what keeps certifications and equipment from silently failing to save, and it is why the mapping lives in exactly one file.

> **JARGON, IN PLAIN WORDS** — A **blob** is a chunk of binary data — here, an image — stored in a database column. An **upsert** is 'insert or update': one statement that creates the row if it is new and updates it if it already exists. **Base64** is a way of writing binary data (like a photo) as plain text so it can travel inside JSON.


## How It Works — Barcode and QR Check-In Lookup

The check-in lookup is the endpoint that makes a scanner useful. A volunteer scans a badge and the browser calls `GET /api/barcode_lookup?code=XXXX`; the server answers with everything needed to auto-fill the check-in form. It tries the scanned code against four columns in turn — barcode, member identifier, callsign, then radio identifier — and stops at the first match:

```
elif path == "/api/barcode_lookup":
    code = qs.get("code",[""])[0].strip().upper()
    if not code:
        return self.send_json({"found":False,"error":"No code provided"},400)
    row = None
    for col in ["barcode_id","member_id","callsign","radio_id"]:
        row = c.execute(
            f"SELECT * FROM roster WHERE UPPER({col})=? AND {col}!='' LIMIT 1",
            (code,)
        ).fetchone()
        if row:
            break
```

The clever part is the fallback. If nobody on the roster matches and the scanned code **looks like a callsign** (checked with a regular expression for the amateur-radio callsign shape), the server looks the callsign up in the FCC database so that a visiting ham who was never entered on the roster still gets their name auto-filled. The reply is tagged `"source":"fcc"` and `"on_roster":false` so the page knows this came from the license database, not the local roster:

```
if re.fullmatch(r"[A-Z0-9]{1,3}[0-9][A-Z]{1,3}", code):
    fcc = fcc_lookup(code)
    if fcc and fcc.get("name"):
        return self.send_json({
            "found": True, "source": "fcc", "on_roster": False,
            "name": fcc["name"], "callsign": code,
            "member_type": "visitor",
            "suggested_position": "Amateur Radio Operator",
        })
```

When a roster member does match, the reply includes a `suggested_position` derived from their role by the small `_suggest_position` helper (a commander maps to Incident Commander, a safety role to Safety Officer, and so on), and it fills the agency field from the member's own visitor agency or, if blank, from the deploying organization's short name via `_org_short(c)`.


## How It Works — The Recent Additions

Four newer endpoints share a theme: they make the appliance work fully offline and stop it from hardcoding one agency's name. The first is the **offline QR image**. FieldCommand used to fetch QR codes from a Google charts URL — a dependency that is now dead and, worse, needs the internet. The `qr_svg` helper replaces it by drawing the QR code locally with ReportLab and returning it as Scalable Vector Graphics (SVG) text:

```
def qr_svg(data, size_px=220):
    """Render `data` as a scannable QR code and return it as an SVG string.
    Generated locally with ReportLab — no internet, no external service. This is
    what replaces the old (now-dead) chart.googleapis.com dependency."""
    from reportlab.graphics.barcode.qr import QrCodeWidget
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics import renderSVG
    q = QrCodeWidget(str(data), barLevel="M")
    x1, y1, x2, y2 = q.getBounds()
    w = (x2 - x1) or 1
    h = (y2 - y1) or 1
    d = Drawing(size_px, size_px)
    d.transform = [size_px / w, 0, 0, size_px / h, -x1 * size_px / w, -y1 * size_px / h]
    d.add(q)
    return renderSVG.drawToString(d)
```

The `GET /api/qr?data=XXXX` endpoint calls it and returns the SVG with `send_bytes` under the content type `image/svg+xml`, along with a `Cache-Control: no-store` header so a QR image is never cached against the wrong data. The second addition is the **member photo endpoint**. Because `member_to_dict` deliberately strips the photo out of roster JSON, the image needs its own route. `GET /api/roster/photo?id=<mid>` reads the stored Base64, decodes it back to real image bytes, handles the case where the stored value is a full `data:` URL, and streams it out:

```
elif path == "/api/roster/photo":
    mid = qs.get("id",[""])[0]
    if not mid:
        return self.send_json({"error":"missing id"},400)
    row = c.execute("SELECT photo_data,photo_mime FROM roster WHERE id=?",
                    (mid,)).fetchone()
    if not row or not row["photo_data"]:
        return self.send_json({"error":"no photo"},404)
    ...
    img = _b64.b64decode(raw)
    return self.send_bytes(img, mime, extra={"Cache-Control":"no-store"})
```

Photos are also **saved** on their own route, `POST /api/roster/photo`, kept separate from the member upsert on purpose so that an ordinary edit of a member's details can never accidentally wipe their photo. The third addition is **printable ID cards**. `GET /api/id_cards.pdf` generates member badges on demand — all eligible members, or one member with `?id=<mid>` — by handing off to a separate `gen_id_cards` module and streaming the resulting PDF back:

```
elif path == "/api/id_cards.pdf":
    mid = qs.get("id",[""])[0] or None
    backs = qs.get("backs",["1"])[0] not in ("0","false","no")
    ...
    _gen.generate_from_db(out_path=out, only_id=mid, backs=backs)
    with open(out,"rb") as f:
        data = f.read()
    return self.send_bytes(data, "application/pdf",
        extra={"Content-Disposition":"inline; filename=member_id_cards.pdf"})
```

The fourth addition is the smallest but matters most for reuse: `_org_short(c)`. FieldCommand is meant to be deployed by any agency, so an agency name must never be baked into the code. This helper reads the deploying organization's short name from the station configuration and returns an empty string — never a hardcoded agency — if it is not set:

```
def _org_short(c):
    """The deploying organization's short name from Setup (agency-neutral).
    Empty string if not configured — never a hardcoded agency."""
    try:
        row = c.execute("SELECT org_short FROM station_config WHERE id=1").fetchone()
        return (row["org_short"] or "") if row else ""
    except Exception:
        return ""
```

> **AGENCY-NEUTRAL IS A HARD RULE** — The whole point of `_org_short` is that FieldCommand ships to any agency and reads its identity from Setup. Never reintroduce a hardcoded agency name, callsign, or logo in this file to 'fill in a blank.' If a value should default to the deploying organization, read it from `station_config`, and let it be empty when Setup has not filled it in.


## The Rest of the Endpoints, at a Glance

The same handler serves many more endpoints in exactly the shapes shown above. This table is a map, not an exhaustive reference — read the matching `if` block in the source for the full behavior:

| Path | Method(s) | What it serves |
| --- | --- | --- |
| `/api/fcc`, `/api/fcc/search`, `/api/fcc/status` | GET | FCC callsign lookup, advanced search, and database freshness — all reading the separate read-only `fcc.db`. |
| `/api/config` | GET / POST | The station's own configuration: callsign, organization, location, logo, module toggles, Wi-Fi, and more. |
| `/api/roster`, `/api/roster/members`, `/api/roster/activations` | GET / POST / DELETE | The member roster, individual member upserts, and check-in activations. |
| `/api/roster/promote`, `/api/roster/import` | POST | Promote a walk-in/visitor onto the roster; bulk-import members. |
| `/api/nets`, `/api/nets/<id>/...` | GET / POST / DELETE | Nets, their check-in entries and traffic, plus open/close/checkout, with automatic ICS-211 check-in-list sync. |
| `/api/position` | GET | Live station position from the GPS daemon, falling back to the configured or default location. |
| `/api/hospitals`, `/api/facilities`, `/api/resource_types`, `/api/repeaters` | GET / POST / DELETE | The reference directories: hospitals (with an optional live CMS import), facilities, NIMS resource types, and repeaters. |
| `/api/mapstate`, `/api/resmap` | GET / POST | Saved map shapes and markers for the incident map and the resource map. |
| `/api/forms`, `/api/forms/<id>` | GET / POST / DELETE | Generic ICS/other form storage — the data blob is stored and re-expanded on read. |
| `/api/dms`, `/api/dms/arm|reset|disarm` | GET / POST | Per-net dead-man's-switch state, armed and watched by the `dms_monitor` background thread. |
| `/api/preflight` | GET | The go/no-go readiness check across services, databases, GPS, Wi-Fi, and setup. |
| `/wan/status`, `/amprgate/status`, `/api/status` | GET | Status files written by sibling monitor scripts, plus a simple health ping. |


## Why It Matters / Design Takeaways

- *One file, one shape.* Every endpoint is a block in a path-matched `if/elif` chain that fetches or writes through `db.py` and answers with `send_json` or `send_bytes`. Learn that shape once and any endpoint is easy to find and safe to extend.
- *Localhost plus nginx is the security boundary.* The server binds to `127.0.0.1` and trusts nginx to handle HTTPS and reach it at `/svc/5050`, so PII never crosses the LAN in cleartext. The bind address is not a knob to turn.
- *Translate at the boundary.* The roster maps database columns to human labels in one place, hides the photo blob behind a `has_photo` flag, and accepts either form on save — so the page and the schema can each speak their own language.
- *Offline and agency-neutral by design.* Recent work replaced an internet QR dependency with a local ReportLab generator, split photo and ID-card delivery into their own byte endpoints, and swapped a hardcoded agency for `_org_short` read from Setup.

> **MAINTAINER'S RULE** — Add an endpoint by adding one `if/elif` branch to the matching `do_GET`/`do_POST`/`do_DELETE` method, reading and writing only through the `get_conn()` connection and replying only through `send_json` or `send_bytes`. Keep the server bound to `127.0.0.1` — reach it through nginx, never by opening the bind address. Never ship a photo blob in list JSON, and never hardcode an agency name: read identity from `station_config` via `_org_short`. Any label/column mapping belongs in the `CERT_*`/`EQUIP_*` tables at the top of the file, nowhere else.


# 7. Building the FCC Database — build_fcc_db.py

*One standalone script, python/build_fcc_db.py, turns the Federal Communications Commission's giant public license dump into a single searchable file, fcc.db. It runs by hand, never from the app, and produces the read-only database the main server uses to look up any United States amateur radio operator by callsign, name, or state.*

> **IN ONE SENTENCE** — `python/build_fcc_db.py` downloads the Federal Communications Commission (FCC) amateur license dump, parses its pipe-delimited files, and loads roughly 800,000 records into a self-contained `fcc.db` that the app only ever reads — so an operator with no internet can still identify any United States ham by callsign.


## What This Is / What It Is For

When a station checks into a net, the operator wants to see who is behind the callsign — the licensee's name, their city and state, their license class. That information is public and it lives in the FCC's **Universal Licensing System (ULS)** database. But the ULS is an online system, and FieldCommand is built to run in a field with no internet. So FieldCommand ships its own copy of the amateur portion of that data, packaged as a single SQLite file called `fcc.db`, and it ships a script that builds that file: [python/build_fcc_db.py](python/build_fcc_db.py).

The script has one job. It takes the FCC's official bulk download — a ZIP file named `l_amat.zip` that contains the entire United States amateur radio license roster — and transforms it into a fast, indexed database the main server can search in milliseconds. It is run **by a person**, on a bench with internet, before the appliance is deployed or when the operator wants fresher data. It is never invoked by the running application, and the application never writes to the file it produces. That one-way relationship is the whole design, and everything below follows from it.

> **JARGON, IN PLAIN WORDS** — The **Federal Communications Commission (FCC)** is the United States agency that licenses radio operators. Its **Universal Licensing System (ULS)** is the public database of every license. A **bulk data dump** is a big downloadable file containing the whole database at once, instead of you querying it one record at a time. **Pipe-delimited** means the columns in each line are separated by the `|` character instead of commas. **SQLite** is a database that is just a single file on disk — no server to run.


## Why It Is a Separate File — the 'Why' Behind the Design

FieldCommand keeps all its live incident data — nets, check-ins, forms, the roster — in one database, `fieldcommand.db`, described in the data-layer chapter. The FCC data deliberately does **not** go in there. It gets its own file, `fcc.db`, for three concrete reasons, and each one traces back to how the two datasets differ.

| Reason | Live incident data (fieldcommand.db) | FCC license data (fcc.db) |
| --- | --- | --- |
| Size | Small — kilobytes to a few megabytes for a whole incident. | Huge — hundreds of megabytes for ~800,000 records with three tables. |
| Who writes it | The app, constantly, from many threads. | Nobody. It is built once by a script and only ever read after that. |
| How you refresh it | Never rebuilt — it grows as the incident runs. | Rebuilt wholesale by re-running the script against a newer FCC dump. |

Mixing the two would be a mistake. A backup of a running incident should be a tiny, fast file copy — if the ~800,000-record reference table were inside it, every backup would drag hundreds of megabytes of unchanging government data along with it. Keeping `fcc.db` separate means the incident database stays small and quick to copy, while the reference database can be swapped out and rebuilt independently without touching a single byte of live data. The script writes to a fixed default path that sits alongside the main data but stands on its own:

```
FCC_URL = "https://data.fcc.gov/download/pub/uls/complete/l_amat.zip"
DEFAULT_ZIP = "/opt/fieldcommand/data/l_amat.zip"
DEFAULT_DB  = "/opt/fieldcommand/data/fcc.db"
```

> **WHY REBUILD-ONLY MATTERS** — Because the app never writes to `fcc.db`, the server can open it read-only and never worry about locking, corruption from a half-finished write, or migrations. The file is a fixed, known-good artifact. All the complexity of building it is contained in this one script, run at a time when a human is watching — not at 2 a.m. in a shelter.


## How It Works — Getting the Source Data

The script can supply its own input. If the ZIP file is not already on disk (or the operator passes `--download` to force a fresh copy), it fetches the current dump straight from the FCC. This is the one moment the tool needs internet, and it is why the tool is run on a bench beforehand rather than in the field. The download prints a live percentage so the person watching knows it is working, because the file is large:

```
def download_fcc(zip_path):
    print(f"Downloading FCC ULS database from {FCC_URL}")
    print("This file is ~200MB and may take several minutes...")
    Path(zip_path).parent.mkdir(parents=True, exist_ok=True)
    def progress(count, block, total):
        pct = min(100, count * block * 100 // total) if total and total > 0 else 0
        print(f"\r  {pct}% ({count*block//1024//1024}MB/{total//1024//1024}MB)", end="", flush=True)
    urllib.request.urlretrieve(FCC_URL, zip_path, reporthook=progress)
```

The decision of whether to download at all is made in `main()`. It is deliberately forgiving: if you point it at a ZIP that already exists, it uses that file and skips the network entirely, so a rebuild from a saved dump needs no internet. Only a missing file or an explicit `--download` triggers the fetch:

```
    if args.download or not zip_path.exists():
        if not zip_path.exists():
            print(f"ZIP not found at {zip_path}, downloading...")
        download_fcc(str(zip_path))

    build_db(str(zip_path), args.db)
```

Inside the ZIP are many `.DAT` files — one per kind of ULS record. FieldCommand only needs three of them, so the extractor pulls exactly those three and ignores the rest. This keeps the temporary working directory small and the load fast:

```
    with zipfile.ZipFile(zip_path) as z:
        names = z.namelist()
        for name in names:
            if name.upper() in ("EN.DAT","HD.DAT","AM.DAT"):
                print(f"  Extracting {name}...")
                z.extract(name, tmp_dir)
```

| File | What it holds | Why FieldCommand wants it |
| --- | --- | --- |
| `EN.DAT` | Entity records — the licensee's name, address, city, state, ZIP. | This is the core 'who is this callsign' answer. It is the only file treated as required. |
| `HD.DAT` | License header — status (active/expired/cancelled) and key dates. | Lets the app show whether a license is currently valid. |
| `AM.DAT` | Amateur-specific detail — operator class (Technician, General, Extra), region. | Shows the operator's privileges/class next to their name. |

`EN.DAT` is the only file the script insists on. If it is missing, the build stops immediately, because a database with no names would be useless. The other two are optional — if they are absent the script warns and carries on, producing a database that still answers 'who is this' but without status or class:

```
    if not en_file:
        print("ERROR: EN.DAT not found in ZIP")
        sys.exit(1)
```


## How It Works — The Tables and the Clever Callsign Column

The build creates three tables that mirror the three files: `en`, `hd`, and `am`. Each has `unique_system_id` as its primary key — the ULS's own stable identifier that ties an entity, a header, and an amateur record together for the same license. The `en` table carries one detail worth calling out, because it is what makes callsign search fast and case-proof:

```
        CREATE TABLE IF NOT EXISTS en (
            record_type TEXT,
            unique_system_id TEXT PRIMARY KEY,
            ...
            call_sign TEXT,
            callsign TEXT GENERATED ALWAYS AS (UPPER(call_sign)) VIRTUAL,
            ...
        )
```

There are two columns for the callsign. `call_sign` holds the raw value exactly as the FCC supplied it. `callsign` is a **generated column** — the database computes it automatically as the upper-cased version of `call_sign`, and it is never stored on disk (`VIRTUAL`). This means the app can search for a callsign without caring whether the user typed `ke4con`, `Ke4Con`, or `KE4CON`; the query matches against the always-upper-case `callsign` column and always finds the record. The operator never has to think about case, and there is no second copy of the data to keep in sync.

> **JARGON, IN PLAIN WORDS** — A **generated column** is a column whose value the database calculates from other columns instead of you storing it. `GENERATED ALWAYS AS (UPPER(call_sign)) VIRTUAL` tells SQLite: 'whenever anyone reads `callsign`, hand them the upper-cased `call_sign` — don't waste disk space storing it.' A **primary key** is the column that uniquely identifies each row. An **index** is a lookup structure that lets the database jump straight to matching rows instead of scanning all 800,000.

Immediately after the tables, the script builds three indexes on `en`. Without them, every callsign lookup would read the entire table; with them, a lookup is near-instant. The indexes match exactly the three ways the app searches — by callsign, by state, and by last name:

```
    conn.execute("CREATE INDEX IF NOT EXISTS idx_en_callsign ON en(callsign)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_en_state ON en(state)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_en_last ON en(last_name)")
```


## How It Works — Loading 800,000 Records Without Melting the Pi

The load is the heart of the script. Each `.DAT` file is plain text with fields separated by the pipe character, so the parser is Python's built-in CSV reader told to use `|` as the delimiter. Two details make it robust against messy government data. First, the files are read as `latin-1` with `errors="replace"`, so an odd byte in an address never crashes the whole import. Second, every row is padded to the exact column count before insert, so a line that is missing its trailing fields still loads cleanly:

```
        with open(filepath, "r", encoding="latin-1", errors="replace") as f:
            reader = csv.reader(f, delimiter="|")
            for row in reader:
                # Pad row to column count
                padded = (row + [""] * len(insert_cols))[:len(insert_cols)]
                batch.append(padded)
```

The generated `callsign` column is not something the script inserts — the database fills it in. So before building the insert statement, the loader reads the table's real columns and drops the generated one from the list, so the number of placeholders matches the number of values it actually supplies:

```
        cols = [row[1] for row in conn.execute(f"PRAGMA table_info({table})")]
        # Remove generated columns
        insert_cols = [c for c in cols if c != "callsign"]
        placeholders = ",".join("?" * len(insert_cols))
        sql = f"INSERT OR REPLACE INTO {table} ({','.join(insert_cols)}) VALUES ({placeholders})"
```

Rows are not inserted one at a time — that would be painfully slow for 800,000 of them. They are collected into batches of 10,000 and written in a single `executemany` call, then committed, then the batch is cleared. This is the single biggest reason the build finishes in a reasonable time on a Raspberry Pi:

```
        batch = []
        BATCH_SIZE = 10000
        ...
                if len(batch) >= BATCH_SIZE:
                    conn.executemany(sql, batch)
                    conn.commit()
                    batch = []
        if batch:
            conn.executemany(sql, batch)
            conn.commit()
```

The database connection itself is tuned for one-time bulk writing, not for the careful concurrent access the live app needs. Because nothing else is touching this file while it builds, the script can safely turn `synchronous` off and hand SQLite a large cache — settings you would never use on the live incident database, but which are exactly right for a throwaway build that will be atomically swapped into place at the end:

```
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("PRAGMA cache_size=-64000")
```


## How It Works — Swapping In the New File Safely

The whole build never writes directly to the final `fcc.db`. It builds into a temporary file (`fcc.db.tmp`), and only at the very end, once every record is loaded and the connection is closed, does it move the finished file into place. If an existing `fcc.db` is there, it is renamed to `.bak` first — so a failed or interrupted build can never leave the operator with a corrupt or half-written database, and there is always a backup of the previous good copy:

```
    conn.close()

    # Replace old db with new
    if db_path.exists():
        db_path.replace(str(db_path) + ".bak")
    Path(tmp_db).replace(db_path)
```

> **WHY THE .tmp / .bak DANCE IS NON-NEGOTIABLE** — A rename on the same filesystem is atomic — it either fully happens or does not happen at all. Building into `fcc.db.tmp` and renaming last means the live `fcc.db` is only ever replaced by a complete, finished file. Never 'simplify' this by having the script write straight into `fcc.db`; an interrupted build would then destroy the working database an operator may be depending on.


## How the Main API Uses the Result

From the running server's side, all of the above is invisible. The application opens `fcc.db` read-only and issues simple `SELECT` queries against the indexed columns — matching an upper-cased callsign against the generated `callsign` column, or filtering `en` by `state` or `last_name`, and joining to `hd` and `am` on `unique_system_id` for status and class. Because the file is never written by the app, there is no locking to coordinate and no migration ever to run: the database is a fixed reference the API simply reads. This is the payoff of keeping the build in its own script — the query path stays trivially simple precisely because all the hard work happened once, ahead of time, in `build_fcc_db.py`.


## Why It Matters / Design Takeaways

- *Reference data is not app data.* The ~800,000-record FCC roster is huge, rebuild-only, and never written by the app, so it lives in its own `fcc.db` — keeping backups of live incident data small and fast.
- *Build offline, use offline.* The one moment internet is needed is the FCC download, done by a person on a bench. After that, an operator with no connectivity can still identify any United States ham.
- *Speed comes from three choices.* A generated upper-case `callsign` column makes search case-proof, three indexes make lookups instant, and 10,000-row batches make the load finish on a Pi.
- *Atomic swap protects the operator.* Building into `.tmp`, backing up the old file to `.bak`, and renaming last means an interrupted build can never corrupt the working database.

> **MAINTAINER'S RULE** — `build_fcc_db.py` is a bench tool, not part of the running app — keep it that way. Never call it from the server, and never make the server write to `fcc.db`. If you add a ULS file or column, extend the relevant `CREATE TABLE` and let the padding/`insert_cols` logic carry it — do not remove the generated `callsign` column or the `.tmp`/`.bak` rename. After any change, run a full build and confirm the finished `fcc.db` opens and a known callsign (case-insensitively) returns the right name, status, and class before you consider it done.


# 8. The ICS Platform Server — ics_platform_server.py

*One Python file, python/ics_platform_server.py, is the whole Incident Command System (ICS) back end. It listens on port 5055, bound to the machine itself, and answers every request about incidents, operational periods, ICS forms, T-cards and resources, check-ins, the activity feed, and meetings. Everything an incident produces flows through this one service.*

> **IN ONE SENTENCE** — `python/ics_platform_server.py` is a single localhost-only web service on port 5055 that routes every Incident Command System (ICS) request with a plain `if/elif` chain, stores all ICS forms as one flexible JavaScript Object Notation (JSON) blob per form, and keeps the incident, its people, and its paperwork in sync through the shared `db.py` data layer.


## What This Is / What It Is For

FieldCommand runs three small web services side by side on the Raspberry Pi. This chapter is about the second of them: the **Incident Command System (ICS) platform server**, the file [python/ics_platform_server.py](python/ics_platform_server.py). Where the main server handles nets, the roster, and the Federal Communications Commission (FCC) callsign lookups, this service owns everything to do with running an incident by the book: creating the incident record, advancing operational periods, saving the ICS forms (the 201, 202, 205, 211, 213, 214, and more), tracking resources on a T-card board, taking personnel check-ins, writing the live activity feed, and scheduling the Planning Section's meetings.

It is one class, `ICSHandler`, on top of Python's built-in `http.server`. There is no web framework, no router library, and no object-relational mapper. A request comes in, one long `if/elif` chain matches the URL path, a few lines of SQL run against the shared database, and a JSON reply goes back. That plainness is deliberate: a volunteer maintainer can read the whole request lifecycle top to bottom without learning a framework first. The service announces itself the same way every time it boots:

```
if __name__ == "__main__":
    db.startup()
    log.info("ICS Platform API on port 5055")
    # Localhost only — reached via nginx at /svc/5055 over HTTPS.
    HTTPServer(("127.0.0.1", 5055), ICSHandler).serve_forever()
```

> **JARGON, IN PLAIN WORDS** — The **Incident Command System (ICS)** is the standard way United States responders organize a scene — who is in charge, who reports to whom, and which paper form records what. An **operational period** is one work shift of the incident (often 12 hours); each period gets its own plan. A **T-card** is the classic pocket-sized card that tracks one resource (a crew, an engine, a person) as it moves across a status board. An **Incident Action Plan (IAP)** is the packet of ICS forms that spells out the plan for one operational period.


## Why localhost-only, behind nginx — the 'Why' Behind the Binding

The very last line binds the server to `127.0.0.1`, the machine's own loopback address, not to `0.0.0.0`. That single choice means **nothing on the network can reach port 5055 directly** — only code already running on the Pi can. Field tablets and laptops never talk to this service straight; they talk to nginx, the web server out front, which holds the Hypertext Transfer Protocol Secure (HTTPS) certificate and forwards `/svc/5055/...` requests inward to this process. So the transport encryption, the single public port, and any access rules live in one place (nginx), and this service stays small and trusting because the only clients that can reach it are local.

That is also why the Cross-Origin Resource Sharing (CORS) headers are wide open. Every response calls `self.cors()`, which allows any origin. On a service exposed to the internet that would be reckless; here it is fine, because the service is not exposed to the internet — nginx is the only door, and it is the one that decides who gets in:

```
def cors(self):
    self.send_header("Access-Control-Allow-Origin","*")
    self.send_header("Access-Control-Allow-Headers","Content-Type")
    self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")
```

> **JARGON, IN PLAIN WORDS** — **localhost / 127.0.0.1** is the address a computer uses to talk to itself; nothing outside the machine can connect to it. **nginx** is a web server that sits in front, terminates HTTPS, and passes requests along to internal services — a **reverse proxy**. **CORS** is a browser rule about which web pages may call which servers; opening it wide is safe only because this server is unreachable from the outside.


## How It Works — The Plain if/elif Router

There is no route table. Each HyperText Transfer Protocol (HTTP) verb has one method — `do_GET`, `do_POST`, `do_DELETE` — and each opens the same way: parse the URL, split off the path, grab the query string, and get a database connection. From there a chain of `if path == ...` / `elif path.startswith(...)` branches picks the handler. The top of `do_GET` shows the shape the whole file follows:

```
def do_GET(self):
    parsed=urlparse(self.path); path=parsed.path.rstrip("/")
    qs=parse_qs(parsed.query); c=get_conn()

    if path == "/api/ics/incidents":
        return self.send_json(rows_to_list(
            c.execute("SELECT * FROM incidents ORDER BY started DESC").fetchall()))
```

Two habits keep this readable and safe. First, every branch ends by calling `send_json`, the one helper that serializes the reply, sets the length, and adds the CORS headers — so no branch can forget a header. Second, every value that reaches SQL is passed as a bound parameter (the `?` placeholders), never glued into the query string. When a whole set of columns must be named dynamically — as in a partial update — the column names come from a fixed in-code whitelist, not from the request body. The T-card save shows that pattern: only names in `TC_COLS` may be written, so a crafted request cannot inject a column name.

```
TC_COLS=["incident_id","resource_id","resource_name","resource_type","category",
         "type","status","assignment","leader","contact","num_personnel","eta",
         "notes","order_number","home_agency","period","daily_cost","hourly_rate",
         "cost_basis","hours_on_incident"]
if c.execute("SELECT 1 FROM ics_tcards WHERE id=?",(cid,)).fetchone():
    # Partial update — only overwrite fields actually provided so a status-only
    # move never wipes leader/contact/personnel/notes/cost on the card.
    present=[k for k in TC_COLS if k in body]
    sets=",".join(f"{k}=?" for k in present)+(", " if present else "")+"updated=?"
    vals=[body[k] for k in present]+[now,cid]
    c.execute(f"UPDATE ics_tcards SET {sets} WHERE id=?",vals)
```

> **PARTIAL UPDATES ARE ON PURPOSE** — The T-card branch only writes the fields the request actually sent. This matters on a status board: when someone drags a card from Available to Assigned, the request carries only the new status, and the leader, contact, personnel count, notes, and cost must survive untouched. If you ever rewrite this to a full-row `INSERT OR REPLACE`, a one-field move will silently blank every other field. Keep partial updates partial.

Creating an incident is the anchor operation the rest of the system hangs off. The `POST /api/ics/incidents` branch mints an identifier, inserts the incident row, immediately creates operational period 1 with the chosen shift length, commits, and writes the first line of the activity feed — all in one handler:

```
if path == "/api/ics/incidents":
    inc_id=body.get("id") or f"inc-{int(time.time()*1000)}"
    c.execute("""INSERT INTO incidents
        (id,name,type,status,jurisdiction,incident_commander,
         location,summary,incident_number,current_period,started)
        VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
        (inc_id,body.get("name",""),body.get("type",""),
         "active",body.get("jurisdiction",""),
         body.get("incident_commander",""),body.get("location",""),
         body.get("summary",""),body.get("incident_number",""),1,now))
    # Create period 1 — persist the chosen Operational Period Duration
    try: shift_hours = int(body.get("period_hours") or 12)
    except (TypeError, ValueError): shift_hours = 12
    c.execute("INSERT INTO ics_periods(id,incident_id,period_num,started,shift_hours) VALUES(?,?,?,?,?)",
              (f"per-{inc_id}-1",inc_id,1,now,shift_hours))
    c.commit()
    log_activity(inc_id,"Command","Incident Created",body.get("name",""))
```

That `log_activity` call appears after almost every write in the file — incident created, period advanced, form saved, T-card updated, meeting scheduled. It is a two-line helper that appends one timestamped row to `activity_log`, and it is what powers the live activity feed the dashboard shows. Because every mutating branch calls it, the feed is a faithful running record of the incident without any branch needing special feed logic:

```
def log_activity(incident_id, section, action, detail):
    get_conn().execute(
        "INSERT INTO activity_log(incident_id,section,action,detail,timestamp)"
        " VALUES(?,?,?,?,?)",
        (incident_id, section, action, detail, utcnow()))
    get_conn().commit()
```


## How It Works — One Flexible Table for Every ICS Form

There are dozens of ICS forms, and no two have the same fields. The ICS-205 is a table of radio channels; the ICS-202 is a list of objectives; the ICS-214 is a running activity log. A traditional design would give each form its own table with its own columns — dozens of tables to define, migrate, and keep in step with the forms. FieldCommand does the opposite: **one** table, `ics_forms`, holds them all. The columns are only the handful common to every form; the entire body of the form lives in a single JSON text column named `data`:

```
CREATE TABLE IF NOT EXISTS ics_forms (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL DEFAULT '',
    form_type   TEXT NOT NULL,              -- ics201, ics202, ics205, etc.
    period      INTEGER DEFAULT 1,
    summary     TEXT DEFAULT '',
    data        TEXT NOT NULL DEFAULT '{}', -- full form JSON blob
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);
```

Saving any form is therefore one branch that works for all of them. The URL carries the form type (`/api/ics/forms/ics205`), the handler dumps the whole request body into `data` with `jdump`, and `INSERT OR REPLACE` means the same call both creates a new form and overwrites an existing one keyed by its `id`:

```
elif path.startswith("/api/ics/forms/"):
    form_type=path.split("/api/ics/forms/")[1].split("/")[0]
    fid=body.get("id") or f"{form_type}-{int(time.time()*1000)}"
    body.update({"id":fid,"form_type":form_type,"updated":now})
    body.setdefault("created",now)
    c.execute("""INSERT OR REPLACE INTO ics_forms
        (id,incident_id,form_type,period,summary,data,created,updated)
        VALUES(?,?,?,?,?,?,?,?)""",
        (fid,body.get("incident_id",""),form_type,body.get("period",1),
         body.get("summary",""),jdump(body),body.get("created",now),now))
    c.commit()
    log_activity(body.get("incident_id",""),form_type.upper(),"Form Saved",fid)
```

Reading a single form does the reverse: fetch the row, then merge the parsed `data` blob back up to the top level so the client sees a flat object with every field, common columns and form-specific fields together. The `jload` helper parses the JSON safely, returning an empty object rather than throwing if the column is somehow malformed:

```
fid=parts[1]
row=c.execute("SELECT * FROM ics_forms WHERE id=?",(fid,)).fetchone()
if row:
    d=dict(row); d.update(jload(d.get("data"),{}))
    return self.send_json(d)
```

> **WHY ONE FLEXIBLE TABLE WINS HERE** — Adding a brand-new ICS form, or a new field to an existing one, needs **zero** database changes — the form's shape lives entirely in the JSON `data` blob, so the front end can define a form and this server stores it without a schema edit or migration. The trade-off is that you cannot easily query *inside* a form with plain SQL (for example, filter forms by a field buried in the blob). FieldCommand accepts that trade because forms are almost always fetched whole, by incident and period; the few places that must reach inside a blob — like pulling channels out of a saved ICS-205 — parse the JSON in Python instead. If you find yourself needing to filter by an inside-the-blob field often, that is the signal to promote it to a real column, not to abandon the pattern.


## How It Works — general_info and Cross-Form Auto-Fill

Every ICS form repeats the same header: incident name, incident number, the operational period, the Incident Commander, the Command and General Staff, the weather, sunrise and sunset. Making a responder retype that on every form would be error-prone and slow. So FieldCommand keeps that shared header once, per incident and per period, in the `general_info` table, and lets every form draw from it. The primary key is literally the incident and period joined together, so there is exactly one header per period:

```
CREATE TABLE IF NOT EXISTS general_info (
    id                      TEXT PRIMARY KEY,  -- "{incident_id}-{period}"
    incident_id             TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    period                  INTEGER NOT NULL DEFAULT 1,
    incident_name           TEXT DEFAULT '',
    incident_number         TEXT DEFAULT '',
    ...
```

The clever part is the fallback on read. When a client asks for the general info of an incident and period that has no saved header yet — a brand-new incident, before anyone has filled the header in — the handler does not return an empty object. It falls back to the incident record itself and synthesizes a starter header from it, so the first form a responder opens is already pre-filled with the incident's name and location:

```
row = c.execute(
    "SELECT * FROM general_info WHERE incident_id=? AND period=?",
    (inc_id, period)).fetchone()
if row:
    return self.send_json(row_to_dict(row))
inc = c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()
if inc:
    d = row_to_dict(inc)
    d["incident_location"] = d.get("location","")
    d["operational_period_number"] = period
    return self.send_json(d)
```

Saving general info flows the other way, and it keeps two records honest at once. It writes the full header into `general_info`, and then it also updates the core `incidents` row with the handful of fields that live there too — name, Incident Commander, location, jurisdiction, ICS variant — so the incident list and the forms never disagree about the basics:

```
c.execute("""UPDATE incidents SET name=?, incident_commander=?,
    location=?, jurisdiction=?, ics_variant=?, updated=? WHERE id=?""",
    (body.get("incident_name",""),body.get("incident_commander",""),
     body.get("incident_location",""),body.get("jurisdiction",""),
     body.get("ics_variant","FEMA"),now, inc_id))
```


## How It Works — Check-In Writes Two Boards at Once

The scan page and the remote check-in page both post to the same endpoint, `POST /api/ics/checkin`. A person signs in once, but two things need to happen: they must appear on the ICS-211 sign-in roster (the `checkin_entries` table), **and** they must appear as a resource on the T-card board so command can see and move them. Rather than make the client do two calls and risk them drifting apart, the one handler does both. It writes the check-in row, then creates or refreshes a matching T-card keyed to the check-in's own identifier:

```
# Auto-populate the T-card board from the 211 sign-in (documented behavior:
# a check-in appears on BOTH the ICS-211 roster and the T-card board).
# Keyed to the check-in id so a re-check-in refreshes rather than duplicates,
# and any board movement already made (status/assignment) is preserved.
tc_id    = f"tc-ci-{ci_id}"
res_name = body.get("name","") or body.get("callsign_id","") or "Unknown"
if c.execute("SELECT 1 FROM ics_tcards WHERE id=?",(tc_id,)).fetchone():
    c.execute("""UPDATE ics_tcards SET incident_id=?, resource_name=?, ...
                 ... WHERE id=?""", ( ... , tc_id))
else:
    c.execute("""INSERT INTO ics_tcards ( ... ) VALUES( ... )""", ( ... ))
```

The deterministic key `tc-ci-{ci_id}` is what makes this safe to call repeatedly. Because the T-card identifier is derived from the check-in identifier, a second check-in by the same person updates the same card instead of creating a duplicate, and because the update branch deliberately does not touch `status` or `assignment`, any move command already made on the board survives the refresh. The response hands back both identifiers so the client knows about each record:

```
return self.send_json({"status":"ok","id":ci_id,"tcard_id":tc_id})
```

> **JARGON, IN PLAIN WORDS** — **ICS-211** is the incident check-in list — the roster of everyone who has signed in. A **deterministic key** is an identifier built by a fixed rule (here, `tc-ci-` plus the check-in id) so the same input always yields the same key; that is how a repeat check-in lands on the same T-card instead of spawning a new one. **INSERT OR REPLACE** is SQLite writing a row that either creates it or overwrites the existing one with the same primary key.


## Why It Matters / Design Takeaways

- *One service owns the whole incident.* Incidents, periods, forms, T-cards, check-ins, the activity feed, and meetings all live behind port 5055, so the rules about how an incident is stored and changed are in one file.
- *Safe because it is unreachable.* Binding to `127.0.0.1` and living behind nginx at `/svc/5055` is what lets the service stay small and open (wide CORS, no per-request auth) without being exposed — the network never touches it directly.
- *A flexible forms table beats dozens of rigid ones.* Storing every ICS form as a JSON blob in `ics_forms` means new forms and new fields need no database change; the cost is that you query forms whole, not by their inner fields.
- *Write the shared header once.* `general_info` holds the common form header per incident and period, auto-fills from the incident record when empty, and writes core fields back to `incidents` so nothing drifts.
- *Keep linked records in sync inside one handler.* A single check-in writes both the ICS-211 roster and the T-card board, keyed deterministically so repeats refresh rather than duplicate.

> **MAINTAINER'S RULE** — Add ICS behavior here, and add it the way this file already works. Route new endpoints as another `if/elif` branch that ends in `send_json`; pass every value to SQL as a bound `?` parameter and pick any dynamic column names from a fixed in-code whitelist, never from the request body. Store a new form or field in the `ics_forms` JSON blob — do not add a table unless you truly need to filter by that field in SQL. Preserve partial updates on the T-card and check-in paths so a status-only move never wipes the rest of a card, and call `log_activity` after every write so the activity feed stays complete. And never bind this service to anything but `127.0.0.1` — its safety depends on nginx being the only way in.


# 9. The Health Monitor — health_monitor.py

*A tiny always-on service, python/health_monitor.py, answers one question over and over: is this appliance healthy and ready to run an incident? It reads the Raspberry Pi's temperature, memory, disks, and each system service, checks the internet and the Global Positioning System (GPS), and feeds the dashboard and the pre-flight readiness screen.*

> **IN ONE SENTENCE** — `python/health_monitor.py` is a small read-only Hypertext Transfer Protocol (HTTP) service on port 5051 that gathers the appliance's vital signs — temperature, memory, disk, service status, internet, GPS — caches them briefly, and serves them as JavaScript Object Notation (JSON) so the dashboard and the pre-flight screen can show a green or red light.


## What This Is / What It Is For

Before an operator keys up a radio or opens the Incident Command System (ICS) forms, they want one honest answer: **is this box working?** The health monitor exists to give that answer. It is [python/health_monitor.py](python/health_monitor.py), a standalone service that reports, in its own words, "CPU temp, memory, disk, service status, internet connectivity, GPS status, Dead Man's Switch state, preflight results." It does not store anything, it does not change anything, and it does not know about incidents or forms. It only looks at the machine and tells you what it sees.

It is a **separate service** on purpose. If the main Federal Communications Commission (FCC) lookup Application Programming Interface (API) on port 5050 hangs, or the ICS platform on port 5055 crashes, the health monitor is a different process and keeps answering — so the dashboard can still tell you *that* one of the others is down. A monitor that shared a process with the thing it watches would die with it. Keeping it small and independent is what lets it be trusted.

> **JARGON, IN PLAIN WORDS** — A **service** here is a background program managed by the operating system (started at boot, restarted if it dies). **systemd** is Linux's service manager, and **systemctl** is the command you use to ask it about a service. **localhost** (address `127.0.0.1`) means "this same machine" — a localhost-only server cannot be reached from the network directly. **nginx** is the web server that sits in front and forwards browser requests to the right internal service.


## How It Is Reached — localhost Only, Through nginx

The service binds to `127.0.0.1` (localhost) and nothing else. The last lines of the file make that explicit, and the comment says exactly why:

```
if __name__ == "__main__":
    print("[health-monitor] Starting on port 5051")
    # Pre-warm cache in background
    threading.Thread(target=collect_health, daemon=True).start()
    # Localhost only — reached via nginx at /svc/5051 over HTTPS.
    server = HTTPServer(("127.0.0.1", 5051), HealthHandler)
    server.serve_forever()
```

Because it binds to localhost, the only way a browser can reach it is through nginx, which forwards a same-origin path to it. The nginx configuration maps `/svc/5051/` to the service and gives it a deliberately short read timeout — a health check that cannot answer in ten seconds is itself a symptom:

```
location /svc/5051/ {   # health monitor
    proxy_pass         http://127.0.0.1:5051/;
    proxy_set_header   Host $host;
    proxy_read_timeout 10;
}
```

So when the dashboard asks for `/svc/5051/api/health/quick`, nginx strips the `/svc/5051/` prefix and the service sees `/api/health/quick`. This is the same same-origin pattern every FieldCommand service uses, which is why the front end works identically over plain HTTP in development and Hypertext Transfer Protocol Secure (HTTPS) in production, with no mixed-content warnings.


## How It Works — Probing the Machine

The heart of the file is a set of small, single-purpose functions, each of which reads one aspect of the machine and returns a plain dictionary. None of them throw: every one is wrapped so that a failure returns an empty or safe default instead of crashing the whole health report. That is the guiding rule of the whole file — **a monitor must never fail louder than the thing it is monitoring.**

Everything that shells out to a command goes through one tiny helper, `run()`, which enforces a timeout and swallows failure into an empty string. A hung command can never hang the health check:

```
def run(cmd, timeout=3):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception:
        return ""
```

Temperature is read the cheap way first (a kernel file), then a Pi-specific fallback. Note the sanity range: a plausible reading is 10–100 °C, and anything outside that is ignored rather than reported as a false alarm:

```
def get_cpu_temp():
    """Read CPU temperature in Celsius"""
    # Try thermal zone (Linux)
    for tz in Path("/sys/class/thermal").glob("thermal_zone*/temp"):
        try:
            v = int(tz.read_text().strip())
            if 10000 < v < 100000:  # sanity: 10–100°C
                return round(v / 1000, 1)
        except Exception:
            pass
    # Try vcgencmd (Pi-specific)
    out = run(["vcgencmd", "measure_temp"])
    ...
```

Memory is parsed straight from `/proc/meminfo`, and disk usage is gathered for each mount point that actually exists (`/`, `/opt`, and the optional Non-Volatile Memory express (NVMe) or Solid State Drive (SSD) mounts). Both convert raw numbers into the megabytes, gigabytes, and percentages the dashboard shows, and both fall back to a zeroed structure on error so the shape of the JSON never changes.

> **JARGON, IN PLAIN WORDS** — `/proc/meminfo` and `/sys/class/thermal` are not real files on a disk — they are windows the Linux kernel exposes as if they were files, so a program can read live memory and temperature just by reading text. **statvfs** is the system call behind free-space numbers. **TPV** (Time-Position-Velocity) is the GPS daemon's report line that carries the current fix, latitude, and longitude.


## How It Works — Services and Connectivity

The list of services the monitor watches is a plain table at the top of the file — a system name paired with a friendly label the dashboard can print. Adding a new service to the readiness view is a one-line change here:

```
SERVICES = [
    ("nginx",           "Web Server"),
    ("fcc-lookup",      "FCC Lookup API"),
    ("health-monitor",  "Health Monitor"),
    ("direwolf",        "Direwolf TNC"),
    ("pat",             "Pat Winlink"),
    ("ics-platform",    "ICS Platform"),
    # ... more
]
```

Checking whether each one is up is exactly what `systemctl is-active` answers, so `get_services()` simply asks the operating system service by service and normalizes the reply into a boolean plus the raw status text:

```
def get_services():
    results = {}
    for svc_name, label in SERVICES:
        out = run(["systemctl", "is-active", svc_name])
        results[svc_name] = {"label": label, "active": out == "active",
                             "status": out or "inactive"}
    return results
```

The internet check is deliberately two-sided. It is easy to fool a naive check — a captive portal will answer HTTP but real name resolution may be broken, and vice versa — so the monitor only reports `connected` when **both** a Domain Name System (DNS) lookup and a real HTTP request to a known 204-no-content endpoint succeed:

```
def get_internet():
    """Check internet via DNS and HTTP"""
    dns_ok = False; http_ok = False
    try:
        socket.setdefaulttimeout(3)
        socket.getaddrinfo("dns.google", 443)
        dns_ok = True
    except Exception: pass
    try:
        urllib.request.urlopen("http://connectivitycheck.gstatic.com/generate_204", timeout=4)
        http_ok = True
    except Exception: pass
    return {"connected": dns_ok and http_ok, "dns": dns_ok, "http": http_ok}
```

GPS is read by talking to the GPS daemon (`gpsd`) directly on its local port 2947, sending a `?POLL;` and parsing the first Time-Position-Velocity line back. A `mode` of 2 or higher means a real position fix. As everywhere else, an unreachable daemon returns a safe "no fix" dictionary rather than an exception.


## How It Works — The Endpoints and the Cache

Collecting everything means shelling out several times, so the full report is **cached for ten seconds**. Many dashboard tiles can refresh at once and only the first one in each ten-second window pays the cost; the rest get the cached copy. The cache is guarded by a lock so two threads never rebuild it at the same time:

```
_cache = {}
_cache_lock = threading.Lock()
_CACHE_TTL = 10  # seconds

def collect_health():
    with _cache_lock:
        now = time.time()
        if _cache.get("ts", 0) + _CACHE_TTL > now:
            return _cache.get("data")
    data = { "timestamp": utcnow(), "cpu_temp": get_cpu_temp(),
             "memory": get_memory(), "disk": get_disk(),
             "services": get_services(), "internet": get_internet(),
             "gps": get_gps(), ... }
    with _cache_lock:
        _cache["data"] = data; _cache["ts"] = time.time()
    return data
```

The request handler routes a handful of read-only paths. The full report lives at `/api/health`; a trimmed, cache-only summary lives at `/api/health/quick` for tiles that just need a green light and a count; and individual aspects (`/services`, `/gps`, `/internet`) are exposed for pages that only care about one thing. The quick check never triggers a fresh collection of its own — it reads whatever is already cached:

```
elif path == "/api/health/quick":
    # Lightweight check — cached only
    d = _cache.get("data") or collect_health()
    svcs = d.get("services", {})
    return self.send_json({
        "cpu_temp":  d.get("cpu_temp"),
        "internet": d.get("internet", {}).get("connected"),
        "gps_fix":  d.get("gps", {}).get("fix"),
        "services_ok": sum(1 for v in svcs.values() if v.get("active")),
        "services_total": len(svcs),
    })
```


## How It Works — Delegating Pre-flight to the Main API

There is one endpoint the health monitor does **not** answer itself. The full pre-flight readiness verdict (the GO / NO-GO decision) is computed by the main API on port 5050, because that is where the incident and configuration data lives. The health monitor exposes `/api/preflight` only as a convenience passthrough, calling the real one over localhost and forwarding its answer:

```
elif path == "/api/preflight":
    # Delegate to fcc_lookup_server's preflight
    try:
        req = urllib.request.urlopen("http://127.0.0.1:5050/api/preflight", timeout=10)
        return self.send_json(json.loads(req.read()))
    except Exception as e:
        return self.send_json({"error": str(e), "verdict": "NO-GO"}, 503)
```

> **WHY A FAILURE HERE RETURNS NO-GO** — If the main API cannot be reached, the passthrough does not return "unknown" — it returns an explicit `"verdict": "NO-GO"` with a 503 status. That is the safe default for a readiness check: when the system cannot prove it is ready, it must say it is **not** ready. Never soften this to a neutral or optimistic answer; a green light nobody earned is worse than a red one.

This is also why the pre-flight *screen* itself talks straight to the main API — `preflight.html` sets `const API = '/svc/5050';` and fetches `/api/preflight` there. The health monitor's copy of the route exists for callers that are already talking to 5051 and want everything from one place, not as the authority on the verdict.


## How the Dashboard Consumes It

The home dashboard is the main consumer. It fetches the quick summary and the service list from the monitor through nginx, each with its own timeout so a slow health check degrades one tile instead of freezing the page:

```
const r  = await fetch("/svc/5051/api/health/quick",  {signal: AbortSignal.timeout(5000)});
const r2 = await fetch("/svc/5051/api/health/services",{signal: AbortSignal.timeout(5000)});
```

Because the responses are plain JSON with a stable shape, the front end only has to read fields like `services_ok`, `services_total`, `internet`, and `gps_fix` and turn them into lights and counters. The ten-second server-side cache means the dashboard can poll freely without ever overloading the Pi with `systemctl` calls.


## Why It Matters / Design Takeaways

- *Independent by design.* The monitor is its own process on its own port, so it survives the failure of any service it watches and can still report that failure.
- *Read-only and crash-proof.* Every probe is wrapped to return a safe default, timeouts bound every external call, and nothing is ever written — a monitor must not become a new source of failure.
- *Cheap to poll.* A ten-second cache behind a lock means many dashboard tiles refreshing at once cost the machine almost nothing.
- *Honest defaults.* Two-sided internet checks avoid captive-portal false positives, and the pre-flight passthrough returns NO-GO when it cannot prove otherwise.
- *One authority per fact.* The readiness verdict is computed once, in the main API, and only forwarded here — the monitor never invents a second opinion.

> **MAINTAINER'S RULE** — Keep the health monitor read-only, bounded, and un-crashable. Every new probe must wrap its work in `try/except` and return a safe default, must use `run()` (or an explicit timeout) for anything external, and must keep the JSON shape stable so the dashboard never sees a missing key. To watch a new service, add one `(name, label)` line to `SERVICES` — nothing else. And never let this service become the authority on a fact another service owns: if a value is computed elsewhere (like the pre-flight verdict), forward it, do not recompute it.


# 10. The Reference Library Server — reference_server.py

*One small service, python/reference_server.py, is FieldCommand's filing cabinet. It takes uploaded reference documents — plans, maps, frequency lists, forms — stores the file on disk and its details in the database, and serves them back with categories, sections, tags, and a downloads count. It is built to handle files far too big for the other services.*

> **IN ONE SENTENCE** — `python/reference_server.py` is a small Hypertext Transfer Protocol (HTTP) service on port 5056 that stores uploaded reference files on disk, keeps their details in the `ref_documents` database table, and serves them back — organized by category, section, and tag, and counting every download — kept separate from the main Application Programming Interface (API) because reference files can be very large.


## What This Is / What It Is For

An incident runs on paper as much as radio: the county plan, the shelter roster template, a band plan, a road-closure map, a scanned mutual-aid agreement. The reference library is where all of that lives so anyone on the network can pull it up. It is [python/reference_server.py](python/reference_server.py), and its own header sums it up: "FieldCommand Reference Library Server — Port 5056 (SQLite via db.py)." It does two jobs — it **stores** an uploaded file (the bytes on disk, the details in the database) and it **serves** files back with enough structure (categories, sections, tags, search) that an operator can actually find the one they need.

It is a **separate service** for one main reason: **size**. The main API deals in small things — a member photo, a logo, a form's fields. Reference documents are the opposite: multi-megabyte Portable Document Format (PDF) manuals, map bundles, even short audio or video clips. Mixing large uploads into the main API would slow every other request and force a large body limit onto services that should never accept one. Giving the library its own process and its own generous limit keeps the fast services fast.

> **JARGON, IN PLAIN WORDS** — **Metadata** is the information *about* a file — its title, category, who it applies to, when it expires — as opposed to the file's actual contents. **multipart/form-data** is the way a web browser packages a file upload: the file bytes and the text fields are bundled together in one request, separated by a **boundary** marker. A **SHA-256** is a fingerprint of the file's contents used to spot duplicates. **nginx** is the web server that forwards browser requests to the right internal service.


## How It Is Reached — localhost Only, Through nginx

Like every FieldCommand service, the library binds only to localhost and is reached through nginx. The last lines of the file show it starting the database (via `db.startup()`) and then binding to `127.0.0.1`:

```
if __name__ == "__main__":
    db.startup()
    log.info(f"Reference Library on port 5056 — {FILES_DIR}")
    # Localhost only — reached via nginx at /svc/5056 over HTTPS.
    HTTPServer(('127.0.0.1',5056),RefsHandler).serve_forever()
```

The nginx block for `/svc/5056/` is where the large-upload story starts. Two settings matter: a longer read timeout (uploading a big file over a field link is slow) and, crucially, `client_max_body_size` raised to 200 megabytes (MB). nginx's default limit is only 1 MB, so without this line every real reference upload would be rejected before it ever reached the service:

```
location /svc/5056/ {   # reference library (large uploads)
    proxy_pass            http://127.0.0.1:5056/;
    proxy_set_header      Host $host;
    proxy_read_timeout    120;
    client_max_body_size  200M;
}
```

> **TWO LIMITS MUST AGREE** — There are **two** size limits, and they must match. nginx enforces `client_max_body_size 200M`, and the service enforces its own `MAX_UPLOAD = 200 * 1024 * 1024`. If you raise one, raise the other. If nginx's limit is lower, big uploads fail with a confusing nginx 413 error the app never sees; if the service's limit is lower, the file uploads fully and is then rejected — a slow, wasteful failure. Keep the pair in lockstep.


## How It Works — Where Files and Metadata Live

The library keeps the **file** and the **facts about the file** in two different places, on purpose. The bytes go to disk in a folder owned by the data layer; the details go into a single database row. The disk paths come straight from `db.py`, so the library never invents its own locations:

```
FILES_DIR = db.FILES_DIR   # /opt/fieldcommand/data/refs/files
THUMB_DIR = db.THUMB_DIR   # /opt/fieldcommand/data/refs/thumbs
MAX_UPLOAD = 200 * 1024 * 1024
ALLOWED_EXT = {'.pdf','.doc','.docx','.xls','.xlsx','.ppt','.pptx',
               '.txt','.md','.csv','.jpg','.jpeg','.png','.gif',
               '.zip','.kml','.kmz','.gpx','.mp3','.mp4'}
```

The metadata lives in the `ref_documents` table, defined once in the data layer. Note how the two array-like fields — `sections` and `tags` — are stored as JavaScript Object Notation (JSON) text, and how the row carries its own accounting fields (`downloads`, `last_downloaded`, `size_bytes`, `sha256`):

```
CREATE TABLE IF NOT EXISTS ref_documents (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL DEFAULT '',
    filename        TEXT NOT NULL DEFAULT '',
    stored_name     TEXT NOT NULL DEFAULT '',
    category        TEXT NOT NULL DEFAULT 'other',
    sections        TEXT NOT NULL DEFAULT '["amateur"]',  -- JSON array
    tags            TEXT NOT NULL DEFAULT '[]',            -- JSON array
    ...
    size_bytes      INTEGER DEFAULT 0,
    sha256          TEXT DEFAULT '',
    uploaded        TEXT NOT NULL,
    downloads       INTEGER NOT NULL DEFAULT 0,
    last_downloaded TEXT
);
```

> **WHY filename AND stored_name ARE SEPARATE** — `filename` is the name the operator sees and downloads as (`McHenry_County_EOP.pdf`). `stored_name` is the safe, unique name the bytes actually live under on disk (`ref_18f2a9c0e11.pdf`). Splitting them means two files with the same human name never collide, a malicious filename can never escape the folder, and the download can still present the friendly name. Never store an uploaded file under its raw original name.


## How It Works — The Upload

A browser sends the file and its metadata together as one `multipart/form-data` POST to `/refs/upload`. The service parses that bundle itself with a small hand-written `parse_multipart()` — splitting on the boundary marker and separating the named text fields from the named file part. The upload handler then walks a clear sequence: reject anything that is not a real file, validate the extension, enforce the size limit, write the bytes, and record the row.

Validation happens before anything is written. The extension must be on the allow-list, and the size must be under the limit — the same 200 MB ceiling nginx enforces:

```
if 'file' not in files: return self.send_err('No file in upload',400)
f=files['file']
orig=safe_name(f['filename']); ext=Path(orig).suffix.lower()
if ext not in ALLOWED_EXT: return self.send_err(f'File type not allowed: {ext}',400)
data=f['data']
if len(data)>MAX_UPLOAD: return self.send_err('File too large',400)
```

Only after validation does the service mint an id, derive the safe `stored_name` from it, and write the bytes to disk. The id is time-based and hex-encoded, so it is unique and sorts by upload order:

```
doc_id=f"ref_{int(time.time()*1000):x}"
stored=f"{doc_id}{ext}"; dest=FILES_DIR/stored
dest.write_bytes(data)
```

The row is then inserted with every field the browser supplied, plus the computed ones. The two array fields are serialized with the data layer's shared `jdump()` helper, the content fingerprint is computed with `file_hash()`, and the upload time is stamped with the shared `utcnow()` — so the library formats time and JSON identically to every other service:

```
c.execute("""INSERT INTO ref_documents
    (id,title,filename,stored_name,category,sections,description,
     tags,source,applies_to,revision,expires,content_type,
     size_bytes,sha256,uploaded)
    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
    (doc_id, fields.get('title','').strip() or orig,
     orig, stored, fields.get('category','other'),
     jdump(sections), fields.get('description','').strip(),
     jdump(tags), ... len(data), file_hash(dest), utcnow()))
c.commit()
```

One nicety: if the upload is a PDF, a thumbnail is generated on a **background thread** so the operator's upload returns immediately instead of waiting for image rendering. If thumbnailing fails (or the tool is absent), it fails silently and the document simply has no preview — a missing thumbnail is never allowed to fail an upload:

```
if ext=='.pdf':
    threading.Thread(target=try_thumbnail,
                     args=(dest,THUMB_DIR/f"{doc_id}.png"),daemon=True).start()
```


## How It Works — Serving a File and Counting Downloads

Getting a document back is two endpoints: `/refs/{id}` returns the metadata as JSON, and `/refs/{id}/file` streams the actual bytes. The file endpoint does one small stateful thing on the way out — it increments the `downloads` counter and stamps `last_downloaded`, so the library can show which references people actually use:

```
fp=FILES_DIR/row['stored_name']
if not fp.exists(): return self.send_err('File missing',404)
c.execute("UPDATE ref_documents SET downloads=downloads+1,last_downloaded=? WHERE id=?",
          (utcnow(),doc_id)); c.commit()
data=fp.read_bytes()
mime=row['content_type'] or mimetypes.guess_type(row['filename'])[0] or 'application/octet-stream'
self.send_response(200)
self.send_header('Content-Type',mime)
self.send_header('Content-Disposition',f'attachment; filename="{row["filename"]}"')
```

The counter is done with a single SQL `downloads=downloads+1`, not by reading the number into Python and writing it back. Letting the database do the increment in one statement is what keeps the count correct even if two people download the same file at the same moment. Notice too that the download is served under the friendly `filename`, while the bytes were read from the safe `stored_name` — the split from earlier paying off.


## How It Works — Categories, Sections, and Tags

Browsing is what makes a pile of files a library. The service exposes small read endpoints for the facets an operator filters by. Categories and their counts come straight from SQL grouping:

```
elif path == '/refs/categories':
    rows=c.execute("SELECT category,COUNT(*) cnt FROM ref_documents GROUP BY category").fetchall()
    return self.send_json({'categories':{r['category']:r['cnt'] for r in rows}})
```

The main listing endpoint `/refs` does the coarse filtering (by category) in SQL, then does the finer filtering — by **section** (amateur vs. ICS), by **tag**, and by free-text **search** — in Python, because those live inside the JSON columns and are easiest to match after parsing. Each document's `sections` and `tags` are decoded with the shared `jload()` before being returned:

```
if tag:
    rows=[r for r in rows if tag in jload(r.get('tags'),[]) ]
if q:
    rows=[r for r in rows if q in (
        (r.get('title','') or '')+(r.get('description','') or '')+
        (r.get('source','') or '')+(r.get('tags','') or '')).lower()]
for r in rows:
    r['sections']=jload(r.get('sections'),[r.get('section','amateur')])
    r['tags']=jload(r.get('tags'),[])
```

> **WHY SECTIONS EXIST** — A document belongs to one or more **sections** — `amateur`, `ics`, or both. This lets the same library serve two audiences from one store: an amateur-radio operator browsing band plans and an incident-staff member browsing ICS forms each see the subset relevant to them, without two separate libraries to maintain. On upload, the special value `both` is expanded to `['amateur','ics']`.


## Why It Matters / Design Takeaways

- *Separated for size.* Reference documents can be hundreds of megabytes, so the library is its own service with its own raised body limit — the fast, small services never carry that weight.
- *File and facts split cleanly.* Bytes live on disk under a safe unique name; details live in one `ref_documents` row under the friendly name — no collisions, no path-escape risk, friendly downloads.
- *Validate before you write.* Extension allow-list and size limit are checked before a single byte hits the disk, and the service's limit mirrors nginx's so the two never disagree.
- *The database keeps the count honest.* Downloads are incremented with one SQL statement, so concurrent downloads never lose a tick.
- *Shared helpers, consistent data.* Time, JSON, and paths all come from the data layer (`utcnow`, `jdump`, `jload`, `FILES_DIR`), so the library stores data exactly like every other service.

> **MAINTAINER'S RULE** — Keep the file and its metadata in step, and keep the two size limits equal. Never store an upload under its raw original name — always mint a safe `stored_name` and serve back under `filename`. When you change `MAX_UPLOAD`, change nginx's `client_max_body_size` to match in the same commit. Add a new file type only by extending `ALLOWED_EXT`, and get paths, timestamps, and JSON only from `db.py` — never hard-code a folder or format the library should be sharing with the rest of the system.


# 11. The Offline Map Tile Server — tile_server.py

*A small Flask service, python/tile_server.py, serves map images out of local files so the tactical map draws perfectly with no internet. The browser asks for /tiles/{tileset}/{z}/{x}/{y}.png, the server pulls that square out of a local MBTiles database, and the map fills in — exactly as if it were talking to an online map provider, except everything is on the Pi.*

> **IN ONE SENTENCE** — `python/tile_server.py` is a tiny web service that hands the map its picture tiles out of local `.mbtiles` files at `/tiles/{tileset}/{z}/{x}/{y}.png`, so the tactical map works fully offline — and `html/lib/tiles.js` is the browser-side code that finds those tiles and falls back to online maps only when the internet is actually there.


## What This Is / What It Is For

The tactical map is the centerpiece of FieldCommand, and a map is really just a grid of small square images called **tiles**. Normally a web map downloads those tiles from an online provider like OpenStreetMap. But FieldCommand runs in a field with no internet, so it cannot rely on any online provider. Instead it serves the tiles itself, from files already on the Raspberry Pi, using a small service: [python/tile_server.py](python/tile_server.py).

The service is a **Flask** web application listening on port 8083. Its job is narrow and mechanical: when the map in the browser needs the tile at a given zoom level and grid position, it asks this server for it by URL, and the server reads that exact square out of a local database and sends back the image. To the mapping library in the browser, this looks identical to talking to a real online tile provider — same URL shape, same PNG images — except the round trip never leaves the Pi. The file's own header spells out the contract:

```
"""
FieldCommand — Offline Map Tile Server
Serves MBTiles databases as XYZ tile endpoints for Leaflet.js
Port 8083  —  http://localhost:8083/tiles/{tileset}/{z}/{x}/{y}.png

MBTiles stores tiles in TMS format (Y-flipped).
We flip Y back to XYZ/Slippy format for Leaflet.
"""
```

> **JARGON, IN PLAIN WORDS** — A **tile** is one small square image of the map (usually 256×256 pixels). A web map is a grid of them. **Zoom/x/y** identify one tile: `z` is how far in you are zoomed, and `x`/`y` are its column and row in the grid at that zoom. **MBTiles** is a single SQLite file that holds thousands of these tile images. **Leaflet** is the JavaScript map library running in the browser. **Flask** is a small Python web-server framework. **Same-origin** means the browser asks for tiles from the same web address it loaded the page from, so no cross-site rules get in the way.


## Why Serve Our Own Tiles — the 'Why' Behind It

The alternative to serving tiles locally is depending on the internet, and for an emergency-communications appliance that is a non-starter. During the exact events FieldCommand is built for — storms, outages, remote deployments — the internet is often the first thing to fail. If the map went blank whenever connectivity dropped, the tool would be useless precisely when it is needed most. So the tiles for the operating area are downloaded ahead of time into MBTiles files, and this server makes them available with no network at all.

Serving them through a standard tile URL, rather than some custom scheme, is a deliberate choice: it means the browser-side map code is ordinary Leaflet and can just as easily point at an online provider when the internet **is** available. The offline path and the online path are the same shape, so switching between them is a matter of which URL the layer uses — not two different code paths. That symmetry is what lets `tiles.js` treat offline and online sources as interchangeable, covered later in this chapter.


## How It Works — The One Coordinate Flip

There is a historical wrinkle in map tiling that this server exists partly to smooth over. MBTiles files store tiles in **TMS** order, where the Y axis counts from the bottom up. Leaflet and most online providers use **XYZ** (also called Slippy) order, where Y counts from the top down. If the server handed the browser's Y straight to the database, the map would be flipped upside down. So there is exactly one small function that converts the browser's Y into the database's row number:

```
def xyz_to_tms_y(z: int, y: int) -> int:
    """Convert XYZ tile Y to TMS tile_row (MBTiles stores TMS)."""
    return (1 << z) - 1 - y
```

The formula reads: at zoom `z` there are `2^z` rows (`1 << z` is a fast way to write two-to-the-power-of-`z`), numbered `0` to `2^z − 1`, and flipping top-to-bottom is subtracting the incoming `y` from the last row number. Every tile fetch runs through this one line, and it is the single most important correctness detail in the file.

> **JARGON, IN PLAIN WORDS** — **TMS** (Tile Map Service) and **XYZ/Slippy** are two conventions for numbering the rows of map tiles. They agree on everything except which end the Y axis starts counting from — TMS from the bottom, XYZ from the top. The `1 << z` is a bit-shift: it computes `2` raised to the power `z` very quickly. Flip the row, and a bottom-counted number becomes a top-counted one.


## How It Works — Tilesets and the Endpoints

A **tileset** is one map style for one area — for example USGS topographic, or satellite imagery. Each tileset is a single file named `{tileset}.mbtiles`, and they all live together in the tile directory (by default `/opt/fieldcommand/tiles`, overridable by an environment variable). The server discovers tilesets simply by listing that folder for `.mbtiles` files — drop a new file in and it appears, with no code change:

```
TILE_DIR  = os.environ.get('FC_TILE_DIR',  '/opt/fieldcommand/tiles')

def list_tilesets() -> List[str]:
    """Return names of all available MBTiles files."""
    if not os.path.isdir(TILE_DIR):
        return []
    return [
        f[:-8] for f in os.listdir(TILE_DIR)
        if f.endswith('.mbtiles') and os.path.isfile(os.path.join(TILE_DIR, f))
    ]
```

On top of that folder, the server exposes a small, predictable set of endpoints. The map uses the tile endpoint constantly; the others are for discovery and health:

| Endpoint | What it returns | Who calls it |
| --- | --- | --- |
| `GET /tiles/` | JSON list of available tilesets with their names, zoom range, and bounds. | The browser, to discover which offline maps exist. |
| `GET /tiles/{tileset}/metadata.json` | One tileset's metadata in TileJSON-compatible form. | Map tooling that wants a tileset's details. |
| `GET /tiles/{tileset}/{z}/{x}/{y}.png` | One tile image (PNG or JPEG). | Leaflet, once per visible tile, as the operator pans and zooms. |
| `GET /health` | JSON status: tile directory, every tileset, and its tile count and zoom range. | The health monitor and installer checks. |

Just like the FCC and main databases, this server gives each thread its own SQLite connection so many tile requests can run at once. The connections are tuned purely for fast read-only serving — notably `synchronous=OFF`, which is safe here because the server never writes to a tileset, only reads:

```
def get_db(tileset: str) -> object:
    """Get or create a thread-local SQLite connection for the tileset."""
    db_path = os.path.join(TILE_DIR, f'{tileset}.mbtiles')
    if not os.path.isfile(db_path):
        return None
    ...
            conn = sqlite3.connect(db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            conn.execute('PRAGMA journal_mode=WAL')
            conn.execute('PRAGMA synchronous=OFF')
            conn.execute('PRAGMA cache_size=2000')    # 2000 pages × 4KB = 8MB cache
            conn.execute('PRAGMA temp_store=MEMORY')
```


## How It Works — Serving One Tile

The tile route is where everything comes together. When Leaflet requests a tile, the handler validates the request, checks the browser's cache, fetches the tile, and returns it — with a fallback for anything it cannot find. First, it guards the coordinates. A zoom outside the valid range is a hard error, but a tile position outside the grid is simply answered with a transparent pixel rather than an error, because the map should never break on an edge request:

```
@app.route('/tiles/<tileset>/<int:z>/<int:x>/<int:y>.png')
@app.route('/tiles/<tileset>/<int:z>/<int:x>/<int:y>.jpg')
def serve_tile(tileset, z, x, y):
    # Validate zoom range
    if z < 0 or z > 22:
        abort(400)
    # Validate tile coordinates
    max_coord = (1 << z)
    if x < 0 or x >= max_coord or y < 0 or y >= max_coord:
        return Response(TRANSPARENT_PNG, 200, { ... })
```

Next it fetches the actual image. The fetch is a single indexed lookup into the MBTiles `tiles` table — and this is where the Y-flip from earlier is applied, turning the browser's XYZ `y` into the TMS `tile_row` the file stores:

```
def fetch_tile(tileset: str, z: int, x: int, y: int) -> Optional[bytes]:
    db = get_db(tileset)
    if not db:
        return None
    tms_y = xyz_to_tms_y(z, y)
    row = db.execute(
        'SELECT tile_data FROM tiles WHERE zoom_level=? AND tile_column=? AND tile_row=?',
        (z, x, tms_y)
    ).fetchone()
    return bytes(row['tile_data']) if row else None
```

The most important design decision in the whole file is what happens when a tile is **not** found — for example, a corner of the map the operator zoomed into that was never downloaded. The server does not return a 404 error, because Leaflet would draw an ugly broken-image box for every missing square. Instead it returns a 1×1 transparent PNG with a `200 OK`, so the map simply shows empty space there and keeps working. A special `X-Tile-Miss` header marks it as a miss for debugging without disturbing the map:

```
    data = fetch_tile(tileset, z, x, y)

    if data is None:
        # Return transparent pixel — allows Leaflet to continue without error
        return Response(TRANSPARENT_PNG, 200, {
            'Content-Type':  'image/png',
            'Cache-Control': f'public, max-age={CACHE_TTL}',
            'X-Tile-Miss':   '1',
        })
```

> **WHY A MISS IS A PIXEL, NOT AN ERROR** — Returning a transparent `200` for a missing tile is the difference between a map with a few blank patches and a map covered in broken-image icons. The operator sees a clean map that simply lacks detail where no tiles were downloaded. Never change a tile miss to a 404 or 500 — Leaflet treats those as failures and the map degrades badly.

When a tile **is** found, the server detects whether the stored bytes are PNG or JPEG (MBTiles can hold either) and sets the right content type, along with caching headers and an ETag so the browser can skip re-downloading a tile it already has:

```
def detect_format(data: bytes) -> str:
    """Detect whether tile data is PNG or JPEG."""
    if data[:4] == b'\x89PNG':
        return 'image/png'
    if data[:2] == b'\xff\xd8':
        return 'image/jpeg'
    return 'image/png'
```


## How the Front End Consumes Tiles — tiles.js

The browser side lives in [html/lib/tiles.js](html/lib/tiles.js), a shared module every map page loads. It defines every tile source — offline and online — in one `SOURCES` table, probes what is actually available, and builds the Leaflet layer control. The single most important line sits right at the top, and it reflects a recent, deliberate change:

```
const FC_TILES = (() => {
    const TILE_SERVER = '';  // same-origin: tiles served at /tiles/... via nginx
```

> **THE RECENT CHANGE — ABSOLUTE URL TO SAME-ORIGIN** — `TILE_SERVER` used to be an absolute address like `http://<pi-ip>:8083`, pointing the browser straight at the tile server's own port. It is now an empty string, so every tile URL becomes a **same-origin** path like `/tiles/usgs_topo/{z}/{x}/{y}.png`, which nginx routes to the tile server behind the scenes. This matters: same-origin means no hard-coded IP address or port in the page, no cross-origin (CORS) complications, and tiles that keep working no matter what address the operator used to reach FieldCommand. If you ever see tiles fail to load, confirm this is still `''` and that nginx still proxies `/tiles/` to port 8083 — do not 'fix' it by putting the absolute URL back.

Every offline source builds its URL from that same `TILE_SERVER` prefix, so flipping the prefix flips them all at once. The offline USGS and Esri sources point at the local `/tiles/...` path; the online sources point at real providers on the internet:

```
        usgs_topo: {
            label:       '🗺 USGS Topo (Offline)',
            group:       'offline',
            url:         `${TILE_SERVER}/tiles/usgs_topo/{z}/{x}/{y}.png`,
            attribution: 'USGS National Map — Public Domain',
            maxZoom:     18,
            offline:     true,
        },
        ...
        osm: {
            label:       '🌐 OpenStreetMap (Online)',
            group:       'online',
            url:         'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
            offline:     false,
        },
```

Before it builds any layers, `tiles.js` runs two probes in parallel — one asking the local tile server what it has, one checking whether the internet is reachable — and waits for both. The tile-server probe hits the same `/tiles` listing endpoint the server exposes, with a short timeout so a missing server fails fast rather than hanging the map:

```
    async function probeTileServer() {
        try {
            const res = await fetch(`${TILE_SERVER}/tiles`, {
                signal: AbortSignal.timeout(2000),
            });
            if (!res.ok) return false;
            const data = await res.json();
            _availableOffline = (data.tilesets || []).map(t => t.id);
            _tileServerOnline = true;
            return true;
        } catch (e) {
            _tileServerOnline = false;
            _availableOffline = [];
            return false;
        }
    }
```

With both probe results in hand, it chooses a default base layer by a fixed preference order — offline tiles always win over online ones, because in the field the local copy is both faster and always available. The preferred default is the USGS Imagery+Topo hybrid, chosen specifically for McHenry County field operations; only if no offline tileset is present does it fall back to an online source:

```
    function getBestDefault() {
        const offlinePreference = ['usgs_imgtopo', 'usgs_imagery', 'usgs_topo',
                                   'esri_imagery', 'esri_street', 'esri_topo',
                                   'esri_relief'];
        for (const id of offlinePreference) {
            if (_availableOffline.includes(id)) return id;
        }
        if (_internetAvailable) return 'usgs_topo_online';  // USGS online when no offline tiles
        return null;  // No tiles available
    }
```

The layer control is then assembled offline-first: every offline tileset the server actually reported is added, then the online sources if the internet was reachable. And if nothing at all is available — no tile server, no internet — the code does not leave a broken map; it adds a labeled blank grey layer so the map still pans and zooms and the operator sees a clear instruction:

```
        if (Object.keys(baseLayers).length === 0) {
            const blank = L.tileLayer('', {
                attribution: 'No tiles available — run download_tiles.sh',
            });
            baseLayers['(No tiles — run download_tiles.sh)'] = blank;
            defaultLayer = blank;
        }
```

The result is a map that degrades gracefully at every level: it prefers local tiles, uses online ones when they exist, and even with neither it stays interactive and tells the operator exactly what to do. All of that behavior rests on the tile server exposing a simple, predictable `/tiles/...` contract that the browser can probe and consume the same way whether the source is a file on the Pi or a provider across the internet.


## Why It Matters / Design Takeaways

- *Offline is the default, not the fallback.* Tiles are served from local MBTiles files so the tactical map works with zero internet — and `getBestDefault` always prefers those local tiles over online ones.
- *One coordinate flip is the whole correctness story.* `xyz_to_tms_y` converts the browser's XYZ Y to the MBTiles TMS row; get that wrong and every map is upside down.
- *A miss is a pixel, not an error.* Missing tiles return a transparent `200` so Leaflet keeps drawing a clean map instead of broken-image boxes.
- *Same-origin `/tiles/...` via nginx.* `TILE_SERVER` is now `''`, so tile URLs carry no hard-coded IP or port and keep working no matter how the operator reached FieldCommand — a deliberate change from the old absolute URL.
- *Drop-in tilesets.* New maps appear just by placing a `.mbtiles` file in the tile directory; the server lists the folder, no code change needed.

> **MAINTAINER'S RULE** — Keep the tile contract stable: the server serves `/tiles/{tileset}/{z}/{x}/{y}.png` from local MBTiles, flips Y with `xyz_to_tms_y`, and returns a transparent pixel for any miss; the browser reaches it same-origin with `TILE_SERVER = ''` proxied by nginx. Do not reintroduce an absolute tile URL, do not turn a tile miss into a 404/500, and do not remove the Y-flip. If you add a tileset, add its file to the tile directory and a matching entry to `SOURCES` in `tiles.js` (and to `offlinePreference` if it should be a candidate default) — then load a map page and confirm the tiles draw right-side-up both offline and online before you consider it done.


# 12. Identity and the RF Gate — identity.js

*One small front-end file, html/lib/identity.js, answers the question every log entry needs: who is at this keyboard? A second, separate piece of code — the station-level callsign gate — answers a different question: is this group even allowed to key up a transmitter? Together they keep FieldCommand honest about who did what, and lawful about who may transmit.*

> **IN ONE SENTENCE** — `identity.js` remembers who the operator is (member or visitor, ham or not) so every action can be attributed, while a separate station-callsign check — the *RF gate* — refuses to switch on any amateur-radio transmit feature unless a licensed station callsign has been configured.


## What This Is / What It Is For

Every screen in FieldCommand — net control, the Incident Command System (ICS) forms, the roster, the map — needs to stamp actions with a name: who checked this station in, who edited this form, who moved that marker. Rather than ask on every page, FieldCommand loads one shared module, [html/lib/identity.js](html/lib/identity.js), on all of them. It keeps a single small record of the current operator, shows a badge in the header, and offers a picker so a person can say who they are. The rest of the site just calls `FC_ID.getDisplayId()` or `FC_ID.getName()` and gets a consistent answer.

The module is written as an Immediately Invoked Function Expression (IIFE) that returns a small public object called `FC_ID`. Everything else — the stored record, the roster it fetches, the picker modal — is private inside the closure. Pages include it with one line at the bottom of the body, and it wires itself up automatically:

```
<script src="/lib/identity.js"></script>
```

There is no build step and no framework. When the file loads it runs `FC_ID.init()`, which reads any saved identity, fetches the roster in the background, draws the header badge, and — if nobody is set yet — pops the picker after a short delay:

```
async function init() {
    load();
    await fetchRoster();
    renderBadge();
    if (!_id) setTimeout(() => { if (!_picker) showPicker(); }, 900);
}
```

> **JARGON, IN PLAIN WORDS** — An **IIFE** (Immediately Invoked Function Expression) is a function that runs the instant it is defined; here it is used to hide helper variables so only the `FC_ID` object is visible to the page. **localStorage** is a small per-browser store on the device — data written to it survives page reloads and reboots, and never leaves the machine. A **callsign** is the license identifier the Federal Communications Commission (FCC) assigns to an amateur radio operator or station; only a licensed holder may transmit.


## Why It Works This Way — Four People, One Record

A real McHenry County Emergency Services Volunteers (MCESV) activation is not just club members. The file's own header comment enumerates the four person types the code must handle, and they do not all have the same identifiers — some are hams with a callsign, some are non-ham members with only a radio identifier, some are visitors from another agency:

| Type | Who they are | Identifiers they have |
| --- | --- | --- |
| Type 1 | Emergency Services Volunteers (ESV) member, ham | Member ID (`ESV-###`) + callsign + Starcom radio ID |
| Type 2 | ESV member, non-ham | Member ID + Starcom radio ID, *no callsign* |
| Type 3 | Mutual aid / visitor, ham | Callsign + their agency, *no ESV member ID* (auto-assigned `VIS-#####`) |
| Type 4 | Mutual aid / visitor, non-ham | Name + radio ID + their agency, *no callsign, no member ID* |

Rather than four different records, all four collapse into one flat object with the same fields — the ones a given person lacks are simply left blank. That single shape is what gets written to the device, and it is what every accessor reads back:

```
member_id      : "ESV-042",   // ESV number, or "VIS-#####" for visitors
callsign       : "K9ESV",     // blank if non-ham
radio_id       : "1042",      // Starcom radio ID (all ESV members have one)
name           : "Jim Anderson",
role           : "Operator",
member_type    : "member" | "visitor" | "mutual_aid",
visitor_agency : "",           // agency name for visitors
is_ham         : true | false,
```

Why keep it on the device instead of forcing a login? Because FieldCommand is a field appliance with no accounts and, deliberately, no password. An operator says who they are once; the answer is saved in `localStorage` under a versioned key and simply reappears next time. Saving is one function, and it also notifies any listeners and repaints the badge:

```
const STORE_KEY = 'fc_operator_identity_v3';

function save(id) {
    _id = id;
    try { localStorage.setItem(STORE_KEY, JSON.stringify(id)); } catch(e) {}
    _cbs.forEach(fn => { try { fn({ ..._id }); } catch(e) {} });
    renderBadge();
}
```

> **WHY THE KEY ENDS IN _v3** — The storage key is `fc_operator_identity_v3`, not `..._identity`. Bumping the version in the key name is a deliberate, cheap migration: when the record shape changes in a way old data cannot satisfy, a new key means old browsers start clean at the picker instead of loading a stale record with missing fields. If you ever change the stored shape incompatibly again, bump to `_v4` — never silently reuse `_v3`.


## How It Works — Choosing the One Identifier That Matters

A log line has room for one identifier, not five. The module centralizes that choice in a single helper, `bestId`, so every screen labels a person the same way. The rule is a fixed priority: callsign first (it is globally unique and license-backed), then the Starcom radio ID, then the ESV member ID, then finally the plain name:

```
/**
 * Best single identifier for a person object (roster row or identity).
 * Priority: callsign → radio_id → member_id → name
 */
function bestId(m) {
    return (m.callsign || m.radio_id || m.member_id || m.name || '').trim();
}
```

That one function is the whole reason `FC_ID.getDisplayId()` is trustworthy: it never returns an empty string when any identifier exists, and it always prefers the most authoritative one. The public accessors are thin wrappers over the stored record, using optional chaining so they are safe to call before anyone has identified themselves:

```
getMemberId:   () => _id?.member_id      || '',
getCallsign:   () => _id?.callsign        || '',
getDisplayId:  () => bestId(_id || {}),
getName:       () => _id?.name            || '',
isHam:         () => !!(_id?.callsign),
isVisitor:     () => ['visitor','mutual_aid'].includes(_id?.member_type),
```

Notice `isHam` is not a stored flag it trusts blindly — it is computed live from the callsign: `!!(_id?.callsign)`. If there is a callsign, the operator is treated as a ham; if the field is blank, they are not. This matters because it means 'ham-ness' can never drift out of sync with the actual callsign on record. The `is_ham` value written into the object at confirm time is set the same way — `is_ham: !!cs` — so the two always agree.

The picker enforces a minimum before it will save. For a member, at least one of Member ID, callsign, or radio ID must be present; for a visitor, a full name and an agency are required. The member branch shows the pattern:

```
if (!mid && !cs && !rid) {
    _showErr('Please enter your Member ID, Callsign, or Starcom Radio ID.'); return;
}
```


## The RF Gate — No Callsign, No Transmit

Knowing *who* is at the keyboard is separate from knowing whether the *station* may legally key a transmitter. That second decision is the *RF gate*, and it lives one level up from the operator record, at the station-configuration level. The rule is blunt and it is written in plain sight: the amateur-radio modules — general amateur, Winlink, Automatic Packet Reporting System (APRS), and the 44Net tunnel — cannot be switched on unless a station callsign has been entered. In [html/setup.html](html/setup.html) they are named as a group:

```
// Modules that transmit on the amateur bands — they require a callsign AND a
// properly licensed operator. They cannot be enabled without a callsign.
const HAM_MODULES = ['amateur', 'winlink', 'aprs', '44net'];
```

Trying to toggle any of those on with no callsign is refused outright, with an explanation that names exactly what to do and why — enter a callsign, and only if the group actually has a licensed operator:

```
function toggleModule(mod) {
  // Block turning on any amateur-radio module unless a callsign is set.
  if (HAM_MODULES.includes(mod) && !modules[mod] && !hasCallsign()) {
    alert('This is an amateur radio feature.\n\n' +
          'Enter a Club / Station Callsign at the top of this page first ...');
    const cb = document.getElementById(`mod_${mod.replace('-','')}`);
    if (cb) cb.checked = false;
    document.getElementById('callsign')?.focus();
    return;
  }
  modules[mod] = !modules[mod];
  // ...
}
```

The gate is not just a one-time check at click time; it is also a *safety net* at save time. Even if a callsign were somehow cleared while a module was on, `saveConfig()` forces every ham module back off before the configuration is written, so a blank callsign can never leave a transmit feature enabled:

```
// Safety net: no callsign means no amateur-radio transmit features, ever.
if (!callsign) HAM_MODULES.forEach(m => { modules[m] = false; });
```

Finally, the dashboard in [html/index.html](html/index.html) enforces the same gate visually. When the station configuration loads, it computes a single flag, `FC_HAM_ENABLED`, from whether a callsign exists and the amateur module is on, and then grays out the Amateur Radio mode button so it cannot even be selected:

```
const hasCall = !!(cfg.callsign && String(cfg.callsign).trim());
const hamEnabled = hasCall && mods.amateur !== false;
window.FC_HAM_ENABLED = cfg.setup_complete ? hamEnabled : true;
if (window.applyModeGating) window.applyModeGating();
```

```
function applyModeGating() {
    const btn = document.getElementById('modeBtn-amateur');
    if (!btn) return;
    const disabled = window.FC_HAM_ENABLED === false;
    btn.classList.toggle('disabled', disabled);
    if (disabled) {
        btn.setAttribute('aria-disabled', 'true');
        btn.title = 'Add a station callsign in Setup to enable amateur radio features';
    }
}
```

> **TWO DIFFERENT QUESTIONS — DO NOT CONFLATE THEM** — `identity.js` answers *who is operating* (per device, for attribution). The RF gate answers *may this station transmit at all* (per station callsign, for legality). An operator can be a licensed ham personally, yet the station still shows no transmit features because *the station* has no callsign configured — and that is correct. Never wire a transmit feature to `FC_ID.isHam()`; wire it to the station gate (`FC_HAM_ENABLED` / the `HAM_MODULES` check). The operator badge is about accountability, not authorization.


## Why It Matters / Design Takeaways

- *One shared identity, everywhere.* Every page loads the same `identity.js`, so 'who did this' is answered identically across net control, forms, roster, and map — no per-page reinvention.
- *One record for four kinds of person.* Members and visitors, hams and non-hams, all fold into a single flat object; blank fields, not separate schemas, carry the differences.
- *Attribution without accounts.* Identity is saved on the device with a versioned `localStorage` key and no password — appropriate for a field appliance, and reset in one call.
- *Ham-ness is computed, never trusted.* `isHam()` is just `!!callsign`, so it can never disagree with the callsign actually on record.
- *The RF gate is defense in depth.* A missing station callsign blocks transmit modules at toggle time, again at save time, and again visually on the dashboard — three independent enforcement points, not one.

> **MAINTAINER'S RULE** — Keep the two concerns separate. To change how an operator is identified or displayed, change `identity.js` (and `bestId` if the priority order shifts) and nothing else — every screen inherits it. To change what may transmit, change the *station callsign gate* (`HAM_MODULES` and the `hasCallsign` / `FC_HAM_ENABLED` checks) — never gate a transmit feature on the operator's personal `isHam()`. Any new amateur-radio transmit module must be added to `HAM_MODULES` so the blank-callsign safety net switches it off too, and if you change the stored identity shape incompatibly, bump the `STORE_KEY` version.


# 13. The Dead Man's Switch — deadmans.py

*A dead man's switch watches an active net and, if the net falls silent for too long, raises an alarm — because in emergency communications a net that goes quiet unnoticed is a net that may have lost its operator. This chapter follows the switch from its single stored row through Arm, Reset, and Disarm to the background monitor that computes the warning and the trigger.*

> **IN ONE SENTENCE** — The dead man's switch stores a tiny amount of state in one singleton row, lets net control *Arm*, *Reset*, or *Disarm* the watch on a net, and runs a background loop that flips the state to *warning* at three-quarters of the inactivity threshold and to *triggered* once the threshold is crossed.


## What This Is / What It Is For

In amateur emergency communications a *net* is a scheduled, controlled on-air conversation run by a net control operator. If that operator is incapacitated — a medical event, a power failure, a radio that dies — the net can simply go quiet, and nobody may notice until it is too late to matter. A *dead man's switch* is the safeguard: an automatic monitor that expects to keep seeing activity, and that raises an alarm when the activity stops. FieldCommand implements one as a small always-running loop plus a handful of Hypertext Transfer Protocol (HTTP) endpoints, backed by [python/deadmans.py](python/deadmans.py) and a single database row.

The idea comes from the safety device on a locomotive or a lawn mower: a control the operator must keep engaged, so that if they let go, the machine stops itself. Here there is no pedal to hold — instead the 'engagement' signal is *net activity*. Every check-in, every logged transmission, every traffic entry updates a timestamp. As long as that timestamp keeps moving, the switch stays calm. When it stops moving for longer than the configured threshold, the switch fires.

> **JARGON, IN PLAIN WORDS** — A **net** is an organized on-air meeting of radio stations run by one controller. A **threshold** here is the number of minutes of silence the switch will tolerate before it alarms. **Singleton** means there is only ever *one* of something — one row that holds the entire switch's state, never a table of many. **Armed / warning / triggered / disarmed** are the four states the switch moves between.


## How State Is Kept — One Singleton Row

The entire switch is described by one row in one table. It is defined in [python/db.py](python/db.py) as `dms_state`, and it is a *singleton*: the table exists only to hold row `id=1`, which is inserted once at schema-creation time and never added to. `INSERT OR IGNORE` guarantees the row exists on every boot without ever duplicating it:

```
-- ── Dead Man's Switch (singleton row id=1) ────────────────────────────────────
CREATE TABLE IF NOT EXISTS dms_state (
    id              INTEGER PRIMARY KEY DEFAULT 1,
    state           TEXT NOT NULL DEFAULT 'disarmed',
    armed_nets      TEXT NOT NULL DEFAULT '[]',  -- JSON array
    threshold_min   INTEGER NOT NULL DEFAULT 30,
    last_activity   TEXT,
    armed_at        TEXT,
    triggered_at    TEXT
);
INSERT OR IGNORE INTO dms_state(id) VALUES(1);
```

Keeping all of the state in one row is a deliberate simplification. There is no history to page through and no per-run record to garbage-collect; the switch is either watching or it is not, and its condition right now is the only thing that matters. Each column carries one piece of that condition:

| Column | What it holds |
| --- | --- |
| `state` | The overall condition of the switch: `disarmed`, `armed`, `warning`, or `triggered`. |
| `armed_nets` | Which nets are being watched, stored as a JavaScript Object Notation (JSON) text column so several nets can be armed at once, each with its own threshold and sub-state. |
| `threshold_min` | The default minutes of silence tolerated before the switch fires (30 by default). |
| `last_activity` | Timestamp of the most recent activity seen across the armed nets — the signal the operator is still 'holding the pedal.' |
| `armed_at` | When the switch was armed. Used for display and auditing. |
| `triggered_at` | When the switch fired, or empty if it has not. Set once, so repeated loops do not keep re-stamping it. |

> **WHY armed_nets IS A TEXT COLUMN, NOT A TABLE** — `armed_nets` holds JSON in a single text column rather than being a child table of one-row-per-net. The switch never needs to query *inside* that list from Structured Query Language (SQL) — it always reads the whole switch state at once, adjusts it in Python, and writes it back whole. A text blob is the simplest store for data that is only ever read and written as a unit. If you ever need to filter or join on individual armed nets from SQL, that is the signal to promote it to a real table — until then, do not.


## How It Works — Arm, Reset, Disarm

Net control drives the switch through three actions, exposed as endpoints on the port-5050 Application Programming Interface (API). Each one reads the singleton row, changes it in memory, and writes it back — the row is always the source of truth. *Arm* starts watching a net: it records the chosen threshold (falling back to 30 minutes), stamps the arm time, sets that net's sub-state to `armed`, and moves the overall `state` to `armed`:

```
elif path == "/api/dms/arm":
    nid = str(body.get("net_id","")).strip()
    if not nid: return self.send_json({"error":"net_id required"},400)
    row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
    armed = jload(row["armed_nets"] if row else None, {})
    if not isinstance(armed, dict): armed = {}
    try: thr = int(body.get("threshold", body.get("threshold_min", 30)) or 30)
    except (ValueError, TypeError): thr = 30
    armed[nid] = {"threshold_min": thr, "armed_at": now, "state": "armed", "triggered_at": None}
    c.execute("UPDATE dms_state SET state='armed', armed_nets=?, last_activity=? WHERE id=1", (jdump(armed), now))
    c.commit(); return self.send_json({"ok":True})
```

*Reset* is what an operator does after the switch has fired and they have confirmed the net is fine: it clears that net's `triggered_at` and returns its sub-state to `armed`, so the watch resumes without disarming. It is a rearm, not a stand-down:

```
elif path == "/api/dms/reset":
    nid = str(body.get("net_id","")).strip()
    row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
    armed = jload(row["armed_nets"] if row else None, {})
    if isinstance(armed, dict) and nid in armed:
        armed[nid]["state"] = "armed"; armed[nid]["triggered_at"] = None
        c.execute("UPDATE dms_state SET armed_nets=? WHERE id=1", (jdump(armed),)); c.commit()
    return self.send_json({"ok":True})
```

*Disarm* stops watching a net entirely: it removes that net from `armed_nets`. The clever part is the overall `state` afterward — if any other nets remain armed the switch stays `armed`; only when the last net is removed does it fall back to `disarmed`:

```
elif path == "/api/dms/disarm":
    nid = str(body.get("net_id","")).strip()
    row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
    armed = jload(row["armed_nets"] if row else None, {})
    if isinstance(armed, dict) and nid in armed:
        del armed[nid]
        c.execute("UPDATE dms_state SET armed_nets=?, state=? WHERE id=1", (jdump(armed), "armed" if armed else "disarmed")); c.commit()
    return self.send_json({"ok":True})
```

The 'holding the pedal' signal — `last_activity` — is stamped whenever the net sees action. Elsewhere in the same server, logging a net entry updates it directly (`UPDATE dms_state SET last_activity=? WHERE id=1`), so ordinary net traffic keeps the switch fed without anyone thinking about it.


## How It Works — Computing the Warning and the Trigger

Deciding the switch is not net control's job — it is done by an independent background loop so that it keeps running even if the user interface is idle. [python/deadmans.py](python/deadmans.py) is a standalone service whose `monitor_loop()` wakes every 15 seconds, reads the state, and — only while the switch is `armed` or already in `warning` — works out how long it has been since the last activity. It converts the threshold from minutes to seconds and finds the most recent activity across the armed nets, deliberately skipping any net flagged as a drill so exercises never fire a real alarm:

```
if dms.get("state") in ("armed", "warning"):
    threshold_sec = dms.get("threshold_min", 30) * 60
    armed_nets = dms.get("armed_nets", [])
    latest = dms.get("last_activity")
    for net_id in armed_nets:
        # Skip drill nets
        f = NETS_DIR / f"{net_id}.json"
        if f.exists():
            net = json.loads(f.read_text())
            if net.get("drill", False):
                continue
            act = get_net_last_activity(net_id)
            if act and (latest is None or act > latest):
                latest = act
```

Timestamps are stored as text, so the loop parses the newest one back into a real datetime (tolerating both a trailing `Z` and a missing time zone) and measures the elapsed seconds. Then comes the heart of the switch — a three-way decision:

```
elapsed = (datetime.now(timezone.utc) - last_dt).total_seconds()
prev_state = dms.get("state")
if elapsed > threshold_sec:
    dms["state"] = "triggered"
    if dms.get("triggered_at") is None:
        dms["triggered_at"] = utcnow()
        print(f"[deadmans] TRIGGERED! No activity for {elapsed/60:.1f} minutes")
elif elapsed > threshold_sec * 0.75:
    dms["state"] = "warning"
    if prev_state == "armed":
        print(f"[deadmans] WARNING: {(threshold_sec - elapsed)/60:.1f} min remaining")
else:
    dms["state"] = "armed"
save_json(DMS_STATE_F, dms)
```

Read from the bottom up, the logic is simple and complete. If elapsed silence is under three-quarters of the threshold, the net is healthy — `armed`. Once it passes *75 percent* of the threshold, the switch enters `warning` — a deliberate early alert that gives net control a few minutes to check in before anything fires (at the default 30-minute threshold, the warning begins at 22.5 minutes of silence). Cross the full threshold and it is `triggered`. The `triggered_at` timestamp is written *only* if it was empty, so the loop can run over and over without resetting the moment of the trigger, and the warning message prints only on the transition from `armed`, not on every 15-second pass.

> **TWO MONITORS, ONE DESIGN** — The same warning/trigger math appears in two places: the standalone `deadmans.py` service (shown here, watching `dms_state.json` with a single global threshold) and an in-process `dms_monitor()` inside the port-5050 server, which watches the `dms_state` *table* with a per-net threshold and wakes every 30 seconds. Both use the identical boundaries — `elapsed > threshold` means triggered, `elapsed > threshold * 0.75` means warning. The `dms_state` row is the canonical state the API arms and disarms; `deadmans.py` is the original independent watchdog. If you change the trigger arithmetic, change it in *both* or they will disagree.


## Why It Matters / Design Takeaways

- *Activity is the pedal.* The switch never asks the operator to do anything extra; ordinary net traffic stamps `last_activity`, and silence is what fires it.
- *All state in one row.* The whole switch is one singleton `dms_state` row — no history, no cleanup — so its current condition is always trivially readable.
- *Arm / Reset / Disarm are precise.* Reset rearms after a confirmed false alarm; Disarm removes one net and only stands the switch fully down when the last net leaves.
- *An early warning, not just an alarm.* The 75-percent boundary turns a hard cutoff into a two-stage alert, buying net control time to respond before the trigger.
- *The monitor is independent.* Deciding runs in a background loop, so the switch keeps watching whether or not anyone is looking at a screen.

> **MAINTAINER'S RULE** — The `dms_state` singleton row is the switch's whole truth — read it, change it in memory, write it back whole; never scatter switch state into other tables. The trigger boundaries live in *two* monitors (`deadmans.py` and the 5050 `dms_monitor`) with identical `> threshold` and `> threshold * 0.75` math: if you retune one, retune the other in the same commit, and add a regression test that a net crossing 75 percent goes `warning` and one crossing 100 percent goes `triggered` — with a drill net firing neither.


# 14. The 44Net Gateway Services — amprgate_status.py & amprgate_poll.py

*FieldCommand can reach out onto the Amateur Packet Radio Network (AMPRNet / 44Net) through a second, dedicated Raspberry Pi that runs a WireGuard tunnel and nothing else. Two small Python programs tie that gateway Pi to the main FieldCommand server: amprgate_status.py runs on the gateway and reports and controls the tunnel, and amprgate_poll.py runs on the server and reads that report every 30 seconds so the dashboard can show 44Net health.*

> **IN ONE SENTENCE** — `amprgate_status.py` runs on a separate gateway Pi and serves read-only 44Net tunnel status on port 9000 while keeping tunnel control locked to localhost port 9001, and `amprgate_poll.py` on the FieldCommand server fetches that status every 30 seconds into a JSON file the dashboard reads.


## What This Is / What It Is For

Amateur radio operators are allocated a whole slice of the Internet address space — the `44.0.0.0/8` block, known as the **Amateur Packet Radio Network (AMPRNet / 44Net)**. To route traffic onto it, a station builds an encrypted tunnel to the AMPRNet gateway and then forwards the `44.0.0.0/8` network through that tunnel. FieldCommand does this on a **second Raspberry Pi that does nothing else** — the gateway Pi at `192.168.50.2`, sitting beside the main FieldCommand server at `192.168.50.1`. The gateway Pi owns the WireGuard tunnel, the routing rules, and the firewall for 44Net; the main server never touches any of it directly.

Two programs connect the two Pis. On the gateway Pi, [python/amprgate_status.py](python/amprgate_status.py) is a small web service that reports whether the tunnel is up, how much data has moved, what the routes look like, and how the gateway Pi itself is doing (temperature, memory, uptime). It also — on a strictly separate, localhost-only port — lets a licensed operator with physical access bring the tunnel up, down, or restart it. On the FieldCommand server, [python/amprgate_poll.py](python/amprgate_poll.py) simply asks the gateway for that status every 30 seconds and writes it to a file, so the main dashboard and health monitor can display 44Net state without ever talking to the gateway themselves.

> **JARGON, IN PLAIN WORDS** — **AMPRNet / 44Net** is the block of Internet addresses (everything starting `44.`) reserved for licensed amateur radio use. **WireGuard** is a modern, fast Virtual Private Network (VPN) — an encrypted tunnel between two machines; here the gateway Pi's end is the network interface called `ampr0`. **Gateway** here means the machine that forwards traffic between the local EMCOMM-NET and 44Net. **Part 97** is the section of United States Federal Communications Commission (FCC) rules governing amateur radio; it requires station identification, which is why access is logged.


## Why the Gateway Is Its Own Pi — the 'Why' Behind the Split

The gateway is deliberately a separate machine so that the risky, privileged work of routing a public Internet block never runs inside the incident-management server. The gateway Pi holds the WireGuard private key, runs Internet Protocol (IP) forwarding, and rewrites firewall rules every time the tunnel comes up or down — all of which is defined in the tunnel config the installer writes:

```
PostUp   = ip route add 44.0.0.0/8 dev ampr0 2>/dev/null || true
PostUp   = iptables -A FORWARD -i ampr0 -o eth0 -j ACCEPT
PostUp   = iptables -A FORWARD -i eth0 -o ampr0 -j ACCEPT
PostUp   = iptables -t nat -A POSTROUTING -o ampr0 -j MASQUERADE
```

Keeping that on its own Pi means a problem on the gateway — a crashed tunnel, a firewall mistake, a reboot — cannot take down net control, the roster, or the forms on the main server. The two machines fail independently. It also keeps the security boundary crisp: the gateway exposes exactly one read-only status endpoint to the network and keeps every control action physically local, which is the model the rest of this chapter walks through.

> **WHY THE INSTALLER LIVES SEPARATELY TOO** — The gateway is set up by its own script, `scripts/setup_44net.sh`, which the banner explicitly says runs on the DEDICATED GATEWAY PI (192.168.50.2), NOT on the FieldCommand server Pi (192.168.50.1). It installs WireGuard, enables IP forwarding, writes `/etc/wireguard/ampr0.conf`, and installs `amprgate_status.py` as a systemd service. The separation is baked in from installation onward, not just at runtime.


## How It Works — The Split-Port Security Model

The single most important design decision in `amprgate_status.py` is that **status and control live on different ports with different reach**. The file's own header spells it out, and the two ports are set at the top of the configuration block:

```
PUBLIC_PORT    = 9000          # Status + UI — accessible from EMCOMM-NET
CONTROL_PORT   = 9001          # Tunnel control — localhost only
WG_INTERFACE   = "ampr0"
```

Port 9000 is bound to all interfaces (`0.0.0.0`) so any device on the EMCOMM-NET can read status and so the FieldCommand server's poller can reach it. Port 9001 is bound to `127.0.0.1` only, which means the operating system itself will not accept a connection to it from anywhere but the gateway Pi's own keyboard. There is no network path to the control port — you have to be sitting at the machine. The two servers are started as two separate `HTTPServer` objects with two different handler classes:

```
def run_public_server():
    server = HTTPServer(("0.0.0.0", PUBLIC_PORT), PublicHandler)
    ...
    server.serve_forever()

def run_local_server():
    server = HTTPServer(("127.0.0.1", CONTROL_PORT), LocalHandler)
    ...
    server.serve_forever()
```

The public `PublicHandler` serves the dashboard UI, the login endpoints, and the read-only `/api/status` — but if anyone tries to reach a tunnel-control action on the public port, it is refused outright with a message telling them where control actually lives:

```
elif path.startswith("/api/tunnel/"):
    # Tunnel control blocked on public port — must use localhost:9001
    self.send_json({
        "ok": False,
        "error": "Tunnel control requires physical access to the gateway Pi. "
                 "Use the local keyboard and browser at http://localhost:9001",
    }, 403)
```

The `LocalHandler` on 9001 is the only place `tunnel_action()` — the code that actually shells out to `wg-quick up`/`down`/`restart` — can be reached. And even there, a valid callsign session is still required before anything happens, so control demands **both** physical presence at the Pi **and** a logged-in licensed operator:

```
token = get_token_from_request(self)
session = validate_session(token)

if not session:
    self.send_json({
        "ok": False,
        "error": "Valid callsign session required. "
                 "Log in at http://192.168.50.2:9000 first.",
    }, 401)
    return
```

> **DEFENSE IN DEPTH, NOT ONE LOCK** — Three independent barriers guard bringing the tunnel up or down: (1) the control port is bound to localhost, so there is no network route to it at all; (2) the installer's firewall rule `ufw deny in on eth0 to any port 9001` blocks it a second time even if the binding ever changed; and (3) the handler still checks for a valid FCC callsign session. Never collapse these into one. Each is there because the other two might someday fail.


## How It Works — Building the Status Report

Everything the status service reports is assembled by `build_status()`, which gathers the tunnel state and the gateway Pi's own vital signs into one dictionary. It is what both `/api/status` endpoints return and what the poller on the server ends up storing:

```
def build_status():
    wg = get_wg_status()
    mem_used, mem_total = get_mem()
    return {
        "timestamp": utcnow(),
        "gateway_ip": "192.168.50.2",
        **wg,
        "cpu_temp": get_cpu_temp(),
        "mem_used_mb": mem_used,
        "mem_total_mb": mem_total,
        "uptime": get_uptime(),
        "ip_forward": get_ip_forward(),
        "routes": get_routes(),
        "peers": get_peers(),
        "access_log": get_access_log(),
    }
```

The tunnel half comes from `get_wg_status()`, which shells out to `wg show ampr0 dump` and reads the raw tab-separated dump WireGuard produces. The key judgement it makes is deciding whether the tunnel is really **up**: it is not enough for the interface to exist — there must be a recent handshake. The code treats the tunnel as up only if it has a 44-address and the last handshake was under five minutes ago:

```
tunnel_up = (ampr_addr is not None and
             hs_epoch_val > 0 and
             (int(time.time()) - hs_epoch_val) < 300)
```

> **WHY A HANDSHAKE, NOT JUST AN INTERFACE** — A WireGuard interface can be configured and have an address while the far end is unreachable — the tunnel looks present but carries nothing. WireGuard only records a handshake timestamp when the two ends actually exchange keys. Checking that the handshake is recent (under 300 seconds) is how the code distinguishes a live tunnel from a dead one that merely still has its interface configured.

The system half — `get_cpu_temp()`, `get_mem()`, `get_uptime()`, `get_ip_forward()` — reads the Pi's own kernel files (`/sys/class/thermal`, `/proc/meminfo`, `/proc/uptime`, `/proc/sys/net/ipv4/ip_forward`) and each wraps its work in a try/except that returns `None` on failure. That matters because the status page must never crash just because one sensor could not be read; a missing value simply shows as a dash on the dashboard. `get_routes()` confirms the `44.0.0.0/8` route is present, and `get_peers()` lists the tunnel peers with their last-handshake age.


## How It Works — Callsign Lookup Back to the Server

Before the gateway will issue a login session, it validates the callsign. It does a quick format check itself, then — for the authoritative answer — calls **back across the LAN to the FieldCommand server's FCC database**. This is the one place the gateway reaches into the main server. The endpoint and its Secure Sockets Layer (SSL) context are configured at the top of the file:

```
# FCC lookup on the FieldCommand Pi, reached via its HTTPS reverse proxy at /svc/5050
import ssl as _ssl
FIELDCOMMAND_API = "https://192.168.50.1/svc/5050"
_FC_SSL = _ssl.create_default_context()
_FC_SSL.check_hostname = False
_FC_SSL.verify_mode = _ssl.CERT_NONE
```

Two things are worth understanding here. First, the call now goes over **HTTPS** to the server's reverse proxy path `/svc/5050`, because the core FCC Application Programming Interface (API) is bound to localhost on the server and is no longer exposed in cleartext. Second, because this crosses the LAN to a Pi presenting a **self-signed or local-Certificate-Authority (CA) certificate**, the code deliberately turns certificate verification off for this one call. The comment in the source explains the reasoning precisely: the FCC data is public, and the lookup degrades gracefully if it fails, so skipping verification of the LAN's own certificate is an accepted trade-off here — not a pattern to copy for anything sensitive. The lookup itself passes that context into the request:

```
url = f"{FIELDCOMMAND_API}/callsign/{cs}"
req = urllib.request.Request(url, headers={"User-Agent": "amprgate/1.0"})
with urllib.request.urlopen(req, timeout=5, context=_FC_SSL) as resp:
    data = json.loads(resp.read().decode())
    if data.get("found"):
        return {"valid": True, "name": data.get("name", ""),
                "license_class": data.get("license_class", ""), "error": None}
```

The graceful fallback is the important safety net. If the FieldCommand server is unreachable — powered off, rebooting, unplugged — the gateway must still be usable, so a network failure falls back to format-only validation and logs that it did so, rather than locking every operator out:

```
except urllib.error.URLError:
    # FieldCommand Pi unreachable — fall back to format-only validation
    access_log("FCC-FALLBACK", cs, "localhost",
               "FieldCommand Pi unreachable — format-only validation used")
    return {"valid": True, "name": None,
            "license_class": "Unknown (FCC DB offline)",
            "error": None, "fallback": True}
```

> **EVERY ACCESS IS LOGGED FOR PART 97** — Logins, failures, logouts, FCC fallbacks, and every tunnel action are written to `/var/log/amprgate-access.log` via `access_log()`. This is not decoration — Part 97 requires station identification, and this log is how the gateway records which licensed operator did what and when. When you add any new privileged action, log it the same way.


## How It Works — The Poller on the Server

The gateway service is only half the picture. The FieldCommand server needs 44Net status on its own dashboard, but the server never talks to the gateway on demand — instead `amprgate_poll.py` runs as a small loop that fetches the status every 30 seconds and writes it to a file. Its whole job is stated in its header, and its configuration is four constants:

```
GATEWAY_URL = "http://192.168.50.2:9000/api/status"
OUTPUT_FILE = Path("/opt/fieldcommand/data/amprgate_status.json")
POLL_INTERVAL = 30  # seconds
TIMEOUT = 5         # seconds per request
```

The poll reads the gateway's read-only status endpoint (no authentication, because it is read-only public data) and stamps the result with when it was polled and whether the gateway answered at all. If the gateway is unreachable, it does not crash or leave a stale file — it writes a clearly-marked `reachable: False` record instead:

```
def poll():
    try:
        with urllib.request.urlopen(GATEWAY_URL, timeout=TIMEOUT) as resp:
            data = json.loads(resp.read().decode())
            data["polled_at"] = utcnow()
            data["reachable"] = True
            return data
    except urllib.error.URLError as e:
        return {"reachable": False, "tunnel": "unknown",
                "error": str(e.reason), "polled_at": utcnow(),
                "gateway_ip": "192.168.50.2"}
```

The write is **atomic** — it writes to a temporary file and then renames it over the real one — so a dashboard reading the file never catches a half-written JSON document. A rename on the same filesystem is atomic; a reader either sees the whole old file or the whole new one, never a torn mix:

```
def write(data):
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(OUTPUT_FILE)
    except Exception as e:
        print(f"[amprgate-poll] Write error: {e}")
```

This poll-to-a-file pattern is the same decoupling FieldCommand uses elsewhere: the network call and the display are separated by a file on disk. The dashboard reads a local file that is always valid and at most 30 seconds old; it never has to wait on, retry, or handle errors from a cross-Pi HTTP call. If the gateway is down, the file simply says so.


## Why It Matters / Design Takeaways

- *Physical separation of concerns.* The gateway is its own Pi so that routing a public Internet block — private keys, IP forwarding, firewall rewrites — can never destabilize the incident-management server. The two fail independently.
- *Status is open, control is local.* Read-only status is served to the whole EMCOMM-NET on port 9000; tunnel control is bound to localhost port 9001, firewalled a second time, and still requires a callsign session. Presence plus identity, never one alone.
- *Reach back, but degrade gracefully.* Callsign validation calls the server's FCC database over HTTPS (skipping verification only for the LAN's own local certificate, on public data), and falls back to format-only validation — logged — when the server is unreachable, so the gateway is never bricked by a server outage.
- *Decouple with a file.* The server never queries the gateway on demand; a 30-second poller writes an always-valid, atomically-replaced JSON file that the dashboard reads. Network latency and gateway outages never reach the UI.

> **MAINTAINER'S RULE** — Never move tunnel control onto the public port, and never bind the control server to anything but `127.0.0.1`. Any new privileged gateway action goes through `LocalHandler` on 9001, requires a valid session, and calls `access_log()` for Part 97. Keep the certificate-verification bypass scoped to the single, public, gracefully-degrading FCC callsign lookup — do not reuse `_FC_SSL` for any call that carries private data or that must not silently fail. And keep the poller's writes atomic (temp file then rename) so the dashboard always reads whole JSON.


# 15. WAN Failover — wan_monitor.py

*FieldCommand is built to run with no internet at all. But when internet IS available, one small program — python/wan_monitor.py — manages up to two internet sources, decides which one is carrying traffic, detects when the preferred one drops, and falls back to the other automatically. It writes a status file the dashboard and the WAN Settings screen read.*

> **IN ONE SENTENCE** — `wan_monitor.py` checks internet every 30 seconds, tries the operator's preferred internet source first and the fallback second using one of three detection methods, and writes an atomic status file that the dashboard and the WAN Settings screen read.


## What This Is / What It Is For

FieldCommand is an **offline-first** system: every core feature — nets, roster, forms, resources, the map — works with no internet whatsoever, because in the field there usually is none. But sometimes there is: a cellular modem, a satellite dish, a phone hotspot, a wired connection at a fixed site. When internet is available, it is worth using — and it is worth having a **backup** internet source that takes over automatically when the first one drops. That is the job of **Wide Area Network (WAN)** failover, and it lives entirely in one file, [python/wan_monitor.py](python/wan_monitor.py).

The monitor runs as a small loop, waking every 30 seconds to answer three questions: is there internet at all right now; if so, which of the configured sources is carrying it; and what are the details of each source (carrier, signal strength, throughput) worth showing on the dashboard. It writes those answers to a status file. It does **not** switch physical connections itself — the operating system and the hardware handle the actual routing — the monitor's job is to **detect and report** which source is live so the rest of FieldCommand, and the operator, always know the true state.

> **JARGON, IN PLAIN WORDS** — **WAN (Wide Area Network)** here just means 'the internet connection' — the link out of the local site to the wider world. **Failover** means automatically switching to a backup when the main one fails. **Preferred** and **fallback** are the two roles a source can hold: preferred is tried first, fallback is the backup. A **poll** is one round of checking; the monitor polls every 30 seconds.


## Why an Offline-First System Still Has Failover — the 'Why'

It would be easy to assume that a system designed to work without internet does not need to manage internet carefully. The opposite is true. Precisely because FieldCommand only reaches out when a link exists, the moments a link *does* exist are valuable and often fragile — a cellular signal that fades behind a building, a satellite dish that loses its view of the sky, a hotspot whose battery dies. Having a second source that quietly takes over, and a dashboard that honestly shows which one is live, is what turns 'we had internet for a while' into 'we kept internet.'

The design is deliberately **technology-agnostic**. The monitor makes no assumption about which slot holds which kind of connection — the file's own docstring is explicit that either source can be cellular, satellite, fixed ISP, or hotspot, and that 'the role is what matters, not the type.' What decides priority is the role an operator assigned, not the hardware:

```
# Each WAN source has a role — 'preferred' or 'fallback'.
# The preferred source is tried first. If it's down or not detected,
# the fallback source is used. Either source can be cellular, satellite,
# fixed ISP, hotspot, or any other type. No assumptions about which
# slot is which technology.
```


## How It Works — The Source Model and Config

Configuration is a JSON file, loaded with a clear order of preference: the site's own saved config first, then a shipped defaults file, then — if both are missing — a bare hard-coded minimum so the monitor can never fail to start:

```
def load_config():
    """Load WAN config — site config first, fallback to defaults."""
    for path in [CONFIG_FILE, DEFAULTS_FILE]:
        try:
            with open(path) as f:
                cfg = json.load(f)
            # Migrate old primary_wan/secondary_wan format to wan_sources array
            if "primary_wan" in cfg and "wan_sources" not in cfg:
                cfg = _migrate_old_config(cfg)
            return cfg
        except Exception:
            pass
```

Each source in the `wan_sources` array carries an `id`, an `enabled` flag, a `role` (`preferred` or `fallback`), a human `label`, a `type`, and — the important part for failover — a `detection_method`. Notice the config also carries a migration step: an older format stored `primary_wan`/`secondary_wan` keys, and `_migrate_old_config()` converts those to the newer role-based `wan_sources` array on the fly, so a site that upgrades keeps its settings. This mirrors the same forward-compatibility discipline the data layer uses — old configs are brought forward, never broken.

> **WHY ROLES, NOT SLOTS** — Storing a `role` on each source instead of hard-coding 'source A is primary' means an operator can swap which connection is preferred without rewiring anything — the Settings screen even has a one-click 'swap roles' button. The monitor simply sorts by role at poll time, so the same two configured sources can trade priority instantly.


## How It Works — The Three Detection Methods

The heart of failover is deciding whether a given source is actually reachable right now. That is `check_source()`, and it supports three methods — each a different level of certainty about whether a WAN path is truly live:

```
def check_source(source):
    method = source.get("detection_method", "internet_only")
    if method == "internet_only":
        return True   # caller already confirmed internet is up
    elif method == "ping":
        host = source.get("ping_host", "")
        if not host:
            return False
        ok, _ = ping_test(host, count=1, timeout=2)
        return ok
    elif method == "admin_reachable":
        url = source.get("admin_url", "")
        if not url:
            return False
        ok, _, _ = http_test(url, timeout=source.get("admin_timeout_s", 3))
        return ok
    return False
```

| Method | What it tests | When to use it |
| --- | --- | --- |
| `internet_only` | Nothing source-specific — it trusts the caller's earlier internet check. Always returns `True` once internet is confirmed up. | A phone hotspot or USB dongle with no queryable address, or when there is only one WAN source and you just need up/down. |
| `ping` | Pings an address that only answers when this WAN path is active (a modem or hotspot gateway IP). Reachable means the path is live. | Two sources where each modem's gateway IP is only reachable over its own path (e.g. Starlink at `192.168.100.1`, Android hotspot at `192.168.43.1`). |
| `admin_reachable` | Makes an HTTP request to the modem's admin page. Answering means the path is live — and the page body may reveal carrier and signal. | A modem/router with a web interface, when you want the bonus of carrier name and signal strength detection. |

The `ping` and `admin_reachable` methods both fail **closed** — if the source has no host or URL configured, or the test does not succeed, they return `False`, so an unconfigured or unreachable source is never mistaken for a live one. Only `internet_only` returns `True` unconditionally, and only because the caller has already proven internet is up before it is ever consulted.


## How It Works — One Poll Cycle

`poll()` runs one full decision. It first establishes whether there is any internet at all by pinging a well-known public address; if that fails, nothing downstream matters and no source is marked active:

```
# Test internet connectivity first
internet_ok, internet_latency = ping_test("1.1.1.1")
```

If internet is up, the enabled sources are **sorted so the preferred role comes first**, and the first one that passes its detection test becomes the active source. This single sort is the whole failover policy — preferred wins when it is reachable; the fallback is only reached if the preferred source fails its check:

```
ordered = sorted(enabled, key=lambda s: (0 if s.get("role") == "preferred" else 1))

for source in ordered:
    if check_source(source):
        active_source_id = source.get("id")
        active_label     = source.get("label", "WAN")
        break
```

There is a careful edge case right after: if internet is up but no source matched — which happens when every source uses `internet_only` and so none 'claims' the link — the code still needs to name an active source rather than show a blank. It picks the first preferred source, or failing that the first source at all, so the dashboard always attributes a live link to something sensible:

```
# If no specific source matched (e.g. all internet_only), use first preferred
if not active_source_id and enabled:
    pref = [s for s in ordered if s.get("role") == "preferred"]
    if pref:
        active_source_id = pref[0].get("id")
        active_label     = pref[0].get("label", "WAN")
```

Once the active source is chosen, `get_source_details()` gathers display detail for every enabled source. When a source exposes an admin page, the monitor scrapes it for carrier name, cellular technology, signal strength, and — for satellite terminals that expose a JSON status like Starlink — latency, throughput, obstruction, and uptime. The signal-strength banding is a good example of turning a raw number into something an operator reads at a glance:

```
rssi_m = re.search(r"rssi[\":\s]+(-?\d+)", body, re.I)
if rssi_m:
    rssi = int(rssi_m.group(1))
    result["signal_dbm"] = rssi
    result["signal_strength"] = (
        f"Excellent ({rssi} dBm)" if rssi >= -70 else
        f"Good ({rssi} dBm)"      if rssi >= -85 else
        f"Fair ({rssi} dBm)"      if rssi >= -100 else
        f"Poor ({rssi} dBm)"
    )
```

> **WHY THE OUTPUT CARRIES 'LEGACY' KEYS** — `poll()` returns both the new structured `wan_sources` map and older flat keys like `instyconnect`, `starlink`, `primary_wan`, and `secondary_wan`. Those are there so an older dashboard (`wan-status.html`) that expected the previous shape keeps working after the role-based rewrite. When you add a field, add it to the new structure; only touch the legacy keys if you are deliberately maintaining that old view.


## How It Works — Writing Status and Surviving Errors

Like the 44Net poller, the monitor writes its result **atomically** — temp file, then rename — so a dashboard reading `wan_status.json` never sees a half-written file:

```
def write_status(data):
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(OUTPUT_FILE)
    except Exception as e:
        print(f"[wan-monitor] Write error: {e}")
```

The main loop is built so a single bad poll can never stop the monitor. If `poll()` throws for any reason, the loop catches it, prints it, and writes an honest 'everything disconnected' status rather than leaving a stale file or dying:

```
while True:
    try:
        data = poll()
        write_status(data)
        ...
    except Exception as e:
        print(f"[wan-monitor] Poll error: {e}")
        write_status({
            "timestamp": utcnow(), "active_source": "none",
            "error": str(e),
            ...
            "wan_sources":  {},
        })
    time.sleep(POLL_INTERVAL)
```


## How It Works — The Front End

The operator side of failover is [html/wan_settings.html](html/wan_settings.html), the WAN / Internet Settings screen. It presents exactly two source cards — Source A and Source B — each with a role badge, an enabled toggle, and the fields the monitor reads: display name, role, type, provider, detection method, and (shown only when relevant) a ping host or admin URL. The screen's intro states the same policy the monitor enforces, in plain words, including that changes take effect on the next 30-second poll:

```
The <strong>preferred</strong> source is tried first.
If it's down or not detected, the <strong>fallback</strong> source is used automatically.
Either source can be cellular, satellite, hotspot, or fixed — the role is what matters, not the type.
Changes take effect within 30 seconds (next poll cycle).
```

The detection-method dropdown drives which extra field appears, and the page shows tailored inline help for each method — real gateway IPs for common hotspots and satellite terminals — so an operator never has to guess. The 'swap roles' button is pure convenience over the role model: it just exchanges the two role values and re-renders, letting the operator flip preferred and fallback in one click:

```
function swapRoles() {
  const ra = document.getElementById('role_a');
  const rb = document.getElementById('role_b');
  const tmp = ra.value;
  ra.value  = rb.value;
  rb.value  = tmp;
  updateCard('a');
  updateCard('b');
}
```

Save posts the assembled config to the Incident Command System (ICS) service (`/svc/5055/api/ics/wan_config`), which persists it to the same `wan_config.json` the monitor reads on its next cycle. The card visuals — the green left border for preferred, amber for fallback, dimmed for disabled — are a live reflection of the role model, updated as the operator edits, so what they see always matches what the monitor will do.


## Why It Matters / Design Takeaways

- *Offline-first, but opportunistic.* FieldCommand needs no internet, yet when a link exists the monitor makes the most of it and keeps a backup ready — turning fragile connectivity into resilient connectivity.
- *Role, not hardware.* Priority is the operator-assigned `preferred`/`fallback` role, sorted at poll time. Any technology can hold either role, and the two can swap in one click.
- *Right-sized detection.* Three methods trade certainty for simplicity — trust internet, ping a path-specific gateway, or query a modem admin page (which also yields carrier and signal). Ping and admin checks fail closed.
- *Never dies, never lies.* A bad poll is caught and reported as an honest disconnected status; the status file is written atomically so the dashboard always reads whole, current JSON.
- *Forward-compatible.* Old `primary_wan`/`secondary_wan` configs migrate to the role array on load, and the output keeps legacy keys so the previous dashboard view keeps working.

> **MAINTAINER'S RULE** — Failover policy lives in one place — the role sort in `poll()`. To change priority behavior, change that sort, not the detection methods. Keep detection methods failing closed (no host/URL or a failed test means `False`); only `internet_only` may return `True`, and only after the internet ping has already passed. Add new fields to the structured `wan_sources` output, leave the legacy keys alone unless you are deliberately maintaining the old dashboard, and keep every config change backward-compatible via `_migrate_old_config()`. Always write the status file atomically (temp then rename).


# 16. Member ID Cards, Access Cards, and Offline QR — gen_id_cards.py & gen_operator_cards.py

*Two small Python scripts turn the roster into laminate-ready cards on plain business-card stock. gen_id_cards.py prints the modern two-sided photo credential — front with a real, scannable Quick Response (QR) code drawn entirely offline; back with the network-access details — while the older gen_operator_cards.py prints the Wi-Fi access card it grew out of. Both are fully agency-neutral, driven from the station's own configuration.*

> **IN ONE SENTENCE** — `gen_id_cards.py` reads the roster and the station's configuration, and draws a two-sided photo identity (ID) card per member — front with photo, identifiers, and a real offline QR that the check-in scanner reads; back with Wi-Fi and dashboard access — laid out ten to a sheet for a home printer, and the web server generates it on demand at `/api/id_cards.pdf`.


## What This Is / What It Is For

When a team shows up to staff an incident, two paper things make the day run: a **photo credential** that proves who someone is and lets them check in, and an **access card** that tells them how to get onto the field network. FieldCommand produces both from the roster it already holds, so nobody has to retype names into a design program. Two scripts under `python/` do this: [python/gen_id_cards.py](python/gen_id_cards.py) is the current, richer generator — a two-sided photo ID card — and [python/gen_operator_cards.py](python/gen_operator_cards.py) is the earlier Wi-Fi-access-only card it grew out of, kept because it still prints a clean single-sided access card and reads a Comma-Separated Values (CSV) file as well as the database.

Both scripts are built on the same idea: lay out cards on **Avery 5371 / 5874 / 8371** business-card stock — ten cards per Letter sheet, each 3.5 inches by 2 inches — using ReportLab's drawing canvas, then print double-sided and cut. Neither needs the internet, a design tool, or a card-printing service. On a Raspberry Pi in a shelter with no connectivity, that self-containment is the whole point.

> **JARGON, IN PLAIN WORDS** — **ReportLab** is a Python library that draws Portable Document Format (PDF) pages by placing text, shapes, and images at exact coordinates — like an artist working on graph paper. **QR code** (Quick Response code) is the square barcode a phone or 2D scanner reads. **Canvas** is ReportLab's blank page you draw onto; its origin (0, 0) is the **bottom-left** corner, so a larger Y means higher up the page.

The most important design promise, stated at the top of `gen_id_cards.py`, is that nothing is tied to any one group. Every piece of branding — organization name, callsign, logo, and even the labels on the identifier fields — is read from `station_config`, the single-row table the Setup screen fills in:

```
AGENCY-NEUTRAL: every branding value (org name, callsign, logo, and the ID-field
labels) is read from station_config, which the Setup screen fills in. Nothing is
hardcoded to any one group — the same code prints correct cards for any agency.
```

That is the difference you will feel first when comparing the two files. The older `gen_operator_cards.py` still carries hardcoded constants near the top — `ORG_SHORT = 'MCESV/MCEMA'`, `CALLSIGN = 'K9ESV'`, a fixed logo path — because it predates the agency-neutral rule. The newer `gen_id_cards.py` has none of that; it pulls the same values from the database at print time. When you maintain these, treat `gen_id_cards.py` as the model and `gen_operator_cards.py` as legacy.


## Why the QR Is Drawn Locally — the 'Why' Behind the Choice

Earlier versions of FieldCommand made a QR code the easy way: they asked Google's chart web service to render one and embedded the returned image. That service was shut down, so every QR silently broke — a bad failure for an offline field tool that is supposed to work with no internet at all. The fix was to stop depending on anyone else's server and draw the QR **inside the process**, with ReportLab's own barcode widget. The same replacement was made in the main server's `/api/qr` endpoint, whose comment records the history plainly:

```
def qr_svg(data, size_px=220):
    """Render `data` as a scannable QR code and return it as an SVG string.
    Generated locally with ReportLab — no internet, no external service. This is
    what replaces the old (now-dead) chart.googleapis.com dependency."""
```

So there are two places a QR is produced from the same underlying widget, and it helps to keep them straight. On the **card**, `gen_id_cards.py` draws the QR directly into the PDF as vector shapes. On **screen**, the Federal Communications Commission (FCC) lookup server's `/api/qr` endpoint renders the same kind of QR as a Scalable Vector Graphics (SVG) image so the roster page can show or download one for any member. Both are offline; both encode the member's `barcode_id`; both exist because the online shortcut died.

> **WHY THIS MATTERS FOR THE FIELD** — A credential whose QR only works with internet access is worse than no QR at all, because it fails at exactly the moment the tool is needed — during an activation, off-grid. Drawing the QR locally is not a nicety; it is what makes the check-in workflow trustworthy. Never reintroduce a network call into card or QR generation.


## How It Works — Drawing One Card

The heart of `gen_id_cards.py` is `draw_id_card(c, x, y, member, cfg)`. It receives the canvas `c`, the bottom-left corner `(x, y)` of one card slot, the member's data as a dictionary, and the station configuration `cfg`. Everything on the card is positioned relative to that corner in inches, so the same function works no matter which of the ten slots it is filling. Its own docstring states the contract:

```
def draw_id_card(c, x, y, member, cfg):
    """Draw a single 3.5" x 2" member ID card. (x, y) is the bottom-left corner."""
```

The first thing it does is resolve branding from `cfg`, always with a fallback so a half-configured station still prints something sensible. Note how the identifier-field **labels** themselves come from configuration — an agency that calls its number a 'Badge Number' instead of 'Member ID' gets its own wording:

```
org_short  = (cfg.get('org_short') or cfg.get('org_name') or 'FieldCommand').strip()
org_full   = (cfg.get('org_name') or org_short).strip()
call_org   = (cfg.get('callsign') or '').strip()
mid_label  = (cfg.get('ps_member_id_label') or 'Member ID').strip()
rid_label  = (cfg.get('ps_id_label') or 'Radio ID').strip()
```

Then it pulls the member's own fields, and makes one important decision: the QR encodes `barcode_id`, but if that is empty it falls back through `member_id`, then `callsign`, then the internal row `id`. In other words, the QR always encodes **something the scanner can match**, chosen in order of preference:

```
barcode   = (member.get('barcode_id') or member_id or callsign or
             member.get('id') or '').strip()
is_ham    = bool(callsign)
type_tag  = {'visitor': 'MUTUAL AID', 'mutual_aid': 'MUTUAL AID'}.get(mtype, 'MEMBER')
```

From there the drawing is deliberate and ordered: a white rounded card body, a navy header band with a thin gold accent line, the logo and organization name in the header, a membership-type tag on the right, the photo on the left, the name and role on the right, an identifier panel, the QR at bottom-right, and a footer band. Each region is drawn with plain ReportLab calls — `roundRect`, `rect`, `drawString`, `drawImage` — clipped to the rounded corners so the colored bands do not spill past the card edge:

```
# ── Header band ─────────────────────────────────────────────────────────────
c.saveState()
p = c.beginPath()
p.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch)
c.clipPath(p, stroke=0, fill=0)
c.setFillColor(EOC)
c.rect(x, y + CARD_H - HB, CARD_W, HB, fill=1, stroke=0)
c.setFillColor(GOLD)
c.rect(x, y + CARD_H - HB - 0.022 * inch, CARD_W, 0.022 * inch, fill=1, stroke=0)
c.restoreState()
```

Two small helpers keep the layout honest. `_fit(c, text, font, max_w, start_sz)` shrinks a font size step by step until the text fits the available width, so a long name never runs off the card. `_labeled_field(c, x, y, w, label, value)` draws the credential's signature look — a tiny uppercase label with the value in bold beneath it — and is reused for each identifier in the panel. The identifier panel builds a list of up to three fields from whatever the member actually has, so a licensed operator shows a callsign while a non-ham shows only the identifiers that apply:

```
fields = []
if callsign:
    fields.append(('Callsign', callsign))
if member_id:
    fields.append((mid_label, member_id))
if radio_id:
    fields.append((rid_label, radio_id))
fields = fields[:3] or [('ID', barcode or '—')]
```


## How It Works — The Real, Scannable QR

The QR is built by `_qr_drawing`, and it is worth reading closely because the same math appears in the server's `qr_svg`. A `QrCodeWidget` knows how to render the code, but at its own natural size; the helper wraps it in a `Drawing` and applies a transform that scales and shifts the widget so it exactly fills a `size_pt`-by-`size_pt` square:

```
def _qr_drawing(data, size_pt):
    """A ReportLab Drawing of a real, scannable QR for `data`, size_pt square."""
    q = QrCodeWidget(str(data), barLevel='M')
    b = q.getBounds()
    w = (b[2] - b[0]) or 1
    h = (b[3] - b[1]) or 1
    d = Drawing(size_pt, size_pt)
    d.transform = [size_pt / w, 0, 0, size_pt / h, -b[0] * size_pt / w, -b[1] * size_pt / h]
    d.add(q)
    return d
```

> **JARGON, IN PLAIN WORDS** — `getBounds()` returns the four edges of the QR at its natural size. The six numbers in `transform` are a standard affine transform: the first and fourth scale it to the square you want, and the last two slide it so its corner lands at the origin. `barLevel='M'` is the error-correction level — Medium — which lets a scanner still read the code if part of it is smudged or the lamination glares.

On the card, the QR is boxed in a white square with a thin border (so it stays scannable against any background) and then drawn with `renderPDF.draw`. The whole block is wrapped so that a bad value can never crash a whole sheet of cards — a single unreadable member should not stop the other nine from printing:

```
if barcode:
    c.setFillColor(white)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.5)
    c.rect(qx - 0.03 * inch, qy - 0.03 * inch, QSZ + 0.06 * inch, QSZ + 0.06 * inch,
           fill=1, stroke=1)
    try:
        renderPDF.draw(_qr_drawing(barcode, QSZ), c, qx, qy)
    except Exception:
        pass
```

That encoded value is the same string the **Scan Check-In** page and any Universal Serial Bus (USB) or Bluetooth 2D barcode scanner look up. The card and the check-in flow agree on `barcode_id` as the shared key, which is what makes 'scan the card to check in' work end to end.


## How It Works — Embedding Photos Without an Image Library

Photos are stored in the database as base64 text (a plain-text encoding of the raw image bytes). `_img_reader` turns that back into something ReportLab can place, and its docstring explains a deliberate constraint: photos are kept as JPEG specifically so ReportLab can embed them **without** the Python Imaging Library (PIL), which is a heavy dependency to avoid on a small appliance:

```
def _img_reader(b64_or_dataurl):
    """Return a ReportLab ImageReader from base64 (or a data: URL), or None.
    Photos are stored/exported as JPEG so ReportLab embeds them without needing
    the Python Imaging Library (PIL)."""
    raw = (b64_or_dataurl or '').strip()
    if not raw:
        return None
    if raw.startswith('data:'):
        raw = raw.split(',', 1)[-1]
    try:
        return ImageReader(io.BytesIO(base64.b64decode(raw)))
    except Exception:
        return None
```

If there is no photo, the card does not leave an ugly gap — it draws a soft panel with the member's initials, so every card looks finished whether or not a picture is on file. The same `_img_reader` handles the organization logo in the header, so an agency with no logo simply gets clean text instead.


## How It Works — Who Gets a Card, and the Sheet Layout

Not everyone in the roster is a member. Walk-ins and mutual-aid personnel are in the same table but should not be handed a full credential unless a partner agency has already supplied a photo. `_include` encodes exactly that rule:

```
def _include(m):
    """Members get a card. Walk-ins / mutual-aid only if they have a photo."""
    mtype = (m.get('member_type') or 'member')
    if mtype in ('visitor', 'mutual_aid'):
        return bool(m.get('photo_data'))
    return True
```

`generate_cards` then paginates the eligible members ten to a sheet and, by default, prints a matching **back** for every front so the sheet can be run through the printer twice for double-sided cards. The clever part is the mirroring: when printing the second side, the columns are flipped so each back lands behind its own front after the sheet is turned over on its long edge:

```
for i, m in enumerate(pg):
    col = i % COLS
    row = i // COLS
    if kind == 'back':
        col = COLS - 1 - col   # mirror for long-edge duplex flip
    x = LEFT_M + col * CARD_W
    y = PAGE_H - TOP_M - (row + 1) * CARD_H
```

The back itself, drawn by `draw_card_back`, is the network-access card: the Wi-Fi network name and password and the dashboard address, all again from `station_config` (`wifi_ssid`, `wifi_pass`, `server_url`). This is the same information the older `gen_operator_cards.py` puts on the front of its single-sided card — the newer script simply moved it to the back of the credential so one printed card does both jobs.


## How It Works — The Web Endpoint That Generates on Demand

A field operator never runs the script by hand. The roster page has a print button that opens the FCC lookup server's `/api/id_cards.pdf` endpoint, which imports the script as a module and calls its one public entry point, `generate_from_db`. The endpoint writes to a temporary file and streams the PDF straight back to the browser to display inline:

```
elif path == "/api/id_cards.pdf":
    mid = qs.get("id",[""])[0] or None
    backs = qs.get("backs",["1"])[0] not in ("0","false","no")
    import tempfile
    try:
        import gen_id_cards as _gen
    except Exception as e:
        return self.send_json({"error":f"card module unavailable: {e}"},500)
    out = os.path.join(tempfile.gettempdir(), "fc_member_id_cards.pdf")
    try:
        _gen.generate_from_db(out_path=out, only_id=mid, backs=backs)
```

On the browser side the call is a single line — the button either prints the whole roster or one member's card, depending on whether an `id` is passed:

```
// Open the printable ID-card PDF. No id → all eligible members; id → one card.
function printIdCards(id) {
  const url = `${API}/api/id_cards.pdf` + (id ? `?id=${encodeURIComponent(id)}` : '');
  window.open(url, '_blank');
}
```

`generate_from_db` is the seam between the web layer and the drawing code: it opens the database, loads the config and the eligible members, and refuses cleanly if there is nothing to print by raising `ValueError("No eligible members to print.")`, which the endpoint turns into a 404 rather than a crash. The same function backs the command-line interface (`--demo`, `--id`, `--out`) so the script is testable on a laptop with no database at all.


## Why It Matters / Design Takeaways

- *Agency-neutral by construction.* `gen_id_cards.py` reads every branding value, including field labels, from `station_config`. The same code prints correct cards for any organization; `gen_operator_cards.py` is the older, hardcoded predecessor to migrate away from.
- *Offline is non-negotiable.* The QR is drawn locally with `QrCodeWidget` after the online Google chart service died. Both the card (`_qr_drawing`) and the on-screen `/api/qr` endpoint share the same offline approach.
- *One shared key.* The QR encodes `barcode_id` (with sensible fallbacks), the exact value the Scan Check-In page matches — which is what makes scan-to-check-in work.
- *Robust drawing.* Font auto-fit, initials when no photo, JPEG-without-PIL embedding, and try/except around the QR mean one bad record never ruins a whole printed sheet.
- *Thin web seam.* The server imports the script and calls `generate_from_db`; the front end is a one-line `window.open`. The drawing logic stays entirely in the script.

> **MAINTAINER'S RULE** — Treat `gen_id_cards.py` as the living card generator and `gen_operator_cards.py` as legacy. Never hardcode a name, callsign, logo, or label into a card — add it to `station_config` and read it through `cfg.get(...)` with a fallback. Never reintroduce a network call into QR or card generation; the whole reason `_qr_drawing` exists is that an online QR broke in the field. And keep `barcode_id` as the single shared check-in key across the card, the QR, and the Scan Check-In page — if you change how it is chosen, change it in all three.


# 17. PDF Generation — iap_pdf.py & ics_pdf_downloader.py

*When an incident is over — or a printout is needed mid-operation — FieldCommand turns saved form data into paper. iap_pdf.py builds the complete Incident Action Plan (IAP) as one merged, cover-paged Portable Document Format (PDF) file, rendering each Incident Command System (ICS) form from the database with ReportLab and stitching them together with pypdf. Its companion, ics_pdf_downloader.py, fetches the blank official Federal Emergency Management Agency (FEMA) forms once, so they are available offline for hand-filling.*

> **IN ONE SENTENCE** — `iap_pdf.py` renders each completed ICS form from its saved data into a PDF page, merges them in standard IAP order behind a cover page, and hands back the bytes for the browser to download; `ics_pdf_downloader.py` separately pulls the blank official FEMA form PDFs down once for offline use.


## What This Is / What It Is For

An **Incident Action Plan (IAP)** is the packet an incident produces for each operational period: the objectives, the org chart, the assignments, the communications plan, the medical plan, and so on. In FieldCommand those forms are filled in on screen and saved as data in the database. But an IAP has to become **paper** — briefed at a meeting, posted on a wall, handed to a section chief. [python/iap_pdf.py](python/iap_pdf.py) is the compiler that turns the saved data back into a single, professional, print-ready PDF.

It is important to see that this is a **build**, not a copy. The script does not store finished PDFs; it re-renders them from the current data every time, so the printout always reflects the latest edits. Its sibling, [python/ics_pdf_downloader.py](python/ics_pdf_downloader.py), does the opposite job — it **fetches** the blank, official FEMA form PDFs from the FEMA website once and caches them locally, so that if someone would rather hand-fill an official form, it is already on the appliance and needs no internet at print time. One script writes PDFs from data; the other downloads PDFs to disk. They are easy to confuse by name, so keep the distinction in mind.

> **JARGON, IN PLAIN WORDS** — **ReportLab** draws PDF pages from scratch. **Platypus** is ReportLab's higher-level layout engine — you hand it a list of 'flowables' (paragraphs, tables, spacers) called a **story**, and it flows them down the page and across page breaks for you. **pypdf** is a separate library that reads finished PDFs and merges them into one. An **operational period** is the block of time an IAP covers (often 12 or 24 hours).


## How It Works — Rendering One Form

Most of `iap_pdf.py` is a set of `render_icsNNN` functions, one per form the project templates. Each takes the form's saved data dictionary `d`, the incident name, and the period; each returns an in-memory PDF for that one form as a `BytesIO` buffer. `render_ics202` (Incident Objectives) is representative — it builds a Platypus **story** section by section and calls `doc.build(story)`:

```
def render_ics202(d, incident_name, period):
    """ICS-202 Incident Objectives."""
    buf = io.BytesIO()
    doc = make_doc(buf, 'ICS-202', 'Incident Objectives', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident / Date / Time'))
    story.append(_field_table([
        ('Incident Name',   d.get('incident_name', incident_name)),
        ('Op Period #',     d.get('operational_period_number', str(period))),
        ('From',            d.get('operational_period_from','')),
        ('To',              d.get('operational_period_to','')),
        ('Date Prepared',   d.get('date_prepared','')),
    ]))
```

Every renderer reads its values with `d.get('key', '')`, so a form that was only partly filled in still produces a clean page — missing fields simply come out blank rather than throwing. That single habit is what lets the compiler run against real, half-complete incident data without special-casing anything.

Forms with repeating rows — a communications plan's channels, an assignment list's resources, a medical plan's aid stations — loop over numbered keys and stop when they run out of data. `render_ics205` (Radio Communications Plan) shows the pattern: it walks up to twenty possible channels and breaks at the first empty name, so the table is exactly as long as the data:

```
for i in range(20):
    name = d.get(f'ch205_name_{i}','')
    if not name: break
    ch_rows.append([
        str(i+1),
        d.get(f'ch205_function_{i}',''),
        name,
        d.get(f'ch205_rx_{i}',''),
        d.get(f'ch205_rx_tone_{i}',''),
        # ... one column per channel field
    ])
```

Not every ICS form has a hand-written renderer. Forms without a specific template fall through to `render_generic`, which turns whatever keys the data has into a two-column label/value table, skipping internal bookkeeping keys — so a newly added form still prints something useful before anyone writes a bespoke layout for it:

```
skip_keys = {'incident_id','form_type','period','summary','created','updated','id'}
pairs = [(k.replace('_',' ').title(), str(v))
         for k, v in sorted(d.items())
         if k not in skip_keys and v and str(v).strip()]
```


## How It Works — Shared Chrome, Styles, and Tables

The reason every page looks like one document — same navy header, same gold form-number badge, same footer with the generation timestamp — is that all renderers get their page through one factory, `make_doc`. It builds a `SimpleDocTemplate` and binds a header/footer function that ReportLab calls on every page, so the ICS chrome is drawn identically everywhere:

```
def make_doc(buf, form_num, form_title, incident_name, op_period):
    """Return a SimpleDocTemplate with header/footer already bound."""
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.5*inch,  rightMargin=0.5*inch,
        topMargin=0.8*inch,   bottomMargin=0.55*inch,
        title=f'{form_num} — {incident_name}',
        author='FieldCommand IMS',
    )
```

> **A SMALL BUT DELIBERATE TRICK** — `make_doc` stashes `incident_name` and `op_period` on the `doc` object and rebinds `doc.build` so the header/footer callback (`_onPage`) is passed to ReportLab as both `onFirstPage` and `onLaterPages`. That is how each rendered form 'remembers' which incident and period to stamp in its header without every renderer having to wire it up. If you write a new renderer, do **not** re-implement the header — just call `make_doc` and it comes for free.

Two more shared helpers keep the look consistent. `_styles()` returns the one paragraph-style palette (heading, body, small, bold, label) every renderer uses, and `_field_table(pairs)` renders a list of label/value pairs as the standard striped two-column table — the workhorse that most form sections are built from:

```
def _field_table(pairs, col_widths=None):
    """Render a list of (label, value) pairs as a 2-col table."""
    styles = _styles()
    rows = []
    for label, value in pairs:
        rows.append([
            Paragraph(label, styles['label']),
            Paragraph(str(value or '—'), styles['body']),
        ])
```

Because `_field_table` substitutes an em-dash for any empty value, blank fields read as intentionally-empty rather than as a layout bug — a small touch that makes a partly-filled form look finished.


## How It Works — Ordering, the Cover Page, and Merging

The IAP has a conventional form order, and `iap_pdf.py` encodes it once as `IAP_FORM_ORDER`, with a `RENDERERS` table mapping the form types that have bespoke layouts to their functions. Keeping the order and the renderer map as plain data at the bottom of the file means adding a form is a one-line change in two lists, not a rewrite:

```
IAP_FORM_ORDER = [
    ('ics202', 'ICS-202 Incident Objectives'),
    ('ics203', 'ICS-203 Organization Assignment List'),
    ('ics204', 'ICS-204 Assignment Lists'),
    ('ics205', 'ICS-205 Radio Communications Plan'),
    # ... through ICS-230
]

RENDERERS = {
    'ics202': render_ics202,
    'ics203': render_ics203,
    'ics204': render_ics204,
    'ics205': render_ics205,
    'ics206': render_ics206,
}
```

`compile_iap` is the entry point that ties it together. It first checks that pypdf is available (merging is impossible without it), starts a `PdfWriter`, optionally appends a rendered cover page, then walks `IAP_FORM_ORDER` and appends each rendered form in turn. Crucially, each form is rendered inside its own `try/except`: the comment says exactly why — one bad form must not sink the whole plan:

```
for fdata in form_list:
    try:
        if renderer:
            buf = renderer(fdata, incident_name, period)
        else:
            buf = render_generic(fdata, form_type,
                                 form_title, incident_name, period)
        writer.append(PdfReader(buf))
    except Exception as e:
        # Log and continue — don't let one bad form break the whole IAP
        import traceback
        traceback.print_exc()
```

> **WHY THIS except IS THE RIGHT CALL** — FieldCommand's rules forbid silently swallowing exceptions in general. This is a considered exception: an IAP is often compiled minutes before a briefing, from data many people touched. A single malformed form should degrade to 'that one page is missing' — logged to the console via `traceback.print_exc()` — not to 'the whole plan failed to print.' The error is printed, not hidden. Keep that behavior; do not let it become a hard failure that blocks the other forms.

After the ordered forms, `compile_iap` also sweeps up any requested form types that were **not** in `IAP_FORM_ORDER`, rendering them generically so nothing the caller asked for is silently dropped. Finally it writes the merged `PdfWriter` into one `BytesIO` and returns the raw bytes — it never touches disk, which suits streaming the result straight to a browser.


## How It Works — The Web Endpoint and the Download

The Incident Command System platform server exposes this at `POST /api/ics/iap_compile`. The endpoint's job is to gather the data and call `compile_iap`; it does not know anything about ReportLab. It looks up the incident name, selects the saved forms for the incident and period (all of them, or only the requested types), and groups them into the `forms_by_type` dictionary the compiler expects:

```
forms_by_type = {}
for r in rows:
    ft = r.get("form_type","")
    try:    fdata = json.loads(r.get("data","{}"))
    except: fdata = {}
    fdata["_form_id"]    = r.get("id","")
    fdata["_form_type"]  = ft
    fdata["_updated"]    = r.get("updated","")
    forms_by_type.setdefault(ft, []).append(fdata)
```

Each form's `data` column is stored as a JSON string in the database, so it is parsed back into a dictionary here — this is the same data blob pattern used across FieldCommand's forms. The endpoint then calls the compiler and, on success, streams the bytes back with the headers that make a browser download (rather than display) the file under a clean, incident-named filename:

```
pdf_bytes = compile_iap(
    forms_by_type,
    incident_name = incident_name,
    period        = period,
    prepared_by   = body.get("prepared_by",""),
    date_str      = body.get("date_str", now[:10]),
    include_title = include_title,
)

safe_name = "".join(c2 if c2.isalnum() else "_" for c2 in incident_name)[:30]
filename  = f"IAP_{safe_name}_P{period}_{now[:10]}.pdf"
self.send_response(200)
self.send_header("Content-Type",        "application/pdf")
self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
```

On the browser side, `iap_compile.html` POSTs the operator's choices — which form types, whether to include the cover page, who prepared it — reads the returned blob, and clicks a temporary link to save it. The filename is taken from the `Content-Disposition` header the server set, so the download is named after the incident:

```
const r = await fetch(`${ICS_API}/api/ics/iap_compile`, {
  method:  'POST',
  headers: {'Content-Type':'application/json'},
  body: JSON.stringify({
    incident_id:   incId,
    period:        parseInt(period) || 1,
    form_types:    [...selectedTypes],
    include_title: title,
    prepared_by:   prepBy,
  })
});
```

If anything fails, the server returns a JSON error with a status code — 503 when the PDF compiler is not installed, 404 when no forms exist for that incident and period, 500 on an unexpected error — and the page shows the message and points the operator at the 'Save as HTML' fallback, so a missing library never leaves someone with no way to get paper.


## How It Works — Fetching the Blank Official Forms

`ics_pdf_downloader.py` is the other half of 'print center.' It downloads the blank, official FEMA ICS forms once and stores them under `/opt/fieldcommand/data/ics_forms/` for offline use. The catalogue is a plain list of `(form_id, filename, description, local_name)` tuples, and `try_download` fetches the primary FEMA Uniform Resource Locator (URL), then an alternate filename form if the first fails:

```
def try_download(form_id, filename, local_name, output_dir, force=False):
    dest = output_dir / local_name
    if dest.exists() and not force:
        return True, f'Already exists ({dest.stat().st_size:,} bytes)'
    primary_url = FEMA_BASE + filename
    ok, msg = download_file(primary_url, dest)
    if ok:
        return True, f'Downloaded from FEMA: {msg}'
```

Two details make this a good field citizen. `download_file` verifies it actually received a PDF — it checks the content type and, if unsure, reads the first bytes to confirm they start with the `%PDF` signature — so a captive-portal login page or an error page never gets saved as if it were a form. And the download loop sleeps half a second between forms with the comment `# Be polite to FEMA servers`, and records what it fetched in a manifest so `--status` can report which forms are already present. This script is run at setup time (or on demand), not during an activation, because it is the one part of the print system that needs the internet.

> **TWO KINDS OF 'PDF' IN THE PRINT CENTER** — It is worth stating plainly for anyone maintaining this: `iap_pdf.py` **generates** filled PDFs from your incident's own data and needs no internet; `ics_pdf_downloader.py` **downloads** blank official forms from FEMA and needs internet once. The first is the everyday path during an activation; the second is a one-time offline-prep convenience.


## Why It Matters / Design Takeaways

- *Build, don't store.* `iap_pdf.py` re-renders every form from current data on each compile, so the printout always matches the latest edits — there are no stale saved PDFs to go out of date.
- *One look, one place.* `make_doc`, `_styles`, and `_field_table` mean every form shares the same chrome and table style; a new renderer inherits the whole look by calling the factory.
- *Data-driven order.* `IAP_FORM_ORDER` and `RENDERERS` keep the form sequence and the renderer map as editable lists; adding a form is a small, local change.
- *Fault-tolerant by design.* Per-form try/except (logged, not hidden) means one malformed form costs one page, never the whole plan — the right trade-off minutes before a briefing.
- *Thin, honest web seam.* The endpoint only gathers data and streams bytes; the front end reads the blob and saves it; errors return clear status codes with a documented fallback.
- *Fetch vs. generate are separate on purpose.* `ics_pdf_downloader.py` is the internet-once step for blank official forms; it validates that it really got a PDF and is polite to FEMA's servers.

> **MAINTAINER'S RULE** — To add or change an IAP form, work only through the seams the file already provides: write a `render_icsNNN(d, incident_name, period)` that reads every value with `d.get(...)`, builds its story from `_section`/`_field_table`, and gets its page from `make_doc`; then register it in `IAP_FORM_ORDER` and `RENDERERS`. Never render a header by hand and never remove the per-form try/except in `compile_iap` — a bad form must degrade to a missing page, not a failed plan. And keep `iap_pdf.py` (generate from data, offline) firmly separate from `ics_pdf_downloader.py` (fetch blank forms, internet once); they are two different jobs that happen to both make PDFs.


# 18. Reference Data and Theming — RepeaterBook, NIMS, and the Theme

*Four support files that never handle a live incident but decide what the app knows and how it looks: fetch_repeaters.py pulls repeater data in from RepeaterBook, nims_resource_types.py and nims_definitions.py carry the offline National Incident Management System (NIMS) resource-typing library that db.py seeds into the database, and apply_theme.py keeps every page on one dark color scheme.*

> **IN ONE SENTENCE** — These four files are FieldCommand's *reference layer*: `fetch_repeaters.py` imports repeater data, `nims_resource_types.py` + `nims_definitions.py` supply the offline NIMS resource-typing library that `db.py` seeds once, and `apply_theme.py` makes every Hyper Text Markup Language (HTML) page share one color theme.


## What This Is / What It Is For

Most of FieldCommand is about the live incident — nets, check-ins, forms, resources. This chapter is about the *reference data* that sits underneath all of that: the facts the app needs to know before anyone starts an incident, and the look it wears while doing it. None of these four files touches a running net. They populate lookup tables and enforce a visual standard, then get out of the way.

Three of them feed the database. `fetch_repeaters.py` downloads amateur radio repeater listings from RepeaterBook and writes them into the `repeaters` table. `nims_resource_types.py` and `nims_definitions.py` are a matched pair of plain Python data files that together form the National Incident Management System (NIMS) resource-typing library — the standard catalog of typed emergency resources (a Type I engine, a Type II hand crew, a heavy Urban Search and Rescue task force) — which `db.py` seeds into the `resource_types` table on a fresh install. The fourth, `apply_theme.py`, feeds the web front end instead of the database: it scans the HTML pages and makes sure every one of them defines the same set of Cascading Style Sheets (CSS) color variables, so the whole application looks like one product.

> **JARGON, IN PLAIN WORDS** — *Reference data* is background information the app looks things up in, as opposed to data the app creates during an incident. *RepeaterBook* is a public online directory of amateur radio repeaters. *NIMS resource typing* is a federal standard that describes emergency resources by kind and capability so that a 'Type II ambulance' means the same thing everywhere. *Seeding* is loading starter rows into a table the first time the database is created.


## fetch_repeaters.py — Bringing Repeater Data In

A repeater extends the range of a handheld or mobile radio, so knowing which repeaters cover the incident area — and their frequencies, tones, and whether they serve emergency groups — is genuinely useful field information. `fetch_repeaters.py` is a standalone command-line script (run by hand or from the maintenance menu) that pulls that data from RepeaterBook's export Application Programming Interface (API) and lands it in the database the web interface reads.

The whole job is three steps: *fetch*, *normalize*, *write*. Fetching is one Hyper Text Transfer Protocol (HTTP) request per state-and-band combination. The important detail is that RepeaterBook changed its rules in 2026 and now requires an approved token; the script sends it as a request header and warns loudly if it is missing:

```
def fetch_repeaters(state, band_code, token):
    """Fetch repeaters for a given state and band from RepeaterBook."""
    params = {
        "state_id": state,
        "band": band_code,
        "status_id": "1",  # On-air only
        "type": "json",
    }
    url = REPEATERBOOK_URL + "?" + urllib.parse.urlencode(params)
    headers = {
        "User-Agent": "FieldCommand-IMS/1.0 EmComm (https://github.com/KE4CON/FieldCommand-IMS)",
        "Accept": "application/json",
    }
    # New (2026+) token authentication. Without this, expect HTTP 403.
    if token:
        headers["X-RB-App-Token"] = token
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read())
    return data.get("results", [])
```

The token is resolved from three places in priority order — the `--token` flag, then the `REPEATERBOOK_TOKEN` environment variable, then a token file on disk — by `get_token()`. That layering is deliberate: an operator can paste a token once into `/opt/fieldcommand/data/repeaterbook_token.txt` and never think about it again, while a developer can override it for a one-off run. If none is found, the script prints a full explanation (apply for a token, or use the offline Comma-Separated Values export instead) and continues anyway so the failure is visible rather than silent.

*Normalizing* is the step that protects the rest of the app from RepeaterBook's field names. The API returns keys like `Callsign`, `Input Freq`, and `Operational Status`; the database uses lowercase columns like `callsign`, `input_freq`, and `status`. `normalize_repeater()` is the single translation layer, and it also does small cleanups — defaulting a blank digital mode to plain `FM`, and turning yes/no fields into 1/0 integers:

```
def normalize_repeater(r):
    """Normalize a RepeaterBook result into the FieldCommand 'repeaters' table schema."""
    def yn(v): return 1 if str(v).strip().lower() in ("yes", "1", "true") else 0
    digital = r.get("Digital", "") or ""
    mode = digital if digital and digital.lower() not in ("", "no", "none") else "FM"
    return {
        "callsign":    r.get("Callsign", ""),
        "output_freq": str(r.get("Frequency", "") or ""),
        "tone":        r.get("PL", "") or "",
        "ares":        yn(r.get("ARES", "")),
        "races":       yn(r.get("RACES", "")),
        "skywarn":     yn(r.get("SKYWARN", "")),
        "source":      "RepeaterBook",
        # ... more fields ...
    }
```

Notice the last field: every normalized row is stamped `"source": "RepeaterBook"`. That stamp is what makes the *write* step safe. `write_to_db()` does not empty the table — it deletes only the rows this script owns, then re-inserts the fresh download, so any repeaters an operator typed in by hand are never touched:

```
def write_to_db(repeaters, db_path):
    """Replace the repeaters table contents with the freshly fetched data."""
    conn = sqlite3.connect(str(db_path))
    now = datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z"
    try:
        # Clear only RepeaterBook-sourced rows so any manual entries survive.
        conn.execute("DELETE FROM repeaters WHERE source = 'RepeaterBook'")
        placeholders = ",".join("?" * len(REP_COLS))
        sql = f"INSERT INTO repeaters ({','.join(REP_COLS)}) VALUES ({placeholders})"
        for rep in repeaters:
            row = [rep.get(c, "") for c in REP_COLS[:-1]] + [now]
            conn.execute(sql, row)
        conn.commit()
```

Two more touches make it field-friendly: results are de-duplicated on `(callsign, output frequency)` because RepeaterBook no longer returns a stable identifier, and there is a polite `time.sleep(args.rate_limit)` (default three seconds) between calls so the download never hammers RepeaterBook's server. A 403 with no data at all exits with a clear message pointing at the token.

> **WHY THE source COLUMN MATTERS** — The `source` column is not decoration — it is the boundary between machine-owned and human-owned rows. `write_to_db` only ever deletes `WHERE source = 'RepeaterBook'`. If you add another importer, give it its own `source` value and delete only that value; never `DELETE FROM repeaters` with no `WHERE`, or you will erase an operator's hand-entered repeaters on the next refresh.


## The NIMS Library — Two Files, One Table

The NIMS resource-typing library is split across two files on purpose, because it answers two different questions. `nims_resource_types.py` answers *what exists and by what numbers*: it is one long Python list where every entry is a fixed nine-field tuple. The file's own docstring documents the shape, which is the contract every row must honor:

```
Format: (nims_id, kind, type_level, category, mission_area,
         description, min_personnel, capabilities, metric_notes)

NIMS_RESOURCE_TYPES = [
    ('1-508-1001','Engine','Type I','Fire','Fire/Hazardous Materials',
     'Engine – Type I (Structure)',4,
     'Structure fire suppression; 1000 GPM pump; 400 gal tank; hose, SCBA, tools',
     '1000 GPM pump, 400 gal tank, 1200 ft 2.5" hose, 4 personnel'),
```

`nims_definitions.py` answers *what it means in plain language*: it is a dictionary keyed by the same `nims_id`, where each value carries four explanatory paragraphs — `what_it_is`, `minimum_standards`, `ordering_guidance`, and `common_confusion`. This is the part that makes the library genuinely useful to a volunteer who is not a career fire officer; it explains, for example, that a Type VI 'engine' is really a small patrol unit whose 150 gallons 'runs out in 5 minutes at full flow':

```
NIMS_DEFINITIONS = {
'1-508-1001': {
    'what_it_is': (
        "A Type I engine is a full-size structural fire suppression apparatus — what most "
        "people think of as a 'fire truck.' ..."
    ),
    'minimum_standards': (
        "1,000 GPM or greater pump capacity. 400-gallon minimum water tank. ..."
    ),
    'ordering_guidance': ( "Order Type I when you need maximum water flow ..." ),
    'common_confusion': ( "Confusion: People sometimes call any fire truck a 'Type I.' ..." ),
},
```

Keeping the two apart means the terse catalog stays easy to scan and extend, while the prose lives in its own file where it can grow long without cluttering the numbers. The `nims_id` (the Federal Emergency Management Agency's Resource Typing Library Tool identifier, for example `1-508-1001`) is the shared key that joins them. Both files are pure data with a tiny `*main*` block that just prints a count — they do no input/output of their own, which is exactly why they are safe to `import`.

> **JARGON, IN PLAIN WORDS** — A *tuple* is a fixed-length, fixed-order group of values in Python; because the order is fixed, position 0 is always the `nims_id`, position 3 is always the `category`, and so on. A *dictionary* is a set of named lookups; here the name (the `nims_id`) points at the four definition paragraphs. Splitting the data this way lets one file stay a compact table and the other hold the long explanations.

The join happens in `db.py`, inside the check-first seeder `seed_resource_types()`. It runs on every boot but does its work only when the table is empty, then loops the list, looks up the matching definition by `nims_id`, and inserts them together in one row. The `(*rt, ...)` unpacks the nine-field tuple straight into the first nine columns, and the four definition strings follow:

```
def seed_resource_types(conn):
    try:
        existing = conn.execute("SELECT COUNT(*) FROM resource_types").fetchone()[0]
        if existing == 0:
            from nims_resource_types import NIMS_RESOURCE_TYPES
            from nims_definitions import NIMS_DEFINITIONS
            for rt in NIMS_RESOURCE_TYPES:
                nims_id = rt[0]
                defn = NIMS_DEFINITIONS.get(nims_id, {})
                conn.execute("""INSERT INTO resource_types
                    (nims_id,kind,type_level,category,mission_area,description,
                     min_personnel,capabilities,metric_notes,
                     definition_what,definition_std,definition_order,definition_conf,
                     custom)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,0)""",
                    (*rt,
                     defn.get('what_it_is',''),
                     defn.get('minimum_standards',''),
                     defn.get('ordering_guidance',''),
                     defn.get('common_confusion','')))
            conn.commit()
```

Two design choices are worth naming. First, `NIMS_DEFINITIONS.get(nims_id, {})` means a resource type with no written definition still seeds cleanly — the four definition columns just come out as empty strings — so the catalog and the prose do not have to stay in perfect lockstep. Second, every seeded row is inserted with `custom=0`, marking it as a NIMS standard the app ships. Rows an agency adds later carry `custom=1`, so the interface can tell 'this is the federal standard' from 'this is ours' — the same owned-versus-added distinction the `source` column draws for repeaters. The whole seed is wrapped in `try/except` that only logs, so a seeding hiccup can never stop the database from initializing.


## apply_theme.py — One Look, Enforced

FieldCommand's web front end is many separate HTML files, each with its own inline `<style>`. Left alone, they would drift — one page a slightly different blue, another missing the alert amber. `apply_theme.py` prevents that drift. It is not a stylesheet; it is a *consistency tool* that treats one canonical block of CSS variables as the single source of truth and makes every page conform. The canonical block and the list of variables every page must define are both constants at the top of the file:

```
THEME_VARS = """:root {
  --bg:#0d1117;      /* page background */
  --panel:#161b22;   /* card / panel background */
  --txt:#c9d1d9;     /* primary text */
  --eoc:#1a3a6b;     /* EOC blue — primary brand */
  --amber:#e3b341;   /* amber — warnings / alerts */
  --green:#3fb950;   /* green — success / online */
  --red:#f85149;     /* red — error / danger */
  --font-hd:'Courier New',monospace;
}"""

REQUIRED_VARS = [
    '--bg', '--panel', '--panel2', '--txt', '--muted', '--line',
    '--eoc', '--eoc-lt', '--amber', '--green', '--red', '--blue',
    '--purple', '--font-hd',
]
```

The tool works in two directions. To check, it parses each page's `:root` blocks with a regular expression, collects the variable names actually defined, and reports any of the `REQUIRED_VARS` that are missing. To fix, `apply_theme()` either replaces an existing `:root` block with the canonical one or, if the page has none, inserts it inside the first `<style>` tag (or ahead of `</head>` as a fallback). The logic is small and readable on purpose:

```
def apply_theme(html: str) -> str:
    """Apply canonical theme to HTML string. Returns modified string."""
    if has_root_block(html):
        return replace_root_block(html)
    return insert_root_block(html)
```

The command-line interface exposes four safe modes — `--check` (report only), `--missing` (list offenders), `--diff` (show the change without writing), and `--apply` (write, with a `--dry-run` option). `--check` even sets the process exit code to non-zero when anything is wrong, which is why it can be dropped into automation. Individual pages still link a shared `theme.css` for the rest of their styling; `apply_theme.py`'s job is narrowly the color-and-font variable contract that every page must satisfy so the buttons, banners, and status colors mean the same thing everywhere. Because those color names carry meaning — green is online, red is danger, amber is a warning — keeping them identical across pages is a correctness concern, not just an aesthetic one.

> **WHERE THE VERDICT COLORS COME FROM** — The Preflight page's GO / CAUTION / NO-GO banner is a live example of the theme in action: its green, amber, and red are `var(--green)`, `var(--amber)`, and `var(--red)` from this exact variable set. Change a value in `THEME_VARS` and re-apply, and every status color across the app moves together.


## Why It Matters / Design Takeaways

- *Reference data is separated from live data.* Repeaters, NIMS types, and the theme are loaded before any incident and never entangled with net or form logic — so they can be refreshed, reseeded, or restyled without risk to incident records.
- *Owned rows are protected by a marker.* The `source` column for repeaters and the `custom` flag for resource types both draw the same line: machine-imported/standard rows can be replaced freely, hand-entered rows never are.
- *Data files stay dumb; loaders stay smart.* `nims_resource_types.py` and `nims_definitions.py` are pure Python data with no input/output, joined by `db.py`'s seeder on a shared key — easy to read, easy to extend, safe to import.
- *Consistency is enforced by a tool, not by discipline.* `apply_theme.py` makes 'every page uses the same colors' a checkable, fixable fact instead of a hope, and its `--check` exit code lets automation guard it.

> **MAINTAINER'S RULE** — Add reference data through its established door and keep the markers intact. New repeater importers get their own `source` value and delete only that value. New NIMS types get a nine-field tuple in `nims_resource_types.py` (and, ideally, a matching `nims_id` entry in `nims_definitions.py`), and seed with `custom=0`; the seeder tolerates a missing definition, so never break the tuple's field order to force one in. New theme colors get added to both `THEME_VARS` and `REQUIRED_VARS` in `apply_theme.py`, then rolled out with `--apply` — never hand-edit one page's `:root` and leave the rest behind.


# 19. The Install and Boot Chain — how a Pi becomes a FieldCommand server

*Two scripts turn a freshly-flashed Raspberry Pi into a running FieldCommand server. Phase 1, fieldcommand-setup.sh, builds a boot-from-RAID-1 mirror across two SSDs and copies the operating system onto it. Phase 2, install.sh, runs once on the first boot from that mirror and stands up everything else — packages, code, the HTTPS certificate, nginx, the firewall, the background services, and the stable device names.*

> **IN ONE SENTENCE** — `fieldcommand-setup.sh` mirrors two SSDs and copies the operating system onto them, then a one-shot systemd service on the first boot runs `install.sh`, which installs the packages, deploys the code, makes the HTTPS certificate, configures nginx and the firewall, and registers the background services and stable device names — so an operator runs one command and walks away.


## What This Is / What It Is For

A FieldCommand server does not arrive as a finished appliance. It starts life as a plain Raspberry Pi 5 with Raspberry Pi Operating System (OS) flashed to a microSD card. Turning that into a hardened, self-healing incident server — one that boots even if a disk dies, serves the dashboard over Hypertext Transfer Protocol Secure (HTTPS), and brings up a dozen background services on their own — is the job of the **install and boot chain**. It is two shell scripts that hand off to each other, plus a small set of systemd unit files and udev rules they lay down along the way.

The whole point is that a volunteer with no Linux background runs **one** command and answers a few questions once. Everything after that is hands-off: the Pi reboots itself as many times as it needs to, resumes where it left off, and finishes by presenting a working dashboard. This chapter follows that chain from the first command to the last service starting, and explains why each piece is where it is.

> **JARGON, IN PLAIN WORDS** — **RAID 1** (Redundant Array of Independent Disks, level 1) means two disks holding identical copies of the same data — a mirror — so the server keeps running if one disk fails. **systemd** is the program Linux uses to start and supervise background services and to run things at boot. **udev** is the part of Linux that reacts when hardware is plugged in — it can, for example, give a device a fixed name. **nginx** is the web server that faces the browser. **TLS** (Transport Layer Security) is the encryption behind the padlock in HTTPS.


## Why Two Phases — the 'Why' Behind the Split

The install is deliberately cut into two scripts because the two halves do fundamentally different kinds of work, and the machine is a different machine between them. **Phase 1** (`fieldcommand-setup.sh`) is disk surgery: it erases two Solid-State Drives (SSDs), builds a mirror across them, and copies the running OS onto that mirror. It has to run from the microSD card, because you cannot rebuild the disk you are booted from. **Phase 2** (`install.sh`) is ordinary software setup: install packages, copy code, write config. It has to run from the finished mirror, because that is where FieldCommand will actually live.

So the split is not stylistic — it follows the hardware. Phase 1 ends by rebooting the Pi off the SD card and onto the new SSD mirror; Phase 2 begins on that first boot. The scripts themselves say so up front. Phase 1's header lays out the entire arc:

```
#   From there it is hands-off. It will:
#     1. Make sure the Pi can see BOTH NVMe SSDs behind the Pironman PCIe switch
#     2. Build a true boot-from-RAID-1 mirror across the two SSDs and copy the
#        running OS onto it  (the corrected "Step 1B" from the Install Guide).
#     3. Reboot into the SSD mirror and, on that first boot, automatically run
#        the FieldCommand installer (install.sh) with your answers.
#     4. Finish and tell you to run the one test only you can do by hand:
#        the pull-a-drive failover test.
```

Notice step 3: Phase 1's real deliverable is not just a mirror — it is a mirror that will **run Phase 2 by itself**. The bridge between them is a config file plus a systemd service, and getting that handoff right is the heart of the chain.


## How It Works — Phase 1 Builds the Mirror

Phase 1 gathers the operator's answers once (callsign, coordinates, Wi-Fi name, server address, and so on), then partitions and mirrors the two drives. The mirror-building is mechanical and careful: identical partition tables on both SSDs, a RAID-1 array across the large partitions, an ext4 filesystem on the array, and then a full copy of the live OS onto it with `rsync`:

```
info "Creating the RAID 1 root array across ${A2} + ${B2}"
run bash -c "yes | mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 --metadata=1.2 '$A2' '$B2'"

info "Formatting: ext4 on the array, FAT32 on each boot partition"
run mkfs.ext4 -F -L fc-root /dev/md0

info "Mounting the array and copying the running OS onto it (this takes a while)"
run rsync -aHAXx --info=progress2 \
    --exclude='/mnt/*' --exclude='/media/*' --exclude='/lost+found' \
    / /mnt/root/
```

After the copy, Phase 1 points the copied OS at the array — it rewrites `cmdline.txt` to `root=/dev/md0`, writes an `/etc/fstab` for the array, records the array in `mdadm.conf` so it assembles at boot, and rebuilds the initial RAM filesystem inside the copy (via `chroot`) so the kernel can even find the mirror early in boot. All of that is so the Pi can boot from the mirror instead of the card. It then sets the Pi 5 bootloader to try the SSDs first but keep the SD card as a fallback, using a comment that documents the magic number so the next maintainer is not left guessing:

```
set_boot_order_nvme() {
    # BOOT_ORDER nibbles read right-to-left: 6=NVMe, 1=SD, 4=USB-MSD, f=retry.
    # 0xf416 = try NVMe, then SD, then USB, then loop — SD stays as a safety net.
```

> **WHY THE SD CARD STAYS BOOTABLE** — The boot order keeps the microSD card as a fallback on purpose. If a mirror build goes wrong or a drive later fails to assemble, pulling power and booting the card gets the operator back to a known-good starting point in the field, with no laptop and no re-imaging. A field appliance should never have a single click that bricks it.


## How It Works — the Handoff to Phase 2

Before it reboots, Phase 1 does three things that together arrange for Phase 2 to run itself. First, it stages a copy of the whole repository onto the array so the installer source travels with the OS. Second, it writes the operator's saved answers next to it as a config file. Third, it installs a **one-shot systemd service** into the array that will run the installer on the first boot:

```
info "Staging the FieldCommand installer on the array ($ARRAY_SRC)"
run mkdir -p "/mnt/root$ARRAY_SRC"
run rsync -a --exclude='.git' "$REPO_ROOT/" "/mnt/root$ARRAY_SRC/"
write_config_file "/mnt/root$ARRAY_SRC/fieldcommand.conf"
install_firstboot_service   # writes into /mnt/root
```

The service it writes is the single most important piece of the handoff, and it is worth reading in full because every line earns its place. It is a `oneshot` service that runs the installer with the saved answers, and it is engineered so it can **never** turn into a boot loop:

```
[Unit]
Description=FieldCommand first-boot installer (runs once from the SSD mirror)
After=network-online.target multi-user.target
Wants=network-online.target
ConditionPathExists=$ARRAY_SRC/scripts/install.sh
ConditionPathExists=!$ARRAY_SRC/.firstboot-done

[Service]
Type=oneshot
# Disable ourselves first so a failure can never boot-loop.
ExecStartPre=/bin/systemctl disable fc-firstboot.service
ExecStart=/usr/bin/env bash $ARRAY_SRC/scripts/install.sh --config $ARRAY_SRC/fieldcommand.conf
ExecStartPost=/usr/bin/touch $ARRAY_SRC/.firstboot-done
StandardOutput=journal+console
StandardError=journal+console
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

There are three independent safety belts here, and understanding them is understanding the whole design:

| Line | What it guarantees |
| --- | --- |
| `After=network-online.target` + `Wants=network-online.target` | The installer waits until the network is actually up, because it downloads packages, map tiles, and the Federal Communications Commission (FCC) database. Starting it earlier would fail on the very first thing it tries. |
| `ConditionPathExists=!$ARRAY_SRC/.firstboot-done` | The service skips itself entirely if the 'done' marker exists. Combined with the `ExecStartPost` that creates that marker on success, the installer runs at most once. |
| `ExecStartPre=/bin/systemctl disable fc-firstboot.service` | It removes its own boot hook *before* doing any work. So even if the installer crashes halfway, the next boot will not run it again — the belt-and-suspenders partner to the `.firstboot-done` marker. |
| `TimeoutStartSec=0` | No timeout. A full install (packages, a ~600 megabyte FCC database, gigabytes of offline content) can legitimately take an hour or more; systemd must not kill it partway. |

> **WHY THE INSTALLER DISABLES ITSELF FIRST** — `ExecStartPre` runs `systemctl disable` on the service *before* `ExecStart` runs the installer. This ordering is intentional and load-bearing: a first-boot installer that fails partway must not re-trigger on the next boot, or a single bad download could trap the Pi in an endless reboot-and-retry cycle in the field. If you ever edit this unit, keep the disable in `ExecStartPre` — never move it to `ExecStartPost`, where a crash would skip it.

One more detail shows how carefully the two phases are kept apart. Phase 1 can also be launched from a desktop auto-start icon; that launcher must **not** survive onto the mirror, or the migrated system would try to re-run Phase 1. So Phase 1 deletes it from the copy before unmounting:

```
# The migrated system boots from the mirror and finishes via the first-boot
# installer service — it must NOT also carry the desktop auto-start launcher,
# or the setup would try to re-run there. Remove it from the array copy.
run rm -f /mnt/root/etc/xdg/autostart/fieldcommand-setup.desktop
```


## How It Works — What install.sh Does, in Order

When the mirror boots for the first time, the `fc-firstboot` service launches `install.sh --config …`. Because a config file was passed, the installer runs fully unattended — the same `ask` helper that would prompt a human simply takes the saved default instead. From here the installer works top to bottom, and the order matters. It installs system packages, creates the `fieldcommand` service account, builds a Python virtual environment, copies the Python services and the web frontend into `/opt/fieldcommand`, and patches the operator's coordinates and callsign into the Hypertext Markup Language (HTML). Then it reaches the three steps that stand up the network face of the server, and their sequence is the part most worth understanding.


### 1. The firewall — the core APIs are never on the wire

The installer configures the Uncomplicated Firewall (ufw) to open only what belongs on the local network: Secure Shell (SSH) on 22, and the web ports 80 and 443. The four core Application Programming Interface (API) services are pointedly **left closed**, because they are only ever reached through nginx over HTTPS:

```
ufw allow 80/tcp    comment "nginx HTTP (redirects to HTTPS)" 2>>"$FC_LOG" || true
ufw allow 443/tcp   comment "nginx HTTPS" 2>>"$FC_LOG" || true
# Core API services (5050 FCC, 5051 Health, 5055 ICS, 5056 Refs) are bound to
# 127.0.0.1 and reached ONLY through nginx (/svc/<port>) over HTTPS. They are
# deliberately NOT opened on the LAN, so operator PII is never on the wire in
# cleartext. (Do not re-add ufw allow rules for 5050/5051/5055/5056.)
```

> **TWO LOCKS, NOT ONE** — The core services are protected two ways at once: each binds only to `127.0.0.1` (so the operating system will not carry its traffic off the box), and the firewall never opens its port anyway. Either alone would do the job; both together mean a single mistake — a service accidentally binding to all interfaces, or a stray `ufw allow` — cannot by itself expose operator Personally Identifiable Information (PII) in cleartext. Do not 'simplify' by removing one.


### 2. The TLS certificate — it must exist before nginx is tested

This is the ordering rule the chapter title hints at. nginx is configured to serve HTTPS, and its config points at `/etc/fieldcommand/tls/server.crt` and `server.key`. If those files are missing, `nginx -t` (the configuration test) fails and nginx will not start. So the installer generates the certificate **first**, by calling `fc-gen-cert.sh`, and only then configures and tests nginx. The installer's own comment states the requirement outright:

```
step "Generating TLS certificate (HTTPS)"
# nginx serves the dashboard over HTTPS. On this closed LAN (no public domain) we
# create our own certificate: a private local Certificate Authority by default
# (install its root on devices once for a warning-free padlock), or a single
# self-signed cert if TLS_SELF_SIGNED=1. Must exist before 'nginx -t' below.
command -v openssl >/dev/null 2>&1 || apt-get install -y openssl 2>>"$FC_LOG" || true
CERT_ARGS="--ip ${SERVER_IP:-192.168.50.1}"
[[ "${TLS_SELF_SIGNED:-0}" == "1" ]] && CERT_ARGS="$CERT_ARGS --self-signed"
if bash "$SCRIPT_DIR/fc-gen-cert.sh" $CERT_ARGS 2>>"$FC_LOG"; then
```

Because there is no public domain name on a closed emergency-communications network, no public Certificate Authority (CA) can issue a certificate. `fc-gen-cert.sh` solves that by being its own certificate authority. By default it creates a private local root CA and signs a server certificate with it; operators install the root once on their devices for a clean padlock. The key trick that makes the certificate valid for `https://192.168.50.1` is putting the server's Internet Protocol (IP) address into the certificate's Subject Alternative Name (SAN):

```
SAN="subjectAltName=IP:${IP},IP:127.0.0.1,DNS:${HOST},DNS:localhost"

echo "==> Generating the server certificate signed by the local CA…"
openssl req -newkey rsa:2048 -nodes \
    -keyout "$SRV_KEY" -out "$TLS_DIR/server.csr" \
    -subj "/O=FieldCommand IMS/CN=${HOST}"
```

The generator is also idempotent and long-lived: it refuses to overwrite an existing certificate unless `--force` is passed (regenerating would invalidate the trust operators already installed), and it uses `DAYS=3650` — about ten years — so a field unit never silently expires between deployments. Both choices come straight from the file:

```
DAYS=3650   # ~10 years, so field units never silently expire

if [[ -f "$SRV_CRT" && -f "$SRV_KEY" && "$FORCE" != "1" ]]; then
    echo "Certificate already present at $SRV_CRT — leaving it in place."
    echo "(Use --force to regenerate; this invalidates any already-installed trust.)"
    exit 0
fi
```


### 3. nginx — one front door, many services behind it

With the certificate in place, the installer drops in the nginx site file, tests it, and restarts nginx. The test can only pass because the certificate already exists:

```
cp "$SCRIPT_DIR/../udev/nginx-fieldcommand.conf" /etc/nginx/sites-available/fieldcommand
ln -sf /etc/nginx/sites-available/fieldcommand /etc/nginx/sites-enabled/fieldcommand
rm -f /etc/nginx/sites-enabled/default
nginx -t 2>>"$FC_LOG" && success "nginx config valid" || warn "nginx config test failed — check manually"
```

The nginx config is what turns a scatter of localhost-only services into a single tidy HTTPS site. Port 80 does nothing but redirect to 443, and the core services are exposed same-origin under `/svc/<port>/` so the browser never has to talk to a raw port or hit a mixed-content wall. The trailing slash on `proxy_pass` quietly strips the prefix, so each backend sees exactly the path it expects:

```
location /svc/5055/ {   # ICS platform
    proxy_pass         http://127.0.0.1:5055/;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_read_timeout 30;
}
```

> **WHY NO HSTS HERE** — The nginx config deliberately omits the usual Strict-Transport-Security header. On a public site HSTS is good practice, but with a self-signed or local-CA certificate it would forbid the browser's one-time 'trust this certificate' click-through and lock operators out of their own appliance. The config carries a comment saying exactly this, so no one 'hardens' it back in by reflex.


## How It Works — systemd Runs the Services, udev Names the Devices

The last stretch of the installer registers the parts that make FieldCommand a real appliance rather than a set of scripts: background services that start at boot and restart on crash, and stable names for hardware that could otherwise land on a different device node each time it is plugged in. These are two different jobs, and Linux already has a purpose-built tool for each — systemd for services, udev for devices. FieldCommand uses both rather than reinventing either.

The service units are copied into `/etc/systemd/system/`, then enabled so they come up on every boot. Each Python service is a tiny, uniform unit — run as the unprivileged `fieldcommand` user, restart automatically, log to the journal:

```
[Unit]
Description=FieldCommand ICS Platform Server (Port 5055)
After=network.target

[Service]
Type=simple
User=fieldcommand
Group=fieldcommand
WorkingDirectory=/opt/fieldcommand
ExecStart=/opt/fieldcommand/venv/bin/python /opt/fieldcommand/python/ics_platform_server.py
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
SyslogIdentifier=ics-platform

[Install]
WantedBy=multi-user.target
```

`Restart=always` with `RestartSec=5` is the appliance behavior in one line: if a service dies at 3 a.m. in a shelter, systemd brings it back five seconds later with no human involved. Running as `User=fieldcommand` (a locked-down account created earlier in the installer, `useradd -r -s /bin/false`) means a compromised service cannot act as root. This same shape repeats across every service unit; the installer just enables them in a loop.

udev handles the other half. A Universal Serial Bus (USB) device does not have a guaranteed name — the same GPS receiver can appear as `/dev/ttyUSB0` today and `/dev/ttyUSB1` tomorrow depending on plug order. The services need a name they can rely on, so udev rules match a device by its vendor and product identifiers and create a fixed symbolic link. The Terminal Node Controller (TNC) rule is a good example, because it also has to distinguish two devices that share the same chip:

```
# Digirig Mobile v1.x uses Silicon Labs CP2102N (same VID:PID as some GPS units)
# Distinguish by USB product string "Digirig Mobile"
SUBSYSTEM=="tty", \
    ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", \
    ATTRS{product}=="Digirig Mobile", \
    SYMLINK+="tnc0 digirig", \
    MODE="0666", \
    TAG+="systemd"
```

That `SYMLINK+="tnc0"` is why the rest of the system can simply open `/dev/tnc0` and never care which physical port the radio interface is on. The GPS rules do the same for `/dev/gps0` — and, tellingly, the GPS rule for the exact same `10c4:ea60` chip carries the mirror-image test, `ATTRS{product}!="Digirig Mobile"`, so a Digirig is claimed as a TNC and a look-alike GPS as a GPS. The two rule files were written to agree with each other on purpose.

The third udev rule is not about a serial name at all — it is an **event trigger**. When a USB drive labeled `FIELDCOMMAND` is inserted, udev starts a systemd backup service, passing the kernel device name through the `%k` template:

```
ACTION=="add", SUBSYSTEM=="block", ENV{ID_FS_LABEL}=="FIELDCOMMAND", \
    RUN+="/bin/systemctl start fieldcommand-backup@%k.service"
```

This is the cleanest illustration of why FieldCommand leans on both tools together instead of one. udev is good at noticing hardware events but must hand off quickly; systemd is good at running a real job with logging and its own lifecycle. So udev only *fires the trigger*, and the templated `fieldcommand-backup@.service` does the actual `rsync` and SQLite backup. Plugging in a labeled thumb drive backs up the whole incident, with no operator action at all — the ultimate lazy-operator feature.


## Why It Matters / Design Takeaways

- *The split follows the hardware.* Phase 1 must run from the SD card because it rebuilds the disks; Phase 2 must run from the finished mirror because that is where FieldCommand lives. The two-script design is not a style choice — it is the only order the machine allows.
- *The handoff is a one-shot service, hardened against loops.* Phase 1's real product is a mirror that finishes installing itself. The `fc-firstboot` unit disables itself before it works, marks itself done after, and has no timeout — three independent guards so a bad first boot can never trap a Pi in the field.
- *Order is correctness, not preference.* The certificate is generated before nginx is tested because `nginx -t` fails without it. Read that ordering as a dependency, not a sequence you can shuffle.
- *Defense in depth on the wire.* The core APIs bind to localhost *and* the firewall never opens them; either alone would suffice, so one slip cannot expose operator data.
- *Use the tools Linux already has.* systemd supervises and restarts the services; udev gives hardware stable names and fires the backup trigger. FieldCommand reinvents neither — it composes them.

> **MAINTAINER'S RULE** — Preserve the ordering and the guards. If you add a service, add its unit to the `SERVICES` list in `install.sh` and enable it the same way — do not hand-roll a one-off. If you add a device, add a udev rule that matches by vendor/product ID and creates a stable `/dev/*` symlink; never make code depend on `/dev/ttyUSB0`. Never generate or test nginx before the TLS certificate exists, never open a core API port on the firewall, and never move the first-boot service's self-disable out of `ExecStartPre`. When in doubt, run the whole chain end to end on real hardware — including the pull-a-drive failover test — before you trust the change.


# 20. Maintenance, Updates, and Preflight — update.sh and preflight_check.py

*Two very different 'preflight' ideas share this chapter. scripts/preflight_check.py is the developer gate — the automated source-integrity check that must PASS before any change is called done. update.sh is the field maintenance menu that keeps a deployed system running. And preflight.html is the operator's field-readiness check, the GO / CAUTION / NO-GO verdict before an activation. Knowing which is which is the whole point.*

> **IN ONE SENTENCE** — `scripts/preflight_check.py` is the *developer gate* that must pass before code is done, `update.sh` is the *field maintenance menu* that keeps a deployed Raspberry Pi running, and `preflight.html` is the *operator's readiness check* that returns a GO / CAUTION / NO-GO verdict before an activation — three tools, three audiences, one word.


## What This Is / What It Is For

The word 'preflight' shows up twice in FieldCommand, meaning two completely different things, and confusing them is a real trap. One is a *developer gate*: `scripts/preflight_check.py`, an automated check that a code change has not broken the source before it ships. The other is a *field-readiness check*: `preflight.html`, the operator-facing checklist that produces a GO / CAUTION / NO-GO verdict before a team activates. This chapter covers both, plus `update.sh`, the maintenance menu that keeps an already-installed system healthy between releases.

The reason the developer gate exists at all comes down to how FieldCommand is built. It is a browser-loaded application: the Python back end is run directly by the interpreter, and the front end is HTML with JavaScript loaded straight into a browser. Nothing is ever compiled ahead of time. That is wonderful for a field appliance — there is no build step to fail in a shelter — but it removes the safety net a compiled language gives you. A stray syntax error in a Python service, a broken brace in a shell script, a malformed JavaScript block, or a corrupted JSON file will not be caught by a compiler, because there is no compiler. It will simply fail at runtime, in the field, possibly during an incident. `preflight_check.py` puts that safety net back.

> **JARGON, IN PLAIN WORDS** — A *compiled* language is checked and translated to machine code before it runs, so many mistakes are caught early. FieldCommand's Python and JavaScript are *interpreted* — read and run on the spot — so those same mistakes stay hidden until the line actually executes. A *gate* is a check that must pass before work is allowed to proceed. A *static check* inspects the source text without running it.


## preflight_check.py — The Developer Gate

The gate's own docstring states exactly the class of breakage it is built to catch — the failures a never-compiled app hides:

```
"""FieldCommand IMS — source integrity preflight.

Catches the class of breakage a browser-loaded, never-compiled app hides:
Python/shell syntax errors, invalid JSON, duplicated-file corruption, and
JavaScript syntax errors inside HTML <script> blocks.

Exits non-zero if any check fails. Used by .github/workflows/ci.yml.
"""
```

It runs five independent checks, each a small function returning a list of failures. *Python compile* walks `python/` and `docs_generators/` and asks Python itself to byte-compile every file, so a syntax error is reported without running the code:

```
def py_compile_all():
    import py_compile
    fails = []
    for base in ("python", "docs_generators"):
        for f in glob.glob(os.path.join(ROOT, base, "**", "*.py"), recursive=True):
            try:
                py_compile.compile(f, doraise=True)
            except py_compile.PyCompileError as e:
                fails.append((rel(f), str(e).splitlines()[-1]))
    return fails
```

*Shell syntax* runs `bash -n` (parse, do not execute) on every script under `scripts/`. *JSON valid* opens and parses every `.json` file in the tree — which is exactly what protects the per-chapter guide files this document is written in. Both are the same tiny pattern: glob the files, run the check, collect failures. Notice that the shell and JavaScript checks degrade gracefully when their tool is missing locally, printing a note and returning no failures, because Continuous Integration (CI) will run them anyway:

```
def shell_all():
    if not shutil.which("bash"):
        print("       (bash not found — shell check skipped locally; CI runs it)"); return []
    fails = []
    for f in glob.glob(os.path.join(ROOT, "scripts", "**", "*.sh"), recursive=True):
        r = subprocess.run(["bash", "-n", f], capture_output=True, text=True)
        if r.returncode:
            fails.append((rel(f), r.stderr.strip()))
    return fails
```

*Corruption / duplication* is the check unique to this project, and it exists because the most common way a hand-edited or tool-merged file breaks here is accidental duplication — a file pasted into itself, two `*main*` guards, two license headers, two top-level `<!DOCTYPE>` lines. It scans source files for those tell-tale signs, and for whole-file duplication it looks for an early chunk of the file recurring later:

```
        if ext == ".py":
            if len(re.findall(r'(?m)^if __name__ ?== ?["\']__main__["\']', c)) > 1:
                flags.append("2+ __main__ guards")
            if c.count("SPDX-License-Identifier") > 1:
                flags.append("2+ SPDX headers")
        if ext in (".html", ".htm"):
            if len(re.findall(r'(?mi)^<!doctype', c)) > 1:
                flags.append("2+ top-level <!DOCTYPE>")
        s = c.strip()
        if len(s) > 800 and s.count(s[:180]) > 1:
            flags.append("early-content chunk recurs (possible whole-file duplication)")
```

*JavaScript syntax* is the cleverest check, because the app's JavaScript is not in tidy `.js` files — most of it lives inside `<script>` blocks in HTML pages. The check extracts every script block with a regular expression, writes each to a temporary file, and runs `node --check` (Node's parse-only mode) on it, reporting the page and the block number on failure:

```
        blocks = [c] if f.endswith(".js") else re.findall(r'<script\b[^>]*>(.*?)</script>', c, re.S | re.I)
        for i, b in enumerate(blocks):
            if not b.strip():
                continue
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
                tf.write(b); name = tf.name
            r = subprocess.run(["node", "--check", name], capture_output=True, text=True)
            os.unlink(name)
            if r.returncode:
                msg = (r.stderr.strip().splitlines() or ["syntax error"])[0]
                fails.append((f"{rel(f)} [script #{i}]", msg))
```

`main()` ties them together. A normal run does all five; the `--js-only` and `--corruption-only` flags run just one for a fast focused pass. The result is boiled down to a single line and a single exit code — the thing CI and a maintainer both read:

```
    ok &= report("Python compile", py_compile_all())
    ok &= report("Shell syntax", shell_all())
    ok &= report("JSON valid", json_all())
    ok &= report("Corruption / duplication", corruption())
    ok &= report("JavaScript syntax", js_all())
    print("\nPREFLIGHT:", "PASS" if ok else "FAIL")
    sys.exit(0 if ok else 1)
```

> **THE ONE RULE** — `preflight_check.py` must print *PREFLIGHT: PASS* before any change is considered done. It runs locally before a push and again in `.github/workflows/ci.yml`, and it exits non-zero on any failure so CI turns red. This is the project's single hard gate: green preflight is the definition of 'the source is not broken.' Do not merge, deploy, or call a task finished while it is FAIL.


## update.sh — Maintaining a Live Deployment

Where `preflight_check.py` guards the source before it ships, `update.sh` operates on a system that is already installed and running in the field. It is a single interactive menu — the one command an operator or maintainer runs to do routine upkeep without touching the full installer. It opens with a numbered list and reads one choice:

```
echo -e "${BOLD}${AMBER}FieldCommand Maintenance Menu${NC}"
echo "  1) Restart all services"
echo "  2) Stop all services"
echo "  3) Check service status"
echo "  5) Refresh FCC database"
echo "  6) Fetch repeater data"
echo "  7) Update web files from current directory"
echo "  8) Backup data to /tmp"
echo "  t) Apply theme consistency check"
read -rp "Select [0-9]: " CHOICE
```

The script is written defensively — `set -euo pipefail` at the top means it stops on the first unhandled error rather than blundering onward. Several menu items tie directly to tools covered elsewhere in this guide: option 6 runs `fetch_repeaters.py` (Chapter 18) and even prompts for the RepeaterBook token if none is saved yet; option `t` runs `apply_theme.py` (Chapter 18) in check mode and offers to apply fixes. The most substantial item is option 7, *Update web files*, which is how a code change actually reaches a running box. It copies the HTML across, then copies a fixed list of Python files, then restarts the services so they pick up the new code:

```
        # Also update Python files so servers stay in sync with HTML
        PY_FILES=(
            db.py
            fcc_lookup_server.py
            health_monitor.py
            fetch_repeaters.py
            ics_platform_server.py
            apply_theme.py
            nims_definitions.py
            nims_resource_types.py
        )
        for f in "${PY_FILES[@]}"; do
            SRC="$SCRIPT_DIR/../python/$f"
            if [[ -f "$SRC" ]]; then
                sudo cp "$SRC" "$FC_HOME/python/$f"
                sudo chmod 755 "$FC_HOME/python/$f"
            fi
        done
        # Restart services to pick up changes
        for svc in fcc-lookup health-monitor deadmans ics-platform ...; do
            sudo systemctl restart "$svc.service" 2>/dev/null && ...
        done
```

The rest of the menu is day-to-day operations: restart, stop, or status-check the systemd services; stream live logs with `journalctl`; rebuild the Federal Communications Commission (FCC) license database; back up the data directory with `rsync`; and show disk usage. Each item is a short, self-contained `case` branch that prints colored success or failure so a maintainer can see at a glance whether it worked. This is deliberately a maintenance tool, not a deployment pipeline — it assumes the code it is copying already passed the developer gate.

> **update.sh TRUSTS THE SOURCE — preflight_check.py IS WHAT EARNS THAT TRUST** — Option 7 copies whatever is in the working directory onto a live field system and restarts services. It performs no syntax checking of its own. That is safe *only because* `preflight_check.py` is supposed to have passed first. The two tools are a pair: the gate proves the source is sound, the menu deploys it. Running `update.sh` on un-checked source is how a broken file reaches the field.


## preflight.html — The Field-Readiness Check

The third 'preflight' has nothing to do with source code. `preflight.html` is the operator's pre-activation checklist, and its output is an operational verdict, not a build result. It walks the team through categories — Data Readiness, Power Systems, Communications Equipment, Computing, Personnel, Logistics, Safety, and Agency Coordination — and each item is marked GO, CAUTION, or NO-GO. The verdict logic is unforgiving in the right way: any NO-GO, or any required item left unconfirmed, forces an overall NO-GO:

```
  } else if(nogoCount>0) {
    verdict='nogo'; sub=`${nogoCount} NO-GO item${nogoCount!==1?'s':''} identified — do not activate`;
  } else if(requiredFail>0) {
    verdict='nogo'; sub=`${requiredFail} required item${requiredFail!==1?'s':''} not confirmed — cannot activate`;
  } else if(cautionCount>0) {
    verdict='caution'; sub=`${cautionCount} item${cautionCount!==1?'s':''} require attention before activation`;
  } else {
    verdict='go'; sub='All checklist items confirmed — cleared for activation';
  }
```

The Data Readiness section is partly automatic: it calls the server's `/api/preflight` endpoint and pre-marks items like the FCC database and member roster based on what the system actually reports, which the operator can then override. The whole thing runs in the browser, saves progress to local storage, and can print or export a JavaScript Object Notation (JSON) report for the incident record. It is a decision aid for a human team, evaluated fresh every activation.

> **TWO PREFLIGHTS, SIDE BY SIDE** — *`preflight_check.py`* — audience: developers/CI. Question: 'is the source broken?' Output: PASS / FAIL exit code. When: before every change ships.  *`preflight.html`* — audience: field operators. Question: 'are we ready to activate?' Output: GO / CAUTION / NO-GO verdict. When: before every activation. They share a name and nothing else; never let a green code gate be mistaken for field readiness, or vice versa.


## Why It Matters / Design Takeaways

- *A never-compiled app needs a static gate.* `preflight_check.py` restores the safety net a compiler would give: it catches Python, shell, JSON, corruption, and in-HTML JavaScript errors before they reach a field system.
- *One rule, one signal.* Everything collapses to `PREFLIGHT: PASS` / `FAIL` and an exit code, so the same check guards a local push and a CI run identically.
- *Maintenance and deployment are separated from the gate.* `update.sh` keeps a live box healthy and copies checked source onto it, but trusts that the gate already ran — the two form a pair, not a substitute.
- *Same word, different jobs.* The developer gate and the field-readiness checklist both say 'preflight,' but one asks 'is the code sound?' and the other asks 'are we ready to activate?' — never conflate them.

> **MAINTAINER'S RULE** — No change is done until `python scripts/preflight_check.py` prints *PREFLIGHT: PASS* — run it locally before you push, and never merge while CI's copy is red. When you add a new file type or a new duplication footgun, add a check for it here so the gate keeps pace with the codebase. And keep the three tools straight: `preflight_check.py` gates the source, `update.sh` maintains the deployment, `preflight.html` clears the field team — do not let one stand in for another.
