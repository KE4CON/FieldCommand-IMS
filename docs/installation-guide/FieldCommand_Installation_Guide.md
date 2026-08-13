# FieldCommand IMS — Installation Guide (World Edition)

*Set up the field server, the network, the workstations, and the offline data — step by step, in plain language.*

*Generated August 13, 2026 · Markdown is the living source of truth.*


---


# 1. Overview — What You're Building

*The whole FieldCommand system at a glance: two small computers, a Wi-Fi network, and a set of workstations — so any phone, tablet, or laptop can run the full incident-management toolset with no internet and no app to install.*

> **QUICK VERSION** — You're building a self-contained command post out of two small computers (Raspberry Pi 5 units), a Wi-Fi router, and a network switch. One computer runs all the FieldCommand tools; the other is an optional amateur-radio gateway. Together they create a private Wi-Fi network named **EMCOMM-NET**. Anyone joins that Wi-Fi from a phone, tablet, or laptop, opens a browser to **http://192.168.50.1**, and has the whole system — no internet, no app to install, nothing to set up on their device. This chapter is the map; the rest of the guide is the build.


## What This Is / What It Is For

FieldCommand Incident Management System (IMS) is a complete, self-contained command post that runs without the internet. It gives an emergency-operations team everything it needs to manage an incident — Incident Command System (ICS) forms, net (radio traffic) logging, resource and personnel tracking, maps, cost documentation, and an offline reference library — all from an ordinary web browser. Nobody needs a special app, an account, or a working internet connection. If the power is out and the cell towers are down, FieldCommand still works, because it carries its own network and all of its data with it.

This chapter does not ask you to build anything yet. It is the picture on the front of the puzzle box: it shows you every piece, explains what each one is for, and shows how they connect — so that when the later chapters walk you through the build step by step, you already understand what you are assembling and why. Read it once, and the rest of the guide will make much more sense.

> **OFFLINE-FIRST IS THE WHOLE POINT** — "Offline-first" means the system is designed to work perfectly with **no internet at all**, and simply does a little extra when the internet happens to be available. That is the opposite of most modern software, which stops working the moment it loses signal. FieldCommand is built the way it is because incidents are exactly when the internet is least reliable.


## The Two Servers — Two Raspberry Pi 5 Computers

The heart of the system is two small computers called **Raspberry Pi 5** units. A Raspberry Pi is a full computer about the size of a deck of cards; it runs quietly, sips power, and costs a fraction of a normal desktop. FieldCommand uses two of them, each with its own separate job. Keeping the jobs on separate computers means one can be rebooted, reconfigured, or upgraded without disturbing the other — and if one ever fails, the other keeps doing its job.

| Server | Address | What it does |
| --- | --- | --- |
| **FieldCommand application server** | `192.168.50.1` | The main computer. It runs **all** of the FieldCommand tools — the dashboard, the ICS forms, net logging, the maps, the roster, the offline reference library, and the health monitor. This is the address everyone opens in their browser to use the system. |
| **44Net / AMPRNet gateway** | `192.168.50.2` | A second, dedicated computer whose only job is to be an amateur-radio internet gateway (the amateur-radio internet is called **AMPRNet** or **44Net**). It is completely optional — only amateur-radio groups use it — and it is kept separate so it can never interfere with the main server. |

> **THE TWO SERVERS ARE THE SAME IN EVERY EDITION** — Both Raspberry Pi 5 servers are identical no matter which group is deploying FieldCommand. What differs between deployments is only the operator workstations and the choice of internet source — both covered below. The servers themselves never change.


## The Network — EMCOMM-NET

The two servers, the workstations, and everyone's phones and tablets all need a way to talk to each other. That is what the network is for. FieldCommand's network is created by two pieces of equipment working together:

- *An ASUS Wi-Fi router.* This broadcasts the private Wi-Fi network — named **EMCOMM-NET** by default — that every device joins. It is a travel-sized Wi-Fi 7 router. Notably, **neither Raspberry Pi creates the Wi-Fi**; the router does that job, which keeps the servers free to do their own work. For larger buildings, two more identical routers can be added as "mesh" extenders to spread the same EMCOMM-NET signal further (covered in the hardware chapter).
- *A UniFi network switch.* A switch is simply a box with many network sockets that lets wired devices join the same network with a plain Ethernet cable. It gives the two servers, the workstations, and a printer fast, rock-solid wired connections, and leaves room to plug in more.

Together, the router and switch form **EMCOMM-NET** — the private, self-contained network the whole command post lives on. It exists whether or not there is any internet, because the router and switch make it themselves. The name **EMCOMM-NET** comes from "emergency communications"; it is just the default network name and has nothing to do with any callsign or group.

> **EMCOMM-NET IS SELF-CONTAINED** — EMCOMM-NET is your own private network. It does not depend on the internet, a phone company, or any outside service to exist. As long as the router and switch have power, the network is up and everyone on it can reach the FieldCommand server — even in a parking lot in the middle of nowhere.


## The Operator Workstations

For the people running the incident from the command post itself, FieldCommand includes dedicated **operator workstations** — Raspberry Pi 500 units, one per operator station, each with its own monitor. These are the seats where net control operators, the planning section, and others sit and work all shift. They connect to EMCOMM-NET by wired cable through the switch, so they are always fast and never drop out.

But here is the key idea that makes the whole design so flexible: **you do not have to use the provided workstations to use FieldCommand.** Because every tool runs in a plain web browser, any device that can join Wi-Fi and open a web page can be a full FieldCommand station.


## How Any Phone, Tablet, or Laptop Joins In

This is the part that surprises most people, so it is worth stating plainly. For anyone to use the entire system, they do just two things:

