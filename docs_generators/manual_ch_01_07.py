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
        ['FieldCommand IMS',   '✓ Fully offline',    '✓ Own network + server', '✓ Full EMCOMM suite',   'Free / open source'],
        ['WebEOC',             '✗ Cloud only',       '✗ Requires infrastructure','✗ None',              '$10,000–50,000/yr'],
        ['E-Team / Veoci',     '✗ Cloud only',       '✗ Requires infrastructure','✗ None',              'Subscription'],
        ['NIMSIAP',            '✗ Internet required','✗ Requires connectivity', '✗ None',               'Free'],
        ['E-iSuite',           '△ Limited',          '△ Laptop only, no network','✗ None',              'License fee'],
    ], widths=[1.4*inch, 0.85*inch, 1.25*inch, 1.1*inch, CW-4.6*inch]))
    s.append(SP(6))

    s.append(P('1.3  System Architecture', H2))
    s.append(tbl(['COMPONENT', 'FUNCTION', 'DEFAULT IP'], [
        ['FieldCommand Pi 5 16GB',
         'Primary server · all 48 web tools · 12+ background services · '
         'RAID-1 NVMe storage · EMCOMM-NET Wi-Fi AP',
         '192.168.50.1'],
        ['44Net Gateway Pi 5  (optional)',
         'AMPRNet WireGuard tunnel · callsign-authenticated access · '
         'Part 97 access log · isolated from primary server',
         '192.168.50.2'],
        ['Wi-Fi router  (primary)',
         'DHCP · AiMesh controller · dual Wide Area Network (WAN) management · '
         'EMCOMM-NET Service Set Identifier (SSID) broadcast. Recommended: ASUS RT-BE58 Go.',
         '192.168.50.254'],
        ['AiMesh nodes  (optional)',
         'EMCOMM-NET coverage extension · seamless roaming. '
         'Recommended: additional ASUS RT-BE58 Go units.',
         'DHCP assigned'],
        ['UniFi Switch Lite 16 Power over Ethernet (PoE)  (recommended)',
         'Wired backbone · powers PoE devices · connects all Pi units, '
         'router, cellular antenna, and workstations',
         'DHCP assigned'],
        ['Operator workstations',
         'Any device with a modern browser: smartphones, tablets, laptops, '
         'Raspberry Pi 500 desktops, Windows or macOS laptops',
         'DHCP assigned'],
    ], widths=[1.8*inch, CW-2.8*inch, 1.0*inch]))
    s.append(SP(4))
    s.append(note(
        'The default server address is 192.168.50.1. This is configurable during '
        'installation. All documentation uses this default — substitute your address '
        'wherever 192.168.50.1 appears if your deployment differs.', 'note'))
    s.append(SP(6))

    s.append(P('1.4  Capability Summary', H2))
    s.append(tbl(['CAPABILITY AREA', 'TOOLS PROVIDED'], [
        ['Incident Management',
         'Five-section ICS structure. Complete IAP form set: ICS-202 through ICS-221. '
         'Live T-card resource board. Pre-planned event templates for 6 incident types. '
         'Incident archive, restore, and scenario/exercise mode.'],
        ['ICS Forms & IAP',
         'Full ICS form set with digital signature capture on all prepared-by and '
         'approved-by fields. One-click IAP Portable Document Format (PDF) compilation with title page and '
         'section dividers. Print center for on-site IAP packages.'],
        ['Federal Emergency Management Agency (FEMA) Documentation',
         'FEMA Public Assistance (PA) cost tracking: Force Account Labor with fringe, Equipment with '
         '2025 FEMA rate schedule (44 built-in rates), Materials, and Contracts. '
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
         'Offline APRS tactical map. SARTopo GeoJSON import. HF propagation tool.'],
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
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(PB())
    return s


def ch2():
    s = chapter(2, 'Getting Started — Connecting to FieldCommand',
                'http://192.168.50.1')
    s.append(P(
        'Every tool in FieldCommand IMS is a web page served from the Pi. No app '
        'installation is required on any device. Any modern browser works — Chrome, '
        'Firefox, Safari, Edge, or the built-in browser on any smartphone or tablet.'))
    s.append(SP(6))

    s.append(P('2.1  First Connection', H2))
    s += steps([
        'Power on the FieldCommand Pi and wait approximately 45 seconds for all services '
        'to start. The system is ready when the EMCOMM-NET Wi-Fi network appears in the '
        'device scan list.',
        'On any smartphone, tablet, or laptop — open Wi-Fi settings and connect to '
        '<b>EMCOMM-NET</b>. The password is on the equipment case label and in the '
        'Installation Guide. No other credentials are required.',
        'Open a browser and navigate to <b>http://192.168.50.1</b>. '
        'The FieldCommand dashboard loads immediately.',
        'Bookmark the dashboard Uniform Resource Locator (URL). On a smartphone, tap <b>Share → Add to Home Screen</b> '
        'to create an icon — it opens like a native app.',
        'If the dashboard does not load, confirm you are connected to EMCOMM-NET and '
        'not to another Wi-Fi network. The Pi does not relay traffic to the internet — '
        'if your device switches to a different network automatically, disable auto-join '
        'on other networks during activations.',
    ])
    s.append(SP(6))

    s.append(P('2.2  Dashboard Modes', H2))
    s.append(P(
        'The dashboard has three selectable modes that filter the tool card grid. '
        'Switching modes does not affect any data — all tools remain accessible in every mode.'))
    s.append(SP(4))
    s.append(tbl(['MODE', 'TOOLS SHOWN PROMINENTLY', 'BEST FOR'], [
        ['All-Hazards Incident Command System (ICS)',
         'Full ICS platform, Incident Action Plan (IAP) forms, T-card resource board, personnel '
         'check-in, Federal Emergency Management Agency (FEMA) cost documentation, event templates, cost dashboard',
         'Any active incident requiring ICS structure'],
        ['Amateur Radio Emergency Communications (EMCOMM)',
         'Net control logger, Federal Communications Commission (FCC) callsign lookup, Automatic Packet Reporting System (APRS) map, Winlink, '
         'JS8Call, Amateur Packet Radio Network (AMPRNet) gateway, High Frequency (HF) propagation, National Traffic System (NTS) radiogram',
         'Amateur radio net operations, ARES/RACES activations'],
        ['Public Safety',
         'Starcom net logger, radio ID roster, resource map, Wide Area Network (WAN) status, '
         'weather radar, hospital directory, facilities',
         'Public safety radio nets, Starcom check-in operations'],
    ], widths=[1.3*inch, CW-2.7*inch, 1.4*inch]))
    s.append(SP(6))

    s.append(P('2.3  WAN Status Indicators', H2))
    s.append(P(
        'The top of the dashboard always shows a live WAN status bar. It polls every '
        '30 seconds and changes color automatically.'))
    s.append(SP(4))
    s.append(tbl(['INDICATOR', 'MEANING', 'CORE TOOLS AFFECTED?'], [
        ['🟢 Green — Cellular',  'Primary internet source active',                'None — fully operational'],
        ['🔵 Blue — Satellite',  'Satellite failover active',                     'None — fully operational'],
        ['🔴 Red — Offline',     'No internet — all core tools continue',         'None — fully operational'],
        ['🟢 AMPRNet UP',        '44Net WireGuard tunnel active',                 'N/A'],
        ['🔴 AMPRNet DOWN',      '44Net tunnel down or gateway Pi unreachable',   'N/A'],
    ], widths=[1.6*inch, CW-3.0*inch, 1.4*inch]))
    s.append(SP(4))
    s.append(note(
        'A red WAN indicator means internet-dependent features are paused — National Weather Service (NWS) radar, '
        'APRS-IS, HF propagation. It does NOT mean FieldCommand IMS is unavailable. '
        'All ICS tools, forms, net loggers, roster, and local maps run normally offline.', 'note'))
    s.append(PB())
    return s


def ch3():
    s = chapter(3, 'Organization Setup & Station Configuration',
                'http://192.168.50.1/setup.html')
    s.append(P(
        'Before using FieldCommand IMS for the first time, complete the Organization '
        'Setup to configure your station identity, Service Set Identifier (SSID), and default settings. '
        'These values appear in Incident Command System (ICS) form headers, net logs, and printed documents.'))
    s.append(SP(6))

    s.append(P('3.1  Setup Fields', H2))
    s.append(tbl(['FIELD', 'WHAT IT CONFIGURES'], [
        ['Organization name',
         'Full name of your agency or group — appears in ICS form headers and cover pages'],
        ['Short name / abbreviation',
         'Used in compact displays, footer lines, and net log headers'],
        ['Primary callsign',
         'Club or personal Federal Communications Commission (FCC) callsign — used for Amateur Packet Radio Network (AMPRNet) authentication and net logs'],
        ['Station grid square',
         'Maidenhead grid locator (4 or 6 character) — used for High Frequency (HF) propagation calculations '
         'and Automatic Packet Reporting System (APRS) position reports'],
        ['Default incident name',
         'Pre-fills the incident name field when creating new incidents'],
        ['Wi-Fi network name (SSID)',
         'Default is EMCOMM-NET — change if you operate multiple FieldCommand systems '
         'simultaneously and need to distinguish them'],
        ['Server address',
         'Default 192.168.50.1 — change only if this conflicts with your existing network'],
        ['Time zone',
         'Used for all timestamps in logs and forms — set to your deployment time zone'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('3.2  Offline vs. Online Feature Table', H2))
    s.append(tbl(['FEATURE', 'OFFLINE?', 'NOTES WHEN OFFLINE'], [
        ['ICS platform — all five sections',    '✓ Full',  'No change'],
        ['All ICS forms and Incident Action Plan (IAP)',               '✓ Full',  'No change'],
        ['T-card resource board',               '✓ Full',  'No change'],
        ['Federal Emergency Management Agency (FEMA) cost tracking',                  '✓ Full',  'No change'],
        ['Event templates',                     '✓ Full',  'No change'],
        ['IAP Portable Document Format (PDF) compilation',                 '✓ Full',  'No change'],
        ['Digital signatures on forms',         '✓ Full',  'No change'],
        ['Net control loggers (both)',           '✓ Full',  'No change'],
        ['FCC callsign lookup',                 '✓ Full',  'Uses local SQLite database — no internet needed'],
        ['Member roster and Quick Response (QR) code check-in',       '✓ Full',  'No change'],
        ['Global Positioning System (GPS) resource map',                    '✓ Full',  'No change'],
        ['Barcode / QR scan check-in',          '✓ Full',  'No change'],
        ['Offline tactical APRS map',           '✓ Full',  'Map tiles local — RF APRS still works'],
        ['Kiwix reference library',             '✓ Full',  'No change'],
        ['National Weather Service (NWS) weather alerts',                  '△ Wide Area Network (WAN)',   'Paused — last alert cached and displayed'],
        ['Next Generation Radar (NEXRAD) animated radar',               '△ WAN',   'Tiles unavailable — offline banner shown'],
        ['APRS-IS internet feed',               '△ WAN',   'RF APRS continues — internet feed pauses'],
        ['HF propagation data',                 '△ WAN',   'Last retrieved data shown until WAN returns'],
        ['AMPRNet / 44Net tunnel',              '△ WAN',   'Tunnel drops — local network unaffected'],
        ['Winlink Telnet sessions',             '△ WAN',   'RF Winlink (VARA/Pactor) continues'],
    ], widths=[2.2*inch, 0.7*inch, CW-2.9*inch]))
    s.append(PB())
    return s


def ch4():
    s = chapter(4, 'Member Roster & Quick Response (QR) code Check-In Codes',
                'http://192.168.50.1/roster.html')
    s.append(P(
        'The Member Roster is the central personnel database. It stores every member, '
        'mutual-aid visitor, and regular participant with their identifiers, certifications, '
        'equipment capabilities, and a unique barcode check-in code that enables rapid '
        'QR-scan check-in at any activation.'))
    s.append(SP(6))

    s.append(P('4.1  Roster Fields', H2))
    s.append(tbl(['FIELD', 'PURPOSE'], [
        ['Member ID',        'Your organization\'s internal identifier (e.g. ESV-042). Primary key.'],
        ['Barcode ID',       'QR/barcode check-in code — defaults to Member ID on first import. '
                             'Can be overridden with a facility badge number or any custom code.'],
        ['Callsign',         'Federal Communications Commission (FCC) amateur radio callsign. Leave blank for non-licensed members.'],
        ['Radio ID',         'Trunked/P25 radio unit number if applicable.'],
        ['Name',             'First and last name.'],
        ['Role',             'Primary function: Operator, Net Control, Logistics, Medical, etc.'],
        ['Member type',      'Member · Visitor · Mutual Aid — affects check-in form behavior.'],
        ['Certifications',   'ICS-100/200/300/400/700/800, EmComm I/II, CPR, First Aid, CERT.'],
        ['Equipment',        'High Frequency (HF), Very High Frequency (VHF), digital modes, Automatic Packet Reporting System (APRS), Winlink, go-box, generator, vehicle.'],
        ['License class',    'Technician, General, Amateur Extra — displayed on net log entries.'],
        ['Phone / Email',    'Contact information — stored locally, never transmitted externally.'],
        ['Grid square',      'Maidenhead grid locator for RF planning.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))

    s.append(P('4.2  Adding and Editing Members', H2))
    s += steps([
        'Click <b>+ Add Member</b> at the top of the roster page.',
        'Enter at minimum a Member ID and name. Add callsign, radio ID, or both if applicable.',
        'Check all applicable certifications and equipment capabilities.',
        'Click <b>Save</b>. The member appears immediately in the roster.',
        'To edit an existing member, click their card to open the detail view, '
        'make changes, and click <b>Save</b>.',
        'To delete a member, open their detail view and click <b>Delete</b>. '
        'This removes them from the roster but does not delete historical net log entries.',
    ])
    s.append(SP(6))

    s.append(P('4.3  Importing Members via CSV', H2))
    s.append(P(
        'Import your existing member list using <b>📥 Import CSV</b>. The CSV must '
        'have a <b>member_id</b> column. All other columns are optional. '
        'Existing member IDs are updated; new IDs are added. '
        'Existing members not in the import file are left unchanged.'))
    s.append(SP(4))
    s.append(P('Required: <b>member_id</b>', CS))
    s.append(P('Optional: <b>callsign · radio_id · first_name · last_name · '
               'role · phone · email · grid · license_class</b>', CS))
    s.append(SP(6))

    s.append(P('4.4  QR Check-In Codes', H2))
    s.append(P(
        'Every member has a personal QR code that enables instant check-in at any '
        'activation using the Scan Check-In page (see Chapter 10). The QR button on '
        'each roster card opens a modal with that member\'s personal code.'))
    s.append(SP(4))
    s += steps([
        'Click the <b>QR</b> button on any member card.',
        'The modal shows the QR code. When internet is available, a true scannable '
        'QR image is generated. When offline, the member ID is displayed in large '
        'text as a manual entry fallback.',
        'Click <b>🖨 Print</b> to open a clean print-ready page with the QR, '
        'the member\'s name, and the FieldCommand check-in Uniform Resource Locator (URL).',
        'Click <b>💾 Save PNG</b> to download the QR code image — members can '
        'save it to their phone\'s home screen or print it on their ID badge.',
    ])
    s.append(SP(4))
    s.append(note(
        'The barcode_id field defaults to the member_id on first import. '
        'If your organization uses physical facility badge scanners, set barcode_id '
        'to match the badge number — the scan check-in will then auto-fill from '
        'a badge swipe.', 'note'))
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
        '<b>Unified Command</b>, see Section 5.3 below.',
        'Click <b>Create Incident</b>. The incident opens immediately and becomes '
        'the active incident. The incident name appears in the dashboard header '
        'and in all form headers.',
    ])
    s.append(SP(6))

    s.append(P('5.2  Single Incident Commander vs. Unified Command', H2))
    s.append(P(
        'ICS supports two command structures, and FieldCommand IMS accommodates both '
        'without any configuration change. The difference is a workflow convention, '
        'not a software setting.'))
    s.append(SP(4))
    s.append(tbl(['STRUCTURE', 'WHEN USED', 'HOW TO CONFIGURE IN FIELDCOMMAND'], [
        ['Single Incident Commander (IC)',
         'One agency or jurisdiction has clear authority. '
         'Most activations involving a single responding organization.',
         'Enter the IC\'s name or callsign in the Incident Commander field '
         'when creating the incident. The ICS-203 org chart will show one IC '
         'at the top of the command structure.'],
        ['Unified Command (UC)',
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
    s.append(tbl(['TYPE', 'DESCRIPTION'], [
        ['All-Hazards',      'General ICS incident — suitable for any event not covered below'],
        ['Search and Rescue','SAR-specific resource typing and form defaults'],
        ['Severe Weather',   'Shelter operations, damage assessment, utility coordination'],
        ['Mass Gathering',   'Large planned event with medical and crowd management focus'],
        ['HazMat',           'Hazardous materials response with decon and zoning emphasis'],
        ['Exercise',         'Training scenario — marked with 🧪 badge; beta reset available'],
    ], widths=[1.4*inch, CW-1.4*inch]))
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
         '✓ Yes — restore any time'],
        ['Restore from USB',
         'Reads the JSON archive from the USB drive and re-inserts all data. '
         'Restores the incident to fully active status.',
         '✓ Yes'],
        ['Hard delete from Pi',
         'Permanently removes the incident and all associated data from the Pi SSD. '
         'Run only after confirming the archive is on USB.',
         '✗ Permanent'],
    ], widths=[1.3*inch, CW-2.3*inch, 1.0*inch]))
    s.append(SP(4))
    s.append(note(
        'The USB drive must be labelled FIELDCOMMAND (all caps). Any USB drive '
        'with this label is recognized automatically. A LaCie Rugged or similar '
        'ruggedized 1TB USB-C drive is recommended for field use.', 'note'))
    s.append(SP(6))

    s.append(P('5.6  Exercise / Scenario Mode', H2))
    s.append(P(
        'Exercises and training scenarios can be tagged as <b>🧪 Scenario</b> when '
        'the incident is created. Scenario incidents display a yellow badge throughout '
        'the interface so operators always know they are in training mode. '
        'A <b>Beta Reset</b> wipes all scenario data — incidents, forms, costs, '
        'check-ins, T-cards, and meetings — while preserving the roster, '
        'hospital directory, channel library, and repeater database. '
        'This returns the system to a clean state for the next exercise without '
        'losing any permanent configuration data.'))
    s.append(PB())
    return s


def ch6():
    s = chapter(6, 'Pre-Planned Event Templates',
                'http://192.168.50.1/event_templates.html')
    s.append(P(
        'Event Templates allow you to pre-configure a complete incident setup — '
        'including objectives, default resource types, communications channels, '
        'and Incident Command System (ICS) organization — and activate it in seconds at the start of an '
        'activation. Templates eliminate the repetitive setup work for recurring '
        'incident types and ensure consistency across activations.'))
    s.append(SP(6))

    s.append(P('6.1  Built-In Templates', H2))
    s.append(P(
        'FieldCommand IMS ships with six built-in templates covering the most common '
        'incident types. Each can be used as-is or edited to match your local protocols.'))
    s.append(SP(4))
    s.append(tbl(['TEMPLATE', 'PRE-CONFIGURED CONTENTS'], [
        ['Emergency Shelter Operations',
         'Shelter management objectives, cot and supply resource types, '
         'registration and medical channels, Red Cross coordination section'],
        ['Search and Rescue',
         'Search and Rescue (SAR) objectives, field team and K9 resource types, '
         'search sector channels, base camp and medical branches'],
        ['Severe Weather Response',
         'Damage assessment objectives, utility and debris resource types, '
         'shelter and Emergency Operations Center (EOC) coordination channels, public information branch'],
        ['Mass Gathering / Special Event',
         'Crowd management objectives, medical and security resource types, '
         'venue and dispatch channels, medical and operations branches'],
        ['HazMat Response',
         'Decon and zoning objectives, HazMat team resource types, '
         'hot/warm/cold zone channels, safety officer emphasis'],
        ['Exercise / Training Scenario',
         'Training objectives, evaluator and observer resource types, '
         'exercise control channel, scenario-tagged (🧪)'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('6.2  Activating a Template', H2))
    s += steps([
        'Navigate to <b>Event Templates</b> from the dashboard.',
        'Click the <b>Activate</b> tab. Browse the template gallery.',
        'Click the template you want. A configuration panel opens.',
        'Enter the incident name, date/time, and any other details you want '
        'to customize before activating.',
        'Click <b>Activate Template</b>. FieldCommand IMS creates a new incident '
        'pre-loaded with all objectives, resource types, channels, and ICS org '
        'structure from the template. You are taken directly to the new incident.',
    ])
    s.append(SP(6))

    s.append(P('6.3  Creating and Editing Templates', H2))
    s += steps([
        'Click the <b>Manage Templates</b> tab.',
        'To edit a template, click its card. The edit modal opens with four tabs: '
        '<b>Objectives</b>, <b>Resources</b>, <b>Channels</b>, and <b>Organization</b>.',
        'Edit any field live. Objectives and resource types are listed — click '
        '<b>+ Add</b> to add items, click the × to remove them.',
        'Click <b>Save Template</b> when finished.',
        'To export a template as a JSON file for sharing with other FieldCommand '
        'systems, click <b>Export JSON</b>. To import a JSON template, click '
        '<b>Import JSON</b> and select the file.',
        'Built-in templates can be edited but not deleted. Custom templates '
        'can be deleted with the <b>🗑 Delete</b> button.',
    ])
    s.append(PB())
    return s


def ch7():
    s = chapter(7, 'Amateur Radio Net Control Logger',
                'http://192.168.50.1/netcontrol.html')
    s.append(P(
        'The Amateur Net Control Logger provides complete net management for licensed '
        'amateur radio operations: ARES, RACES, AUXCOMM, and any other amateur net. '
        'It replaces paper net logs with a live digital record that feeds directly '
        'into the ICS-309 communications log.'))
    s.append(SP(6))

    s.append(P('7.1  Opening a Net', H2))
    s += steps([
        'Navigate to <b>Net Control Logger</b> from the dashboard.',
        'Enter the net name, frequency, and mode (SSB / FM / Digital / Other).',
        'Verify the date and time are correct — these become the net open timestamp.',
        'Click <b>Open Net</b>. The status banner turns green and the elapsed timer starts.',
        'Share the <b>🔗 Observer Link</b> with section chiefs or served agencies '
        'so they can monitor the net in read-only view on their own devices. '
        'The observer page auto-refreshes every 15 seconds.',
    ])
    s.append(SP(6))

    s.append(P('7.2  Logging Check-Ins', H2))
    s.append(P(
        'When a station checks in, type their callsign in the callsign field. '
        'FieldCommand IMS looks up the callsign instantly in the <b>offline Federal Communications Commission (FCC) database</b> '
        '— 800,000+ amateur licensees stored locally on the Pi — and fills the operator\'s '
        'name and license class automatically. If the station is on your roster, their '
        'member ID is filled as well. No internet required.'))
    s.append(SP(4))
    s += steps([
        'Type the station\'s callsign. Name fills automatically as you type.',
        'Enter location or remarks if desired.',
        'Click <b>Check In</b> or press Enter. The entry appears with a timestamp.',
        'To check a station out, click <b>Check Out</b> on their row. '
        'Checkout time and participation duration are recorded automatically, '
        'rounded up to the nearest quarter-hour for reimbursement documentation.',
        'For traffic, use the traffic entry at the bottom — enter precedence, '
        'addressee, and a brief description.',
    ])
    s.append(SP(6))

    s.append(P('7.3  Closing a Net and Exporting ICS-309', H2))
    s += steps([
        'Click <b>Close Net</b>. All remaining checked-in stations are '
        'automatically checked out with the net close timestamp.',
        'Net open time, close time, and total duration appear in the header.',
        'Click <b>📋 Export ICS-309</b> to download the complete ICS-309 '
        'Communications Log as a formatted document ready for the Incident Action Plan (IAP).',
        'The ICS-309 includes: net name, frequency, mode, open/close times, '
        'total duration, and a full check-in table with individual participation '
        'durations rounded up to the nearest quarter-hour.',
    ])
    s.append(SP(6))
    s.append(note(
        'The Dead Man\'s Switch (deadmans.html) monitors net activity and '
        'sounds an alert if no check-in is logged within a configurable time window. '
        'It is designed for safety monitoring during Search and Rescue (SAR) and field operations where '
        'radio silence may indicate an emergency. See Chapter 12.', 'note'))
    s.append(PB())
    return s
