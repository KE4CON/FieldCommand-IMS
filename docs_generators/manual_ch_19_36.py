#!/usr/bin/env python3
"""manual_ch_19_36.py — Chapters 19–34 plus Appendix."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from manual_framework import *
print("Chapters 19-36 + Appendix module loaded OK")

def ch19():
    s = chapter(19, 'Federal Emergency Management Agency (FEMA) Equipment Rate Schedule',
                'http://192.168.50.1/fema_rates.html')
    s.append(P(
        'The FEMA Equipment Rates page maintains the Schedule of Equipment Rates '
        'used by the FEMA cost documentation module. FieldCommand IMS ships with '
        'all 44 standard FEMA equipment categories pre-loaded from the 2025 schedule. '
        'Rates can be updated annually as FEMA publishes new schedules.'))
    s.append(SP(6))
    s.append(P('19.1  Viewing and Searching Rates', H2))
    s += steps([
        'Navigate to <b>FEMA Equipment Rates</b> from the Finance section.',
        'The table shows all 44 categories with FEMA code, description, '
        'unit (hour or day), and current rate.',
        'Use the search box to filter by equipment type or FEMA code.',
        'A <b>Rate Year</b> badge shows which year\'s schedule is loaded. '
        'A yellow warning appears when rates are more than one year old.',
    ])
    s.append(SP(6))
    s.append(P('19.2  Updating Rates', H2))
    s += steps([
        'Download the current FEMA Schedule of Equipment Rates from fema.gov.',
        'On the FEMA Equipment Rates page, click <b>✏ Edit</b> on any row '
        'to update that rate. Enter the new rate and click <b>Save</b>.',
        'After updating all changed rates, click <b>Update Rate Year</b> '
        'and enter the current year. This clears the stale-rates warning.',
        'Rates are stored in the local database and used immediately by '
        'the FEMA cost documentation module.',
    ])
    s.append(PB())
    return s


def ch20():
    s = chapter(20, 'Cost Tracking Dashboard',
                'http://192.168.50.1/cost_dashboard.html')
    s.append(P(
        'The Cost Dashboard provides a real-time financial overview of the active '
        'incident. It aggregates all Federal Emergency Management Agency (FEMA) cost entries and T-card daily rates into '
        'a summary view updated automatically every two minutes.'))
    s.append(SP(6))
    s.append(P('20.1  Dashboard Panels', H2))
    s.append(tbl(['PANEL', 'WHAT IT SHOWS'], [
        ['Total incident cost',
         'Running total of all documented costs across all categories. '
         'Large tile at the top — visible at a glance from across the room.'],
        ['Cost by category',
         'Horizontal breakdown bars: Labor · Equipment · Materials · Contracts. '
         'Shows both dollar amount and percentage of total for each category.'],
        ['Resources by type',
         'Personnel count and cost contribution from T-card resources, '
         'grouped by resource type.'],
        ['Cost projection',
         'Extrapolated cost based on current daily burn rate × remaining '
         'operational periods. Useful for budget management during multi-day incidents.'],
        ['Budget tracker',
         'Compare actual costs against an authorized budget amount. '
         'Enter the budget figure to see remaining balance and percentage used.'],
        ['Per-period breakdown',
         'Cost summary broken out by operational period — useful for '
         'after-action documentation and FEMA Project Worksheet (PW) preparation.'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(4))
    s.append(note(
        'The cost dashboard draws data from both the FEMA cost entries '
        '(fema_costs.html) and the daily rate fields on T-cards. '
        'Set daily or hourly rates on each T-card to see resource costs '
        'reflected automatically in the dashboard.', 'note'))
    s.append(PB())
    return s



def ch21():
    s = chapter(21, 'Personnel Accountability',
                'http://192.168.50.1/accountability.html')
    s.append(P(
        'Personnel accountability is a fundamental National Incident Management System (NIMS)/ICS safety requirement. '
        'At any moment during an incident, the Incident Commander and Safety Officer '
        'must be able to answer two questions with certainty: '
        '<b>Who is on this incident?</b> and <b>Where is each person right now?</b> '
        'Failure to maintain accountability has resulted in responder fatalities '
        'at wildland fires, structural collapses, and other incidents where conditions '
        'changed rapidly and personnel could not be located.'))
    s.append(SP(4))
    s.append(P(
        'FieldCommand IMS implements a two-level accountability system that mirrors '
        'the Incident Command System (ICS) doctrine: incident-level accountability through the ICS-211 Check-In '
        'List, and resource-level accountability through the T-card personnel roster. '
        'The Personnel Accountability page integrates both into a single Safety Officer '
        'tool with Personnel Accountability Report (PAR) (Personnel Accountability Report) tracking, check-out recording, '
        'last-known-location logging, and automatic cross-referencing between the two lists.'))
    s.append(SP(6))

    s.append(P('21.1  The Two Levels of Personnel Accountability', H2))
    s.append(tbl(['LEVEL — TOOL', 'WHAT IT TRACKS', 'MAINTAINED BY'], [
        ['Incident level\n\nICS-211 Check-In List\n(checkin.html / scan_checkin.html)',
         'Who has formally checked into this incident? '
         'When did each person arrive? Have they checked out? '
         'Every person on the incident must have an ICS-211 entry '
         'regardless of agency, role, or resource assignment.',
         'Check-in recorder at entry points. '
         'Resources Unit Leader (RESL) maintains the master list.'],
        ['Resource level\n\nT-Card Personnel tab',
         'Who is assigned to each specific resource? '
         'Which crew or unit is each person on? '
         'Where should each crew member be right now?',
         'Ops Section Chief (OSC); crew supervisors update T-card lists.'],
    ], widths=[1.6*inch, CW-4.1*inch, 2.5*inch]))
    s.append(SP(4))
    s.append(note(
        'Both levels are required — neither alone is sufficient. '
        'The ICS-211 tells you everyone who is on the incident. '
        'The T-card personnel roster tells you which resource each person '
        'is assigned to and where they should be. '
        'The cross-reference between the two catches gaps in both directions: '
        'people who checked in but were never assigned to a resource, '
        'and people on a T-card who never completed formal ICS-211 check-in.', 'warn'))
    s.append(SP(6))

    s.append(P('21.2  ICS-211 Check-In — Incident-Level Accountability', H2))
    s.append(P(
        'Every person arriving at the incident — regardless of agency, role, or resource '
        'assignment — must complete ICS-211 check-in. This is the foundation of personnel '
        'accountability. There are three ways to check in:'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'BEST FOR'], [
        ['Camera scan (scan_checkin.html)',
         'High-throughput check-in stations and members with personal '
         'Quick Response (QR) codes or barcodes. '
         'Scan detects automatically at 4 frames per second — no typing required.'],
        ['Manual form entry (checkin.html)',
         'Walk-in personnel, mutual aid, or any person without a Quick Response (QR) code. '
         'Full ICS-211 form with ICS position dropdown and agency field.'],
        ['Scan page manual fallback (scan_checkin.html)',
         'When camera is unavailable — type the member ID, callsign, or radio ID '
         'directly into the manual entry field on the scan page.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(SP(6))

    s.append(P('21.3  ICS-211 Check-Out', H2))
    s.append(P(
        'Check-out is as important as check-in. When a person leaves the incident — '
        'for any reason — they must be checked out so the accountability system '
        'reflects the actual population on the incident. Unchecked-out personnel '
        'create false positives in PAR counts and can trigger unnecessary searches.'))
    s.append(SP(4))
    s += steps([
        'Navigate to <b>Personnel Accountability</b> from the dashboard, '
        'or to <b>Incident Check-In</b> (checkin.html).',
        'Find the person in the ICS-211 check-in list.',
        'Click <b>Check Out</b> on their row. The checkout timestamp is recorded '
        'automatically. They are removed from the active accountability count.',
        'Their record is retained for documentation — they do not disappear '
        'from the list, they move to the "Checked Out" section.',
        'For mass checkout at incident close, use <b>Conduct PAR → Check All Out</b> '
        'from the Personnel Accountability page.',
    ])
    s.append(SP(6))

    s.append(P('21.4  T-Card Personnel Roster — Resource-Level Accountability', H2))
    s.append(P(
        'Every resource T-card should have a complete list of the personnel assigned '
        'to it. This is maintained by the Operations Section and crew supervisors, '
        'and it gives the Safety Officer resource-level accountability: not just '
        '"Jones is on this incident" but "Jones is assigned to Engine 12, '
        'which is assigned to Division Alpha."'))
    s.append(SP(4))
    s += steps([
        'Navigate to <b>ICS Operations</b> from the ICS section.',
        'Click any T-card to open its detail panel.',
        'Click the <b>👤 PERSONNEL</b> tab.',
        'Add each person assigned to that resource — name, their position on '
        'the resource (Crew Boss, EMT, Operator, etc.), agency, and contact/callsign.',
        'If the person is in the roster, type their name and click the suggestion '
        'chip — callsign and agency fill automatically.',
        'Repeat for every person on every resource. '
        'The T-card board shows the personnel count on each card.',
        'Update the list if personnel rotate on or off a resource during the incident.',
    ])
    s.append(SP(4))
    s.append(note(
        'The T-card personnel list and the ICS-211 check-in list are separate records. '
        'Adding someone to a T-card does NOT automatically check them into the ICS-211. '
        'Both must be maintained. The Cross-Reference view on the Personnel Accountability '
        'page flags anyone who is in one list but not the other.', 'warn'))
    s.append(SP(6))

    s.append(P('21.5  Personnel Accountability Report (PAR)', H2))
    s.append(P(
        'A Personnel Accountability Report (PAR) is a formal roll call — a deliberate, '
        'time-stamped check that confirms every person on the incident is accounted for. '
        'PARs should be conducted at regular intervals (typically every operational period '
        'or whenever conditions change), at all incident transitions (shift changes, '
        'operational period changes), whenever a hazard escalates, and immediately '
        'whenever any person cannot be located.'))
    s.append(SP(4))
    s.append(P(
        'The Personnel Accountability page (accountability.html) is the Safety Officer\'s '
        'primary PAR tool. It shows both the ICS-211 list and the T-card personnel roster, '
        'with PAR confirmation buttons for each person.'))
    s.append(SP(4))
    s += steps([
        'Navigate to <b>Personnel Accountability</b> from the dashboard.',
        'Select the incident and operational period.',
        'Click <b>🔴 Conduct PAR</b>. The timestamp is recorded. '
        'The display switches to the ICS-211 list with all personnel sorted '
        'so unconfirmed personnel appear at the top.',
        'Contact each supervisor or crew boss by radio and have them confirm '
        'all personnel on their resource. As each person is confirmed, '
        'click <b>✓ PAR</b> on their row. The count updates in real time.',
        'For T-card-level PAR, switch to the <b>T-CARD PERSONNEL</b> tab '
        'and confirm by resource — each resource group shows its own PAR count.',
        'The <b>⚠ UNACCOUNTED</b> tab shows only the personnel who have not '
        'been confirmed. If anyone cannot be accounted for after exhausting '
        'radio contact, escalate immediately to the Incident Commander (IC).',
        'When all personnel are confirmed, the summary tiles show 0 unaccounted '
        'and the PAR badge updates to green.',
        'To begin a new PAR cycle, click <b>↺ Reset PAR</b>. '
        'All confirmation flags are cleared and the cycle begins again.',
    ])
    s.append(SP(6))

    s.append(P('21.6  Last Known Location', H2))
    s.append(P(
        'The last known location field provides an additional layer of situational '
        'awareness during a PAR. When a supervisor confirms their crew, they can '
        'also report the crew\'s current location — division, sector, grid coordinate, '
        'or landmark. This information displays on both the accountability page '
        'and the resource map.'))
    s.append(SP(4))
    s.append(P(
        'To update last known location: click the <b>📍 Location</b> button '
        'on any person\'s row. A text field appears — enter the location '
        '(e.g. "Division Alpha, east perimeter" or "Base Camp medical tent") '
        'and click Save. The location is recorded with a timestamp.'))
    s.append(SP(6))

    s.append(P('21.7  Cross-Reference — Closing the Accountability Gap', H2))
    s.append(P(
        'The Cross-Reference tab compares the ICS-211 check-in list against '
        'the T-card personnel rosters and flags two specific gaps:'))
    s.append(SP(4))
    s.append(tbl(['CONDITION', 'WHAT IT MEANS', 'ACTION REQUIRED'], [
        ['Checked in — not on any T-card',
         'The person completed ICS-211 check-in but does not appear on '
         'any resource T-card. They are on the incident but not assigned '
         'to any resource. They may be floating staff, a late assignment, '
         'or the T-card may not have been updated.',
         'Assign them to a resource and add them to the T-card, '
         'or confirm they are intentionally unassigned (e.g. Safety Officer, PIO) '
         'and note their location.'],
        ['On T-card — not checked in via ICS-211',
         'The person is listed on a resource T-card but has no ICS-211 entry. '
         'This is a <b>safety gap</b>: they are on the incident, possibly deployed '
         'to a hazardous area, but are not in the formal accountability system.',
         'Direct them to complete ICS-211 check-in immediately. '
         'If they cannot be located, escalate to the IC.'],
    ], widths=[1.8*inch, CW-3.8*inch, 2.0*inch]))
    s.append(SP(4))
    s.append(note(
        'Run the cross-reference at the start of each operational period and any time '
        'new personnel arrive at the incident. A clean cross-reference — no flags in '
        'either direction — means your ICS-211 and T-card rosters are in sync and '
        'every person on the incident is in both the formal check-in system '
        'and assigned to a resource.', 'note'))
    s.append(SP(6))

    s.append(P('21.8  Accountability During Rapid Deterioration', H2))
    s.append(P(
        'When incident conditions change rapidly — a structure becoming unstable, '
        'a fire run, a weather change, a hazmat release — the Safety Officer '
        'may need to conduct an emergency PAR immediately. '
        'The following procedure is recommended:'))
    s.append(SP(4))
    s += steps([
        'Click <b>🔴 Conduct PAR</b> immediately. The timestamp establishes '
        'the start of the accountability check.',
        'Transmit on the incident command channel: '
        '"<i>All supervisors, this is Safety, emergency PAR — '
        'report personnel count by division/group immediately.</i>"',
        'As each supervisor reports, click <b>✓ PAR</b> for each person '
        'on their resource in the T-CARD PERSONNEL tab.',
        'Check the <b>⚠ UNACCOUNTED</b> tab after each supervisor reports. '
        'If anyone remains unaccounted after all supervisors have reported, '
        'transmit their name and last known assignment immediately.',
        'If a person cannot be located within five minutes, '
        'treat it as a missing responder emergency — notify the IC, '
        'halt operations in the affected area, and initiate search.',
        'The Dead Man\'s Switch (deadmans.html) should already be active '
        'if this is a Search and Rescue (SAR) or high-risk operation — it provides an independent '
        'alert if net check-ins stop (see Chapter 12).',
    ])
    s.append(PB())
    return s

def ch22():
    s = chapter(22, 'ICS-213 General Message',
                'http://192.168.50.1/ics213.html')
    s.append(P(
        'The ICS-213 General Message is the standard Incident Command System (ICS) form for written '
        'communications between sections, agencies, or individuals during an incident. '
        'FieldCommand IMS provides a fillable ICS-213 with digital signature capture, '
        'print output, and Winlink integration.'))
    s.append(SP(6))
    s.append(P('21.1  Completing an ICS-213', H2))
    s += steps([
        'Navigate to <b>ICS-213 General Message</b> from the dashboard.',
        'Fill in: To, From (callsign auto-fills name from Federal Communications Commission (FCC) database), '
        'Subject, and Date/Time.',
        'Type the message in the message body field.',
        'If a reply is required, check <b>Reply Requested</b>.',
        'Click the <b>Prepared By</b> signature field and sign with '
        'mouse, touch, or stylus (see Chapter 17.2 for signature instructions).',
        'Click <b>Print</b> to print the completed form, or '
        '<b>Send via Winlink</b> to route the message through Winlink '
        'if a Winlink session is active.',
    ])
    s.append(SP(6))
    s.append(P('21.2  Winlink Integration', H2))
    s.append(P(
        'A completed ICS-213 can be exported directly to Winlink Express or Pat '
        'as a formatted Winlink ICS-213 message. The recipient address, subject, '
        'and message body are pre-filled. See Chapter 29 for Winlink configuration.'))
    s.append(PB())
    return s


def ch23():
    s = chapter(23, 'ICS-214 Activity Log & ICS-309 Communications Log',
                'http://192.168.50.1/ics214.html')
    s.append(P(
        'The ICS-214 Activity Log records the activities and significant events '
        'for each resource or section during an operational period. '
        'Completed ICS-214 entries can be exported directly to Federal Emergency Management Agency (FEMA) Public Assistance (PA) labor '
        'cost documentation, bridging the gap between activity logging and '
        'reimbursement paperwork.'))
    s.append(SP(6))
    s.append(P('22.1  ICS-214 Activity Log', H2))
    s += steps([
        'Navigate to <b>ICS-214</b> from the Planning section.',
        'Select the resource or section this log covers.',
        'For each significant activity, click <b>+ Add Entry</b>: '
        'enter the time, activity description, and resources involved.',
        'At the end of the operational period, click <b>Prepared By</b> '
        'and sign the form.',
        'Click <b>Export to FEMA Labor</b> to push hours from this log '
        'directly into the FEMA Force Account Labor documentation for '
        'the active incident.',
    ])
    s.append(SP(6))
    s.append(P('22.2  ICS-309 Communications Log', H2))
    s.append(P(
        'The ICS-309 is generated automatically from Net Logger data. '
        'It can also be filled manually using the ICS-309 form (ics309.html) '
        'for radio traffic not captured in the Net Logger.'))
    s += steps([
        'Navigate to <b>ICS-309</b> from the Communications section.',
        'Select the net or communications log to reference.',
        'Add manual entries for traffic not logged in the Net Logger.',
        'Click <b>Export ICS-309</b> to download the formatted log for the Incident Action Plan (IAP).',
    ])
    s.append(PB())
    return s


def ch24():
    s = chapter(24, 'Wide Area Network (WAN) Settings & Dual-Source Internet Configuration',
                'http://192.168.50.1/wan_settings.html')
    s.append(P(
        'FieldCommand IMS supports two simultaneous internet sources — primary '
        'and fallback — with automatic failover between them. The WAN Settings page '
        'configures how each source is detected and how the system monitors them. '
        'No carrier names or hardware brands are hardcoded — the system works with '
        'any cellular modem, phone hotspot, satellite dish, or fixed broadband.'))
    s.append(SP(6))

    s.append(P('23.1  WAN Source Configuration', H2))
    s.append(tbl(['FIELD', 'OPTIONS AND DESCRIPTION'], [
        ['Role',
         '<b>Preferred</b> — the primary WAN source. Used first when available.\n'
         '<b>Fallback</b> — used only when the preferred source is unavailable.'],
        ['Label',
         'Human-readable name shown on the dashboard status bar: '
         '"Cellular", "Satellite", "Hotspot", etc.'],
        ['Type',
         'Cellular · Satellite · Hotspot · Fixed broadband · Other'],
        ['Detection method',
         'How the monitor determines if this source is up. '
         'See the table below for all methods.'],
        ['Enabled',
         'Toggle a source on or off without deleting its configuration.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('23.2  Detection Methods', H2))
    s.append(tbl(['METHOD', 'HOW IT WORKS', 'BEST FOR'], [
        ['internet_only',
         'Attempts an outbound internet connection. Succeeds if any internet '
         'Any internet path succeeds.',
         'Phone hotspots, Universal Serial Bus (USB) cellular dongles, any source without a fixed gateway IP'],
        ['ping',
         'Pings a specific IP address — typically the modem or router gateway. '
         'Enter the gateway IP address.',
         'Sources with a known gateway IP (e.g. a cellular router on 192.168.1.1)'],
        ['admin_reachable',
         'Checks if the modem\'s admin web interface is reachable at a given Uniform Resource Locator (URL). '
         'Faster than a full internet check for modems with local admin pages.',
         'Cellular modems with a local admin interface'],
    ], widths=[1.6*inch, CW-3.4*inch, 1.8*inch]))
    s.append(SP(6))

    s.append(P('23.3  Swapping Preferred and Fallback', H2))
    s.append(P(
        'To swap which source is preferred and which is fallback, click the '
        '<b>⇄ Swap Roles</b> button on the WAN Settings page. '
        'This takes effect immediately without restarting any services. '
        'Use this when you want to manually prefer satellite over cellular, '
        'for example, without changing your physical connections.'))
    s.append(SP(4))
    s.append(note(
        'The WAN monitor runs as a background service and updates the dashboard '
        'status bar every 30 seconds. If you change WAN settings, allow up to '
        '60 seconds for the new configuration to take effect.', 'note'))
    s.append(PB())
    return s


def ch25():
    s = chapter(25, 'National Weather Service (NWS) Animated Radar',
                'http://192.168.50.1/radar.html')
    s.append(P(
        'The Next Generation Radar (NEXRAD) Radar page displays animated radar loops from the National '
        'Weather Service using NWS RIDGE II tiles. It requires an active internet '
        'connection and shows an offline banner when Wide Area Network (WAN) is unavailable. '
        'The radar page is accessible from all three dashboard modes.'))
    s.append(SP(6))

    s.append(P('24.1  Radar Controls', H2))
    s.append(tbl(['CONTROL', 'FUNCTION'], [
        ['▶ / ⏸ Play/Pause',   'Start or stop the radar animation loop'],
        ['◀ / ▶ Step',         'Advance one frame at a time — useful for analyzing storm movement'],
        ['Timeline scrubber',  'Jump to any point in the loaded radar loop'],
        ['Speed selector',     '0.5× · 1× · 2× · 4× — controls animation playback speed'],
        ['Palette',            'Standard (reflectivity color scale) · Dual-pol · Enhanced'],
        ['Station selector',   'Select the nearest NEXRAD radar station for your deployment area'],
        ['Auto-refresh',       'Loads new radar data every 5 minutes automatically'],
        ['Reflectivity legend','Color scale overlay showing dBZ values and associated precip rates'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('24.2  Fallback When Offline', H2))
    s.append(P(
        'When the WAN connection is unavailable, the radar page displays an '
        '"Offline — radar unavailable" banner and shows the last successfully '
        'loaded frame with its timestamp. This allows you to see the most recently '
        'received radar image until connectivity is restored. '
        'The page polls for WAN restoration every 30 seconds and resumes '
        'loading new tiles automatically when internet returns.'))
    s.append(PB())
    return s


def ch26():
    s = chapter(26, 'High Frequency (HF) Propagation Tool',
                'http://192.168.50.1/propagation.html')
    s.append(P(
        'The HF Propagation tool retrieves current band conditions from the '
        'Space Weather Prediction Center (SWPC) and displays a band-by-band '
        'propagation forecast. It requires internet access to fetch current data '
        'but displays the last retrieved forecast when offline.'))
    s.append(SP(6))
    s.append(tbl(['BAND', 'TYPICAL USE IN Emergency Communications (EMCOMM)'], [
        ['160m / 80m',  'Regional night-time nets, 0–500 mile coverage'],
        ['40m',         'Primary EMCOMM HF band — day/night, 500–2000 miles'],
        ['20m',         'Long-haul — 2000+ miles, daytime primary'],
        ['15m / 10m',   'Long-haul when solar conditions are favorable'],
        ['6m / 2m',     'Very High Frequency (VHF) — not covered by HF propagation tool'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(4))
    s.append(P(
        'The tool shows Solar Flux Index (SFI), A-index, K-index, and '
        'predicted propagation quality per band. The K-index is the most '
        'immediately useful: K 0–2 is excellent; K 3–4 is fair; K 5+ '
        'indicates a geomagnetic disturbance that degrades HF propagation.'))
    s.append(PB())
    return s


def ch27():
    s = chapter(27, 'Winlink Radio Email',
                'http://192.168.50.1/winlink-import.html')
    s.append(P(
        'FieldCommand IMS integrates with Winlink — the global radio email network '
        'used for Incident Command System (ICS) messaging over RF when internet is unavailable. The integration '
        'covers: outbound ICS-213 messages via Winlink, inbound Winlink form import, '
        'and Pat (a cross-platform Winlink client) running alongside FieldCommand.'))
    s.append(SP(6))

    s.append(P('26.1  Winlink Configuration Options', H2))
    s.append(tbl(['CLIENT', 'PLATFORM', 'TRANSPORT'], [
        ['Winlink Express',  'Windows laptop',         'VARA High Frequency (HF), VARA FM, Telnet, Pactor'],
        ['Pat',              'Raspberry Pi / Linux',   'VARA FM (via Wine), Telnet, AX.25'],
        ['RMS Express',      'Windows laptop',         'Pactor (requires SCS modem)'],
    ], widths=[1.3*inch, 1.5*inch, CW-2.8*inch]))
    s.append(SP(6))

    s.append(P('26.2  Winlink Form Import', H2))
    s.append(P(
        'When Winlink messages arrive containing ICS forms (ICS-213, ICS-214, '
        'position reports), they can be imported directly into FieldCommand IMS '
        'using the Winlink Form Import page.'))
    s.append(SP(4))
    s += steps([
        'In Winlink Express or Pat, read the incoming message with the ICS form attachment.',
        'Save the form as an XML or HTML file.',
        'Navigate to <b>Winlink Form Import</b> from the dashboard.',
        'Click <b>Choose File</b> and select the exported form file.',
        'Click <b>Import</b>. FieldCommand IMS parses the form data and '
        'creates the appropriate ICS form entry in the active incident.',
    ])
    s.append(PB())
    return s


def ch28():
    s = chapter(28, 'Amateur Packet Radio Network (AMPRNet) (44Net) Gateway',
                'http://192.168.50.1/amprgate.html')
    s.append(P(
        'The AMPRNet gateway provides a WireGuard-based tunnel into the 44.0.0.0/8 '
        'amateur radio IP network when internet is available. It runs on a dedicated '
        'second Raspberry Pi (192.168.50.2) — completely isolated from the primary '
        'FieldCommand server. If the gateway fails, nothing on the primary server is affected.'))
    s.append(SP(6))

    s.append(P('27.1  Access Control', H2))
    s.append(P(
        'The AMPRNet gateway enforces Part 97 access control: only licensed amateur '
        'operators with a valid Federal Communications Commission (FCC) callsign may authenticate. Authentication is '
        'validated against the offline FCC database. All access attempts are logged '
        'to /var/log/amprgate-access.log with callsign, IP, timestamp, and result. '
        'Session tokens have an 8-hour TTL.'))
    s.append(SP(6))

    s.append(P('27.2  Gateway Status Page', H2))
    s.append(P(
        'The AMPRNet status page (amprgate.html) shows: tunnel up/down status, '
        'your assigned 44.x.x.x address, connected peers, and the access log. '
        'The public read-only port (9000) is accessible from any device on '
        'EMCOMM-NET. Tunnel control is restricted to the Pi console (port 9001, '
        'localhost only).'))
    s.append(SP(4))
    s.append(note(
        'AMPRNet IP allocation requires registration at portal.ampr.org. '
        'Request a /29 subnet under your callsign. See the Installation Guide '
        'for the complete AMPRNet setup procedure.', 'note'))
    s.append(PB())
    return s


def ch29():
    s = chapter(29, 'JS8Call — High Frequency (HF) Digital Messaging',
                'http://192.168.50.1/')
    s.append(P(
        'JS8Call is a weak-signal HF digital mode designed for keyboard-to-keyboard '
        'messaging and store-and-forward relay. It operates on a Windows laptop '
        'connected to the incident\'s HF transceiver (e.g. an IC-7300 with a '
        'Digirig or similar Universal Serial Bus (USB) audio interface) alongside the FieldCommand system '
        'on the same EMCOMM-NET network.'))
    s.append(SP(6))
    s.append(P('28.1  JS8Call for Emergency Communications (EMCOMM)', H2))
    s.append(tbl(['CAPABILITY', 'DESCRIPTION'], [
        ['Keyboard messaging',   'Real-time chat-style messaging between stations — no callsign required to copy'],
        ['Store and forward',    'Messages are stored at relay stations and forwarded when the destination is heard'],
        ['Heartbeat beacons',    'Automatic periodic beacons announce your station and provide propagation data'],
        ['Group messaging',      'Messages addressed to @EMCOMM, @ARES, @RACES reach all monitoring stations'],
        ['SNR as low as -24dB', 'Copies signals far weaker than SSB voice or Winlink VARA'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))
    s.append(P('28.2  Integration with FieldCommand', H2))
    s.append(P(
        'JS8Call traffic is monitored on the EMCOMM-NET network. Incoming messages '
        'that match Incident Command System (ICS) message formats can be manually entered into the ICS-213 '
        'or the Net Control Logger. A future integration (planned for a subsequent '
        'release) will allow direct JS8Call message ingestion into the incident log.'))
    s.append(PB())
    return s


def ch30():
    s = chapter(30, 'National Traffic System (NTS) Radiogram Generator',
                'http://192.168.50.1/nts.html')
    s.append(P(
        'The NTS Radiogram Generator produces properly formatted ARRL National '
        'Traffic System radiograms for formal message handling. NTS radiograms '
        'are the standard for health-and-welfare and priority traffic during '
        'disasters when telephone and internet are unavailable.'))
    s.append(SP(6))
    s.append(P('29.1  Radiogram Fields', H2))
    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Precedence',    'ROUTINE · WELFARE · PRIORITY · EMERGENCY'],
        ['Handling',      'HXG (delivery by mail), HXC (report delivery), others'],
        ['Station of origin', 'Originating callsign'],
        ['Check',         'Word count of the text — calculated automatically'],
        ['Place of origin', 'City/state of the originating station'],
        ['Time/Date',     'When the message was filed — filled automatically'],
        ['To / Phone',    'Addressee name and phone number for final delivery'],
        ['Text',          'Message body — 25 words maximum for efficient traffic handling'],
        ['Sent by',       'Callsign of the operator sending this copy'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P(
        'Click <b>Generate Radiogram</b> to produce a formatted radiogram '
        'ready to transmit. The word count (check) is calculated automatically. '
        'Click <b>Print</b> to print on a standard traffic form.'))
    s.append(PB())
    return s


def ch31():
    s = chapter(31, 'Repeater Database',
                'http://192.168.50.1/repeaters.html')
    s.append(P(
        'The Repeater Database stores Very High Frequency (VHF)/UHF repeater information for your '
        'deployment area. It is used by the ICS-205 communications plan, '
        'the channel library, and the cheat sheets. '
        'Data is stored locally — no internet required.'))
    s.append(SP(6))
    s.append(P('30.1  Repeater Fields', H2))
    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Callsign',         'Repeater trustee callsign'],
        ['Output frequency', 'Receive frequency (what you listen on)'],
        ['Offset',           '± MHz, or simplex'],
        ['CTCSS / DCS',      'Tone or digital code required to access'],
        ['Mode',             'FM · D-STAR · Fusion (C4FM) · P25 · DMR'],
        ['Coverage',         'Coverage description — city/county/regional'],
        ['Notes',            'Access restrictions, linking, EchoLink node, etc.'],
        ['Emergency use',    'Flag as preferred for emergency use — highlighted in the ICS-205'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s += steps([
        'Click <b>+ Add Repeater</b>.',
        'Fill in all applicable fields.',
        'Click <b>Save</b>. The repeater appears in the database and is '
        'immediately available in the ICS-205 channel picker and the cheat sheets.',
    ])
    s.append(PB())
    return s


def ch32():
    s = chapter(32, 'Channel Library',
                'http://192.168.50.1/channel_library.html')
    s.append(P(
        'The Channel Library stores pre-configured communications channels for '
        'common operations: mutual aid interoperability, public safety talk groups, '
        'amateur simplex and repeater frequencies, and satellite channels. '
        'Channels from the library can be inserted directly into the ICS-205 '
        'Communications Plan with a single click.'))
    s.append(SP(6))
    s.append(P(
        'Each channel entry stores: channel name, frequency/talk group, mode, '
        'CTCSS tone, purpose, and agency assignment. '
        'The library is pre-populated with common interoperability channels '
        'and can be customized for your jurisdiction\'s channel plan.'))
    s.append(SP(4))
    s.append(note(
        'NIFOG (National Interoperability Field Operations Guide) channels '
        'and VTAC channels are included in the default library. '
        'Your jurisdiction\'s specific mutual aid channels should be added '
        'during initial system configuration.', 'note'))
    s.append(PB())
    return s


def ch33():
    s = chapter(33, 'Hospital Proximity & Facilities Directory',
                'http://192.168.50.1/hospitals.html')
    s.append(P(
        'The Hospital Proximity page and Facilities Directory store the locations '
        'and contact information for medical facilities, EOCs, staging areas, '
        'and other operational facilities used during incidents.'))
    s.append(SP(6))
    s.append(P('32.1  Hospital Directory', H2))
    s.append(tbl(['FIELD', 'DESCRIPTION'], [
        ['Facility name',     'Official hospital or clinic name'],
        ['Address',           'Street address for navigation'],
        ['Trauma level',      'Level I · II · III · IV · not designated'],
        ['Phone',             'Main switchboard and emergency department numbers'],
        ['Helipad',           'Yes / No — for aeromedical considerations'],
        ['Distance',          'Calculated from your station grid square (approximate)'],
        ['Notes',             'Diversion status, special capabilities, current capacity'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))
    s.append(P('32.2  Facilities Directory', H2))
    s.append(P(
        'The Facilities Directory (facilities.html) stores staging areas, '
        'EOCs, shelters, supply depots, and other operational locations. '
        'Facilities appear in the ICS-205 and can be linked to T-card assignments. '
        'Each facility stores name, address, type, capacity, and operational notes.'))
    s.append(PB())
    return s


def ch34():
    s = chapter(34, 'Reference Tools — Grid, Cheat Sheets, Resources, Print Center',
                '')
    s.append(P(
        'FieldCommand IMS includes a set of reference and utility tools used '
        'throughout incident operations. All operate fully offline.'))
    s.append(SP(6))

    s.append(P('33.1  Grid Square Calculator', H2))
    s.append(P(
        'The Grid Square Calculator (grid.html) converts between Maidenhead grid '
        'locators and decimal coordinates, and calculates distance and bearing '
        'between two grid squares. It supports 4-character (e.g. EN52) and '
        '6-character (e.g. EN52ab) precision.'))
    s.append(SP(4))
    s.append(tbl(['FUNCTION', 'INPUT', 'OUTPUT'], [
        ['Grid to coordinates',   'Maidenhead grid square (4 or 6 char)',    'Decimal lat/lon and DMS'],
        ['Coordinates to grid',   'Decimal lat/lon',                         'Maidenhead grid square'],
        ['Distance and bearing',  'Two grid squares',                        'Distance (km/mi) and true bearing'],
    ], widths=[1.5*inch, CW*0.42, CW-1.5*inch-CW*0.42]))
    s.append(SP(6))

    s.append(P('33.2  Radio Cheat Sheets', H2))
    s.append(P(
        'The Cheat Sheets page (cheatsheets.html) provides quick-reference cards '
        'for common amateur radio and Incident Command System (ICS) procedures: '
        'phonetic alphabet, Q-codes, RST signal report scale, '
        'ICS command structure, National Incident Management System (NIMS) resource typing, and common High Frequency (HF) calling frequencies. '
        'All cards are printable and designed to fit on a single laminated sheet.'))
    s.append(SP(6))

    s.append(P('33.3  NIMS Resource Typing Library', H2))
    s.append(P(
        'The NIMS Resource Typing Library (resource_types.html) contains '
        'the standard NIMS resource type definitions used to populate T-cards. '
        'Custom resource types specific to your organization can be added here '
        'and immediately become available on the T-card board.'))
    s.append(SP(6))

    s.append(P('33.4  ICS Position Checklists', H2))
    s.append(P(
        'The Position Checklists page (position_checklists.html) provides '
        'NIMS-standard activation checklists for each ICS position: '
        'Incident Commander (IC), Safety Officer, Operations, Planning, Logistics, Finance, '
        'and key unit leaders. Each checklist can be checked off during '
        'position activation and printed for the position binder.'))
    s.append(SP(6))

    s.append(P('33.5  Print Center', H2))
    s.append(P(
        'The Print Center (printcenter.html) provides optimized print layouts for '
        'all ICS forms and documents. From any device on EMCOMM-NET, select the '
        'document to print and click Print — the job routes to any printer '
        'configured on the Pi via CUPS. Print jobs do not require the operator '
        'to be physically at the printer.'))
    s.append(PB())
    return s


def ch35():
    s = chapter(35, 'Network Hardware — Routers, Switch, and Coverage Extension',
                '')
    s.append(P(
        'FieldCommand IMS is designed to work with standard Wi-Fi routers, '
        'managed Power over Ethernet (PoE) switches, and mesh networking to provide reliable wireless '
        'coverage across a deployment site. This chapter covers the recommended '
        'hardware configuration and how to extend coverage using AiMesh nodes.'))
    s.append(SP(6))

    s.append(P('34.1  Recommended Router — ASUS RT-BE58 Go', H2))
    s.append(P(
        'The ASUS RT-BE58 Go is the recommended primary router for FieldCommand IMS. '
        'It is a compact, portable Wi-Fi 7 router designed for mobile deployments — '
        'it runs on USB-C power, supports AiMesh for seamless coverage extension, '
        'and provides dual Wide Area Network (WAN) ports for simultaneous cellular and satellite sources. '
        'It is available from most electronics retailers for approximately $100–130.'))
    s.append(SP(4))
    s.append(tbl(['SPEC', 'RT-BE58 Go'], [
        ['Wi-Fi standard',     'Wi-Fi 7 (802.11be) — backward compatible with all devices'],
        ['Bands',              '2.4 GHz + 5 GHz dual-band'],
        ['WAN ports',          '2× — one for cellular/primary, one for satellite/secondary'],
        ['Power',              'USB-C — runs from any 65W USB-C PD adapter or battery bank'],
        ['AiMesh support',     '✓ — extends EMCOMM-NET coverage with additional RT-BE58 Go units'],
        ['Typical range',      '~2,500 sq ft indoors / larger outdoors'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))

    s.append(P('34.2  Extending Coverage with AiMesh', H2))
    s.append(P(
        'AiMesh is ASUS\'s mesh networking system. Additional ASUS RT-BE58 Go '
        'units can be added as AiMesh nodes to extend the EMCOMM-NET signal '
        'to additional rooms, floors, or outdoor areas. All nodes use the same '
        'Service Set Identifier (SSID) and password — devices roam between nodes automatically without '
        'reconnecting. Nodes are connected to the primary router via wired Ethernet '
        'through the UniFi switch for best performance.'))
    s.append(SP(4))
    s += steps([
        'Connect the AiMesh node to the UniFi switch with an Ethernet cable.',
        'Power on the node. It will appear in the ASUS Router app or the '
        'primary router\'s admin interface at 192.168.50.254.',
        'In the router admin interface, navigate to <b>AiMesh</b> and '
        'click <b>Add AiMesh Node</b>. The new node appears automatically.',
        'Click <b>Connect</b>. The node joins the mesh and begins broadcasting '
        'EMCOMM-NET within about 60 seconds.',
        'Position nodes to overlap coverage by 20–30% for seamless roaming.',
    ])
    s.append(SP(6))

    s.append(P('34.3  UniFi Switch Lite 16 PoE', H2))
    s.append(P(
        'The UniFi Switch Lite 16 PoE is the recommended wired backbone switch. '
        'It provides 16 ports with PoE+ on 8 ports — powering PoE devices '
        '(cellular antennas, cameras, PoE access points) without separate power '
        'adapters. The UniFi management interface provides per-port visibility '
        'of link status, speed, and PoE power draw, which is useful for '
        'diagnosing connectivity issues in the field.'))
    s.append(SP(4))
    s.append(tbl(['PORT GROUP', 'RECOMMENDED USE'], [
        ['Ports 1–2',    'FieldCommand Pi 5 (primary server) and 44Net Gateway Pi 5'],
        ['Ports 3–4',    'ASUS RT-BE58 Go primary router LAN and AiMesh node uplinks'],
        ['Ports 5–8',    'PoE — cellular antenna, satellite PoE injector, PoE cameras'],
        ['Ports 9–16',   'Operator workstations (Pi 500 units, Windows laptop, tablets)'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(6))

    s.append(P('34.4  Power Considerations', H2))
    s.append(P(
        'For field deployments without shore power, FieldCommand IMS can run from '
        'two Astron RS-35M-AP regulated linear power supplies (one per Pi cluster) '
        'fed from a portable generator, or from a high-capacity LiFePO4 battery '
        'with a pure-sine inverter. The complete system draws approximately '
        '80–120 watts under typical load. For battery-only operation, a 100Ah '
        '12V LiFePO4 battery provides approximately 8–10 hours of runtime.'))
    s.append(PB())
    return s


def ch_appendix():
    s = chapter(36, 'Appendix — Quick Reference & Administration',
                '')
    s.append(P('A.1  All Pages — Uniform Resource Locator (URL) Reference', H2))
    pages = [
        ('index.html',             'Main Dashboard'),
        ('incident.html',          'Incident Management / Command Section'),
        ('incident_mgmt.html',     'Incident Archive, Restore, Delete, Beta Reset'),
        ('event_templates.html',   'Pre-Planned Event Templates'),
        ('resources.html',         'T-Card Resource Board'),
        ('resource_map.html',      'GPS-Tracked Resource Map'),
        ('resource_types.html',    'National Incident Management System (NIMS) Resource Typing Library'),
        ('checkin.html',           'Manual Check-In (ICS-211)'),
        ('scan_checkin.html',      'Quick Response (QR) code / Barcode Scan Check-In'),
        ('roster.html',            'Member Roster and QR Code Generator'),
        ('netcontrol.html',        'Amateur Radio Net Control Logger'),
        ('starcom.html',           'Public Safety Net Logger'),
        ('observer.html',          'Observer Mode — Read-Only Net View'),
        ('deadmans.html',          'Dead Man\'s Switch'),
        ('iap.html',               'Incident Action Plan (IAP) Assembly — Planning Section'),
        ('iap_compile.html',       'IAP One-Click Portable Document Format (PDF) Compilation'),
        ('ics-form.html',          'Incident Command System (ICS) Form Suite — all forms'),
        ('ics213.html',            'ICS-213 General Message'),
        ('ics214.html',            'ICS-214 Activity Log'),
        ('ics309.html',            'ICS-309 Communications Log'),
        ('fema_costs.html',        'Federal Emergency Management Agency (FEMA) Public Assistance (PA) Cost Documentation'),
        ('fema_rates.html',        'FEMA Equipment Rate Schedule'),
        ('cost_dashboard.html',    'Real-Time Cost Dashboard'),
        ('wan_settings.html',      'Wide Area Network (WAN) Source Configuration'),
        ('wan-status.html',        'WAN Status Detail Page'),
        ('radar.html',             'Animated Next Generation Radar (NEXRAD) Radar'),
        ('propagation.html',       'High Frequency (HF) Propagation Data'),
        ('tactical.html',          'Tactical Automatic Packet Reporting System (APRS) Map'),
        ('resmap.html',            'Public Safety Resource Map (Starcom)'),
        ('callsign.html',          'Federal Communications Commission (FCC) Callsign Lookup'),
        ('amprgate.html',          'Amateur Packet Radio Network (AMPRNet) (44Net) Gateway Status'),
        ('nts.html',               'National Traffic System (NTS) Radiogram Generator'),
        ('winlink-import.html',    'Winlink Form Import'),
        ('briefing_204a.html',     'ICS-204A Briefing Sheet'),
        ('hospitals.html',         'Hospital Proximity Directory'),
        ('facilities.html',        'Facilities Directory'),
        ('repeaters.html',         'Repeater Database'),
        ('channel_library.html',   'Channel Library'),
        ('cheatsheets.html',       'Radio / ICS Cheat Sheets'),
        ('grid.html',              'Grid Square Calculator'),
        ('position_checklists.html','ICS Position Checklists'),
        ('meetings.html',          'Meeting Scheduler'),
        ('printcenter.html',       'Print Center'),
        ('sartopo_import.html',    'SARTopo GeoJSON Import'),
        ('preflight.html',         'Preflight Deployment Checklist'),
        ('refs.html',              'Reference Library'),
        ('setup.html',             'Organization Setup'),
        ('general_info.html',      'General Info / ICS-201'),
    ]
    s.append(tbl(['URL', 'DESCRIPTION'],
        [[f'192.168.50.1/{p}', d] for p, d in pages],
        widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(6))

    s.append(P('A.2  API Ports', H2))
    s.append(tbl(['PORT', 'SERVICE', 'FUNCTION'], [
        ['5050',  'fcc_lookup_server.py',    'FCC lookups · incidents · roster · WAN config'],
        ['5051',  'ics_platform_server.py',  'ICS forms · T-cards · check-ins · FEMA costs · Global Positioning System (GPS)'],
        ['9000',  'amprgate_status.py',      '44Net status — public read-only on EMCOMM-NET'],
        ['9001',  'amprgate_status.py',      'Tunnel control — localhost only'],
        ['80',    'nginx',                   'Serves all HTML pages and static assets'],
    ], widths=[0.5*inch, 2.2*inch, CW-2.7*inch]))
    s.append(SP(6))

    s.append(P('A.3  Background Services (systemd)', H2))
    s.append(tbl(['SERVICE FILE', 'FUNCTION'], [
        ['fieldcommand-main.service',        'ICS platform server (port 5051)'],
        ['fieldcommand-fcc.service',         'FCC lookup and config server (port 5050)'],
        ['wan-monitor.service',              'WAN source monitoring and failover'],
        ['aprs-rf.service',                  'RF APRS receive via direwolf or Terminal Node Controller (TNC)'],
        ['amprgate-status.service',          '44Net status API (ports 9000/9001)'],
        ['amprgate-poll.service',            '44Net tunnel keepalive and reconnect'],
        ['kiwix-serve.service',              'Kiwix offline reference library server'],
        ['backup.service / backup.timer',    'Nightly SQLite backup to Universal Serial Bus (USB) drive'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(6))

    s.append(P('A.4  Copyright & License', H2))
    s.append(P('A.5  Abbreviations & Acronyms', H2))
    s.append(P(
        'The following abbreviations and acronyms are used throughout this manual. '
        'Each is defined on first use in every chapter. This table serves as a '
        'quick reference for readers who open to a chapter mid-document.'))
    s.append(SP(4))
    from manual_framework import ABBREVIATIONS
    AB = ParagraphStyle('AB', fontName='Helvetica-Bold', fontSize=8, leading=11)
    AD = ParagraphStyle('AD', fontName='Helvetica', fontSize=7.5, leading=10, textColor=HexColor('#333333'))
    abbrev_rows = sorted(ABBREVIATIONS.items())
    mid = len(abbrev_rows) // 2 + len(abbrev_rows) % 2
    col1 = abbrev_rows[:mid]
    col2 = abbrev_rows[mid:]
    while len(col2) < len(col1):
        col2.append(('', ''))
    combined = []
    for (a1,d1),(a2,d2) in zip(col1, col2):
        combined.append([
            Paragraph(f'<b>{a1}</b>', AB),
            Paragraph(d1, AD),
            Paragraph(f'<b>{a2}</b>', AB) if a2 else Paragraph('', AD),
            Paragraph(d2, AD) if d2 else Paragraph('', AD),
        ])
    col_w = CW / 2 - 0.1*inch
    abbr_tbl = Table(combined,
        colWidths=[0.65*inch, col_w-0.65*inch, 0.65*inch, col_w-0.65*inch],
        repeatRows=0, splitByRow=1)
    abbr_tbl.setStyle(TableStyle([
        ('FONTSIZE',      (0,0),(-1,-1), 8),
        ('LEADING',       (0,0),(-1,-1), 10),
        ('TOPPADDING',    (0,0),(-1,-1), 3),
        ('BOTTOMPADDING', (0,0),(-1,-1), 3),
        ('LEFTPADDING',   (0,0),(-1,-1), 4),
        ('RIGHTPADDING',  (0,0),(-1,-1), 4),
        ('LINEBELOW',     (0,0),(-1,-2), 0.25, LINE),
        ('LINEAFTER',     (1,0),(1,-1),  0.5,  LINE),
        ('VALIGN',        (0,0),(-1,-1), 'TOP'),
    ]))
    s.append(abbr_tbl)
    s.append(SP(6))

    s.append(P(
        'FieldCommand IMS v1.0 — Copyright © 2026 James Rospopo KE4CON. '
        'Developed for emergency management and amateur radio organizations. '
        'Source code: MIT License. Documentation: CC BY-SA 4.0. '
        'GitHub: https://github.com/KE4CON/FieldCommand-IMS'))
    s.append(PB())
    return s