1. Join the Wi-Fi network named **EMCOMM-NET** (the same way you'd join any Wi-Fi — pick it from the list and enter the password).
2. Open a web browser and go to **http://192.168.50.1** (type it exactly, including the `http://`).

That's it. The full FieldCommand dashboard opens, and every tool is available. There is **no app to download**, **no account to create**, **no internet required**, and **nothing to install or configure on the device**. A volunteer can walk in with the phone in their pocket, join EMCOMM-NET, open the page, and start logging traffic within a minute. The same is true for a tablet, a personal laptop, or a borrowed Chromebook. Everyone reaches the same live system at the same address, and everyone sees the same up-to-the-second information.

> **WHY A BROWSER, AND WHY IT MATTERS** — Running everything in the web browser is a deliberate choice. Browsers are already on every phone, tablet, and computer, so there is nothing to install and nothing that can be the "wrong version." It also means a team can scale from two operators to twenty just by having more people join EMCOMM-NET — no extra software, no licenses, no setup.


## How the Pieces Fit Together

Here is the entire system in one table. Every later chapter builds one of these pieces; this is the shape of the finished command post.

| Piece | What it is | Its job in the system |
| --- | --- | --- |
| FieldCommand application server | A Raspberry Pi 5 at `192.168.50.1` | Runs all the tools; the address everyone's browser opens. |
| 44Net / AMPRNet gateway | A second Raspberry Pi 5 at `192.168.50.2` | Optional amateur-radio internet gateway; kept separate from the main server. |
| ASUS Wi-Fi router | A travel-sized Wi-Fi 7 router (plus optional mesh units) | Broadcasts the EMCOMM-NET Wi-Fi that all devices join. |
| UniFi network switch | A managed 16-port switch | Wires the servers, workstations, and printer together at high speed. |
| Operator workstations | Raspberry Pi 500 units with monitors | Dedicated seats for the command-post staff (optional but recommended). |
| Any phone / tablet / laptop | Whatever devices people already have | Join EMCOMM-NET, open `http://192.168.50.1`, and become a full station. |


## What's Required and What's Optional

The command post above is fully functional entirely on its own, with no outside connection. A few things are genuinely optional and only add extra capability when you want it:

| Capability | Required? | What it adds |
| --- | --- | --- |
| **Internet / wide-area network (WAN)** | Optional | When available, it switches on live extras — National Weather Service alerts, live amateur-radio position data, and space-weather propagation. The core system works fully without it. The internet source differs by edition: a cellular modem (primary internet) or a satellite link (fallback internet). |
| **Amateur radio** | Optional | Adds the ham features — APRS position mapping, Winlink email-over-radio, the 44Net gateway, and JS8Call. These legally require a licensed operator, so a group without one simply skips them. All amateur-radio setup lives in Part 2 of this guide. |

> **NON-HAM GROUPS: YOU LOSE NOTHING** — If your group has no licensed amateur-radio operators, you skip the second (gateway) Raspberry Pi and all of Part 2. The core incident-management system — ICS forms, net logging, resource tracking, maps, cost documentation, and the offline library — is completely unaffected and remains fully usable.


## How the Rest of This Guide Is Organized

The guide is split into two parts so you only read what applies to you:

- *Part 1 — Core install (everyone).* This builds the command post described in this chapter: the hardware you need, the one-command server setup, the pull-a-drive reliability test, the network, the workstations, printing, and the offline data library. Every group does Part 1.
- *Part 2 — Amateur radio (optional).* This covers the ham-radio additions: the 44Net gateway, APRS, Winlink, and the related equipment. Only groups with a licensed amateur-radio operator need it; everyone else can stop after Part 1.

The very next chapter is the shopping list — every piece of hardware named above, with the exact models and what each one is for — so you can gather (or check off) everything before the build begins.


## Troubleshooting

- *I only have one Raspberry Pi — is that a problem?* Only if you want amateur-radio features. The **second** Pi is the optional 44Net/AMPRNet gateway. The core system runs entirely on the first Pi (the application server at `192.168.50.1`). Non-ham groups need only one.
- *Do operators need the internet to use FieldCommand?* No. Everything runs on the local EMCOMM-NET network. The internet is optional and only adds live extras (weather alerts, propagation data). With no internet, the full incident-management system still works.
- *Does each person have to install an app or make an account?* No. Anyone joins the EMCOMM-NET Wi-Fi and opens `http://192.168.50.1` in a browser. There is no app, no account, and no per-device setup.
- *I joined EMCOMM-NET but the page won't load.* Make sure you typed the full address including `http://` — for example `http://192.168.50.1` — and that you are connected to **EMCOMM-NET** specifically, not some other nearby Wi-Fi. Confirm the router and the application-server Pi both have power.
- *Why is the Wi-Fi named EMCOMM-NET and not my group's name?* `EMCOMM-NET` is just the default network name (short for "emergency communications"). You can rename it later in the Setup screen; it is never tied to a callsign or a specific group.


# 2. What You Need — Hardware & Bill of Materials

*The complete shopping list for a FieldCommand command post: the two servers, the network gear, the operator workstations, printers, backup drives, and the optional extras — with exact models and what each part is for.*

> **QUICK VERSION** — Gather two **Raspberry Pi 5** computers (16 GB), an enclosure with two mirrored solid-state drives for the main one, three **ASUS RT-BE58 Go** Wi-Fi routers, one **UniFi Switch Lite 16 PoE** network switch, four **Raspberry Pi 500** workstations with monitors, a printer, and a backup drive. That's a full command post. Amateur-radio gear is a separate optional category you can skip entirely if your group has no licensed operators. The tables below give the exact models and the reason for each.


## What This Is / What It Is For

This chapter is the shopping list. It names every piece of hardware in a FieldCommand command post, tells you the exact model to look for, and — just as importantly — explains **why** each part is there, so you can make sensible substitutions or trim the list to fit your budget and your mission. Nothing here is a surprise: every item was introduced in the Overview chapter; this is where you get the specifics.

You do not need to be a computer person to use this list. Read each table's "Purpose" column to understand what a part does, then buy (or check off) the model named. Where a part is optional, the table says so plainly. Prices, where shown, are rough guides only and move around a lot — treat any "~$" figure as a ballpark, not a quote.

> **HOW TO READ THIS LIST** — **Required** items are the minimum for a working core system. **Recommended** items are ones almost every group will want. **Optional** items add capability you may or may not need. The single biggest optional block is the **Amateur Radio Equipment** category at the end — an entire group of parts that non-ham deployments skip completely.


## The Two Servers — Raspberry Pi 5 Units

FieldCommand runs on two Raspberry Pi 5 computers. One is the **application server** that runs all the tools; the other is the **44Net / AMPRNet gateway** for amateur-radio groups. They use the same base computer so you can keep a single type of spare part on hand. The important difference is the enclosure and drives: the application server holds its data on **two mirrored drives** for reliability, while the gateway needs only a single modest drive.

| Unit | Computer & enclosure | Storage | Role |
| --- | --- | --- | --- |
| **FieldCommand application server** | Raspberry Pi 5 — 16 GB memory (RAM), in a **Pironman MAX 5** tower enclosure (holds two M.2 solid-state drives, has a small display and cooling fans) | **2 × 1 TB NVMe SSD**, set up as a **RAID 1 mirror** (two drives holding an identical copy, so one can fail without data loss) | Runs every FieldCommand service: web server, forms, net logging, maps, roster, offline library, health monitor. Fixed address `192.168.50.1`. |
| **44Net / AMPRNet gateway** | Raspberry Pi 5 — 16 GB memory (RAM), in a compact **Argon NEO 5 M.2** case (small, quiet, passively cooled) | **256 GB M.2 SATA SSD** (holds the operating system, the tunnel configuration, and routing tables) | Dedicated amateur-radio internet gateway. Completely independent of the application server. Fixed address `192.168.50.2`. |

> **ACRONYMS, IN PLAIN WORDS** — **RAM** (Random Access Memory) is a computer's short-term working memory. **SSD** (Solid-State Drive) is fast storage with no moving parts. **NVMe** and **SATA** are two ways an SSD connects — NVMe is faster; SATA is cheaper and plenty for the gateway. **RAID 1** means two drives kept as identical mirror copies so one can fail with no data loss. The one-command setup chapter builds and tests that mirror for you.

> **BUDGET TIP FOR THE GATEWAY** — The gateway does very little compared to the main server. If money is tight, an **8 GB** Raspberry Pi 5 works fine for the gateway-only role. Matching both units at 16 GB is only about keeping your spare parts interchangeable.


## Networking — Router, Mesh, and Switch

The network is what ties every device together into EMCOMM-NET. Neither Raspberry Pi makes the Wi-Fi — that is the router's job. Wired devices connect through the switch. Here is the core networking gear:

| Device | Model / spec | Purpose |
| --- | --- | --- |
| **Wi-Fi router** | ASUS RT-BE58 Go — Wi-Fi 7, 2.5 G LAN uplink, USB-C 18 W power — **quantity 3 recommended** (1 primary + 2 mesh nodes) | Broadcasts the EMCOMM-NET Wi-Fi, hands out addresses to devices, and (when present) routes the optional internet connection. Travel-sized and rugged. |
| **Network switch** | Ubiquiti UniFi Switch Lite 16 PoE — 16 gigabit ports, 8 with Power over Ethernet (PoE), 2 fiber uplink ports | Wires the two Pis, the workstations, the laptop, and a printer together at full speed, with room to spare. The PoE ports can power cameras or extra access points without a separate power brick. |
| **Ethernet cables** | CAT 6 patch cables, roughly 1–6 ft, about 10 of them | Connect the router to the switch, both Pis, the laptop, the printer, and the four workstations. Buy lengths that suit your table layout. |

> **WHAT "POE" MEANS** — **PoE** (Power over Ethernet) means a single network cable carries both data **and** electrical power. It lets you run a camera or a Wi-Fi access point from just one cable, with no nearby power outlet — handy in a bare EOC room or a tent.


## Extending Wi-Fi Coverage for Larger Venues

A single router covers a normal room easily. For a big building, a shelter, or an outdoor staging area, you add one or two more of the **same** ASUS routers as "mesh nodes" — extra Wi-Fi points that repeat the exact same EMCOMM-NET network. Devices move between them automatically with no reconnecting and no password re-entry. Because every router is identical, any one of them can serve as the primary.

| Deployment scenario | Recommended setup |
| --- | --- |
| Single room, under 2,500 sq ft | 1 × RT-BE58 Go primary only — no extension needed |
| Multi-room EOC or large shelter, 2,500–7,500 sq ft | 1 primary + 1 mesh node — wired backhaul through the switch |
| Large building or campus, 7,500–20,000 sq ft | 1 primary + 2 mesh nodes — wired backhaul through the switch |
| Outdoor search-and-rescue staging area | 1 primary at the command post + 1–2 mesh nodes at field positions, run on battery |

> **WIRED "BACKHAUL" IS BEST WHEN YOU CAN** — "Backhaul" is the link that carries traffic from a mesh node back to the main router. Running a CAT 6 Ethernet cable from the switch to each mesh node (a **wired** backhaul) gives full speed and rock-solid reliability. Wireless backhaul works too and is fine when running a cable isn't practical — for battery-powered field positions, for example.


## Operator Workstations

For the staff working the whole shift at the command post, FieldCommand includes dedicated workstations — one per operator seat. These are always-connected wired stations, so they never drop out. Remember from the Overview chapter that they are **recommended, not required**: any phone, tablet, or laptop on EMCOMM-NET is also a full station. The workstation model is the one part of the build that differs between editions.

| Item | Model / spec | Purpose |
| --- | --- | --- |
| **Operator workstation × 4** | Raspberry Pi 500 — a complete computer built into a keyboard, one per operator station | The permanent seats for net control, planning, and other command-post roles. |
| **Workstation monitor × 4** | Raspberry Pi Monitor 15.6" Full HD touchscreen — built-in speakers, kickstand, powered over USB-C | One screen per workstation. Touchscreen makes forms and maps easy to work with. |
| **Video & power cables** | One micro-HDMI-to-HDMI cable and one 27 W USB-C power supply per station | Connects each workstation to its monitor and powers it. Often the monitor can power the workstation over USB-C, simplifying cabling. |


## Backup, Location, and Connectivity Extras

A handful of small accessories protect your data and add useful capability. The two backup items are strongly recommended; the rest are genuinely optional.

| Item | Required? | Purpose |
| --- | --- | --- |
| USB flash drive, 32 GB or larger, **labeled `FIELDCOMMAND`** | Recommended | Plug it in and FieldCommand instantly backs up all live data to it — a one-second insurance policy. The label is what triggers the automatic backup. |
| External USB hard drive, 1 TB or larger (e.g. LaCie Rugged) | Recommended | Holds the full incident archive and a complete system backup. A rugged model survives drops and crushing in the field. Label it `FIELDCOMMAND` for automatic backups too. |
| 2D barcode / QR-code scanner (USB or Bluetooth keyboard-wedge) | Recommended | Speeds up a staffed check-in table: scan an operator's QR access card instead of typing. Must be a **2D imager** (see the note below). Needs no drivers and no camera — it types the scanned code like a keyboard. Roughly $50–100. |
| USB GPS receiver (u-blox or GlobalSat puck) | Optional | Gives the system a live position for the tactical map and location-based weather alerts. |
| Powered USB hub (4- or 7-port, **with its own power supply**) | Optional | Needed only if you connect several USB devices at once (GPS + backup drive + radio interface). It **must** be a powered hub — unpowered ones cause instability. |
| Avery 5371 business-card sheets | Optional | For printing operator access cards — 10 cards per sheet, laser or inkjet. |

> **THE SCANNER MUST BE A "2D" MODEL TO READ QR CODES** — There are two kinds of handheld scanner, and only one reads the square QR codes FieldCommand puts on operator access cards. A **1-dimensional (1D)** scanner reads only the old-style striped **linear barcodes** — the kind on a grocery item — and **cannot** read a QR code. A **2-dimensional (2D)** scanner (also called a **2D imager**) reads both the striped barcodes **and** square QR codes. **Buy a 2D model.** When shopping, look for the words "2D", "QR", or "imager" in the product name; avoid anything that says "laser" or "1D" only. Either **USB** (plug-in) or **Bluetooth** (wireless) is fine — both types act as a "keyboard wedge," meaning the scanned code simply appears in whatever box the cursor is in, exactly as if you had typed it. No software or driver is needed.

The FieldCommand server also needs an internet source **only if** you want the optional live extras (weather alerts, propagation data). The wide-area-network (WAN) source depends on your edition: a cellular modem (primary internet) or a satellite link (fallback internet). Site Ethernet or a tethered phone also work. The core system runs perfectly with no WAN at all.


## Printers

Printing ICS forms, maps, and Incident Action Plans on paper is a core part of running an incident. FieldCommand shares one printer across the whole EMCOMM-NET network using the built-in printing system (installed automatically), so any operator can print to it. Pick the printer that suits your operation — you do not need all of these, just one.

| Category | Example models | Best for |
| --- | --- | --- |
| **Monochrome laser** | Brother HL-L2350DW (recommended); HP LaserJet Pro M15w / P1102w | The everyday workhorse — fast, cheap per page, excellent Linux support. Best all-around choice for text forms. |
| **Color multifunction laser** | Brother MFC-L3770CDW; HP Color LaserJet Pro MFP M479fdw; Canon imageCLASS MF743Cdw | Print, scan, copy, and fax in one. Prints color maps and IAP packages. Good for a permanent EOC install. |
| **Portable / battery-powered** | Canon PIXMA TR150 (built-in battery); HP OfficeJet 200 | Field deployments with no wall power — a shelter, a tent, a vehicle. Runs on a charge. |

> **USB OR WI-FI — EITHER WORKS** — You can plug a printer into the FieldCommand server by USB and it becomes shared across EMCOMM-NET automatically, **or** connect a Wi-Fi printer directly to EMCOMM-NET. Both approaches are covered in the printer-setup chapter.


## The Full Bill of Materials, at a Glance

This table gathers the core parts (Part 1) into one place so you can shop or check them off in a single pass. Amateur-radio equipment is listed separately in the next section because most of it is optional.

| Item | Model / spec | Quantity |
| --- | --- | --- |
| Raspberry Pi 5 — 16 GB (application server) | Raspberry Pi 5 Model B, 16 GB RAM | 1 |
| Pironman MAX 5 enclosure | Tower case, dual M.2 NVMe, display, active cooling | 1 |
| NVMe SSD (for the mirror) | 1 TB M.2 2280 PCIe NVMe (e.g. WD Blue SN580, Samsung 980) | 2 |
| Raspberry Pi 5 — 16 GB (44Net gateway) | Raspberry Pi 5 Model B, 16 GB RAM (8 GB works for gateway-only) | 1 |
| Argon NEO 5 M.2 case | Compact, passively cooled, M.2 SATA slot | 1 |
| M.2 SATA SSD (gateway) | 256 GB M.2 SATA SSD | 1 |
| Raspberry Pi 27 W USB-C power supply | Official Raspberry Pi 27 W USB-C supply — one per Pi | 2 |
| MicroSD card (initial setup) | 32 GB Class 10 / A1 microSD | 1 |
| ASUS RT-BE58 Go router | Wi-Fi 7 travel router (1 primary + 2 mesh nodes) | 3 |
| UniFi Switch Lite 16 PoE | Ubiquiti USW-Lite-16-PoE — 16-port gigabit, 8 × PoE | 1 |
| CAT 6 Ethernet cables | 1–6 ft patch cables | ~10 |
| Raspberry Pi 500 operator workstation | Keyboard computer, one per operator station | 4 |
| Raspberry Pi Monitor 15.6" | Full HD IPS touchscreen — one per workstation | 4 |
| USB flash drive, labeled FIELDCOMMAND | 32 GB+ USB 3.0 — auto-backup trigger | 1 |
| External USB hard drive | 1 TB+ (e.g. LaCie Rugged) — archive & full backup | 1 |
| 2D barcode / QR scanner (optional, recommended) | USB or Bluetooth 2D imager / keyboard-wedge — for a staffed check-in table | 1 |
| Printer (choose one) | Monochrome, color MFP, or portable — see printer table | 1 |


## Amateur-Radio Equipment (Optional — Part 2)

> **SKIP THIS ENTIRE CATEGORY IF YOU HAVE NO HAMS** — Every item below is needed **only** if a licensed amateur-radio group is leading or partnering in the deployment. If FieldCommand is being deployed by a public-safety agency or a served organization **without** licensed amateur-radio operators, skip this whole category. The core system in Part 1 is unaffected.

For groups that do use amateur radio, these are the parts that enable the ham features. They are covered in full in Part 2 of this guide; the table here is just so you can plan and purchase alongside the rest.

| Item | Needed when | Purpose |
| --- | --- | --- |
| USB radio interface — Digirig Mobile | Using APRS | A tiny combined sound and control interface that connects a radio to the Pi, enabling APRS transmit and receive. |
| USB radio interface — SignaLink USB (alternative) | Using APRS | A widely used sound interface; needs a radio-specific audio cable. Interchangeable with the Digirig for this role. |
| Mobilinkd TNC4 (Bluetooth alternative) | Using APRS | A wireless APRS interface — useful when no USB port is free or for very portable setups. |
| Rig interface cable | Using any radio interface | The radio-specific audio and push-to-talk cable joining the interface to your transceiver. Buy the one for your radio model. |
| Windows laptop | Using HF (high-frequency) radio | Any Windows 10/11 laptop, for Winlink Express and JS8Call. Connects to the radio by USB. See Part 2E. |


## Troubleshooting

- *Do I really need two Raspberry Pi 5 units?* Only if you want amateur-radio features. The **second** Pi is the optional 44Net/AMPRNet gateway. A non-ham group buys just **one** Pi 5 (the application server) and skips the gateway entirely.
- *Can I use a single drive instead of two?* Yes, but you lose the safety of the mirror. The two-drive **RAID 1** setup means one drive can fail with no data loss — strongly recommended for a system running real incidents. With one drive, a drive failure loses everything since the last backup.
- *The exact Pi 5 or SSD model I want is out of stock or oddly expensive.* Prices and stock for Raspberry Pi 5 units and NVMe drives swing with memory-chip shortages. Any Raspberry Pi 5 (16 GB, or 8 GB for the gateway) and any reputable 1 TB M.2 NVMe drive will work — the specific brands named are examples, not requirements.
- *Do I have to buy the four workstations?* No. They are recommended dedicated seats, but any phone, tablet, or laptop on EMCOMM-NET is a full station (see the Overview chapter). Buy as many or as few workstations as your command post needs.
- *Which printer should I get if I only buy one?* For most groups, a monochrome laser (e.g. Brother HL-L2350DW) is the best single choice — fast, inexpensive to run, and well supported. Add a color or portable model only if your mission specifically needs color maps or battery printing.
- *My USB devices behave strangely when several are plugged in.* Use a **powered** USB hub (one with its own power adapter). Unpowered hubs can't supply enough power for a GPS, a backup drive, and a radio interface at once, which causes dropouts.


# 3. Before You Begin — Flash the microSD Card

*Put the operating system on a memory card and drop the FieldCommand software onto it — the one preparation step you do on your own computer before the Raspberry Pi ever powers on.*

> **QUICK VERSION** — On your computer, install the **Raspberry Pi Imager** from **raspberrypi.com/software**. Use it to write **Raspberry Pi OS (64-bit, Desktop)** to a microSD card, and in its **Advanced Options** set the hostname to **`fieldcommand.local`** and the username to **`fieldcommand`** (that exact username is required). When it finishes, a small drive named **`bootfs`** appears on your computer — copy the whole **`FieldCommand-IMS`** folder onto it. Put the card in the Pi 5, connect a monitor and keyboard, and power it on. The next chapter runs the one command that builds the server.


## What This Is / What It Is For

A Raspberry Pi doesn't come with an operating system — the software that makes it a working computer — so before it can do anything you have to put one on a memory card for it. That card is a **microSD card** (Secure Digital, the same tiny card a phone or camera uses). Writing the operating system onto the card is called **flashing** it. This chapter walks you through flashing the card on your own laptop or desktop computer, and then dropping the FieldCommand software folder onto that same card so it's waiting for the Pi on first boot.

Everything here happens **on your regular computer**, not on the Pi. The Pi stays switched off until the very end. When you're done, you'll have one prepared microSD card; you slide it into the Pi, power on, and the next chapter takes over. Think of this as packing the Pi's lunch before it goes to work.

> **WHO DOES THIS** — This is a one-time job for whoever is building the server — one person, at a desk, before the equipment ever ships to the field. It takes about fifteen minutes, most of which is the card writing itself while you wait.


## What You Need on Hand

- *A computer* — any Windows, macOS, or Linux laptop or desktop with a way to read a microSD card (a built-in card slot, or a small USB card reader).
- *A microSD card* — 32 gigabytes (GB) or larger is plenty for this setup card. A name-brand card (SanDisk, Samsung, Kingston) is worth the couple of extra dollars; cheap no-name cards fail often.
- *The Raspberry Pi Imager* — one free program from the Raspberry Pi people that both downloads the operating system and writes it to the card. Getting it is the next step.
- *The FieldCommand software* — the `FieldCommand-IMS` folder, either already on your computer or downloaded from GitHub (covered further down).

> **FLASHING ERASES THE CARD** — Writing the operating system wipes everything already on the microSD card. That's normal and expected for a blank setup card — but if you grabbed a card that has photos or other files on it, copy those off first. The Imager will warn you before it writes, but it never hurts to check.


## Install the Raspberry Pi Imager

1. On your computer, open a web browser and go to **raspberrypi.com/software** (type it exactly).
2. Click the big download button for **your** computer's system — it offers **Download for Windows**, **Download for macOS**, and **Download for Ubuntu/Linux**. Pick the one that matches the computer you're using.
3. When the file finishes downloading, open it and follow the normal install prompts for your system (on Windows, click through the installer; on macOS, drag the Raspberry Pi Imager icon into your Applications folder).
4. Open the newly installed **Raspberry Pi Imager**. You'll see a simple window with three buttons: **Choose Device**, **Choose OS**, and **Choose Storage**.

> **"OS" MEANS OPERATING SYSTEM** — Throughout the Imager and this guide, **OS** is short for **operating system** — the base software that runs the computer, the same idea as Windows or macOS on your laptop. On the Pi it's a version of Linux called Raspberry Pi OS.


## Choose the Device and the Operating System

1. Click **Choose Device** and select **Raspberry Pi 5** — the model this build uses.
2. Click **Choose OS**. From the list, pick **Raspberry Pi OS (other)**, then choose **Raspberry Pi OS (64-bit)** — the full **Desktop** edition.

There are a few editions to choose from, and the right one depends on how you plan to work. For **building and setting up** the server, the **Desktop** edition is the easiest because it gives the Pi a normal screen with a mouse, menus, and a web browser right on the Pi — handy for testing. Here is the plain-language comparison:

| OS edition | What it gives you | Best for |
| --- | --- | --- |
| **Raspberry Pi OS (64-bit) Desktop** *(recommended for setup)* | A full graphical screen on the Pi — menus, a mouse, and a local web browser. Easiest for new users and for testing. | Building the server and troubleshooting with a monitor and keyboard connected. |
| **Raspberry Pi OS (64-bit) Lite** | No screen or menus at all — text only. Uses less memory and boots faster, but you configure it over the network from your laptop. | Experienced Linux admins running a lean production server. |
| **Ubuntu Server 24.04 LTS** | A different flavor of Linux, also text-only. Familiar to admins already standardized on Ubuntu. | Organizations that already use Ubuntu everywhere. |

> **WHEN IN DOUBT, PICK DESKTOP (64-BIT)** — If you're not sure, choose **Raspberry Pi OS (64-bit) Desktop**. It's the friendliest for the build steps in this guide, and everything in the next chapter is written assuming you have a monitor and keyboard on the Pi. You can always move to the leaner Lite edition later once you're comfortable.


## The Advanced Options — Set These Before You Write

Before it writes the card, the Imager lets you pre-fill some settings so the Pi comes up ready to use. This step matters — one of these settings is **required** for FieldCommand to install correctly.

1. Click **Choose Storage** and pick your microSD card from the list. Double-check the size matches your card, so you don't accidentally pick another drive.
2. Click **Next**. The Imager asks **"Would you like to apply OS customisation settings?"** — click **Edit Settings** (on some versions, the gear icon).
3. Fill in the settings using the table below.
4. Click **Save**, then click **Yes** to apply the settings, then **Yes** again to confirm you want to write the card. Writing takes several minutes — let it finish.

| Imager option | What to set it to | Why |
| --- | --- | --- |
| **Hostname** | `fieldcommand.local` | This is the name the Pi answers to on the network. Setting it here means the Pi is reachable as `fieldcommand.local` from any device. |
| **Username** | `fieldcommand` *(required — type it exactly)* | The FieldCommand installer expects this exact username. If you use anything else, the setup in the next chapter will not find its files. |
| **Password** | Choose a strong password and **write it down** | You'll need it the first time you use `sudo` on the Pi and to reach the print system's admin page. There is no way to recover it if you forget it. |
| **Enable SSH** | Optional for Desktop — leave it on if you'd like to reach the Pi remotely later; it's fine to leave off if you have a monitor and keyboard on the Pi | SSH (Secure Shell) is a way to control the Pi from another computer with no screen. The Desktop edition doesn't need it for setup. |
| **Configure wireless LAN (Wi-Fi)** | Enter your **home or workbench** Wi-Fi name and password | This gets the Pi online during the build so it can download software. The field network (EMCOMM-NET) is set up much later — this is just for now. |
| **Locale / Time zone & keyboard** | Set your local time zone (for example, US/Central) and keyboard layout | So the Pi's clock and keyboard match where you are. |

> **THE USERNAME MUST BE fieldcommand** — Of everything on this screen, the **Username** is the one you cannot change. Type **`fieldcommand`** exactly — all lowercase, one word. The installer in the next chapter looks for files under that exact user; a different name (even `FieldCommand` or `field_command`) will make the setup fail with confusing errors. The hostname `fieldcommand.local` and the password are up to you, but the username is fixed.


## Put the FieldCommand Software on the Card

Flashing put the operating system on the card. Now you add the FieldCommand software itself, so it's already there when the Pi boots — no internet required on the Pi. When the Imager finishes writing, it ejects and re-mounts the card, and a small drive appears on your computer named **`bootfs`**. That's the card's boot partition — the one place both your computer and the Pi can read.

1. Leave the card in your computer (or re-insert it) after the Imager finishes. Open your file manager (File Explorer on Windows, Finder on macOS).
2. Find the small drive named **`bootfs`**. It's usually just a few hundred megabytes in size — that's correct; it's meant to be small.
3. Copy the **entire `FieldCommand-IMS` folder** onto the `bootfs` drive — the whole folder, not just the files inside it. Drag it in, or copy and paste it.
4. Wait for the copy to finish completely before you eject the card. Then safely eject `bootfs` (right-click → Eject on Windows, or drag to the eject icon on macOS).

> **WHY THE FOLDER GOES ON bootfs SPECIFICALLY** — Flashing creates two drives on the card: **`bootfs`** (small, and readable by any computer) and **`rootfs`** (the big Linux part, which Windows and macOS can't open). The `FieldCommand-IMS` folder must go on **`bootfs`** because that's the drive your computer can write to — and on the Pi, that same drive shows up at the path **`/boot/firmware`**, which is where the setup command looks for it.


## If You Downloaded the ZIP from GitHub — Rename It

If you got the FieldCommand software by downloading it as a **ZIP** file from GitHub (the website where the source code lives), there's one small thing to fix. GitHub packs the download so that, when you unzip it, the folder comes out named **`FieldCommand-IMS-main`** — with a `-main` on the end. The setup command in the next chapter looks for a folder named exactly **`FieldCommand-IMS`**, without the `-main`.

1. Unzip the downloaded file (on Windows, right-click → Extract All; on macOS, double-click it).
2. You'll see a folder named **`FieldCommand-IMS-main`**.
3. Rename that folder to **`FieldCommand-IMS`** — remove the `-main` from the end (right-click → Rename).
4. Now copy that renamed **`FieldCommand-IMS`** folder onto the `bootfs` drive as described above.

> **OPTIONAL — DROP IN A fieldcommand.conf FOR HANDS-OFF SETUP** — If you want the next chapter's setup to run without asking you any questions (handy when you're building several identical servers), you can fill in a small text file named **`fieldcommand.conf`** ahead of time and copy it onto **`bootfs`** right alongside the `FieldCommand-IMS` folder. A ready-to-edit sample lives inside the `scripts` folder. This is completely optional — skip it and the setup simply asks its questions on screen instead. The next chapter covers the file in full.


## The Shortcut — If the Pi Will Have Internet

Copying the folder onto the card is the method that needs **no internet on the Pi at all** — ideal for a field build. But if your Pi will be plugged into the internet when you set it up, there's an even shorter path: skip copying the folder entirely, and let the Pi download FieldCommand itself with a single command once it boots. You'd flash the card exactly as above (still setting the username to `fieldcommand`), leave the folder off, and run one line on the Pi. The next chapter shows that one-line command. Pick whichever fits: copy-the-folder for offline, or the one-liner for online — you don't need both.


## Put the Card in the Pi and Power On

1. Make sure you've safely ejected the card from your computer, so nothing was left half-copied.
2. Slide the microSD card into the **Raspberry Pi 5**'s card slot (on the underside edge of the board). It clicks in; the metal contacts face the board.
3. Connect a **monitor** to one of the Pi's micro-HDMI ports and a **USB keyboard** (a mouse too, for the Desktop edition).
4. Plug in the Pi's **USB-C power supply** last. The Pi powers on the moment it has power — there's no separate power button.
5. Watch the monitor. The Pi boots into Raspberry Pi OS the first time, which takes a couple of minutes. When it settles onto the desktop (or a text login prompt for Lite), you're ready for the next chapter.

> **WHAT COMES NEXT** — That's the whole card-preparation job. The next chapter, **The One-Command Setup**, is where the Pi actually becomes a FieldCommand server — you open a terminal, run a single command, answer a few short questions, and it builds everything by itself.


## Troubleshooting

- *The `bootfs` drive never appeared after flashing.* Eject the card and re-insert it — the drive often shows up on the second mount. On Windows, `bootfs` sometimes appears without a drive letter; open Disk Management, find the small FAT partition on the card, and assign it a letter. Make sure you're looking at the **small** partition (`bootfs`), not the large `rootfs` one, which Windows and macOS can't read at all.
- *I can't open or see the big part of the card (`rootfs`).* That's expected and not a problem. `rootfs` is the Linux part of the card and Windows and macOS deliberately can't read it. You only ever need the small `bootfs` drive on your computer.
- *The setup later can't find the FieldCommand files.* The most common cause is the **username** wasn't set to exactly `fieldcommand`, or the folder is named `FieldCommand-IMS-main` instead of `FieldCommand-IMS`. Re-flash with the username `fieldcommand`, and make sure the folder on `bootfs` is named `FieldCommand-IMS` with no `-main`.
- *The Pi shows nothing on the monitor / won't boot.* Power off and re-seat the microSD card firmly — a card not fully clicked in is the usual cause. Confirm the monitor cable is in a **micro-HDMI** port on the Pi (the small one), and that you flashed a **64-bit** Raspberry Pi OS. If the card is old or off-brand, try flashing a fresh name-brand card.
- *The Imager can't see my card under "Choose Storage."* Check the card is fully seated in the reader, try a different USB port or reader, and make sure the card isn't locked (some full-size SD adapters have a tiny lock switch on the side — slide it away from "Lock").
- *Writing the card fails partway through.* This is almost always a failing or counterfeit card. Try a different, name-brand microSD card. Re-download the Imager if the problem repeats across cards.


# 4. The One-Command Setup — Build the Server

*The single command that turns a freshly-imaged Raspberry Pi into a finished FieldCommand server — it builds the mirrored drives, copies the operating system, reboots, and installs and configures everything for you.*

> **QUICK VERSION** — On the Pi, open a terminal and run **`sudo bash fieldcommand-setup.sh`**. Answer a few short questions (callsign, location, Wi-Fi, a couple of options), type **YES** when it asks to erase the two drives, and walk away. It builds the mirrored drives, reboots into them, and installs and configures FieldCommand IMS by itself. When it's done, do the **pull-a-drive test** in the next chapter.


## What This Is / What It Is For

In the previous chapters you imaged a microSD card and put the FieldCommand software where the Pi can find it. This chapter is where the server actually gets built. Instead of a dozen fiddly manual steps — partitioning drives, creating the mirror, copying the operating system, editing boot files, installing packages — **one command does all of it**. You run it once, answer a few questions at the start, confirm the drive erase, and it runs hands-off from there.

The command is a script named **`fieldcommand-setup.sh`**. It lives in the **`scripts`** folder of the FieldCommand software. Everything it does is described below in plain language so you know exactly what is happening and why — but you do not have to understand any of it to use it. You just run it and answer the prompts.

> **WHO DOES THIS** — This is a one-time job done by whoever is building the server — one person, at a workbench, before the equipment goes to the field. Everyone else just connects to the finished server over Wi-Fi (they never touch this).


## What the One Command Does, Start to Finish

From the single command, the setup works through five things in order. You do not run these separately — they are listed so you can follow along on screen and know what each stage means:

| Stage | What it does | Why it matters |
| --- | --- | --- |
| **Bring the bootloader up to date** | Updates the Pi's low-level start-up firmware to a known-good version. | Booting a Pi 5 from mirrored drives depends on recent firmware. Doing this on every unit removes the most common reason one drive isn't seen. |
| **Stage 0 — See both drives** | Makes sure the Pi can see **both** solid-state drives (SSDs) behind the enclosure's expansion board. If it can't, it adds two settings and reboots once. | The mirror needs two drives. This stage guarantees both are visible before anything is erased. |
| **Stage 1 — Pick the drives & confirm** | Shows you the two drives it will use and waits for you to type **YES**. | This is the safety pause. Nothing is erased until you confirm the exact drives. |
| **Stage 2 — Build the mirror & copy the OS** | Partitions and formats both drives, creates the RAID 1 mirror, copies the running operating system onto it, and points the Pi at the mirror to boot from. | This is the heavy lifting — the part that would take many careful manual steps by hand. |
| **Reboot & finish** | Reboots into the mirrored drives and, on that first boot, automatically installs and configures FieldCommand IMS with your answers. | You end up with a fully installed, fully configured server — not just a mirror. |

> **"RAID 1" AND "MIRROR" MEAN THE SAME THING HERE** — A **mirror** (the technical name is **RAID 1**) means two drives holding an identical copy of everything, kept in step automatically. If one drive fails, the other keeps running with all your data. The next chapter covers how to prove that actually works. For now, just know that's what the setup is building.


## How You Answer Its Questions — Two Ways

The setup needs a handful of answers: your callsign (or none), your location, the Wi-Fi name and password, and a couple of data options. You can provide them **either** way:

- *On screen (interactive).* You just run the command and it asks each question in turn, showing a sensible default in brackets. Press Enter to accept a default, or type your own answer. This is the normal way and needs no preparation.
- *From a file (unattended).* You fill in a small text file named **`fieldcommand.conf`** ahead of time and the setup reads your answers from it, asking nothing on screen. This is ideal when you're building several identical servers. The next chapter covers this file in full.

> **THE CALLSIGN IS OPTIONAL — ON PURPOSE** — When it asks for a **station callsign**, you can leave it blank. Do that if your group has no licensed amateur-radio operators — FieldCommand works fully without it and simply keeps the Amateur Radio tools switched off. Only enter a callsign if you have a properly licensed operator with privileges on the bands and modes you intend to use. You can always add one later in the Setup screen.


## Running It — The Exact Command

On the Pi (with a monitor and keyboard connected, booted from the microSD card), open a **Terminal** window and type this one line, then press Enter:

```
sudo bash /boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh
```

The word **`sudo`** means "do this as the administrator" — it may ask for your password the first time. If you copied the FieldCommand folder somewhere else, point the command at wherever the `scripts` folder actually is. That's the whole thing. From here it prints what it's doing as it goes, in plain, labeled steps.

> **IF THE PI HAS INTERNET, THERE'S AN EVEN SHORTER WAY** — Instead of copying the FieldCommand folder to the card first, you can have the Pi download it and launch the same setup with a single line:

`curl -fsSL https://raw.githubusercontent.com/KE4CON/FieldCommand-IMS/main/scripts/bootstrap.sh | sudo bash`

This needs the Pi to be online. The copy-the-folder method above needs no internet at all — pick whichever fits your situation.


## See What It Would Do First — The Dry Run

If you'd like to watch the whole process print out **without changing anything**, add **`--dry-run`** to the end of the command:

```
sudo bash /boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh --dry-run
```

In dry-run mode it announces every action it would take — which drives it would erase, what it would install — but touches nothing. It's a safe way to preview the run and confirm it sees both of your drives before you commit. When you're satisfied, run it again without `--dry-run` to do it for real.


## The Safety Pause — Confirming the Erase

Building a mirror means **completely erasing both solid-state drives**. The setup will not do this quietly. When it reaches Stage 1 it stops, lists the two exact drives — by size, model, and serial number — and prints:

```
The following drives will be COMPLETELY ERASED:
Type YES (all caps) to erase these two drives and build the mirror:
```

Nothing is erased until you type **`YES`** in capital letters and press Enter. Anything else — a lowercase "yes", a stray keypress, closing the window — cancels safely and leaves the drives untouched. Read the two drives it lists and make sure they're the ones you mean to wipe.

> **BOTH DRIVES ARE ERASED — CHECK BEFORE YOU TYPE YES** — This step erases everything on both SSDs. That's expected — they're brand-new blank drives in a normal build — but if there's any chance one of them holds data you want, stop and copy it off first. The microSD card is not touched, so a mistake here never harms the card you booted from.


## What Happens After It Reboots

Once the mirror is built and the operating system is copied over, the setup reboots the Pi **into the mirrored drives**. On that very first boot it runs the FieldCommand installer automatically — installing the web server, the maps, the offline data you asked for, and writing your configuration — with no further input from you. You'll see it work through the install on screen and finish on its own.

When it's done you have a complete, configured FieldCommand server running from a fault-tolerant mirror. There is exactly **one** thing left that only you can do by hand: the **pull-a-drive test**, which proves the mirror actually protects you. That's the whole of the next chapter — don't skip it.

> **A MIRROR YOU HAVEN'T TESTED IS A MIRROR YOU CAN'T TRUST** — The setup builds the mirror, but only pulling a drive with the power off and watching the server come back up on the remaining drive proves it works. It takes ten minutes and it is the entire point of having two drives. The next chapter walks you through it.


## It Turns On Secure HTTPS For You

As part of the automatic install, the setup also switches the server over to **secure HTTPS** — the same kind of encrypted connection your bank's website uses, shown by a **padlock** in the browser. You do not do anything for this: it creates the security certificate and configures the web server on its own. From then on the tools are served at **`https://192.168.50.1`** (note the **`s`**), and if anyone types the plain `http://` address the server automatically sends them to the secure one. This keeps operator and member information encrypted as it crosses the Wi-Fi, instead of traveling in plain readable text.

By default the certificate comes from a small private **Certificate Authority (CA)** that lives on the FieldCommand server itself — a trusted "stamp" that vouches for the server. There is **one** small, one-time step per device to make the padlock look completely clean: installing that stamp (a file named **`fieldcommand-ca.crt`**) on each phone, tablet, or computer. The connect chapter walks through it in plain steps; it takes under a minute and you only ever do it once per device.

> **A SIMPLER "SELF-SIGNED" MODE, IF YOU PREFER** — If you would rather not distribute a certificate file to each device, you can build the server so it signs its own certificate instead. Run the setup with **`TLS_SELF_SIGNED=1`** in front of the command. There is then nothing to install on any device — but each device shows a one-time **"not secure"** warning that a person taps through to accept the first time they connect. It is a trade-off: the default (private CA) needs a one-time file on each device but then looks perfectly clean; self-signed needs no file but shows that first-time warning. Either way the connection is fully encrypted. The connect chapter covers both.


## Troubleshooting

- *It says "Fewer than two NVMe drives are visible" and reboots.* That's normal on the first run — it just switched on the setting that lets the Pi see both drives, and it needs one reboot to take effect. After the reboot, run the same command again; your earlier answers were saved, so it picks up where it left off and moves on to the erase confirmation.
- *After that reboot it still sees only one drive.* This is a hardware seating issue, not a software one. Power off, re-seat both SSDs firmly in their slots, check the enclosure's ribbon cable is fully home, then run the command again.
- *It says the system is "already running from a RAID array."* The mirror is already built — setup has been done on this Pi. You don't need to run it again. If you truly want to rebuild from scratch, that's a deliberate wipe-and-start-over, not a re-run.
- *It says it's "running from NVMe, not the microSD card."* You booted from the solid-state drives instead of the card. Power off, make sure the microSD card is inserted, and boot from it to build the mirror.
- *"Could not gain administrator rights."* Run it with `sudo` at the front exactly as shown above. On a brand-new Pi, the first `sudo` command may ask for the password you set when you imaged the card.
- *I want to stop partway through.* Before you type YES to the erase, you can cancel anything safely — nothing has been changed yet. Press Ctrl+C to stop. After the erase begins, let it finish; if it's interrupted, re-run it and let it rebuild the mirror cleanly.


# 5. Unattended Setup — The fieldcommand.conf File

*An optional little text file that answers all of the setup's questions ahead of time, so the one-command build runs with nothing to type on screen — perfect for stamping out several identical servers.*

> **QUICK VERSION** — Copy **`fieldcommand.conf.sample`** to a plain text file named **`fieldcommand.conf`**, fill in your values, and drop it on the SD card's boot partition (so it lands at **`/boot/firmware/fieldcommand.conf`**). Run the setup as usual — it finds the file, asks **nothing**, and builds the server from your answers. Anything you leave out of the file is either asked on screen or takes its normal default. This is optional; skip the whole chapter if you're happy answering the questions live.


## What This Is / What It Is For

In the previous chapter, the one-command setup asked you a handful of short questions on screen — your callsign, your location, the Wi-Fi name and password, and a couple of data options. That's the normal way, and for a single server it's perfectly fine. But there's a second way: you can write those answers into a small text file **ahead of time**, and the setup will read them straight from the file and ask you **nothing**. This is called an **unattended** (or **hands-off**) setup.

The file is named **`fieldcommand.conf`**. It is completely **optional** — the setup works fine without it. You'd bother making one for two reasons: you're building **several identical servers** and don't want to type the same answers over and over, or you want every unit configured **exactly** the same way with no chance of a typo on screen. Fill the file in once, copy it to each SD card, and every build comes out identical.

> **YOU DON'T NEED THIS FILE** — If you're building just one server, or you're happy pressing Enter through the questions, you can ignore this chapter entirely. The config file is a convenience for repeat builds and identical fleets — not a requirement. Everything it does, the on-screen questions do too.


## Start From the Sample

You don't write this file from a blank page. The FieldCommand software ships a ready-made example named **`fieldcommand.conf.sample`** in its **`scripts`** folder. It already lists every setting, with a comment above each one explaining what it does. The easiest path is to copy that sample, rename the copy to **`fieldcommand.conf`** (drop the `.sample`), and change the values to match your group.

1. Find **`fieldcommand.conf.sample`** in the FieldCommand **`scripts`** folder.
2. Make a copy of it and rename the copy to **`fieldcommand.conf`** — the exact name matters, so type it carefully, all lowercase, no `.sample` on the end.
3. Open **`fieldcommand.conf`** in any plain text editor (Notepad on Windows, TextEdit in plain-text mode on a Mac, or a code editor).
4. Change the values on the right of each `=` sign to your own. Keep the quotation marks around each value.
5. Save the file (as plain text, not rich text), then put it in one of the locations described next.

> **SAVE IT AS PLAIN TEXT, AND KEEP THE QUOTES** — This file must be plain text. If your editor offers "Rich Text" or adds a `.txt`, `.rtf`, or `.doc` ending, the setup won't read it. On Windows Notepad, use **File ▸ Save As** and set **Save as type** to **All Files**, then name it exactly `fieldcommand.conf`. Keep the double quotes around each value (for example `AP_SSID="EMCOMM-NET"`) — they're part of the format.


## Where to Put It — the Three Locations

When the setup starts, it looks for the config file in a fixed order and uses the **first** one it finds. You only need to place it in **one** of these spots. Here they are, in the order the setup checks them:

| Order | Where | When to use it |
| --- | --- | --- |
| 1 | **Wherever `--config` points.** Run the setup with `--config /path/to/fieldcommand.conf` and it reads that exact file. | When your file lives somewhere unusual, or you keep several and want to pick one by name. |
| 2 | **On the SD card's boot partition** — it ends up at **`/boot/firmware/fieldcommand.conf`** on the Pi (older images: `/boot/fieldcommand.conf`). | The easiest for a fleet: you can drop the file onto the card from your everyday computer before the card ever goes in the Pi. |
| 3 | **Next to the setup script** — in the same folder as `fieldcommand-setup.sh` (so, `scripts/fieldcommand.conf`). | Handy if you copied the whole FieldCommand folder to the card and want the answers to travel with it. |

For most people building a batch of servers, **location 2 is the winner**: after you image an SD card, the card shows up on your computer as a small drive (the "boot" partition). Just copy `fieldcommand.conf` onto it, right alongside the FieldCommand folder, and eject. When that card boots in a Pi, the setup finds the file immediately and runs hands-off.

> **THE `--config` OPTION SPELLED OUT** — To point the setup at a file by name, add `--config` and the full path to the run command, like this:

`sudo bash fieldcommand-setup.sh --config /home/pi/fieldcommand.conf`

Substitute your real path for `/home/pi/fieldcommand.conf`. This beats every other location, so it's the surest way to be certain which file is used.


## The Golden Rule — Leave Out Anything You're Unsure Of

You do **not** have to fill in every line. The setup treats the file as a set of answers you've **already given**. For any setting you include, it uses your value and doesn't ask. For any setting you **leave out** (delete the line, or don't add it), one of two things happens:

- If you provided a config file at all, the setup runs **hands-off** and quietly uses each missing setting's **normal default** (the same default shown in brackets when you'd answer on screen).
- So a partial file is completely fine: fill in the two or three things that differ for your group (usually the location and the Wi-Fi password), leave the rest out, and the sensible defaults fill the gaps.

> **A FILE MEANS NO QUESTIONS AT ALL** — The moment the setup finds a config file, it switches to hands-off mode for the **whole** run — it will not stop to ask about a setting you left out; it uses that setting's default instead. If you want to be asked about something on screen, don't use a config file for that build (or fill the file in completely so nothing is left to chance). The one thing the setup **always** pauses for is the drive-erase confirmation in Chapter 4 — that safety stop happens no matter what, config file or not.


## Every Setting, Explained

Here is every line in the file, what it controls, what to type, and — where it matters — how much disk space and download time your choice costs. The defaults shown are exactly what you get if you leave the line out.

| Setting | What it does | Values / default |
| --- | --- | --- |
| **`PROFILE`** | How much of FieldCommand to install. **Full** installs everything (the web app plus the background radio/data services); **Server only** installs the back-end services without the web front-end; **Web only** installs just the web front-end. | `1`=Full (recommended), `2`=Server only, `3`=Web only. Default **`1`**. Leave it on `1` unless you have a specific split-role setup. |
| **`CALLSIGN`** | Your group's amateur-radio station callsign. Setting it turns **on** the Amateur Radio features; leaving it blank keeps them switched off. It's automatically made all-uppercase. | A callsign in quotes (e.g. `"KE4CON"`), or empty `""`. Default **blank**. See the callout below — blank is a valid, deliberate choice. |
| **`STATION_LAT`** | Your station's latitude in decimal degrees. Used for the map, weather, and sunrise/sunset times. | A number in quotes, e.g. `"42.3153"`. Default **`42.3153`**. Positive for north. |
| **`STATION_LON`** | Your station's longitude in decimal degrees. Same uses as latitude. | A number in quotes, e.g. `"-88.4473"`. Default **`-88.4473`**. Note the **minus sign** for west. |
| **`AP_SSID`** | The name of the Wi-Fi network the field devices join (broadcast by the router). This is the network operators see and connect to. | A network name in quotes. Default **`EMCOMM-NET`**. Leave it as-is unless your group standardizes on a different name. |
| **`AP_PASS`** | The password for that Wi-Fi network. Everyone who connects types this once. | A password in quotes. Default **`fieldcommand2026`**. **Change this** to your own before a real deployment. |
| **`SERVER_IP`** | The fixed network address the Pi serves the FieldCommand app on. This is the address operators type into their browser. | An address in quotes. Default **`192.168.50.1`**. Leave it alone unless you know your network needs a different address. |
| **`DO_FCC`** | Whether to download the full Federal Communications Commission (FCC) amateur-radio license database during install, so you can look up any US callsign offline. | `y` or `N`. Default **`N`**. Costs about **600 megabytes (MB)** of download and disk — say `y` only if you want offline callsign lookups. |
| **`TILE_PRESET`** | How much of the offline **map** to install. Higher tiers cover more area at higher detail, so the map still works with no internet. Bigger tiers take longer to download and use more disk. | `0`=skip · `1`=essential (~8 MB) · `2`=standard (~180 MB) · `3`=full (~1.6 gigabytes, GB). Default **`1`**. |
| **`KIWIX_TIER`** | How much of the offline **reference library** (Kiwix — offline copies of Wikipedia, medical and survival references, and similar) to install. Higher tiers include more material. This is the biggest space user of them all. | `0`=skip · `1`=essential (~2.5 GB) · `2`=extended (~10 GB) · `3`=full (~25 GB). Default **`1`**. |

> **PLAN FOR THE DOWNLOAD SIZE AND TIME** — The three data options — `DO_FCC`, `TILE_PRESET`, and `KIWIX_TIER` — decide how long the install takes and how much of the drive it fills. The essentials (`TILE_PRESET="1"` and `KIWIX_TIER="1"`) are a light ~10 MB of maps and ~2.5 GB of library — quick, and enough for a first build. The full tiers together pull down well over 25 GB and need a solid internet connection and patience. If you're on a slow or metered connection, start with the essentials; you can always add more later. These downloads happen after the reboot, during the automatic install.


## The Callsign Line Can Be Empty — On Purpose

The **`CALLSIGN`** line is the one setting people most often wonder about. Leaving it blank is not a mistake or an oversight — it's a supported choice, and for many groups it's the correct one.

> **LEAVE THE CALLSIGN BLANK IF YOU HAVE NO LICENSED HAMS** — If **no one in your group is a licensed amateur-radio operator**, set `CALLSIGN=""` (empty quotes). FieldCommand then works fully and simply keeps the **Amateur Radio** tools switched off, so you only see the features you're allowed to use. Enter a callsign **only** if you have a properly licensed operator with privileges on the bands and modes you intend to use — transmitting without a license is unlawful. You can always add a callsign later on the Setup screen (Chapter 6 of the User Manual) if your group licenses an operator down the road.


## A Complete Sample File

Here is a full, ready-to-edit config file. Every line is filled in with a typical value, so you can copy this, change the handful that differ for your group, and be done. Lines that begin with `#` are **comments** — friendly notes the setup ignores — so you can leave them in for reference.

```
# FieldCommand IMS — unattended setup answers

# Install profile: 1=Full (recommended), 2=Server only, 3=Web only
PROFILE="1"

# Station callsign — OPTIONAL. Leave blank ("") if no amateur operators.
CALLSIGN=""

# Station location (decimal degrees). Used for weather, maps, sunrise/sunset.
STATION_LAT="42.3153"
STATION_LON="-88.4473"

# WiFi network the field devices connect to.
AP_SSID="EMCOMM-NET"
AP_PASS="fieldcommand2026"

# Static IP the Pi serves the app on.
SERVER_IP="192.168.50.1"

# Download the FCC amateur database during install? (~600 MB)  y or N
DO_FCC="N"

# Offline map tiles: 0=skip, 1=essential(~8MB), 2=standard(~180MB), 3=full(~1.6GB)
TILE_PRESET="1"

# Kiwix offline library: 0=skip, 1=essential(~2.5GB), 2=extended(~10GB), 3=full(~25GB)
KIWIX_TIER="1"

# ── Advanced (optional) — leave commented for automatic drive selection ──
#FC_SSD_A="/dev/nvme0n1"
#FC_SSD_B="/dev/nvme1n1"
```


## The Advanced Drive Settings (Almost Everyone Skips These)

At the bottom of the sample you'll see two lines that start with `#` — **`FC_SSD_A`** and **`FC_SSD_B`**. Because they begin with `#`, they're **switched off** (commented out), and that's how they should stay for nearly every build.

Normally the setup finds your two solid-state drives (SSDs) by itself and mirrors them — you don't have to name them. These two lines exist only for the rare case where you need to **force** exactly which two drives become the mirror (for example, if a Pi has more than two drives attached and the automatic pick isn't what you want). To use them, you'd remove the `#` from the front of each line and put in the correct device names. If you don't recognize what a device name like `/dev/nvme0n1` means, that's a sure sign you should leave these lines commented out and let the setup choose.

