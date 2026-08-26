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
        "The Public Safety Net Logger is the tool for running a radio net where operators "
        "check in by radio ID or unit number instead of by amateur callsign. It is built "
        "for trunked radio, Project 25 (P25), Digital Mobile Radio (DMR), and conventional "
        "public safety systems, and for interoperability exercises and served-agency "
        "support where some participants may not hold an amateur license. It keeps a "
        "complete, time-stamped log of every unit and every message, calculates on-net "
        "time for cost recovery, and exports the whole net as a printable Incident Command "
        "System ICS-309 Communications Log. Everything you log is saved on the server the "
        "moment you enter it.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: create a net, log each unit as it checks in, log the message "
        "traffic, then close the net and export the ICS-309.", 'tip'))
    s.append(SP(6))

    s.append(P('8.1  How It Differs From the Amateur Net Logger', H2))
    s.append(P(
        "The Public Safety Net Logger and the Amateur Net Logger (Chapter 7) look and work "
        "almost the same. The difference is the primary identifier and whether a license "
        "check applies."))
    s.append(SP(4))
    s.append(tbl(['FEATURE', 'AMATEUR NET LOGGER', 'PUBLIC SAFETY NET LOGGER'], [
        ['Primary ID',        'Amateur radio callsign, auto-filled from the local database',
                              'Radio ID or unit number'],
        ['License check',     'Federal Communications Commission (FCC) lookup confirms an active license',
                              'None required'],
        ['Roster lookup',     'By callsign to name and member ID',
                              'By radio ID to name and member ID'],
        ['ICS-309 station',   'Callsign in the station column',
                              'Radio ID in the station column'],
        ['Typical use',       'Amateur emergency communications nets',
                              'Public safety agency nets, interoperability exercises'],
    ], widths=[1.3*inch, CW*0.40, CW-1.3*inch-CW*0.40]))
    s.append(SP(4))
    s.append(note(
        "A participant who holds both an amateur license and a public safety radio ID "
        "should check into the public safety net by radio ID only. If the same person also "
        "works a concurrent amateur net on the incident, they check into the Amateur Net "
        "Logger separately by callsign. This keeps both logs accurate.", 'note'))
    s.append(SP(6))

    s.append(P('8.2  The Screen at a Glance', H2))
    s.append(P(
        "The page has three working areas. Learn where each lives and the rest is easy."))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IS THERE'], [
        ['Top bar',
         'The <b>+ New Net</b> button, a row of badges for the active nets (click a badge '
         'to switch nets), and on the right the <b>Observer Link</b>, <b>ICS-309</b>, and '
         '<b>Backup</b> buttons.'],
        ['Center column',
         'The net header (name, type, open/close times, <b>Drill Mode</b> checkbox, and '
         '<b>Close Net</b> button), the entry form for logging units, and the two tabs '
         '<b>Units Logged</b> and <b>Traffic</b>.'],
        ['Right sidebar',
         'The <b>Net Summary</b> panel (net, type, unit count, traffic count, and times) '
         'and an <b>Active Nets</b> list.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('8.3  Creating a Net', H2))
    s += steps([
        'Click <b>+ New Net</b> at the top left. The <b>Create Starcom Net</b> box opens.',
        'Fill in the fields (only the name is required), described in the table below.',
        'Click <b>Create Net</b>. The net opens, its badge appears in the top bar, and the '
        'entry form becomes ready. Click <b>Cancel</b> to close the box without creating a net.',
    ])
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Net Name', 'Required. A short name for this net, such as "County Interop 1".'],
        ['Net Type', 'The kind of net, chosen from a list: Dispatch Net, Tactical Net, '
         'Command Net, Mutual Aid Net, Search and Rescue Net, EOC Coordination Net, or '
         'Medical Net. (EOC is the Emergency Operations Center.)'],
        ['Talkgroup', 'The radio technology in use: Digital Talkgroup, Conventional '
         'Digital, Conventional Analog, P25, or DMR.'],
        ['Channel / Frequency', 'The channel name or frequency the net is running on, '
         'for example "TAC-4" or "155.340".'],
        ['Dispatch Center', 'The dispatch center or agency the net answers to. It shows in '
         'the net header once set.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('8.4  Logging a Unit Check-In', H2))
    s.append(P(
        "With a net open, use the entry form to log each unit. Only the Radio ID is "
        "required; fill in as much of the rest as the traffic gives you."))
    s.append(SP(4))
    s += steps([
        'In <b>Radio ID / Unit #</b>, type the unit number or radio ID exactly as heard.',
        'Add the <b>Unit Name / Callsign</b> if you have it.',
        'Choose a <b>Status</b> and a <b>Precedence</b> (see 8.5).',
        'Optionally add the <b>Talkgroup</b>, a <b>Channel / Frequency</b> (or click '
        '<b>Pick</b> to choose from the Channel Library, see 8.6), a <b>Location</b>, and '
        '<b>Remarks</b>.',
        'Optionally set an <b>ICS Position for this incident</b> and an <b>Incident ID</b>; '
        'entering an Incident ID reveals an <b>ICS-211</b> link to the check-in list.',
        'Click <b>LOG ENTRY</b>. The unit appears at the top of the <b>Units Logged</b> tab '
        'and is saved at once. Click <b>Clear</b> to empty the form without logging.',
    ])
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Dispatch Center', 'Sets or updates the dispatch center shown in the net header.'],
        ['Radio ID / Unit #', 'Required. The primary identifier for the unit.'],
        ['Unit Name / Callsign', 'A friendlier name, or the operator callsign if licensed.'],
        ['Status', 'What the unit is doing right now (see 8.5).'],
        ['Talkgroup', 'The talkgroup or channel type the unit is on.'],
        ['Channel / Frequency', 'The specific channel; the <b>Pick</b> button pulls from '
         'the incident ICS-205 and Channel Library.'],
        ['Precedence', 'How urgent the traffic is (see 8.5). Sets the color stripe on the '
         'log entry.'],
        ['Location', 'Where the unit is; shown with a pin marker on the entry.'],
        ['Remarks', 'Any free-text note about this unit or message.'],
        ['ICS Position', 'Optional. The Incident Command System role this unit fills, '
         'chosen from grouped Command, Operations, Planning, Logistics, and Finance lists.'],
        ['Incident ID', 'Optional. Ties the entry to a specific incident and shows the '
         'ICS-211 Check-In List link.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('8.5  Status, Precedence, and Talkgroup Options', H2))
    s.append(P('The drop-down choices on the entry form, in plain language.'))
    s.append(SP(4))
    s.append(P('8.5.1  Status', H3))
    s.append(tbl(['OPTION', 'MEANING'], [
        ['Check-In', 'The unit is joining the net.'],
        ['Traffic / Priority Traffic', 'The unit is passing a message, routine or urgent.'],
        ['Emergency', 'Life-safety traffic that takes priority over everything else.'],
        ['Dispatch', 'A dispatch assignment to a unit.'],
        ['Check-Out', 'The unit is leaving the net.'],
        ['En Route / On Scene / Available / Out of Service',
         'Standard unit-status reports used to track where a unit is in its assignment.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P('8.5.2  Precedence', H3))
    s.append(tbl(['OPTION', 'MEANING'], [
        ['Routine', 'Normal traffic. No color emphasis.'],
        ['Welfare', 'Health-and-welfare traffic. Green stripe.'],
        ['Priority', 'Important, time-sensitive traffic. Amber stripe.'],
        ['Emergency', 'Life-safety traffic. Red stripe, most prominent.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P('8.5.3  Talkgroup', H3))
    s.append(P(
        "The talkgroup list on the entry form offers Digital Talkgroup, Conventional "
        "Digital, Conventional Analog, P25 Direct, DMR Direct, and GMRS (General Mobile "
        "Radio Service). Pick the one that matches how the unit is transmitting."))
    s.append(SP(6))

    s.append(P('8.6  Picking a Channel From the Library', H2))
    s.append(P(
        "Rather than typing a frequency, click the <b>Pick</b> button next to the "
        "<b>Channel / Frequency</b> field. FieldCommand reads the active incident "
        "communications plan and opens a <b>Select Channel</b> list."))
    s.append(SP(4))
    s += steps([
        'Click <b>Pick</b>. A search box and a list of channels appear.',
        'Each row is tagged by source: <b>205</b> (from the incident ICS-205 plan), '
        '<b>RPT</b> (from the repeater database), or <b>LIB</b> (the Channel Library).',
        'Type in the search box to filter, then click a channel. Its name and frequency '
        'fill the field. Click <b>Cancel</b> to close without choosing.',
    ])
    s.append(note(
        "If you see \"No channels found,\" the incident has no ICS-205 plan yet. Type the "
        "channel by hand, or build the communications plan first (Chapter 6 and the ICS "
        "forms).", 'note'))
    s.append(SP(6))

    s.append(P('8.7  Logging Message Traffic', H2))
    s.append(P(
        "The <b>Traffic</b> tab keeps the formal message log — the heart of the ICS-309. "
        "Click the <b>Traffic</b> tab, then fill the row at the top:"))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['From Unit / Radio ID', 'Who originated the message.'],
        ['To Unit / Address', 'Who the message is for.'],
        ['Type', 'The handling: Dispatch, Tactical, Resource Request, Status, Priority, '
         'or Emergency.'],
        ['Message summary', 'A short plain-language summary of the message.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(P(
        "Click <b>Log</b> to record it. The message appears at the top of the traffic list "
        "with its time stamp, and the traffic counter updates in the header and sidebar."))
    s.append(SP(6))

    s.append(P('8.8  Checking Units Out and On-Net Time', H2))
    s.append(P(
        "Each logged unit shows its check-in time, its status badge, any member ID pulled "
        "from the roster, and a running <b>Duration</b>. When a unit leaves, click its "
        "<b>Check Out</b> button; the button changes to show the unit is out and the "
        "duration freezes. Any unit still on the net when you close it is checked out "
        "automatically."))
    s.append(note(
        "Durations are rounded UP to the nearest quarter hour (a unit on for one minute "
        "counts as 0:15). This matches how reimbursable personnel time is usually claimed. "
        "The member ID shown on an entry comes from the roster when the radio ID or name "
        "matches a member.", 'note'))
    s.append(SP(6))

    s.append(P('8.9  Drill Mode', H2))
    s.append(P(
        "Before an exercise, tick the <b>Drill Mode</b> checkbox in the net header. A bold "
        "banner reading DRILL / EXERCISE - NOT ACTUAL EMERGENCY appears across the top, and "
        "the exported ICS-309 is stamped DRILL / EXERCISE. This prevents an exercise log "
        "from ever being mistaken for a real event. Un-tick it to return to normal."))
    s.append(SP(6))

    s.append(P('8.10  Closing, Exporting, and Sharing', H2))
    s.append(P(
        "Three buttons at the top right, plus <b>Close Net</b> in the header, finish the net."))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Close Net', 'Ends the net, stamps the close time, and automatically checks out '
         'every remaining unit. You are asked to confirm first.'],
        ['ICS-309', 'Builds the printable ICS-309 Communications Log — the message traffic '
         'log and the unit check-in log, with net times and totals — and opens it to print '
         'or save as a file.'],
        ['Observer Link', 'Copies a read-only, auto-refreshing web link to this net that '
         'you can share with any device on the network (the Observer view, Chapter 9).'],
        ['Backup', 'Downloads the entire net as a JSON data file for your own records.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(note(
        "Closing a net does not delete it. All net data stays on the server and is part of "
        "the incident record, so you can reopen the ICS-309 or the backup at any time.", 'tip'))
    s.append(SP(6))

    s.append(P('8.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The entry form is missing',
         'No net is selected. Click a net badge in the top bar, or click + New Net to '
         'create one. The form appears once a net is open.'],
        ['"Select a net first" when I click Log Entry',
         'Same cause. Pick or create a net first, then log the unit.'],
        ['"Enter a Radio ID" warning',
         'The Radio ID / Unit # box is empty. It is the one required field on the entry '
         'form; type the unit identifier and log again.'],
        ['The Pick button says no channels found',
         'The incident has no ICS-205 communications plan for period 1. Type the channel by '
         'hand, or build the ICS-205 first.'],
        ['A unit shows no member ID',
         'The radio ID or name did not match anyone on the roster. That is normal for '
         'outside agencies; the log is still complete. Add the person to the roster if they '
         'belong to your group.'],
        ['My exercise log looks like a real event',
         'Turn on Drill Mode before the exercise. It stamps the banner and the ICS-309 so '
         'the log cannot be mistaken for an actual emergency.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch9():
    s = chapter(9, 'Observer Mode — Read-Only Net View',
                'http://192.168.50.1/observer.html')
    s.append(P(
        'Observer Mode is a read-only, self-refreshing window into any active net. It shows the '
        'same check-in list and traffic log the Net Control operator sees, but it has no buttons '
        'that change anything - nobody watching an observer screen can add a check-in, close the '
        'net, or edit a single field. That is exactly why it exists. A section chief, a served-'
        'agency liaison, an Emergency Operations Center (EOC) duty officer, or a served-agency '
        'representative can keep the net picture up on their own device without ever touching, or '
        'accidentally disturbing, the live Net Control workstation. Any device already on the '
        'EMCOMM-NET Wi-Fi opens the page in a browser - no app to install, no login, any '
        'operating system.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: hand someone the observer link and they can watch the net live, '
        'read-only, refreshing itself every fifteen seconds.', 'tip'))
    s.append(SP(6))

    s.append(P('9.1  Opening the Observer Page', H2))
    s.append(P(
        'There are two ways in. Most observers arrive by a shared link that already points at one '
        'specific net; anyone who opens the page with no net chosen gets a picker of every net on '
        'the server.'))
    s += steps([
        'The everyday way: the Net Control operator clicks <b>Observer Link</b> on the active '
        'net, which copies a web address (Uniform Resource Locator, or URL) ending in '
        '<b>?net=</b> and the net number. They share it - over the net by voice, by Winlink or '
        'JS8Call message, or by reading it out. You open that link and the page goes straight to '
        'that net.',
        'The pick-it-yourself way: open <b>http://192.168.50.1/observer.html</b> with no net on '
        'the end of the address. The page shows <b>Select a Net to Observe</b> and lists every '
        'net (see 9.3). Click the one you want.',
        'Bookmark the link once you are on the net you want - it reopens the same net every time.',
    ])
    s.append(SP(6))

    s.append(P('9.2  The Header Bar', H2))
    s.append(P(
        'A colored strip runs across the very top of every observer screen. It never scrolls '
        'away, so the read-only reminder and the clock are always in view.'))
    s.append(SP(4))
    s.append(tbl(['WHAT YOU SEE', 'WHAT IT MEANS'], [
        ['An eye icon and the words <b>OBSERVER MODE - READ ONLY</b>',
         'The permanent reminder that this screen cannot change anything. It is on every '
         'observer page.'],
        ['A second line under it',
         'The name of the net you are watching (with "(Starcom)" added when it is a public-'
         'service net). It reads "Loading..." for a moment while the page fetches the net.'],
        ['A large green clock on the right',
         'The current time in Coordinated Universal Time (UTC), the 24-hour standard used on '
         'every ICS form. It ticks once a second.'],
        ['<b>Auto-refresh in N s</b>',
         'A countdown to the next automatic reload. It starts at 15 and counts down.'],
        ['A thin bar directly below the strip',
         'A progress bar that drains from full to empty over the fifteen seconds, a visual '
         'twin of the countdown number.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(SP(6))

    s.append(P('9.3  The Net Picker', H2))
    s.append(P(
        'When you open the page without choosing a net, the picker lists every net on the '
        'server so you can select one. Each row is one net.'))
    s.append(SP(4))
    s.append(tbl(['ON EACH ROW', 'WHAT IT TELLS YOU'], [
        ['Net name (bold)', 'The name the operator gave the net, such as "Thursday Evening Net".'],
        ['Type and entry count', 'The net type and how many stations have been logged - for '
         'example, "ARES Net - 12 entries".'],
        ['<b>ACTIVE</b> or <b>CLOSED</b> badge', 'Green ACTIVE means the net is still open; gray '
         'CLOSED means it has ended (you can still read a closed net).'],
        ['<b>STARCOM</b> badge', 'Blue badge marking a public-service net (shown only when it '
         'applies).'],
        ['<b>DRILL</b> badge', 'Amber badge marking an exercise, not a real event (shown only '
         'when it applies).'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(P('Click a row to open that net. The address bar updates to the direct link, which '
               'you can then bookmark or share.'))
    s.append(SP(6))

    s.append(P('9.4  The Net Header', H2))
    s.append(P(
        'Once a net is open, a panel at the top of the view identifies it and shows its state.'))
    s.append(SP(4))
    s.append(tbl(['ELEMENT', 'WHAT IT SHOWS'], [
        ['Net name (large)', 'The name of the net being observed.'],
        ['Meta line', 'The net type and its identifying number - for example, "ARES Net - '
         'ID: 4" - with "STARCOM" added on a public-service net.'],
        ['Status badge', 'Green <b>ACTIVE</b> while the net is open, gray <b>CLOSED</b> after it '
         'ends.'],
        ['<b>Updated HH:MM UTC</b>', 'The time of the most recent refresh, so you can confirm the '
         'view is current.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(note(
        'If the net is a drill, a bold banner reading "DRILL / EXERCISE - NOT ACTUAL EMERGENCY" '
        'appears across the top of the view. It is there so no one mistakes exercise traffic for '
        'a real event.', 'warn'))
    s.append(SP(6))

    s.append(P('9.5  The Stations Logged Column', H2))
    s.append(P(
        'The left half of the view is the check-in list, headed <b>STATIONS LOGGED</b> with a '
        'live count in parentheses. The newest check-in sits at the top. Each station is one '
        'card:'))
    s.append(SP(4))
    s.append(tbl(['ON EACH CARD', 'WHAT IT MEANS'], [
        ['Callsign (bold)', 'The station callsign as Net Control logged it.'],
        ['Name', 'The operator name, when it was captured (often auto-filled from the offline '
         'FCC database).'],
        ['Status badge', 'The station status the operator recorded - it is color-coded by '
         'message precedence (see 9.6).'],
        ['Time in UTC', 'The check-in time as hours:minutes:seconds, 24-hour UTC.'],
        ['Location', 'The station location, when one was entered (shown after the time).'],
        ['Remarks', 'Any note the operator added for that station, shown under the line.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(P('If no one has checked in yet, the column reads <b>No stations logged</b>.'))
    s.append(SP(6))

    s.append(P('9.6  Precedence Colors', H2))
    s.append(P(
        'Each station card carries a colored left edge that reflects the precedence (urgency) of '
        'its traffic, so an observer can spot an emergency at a glance without reading every '
        'line.'))
    s.append(SP(4))
    s.append(tbl(['PRECEDENCE', 'LEFT-EDGE COLOR', 'MEANING'], [
        ['EMERGENCY', 'Red', 'Immediate danger to life or property - the highest urgency.'],
        ['PRIORITY', 'Amber', 'Important traffic that needs prompt handling but is not life-'
         'threatening.'],
        ['WELFARE', 'Green', 'Health-and-welfare traffic - status of people, reassurance '
         'messages.'],
        ['ROUTINE', 'Plain gray', 'Normal traffic with no special urgency (the default).'],
    ], widths=[1.4*inch, 1.4*inch, CW-2.8*inch]))
    s.append(SP(6))

    s.append(P('9.7  The Traffic Log Column', H2))
    s.append(P(
        'The right half of the view is headed <b>TRAFFIC LOG</b> with its own live count. It '
        'lists formal message traffic passed on the net, newest first. Each entry is one card:'))
    s.append(SP(4))
    s.append(tbl(['ON EACH CARD', 'WHAT IT MEANS'], [
        ['From and to callsigns', 'The sending station and the receiving station, shown as '
         '"FROM to TO".'],
        ['Time in UTC', 'When the traffic was logged, hours:minutes:seconds UTC.'],
        ['Type', 'The kind of traffic the operator recorded, shown after the time.'],
        ['Note', 'A short description of the message, when one was entered.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(P('When nothing has been passed, the column reads <b>No traffic</b>.'))
    s.append(SP(6))

    s.append(P('9.8  Staying Current - Auto-Refresh', H2))
    s.append(P(
        'The page reloads its data by itself every fifteen seconds. You do not touch anything - '
        'the countdown in the header reaches zero, the page pulls the latest check-ins and '
        'traffic, the "Updated" time changes, and the countdown starts over. That is why an '
        'observer screen left up on a wall monitor stays honest without an operator babysitting '
        'it. The clock in the header ticks every second on its own, separate from the fifteen-'
        'second data refresh.'))
    s.append(SP(4))
    s.append(note(
        'Observer Mode does not repeat the net frequency or mode, and it has no elapsed-net '
        'timer - it shows the net name, type, and identifying number instead. For the full net '
        'controls and timers, use the Net Control page (Chapter 7).', 'note'))
    s.append(SP(6))

    s.append(P('9.9  What Observers Can and Cannot Do', H2))
    s.append(P(
        'Observer Mode is read-only by design. There is no way, from this page, to change the '
        'net - the buttons simply are not there.'))
    s.append(SP(4))
    s.append(tbl(['OBSERVERS CAN', 'OBSERVERS CANNOT'], [
        ['See every check-in live, newest first', 'Add, edit, or remove a check-in'],
        ['See the net status and last-updated time', 'Open or close the net'],
        ['Read the full traffic log', 'Add or change a traffic entry'],
        ['Watch it refresh itself every 15 seconds', 'Change any net setting'],
        ['Bookmark and reopen the observer link', 'Reach the Net Control workstation view'],
        ['Switch nets from the picker', 'Delete or export net data'],
    ], widths=[CW/2, CW/2]))
    s.append(SP(6))

    s.append(P('9.10  Sharing the Observer Link', H2))
    s.append(P(
        'The link is generated on the Net Control side, so a busy observer never has to build a '
        'web address by hand.'))
    s += steps([
        'On the Net Control page (Chapter 7), select the net you want people to watch.',
        'Click <b>Observer Link</b>. The web address for that net is copied to the clipboard.',
        'Paste and share it - in a group chat, a Winlink or JS8Call message, an email on the '
        'LAN, or read it aloud over the net.',
        'Each observer opens the link on any device already joined to the EMCOMM-NET Wi-Fi. It '
        'lands directly on that net, read-only, and begins refreshing.',
    ])
    s.append(SP(6))

    s.append(P('9.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The page says "Cannot reach API server at 192.168.50.1:5050"',
         'The core service is not answering. Confirm the device is on EMCOMM-NET Wi-Fi, then '
         'check that the fcc-lookup service is running on the Pi (Chapter on System Health). '
         'Reload once it is back.'],
        ['A pop-up says "Net not found"',
         'The link points at a net number that no longer exists on this server. Open '
         'http://192.168.50.1/observer.html with no net on the end and pick the net from the '
         'list.'],
        ['The picker shows "No nets found"',
         'No net has been created yet. Open one on the Net Control page first, then reopen the '
         'observer link.'],
        ['New check-ins are not appearing',
         'The page refreshes every fifteen seconds - wait for the countdown, or reload the page. '
         'If it still lags, confirm Net Control is actually logging to that same net number.'],
        ['The screen is stuck on an error after a brief hiccup',
         'A momentary network drop can leave the view showing an error. Reload the page - it '
         'recovers and resumes refreshing.'],
        ['I see edit buttons and want to change something',
         'You will not - Observer Mode has none by design. To make changes, use the Net Control '
         'workstation (Chapter 7).'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch10():
    s = chapter(10, 'Barcode & Quick Response (QR) code Scan Check-In',
                'http://192.168.50.1/scan_checkin.html')
    s.append(P(
        'The Scan Check-In page turns any phone, tablet, or laptop into a fast personnel '
        "check-in station. Point the camera at a member's Quick Response (QR) code or "
        'barcode, or type an identifier by hand, and the person is looked up in the roster, '
        'their details fill in, and one tap records the check-in against the current '
        'incident. It uses the web browser\'s own built-in Barcode Detector -- no app to '
        'install, no library to download, no internet -- so it works fully offline on '
        'EMCOMM-NET. It reads QR codes plus Code 128, Code 39, European Article Number '
        '(EAN) 13 and 8, Data Matrix, Portable Document Format 417 (PDF417), and Aztec '
        'barcodes.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: scan the code or type the identifier, glance at the auto-filled '
        'details, and tap Check In -- the person is on the incident roster in seconds.', 'tip'))
    s.append(SP(6))

    s.append(P('10.1  Four Ways to Read a Person In', H2))
    s.append(P(
        'The page offers four input methods and picks the ones your device can actually do. '
        'A staffed check-in station usually uses the live camera or a USB scanner; a '
        'walk-up on a plain phone uses Take Photo or manual entry.'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'HOW IT WORKS', 'BEST FOR'], [
        ['Live camera',
         'The rear camera runs as a viewfinder and detects a code automatically at four '
         'frames per second. The same code is ignored for three seconds so one card is not '
         'read twice. Needs a secure Hypertext Transfer Protocol Secure (HTTPS) link.',
         'A staffed, high-volume check-in station'],
        ['Take Photo of QR',
         'Snaps one still photo with the device camera and reads the code out of that '
         'picture. Works over a plain (non-HTTPS) link where the live viewfinder is blocked.',
         'A phone or tablet on a plain http connection'],
        ['Manual ID entry',
         'Type a member identifier, callsign, or radio identifier and press Enter or click '
         'Look Up. Same roster lookup as a scan.',
         'Walk-ins with no code; when no camera is available'],
        ['USB or Bluetooth scanner',
         'A hardware scanner acts like a keyboard: it "types" the code and presses Enter '
         'into the manual box, which stays focused so the lookup fires hands-free.',
         'A fixed desk station reading printed badges'],
    ], widths=[1.25*inch, CW-3.05*inch, 1.8*inch]))
    s.append(SP(6))

    s.append(P('10.2  The Screen at a Glance', H2))
    s.append(P(
        'From top to bottom the page is laid out in the order you use it:'))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IT IS'], [
        ['Camera viewfinder',
         'The black scan window with a white corner frame and a moving blue scan line. '
         'A status line at the bottom tells you what the scanner is doing.'],
        ['Camera controls',
         'The <b>Start Camera</b> and <b>Stop Camera</b> buttons and a camera-picker '
         'drop-down (front or rear) for the live scan.'],
        ['Take Photo of QR',
         'A button that opens the device camera to snap one still, with a short note '
         'explaining it reads the person\'s QR card.'],
        ['Manual ID entry',
         'A single text box ("KE4CON  or  ESV-001  or  412") with a <b>Look Up</b> button.'],
        ['Check-in form',
         'The details that appear once a code resolves -- name, identifier, agency, '
         'position, and resource type -- with the green <b>Check In</b> button.'],
        ['Recent Check-Ins This Session',
         'A running list of the last check-ins made on this device since the page opened.'],
        ['Incident badge',
         'The strip at the very bottom naming the incident and operational period these '
         'check-ins are being filed under.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('10.3  Choosing the Incident First', H2))
    s.append(P(
        'Every check-in is filed against one incident and one operational period. The badge '
        'at the bottom of the page shows which. When it reads <b>Incident: (name) - Period '
        '(number)</b> you are ready. If it reads <b>No incident selected</b>, the check-ins '
        'have nowhere to land -- open the page from the incident\'s ICS-211 Share Uniform '
        'Resource Locator (URL) link, or select an incident on the dashboard first, so the '
        'page opens already pointed at the right incident.'))
    s.append(SP(6))

    s.append(P('10.4  Checking Someone In with the Live Camera', H2))
    s += steps([
        'Open <b>Scan Check-In</b> from the dashboard. Confirm the incident badge at the '
        'bottom names the right incident.',
        'Click <b>Start Camera</b>. If the device has more than one camera, choose the '
        'rear-facing one from the camera drop-down first.',
        'Hold the member\'s QR code or barcode inside the white corner frame. The status '
        'line reads "Scanning..." and then "Scanned: (code)" when it catches one. On phones '
        'that support it, the device gives a short buzz.',
        'If the person is on the roster, their details fill in with green borders and a green '
        'banner names them and marks them a roster member or a visitor. Glance over the '
        'fields and correct anything that is wrong.',
        'If the person is not on the roster, a red "not in roster" banner appears and their '
        'scanned code drops into the identifier field. Type the name and agency by hand.',
        'Click <b>Check In</b>. A full-screen "CHECK-IN COMPLETE" confirmation shows the '
        'name and the check-in time, and the phone buzzes.',
        'Click <b>Scan Next Person</b> to clear the form for the next member. Use '
        '<b>Stop Camera</b> when the line is done.',
    ])
    s.append(SP(6))

    s.append(P('10.5  Take Photo and Manual Entry (No Live Camera)', H2))
    s.append(P(
        'The live viewfinder needs a secure HTTPS link. On a plain http connection, or on a '
        'browser that blocks it, use one of these instead -- both reach the same lookup.'))
    s.append(P('<b>Take Photo of QR</b> -- click the button, snap one clear photo that fills '
               'the frame with the code, and the page reads it from the still image. If it '
               'reads "No QR code found", hold steady, get closer, and retake.', Bullet))
    s.append(P('<b>Manual ID entry</b> -- type the person\'s callsign, member identifier, or '
               'radio identifier in the box and press Enter or click <b>Look Up</b>. A USB '
               'or Bluetooth scanner feeds this same box automatically.', Bullet))
    s.append(SP(6))

    s.append(P('10.6  How the Roster Lookup Works', H2))
    s.append(P(
        'Whatever the code says -- scanned, photographed, or typed -- it is trimmed, forced '
        'to capital letters, and matched against the roster. The lookup tries these fields '
        'in order until it finds a match:'))
    s.append(SP(2))
    s.append(tbl(['ORDER', 'FIELD MATCHED', 'EXAMPLE VALUE'], [
        ['1st', 'barcode_id (the badge or card code)', 'ESV-001'],
        ['2nd', 'member_id (roster membership number)', 'ESV-001'],
        ['3rd', 'callsign (Federal Communications Commission license)', 'KE4CON'],
        ['4th', 'radio_id (tactical or unit number)', '412'],
    ], widths=[0.75*inch, CW-2.35*inch, 1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'A found member auto-fills their name, identifier, and agency, and pre-selects a '
        'suggested Incident Command System (ICS) position when the roster carries one. '
        'Nothing is filed until you click Check In, so you always get a chance to correct '
        'the details first.', 'note'))
    s.append(SP(6))

    s.append(P('10.7  The Check-In Form', H2))
    s.append(P(
        'Once a code resolves, the form appears. Only the name is required; fill in as much '
        'of the rest as you know.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Full Name *',
         'Required. The person\'s first and last name. Auto-filled for a roster member.'],
        ['Callsign / ID',
         'The person\'s amateur callsign or unit identifier, such as "KE4CON" or "Unit 412".'],
        ['Agency',
         'The organization the person represents -- their home group or a mutual-aid agency.'],
        ['ICS Position',
         'The role they are filling on this incident, chosen from the drop-down in 10.7.1. '
         'Left as "Select position..." if unknown.'],
        ['Resource Type',
         'What kind of resource they are, chosen from the drop-down in 10.7.2.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))

    s.append(P('10.7.1  ICS Position Choices', H3))
    s.append(tbl(['POSITION', 'WHO IT IS'], [
        ['Incident Commander (IC)', 'The person in overall charge of the incident.'],
        ['Safety Officer (SOFR)', 'Responsible for personnel safety.'],
        ['Operations / Planning / Logistics / Finance-Admin Section Chief',
         'The four section chiefs leading tactics, the plan, support, and cost.'],
        ['Branch Director / Division-Group Supervisor (DIVS)',
         'Mid-level supervisors under Operations.'],
        ['Net Control / Amateur Radio Operator', 'The communications-unit roles.'],
        ['Emergency Medical / Volunteer / Other',
         'Medical personnel, general volunteers, and anything not listed above.'],
    ], widths=[2.7*inch, CW-2.7*inch]))
    s.append(SP(4))

    s.append(P('10.7.2  Resource Type Choices', H3))
    s.append(tbl(['TYPE', 'MEANING'], [
        ['Personnel', 'An individual person or staffed position.'],
        ['Amateur Radio', 'A licensed amateur radio operator resource.'],
        ['Engine', 'A fire engine or similar apparatus.'],
        ['Crew', 'An organized team that works as one unit.'],
        ['Vehicle', 'Any other vehicle -- truck, bus, or boat.'],
        ['Equipment', 'Gear and supplies rather than people.'],
        ['Other', 'Anything that does not fit the categories above.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('10.8  Confirmation and Session History', H2))
    s.append(P(
        'When you click <b>Check In</b>, the record is sent to the incident and a green '
        'full-screen confirmation shows the person\'s name and the time they were logged. '
        'The check-in is now on the incident\'s ICS-211 check-in list and cannot be lost -- '
        'incident data is saved on the server and backed up. Each check-in also drops onto '
        'the <b>Recent Check-Ins This Session</b> panel, which keeps the last ten made on '
        'this device so a single operator can see who they have just processed. That panel '
        'is a convenience list for this session only; the durable record lives on the '
        'server. Click <b>Scan Next Person</b> to clear the form and carry on.'))
    s.append(SP(6))

    s.append(P('10.9  Which Devices Can Scan', H2))
    s.append(P(
        'The scanner relies on two browser features: the Barcode Detector (to read a code) '
        'and a secure context (to run the live camera). What a device can do depends on '
        'which it has.'))
    s.append(SP(4))
    s.append(tbl(['DEVICE / BROWSER', 'WHAT WORKS'], [
        ['Chrome or Edge over HTTPS (Android or desktop)',
         'Everything -- live camera, Take Photo, manual entry, and USB or Bluetooth scanners.'],
        ['Chrome or Edge over plain http',
         'Live camera is disabled; Take Photo, manual entry, and hardware scanners all work.'],
        ['Apple iOS Safari, or Firefox',
         'No code reading at all -- the scan buttons are disabled. Manual entry and a '
         'USB or Bluetooth scanner still work.'],
    ], widths=[2.7*inch, CW-2.7*inch]))
    s.append(SP(4))
    s.append(note(
        'When the browser cannot read codes, the page says so on the status line and steers '
        'you to manual entry, so a check-in station is never fully blocked -- someone can '
        'always type the identifier.', 'note'))
    s.append(SP(6))

    s.append(P('10.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Start Camera is grayed out',
         'You are on a plain http link or an unsupported browser. Use <b>Take Photo of QR</b> '
         'or manual entry, or open the page over the secure HTTPS link.'],
        ['The status line says the browser cannot read QR codes',
         'It is likely an iPhone Safari or Firefox. Type the member identifier, callsign, or '
         'radio identifier in the manual box, or use a USB or Bluetooth scanner.'],
        ['"No QR code found in that photo"',
         'Hold the phone steady, fill the frame with the code, and retake. If it still '
         'fails, type the identifier in the manual box instead.'],
        ['A member scans as "not in roster"',
         'The code did not match any barcode, member, callsign, or radio identifier. Fill in '
         'the name and agency by hand and check them in; add them to the roster later.'],
        ['The bottom badge says "No incident selected"',
         'The page is not pointed at an incident. Open it from the incident\'s ICS-211 Share '
         'URL, or select an incident on the dashboard, then reopen Scan Check-In.'],
        ['"Check-in failed" or a server error appears',
         'The device briefly lost the EMCOMM-NET link. Confirm the Wi-Fi connection and try '
         'Check In again; the form keeps your entries.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch11():
    s = chapter(11, 'Federal Communications Commission (FCC) Callsign Lookup',
                'http://192.168.50.1/callsign.html')
    s.append(P(
        'The Callsign Lookup tool puts the entire national Federal Communications Commission '
        '(FCC) amateur radio license database in your hands with no internet connection. Over '
        '800,000 active licensees are stored locally in a SQLite database on the Pi, so you '
        'can confirm a station name, verify a license class and status, or find a licensee by '
        'name or location in a fraction of a second - even when every outside network is down. '
        'The same database quietly powers the Net Control Logger, the Scan Check-In tool, and '
        'the Incident Command System (ICS) message forms, filling in names automatically as '
        'you work. This chapter covers the standalone lookup page and how the shared database '
        'is used everywhere else.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: type a callsign and press Enter to see the licensee, or use '
        'Advanced Search to find people by name, city, state, class, or grid square - all '
        'offline.', 'tip'))
    s.append(SP(6))

    s.append(P('11.1  Reading the Screen', H2))
    s.append(P(
        'You reach the tool from the top navigation bar (<b>Callsign Lookup</b>) or from the '
        'dashboard. The page has four parts, stacked top to bottom:'))
    s.append(SP(2))
    s.append(tbl(['AREA', 'WHAT IS THERE'], [
        ['Search hero (top)',
         'The <b>CALLSIGN LOOKUP</b> banner, the line "FCC Amateur Radio License Database - '
         'Offline SQLite - Updated weekly", a large callsign entry box, and the '
         '<b>Look Up</b> button.'],
        ['Result card',
         'Appears under the search box after a lookup. Shows the licensee in large type with '
         'a color-coded license-class tag, an Active or Expired status dot, and a grid of '
         'details.'],
        ['Advanced Search',
         'A panel headed <b>Advanced Search</b> for finding licensees by name, city, state, '
         'class, or grid square when you do not know the callsign. Results appear as a table '
         'below it.'],
        ['Recent Lookups',
         'A row of buttons, one per callsign you looked up recently, so you can re-check a '
         'station with one click.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('11.2  Looking Up a Single Callsign', H2))
    s += steps([
        'Click the callsign box (it shows the example <b>W8XYZ</b> until you type). Type a '
        'callsign - it is forced to capital letters automatically, so case does not matter.',
        'Press <b>Enter</b> or click <b>Look Up</b>. Results are not live-as-you-type; nothing '
        'happens until you submit.',
        'The result card scrolls into view. A match shows the callsign in large amber letters '
        'with the licensee details described in 11.3.',
        'If there is no match, the card turns red and reads "Callsign ... not found in FCC '
        'database" with a suggestion to search by name instead or to confirm the database is '
        'up to date.',
    ])
    s.append(note(
        'You can also arrive with a callsign already loaded: another page can link here with '
        '?call=W8XYZ on the end of the address, and the lookup runs on its own the moment the '
        'page opens.', 'note'))
    s.append(SP(6))

    s.append(P('11.3  Understanding the Result Card', H2))
    s.append(P(
        'A found record shows the callsign, a colored <b>license-class</b> tag, a status dot '
        '(a green dot with <b>Active</b>, or a red dot with the status word when the license '
        'is not active), and a grid of detail fields. Each field is labeled; a dash means the '
        'database has no value for it.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Name', 'The licensee - a person\'s name, or an entity/club name.'],
        ['City, State', 'The mailing city and two-letter state from the license.'],
        ['Zip Code', 'The mailing ZIP code on file.'],
        ['Country', 'The country of the license; almost always US.'],
        ['Grant Date', 'The date the current license term was granted by the FCC.'],
        ['Expiration Date', 'When the license expires. Shown in red if the date has already '
         'passed.'],
        ['FRN', 'The FCC Registration Number - the identifier that ties all of a person\'s '
         'FCC licenses together.'],
        ['License ID', 'The FCC internal license record number, used to build the online '
         'lookup link.'],
        ['Grid Square', 'The Maidenhead grid locator (for example EN80), shown only when the '
         'record has one.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P('11.3.1  License-Class Colors', H3))
    s.append(P(
        'The class tag is color-coded so you can read the privilege level at a glance:'))
    s.append(SP(2))
    s.append(tbl(['TAG', 'CLASS', 'COLOR'], [
        ['T', 'Technician', 'Green'],
        ['G', 'General', 'Amber'],
        ['E', 'Amateur Extra', 'Red'],
        ['N', 'Novice', 'Blue'],
        ['P', 'Advanced', 'Purple'],
    ], widths=[0.7*inch, 2.2*inch, CW-2.9*inch]))
    s.append(SP(6))

    s.append(P('11.4  The Result Buttons', H2))
    s.append(P(
        'Three buttons sit at the bottom of a found result card:'))
    s.append(SP(2))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['FCC ULS',
         'Opens the official FCC Universal Licensing System page for this license in a new '
         'browser tab. This is the one action that needs the internet - it reaches out to '
         'the FCC website, so it works only when a Wide Area Network (WAN) is present.'],
        ['+ Add to Roster',
         'Jumps to the Roster page with this callsign already filled in, so you can create a '
         'roster entry from the FCC record without retyping it.'],
        ['Copy',
         'Copies the callsign to the clipboard so you can paste it into a log, a form, or a '
         'message.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('11.5  Advanced Search - Finding a Licensee by Name or Place', H2))
    s.append(P(
        'When you do not have the callsign - you know the name of a person who checked in, or '
        'you want everyone with a license in a town - use the <b>Advanced Search</b> panel. '
        'Fill in any one or more fields and the tool finds every matching record (up to 100 '
        'at a time).'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Last Name / Entity Name', 'A person\'s last name, or a club or entity name.'],
        ['First Name', 'A person\'s first name.'],
        ['State', 'A drop-down of all states; leave on <b>All States</b> to search '
         'everywhere.'],
        ['License Class', 'A drop-down: <b>All Classes</b>, Technician, General, Amateur '
         'Extra, Novice, or Advanced.'],
        ['City', 'The mailing city.'],
        ['Grid Square', 'A Maidenhead grid locator (for example EN80); forced to capital '
         'letters as you type.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s += steps([
        'Type into one or more of the fields above. The more fields you fill, the narrower '
        'the result.',
        'Click <b>Search</b>. If you leave every field blank, the tool reminds you to enter '
        'at least one criterion.',
        'Matches appear in a results table below the panel, with a count such as "12 results '
        'found" shown at the right of the button row.',
        'Click <b>Clear</b> to empty all the search fields and wipe the results table so you '
        'can start a fresh search.',
    ])
    s.append(SP(6))

    s.append(P('11.6  The Search Results Table', H2))
    s.append(P(
        'Advanced Search lists its matches in a table. Each row is one licensee:'))
    s.append(SP(2))
    s.append(tbl(['COLUMN', 'WHAT IT SHOWS'], [
        ['Callsign', 'The callsign, shown in amber. Click it to run a full single-callsign '
         'lookup and see the complete result card for that station.'],
        ['Name', 'The licensee name, or the first and last name joined together.'],
        ['Class', 'A short class label - Tech, General, Extra, Novice, or Advanced.'],
        ['City', 'The mailing city.'],
        ['State', 'The two-letter state.'],
        ['Status', 'Green <b>Active</b> for a current license, red <b>Expired</b> otherwise.'],
        ['Expires', 'The license expiration date.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(4))
    s.append(note(
        'The list shows at most 100 records at once. If your search returns more than that, '
        'add another field - a state, a city, or a class - to narrow it down to the person '
        'or group you actually want.', 'tip'))
    s.append(SP(6))

    s.append(P('11.7  Recent Lookups', H2))
    s.append(P(
        'Every single-callsign lookup that finds a match is remembered on this device and '
        'shown as a button in the <b>Recent Lookups</b> row at the bottom of the page (the '
        'most recent up to twenty). Click any of those buttons to look the station up again '
        'instantly. The list is stored in this browser only, so a different tablet or laptop '
        'keeps its own recent list, and clearing the browser\'s stored data empties it.'))
    s.append(SP(6))

    s.append(P('11.8  Automatic Lookup in Other Tools', H2))
    s.append(P(
        'You rarely need to open this page by hand, because the same offline FCC database is '
        'queried automatically wherever a callsign is entered:'))
    s.append(SP(2))
    s.append(tbl(['WHERE', 'HOW IT WORKS'], [
        ['Net Control Logger',
         'When you enter a callsign in the check-in field, the name and license class fill in '
         'automatically. A red border warns you when the callsign is not found or the license '
         'has expired.'],
        ['Scan Check-In',
         'After a Quick Response (QR) code scan or a manual entry, if the value is a callsign '
         'the FCC record fills the name field (falling back to the roster if the callsign is '
         'not in the database).'],
        ['ICS-213 General Message',
         'The "From Callsign" field fills the operator name from the FCC database, so the '
         'message header is complete without extra typing.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('11.9  Keeping the Database Current', H2))
    s.append(P(
        'The FCC releases license changes constantly, so the local copy is meant to be '
        'refreshed about once a week. Updating it does not require the Pi to be online during '
        'an incident - you download the FCC data once, when you do have internet, and import '
        'it into the Pi.'))
    s += steps([
        'On a computer with internet, download the FCC Universal Licensing System (ULS) '
        'amateur database export from wireless.fcc.gov/uls.',
        'Copy the downloaded file to the Pi and run the database import script as described '
        'in the Installation Guide.',
        'The tool will then serve the newer records immediately; no restart of the whole '
        'system is needed.',
    ])
    s.append(note(
        'The banner line under the title reads "Updated weekly" as a reminder of the intended '
        'schedule. If a station you know is licensed does not appear, the local copy is most '
        'likely just older than that station\'s license - refresh it when you next have '
        'internet.', 'note'))
    s.append(SP(6))

    s.append(P('11.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['A callsign I know is valid shows "not found"',
         'The local database may be older than that license. Refresh the FCC data (11.9), or '
         'use Advanced Search by name to confirm the record exists under a different '
         'spelling.'],
        ['"Could not reach local FCC database" / API error',
         'The core Application Programming Interface (API) server on port 5050 is not '
         'responding. Confirm the fcc-lookup service is running and reload the page.'],
        ['Nothing happens when I type',
         'Lookup is not live-as-you-type. Press Enter or click Look Up to run the search.'],
        ['The FCC ULS button does nothing / shows an error',
         'That button opens the official FCC website and needs the internet. Without a WAN it '
         'cannot load; use the offline details on the result card instead.'],
        ['Advanced Search says "Enter at least one search criterion"',
         'Every field was left blank. Fill in at least one field - a name, city, state, '
         'class, or grid - then click Search.'],
        ['My Recent Lookups list is empty on another device',
         'Recent Lookups is stored per browser. A different tablet or laptop keeps its own '
         'list, and clearing browser data empties it - this is normal.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch12():
    s = chapter(12, 'Dead Man\'s Switch',
                'http://192.168.50.1/deadmans.html')
    s.append(P(
        "The Dead Man's Switch is a safety watchdog for your radio nets. It watches how "
        "long it has been since a net logged any activity, and if that quiet stretch grows "
        "past a time limit you set, it sounds an alarm and flashes a red banner across the "
        "screen. It is built for field operations - especially search and rescue - where "
        "radio silence beyond a set interval may be the first sign that a field team is in "
        "trouble. You do not have to remember to watch the clock; the page watches it for "
        "you and interrupts you the moment a net goes quiet too long.", Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: it is a countdown timer per net that raises an alarm when a net '
        'stops checking in - so a silent team never goes unnoticed.', 'tip'))
    s.append(SP(6))

    s.append(P('12.1  How It Works and the Four States', H2))
    s.append(P(
        "Every open net has its own countdown running toward a threshold - a number of "
        "minutes of allowed silence. Each time that net records activity (a check-in logged "
        "in Net Control), the countdown resets to full. If activity stops, the countdown "
        "runs down, and the net moves through four states shown by the big ring at the top "
        "of the page and by the colored badge on each net card."))
    s.append(SP(4))
    s.append(tbl(['STATE', 'WHAT IT MEANS'], [
        ['DISARMED',
         'Green. The net is not being watched right now. The ring reads <b>ALL CLEAR</b>. '
         'Nothing will alarm until you arm it.'],
        ['ARMED',
         'Amber. The net is live and being watched. The ring reads <b>MONITORING</b>. The '
         'countdown is running and activity keeps resetting it.'],
        ['WARNING',
         'Red. Silence has passed the warning mark (by default 75 percent of the '
         'threshold). This is your early heads-up that time is running out.'],
        ['TRIGGERED',
         'Red and pulsing. The full threshold elapsed with no activity. The alarm sounds '
         'and the top banner flashes <b>DEAD MAN\'S SWITCH TRIGGERED</b>.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P(
        'The top ring always shows the <b>worst</b> state across all your nets, so a single '
        'triggered net turns the whole page red even if others are calm.'))
    s.append(SP(6))

    s.append(P('12.2  Opening the Page', H2))
    s.append(P(
        'Open <b>Dead Man\'s Switch</b> from the top navigation bar, or go straight to '
        'http://192.168.50.1/deadmans.html. Best practice is to leave it open on a '
        'dedicated monitor or tablet at the Net Control position or the Emergency Operations '
        'Center (EOC) duty station, where the person watching the nets will see and hear it. '
        'Make sure that device has its speaker on and turned up - the alarm is audible.'))
    s.append(SP(4))
    s.append(note(
        'The alarm sound is produced by the browser on the device showing this page. If the '
        'screen is off, the tab is closed, or the volume is muted, no one hears it. Keep the '
        'page open and awake at a staffed position.', 'warn'))
    s.append(SP(6))

    s.append(P('12.3  Setting the Default Configuration', H2))
    s.append(P(
        'The <b>DEFAULT CONFIGURATION</b> panel near the top sets the values used for new '
        'nets you arm. Change them to suit the operation, then click <b>Save Defaults</b>. '
        'These settings are remembered on this device.'))
    s.append(SP(4))
    s.append(tbl(['SETTING', 'WHAT IT MEANS'], [
        ['Default Threshold (minutes)',
         'How many minutes of silence are allowed before a net triggers. Default 30; allowed '
         '1 to 480. Common field values are 10, 15, or 30 minutes.'],
        ['Warning at (% of threshold)',
         'How far into the countdown the amber-to-red WARNING appears, as a percentage of '
         'the threshold. Default 75; allowed 50 to 95. At a 30-minute threshold, 75 percent '
         'warns at 22.5 minutes of silence.'],
        ['Poll Interval (seconds)',
         'How often the page asks the server for fresh net activity. Default 15; allowed 5 '
         'to 60. Lower is more responsive but asks the server more often.'],
        ['Alert Sound',
         'The sound played when a net triggers: <b>Beep</b> (a softer tone), <b>Alarm</b> (a '
         'higher, more urgent tone), or <b>None (visual only)</b> - the banner still flashes '
         'but nothing sounds.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        'The countdown timers on the page tick every second on their own; the Poll Interval '
        'only controls how often the page refreshes the real activity data from the server, '
        'not how smoothly the numbers count down.', 'note'))
    s.append(SP(6))

    s.append(P('12.4  Where Monitored Nets Come From', H2))
    s.append(P(
        'The Dead Man\'s Switch does not create nets. It watches the nets you open in <b>Net '
        'Control</b> (Chapter 11). When you start a net there, it appears under <b>MONITORED '
        'NETS</b> on this page as a card. If no nets are open, the page shows "No active nets '
        'being monitored" and tells you to open a net in Net Control and arm the switch. Each '
        'net you have open gets its own card and its own independent countdown.'))
    s.append(SP(6))

    s.append(P('12.5  Reading a Net Card', H2))
    s.append(P(
        'Each net card shows that net\'s live status at a glance. The colored bar down the '
        'left edge and the badge in the corner match the four states in 12.1.'))
    s.append(SP(4))
    s.append(tbl(['CARD ELEMENT', 'WHAT IT SHOWS'], [
        ['Net name and badge',
         'The net\'s name, with a state badge (DISARMED, ARMED, WARNING, or TRIGGERED).'],
        ['Big timer',
         'The time remaining until this net triggers, counting down as minutes:seconds. It '
         'is colored to match the state.'],
        ['"remaining of N min threshold"',
         'A reminder of the total threshold this net is counting down from.'],
        ['Progress bar',
         'A bar that fills as silence grows - empty just after activity, full at trigger.'],
        ['Last activity',
         'The clock time (UTC) of the most recent logged activity on this net.'],
        ['Elapsed',
         'How many minutes have passed since that last activity.'],
        ['Warning at',
         'The minute mark and percentage at which this net moves to WARNING.'],
        ['Triggered',
         'Shown only after a trigger: the UTC time the alarm fired.'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(SP(6))

    s.append(P('12.6  Arming, Resetting, and Disarming a Net', H2))
    s.append(P(
        'The buttons at the bottom of each card change with the net\'s state. You will only '
        'ever see the buttons that make sense for what the net is doing right now.'))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHEN IT APPEARS / WHAT IT DOES'], [
        ['Arm',
         'Shown when the net is DISARMED. Starts watching the net using the current default '
         'threshold. The net turns amber (ARMED) and the countdown begins.'],
        ['Reset',
         'Shown when the net is armed, warning, or triggered. Restarts the countdown from '
         'full - use it to clear a warning or a trigger once you have confirmed the team is '
         'fine, or after any manual check-in.'],
        ['Disarm',
         'Shown when the net is armed, warning, or triggered. Stops watching the net '
         'entirely and returns it to DISARMED. You are asked to confirm first.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P('The everyday routine for a net is short:'))
    s += steps([
        'Open the net in Net Control so its card appears here.',
        'On the card, click <b>Arm</b>. The card turns amber and the countdown starts.',
        'As the net runs, each check-in logged in Net Control resets the countdown '
        'automatically - you do nothing.',
        'If a net reaches WARNING or TRIGGERED, investigate. If the team is confirmed safe, '
        'click <b>Reset</b> to restart the countdown.',
        'When the net closes, click <b>Disarm</b> and confirm.',
    ])
    s.append(SP(6))

    s.append(P('12.7  When a Net Triggers', H2))
    s.append(P(
        'A trigger is meant to be impossible to miss. When any net hits its threshold: the '
        'red <b>DEAD MAN\'S SWITCH TRIGGERED - NET INACTIVITY ALARM</b> banner appears and '
        'flashes at the top of the page, the alarm sound plays (unless Alert Sound is set to '
        'None), the top ring turns red and reads <b>TRIGGERED</b>, and the net\'s own card '
        'pulses red. Treat it as a real event until proven otherwise:'))
    s += steps([
        'Look at which net card is red - the "Triggered" line shows the time it fired.',
        'Attempt contact with the field team or net on that net immediately.',
        'If you reach them and all is well, click <b>Reset</b> on that card to silence the '
        'alarm and restart the countdown.',
        'If you cannot reach them, follow your group\'s overdue-team procedure. The alarm '
        'stays up until you Reset or Disarm the net.',
    ])
    s.append(note(
        'Reset silences the alarm and gives the net a fresh full countdown; Disarm silences '
        'it and stops watching that net altogether. Reset when the net is continuing; disarm '
        'only when the net is truly closing.', 'tip'))
    s.append(SP(6))

    s.append(P('12.8  The Activity Log', H2))
    s.append(P(
        'Below the net cards, the <b>ACTIVITY LOG</b> timeline records what happened on this '
        'page - each arm, reset, disarm, and configuration change, with a UTC time and the '
        'net it applied to. It is a quick running record of operator actions during the '
        'watch. Click <b>Clear</b> above the log to empty it. This log lives in the browser '
        'on this device for the current session; it is a convenience view, not the permanent '
        'incident record - the net check-ins themselves are saved by Net Control.'))
    s.append(SP(6))

    s.append(P('12.9  Practical Tips for the Watch', H2))
    s.append(P('<b>Match the threshold to the risk.</b> A short SAR sweep in bad terrain '
               'may warrant a 10-minute threshold; a stable shelter net can run at 30 or '
               'more.', Bullet))
    s.append(P('<b>Keep the page on a staffed, awake screen.</b> A blanked or muted device '
               'is a silent alarm.', Bullet))
    s.append(P('<b>Reset promptly after any manual check-in</b> so a routine gap does not '
               'grow into a false trigger.', Bullet))
    s.append(P('<b>Disarm nets you have closed</b> so the ring reflects only nets that are '
               'genuinely being watched.', Bullet))
    s.append(SP(6))

    s.append(P('12.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The page says "No active nets being monitored"',
         'No net is open. Open a net in Net Control (Chapter 11); it will appear here as a '
         'card, then click Arm.'],
        ['A net alarmed but the team is fine',
         'A routine gap outran the threshold. Click Reset on that card to restart the '
         'countdown, and consider a longer threshold for this operation.'],
        ['No sound when a net triggers',
         'Check that Alert Sound is not set to None, the device volume is up, and the tab is '
         'open. Some browsers need a click on the page first before they will play sound.'],
        ['The countdown does not reset on check-ins',
         'Confirm check-ins are being logged in Net Control for that net, and that the page '
         'shows "Updated" (not "Server offline") on the MONITORED NETS line.'],
        ['"Server offline" appears on the refresh line',
         'The page cannot reach the server. Confirm you are on the EMCOMM-NET Wi-Fi and can '
         'open the dashboard at 192.168.50.1; the page retries on its own once reachable.'],
        ['My default settings were not remembered',
         'Click Save Defaults after changing them. Settings are stored per device, so a '
         'different tablet or a cleared browser starts from the defaults again.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch13():
    s = chapter(13, 'Tactical Automatic Packet Reporting System (APRS) Map',
                'http://192.168.50.1/tactical.html')
    s.append(P(
        "The Tactical Map is your live picture of who and what is on the air. It is a "
        "full-screen Leaflet map that plots every Automatic Packet Reporting System "
        "(APRS) station it can hear, drawn from as many as three feeds at once: Direwolf "
        "decoding signals straight off the radio, the YAAC (Yet Another APRS Client) "
        "program, and the internet APRS-IS feed when a Wide Area Network (WAN) is "
        "available. It is the primary situational-awareness display for tracking field "
        "teams, vehicles, and mobile resources, and it doubles as a place to send and "
        "receive short APRS text messages and to drop your own labeled markers on the "
        "map.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: the Tactical Map merges every APRS source into a single live "
        "map of stations, color-coded by how recently each one was heard.", 'tip'))
    s.append(SP(6))

    s.append(note(
        "Offline caveat: the map is fully offline only when the Leaflet map library and "
        "the base map tiles are served locally from the Pi. In the current build, "
        "Leaflet and the default base tiles load from the internet (a Content Delivery "
        "Network), so without a WAN the base map may not draw. Station markers and your "
        "overlays still plot on whatever base is available. Pre-download tiles with "
        "<b>sudo bash download_tiles.sh</b> for a true no-internet map.", 'warn'))
    s.append(SP(6))

    s.append(P('13.1  Reading the Screen at a Glance', H2))
    s.append(P(
        "The screen has three parts: a thin top bar, the map itself, and a sidebar on "
        "the right. Along the top bar, left to right, you will see the home icon (returns "
        "to the dashboard), the <b>TACTICAL MAP</b> title, a live <b>Stations</b> count, "
        "a <b>Refresh</b> button that re-polls every source, a <b>KML</b> button that "
        "exports what is on the map, and a UTC clock. Down the left edge of the map is a "
        "column of layer toggle buttons. The right sidebar holds five tabs."))
    s.append(SP(4))
    s.append(tbl(['SIDEBAR TAB', 'WHAT IT SHOWS'], [
        ['Stations', 'The searchable, filterable list of every station on the map, newest first.'],
        ['Msgs', 'Received APRS text messages and a form to send one.'],
        ['Markers', 'Your own hand-placed map markers (EOC, shelter, command post, and so on).'],
        ['Sources', 'The connection status and station counts for Direwolf, YAAC, and APRS-IS.'],
        ['Settings (gear icon)', 'Your station location, source addresses, and all display options.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('13.2  The Three Data Sources', H2))
    s.append(P(
        "The map can listen to three feeds at once and merges them into one deduplicated "
        "list, so a station heard by more than one source appears only once. Open the "
        "<b>Sources</b> tab to see each feed, its address, and how many stations it is "
        "contributing right now. Each source has its own color, used for the marker "
        "border and the list badges."))
    s.append(SP(4))
    s.append(tbl(['SOURCE', 'COLOR', 'WHERE IT COMES FROM', 'NEEDS WAN?'], [
        ['Direwolf (RF)', 'Green',
         'Live APRS off the radio. Direwolf decodes it; APRS Command serves it to the '
         'map. Always available with no internet.',
         'No'],
        ['YAAC', 'Blue',
         'The YAAC program running on the network, offering its own station feed over a '
         'local port.',
         'No'],
        ['APRS-IS', 'Purple',
         'The worldwide internet APRS feed by way of the aprs.fi service.',
         'Yes'],
    ], widths=[1.2*inch, 0.8*inch, CW-3.0*inch, 1.0*inch]))
    s.append(SP(4))
    s.append(P(
        "At the bottom of the Sources tab a <b>Merged Dataset</b> box tallies the total "
        "unique stations and how many came from each source alone or from more than one. "
        "Each source panel has a <b>Poll</b> button to fetch it on demand; the YAAC "
        "panel also has <b>Open UI</b> and a <b>Setup</b> guide. To use APRS-IS, paste "
        "an aprs.fi Application Programming Interface (API) key into the key box; leave "
        "it blank to keep that feed off."))
    s.append(SP(6))

    s.append(P('13.3  Map Layer Toggles', H2))
    s.append(P(
        "The column of buttons down the left side of the map turns individual layers on "
        "and off. A lit button means the layer is showing. This lets you declutter the "
        "map, for example hiding the busy internet feed to see only what you are hearing "
        "on the radio."))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT TOGGLES'], [
        ['Direwolf', 'The green RF stations decoded off the radio.'],
        ['YAAC', 'The blue stations from the YAAC feed.'],
        ['APRS-IS', 'The purple stations from the internet feed.'],
        ['Overlays', 'Your own hand-placed markers from the Markers tab.'],
        ['My Station', 'The marker for your own location.'],
        ['Range Ring', 'A dashed distance circle around your station (radius set in Settings).'],
        ['Track', 'The movement trail of a station you chose to follow.'],
        ['Repeaters', 'The repeater database overlay, loaded from the FieldCommand server.'],
        ['SARTopo', 'An imported SARTopo / CalTopo GeoJSON overlay (see 13.9).'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('13.4  Station Markers -- Color, Symbol, and Age', H2))
    s.append(P(
        "Each station is drawn with its standard APRS symbol (a car, a house, a weather "
        "flag, and so on) or, if you prefer, a plain colored dot. Two things carry "
        "meaning: the fill color tells you how recently the station was heard, and the "
        "marker border tells you which source it came from."))
    s.append(SP(4))
    s.append(tbl(['FILL COLOR', 'MEANING'], [
        ['Green', 'Fresh -- heard within the age threshold (default 15 minutes).'],
        ['Amber', 'Aging -- heard between the threshold and four times it (about 15 to 60 minutes).'],
        ['Gray', 'Old -- not heard for more than an hour.'],
        ['Blue', 'Your own station marker.'],
        ['Magenta', 'A manual overlay marker you placed.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(4))
    s.append(P(
        "The border color repeats the source scheme: green for Direwolf, blue for YAAC, "
        "purple for APRS-IS, and white when the same station was seen by more than one "
        "source. Click any marker to open a popup listing its symbol, type, comment, "
        "speed, course, altitude, path, frequency (when reported), and when it was last "
        "heard. The popup also has a <b>Track</b> button and a <b>Message</b> button for "
        "that station."))
    s.append(SP(6))

    s.append(P('13.5  The Stations List and Filters', H2))
    s.append(P(
        "The <b>Stations</b> tab lists every station on the map, sorted with the most "
        "recently heard at the top. Type in the search box to match a callsign or "
        "comment. Two drop-downs narrow the list further:"))
    s.append(SP(4))
    s.append(tbl(['FILTER', 'CHOICES'], [
        ['Source', 'All sources, Direwolf, YAAC, or APRS-IS.'],
        ['Type', 'All types, Mobile, Fixed, Weather, Digi (digipeater), or iGate.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P(
        "Clicking a station in the list centers the map on it and opens its popup. A "
        "small colored badge on each row shows which source or sources heard it."))
    s.append(SP(6))

    s.append(P('13.6  Placing Manual Markers', H2))
    s.append(P(
        "APRS shows you what is on the air, but many important places -- the Emergency "
        "Operations Center (EOC), a shelter, a command post -- are not beaconing. Use "
        "the <b>Markers</b> tab to drop your own labeled markers on the map."))
    s += steps([
        "Open the <b>Markers</b> tab in the sidebar.",
        "Type a <b>Label</b> such as \"North Shelter\" or \"Command Post\".",
        "Choose a <b>Type</b> from the list: EOC, Shelter, Staging Area, Command Post, "
        "Medical, Repeater, Fire / Hazmat, Law Enforcement, or Custom -- each has its "
        "own icon.",
        "Set the location: either type the <b>Latitude</b> and <b>Longitude</b>, or "
        "click <b>Pick on Map</b> and then click the spot on the map (the cursor becomes "
        "a crosshair and fills in the coordinates for you).",
        "Add optional <b>Notes</b>, then click <b>+ Add Marker</b>. The marker appears at "
        "once and is listed under <b>Placed Markers</b>.",
    ])
    s.append(P(
        "Placed markers are remembered between sessions. Use <b>Clear All Markers</b> at "
        "the bottom of the tab to remove them all (it asks you to confirm first)."))
    s.append(SP(6))

    s.append(P('13.7  APRS Messages', H2))
    s.append(P(
        "The <b>Msgs</b> tab receives short APRS text messages addressed to your station "
        "and lets you send one. Received messages show the sender, the recipient, the "
        "text, and the time; unread ones are marked with a green edge. To send a message:"))
    s += steps([
        "Open the <b>Msgs</b> tab and find the <b>Send APRS Message</b> form at the bottom.",
        "Enter the destination callsign in <b>To callsign</b> (for example, a field "
        "team's radio callsign).",
        "Type your message in the text box. APRS limits a message to <b>67 characters</b>, "
        "so keep it short.",
        "Choose how to send it in the <b>Via</b> drop-down: <b>Via Direwolf</b> (over the "
        "radio) or <b>Via YAAC</b>.",
        "Click <b>Send</b>. The status line below the form confirms the result.",
    ])
    s.append(note(
        "You can also start a message from a station's map popup: click its <b>Message</b> "
        "button and the To field is filled in for you.", 'tip'))
    s.append(SP(6))

    s.append(P('13.8  Settings -- My Station, Sources, and Display', H2))
    s.append(P(
        "The gear tab holds every setting. It is grouped into three sections plus a "
        "legend. Your entries are saved in the browser, so this map remembers them the "
        "next time you open it on the same device."))
    s.append(SP(4))
    s.append(P('13.8.1  My Station', H3))
    s.append(P(
        "Enter your <b>Callsign</b>, <b>Latitude</b>, and <b>Longitude</b>. If the Pi "
        "has a Global Positioning System (GPS) fix, the map fills these in from the live "
        "position automatically. <b>Center on Station</b> jumps the map back to you."))
    s.append(SP(4))
    s.append(P('13.8.2  APRS Sources', H3))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['RF source host',
         'The address of the computer running APRS Command that serves the Direwolf '
         'stations. Use "localhost" for a Pi-side bridge, or the laptop\'s Internet '
         'Protocol (IP) address, for example 192.168.50.42.'],
        ['RF source port', 'The port that feed listens on. Default 8080.'],
        ['YAAC port', 'The port the YAAC feed listens on. Default 8082.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P('13.8.3  Display', H3))
    s.append(tbl(['OPTION', 'WHAT IT DOES'], [
        ['Auto-refresh (seconds)',
         'How often the map re-polls: 15s, 30s, 60s, 2 min, or Manual only. Use a short '
         'interval when resources are actively moving.'],
        ['Map Tiles',
         'Shows whether offline tilesets are loaded. Switch the base map with the layer '
         'control in the top-right corner of the map.'],
        ['Station age threshold (min)',
         'The number of minutes that counts as "fresh" (green). Default 15.'],
        ['Range ring radius (km)',
         'The size of the dashed distance circle around your station. Default 50 km.'],
        ['Show APRS symbols',
         'Choose emoji-style symbols or plain colored dots for less clutter.'],
        ['Station labels',
         'Show or hide the callsign text above each marker.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(6))

    s.append(P('13.9  Tracking, Range Ring, Repeaters, and SARTopo Overlays', H2))
    s.append(P(
        "Four extra layers add context beyond the live stations:"))
    s.append(P(
        "<b>Track</b> -- click <b>Track</b> in a station's popup (or the Track button on "
        "the left) to follow one station and draw its movement trail as it beacons.", Bullet))
    s.append(P(
        "<b>Range Ring</b> -- turns on a dashed circle at the radius set in Settings, so "
        "you can judge distance from your station at a glance.", Bullet))
    s.append(P(
        "<b>Repeaters</b> -- overlays the repeater database served by the FieldCommand "
        "server, handy for choosing a machine to work through.", Bullet))
    s.append(P(
        "<b>SARTopo</b> -- shows search sectors, assignments, and zones you imported "
        "from SARTopo or CalTopo. Export your map as GeoJSON, import it on the SARTopo "
        "Import page, then turn on the SARTopo layer here. The overlay stays put across "
        "refreshes until you clear it.", Bullet))
    s.append(SP(6))

    s.append(P('13.10  Exporting to KML', H2))
    s.append(P(
        "Click <b>KML</b> in the top bar to download every station currently on the map "
        "as a Keyhole Markup Language (KML) file. Open it in Google Earth or share it "
        "with another agency to hand off the tactical picture. Each placemark carries the "
        "station callsign, its comment, and which source or sources heard it."))
    s.append(SP(6))

    s.append(P('13.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The map is blank -- no base map draws',
         'You have no internet and offline tiles are not installed. Run '
         '"sudo bash download_tiles.sh" on the Pi, then reload. Station markers still '
         'plot even without a base map.'],
        ['No stations appear at all',
         'Check the Sources tab. If Direwolf shows a count of "--", confirm the RF '
         'source host and port in Settings point at the computer running APRS Command, '
         'then click Poll. With no radio traffic there is simply nothing to hear.'],
        ['The purple APRS-IS feed shows nothing',
         'APRS-IS needs the internet and an aprs.fi API key. Confirm a WAN is up and '
         'paste a valid key into the aprs.fi key box on the Sources tab.'],
        ['All my stations are gray',
         'Gray means "not heard in over an hour." Either traffic has stopped, or your '
         'device clock is wrong -- age is measured against the clock, so a bad clock '
         'ages every station. Check the UTC clock in the top bar.'],
        ['A sent message never confirms',
         'The message must go out over a live source. Make sure the Via source (Direwolf '
         'or YAAC) is connected on the Sources tab, keep the text to 67 characters, and '
         'watch the status line under the Send button for the result.'],
        ['My placed markers disappeared',
         'Markers are saved in this browser only. Opening the map on a different device '
         'or after clearing browser data starts fresh. Re-add them, and avoid clearing '
         'site data for 192.168.50.1.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch14():
    s = chapter(14, 'GPS-Tracked Resource Map',
                'http://192.168.50.1/resource_map.html')
    s.append(P(
        'The Resource Map is a live picture of where your resources actually are. It reads '
        'the same T-cards you build on the Operations board (Chapter 16) and draws each one '
        'that has a Global Positioning System (GPS) position as a color-coded pin on a map, '
        'colored to match its current status. Resources that do not have a position yet are '
        "listed in the sidebar so the Operations Section can see at a glance what still needs "
        'to be placed. You set a position three ways -- from a phone standing at the '
        'resource, by clicking the map, or by typing coordinates -- and the pin appears '
        'immediately for every operator on EMCOMM-NET.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: pick an incident, and the map shows every resource that has a GPS '
        'fix as a status-colored pin, with the un-placed ones waiting in the sidebar.', 'tip'))
    s.append(SP(6))

    s.append(P('14.1  Where the Positions Come From', H2))
    s.append(P(
        'The Resource Map does not keep its own list of resources. It draws the <b>T-cards</b> '
        'for the incident you choose -- the same resource cards created and tracked on the '
        'Operations T-card board. Each pin carries the resource name, its type, its status, '
        'its current assignment, and how many personnel it holds, all pulled straight from '
        'that card. Setting a position on this page writes the coordinates back onto the '
        'T-card, so the resource carries its last known location everywhere in the app.'))
    s.append(note(
        'A resource has to exist as a T-card before it can appear here. If a resource is '
        'missing from the map and the sidebar, add it on the Operations board first, then '
        'come back and place it.', 'note'))
    s.append(SP(6))

    s.append(P('14.2  The Top Bar', H2))
    s.append(P(
        'The controls that act on the whole map run across the top of the page:'))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Incident selector',
         'The drop-down that reads "Select incident..." until you choose one. Pick which '
         "incident's resources to show. Your choice is remembered, so the same incident "
         'loads automatically the next time you open the page.'],
        ['My Location',
         'Drops an amber marker at your own device GPS position and zooms the map to it. '
         'Handy for checking the map against a spot you can see.'],
        ['Refresh',
         'Reloads every resource position from the server right now. Use it after someone '
         'else has moved or placed a resource.'],
        ['Repeaters',
         'Toggles an overlay of amateur repeaters from the Repeater Database on and off '
         '(see 14.7). The button border turns gold while the overlay is on.'],
        ['Auto-refresh 30s',
         'A checkbox. When ticked, the map reloads positions by itself every 30 seconds -- '
         'turn it on when resources are moving and updating live.'],
        ['T-Cards / Dashboard',
         'The two links at the far right jump to the Operations T-card board and back to '
         'the main dashboard.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('14.3  Marker Colors and the Legend', H2))
    s.append(P(
        'Each positioned resource is a teardrop pin holding the first letter of its resource '
        'type, painted the color of its status. The legend in the lower-left corner of the '
        'map is your key. The status colors are:'))
    s.append(SP(4))
    s.append(tbl(['COLOR', 'STATUS IT MEANS'], [
        ['Green',  'Available -- ready to be assigned.'],
        ['Navy',   'Assigned -- working an assignment.'],
        ['Blue',   'Staging -- checked in and waiting at a staging area.'],
        ['Red',    'Out of Service -- not available (also used for En Route on the sidebar dot).'],
        ['Amber',  'En Route -- moving to an assignment (shown amber on the map pin).'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(4))
    s.append(P(
        'The legend also reminds you that an "X" means a resource has no GPS position yet, '
        'and that clicking any pin lets you edit it. Resources with no position are not '
        'drawn on the map -- they wait in the sidebar until you place them.'))
    s.append(SP(6))

    s.append(P('14.4  The Resources Sidebar', H2))
    s.append(P(
        'The panel down the right side lists every resource on the T-card board, placed or '
        'not. Its header shows a running count -- for example "3/7 have GPS" -- so you can '
        'see how much of the incident is positioned. Each row shows the resource name with a '
        'colored status dot, then a line of details, and, if it is placed, its coordinates:'))
    s.append(SP(4))
    s.append(tbl(['ROW ELEMENT', 'WHAT IT SHOWS'], [
        ['Status dot',
         'A small colored dot before the name, matching the status colors above.'],
        ['Name',
         'The resource name from its T-card.'],
        ['Details line',
         'The resource type, the status, the assignment (in italics) if one is set, and the '
         'personnel count if it is above zero, separated by dots.'],
        ['Coordinates line',
         'For a placed resource: its latitude and longitude, any location label, and the '
         'time the position was last updated.'],
        ['Left edge bar',
         'A green stripe on the left marks a resource that has a GPS position; a dim gray '
         'stripe and the words "No GPS -- click to set position" mark one that does not.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P(
        'Click any row to open the Set Position window for that resource. The <b>Set All...</b> '
        'button in the sidebar header is a reminder prompt -- it tells you to click each '
        'resource in turn, or to use the map-click method, to place them one by one.'))
    s.append(SP(6))

    s.append(P('14.5  Setting a Resource Position', H2))
    s.append(P(
        'Click a resource in the sidebar, or click an existing pin on the map and choose '
        '<b>Update Position</b> in its popup. Either opens the Set Position window, titled '
        'with the resource name. Three methods are offered, and you can mix them -- for '
        'example, use the map click to get close, then fine-tune the numbers by hand:'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'HOW TO USE IT', 'BEST FOR'], [
        ['Use Device GPS',
         'Click the <b>Use Device GPS</b> button. The browser asks permission, then fills '
         'in the latitude and longitude from this device and shows the accuracy in meters.',
         'An operator standing at the resource with a phone or tablet.'],
        ['Click Map to Place',
         'Click <b>Click Map to Place</b>. The window closes and the pointer becomes a '
         'crosshair; click the spot on the map. The window reopens with the coordinates '
         'filled in.',
         'Placing a resource by a location you can see on the map.'],
        ['Type coordinates',
         'Type the decimal <b>Latitude</b> and <b>Longitude</b> straight into the two '
         'fields (for example 42.30890 and -88.43560).',
         'A position read from a paper map, a GPS receiver, or a radio report.'],
    ], widths=[1.5*inch, CW-3.3*inch, 1.8*inch]))
    s.append(SP(4))
    s.append(P('To place a resource:'))
    s += steps([
        'Open the Set Position window by clicking the resource in the sidebar (or a pin, '
        'then <b>Update Position</b>).',
        'Fill in the coordinates using any of the three methods above.',
        'Optionally type a <b>Location Label</b> -- a plain description such as "Division '
        'Alpha staging area" that shows under the coordinates and in the pin popup.',
        'Click <b>Save Position</b>. The pin appears on the map at once and the sidebar row '
        'gains its green edge and coordinates.',
    ])
    s.append(note(
        'The app checks your numbers before saving: latitude must be between -90 and 90 and '
        'longitude between -180 and 180, and both must be real numbers. If they are not, it '
        'says "Enter valid coordinates" or "Coordinates out of range" and nothing is saved.',
        'note'))
    s.append(SP(6))

    s.append(P('14.6  Updating or Clearing a Position', H2))
    s.append(P(
        'To move a resource, open it again and set a new position the same way -- the new '
        'coordinates replace the old ones and the update time refreshes. To remove a position '
        'entirely, open the resource and click <b>Clear GPS</b>. The pin disappears from the '
        'map and the resource drops back to the un-placed list in the sidebar. The T-card '
        'itself is not deleted; only its location is cleared. The <b>Clear GPS</b> button '
        'appears only for a resource that already has a position; <b>Cancel</b> closes the '
        'window without changing anything.'))
    s.append(SP(6))

    s.append(P('14.7  The Repeater Overlay', H2))
    s.append(P(
        'Click <b>Repeaters</b> to lay the amateur repeaters from the Repeater Database over '
        'the map -- useful for planning which machine a moving resource can reach. Each '
        'repeater is a small dot, colored by its mode, with a popup that shows the output '
        'frequency, callsign, offset, tone, and town. Repeaters flagged for emergency '
        'communications are drawn in gold and their popups list the ARES, RACES, or SKYWARN '
        'tags. The dot colors are:'))
    s.append(SP(4))
    s.append(tbl(['DOT COLOR', 'REPEATER TYPE'], [
        ['Gold',   'Flagged for ARES, RACES, or SKYWARN emergency communications.'],
        ['Green',  'Standard analog FM.'],
        ['Blue',   'D-STAR digital.'],
        ['Orange', 'C4FM / System Fusion digital.'],
        ['Purple', 'Digital Mobile Radio (DMR).'],
        ['Red',    'Project 25 (P25) digital.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P(
        'Click <b>Repeaters</b> again to hide the overlay. The overlay is empty until you '
        'have imported repeater data on the Repeater Database page -- if none is loaded, the '
        'app tells you to import a RepeaterBook file first.'))
    s.append(SP(6))

    s.append(P('14.8  My Location and Auto-Refresh', H2))
    s.append(P(
        'The <b>My Location</b> button uses this device\'s own GPS to zoom the map to where '
        'you are and drop a bright amber circle labeled "Your location." It does not change '
        'any resource -- it is only for orienting yourself. Tick <b>Auto-refresh 30s</b> when '
        'an incident is moving so the map keeps itself current without your clicking '
        '<b>Refresh</b>; clear the checkbox to stop it. Because every operator reads the same '
        'server, a position one person sets shows up for everyone on the next refresh.'))
    s.append(SP(6))

    s.append(P('14.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The sidebar says "Select an incident above" and nothing loads.',
         'Choose an incident in the top-bar drop-down. The map only shows resources once an '
         'incident is selected.'],
        ['A resource I expect is not on the map or in the sidebar.',
         'It has no T-card. Add it on the Operations T-card board first, then return -- the '
         'map only lists resources that exist as T-cards.'],
        ['The Use Device GPS button does nothing or reports an error.',
         'The browser needs permission and a real location fix. Allow location access when '
         'asked, make sure the device has GPS, and try outdoors; otherwise type the '
         'coordinates by hand.'],
        ['I clicked Save Position but it refused.',
         'The coordinates were blank, not numbers, or out of range. Latitude must be -90 to '
         '90 and longitude -180 to 180. Re-enter valid decimal values and save again.'],
        ['The Repeaters overlay is empty or will not load.',
         'No repeater data is imported. Open the Repeater Database page and import a '
         'RepeaterBook file, then toggle the overlay again.'],
        ['Someone placed a resource but I do not see it.',
         'Click Refresh, or tick Auto-refresh 30s. Each device reads its own copy until it '
         'reloads from the server.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch15():
    s = chapter(15, 'Incident Command System (ICS) Platform Overview — Five-Section Structure',
                'http://192.168.50.1/incident.html')
    s.append(P(
        'The Incident Management screen is the front door to every incident FieldCommand IMS '
        'runs. From this one page you create an incident, pick its type and command details, '
        'and reach every Incident Command System (ICS) form for that incident. ICS is the '
        'standard command structure defined by the National Incident Management System '
        '(NIMS); it organizes any incident into five sections — Command, Operations, '
        'Planning, Logistics, and Finance / Administration. Everything on this page is grouped '
        'by those five sections, and every form you open writes back to the same incident '
        'record, so a change made in one section shows up everywhere else at once.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: open Incident Management, create or pick an incident, then click the '
        'ICS forms you need — all five sections work from one shared incident record.', 'tip'))
    s.append(SP(6))

    s.append(P('15.1  The Incident Management Screen', H2))
    s.append(P(
        'Open <b>Incident Management</b> from the dashboard, or browse straight to '
        '<b>http://192.168.50.1/incident.html</b> on any EMCOMM-NET device. Across the top is '
        'a dark header with an <b>ICS</b> badge, the words <b>INCIDENT MANAGEMENT</b>, a '
        '<b>+ New Incident</b> button on the right, and a <b>Dashboard</b> link back to the '
        'home page. Below the header the screen is split into two columns:'))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IT SHOWS'], [
        ['Left column (list)',
         'Two lists of incidents on this server: <b>Active Incidents</b> at the top and '
         '<b>Closed Incidents</b> below. Each incident is a clickable card.'],
        ['Right column (workspace)',
         'The workspace for the incident you have selected. Until you pick one it reads '
         '"NO INCIDENT SELECTED" with a <b>+ Create New Incident</b> button.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('15.2  The Incident List', H2))
    s.append(P(
        'Every incident card in the left column shows a colored status dot (green for active, '
        'gray for closed) and a summary line so you can find the right incident at a glance. '
        'The card carries these details:'))
    s.append(SP(4))
    s.append(tbl(['ITEM', 'WHAT IT MEANS'], [
        ['Incident name', 'The name you gave the incident, or "Unnamed Incident" if none.'],
        ['Type badge', 'The incident type, shown as a small rounded badge.'],
        ['Number', 'Your agency tracking number, shown with a "#" when one was entered.'],
        ['Period', 'The current operational period number (Period 1, Period 2, and so on).'],
        ['Started', 'The date the incident was created.'],
        ['IC', 'The Incident Commander name, when one was set.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P('Click any card to load that incident into the workspace on the right.'))
    s.append(SP(6))

    s.append(P('15.3  Creating a New Incident', H2))
    s.append(P(
        'Click <b>+ New Incident</b> (top right) or the <b>+ Create New Incident</b> button in '
        'the empty workspace. The <b>CREATE NEW INCIDENT</b> window opens.'))
    s += steps([
        'Type the <b>Incident Name</b> (required) — for example "McHenry County Winter Storm '
        "Response 2026\". If your setup saved a default name, it is filled in for you.",
        'Enter an <b>Incident Number</b> if your agency assigns one (optional), such as '
        '"2026-0142".',
        'Choose an <b>Incident Type</b> (required) from the drop-down — see the type list in '
        '15.4.',
        'Fill in <b>Jurisdiction</b> (for example "McHenry County, IL") and <b>Incident '
        'Location / Address</b> (a street address or Global Positioning System (GPS) '
        'coordinates). Jurisdiction may be pre-filled from your setup.',
        'Set the <b>Incident Commander</b> — start typing to pick a name from the roster, or '
        'type any name or callsign for someone not on the roster.',
        'Pick the <b>Operational Period Duration</b> (12 hours is the standard default; 8, 24, '
        'or 6 hours are also offered) and the <b>ICS Form Variant</b> (see 15.5).',
        'Add an <b>Initial Situation Summary</b> if you have one, then click <b>CREATE '
        'INCIDENT</b>. The incident appears in the Active list and opens in the workspace. '
        'Click <b>Cancel</b> to close without creating.',
    ])
    s.append(note(
        'Only the Incident Name and Incident Type are required. Everything else can be left '
        'blank now and filled in later with the Edit button.', 'note'))
    s.append(SP(6))

    s.append(P('15.4  Incident Types', H2))
    s.append(P(
        'The <b>Incident Type</b> drop-down groups the all-hazards types into seven '
        'categories. Pick the closest match; it sets the badge on the card and helps organize '
        'your records.'))
    s.append(SP(4))
    s.append(tbl(['CATEGORY', 'EXAMPLE TYPES'], [
        ['Natural Hazards',
         'Winter Storm, Flooding, Tornado / Severe Weather, Earthquake, Wildfire, Heat '
         'Emergency, Drought.'],
        ['Technological',
         'Hazmat / Chemical Spill, Transportation Accident, Structure Fire, Power Outage / '
         'Infrastructure, Dam Failure, Nuclear / Radiological.'],
        ['Human-Caused',
         'Mass Casualty Incident, Active Threat, Civil Disturbance, Terrorism.'],
        ['Search & Rescue',
         'Wilderness, Urban, and Water search; Missing Person (Dementia / Memory) and '
         'Missing Person (Child).'],
        ['Public Health',
         'Disease Outbreak / Pandemic, Mass Casualty (Medical), Public Health Emergency.'],
        ['Planned Events',
         'Planned Event (Public Safety), Planned Event (EMCOMM Exercise), Drill / Training '
         'Exercise.'],
        ['Other',
         'Mutual Aid Request, EOC Activation, Other / All-Hazards.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('15.5  ICS Form Variant — FEMA, USCG, or NWCG', H2))
    s.append(P(
        'Different agencies use slightly different editions of the ICS forms. The <b>ICS Form '
        'Variant</b> picker offers three pills — <b>FEMA</b> (Federal Emergency Management '
        'Agency, the all-hazards default), <b>USCG</b> (United States Coast Guard), and '
        '<b>NWCG</b> (National Wildfire Coordinating Group). Your setup default is selected '
        'automatically. The chosen variant is shown on the workspace above the forms, and you '
        'can change it later with the <b>Change</b> link there.'))
    s.append(SP(6))

    s.append(P('15.6  The Incident Workspace', H2))
    s.append(P(
        'Selecting an incident fills the right column. At the top a header repeats the '
        'incident name, its type badge, the location, jurisdiction, Incident Commander, and '
        'the start time in Coordinated Universal Time (UTC), plus the summary if one was '
        'entered. For an active incident three buttons sit at the right of this header:'))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['Next Period', 'Advances the incident to the next operational period (see 15.7).'],
        ['Edit', 'Opens the full incident editor to change any detail.'],
        ['Close Incident', 'Ends the incident and moves it to the Closed list (see 15.9).'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P('A closed incident shows the word CLOSED here instead of the buttons.'))
    s.append(SP(6))

    s.append(P('15.7  Operational Periods', H2))
    s.append(P(
        'An operational period is one planning block of an incident — often a 12-hour shift. '
        'Below the header the <b>OP</b> bar shows the current period number ("OP 1"), when it '
        'started, a <b>GENERAL INFO</b> button that opens the ICS-201 initial briefing for '
        'this period, and an <b>Export IAP</b> button that opens the Incident Action Plan '
        '(IAP) for printing.'))
    s.append(P(
        'When it is time to roll over to the next shift, click <b>Next Period</b> in the '
        'header. The <b>ADVANCE OPERATIONAL PERIOD</b> window opens with an <b>Objectives '
        'carried forward to next period</b> box. Type the objectives that continue into the '
        'new period and click <b>Advance Period</b>. The period counter increases and the new '
        'period becomes current; every ICS form now works against that new period.'))
    s.append(SP(6))

    s.append(P('15.8  The ICS Forms Navigator — Five Sections', H2))
    s.append(P(
        'The heart of the workspace is a grid of form buttons grouped under colored section '
        'dividers, one group per ICS section. Each button shows the form number (such as '
        '"ICS-202"), its plain name, and which agency variants it supports. Click a button to '
        'open that form; forms save automatically. The table below lists the forms exactly as '
        'they are grouped on the page.'))
    s.append(SP(4))
    s.append(tbl(['SECTION', 'FORMS ON THE PAGE'], [
        ['Command',
         'ICS-201 Incident Briefing, ICS-202 Incident Objectives, ICS-207 Organization '
         'Chart, ICS-208 Safety Message/Plan.'],
        ['Operations',
         'ICS-204 Assignment List, ICS-211 Check-In List, ICS-219 Resource Status '
         '(T-Cards), ICS-210 Resource Status Change.'],
        ['Planning',
         'ICS-203 Organization Assignment, ICS-209 Incident Status Summary, ICS-215 '
         'Operational Planning Worksheet, ICS-215A IAP Safety Analysis.'],
        ['Logistics',
         'ICS-205 Radio Communications Plan, ICS-205A Communications List, ICS-206 Medical '
         'Plan, ICS-213RR Resource Request.'],
        ['Finance / Admin',
         'ICS-214 Activity Log, ICS-220 Air Operations Summary, ICS-221 Demobilization '
         'Check-Out.'],
        ['Communications Unit',
         'ICS-213 General Message and ICS-309 Communications Log. ICS-309 and the ICS-211 '
         'check-in are handled through the Net Logger.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(note(
        'The section a form is grouped under on this screen is where you reach it, not '
        'always where it is developed. For example, the Communications Unit and Medical Unit '
        'sit in the Logistics service branch and develop ICS-205, 205A, 206, and 309; the '
        'Planning Section then assembles those into the IAP. See Chapter 17 for the full '
        'development-responsibility table.', 'note'))
    s.append(SP(6))

    s.append(P('15.9  Meeting Scheduler, Activity Log, Editing and Closing', H2))
    s.append(P(
        'Under the Planning section a <b>Meeting Scheduler</b> link plans meetings, agendas, '
        'required attendees, and minutes for the incident. At the bottom of the workspace the '
        '<b>ACTIVITY LOG</b> feed lists recent actions with a time, the section, and what '
        'happened, so anyone can see the incident history at a glance.'))
    s.append(P(
        'To change incident details, click <b>Edit</b> in the header — it opens the full '
        'incident editor. To end an incident, click <b>Close Incident</b>; you are asked to '
        'confirm because closing cannot be undone. A closed incident stays on the server in '
        'the Closed list as a permanent record — nothing an incident produces is thrown away.'))
    s.append(note(
        'Incident data is permanent. Every incident, form, T-card, and activity entry is '
        'saved on the server and backed up. Closing an incident archives it; it does not '
        'delete it.', 'warn'))
    s.append(SP(6))

    s.append(P('15.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The incident list shows "ICS platform offline"',
         'The ICS platform service (port 5055) is not responding. Check that the '
         'ics-platform service is running (see the Health Monitor), then reload the page.'],
        ['CREATE INCIDENT does nothing / a warning appears',
         'Incident Name and Incident Type are both required. Fill in the name and pick a '
         'type from the drop-down, then click CREATE INCIDENT again.'],
        ['I do not see my new incident in the list',
         'It may already be active but the list did not refresh — reload the page. If it was '
         'closed, look in the Closed Incidents list lower in the left column.'],
        ['The Next Period / Edit / Close buttons are missing',
         'That incident is closed; a closed incident shows the word CLOSED instead. Closed '
         'incidents are read-only records.'],
        ['The wrong form edition (FEMA vs USCG vs NWCG) is showing',
         'Click the Change link above the form buttons and enter FEMA, USCG, or NWCG to set '
         'the variant for this incident.'],
        ['The Incident Commander picker is empty',
         'The roster has no members yet, or the core API (port 5050) is unreachable. You can '
         'still type any name or callsign by hand; import the roster later.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch16():
    s = chapter(16, 'Incident Command System (ICS) Operations Section — T-Card Resource Board',
                'http://192.168.50.1/ics/operations.html')
    s.append(P(
        "The Operations page is where the Operations Section keeps track of every resource "
        "working the incident — every engine, crew, individual, helicopter, and piece of "
        "equipment — and shows at a glance what each one is doing right now. It is a digital "
        "version of the paper ICS T-card rack that hangs on the wall in a traditional command "
        "post: one card per resource, sorted into columns by status. But because it lives on "
        "the server, every operator on EMCOMM-NET sees the same board at the same time, a "
        "card can be dragged from column to column, and the board stays in step with your "
        "ICS-204 Assignment Lists. Everything you enter here is saved on the server, not just "
        "in the browser, so it survives, backs up, and shows on every device.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: this is your live resource status board — add a card for each "
        "resource, drag it to the right column as its status changes, and open a card to "
        "record who is on it.", 'tip'))
    s.append(SP(6))

    s.append(P('16.1  The Three Views', H2))
    s.append(P(
        "Across the top of the page are three tabs. They all show the same resources — just "
        "in different shapes for different jobs. Click a tab to switch views."))
    s.append(SP(4))
    s.append(tbl(['TAB', 'WHAT IT SHOWS'], [
        ['T-Card Board',
         'The everyday view. One card per resource, sorted into four status columns. Drag a '
         'card between columns to change its status.'],
        ['Resource List',
         'The same resources as a full-width table, with more columns visible at once. Good '
         'for scanning, printing, or finding one resource quickly.'],
        ['Assignments',
         'Only the resources currently set to Assigned, shown as the working ICS-204 '
         'assignment picture.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('16.2  The T-Card Board', H2))
    s.append(P(
        "The board has four columns, left to right: <b>Available</b>, <b>Staged</b>, "
        "<b>Assigned</b>, and <b>Out of Service</b>. A small count next to each column title "
        "tells you how many resources are in it. Each card shows the resource type icon and "
        "type, the resource ID, the name, its current assignment, and a personnel count when "
        "people are listed on it. A color-coded legend near the panel title reminds you which "
        "color means which status."))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['Available', 'On scene and ready to be assigned. This is the default for a new resource.'],
        ['Staged', 'Standing by at a staging area, held in reserve until needed.'],
        ['Assigned', 'Working a task now, tied to a division, group, or sector.'],
        ['Out of Service', 'Not usable right now — broken down, resting, or demobilized.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P(
        "To move a resource, click and hold its card, drag it to the target column, and let "
        "go. The card lands in the new column, its color changes to match, and the change is "
        "saved to the server for everyone. When you drag a card into <b>Assigned</b>, a small "
        "box pops up asking for the Division or Group (for example, \"Division Alpha\" or "
        "\"Group SAR\"); type it and click OK, or leave it blank. Dragging a card out of "
        "Assigned clears its division automatically."))
    s.append(note(
        "The <b>Sync from ICS-204s</b> button at the top of the board pulls resources listed "
        "on your ICS-204 Assignment Lists onto the board — creating a card for any that are "
        "missing and marking them Assigned to their division. The board also runs this sync "
        "on its own a moment after the page loads. See 16.9 for how the two-way sync works.", 'note'))
    s.append(SP(6))

    s.append(P('16.3  Adding a Resource', H2))
    s += steps([
        "Click <b>+ Add Resource</b> at the top right of the page. The Add Resource box opens.",
        "Fill in <b>Resource ID</b> — a short label such as \"E-101\". This is required.",
        "Choose a <b>Type</b> from the drop-down (see the table in 16.4). This is required.",
        "Enter a <b>Name / Description</b> — for example, \"Engine 101 - F-250 Brush Truck\". "
        "This is required.",
        "Fill in <b>Capability</b> if it helps — a free-text note such as \"Type III, 5 persons\".",
        "Set the starting <b>Status</b> (Available, Staged, Assigned, or Out of Service). "
        "Most new resources start as Available.",
        "Add an <b>Assignment / Location</b> and a <b>Contact / Callsign</b> if you know them "
        "(for example, \"Division A - Sector 3\" and a callsign or channel).",
        "Click <b>Add Resource</b>. The card appears on the board and the record is saved to "
        "the server. Click <b>Cancel</b> instead to close without saving.",
    ])
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Resource ID *', 'Required. Short unit designator, such as E-101 or Team Alpha.'],
        ['Type *', 'Required. The kind of resource, chosen from the drop-down (16.4).'],
        ['Name / Description *', 'Required. The plain-language name or description of the unit.'],
        ['Capability', 'Optional note on what the resource can do, such as type and crew size.'],
        ['Status', 'Which column the card starts in.'],
        ['Assignment / Location', 'Where the resource is or what task it has.'],
        ['Contact / Callsign', 'How to reach it on the radio — a callsign or channel.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('16.4  Resource Types', H2))
    s.append(P(
        "The <b>Type</b> drop-down offers six categories. The type sets the icon shown on the "
        "card and groups like resources together; it does not restrict what you can do with "
        "the resource."))
    s.append(SP(4))
    s.append(tbl(['TYPE', 'WHAT IT COVERS'], [
        ['Engine / Vehicle', 'A fire engine, brush truck, or any other apparatus or vehicle.'],
        ['Crew / Team', 'An organized team that works together as one unit.'],
        ['Individual', 'A single person or staffed position.'],
        ['Helicopter', 'A rotary-wing air resource.'],
        ['Equipment', 'Gear and supplies — generators, pumps, go-kits, tools.'],
        ['Other', 'Anything that does not fit the categories above.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('16.5  Opening a Resource and Changing Its Status', H2))
    s.append(P(
        "Click any card on the board (or any row in the Resource List) to open the resource "
        "detail panel. The title shows the resource ID and name, and the panel opens on the "
        "<b>INFO</b> tab. The Info tab shows the fields below and lets you edit the "
        "assignment. Along the bottom of the panel are one-click status buttons and a Delete "
        "button."))
    s.append(SP(4))
    s.append(tbl(['ITEM', 'WHAT IT MEANS'], [
        ['Type', 'The resource type and its icon.'],
        ['Status', 'The current status chip.'],
        ['Leader', 'The supervisor or crew boss for this resource.'],
        ['Contact', 'The radio callsign or channel for the resource.'],
        ['Home Agency', 'The agency or mutual-aid source the resource belongs to.'],
        ['Personnel (count)', 'How many people are listed on the resource (set on the Personnel tab).'],
        ['Assignment / Division / Sector',
         'An editable box for the current task. Type a new value and click Update Assignment.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(P('16.5.1  Two ways to change status', H3))
    s += steps([
        "Fastest way: on the board, drag the card into the column you want.",
        "From the detail panel: open the resource, then click one of the bottom buttons — "
        "<b>Available</b>, <b>Staged</b>, <b>Assigned</b>, or <b>Out of Service</b>. The "
        "panel closes and the card moves.",
        "To change the task without changing status, type into the "
        "<b>Assignment / Division / Sector</b> box and click <b>Update Assignment</b>.",
        "To remove a resource entirely, click <b>Delete</b> and confirm. This cannot be undone.",
    ])
    s.append(SP(6))

    s.append(P('16.6  The Personnel Tab', H2))
    s.append(P(
        "On a paper ICS T-card, the back lists the individual people on that resource — not "
        "just a headcount, but names, roles, and contacts. FieldCommand does the same with a "
        "<b>PERSONNEL</b> tab on the detail panel. The number in parentheses next to the tab "
        "name is the current headcount, and adding or removing a person updates the personnel "
        "count shown on the card automatically. The name field is linked to the Member Roster, "
        "so as you type, matching people appear as blue suggestion chips you can click to "
        "auto-fill."))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Name *',
         "Required. The person's full name. Type at least two letters to see roster "
         "suggestions; click a suggestion to fill the name, callsign, and agency."],
        ['ICS Position on Resource',
         "The role this person fills on this resource, chosen from the drop-down (16.7). "
         "This is their job on the resource, not their spot on the overall org chart."],
        ['Agency', 'Home agency or mutual-aid source. Auto-filled from the roster when matched.'],
        ['Contact / Callsign',
         'Radio callsign, channel, or phone for this person. Auto-filled from the roster when '
         'a licensed operator is matched.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s += steps([
        "Open a resource and click the <b>PERSONNEL</b> tab.",
        "Under <b>+ ADD PERSONNEL</b>, begin typing a name in the <b>Name</b> field. Click a "
        "blue suggestion chip to auto-fill from the roster, or just type a name by hand.",
        "Pick the <b>ICS Position on Resource</b> from the drop-down.",
        "Fill in <b>Agency</b> and <b>Contact / Callsign</b> if they did not auto-fill.",
        "Click <b>Add to Resource</b>. The person appears in the list and the count updates.",
        "To remove someone, click the remove (x) button on their row and confirm.",
    ])
    s.append(note(
        "The Personnel tab answers \"who is on this resource?\" It is separate from the "
        "ICS-211 check-in list, which answers \"who has checked into this incident?\" A "
        "mutual-aid crew might all be listed on their engine's Personnel tab while only the "
        "crew boss checks in on the ICS-211.", 'note'))
    s.append(SP(6))

    s.append(P('16.7  ICS Position on Resource — Options', H2))
    s.append(P(
        "The <b>ICS Position on Resource</b> drop-down offers the roles below, plus "
        "<b>Other</b> for anything not listed."))
    s.append(SP(4))
    s.append(tbl(['POSITION', 'PLAIN MEANING'], [
        ['Crew Boss', 'Leads a crew that works as one unit.'],
        ['Single Resource Boss', 'Supervises a single resource such as one engine.'],
        ['Division Supervisor', 'Runs a geographic division.'],
        ['Task Force Leader', 'Leads a task force of mixed resource types.'],
        ['Strike Team Leader', 'Leads a strike team of the same resource type.'],
        ['Paramedic / EMT', 'Provides emergency medical care.'],
        ['Firefighter', 'Fireground personnel.'],
        ['Emergency Radio Operator', 'A licensed operator handling radio traffic.'],
        ['Net Control', 'Runs a radio net.'],
        ['Operator / Driver / Operator / Equipment Operator', 'Runs a vehicle or a piece of equipment.'],
        ['Logistics Support', 'Provides supply, transport, or support to the resource.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(SP(6))

    s.append(P('16.8  The Resource List and Assignments Views', H2))
    s.append(P(
        "The <b>Resource List</b> tab shows every resource in one wide table. Click any row "
        "to open the same detail panel, or use the <b>Edit</b> button in the Actions column."))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT SHOWS'], [
        ['Resource ID', 'The short designator.'],
        ['Type', 'The resource type and icon.'],
        ['Name / Description', 'The plain-language name.'],
        ['Capability', 'The capability note, if any.'],
        ['Status', 'A color-coded status chip.'],
        ['Assignment', 'The current task or division.'],
        ['Contact', 'The callsign or channel.'],
        ['Actions', 'An Edit button that opens the detail panel.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(P(
        "The <b>Assignments</b> tab, titled <b>Current Assignments (ICS-204)</b>, lists only "
        "the resources set to Assigned, in Resource, Type, Assignment, and Contact columns — "
        "your at-a-glance ICS-204 picture. The <b>+ Add Assignment</b> button opens the same "
        "Add Resource box so you can add a resource without leaving this view."))
    s.append(SP(6))

    s.append(P('16.9  Keeping the Board and the ICS-204 in Sync', H2))
    s.append(P(
        "The T-Card Board and the Planning Section's ICS-204 Assignment Lists describe the "
        "same resources, so FieldCommand keeps them in step both directions. When you drag a "
        "card, the app looks for that resource on any ICS-204 for the incident and updates it "
        "— for example, writing the new division when a card goes to Assigned, or noting "
        "\"OUT OF SERVICE\" when a card goes Out of Service. Going the other way, "
        "<b>Sync from ICS-204s</b> reads the assignment lists and brings those resources onto "
        "the board, creating a card for any that are not there yet. Because ICS-211 "
        "self check-ins also land in the same resource store, a person who checks in can show "
        "up here automatically."))
    s.append(note(
        "The board keeps a local copy in the browser so it paints instantly, then refreshes "
        "from the server, which is the authoritative record. If you are briefly offline, the "
        "board still shows the last known picture and syncs again when the connection returns.", 'tip'))
    s.append(SP(6))

    s.append(P('16.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['A card will not drag',
         'Click and hold directly on the card body, then drag. A single quick click opens the '
         'detail panel instead — that is normal.'],
        ['I clicked Add Resource but nothing was saved',
         'Resource ID, Type, and Name / Description are required. Fill all three, then click '
         'Add Resource again.'],
        ['Sync from ICS-204s did nothing',
         'The sync needs a selected incident and at least one ICS-204 with resources listed. '
         'Confirm an incident is selected and that Planning has built a 204 first.'],
        ['A resource shows on the board that I did not add',
         'It was pulled in by the ICS-204 sync or an ICS-211 self check-in. Open it to see its '
         'details, or delete it if it does not belong.'],
        ['The personnel count on the card looks wrong',
         'Open the resource, click the Personnel tab to reload the real list, then close it — '
         'the card count refreshes from the server.'],
        ['My changes are not showing on another operator\'s screen',
         'Each device refreshes from the server on load and after a change. Have them reload '
         'the Operations page; if it still lags, check that the ICS platform service (port '
         '5055) is running from the Health page.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch17():
    s = chapter(17, 'Incident Command System (ICS) Planning Section & Incident Action Plan (IAP) Assembly',
                'http://192.168.50.1/iap.html')
    s.append(P(
        "The Incident Action Plan (IAP) is the written work plan for one operational period - "
        "the block of time (often 12 hours) that one shift of responders works to a single set "
        "of goals. It is the Planning Section's job to assemble it. The IAP Assembly page pulls "
        "together the Incident Command System (ICS) forms your team has filled out, lets you "
        "choose which ones belong in the package, shows you at a glance how complete the plan is, "
        "and turns the whole thing into a printed plan or a portable file you can carry off-site. "
        "You do not build a form here - you build the finished plan out of forms.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: this page is the assembly line - tick the forms you want, watch the "
        "completeness meter, then Print or Save the plan for the next shift.", 'tip'))
    s.append(SP(6))

    s.append(P('17.1  The Assembly Screen at a Glance', H2))
    s.append(P(
        "Open the page and the dark blue header across the top reads INCIDENT ACTION PLAN - "
        "ASSEMBLY, with the current incident name shown beside it (or \"No incident selected\" "
        "if you have not chosen one). The rest of the screen is split into two columns."))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IS THERE'], [
        ['Header buttons (top right)',
         'Four controls: Print IAP, Save as PDF, Save as HTML, and an Incident link that '
         'returns you to the incident page. These act on the whole plan.'],
        ['Left column',
         'The IAP Form Checklist for the chosen operational period - one card per ICS form, '
         'with a checkbox, the form number and title, its ICS section, and its status.'],
        ['Right column',
         'A live IAP Cover Page preview, the IAP OPTIONS box (operational period and form '
         'variant), the COMPLETENESS meter, and a QUICK LINKS list of the first forms.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('17.2  The IAP Form Checklist', H2))
    s.append(P(
        "The left column lists every ICS form FieldCommand knows how to place in an IAP, in "
        "assembly order. Each row shows the form number (for example ICS-205), its plain title, "
        "and the ICS section that owns it - color coded so you can scan by section. The six forms "
        "marked Required are pre-checked because a complete IAP is not valid without them. The "
        "table below is the full set the page carries."))
    s.append(SP(4))
    s.append(tbl(['FORM', 'TITLE', 'SECTION', 'REQUIRED?'], [
        ['ICS-201',  'Incident Briefing',                'Command',    'Yes'],
        ['ICS-202',  'Incident Objectives',              'Command',    'Yes'],
        ['ICS-203',  'Organization Assignment List',     'Planning',   'Yes'],
        ['ICS-204',  'Assignment List',                  'Operations', 'Yes'],
        ['ICS-205',  'Radio Communications Plan',        'Logistics',  'Yes'],
        ['ICS-205A', 'Communications List',              'Logistics',  'No'],
        ['ICS-206',  'Medical Plan',                     'Logistics',  'Yes'],
        ['ICS-207',  'Organization Chart',               'Command',    'No'],
        ['ICS-208',  'Safety Message / Plan',            'Command',    'No'],
        ['ICS-209',  'Incident Status Summary',          'Planning',   'No'],
        ['ICS-213RR','Resource Request',                 'Logistics',  'No'],
        ['ICS-214',  'Activity Log',                     'All',        'No'],
        ['ICS-215',  'Operational Planning Worksheet',   'Planning',   'No'],
        ['ICS-215A', 'IAP Safety Analysis',              'Command',    'No'],
        ['ICS-210',  'Resource Status Change',           'Planning',   'No'],
        ['ICS-211',  'Incident Check-In List',           'Command',    'No'],
        ['ICS-213',  'General Message',                  'All',        'No'],
        ['ICS-216',  'Radio Requirements Worksheet',     'Logistics',  'No'],
        ['ICS-217A', 'Comms Resources Available',        'Logistics',  'No'],
        ['ICS-218',  'Support Vehicle / Equip Inventory','Logistics',  'No'],
        ['ICS-219',  'Resource Status Cards (T-Board)',  'Planning',   'No'],
        ['ICS-220',  'Air Operations Summary',           'Operations', 'No'],
        ['ICS-223',  'Wildlife Protection Measures',     'Planning',   'No'],
        ['ICS-224',  'Crew Performance Rating',          'Finance',    'No'],
        ['ICS-225',  'Personnel Performance Rating',     'Finance',    'No'],
        ['ICS-226',  'Work Capacity Test Record',        'Finance',    'No'],
        ['ICS-233',  'Open Action Tracker',              'Planning',   'No'],
        ['ICS-234',  'Work Analysis Matrix',             'Planning',   'No'],
    ], widths=[0.85*inch, 2.75*inch, 0.95*inch, CW-4.55*inch]))
    s.append(SP(6))

    s.append(P('17.3  Reading a Form Card', H2))
    s.append(P(
        "Every card carries a colored status pill on the right that tells you whether the form is "
        "ready. The status is read live from the server for the operational period you have "
        "selected, so it changes the moment someone saves that form."))
    s.append(SP(4))
    s.append(tbl(['STATUS PILL', 'WHAT IT MEANS'], [
        ['Saved (green)',
         'The form has been filled in and saved for this incident and period. It is ready to '
         'include in the IAP.'],
        ['Required - not yet saved (red)',
         'This is one of the six required forms and it has no saved content yet. The plan is not '
         'complete until it is filled in.'],
        ['Not started (amber)',
         'An optional form that has not been saved. Include it only if the incident needs it.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(SP(4))
    s.append(P(
        "At the far right of each card is an Open link (or Edit, if the form is already saved). "
        "Clicking it leaves this page and opens that ICS form in the form editor, carrying the "
        "same incident and period along so you land in the right place. Fill the form in there, "
        "including any Prepared By or Approved By signature, then return to this page - the card "
        "updates to Saved."))
    s.append(SP(6))

    s.append(P('17.4  Choosing Which Forms to Include', H2))
    s.append(P(
        "The checkbox on the left of each card, and the card itself, control whether the form "
        "goes into the plan. Clicking anywhere on a card toggles it."))
    s.append(SP(4))
    s += steps([
        "Make sure the correct operational period is chosen in the IAP OPTIONS box (see 17.6) - "
        "the checklist and every status pill follow that choice.",
        "Leave the six Required forms checked. They are pre-selected for you.",
        "Click any optional card to add it to the plan. A checked card turns green to show it is "
        "included; click again to remove it.",
        "A typical amateur or public-service IAP includes ICS-202, 203, 204, 205, 205A, 206, 207, "
        "and 208 - objectives, organization, assignments, comms plan, comms list, medical plan, "
        "org chart, and safety message.",
    ])
    s.append(note(
        "You can include a form that is not yet saved, but it will be blank in the finished plan. "
        "The completeness meter is your guard against printing an empty required form.", 'warn'))
    s.append(SP(6))

    s.append(P('17.5  The Cover Page Preview', H2))
    s.append(P(
        "The IAP Cover Page box at the top of the right column shows exactly what the front page "
        "of your plan will look like, built from your organization settings and the active "
        "incident. It updates by itself - there is nothing to fill in here."))
    s.append(SP(4))
    s.append(tbl(['COVER LINE', 'WHERE IT COMES FROM'], [
        ['Logo',                 'Your organization logo, if one was uploaded in Settings.'],
        ['Organization name',    'The short organization name or callsign from your configuration.'],
        ['Incident name',        'The name of the active incident.'],
        ['Operational Period',   'The period number chosen in the IAP OPTIONS box.'],
        ['Incident Commander',   "The Incident Commander recorded on the incident (a dash if none is set)."],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('17.6  IAP Options - Period and Form Variant', H2))
    s.append(P(
        "The IAP OPTIONS box holds two dropdowns that shape the whole plan."))
    s.append(SP(4))
    s.append(tbl(['OPTION', 'WHAT IT DOES'], [
        ['Operational Period',
         'Choose Period 1 through 5. Changing it reloads the checklist and every status pill for '
         'that period, and updates the cover page. Each period is its own set of saved forms.'],
        ['ICS Form Variant',
         'FEMA, USCG (United States Coast Guard), or NWCG (National Wildfire Coordinating Group). '
         'This tags the plan for the form family your agency uses; the label prints on the cover '
         'and contents pages. For most all-hazards use, leave it on FEMA.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('17.7  The Completeness Meter and Quick Links', H2))
    s.append(P(
        "The COMPLETENESS box shows a colored bar and a line of text such as \"4 of 6 required "
        "forms saved (67% complete)\". The bar is red below 60 percent, amber up to 99 percent, "
        "and green only when all six required forms are saved. Use it as your go / no-go check "
        "before you print: if it is not green, a required form is still blank."))
    s.append(P(
        "Below it, the QUICK LINKS box lists the first several forms with a green check when saved "
        "or a dash when not, each a one-click shortcut into that form's editor - a fast way to "
        "jump to the forms most plans start with.", Body))
    s.append(SP(6))

    s.append(P('17.8  Exporting the Finished IAP', H2))
    s.append(P(
        "The three header buttons turn your selected forms into the finished plan. Choose by "
        "where the plan needs to go and whether a printer is on hand."))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHEN TO USE IT', 'WHAT HAPPENS'], [
        ['Print IAP',
         'A printer is on EMCOMM-NET or attached to your device.',
         'Opens a print-ready cover page, a contents table, and links to every included form in a '
         'new browser tab, then opens the print dialog. Allow pop-ups if nothing appears.'],
        ['Save as PDF (recommended)',
         'No printer on site, or the plan must go off-site, to the Emergency Operations Center '
         '(EOC), or into the archive.',
         'Sends your form list to the FieldCommand server, which builds a proper 8.5 by 11 inch '
         'Portable Document Format (PDF) and downloads it as '
         '<font face="Courier">IAP_[Incident]_Period[N]_[Date].pdf</font>. Opens on any device.'],
        ['Save as HTML (fallback)',
         'The server is unreachable, or you want a lightweight file with no server call.',
         'Downloads a self-contained web-page file straight from the browser. Open it and use '
         'File - Print. Page breaks can vary by browser, so prefer PDF when layout matters.'],
    ], widths=[1.35*inch, 1.95*inch, CW-3.3*inch]))
    s.append(SP(4))
    s += steps([
        "Confirm the operational period, the form variant, and your checked forms.",
        "Watch the completeness meter turn green before you commit the plan.",
        "To print now, click <b>Print IAP</b>, then pick the site printer in the dialog.",
        "To carry the plan off-site, click <b>Save as PDF</b>. The button shows Generating while "
        "the Pi builds it (a few seconds), then the PDF downloads on its own.",
        "Only if the PDF button fails, click <b>Save as HTML</b> and print that file from any "
        "browser with File - Print.",
    ])
    s.append(note(
        "The PDF is built on the Pi and downloads to whatever device you are on - the printer does "
        "not have to be attached to that device. The file is self-contained and can be printed "
        "anywhere later. For the full compiler with embedded signatures and section dividers, use "
        "the IAP Compile page (iap_compile.html).", 'note'))
    s.append(SP(6))

    s.append(P('17.9  Doctrine Note - Forms That Cross Section Lines', H2))
    s.append(P(
        "The checklist colors ICS-205, ICS-205A, and ICS-206 as Logistics forms, which surprises "
        "some operators because they appear in the IAP that Planning assembles. That is correct "
        "ICS doctrine: the forms are developed in Logistics but distributed through Planning. "
        "Knowing this tells you who to ask when one needs fixing."))
    s.append(SP(4))
    s.append(tbl(['FORM', 'WHO DEVELOPS IT'], [
        ['ICS-205 Radio Comms Plan',
         "Developed by the Communications Unit Leader (COML) under Logistics, then handed to "
         "Planning for the IAP. To correct it, go to the COML - not the Planning Section Chief."],
        ['ICS-205A Comms List',
         'Also developed by the COML under Logistics. A supplemental contact directory, usually '
         'attached to the IAP.'],
        ['ICS-206 Medical Plan',
         "Developed by the Medical Unit Leader (MEDL) under Logistics. The Safety Officer must "
         "review and concur before it is finalized."],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('17.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Header reads "No incident selected" and every card is blank.',
         'You opened the page without an active incident. Go back through the Incident link, '
         'select or start an incident, then open IAP Assembly again so the incident id is passed.'],
        ['A form you saved still shows "Not started" or "Required - not yet saved".',
         'Check the Operational Period dropdown - status is per period. Set it to the period you '
         'saved the form in. If still wrong, reopen the form, confirm it saved, and reload.'],
        ['Completeness meter will not turn green.',
         'One of the six required forms (ICS-201, 202, 203, 204, 205, 206) is still blank. Find '
         'the red pill in the checklist, click Open, fill and save that form, then return.'],
        ['Print IAP does nothing / no new tab appears.',
         'The browser blocked the pop-up. Allow pop-ups for this site and click Print IAP again, '
         'or use Save as PDF, which needs no pop-up.'],
        ['Save as PDF shows an error or stays on "Generating".',
         'The Pi server did not answer. Confirm you are on EMCOMM-NET and the Pi is running, then '
         'retry. As a stopgap, use Save as HTML and print that file from a browser.'],
        ['The PDF opens but a form page is empty.',
         'That form was included while unsaved. Uncheck it, or open it, add its content and save, '
         'then export the IAP again.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(PB())
    return s


def ch18():
    s = chapter(18, 'Federal Emergency Management Agency (FEMA) Public Assistance (PA) Cost Documentation',
                'http://192.168.50.1/fema_costs.html')
    s.append(P(
        'When a disaster is federally declared, the Federal Emergency Management Agency (FEMA) '
        'can reimburse eligible response costs through its Public Assistance (PA) program. But '
        'FEMA only pays for costs you can prove -- who worked, what equipment ran, what you '
        'bought, at what rate, on what dates, tied to this disaster. The FEMA PA Cost '
        'Documentation screen is where you capture all of that while the incident is happening, '
        'so the paperwork is already built when the reimbursement claim comes due. It records '
        'the three cost buckets FEMA recognizes -- Force Account Labor (your own people), Force '
        'Account Equipment (your own vehicles and gear), and Materials and Contracts -- adds up '
        'the eligible total, and produces a Project Worksheet summary you hand to your state '
        'emergency management agency.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: log your labor, equipment, and purchases here as the incident runs, '
        'and the app tallies the FEMA-eligible total and exports a Project Worksheet summary '
        'for you.', 'tip'))
    s.append(SP(6))

    s.append(P('18.1  Opening the Screen and Picking an Incident', H2))
    s.append(P(
        'Open <b>FEMA PA Cost Documentation</b> from the dashboard. Everything on this page is '
        'tied to one incident, so the first thing to do is choose it. At the top right of the '
        'page header is the <b>Select incident...</b> drop-down. Pick your incident from the '
        'list; the page then loads that incident\'s labor, equipment, and material entries and '
        'fills the totals bar. Your choice is remembered, so the next time you open the page the '
        'same incident is already selected.'))
    s.append(SP(4))
    s.append(note(
        'If the drop-down still says "Select incident..." and the tables read "No entries," you '
        'have not chosen an incident yet -- nothing will save until you do. Create the incident '
        'first (Chapter 8) if it is not in the list.', 'warn'))
    s.append(SP(6))

    s.append(P('18.2  Reading the Totals Bar', H2))
    s.append(P(
        'Directly under the header is the totals bar -- four running numbers that update the '
        'instant you add, edit, or delete an entry. This is your at-a-glance picture of how much '
        'the incident has cost so far in FEMA-eligible terms.'))
    s.append(SP(4))
    s.append(tbl(['TOTAL', 'WHAT IT COUNTS'], [
        ['Force Acct Labor', 'The sum of every labor entry, hours times rate, with fringe '
         'benefits added in.'],
        ['Force Acct Equipment', 'The sum of every equipment entry, hours times the FEMA hourly '
         'rate.'],
        ['Materials / Contracts', 'The sum of every material, supply, contract, and rental '
         'entry.'],
        ['Total Eligible Costs', 'All three buckets added together -- the headline number, shown '
         'in green, set off by a divider on the right.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        'A small reminder printed beside the totals says to review every entry with your Finance '
        'Section Chief before submission. If the loaded FEMA equipment rates are more than a year '
        'old, an amber reminder banner appears above the tabs with a <b>Review Rates</b> link '
        'that jumps to the FEMA Equipment Rates page (Chapter 19).'))
    s.append(SP(6))

    s.append(P('18.3  The Four Tabs', H2))
    s.append(P(
        'The work is split across four tabs, chosen with the row of tab labels below the totals '
        'bar. Click a tab to switch views; the totals bar stays visible the whole time.'))
    s.append(SP(4))
    s.append(tbl(['TAB', 'WHAT YOU DO THERE'], [
        ['Force Account Labor', 'Log hours for your own employees and volunteers.'],
        ['Force Account Equipment', 'Log hours for your own vehicles and equipment at FEMA '
         'rates.'],
        ['Materials / Contracts', 'Log purchases, supplies, rentals, and contracted work.'],
        ['Project Worksheet', 'Enter the applicant and disaster details and review the eligible '
         'cost summary.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('18.4  Force Account Labor', H2))
    s.append(P(
        '"Force account" means your own personnel -- not a contractor. FEMA generally reimburses '
        '<b>overtime</b> for your regular employees and, depending on your state\'s policy, may '
        'reimburse volunteer time. On this tab, click <b>+ Add Labor Entry</b> to open the labor '
        'form. Each field maps to what FEMA wants on the record.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Employee Name', 'Required. The person\'s name, entered "Last, First."'],
        ['Position / Title', 'Their job title or ICS position, such as "Emergency Manager."'],
        ['Department', 'The agency or unit they belong to, such as "McHenry County OEM."'],
        ['Date Worked', 'The calendar day these hours were worked.'],
        ['Regular Hours', 'Straight-time hours worked on the incident.'],
        ['Overtime Hours', 'Overtime hours -- the primary FEMA-reimbursable category for paid '
         'staff.'],
        ['Regular Rate ($/hr)', 'The straight-time hourly wage from payroll.'],
        ['OT Rate ($/hr)', 'The overtime hourly wage.'],
        ['Fringe Benefits %', 'Fringe (taxes, insurance, retirement) as a percentage of wages. '
         'Defaults to 30. FEMA requires fringe be documented.'],
        ['Preview Total', 'Calculated live as you type -- (reg hrs x reg rate + OT hrs x OT rate) '
         'x (1 + fringe%).'],
        ['Notes', 'Free text -- the assignment, EOC watch, or any justification.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s += steps([
        'Click <b>+ Add Labor Entry</b>.',
        'Fill in the name (required), position, department, and date.',
        'Enter regular and overtime hours and their rates. Watch the <b>Preview Total</b> update.',
        'Adjust <b>Fringe Benefits %</b> if your rate differs from the 30 default.',
        'Click <b>SAVE</b>. The entry appears in the labor table and the totals bar jumps.',
    ])
    s.append(SP(4))
    s.append(P(
        'The saved rows show as a table with columns Employee, Position / Title, Dept, Date, Reg '
        'Hrs, OT Hrs, Reg Rate, OT Rate, Fringe %, Labor Cost, Total w/Fringe, and Notes. Click '
        'the pencil (edit) button at the end of any row to reopen that entry; from the edit form '
        'you can change any field and click <b>SAVE</b>, or click <b>Delete</b> to remove it.'))
    s.append(SP(6))

    s.append(P('18.4.1  Importing from ICS-214', H3))
    s.append(P(
        'Rather than retype names, click <b>Import from ICS-214</b>. FieldCommand reads the '
        'completed ICS-214 Activity Logs for the selected incident and creates a labor entry for '
        'each unit leader, tagged with the operational period it came from. The imported rows '
        'come in with placeholder hours and a zero rate -- you must open each one and fill in the '
        'real hours and pay rates. A message tells you how many leaders were imported.'))
    s.append(SP(6))

    s.append(P('18.5  Force Account Equipment', H2))
    s.append(P(
        'This tab logs your own equipment -- trucks, generators, pumps, chainsaws -- at the '
        'hourly rates published in the FEMA Schedule of Equipment Rates. Click <b>+ Add Equipment '
        'Entry</b> to open the form.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Equipment Type', 'Required. What it is, such as "Pickup Truck (< 1 Ton)."'],
        ['Agency Unit ID', 'Your own identifier for the unit, such as "E-412" or "Unit 7."'],
        ['FEMA Schedule Code', 'The code from the FEMA rate schedule (for example 2-7-1).'],
        ['Date Used', 'The day the equipment ran on the incident.'],
        ['Hours Used', 'How many hours it operated.'],
        ['FEMA Rate ($/hr)', 'The eligible hourly rate. Type it, or click <b>Lookup</b> to pick '
         'from the loaded schedule.'],
        ['Operator Name', 'Who ran it, if the operator is tracked separately from labor.'],
        ['Preview Total', 'Calculated live -- hours x rate.'],
        ['Notes', 'Mileage, fuel, or purpose.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        'The <b>Lookup</b> button opens the <b>FEMA Equipment Rate Lookup</b> picker. Type in the '
        'search box to filter by equipment name, code, or category; each row shows the equipment, '
        'its rate, and its unit. Click <b>Use</b> on a row to drop that rate into the form (and '
        'the description and code, if those fields are empty). A <b>Manage rates</b> link in the '
        'picker opens the FEMA Equipment Rates page for editing the schedule itself. The saved '
        'equipment table lists Equipment, Unit ID, FEMA Code, Date, Hours, Rate/Hr, Operator, '
        'Total, and Notes, each row with a pencil (edit) button.'))
    s.append(SP(6))

    s.append(P('18.6  Materials and Contracts', H2))
    s.append(P(
        'This tab captures anything you bought or contracted for the incident. Click <b>+ Add '
        'Material / Contract</b> to open the form.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Description', 'Required. What it is, such as "Barricades, traffic cones, sandbags."'],
        ['Category', 'One of Materials, Supplies, Contracts, Rental, or Other.'],
        ['Vendor / Contractor', 'Who you bought it from or who did the work.'],
        ['Purchase / Invoice Date', 'The date on the receipt or invoice.'],
        ['Quantity', 'How many units. Defaults to 1.'],
        ['Unit', 'The unit of measure -- each, ton, cubic yard, hour.'],
        ['Unit Cost ($)', 'The price per unit.'],
        ['Total Cost', 'Calculated live -- quantity x unit cost.'],
        ['PO / Contract #', 'The purchase order or contract number, such as "PO-2026-001."'],
        ['Notes', 'Receipt number or justification.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        'Attach or keep the purchase order, invoice, and receipt for every material entry. FEMA '
        'requires source documentation for each purchase; the note field and PO number here are '
        'your pointer back to the paper.', 'note'))
    s.append(SP(4))
    s.append(P(
        'The saved table shows Description, Category (as a colored tag), Vendor, Date, Qty, Unit, '
        'Unit Cost, Total, PO #, and Notes, each row with a pencil (edit) button for changes or '
        'deletion.'))
    s.append(SP(6))

    s.append(P('18.7  The Project Worksheet Tab', H2))
    s.append(P(
        'The Project Worksheet (PW) is FEMA Form FF-104-FY-21-112 -- the form your state emergency '
        'management agency uses to package a reimbursement. This tab does not replace the official '
        'form; it gathers the header details and rolls up the costs so preparing the real PW is '
        'straightforward. Fill in the top fields, and the cost summary below fills itself from the '
        'entries you made on the other tabs.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Applicant Name', 'The organization claiming the costs.'],
        ['Disaster / Declaration Number', 'The FEMA disaster number, in the form FEMA-DR-XXXX-IL.'],
        ['Incident Name', 'Auto-filled from the selected incident; editable.'],
        ['Work Category', 'One of FEMA\'s categories A through G (Debris Removal, Emergency '
         'Protective Measures, Roads and Bridges, Water Control Facilities, Buildings and '
         'Equipment, Utilities, or Parks/Recreational/Other).'],
        ['Work Description / Scope', 'A plain-language description of the work performed, the '
         'facilities affected, and why it was necessary.'],
        ['Work Start Date / Work End Date', 'The span of the work being claimed.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(P(
        'Below the header is the <b>Eligible Cost Summary</b> -- Force Account Labor, Force '
        'Account Equipment, Materials and Contracts, and the green <b>Total Eligible Project '
        'Cost</b>. These mirror the totals bar and cannot be typed over; change a cost by editing '
        'the underlying entry on its tab. An amber notice at the bottom repeats the rules: this '
        'summary does not replace the official form, all costs must go through your state agency '
        'with supporting documentation, and costs must be tied to the disaster and not covered by '
        'insurance.'))
    s.append(SP(6))

    s.append(P('18.8  Exporting the Project Worksheet Summary', H2))
    s.append(P(
        'When you are ready to hand off the numbers, click the <b>Export PW</b> button in the page '
        'header. FieldCommand builds a plain-text file and downloads it. The file leads with the '
        'applicant, disaster number, incident, category, and work period, then the scope of work, '
        'then a cost summary, then line-by-line detail for every labor, equipment, and material '
        'entry, and closes with a generated timestamp and a reminder to submit through your state '
        'agency. Open it in any text editor or spreadsheet, or paste it into the FEMA Grants '
        'Portal.'))
    s.append(SP(4))
    s.append(note(
        'The export reflects whatever is on screen at that moment. If the header fields are blank, '
        'the file shows placeholders like "[Enter DR number]" -- fill the Project Worksheet tab '
        'first so the export is complete.', 'warn'))
    s.append(SP(6))

    s.append(P('18.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Tables all say "No entries" and nothing saves',
         'No incident is selected. Choose one from the "Select incident..." drop-down at the top '
         'right first; every entry is tied to an incident.'],
        ['"Import from ICS-214" says "Select an incident first"',
         'Pick the incident in the header drop-down, then click Import again. Import only works on '
         'the selected incident\'s ICS-214 logs.'],
        ['Imported labor rows show 8 hours and a $0 rate',
         'That is expected -- the import brings in unit leaders as placeholders. Open each row with '
         'the pencil button and enter the real hours and pay rates.'],
        ['An amber banner warns the FEMA rates are outdated',
         'The loaded equipment schedule is over a year old. Click "Review Rates" (or "Manage '
         'rates" in the Lookup picker) to update the schedule on the FEMA Equipment Rates page '
         '(Chapter 19).'],
        ['Preview Total or the cost summary stays $0.00',
         'A rate or hours field is blank or zero. Labor needs hours and a rate; equipment needs '
         'hours and a FEMA rate; materials need quantity and unit cost.'],
        ['The exported file shows "[Enter DR number]" or other placeholders',
         'Those header fields were empty at export time. Fill in the Project Worksheet tab '
         '(applicant, disaster number, category, scope) and export again.'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(PB())
    return s

