#!/usr/bin/env python3
"""manual_ch_01_07.py — Chapters 1–7: Introduction through Net Loggers."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *

def ch1():
    s = chapter(1, 'Introduction & System Overview')
    s.append(P(
        'When a disaster takes down commercial infrastructure — cellular networks, internet, '
        'power — the tools modern emergency management depends on disappear precisely when '
        'they are needed most. Incident logs revert to paper. Resource tracking becomes a '
        'whiteboard. Incident Command System (ICS) forms are filled out by hand, photocopied, and hand-carried between '
        'rooms. Situational awareness degrades to whatever one person can hold in their head. '
        'Every organization that has worked a major activation knows this failure mode, and '
        'most have simply accepted it as the cost of doing business.', Lead))
    s.append(P(
        'FieldCommand IMS was built to eliminate that failure mode. It is a complete, '
        'self-contained incident management platform that carries its own network, its own '
        'server, and its own tools — and it operates with no internet connection, no cellular '
        'service, and no outside infrastructure of any kind. The cell towers are down, the '
        'internet is gone, and you are running on a generator in a parking lot. '
        'That is exactly when you need incident management software most — and that is '
        'exactly when FieldCommand IMS is designed to perform.'))
    # Deploying-org / served-agency line — ESV edition only (blank in World).
    if ed('org'):
        line = f"This edition is prepared for <b>{ed('org')}</b>"
        if ed('served'):
            line += f", the amateur-radio emergency-communications group serving the <b>{ed('served')}</b>"
        line += '.'
        s.append(SP(4))
        s.append(P(line))
    s.append(SP(4))
    s.append(note(
        'In one sentence: FieldCommand IMS is a full ICS incident management system that '
        'brings its own Wi-Fi, its own server, and radio communications built in, and keeps '
        'working when the internet and cell service are gone.', 'tip'))
    s.append(SP(6))

    s.append(P('1.1  What FieldCommand IMS Is', H2))
    s.append(P(
        'FieldCommand IMS is a <b>complete ICS/NIMS all-hazards incident management system</b> — '
        'not simply an amateur radio or Emergency Communications (EMCOMM) tool. It manages the full lifecycle of any '
        'incident from initial response through demobilization using standard ICS forms and '
        'workflows. It runs on a Raspberry Pi 5 server and broadcasts its own private Wi-Fi '
        'access point. Any smartphone, tablet, or laptop that joins that network immediately '
        'has access to the full suite of 48 tools through a standard web browser — no app '
        'installation, no accounts, and no per-device configuration required.'))
    s.append(SP(4))
    s.append(P(
        'The letters IMS stand for <b>Incident Management System</b>. The whole product is '
        "designed around one belief: communications and incident management are inseparable. "
        'Running an incident means running its Incident Action Plan (IAP), tracking its '
        'resources, and moving its message traffic — all at once. FieldCommand IMS marries '
        'the communications side and the planning side in a single tool so that a net check-in, '
        'a resource assignment, and an ICS form are all part of one connected picture rather '
        'than three separate systems that never talk to each other.'))
    s.append(SP(4))
    s.append(P(
        'When internet connectivity is available, live features activate automatically: '
        'National Weather Service (NWS) weather alerts, APRS-IS, animated Next Generation Radar (NEXRAD) radar, and High Frequency (HF) propagation data. '
        'If connectivity is lost at any point, all core tools continue without interruption. '
        'The system degrades gracefully and recovers automatically.'))
    s.append(SP(6))

    s.append(P('1.2  How FieldCommand IMS Differs From Other ICS Platforms', H2))
    s.append(P(
        'Platforms such as WebEOC, E-Team, NIMSIAP, National Incident Management System (NIMS) Logic, and E-iSuite deliver '
        'powerful incident management capability — but every one of them requires a working '
        'internet connection and functioning server infrastructure. They are cloud-dependent '
        'by design. When a major disaster disables that infrastructure, they fail with it — '
        'at exactly the moment capability is most critical.'))
    s.append(SP(4))
    s.append(P(
        'FieldCommand IMS is built on the opposite assumption: infrastructure will fail, and '
        'incident management capability must survive that failure. It carries its own '
        'infrastructure — server, network, storage, and tools — in a single deployable '
        'package. It requires no IT department, carries no licensing fees, and does not '
        'fail when the internet fails.'))
    s.append(SP(4))
    s.append(P(
        'The feature that sets FieldCommand IMS apart from every platform in this category '
        'is its native integration of amateur radio and public safety communications directly '
        'into the incident management workflow. No other ICS platform includes built-in net '
        'control logging, Federal Communications Commission (FCC) callsign validation against the full national licensee database, '
        'Automatic Packet Reporting System (APRS) tactical mapping, Winlink radio email, JS8Call HF messaging, or Amateur Packet Radio Network (AMPRNet) gateway '
        'capability. These are not add-ons — they are core features fully integrated with the '
        'ICS platform so that radio traffic, net logs, and check-in data flow directly into '
        'ICS-309 communications logs, ICS-214 activity logs, and the Incident Action Plan (IAP).'))
    s.append(SP(6))
    s.append(tbl(['PLATFORM', 'OFFLINE?', 'SELF-CONTAINED?', 'NATIVE EMCOMM?', 'COST'], [
        ['FieldCommand IMS',   'Fully offline',    'Own network + server', 'Full EMCOMM',   'Free / open source'],
        ['WebEOC',             'Cloud only',       'Needs infrastructure','None',              '$10,000-50,000/yr'],
        ['E-Team / Veoci',     'Cloud only',       'Needs infrastructure','None',              'Subscription'],
        ['NIMSIAP',            'Internet required','Requires connectivity', 'None',               'Free'],
        ['E-iSuite',           'Limited',          'Laptop, no network','None',              'License fee'],
    ], widths=[1.4*inch, 1.15*inch, 1.55*inch, 1.3*inch, CW-5.4*inch]))
    s.append(SP(6))

    s.append(P('1.3  System Architecture', H2))
    s.append(P(
        'A complete FieldCommand IMS deployment is a small stack of purpose-built parts. The '
        'table below lists each component, what it does, and the network address it uses by '
        'default. Only the first component — the FieldCommand Pi 5 server — is strictly '
        'required; everything else extends coverage, adds a radio gateway, or hardens the '
        'network. All of the tools in this manual are served by that one Pi.'))
    s.append(SP(4))
    s.append(tbl(['COMPONENT', 'FUNCTION', 'DEFAULT IP'], [
        ['FieldCommand Pi 5 16GB',
         'Primary server / all 48 web tools / 12+ background services / '
         'RAID-1 NVMe storage / EMCOMM-NET Wi-Fi AP',
         '192.168.50.1'],
        ['44Net Gateway Pi 5  (optional)',
         'AMPRNet WireGuard tunnel / callsign-authenticated access / '
         'Part 97 access log / isolated from primary server',
         '192.168.50.2'],
        ['Wi-Fi router  (primary)',
         'DHCP / AiMesh controller / dual Wide Area Network (WAN) management / '
         'EMCOMM-NET Service Set Identifier (SSID) broadcast. Recommended: ASUS RT-BE58 Go.',
         '192.168.50.254'],
        ['AiMesh nodes  (optional)',
         'EMCOMM-NET coverage extension / seamless roaming. '
         'Recommended: additional ASUS RT-BE58 Go units.',
         'DHCP assigned'],
        ['UniFi Switch Lite 16 Power over Ethernet (PoE)  (recommended)',
         'Wired backbone / powers PoE devices / connects all Pi units, '
         'router, cellular antenna, and workstations',
         'DHCP assigned'],
        ['Operator workstations',
         'Any device with a modern browser: smartphones, tablets, laptops, '
         'Raspberry Pi 500 desktops, Windows or macOS laptops',
         'DHCP assigned'],
    ], widths=[1.9*inch, CW-3.05*inch, 1.15*inch]))
    s.append(SP(4))
    s.append(note(
        'The default server address is 192.168.50.1. This is configurable during '
        'installation. All documentation uses this default — substitute your address '
        'wherever 192.168.50.1 appears if your deployment differs.', 'note'))
    s.append(SP(4))
    s.append(note(
        'The Wi-Fi network is broadcast by the router, not by the Pi. The Pi is the server '
        'and the router is the radio that puts the EMCOMM-NET network on the air. Operators '
        'join EMCOMM-NET and then reach the Pi at 192.168.50.1. This split is why coverage '
        'can be extended with ordinary mesh nodes without touching the server.', 'note'))
    s.append(SP(6))

    s.append(P('1.4  Capability Summary', H2))
    s.append(P(
        'FieldCommand IMS groups its 48 tools into nine capability areas. Every area is '
        'covered in depth in its own chapter later in this manual; the table below is a '
        'one-look inventory of what the system does.'))
    s.append(SP(4))
    s.append(tbl(['CAPABILITY AREA', 'TOOLS PROVIDED'], [
        ['Incident Management',
         'Five-section ICS structure. Complete IAP form set: ICS-202 through ICS-221. '
         'Live T-card resource board. A growing library of pre-planned event templates. '
         'Incident archive, restore, and scenario/exercise mode.'],
        ['ICS Forms & IAP',
         'Full ICS form set with digital signature capture on all prepared-by and '
         'approved-by fields. One-click IAP Portable Document Format (PDF) compilation with title page and '
         'section dividers. Print center for on-site IAP packages.'],
        ['Federal Emergency Management Agency (FEMA) Documentation',
         'FEMA Public Assistance (PA) cost tracking: Force Account Labor with fringe, Equipment with '
         '2025 FEMA rate schedule (45 built-in rates), Materials, and Contracts. '
         'Real-time cost dashboard. ICS-214 import. Project Worksheet text export.'],
        ['Amateur Radio EMCOMM',
         'Net control logger with FCC callsign auto-fill from offline 800,000+ '
         'licensee database. APRS tactical map. Winlink and Pat radio email. '
         'JS8Call HF digital. AMPRNet 44Net gateway. National Traffic System (NTS) radiogram generator.'],
        ['Public Safety Comms',
         'Trunked/P25 net logger with radio ID check-in. EMA member ID lookup. '
         'ICS-309 export. Observer mode for read-only net monitoring on any device.'],
        ['Situational Awareness',
         'Animated NEXRAD radar (WAN required). Live NWS weather alerts. '
         'GPS-tracked resource map with status-coded SVG markers. '
         'Offline APRS tactical map. CalTopo / SARTopo GeoJSON import. HF propagation tool.'],
        ['Personnel & Check-In',
         'Member roster with certifications, radio IDs, and Quick Response (QR) code check-in codes. '
         'QR/barcode camera scan check-in using native BarcodeDetector API. '
         'ICS-211 check-in log. Digital ID card generator.'],
        ['WAN & Connectivity',
         'Dual WAN source support: any cellular modem, hotspot, or satellite dish. '
         'Preferred/fallback role configuration. Configurable detection per source. '
         'Automatic failover. Real-time WAN status with 30-second polling.'],
        ['Reference & Offline Content',
         'Kiwix offline Wikipedia and reference library. Radio frequency cheat sheets. '
         'Hospital and facilities directory. Repeater database. Channel library. '
         'NIMS resource typing library. ICS position checklists.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('1.5  Every Incident Record Is Saved', H2))
    s.append(P(
        'FieldCommand IMS treats incident data as permanent. Everything an incident produces '
        '— net logs, ICS forms, T-cards, the IAP, cost records, resource assignments, roster '
        'snapshots, check-ins, and attachments — is written to the server and kept. Nothing '
        'is held only in a browser tab or only in memory, so a device that loses power or '
        'wanders off the network does not take the record with it. Any operator who reconnects '
        'sees the same live picture as everyone else.'))
    s.append(SP(4))
    s.append(P(
        'The server stores this in a database on its mirrored (RAID-1) solid-state storage, so '
        'a single drive failure does not lose data. Completed incidents can be archived and '
        'later restored, and the whole data set is copied to an external backup drive. The '
        'practical result is that an incident worked on FieldCommand IMS becomes a durable, '
        'auditable record you can reopen, reprint, or hand to a served agency long after the '
        'event is over.'))
    s.append(SP(4))
    s.append(note(
        'This is the deliberate opposite of a throwaway tool. If you are building or changing '
        'an incident feature, the default is to persist it on the server, not to keep it in '
        'the browser only.', 'tip'))
    s.append(SP(6))

    s.append(P('1.6  Offline First, Online When Available', H2))
    s.append(P(
        'The whole tool set is designed to run with zero internet. A small number of features '
        'depend on an outside connection and light up automatically when a Wide Area Network '
        '(WAN) — cellular or satellite — is present; if that connection drops, those features '
        'pause and everything else keeps running. The dashboard WAN status card shows the '
        'current state at a glance (covered in the Getting Started chapter). The table below '
        'shows the split.'))
    s.append(SP(4))
    s.append(tbl(['FEATURE GROUP', 'RUNS OFFLINE?', 'NOTES'], [
        ['ICS platform, forms, IAP, T-cards',   'Always',        'No internet needed at any time'],
        ['FEMA cost tracking and dashboards',   'Always',        'Rate schedule is built in'],
        ['Net loggers (amateur and public safety)', 'Always',    'Local logging and export'],
        ['FCC callsign lookup',                 'Always',        'Reads the local offline licensee database'],
        ['Roster, check-in, resource map',      'Always',        'Local data and local maps'],
        ['NEXRAD weather radar',                'Internet only', 'Animated radar imagery needs a WAN'],
        ['NWS weather alerts',                  'Internet only', 'Live alert feed needs a WAN'],
        ['APRS-IS internet feed',               'Internet only', 'Off-air APRS still works over radio'],
        ['HF propagation data',                 'Internet only', 'Live space-weather data needs a WAN'],
    ], widths=[2.5*inch, 1.3*inch, CW-3.8*inch]))
    s.append(SP(4))
    s.append(note(
        'A red WAN indicator never means FieldCommand IMS is down. It means only the '
        'internet-dependent extras are paused. Every ICS tool, form, net logger, and local '
        'map continues to work normally.', 'note'))
    s.append(SP(6))

    s.append(P('1.7  Amateur Radio Is Optional and License-Gated', H2))
    s.append(P(
        'FieldCommand IMS serves two kinds of groups: those with licensed amateur radio '
        'operators and those without. The amateur radio features — the net control logger, '
        'APRS tactical map, Winlink and Pat radio email, JS8Call HF digital, the AMPRNet 44Net '
        'gateway, and the NTS radiogram generator — are grouped under an Amateur Radio mode '
        'that turns on only when a station callsign has been entered during setup.'))
    s.append(SP(4))
    s.append(P(
        'A group with no licensed operators simply leaves the callsign blank. The Amateur '
        'Radio mode then stays grayed out, and every other part of the system — the full ICS '
        'platform, forms, cost tracking, roster, check-in, resource map, and the public-safety '
        'net logger — works exactly the same. A callsign can be added later at any time to '
        'unlock the amateur features.'))
    s.append(SP(4))
    s.append(note(
        'Amateur radio transmissions are legal only when made by a properly licensed operator '
        'with privileges on the bands and modes in use. Turning on the amateur features does '
        'not grant that authority. If your group is not licensed, leave the callsign blank and '
        'use the rest of the system freely.', 'warn'))
    s.append(SP(6))

    s.append(P('1.8  Who Uses FieldCommand IMS', H2))
    s.append(P(
        'FieldCommand IMS is a multi-user system. Every operator who joins the EMCOMM-NET '
        'network and opens a browser sees the same live incident. There are no per-device '
        'accounts to manage; roles below describe how people typically use the system, not '
        'logins the software enforces.'))
    s.append(SP(4))
    s.append(tbl(['ROLE', 'HOW THEY USE THE SYSTEM'], [
        ['Incident Commander / Command Staff',
         'Set objectives, approve the IAP, watch the whole picture from the dashboard and '
         'resource board.'],
        ['Planning Section',
         'Build and compile the IAP, manage ICS forms, run T-card resource status, and set '
         'up event templates.'],
        ['Operations Section',
         'Track assignments and resources on the ground, read the tactical and resource maps.'],
        ['Logistics Section',
         'Order and account for resources, manage the communications plan and reference '
         'material.'],
        ['Finance / Administration',
         'Record FEMA Public Assistance costs — labor, equipment, materials, contracts — and '
         'watch the cost dashboard.'],
        ['Communications Unit / Net Control',
         'Run the net loggers, validate callsigns and radio IDs, and move message traffic.'],
        ['Any responder or observer',
         'Check in by QR code, view read-only net and incident status from a phone or tablet.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(6))

    s.append(P('1.9  How This Manual Is Organized', H2))
    s.append(P(
        'This manual follows the order you will use the system. Early chapters get you '
        'connected and configured; the middle chapters cover the day-to-day tools; the later '
        'chapters cover the ICS platform, FEMA documentation, radio features, and network '
        'hardware; and the final reference chapters answer questions and define terms.'))
    s.append(P('<b>Getting connected</b> — join EMCOMM-NET and complete Organization Setup '
               '(Chapters 2 and 3).', Bullet))
    s.append(P('<b>Everyday tools</b> — the dashboard, event templates, and net loggers for '
               'running an activation.', Bullet))
    s.append(P('<b>Incident management</b> — the ICS platform, the ICS form set, the IAP, the '
               'T-card board, and FEMA cost tracking.', Bullet))
    s.append(P('<b>Communications and situational awareness</b> — the amateur radio features, '
               'the two maps, weather, and personnel check-in.', Bullet))
    s.append(P('<b>Reference</b> — network hardware, troubleshooting and frequently asked '
               'questions, a glossary, and a menu reference.', Bullet))
    s.append(SP(4))
    s.append(note(
        'Every chapter opens with a short plain-language summary, so a reader in a hurry can '
        'skim the top of a chapter and still succeed. If you are brand new, read Chapters 2 '
        'and 3 first, then jump to whichever tool you need.', 'tip'))
    s.append(SP(6))

    s.append(P('1.10  Common Questions', H2))
    s.append(tbl(['QUESTION', 'ANSWER'], [
        ['Do I need to install an app?',
         'No. Every tool is a web page. Join EMCOMM-NET and open a browser to 192.168.50.1.'],
        ['Does it need the internet to work?',
         'No. The full tool set runs offline. Only weather radar, NWS alerts, APRS-IS, and '
         'HF propagation need a WAN, and they resume automatically when one returns.'],
        ['Do I need a login or account?',
         'No. FieldCommand IMS is a no-login, open-LAN tool by design. Any device on '
         'EMCOMM-NET reaches the whole dashboard.'],
        ['We have no licensed hams. Can we still use it?',
         'Yes. Leave the callsign blank during setup. The amateur features stay off and '
         'everything else works normally.'],
        ['What happens to our data after the incident?',
         'It is saved on the server, mirrored across two drives, backed up to an external '
         'drive, and can be archived and restored later.'],
        ['Which devices work?',
         'Any device with a modern browser — a phone, tablet, laptop, or a Raspberry Pi '
         'desktop — on any operating system.'],
        ['Does it cost anything?',
         'The software is free and open source. Your only cost is the hardware in the '
         'architecture table above.'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(PB())
    return s


def ch2():
    s = chapter(2, 'Getting Started — Connecting to FieldCommand',
                'http://192.168.50.1')
    s.append(P(
        "Every tool in FieldCommand IMS is a web page served from the Raspberry Pi. There is "
        "nothing to install on any device, no account to create, and no password to remember "
        "beyond the one for the Wi-Fi. You join the EMCOMM-NET wireless network, open a browser, "
        "type one address, and the full dashboard appears. It works the same way on an iPhone, "
        "an Android tablet, a Windows laptop, a Mac, or an operator workstation. This chapter "
        "walks you through that first connection, then shows you how to read the dashboard, "
        "switch between its three modes, and understand the status indicators you will see.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: connect to the EMCOMM-NET Wi-Fi, open http://192.168.50.1 in any "
        "browser, and every FieldCommand tool is there — no app, no login.", 'tip'))
    s.append(SP(6))

    s.append(P('2.1  What You Need to Connect', H2))
    s.append(P(
        "Any modern device with a web browser and Wi-Fi can reach FieldCommand. You do not need "
        "the internet, a cellular signal, or any special software. The list below is everything "
        "that matters."))
    s.append(SP(4))
    s.append(tbl(['YOU NEED', 'DETAILS'], [
        ['A device with Wi-Fi',
         'A smartphone, tablet, laptop, or an operator workstation. Any operating system works.'],
        ['A modern browser',
         'Chrome, Firefox, Safari, Edge, or the built-in browser on a phone or tablet. Nothing '
         'to download or update.'],
        ['The EMCOMM-NET password',
         'Printed on the equipment case label and in the Installation Guide. It is the only '
         'credential you enter anywhere.'],
        ['Nothing else',
         'No internet, no cellular data, no app store, no user account. The Pi carries its own '
         'network and its own copy of every tool.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('2.2  First Connection', H2))
    s += steps([
        "Power on the FieldCommand Pi and wait approximately 45 seconds for all services to "
        "start. The system is ready when the EMCOMM-NET Wi-Fi network appears in your device "
        "scan list.",
        "On any smartphone, tablet, or laptop, open Wi-Fi settings and connect to "
        "<b>EMCOMM-NET</b>. The password is on the equipment case label and in the Installation "
        "Guide. No other credentials are required.",
        "Open a browser and go to <b>http://192.168.50.1</b>. The FieldCommand dashboard loads "
        "immediately.",
        "Bookmark the dashboard address (its Uniform Resource Locator, or URL). On a smartphone, "
        "tap <b>Share</b> then <b>Add to Home Screen</b> to create an icon that opens like a "
        "native app.",
        "If the dashboard does not load, confirm you are connected to EMCOMM-NET and not to "
        "another Wi-Fi network. The Pi does not relay traffic to the internet, so if your device "
        "switches to a different network automatically, turn off auto-join on other networks "
        "during activations.",
    ])
    s.append(note(
        "The EMCOMM-NET Wi-Fi is broadcast by an external ASUS router, not by the Pi itself. If "
        "no EMCOMM-NET network appears at all, the router may still be starting or may be "
        "unplugged — see the Installation Guide network section.", 'note'))
    s.append(SP(6))

    s.append(P('2.3  Reading the Dashboard', H2))
    s.append(P(
        "Across the very top of every page is the <b>hero bar</b>. It never scrolls away and "
        "tells you, at a glance, who this station is and what time it is. Below it sits the mode "
        "switcher (covered next). Here is what each part of the hero bar shows."))
    s.append(SP(4))
    s.append(tbl(['HERO BAR ELEMENT', 'WHAT IT SHOWS'], [
        ['Callsign badge (top left)',
         "The station callsign set during setup — for example a club callsign. Before setup is "
         "finished it reads <b>EMCOMM-NET</b>. If an organization name and logo were configured, "
         "they appear just below the badge."],
        ['INCIDENT MANAGEMENT SYSTEM',
         "The product name and version (v1.0). This confirms you are on the FieldCommand "
         "dashboard and not another page."],
        ['Primary clock (large)',
         "The main time display. In Amateur Radio mode this is <b>UTC</b> (Coordinated Universal "
         "Time), the worldwide amateur radio standard. In the other two modes it is your "
         "<b>local</b> time, which the Incident Command System (ICS) uses on forms."],
        ['Secondary clock (small)',
         "The other time zone, shown smaller underneath — so both UTC and local time are always "
         "visible, whichever mode you are in."],
        ['Mode pill (top right)',
         "A colored badge that names the mode you are currently in, so you always know which set "
         "of tools is on screen."],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        "Under the hero bar, the working area shows the tool cards for the current mode on the "
        "left and a status column on the right. Each tool is a labeled card you tap or click to "
        "open. You never have to hunt through menus — everything for the job at hand is on one "
        "screen."))
    s.append(SP(6))

    s.append(P('2.4  The Three Modes', H2))
    s.append(P(
        "FieldCommand groups its tools into three modes, chosen from the <b>mode switcher</b> "
        "bar just under the hero bar. A mode is only a filter on which tool cards show first. "
        "Switching modes never changes, hides, or deletes any data — every tool stays available, "
        "and any incident, log, or form you created is still there whichever mode you are in."))
    s.append(SP(4))
    s.append(tbl(['MODE', 'TOOLS SHOWN PROMINENTLY', 'BEST FOR'], [
        ['Amateur Radio',
         'Net control logger, Federal Communications Commission (FCC) callsign lookup, Automatic '
         'Packet Reporting System (APRS) map, Winlink, JS8Call, Amateur Packet Radio Network '
         '(AMPRNet) gateway, High Frequency (HF) propagation, National Traffic System (NTS) radiogram',
         'Amateur radio net operations, ARES/RACES activations'],
        [ed('ps_mode'),
         f"{ed('ps_logger')}, radio ID roster, resource map, Wide Area Network (WAN) status, "
         "weather radar, hospital directory, facilities",
         f"Public safety radio nets, {ed('ps_checkin')} operations"],
        ['ICS',
         'Full ICS platform, Incident Action Plan (IAP) forms, T-card resource board, personnel '
         'check-in, Federal Emergency Management Agency (FEMA) cost documentation, event '
         'templates, cost dashboard',
         'Any active incident requiring ICS structure'],
    ], widths=[1.3*inch, CW-3.1*inch, 1.8*inch]))
    s.append(SP(6))

    s.append(P('2.5  Switching Modes and What Changes', H2))
    s.append(P(
        "The mode switcher has three buttons, each with an icon and a short subtitle listing "
        "what it covers. Changing modes takes one tap."))
    s.append(SP(4))
    s += steps([
        "Tap or click one of the three buttons in the mode bar: <b>Amateur Radio</b>, "
        f"<b>{ed('ps_mode')}</b>, or <b>ICS / Incident Command</b>.",
        "The tool cards below switch to that mode. The colored mode pill in the hero bar changes "
        "to match, and the clock re-orders (UTC first in Amateur Radio mode, local time first in "
        "the other two).",
        "Your choice is remembered on <b>this device</b> in the browser, so the next time you "
        "open the dashboard on the same device it returns to the mode you last used.",
    ])
    s.append(note(
        "You can open the dashboard straight into a mode by adding it to the address: "
        "<b>http://192.168.50.1/?mode=ics</b> opens ICS mode, <b>?mode=amateur</b> opens Amateur "
        "Radio, and <b>?mode=starcom</b> opens the public-safety mode. This is handy for a "
        "big-screen display you always want in one mode.", 'tip'))
    s.append(P(
        "Because the choice is saved per device, two operators can sit side by side on their own "
        "tablets, one in ICS mode and one in Amateur Radio mode, and neither affects the other. "
        "They are both looking at the same live data on the same server."))
    s.append(SP(6))

    s.append(P('2.6  When Amateur Radio Mode Is Grayed Out', H2))
    s.append(P(
        "The Amateur Radio mode button is available only when a station callsign has been "
        "entered in the Setup wizard. A group with no licensed amateur radio operators leaves "
        "the callsign blank, and the button then shows a small padlock hint reading "
        "<b>Add a callsign in Setup to enable</b>. Tapping it does nothing, and the dashboard "
        "opens in ICS mode instead. Every incident-management and public-safety tool still works "
        "normally — only the amateur radio tools are held back."))
    s.append(SP(4))
    s.append(note(
        "A callsign, and the amateur radio features it unlocks, must only be used by a properly "
        "licensed operator with privileges on the bands and modes in use. You can add a callsign "
        "later in the Setup wizard at any time; the Amateur Radio mode lights up as soon as one "
        "is saved. Until setup is finished, all three modes are shown so you can explore the "
        "system before configuring it.", 'warn'))
    s.append(SP(6))

    s.append(P('2.7  The Weather and Radar Row', H2))
    s.append(P(
        "At the top of the working area is a row that gives you a quick weather picture. It has "
        "two parts, and both depend on the internet — they light up when a WAN connection is "
        "present and wait quietly when there is none."))
    s.append(SP(4))
    s.append(tbl(['ITEM', 'WHAT IT DOES'], [
        ['NWS Weather Alerts',
         "A live feed of National Weather Service (NWS) watches, warnings, and advisories for the "
         "area. A colored dot and a status line show whether it is current. The refresh symbol "
         "re-checks on demand. Offline, it reads <b>Waiting for internet connection</b>."],
        ['NWS Radar',
         "A card that opens an animated NEXRAD (Next-Generation Radar) rain-and-storm loop for "
         "your area. Its small status badge shows whether the loop is reachable right now."],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        "These two are the clearest example of FieldCommand being offline-first. When the "
        "internet is gone they simply say so and stay out of your way — every other tool on the "
        "dashboard keeps working exactly as before.", 'note'))
    s.append(SP(6))

    s.append(P('2.8  WAN Status Indicators', H2))
    s.append(P(
        "Each mode includes a live <b>WAN Status</b> card in its status column (there is no "
        "top-of-page status bar). WAN stands for Wide Area Network — the path to the internet. "
        "The card re-checks about every 30 seconds and changes color on its own."))
    s.append(SP(4))
    s.append(tbl(['INDICATOR', 'MEANING', 'CORE TOOLS AFFECTED?'], [
        ['Green — Cellular',  'Primary internet source active',                'None — fully operational'],
        ['Blue — Satellite',  'Satellite failover active',                     'None — fully operational'],
        ['Red — Offline',     'No internet — all core tools continue',         'None — fully operational'],
        ['AMPRNet UP',        '44Net WireGuard tunnel active',                 'N/A'],
        ['AMPRNet DOWN',      '44Net tunnel down or gateway Pi unreachable',   'N/A'],
    ], widths=[1.6*inch, CW-3.4*inch, 1.8*inch]))
    s.append(SP(4))
    s.append(note(
        "A red WAN indicator means the internet-dependent features are paused — NWS radar, "
        "APRS-IS, HF propagation. It does NOT mean FieldCommand IMS is unavailable. All ICS "
        "tools, forms, net loggers, roster, and local maps run normally offline.", 'note'))
    s.append(SP(6))

    s.append(P('2.9  Using It on a Phone or Tablet', H2))
    s.append(P(
        "FieldCommand is built to be used from whatever device an operator already carries. A "
        "few small habits make it feel like a real app and keep every operator on the same page."))
    s.append(P("<b>Add it to your home screen.</b> On a phone, open the dashboard, tap "
               "<b>Share</b> then <b>Add to Home Screen</b>. You get a tap-to-open icon and a "
               "full-screen view with no browser clutter.", Bullet))
    s.append(P("<b>Many people at once.</b> Every operator who joins EMCOMM-NET can open the "
               "dashboard at the same time. They all see the same live incident data; a change "
               "one person saves appears for everyone.", Bullet))
    s.append(P("<b>Each device is independent.</b> The mode you pick and any on-screen "
               "preferences are remembered on that device only, so a shared wall display and a "
               "handheld tablet can show different modes at the same time.", Bullet))
    s.append(P("<b>Stay on EMCOMM-NET.</b> Turn off auto-join for home, cellular, and hotspot "
               "networks during an activation so your phone does not silently wander off the "
               "FieldCommand Wi-Fi.", Bullet))
    s.append(SP(6))

    s.append(P('2.10  Common Questions', H2))
    s.append(tbl(['QUESTION', 'ANSWER'], [
        ['Do I have to install an app?',
         "No. FieldCommand is web pages served from the Pi. Any browser opens them. Adding it to "
         "your home screen only creates a shortcut."],
        ['Is there a login or password for the dashboard?',
         "No login. The only password is for the EMCOMM-NET Wi-Fi. FieldCommand is deliberately a "
         "no-login tool on a private, isolated network."],
        ['Which address do I type?',
         "Always <b>http://192.168.50.1</b>. Bookmark it or add it to your home screen so you "
         "never have to type it again."],
        ['Does it work with no internet?',
         "Yes. That is the whole point. Only a few features (NWS radar and alerts, APRS-IS, HF "
         "propagation) need the internet; everything else runs fully offline."],
        ['Why is the Amateur Radio button grayed out?',
         "No station callsign has been set. Open the Setup wizard and add a callsign to enable it "
         "(see 2.6). This is normal for a group with no licensed operators."],
        ['Which mode should I start in?',
         "Whichever fits the job: Amateur Radio for ham nets, the public-safety mode for radio "
         "ID and unit tracking, ICS for running an incident. You can switch any time without "
         "losing data."],
        ['Two of us see different screens — is something wrong?',
         "No. The mode is remembered per device, so each operator can be in a different mode. The "
         "underlying data is the same for everyone."],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch3():
    s = chapter(3, 'Organization Setup & Station Configuration',
                'http://192.168.50.1/setup.html')
    s.append(P(
        'Before using FieldCommand IMS for the first time, complete the Organization Setup '
        'to configure your station identity, network defaults, and — if you use one — the '
        'public-safety net settings. These values flow into Incident Command System (ICS) '
        'form headers, net logs, cover pages, and printed documents, so it is worth setting '
        'them accurately once at the start. Open it from the dashboard, fill in the fields '
        'below, and click Save at the bottom.', Lead))
    s.append(SP(4))
    s.append(note(
        'The station callsign is OPTIONAL. A group with no licensed amateur-radio operators '
        'leaves it blank, and FieldCommand keeps the Amateur Radio features grayed out while '
        'everything else works normally. Add a callsign later to turn those features on.',
        'note'))
    s.append(SP(6))

    s.append(P('3.1  Station & Organization Identity', H2))
    s.append(P('These fields identify your group on forms, logs, and printed documents.'))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['Club / Station Callsign',
         'Your group or station FCC callsign (for example, K9ESV). Leave blank if you have '
         'no licensed operators — the amateur features then stay off by design.'],
        ['Personal Callsign (Operator)',
         'The individual operator or builder callsign (for example, KE4CON). Optional.'],
        ['Organization Full Name',
         'Required. The full name of your agency or group — shown in ICS form headers and '
         'on cover pages.'],
        ['Organization Abbreviation',
         'A short form for compact displays, footers, and net-log headers (e.g. MCESV).'],
        ['Associated Agency Name',
         'The served agency or authority having jurisdiction, if any (for example, a county '
         'emergency management agency).'],
        ['Agency Abbreviation', 'The short form of the associated agency.'],
        ['City / County / State', 'Your location, used on headers and printed documents.'],
        ['Contact Email', 'A contact address shown where forms call for one. Optional.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('3.2  Position, Network, and Regional Defaults', H2))
    s.append(tbl(['FIELD', 'WHAT IT CONFIGURES'], [
        ['Latitude / Longitude (decimal)',
         'The station position (for example, 42.3247 / -88.3822). Used for HF propagation '
         'and APRS position reports.'],
        ['Grid Square (Maidenhead)',
         'The 4- or 6-character grid locator (for example, EN52wa). Used for propagation '
         'calculations and APRS.'],
        ['Default Incident Name',
         'Pre-fills the incident-name field when you create a new incident (for example, '
         '"County EOC Activation").'],
        ['Wi-Fi Network Name (SSID)',
         'The network name FieldCommand records and displays (default EMCOMM-NET). Note: the '
         'ASUS router broadcasts this network — the Pi does not (see the Network Hardware '
         'chapter).'],
        ['Wi-Fi Password',
         'Recorded here for reference; set the matching value on the router itself.'],
        ['Server Address',
         'The address operators type in their browser (default http://192.168.50.1). Change '
         'only if your network requires it.'],
        ['Time Zone',
         'Sets the time zone for every timestamp in logs and forms (for example, '
         'America/Chicago). Set it to your deployment time zone.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('3.3  Public-Safety Net Settings', H2))
    s.append(P(
        'If your group runs a public-safety (non-amateur) net, set the system details here. '
        'They label the public-safety net logger and its check-in fields, and they do not '
        'require a callsign.'))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['Primary System Name',
         'Required for the public-safety logger. The radio system name (for example, a '
         'statewide system, a mutual-aid system, or a P25 zone).'],
        ['System Type', 'The kind of system, chosen from the list.'],
        ['Unit ID Field Label',
         'Required. What each station is identified by on this system (for example, Radio '
         'ID, Unit #, Badge #, or Apparatus #). This label is used throughout the '
         'public-safety logger and check-in.'],
        ['Dispatch Center Name', 'The dispatch center for this system, if applicable.'],
        ['Secondary System Name',
         'An optional second system (for example, a mutual-aid or interoperability system).'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('3.4  Offline vs. Online Feature Table', H2))
    s.append(tbl(['FEATURE', 'OFFLINE?', 'NOTES WHEN OFFLINE'], [
        ['ICS platform — all five sections',    'Full',  'No change'],
        ['All ICS forms and IAP',               'Full',  'No change'],
        ['T-card resource board',               'Full',  'No change'],
        ['FEMA cost tracking',                  'Full',  'No change'],
        ['Event templates',                     'Full',  'No change'],
        ['IAP PDF compilation',                 'Full',  'No change'],
        ['Digital signatures on forms',         'Full',  'No change'],
        ['Net control loggers (both)',           'Full',  'No change'],
        ['FCC callsign lookup',                 'Full',  'Uses local SQLite database — no internet needed'],
        ['Member roster and QR check-in',       'Full',  'No change'],
        ['GPS resource map',                    'Full',  'No change'],
        ['Barcode / QR scan check-in',          'Full',  'No change'],
        ['Offline tactical APRS map',           'Full',  'Map tiles local — RF APRS still works'],
        ['Kiwix reference library',             'Full',  'No change'],
        ['NWS weather alerts',                  'WAN',   'Paused — last alert cached and displayed'],
        ['NEXRAD animated radar',               'WAN',   'Tiles unavailable — offline banner shown'],
        ['APRS-IS internet feed',               'WAN',   'RF APRS continues — internet feed pauses'],
        ['HF propagation data',                 'WAN',   'Last retrieved data shown until WAN returns'],
        ['AMPRNet / 44Net tunnel',              'WAN',   'Tunnel drops — local network unaffected'],
        ['Winlink Telnet sessions',             'WAN',   'RF Winlink (VARA/Pactor) continues'],
    ], widths=[2.2*inch, 0.9*inch, CW-3.1*inch]))
    s.append(SP(6))

    s.append(P('3.5  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The Amateur Radio features are grayed out',
         'No station callsign is set. Open Setup, enter your Club / Station Callsign, and '
         'save. Amateur features stay off by design until a callsign is present.'],
        ['My changes did not show up on forms or headers',
         'Make sure you clicked Save at the bottom of the Setup page, then re-open the form '
         '— headers read the saved values.'],
        ['The Wi-Fi name I set here is not being broadcast',
         'This field only records the name for display. The ASUS router broadcasts the Wi-Fi '
         '— set the matching SSID and password on the router (see the Network Hardware '
         'chapter).'],
        ['Timestamps are off by several hours',
         'The Time Zone is wrong. Set it to your deployment zone (for example, '
         'America/Chicago) and save; new entries use the corrected zone.'],
        ['I changed the Server Address and now devices cannot reach the app',
         'Put it back to the default (http://192.168.50.1). Change it only if you have also '
         'reconfigured the router and the static IP to match.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(PB())
    return s


def ch4():
    s = chapter(4, 'Member Roster & Quick Response (QR) code Check-In Codes',
                'http://192.168.50.1/roster.html')
    s.append(P(
        "The Member Roster is the central personnel database for your whole operation. It "
        "stores every member, mutual-aid visitor, and regular participant with their "
        "identifiers, license class, roles, certifications, equipment capabilities, an "
        "optional photo, and a personal check-in code. From this one page you build and "
        "search the roster, print laminate-ready photo identification (ID) cards, show a "
        "member's Quick Response (QR) check-in code, and run live check-in when an "
        "activation starts. Everything you enter here is saved on the server, so it "
        "survives a reboot and lands in the incident record and backups.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: enter your people once, and the roster feeds check-in, net logs, "
        "ID cards, and QR codes for every activation afterward.", 'tip'))
    s.append(SP(6))

    s.append(P('4.1  The Two Views: Directory and Activation', H2))
    s.append(P(
        "The roster page has two tabs across the top, each showing a live count in "
        "parentheses:"))
    s.append(P("<b>Directory</b> - every member as a card. This is where you add, search, "
               "edit, import, export, and print. It is the everyday view.", Bullet))
    s.append(P("<b>Activation</b> - the live check-in board used when an incident is "
               "running: click a member to check them in, track who is Active, Standby, or "
               "Released, and add walk-ins (see 4.7 and 4.8).", Bullet))
    s.append(P(
        "Above the tabs sits the toolbar that acts on the whole roster:"))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['Search box', 'Type any part of a name, callsign, Member ID, or Radio ID to filter '
         'the Directory instantly.'],
        ['+ Add Member', 'Opens the blank member editor (see 4.4).'],
        ['Import CSV', 'Loads members from a spreadsheet file (see 4.9). Hover the button to '
         'see the exact column list.'],
        ['Export CSV', 'Downloads the whole roster as a spreadsheet file (see 4.9).'],
        ['Print ID Cards', 'Opens a print-ready Portable Document Format (PDF) of photo ID '
         'cards with a scannable QR for every member (see 4.5).'],
        ['Print', 'Opens your browser print dialog for a paper copy of the on-screen roster.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('4.2  Reading a Member Card', H2))
    s.append(P(
        "In the Directory, each member appears as a card. At a glance the card shows the "
        "member's photo (or the first letter of their first name if no photo is stored), "
        "their name, and colored badges for the pieces of identity they have:"))
    s.append(SP(4))
    s.append(tbl(['ON THE CARD', 'WHAT IT MEANS'], [
        ['License class badge', 'The amateur license class, such as Technician or General, '
         'shown only if set.'],
        ['Role badges', 'Any assigned roles, such as Net Control or Operator.'],
        ['Callsign badge', 'The Federal Communications Commission (FCC) amateur callsign.'],
        ['Radio ID badge', 'The trunked or Project 25 (P25) radio unit number.'],
        ['Member ID badge', 'Your organization\'s internal member number.'],
        ['Certification dots', 'Five small dots for ICS-100, ICS-200, ICS-700, EmComm I, and '
         'CPR/AED - green means held, gray means not held. Hover a dot to read which one.'],
        ['QR button', 'Opens that member\'s personal check-in code (see 4.6).'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(note(
        "Click anywhere on the card (except the QR button) to open the full editor for that "
        "member.", 'note'))
    s.append(SP(6))

    s.append(P('4.3  Member Fields', H2))
    s.append(P(
        "The Add and Edit windows use the same form, grouped into labeled sections. Only a "
        "name or a callsign is really needed to save a usable record; every other field is "
        "optional and can be filled in later."))
    s.append(SP(4))

    s.append(P('4.3.1  Identifiers', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Callsign', 'The FCC amateur radio callsign (for example W8XXX). Typed in capitals '
         'automatically. Leave blank for members who are not licensed.'],
        ['Radio ID / Unit #', 'The public-service radio unit number if the member carries a '
         'P25, Digital Mobile Radio (DMR), or General Mobile Radio Service (GMRS) radio.'],
        ['Member ID', 'Your internal member number - for example an ARES, RACES, or American '
         'Radio Relay League (ARRL) number. Used as the default check-in code.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))

    s.append(P('4.3.2  Personal Information', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['First / Last Name', 'The member\'s name as it should appear on cards and logs.'],
        ['License Class', 'Chosen from a list: Amateur Extra, General, Technician, Novice, '
         'Advanced, GMRS, or No amateur license.'],
        ['Phone / Email', 'Contact details. Stored on the local server only.'],
        ['Address', 'Mailing or home address, optional.'],
        ['Grid Square', 'The Maidenhead grid locator for radio planning (for example EN90). '
         'Up to eight characters.'],
        ['Emergency Contact', 'Who to call for this member in an emergency.'],
        ['Notes', 'A free-text box for anything else worth recording.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))

    s.append(P('4.3.3  Roles, Certifications, and Equipment', H3))
    s.append(P(
        "Three grids of checkboxes capture what a member can do. Tick every box that "
        "applies:"))
    s.append(P("<b>Roles</b> - Net Control (NCS), Operator, Liaison, and Emergency "
               "Coordinator (EC).", Bullet))
    s.append(P("<b>Certifications</b> - ICS-100, ICS-200, ICS-300, ICS-400, ICS-700, "
               "ICS-800, EmComm I, EmComm II, CPR/AED, First Aid, and CERT.", Bullet))
    s.append(P("<b>Equipment</b> - HF Radio, VHF/UHF, Digital, Packet, PACTOR Modem, "
               "VARA HF, VARA FM, APRS, Winlink, Go-Box, Generator, Battery/Solar, and "
               "Vehicle Mount.", Bullet))
    s.append(SP(6))

    s.append(P('4.4  Adding and Editing Members', H2))
    s += steps([
        "Click <b>+ Add Member</b> in the toolbar.",
        "Fill in at least a name or a callsign. Add the Radio ID, Member ID, and personal "
        "details as needed.",
        "Tick the applicable Roles, Certifications, and Equipment boxes.",
        "Click <b>Save Member</b>. The member appears in the Directory right away.",
        "To change an existing member, click their card, edit any field, and click "
        "<b>Save Member</b> again.",
        "To remove someone, open their card and click <b>Delete</b>, then confirm. This "
        "removes the roster entry but does not erase past net-log or check-in history.",
    ])
    s.append(SP(6))

    s.append(P('4.5  Member Photos and Printable ID Cards', H2))
    s.append(P(
        "Each member record can hold one photo, used to print a laminate-ready ID card with "
        "a scannable QR check-in code. In the editor, under <b>Photo (for ID card)</b>, "
        "click <b>Take / upload photo</b> to use any phone or webcam picture - a "
        "head-and-shoulders shot on a plain background works best. The photo is resized "
        "automatically before it is stored, so you do not need to shrink it yourself. Click "
        "<b>Remove</b> to clear it."))
    s.append(SP(4))
    s.append(P("There are two ways to print cards:"))
    s.append(P("<b>All cards at once</b> - click <b>Print ID Cards</b> in the toolbar. This "
               "opens a PDF of cards for every member. Walk-in and mutual-aid entries are "
               "included only if they have a photo.", Bullet))
    s.append(P("<b>One card</b> - open a member, then click the <b>ID Card</b> button next "
               "to Save to print just that person.", Bullet))
    s.append(note(
        "A photo is optional. A member with no photo still gets a roster card and a QR code; "
        "they simply are not included in the printed photo-ID batch.", 'note'))
    s.append(SP(6))

    s.append(P('4.6  QR Check-In Codes', H2))
    s.append(P(
        "Every member has a personal QR code that lets them check in instantly at any "
        "activation using the Scan Check-In page (see Chapter 10). The QR button on each "
        "card opens a window with that member's code."))
    s.append(SP(4))
    s += steps([
        "Click the <b>QR</b> button on any member card.",
        "The window shows a scannable QR image, the member's name, and the code in plain "
        "text underneath. The QR image is generated by the FieldCommand server itself, so it "
        "works fully offline - no internet is required.",
        "Click <b>Print</b> to open a clean print page with the QR, the name, and the "
        "check-in code, ready to laminate or tape to a badge.",
        "Click <b>Save</b> to download the QR image so a member can keep it on their phone.",
    ])
    s.append(P(
        "The code carried by the QR is the member's barcode identifier if one was set during "
        "import; otherwise it falls back to the callsign, and then to the Member ID. If the "
        "QR image ever fails to load, the plain-text code shown below it is a working "
        "manual-entry fallback - the operator can type it into the Scan Check-In page by "
        "hand."))
    s.append(SP(6))

    s.append(P('4.7  Activation: Checking Members In', H2))
    s.append(P(
        "When an incident starts, switch to the <b>Activation</b> tab. It splits into two "
        "columns: <b>Roster - Click to Check In</b> on the left, and <b>Activated "
        "Personnel</b> on the right."))
    s.append(SP(4))
    s += steps([
        "Use the <b>Search member to check in</b> box to find a person, or scroll the left "
        "list.",
        "Click a member. A small prompt asks for their <b>Assignment</b> - type it (for "
        "example \"Shelter Net\") and confirm, or leave it blank.",
        "The member moves to the Activated Personnel column with a status of <b>Active</b>.",
        "Change anyone's status with the dropdown on their row: <b>Active</b>, "
        "<b>Standby</b>, or <b>Released</b>. Released personnel drop out of the active count.",
        "Click <b>Export Log</b> at any time to download the activation record as a "
        "spreadsheet for the incident file.",
    ])
    s.append(SP(6))

    s.append(P('4.8  Walk-In Check-In', H2))
    s.append(P(
        "A walk-in is someone who shows up to help but is not yet on the roster - a "
        "mutual-aid operator or a first-time volunteer. You can check them in without "
        "stopping to build a full record."))
    s.append(SP(4))
    s += steps([
        "On the Activation tab, click <b>+ Walk-In Check-In</b>.",
        "Enter what you know: <b>Callsign or Radio ID</b>, <b>Name</b>, <b>Organization</b>, "
        "and <b>Assignment</b>. A callsign or a name is enough.",
        "Click <b>Check In Walk-In</b>. They appear in Activated Personnel with a yellow "
        "<b>WALK-IN</b> badge.",
        "If you later want to keep them, click the <b>+ Roster</b> button on their row to "
        "save them as a permanent member you can then finish editing.",
    ])
    s.append(note(
        "Walk-ins are part of the live activation but are not saved to the permanent roster "
        "until you use + Roster. Do that before they leave if you want to keep the record.",
        'warn'))
    s.append(SP(6))

    s.append(P('4.9  Importing and Exporting via CSV', H2))
    s.append(P(
        "You can load an existing member list from a Comma-Separated Values (CSV) "
        "spreadsheet instead of typing everyone in. Click <b>Import CSV</b> and choose your "
        "file. The first row must be column headings."))
    s.append(SP(4))
    s.append(P("Recognized columns: <b>member_id, callsign, radio_id, first_name, "
               "last_name, role, phone, email, grid</b>, plus optional <b>license_class</b> "
               "and <b>roles</b> (several roles separated by semicolons).", Body))
    s.append(P(
        "Import matches each row to a member by a natural key (Member ID first, then "
        "callsign, then Radio ID, then name), so re-importing an updated file updates the "
        "existing people instead of creating duplicates. Members already on the server who "
        "are not in the file are left untouched. To go the other way, click <b>Export "
        "CSV</b>: FieldCommand downloads the whole roster as a dated CSV file you can edit "
        "in a spreadsheet or hand to another server."))
    s.append(SP(6))

    s.append(P('4.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The Directory says "Cannot reach API"',
         'The core service on port 5050 is not answering. Check the dashboard health panel '
         'and make sure the fcc-lookup service is running, then reload the page.'],
        ['A QR image will not appear',
         'The plain-text code shown under it still works - type it into the Scan Check-In '
         'page by hand. If it keeps failing, confirm the fcc-lookup service is running.'],
        ['A member is missing from the Print ID Cards batch',
         'Cards print only for members who have a photo saved (and always for walk-ins only '
         'if they have one). Open the member, add a photo, and print again.'],
        ['Import CSV added duplicate people',
         'The rows had no Member ID, callsign, or Radio ID to match on, so each became a new '
         'record. Add one of those columns and re-import to merge them.'],
        ['A walk-in disappeared after the activation',
         'Walk-ins are not permanent unless saved. Next time click + Roster on their row '
         'before they are released to keep the record.'],
        ['The activation count looks wrong',
         'Personnel marked Released are excluded from the active count by design. Set their '
         'status back to Active or Standby if they are still working.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch5():
    s = chapter(5, 'Incident Management — Creating and Managing Incidents',
                'http://192.168.50.1/incident.html')
    s.append(P(
        'All Incident Command System (ICS) work in FieldCommand IMS is organized around an <b>incident</b>. '
        'An incident holds the ICS forms, resource T-cards, personnel check-ins, '
        'cost tracking, and net log associations for one activation or exercise. '
        'You can have multiple incidents in the system simultaneously — only one '
        'is designated the <b>active incident</b> at any time.'))
    s.append(SP(6))

    s.append(P('5.1  Creating an Incident', H2))
    s += steps([
        'Navigate to <b>Incident Management</b> from the dashboard.',
        'Click <b>+ New Incident</b>.',
        'Enter the incident name, incident number (if assigned by your agency), '
        'incident type, and initial operational period.',
        'Select the incident commander from your roster, or type a name if '
        'the Incident Commander (IC) is not in the roster. For incidents operating under '
        '<b>Unified Command</b>, see Section 5.2 below.',
        'Click <b>Create Incident</b>. The incident opens immediately and becomes '
        'the active incident. The incident name appears in the dashboard header '
        'and in all form headers.',
    ])
    s.append(SP(4))
    s.append(P('The New Incident form has these fields:'))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['Incident Name', 'Required. A clear name for the activation, such as '
         '"Fox River Flooding". Shown in the dashboard header and on every form.'],
        ['Incident Number', 'Your agency\'s assigned number, if you have one '
         '(for example, 2026-0142). Optional.'],
        ['Incident Type', 'Required. The category that best fits the activation — '
         'see the list in Section 5.3.'],
        ['Jurisdiction', 'The responsible jurisdiction (for example, '
         '"McHenry County, IL"). Optional.'],
        ['Incident Location / Address', 'Where the incident is centered. Optional.'],
        ['Incident Commander', 'Pick a name from the roster or type one. For a '
         'multi-agency response, enter "Unified Command" (see Section 5.2).'],
        ['Operational Period Duration', 'How long each operational period lasts '
         '(commonly 12 or 24 hours). Used as the default for later periods.'],
        ['ICS Form Variant', 'Which edition of the ICS forms this incident uses. '
         'Leave the default unless your agency standardizes on a specific variant.'],
        ['Initial Situation Summary', 'A short description of what is happening at '
         'the time of activation.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('5.2  Command Structure — Single Incident Commander vs. Unified Command', H2))
    s.append(P(
        'ICS supports two command structures, and FieldCommand IMS accommodates both '
        'without any configuration change. The difference is a workflow convention, '
        'not a software setting.'))
    s.append(SP(4))
    s.append(tbl(['STRUCTURE', 'WHEN USED', 'HOW TO CONFIGURE IN FIELDCOMMAND'], [
        ['Single IC',
         'One agency or jurisdiction has clear authority. '
         'Most activations involving a single responding organization.',
         'Enter the IC\'s name or callsign in the Incident Commander field '
         'when creating the incident. The ICS-203 org chart will show one IC '
         'at the top of the command structure.'],
        ['Unified Command',
         'Two or more agencies or jurisdictions share command authority — '
         'common in multi-agency responses, complex disasters, or incidents '
         'crossing jurisdictional boundaries. Each contributing agency provides '
         'an IC-equivalent to the UC group. All agencies still work from '
         'a single Incident Action Plan (IAP).',
         'Enter "Unified Command" or the UC group designation in the '
         'Incident Commander field. List each UC member in the ICS-203 '
         'Organization Assignment List under the Unified Command section. '
         'All ICS forms, T-cards, and cost documentation continue to function '
         'identically — the UC structure is a labeling and documentation '
         'convention within the same incident record.'],
    ], widths=[1.3*inch, CW*0.42, CW-1.3*inch-CW*0.42]))
    s.append(SP(4))
    s.append(note(
        'Under Unified Command, each participating agency still develops its own '
        'objectives, but those objectives are reconciled into a single IAP. '
        'The Planning Section Chief role in the ICS-203 is typically filled by '
        'one agency on a rotating basis or by consensus. FieldCommand IMS '
        'supports multiple ICS-204 Assignment Lists — one per branch or division — '
        'which accommodates multi-agency operational structures naturally.', 'note'))
    s.append(SP(8))

    s.append(P('5.3  Incident Types', H2))
    s.append(P(
        'When creating an incident, pick the type that best matches the activation from a '
        'large categorized dropdown (about 32 options grouped into seven categories). '
        'The type labels the incident badge throughout the interface. '
        'All types use the same underlying ICS form set — the type is an organizational '
        'label, not a functional restriction.'))
    s.append(SP(4))
    s.append(tbl(['CATEGORY', 'EXAMPLE TYPES'], [
        ['Natural Hazards',  'Winter Storm, Flooding, Tornado / Severe Weather, Earthquake, Wildfire, Heat Emergency, Drought'],
        ['Technological',    'Hazmat / Chemical Spill, Transportation Accident, Structure Fire, Power Outage / Infrastructure, Dam Failure, Nuclear / Radiological'],
        ['Human-Caused',     'Mass Casualty Incident, Active Threat, Civil Disturbance, Terrorism'],
        ['Search & Rescue',  'Wilderness, Urban, Water, Missing Person — Dementia / Memory, Missing Person — Child'],
        ['Public Health',    'Disease Outbreak / Pandemic, Mass Casualty — Medical, Public Health Emergency'],
        ['Planned Events',   'Planned Event — Public Safety, Planned Event — EMCOMM Exercise, Drill / Training Exercise'],
        ['Other',            'Mutual Aid Request, EOC Activation, Other / All-Hazards'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(3))
    s.append(P(
        'Any incident can be flagged as a drill/exercise. Beta Reset (under incident settings) '
        'wipes exercise data while preserving the roster, channel library, and repeater database.'))
    s.append(SP(6))

    s.append(P('5.4  Operational Periods', H2))
    s.append(P(
        'ICS organizes work into <b>operational periods</b> — typically 12 or 24-hour '
        'blocks. FieldCommand IMS tracks the current operational period and uses it as '
        'the default for new T-cards, check-ins, and form entries. To advance to a new '
        'operational period, click <b>+ New Period</b> in the incident header. '
        'Prior period data is retained and viewable.'))
    s.append(SP(6))

    s.append(P('5.5  Archive, Restore, and Delete', H2))
    s.append(P(
        'After an incident closes, the full data package can be archived to a Universal Serial Bus (USB) drive '
        'for long-term storage and removed from the Pi\'s active storage.'))
    s.append(SP(4))
    s.append(tbl(['ACTION', 'WHAT IT DOES', 'REVERSIBLE?'], [
        ['Archive to USB',
         'Writes a complete JSON package (all forms, T-cards, check-ins, costs, '
         'net log associations) to /media/fieldcommand/backup/incidents/ on the '
         'labelled USB drive. Marks the incident as archived on the Pi.',
         'Yes — restore any time'],
        ['Restore from USB',
         'Reads the JSON archive from the USB drive and re-inserts all data. '
         'Restores the incident to fully active status.',
         'Yes'],
        ['Hard delete from Pi',
         'Permanently removes the incident and all associated data from the Pi SSD. '
         'Run only after confirming the archive is on USB.',
         'Permanent'],
    ], widths=[1.3*inch, CW-2.6*inch, 1.3*inch]))
    s.append(SP(4))
    s.append(note(
        'The USB drive must be labelled FIELDCOMMAND (all caps). Any USB drive '
        'with this label is recognized automatically. A LaCie Rugged or similar '
        'ruggedized 1TB USB-C drive is recommended for field use.', 'note'))
    s.append(SP(6))

    s.append(P('5.6  Exercise / Scenario Mode', H2))
    s.append(P(
        'Exercises and training scenarios can be tagged as <b>Scenario</b> when '
        'the incident is created. Scenario incidents display a yellow badge throughout '
        'the interface so operators always know they are in training mode. '
        'A <b>Beta Reset</b> wipes all scenario data — incidents, forms, costs, '
        'check-ins, T-cards, and meetings — while preserving the roster, '
        'hospital directory, channel library, and repeater database. '
        'This returns the system to a clean state for the next exercise without '
        'losing any permanent configuration data.'))
    s.append(SP(6))

    s.append(P('5.7  Working with Multiple Incidents — Selecting, Switching, and Editing', H2))
    s.append(P(
        'The Incident Management screen lists every incident on the server. You can keep '
        'several at once, but only one is the <b>active</b> incident at a time — the one all '
        'new forms, T-cards, check-ins, and costs attach to.'))
    s.append(SP(4))
    s.append(P('<b>Open / switch the active incident.</b> Click any incident in the list to '
               'open it and make it active. Its name then shows in the dashboard header and '
               'on every form. If none exist yet, the screen reads "No active incidents".',
               Bullet))
    s.append(P('<b>Check which one is active.</b> The active incident\'s name always appears '
               'in the dashboard header. Each card in the list also shows its current '
               'operational period (for example, "Period 2").', Bullet))
    s.append(P('<b>Edit an incident.</b> Click <b>Edit</b> on the incident to change its '
               'name, number, type, commander, jurisdiction, location, or summary.', Bullet))
    s.append(P('<b>Advance the operational period.</b> Click <b>Next Period</b> to open the '
               'period prompt, review the objectives carried forward, and start the next '
               'operational period (see Section 5.4).', Bullet))
    s.append(SP(6))

    s.append(P('5.8  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['My forms or T-cards are attaching to the wrong incident',
         'Check which incident is active — its name is in the dashboard header. Open the '
         'correct one from Incident Management to make it active, then continue.'],
        ['I don\'t see my incident in the list',
         'It may have been archived (Section 5.5); archived incidents are restored from the '
         'USB drive. Also confirm you are on the right server (192.168.50.1).'],
        ['Archive to USB failed or the drive was not found',
         'The backup drive must be labelled FIELDCOMMAND (all capitals) and plugged in. '
         'Re-insert it, wait a few seconds, and try the archive again.'],
        ['I can\'t delete an incident / I\'m worried about deleting one',
         'Hard delete is permanent. Archive to USB first (Section 5.5), confirm the archive '
         'is on the drive, and only then hard-delete from the Pi.'],
        ['Objectives did not carry into the new operational period',
         'Use Next Period to advance (not a brand-new incident). The carry-forward prompt is '
         'where you keep or edit the objectives for the new period.'],
        ['My exercise/scenario data will not clear',
         'Use Beta Reset in the incident settings. It wipes exercise data (incidents, forms, '
         'costs, check-ins, T-cards) but preserves the roster, channel library, and repeater '
         'database.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(PB())
    return s


def ch6():
    s = chapter(6, 'Pre-Planned Event Templates',
                'http://192.168.50.1/event_templates.html')
    s.append(P(
        'A Pre-Planned Event Template is a complete, ready-made incident setup that you '
        'activate in seconds. Instead of building an incident from a blank page while the '
        'clock is running, you choose a template that already contains the objectives, the '
        'resource types you will need, the communications plan, and the Incident Command '
        'System (ICS) organization for that kind of event. Templates remove repetitive '
        'setup work, prevent the mistakes that happen when people build under pressure, and '
        'make every activation of the same event type look and run the same way.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: a template is a saved incident blueprint — pick it, name the '
        'incident, and everything is pre-loaded and ready to adjust.', 'tip'))
    s.append(SP(6))

    s.append(P('6.1  What a Template Contains', H2))
    s.append(P(
        'Every template holds five kinds of pre-planned content. When you activate the '
        'template, each part is copied into the new incident so you can start work at once '
        'and adjust as the event develops.'))
    s.append(SP(4))
    s.append(tbl(['PART', 'WHAT IT PRE-LOADS INTO THE INCIDENT'], [
        ['Objectives',
         'The incident objectives — the ICS-202 "what we are trying to achieve" list. '
         'Plain-language goals for the operational period.'],
        ['Resources',
         'The kinds and quantities of resources you expect to need — teams, vehicles, '
         'equipment — so ordering and the T-card board start already populated.'],
        ['Channels',
         'The communications plan: named channels with receive and transmit frequencies, '
         'tone, mode, and the job each channel does.'],
        ['Organization',
         'The ICS command and general-staff roles, plus branch and division labels, so the '
         'org chart is drawn before anyone arrives.'],
        ['Safety & flags',
         'A safety message for the Safety Officer, plus optional flags that mark the '
         'template as a training scenario, a protected standard template, or a candidate '
         'for a future update.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))

    s.append(P('6.2  Built-In Templates', H2))
    s.append(P(
        'FieldCommand IMS ships with ten built-in templates covering the most common '
        'incident types. Each can be used as-is or edited to match your local protocols.'))
    s.append(SP(4))
    s.append(tbl(['TEMPLATE', 'PRE-CONFIGURED CONTENTS'], [
        ['Shelter Activation',
         'Shelter management objectives, cot and supply resource types, '
         'registration and medical channels, Red Cross coordination section'],
        ['Search & Rescue',
         'Search and Rescue (SAR) objectives, field team and K9 resource types, '
         'search sector channels, base camp and medical branches'],
        ['Severe Weather',
         'Damage assessment objectives, utility and debris resource types, '
         'shelter and Emergency Operations Center (EOC) coordination channels, public information branch'],
        ['Mass Gathering / Event',
         'Crowd management objectives, medical and security resource types, '
         'venue and dispatch channels, medical and operations branches'],
        ['HazMat / Spill',
         'Decon and zoning objectives, HazMat team resource types, '
         'hot/warm/cold zone channels, safety officer emphasis'],
        ['Planned Exercise / Drill',
         'Training objectives, evaluator and observer resource types, '
         'exercise control channel, scenario-tagged ()'],
        ['Flood Response',
         'Swiftwater rescue and evacuation objectives, boat and high-water resource '
         'types, water-rescue and evacuation channels, rescue and mass-care sections'],
        ['Wildland / Interface Fire',
         'Structure-protection and LCES objectives, engine, crew, and air resource '
         'types, ground-operations and evacuation channels, fire-suppression branch'],
        ['Winter Storm / Power Outage',
         'Warming-center and welfare-check objectives, generator and high-clearance '
         'resource types, welfare and utility-liaison channels, mass-care section'],
        ['Communications Support',
         'Net and Winlink objectives, net-control and go-kit resource types, '
         'primary-net, tactical, and digital channels, communications-unit branch'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        'The built-in set grows over time. A FieldCommand update can add new templates for '
        'situations other agencies encounter; they appear automatically after the update '
        'and never overwrite a template you have already customized.', 'note'))
    s.append(SP(6))

    s.append(P('6.3  The Two Views: Activate and Manage', H2))
    s.append(P(
        'The Event Templates screen has two views, chosen with the toggle near the top of '
        'the page:'))
    s.append(P('<b>Activate</b> — a gallery of templates for starting a real incident. This '
               'is the everyday view.', Bullet))
    s.append(P('<b>Manage</b> — the same templates shown as editable cards, for building, '
               'editing, reordering, exporting, importing, and deleting.', Bullet))
    s.append(P('Across the top are the toolbar buttons that act on the whole library:'))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['+ New Template', 'Opens the editor with a blank template.'],
        ['Import JSON', 'Loads templates from a JSON file — from another FieldCommand '
         'server or a shared pack.'],
        ['Export All', 'Downloads every template on this server as one JSON file — a '
         'backup or a share.'],
        ['Export Update Candidates', 'Downloads only the templates you have flagged for '
         'future updates (see 6.7).'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('6.4  Activating a Template', H2))
    s += steps([
        'Open <b>Event Templates</b> from the dashboard and make sure you are on the '
        '<b>Activate</b> view.',
        'Browse the gallery and click the template you want. A configuration panel opens.',
        'Enter the incident name, the date and time, and any other details you want to set '
        'before activating.',
        'Click <b>Activate Template</b>. FieldCommand creates the incident and, from the '
        'template, auto-fills its core Incident Action Plan (IAP) forms — <b>ICS-202</b> '
        '(objectives and safety message), <b>ICS-203</b> (the organization assignments), '
        'and <b>ICS-205</b> (the communications plan) — and builds a <b>T-card</b> for each '
        'resource.',
        'Use the success links that appear to open the ICS-202, ICS-203, or ICS-205 form, '
        'the T-card board, or the dashboard.',
    ])
    s.append(note(
        'Activation fills in every ICS form the template carries data for — the objectives '
        'and safety message (ICS-202), the organization (ICS-203), and the communications '
        'plan (ICS-205) — and builds the T-card board. From there you complete the rest of '
        'the Incident Action Plan (the assignment lists, medical plan, safety plan, and any '
        'other forms the incident needs) and assemble and print it in the IAP section of '
        'the app. Activation gives you the head start; the IAP section is where you finish '
        'building it.', 'note'))
    s.append(SP(6))

    s.append(P('6.5  Building or Editing a Template', H2))
    s.append(P(
        'In the Manage view, click a card to edit it, or click <b>+ New Template</b> for a '
        'blank one. The editor opens as a single form with the sections below. Every field '
        'is optional except the template name. Click <b>Save Template</b> when finished; all '
        'template data is stored on the server and is not overwritten by app updates.'))
    s.append(SP(4))

    s.append(P('6.5.1  Basic Information', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Template Name', 'Required. The name shown on the card and in the gallery — for '
         'example, "Flood Response".'],
        ['Incident Type Label', 'A short category shown under the name, such as '
         '"Flood — Water Rescue". Optional.'],
        ['Icon (emoji)', 'A single emoji shown on the card for quick recognition, such as '
         '. Optional.'],
        ['Sort Order', 'A number that sets the card position in the gallery — lower numbers '
         'appear first.'],
        ['Summary / Description', 'One line describing the template, shown on the card.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))

    s.append(P('6.5.2  Objectives', H3))
    s.append(P(
        'The incident objectives, one per line. Click <b>+ Add Objective</b> to add a line '
        'and the × to remove one. Write them as plain-language goals; they become the '
        'ICS-202 objectives on the activated incident.'))
    s.append(SP(4))

    s.append(P('6.5.3  Safety Message', H3))
    s.append(P(
        'A short safety briefing for this event type. It carries into the incident for the '
        'Safety Officer and appears with the safety information for the operational period. '
        'Use it for the standing hazards and rules that apply every time you run this kind '
        'of event.'))
    s.append(SP(4))

    s.append(P('6.5.4  Resources', H3))
    s.append(P('Each resource row has three fields:'))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Name', 'The resource label, such as "Swiftwater Rescue Team".'],
        ['Type', 'The kind of resource, chosen from a list — see the reference table in 6.8.'],
        ['Qty', 'How many of this resource the template expects — a starting number you can '
         'change on the incident.'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(4))

    s.append(P('6.5.5  Channels', H3))
    s.append(P('Each channel row is a line in the communications plan:'))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Name', 'The channel purpose name, such as "Command" or "Water Rescue Tactical".'],
        ['RX', 'Receive frequency — what the radio listens on, in megahertz (e.g. 146.520).'],
        ['TX', 'Transmit frequency — what the radio sends on. On a simplex channel, RX and '
         'TX are the same.'],
        ['Tone', 'The sub-audible tone (CTCSS/PL) if the channel needs one; leave blank for '
         'none.'],
        ['Mode', 'The radio mode — see the reference table in 6.8.'],
        ['Function', 'The job the channel does — Command, Tactical, Medical, and so on (6.8).'],
    ], widths=[1.1*inch, CW-1.1*inch]))
    s.append(SP(4))

    s.append(P('6.5.6  Organization', H3))
    s.append(P(
        'The ICS structure the incident starts with. Fill in the roles and the branch and '
        'division labels that fit this event type:'))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Operations Section Chief', 'The person or role leading tactical operations.'],
        ['Safety Officer', 'The role responsible for personnel safety and the safety message.'],
        ['Public Information Officer', 'The role handling public and media information.'],
        ['Branch label', 'The name of the first operations branch, such as '
         '"Rescue & Evacuation".'],
        ['Division A–D labels', 'Names for up to four divisions or groups under operations, '
         'such as "Swiftwater Rescue".'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))

    s.append(P('6.5.7  Flags', H3))
    s.append(P('Three checkboxes sit at the bottom of the editor:'))
    s.append(P('<b>Training scenario ()</b> — incidents started from this template are '
               'marked as exercises, not real events.', Bullet))
    s.append(P('<b>Standard template ()</b> — pins the template with the built-ins and '
               'protects it from deletion (see 6.6).', Bullet))
    s.append(P('<b>Suggest for future updates ()</b> — flags the template as a candidate '
               'to ship with FieldCommand (see 6.7).', Bullet))
    s.append(SP(6))

    s.append(P('6.6  Standard Templates and Deletion Protection', H2))
    s.append(P(
        'Templates come in three levels. The only difference is whether they can be deleted '
        '— all three are fully editable.'))
    s.append(SP(4))
    s.append(tbl(['TYPE', 'CAN EDIT?', 'CAN DELETE?'], [
        ['Built-in (shipped with FieldCommand)', 'Yes', 'No — protected'],
        ['Standard (you marked it )', 'Yes', 'No — protected'],
        ['Ordinary custom', 'Yes', 'Yes — Delete button'],
    ], widths=[3.1*inch, 1.1*inch, CW-4.2*inch]))
    s.append(P(
        'Mark a template you rely on as <b>standard ()</b> so a busy operator cannot delete '
        'it by accident during an activation. To remove a standard template, open it and '
        'un-tick the standard box first; then the Delete button returns. Built-in '
        'templates cannot be deleted at all, but they can be disabled.'))
    s.append(note(
        'To hide a built-in template you never use, open it and turn off <b>Enabled</b>. It '
        'disappears from the Activate gallery but is kept in Manage, so you can turn it back '
        'on later.', 'tip'))
    s.append(SP(6))

    s.append(P('6.7  Sharing Templates and Suggesting New Ones', H2))
    s.append(P(
        'Templates are plain JSON files, so they move easily between servers and agencies.'))
    s.append(P('<b>Export one</b> — in the editor, click <b>Export JSON</b> to download '
               'that single template.', Bullet))
    s.append(P('<b>Export all</b> — on the main screen, click <b>Export All</b> for the '
               'whole library as one file (a good backup).', Bullet))
    s.append(P('<b>Import</b> — click <b>Import JSON</b> and choose a file. Imported '
               'templates are added; if an incoming template shares an identifier with one '
               'you already have, it is added under a new identifier instead of overwriting '
               'yours.', Bullet))
    s.append(SP(4))
    s.append(P('6.7.1  Suggesting a Template for a Future Update', H3))
    s.append(P(
        'When your group builds a template for a recurring local situation that other '
        'agencies would probably find useful too, you can suggest it for a future '
        'FieldCommand release without forcing it on anyone:'))
    s += steps([
        'Open the template, tick <b>Suggest this template for future FieldCommand '
        'updates ()</b>, and save. This only flags it — nothing leaves your server yet.',
        'On the main Event Templates screen, click <b>Export Update Candidates</b>. '
        'FieldCommand downloads one JSON file containing only your flagged templates.',
        'Send that file to whoever maintains your FieldCommand build.',
    ])
    s.append(P(
        'The maintainer reviews the suggestions and can add the worthwhile ones to a future '
        'update. Shipped templates then appear automatically on every server after that '
        'update — and because updates only add templates with new identifiers, they never '
        'overwrite a template you have customized. Not every local situation belongs in the '
        'shipped product, and that is fine: a template you never flag stays entirely on your '
        'own server.'))
    s.append(SP(6))

    s.append(P('6.8  Reference — Channel and Resource Options', H2))
    s.append(P(
        'The drop-down choices in the channel and resource sections, in plain language.'))
    s.append(SP(4))
    s.append(P('6.8.1  Channel Function', H3))
    s.append(tbl(['OPTION', 'MEANING'], [
        ['Command', 'The command net — command staff and unit leaders coordinate here.'],
        ['Tactical', 'A working channel for a specific job or team on the ground.'],
        ['Medical', 'Medical coordination and patient traffic.'],
        ['Logistics', 'Ordering, supply, transport, and support traffic.'],
        ['Liaison', 'Coordination with outside agencies, the EOC, or utilities.'],
        ['Other', 'Any purpose that does not fit the categories above, such as a data channel.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(4))
    s.append(P('6.8.2  Radio Mode', H3))
    s.append(tbl(['MODE', 'MEANING'], [
        ['FM', 'Frequency Modulation — the standard voice mode on VHF/UHF (2 m, 70 cm).'],
        ['NFM', 'Narrow FM — FM at reduced deviation, used where narrow channel spacing is required.'],
        ['AM', 'Amplitude Modulation — for example, aircraft-band monitoring.'],
        ['USB', 'Upper Sideband — a common voice mode on the higher HF bands.'],
        ['LSB', 'Lower Sideband — a common voice mode on the lower HF bands.'],
        ['DIG', 'A digital mode — packet, VARA, and similar data modes such as Winlink.'],
    ], widths=[1.0*inch, CW-1.0*inch]))
    s.append(SP(4))
    s.append(P('6.8.3  Resource Type', H3))
    s.append(tbl(['TYPE', 'MEANING'], [
        ['Personnel', 'Individual people or staffed positions.'],
        ['Crew', 'An organized team that works as a single unit.'],
        ['Engine', 'A fire engine or similar apparatus.'],
        ['Vehicle', 'Any other vehicle — truck, bus, boat, or high-water vehicle.'],
        ['Equipment', 'Gear and supplies — generators, cots, go-kits, tools.'],
        ['Helicopter', 'A rotary-wing air resource.'],
        ['Other', 'Anything that does not fit the categories above.'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(6))

    s.append(P('6.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['A template I want is not in the gallery',
         'It may be disabled. Switch to the Manage view — disabled templates still appear '
         'there. Open it and turn Enabled back on.'],
        ['The Delete button is missing',
         'The template is built-in or marked standard (). Un-tick the standard box to '
         'delete it, or disable it instead.'],
        ['I imported a file but my edited template is unchanged',
         'Import never overwrites an existing template. The incoming one was added under a '
         'new identifier — look for a second card with a similar name.'],
        ['Export Update Candidates downloaded nothing',
         'No template is flagged yet. Open a template, tick "Suggest for future updates ()", '
         'save, then export again.'],
        ['Activating did not open the incident',
         'That is expected — activation shows success links instead. Click a link to open '
         'the new incident, its IAP, or its T-cards.'],
        ['My template changes disappeared after an update',
         'They should not — template data is stored on the server and updates only add new '
         'templates. Confirm you are on the right server (192.168.50.1) and the Manage view.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch7():
    s = chapter(7, 'Amateur Radio Net Control Logger',
                'http://192.168.50.1/netcontrol.html')
    s.append(P(
        'The Amateur Radio Net Control Logger is the digital net log for licensed amateur '
        'radio operations - Amateur Radio Emergency Service (ARES), Radio Amateur Civil '
        'Emergency Service (RACES), Auxiliary Communications (AUXCOMM), SKYWARN, and any '
        'other amateur net. It replaces the paper net log with a live record: you open a '
        'net, log each station as it checks in, capture message traffic, and at the end '
        'export a finished ICS-309 Communications Log ready for the Incident Action Plan '
        "(IAP). It runs several nets at once, autofills each station's name from the "
        'offline Federal Communications Commission (FCC) database, and lets section chiefs '
        'watch a read-only copy from their own devices.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: create a net, type each callsign as stations report in, and '
        'FieldCommand keeps the times, durations, and traffic - then hands you the '
        'ICS-309.', 'tip'))
    s.append(SP(6))

    s.append(P('7.1  How the Screen Is Laid Out', H2))
    s.append(P(
        'The page has four working areas. Knowing where each one lives makes the rest of '
        'this chapter quick to follow.'))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IS THERE'], [
        ['Net tabs bar (top)',
         'The <b>NET TABS</b> strip with a green <b>+ New Net</b> button, one badge per '
         'open net showing its name and check-in count, and on the right the '
         '<b>Observer Link</b>, <b>ICS-309</b>, and <b>Backup JSON</b> buttons.'],
        ['Net header',
         'The green-edged panel naming the selected net, with its <b>Opened</b>, '
         '<b>Closed</b>, and live <b>Duration</b> times, a <b>Drill Mode</b> checkbox, '
         'and the red <b>Close Net</b> button.'],
        ['Entry form + tabs',
         'The station check-in form, then three tabs - <b>Stations Logged</b>, '
         '<b>Traffic Log</b>, and <b>Roster Chips</b>.'],
        ['Sidebar (right)',
         'The <b>NET SUMMARY</b>, <b>ACTIVE NETS</b>, and <b>LAST 5 ENTRIES</b> panels '
         'that update as you log.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('7.2  Opening a Net', H2))
    s += steps([
        'Open <b>Net Control</b> from the dashboard and click the green <b>+ New Net</b> '
        'button in the NET TABS bar. The <b>Create New Net</b> window opens.',
        'Type a <b>Net Name</b> - for example, "Thursday Evening Net". This is the only '
        'required field.',
        'Choose a <b>Net Type</b> from the list (ARES Net, RACES Net, SKYWARN Net, '
        'EmComm Net, Traffic Net, Training Net, HF Net, VHF/UHF Net, or Digital Net).',
        'Type the <b>Frequency / Mode</b> (for example, "146.520 FM"), or click the amber '
        '<b>Pick</b> button to choose a channel from the ICS-205 communications plan or '
        'the Channel Library (see 7.2.1).',
        'Optionally pick a <b>Mode</b> and set an <b>open time</b>. Leave the open-time box '
        'blank to use the current moment; fill it in only to back-date a net that already '
        'started.',
        'Type the <b>Net Control Callsign</b> of the operator running the net.',
        'Click the green <b>Create Net</b> button. The net appears as a badge in the NET '
        'TABS bar, the header fills in, and the live Duration timer starts counting.',
    ])
    s.append(note(
        'You can run several nets at the same time - each gets its own badge. Click any '
        'badge to switch to that net. Every button on the top bar (Observer Link, ICS-309, '
        'Backup JSON) always acts on the net you currently have selected.', 'note'))
    s.append(SP(4))
    s.append(P('7.2.1  Picking a Channel Instead of Typing', H3))
    s.append(P(
        'The <b>Pick</b> button next to the Frequency / Mode box opens a searchable '
        '<b>Select Channel</b> list. It pulls channels from the incident ICS-205 (tagged '
        '<b>205</b>), the repeater database (tagged <b>RPT</b>), and the Channel Library '
        '(tagged <b>LIB</b>), and shows each channel name, receive frequency, mode, and '
        'sub-audible tone. Click a channel and its frequency and mode drop straight into '
        'the net. If no channels are set up, the app tells you to type the frequency '
        'by hand.'))
    s.append(SP(6))

    s.append(P('7.3  Logging Check-Ins', H2))
    s.append(P(
        'Once a net is selected, the check-in form appears above the tabs. Logging a '
        'station takes one field and one key.'))
    s.append(SP(4))
    s += steps([
        'Type the reporting station\'s callsign in the <b>Callsign</b> box. It forces '
        'upper case as you type.',
        'When you finish the callsign, FieldCommand looks it up in the offline FCC '
        'database and fills the <b>Name</b> box automatically (see 7.4). Correct or add '
        'the name if needed.',
        'Set the <b>status</b> drop-down if this is more than a plain check-in (the '
        'choices are Check-In, Traffic, Priority, Emergency, Net Control, Check-Out, '
        'Mobile, and Portable).',
        'Optionally add a <b>Location/Grid</b>, a <b>precedence</b> (Routine, Welfare, '
        'Priority, or Emergency), and free-text <b>Remarks / Traffic</b>.',
        'If this station is filling an incident job, choose an <b>ICS Position</b> from '
        'the grouped list and type the <b>Incident ID</b>; an <b>ICS-211</b> link then '
        'appears to open the Check-In List.',
        'Press <b>Enter</b> or click the green <b>LOG ENTRY</b> button. The station appears '
        'in the Stations Logged list with a timestamp, and the sidebar counts update. '
        'Click <b>Clear</b> to empty the form without logging.',
    ])
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Callsign', 'The station identifier - the only field you truly must enter. '
         'Triggers the FCC lookup.'],
        ['Name', 'The operator name. Filled from the FCC database; you can overwrite it.'],
        ['status', 'How this station is reporting - check-in, traffic, emergency, mobile, '
         'and so on.'],
        ['Location/Grid', 'Where the station is - a town, address, or Maidenhead grid '
         'square.'],
        ['precedence', 'Message urgency - Routine, Welfare, Priority, or Emergency. It '
         'color-codes the row.'],
        ['Remarks / Traffic', 'A short note about the station or a message it is passing.'],
        ['ICS Position', 'The Incident Command System job the operator holds, chosen from '
         'a grouped list (Command, Operations, Planning, and so on). Optional.'],
        ['Incident ID', 'The incident this check-in belongs to, so it can flow to the '
         'ICS-211 Check-In List. Optional.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('7.4  The FCC Autofill Card', H2))
    s.append(P(
        'FieldCommand stores the entire United States amateur license database - more than '
        '800,000 licensees - on the Pi itself, so lookups work with no internet. As soon '
        'as you type a valid callsign, a blue <b>autofill card</b> appears above the form '
        'showing what the FCC has on file.'))
    s.append(SP(4))
    s.append(tbl(['CARD FIELD', 'WHAT IT SHOWS'], [
        ['Name', 'The licensed operator or club name on record.'],
        ['Class', 'The license class - Technician, General, Amateur Extra, and so on.'],
        ['Status', 'Whether the license is active, expired, or otherwise.'],
        ['Location', 'The city and state on the license.'],
        ['Expires', 'The license expiration date.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(note(
        'The lookup only runs while the <b>Auto FCC lookup</b> checkbox at the bottom '
        'right of the form is ticked. Turn it off to log a special-event or tactical '
        'callsign the FCC would not recognize.', 'tip'))
    s.append(SP(6))

    s.append(P('7.5  Managing Logged Stations', H2))
    s.append(P(
        'Every logged station is a row in the <b>Stations Logged</b> tab. The newest sits '
        'at the top. Each row shows the time, the callsign and name, a colored status '
        'badge, and a running <b>Duration</b>. Three buttons sit on the right of each row.'))
    s.append(SP(4))
    s.append(tbl(['CONTROL / TAG', 'WHAT IT DOES'], [
        ['Check Out', 'Marks the station as leaving the net. The checkout time is stamped '
         'and the participation duration stops climbing. Once out, the button reads '
         '"Out" and is grayed.'],
        ['+ Roster', 'Adds a station that is not yet on your roster to the permanent '
         'roster, assigning it a member ID. Shows only for stations not already on file.'],
        ['x (remove)', 'Deletes the entry from this net - use it to clear a mistaken '
         'log.'],
        ['WALK-IN tag', 'An amber flag on a station logged by name with no FCC-verified '
         'callsign.'],
        ['ESV tag', 'A blue member-ID tag shown when the station matches your roster.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(note(
        'Participation duration is rounded <b>up to the nearest quarter-hour</b> - so a '
        'station on the net for 6 minutes counts as 15 minutes. This is deliberate: it '
        'matches how volunteer time is documented for reimbursement and cost recovery.',
        'note'))
    s.append(SP(6))

    s.append(P('7.6  The Traffic Log', H2))
    s.append(P(
        'Formal message traffic - radiograms and welfare messages - belongs in the '
        '<b>Traffic Log</b> tab, separate from station check-ins. On the ICS-309 this '
        'traffic is the main content, so log it here rather than burying it in remarks.'))
    s.append(SP(4))
    s += steps([
        'Click the <b>Traffic Log</b> tab.',
        'Fill the <b>From callsign</b>, the <b>To callsign/address</b>, a message '
        '<b>type</b> (Radiogram, Health & Welfare, Official, Priority, or Emergency), and '
        'a short <b>Message summary</b>.',
        'Click <b>Log Traffic</b>. The message is stamped and listed newest-first, and '
        'the sidebar Traffic count goes up.',
    ])
    s.append(SP(6))

    s.append(P('7.7  Roster Chips - One-Click Check-Ins', H2))
    s.append(P(
        'For a recurring net with the same regulars, the <b>Roster Chips</b> tab turns '
        'each member into a clickable button. Click the dashed <b>import roster</b> area '
        '(or drag a file onto it) and pick a <b>CSV or JSON</b> file of your members. Each '
        'becomes a chip showing callsign and name. Clicking a chip drops that station into '
        'the check-in form and runs the FCC lookup, so you only press Enter to log it. A '
        'CSV needs a header row with a <b>callsign</b> (or <b>call</b>) column and a '
        '<b>name</b> column, or separate <b>first_name</b> and <b>last_name</b> columns.'))
    s.append(SP(6))

    s.append(P('7.8  Drill Mode', H2))
    s.append(P(
        'When you are training rather than running a real event, tick the <b>Drill Mode</b> '
        'checkbox in the net header. A bold <b>DRILL / EXERCISE - NOT ACTUAL EMERGENCY</b> '
        'banner appears across the top, and any ICS-309 you export from that net is stamped '
        'with a large diagonal <b>DRILL EXERCISE</b> watermark. This keeps practice logs '
        'from ever being mistaken for real incident records. Un-tick the box to return the '
        'net to normal.'))
    s.append(SP(6))

    s.append(P('7.9  Closing a Net and Exporting the ICS-309', H2))
    s += steps([
        'When the net is over, click the red <b>Close Net</b> button in the header and '
        'confirm. Every station still checked in is <b>automatically checked out</b> at '
        'the net-close time, so no duration is left open-ended.',
        'The header now shows the final <b>Opened</b>, <b>Closed</b>, and total '
        '<b>Duration</b>.',
        'Click the <b>ICS-309</b> button on the top bar. FieldCommand builds the finished '
        'Communications Log and both downloads it as a file and opens it in a print window.',
        'Review or print it, then attach it to the Incident Action Plan.',
    ])
    s.append(P(
        'The exported ICS-309 carries a summary block (net type, frequency and mode, open '
        'and close times, total duration, total check-ins, and total messages), the full '
        '<b>Message Traffic Log</b>, and the full <b>Station Check-In Log</b> with each '
        "operator's rounded-up participation duration and member ID. A closed net is not "
        'deleted - it moves into the <b>Closed nets</b> drop-down in the tabs bar, so you '
        'can reopen and re-export it any time.'))
    s.append(note(
        'The <b>Dead Man\'s Switch</b> (Chapter 12) watches net activity and sounds an '
        'alert if no check-in is logged within a set time window. It is meant for safety '
        'monitoring during Search and Rescue (SAR) and field operations, where radio '
        'silence can mean trouble.', 'note'))
    s.append(SP(6))

    s.append(P('7.10  Observer Link and Backup', H2))
    s.append(P(
        'Two more top-bar buttons help you share and protect a net. <b>Observer Link</b> '
        'copies a read-only web address for the selected net; hand it to a section chief '
        'or served agency and they watch the same log update on their own device - the '
        'observer page refreshes on its own and cannot change anything. <b>Backup JSON</b> '
        'downloads the entire net - every check-in, message, and roster chip - as a single '
        'data file you can archive or move to another server. Net data also lives on the '
        'server itself, so a browser refresh never loses a log.'))
    s.append(SP(6))

    s.append(P('7.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The callsign name does not autofill',
         'Confirm the <b>Auto FCC lookup</b> checkbox is ticked, and type at least three '
         'characters. Club and brand-new callsigns may not be in the FCC database - just '
         'type the name by hand.'],
        ['LOG ENTRY says "Select a net first"',
         'No net is selected. Click a net badge in the NET TABS bar, or click <b>+ New '
         'Net</b> to create one, then log again.'],
        ['The net badges say "Cannot reach API server"',
         'The core API service is not answering. Check that you are on the '
         '192.168.50.1 server and that the fcc-lookup service is running (see the Health '
         'dashboard).'],
        ['Pick shows "No channels found"',
         'No ICS-205 or Channel Library is set up for this incident. Type the frequency '
         'and mode by hand, or build the communications plan first.'],
        ['A station\'s duration keeps climbing after it left',
         'It was never checked out. Click <b>Check Out</b> on that row, or close the net - '
         'closing checks out everyone still on.'],
        ['The ICS-309 has a DRILL watermark on a real event',
         'The net has Drill Mode on. Un-tick <b>Drill Mode</b> in the header, then export '
         'the ICS-309 again.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s