> **DON'T UNCOMMENT THESE UNLESS YOU'RE SURE** — Forcing the wrong two device names here points the mirror-build at the wrong drives. For a standard two-SSD FieldCommand server, leave `FC_SSD_A` and `FC_SSD_B` commented out (with their `#`) and let the setup detect the drives automatically — it's the safe, tested path.


## Troubleshooting

- *The setup still asks me questions on screen — it didn't find my file.* The setup only goes hands-off when it finds the file. Check three things: the name is exactly `fieldcommand.conf` (all lowercase, no `.txt` or `.sample` on the end — Windows sometimes hides file endings, so turn on "file name extensions" in Explorer to be sure); the file is in one of the three locations (on the SD boot partition it should sit at `/boot/firmware/fieldcommand.conf`); and you saved it as plain text. To remove all doubt, pass it by name: `--config /full/path/to/fieldcommand.conf`.
- *It found the file but a setting didn't take effect.* Most often the line was misspelled, or the quotes or the `=` were dropped. Each line must read `KEY="value"` exactly — for example `SERVER_IP="192.168.50.1"`. Compare your line against the sample. Also remember the setting names are case-sensitive: it's `AP_SSID`, not `ap_ssid`.
- *I left a line out and it used a value I didn't want.* A left-out line takes its **default** (the value shown in the table above). If you want a different value, add the line back and set it. If you want to be asked on screen instead, don't use a config file for that build.
- *My callsign didn't turn the ham features on.* Make sure `CALLSIGN` has a real callsign inside the quotes, e.g. `CALLSIGN="KE4CON"`, not empty quotes `""`. An empty value deliberately keeps the Amateur Radio tools off.
- *The install ran but skipped the maps or library I wanted.* You likely left `TILE_PRESET` or `KIWIX_TIER` at `0` (skip) or `1` (essential). Set them to `2` or `3` for more, remembering the larger tiers are big downloads (up to ~1.6 GB of maps and ~25 GB of library) that need a good internet connection.
- *It went hands-off but I wanted to answer one question live.* A config file makes the **whole** run hands-off — there's no per-question opt-out. Either fill the file in completely, or don't use a file for that build and answer everything on screen. Either way, the drive-erase confirmation still stops and waits for you to type `YES`.


# 6. The Mirror & the Pull-a-Drive Test

*What the one-command setup quietly built for you — two solid-state drives holding identical copies of everything — and the ten-minute test that proves it will actually save you when a drive dies.*

> **QUICK VERSION** — The setup built a **mirror** — two drives keeping an identical copy of everything, so the server survives one drive dying. Prove it works: power off, pull the microSD card and **one** drive, power on — it must boot and FieldCommand must come up on the one remaining drive. Power off, swap which drive is out, power on — it must boot on the other alone. Then power off, put both back, power on, and re-add the drive that was out with **`sudo mdadm /dev/md0 --add <that drive's p2>`**, watching **`cat /proc/mdstat`** rebuild. If it passes both pulls, your mirror is real.


## What This Is / What It Is For

In the previous chapter, the one-command setup did a lot of work you never had to watch: it built a **mirror** across two solid-state drives, copied the whole operating system onto it, told the Pi to start up from those drives, and set an installer to run itself the first time the mirror booted. This chapter has two parts. First, a plain-language tour of what all that means. Second — and this is the part **only you can do** — the **pull-a-drive test**, the short, hands-on check that proves the mirror will actually protect the server when a real drive fails one day in the field.

You do not need to understand the technical machinery to run the test — the steps are printed for you at the end of the setup, word for word, and repeated here with an explanation of each one. But read the first half so you know **why** you're pulling drives out of a working server: it feels wrong the first time, and it isn't.

> **WHO DOES THIS** — This is the last job of the person building the server, done once at the workbench before the equipment ever goes to the field. It takes about ten minutes. Everyone else just uses the finished, tested server — they never see any of this.


## What a Mirror Is, and Why It Protects You

A **mirror** — the formal name is **Redundant Array of Independent Disks level 1 (RAID 1)** — means two drives that hold an **identical copy of everything**, kept in step automatically. Every time the server writes a file, it writes it to **both** drives at the same moment. The two drives are always the same, byte for byte.

Here is why that matters. A **solid-state drive (SSD)** — the small, fast storage card the server keeps its data on — is reliable, but nothing lasts forever. Drives fail without warning, usually at the worst time: during an activation, in the field, far from a spare. On an ordinary single-drive computer, a dead drive means the whole system stops and everything on it is gone. During a real incident, that is a disaster.

With a mirror, one drive can die completely and **the server keeps running on the other one**, with every incident record, form, map, and setting intact. Nobody at the incident even needs to know it happened. You replace the dead drive later, at your leisure, and the mirror copies everything back automatically. That is the entire reason FieldCommand is built on two drives instead of one: so a single hardware failure is a shrug, not an emergency.

> **A MIRROR IS NOT A BACKUP** — A mirror protects you from a **drive dying**. It does not protect you from someone deleting the wrong file, or from a mistake being copied — because whatever happens gets written to both drives at once. A mirror keeps the server **running** through a hardware failure; it is not a substitute for keeping backup copies of your important data somewhere else. Both are worth having, and they do different jobs.


## What the Setup Built in Stage 2

During Stage 2 of the one-command setup (the "heavy lifting" stage), four things happened. You don't run any of these yourself — the setup did all of it — but knowing what each one means helps you understand what the pull-a-drive test is checking:

| What the setup built | In plain language | Why it matters |
| --- | --- | --- |
| **The RAID 1 mirror across both SSDs** | It joined the two drives into one mirrored pair so they always hold the same thing. | This is the fault tolerance itself — the thing that lets one drive fail without stopping the server. |
| **A copy of the running operating system onto the mirror** | It copied the entire working system — the operating system (OS), the FieldCommand software, everything — from the microSD card onto the mirrored drives. | The server now lives on the fault-tolerant mirror, not on the single card. The card was only ever the starting point. |
| **A new boot order — drives first, card as fallback** | It told the Pi 5 to start up from the fast solid-state drives first, and to fall back to the microSD card only if the drives can't be used. | Day to day, the Pi runs entirely from the mirror. The card sits there quietly as a safety net (more on this below). |
| **A one-time first-boot installer** | It set up a service that runs the FieldCommand installer **automatically, exactly once**, the first time the mirror boots — then switches itself off so it never runs again. | You got a fully installed, fully configured server with no extra steps — and no risk of it re-installing on every reboot. |

> **"RAID 1," "MIRROR," AND "THE ARRAY" ALL MEAN THE SAME THING** — You'll see three names for the same object. A **mirror** is the everyday word. **RAID 1** is the technical name (Redundant Array of Independent Disks, level 1). **The array** — and its system name **`/dev/md0`** — is how the Pi refers to the mirrored pair internally. When the test tells you to type `/dev/md0`, that is simply "the mirror."


## Why the SD Card Is Kept as a Fallback

You might expect the setup to erase the microSD card once the server moves onto the mirror. It deliberately does not. The Pi's start-up order is set to try the solid-state drives **first**, and fall back to the card only if the drives can't start the system. Leaving a working card in the slot means that even in a strange failure the Pi has one more way to come up.

That fallback is exactly why the first thing the pull-a-drive test tells you to do is **remove the microSD card**. If you left it in, the Pi might quietly boot from the **card** instead of the mirror — and you'd learn nothing about whether the mirror works. Pulling the card forces the Pi to prove it can run on a single remaining drive, with no safety net.


## Why the Pull-a-Drive Test Is Non-Negotiable

The setup **builds** the mirror. It cannot **prove** the mirror works — and the gap between those two things is exactly where field disasters hide. A mirror can be built correctly on paper and still fail to boot on one drive because of a firmware quirk, a loose cable, a drive seated a hair short, or a boot file that didn't copy to the second drive. The only way to know is to actually pull a drive out, with the power off, and watch the server come back up without it.

This is a small amount of work for an enormous amount of confidence — about ten minutes at the bench. In return you get the certain knowledge that when a drive dies during a real activation, the server will keep running exactly as designed, because you already watched it do so.

> **A MIRROR YOU HAVE NOT TESTED BY PULLING A DRIVE IS A MIRROR YOU CANNOT RELY ON.** — This is the single most important sentence in the whole installation. An untested mirror gives you a false sense of safety — you **think** you're protected, so you don't keep other backups, and then the one time it matters, the mirror doesn't come up and you've lost everything. Do not skip this test. Do not do it "later." Do it now, on the bench, before this server ever goes to an incident.


## The Pull-a-Drive Test — Step by Step

When the setup finishes building the mirror, it prints these exact instructions on screen before it reboots. They are reproduced here word for word, with an explanation of what you should see at each stage. You'll need to reach the drives, so have the Pi somewhere you can safely power it off and get at the two SSD slots.


### Part 1 — Boot on one drive alone

1. Shut the server down cleanly: open a terminal and run **`sudo poweroff`**, and wait for the Pi to fully power down.
2. Remove the **microSD card** AND **one** of the two SSDs. (It doesn't matter which SSD you pull first — call the one you removed "drive A.")
3. Power the Pi back on.
4. Watch it start up. **The Pi must boot and FieldCommand must come up on the remaining SSD alone** — the one drive you left in ("drive B"). Give it a minute; a mirror running on one drive can take slightly longer to start.
5. Confirm FieldCommand is actually working: from another device on the Wi-Fi, open the server address in a browser and check the dashboard loads normally. It should look and behave exactly as it did with both drives in.

> **WHAT YOU JUST PROVED** — The server booted and ran with drive A completely gone. That is the failure you're protecting against — a dead drive — and you just watched the server shrug it off. But you've only tested **one** of the two drives so far. A mirror that boots on drive B but not on drive A is still a broken mirror, so keep going.


### Part 2 — Boot on the other drive alone

1. Shut the server down again with **`sudo poweroff`** and wait for it to fully power off.
2. **Swap which SSD is out**: put drive A back in, and take drive B out. (Leave the microSD card out for this part too.) Now the server has only the drive that was **removed** during Part 1.
3. Power the Pi back on.
4. Again, **it must boot on the other drive alone** — this time on drive A. Wait for it, then confirm the FieldCommand dashboard loads from another device just as before.

> **BOTH PULLS MUST PASS — NOT JUST ONE** — You have to see the server boot on **each** drive by itself, because a mirror is only as good as its weakest half. If it boots fine on drive A but won't come up on drive B (or the other way around), the boot files didn't make it onto both drives correctly, and the mirror will not save you if the wrong drive is the one that dies. See Troubleshooting below before you trust it.


### Part 3 — Put both drives back and rebuild the mirror

You've now proven the server boots on either drive alone. The last part puts the mirror back together. Because you ran the server on one drive at a time, the drive that was **out** is now behind — it missed whatever changed while it was removed. You tell the mirror to catch that drive back up:

1. Shut the server down one more time with **`sudo poweroff`**.
2. **Reinsert both SSDs** and reinsert the **microSD card**, so everything is back the way it started.
3. Power the Pi on and let it boot normally.
4. Re-add the drive that was out to the mirror. Open a terminal and run: **`sudo mdadm /dev/md0 --add <that drive's p2>`** — replacing `<that drive's p2>` with the second partition of the drive you're re-adding (for example `/dev/nvme1n1p2`). See the Troubleshooting note below on finding the right `p2`.
5. Watch the mirror rebuild by running: **`cat /proc/mdstat`**. You'll see a progress bar and a percentage climbing toward 100%. When it finishes, both drives are identical again and the mirror is whole.

```
sudo mdadm /dev/md0 --add /dev/nvme1n1p2
cat /proc/mdstat
```

The rebuild runs in the background — you can keep using the server while it works, and it survives a reboot if you shut down before it finishes. Once **`cat /proc/mdstat`** shows both drives in sync with no recovery percentage, the pull-a-drive test is complete and your mirror is proven. The server is ready for the field.

> **DO A DRY RUN OF THE REAL THING** — This test is also a rehearsal for the day a drive really fails. If a drive dies during an activation, the recovery is exactly Part 3: power off, fit a fresh drive, power on, run the same **`sudo mdadm /dev/md0 --add …`** command, and let it rebuild. Because you practiced it here on the bench, you'll know exactly what to do when it counts.


## Troubleshooting

- *The Pi won't boot at all with one drive out.* First make sure you actually removed the **microSD card** as well — if the card is still in, the Pi may boot from the card instead of testing the mirror, which defeats the test. If the card is out and the Pi still won't start on the single drive, the boot files likely didn't copy to that drive correctly. Power off, put **both** drives back in (and the card), boot normally, and re-run the one-command setup so it rebuilds the mirror cleanly — then test again.
- *It boots on one drive but not the other.* This is the same problem as above, seen from the other side: the boot files made it onto one drive but not both. Don't trust the mirror. Put both drives back, boot normally, and re-run the setup to rebuild, then repeat the pull test until **both** single-drive boots succeed.
- *The rebuild seems stuck / it's taking a very long time.* A rebuild copies the whole drive, so it genuinely takes a while — often many minutes. Run **`cat /proc/mdstat`** again: if the percentage is still climbing, even slowly, it's working — just be patient. If it truly hasn't moved at all after a good while, run **`sudo mdadm --detail /dev/md0`** to check the array's state, and see the array-health note below.
- *I don't know which partition is the drive's "p2."* Each SSD is split into two partitions. The **first** (`p1`, the small one) is the boot partition; the **second** (`p2`, the large one) is the part that belongs to the mirror. So the mirror partition is always the drive's name followed by **`p2`** — for the first drive that's **`/dev/nvme0n1p2`**, and for the second it's **`/dev/nvme1n1p2`**. To see the drives and their partitions plainly, run **`lsblk`**: it lists each drive with its `p1` and `p2` underneath. Add the **`p2`** of whichever drive you pulled.
- *How do I check the mirror's health at any time?* Two commands tell you everything. **`cat /proc/mdstat`** gives a quick one-look summary — you want to see both drives listed as `[UU]` (both Up), and no rebuild percentage running. **`sudo mdadm --detail /dev/md0`** gives the full report: look for **State: clean** or **active**, and **both** devices shown as `active sync`. If either command shows a drive as `removed`, `faulty`, or the state as `degraded`, the mirror is running on one drive — re-add or replace the missing drive as in Part 3.
- *After a real drive failure, what do I actually do?* Exactly Part 3 of the test: power off, remove the dead SSD and fit a healthy replacement of the same size (or larger), power on, then run **`sudo mdadm /dev/md0 --add <the new drive's p2>`** and watch **`cat /proc/mdstat`** rebuild. Because you rehearsed it on the bench, this is familiar ground, not a crisis.


# 7. Network Hardware — Router, Switch & Coverage

*The Wi-Fi router, the wired switch, and the mesh nodes that build EMCOMM-NET — the private field network everyone connects to. What each box does, how they cable together, and how to make the signal reach every corner of your building.*

> **QUICK VERSION** — One **ASUS RT-BE58 Go** router makes the **EMCOMM-NET** Wi-Fi and hands out addresses. One **UniFi Switch Lite 16 PoE** is the wiring hub — plug the router into **Port 1**, the FieldCommand Pi into **Port 2**, the 44Net gateway Pi into **Port 3**, and everything else into the ports after that. For a bigger building, add one or two more identical ASUS routers as **AiMesh nodes** (wired into switch **Ports 11 and 12**); they all broadcast the same **EMCOMM-NET** name, so devices roam without reconnecting. That's the whole network.


## What This Is / What It Is For

FieldCommand runs on its own private network with no dependence on the internet. That network is called **EMCOMM-NET** (short for **emergency communications network**), and this chapter is about the three kinds of box that build it: a **router** that broadcasts the Wi-Fi, a **switch** that ties the wired gear together, and — for larger spaces — extra routers that spread the Wi-Fi signal further. Get these three cabled correctly and every phone, tablet, and laptop in the room can reach the FieldCommand tools by opening a web browser. Nothing here requires internet; the network works completely on its own.

An important design choice sits underneath everything in this chapter: **neither Raspberry Pi runs the Wi-Fi.** The two Pi computers (the FieldCommand server and the 44Net gateway) are wired-only. All the Wi-Fi — making the signal, giving out addresses, letting devices roam — is handled by the dedicated **ASUS** router. This keeps the servers focused on serving the app and lets a purpose-built router do the job it's good at, which means a stronger, more reliable signal for everyone.

> **WHO DOES THIS** — This is a one-time bench-and-site job for whoever builds and deploys the kit. You cable it once, and from then on operators simply join the **EMCOMM-NET** Wi-Fi and start working. The next chapter covers exactly how a device connects and how addresses are assigned.

> **A NOTE ON WHERE THE INTERNET COMES FROM** — EMCOMM-NET runs fine with no internet at all. If you do want an upstream connection for the features that use it, the primary source is a cellular modem (primary internet) with a satellite link (fallback internet) as an automatic backup, both feeding the router's WAN port. That setup has its own chapter later in this guide — this chapter is only about the local network, so we won't cover the upstream wiring here.


## The ASUS RT-BE58 Go — The Access Point and DHCP Server

The **ASUS RT-BE58 Go** is a small, travel-sized **Wi-Fi 7** router. In the FieldCommand kit it plays two roles at once, and it's worth knowing both by name:

| Role | In plain words | What it does for you |
| --- | --- | --- |
| **Access point (AP)** | The thing that makes the Wi-Fi signal | It broadcasts the **EMCOMM-NET** wireless network on both the 2.4 GHz and 5 GHz bands, so any device in range can join. |
| **Dynamic Host Configuration Protocol (DHCP) server** | The thing that hands out addresses | When a device joins EMCOMM-NET, the router automatically gives it an Internet Protocol (IP) address — its number on the network — from the pool **192.168.50.100** through **192.168.50.200**. The operator does nothing. |
| **Wide Area Network (WAN) gateway** *(optional)* | The doorway to the outside | If you connect an upstream internet source, the router routes traffic to it. This is optional and covered in a later chapter. |

You power the router over **Universal Serial Bus Type-C (USB-C)** at 18 watts — a standard phone-style adapter, or a USB-C power bank when you're running on batteries in the field. Its fast 2.5-gigabit local network (LAN) port connects to the switch. That is the whole physical footprint of the router: power in, one cable to the switch, and Wi-Fi out to the room.

> **THE ROUTER, NOT THE PI, IS THE ACCESS POINT** — If you have ever set up a Raspberry Pi to be its own Wi-Fi hotspot, forget that here. The FieldCommand Pi is a **wired client** only — it plugs into the switch with an Ethernet cable and never broadcasts Wi-Fi. All Wi-Fi comes from the ASUS router. This is deliberate: a real router gives a stronger, more reliable signal and frees the Pi to run the app.


## The UniFi Switch Lite 16 PoE — The Wiring Hub

The **UniFi Switch Lite 16 PoE** is the central wiring hub for the whole deployment. A switch is simply a box with many Ethernet sockets (ports) that lets all your wired devices talk to each other. This one has **16 gigabit ports**: **8** of them supply **Power over Ethernet (PoE)** — meaning they can send electricity down the same network cable that carries data, so a camera or a future access point needs no separate power brick — and **8** are ordinary data-only ports. It also has **2** high-speed fiber (SFP) uplink slots you won't need for a basic build. Its included 45-watt power supply runs the whole thing.

The ports are assigned to specific devices. Wiring them in this exact order keeps everyone's address predictable and makes fault-finding easy. Here is the layout:

| Port | What plugs in here | Notes |
| --- | --- | --- |
| **Port 1** | **ASUS RT-BE58 Go** router (LAN uplink) | The router's link into the wired world. All wired devices reach the internet and each other through this. |
| **Port 2** | **FieldCommand Pi 5** (the main server) | Fixed address **192.168.50.1** — every browser tool lives here. |
| **Port 3** | **44Net gateway Pi 5** | Fixed address **192.168.50.2** — the amateur-radio (AMPRNet) gateway. Optional; only if you run 44Net. |
| **Port 4** | **Windows laptop** | Winlink / JS8Call station. Can also join by Wi-Fi instead. |
| **Port 5** | **Color multifunction printer (MFP)** | The shared network printer. Can also join by Wi-Fi instead. |
| **Ports 6–9** | **Operator workstations** (up to four Pi 500s) | One workstation per port. |
| **Port 10** | **Satellite dish** *(optional)* | Only if you use a satellite upstream source. |
| **Ports 11–12** | **AiMesh nodes** (extra ASUS routers) | The wired backhaul for coverage extension — see below. |
| **Ports 13–16** | **Spare** | Room to grow — plug in anything else you bring. |

> **WHAT POWER OVER ETHERNET BUYS YOU** — The eight PoE ports carry both data and power on one cable (a 45-watt budget across them). That means devices like security cameras, extra UniFi access points, or other PoE gear can be powered straight from the switch — no separate power adapter and no outlet needed at the far end of the cable. For a basic FieldCommand build you may never use this, but it's there when you expand.


## Extending Coverage — AiMesh Nodes

One ASUS router covers a single room easily. For anything larger — a multi-room emergency operations center (EOC), a whole building, or an outdoor staging area — a single router's Wi-Fi won't reach every corner. The fix is **AiMesh**, ASUS's built-in feature for chaining identical routers together into one seamless network.

The standard FieldCommand deployment ships **three** identical ASUS RT-BE58 Go routers: **one primary** (connected to the switch and any upstream source) and **two AiMesh nodes** that repeat the signal in other areas. Because all three broadcast the **same EMCOMM-NET name (SSID)** and the same password, a phone or laptop moves from one to the next automatically — no reconnecting, no re-entering the password, no awareness of which router it's actually using. The technical term for the Wi-Fi network's name is the **Service Set Identifier (SSID)**; here it's always **EMCOMM-NET**.

> **USE WIRED BACKHAUL — RUN A CABLE TO EACH NODE** — Each mesh node connects back to the primary through the switch with a real Ethernet cable — a **CAT 6 patch cable** from a spare **UniFi switch port (11 or 12)** to the node's LAN port. This wired link between routers is called the **backhaul**. A wired backhaul is far faster and more reliable than letting the nodes talk over Wi-Fi, and it means the mesh doesn't eat into the Wi-Fi speed your operators are using. Always cable the nodes when you can.

Pairing a node takes under five minutes on site: cable it into the switch, power it up, open the primary router's **AiMesh** page, and let it adopt the node. The primary then pushes the EMCOMM-NET name, password, and settings to the node automatically. You place the node where its coverage is needed and confirm a phone still shows full signal at the farthest point.


## How Many Nodes Do I Need?

Match the number of routers to the size and shape of the space you're covering. Use this as a starting guide, then walk the far corners with a phone on EMCOMM-NET to confirm the signal holds:

| Your space | Recommended setup |
| --- | --- |
| **Single-room EOC** (under 2,500 square feet) | **1 primary router only** — no extension needed. |
| **Multi-room EOC or large shelter** (2,500–7,500 square feet) | **1 primary + 1 node** — wired backhaul via switch **Port 11**. |
| **Large building or campus** (7,500–20,000 square feet) | **1 primary + 2 nodes** — wired backhaul via switch **Ports 11 and 12**. |
| **Outdoor search-and-rescue (SAR) staging area** | **1 primary at the command post + 1–2 nodes at field positions**, each on battery power. |

> **YOU DON'T HAVE TO DEPLOY ALL THREE** — Bring what the space needs. A small activation in one room runs perfectly on the single primary router — leave the two nodes in the case. Add a node only when a phone starts dropping bars at the edge of your coverage.


## Cabling It All Together

Here is the physical build, in order. You can do this on a bench first and it will work the same way on site. Use ordinary Ethernet patch cables (CAT 6 is recommended).

1. Set the **UniFi Switch Lite 16 PoE** where it can stay — this is your hub. Plug its included **45-watt power supply** into an outlet (or your power system) and let it boot.
2. Cable the **ASUS RT-BE58 Go** router's **LAN port** to switch **Port 1**. Power the router from its **USB-C 18-watt** adapter (or a USB-C power bank in the field).
3. Cable the **FieldCommand Pi 5** to switch **Port 2**. This Pi is the main server and will live at address **192.168.50.1**.
4. If you run the amateur-radio gateway, cable the **44Net gateway Pi 5** to switch **Port 3** (address **192.168.50.2**). Skip this if you're not using 44Net.
5. Cable the rest as you need them: the **Windows laptop** to **Port 4**, the **network printer** to **Port 5**, and up to four **operator workstations** to **Ports 6–9**. Any of these can instead join over EMCOMM-NET Wi-Fi.
6. If you're extending coverage, cable each **AiMesh node** into **Port 11** (and **Port 12** for a second node), power it, and pair it from the primary router's AiMesh page.
7. Leave the upstream internet source disconnected for now — that belongs to its own chapter. EMCOMM-NET works without it.

> **WHY THIS ORDER OF PORTS MATTERS** — The switch ports are matched to fixed addresses (Port 2 → 192.168.50.1, Port 3 → 192.168.50.2, and so on). Following the layout keeps every device's address predictable, so if something ever goes quiet you know exactly which port and which address to check. The next chapter explains the addressing scheme in full.


## Troubleshooting

- *No Wi-Fi at all — I don't see EMCOMM-NET on my phone.* First confirm the **ASUS router** has power (its lights are on) and that its **LAN port is cabled to switch Port 1**. Remember the Pi does **not** make Wi-Fi, so a running Pi with a dark router still means no signal. If the router is powered and cabled but there's still no network name, it may not be configured yet — routing configuration is covered in an earlier setup step; the router must be broadcasting **EMCOMM-NET** before any device can join.
- *A device joins EMCOMM-NET but can't reach the tools.* The Wi-Fi is fine but the wired side may be broken. Check that the **FieldCommand Pi is cabled to switch Port 2** and powered, and that the **switch itself has power**. The next chapter walks through confirming a device can reach the dashboard at `http://192.168.50.1`.
- *A mesh node won't pair.* Make sure the node is **cabled into switch Port 11 or 12** (wired backhaul) and powered on, then open the **primary router's AiMesh page** and start adoption there — you pair from the primary, not from the node. Give it a minute; the primary pushes the settings automatically. If it still won't appear, power-cycle the node and try the pairing once more.
- *Coverage is weak in one part of the building.* You've outgrown a single router for that space. Add an **AiMesh node** near the weak area (see the how-many-nodes table), cable its backhaul to a spare switch port, and pair it. Walk the far corner with a phone on EMCOMM-NET afterward to confirm full bars.
- *A mesh node shows connected but everything is slow.* Check that its **backhaul is wired**, not wireless — a node repeating over Wi-Fi is much slower and eats into everyone's speed. Run a CAT 6 cable from the node's LAN port back to a spare switch port and re-check.
- *I ran out of ports.* Ports **13–16** are spare by design. If those are full too, the switch has 16 ports total — move rarely-used wired gear onto EMCOMM-NET Wi-Fi instead, which frees ports for the things that must be wired.


# 8. EMCOMM-NET & Static IP — How Everyone Connects

*The moment it all comes together for the operator: join one Wi-Fi network, open a browser, and every FieldCommand tool is there — no app, no internet, no per-device setup. This chapter explains the simple addressing behind that, and what to change (carefully) if you ever must.*

> **QUICK VERSION** — On any phone, tablet, or laptop: **(1)** join the Wi-Fi network named **EMCOMM-NET**, **(2)** open a web browser, **(3)** type **`http://192.168.50.1`** and press Go. The FieldCommand dashboard appears. That's the entire connection process — no app to install, no internet, nothing to set up on the device. It works the same for everyone, every time.


## What This Is / What It Is For

This is the chapter your operators actually live in. Everything built in the previous chapters — the server, the mirror, the router, the switch — exists so that this final step is dead simple: a person walks up with a device they already own, joins one Wi-Fi network, opens a browser, and works. No accounts, no app store, no cell signal, no fiddling. This chapter explains how that works and the small, fixed set of addresses that make it reliable.

The whole system is designed around a single promise: **if you can open a web page, you can use FieldCommand.** The tools are ordinary web pages served by the FieldCommand Pi. Any modern browser on any device — Android, iPhone, iPad, Windows, Mac, Linux — reaches them the same way. There is nothing to download and nothing to keep updated on the operator's device.

> **WHO DOES THIS** — The three connection steps are done by **every operator**, on their own device, every time they arrive — and they need no training to do it. The addressing scheme further down is set up **once** by whoever builds the server; operators never touch it.


## How Any Device Joins — Three Steps

This is the process to teach every operator. It is identical on every kind of device, so you can put it on a card by the door:

1. **Join the Wi-Fi.** Open the device's Wi-Fi settings and connect to the network named **EMCOMM-NET**. Enter the password when asked (your team sets this; the factory example is `fieldcommand2026`, which you should change for real operations).
2. **Open a web browser.** Any browser works — Chrome, Safari, Edge, Firefox. It does not matter which.
3. **Go to the server.** In the address bar type **`http://192.168.50.1`** exactly — including the `http://` at the front — and press Enter or Go. The FieldCommand dashboard loads, and the operator is working.

> **NO APP, NO INTERNET, NO PER-DEVICE SETUP** — There is deliberately **nothing to install**. FieldCommand is not an app — it's a set of web pages the server hands to your browser. It needs **no internet**, because everything runs on the local EMCOMM-NET. And it needs **no setup on each device** — the router hands out the network address automatically the moment a device joins. A brand-new phone that has never seen the system before is fully working within seconds of joining EMCOMM-NET.

Because the address is served automatically, an operator never types their own device's address or configures anything. They only ever type the **server's** address, `http://192.168.50.1`, to reach the tools. Everything else is handled for them.


## The Static IP Scheme — Who Lives Where

Every device on a network has an **Internet Protocol (IP) address** — its unique number on the network. On EMCOMM-NET, a few important machines are given **fixed** (static) addresses that never change, while everyday devices get a temporary one automatically. Fixed addresses matter because operators and other services need to always find the server at the same place. Here is the full scheme:

| Address | Who has it | Fixed or automatic? |
| --- | --- | --- |
| **192.168.50.1** | **FieldCommand server** (the main Pi) — where every tool lives; this is the address operators type | **Fixed** (static) |
| **192.168.50.2** | **44Net gateway Pi** — the amateur-radio (AMPRNet) gateway; only present if you run 44Net | **Fixed** (static) |
| **192.168.50.254** | **The ASUS router itself** — its own admin page, kept separate so the server's address stays clean | **Fixed** (static) |
| **192.168.50.100 – 192.168.50.200** | **Everyday client devices** — phones, tablets, laptops. Each gets the next free address in this pool automatically when it joins | **Automatic** (DHCP pool) |
| **192.168.50.3 – 192.168.50.23** (selected) | **Optional reserved devices** — e.g. the Windows laptop, the network printer, and workstations, when a group wants their address pinned | **Reserved** (by choice) |

> **THE POOL COMES STRAIGHT FROM THE CONFIGURATION** — The client pool **192.168.50.100–192.168.50.200** and the fact that all clients are pointed at **192.168.50.1** as their gateway and name server are set in the network's Dynamic Host Configuration Protocol (DHCP) configuration. Every device that joins is told, automatically: "your gateway is 192.168.50.1, and you're on the same 192.168.50.x network as the server." That's why a fresh device just works.

The upshot for a human: **you only ever need to remember one address — `192.168.50.1`.** That's the server, that's where the tools are, and that's the only thing anyone types.


## How the Server's Address Is Set and Served

Two small pieces of configuration make the address stable, and both are handled for you during installation. You don't have to do anything with them — this section is here so you understand what's under the hood if you ever need to look.

| Piece | What it does | Set where |
| --- | --- | --- |
| **The Pi's static IP** | Pins the FieldCommand server to **192.168.50.1** on its wired Ethernet connection, so it's always found at the same place | Set on the Pi during installation (its wired network profile) |
| **The router's DHCP + Wi-Fi** | Broadcasts the **EMCOMM-NET** name and hands every joining device an address from the **.100–.200** pool, pointed at the server | Set once on the ASUS router (earlier setup step) |

In other words, the **server** claims a fixed address, and the **router** makes sure every other device can find it. Once both are in place — which the installer arranges — the connect-in-three-steps experience simply works, activation after activation, with no further attention.


## What to Change If You Truly Must

For almost every group, the defaults — the **EMCOMM-NET** network name and the **192.168.50.1** server address — are exactly right and should be left alone. They're plain, they're memorable, and everything is already wired to expect them. But if your situation forces a change (for example, a name clash with another network on site), it is possible. Do it carefully.

> **CHANGE THE NAME OR THE ADDRESS IN BOTH PLACES, OR NOBODY CONNECTS** — The Wi-Fi network name (**SSID**) and the server address are how every operator's device finds the system. They are configured in **two** places that must agree: on the **router** (which broadcasts the name and hands out addresses) and on the **FieldCommand server** itself (its Setup screen and its static address). If you change one and not the other, they no longer match — and when they don't match, **operators cannot connect at all.** Change both, together, or change neither.

If you do change them, follow this rule: pick the new name and address, set them on the **router** first (its Wi-Fi name, and the address it expects the server to use), then set the matching values on the **server** — its static IP and the **Server Address** and **Wi-Fi Network Name** fields on the Setup screen. Then reconnect a test device to the new name and confirm the new address loads before you rely on it. If anything goes wrong, the safest move is to put both back to the defaults (`EMCOMM-NET` and `http://192.168.50.1`).

> **THE ROUTER ADMIN LIVES SEPARATELY, ON PURPOSE** — The router keeps its own admin page at **192.168.50.254**, deliberately separated from the server's **192.168.50.1**. That way the address operators type for the tools (`192.168.50.1`) stays clean and never collides with the router's settings page. Leave that separation in place.


## Trusting the Security Certificate (HTTPS)

FieldCommand serves its tools over **HTTPS** — the secure, encrypted kind of web connection, marked by a **padlock** in the browser's address bar. This is turned on automatically when the server is built (see the one-command setup chapter), so member and operator information is never sent in plain readable text across the Wi-Fi. You don't turn anything on; it's already there. The address becomes **`https://192.168.50.1`** (note the **`s`** after `http`), and if anyone types the plain **`http://192.168.50.1`** the server automatically forwards them to the secure address — so the three connection steps still work exactly as written.

There is just **one** small, one-time step per device to make the padlock look completely clean, and it depends on how the server was built:

| How the server was built | What each device does (once) | What the operator sees |
| --- | --- | --- |
| **Private local CA** (the default, recommended) | Install the server's root certificate — a file named **`fieldcommand-ca.crt`** — on the device one time. After that, the padlock is clean with no warnings, forever. | A normal, clean padlock — just like any major website. |
| **Self-signed** (built with `TLS_SELF_SIGNED=1`) | Nothing to install. The first time the device connects, tap through a one-time **"not secure" / "your connection is not private"** warning to accept it. | A one-time warning screen on the first visit, then normal use. |

> **WHAT A "CERTIFICATE AUTHORITY" IS, IN PLAIN WORDS** — A **Certificate Authority (CA)** is simply a trusted "stamp" that vouches for a server's identity, so the browser shows a clean padlock instead of a warning. FieldCommand runs its own tiny private CA on the server. Installing its root file, **`fieldcommand-ca.crt`**, on a device teaches that device to trust the FieldCommand server — and only the FieldCommand server. It gives no access to anything else and involves no internet.

Here is the one-time install of the root certificate on a device (only needed for the default private-CA build). Do this once per phone, tablet, or computer:

1. Join **EMCOMM-NET** and, in a browser, go to **`https://192.168.50.1/fieldcommand-ca.crt`**. The file **`fieldcommand-ca.crt`** downloads. (Whoever builds the server can also copy it straight from the server at **`/opt/fieldcommand/html/fieldcommand-ca.crt`** onto a USB drive to hand around.)
2. Open the downloaded file and follow the device's prompt to install or trust it. On **Windows**, double-click it, choose **Install Certificate → Local Machine → Trusted Root Certification Authorities**. On **macOS**, open it in **Keychain Access**, then set it to **Always Trust**. On **iPhone/iPad**, it installs as a **profile** in **Settings → General → VPN & Device Management**, then you switch it on under **Settings → General → About → Certificate Trust Settings**. On **Android**, use **Settings → Security → Encryption & credentials → Install a certificate → CA certificate**.
3. Reload **`https://192.168.50.1`**. The padlock is now clean, with no warning. You never have to do this again on that device.

> **THE ONE-TIME WARNING IS SAFE TO ACCEPT ON YOUR OWN NETWORK** — If your server was built in **self-signed** mode, the first-visit **"not secure"** warning is expected and harmless here. It appears only because the certificate wasn't issued by one of the big public authorities — not because anything is wrong. On your own private EMCOMM-NET, tap **Advanced** and then **Proceed / Continue** (the exact words vary by browser) to accept it once. The connection is still fully encrypted.


## Verifying a Client Can Reach the Dashboard

Before you hand the system to operators, prove it from a device you're holding — ideally one that has never touched the system, to confirm the from-scratch experience really is that simple:

1. On a phone or laptop, open Wi-Fi settings and join **EMCOMM-NET**. Watch for it to show as connected.
2. Open any web browser and go to **`http://192.168.50.1`** (type the `http://` too).
3. Confirm the **FieldCommand dashboard** loads. If it does, this device — and any device like it — is good to go.
4. *(Optional check for builders.)* Look at the device's own Wi-Fi details; its address should be somewhere in **192.168.50.100–192.168.50.200**, confirming the router handed it one from the pool.

> **MAKE IT EVEN EASIER — SET IT AS THE HOME PAGE** — On a fixed operator workstation, you can set the browser's start page to `http://192.168.50.1` so the dashboard opens the instant the browser launches — one less thing for an operator to type. On a Pi 500 workstation running Chromium, that's **Settings → On startup → Open a specific page → `http://192.168.50.1`**.


## Troubleshooting

- *I can't reach `192.168.50.1`.* First, confirm the device is actually **joined to EMCOMM-NET** (not your phone's cellular data or a different Wi-Fi). Then confirm you typed the address exactly, **with `http://` in front**. If the Wi-Fi is right and the address still won't load, the **server may be off or unplugged** — check the FieldCommand Pi has power and is cabled into switch Port 2 (previous chapter).
- *I left off the `http://` and it searched the web instead.* Some browsers treat `192.168.50.1` on its own as a search. Type the full **`http://192.168.50.1`** — with the `http://` — and it will load the page instead of searching. The server automatically forwards you to the secure **`https://`** address, so you don't have to type the `s` yourself.
- *The browser says "Not secure" or "Your connection is not private."* This is about the security certificate, not a real problem on your own EMCOMM-NET. If the server was built the default way (private CA), install the root certificate **`fieldcommand-ca.crt`** on this device once — see "Trusting the Security Certificate" above — and the warning goes away for good. If the server was built in self-signed mode, this warning is expected on each device's first visit; tap **Advanced** then **Proceed / Continue** to accept it once. The download link for the root file is **`https://192.168.50.1/fieldcommand-ca.crt`**.
- *My device got the wrong IP address.* If a device shows an address that is **not** in the `192.168.50.x` range, it probably didn't get one from the router. Turn its Wi-Fi off and on to rejoin EMCOMM-NET and pick up a fresh address from the pool. If it still gets the wrong range, it may be stuck on a different network or have a manually-set address — remove any manual IP setting so it uses **automatic (DHCP)**.
- *It works when I'm plugged in with a cable but not over Wi-Fi.* The wired side is fine, so the issue is the **Wi-Fi**. Confirm the **ASUS router** is powered and broadcasting **EMCOMM-NET**, that you joined that exact network, and that you're in range (add a mesh node if coverage is weak — see the previous chapter). Remember the Pi itself does not make Wi-Fi; the router does.
- *Everyone suddenly can't connect after someone changed a setting.* The **Wi-Fi name or server address** was very likely changed on one side but not the other. They must match in both the **router** and the **server**. Put both back to the defaults — **`EMCOMM-NET`** and **`http://192.168.50.1`** — and have everyone rejoin.
- *The page loads but looks half-broken or out of date.* Do a hard refresh in the browser (pull down to refresh on a phone, or Ctrl+F5 / Cmd+Shift+R on a computer). The server tells browsers not to cache the main pages, so a refresh pulls the current version cleanly.


