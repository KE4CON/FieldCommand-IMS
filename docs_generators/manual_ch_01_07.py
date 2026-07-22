#!/usr/bin/env python3
"""manual_ch_01_07.py — Chapters 1–7 of the FieldCommand IMS User Manual.
Universal edition — no organization-specific content.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *


def ch1():
    s = chapter(1, 'Introduction & System Overview')

    # ── Opening — the problem statement ─────────────────────────────────────
    s.append(P(
        'When a disaster takes down commercial infrastructure — cellular networks, internet, '
        'power — the tools modern emergency management depends on disappear precisely when '
        'they are needed most. Incident logs revert to paper. Resource tracking becomes a '
        'whiteboard. ICS forms are filled out by hand, photocopied, and hand-carried between '
        'rooms. Situational awareness degrades to whatever one person can hold in their head. '
        'Every organization that has worked a major activation knows this failure mode, and '
        'most have simply accepted it as the cost of doing business.', Lead))
    s.append(SP(4))
    s.append(P(
        'FieldCommand IMS was built to eliminate that failure mode. It is a complete, '
        'self-contained incident management platform that carries its own network, its own '
        'server, and its own tools — and it operates with no internet connection, no cellular '
        'service, and no outside infrastructure of any kind. The cell towers are down, the '
        'internet is gone, and you are running on a generator in a parking lot. '
        'That is exactly when you need incident management software most — and that is '
        'exactly when FieldCommand IMS is designed to perform.'))
    s.append(SP(8))

    # ── What it is ───────────────────────────────────────────────────────────
    s.append(P('1.1  What FieldCommand IMS Is', H2))
    s.append(P(
        'FieldCommand IMS is a <b>complete ICS/NIMS all-hazards incident management system</b> '
        '— not simply an amateur radio tool. It is designed to manage the full lifecycle of '
        'any incident from initial response through demobilization, using standard ICS forms '
        'and workflows. It runs on a Raspberry Pi 5 server and broadcasts its own private '
        'Wi-Fi access point. Any smartphone, tablet, or laptop that connects to that network '
        'immediately has access to the full suite of tools through a standard web browser — '
        'no app installation, no accounts, and no per-device configuration required.'))
    s.append(SP(4))
    s.append(P(
        'Version 1.0 provides 48 web-based tools covering every phase of incident management: '
        'command setup, incident action plan development, resource tracking, personnel check-in, '
        'communications logging, situational awareness, logistics, finance, and demobilization. '
        'When internet connectivity is available, live features activate automatically — '
        'NWS weather alerts, APRS-IS, animated NEXRAD radar, and HF propagation data. '
        'If internet connectivity is lost at any point, all core tools continue without '
        'interruption. The system degrades gracefully and recovers automatically.'))
    s.append(SP(8))

    # ── How it differs from other ICS platforms ──────────────────────────────
    s.append(P('1.2  How FieldCommand IMS Differs From Other ICS Platforms', H2))
    s.append(P(
        'Platforms such as WebEOC, E-Team, NIMSIAP, NIMS Logic, and E-iSuite deliver '
        'powerful incident management capability — but every one of them assumes a working '
        'internet connection and a functioning server infrastructure. They are cloud-dependent '
        'by design. When a major disaster disables the very infrastructure those platforms '
        'rely on, they go offline with it. The capability disappears at exactly the moment '
        'it is most critical.'))
    s.append(SP(4))
    s.append(P(
        'FieldCommand IMS is built on the opposite assumption: that infrastructure will fail, '
        'and that incident management capability must survive that failure. It does this by '
        'carrying its own infrastructure — server, network, storage, and tools — in a single '
        'deployable package. It does not connect to any external service for core operations. '
        'It does not require an IT department to stand up. It does not carry per-seat licensing '
        'fees. And it does not fail when the internet fails.'))
    s.append(SP(6))
    s.append(tbl(['PLATFORM', 'OFFLINE?', 'DEPLOYABLE?', 'NATIVE EMCOMM?', 'COST'], [
        ['FieldCommand IMS',
         '✓ Fully offline — all features',
         '✓ Deploys in under 30 minutes',
         '✓ Amateur radio + public safety native',
         'Free / open source'],
        ['WebEOC',
         '✗ Cloud-dependent',
         '✗ Requires server infrastructure',
         '✗ None',
         '$10,000–50,000/year'],
        ['E-Team',
         '✗ Cloud-dependent',
         '✗ Requires server infrastructure',
         '✗ None',
         'Subscription / agency contract'],
        ['NIMSIAP',
         '✗ Internet required',
         '✗ Requires connectivity',
         '✗ None',
         'Subscription'],
        ['E-iSuite',
         '△ Limited offline mode',
         '△ Laptop install — no built-in network',
         '✗ None',
         'License fee'],
    ], widths=[1.4*inch, 0.85*inch, 1.05*inch, 1.15*inch, CW-4.45*inch]))
    s.append(SP(6))
    s.append(P(
        'The feature that sets FieldCommand IMS apart from every platform in this category '
        'is its native integration of amateur radio and public safety communications directly '
        'into the incident management workflow. No other ICS platform includes built-in net '
        'control logging, FCC callsign validation against the full national licensee database, '
        'APRS tactical mapping, Winlink radio email, JS8Call HF messaging, or AMPRNet gateway '
        'capability. These are not add-ons — they are core features, fully integrated with '
        'the ICS platform so that radio traffic, net logs, and check-in data flow directly '
        'into ICS-309 communications logs, ICS-214 activity logs, and the IAP.'))
    s.append(SP(8))

    # ── Key capabilities summary ─────────────────────────────────────────────
    s.append(P('1.3  Key Capabilities at a Glance', H2))
    s.append(tbl(['CAPABILITY AREA', 'WHAT IT PROVIDES'], [
        ['ICS/NIMS Incident Management',
         'Full five-section ICS structure — Command, Operations, Planning, Logistics, '
         'Finance/Admin. Complete IAP form set including ICS-202 through ICS-221. '
         'Live T-card resource board. Planning P cycle tracking. Digital signatures. '
         'One-click IAP PDF assembly. FEMA/USCG/NWCG form variants selectable per form.'],
        ['Amateur Radio EMCOMM',
         'Net control logger with FCC callsign auto-fill from offline database of '
         '800,000+ licensees. Net open/close timestamps, check-out tracking, ICS-309 '
         'export. APRS tactical map with live station overlay. Winlink and Pat radio '
         'email integration. JS8Call HF digital messaging. AMPRNet (44Net) gateway.'],
        ['Public Safety Communications',
         'Separate net logger for trunked/P25 radio systems. Radio ID-based check-in. '
         'EMA member ID lookup. Interoperable with amateur radio nets on the same '
         'incident. ICS-309 export with agency-standard format.'],
        ['Situational Awareness',
         'Offline APRS tactical mapping. Live NWS weather alerts (when internet up). '
         'Animated NEXRAD radar loop with county overlays. GPS-tracked resource map '
         'with status-coded markers. HF propagation tool. Barcode/QR check-in scanning.'],
        ['Resource & Personnel',
         'Member roster with certifications, radio IDs, and barcode check-in codes. '
         'QR code generator per member. T-card resource board by type/status/assignment. '
         'FEMA PA cost tracking for labor, equipment, and materials. FEMA equipment '
         'rate schedule with 44 built-in rates.'],
        ['Incident Action Plan',
         'Pre-planned event templates for 6 common incident types. FEMA reimbursement '
         'documentation with PA cost tracking. Digital signature capture on all forms. '
         'One-click IAP PDF compilation. Print center for on-site IAP packages.'],
        ['WAN & Connectivity',
         'Dual WAN source support — any cellular modem, phone hotspot, or satellite. '
         'Preferred/fallback role configuration. Automatic failover. Real-time WAN '
         'status dashboard. Configurable detection per source type.'],
        ['Reference & Offline Content',
         'Kiwix offline Wikipedia and reference library. Radio frequency cheat sheets. '
         'Hospital and facilities directory. Repeater database. HF propagation data.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(8))

    # ── Architecture overview ────────────────────────────────────────────────
    s.append(P('1.4  System Architecture', H2))
    s.append(P(
        'FieldCommand IMS uses two Raspberry Pi 5 computers. The primary server runs the '
        'full application suite and broadcasts the EMCOMM-NET Wi-Fi access point. A dedicated '
        'secondary Pi, connected to the same wired switch, serves as an optional AMPRNet '
        '(44Net) gateway — maintaining a permanent WireGuard tunnel into the 44.0.0.0/8 '
        'amateur radio IP network when internet is available. '
        'One or more Wi-Fi routers extend coverage to additional rooms, outdoor staging areas, '
        'or upper floors as needed. The entire system can be powered from shore power, '
        'battery, or a generator.'))
    s.append(SP(4))
    s.append(tbl(['COMPONENT', 'FUNCTION', 'DEFAULT IP'], [
        ['FieldCommand Pi 5',
         'Primary application server · all 48 web tools · 12+ background services · '
         'RAID 1 NVMe storage · EMCOMM-NET AP',
         '192.168.50.1'],
        ['44Net Gateway Pi 5  (optional)',
         'AMPRNet WireGuard tunnel · callsign-authenticated access · '
         'Part 97 access log · isolated from primary server',
         '192.168.50.2'],
        ['Wi-Fi router  (primary)',
         'DHCP server · AiMesh controller · dual WAN management · '
         'EMCOMM-NET SSID',
         '192.168.50.254'],
        ['Wi-Fi mesh nodes  (optional)',
         'EMCOMM-NET coverage extension · seamless roaming · '
         'same SSID as primary',
         'Assigned by DHCP'],
        ['Operator workstations',
         'Any device with a modern browser — smartphones, tablets, laptops, '
         'Raspberry Pi 500 desktops',
         'Assigned by DHCP'],
    ], widths=[1.7*inch, CW-2.7*inch, 1.0*inch]))
    s.append(SP(6))
    s.append(note(
        'The default IP address of the FieldCommand server is 192.168.50.1. '
        'This address is configurable during installation. All documentation examples '
        'use the default. If your deployment uses a different address, substitute it '
        'wherever 192.168.50.1 appears.', 'note'))
    s.append(PB())
    return s


def ch2():
    s = chapter(2, 'Getting Started — Connecting to FieldCommand',
                'http://192.168.50.1')
    s.append(P(
        'Every tool in FieldCommand IMS is a web page served from the Pi at '
        '192.168.50.1 (or your configured address). No app installation is required '
        'on any device. Any modern browser works — Chrome, Firefox, Safari, Edge, '
        'or the built-in browser on Android or iOS.'))
    s.append(SP(6))

    s.append(P('Connecting for the First Time', H2))
    s += steps([
        'Power on the FieldCommand Pi and wait approximately 45 seconds for all '
        'services to start. The status LED on the Pi case (if fitted) will turn solid '
        'when the server is ready.',
        'On any smartphone, tablet, or laptop, open the Wi-Fi settings and connect to '
        'the <b>EMCOMM-NET</b> network. The default password is printed on the equipment '
        'case label and in the Installation Guide. No other credentials are required.',
        'Open a browser and navigate to <b>http://192.168.50.1</b>. The FieldCommand '
        'dashboard loads immediately. If the page does not appear, confirm you are '
        'connected to EMCOMM-NET and not to a different network.',
        'Bookmark the dashboard URL. On a smartphone, use <b>Add to Home Screen</b> '
        'to create a shortcut — the web app is designed to work like a native app '
        'once bookmarked.',
        'From the dashboard, select the tool you need. All tools are accessible from '
        'a single page organized by function. No login is required for any tool.',
    ])
    s.append(SP(6))

    s.append(P('Dashboard Modes', H2))
    s.append(P(
        'The dashboard presents three selectable modes that filter which tools appear '
        'prominently based on your current role. You can switch modes at any time — '
        'switching does not affect any data and all tools remain accessible.'))
    s.append(SP(4))
    s.append(tbl(['MODE', 'TOOLS SHOWN', 'BEST FOR'], [
        ['All-Hazards ICS',
         'Full ICS platform, IAP tools, resource tracking, personnel check-in, '
         'FEMA cost documentation, event templates',
         'Active incidents requiring ICS structure — any scale or type'],
        ['Amateur Radio EMCOMM',
         'Net control logger, FCC callsign lookup, APRS map, Winlink, '
         'JS8Call, AMPRNet gateway, propagation',
         'Amateur radio net operations, ARES/RACES activations'],
        ['Public Safety',
         'Starcom/trunked net logger, radio ID roster, resource map, '
         'WAN status, weather radar',
         'Public safety radio net operations, Starcom check-in nets'],
    ], widths=[1.2*inch, CW-2.5*inch, 1.3*inch]))
    s.append(SP(6))

    s.append(P('WAN Status Indicators', H2))
    s.append(P(
        'The top of the dashboard always displays a WAN status bar showing internet '
        'connectivity and, if configured, AMPRNet gateway status. The color and label '
        'change automatically every 30 seconds.'))
    s.append(SP(4))
    s.append(tbl(['INDICATOR', 'MEANING'], [
        ['🟢 Green — Cellular',    'Primary internet source (cellular modem, hotspot) is active'],
        ['🔵 Blue — Satellite',    'Satellite internet is active (cellular has failed over)'],
        ['🔴 Red — Offline',       'No internet — all core tools remain fully operational'],
        ['🟢 AMPRNet Connected',   '44Net WireGuard tunnel is up and routing'],
        ['🔴 AMPRNet Offline',     '44Net tunnel is down or gateway Pi is unreachable'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))
    s.append(note(
        'A red WAN indicator means internet-dependent features (NWS radar, APRS-IS, '
        'HF propagation, FCC database updates) are paused. It does not mean '
        'FieldCommand IMS is unavailable — all ICS tools, net loggers, roster, '
        'forms, and local map features continue operating normally.', 'note'))
    s.append(PB())
    return s


def ch3():
    s = chapter(3, 'The Main Dashboard',
                'http://192.168.50.1/index.html')
    s.append(P(
        'The dashboard is the home screen and navigation hub for all FieldCommand tools. '
        'It loads automatically when you navigate to the server address. Every tool card '
        'on the dashboard launches the corresponding page in the same browser tab — the '
        'back button or the navigation bar returns you to the dashboard.'))
    s.append(SP(6))

    s.append(P('Dashboard Layout', H2))
    s.append(tbl(['SECTION', 'CONTENTS'], [
        ['WAN & AMPRNet status bar',
         'Live connectivity status — polls every 30 seconds. '
         'Cellular, satellite, or offline indicator. AMPRNet gateway dot.'],
        ['Mode selector',
         'Three tabs: All-Hazards ICS · Amateur Radio EMCOMM · Public Safety. '
         'Filters which tool cards appear in the main grid.'],
        ['Tool card grid',
         'One card per tool. Color-coded by section: blue = operations, '
         'amber = public safety, purple = ICS forms, green = reference. '
         'Click any card to launch that tool.'],
        ['Quick actions',
         'Bottom strip: current incident name, active period, and links to '
         'the most recent net log and the print center.'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(6))

    s.append(P('Offline vs. Online Features', H2))
    s.append(P(
        'The following table shows which features require internet connectivity and '
        'which operate fully offline. All core incident management functions are offline.'))
    s.append(SP(4))
    s.append(tbl(['FEATURE', 'OFFLINE?', 'WHAT CHANGES WHEN OFFLINE'], [
        ['ICS platform (all five sections)', '✓ Full', 'Nothing — fully offline'],
        ['IAP form set (all ICS forms)',     '✓ Full', 'Nothing — fully offline'],
        ['T-card resource board',            '✓ Full', 'Nothing — fully offline'],
        ['Net control loggers (both)',       '✓ Full', 'Nothing — fully offline'],
        ['FCC callsign lookup',              '✓ Full', 'Uses local SQLite database — no internet needed'],
        ['Member roster',                   '✓ Full', 'Nothing — fully offline'],
        ['Offline tactical map (APRS)',      '✓ Full', 'Map tiles local — RF APRS still works'],
        ['Resource map (GPS)',               '✓ Full', 'Nothing — fully offline'],
        ['Kiwix reference library',         '✓ Full', 'Nothing — fully offline'],
        ['NWS weather alerts',              '△ WAN', 'Alerts pause — last alert cached and shown'],
        ['NEXRAD animated radar',           '△ WAN', 'Offline overlay shown; radar tiles unavailable'],
        ['APRS-IS live feed',               '△ WAN', 'RF APRS still works; internet feed pauses'],
        ['HF propagation data',             '△ WAN', 'Last retrieved data shown until refresh'],
        ['AMPRNet / 44Net tunnel',          '△ WAN', 'Tunnel drops; local EMCOMM-NET unaffected'],
    ], widths=[2.1*inch, 0.7*inch, CW-2.8*inch]))
    s.append(PB())
    return s


def ch4():
    s = chapter(4, 'Member Roster',
                'http://192.168.50.1/roster.html')
    s.append(P(
        'The Member Roster is the central personnel database for your organization. '
        'It stores every member, mutual-aid visitor, and regular participant — with '
        'their callsign, radio ID, certifications, equipment capabilities, and a unique '
        'check-in code that enables rapid QR/barcode check-in at activations.'))
    s.append(SP(6))

    s.append(P('Roster Fields', H2))
    s.append(tbl(['FIELD', 'PURPOSE'], [
        ['Member ID',        'Your organization\'s internal identifier (e.g. ESV-042)'],
        ['Callsign',         'FCC amateur radio callsign — leave blank for non-licensed members'],
        ['Radio ID',         'Public safety or trunked radio ID if applicable'],
        ['Barcode ID',       'QR/barcode check-in code — defaults to Member ID; can be overridden '
                             'with a facility badge number or custom code'],
        ['Name',             'First and last name'],
        ['Role',             'Primary function (Operator, Net Control, Logistics, etc.)'],
        ['Member type',      'Member · Visitor · Mutual Aid — affects check-in form behavior'],
        ['Certifications',   'ICS-100/200/300/400/700/800, EmComm levels 1–2, CPR, First Aid, CERT'],
        ['Equipment',        'HF, VHF, digital modes, APRS, Winlink, go-box, generator, vehicle'],
        ['Phone / Email',    'Contact information — stored locally, never transmitted externally'],
        ['Grid square',      'Maidenhead grid locator for RF planning'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))

    s.append(P('Adding Members', H2))
    s += steps([
        'Click <b>+ Add Member</b> at the top of the roster page.',
        'Enter the member\'s ID, name, and at minimum one identifier — callsign, '
        'radio ID, or member ID. All three can be filled if applicable.',
        'Select certifications and equipment capabilities using the checkboxes.',
        'Click <b>Save</b>. The member appears immediately in the roster list.',
        'To generate a QR check-in code for the member, click the <b>QR</b> button '
        'on their roster card. The code can be printed or saved as a PNG for the '
        'member to store on their phone.',
    ])
    s.append(SP(6))

    s.append(P('Importing Members via CSV', H2))
    s.append(P(
        'If your organization maintains a member list in a spreadsheet, you can import '
        'it directly using the <b>📥 Import CSV</b> button. The CSV must contain at minimum '
        'a <b>member_id</b> column. All other columns are optional and will be skipped '
        'if not present. Existing members with the same member_id are updated; '
        'new member IDs are added.'))
    s.append(SP(4))
    s.append(P('Required CSV column header: <b>member_id</b>', CS))
    s.append(P('Optional headers: <b>callsign · radio_id · first_name · last_name · '
               'role · phone · email · grid</b>', CS))
    s.append(SP(6))

    s.append(note(
        'The roster is stored in the local SQLite database on the Pi. '
        'It is included in all automatic backups. Exporting the roster as CSV '
        '(📤 Export CSV) is recommended before any software update.', 'note'))
    s.append(PB())
    return s


def ch5():
    s = chapter(5, 'Operator Identity System',
                'http://192.168.50.1/roster.html')
    s.append(P(
        'The Operator Identity System provides printed and digital identification cards '
        'for personnel at activations and exercises. Cards are generated from the roster '
        'database and can be printed on standard paper and laminated, or displayed '
        'digitally on a phone or tablet.'))
    s.append(SP(6))

    s.append(P('What an Identity Card Shows', H2))
    s.append(tbl(['ELEMENT', 'CONTENT'], [
        ['Name',                'Full name from roster'],
        ['Member ID',           'Organization member number or visitor ID'],
        ['Callsign / Radio ID', 'Amateur callsign, public safety radio ID, or both'],
        ['Role',                'Primary function at this activation'],
        ['Certifications',      'ICS levels and special certifications as colored badges'],
        ['Organization',        'Deploying agency or club name'],
        ['QR check-in code',    'Scannable code for instant check-in at future activations'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('Generating Identity Cards', H2))
    s += steps([
        'Navigate to the roster page and locate the member.',
        'Click the member card to open the detail view.',
        'Click <b>🪪 Print ID Card</b>. A print-ready card opens in a new tab.',
        'Print on card stock (Avery 5392 or similar) or standard paper for lamination. '
        'Cards are sized to fit a standard ID badge holder (3.375" × 2.125").',
        'For walk-in mutual-aid personnel without a roster entry, use '
        '<b>+ Walk-In Check-In</b> on the roster page to create a temporary record '
        'and generate a one-time card.',
    ])
    s.append(SP(6))

    s.append(P('QR Codes for Rapid Check-In', H2))
    s.append(P(
        'Every member can carry a personal QR code that enables instant check-in at '
        'any activation using the Scan Check-In page. The QR button on each roster card '
        'opens a modal with the member\'s personal code. When internet is available, '
        'the code is rendered as a true QR image. When offline, a large-text fallback '
        'displays the scannable ID for manual entry. Both the QR image and the text '
        'code can be printed or saved as a PNG.'))
    s.append(PB())
    return s


def ch6():
    s = chapter(6, 'Amateur Net Control Logger',
                'http://192.168.50.1/netcontrol.html')
    s.append(P(
        'The Amateur Net Control Logger provides a complete net management interface '
        'for licensed amateur radio operations including ARES, RACES, AUXCOMM, and '
        'any other amateur net. It replaces paper net logs with a live digital record '
        'that feeds directly into the ICS-309 communications log for the incident '
        'action plan.'))
    s.append(SP(6))

    s.append(P('Opening a Net', H2))
    s += steps([
        'Navigate to <b>Net Control Logger</b> from the dashboard.',
        'Enter the net name, frequency, and mode (SSB/FM/Digital/Other).',
        'Select the net type: <b>Amateur</b> (for ARES/RACES/AUXCOMM nets).',
        'Click <b>Open Net</b>. The net opens with a timestamp. The net status '
        'banner turns green and shows the elapsed time.',
        'The page URL now contains the net ID — share this URL with the '
        '<b>🔗 Observer Link</b> button so section chiefs or served agencies can '
        'monitor the net in read-only view on their own devices.',
    ])
    s.append(SP(6))

    s.append(P('Logging Check-Ins', H2))
    s.append(P(
        'When a station checks in, type their callsign in the check-in box and press '
        'Enter. FieldCommand IMS looks up the callsign instantly in the offline FCC '
        'database and fills in the operator\'s full name and license class automatically. '
        'If the station is on your roster, their EMA or member ID is filled as well. '
        'No internet is required for callsign lookup — the full national database of '
        '800,000+ amateur licensees is stored locally on the Pi.'))
    s.append(SP(4))
    s += steps([
        'Type the station\'s callsign in the <b>Callsign</b> field. The name fills '
        'automatically from the FCC database as you type.',
        'Enter their location or remarks if desired.',
        'Click <b>Check In</b> or press Enter. The entry appears in the log with a '
        'timestamp.',
        'To check a station out, click <b>Check Out</b> on their row. The checkout '
        'time and participation duration are recorded automatically.',
        'When a station passes traffic or sends a message, use the traffic entry at '
        'the bottom of the page to record it with precedence and addressee.',
    ])
    s.append(SP(6))

    s.append(P('Closing a Net and Exporting the Log', H2))
    s += steps([
        'Click <b>Close Net</b>. Any stations still checked in are automatically '
        'checked out with the net close time. Net duration appears in the header.',
        'Click <b>📋 Export ICS-309</b> to download the complete ICS-309 Communications '
        'Log as a formatted document ready for the incident action plan.',
        'The ICS-309 includes: net name, frequency, mode, net open/close times, '
        'total duration, and a full check-in table with individual participation '
        'durations rounded up to the nearest quarter-hour — the standard for '
        'reimbursement documentation.',
    ])
    s.append(SP(6))
    s.append(note(
        'The Dead Man\'s Switch (page: deadmans.html) monitors net activity and '
        'sounds an audible alert if no check-in is logged within a configurable '
        'time threshold. It is designed for safety monitoring during search and '
        'rescue and other field operations where radio silence can indicate an '
        'emergency. See Chapter 12 for Dead Man\'s Switch operation.', 'note'))
    s.append(PB())
    return s


def ch7():
    s = chapter(7, 'Public Safety Net Logger',
                'http://192.168.50.1/starcom.html')
    s.append(P(
        'The Public Safety Net Logger handles trunked radio, P25, and other public safety '
        'radio systems where check-in is by radio ID rather than amateur callsign. '
        'It is designed for interoperability exercises, served-agency support, and any '
        'net where participants may not hold amateur licenses.'))
    s.append(SP(6))

    s.append(P('Key Differences from the Amateur Logger', H2))
    s.append(tbl(['FEATURE', 'AMATEUR NET LOGGER', 'PUBLIC SAFETY NET LOGGER'], [
        ['Primary identifier',
         'FCC callsign — auto-filled from local database',
         'Radio ID (unit number or talk group ID)'],
        ['License check',
         'FCC ULS lookup — confirms active license',
         'None required — any radio user can check in'],
        ['Roster lookup',
         'By callsign → returns name and member ID',
         'By radio ID → returns name and member ID'],
        ['ICS-309 format',
         'Callsign in station column',
         'Radio ID in station column'],
        ['Typical use',
         'ARES/RACES/AUXCOMM amateur nets',
         'Public safety agency check-in, interop exercises, Starcom-type nets'],
    ], widths=[1.3*inch, CW*0.38, CW-1.3*inch-CW*0.38]))
    s.append(SP(6))

    s.append(P('Operating the Public Safety Net Logger', H2))
    s.append(P(
        'Operation follows the same workflow as the Amateur Net Logger. Open the net, '
        'enter radio IDs as stations check in, and export the ICS-309 at net close. '
        'The key operational note is that check-in by radio ID is the standard — '
        'operators do not need callsigns, and the FCC database lookup is not invoked. '
        'If a roster member has both a radio ID and a callsign, the system will '
        'display both on their check-in row for reference.'))
    s.append(SP(6))

    s.append(P('Observer Mode', H2))
    s.append(P(
        'Both net loggers support Observer Mode — a read-only, auto-refreshing view '
        'of the active net accessible from any device on EMCOMM-NET. The Observer '
        'link is generated by clicking <b>🔗 Observer Link</b> and can be sent by '
        'Winlink, JS8Call, or read over the air. Observers cannot modify the log — '
        'they see the live net status, check-in list, and traffic log, updating '
        'every 15 seconds automatically. No login is required.'))
    s.append(SP(6))

    s.append(note(
        'Participants in public safety nets who also hold amateur licenses should '
        'check into the public safety net by radio ID only — this maintains '
        'the integrity of the agency\'s radio log. If the same person needs to '
        'participate in an amateur net on the same incident, they check into the '
        'Amateur Net Logger separately by callsign.', 'note'))
    s.append(PB())
    return s
