#!/usr/bin/env python3
"""manual_ch_08_18.py — Chapters 8–18: Net Loggers through ICS Planning."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *
print("Chapters 8-18 module loaded OK")

def ch8():
    s = chapter(8, 'Public Safety Net Logger',
                'http://192.168.50.1/starcom.html')
    s.append(P(
        'The Public Safety Net Logger handles trunked radio, P25, and other public '
        'safety radio systems where check-in is by radio ID rather than callsign. '
        'It is designed for interoperability exercises, served-agency support, and '
        'any net where participants may not hold amateur licenses.'))
    s.append(SP(4))
    s.append(tbl(['FEATURE', 'AMATEUR NET LOGGER', 'PUBLIC SAFETY NET LOGGER'], [
        ['Primary ID',        'Federal Communications Commission (FCC) callsign — auto-filled from local database',
                              'Radio ID (unit number)'],
        ['License check',     'FCC ULS lookup confirms active license',
                              'None required'],
        ['Roster lookup',     'By callsign → name and member ID',
                              'By radio ID → name and member ID'],
        ['ICS-309 format',    'Callsign in station column',
                              'Radio ID in station column'],
        ['Typical use',       'ARES / RACES / AUXCOMM',
                              'Public safety agency nets, interop exercises'],
    ], widths=[1.3*inch, CW*0.40, CW-1.3*inch-CW*0.40]))
    s.append(SP(6))
    s.append(P('Operation follows the same workflow as the Amateur Net Logger — '
               'open the net, log check-ins by radio ID, and export ICS-309 at close. '
               'Observer Mode is also available: click <b>🔗 Observer Link</b> to share '
               'a read-only, auto-refreshing view of the active net with any device on '
               'EMCOMM-NET.'))
    s.append(SP(4))
    s.append(note(
        'Participants who hold both an amateur license and a public safety radio ID '
        'should check into the public safety net by radio ID only. If they need to '
        'participate in a concurrent amateur net on the same incident, they check into '
        'the Amateur Net Logger separately by callsign. This maintains the integrity '
        'of both logs.', 'note'))
    s.append(PB())
    return s


def ch9():
    s = chapter(9, 'Observer Mode — Read-Only Net View',
                'http://192.168.50.1/observer.html')
    s.append(P(
        'Observer Mode provides a read-only, auto-refreshing view of any active net. '
        'It is designed for section chiefs, served agency liaisons, Emergency Operations Center (EOC) duty officers, '
        'or anyone who needs to monitor net activity without access to the Net Control '
        'workstation.'))
    s.append(SP(6))
    s.append(P('9.1  Accessing Observer Mode', H2))
    s += steps([
        'The Net Control operator clicks <b>🔗 Observer Link</b> on the active net page.',
        'The Uniform Resource Locator (URL) is copied to the clipboard. Share it via Winlink, JS8Call, in person, '
        'or announce it over the net.',
        'Any device on EMCOMM-NET opens the link in a browser. No login required.',
        'The observer page shows: net name, frequency, mode, elapsed time, '
        'current check-in list with callsigns/names/times, and the traffic log. '
        'It refreshes automatically every 15 seconds.',
    ])
    s.append(SP(6))
    s.append(P('9.2  What Observers Can and Cannot Do', H2))
    s.append(tbl(['OBSERVERS CAN', 'OBSERVERS CANNOT'], [
        ['View all check-ins in real time',           'Add or remove check-ins'],
        ['View net open time and elapsed duration',   'Close the net'],
        ['View the traffic log',                      'Add traffic entries'],
        ['Refresh the page to get latest data',       'Change any net settings'],
        ['Bookmark the observer URL for re-use',      'Access the Net Control view'],
    ], widths=[CW/2, CW/2]))
    s.append(PB())
    return s


def ch10():
    s = chapter(10, 'Barcode & Quick Response (QR) code Scan Check-In',
                'http://192.168.50.1/scan_checkin.html')
    s.append(P(
        'The Scan Check-In page enables rapid personnel check-in at activations using '
        'a smartphone or tablet camera. It uses the browser\'s native BarcodeDetector API '
        '— no external library, no CDN dependency, works fully offline. '
        'It supports QR codes, Code 128, Code 39, EAN-13, Data Matrix, PDF417, '
        'and Aztec formats.'))
    s.append(SP(6))

    s.append(P('10.1  Two Check-In Methods', H2))
    s.append(tbl(['METHOD', 'HOW IT WORKS', 'BEST FOR'], [
        ['Camera scan',
         'Point the device camera at the member\'s QR code or barcode. '
         'Detection is automatic at 4 frames per second. '
         'The same code is debounced for 3 seconds to prevent duplicate submissions.',
         'High-throughput check-in stations; members with printed QR codes'],
        ['Manual ID entry',
         'Type a member ID, callsign, or radio ID in the manual entry field '
         'and press Enter or click Look Up. Same roster lookup as camera scan.',
         'When camera unavailable; walk-in personnel without a QR code'],
    ], widths=[1.3*inch, CW-3.1*inch, 1.8*inch]))
    s.append(SP(6))

    s.append(P('10.2  Check-In Workflow', H2))
    s += steps([
        'Navigate to <b>Scan Check-In</b> from the dashboard.',
        'Click <b>📷 Start Camera</b>. If multiple cameras are present (front/rear), '
        'select the rear-facing camera from the dropdown.',
        'Point the camera at the member\'s QR code. The system detects it automatically '
        'and looks up the member in the roster.',
        'If the member is found: their name, agency, and suggested Incident Command System (ICS) position '
        'auto-fill with green borders. Review the fields — edit if needed.',
        'If the member is not in the roster: a "not found" banner appears. '
        'Their scanned ID fills the ID field. Fill in name and agency manually.',
        'Click <b>✓ Check In</b>. A full-screen success confirmation appears '
        'with the member\'s name and check-in time. The device vibrates briefly '
        'on phones that support it.',
        'Click <b>Scan Next Person</b> to clear the form and check in the next member. '
        'The session history panel at the bottom shows the last 10 check-ins.',
    ])
    s.append(SP(6))

    s.append(P('10.3  Roster Lookup Order', H2))
    s.append(P(
        'When a code is scanned or a manual ID is entered, the system searches '
        'the roster in this order until a match is found:'))
    s.append(SP(2))
    s.append(tbl(['SEARCH ORDER', 'FIELD SEARCHED', 'EXAMPLE VALUE'], [
        ['1st', 'barcode_id',  'ESV-042  (or badge number if overridden)'],
        ['2nd', 'member_id',   'ESV-042'],
        ['3rd', 'callsign',    'KE4CON'],
        ['4th', 'radio_id',    '412'],
    ], widths=[0.9*inch, 1.3*inch, CW-2.2*inch]))
    s.append(SP(4))
    s.append(note(
        'BarcodeDetector is supported on Chrome (Android and desktop), Edge, '
        'and Samsung Internet. It is not supported on iOS Safari or Firefox. '
        'On unsupported browsers, the camera scan button is disabled and '
        'the manual entry fallback works normally.', 'note'))
    s.append(PB())
    return s


def ch11():
    s = chapter(11, 'Federal Communications Commission (FCC) Callsign Lookup',
                'http://192.168.50.1/callsign.html')
    s.append(P(
        'The FCC Callsign Lookup tool provides instant offline access to the full '
        'national FCC amateur radio licensee database — over 800,000 active licensees. '
        'The database is stored locally in SQLite on the Pi and is used automatically '
        'by the Net Control Logger, Scan Check-In, and Incident Action Plan (IAP) forms. '
        'No internet connection is required.'))
    s.append(SP(6))

    s.append(P('11.1  Manual Lookup', H2))
    s += steps([
        'Navigate to <b>Callsign Lookup</b> from the dashboard.',
        'Type any callsign in the search field. Results appear as you type.',
        'The result shows: callsign, name, license class, expiration date, '
        'grid square, and mailing address city/state.',
        'Click <b>Copy</b> to copy the callsign to the clipboard, or '
        '<b>Add to Roster</b> to create a roster entry from the FCC record.',
    ])
    s.append(SP(6))

    s.append(P('11.2  Automatic Lookup in Other Tools', H2))
    s.append(P(
        'The callsign database is queried automatically in three other places:'))
    s.append(SP(2))
    s.append(tbl(['WHERE', 'HOW IT WORKS'], [
        ['Net Control Logger',
         'As you type a callsign in the check-in field, the name and license '
         'class fill automatically. A red border appears if the callsign is not '
         'found or the license is expired.'],
        ['Scan Check-In',
         'After a Quick Response (QR) code scan or manual entry, if the code is a callsign, '
         'the FCC record is used to fill the name field.'],
        ['ICS-213 / ICS-214',
         'The "From" callsign field in the general message form validates '
         'against the FCC database and fills the operator name.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'The FCC database is updated quarterly. To update, download the FCC '
        'ULS database export from wireless.fcc.gov/uls and run the database '
        'import script as described in the Installation Guide.', 'note'))
    s.append(PB())
    return s


def ch12():
    s = chapter(12, 'Dead Man\'s Switch',
                'http://192.168.50.1/deadmans.html')
    s.append(P(
        'The Dead Man\'s Switch monitors net activity and triggers an audible alert '
        'if no check-in is logged within a configurable time window. It is designed '
        'for field operations — particularly search and rescue — where radio silence '
        'beyond a set interval may indicate a field team emergency.'))
    s.append(SP(6))
    s.append(P('12.1  Configuration', H2))
    s.append(tbl(['SETTING', 'DESCRIPTION'], [
        ['Check-in interval',
         'Maximum time allowed between net check-ins before the alert fires. '
         'Common values: 10, 15, 30 minutes. Configurable per operation.'],
        ['Alert type',
         'Audible tone through the browser (requires speaker). '
         'Visual flashing banner on the Dead Man\'s page.'],
        ['Reset',
         'Any new check-in in the Net Control Logger resets the timer automatically.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))
    s.append(P('12.2  Operating the Dead Man\'s Switch', H2))
    s += steps([
        'Open the Dead Man\'s Switch page on a dedicated monitor or tablet '
        'at the Net Control position or Emergency Operations Center (EOC) duty station.',
        'Select the active net from the dropdown.',
        'Set the check-in interval and click <b>Start Monitoring</b>.',
        'The countdown timer displays time remaining until alert.',
        'If the timer reaches zero, the audible alert fires and the page '
        'flashes red. Acknowledge with <b>Acknowledge</b> and investigate.',
        'Any check-in logged in the Net Control Logger resets the timer automatically.',
        'Click <b>Stop Monitoring</b> when the net closes.',
    ])
    s.append(PB())
    return s


def ch13():
    s = chapter(13, 'Tactical Automatic Packet Reporting System (APRS) Map',
                'http://192.168.50.1/tactical.html')
    s.append(P(
        'The Tactical Map provides an offline-capable, Leaflet-based map showing APRS '
        'station positions from both RF APRS (always available) and APRS-IS internet '
        'feed (when Wide Area Network (WAN) is up). It is the primary situational awareness tool for '
        'tracking field teams, vehicles, and mobile resources.'))
    s.append(SP(6))

    s.append(P('13.1  Map Layers', H2))
    s.append(tbl(['LAYER', 'SOURCE', 'REQUIRES WAN?'], [
        ['Map tiles',              'OpenStreetMap / CartoDB Dark',              'Cached locally for offline use'],
        ['APRS-IS stations',       'Internet APRS-IS feed',                     '✓ WAN required'],
        ['RF APRS stations',       'Local Terminal Node Controller (TNC) or direwolf connected to Pi',     '✗ Offline — always available'],
        ['SARTopo overlays',       'GeoJSON import from sartopo_import.html',   '✗ Offline once imported'],
        ['Weather alert polygons', 'National Weather Service (NWS) API',                                   '✓ WAN required'],
    ], widths=[1.5*inch, CW-3.1*inch, 1.6*inch]))
    s.append(SP(6))

    s.append(P('13.2  Station Markers', H2))
    s.append(P(
        'Each APRS station is displayed with its standard APRS symbol. Clicking '
        'a marker opens a popup showing: callsign, timestamp of last beacon, '
        'speed and course (if moving), altitude, and the raw APRS comment field. '
        'Stations are color-coded by age — bright for recent beacons, faded for '
        'stations not heard in more than 30 minutes.'))
    s.append(SP(6))

    s.append(P('13.3  SARTopo GeoJSON Import', H2))
    s.append(P(
        'Planning data from SARTopo (search sectors, assignments, exclusion zones) '
        'can be exported as GeoJSON and imported into the tactical map using the '
        'SARTopo Import page (sartopo_import.html). Once imported, the overlay '
        'persists on the map through browser refreshes.'))
    s += steps([
        'In SARTopo, export your map or layer as GeoJSON.',
        'Navigate to <b>SARTopo Import</b> from the reference section of the dashboard.',
        'Click <b>Choose File</b> and select the GeoJSON file.',
        'Click <b>Import</b>. The overlay appears on the tactical map immediately.',
        'To remove the overlay, return to SARTopo Import and click <b>Clear Overlay</b>.',
    ])
    s.append(PB())
    return s


def ch14():
    s = chapter(14, 'GPS-Tracked Resource Map',
                'http://192.168.50.1/resource_map.html')
    s.append(P(
        'The Resource Map displays the current Global Positioning System (GPS) positions of all Incident Command System (ICS) resources '
        'for the active incident. Each resource is drawn as a color-coded SVG pin '
        'whose color reflects its current status. Resources without a GPS position '
        'appear as dashed circles in the sidebar so the Operations Section can see '
        'what still needs to be positioned.'))
    s.append(SP(6))

    s.append(P('14.1  Map Controls', H2))
    s.append(tbl(['CONTROL', 'FUNCTION'], [
        ['Incident selector',
         'Choose which incident\'s resources to display. '
         'The last selected incident is remembered between sessions.'],
        ['↺ Refresh',
         'Reload all resource positions from the server.'],
        ['📍 My Location',
         'Place a marker at your current device GPS position and zoom to it. '
         'Useful for confirming map accuracy against your known position.'],
        ['Auto-refresh 30s',
         'Enable automatic position refresh every 30 seconds. '
         'Use when resources are actively moving and updating their positions.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('14.2  Marker Colors by Status', H2))
    s.append(tbl(['COLOR', 'STATUS'], [
        ['🟢 Green',    'Available'],
        ['🔵 Blue',     'Assigned'],
        ['🔵 Light blue', 'Staging'],
        ['🔴 Red',      'Out of Service or En Route'],
        ['Dashed circle', 'No GPS position set yet'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(6))

    s.append(P('14.3  Setting a Resource Position', H2))
    s.append(P(
        'Click any resource in the sidebar — or click an existing pin on the map — '
        'to open the Set Position modal. Three methods are available:'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'HOW TO USE', 'BEST FOR'], [
        ['Device GPS',
         'Click <b>📍 Use Device GPS</b>. The browser requests your device\'s '
         'GPS position. Accuracy (±meters) is shown.',
         'Field operator at the resource\'s location using a phone'],
        ['Click map to place',
         'Click <b>🗺 Click Map to Place</b>. The modal closes and the cursor '
         'changes to a crosshair. Click anywhere on the map to set the position.',
         'Incident Commander (IC) or Planning placing resources on a map by known location'],
        ['Manual coordinates',
         'Type decimal latitude and longitude directly into the fields.',
         'Position known from a paper map, GPS receiver, or radio report'],
    ], widths=[1.4*inch, CW-3.2*inch, 1.8*inch]))
    s.append(SP(4))
    s.append(P(
        'Optionally enter a <b>Location Label</b> (e.g. "Division Alpha staging area") '
        'to display a human-readable description below the coordinates. '
        'Click <b>Save Position</b>. The pin appears on the map immediately. '
        'Click <b>Clear GPS</b> to remove the position.'))
    s.append(PB())
    return s


def ch15():
    s = chapter(15, 'Incident Command System (ICS) Platform Overview — Five-Section Structure',
                'http://192.168.50.1/incident.html')
    s.append(P(
        'FieldCommand IMS implements the full five-section ICS structure defined by '
        'National Incident Management System (NIMS). Each section has its own page with the forms, tools, and resource '
        'displays appropriate to that function. All sections work from the same '
        'underlying incident database — a resource added in Operations appears '
        'immediately in Logistics and Finance.'))
    s.append(SP(6))

    s.append(tbl(['ICS SECTION', 'PAGE', 'KEY TOOLS'], [
        ['Command',
         'incident.html',
         'Incident overview, general info, ICS-201 initial briefing, '
         'ICS-202 objectives, ICS-207 org chart, ICS-208 safety message, '
         'position checklists, meeting scheduler. '
         'Note: the Safety Officer (SOFR) and Public Information Officer (PIO) '
         'are Command Staff — they report directly to the Incident Commander (IC), not to a section.'],
        ['Operations',
         'resources.html',
         'T-card resource board by type and status, assignment tracking, '
         'Global Positioning System (GPS) resource map, ICS-204 assignment lists. '
         'Note: ICS-204 is developed by the Resources Unit (Planning) '
         'but distributed to and used by Operations supervisors.'],
        ['Planning',
         'iap.html',
         'Incident Action Plan (IAP) assembly, ICS-202 objectives, ICS-203 org assignment list, '
         'ICS-209 status summary, ICS-211 check-in list, ICS-221 demobilization, '
         'Planning P cycle. '
         'Note: Planning assembles and distributes the IAP but does not develop '
         'all forms in it — see the form table in Chapter 17 for development responsibility.'],
        ['Logistics',
         'ics-form.html',
         'ICS-205 radio comms plan (Communications Unit Leader (COML)), ICS-205A comms list (COML), '
         'ICS-206 medical plan (Medical Unit Leader (MEDL)), ICS-218 support vehicle inventory (GSUL), '
         'ICS-309 communications log (COML), facilities directory, channel library. '
         'Note: the Communications Unit and Medical Unit are in the '
         'Logistics Service Branch. They develop ICS-205, 205A, 206, and 309 — '
         'these forms are then included in the IAP by the Planning Section.'],
        ['Finance / Admin',
         'fema_costs.html',
         'Federal Emergency Management Agency (FEMA) Public Assistance (PA) cost tracking, Force Account Labor with fringe, Equipment '
         'with FEMA rate schedule, Materials, Contracts, cost dashboard, '
         'ICS-214 activity log import. '
         'Note: ICS-214 is completed by all supervisors in every section — '
         'Finance/Admin collects them for cost documentation and records.'],
    ], widths=[1.2*inch, 1.5*inch, CW-2.7*inch]))
    s.append(SP(6))

    s.append(P('15.1  Command Structure — Single IC or Unified Command', H2))
    s.append(P(
        'The ICS-203 Organization Assignment List is where the command structure is '
        'formally documented. For a Single IC incident, the IC\'s name appears at the '
        'top of the org chart. For a Unified Command incident, the Unified Command (UC) member agencies '
        'are listed collectively at the Command level. FieldCommand IMS handles both '
        'structures identically — the ICS-203, ICS-202, and all downstream forms '
        'work the same way regardless of command structure. '
        'See Chapter 5.2 for guidance on configuring each structure.'))
    s.append(SP(6))

    s.append(P('15.2  General Info — ICS-201 Initial Briefing', H2))
    s.append(P(
        'The General Info page (general_info.html) holds the ICS-201 Initial Incident '
        'Briefing data: situation summary, initial response actions, current organization, '
        'and resource summary. It is typically completed by the first-arriving IC and '
        'updated through the first operational period.'))
    s.append(SP(6))

    s.append(P('15.3  Preflight Deployment Checklist', H2))
    s.append(P(
        'The Preflight page (preflight.html) provides a comprehensive GO/CAUTION/NO-GO '
        'checklist for verifying system and data readiness before every activation. '
        'It combines automated server checks that run without any operator input '
        'with a manual section-by-section checklist covering hardware, power, '
        'communications, personnel, logistics, safety, and agency coordination. '
        'A rolling verdict at the top of the page updates in real time as items are checked.'))
    s.append(SP(6))

    s.append(P('Data Readiness — Automated Checks', H3))
    s.append(P(
        'The first section of the preflight checklist — Data Readiness — runs automatically '
        'when the page loads and whenever the operator clicks Re-Check. '
        'It queries the FieldCommand server and verifies six critical data items:'))
    s.append(SP(4))
    s.append(tbl(['CHECK ITEM', 'WHAT IS VERIFIED', 'REQUIRED FOR GO?'], [
        ['Organization Setup',
         'Org name and callsign have been entered in the setup page.',
         'Yes — required'],
        ['FCC Callsign Database',
         'FCC amateur license database is present and less than 14 days old. '
         'Shows record count and age in days.',
         'Yes — required'],
        ['Member Roster',
         'At least one member has been imported or entered in the roster.',
         'Recommended'],
        ['Repeater Database',
         'Repeater data has been loaded from a RepeaterBook CSV or manual entry. '
         'Shows total count and how many have map coordinates.',
         'Recommended'],
        ['Channel Library',
         'At least one channel has been added to the channel library.',
         'Recommended'],
        ['Active Incident',
         'An incident has been created and set to active status.',
         'Recommended'],
    ], widths=[1.4*inch, 3.0*inch, CW-4.4*inch]))
    s.append(SP(4))
    s.append(note(
        'Each auto-check item shows live server detail inline — for example '
        '"✓ 847,223 records, 3.2 days old" or "✗ 0 repeaters loaded." '
        'Items that fail auto-check are automatically set to NO-GO. '
        'Operators can override any item manually if circumstances warrant. '
        'Each NO-GO item description includes the page URL to navigate to and fix it.',
        'note'))
    s.append(SP(6))

    s.append(P('Manual Checklist Sections', H3))
    s.append(tbl(['SECTION', 'COVERS'], [
        ['⚡ Power Systems',
         'Shore/generator power, battery backup/UPS, solar, fuel, power distribution'],
        ['📻 Communications Equipment',
         'HF radio, VHF/UHF radio, go-kit radios, antennas, repeater access, '
         'Winlink, JS8Call'],
        ['💻 Computing & Software',
         'Server boot, FCC database, nginx, API server, health monitor, '
         'Graywolf APRS, Kiwix, Wi-Fi AP'],
        ['👤 Personnel & Staffing',
         'Net Control operator, alternate NCS, agency liaison, operator briefing, '
         'roster check-in'],
        ['📦 Logistics & Supplies',
         'Food and water, first aid, weather protection, spare parts, '
         'lighting, paper backup forms'],
        ['🛡 Safety & Security',
         'Lightning protection, RF exposure, CO detector, emergency comms plan, '
         'contact list'],
        ['🤝 Agency Coordination',
         'EOC check-in, frequencies confirmed, ICP location, resource request '
         'process, demobilization plan'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(6))
    s.append(P('How to Use the Preflight Checklist', H3))
    s += steps([
        'Open <b>http://192.168.50.1/preflight.html</b> on any EMCOMM-NET device. '
        'The Data Readiness section runs automatically — review any NO-GO items first.',
        'For each NO-GO data item, click the link in the item description to navigate '
        'to the fix page (roster.html, repeaters.html, channel_library.html, or incident.html). '
        'Return to preflight and click <b>↺ Auto-Check</b> to re-verify.',
        'Work through each manual section. For each item, click '
        '<b>✓ GO</b>, <b>⚠ CAUTION</b>, or <b>✕ NO-GO</b>. '
        'Add a note in the text field if needed.',
        'The verdict banner updates in real time. '
        '<b>GO</b> (green) means all required items are confirmed. '
        '<b>CAUTION</b> (amber) means optional items need attention. '
        '<b>NO-GO</b> (red) means a required item has failed — do not activate.',
        'Click <b>Save State</b> to store the current checklist to browser storage '
        'for the shift record. Click <b>Export Report</b> to download a JSON summary '
        'for documentation.',
    ])
    s.append(PB())
    return s


def ch16():
    s = chapter(16, 'Incident Command System (ICS) Operations Section — T-Card Resource Board',
                'http://192.168.50.1/resources.html')
    s.append(P(
        'The T-Card Resource Board is the Operations Section\'s primary resource '
        'tracking tool. It mirrors the physical ICS T-card system used in traditional '
        'incident management but adds live status, assignment tracking, Global Positioning System (GPS) integration, '
        'and direct export to ICS-204 assignment lists.'))
    s.append(SP(6))

    s.append(P('16.1  Resource Types', H2))
    s.append(P(
        'Resources are organized by National Incident Management System (NIMS) type. The Resource Types library '
        '(resource_types.html) defines the types available in your system. '
        'FieldCommand ships with standard NIMS types pre-loaded: '
        'Crew, Engine, Helicopter, Dozer, Water Tender, Medical Unit, '
        'Strike Team, Task Force, and Single Resource. '
        'Custom types can be added for your specific operations.'))
    s.append(SP(6))

    s.append(P('16.2  T-Card Fields', H2))
    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Resource name',       'Unit designation (Engine 12, Team Alpha, Unit 412)'],
        ['Resource type',       'NIMS type from the resource types library'],
        ['Status',              'Available · Assigned · Staging · Out of Service · En Route'],
        ['Assignment',          'Current task or division/group assignment'],
        ['Leader',              'Supervisor name or callsign'],
        ['Personnel count',     'Number of personnel on this resource'],
        ['Category',            'Agency, mutual aid source, or contractor'],
        ['Daily cost / Rate',   'Used by Federal Emergency Management Agency (FEMA) cost tracking and cost dashboard'],
        ['GPS position',        'Latitude, longitude, location label — set from Resource Map'],
        ['Operational period',  'Which OP period this T-card was created for'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('16.3  Personnel Assigned to a Resource', H2))
    s.append(P(
        'On a physical ICS T-card, the back of the card lists the individual personnel '
        'assigned to that resource — not just the count, but the names, ICS positions, '
        'and contact information for each person on the crew, unit, or team. '
        'FieldCommand IMS replicates this with a dedicated Personnel tab on every T-card '
        'detail panel. This roster is linked to the master Member Roster so that '
        'names auto-fill from existing records.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Name',               'Full name of the assigned person. '
                               'Begin typing to see roster autocomplete suggestions — '
                               'selecting a suggestion fills name, callsign, and agency automatically.'],
        ['ICS Position on Resource',
                               'The specific role this person fills on this resource. '
                               'Examples: Crew Boss, Paramedic/EMT, Emergency Radio Operator, '
                               'Driver/Operator, Equipment Operator. Different from their '
                               'overall ICS position on the org chart.'],
        ['Agency',             'Home agency or mutual aid source. '
                               'Auto-filled from roster when name is matched.'],
        ['Contact / Callsign', 'Radio callsign, channel, or phone number for this person. '
                               'Auto-filled from roster when a licensed amateur is matched.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('16.4  Using the Personnel Tab', H2))
    s += steps([
        'Click any T-card on the resource board to open the detail panel.',
        'Click the <b>👤 PERSONNEL</b> tab at the top of the panel. '
        'The count in parentheses shows how many personnel are currently listed.',
        'Begin typing a name in the Name field. If the person is in the roster, '
        'their name appears as a blue suggestion chip below the field. '
        'Click the chip to auto-fill name, callsign, and agency.',
        'Select the person\'s ICS position on this specific resource from the dropdown. '
        'This is their functional role on the resource — Crew Boss, EMT, Operator, etc.',
        'Fill in agency and contact if not auto-filled from the roster.',
        'Click <b>✓ Add to Resource</b>. The person appears in the personnel list '
        'and the personnel count on the T-card board updates automatically.',
        'To remove a person, click the <b>✕</b> button on their row. '
        'The count updates automatically.',
    ])
    s.append(SP(4))
    s.append(note(
        'The Personnel tab roster is separate from the check-in list (ICS-211). '
        'The personnel list answers "who is on this resource?" — '
        'the check-in list answers "who has checked into this incident?" '
        'A person can be in both, or either. For example, a mutual-aid crew '
        'might all be listed on their engine\'s T-card personnel tab '
        'but only the crew boss may check into the ICS-211 on behalf of the crew.', 'note'))
    s.append(SP(6))

    s.append(P('16.5  Adding and Managing Resources', H2))
    s += steps([
        'On the T-Card board, click <b>+ Add Resource</b>.',
        'Fill in the resource name, type, status, and assignment.',
        'Click <b>Save</b>. The T-card appears on the board.',
        'To change status, click the status badge on the T-card and select the new status.',
        'To reassign, click the assignment field and type the new assignment.',
        'To set or update GPS position, click <b>📍 Set Position</b> or go to '
        'the Resource Map (Chapter 14).',
        'To close out a resource, set status to <b>Out of Service</b> and '
        'fill in the demobilization notes.',
    ])
    s.append(PB())
    return s


def ch17():
    s = chapter(17, 'Incident Command System (ICS) Planning Section & Incident Action Plan (IAP) Assembly',
                'http://192.168.50.1/iap.html')
    s.append(P(
        'The Planning Section manages the Incident Action Plan — the written work plan '
        'for each operational period. FieldCommand IMS covers the full ICS form set '
        'needed to build a complete IAP, with digital signature capture and one-click '
        'Portable Document Format (PDF) compilation.'))
    s.append(SP(6))

    s.append(P('17.1  IAP Form Set', H2))
    s.append(P(
        'The table below shows every ICS form in FieldCommand IMS with two key '
        'attributes: who is responsible for <b>developing</b> it, and which section '
        'it is <b>distributed through</b>. These are not always the same. '
        'Several forms are developed by Logistics unit leaders but assembled into '
        'the IAP and distributed by the Planning Section — a distinction that '
        'confuses many operators and is explained in the notes below the table.'))
    s.append(SP(4))
    s.append(tbl(['FORM', 'TITLE', 'DEVELOPED BY', 'DISTRIBUTED THROUGH / IN IAP?'], [
        ['ICS-202',  'Incident Objectives',
         'Planning Section Chief / IC',
         'Planning · ✓ IAP'],
        ['ICS-203',  'Organization Assignment List',
         'Resources Unit Leader (RESL) — Planning',
         'Planning · ✓ IAP'],
        ['ICS-204',  'Assignment List',
         'Resources Unit Leader (RESL) — Planning',
         'Operations (from Planning) · ✓ IAP'],
        ['ICS-205',  'Radio Communications Plan',
         'Comms Unit Leader (Communications Unit Leader (COML)) — <b>Logistics</b>/Service Branch',
         'Via Planning into IAP · ✓ IAP'],
        ['ICS-205A', 'Communications List',
         'Comms Unit Leader (COML) — <b>Logistics</b>/Service Branch',
         'Supplemental — often in IAP'],
        ['ICS-206',  'Medical Plan',
         'Medical Unit Leader (MEDL) — <b>Logistics</b>/Service Branch',
         'Via Planning into IAP · ✓ IAP'],
        ['ICS-207',  'Incident Organization Chart',
         'Resources Unit Leader (RESL) — Planning',
         'Command display · ✓ IAP'],
        ['ICS-208',  'Safety Message / Plan',
         'Safety Officer (SOFR) — Command Staff',
         'Via Planning into IAP · ✓ IAP'],
        ['ICS-209',  'Incident Status Summary',
         'Situation Unit Leader (SITL) — Planning',
         'Sent to MAC/EOC — not in IAP'],
        ['ICS-211',  'Incident Check-In List',
         'Resources Unit Leader (RESL) — Planning',
         'Entry point recorders — not in IAP'],
        ['ICS-213',  'General Message',
         'Any ICS position',
         'Any section — not in IAP'],
        ['ICS-214',  'Activity Log',
         'All supervisors — every section',
         'Documentation only — not in IAP'],
        ['ICS-215A', 'IAP Safety Analysis',
         'Safety Officer (SOFR) — Command Staff, with Ops input',
         'Via Planning into IAP · ✓ IAP'],
        ['ICS-218',  'Support Vehicle/Equipment Inventory',
         'Ground Support Unit Leader (GSUL) — Logistics/Support Branch',
         'Logistics internal — not in IAP'],
        ['ICS-221',  'Demobilization Check-Out',
         'Demob Unit Leader (DMOB) — Planning',
         'Signed by demob resources — not in IAP'],
        ['ICS-309',  'Communications Log',
         'Comms Unit Leader (COML) / any operator — <b>Logistics</b>',
         'Comms unit records — not in IAP'],
    ], widths=[0.78*inch, 2.15*inch, 2.55*inch, CW-5.48*inch]))
    s.append(SP(6))
    s.append(P('17.1a  ICS Doctrine Notes — Forms That Cross Section Lines', H2))
    s.append(P(
        'Three forms are commonly misattributed in the field because they appear '
        'in the IAP (which Planning assembles) but are developed by Logistics unit '
        'leaders. Understanding the distinction matters for knowing who to ask '
        'when a form needs to be corrected or updated.'))
    s.append(SP(4))
    s.append(tbl(['FORM', 'THE DOCTRINE DISTINCTION'], [
        ['ICS-205\nRadio Comms Plan',
         'The <b>Communications Unit Leader (COML)</b> develops the ICS-205. '
         'The COML reports to the Service Branch Director under the Logistics Section. '
         'The completed ICS-205 is handed to the Planning Section, which includes '
         'it in the IAP and distributes it at the operational period briefing. '
         'If the ICS-205 needs to be corrected, go to the COML — not the Planning Section Chief.'],
        ['ICS-205A\nComms List',
         'Also developed by the <b>COML</b> under Logistics. The 205A is a '
         'supplemental contact directory — not always formally in the IAP but '
         'typically attached. Same attribution rule: developed in Logistics, '
         'Via Planning.'],
        ['ICS-206\nMedical Plan',
         'The <b>Medical Unit Leader (MEDL)</b> develops the ICS-206. '
         'The MEDL also reports to the Service Branch Director under Logistics. '
         'The completed ICS-206 goes to Planning for IAP inclusion. '
         'The Safety Officer (SOFR) must review and concur with the ICS-206 '
         'before it is finalized — their signature appears on the form.'],
    ], widths=[1.0*inch, CW-1.0*inch]))
    s.append(SP(6))

    s.append(P('17.2  Digital Signature Capture', H2))
    s.append(P(
        'All 16 Prepared By and Approved By fields across the ICS form set support '
        'digital signature capture. A signature pad appears below each signature field '
        'on every form. Signatures are stored as white-background PNG images and '
        'are embedded in the printed form and the IAP PDF.'))
    s.append(SP(4))
    s += steps([
        'Click on any <b>Prepared By</b> or <b>Approved By</b> signature field.',
        'A signature pad opens below the field.',
        'Sign using mouse, touchscreen, or stylus. '
        'The signature supports pressure sensitivity on compatible styluses.',
        'Click <b>Accept</b>. A preview of the signature appears below the field.',
        'The signature is saved automatically and restored if the page is reloaded.',
        'To clear a signature, click <b>Clear</b> on the signature pad.',
    ])
    s.append(SP(6))

    s.append(P('17.3  IAP Assembly Page — Print and Save', H2))
    s.append(P(
        'The IAP Assembly page (iap.html) lets the Planning Section select which '
        'ICS forms to include in the operational period package, then either print '
        'the IAP immediately or save it as a portable file for off-site printing. '
        'Two export options are available:'))
    s.append(SP(4))
    s.append(tbl(['OPTION', 'WHEN TO USE', 'HOW IT WORKS'], [
        ['🖨 Print IAP',
         'A printer is available on EMCOMM-NET or attached to the operator device.',
         'Opens a formatted print window in a new browser tab with a cover page, '
         'table of contents, and links to each selected ICS form. '
         'The browser print dialog opens automatically.'],
        ['📄 Save as PDF  (recommended)',
         'No printer on site, or the IAP needs to be taken off-site, '
         'emailed to the EOC, or archived. '
         'Use this as the primary save option.',
         'Posts the selected form list to the FieldCommand server, which generates '
         'a proper 8.5" × 11" PDF using ReportLab — the same engine used for all '
         'FieldCommand documents. Downloads as IAP_[Incident]_Period[N]_[Date].pdf. '
         'Opens in any PDF viewer on any device. Guaranteed correct page layout, '
         'margins, and pagination. Requires the FieldCommand Pi to be running '
         '(always true on EMCOMM-NET).'],
        ['💾 Save as HTML  (fallback)',
         'Server is unreachable, or the operator prefers a lightweight portable file.',
         'Downloads a self-contained HTML file with the IAP cover page and form index '
         'directly from the browser — no server call required. '
         'Open in any browser and use File → Print (Ctrl+P / Cmd+P) to print. '
         'Note: HTML printing can produce inconsistent page layout depending on the '
         'browser and its print settings. Use PDF when layout matters.'],
    ], widths=[1.2*inch, 2.0*inch, CW-3.2*inch]))
    s.append(SP(4))
    s += steps([
        'Navigate to <b>http://192.168.50.1/iap.html</b> or click IAP in the Planning section.',
        'Select the operational period and variant (full/command/logistics).',
        'Check the forms to include. Required forms are pre-checked. '
        'Typically include ICS-202, 203, 204, 205, 205A, 206, 207, and 208.',
        '<b>To print on-site:</b> click <b>🖨 Print IAP</b>. '
        'A formatted print window opens in a new tab. Select the site printer.',
        '<b>To save off-site (PDF — recommended):</b> click <b>📄 Save as PDF</b>. '
        'The Pi generates a proper PDF and it downloads automatically as '
        '<font face="Courier">IAP_[Incident]_Period[N]_[Date].pdf</font>. '
        'Copy to USB or email — opens in any PDF viewer anywhere.',
        '<b>To save off-site (HTML — fallback):</b> click <b>💾 Save as HTML</b>. '
        'Downloads immediately without a server call. '
        'Open in any browser and use File → Print. '
        'Use this only if the PDF button fails.',
    ])
    s.append(SP(6))

    s.append(P('17.4  IAP PDF Compilation', H2))
    s.append(P(
        'The IAP Compile page (iap_compile.html) assembles all completed ICS forms '
        'into a single server-generated PDF with embedded signatures, a cover page, '
        'and section dividers. This is the full distributable IAP package.'))
    s.append(SP(4))
    s += steps([
        'Navigate to <b>IAP Compile</b> from the dashboard or the Planning section.',
        'The page shows a checklist of all ICS forms for the active incident. '
        'Completed forms show a checkmark. Incomplete or missing forms are flagged.',
        'Select which forms to include. '
        'Required forms for a standard IAP: ICS-202, 203, 204, 205, 206, 207, 208.',
        'Click <b>Download IAP PDF</b>. The Pi server generates the PDF — '
        'this takes 5 to 15 seconds depending on how many forms are included.',
        'The PDF downloads automatically. It can be printed from any device on '
        'EMCOMM-NET or saved to USB for off-site printing.',
    ])
    s.append(SP(4))
    s.append(note(
        'The IAP PDF is generated on the Pi server and can be downloaded from any device '
        'on EMCOMM-NET — no printer needs to be connected to the device that generates it. '
        'The downloaded PDF is fully self-contained and can be printed at any location.',
        'note'))
    s.append(PB())
    return s


def ch18():
    s = chapter(18, 'Federal Emergency Management Agency (FEMA) Public Assistance (PA) Cost Documentation',
                'http://192.168.50.1/fema_costs.html')
    s.append(P(
        'The FEMA PA Cost Documentation module tracks all reimbursable costs for '
        'FEMA Public Assistance (PA) grant documentation. It covers the four FEMA '
        'cost categories: Force Account Labor, Equipment, Materials, and Contracts. '
        'All entries are tied to the active incident and operational period.'))
    s.append(SP(6))

    s.append(P('18.1  Force Account Labor', H2))
    s.append(P(
        'Force Account Labor tracks regular-time and overtime hours for your '
        'organization\'s employees and volunteers. For FEMA PA purposes, only overtime '
        'hours are reimbursable for regular employees; all hours may be reimbursable '
        'for volunteers depending on your state\'s policies.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'FEMA REQUIREMENT'], [
        ['Employee name',        'Full name as on payroll records'],
        ['Job title / class',    'Official job classification'],
        ['Regular hours',        'Regular-time hours worked on incident'],
        ['Overtime hours',       'Overtime hours — primary FEMA reimbursable category'],
        ['Hourly rate',          'Regular hourly rate from payroll'],
        ['Fringe benefit rate',  'Fringe as percentage of wages (FEMA requires fringe documentation)'],
        ['Total with fringe',    'Calculated automatically: (hours × rate) × (1 + fringe%)'],
        ['ICS-214 import',       'Import hours directly from a completed ICS-214 Activity Log'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('18.2  Equipment', H2))
    s.append(P(
        'Equipment entries use the FEMA Schedule of Equipment Rates. '
        'FieldCommand IMS includes all 44 standard FEMA equipment categories '
        'pre-loaded from the current year schedule. Select the equipment type '
        'and the applicable rate fills automatically.'))
    s.append(SP(4))
    s += steps([
        'Click <b>+ Add Equipment Entry</b>.',
        'Click <b>📋 Lookup</b> to open the rate picker. '
        'Search by equipment type — the FEMA rate fills automatically.',
        'Enter hours used and the equipment identifier (unit number or VIN).',
        'Add the operator name if the operator is separate from the equipment.',
        'The total calculates automatically: hours × FEMA rate.',
    ])
    s.append(SP(6))

    s.append(P('18.3  Materials and Contracts', H2))
    s.append(P(
        'Materials entries document consumable supplies purchased specifically for '
        'the incident. Contracts entries document work performed by contractors. '
        'Both require: vendor name, description, purchase order or contract number, '
        'unit cost, quantity, and total. '
        'Attach receipts and PO documentation as noted — FEMA requires source documentation '
        'for all cost claims.'))
    s.append(SP(6))

    s.append(P('18.4  Project Worksheet Export', H2))
    s.append(P(
        'Click <b>📄 Export Project Worksheet (PW) Text</b> to generate a formatted text summary of all '
        'cost entries suitable for copying into the FEMA Grants Portal or attaching '
        'to a Project Worksheet. The export includes incident name, dates, '
        'itemized costs by category, and total claimed amount.'))
    s.append(SP(4))
    s.append(note(
        'FEMA equipment rates are updated annually. The system displays a reminder '
        'when the loaded rates are more than one year old. Update rates using the '
        'FEMA Equipment Rates page (Chapter 19).', 'note'))
    s.append(PB())
    return s