# 9. Offline Map Tiles & the Kiwix Library

*Loading the two big piles of reference data onto the server before it goes to the field: the map pictures the tactical map draws from, and Kiwix — an offline copy of Wikipedia and other reference libraries you can read in a browser with no internet.*

> **QUICK VERSION** — A FieldCommand server runs with **no internet**, so its map pictures and reference books must be copied on **while you still have internet** — on the workbench, before deployment. The easy path: the one-command setup already asked you two questions — **map tiles** (`TILE_PRESET`) and the **Kiwix library** (`KIWIX_TIER`) — and downloaded what you chose. To add more later, plug the server into the internet and run **`sudo bash download_tiles.sh`** for maps or **`sudo bash kiwix_setup.sh`** for the library. Operators reach the library in a browser at the server address on port **8081**.


## What This Is / What It Is For

FieldCommand IMS (Incident Management System) is built to run where there is **no internet at all** — a parking lot, a shelter, a served agency's basement, a remote staging area. That is the whole point of it. But two of its most useful features normally depend on the internet: the **tactical map**, which pulls its map pictures from the web as you pan and zoom, and any **reference lookup** an operator might want mid-incident (a medical fact, a repair procedure, a piece of ham-radio know-how).

The fix for both is the same idea: **copy the data onto the server ahead of time, while you still have internet**, so it is sitting on the server's own drives when you get to the field. This chapter covers the two big data sets you load this way — **offline map tiles** for the map, and the **Kiwix offline library** for reference reading. You do this **once**, at the workbench, before the equipment ever leaves for an incident.

> **DO THIS WHILE YOU STILL HAVE INTERNET** — Every download in this chapter needs a working internet connection **at the time you run it**. That is fine — you are meant to do it on the bench during setup. Once the server is deployed and offline, whatever you loaded is all it has. If you are not sure how much to load, load **more** now; you cannot go back and get it in the field.

> **WHO DOES THIS** — This is a one-time job for whoever builds the server. Field operators never touch it — they just use the map and open the library in a browser. If you took the defaults during the one-command setup (Chapter 4), a starter set of both is **already loaded** and you can skip straight to the Troubleshooting section, or come back here only when you want to add more.


## Part 1 — Offline Map Tiles

The tactical map is stitched together from thousands of small square images called **tiles**. Each tile is one little piece of the map at one zoom level; the map software fits them together like floor tiles to make the picture you pan and scroll around. Online maps fetch these tiles from the internet the instant you need them. A field server can't do that — so the tiles have to already be on the server.

That is what an **offline tile download** does: it fetches the tiles for the area you care about, at the zoom levels you care about, and stores them in a file on the server. After that the map works fully offline — roads, terrain, aerial imagery, the lot — for the area you downloaded. **Outside** that area, or zoomed in **closer** than the levels you fetched, the map simply shows blank gray squares, because those tiles were never downloaded.

> **WHY THE MAP IS BLANK UNTIL YOU DO THIS** — A brand-new server has **no tiles**. If you open the map before loading any, you'll see gray squares and no roads — nothing is broken, the pictures simply aren't there yet. Load a tile preset and the area you picked fills in. This is the single most common "is it broken?" question, and the answer is almost always "no tiles were downloaded for that spot."


### The Four Tile Presets

To keep the choice simple, the setup offers four ready-made **presets**, chosen with the `TILE_PRESET` setting. Each is a bigger area and finer detail than the one before — and a bigger download. Pick based on how much of the map you need to see up close versus how much drive space and download time you want to spend.

| Preset (TILE_PRESET) | Size on disk | What it covers | Good for |
| --- | --- | --- | --- |
| **0 — Skip** | 0 | Nothing — no tiles at all | You'll load tiles later, or the map isn't needed. |
| **1 — Essential** | ~8 MB | Your home county at a wide, low-detail zoom — enough to see the county shape, major roads, and where things sit in relation to each other. | A fast, tiny download that gets a usable map on screen immediately. A fine starting point for any deployment. |
| **2 — Standard** | ~180 MB | Your county area down to street level — you can zoom in and read individual roads and neighborhoods. | The recommended everyday choice. Enough detail to actually navigate and assign sectors, still small enough to download in minutes. |
| **3 — Full** | ~1.6 GB | The widest area at the finest detail — building- and parcel-level zoom across your county and a buffer around it. | Search-and-rescue grids, damage assessment, anything where you must zoom right in. Largest download; needs the most drive space. |

> **WHAT "ZOOM LEVEL" MEANS FOR SIZE** — The reason **Full** is hundreds of times bigger than **Essential** is zoom. Each step closer in doubles the map's detail in every direction, which multiplies the number of tiles enormously. A whole state at a wide zoom is a small download; a single county at building-level zoom is a large one. The presets balance area against detail so you don't have to think about it — but that is why the sizes jump the way they do.


### The Easy Way — Let the Setup Do It

The simplest path is the one you probably already took. During the one-command setup (Chapter 4), it asked which tile preset you wanted, or read your choice from the `TILE_PRESET` line in the `fieldcommand.conf` answers file. Whatever you picked, it downloaded and stored for you as part of the build — no separate step. If you accepted the default there, your server already has a starter map and you don't need to do anything else here.

```
# From fieldcommand.conf — the setup used this automatically:
# Offline map tiles: 0=skip, 1=essential(~8MB), 2=standard(~180MB), 3=full(~1.6GB)
TILE_PRESET="1"
```


### Adding or Changing Tiles Later

You can add more map area or finer detail at any time — you are never locked into the preset you chose at build time. You just need to give the server internet again for the download. The tool is a script named **`download_tiles.sh`** in the FieldCommand `scripts` folder.

1. Connect the server to the internet (plug it into a network that has internet, or otherwise give it a connection) — the download needs it.
2. Open a terminal on the server and run **`sudo bash download_tiles.sh`** (the word `sudo` means "as administrator"; it may ask for your password).
3. A menu appears with the same Essential / Standard / Full choices, plus options to search for a specific county or state, or to type in your own area by coordinates.
4. Pick what you want. The script shows you the rough number of tiles, the download size, and about how long it will take, then asks you to confirm before it starts.
5. Let it run. It prints its progress as it goes and can be **resumed** — if it's interrupted, just run it again and it picks up the tiles it hasn't fetched yet, skipping the ones it already has.
6. When it finishes, the new area is immediately part of the offline map. Disconnect the internet again and you're ready for the field.

> **IT ONLY DOWNLOADS WHAT'S MISSING** — Running the tile download again never re-fetches tiles you already have — it only pulls the new ones. That means adding a neighboring county, or a finer zoom level, costs only the extra data, not a fresh start. It also means a stopped download is safe to simply re-run.


## Part 2 — The Kiwix Offline Library

**Kiwix** is a free program that serves **offline copies of whole websites** — you read them in an ordinary web browser exactly as if you were online, except everything is stored on the server and needs no internet. The copies come as single files called **ZIM files** (that's just the file format's name). FieldCommand can host a curated shelf of these that are useful during an incident.

Why does an incident-management server need Wikipedia? Because when the internet is down, an operator may still need to look something up: how to treat a specific injury, how to repair a generator or a radio, an evacuation or shelter detail, a piece of technical reference. Kiwix puts a small **reference library** on the server so those answers are available offline, in a browser, to anyone on the network.

> **WHAT'S ON THE SHELF** — The curated collection leans toward things that matter in the field: **WikiMed** (a full medical encyclopedia — symptoms, treatments, drugs, procedures), **Wikipedia** (compact or full), **Wikivoyage** (shelter, evacuation, and travel logistics), **Wikibooks** (first aid, survival, ham radio, electronics, field skills), **iFixit** (step-by-step repair guides for radios, computers, vehicles, generators, medical gear), and more advanced medical, training, and electronics references. You choose how much of this to load with the tiers below.


### The Three Kiwix Tiers

Just like the tile presets, the Kiwix content is grouped into simple **tiers**, chosen with the `KIWIX_TIER` setting. Each tier adds more libraries — and a lot more drive space. These downloads are **much larger** than the map tiles (whole encyclopedias), so plan your drive space accordingly.

| Tier (KIWIX_TIER) | Size on disk | What it adds | What that gives you |
| --- | --- | --- | --- |
| **0 — Skip** | 0 | Nothing — Kiwix not installed | You don't need offline reference, or you'll add it later. |
| **1 — Essential** | ~2.5 GB | Medical encyclopedia, a compact Wikipedia, and the shelter/travel guide | The core field reference: medical lookup, general facts, and evacuation/shelter logistics. The recommended starting point. |
| **2 — Extended** | ~10 GB | Everything in Tier 1, **plus** the how-to/field-manual library and the equipment-repair guides | Adds hands-on knowledge — first aid, survival, electronics, and step-by-step repair for the gear you bring. |
| **3 — Full** | ~25 GB | Everything in Tiers 1 and 2, **plus** the full medical Wikipedia, a training/education library, and an electronics Q&A archive | The complete shelf: comprehensive clinical reference, Incident Command System (ICS) and responder training, and deep electronics/radio troubleshooting. |

> **CHECK YOUR DRIVE SPACE FIRST** — **Tier 3 is about 25 gigabytes.** Make sure the server's drives have room before you start — the download tool checks free space and will stop rather than fill the disk, but it's better to plan ahead. If you're tight on space, Tier 1 (~2.5 GB) already covers the most critical need, which is offline medical reference.


### How the Setup Loads It

As with tiles, the one-command setup already handled this if you let it. It asked which Kiwix tier you wanted, or read the `KIWIX_TIER` line from your answers file, then installed the Kiwix server and downloaded the tier you chose. If you took the default, a starter library is already on the server and serving.

```
# From fieldcommand.conf — the setup used this automatically:
# Kiwix offline library: 0=skip, 1=essential(~2.5GB), 2=extended(~10GB), 3=full(~25GB)
KIWIX_TIER="1"
```


### How Operators Reach the Library

Once Kiwix is loaded, anyone on the field network can read it in a browser — no login, no special app. Kiwix serves its pages on **port 8081** of the server. "Port 8081" just means you add `:8081` to the end of the server address in the browser.

1. Make sure your device is connected to the FieldCommand Wi-Fi network — by default named **EMCOMM-NET**.
2. Open any web browser.
3. In the address bar, type the server address followed by **`:8081`**. With the default server address that is **http://192.168.50.1:8081** (type it exactly, including the `http://`). If your build uses a different server address, use your real one with `:8081` on the end.
4. The Kiwix library page opens, listing every reference book you loaded. Click one to open it and read or search it just like a normal website — entirely offline.

> **MAKE IT EASY TO FIND ON THE DAY** — Field operators won't remember a port number under pressure. Write **http://192.168.50.1:8081** (or your real address) on the same card or sign that lists the Wi-Fi name and password, so anyone can pull up the reference library without asking. The FieldCommand dashboard may also link to it directly.


### Adding or Expanding the Library Later

You can grow the library at any time — step up from Tier 1 to Tier 2, or add individual titles — as long as the server has internet for the download. The tool is a script named **`kiwix_setup.sh`** in the `scripts` folder.

1. Give the server an internet connection — these downloads are large and need it.
2. Open a terminal and run **`sudo bash kiwix_setup.sh`** to get the interactive menu, or run **`sudo bash kiwix_setup.sh --tier 2`** to jump straight to a tier.
3. The menu lists every available title with its size and whether it's already installed, and lets you pick a whole tier or choose titles one at a time.
4. Confirm the plan. It shows the total download size (already-installed titles are skipped) before it starts.
5. Let it download. Large titles can take a long time on a slow connection; the download **resumes** if interrupted — just re-run the same command and it continues where it stopped.
6. When it's done, Kiwix automatically starts serving the new titles at the same port 8081 address — no extra step. Disconnect the internet and you're field-ready.

> **CHECK WHAT YOU'VE GOT** — To see what's already loaded without downloading anything, run **`sudo bash kiwix_setup.sh --status`** for the library or **`sudo bash download_tiles.sh --status`** for the map tiles. Each prints what's installed and how much space it uses — handy before a deployment to confirm the server is stocked.


## Troubleshooting

- *The map shows blank gray squares with no roads.* No tiles are loaded for that spot, or you've zoomed in closer than the detail you downloaded. If the *whole* map is blank, no tiles were ever loaded — run `sudo bash download_tiles.sh` (with internet) and pick a preset. If only *part* is blank, it's outside your downloaded area, or zoomed in past the level you fetched; download a larger area or the **Full** preset, which includes finer zoom.
- *The Kiwix library page won't load.* First, check the address — it must include the port: **http://192.168.50.1:8081** (or your real server address with `:8081`), including the `http://`. Second, make sure you're connected to the **EMCOMM-NET** Wi-Fi. Third, Kiwix may not be installed if you chose tier **0** at setup — run `sudo bash kiwix_setup.sh` with internet and pick a tier. To confirm it's running, run `sudo bash kiwix_setup.sh --status` on the server.
- *Kiwix loads but the shelf is empty (no books).* The Kiwix server is running but no libraries were downloaded — this happens if the install set up the system but the download was skipped or failed. Run `sudo bash kiwix_setup.sh --tier 1` with internet to fetch the essential titles.
- *The download stops partway through / "insufficient disk space."* The drive filled up. Kiwix checks free space and stops before overflowing rather than corrupting anything. Free up room or choose a smaller tier/preset. Remember Tier 3 Kiwix is ~25 GB and Full tiles are ~1.6 GB — make sure the space is there before starting.
- *The download got interrupted (lost internet, closed the window).* No harm done — both tools **resume**. Just run the same command again once internet is back. The tile downloader skips tiles it already has; the Kiwix downloader picks partial files up where they left off. Nothing needs to be deleted or restarted from scratch.
- *I loaded tiles/books but they're not showing up.* For tiles, re-run with `--status` to confirm they downloaded; if they're listed but the map is still blank, the tile server may need a restart (the download tool tells you the exact command when it finishes). For Kiwix, the library starts serving new titles automatically — reload the browser page at the `:8081` address.
- *I only have a little internet time — what should I load first?* Load **tile preset 1 (Essential, ~8 MB)** and **Kiwix tier 1 (~2.5 GB)** first. Those two cover a usable map and the most critical offline reference (medical) for the least data. Add more later whenever you next have a good connection.


# 10. Printing — Sharing a Printer with CUPS

*How FieldCommand shares one printer with every device on the network so anyone can print an ICS form, the Incident Action Plan, or a map — plus a list of printers that just work.*

> **QUICK VERSION** — The FieldCommand server already runs the **Common Unix Printing System (CUPS)** — the software that shares one printer with the whole team. Plug a printer into the server by USB, **or** put a Wi-Fi/Ethernet printer on the `EMCOMM-NET` network. Then, from any device, open a browser to **http://192.168.50.1:631**, click **Administration → Add Printer**, log in as **`fieldcommand`** with your server password, pick your printer, choose its driver, tick **Share This Printer** and **set it as the default**, and click **Print Test Page**. Everyone on `EMCOMM-NET` — every browser, LibreOffice, every app — can now print to it.


## What This Is / What It Is For

At a real incident, paper still matters. Section chiefs sign a printed **Incident Command System (ICS)** form; the **Incident Action Plan (IAP)** goes out as a stapled packet at the start of each operational period; briefings hand out printed maps; the check-in and resource boards get printed and pinned to the wall. If only the one laptop next to the printer can print, everyone crowds around that one machine — and that is the last thing you want during an activation. You want **any** operator, at **any** workstation, to hit Print and have the page come out on the shared printer across the room.

That is exactly what the server sets up for you. During installation, FieldCommand installs the **Common Unix Printing System (CUPS)** — the standard, long-proven software that manages printers and shares them over a network. You set up **one** printer on the server, and CUPS makes it available to every device on the `EMCOMM-NET` network at once: the Windows laptop, the operator workstations, tablets, and phones. No operator has to install a driver — they just pick the shared printer and print.

> **WHO DOES THIS** — Adding the printer is a one-time job for whoever sets up the server — the same person who ran the setup in the earlier chapters. Everyone else simply picks the shared printer in their print box and prints. They never touch the CUPS admin page.

> **"CUPS" AND "PRINT SERVER" MEAN THE SAME THING HERE** — When this guide says the **print server**, it means CUPS running on the FieldCommand server. It is already installed and running — you do not install it. Your only job is to tell it which printer you're using, which is what this chapter covers.


## First, Connect the Printer — Two Ways

Before CUPS can share a printer, the printer has to be reachable. There are two ways to connect one, and both work well. Pick whichever fits your gear:

| Way to connect | How it works | Best when |
| --- | --- | --- |
| **USB into the server** | You plug the printer's Universal Serial Bus (USB) cable straight into a spare USB port on the FieldCommand server (or into a powered USB hub on it). CUPS shares that USB printer out to the whole network. | You have a plain USB printer, or you want the printer physically next to the server. |
| **On the network (Wi-Fi or Ethernet)** | The printer joins the `EMCOMM-NET` network on its own — over Wi-Fi, or with a network (Ethernet) cable to the switch. It gets its own address on the network and CUPS talks to it there. | You have a Wi-Fi or Ethernet printer, or you want the printer somewhere away from the server. |

> **A NETWORK PRINTER IS THE LEAST FUSS FOR A PERMANENT SETUP** — If your printer has built-in Wi-Fi or an Ethernet port, joining it to `EMCOMM-NET` is usually the smoothest choice — especially a color **multifunction printer (MFP)**, an all-in-one that prints, scans, copies, and often faxes, living permanently at your **Emergency Operations Center (EOC)**. Use the printer's own control-panel menu to join the `EMCOMM-NET` Wi-Fi (enter the Wi-Fi password when it asks), or run a network cable from the printer to a spare port on the switch. Either way, the next section is the same — you still add it in CUPS so it becomes the one shared printer everyone uses.


## Open the CUPS Admin Page

CUPS has a simple web page for adding and managing printers. You reach it in a browser from any device on `EMCOMM-NET` — you do not need to be sitting at the server.

1. On any device connected to the `EMCOMM-NET` Wi-Fi, open a web browser.
2. In the address bar, type the CUPS address exactly — **http://192.168.50.1:631** — and press Enter. (That `:631` on the end is the printing port; it is what tells the browser you want the print server, not the main FieldCommand dashboard.)
3. The CUPS home page opens. Along the top you'll see tabs including **Administration**. Click **Administration**.
4. On the Administration page, click the **Add Printer** button.

> **WHY THE ADDRESS ENDS IN :631** — The main FieldCommand dashboard lives at **http://192.168.50.1**. The print server lives at the **same** address with **:631** added. Leave off the `:631` and you'll land on the dashboard instead of the printer page — a very common mix-up, so type it in full.


## Log In as fieldcommand

The moment you click **Add Printer**, CUPS asks who you are — because adding a printer changes the server, and it only lets an administrator do that.

1. A small login box pops up asking for a username and password.
2. For the **User Name**, type **`fieldcommand`** (all lowercase). This is the server's own administrator account.
3. For the **Password**, type the password you set for the server when you imaged the card back in the early setup chapters. It is the **same** password you'd use to log in to the server itself.
4. Click **OK** (or **Log In**). CUPS now lets you continue adding the printer.

> **IT'S THE SERVER PASSWORD — NOT A SEPARATE ONE** — There is no special "CUPS password." The account is **`fieldcommand`** and the password is the one you chose for the server during setup. If you don't know it, it's whatever was entered as the password when the server's card was imaged. Write it down somewhere safe — you'll want it any time you add or change a printer.


## Pick the Printer and Its Driver

After you log in, CUPS walks you through a few short screens. Take them one at a time:

1. **Choose the printer.** CUPS lists the printers it can see. A USB printer plugged into the server appears under **Local Printers**. A Wi-Fi or Ethernet printer on `EMCOMM-NET` appears under the network/discovered list. Click the round button next to your printer, then click **Continue**.
2. **Name and share it.** Give it a plain **Name** (for example, `FieldCommand-Printer`), and optionally a Description and Location. **Tick the box marked "Share This Printer."** This is the box that makes the printer available to everyone on the network — don't skip it. Click **Continue**.
3. **Choose the driver.** CUPS suggests a driver — the small piece of software that speaks your printer's language. Usually the right one is already highlighted; leave it as CUPS suggests, or pick the entry that matches your make and model most closely. Click **Add Printer**.
4. **Set default options.** On the options screen, set **Paper Size** to **Letter** (the United States standard), and set any other defaults you want. Click **Set Default Options**.

> **MAKE IT THE DEFAULT SO PRINT JUST WORKS** — Back on the printer's page in CUPS, open the **Maintenance** or **Administration** drop-down for that printer and choose **Set as Server Default**. This makes your printer the one that comes up automatically everywhere, so operators can hit Print without hunting through a list. Do this once and you're done.

> **THE RIGHT DRIVER IS WHAT SEPARATES CLEAN PAGES FROM GARBAGE** — If you force a driver that doesn't match your printer, pages may come out as jumbled characters, half-printed, or covered in stray symbols. When in doubt, accept the driver CUPS recommends for your exact model, or choose the closest match to your make and model. The recommended printers below were chosen specifically because their drivers install cleanly and correctly.


## Recommended Printers That Just Work

Not every printer plays nicely with a Linux print server. The models below were chosen because their drivers install cleanly with CUPS and they hold up to field use. You don't have to buy one of these — but if you're picking a printer for FieldCommand, start here. Each one connects by USB **or** over the network, so it works with either connection method above.

| Printer | Type | Connects by | Why it's a good pick |
| --- | --- | --- | --- |
| **Brother HL-L2350DW** | Monochrome (black-and-white) laser | USB or Wi-Fi | The best all-round choice for most deployments. Excellent driver support out of the box, fast, compact, prints double-sided, and durable. Around $130. |
| **HP LaserJet Pro M15w / P1102w** | Monochrome laser | USB or Wi-Fi | Full support through HP's Linux driver, which installs automatically with CUPS. Fast, reliable, and very low cost per page. Around $150. |
| **Brother MFC-L3770CDW** | Color laser multifunction printer (MFP) — print, scan, copy, fax | USB, Wi-Fi, or Ethernet | Prints color ICS maps and full IAP packets clearly. Full Linux support. A strong choice for a permanent EOC. Around $400. |
| **HP Color LaserJet Pro MFP M479fdw** | Color laser MFP | USB, Wi-Fi, or Ethernet | HP's Linux driver works with CUPS out of the box. Great for IAP packets with color-coded sections. Around $500. |
| **Canon imageCLASS MF743Cdw** | Color laser MFP | USB, Wi-Fi, or Ethernet | Good Linux driver, handles both letter and legal paper. A solid fit for a permanent EOC installation. Around $450. |
| **Canon PIXMA TR150** | Portable color inkjet — built-in battery | USB or Wi-Fi | Runs on a rechargeable battery, about 200 pages per charge — for field stations with no wall power. Letter size. Around $200. |
| **HP OfficeJet 200** | Portable inkjet — optional battery | USB or Wi-Fi | Larger paper tray than the TR150; an optional battery accessory frees it from wall power. Good for shelter check-in stations and mobile command posts. Around $180. |

> **MONO LASER FOR FORMS, COLOR MFP FOR MAPS, PORTABLE FOR THE FIELD** — A quick way to choose: a **monochrome laser** (like the Brother HL-L2350DW) is the cheap, reliable workhorse for the mountain of black-and-white ICS forms and IAP text. A **color laser MFP** (like the Brother MFC-L3770CDW) earns its keep when you print color maps and color-coded plans at a fixed EOC. A **portable, battery-powered** printer (like the Canon PIXMA TR150) is for deployments with no shore power — a shelter or a mobile command post.


## Print a Test Page

Before you trust the printer in the middle of an activation, prove it works. CUPS has a one-click test built in:

1. On the CUPS admin page, click the **Printers** tab at the top and click the name of the printer you just added.
2. Open the **Maintenance** drop-down and choose **Print Test Page**.
3. A CUPS test page should print within a few seconds — a page with color bars, alignment marks, and text. If it comes out clean and readable, your printer is set up correctly.

For a real-world test, open any FieldCommand page that has a **Print** button — for example the **Print Center** — and print one ICS form. Watch that it comes out on the shared printer and looks right. That confirms the whole path works, from the app all the way to paper.


## Every App Uses This Same Printer

Here's the payoff. Because CUPS shares the printer to the whole system, you set it up **once** and everything uses it. FieldCommand's own **Print** buttons print to it. So does everything else on the workstations: **LibreOffice** (the free office suite for letters, spreadsheets, and documents), the web browser, the map viewer — any program with a Print command finds the same shared printer in its list. So when someone types up a quick memo in LibreOffice, or a section chief prints a resource spreadsheet, it lands on the same printer as the ICS forms and the IAP, with no extra setup. One printer, one setup, the whole team and every program printing to it.

> **OTHER DEVICES FIND IT AUTOMATICALLY** — The server also advertises the shared printer over the network so most devices discover it on their own. A Windows laptop finds it under **Settings → Printers & scanners → Add a printer**. A Mac finds it under **System Settings → Printers & Scanners → +**. Apple iPads and iPhones can print to it straight from the Share → Print menu (no setup at all). On the Raspberry Pi workstations, the printer simply appears in the browser's print box. In every case they're using the one printer you set up here.


## Troubleshooting

- *My printer isn't in the list when I click Add Printer.* For a **USB** printer: make sure it's powered on and the USB cable is firmly seated at both ends, then reload the page — a printer that's off or asleep won't show up. For a **network** printer: make sure it has actually joined `EMCOMM-NET` (check its own screen shows it's connected to that Wi-Fi, or that its network cable is plugged into the switch) and that it's powered on. Give it a minute after it connects, then reload the Add Printer page.
- *The login box won't accept my username and password.* The username is **`fieldcommand`** in all lowercase, and the password is the **server's** password — the one set when the card was imaged, the same one you'd use to log in to the server. There is no separate CUPS password. Retype both carefully (passwords are case-sensitive).
- *I can't reach http://192.168.50.1:631 at all — the page won't load.* Two things to check. First, make sure your device is connected to the `EMCOMM-NET` Wi-Fi, not some other network. Second, make sure you typed the address in full **with the `:631` on the end** — without it you'll get the main dashboard or an error, not the print server.
- *The pages print as garbage — jumbled characters, stray symbols, or half a page.* This is almost always the wrong driver. Go back into CUPS, open the printer, choose **Modify Printer**, and step through until you can pick the driver again — select the one that matches your exact make and model, or accept the one CUPS recommends. Print a test page to confirm.
- *My color printer only prints in black and white.* Open the printer in CUPS, go to **Set Default Options**, and look for a **Color Mode** (or similar) setting — make sure it's set to **Color**, not Grayscale or Black. Also confirm you picked the **color** driver for your model, and that the printer has color toner or ink installed and not empty.
- *I plugged in a USB printer but the server doesn't detect it.* Unplug it and plug it back into a different USB port on the server. If it's on a USB hub, use a **powered** hub (one with its own power adapter) — an unpowered hub often can't drive a printer. Power the printer off and on, wait for it to finish warming up, then reload the Add Printer page.
- *Everyone else can't find the shared printer on their devices.* Confirm you ticked **Share This Printer** when you added it. Open the printer in CUPS and check that sharing is on. Also make sure the other devices are on the `EMCOMM-NET` network — a device on a different network can't see the shared printer.
- *There's no printing at all this activation and I want to skip it.* That's fine — printing is optional. FieldCommand runs perfectly without a printer; you just won't be able to print forms until one is added. You can add a printer any time later by following this chapter.


# 11. Operator Workstations — Raspberry Pi 500

*The ready-to-use computers you set at each operating position — a Raspberry Pi 500 keyboard-computer and a monitor, joined to EMCOMM-NET and pointed at the FieldCommand dashboard, so an operator can sit down and work in seconds.*

> **QUICK VERSION** — Set a **Raspberry Pi 500** and a monitor at each operating position. Plug the Raspberry Pi 500 into the switch with a network cable (or join **EMCOMM-NET** over Wi-Fi), plug in the monitor and power, and turn it on. Open the built-in **Chromium** web browser and go to **http://192.168.50.1**. That's a working operator station. To make it open FieldCommand by itself every time it starts, set Chromium's start page (below). Four stations is typical.


## What This Is / What It Is For

An **operator workstation** is a small, ready-to-use computer you place at each operating position — the check-in table, the net control desk, the resource-tracking corner. It is nothing more than a **Raspberry Pi 500** (a complete computer built into a keyboard) plus a **monitor**, connected to your FieldCommand network and showing the dashboard in a web browser. An operator walks up, sits down, and is already looking at the tools — no logging in to a personal account, no installing anything, no hunting for a cable.

FieldCommand is a **web application**: everything it does happens in a web browser pointed at the server. That means a workstation does not need any special software — it only needs a browser and a connection to the server. The whole job of this chapter is getting a browser on a screen at each position, aimed at **http://192.168.50.1**, so the people doing the work have the tools in front of them.

> **WHY DEDICATED WORKSTATIONS INSTEAD OF "BRING YOUR OWN"** — Anyone can connect their own phone, tablet, or laptop to EMCOMM-NET and reach the same dashboard — nothing stops them, and it is a fine way for helpers to pitch in. But **dedicated** Raspberry Pi 500 stations give you consistency you can count on: every position looks and behaves the same, there are no dead phone batteries mid-shift, no personal notifications popping up over an ICS form, and a fresh operator on the next shift finds the station exactly as the last one left it. For the core positions you staff every activation, dedicated stations are worth it.


## What Each Station Is Made Of

A single operator workstation is just a handful of parts. Here is what one station needs and what each piece is for:

| Part | What it is | Why it's there |
| --- | --- | --- |
| **Raspberry Pi 500** | A complete computer built into a keyboard — you add a screen, and it's a full desktop. Runs the Raspberry Pi OS Desktop operating system with the Chromium web browser already installed. | This is the workstation's brain. It joins the network and runs the browser that shows FieldCommand. |
| **Monitor** | A 15.6-inch Full HD screen (the Raspberry Pi Monitor is the matched choice — it powers from the Raspberry Pi 500 over a single USB-C cable and has a built-in kickstand). | So the operator can see the dashboard. Any HDMI monitor works; the matched 15.6-inch one keeps the station compact and travel-friendly. |
| **micro-HDMI to HDMI video cable** | A short cable from the Raspberry Pi 500's micro-HDMI port to the monitor's HDMI port. | Carries the picture from the computer to the screen. |
| **USB-C power supply (27 W)** | The official Raspberry Pi USB-C power supply. | Powers the Raspberry Pi 500. If the monitor supplies power over USB-C, the Raspberry Pi 500 can run from the monitor instead — one less brick. |
| **Network cable (optional)** | A short CAT 6 Ethernet patch cable from the Raspberry Pi 500 to the network switch. | The most reliable way to connect. Skip it if you join EMCOMM-NET over Wi-Fi instead. |
| **Mouse (optional)** | A USB mouse. | The Raspberry Pi 500 has a keyboard built in; a mouse just makes pointing and clicking easier. A touchscreen monitor removes the need for one. |

> **"HDMI", "MICRO-HDMI", AND "USB-C" — IN PLAIN WORDS** — **HDMI** (High-Definition Multimedia Interface) is the standard cable that carries video to a screen. **Micro-HDMI** is the same thing with a smaller plug on the computer end — that's why the video cable has a big plug at the monitor and a tiny plug at the Raspberry Pi 500. **USB-C** is the small oval connector used here for power. You don't need to understand any of it beyond matching each cable to its labeled port.


## Setting Up One Workstation

Do this once per position. It takes a few minutes and needs no technical knowledge — you are connecting cables and opening a browser.


### Step 1 — Connect it to the network

Pick **one** of these two ways to get the workstation onto EMCOMM-NET:

- *Wired (recommended).* Run a short network cable from the Raspberry Pi 500's Ethernet port to any open port on the **network switch** (the box everything plugs into). Wired is steadier than Wi-Fi and never drops mid-net — use it whenever the station sits near the switch. The switch hands the workstation an address automatically; you do nothing else.
- *Wi-Fi.* If a cable won't reach, join the workstation to the **EMCOMM-NET** Wi-Fi network the same way you'd join any Wi-Fi: click the network icon on the Raspberry Pi 500 desktop, pick **EMCOMM-NET** from the list, and type the Wi-Fi password. This is the right choice for a station across the room or in another tent.


### Step 2 — Connect the monitor and power

1. Plug the **micro-HDMI to HDMI** cable in: the small end into the Raspberry Pi 500, the large end into the monitor.
2. Power the monitor (its own supply, or a USB-C cable if it draws power that way).
3. Power the Raspberry Pi 500 with the **27 W USB-C** supply — or, if your monitor feeds power out over USB-C, run that single cable to the Raspberry Pi 500 and skip the separate brick.
4. The Raspberry Pi 500 starts up on its own and lands on the Raspberry Pi OS desktop in under a minute. You'll see a normal desktop with a taskbar.


### Step 3 — Open the FieldCommand dashboard

1. On the taskbar, click the **Chromium** web browser icon (the round, four-color circle).
2. In the address bar at the top, type **http://192.168.50.1** exactly — including the `http://` — and press Enter.
3. The FieldCommand dashboard opens. This station is now ready for an operator.

> **PREFER FULL-SCREEN FOR A CLEANER LOOK** — Press **F11** to put Chromium into full-screen mode — the address bar and desktop disappear, leaving only FieldCommand. Press **F11** again to come back out. Full-screen keeps operators focused on the tools and looks tidy on a small monitor.


## Make It Open FieldCommand By Itself

You don't want to reopen the browser and re-type the address every time a station powers on. Set the browser's **start page** once, and from then on the Raspberry Pi 500 boots straight to the dashboard with no clicks at all — a true walk-up-and-work station (sometimes called **kiosk mode**).

1. In Chromium, click the **three-dot menu** at the top-right and choose **Settings**.
2. In the left list, click **On startup**.
3. Choose **Open a specific page or set of pages**, then click **Add a new page**.
4. Type **http://192.168.50.1** and click **Add**.
5. Close Settings. From now on, every time this Raspberry Pi 500 starts, Chromium opens straight to the FieldCommand dashboard.

> **A DIFFERENT BROWSER IS FINE** — Chromium comes pre-installed and is the recommended choice, but the Raspberry Pi 500 can also run **Firefox** (install with `sudo apt install firefox-esr`) or the very lightweight **GNOME Web** browser (`sudo apt install epiphany-browser`) if you ever want an alternative — for example on a check-in station with many tabs open where you want the smallest memory footprint. All of them reach the same dashboard at the same address.


## How Many Workstations Do You Need?

There is no fixed number — you set up one workstation per operating position you want to staff. A common, comfortable starting point is **four** Raspberry Pi 500 stations, which covers the core roles most activations run at once:

- *Net control* — the operator running the radio net and logging check-ins.
- *Check-in / registration* — logging people and resources as they arrive.
- *Resource / status tracking* — keeping the ICS boards and forms current.
- *A spare or floating station* — for the incident commander, a message clerk, or whoever needs a screen next.

Add more as your positions grow; remove them when you run lean. Because every station is identical and connects the same way, scaling up or down is just plugging in or unplugging one more Raspberry Pi 500. The switch has ports set aside for them, so there's room to expand without reconfiguring anything.


## More Than Just a Browser

A Raspberry Pi 500 workstation is a full Linux desktop computer, not a locked-down terminal — so it can do ordinary desktop work alongside FieldCommand when you need it to. That flexibility is a bonus, not a requirement; most of the time a station just shows the dashboard.

- *Office documents.* **LibreOffice** — a free office suite that opens and creates documents, spreadsheets, and presentations — comes with the Raspberry Pi OS Desktop. An operator can draft a message, keep a side spreadsheet, or open a PDF without leaving the station.
- *Printing.* Every workstation can print to the shared network printer through FieldCommand's print server. Chromium finds the printer automatically, so printing an ICS form or a net log is just **File → Print**. The full setup and any troubleshooting live in the **Printing** chapter — this is only a pointer to it.


## Troubleshooting

- *The workstation can't reach the dashboard / the page won't load.* First confirm the network connection: for a wired station, check the CAT 6 cable is firmly seated at both the Raspberry Pi 500 and the switch, and that the switch port's light is on; for Wi-Fi, click the network icon and confirm it's joined to **EMCOMM-NET**. Then check the address is typed exactly as `http://192.168.50.1`, including the `http://`. If other stations reach the dashboard but this one doesn't, the problem is this station's connection, not the server.
- *No picture on the monitor.* Make sure the small (**micro-HDMI**) end of the video cable is in the Raspberry Pi 500 and the large (**HDMI**) end is in the monitor — it's easy to reverse. Confirm the monitor is powered on and set to its **HDMI** input. If the monitor draws power over USB-C, check that cable too. As a test, try the other micro-HDMI port on the Raspberry Pi 500.
- *The keyboard or mouse doesn't respond.* The keyboard is built into the Raspberry Pi 500 and works as soon as the computer is powered — if nothing types, the Raspberry Pi 500 itself may not be powered (check the USB-C power and look for its power light). For a separate USB mouse, unplug it and plug it back into a USB port; give it a few seconds to be recognized. A touchscreen monitor needs its USB touch cable connected to the Raspberry Pi 500, not just the video cable.
- *It boots to the desktop but not to FieldCommand.* You haven't set the start page yet, or it was cleared. Open Chromium, go to **Settings → On startup**, choose **Open a specific page**, and add **http://192.168.50.1** (see the steps above). After that it opens the dashboard on every boot.
- *The screen is cut off or too big/small.* This is a display-resolution mismatch. On the Raspberry Pi 500 desktop, open **Screen Configuration** (or **Settings → Displays**) and set the resolution to match the monitor — Full HD (1920×1080) for the matched 15.6-inch screen. The picture will snap to fit.
- *The station is slow with many tabs open.* A Raspberry Pi 500 is a small computer; a dozen open browser tabs will tax it. Close tabs you're not using, or switch that station to the lighter **GNOME Web** browser for check-in duty where memory is tight.


# 12. Internet / WAN — Connecting Upstream (Optional)

*FieldCommand is offline-first — it runs completely without the internet. This chapter shows how to add an optional upstream internet connection, and how automatic failover keeps you online if one source drops.*

> **QUICK VERSION** — You do **not** need the internet — FieldCommand works fully offline. If you want the online extras (weather alerts, live position data, propagation), plug your internet source into the **router's WAN port** and set it as the **preferred** source in the **WAN Settings** screen. Add a second source as the **fallback** and the router switches to it automatically if the first goes down. your organization uses a cellular modem (primary internet) first, and a satellite link (fallback internet) if that primary source drops.


## What This Is / What It Is For

FieldCommand is built **offline-first**. Everything that matters during an incident — the dashboard, net logging, Incident Command System (ICS) forms, maps, the roster, resource tracking, the reference library — lives on the server itself and runs with **no internet connection at all**. That is a deliberate design choice: when a disaster takes the internet down, your incident tools must not go down with it. So the first thing to understand about this chapter is that everything in it is **optional**.

A **Wide Area Network (WAN)** connection — plain-language: a link out to the internet — only adds a few *live extras* on top of the system you already have. Nothing you rely on depends on it. If you never connect the internet, you lose none of the core function; you simply don't see the handful of features that pull in live outside data.

> **WHAT INTERNET ADDS — AND WHAT IT DOESN'T** — **Adds (live extras only):** National Weather Service (NWS) weather alerts for your area, **APRS-IS** (the internet side of the Automatic Packet Reporting System, showing live station positions from the wider network), and **HF propagation** data (which radio bands are working right now). **Doesn't affect anything else:** net logging, ICS forms, maps, roster, resource tracking, and printing all work exactly the same with or without internet. When the internet is unavailable, those live extras simply pause and everything else keeps running without interruption.


## Preferred and Fallback — The Idea

FieldCommand can use up to **two** internet sources, and what matters is the **role** you give each one, not what type it is. A source can be cellular, satellite, a hotspot, or a wired connection — the router treats them the same. You assign each source one of two roles:

| Role | What it means | In plain words |
| --- | --- | --- |
| **Preferred** | The source the router tries **first**. As long as it's working, this is the one carrying your internet traffic. | Your main internet. |
| **Fallback** | The backup. The router uses it **only** when the preferred source is down or can't be detected. | Your spare, used automatically if the main one fails. |

You can enable just one source (main only, no backup) or both (main plus automatic backup). With both configured, you get **automatic failover** — the router notices the preferred source has dropped and moves your traffic to the fallback on its own, without anyone touching a setting.


## The Two Sources for your organization

your organization is set up with two internet sources so it stays online even if one fails:

| Source | Role | Notes |
| --- | --- | --- |
| a cellular modem (primary internet) | **Preferred** — used first | This is the day-to-day internet path. Cellular is quick to bring up in the field and works almost anywhere there's mobile coverage. |
| a satellite link (fallback internet) | **Fallback** — used if the primary drops | Satellite keeps you online where cellular coverage is weak or overloaded — for example a remote staging area, or a wide-area outage that's saturated the cell network. |

With both in place, your organization uses a cellular modem (primary internet) first, and if that primary source drops, the router quietly switches to a satellite link (fallback internet) — the live extras keep flowing and no one has to intervene. If your group only has one of the two, that's fine: set the one you have as the preferred source and leave the second slot empty.


## Where the Internet Plugs In

All internet connections attach to the **router**, not to the network switch and not to the FieldCommand server. The router is the box that both provides your EMCOMM-NET Wi-Fi and manages the connection out to the internet. It has a dedicated **WAN port** (sometimes labeled **uplink** or **internet**) for exactly this.

| Source | Where it connects | How |
| --- | --- | --- |
| Cellular modem or antenna | Router **WAN** (uplink) port | Run the modem's network cable straight into the router's WAN port. The router pulls an address automatically — set its WAN type to **Automatic IP (DHCP)** if it asks. |
| Satellite link | Router **USB** WAN port (via a USB-to-Ethernet adapter) | The satellite equipment's network cable goes through a small USB-to-Ethernet adapter into the router's USB port. Enable the router's **Dual WAN** option so it can fail over between the two. |
| Site wired internet | Router **WAN** (uplink) port | Plug the venue's internet cable into the WAN port and set **Automatic IP (DHCP)**. A good, cheap primary when the site has reliable wired internet. |
| Phone hotspot | Router **USB** port (USB tether) or over Wi-Fi | A last-resort path — tether a phone by USB cable, or have the router join the phone's hotspot. Handy when nothing else is available. |

> **THE INTERNET SOURCE IS SEPARATE FROM THE OPERATOR NETWORK** — The WAN (internet) connection plugs into the router's **WAN/uplink** side. Your operator devices, workstations, and the server all live on the **local** side — EMCOMM-NET, addresses in the `192.168.50.x` range. The router keeps the two apart and bridges internet traffic across only when a WAN source is up. This is why unplugging the internet never disturbs the operators: they're on a different side of the router entirely.


## Setting the Sources — The WAN Settings Screen

Once the hardware is plugged in, you tell FieldCommand about your sources on its own **WAN / Internet Settings** screen. This is where you name each source, give it the preferred or fallback role, and choose how the system checks whether it's up.

1. On any device connected to EMCOMM-NET, open a browser and go to the FieldCommand dashboard at **http://192.168.50.1**.
2. Open the **WAN / Internet Settings** screen (the admin area for internet sources).
3. You'll see two source cards, **Source A** and **Source B**. In each, tick **Enabled**, type a **Display Name** (for example, the name of your carrier or `Satellite`), pick the **Role** (Preferred or Fallback), and choose the **Type** (cellular, satellite, hotspot, or fixed).
4. Set the **Detection Method** — how FieldCommand decides the source is really up. Choose **Internet reachable** for the simplest up/down check, **Ping a gateway IP** to check a specific address that only answers when that path is live, or **Modem admin page responds** to also read carrier and signal details when the modem supports it.
5. Click **Save Settings**. Your changes take effect within about **30 seconds** (the next check cycle).

> **SWAPPING WHICH SOURCE IS PRIMARY** — If you want to flip which source is the main one — say cellular becomes flaky and you'd rather lead with satellite — use the **Swap preferred ↔ fallback roles** button on the WAN Settings screen. It trades the two roles in one click; Save, and the change is live within about 30 seconds. You don't have to unplug or reconfigure anything.


## How Automatic Failover Works

When both sources are configured, you don't manage the switch between them — the router does. Here is the plain-language version of what happens:

1. The router uses your **preferred** source (a cellular modem (primary internet)) for all internet traffic while it's healthy.
2. It quietly and constantly checks whether that source is still reachable, using the detection method you chose.
3. The moment the preferred source stops answering, the router moves your traffic to the **fallback** source (a satellite link (fallback internet)) — automatically, within seconds.
4. When the preferred source comes back, the router returns to it on its own. You end up back on your main internet without lifting a finger.

> **FAILOVER ONLY MATTERS FOR THE LIVE EXTRAS** — Remember what's actually riding on the internet: weather alerts, APRS-IS, and propagation data. During the brief moment a failover takes, those extras may blink and refresh — and that's the worst that happens. Your net logging, ICS forms, maps, and every other core tool never notice, because they don't use the internet in the first place.


## How to Tell Whether Internet Is Up

FieldCommand shows the internet status right on the dashboard so you always know where you stand. Look for the **WAN status card** (you can turn the card on or off in WAN Settings under **Dashboard Display**). It tells you which source is active — preferred or fallback — and whether it's currently reachable. If the card shows the source is down and no fallback is available, you're running fully offline, which, again, is a perfectly normal state for FieldCommand.

You can also just watch the live extras themselves: if NWS weather alerts and APRS-IS positions are updating, you have internet; if they've paused, you don't. Either way the rest of the system carries on exactly the same.


## Troubleshooting

- *I connected a source but there's still no internet.* Confirm the source cable is in the router's **WAN/uplink** port (or the USB port for a USB-based source), not into the network switch. In the modem's own setup, make sure it actually has service. In WAN Settings, confirm the source is **Enabled** and **Saved**, then wait the ~30-second check cycle. If you chose **Ping a gateway IP**, double-check the address is the one that answers on that path (for example, a Starlink link answers at `192.168.100.1`).
- *Failover isn't switching to the backup.* Both sources must be **Enabled** in WAN Settings, one set to **Preferred** and the other to **Fallback**, and **Dual WAN** must be turned on in the router's own settings so it's allowed to switch. Also check that each source's **Detection Method** is set to something that truly tests that path — if both are set to "Internet reachable" and the router can still see the internet another way, it may not think the preferred source has failed. Using **Ping a gateway IP** on each source makes the up/down decision much more reliable.
- *The live extras (weather, APRS-IS, propagation) aren't appearing.* Those features only work when the internet is up. First confirm internet is actually connected using the **WAN status card** on the dashboard. If internet is up but a specific extra is still missing, its module may be switched off in the main Setup screen — check that the feature is enabled there. Note that some features (like APRS-IS) may also need a licensed callsign set before they'll turn on.
- *The WAN status card shows the fallback is active when it shouldn't be.* Your preferred source has dropped and the router did its job — it moved you to the backup. Check the preferred source's hardware (cellular signal, cable seating, modem power). When the preferred source recovers, the router returns to it automatically; you don't need to change anything in FieldCommand.
- *I changed a WAN setting but nothing happened.* Changes take effect on the next check cycle — give it about **30 seconds** after you click **Save Settings**. If it still hasn't taken, re-open WAN Settings, confirm your change is shown (a save that didn't go through would have reverted), and Save again.
- *I have no internet at all and want to make sure that's OK.* It is. Leave both source slots disabled if you like. The dashboard, net logs, ICS forms, maps, roster, resource tracking, and printing all run entirely on the local server. Running FieldCommand with no internet is a fully supported, everyday mode — you'll simply not see the live outside-data extras.


# 13. First-Boot Verification, Maintenance & Backups

*How to prove the finished server actually works, how to keep it up to date, and how to make backups so you never lose an incident's data.*

> **QUICK VERSION** — Open a browser on the FieldCommand Wi-Fi and go to **http://192.168.50.1** — the dashboard should load. Then open the **Pre-Flight** page and press **Auto-Check**: a green **GO** means the core services are up and the install worked. To update the server, run **`sudo bash /opt/fieldcommand/scripts/update.sh`** while it has internet — normally only before a deployment. To back up, plug in a USB drive labeled **FIELDCOMMAND** and it copies your data automatically.


## What This Is / What It Is For

The server is built and installed. This chapter is about the three things you do right after that build, and keep doing for the life of the server: **prove it works**, **keep it current**, and **protect its data**. None of these is hard — most of it is a page you open in a browser or a single command — but skipping them is how groups get surprised in the field. A five-minute check now beats a dead dashboard during a real activation.

The chapter is in three parts. **Part 1 — Verify** confirms the install actually succeeded, using FieldCommand's own built-in **Pre-Flight** readiness check plus a short by-hand list. **Part 2 — Maintenance & Updates** explains how and when to update. **Part 3 — Backups** covers the plug-in-a-USB-drive auto-backup and a full-system backup, and tells you exactly where your incident data lives so you always know what you're protecting.

> **WHO DOES THIS** — Verifying is done once, by whoever built the server, right after the install finishes — and again as a habit before every deployment. Updates and backups are ongoing housekeeping for the same administrator. Regular operators never need to touch any of this.


## Part 1 — Verify the Install Worked

There are two ways to confirm the server came up correctly. The fast, official way is FieldCommand's **Pre-Flight** page, which checks the core services for you and gives a single **GO / CAUTION / NO-GO** verdict. The second is a short by-hand checklist you can run in under a minute. Do both the first time; after that, the Pre-Flight page alone is enough.


### The Pre-Flight Readiness Check — GO / CAUTION / NO-GO

**Pre-flight** is the readiness page pilots borrow their name from: a go/no-go check you run before you commit. In FieldCommand it lives at **http://192.168.50.1/preflight.html** (or click **Preflight** in the top navigation bar). At the very top it shows one big verdict word and a colored progress bar. To check the install, you only care about the first section, **Data Readiness**, which the server can fill in **automatically**.

1. On a device connected to the FieldCommand Wi-Fi, open a browser and go to **http://192.168.50.1/preflight.html**.
2. Find the **🗄 Data Readiness (Auto-Checked)** section at the top and click its **Auto-Check** button (it may run on its own when the page loads).
3. The page asks the server how it's doing and marks each item with a green check or a red cross. Watch the big verdict word at the top.

The verdict word can be one of three states. Here is exactly what each means for a freshly-built server:

| Verdict | Color | What it means | What to do |
| --- | --- | --- | --- |
| **GO** | Green | Every required item is confirmed. The core services answered, the dashboard is up, and nothing is failing. | The install is good. You're done verifying. |
| **CAUTION** | Amber | Nothing is broken, but some items aren't confirmed yet — usually optional ones you haven't set up (a roster, repeater data), or items you simply haven't checked off by hand. | Fine for confirming the install. Read the amber items; anything you plan to use in the field, set up before deployment. |
| **NO-GO** | Red | At least one **required** item failed or is unconfirmed — for example a core service didn't answer, or Organization Setup was never completed. | The install has a real problem. Read which item shows a red cross and see Troubleshooting below. |

> **CAUTION IS NORMAL ON A BRAND-NEW SERVER** — A freshly-built server almost always shows **CAUTION**, not GO — simply because optional things like the member roster, repeater database, or an active incident haven't been set up yet. That does **not** mean the install failed. For verifying the install, what you care about is that the **required** items (the ones with a small red dot) are green and that you never see **NO-GO**. You'll reach GO later, in the field, once everything is loaded.

> **PRE-FLIGHT IS ALSO YOUR PRE-DEPLOYMENT CHECK** — This same page is what your team runs before every activation — power, antennas, personnel, and safety items are all on it. Right now you're only using the auto-checked Data Readiness section to confirm the build. Keep the page in mind: it's the standard go/no-go review your net control operator will use for real.


### The Quick By-Hand Checklist

If you'd rather confirm the basics yourself, or the Pre-Flight page won't load, run this short list. Each item takes seconds:

| Check | How to confirm | Good result |
| --- | --- | --- |
| **The dashboard loads** | In a browser on the FieldCommand Wi-Fi, go to **http://192.168.50.1** | The FieldCommand dashboard appears with its tiles and the clock ticking. |
| **Wi-Fi is reachable** | On a phone or laptop, look for the Wi-Fi network named **EMCOMM-NET** and connect to it | The device connects and gets an address in the `192.168.50.x` range. |
| **The lookup service answers** | Browse to **http://192.168.50.1:5050** (the FCC callsign lookup API) | You get a response from the server rather than a connection error. |
| **Offline reference is up (if installed)** | Browse to **http://192.168.50.1:8081** (the Kiwix offline library) | The Kiwix welcome page loads with whatever offline books you installed. |
| **Winlink backup is up (if installed)** | Browse to **http://192.168.50.1:8090** (the Pat Winlink client) | The Pat web page loads. |

Acronyms, once: **API** means *Application Programming Interface* — a small web address other software talks to; you're just confirming it answers. **FCC** is the *Federal Communications Commission*, whose callsign database FieldCommand looks up offline. **SSID** (seen on the Setup screen) is a *Service Set Identifier*, the technical name for a Wi-Fi network's name.


### The Real Service Ports — a Reference

FieldCommand is several small services working together, each listening on its own **port** (a numbered doorway on the same server address). You don't normally think about them, but when you're verifying an install — or chasing a problem later — knowing the real ports lets you test each piece directly. A **port** is just the number after the colon in an address like `192.168.50.1:5050`.

| Address | Service | What it does |
| --- | --- | --- |
| **http://192.168.50.1** | Web dashboard (nginx) | Serves every FieldCommand page — the main front door on the standard web port 80. |
| **:5050** | FCC Lookup / core API | Callsign lookups, organization config, incidents, and net logs. |
| **:5051** | Health Monitor / ICS platform | System health and the ICS forms, T-cards, check-ins, GPS, and cost tracking. |
| **:8000 / :8001** | Direwolf TNC | Decodes APRS off the radio (AGWPE on 8000, KISS on 8001). Optional — amateur radio only. |
| **:8081** | Kiwix offline library | Wikipedia, medical, and reference books served offline. Optional. |
| **:8083** | Offline map tiles | The local map imagery so maps work with no internet. Optional. |
| **:8090** | Pat Winlink | Browser-based backup Winlink radio-email client. Optional. |

> **OPTIONAL SERVICES ONLY EXIST IF YOU INSTALLED THEM** — The services marked *Optional* above (Kiwix, map tiles, Pat, Direwolf) are only present if you chose them during setup. If one of those addresses doesn't answer but you never installed it, that's expected — not a fault. The dashboard and the two core services (5050 and 5051) should always be up.


## Part 2 — Maintenance & Updates

FieldCommand ships one tool for all upkeep: a menu-driven script called **`update.sh`**. You run it and pick a numbered option — restart services, check their status, refresh data, update the web files, and so on. It's the single place you go for routine maintenance.

```
sudo bash /opt/fieldcommand/scripts/update.sh
```

The word **`sudo`** means "run this as the administrator"; it may ask for the server's password. When the menu appears, you type the number or letter of what you want and press Enter. The most useful choices are:

| Choice | What it does | When you'd use it |
| --- | --- | --- |
| **3) Check service status** | Lists every service with a green or red dot. | The quickest health check — run this first if something seems off. |
| **1) Restart all services** | Stops and starts every service cleanly. | After an update, or to clear a service that's misbehaving. |
| **7) Update web files** | Copies the newest FieldCommand pages and programs into place and restarts services. | When you've pulled a newer version of the software and want it live. |
| **5) Refresh FCC database** | Rebuilds the offline callsign database from the latest data. | Before a deployment, while online, so lookups are current. |
| **8) Backup data** | Copies the runtime data to a folder (see Part 3). | A fast on-demand snapshot without hunting for a USB drive. |


### When to Update — and Why the Server Runs Offline

The FieldCommand server is built to run **completely offline**. In the field it usually has no internet at all — that's the whole point of an off-grid emergency system. Because of that, there is no automatic "check for updates" running in the background, and there shouldn't be. **You** decide when to update, and you do it deliberately, on your own schedule.

> **UPDATE BEFORE A DEPLOYMENT, WHILE YOU STILL HAVE INTERNET** — The right time to update — and to refresh the FCC callsign database and repeater data — is **at home base, before you deploy, while the server is online**. Do it as part of packing the go-kit. Once you're in the field the server is offline by design, so an update there usually isn't possible and definitely isn't the moment to try. Update early, verify with Pre-Flight, then deploy a known-good server.

Between deployments, a good rhythm is: update and refresh data before any planned activation or exercise, run the Pre-Flight check to confirm everything still reads GO or a benign CAUTION, then set the server aside ready to go. There is no need to update a server that's sitting idle and working.


## Part 3 — Backups

A mirror (RAID 1) protects you if a **drive** dies, but it is **not a backup** — it faithfully copies mistakes and deletions to both drives instantly. Backups are separate and just as important: they capture your incident data onto a drive you can remove and store somewhere safe. FieldCommand gives you two easy ways to do this.


### USB Auto-Backup — Just Plug In a Drive Labeled FIELDCOMMAND

The simplest backup in FieldCommand needs no commands at all. The server watches for a USB drive whose volume label is exactly **FIELDCOMMAND** (all capital letters). The moment you plug one in, the server automatically copies all of its runtime data — including a clean snapshot of the incident database — onto that drive, into a folder stamped with the date and time.

1. Prepare a USB drive whose volume label is exactly **FIELDCOMMAND** (all capitals). On Windows, format it as FAT32 and set the volume label to `FIELDCOMMAND`; on Linux you can run `sudo mkfs.vfat -n FIELDCOMMAND /dev/sda1` (substitute your real device name).
2. Plug the drive into the FieldCommand server.
3. The backup runs by itself. Your data is copied to **/media/fieldcommand/backup/** in a folder named for the current date and time (for example `20260812_143005`).
4. Wait a few seconds, then remove the drive and store it somewhere safe. Repeat as often as you like — each insertion makes a fresh, separate backup.

> **THE LABEL MUST BE EXACTLY FIELDCOMMAND** — The trigger matches the volume label **FIELDCOMMAND** in all capital letters — nothing else. A drive labeled `Fieldcommand`, `FIELD-COMMAND`, or `BACKUP` will simply be ignored and no backup happens. If plugging in your drive does nothing, the label is almost always the reason. Re-label it and try again.


### Full-System Backup to an External Drive

The USB auto-backup captures your **data**. For a deployment archive or a belt-and-suspenders copy, you can also make an on-demand backup from the maintenance menu: run **`update.sh`** and choose **8) Backup data**, which writes a timestamped copy of the runtime data to the server. For a genuine full-system copy you'd take before major changes, back the whole data folder up to a large external drive (a rugged USB hard drive is ideal) so an entire incident's records live on removable media you keep off the server.


### Where the Incident Data Lives

It helps to know exactly what you're protecting. Everything FieldCommand creates during an activation — your organization configuration, incidents, net logs, ICS forms, check-ins, and the main database — lives under one folder on the server:

```
/opt/fieldcommand/data/
```

Inside it, **`fieldcommand.db`** is the single database file holding the live incident records. Both backup methods above copy this folder, and the USB auto-backup additionally makes a clean, consistent snapshot of the database so you always have a good copy even if the server was busy. The web pages themselves live separately under **/opt/fieldcommand/html/**, but those come from the software and don't need backing up the way your data does.

> **A SIMPLE, RELIABLE BACKUP HABIT** — Keep one USB drive labeled **FIELDCOMMAND** in the go-kit at all times. Plug it in at the end of every operating period — a shift change, a net closing, the end of the day — and you'll always have a recent, removable copy of the incident's data. It costs ten seconds and it's the single best protection against losing a day's work.


## Troubleshooting

- *Pre-Flight shows NO-GO / a service item has a red cross.* A required service isn't answering. Run the maintenance menu — `sudo bash /opt/fieldcommand/scripts/update.sh` — and choose **3) Check service status** to see which one is down, then **1) Restart all services**. Re-run the Pre-Flight Auto-Check. If a specific service keeps failing, check its log with `journalctl -u fcc-lookup -n 50` (swap in the failing service's name).
- *Pre-Flight says "Server unreachable" when I press Auto-Check.* The page loaded but the core service on port 5050 didn't answer. Confirm the dashboard itself loads at **http://192.168.50.1**; if it doesn't, the server or its web service is down — restart services from the maintenance menu. If the dashboard loads but Auto-Check still fails, restart the services and try again.
- *The dashboard loads but only partly — some tiles or pages are missing or error.* That's usually an **optional service** that isn't running (Kiwix, map tiles, Pat, or Direwolf), or one that needs a restart. Check service status from the maintenance menu (choice 3). A service you never installed will always look "down" — that's expected, not a fault. Restart the ones you do use with choice 1.
- *An update fails, or won't run because there's no internet.* Updates and data refreshes need the server to be **online**, which it usually isn't in the field. Wait until the server is back at home base with internet, then run the update there. If an update ran but a service didn't come back, use the maintenance menu to **Restart all services** (choice 1) and re-check status (choice 3).
- *I plugged in the backup drive and nothing happened.* The volume label must be exactly **FIELDCOMMAND** in all capital letters — this is the single most common cause. Re-label the drive (`FIELDCOMMAND`) and re-insert it. Also make sure the drive is a standard USB drive the server can mount; give it a few seconds after inserting, then look for a dated folder under `/media/fieldcommand/backup/` to confirm the copy ran.
- *I'm not sure the backup actually worked.* After inserting a FIELDCOMMAND drive, a new folder named with the current date and time (like `20260812_143005`) should appear on the drive under `backup/`, containing a `data` folder and a `fieldcommand_backup.db` file. If those are there, the backup succeeded. If not, re-check the label and try again.


# 14. Troubleshooting the Installation

*One place to look when something in the build doesn't go to plan — organized by symptom, from won't-boot to no-Wi-Fi to printing, with the log locations that tell you what really happened.*

> **QUICK VERSION** — Find your symptom below and try the fixes in order — most install problems are one of a handful of well-known things: a boot order pointing at the wrong drive, a loose second drive, a network cable or static-IP mismatch, or a service that just needs a restart. When a fix isn't obvious, jump to the last section, **Where to Find the Logs**, capture the two log files it names, and you'll have exactly what's needed to get help.


## What This Is / What It Is For

Building the server usually goes smoothly, but hardware is hardware and networks are networks — sometimes a drive doesn't seat, a cable is loose, or a setting doesn't take on the first try. This chapter gathers the problems people actually hit during an install into one scannable place, grouped by what you're seeing on screen. Each group is a short list of "if this, then try that" fixes, ordered from the most likely cause to the least.

Work top to bottom within your symptom group: the first fix listed is the most common cause, so trying them in order usually gets you there fastest. If nothing here solves it, the final section tells you exactly which log files to capture — those are what turn a frustrating guess into a quick diagnosis.

> **THIS CHAPTER IS ALL TROUBLESHOOTING** — Every other chapter ends with its own short Troubleshooting list for that chapter's task. This chapter is the opposite — it's *all* troubleshooting, pulled together across the whole install, so you have a single page to scan when you're not sure which step the problem belongs to. It ends not with a Troubleshooting section but with **Where to Find the Logs**.


## Boot Problems


### The Pi boots to the microSD card instead of the drives

- This is normal *during* the build — the card is what runs the setup that creates the mirror. It's only a problem *after* the build, when the Pi should be booting from the mirrored solid-state drives (SSDs) but keeps coming up on the card.
- *First, check the boot order.* The Pi 5 tries devices in a set order. After the mirror is built you want it to prefer the drives. If the card is still inserted and takes priority, the simplest fix is to shut down, remove the microSD card, and power back on — with no card present, the Pi boots the drives.
- *If it still won't boot without the card,* the mirror's boot files may not have been put in place. Re-insert the card, boot it, and re-run the one-command setup; it detects the existing mirror and repairs the boot configuration rather than rebuilding from scratch.
- *Confirm which device you actually booted.* If you're unsure whether you're on the card or the drives, the setup script itself will tell you — it refuses to build a mirror while running from the drives, and says so plainly.


### The Pi won't boot at all (no dashboard, no display activity)

- *Give it time.* The very first boot after the install does extra work (it finishes installing and configuring FieldCommand). Allow several minutes before deciding it's stuck.
- *Check power.* The Pi 5 needs its official 27-watt USB-C power supply. An underpowered supply or a thin cable causes random failures to boot. Use the recommended supply.
- *Re-seat the microSD card* (if you're booting from it) — a card not fully home is a common no-boot cause.
- *Try a monitor and keyboard.* Connecting a display shows you where it stops. If you see boot text that halts, note the last lines — they point at the failing step and match an entry in the logs.


## Drive Problems


### Only one drive is seen

- *On the first setup run this is expected.* The setup switches on the setting that lets the Pi see both drives behind the expansion board, then reboots once. Run the same command again after that reboot and it should see both.
- *If it still sees only one after that reboot, it's hardware seating, not software.* Power off completely, then firmly re-seat both SSDs in their slots and check that the enclosure's PCIe (Peripheral Component Interconnect Express — the internal expansion connection) ribbon or board is fully home. Loose seating is the number-one cause of a missing second drive.
- *Swap slots to isolate a bad drive.* If one drive is never seen no matter which fixes you try, move it to the other slot. If the fault follows the drive, that drive (or its slot connector) is suspect; if it stays with the slot, the slot or cable is suspect.


### The mirror is degraded, or rebuilding

- *"Degraded" means the mirror is running on one drive.* That's the mirror doing its job — the server keeps working — but you've lost the redundancy until it's repaired. This is exactly the state you saw on purpose during the pull-a-drive test.
- *"Rebuilding" (or "resyncing") means it's copying data back onto a returned or replaced drive* to restore the two-identical-copies state. This happens automatically after you re-insert a drive. Let it finish — it can take a while on large drives, and the server stays usable throughout.
- *If a drive genuinely failed,* power off, replace it with a same-size (or larger) blank SSD, power back on, and the mirror rebuilds onto the new drive on its own. Don't remove the *good* drive — that's the one holding all your data.
- *Don't panic at a degraded state after a power loss.* A hard power-off can leave the mirror briefly out of step; it re-syncs on its own at the next boot.


## Can't Reach the Dashboard at 192.168.50.1

- *Confirm you're on the right Wi-Fi.* Your device must be joined to the FieldCommand network named **EMCOMM-NET**, not your home or phone network. Check the Wi-Fi indicator and reconnect if needed.
- *Type the address exactly, with `http://`.* Use **http://192.168.50.1** — not `https://`, and no `www`. Some browsers hide the `http://` or try to search instead; type the full address into the address bar.
- *Check your device got an address.* When properly connected, your phone or laptop should have an address starting `192.168.50.` If it has something else, it isn't really on the FieldCommand network — forget the network and rejoin.
- *The server's static IP may not be set.* The FieldCommand Pi must hold the fixed address **192.168.50.1**. If the dashboard is unreachable from a device that *is* on EMCOMM-NET, the Pi may not have taken its static address — reboot the Pi, and if it persists, re-check the network configuration step from the earlier chapters.
- *Try a different device.* If one laptop can't reach it but a phone can, the problem is that laptop's network settings, not the server.
- *Restart the web service.* If devices are on the network and addressed correctly but still get nothing, the web server may be down. On the Pi, run `sudo bash /opt/fieldcommand/scripts/update.sh` and choose **3) Check service status**, then **1) Restart all services**.


## No Wi-Fi, or a Mesh Node Won't Pair

- *No EMCOMM-NET network appears at all.* The Wi-Fi access point service may not have started. On the Pi, check service status from the maintenance menu (`update.sh`, choice 3) and restart services (choice 1). Confirm the router/access-point hardware is powered.
- *Wrong Wi-Fi password.* The default access-point password is set during install. If devices see EMCOMM-NET but can't join, you're likely typing the wrong password — re-check what was set during setup.
- *A mesh node won't pair or link.* The standard deployment uses wired backhaul between the main router and its nodes through the network switch. First confirm the CAT-6 cable from the switch to each node's LAN port is fully seated at both ends and the node is powered.
- *Pair the node the manufacturer's way.* Mesh nodes link to the primary router via the router's own pairing process (its app or web page), not through FieldCommand. If a node won't join, follow the router maker's pairing steps, then confirm the node hands out addresses in the `192.168.50.x` range.
- *Move the node closer for the first link,* then place it where you need it. An initial pairing sometimes needs the node near the primary router even when the final position is farther away.


## Printing Problems (CUPS)

FieldCommand prints ICS forms and maps through **CUPS** (the *Common UNIX Printing System*), the standard Linux printing service. Most printing issues are the printer not being added yet or not being reachable on the network.

- *Add the printer first.* Open the CUPS admin page in a browser on the server at **http://192.168.50.1:631**, choose to add a printer, and pick your model. Until a printer is added, nothing will print.
- *Confirm the printer is on the network.* A Wi-Fi or Ethernet printer must be on the same network the server can reach. Print a test page from CUPS once it's added.
- *Use a network or USB connection the Pi supports.* Recommended printers have full Linux/CUPS support; confirm yours is connected by USB to the Pi or reachable over the network.
- *Restart the printing service.* If a previously working printer stops, restart CUPS on the Pi and try the test page again. Check that the printer has paper and isn't showing its own error.
- *Discovery not finding the printer.* Network printer auto-discovery uses a service called Avahi; if the printer doesn't appear automatically, add it by its address in the CUPS page instead of waiting for discovery.


## Offline Data Missing (Map Tiles and Kiwix)

- *Maps are blank or gray.* The offline map tiles (served on port **8083**) may not have been downloaded during setup, or the tile service isn't running. These downloads are optional and large, so they're sometimes skipped. Confirm the tile service is running (maintenance menu, choice 3) and that tiles were downloaded for your area.
- *The offline library (Wikipedia, medical, reference) won't open.* That's Kiwix, served on port **8081**. If **http://192.168.50.1:8081** doesn't load, either the Kiwix service is down or no offline books (ZIM files) were downloaded. The installer can add the service without the downloads, so an empty library means the books still need fetching.
- *Re-run the specific downloader.* Map tiles and Kiwix books each have their own setup step you can run later, on your own schedule, when the server has internet — these don't require rebuilding anything.
- *Remember these are optional.* If your group doesn't use offline maps or the reference library, these services being empty or off is expected and harmless — it does not mean the install failed.


## The First-Boot Installer Didn't Run

- *Symptom: the mirror was built and the Pi rebooted, but FieldCommand isn't installed* (the dashboard doesn't come up even though you're on the network and addressed correctly).
- *Give it time on that first boot.* The automatic install runs *on the first boot into the mirror* and takes several minutes. Watch a connected monitor — you should see it working through the install. Don't power it off mid-install.
- *Re-run the installer by hand.* If the first-boot install truly didn't fire, you can run it directly on the Pi: `sudo bash /opt/fieldcommand/scripts/install.sh`. It installs the services, web server, and configuration the same way the automatic run would.
- *Check the setup log for where it stopped.* The one-command build writes a log (see the next section). Its last lines show which stage it reached, so you can tell whether the mirror finished but the install didn't start.


## Where to Find the Logs

When a fix above doesn't solve it, the logs tell you what really happened — which step ran, which failed, and the exact error. Capturing these two files (and, for a specific service, its journal) gives whoever helps you everything they need. There's no guessing once you have the log.

| Log | Where it is | What it covers |
| --- | --- | --- |
| **Setup log** | `/var/log/fieldcommand-setup.log` | The one-command build: bootloader update, seeing both drives, building the mirror, copying the OS, and kicking off the first-boot install. Start here for boot and drive problems. |
| **Install log** | `/var/log/fieldcommand-install.log` | The FieldCommand installer itself: services, web server, Wi-Fi access point, FCC database, printing, and optional data. Start here for service, network, and printing problems. |
| **Per-service journal** | `journalctl -u <service> -n 50` | The recent output of one specific service. Swap in the service name — for example `journalctl -u fcc-lookup -n 50`, `journalctl -u nginx -n 50`, or `journalctl -u direwolf -n 50`. |

To read a log on the Pi, use `sudo tail -n 50 /var/log/fieldcommand-setup.log` (shows the last 50 lines) or `sudo less /var/log/fieldcommand-setup.log` (scroll with the arrow keys, press `q` to quit). Two more specialized logs exist if you're chasing those specific downloads: **`/var/log/fieldcommand-tiles.log`** for offline map tiles and **`/var/log/fieldcommand-kiwix.log`** for the offline library.

> **GETTING MORE HELP — CAPTURE THESE FIRST** — Before you reach out for help, grab the **last 50 lines** of both **`/var/log/fieldcommand-setup.log`** and **`/var/log/fieldcommand-install.log`**, plus the status list from the maintenance menu (`sudo bash /opt/fieldcommand/scripts/update.sh`, choice **3) Check service status**). Note your symptom in one plain sentence — what you did, what you expected, what you saw. That small bundle usually turns a hard-to-describe install problem into a quick, specific answer.

> **A SERVICE THAT WON'T STAY UP** — If the status list shows a service that keeps stopping, its journal is the fastest way to see why: run `journalctl -u <service> -n 50` with that service's name. The last lines almost always name the actual cause — a missing file, a permission problem, or low disk space (check free space with `df -h /`). Fix that root cause rather than just restarting in a loop.


# 15. AMPRNet / 44Net Gateway (Optional)

*How to set up the optional second Raspberry Pi that connects your whole field network to the worldwide amateur-radio internet — the Amateur Packet Radio Network — and how to check that the tunnel is up.*

> **QUICK VERSION** — On the **separate gateway Pi** (not the FieldCommand server), run **`sudo bash setup_44net.sh`**. Answer a few questions — the gateway's address (`192.168.50.2`), your router's address, and the three values you copied from the AMPRNet portal (your assigned `44.x.x.x/29` address, your WireGuard private key, and the gateway public key). It installs everything, then tells you to finish three short steps: paste your credentials into the config, run **`sudo wg-quick up ampr0`**, and add one route on your router. Check the **AMPRNet Gateway** page in FieldCommand to see a green **TUNNEL UP**.

> **THIS ENTIRE CHAPTER IS OPTIONAL — AND FOR LICENSED HAMS ONLY** — Everything in Part 2, including this chapter, is **completely optional**. If your group is a public-safety agency, a served agency, or any team **without a licensed amateur-radio operator**, you can **skip all of Part 2** — FieldCommand runs fully without it. The AMPRNet gateway connects your network to the amateur-radio internet, and that is only lawful for a properly licensed operator. Getting a 44Net address is tied to a valid **Federal Communications Commission (FCC)** amateur license. If nobody in your group holds one, stop here and move on to the rest of the guide.


## What This Is / What It Is For

The **Amateur Packet Radio Network (AMPRNet, also called 44Net)** is a worldwide internet built by and for licensed amateur-radio operators. It uses its own block of internet addresses — everything that begins with **44** (written `44.0.0.0/8`, meaning every address from 44.0.0.0 through 44.255.255.255). Stations on this network can reach each other directly for things like Winlink email over radio paths, the **Automatic Packet Reporting System (APRS)** position network, and data links between field sites — all inside the amateur-radio community rather than over the ordinary commercial internet.

By itself, a FieldCommand server does not touch AMPRNet. This chapter adds an **optional second Raspberry Pi** — a dedicated **gateway** — whose only job is to build a secure tunnel out to the AMPRNet and pass traffic back and forth. Once it is running, **every device on your EMCOMM-NET Wi-Fi** can reach any 44Net address in the world, without each device needing its own setup.

> **THE GATEWAY PI IS A SEPARATE COMPUTER FROM THE SERVER** — This is the single most important thing to understand in this chapter. The **44Net gateway runs on its own Raspberry Pi 5**, with its own address **192.168.50.2**. It is **not** the FieldCommand server (that is a different Pi at **192.168.50.1**). The two never share software. The gateway Pi runs only three things — the tunnel, the routing between the two networks, and a small status page. If the gateway Pi is switched off, FieldCommand keeps working exactly as before; you simply lose the 44Net connection until it comes back.


## How the Gateway Works, in Plain Words

The gateway does three jobs, and it helps to picture each one:

| Job | What it means | Why it matters |
| --- | --- | --- |
| **The tunnel** | A private, encrypted pipe (built with software called **WireGuard**) runs from the gateway Pi out across the ordinary internet to the AMPRNet's own gateway server, `amprgw.ampr.org`. Inside FieldCommand this pipe is the network interface named **`ampr0`**. | It is how a Pi sitting on your local network becomes a real, addressable member of the worldwide 44Net. |
| **The routing** | The gateway passes traffic between your local **EMCOMM-NET** side and the **44Net** side, so a laptop on your Wi-Fi can talk to a 44 address and the replies find their way back. | Without routing, the tunnel would exist but only the gateway Pi itself could use it. Routing shares it with everyone. |
| **The status page** | A small web page on the gateway (at **http://192.168.50.2:9000**) shows whether the tunnel is up, your assigned address, data moving through, and the gateway Pi's health. FieldCommand also mirrors this on its own **AMPRNet Gateway** page. | It is how you confirm — at a glance, with no typing of commands — that everything is working. |

> **"WIREGUARD" AND "TUNNEL" MEAN THE SAME THING HERE** — **WireGuard** is just the name of the modern, well-regarded software that builds the encrypted tunnel. When this chapter says "bring the tunnel up" or mentions **`ampr0`**, it is talking about the WireGuard connection to AMPRNet. You do not need to understand how it works to use it — you paste in three values from the portal and start it.


## Before You Start — Get Your 44Net Allocation

You cannot build the tunnel until the AMPRNet administrators have assigned you a small block of 44 addresses. This is a one-time registration and it is **not instant** — plan for it to take **two to four weeks**, so start it well before you need it. Do this part first; the software setup below takes only minutes once you have your numbers in hand.

1. Have your licensed operator go to the AMPRNet portal at **https://portal.ampr.org** and sign in using their **FCC callsign** as the username. The portal checks the license automatically against the FCC's records.
2. Contact your **regional AMPRNet coordinator** first — allocations are handled region by region. Your operator can find the right contact through their ARRL Section or the AMPRNet mailing list.
3. Request a small allocation (a `44.x.x.x/29` block is typical — that is a handful of addresses, plenty for one field site).
4. Wait for approval. When it comes, open the portal and go to **Subnets → My Subnets**, click your allocation, then open its **WireGuard Config**.
5. From that page, copy down **three things** and keep them safe: your assigned **`44.x.x.x/29` address**, your **WireGuard private key**, and the **AMPRNet gateway public key**. You will type all three into the setup below.

> **TREAT THE PRIVATE KEY LIKE A PASSWORD** — The **WireGuard private key** is the secret that proves your gateway is really yours. Do not email it around, post it, or store it where others can read it. Keep a printed copy with your station papers, and only type it into the gateway Pi during setup. If it is ever exposed, the portal can generate a new one.


## What the Setup Script Configures

All of the gateway software is installed by a single script named **`setup_44net.sh`**. You run it **on the gateway Pi**, and it works through everything for you. So you know exactly what it is doing, here is the full list — you do not have to act on any of it, it happens automatically:

- Installs the needed software: **WireGuard** (the tunnel), **Python** with **Flask** (for the status page), **iptables** (the routing rules), and a few small helpers.
- Creates a dedicated, limited system user named **`amprgate`** to run the status service safely.
- Turns on **IP forwarding** — the switch that lets the Pi pass traffic between your two networks (this is what makes the routing work).
- Writes the WireGuard tunnel configuration file at **`/etc/wireguard/ampr0.conf`**, filling in your portal values and the rules that route `44.0.0.0/8` through the tunnel.
- Sets the gateway Pi's fixed address to **192.168.50.2** on the wired network.
- Installs the **status page** and sets it to start automatically, reachable at **http://192.168.50.2:9000**.
- Sets up the firewall so the status page is reachable from your local network, while the sensitive tunnel-control port stays locked to the gateway Pi itself.
- Sets the tunnel and the status page to start again on their own every time the gateway Pi reboots.

> **WHAT THE SCRIPT ASKS YOU** — The setup pauses to ask five short questions. Each shows a sensible default in brackets — press Enter to accept it — except the three portal values, which only you have.

| It asks for | What to type | Default |
| --- | --- | --- |
| **Gateway Pi static IP** | Leave as the default unless your network is unusual. | `192.168.50.2` |
| **EMCOMM-NET gateway (router IP)** | Your router's address. Leave as the default for a standard FieldCommand kit. | `192.168.50.254` |
| **Your 44.x.x.x/29 allocated address** | The address block the AMPRNet portal assigned you. | (none — from portal) |
| **Your WireGuard private key** | The private key from the portal's WireGuard Config page. | (none — from portal) |
| **AMPRNet gateway public key** | The gateway public key from the same portal page. | (none — from portal) |

> **YOU CAN RUN THE SCRIPT BEFORE YOUR ALLOCATION ARRIVES** — If your `44` block has not come through yet, you can still run the setup to install everything — just leave the three portal fields blank. The script writes the config with placeholders and clearly warns you to fill them in later. When your allocation arrives, edit the config file (the last section of this chapter shows how) and bring the tunnel up. Nothing is wasted.


## Running the Setup

Sit down at the **gateway Pi** — the second Pi, not the FieldCommand server — with a monitor and keyboard connected. Open a **Terminal** window, and from the folder that holds the script, type this one line and press Enter:

```
sudo bash setup_44net.sh
```

The word **`sudo`** means "do this as the administrator"; it may ask for the Pi's password the first time. A banner appears, then the five questions above. Answer them, review the short summary it prints, and type **`Y`** to proceed. From there it installs and configures everything, printing each labeled step as it goes. When it finishes, it prints a list of manual finishing steps — covered next — and offers to reboot.

> **RUN THIS ON THE RIGHT PI** — This script is for the **dedicated gateway Pi only**. Do **not** run it on the FieldCommand server Pi (192.168.50.1). The script itself checks and expects to be the gateway, but the surest safeguard is simply to confirm you are sitting at the second Pi before you type the command.


## The Manual Finishing Steps

The script does the heavy lifting, but a few final steps need a human — mostly because they involve your secret credentials and your router. The script prints these on screen when it finishes; they are repeated here so you can follow along.


### 1. Add your credentials (only if you left them blank)

If you already typed your three portal values during setup, skip to step 2. Otherwise, open the config file and paste them in:

```
sudo nano /etc/wireguard/ampr0.conf
```

Replace the placeholder text on the **`PrivateKey`**, **`Address`**, and **`PublicKey`** lines with your real portal values. Save the file (in the `nano` editor, press **Ctrl+O** then Enter, then **Ctrl+X** to exit).


### 2. Start the tunnel

Bring the WireGuard tunnel up, then check it:

```
sudo wg-quick up ampr0
sudo wg show ampr0
```

The second command should show a recent **latest handshake** and some **transfer** figures — proof the gateway has reached the AMPRNet server. Because you enabled the tunnel to start at boot during setup, you only run `wg-quick up` by hand this one time; after a reboot it comes up on its own.


### 3. Tell your router about the 44Net route

One setting on your router lets every other device on EMCOMM-NET use the gateway automatically. On the standard FieldCommand ASUS router:

1. Open a browser to your router's admin page — **http://192.168.50.254** — and sign in.
2. Go to **LAN → Route → Add**.
3. Set **Network/Host IP** to **44.0.0.0**.
4. Set **Netmask** to **255.0.0.0**.
5. Set **Gateway** to **192.168.50.2** (the gateway Pi).
6. Set **Interface** to **LAN**, then click **Apply**.

> **WHAT THIS ROUTE DOES** — This single line tells the router, "any traffic headed for a 44 address, hand it to the gateway Pi at 192.168.50.2." Without it, only the gateway Pi itself could reach 44Net; with it, every laptop, tablet, and phone on your Wi-Fi can.


## Checking the Tunnel and Routing Are Up

You have three easy ways to confirm everything is working — pick whichever is handy.

- *From the gateway Pi itself:* run **`sudo wg show ampr0`**. A recent handshake and transfer numbers mean the tunnel is live.
- *From the FieldCommand server Pi:* run **`ping 44.0.0.1 -c 4`**. Replies from `44.0.0.1` (the AMPRNet gateway) mean traffic is routing all the way through.
- *From any device on EMCOMM-NET:* open FieldCommand's **AMPRNet Gateway** page in a browser. This is the easiest check and needs no commands.

The **AMPRNet Gateway** page in FieldCommand is the friendliest of the three. At the top it shows a big banner: a green **TUNNEL UP — AMPRNet Connected** when all is well, a red **TUNNEL DOWN** if the tunnel dropped, or an amber **Gateway Unreachable** if the gateway Pi is not responding at all (usually because it is switched off). Below the banner, cards show your assigned **AMPRNet address**, the **last handshake** time, **data received and sent**, and the gateway Pi's **temperature, memory, IP forwarding**, and **uptime**. Further down, an **Active Routes** table and a **Connected Peers** table confirm the routing, and an **Access Log** lists recent station identifications for your records. The page refreshes itself every 30 seconds.

> **THE TUNNEL CONTROL BUTTONS ONLY WORK AT THE GATEWAY PI** — The AMPRNet Gateway page shows **Bring Tunnel UP / DOWN / Restart** buttons, but for safety they only work when the page is opened **in the browser on the gateway Pi itself** (at `http://localhost:9001`), and only after a valid callsign login. From an operator's laptop or phone the page is **read-only** — you can watch the status but not change it. This is deliberate: it keeps a station-controlling function under the physical control of a licensed operator at the equipment. To restart the tunnel, sit at the gateway Pi, open its browser, log in with your callsign, and use the buttons there.

> **STAY WITHIN THE RULES (PART 97)** — Everything crossing the 44Net is amateur-radio traffic and is governed by the FCC's amateur rules (Part 97): no encryption of the **content** of messages, station identification as required, and amateur purposes only. (The tunnel's own encryption is fine — it protects the transport, not the message content, which is expressly allowed.) The licensed operator who owns the allocation is responsible for what passes through the gateway.


## Troubleshooting

- *The tunnel won't come up / `wg show` shows no handshake.* First, the three portal values are the usual cause — open `sudo nano /etc/wireguard/ampr0.conf` and confirm the **PrivateKey**, **Address**, and **PublicKey** lines hold your real values, not the `REPLACE_WITH...` placeholders. Save, then run `sudo wg-quick down ampr0` followed by `sudo wg-quick up ampr0`. Second, the gateway Pi needs a working internet path to reach `amprgw.ampr.org` — confirm the Pi can reach the internet at all.
- *The tunnel is up but nothing on the network can reach 44 addresses.* This is almost always the router route. Re-check **LAN → Route** on the router (http://192.168.50.254): Network **44.0.0.0**, Netmask **255.0.0.0**, Gateway **192.168.50.2**, Interface **LAN**. Also confirm IP forwarding is on — the FieldCommand AMPRNet Gateway page shows **IP Forwarding: ✓ Enabled** when it is; if it reads disabled, the setup did not finish cleanly, so re-run `setup_44net.sh`.
- *`ping 44.0.0.1` from the server Pi times out.* Work outward: is the tunnel up on the gateway (`sudo wg show ampr0`)? Is the router route in place? Is the gateway Pi's IP forwarding enabled? Each of the three must be true for traffic to reach 44Net.
- *The AMPRNet Gateway page shows amber "Gateway Unreachable."* The FieldCommand server cannot see the gateway Pi. Make sure the gateway Pi is **powered on** and plugged into the network (it is a separate computer and can be off even when the server is running). Confirm it holds address **192.168.50.2**.
- *The status page at http://192.168.50.2:9000 won't load.* The status service may not be running. On the gateway Pi, check it with `sudo systemctl status amprgate-status` and restart it with `sudo systemctl restart amprgate-status`. Also confirm you typed the gateway address (`.2`), not the server address (`.1`).
- *The tunnel keeps dropping after a while.* This is usually the internet link the tunnel rides on going up and down. The config already sends a keepalive every 25 seconds to hold the tunnel open through most home and cellular connections; if the underlying internet is genuinely unstable, the tunnel will follow it. It comes back on its own when the link returns.
- *I can't press the tunnel buttons from my laptop.* That is expected — the controls only work in the browser on the gateway Pi itself, after a callsign login. See the note above. Read-only status is available everywhere.


# 16. FCC Amateur Database & APRS (Optional)

*Turn on the offline database of every US amateur-radio license so you can look up any callsign in the field with no internet — and set up APRS so live station positions appear on the tactical map.*

> **QUICK VERSION** — **FCC database:** during the main setup, answer **Y** to "Download FCC database" (about 600 megabytes). Then open the **Callsign Lookup** page in FieldCommand, type a callsign, and press **Look Up** — name, license class, and address appear instantly, no internet needed. **APRS:** plug a USB **Terminal Node Controller (TNC)** into the Pi (it appears as **`/dev/tnc0`**), edit two lines in **`/etc/direwolf.conf`** (your sound device and your callsign), restart Direwolf, and live stations show up on the tactical map.

> **THIS CHAPTER IS OPTIONAL — AND TRANSMITTING NEEDS A LICENSE** — Like all of Part 2, this chapter is **optional** and aimed at groups with a licensed amateur-radio operator. The **offline FCC database is a read-only reference** and is handy to any group that logs hams during a net, licensed or not. But **APRS transmit** — sending your own position or relaying others — is on-air amateur operation and is only lawful under the control of a **properly licensed operator** with privileges on the band and mode used. A group with no hams can safely skip the APRS half of this chapter (and the database half too, if it never logs callsigns).


## What This Is / What It Is For

This chapter covers two independent amateur-radio features. You can turn on either one, both, or neither:

- *The offline FCC amateur license database* — a full local copy of the **Federal Communications Commission (FCC)** records for roughly **800,000 US amateur licensees**, so you can look up any callsign instantly, even with no internet.
- *APRS* — the **Automatic Packet Reporting System**, the amateur network that carries station positions, weather, and short messages over the air. With a small piece of hardware and a radio, live station positions appear on FieldCommand's tactical map.

They share this chapter because both are amateur-radio tools, but they do not depend on each other. Set up whichever your group needs.


## The Offline FCC License Database

When a net-control operator types a callsign into a check-in field, it is enormously helpful to see the operator's name, license class, and town immediately — to confirm the person is who they say, to fill an ICS form correctly, or just to greet a new check-in by name. Online lookup services do this, but in a real activation you often have **no internet**. FieldCommand solves that by keeping the **entire FCC amateur database on the server's own drives**, so a lookup returns in well under a second whether or not there is any connection to the outside world.

> **WHY OFFLINE MATTERS IN THE FIELD** — The whole point of FieldCommand is to keep working when the normal internet is down — that is exactly when an emergency net is running. A callsign lookup that needs the internet is useless in a blackout. Holding all 800,000 records locally (about 600 megabytes on the mirrored drives) means the lookup is always available, and always fast.


### Turning the Database On

The easiest time to enable the database is during the main one-command setup (covered earlier in this guide). When it asks **"Download FCC database"**, the default is **N**, but the recommended answer is **Y**. Answering **Y** downloads and builds the database as part of the install — it needs an active internet connection for a few minutes while it runs.

If you skipped it during setup, or you want to rebuild it later, you can build it by hand. On the FieldCommand server Pi, open a Terminal and run:

```
# Build (or rebuild) the FCC database — needs internet, takes about 5-10 minutes:
sudo -u fieldcommand \
  /opt/fieldcommand/venv/bin/python \
  /opt/fieldcommand/python/build_fcc_db.py
```

The build takes roughly **5 to 10 minutes** on a Raspberry Pi 5 and requires internet **only while it runs** — once built, the lookup itself never needs a connection. FieldCommand also keeps the data current on its own: a weekly refresh timer updates the records automatically. You can check or force it:

```
# See the automatic weekly refresh timer:
sudo systemctl status fcc-refresh.timer
# Force an immediate refresh (needs internet):
sudo systemctl start fcc-refresh.service
```

> **HOW TO TELL IT'S READY** — In FieldCommand, the **Preflight → Data Readiness** screen has an **FCC Callsign Database** line showing how many records are loaded and how old they are. A healthy record count (hundreds of thousands) and a recent date mean the lookup is ready. If it shows zero records, the database was never built — run the build command above.


### Using the Callsign Lookup Page

Open the **Callsign Lookup** page from the FieldCommand dashboard (or the top navigation bar). It has two ways to search:

| Feature | How to use it | What you get |
| --- | --- | --- |
| **Single lookup** | Type a callsign in the big box and press **Enter** or click **Look Up**. | One result card: the callsign, license class (Technician, General, Extra, and so on), Active/Expired status, name, city and state, ZIP, grant and expiration dates, FRN, license ID, and grid square if known. |
| **Advanced search** | Fill any of Last/Entity Name, First Name, State, License Class, City, or Grid Square, then click **Search**. | A table of every matching licensee (up to 100). Click any callsign in the table to open its full result card. |
| **Recent lookups** | Nothing to set up — the page remembers callsigns you looked up and shows them as quick buttons. | One click re-opens a recent callsign, handy during a busy net. |

From a result card you can also add the operator straight to your incident **roster**, or copy the callsign to the clipboard. The net-control loggers use the same database behind the scenes, so callsigns you enter there fill in the operator's details automatically.


## APRS — Live Positions on the Map

APRS is the amateur network that carries short bursts of data — most usefully, **where stations are**. With APRS working, the tactical map shows live markers for participating stations as they report in: mobile units, portable operators, weather stations, and digipeaters. FieldCommand builds this from two free programs plus one small piece of hardware.

| Piece | What it is | What it does here |
| --- | --- | --- |
| **Direwolf** | A **software TNC** — a **Terminal Node Controller** done in software instead of a separate box. | It listens to the radio's audio and decodes the APRS data packets (and encodes yours to transmit). It is the engine; it has no screen of its own. |
| **A USB TNC** | A small hardware adapter (Digirig Mobile or SignaLink USB) between the Pi and the radio. | It carries audio both ways between the Pi and the transceiver and keys the radio to transmit. Direwolf needs it to hear and speak to the radio. |
| **YAAC** | "Yet Another APRS Client" — an optional Java program that can run on the Pi. | An on-Pi APRS display, if you want one. It is optional; the tactical map is the main way FieldCommand shows APRS. |

> **MOST OF THIS IS ALREADY INSTALLED** — The FieldCommand installer sets up **Direwolf** and **YAAC** for you, writes a starter **`/etc/direwolf.conf`**, and enables the Direwolf service. So in the normal case you do not install anything here — you connect the TNC and edit two lines of the config. The manual install steps exist only as a fallback if the automatic install failed.


### Connecting the USB TNC

Plug your USB TNC — a **Digirig Mobile** or a **SignaLink USB** — into one of the Pi's USB ports (or a powered USB hub). FieldCommand gives it a stable, predictable device name so software always finds it in the same place:

```
ls -la /dev/tnc0
```

The name **`/dev/tnc0`** always points to your TNC, no matter which USB port you use or what else is plugged in. FieldCommand sets this up with a **udev rule** — a small system rule that recognizes the TNC by its identity. This matters because a common USB GPS receiver uses the very same chip inside as the Digirig; the rules are written to tell them apart so your GPS never gets mistaken for your TNC or the other way around. Your radio then connects to the TNC with the audio and keying cable made for your specific transceiver.

> **GET THE RIGHT CABLE FOR YOUR RADIO** — The TNC needs a radio-specific cable to reach your transceiver. For a **Digirig**, order the cable for your exact radio model from **digirig.net**. For a **SignaLink USB**, order the matching Tigertronics cable for your rig. The wrong cable is the most common reason a freshly connected TNC hears nothing.


### Configuring Direwolf (First Run)

Direwolf needs to know two things: which sound device is your TNC, and what callsign to identify with. Set them once:

1. Find your TNC's sound device. Run **`arecord -l`** and note the **card** and **device** numbers it lists for the TNC (for example, card 1, device 0).
2. Open the config for editing: **`sudo nano /etc/direwolf.conf`**.
3. Set the **`ADEVICE`** line to your sound device — for card 1, device 0 that is **`plughw:1,0`**.
4. Set the **`MYCALL`** line to your callsign with an APRS suffix (an **SSID**), for example **your club callsign-5**. The suffix is a number that labels this particular station.
5. Save and exit (in `nano`: **Ctrl+O**, Enter, then **Ctrl+X**), then restart Direwolf: **`sudo systemctl restart direwolf`**.

> **RECEIVE FIRST, TRANSMIT ONLY WHEN LICENSED AND READY** — Out of the box Direwolf is **receive-only** — it listens and decodes but never keys the radio. That is the safe way to start: you can confirm everything works by watching stations decode, with no transmission at all. **Transmitting** (acting as an iGate or a digipeater, or beaconing your own position) is on-air amateur operation. Only enable it if a **licensed operator** is in control, and configure the keying method (PTT) in the config — by GPIO pin, CM108 sound-card keying, or rig control — to match your TNC and radio.


### Feeding the Tactical Map

Direwolf decodes packets but does not draw the map itself. You point the map at whatever reads Direwolf's output. In FieldCommand, open **Tactical → Settings → APRS Sources** and choose the source that matches your setup:

| Source | Connects to Direwolf via | Map setting |
| --- | --- | --- |
| **APRS Command (Windows laptop)** | KISS on TCP port **8001**, or AGW on port **8000**, over EMCOMM-NET | Set the RF source host to the laptop's IP address |
| **Pi-side KISS bridge (optional)** | KISS on **localhost:8001** | Set the RF source host to **localhost** — lets the map work without the laptop |
| **APRS-IS internet (only if online)** | the internet APRS-IS network | Turn on the APRS-IS layer on the map |

Once a source is feeding it, stations decoded off the air appear as markers on the tactical map and update as new packets arrive.

> **THE LIVE APRS FEED IS CARRIED OVER SECURE HTTPS FOR YOU** — Because FieldCommand now serves everything over secure **HTTPS** (see the connect chapter), the tactical map's live APRS feed is passed through the web server automatically at the addresses **`/aprs-gw/`** and **`/aprs-yc/`**. You normally do nothing for this — it just works. It matters only in one case: if your **APRS gateway** (the radio-facing gateway, such as **YAAC**) runs on a **different computer** than the FieldCommand server — for example, on the operations laptop — then those two feeds need to be told where to find it. Whoever builds the server edits the two **`proxy_pass`** lines for `/aprs-gw/` and `/aprs-yc/` in the web-server (nginx) configuration so they point at that other computer's address, then restarts the web server. If the gateway runs on the FieldCommand server itself (the usual case), leave these alone.


### Verifying APRS Is Working

Two quick checks confirm the chain is alive. On the server Pi:

```
# Watch Direwolf decode packets off the radio in real time:
journalctl -u direwolf -f
# Confirm the KISS/AGW ports are listening:
ss -tlnp | grep -E "8000|8001"
```

If a nearby station or digipeater is active, the first command scrolls decoded packets as they arrive — that is your proof the TNC, radio, and Direwolf are all working together. The second command should list ports **8000** and **8001** as listening, which is what the map connects to.


## Troubleshooting

- *The Callsign Lookup page finds nothing / every callsign is "not found."* The database was probably never built. Open **Preflight → Data Readiness** and check the **FCC Callsign Database** record count; if it is zero, run the build command shown above. Remember the build needs internet while it runs (but not afterward).
- *Lookup says "Could not reach local FCC database."* The lookup service is not answering. On the server Pi, check it is alive with **`curl http://localhost:5050/health`**. If that fails, the database service needs restarting — the lookup runs on port 5050 of the FieldCommand server.
- *A callsign really isn't in the database.* The database holds **US** amateur licensees and is refreshed weekly. A brand-new license, a recent change, or a non-US callsign may not be present yet. Force a refresh with **`sudo systemctl start fcc-refresh.service`** (needs internet), or search by name in Advanced Search.
- *The TNC isn't detected / `/dev/tnc0` is missing.* Run **`ls -la /dev/tnc0`** — if nothing is there, unplug and replug the TNC, and confirm it is a supported unit (Digirig Mobile or SignaLink USB). If a USB GPS is also plugged in, make sure each shows up separately (`/dev/gps0` and `/dev/tnc0`); the udev rules keep them distinct, but a truly unknown adapter may not match either rule.
- *No APRS packets are decoded.* Work through the chain from the radio inward. Is the radio on the right APRS frequency and turned up? Is the correct radio-specific cable connecting the TNC to the radio? In **`/etc/direwolf.conf`**, does **`ADEVICE`** match the card/device from **`arecord -l`**? Watch **`journalctl -u direwolf -f`** while a known station is active — silence there points to audio or cabling; scrolling gibberish points to audio levels (next item).
- *Audio levels are wrong (garbled or no decode).* APRS is fussy about receive audio level. Too low and Direwolf hears nothing; too high and packets are distorted and fail to decode. Adjust the radio's volume and the TNC's input level a little at a time, watching the decode log until clean packets appear.
- *Direwolf won't transmit.* Transmit is off until you configure keying (PTT) in **`/etc/direwolf.conf`** and only under a licensed operator's control. Confirm the PTT method (GPIO, CM108, or rig control) matches your hardware, and that your radio is actually able to transmit on the frequency in use.
- *The map shows no stations even though Direwolf is decoding.* The map is not pointed at the feed. In **Tactical → Settings → APRS Sources**, set the source and host to match your setup (see the table above), and confirm ports **8000/8001** are listening with **`ss -tlnp | grep -E "8000|8001"`**.


# 17. Winlink — Pat, Winlink Express & JS8Call (Optional)

*Email over the radio, for when the internet is down — the browser-based Pat client built into the Pi, and the Windows-laptop station running Winlink Express, VARA HF, and JS8Call.*

> **QUICK VERSION** — Winlink is **email carried over the radio** when the internet is gone. Two paths come with FieldCommand. **On the Pi:** a browser Winlink client called **Pat** is already installed — reach it at **http://192.168.50.1:8090**, add your Winlink password, done. It's the backup. **On a Windows laptop (the primary HF station):** install **Winlink Express + VARA HF** and **JS8Call**, plug an HF radio like an **IC-7300** in with one Universal Serial Bus (USB) cable, and the FieldCommand dashboard's JS8Call card opens the laptop's JS8Call screen. Then send one test message to prove it works.

> **THIS WHOLE CHAPTER IS OPTIONAL — HAM GROUPS ONLY** — Part 2 of this guide is only for groups that include a **licensed amateur-radio operator**. If nobody in your organization holds an amateur-radio license, **skip this chapter entirely** — FieldCommand runs fully without it. Transmitting on the amateur bands is **against the law without a proper license**, and every mode here (Winlink over radio, VARA HF, JS8Call) must be operated by someone licensed with privileges on the bands and modes being used. Nothing in this chapter changes that.


## What This Is / What It Is For

**Winlink** is a worldwide system that sends and receives email **over amateur radio** instead of over the internet. When the power grid is up and the internet is working, email is easy. During the exact emergencies FieldCommand is built for — a hurricane, an ice storm, a wide-area outage — the internet is often the first thing to fail. Winlink keeps a real email path alive by carrying those messages on radio waves, from your station to a **Radio Message Server (RMS)** gateway that is still on the internet, and out to the normal email world from there.

For an incident, that means you can still get a formal Incident Command System (ICS) message, a resource request, or a health-and-welfare note out of the disaster area even when cell towers and broadband are dead. It is slower than broadband and it is text-first, but it works when nothing else does — which is the whole point.

FieldCommand gives you Winlink **two** ways, and they back each other up:

- *Pat, on the Pi.* A small Winlink program called **Pat** is already installed on the FieldCommand server. You use it from any web browser on the field Wi-Fi — there is nothing to install. It is the **backup** path, and it is handy for Very High Frequency (VHF) Packet when a modem is plugged straight into the Pi.
- *A Windows laptop.* A separate Windows laptop running **Winlink Express** (the standard Winlink program most operators know) plus the **VARA HF** modem and **JS8Call**. This is the **primary** High Frequency (HF) digital station, connected to an HF radio such as an Icom IC-7300.

> **WHO DOES THIS** — This is set up once, by the licensed operator who owns the radio gear, before the equipment goes to the field. Everyone else just uses the finished station. You do **not** need to touch this to use the rest of FieldCommand.


## The Pi's Built-in Winlink Client — Pat on Port 8090

**Pat** is an open-source Winlink program that runs directly on the FieldCommand Pi. Because it lives on the server, you reach it from a browser on any device joined to the field Wi-Fi — no software to load on your laptop or phone. The FieldCommand installer downloads and configures Pat for you, so this section is mostly about **checking that it is running** and **adding your personal Winlink password** so you can log in to the Winlink system.

Pat is served on **port 8090**. A "port" is just a numbered doorway on the server; you reach a specific program by adding the port number after a colon at the end of the address. So the full address for Pat is the normal server address with **`:8090`** on the end.

> **WHY PAT IS THE BACKUP, NOT THE MAIN STATION** — For most groups the **Windows laptop** (next section) is the primary Winlink station, because Winlink Express plus VARA HF is the combination the wider Winlink community uses and supports. Pat on the Pi is the **fallback** — for when the laptop is unavailable, or for VHF Packet with a modem wired straight to the Pi. Set both up; lean on the laptop.


### Reaching Pat and Adding Your Password

1. On any device joined to the field Wi-Fi, open a web browser.
2. Go to **http://192.168.50.1:8090** — type it exactly, including the `http://` and the `:8090` on the end. The Pat inbox screen opens.
3. If the page does not open, the Pat program may not be running. On the Pi, open a Terminal and check it with the commands below, then try the address again.
4. Add your Winlink account password so Pat can log in. On the Pi, open Pat's configuration file with the editor command shown below, type your Winlink password into the `secure_login_password` line, save, and restart Pat.

```
# On the Pi — check that Pat is running and listening on port 8090:
sudo systemctl status pat
# If it is not running, start it and set it to start on every boot:
sudo systemctl start pat && sudo systemctl enable pat
# Confirm the port is open:
ss -tlnp | grep 8090

# Add your Winlink password (opens the config file in a simple editor):
sudo nano /opt/fieldcommand/.config/pat/config.json
#   "secure_login_password": "xxxxx"   <- put your Winlink password here
#   "http_addr": "0.0.0.0:8090"        <- leave as 0.0.0.0 so the field Wi-Fi can reach it
# Save (Ctrl+O, Enter) and exit (Ctrl+X), then restart Pat:
sudo systemctl restart pat
```

> **THE ADDRESS MUST STAY 0.0.0.0, NOT 127.0.0.1** — In Pat's config, the `http_addr` line must read **`0.0.0.0:8090`**. The `0.0.0.0` part means "let other devices on the Wi-Fi reach me." If it is ever changed to `127.0.0.1`, Pat will only answer on the Pi itself and the browser page at `http://192.168.50.1:8090` will fail to load from anywhere else. Leave it as `0.0.0.0`.


## The Windows Laptop — Why It's the Primary HF Station

The primary High Frequency (HF) digital station is a **Windows laptop** connected to an HF transceiver — in the reference build, an **Icom IC-7300**. Why a Windows laptop instead of doing everything on the Pi? Because the two programs most Winlink HF operators rely on — **Winlink Express** and the **VARA HF** modem — are Windows programs, widely used and well-supported across the amateur community. Running them on the platform they were built for is the least-surprising, most-reliable path, so FieldCommand treats the laptop as the main station and Pat on the Pi as the backup.

The laptop joins the same field network as everything else — either on the **EMCOMM-NET** Wi-Fi or plugged into the network switch with an Ethernet cable. That shared network is what lets the FieldCommand dashboard reach the laptop's JS8Call program later on.


### Connecting the Laptop to the Radio (One USB Cable)

The IC-7300 connects to the laptop with a **single USB cable**. That one cable carries both the radio's audio (so the computer can hear and speak the digital tones) and the radio's control channel (so the computer can set the frequency and key the transmitter). Before the software will work, set a handful of one-time options in the radio's menus:

| IC-7300 menu path | Setting | What it does |
| --- | --- | --- |
| SET → Connectors → CI-V Baud Rate | 115200 | How fast the laptop talks to the radio's control channel. Must match the software. |
| SET → Connectors → CI-V Transceive | ON | Lets the radio and software keep each other in step on frequency and mode. |
| SET → Connectors → USB Send/Keying → USB Send | RTS | Chooses which control line keys the transmitter (Push To Talk, or PTT) over USB. |
| SET → Connectors → MOD Input → USB MOD Level | 40–50% | How loud the computer's audio is fed into the radio. Too high causes distortion. |
| COMP button (speech compression) | OFF | Compression is for voice; it garbles digital tones. Turn it off for data. |
| Mode (for digital operation) | USB-D | The correct sideband/data mode for Winlink and JS8Call. |


## Install Winlink Express + VARA HF

**Winlink Express** is the standard Windows program for sending and receiving Winlink email. **VARA HF** is the **modem** — the software that turns your message into the warble of tones the radio transmits, and turns received tones back into text. You need both. Install Winlink Express first, then VARA HF.

1. Download Winlink Express from **winlink.org/client-software**. Run the installer and accept the defaults.
2. On first launch, enter your **callsign**, your **Winlink password**, and your **grid square** (a short location code for your county).
3. Go to **Settings → Radio Setup**. Set **Radio = IC-7300**, **Control Port =** the COM port shown for the radio (check Windows Device Manager if unsure), **Baud Rate = 115200**, and tick **PTT via CAT**.
4. Go to **Settings → Sound Card**. Set both **Input** and **Output** to **USB Audio CODEC (IC-7300)** — that is the radio's built-in sound device.
5. Download and install **VARA HF** from **winlink.org → VARA → VARA HF Modem**. In VARA HF's own Settings, choose the **same** audio devices you set above.
6. Test it: open a **VARA HF session** in Winlink Express and connect to any Winlink RMS gateway on the 40-meter band to confirm the audio and radio control are working (see "Verifying a Connection" below).

> **WHAT'S A 'COM PORT'?** — When you plug the radio in, Windows gives its control channel a name like **COM5**. That is the "Control Port" the software asks for. If you are not sure which one it is, open **Device Manager**, expand **Ports (COM & LPT)**, and look for the Silicon Labs or IC-7300 entry — the number in parentheses is your COM port. Use the **same** COM port in Winlink Express and in JS8Call.


## Install JS8Call and Wire It to the Dashboard

**JS8Call** is a keyboard-to-keyboard HF messaging program — think of it as slow, extremely weak-signal text chat that gets through when voice cannot. FieldCommand's dashboard has a **JS8Call card** that opens the laptop's JS8Call screen in a browser, so operators at the command post can watch traffic without sitting at the radio. To make that work, JS8Call has to be told to accept a network connection, and the dashboard card has to be told the laptop's address.

1. Download JS8Call from **js8call.com → Windows installer**. Run it and accept the defaults.
2. Launch JS8Call, then open **File → Settings** (or press F2). On the **General** tab set **My Call =** your callsign and **My Grid =** your grid square.
3. On the **Audio** tab, set both **Input** and **Output** to **USB Audio CODEC (IC-7300)**.
4. On the **Radio** tab, set **Rig = IC-7300**, **PTT Method = CAT**, **Serial Port =** the same COM port you used for Winlink, and **Baud Rate = 115200**.
5. On the **Reporting** tab (this is the important one): set **TCP Server Hostname = 0.0.0.0** (you MUST change it from 127.0.0.1), tick **Enable TCP Server API**, set **TCP Server Port = 2442**, and tick **Accept TCP Requests**.
6. Click **OK**, then **restart JS8Call** so the network settings take effect.
7. Allow JS8Call through the Windows firewall so the dashboard can reach it (steps below).
8. Find the laptop's address and enter it into the dashboard's JS8Call card (steps below).

> **THE JS8CALL CARD ONLY WORKS IF HOSTNAME IS 0.0.0.0** — On JS8Call's **Reporting** tab, **TCP Server Hostname** ships as `127.0.0.1`, which means "talk to myself only." You **must** change it to **`0.0.0.0`** so the FieldCommand dashboard on the Pi can reach JS8Call across the network. If you skip this, the dashboard's JS8Call card will not open — this is the single most common reason it fails.

```
# 1) Let JS8Call through the Windows firewall (once):
#    Search "Windows Defender Firewall" -> Advanced Settings
#    Inbound Rules -> New Rule -> Port -> TCP -> Specific port: 2442 -> Allow -> All profiles
#    Name the rule: JS8Call API

# 2) Find the laptop's address on the field network:
#    Open Command Prompt and run:
ipconfig
#    Note the IPv4 Address for the EMCOMM-NET adapter, e.g. 192.168.50.105

# 3) Point the dashboard's JS8Call card at the laptop:
#    Connect to EMCOMM-NET, open http://192.168.50.1
#    Find the JS8Call card (purple) in the Amateur Radio section
#    Click the card, enter the laptop IP (e.g. 192.168.50.105)
#    The card saves it and opens http://192.168.50.105:2442
```

> **GIVE THE LAPTOP A FIXED ADDRESS** — So the JS8Call card keeps working after a reboot, give the laptop a **fixed** address on the network. In the router's admin page, find the DHCP (Dynamic Host Configuration Protocol) reservation list, and tie the laptop's hardware (MAC) address to a set number such as **192.168.50.2**. Then the address never changes and you never have to re-enter it in the card.


## Verifying a Connection

Do not assume it works — prove it. A quick round trip confirms the audio levels, the radio control, and your Winlink login are all correct before you ever need them for real.

1. On the laptop, open **Winlink Express** and start a new message to your own everyday email address. Type a short test line and click **Post to Outbox**.
2. Open a **VARA HF Winlink** session. Set the IC-7300 to a known Winlink RMS gateway frequency in the 40-meter band for your region.
3. Click **Start**. Winlink Express scans and connects to the nearest gateway; you will hear the tones and see the connection progress in the session window.
4. Watch the session complete and disconnect on its own. Your outgoing message is now on its way, and any waiting mail is pulled down.
5. Check your normal email inbox — your test message should arrive within a few minutes, proving the whole radio-to-internet path works.
6. To confirm the Pi's backup path, open **http://192.168.50.1:8090** in a browser and check that the **Pat** inbox loads and shows your callsign.

> **SHARING ONE RADIO BETWEEN VARA AND JS8CALL** — Winlink Express (via VARA HF) and JS8Call both want the same radio's audio and COM port, so only run **one at a time**. To switch from JS8Call to Winlink: click **Disconnect** in JS8Call, open **VARA HF** (it reclaims the audio device), then use Winlink Express. To switch back: finish any Winlink transmission, close VARA HF, then open JS8Call and click **Connect**. Running both at once needs a **second** radio and interface.


## Troubleshooting

- *The Pat page won't open at http://192.168.50.1:8090.* The Pat program is probably not running. On the Pi, run `sudo systemctl start pat && sudo systemctl enable pat`, then reload the page. Confirm the port is listening with `ss -tlnp | grep 8090`. Also make sure your device is on the field Wi-Fi and that you typed the `:8090` on the end of the address.
- *Pat opens but I can't log in / start a session.* You most likely haven't added your Winlink password. Edit `/opt/fieldcommand/.config/pat/config.json`, put your password on the `secure_login_password` line, save, and run `sudo systemctl restart pat`. Confirm `http_addr` still reads `0.0.0.0:8090`.
- *Winlink Express or VARA won't connect — the radio isn't keying (won't transmit).* Check the IC-7300 one-time settings: **CI-V Baud Rate = 115200**, **USB Send = RTS**, and in Winlink's Radio Setup make sure **PTT via CAT** is ticked and the **Control Port** is the radio's real COM port (verify it in Device Manager). If the COM port is wrong, nothing keys.
- *It connects but the other station can't decode me / audio sounds distorted.* Your transmit audio is too loud. Lower the IC-7300 **USB MOD Level** toward 40%, and make sure **speech compression (COMP) is OFF** — compression garbles digital tones. On receive, if levels look pinned, lower the input in VARA HF or JS8Call.
- *The dashboard's JS8Call card won't open.* In JS8Call, open **File → Settings → Reporting** and confirm **Enable TCP Server API** is ticked, **Port = 2442**, and **Hostname = 0.0.0.0** (not 127.0.0.1). Restart JS8Call. Confirm the Windows firewall has the inbound rule allowing TCP port 2442, and that the IP you typed into the card is the laptop's current EMCOMM-NET address.
- *The JS8Call card worked yesterday but not today.* The laptop's address probably changed. Either re-enter the current address (run `ipconfig` on the laptop to find it) into the card, or give the laptop a fixed DHCP reservation in the router so the address never moves.
- *A Winlink form import fails on the Pi.* You must import the form's **.xml attachment**, not the message body. In Winlink Express, right-click the `.xml` attachment, choose **Save As**, then import the saved file.


# 18. TNC & Modem Setup (Optional)

*The hardware that connects a radio to the Pi — USB TNCs, a Bluetooth TNC, and the SCS PACTOR modem — plus the stable device names that keep a TNC and a GPS from being confused for each other.*

> **QUICK VERSION** — A **Terminal Node Controller (TNC)** is the little box that connects a radio to a computer so they can trade digital data. Pick one: a **Digirig Mobile** or **SignaLink USB** (both plug into the Pi over Universal Serial Bus, or USB), a **Mobilinkd TNC4** (wireless, over Bluetooth), or an **SCS PACTOR modem** (top-tier High Frequency performance for Winlink). You also need a **radio-specific cable** between the TNC and your transceiver. FieldCommand automatically gives your USB TNC the stable name **`/dev/tnc0`** so it never gets confused with your GPS — verify with `ls -la /dev/tnc0`.

> **THIS WHOLE CHAPTER IS OPTIONAL — HAM GROUPS ONLY** — Part 2 of this guide is only for groups that include a **licensed amateur-radio operator**. If nobody in your organization holds an amateur-radio license, **skip this chapter** — none of this hardware is needed, and FieldCommand runs fully without it. A TNC or modem exists to put signals **on the air**, and transmitting on the amateur bands is **illegal without a proper license**. Everything here must be operated by someone licensed with privileges on the bands and modes being used.


## What This Is / What It Is For

A **Terminal Node Controller (TNC)** is the piece of hardware that sits between a **radio** and a **computer**. On one side it speaks to the radio in sound — the tones and warbles that travel over the air. On the other side it speaks to the computer in data. It also handles **Push To Talk (PTT)** — the signal that keys the radio's transmitter at the right moment. Without a TNC, the Pi and the radio have no common language; with one, the Pi can send and receive Automatic Packet Reporting System (APRS) position beacons, run VHF Packet Winlink, and more.

This chapter covers the hardware choices — which TNC or modem to use, how each connects, and the cables you need — and one small-but-important piece of housekeeping: making sure the Pi always calls your TNC by the **same name**, even though it and other USB devices can look almost identical to the operating system. Get the hardware and the naming right once, and the software just works.

> **WHO DOES THIS** — This is a one-time hardware job for the licensed operator building the radio station. You choose one TNC (or the PACTOR modem), cable it to your radio, plug it into the Pi, and confirm the device name. After that, the APRS and Winlink software use it without further fuss.


## The Hardware Options

There are four common ways to connect a radio to the Pi (or, for PACTOR, to the Windows laptop). You only need **one**. Which one depends on your radio, your budget, and whether you want High Frequency (HF) performance or simple Very High Frequency (VHF) APRS and Packet.


### USB TNCs — Digirig Mobile and SignaLink USB

The two most common choices both plug into the Pi over a USB cable:

- *Digirig Mobile.* A small, modern all-in-one interface: it carries both the audio and the radio-control (Computer Aided Transceiver, or CAT) connection in one compact unit. It's an excellent, inexpensive choice for APRS transmit and receive (paired with the Direwolf software) and for VHF Packet Winlink (paired with Pat). Radio-specific cables are sold by model at **digirig.net**.
- *SignaLink USB.* A long-established, very widely supported USB audio interface from Tigertronics. It handles the audio path and generates PTT itself. It needs a **separate Tigertronics cable made for your exact radio**. Choose this if you want the most battle-tested, well-documented option in the hobby.


### The Bluetooth Option — Mobilinkd TNC4

The **Mobilinkd TNC4** is a Bluetooth APRS TNC — no USB cable to the computer at all. It pairs wirelessly with the YAAC APRS program on the Pi, or with an APRSdroid app on a phone. Reach for it when a USB port is scarce, or when you want the TNC physically at the radio and the computer a short distance away without a cable run.


### The SCS PACTOR Modem — Top-Tier HF Winlink

**PACTOR** is a high-performance HF digital mode used heavily in Winlink work. On weak or noisy HF paths it moves data noticeably faster and more reliably than the software VARA HF modem, and it is the only path to PACTOR level 4. **SCS (Special Communications Systems)** makes the only PACTOR-licensed modems. A PACTOR modem connects between the HF radio (such as the IC-7300) and the **Windows laptop** (not the Pi). It is genuinely optional — VARA HF serves most groups well — but for serious HF message handling it is the gold standard.

| SCS model | PACTOR level | Notes |
| --- | --- | --- |
| SCS Tracker DSP TNC | 1 / 2 / 3 | Entry-level PACTOR TNC; good for most Winlink work. |
| SCS PTC-IIIusb | 1 / 2 / 3 | Also does Packet, AMTOR, RTTY. Around $650. |
| SCS P4dragon DR-7400 | 1 / 2 / 3 / 4 | Compact, proven PACTOR 4 modem; a good entry point to level 4. Around $1,100. |
| SCS PXdragon DR-9400 (flagship) | 1 / 2 / 3 / 4 | Current top model; USB-C plus LAN, up to 10,500 bits per second on PACTOR 4. |

> **PACTOR 3 AND 4 COST EXTRA** — PACTOR **1 and 2** are free to all licensed amateurs. PACTOR **3 and 4** require a separate one-time license fee paid to SCS, on top of your normal Winlink account. Levels 1 and 2 are plenty to get on the air and pass traffic; add 3/4 later if your nets need the extra throughput.


## Matching a TNC to Its Best Use

Use this table to pick quickly. Again, you only need one.

| Option | Connects via | Best for |
| --- | --- | --- |
| Digirig Mobile | USB to the Pi | APRS and VHF Packet Winlink on a budget; audio + CAT in one small unit. |
| SignaLink USB | USB to the Pi | APRS and Packet where the most widely-supported, well-documented interface is wanted. |
| Mobilinkd TNC4 | Bluetooth (wireless) | APRS when a USB port is unavailable, or when you want no cable to the computer. |
| SCS PACTOR modem | USB / LAN to the Windows laptop | Highest-performance HF Winlink on marginal paths; the only route to PACTOR 4. |


## Rig Interface Cables — the Radio-Specific Link

Whatever TNC you pick, it still needs the right **cable to your specific radio**. This cable carries the receive audio, the transmit audio, and the PTT keying line between the TNC and the transceiver. There is no universal cable — the plugs and pinout differ from radio to radio, so the cable is chosen by **radio model**:

- *Digirig:* order the matching cable for your exact radio model at **digirig.net**.
- *SignaLink USB:* order the matching **Tigertronics** cable for your exact radio (a separate cable per rig).
- *SCS PACTOR modem:* the audio and PTT cables are typically **included with the modem**; you connect it to the radio's accessory (ACC) jack.

> **LET VARA AND PACTOR SHARE ONE RADIO** — If you run **both** VARA HF (over the radio's USB audio) and a PACTOR modem on the **same** IC-7300, point the PACTOR modem at the radio's **ACC (accessory) jack** for its audio, and leave VARA on the USB audio path. With the two audio paths kept separate, both can stay wired up at once — you just operate one mode at a time.


## Stable Device Names — Why /dev/tnc0 Matters

Here is the subtle problem that this section solves. When you plug a USB device into the Pi, Linux gives it a plain, first-come-first-served name like **`/dev/ttyUSB0`**. Plug in a second USB device and it becomes **`/dev/ttyUSB1`**. The catch: **which device gets which number can change** depending on the order things were plugged in or powered up. So the TNC you told your software was at `ttyUSB0` might be at `ttyUSB1` the next time you boot — and suddenly APRS or Winlink is talking to the wrong device, or to nothing at all.

It gets worse in one specific, real case. The popular **Digirig Mobile TNC** and a common **GPS receiver** use the **same USB chip** (a Silicon Labs CP2102). To the operating system they look nearly identical, so the plain `ttyUSB` numbers are especially likely to swap between them. That is a recipe for the TNC and the GPS constantly trading places.

FieldCommand fixes this with **udev rules** — small instructions that tell Linux, "whenever you see *this* device, always give it *this* name." The installer puts these rules in place for you. Instead of the shifting `ttyUSB` numbers, your TNC always answers to the fixed name **`/dev/tnc0`** (plus a friendly alias like `/dev/digirig` or `/dev/signalink`), and the GPS always answers to **`/dev/gps0`** — no matter what order anything was plugged in. Your software points at `/dev/tnc0` once and never has to change.

> **HOW THE RULE TELLS A DIGIRIG FROM A GPS** — Because the Digirig and the GPS share the same chip, the udev rule can't tell them apart by chip alone. It looks deeper — at the USB **product description string**. The Digirig identifies itself with the text **"Digirig Mobile"**, so the TNC rule matches only that, and the GPS rule specifically **excludes** Digirig. The result: the Digirig always becomes `/dev/tnc0` and the GPS always becomes `/dev/gps0`, even though they use identical chips.

The installer copies the TNC rules into place and reloads them automatically, so on a normal FieldCommand build you don't have to do anything. The `/dev/tnc0` name simply appears the moment you plug the TNC in. The commands below are for **verifying** it worked, or for adding a TNC the rules don't yet recognize.


## Verifying the Device Name

After plugging the TNC into the Pi, confirm it received the stable name. Two quick commands do it:

```
# 1) Confirm the stable symlink exists and see what it points to:
ls -la /dev/tnc0
#    Expected: /dev/tnc0 -> ttyUSB0  (an arrow to the real device)
#    Also check the GPS, if you have one, so they didn't collide:
ls -la /dev/gps0

# 2) If /dev/tnc0 is missing, look at the raw device's USB IDs so you
#    can see what it actually is (vendor, product, and product string):
udevadm info -a -n /dev/ttyUSB0 | grep -E "idVendor|idProduct|product"

# 3) After adding or editing a rule, reload the rules and re-trigger:
sudo udevadm control --reload-rules && sudo udevadm trigger
```

In the APRS software (YAAC), you then simply point the serial TNC port at **`/dev/tnc0`** — because that name never changes, you set it once and it keeps working across reboots and re-plugs.

> **IF YOUR TNC ISN'T ONE OF THE LISTED MODELS** — The rules already cover Digirig, SignaLink, and common FTDI-chip TNCs. If you have a different TNC, run `lsusb` and the `udevadm info` command above to read its **idVendor** and **idProduct** values, then add a matching line to `/etc/udev/rules.d/99-fieldcommand-tnc.rules` that assigns `SYMLINK+="tnc0"`. Reload with the command in step 3. There's a commented example in that file to copy.


## Troubleshooting

- *The TNC isn't detected at all.* Confirm the USB cable is fully seated and, for a powered TNC, that it's switched on. Run `lsusb` — your device should appear in the list. If it doesn't, try a different USB cable (some are charge-only with no data wires) or a different port on the Pi's powered USB hub.
- */dev/tnc0 doesn't exist even though the device shows in lsusb.* The udev rule didn't match. Read the device's IDs with `udevadm info -a -n /dev/ttyUSB0 | grep -E "idVendor|idProduct|product"`, compare them to the rules in `/etc/udev/rules.d/99-fieldcommand-tnc.rules`, add or fix a matching line, then run `sudo udevadm control --reload-rules && sudo udevadm trigger` and re-plug the TNC.
- *My software points at the wrong device / the TNC and GPS keep swapping.* This is exactly what the stable names prevent — so stop using `/dev/ttyUSB0` or `/dev/ttyUSB1` in your software and use **`/dev/tnc0`** (for the TNC) and **`/dev/gps0`** (for the GPS) instead. Those names always follow the right device.
- *Two devices are fighting over the same name.* Only one device can own `/dev/tnc0`. If you truly run two TNCs, give the second one its own symlink (for example `tnc1`) by adding a separate, more specific rule matched on that device's serial number, so each gets a distinct, stable name.
- *The radio won't key (no PTT / it never transmits).* Check the **rig interface cable** is the correct one for your radio model and fully plugged in at both ends. For a Digirig or SignaLink, confirm the software's PTT method matches how the TNC keys (CAT versus a hardware line). A wrong or half-seated cable is the usual cause.
- *Audio is distorted or the far end can't decode me.* Transmit audio is too loud. Turn the drive down — on the IC-7300 lower the **USB MOD Level** toward 40%, or reduce the TNC's output level — and make sure **speech compression is OFF**. On receive, if the software's level meter is pinned to the top, lower the input level in the software.
- *The SCS PACTOR modem doesn't respond.* Confirm you selected the correct COM port for the modem in Winlink Express, that the USB (or LAN) cable is seated, and try the modem's lower default baud rate if the higher one is silent. In a terminal to the modem, the `ver` command should return its firmware version and model — no response there means a cabling or port problem, not a radio one.
