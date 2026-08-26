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
        'The FEMA Equipment Rate Schedule page holds the list of dollar figures FieldCommand '
        'uses to put a price on your own equipment when you document the cost of an incident. '
        'When the Federal Emergency Management Agency (FEMA) reimburses a disaster, it does '
        'not pay whatever you ask for a piece of equipment you already own -- it pays a set '
        'published rate for each type of machine, per hour or per day it was used. Those '
        'published figures are the <b>Schedule of Equipment Rates</b>, and this page is your '
        'local copy of them. FieldCommand ships with the standard set of about 44 equipment '
        'categories already loaded from the 2025 schedule, so cost documentation works the '
        'day you turn the app on. This chapter shows you how to read the rates, search them, '
        'correct one, add a rate FEMA does not list, and roll the whole schedule forward when '
        'FEMA publishes a new year.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: this page is the price list for applicant-owned equipment -- the '
        'per-hour or per-day figures the FEMA Force Account Equipment costs are calculated '
        'from. It covers equipment only; personnel labor is priced separately.', 'tip'))
    s.append(SP(4))
    s.append(note(
        'These rates cover <b>equipment only</b>. Labor -- the pay and fringe for the people '
        'operating the equipment -- is tracked as a separate cost and is not included in any '
        'figure on this page. The page header says so directly: "Labor NOT included."', 'warn'))
    s.append(SP(6))

    s.append(P('19.1  Opening the Page and Reading the Header', H2))
    s.append(P(
        'Open <b>FEMA Equipment Rates</b> from the Finance section of the dashboard. The blue '
        '<b>FEMA</b> badge and the title <b>FEMA Equipment Rate Schedule</b> sit across the '
        'top, with the reminder line "Eligible reimbursement rates for applicant-owned '
        'equipment - Labor NOT included" beneath them. On the right of that header bar are '
        'three controls you will use throughout this chapter.'))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Update Rate Year (calendar button)',
         'Opens the Update FEMA Rate Year window. Use it once a year, after FEMA publishes a '
         'new schedule, to stamp the new year onto every rate (see 19.8).'],
        ['+ Add Custom Rate',
         'Opens a blank Add Custom Rate window so you can add a piece of equipment the '
         'standard schedule does not list (see 19.6).'],
        ['FEMA Costs (back link)',
         'Returns you to the FEMA Cost Documentation page, where the rates on this page are '
         'actually put to work costing an incident.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('19.2  The Rate Year and Source Bar', H2))
    s.append(P(
        'Directly under the header is a thin information bar that tells you which schedule you '
        'are looking at and where the official numbers come from.'))
    s.append(SP(4))
    s.append(tbl(['ITEM', 'WHAT IT MEANS'], [
        ['Rate Year',
         'The year of the FEMA schedule these figures represent -- for example, 2025. This is '
         'the single most important thing to check before an incident, because you must use '
         'the rate that was in effect at the time of your disaster declaration.'],
        ['Source',
         'A link to the official fema.gov "Schedule of Equipment Rates" page. It opens in a '
         'new browser tab and needs an internet connection; it is the master list you check '
         'your local copy against.'],
        ['Labor reminder',
         'A standing note that labor costs are tracked separately and these rates cover '
         'equipment only. Always use the rate in effect when your disaster was declared.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('19.3  The Stale-Rate Reminder Banner', H2))
    s.append(P(
        'When the loaded rates are getting old, a yellow reminder banner appears above the '
        'information bar. It is the app nudging you to check fema.gov for a newer schedule '
        'and update your local copy. If the banner is not showing, your rates are considered '
        'current and nothing is wrong. When you see it, do not panic -- the numbers still '
        'work; they simply may no longer match the latest FEMA publication. Follow the '
        'yearly-update steps in 19.8 to clear it.'))
    s.append(SP(6))

    s.append(P('19.4  Reading the Rate Table', H2))
    s.append(P(
        'The main table lists every rate, grouped under a colored category header row (for '
        'example, "Generators" or "Vehicles"). Each equipment row has these columns.'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['Code',
         'The FEMA code for that equipment line, such as "6-1-4". Blank shows as a dash. This '
         'is the identifier FEMA uses in its own schedule.'],
        ['Description',
         'The plain description of the equipment, such as "Generator, 10-25 kW". This is what '
         'you match your real equipment against.'],
        ['Unit',
         'How the rate is charged -- hour, day, mile, or each. It tells you what one unit of '
         'the rate buys.'],
        ['Rate',
         'The dollar figure per unit, shown in green (for example, $27.50). This is the '
         'number multiplied by usage to price the equipment.'],
        ['Year',
         'The schedule year this specific rate belongs to. Normally it matches the Rate Year '
         'in the bar above; a mismatch flags a rate you updated by hand out of step.'],
        ['Notes',
         'Any extra note attached to the rate -- a size band, a condition, or a reminder. '
         'Often blank.'],
        ['Edit (pencil button)',
         'The small pencil button at the end of each row. Click it to open that rate in the '
         'edit window (see 19.5).'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('19.5  Searching and Filtering', H2))
    s.append(P(
        'With dozens of rates loaded, two controls above the table help you find one fast.'))
    s += steps([
        'Type into the <b>Search equipment...</b> box to filter the table live. It matches '
        'the description, the FEMA code, and the category, so typing "generator", "6-1", or '
        '"vehicles" all narrow the list as you type.',
        'Use the <b>All categories</b> drop-down to show only one category at a time. Choose '
        'a category to hide everything else; choose "All categories" again to bring the full '
        'list back.',
        'The small count next to the drop-down (for example, "12 rates") tells you how many '
        'rows match what you have typed and chosen, so you know the filter is working.',
    ])
    s.append(note(
        'Search and category filter work together. If a rate you expect is missing, clear the '
        'search box first and set the drop-down back to "All categories" -- one of the two is '
        'probably still narrowing the list.', 'tip'))
    s.append(SP(6))

    s.append(P('19.6  Editing an Existing Rate', H2))
    s.append(P(
        'When FEMA changes a figure, or you find one that does not match the official '
        'schedule, correct it in place.'))
    s += steps([
        'Find the rate using search or the category filter, then click the <b>pencil</b> '
        'button at the end of its row. The <b>Edit Rate</b> window opens with the current '
        'values already filled in.',
        'Change the figure in the <b>Rate ($/unit)</b> box, and adjust any other field that '
        'needs it.',
        'Click the green <b>SAVE</b> button. The window closes and the table refreshes with '
        'the new figure immediately.',
    ])
    s.append(P(
        'The edit window is the same form used to add a rate. Its fields are:'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Description',
         'Required. The plain name of the equipment, such as "Generator, 10-25 kW".'],
        ['Category',
         'The group the rate is filed under, such as "Generators" or "Vehicles". It sets '
         'which colored header row the rate appears beneath.'],
        ['FEMA Code',
         'The official FEMA code, such as "6-1-4". Optional, but worth filling in so your '
         'copy matches the published schedule.'],
        ['Unit',
         'How the rate is charged -- pick hour, day, mile, or each from the list.'],
        ['Rate ($/unit)',
         'The dollar figure for one unit. Type numbers only; the app formats it as currency.'],
        ['Rate Year',
         'The schedule year this figure belongs to. It defaults to the current Rate Year.'],
        ['Notes',
         'Optional free text -- a size band, a condition, or a reminder about the rate.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P('The <b>Unit</b> drop-down offers four choices:'))
    s.append(tbl(['UNIT', 'MEANING'], [
        ['hour', 'The rate is charged for each hour the equipment is used.'],
        ['day', 'The rate is charged for each day the equipment is used.'],
        ['mile', 'The rate is charged for each mile driven -- used for some vehicles.'],
        ['each', 'The rate is a flat charge per item, not tied to time or distance.'],
    ], widths=[1.0*inch, CW-1.0*inch]))
    s.append(SP(6))

    s.append(P('19.7  Adding a Custom Rate', H2))
    s.append(P(
        'The standard schedule does not list every machine a local group owns. When you have '
        'a piece of equipment FEMA does not cover with a standard line, add your own rate.'))
    s += steps([
        'Click <b>+ Add Custom Rate</b> in the top-right of the header. The <b>Add Custom '
        'Rate</b> window opens with empty fields.',
        'Fill in at least the <b>Description</b> -- it is the only required field. Add the '
        '<b>Category</b>, <b>FEMA Code</b>, <b>Unit</b>, <b>Rate</b>, <b>Rate Year</b>, and '
        '<b>Notes</b> as needed.',
        'Click <b>SAVE</b>. The new rate is stored locally and appears in the table under its '
        'category right away, ready to use in cost documentation.',
    ])
    s.append(note(
        'If you click SAVE with the Description empty, the app stops you with a "Description '
        'required" message. Fill it in and save again.', 'note'))
    s.append(SP(6))

    s.append(P('19.7.1  Deleting a Rate', H3))
    s.append(P(
        'To remove a rate you no longer want, open it with the pencil button and click the '
        'red <b>Delete</b> button in the edit window. The app asks "Delete this rate?" first; '
        'click OK to confirm. The rate is removed from the active list. Delete a rate only '
        'when you are sure no past incident cost record still depends on it.'))
    s.append(SP(6))

    s.append(P('19.8  Updating the Rate Year After FEMA Publishes', H2))
    s.append(P(
        'FEMA publishes a fresh Schedule of Equipment Rates from time to time. When it does, '
        'you roll your local copy forward. The year-update tool stamps the new year onto '
        'every rate at once -- but it is important to understand what it does and does not '
        'change.'))
    s += steps([
        'Click <b>Update Rate Year</b> (the calendar button) in the header. The <b>Update '
        'FEMA Rate Year</b> window opens.',
        'Type the new year in the <b>New Rate Year</b> box.',
        'Click <b>Update Year Tag</b>. The app stamps that year onto all existing rates and '
        'confirms how many it updated.',
        'Then open fema.gov (use the Source link) and correct the individual dollar figures '
        'that actually changed, editing each one as in 19.6.',
    ])
    s.append(note(
        'The Update Year tool changes only the <b>year label</b> on your rates -- it does NOT '
        'change any dollar amount. FieldCommand cannot download the new figures for you. You '
        'still have to compare against fema.gov and edit the individual rates that changed. '
        'Update the year first, then the amounts.', 'warn'))
    s.append(SP(6))

    s.append(P('19.9  How These Rates Feed Cost Documentation', H2))
    s.append(P(
        'This page is a reference list; you do not tie rates to a specific incident here. The '
        'work of costing an incident happens on the <b>FEMA Cost Documentation</b> page (the '
        'FEMA Costs back link), where each piece of Force Account Equipment you log is priced '
        'against the matching rate from this schedule and multiplied by the hours or days it '
        'ran. Those equipment totals then roll up into the incident financial picture on the '
        'Cost Tracking Dashboard (Chapter 20). Keeping this schedule accurate and current is '
        'what makes those downstream totals defensible when you submit for reimbursement.'))
    s.append(SP(6))

    s.append(P('19.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The table says "Loading rates..." and never fills in',
         'The ICS platform service (port 5055) is not answering. Check that the ics-platform '
         'service is running from the Health page, then reload the page.'],
        ['A yellow reminder banner is showing at the top',
         'Your rates are getting old. Check fema.gov for a newer Schedule of Equipment Rates, '
         'then use Update Rate Year and edit the changed figures (see 19.8).'],
        ['A rate I know exists is not in the table',
         'A search term or the category drop-down is still filtering. Clear the Search box '
         'and set the drop-down back to "All categories".'],
        ['I clicked SAVE and got "Description required"',
         'The Description field was empty. Type a description -- it is the one field every '
         'rate must have -- and save again.'],
        ['I updated the year but the dollar amounts look the same',
         'That is expected. Update Rate Year only changes the year label. Edit each changed '
         'figure by hand from the official fema.gov schedule.'],
        ['The Source link will not open',
         'That link needs internet. On an offline field network it will not load; check it '
         'from a device with a WAN connection before the incident.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch20():
    s = chapter(20, 'Cost Tracking Dashboard',
                'http://192.168.50.1/cost_dashboard.html')
    s.append(P(
        'The Cost Tracking Dashboard is the incident financial picture on one screen. It '
        'reads every Federal Emergency Management Agency (FEMA) Force Account cost entry you '
        'have logged and every daily rate you have set on a T-card, adds them all up, and '
        'shows the running total, where the money is going, how fast it is being spent, and '
        'what the incident is likely to cost if it keeps going at the current pace. It is a '
        '<b>read-only</b> view -- you do not type costs here; you type them on the FEMA PA '
        "Cost Documentation page (fema_costs.html) and on the T-cards, and this dashboard "
        'reflects them. The Finance/Administration Section Chief lives on this page during a '
        'multi-day incident, and the Incident Commander glances at the big Total Costs number '
        'from across the room.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: enter costs on the FEMA cost page and rates on the T-cards, then '
        'watch this dashboard total them, chart them, and project them forward -- '
        'automatically, refreshed every two minutes.', 'tip'))
    s.append(SP(6))

    s.append(P('20.1  Opening the Dashboard and Choosing an Incident', H2))
    s.append(P(
        'The page opens showing "Select an incident to view cost dashboard." Nothing is '
        'calculated until you pick which incident you want to look at.'))
    s += steps([
        'Open <b>Cost Dashboard</b> from the main dashboard.',
        'At the top right, open the <b>Select incident...</b> drop-down and choose the '
        'incident. The dashboard fills in immediately.',
        'The incident you pick is remembered, so the next time you open the page it loads '
        'that same incident for you.',
        'To force an immediate update without waiting for the two-minute cycle, click the '
        '<b>Refresh</b> button next to the drop-down.',
    ])
    s.append(note(
        'The page reloads its own numbers automatically every two minutes, so a screen left '
        'up on a wall monitor stays current on its own. You do not have to keep clicking '
        'Refresh.', 'note'))
    s.append(SP(4))
    s.append(P(
        'Two shortcuts sit in the top bar for jumping to where costs are actually entered: '
        'the <b>Edit Costs</b> button and the <b>Dashboard</b> back link. Edit Costs opens '
        'the FEMA PA Cost Documentation page; the back link returns you to the main '
        'FieldCommand dashboard.'))
    s.append(SP(6))

    s.append(P('20.2  The Six Summary Tiles', H2))
    s.append(P(
        'Across the top of the dashboard are six large tiles. Each is sized to be readable '
        'from a distance so command staff can see the headline figures without leaning in.'))
    s.append(SP(4))
    s.append(tbl(['TILE', 'WHAT IT SHOWS'], [
        ['Total Costs',
         'The grand total of every documented cost on the incident. The small line '
         'underneath counts how many resources and how many personnel are on the T-card '
         'board (for example, "8 resources - 24 personnel").'],
        ['Force Acct Labor',
         'The total of all Force Account Labor entries -- your own personnel hours, '
         'including any fringe. The small line counts how many labor entries make up the '
         'figure.'],
        ['Force Acct Equipment',
         'The total of all Force Account Equipment entries -- your own owned equipment '
         'run at FEMA equipment rates. The small line counts the equipment entries.'],
        ['Materials / Contracts',
         'The total of all materials and contracted-cost entries -- purchased supplies and '
         'outside contracts. The small line counts the material entries.'],
        ['Elapsed Time',
         'How long the incident has been open, shown in minutes, hours, or days. This is '
         'the clock the burn rate and projections are measured against. Shows a dash if the '
         'incident has no open time recorded.'],
        ['Burn Rate',
         'How fast money is being spent -- the dollars-per-hour figure. The small line '
         'restates it as a per-day and per-12-hour-period figure. Shows a dash with "Enter '
         'costs above to calculate" until there are both costs and elapsed time.'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(6))

    s.append(P('20.3  The Cost Breakdown Bars', H2))
    s.append(P(
        'Below the tiles, the <b>Cost Breakdown</b> card draws one horizontal bar for each '
        'of the three cost categories, so you can see at a glance which category is driving '
        'the spend. Each bar is labeled with the exact dollar amount and the percentage of '
        'the total it represents.'))
    s.append(SP(4))
    s.append(tbl(['BAR', 'WHAT IT REPRESENTS'], [
        ['Force Account Labor', 'Your personnel labor costs -- usually the largest bar on a '
         'staffed incident.'],
        ['Force Account Equipment', 'Your owned equipment costs at FEMA equipment rates.'],
        ['Materials / Contracts', 'Purchased materials and contracted services.'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(note(
        'The percentages are shares of the current total, so they always add up to roughly '
        '100 percent. If one bar fills most of the width, that is where your money is going '
        '-- a fast sanity check that the cost mix looks right for this kind of incident.', 'note'))
    s.append(SP(6))

    s.append(P('20.4  Resources on Incident', H2))
    s.append(P(
        'The <b>Resources on Incident</b> card, on the left of the middle row, groups the '
        'T-card resource board by resource type and shows what each type is contributing. '
        'The small line at the top reminds you: "T-card resources. Set daily cost to include '
        'in burn rate estimate." The <b>Edit rates</b> link jumps to the FEMA cost page '
        'where daily rates are set.'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['Resource / Type', 'The resource type name (for example, Crew, Engine, Personnel), '
         'with a small line under it counting how many resources of that type are on the '
         'board.'],
        ['Count', 'How many resources of this type are currently on the T-card board.'],
        ['Personnel', 'How many people are assigned across the resources of this type.'],
        ['Est Daily $', 'The estimated cost per day for this type, from the daily rates set '
         'on the T-cards. Shows a dash when no rate has been set.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(P(
        'When at least one resource is present, a <b>Totals</b> line appears at the bottom '
        'of the card with the total personnel count and the total estimated cost per day. If '
        'the board is empty, the card reads "No resources on T-card board."'))
    s.append(note(
        'A resource shows a dash in the Est Daily $ column until you give it a daily rate on '
        'its T-card. Resources with no rate still count toward personnel accountability, but '
        'they contribute nothing to the burn rate -- so set rates on the resources you want '
        'reflected in the cost projection.', 'tip'))
    s.append(SP(6))

    s.append(P('20.5  Cost Projection', H2))
    s.append(P(
        'The <b>Cost Projection</b> card, on the right of the middle row, extrapolates the '
        'current burn rate forward to four fixed horizons so you can plan and request '
        'budget before you run out. It reads "Based on entered costs and elapsed time. '
        'Projections assume current burn rate continues."'))
    s.append(SP(4))
    s.append(tbl(['HORIZON', 'WHAT IT ESTIMATES'], [
        ['Next 12hr (1 period)', 'Projected total after one more 12-hour operational period.'],
        ['Next 24hr (1 day)', 'Projected total after one more day.'],
        ['Next 72hr (3 days)', 'Projected total after three more days.'],
        ['Next 7 days', 'Projected total after a full week.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(P(
        'Each row shows the projected running total, with the added amount for that horizon '
        'in parentheses. Until there are both costs and an incident start time, the card '
        'reads "Enter costs and incident start time for projections."'))
    s.append(note(
        'These are straight-line estimates -- they assume you keep spending at the same rate '
        'you have so far. A demobilizing incident will come in under the projection; a '
        'ramping one will run over it. Treat the numbers as planning figures and verify them '
        'with the Finance Section Chief before committing to a budget request.', 'warn'))
    s.append(SP(6))

    s.append(P('20.6  Budget Tracker', H2))
    s.append(P(
        'The <b>Budget Tracker</b> sits at the bottom of the Cost Projection card. Enter an '
        'authorized dollar figure and it shows how much of that budget you have used, in a '
        'colored bar, plus how much is left.'))
    s.append(SP(4))
    s += steps([
        'In the <b>Budget Limit</b> box, type the authorized dollar amount -- for example, '
        '50000 for a $50,000 authorization.',
        'Click <b>Set</b> (or the bar updates as you type).',
        'Read the bar: the left label shows the amount spent of the budget, and the right '
        'label shows the percentage spent.',
        'Read the line under the bar: it shows either "$X remaining" in green, or "$X over '
        'budget" in red when spending has passed the limit.',
    ])
    s.append(P(
        'The bar changes color as a warning: <b>green</b> below 70 percent, <b>amber</b> at '
        '70 percent or more, and <b>red</b> at 90 percent or more. Once you cross the limit, '
        'the remaining line flips to red and reads "over budget."'))
    s.append(SP(6))

    s.append(P('20.7  Cost by Operational Period', H2))
    s.append(P(
        'The <b>Cost by Op Period</b> card at the bottom breaks the FEMA Force Account costs '
        'out by the operational period each entry was tagged to. This is the layout you want '
        'for after-action documentation and for building a FEMA Project Worksheet (PW). It '
        'reads "From FEMA force account entries tagged by period."'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['Period', 'The operational period label -- "Period 1", "Period 2", and so on. '
         'Entries with no period tag are grouped under "Unassigned".'],
        ['Labor', 'Force Account Labor cost logged in that period, including fringe.'],
        ['Equipment', 'Force Account Equipment cost logged in that period.'],
        ['Materials', 'Materials and contract cost logged in that period.'],
        ['Total', 'The row total for the period -- labor plus equipment plus materials.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(P(
        'If nothing is tagged yet, the card reads "No period data -- tag FEMA cost entries '
        'with an op period." To populate it, set the operational period on each entry when '
        'you record it on the FEMA cost page.'))
    s.append(SP(6))

    s.append(P('20.8  Where the Numbers Come From', H2))
    s.append(P(
        'Everything on this dashboard is a reflection of data entered elsewhere. Knowing the '
        'source of each figure tells you exactly where to go to correct it.'))
    s.append(SP(4))
    s.append(tbl(['DASHBOARD FIGURE', 'ITS SOURCE'], [
        ['Total Costs, category totals, breakdown bars, per-period table',
         'The FEMA PA Cost Documentation page (fema_costs.html) -- the Labor, Equipment, '
         'and Materials entries you record there.'],
        ['Resources on Incident, personnel counts, Est Daily $',
         'The T-card board -- the resources on it, the people assigned to them, and the '
         'daily rates set on each card.'],
        ['Elapsed Time, Burn Rate, projections',
         'Calculated from the incident open time and the totals above.'],
        ['Budget Tracker',
         'The budget figure you type into this page, compared against the Total Costs.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(note(
        'The footer states the scope plainly: costs shown are from FEMA Force Account '
        'entries only, and all projections are estimates to verify with the Finance Section '
        'Chief. If a real cost is missing from the dashboard, it has not been entered on the '
        'FEMA cost page yet.', 'note'))
    s.append(SP(6))

    s.append(P('20.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The dashboard is blank and says "Select an incident"',
         'No incident is chosen. Open the "Select incident..." drop-down at the top right '
         'and pick one.'],
        ['Total Costs shows $0 but I know we have spent money',
         'Nothing has been recorded yet. Click Edit Costs to open the FEMA PA Cost '
         'Documentation page and enter the labor, equipment, and material costs.'],
        ['Burn Rate and projections show a dash',
         'They need both entered costs and an incident open time. Confirm the incident has a '
         'start time recorded and that at least one cost has been entered.'],
        ['A resource shows a dash under Est Daily $',
         'That T-card has no daily rate set. Open the resource on the T-card board (or click '
         'Edit rates) and enter a daily cost.'],
        ['The Cost by Op Period card says "No period data"',
         'The FEMA cost entries are not tagged to a period. Open each entry on the FEMA cost '
         'page and set its operational period.'],
        ['The numbers look stale',
         'The page refreshes every two minutes on its own. To update now, click the Refresh '
         'button; if it still looks wrong, confirm you are on the correct incident.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch21():
    s = chapter(21, 'Personnel Accountability',
                'http://192.168.50.1/accountability.html')
    s.append(P(
        'Personnel accountability is a fundamental National Incident Management System (NIMS) '
        'and Incident Command System (ICS) safety requirement. At any moment during an incident, '
        'the Incident Commander (IC) and the Safety Officer must be able to answer two questions '
        'with certainty: <b>Who is on this incident?</b> and <b>Where is each person right now?</b> '
        'Failure to maintain accountability has cost responders their lives at wildland fires, '
        'structural collapses, and other incidents where conditions changed fast and people could '
        'not be located. The Personnel Accountability page (accountability.html) is the Safety '
        "Officer's single screen for keeping both answers current.", Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: this is the Safety Officer roll-call board -- it lists everyone on the '
        'incident, lets you run a timed head count (a PAR), and flags anyone who is not fully '
        'accounted for.', 'tip'))
    s.append(SP(6))

    s.append(P('21.1  The Two Levels of Personnel Accountability', H2))
    s.append(P(
        'FieldCommand tracks people two ways at once, because either one alone leaves a gap. '
        'The page pulls both together so the Safety Officer sees a single, cross-checked picture.'))
    s.append(SP(4))
    s.append(tbl(['LEVEL -- TOOL', 'WHAT IT TRACKS', 'MAINTAINED BY'], [
        ['Incident level\n\nICS-211 Check-In List',
         'Who has formally checked into this incident, when they arrived, and whether they have '
         'checked out. Every person on the incident must have an ICS-211 entry regardless of '
         'agency, role, or resource assignment.',
         'Check-in recorders at entry points; the Resources Unit Leader (RESL) keeps the master list.'],
        ['Resource level\n\nT-Card Personnel',
         'Who is assigned to each specific resource (crew, engine, unit), and therefore where each '
         'person is supposed to be right now.',
         'The Operations Section and crew supervisors, who build each T-card personnel list.'],
    ], widths=[1.5*inch, CW-4.0*inch, 2.5*inch]))
    s.append(SP(4))
    s.append(note(
        'Both levels are required -- neither alone is enough. The ICS-211 tells you everyone who is '
        'on the incident. The T-card list tells you which resource each person is on and where they '
        'should be. The Cross-Reference tab compares the two and catches gaps in both directions.', 'warn'))
    s.append(SP(6))

    s.append(P('21.2  The Screen at a Glance', H2))
    s.append(P(
        'The page opens with a red header reading <b>PERSONNEL ACCOUNTABILITY</b> and the sub-line '
        '"Safety Officer tool - All personnel - All resources". A control bar runs across the top; '
        'below it, four tabs switch between the working lists.'))
    s.append(SP(4))
    s.append(P('The control bar holds these buttons and menus:'))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Select incident...', 'Choose which incident this board is for. Your choice is remembered '
         'the next time you open the page.'],
        ['Period 1', 'Pick the operational period. Accountability is tracked per period.'],
        ['Refresh', 'Reloads the counts and lists from the server right now.'],
        ['Conduct PAR', 'Starts a Personnel Accountability Report -- a timed roll call (see 21.5).'],
        ['Reset PAR', 'Clears every PAR confirmation and starts a fresh PAR cycle.'],
        ['Print', 'Opens a clean print view of the current list (buttons and tabs are hidden).'],
        ['Auto 60s', 'A checkbox that reloads the board automatically every 60 seconds.'],
        ['Dashboard', 'Returns to the main dashboard.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P('The four tabs are:'))
    s.append(P('<b>ICS-211 CHECK-IN LIST</b> -- everyone who has checked into the incident.', Bullet))
    s.append(P('<b>T-CARD PERSONNEL</b> -- personnel grouped by the resource they are assigned to.', Bullet))
    s.append(P('<b>UNACCOUNTED</b> -- only the people not yet confirmed in the current PAR.', Bullet))
    s.append(P('<b>CROSS-REFERENCE</b> -- gaps between the two lists (see 21.9).', Bullet))
    s.append(SP(6))

    s.append(P('21.3  The Summary Tiles and PAR Badge', H2))
    s.append(P(
        'A strip of six count tiles sits under the header, giving the whole-incident picture at a '
        'glance. To their right, the <b>PAR badge</b> shows when the last PAR was run and whether '
        'everyone was accounted for.'))
    s.append(SP(4))
    s.append(tbl(['TILE', 'WHAT IT COUNTS'], [
        ['Total Personnel', 'Everyone known to this incident and period, checked in or out.'],
        ['Checked In', 'People currently checked in (still on the incident).'],
        ['Checked Out', 'People who have been checked out and are no longer counted as present.'],
        ['PAR Confirmed', 'People confirmed accounted for in the current PAR cycle.'],
        ['Unaccounted', 'Checked-in people not yet confirmed in the current PAR. This is the number '
         'to watch -- it should reach zero.'],
        ['On T-Cards', 'People listed on resource T-cards.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'When a PAR is running and anyone is still unaccounted, a red <b>UNACCOUNTED PERSONNEL</b> '
        'banner appears near the top with the count. It clears itself the moment the last person '
        'is confirmed.', 'note'))
    s.append(SP(6))

    s.append(P('21.4  The ICS-211 Check-In List Tab', H2))
    s.append(P(
        'This tab lists everyone who has completed ICS-211 check-in for the selected incident and '
        'period. (Check-in itself is done on the separate Incident Check-In and camera-scan pages, '
        'covered in the check-in chapter.) The list sorts unconfirmed checked-in people to the top '
        'during a PAR so the ones needing attention are always in view.'))
    s.append(SP(4))
    s.append(P('Each person row shows:'))
    s.append(tbl(['ITEM ON THE ROW', 'WHAT IT MEANS'], [
        ['Name', "The person's name."],
        ['Callsign / ID badge', 'A blue tag with their callsign or member ID, when one is on file.'],
        ['Agency - Position - Resource', "The person's agency, ICS position, and resource type, "
         'joined with dots.'],
        ['In / Out / PAR times', 'Check-in time, check-out time (if any), and the time they were '
         'last PAR-confirmed.'],
        ['Location line', 'The last known location, if one has been entered, shown with a marker.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(P(
        'A colored left edge tells you each row status at a glance: green means PAR-confirmed, red '
        'means checked in but not yet confirmed in this PAR, and a faded gray row means the person '
        'is checked out. The action buttons on each row are <b>PAR</b> (confirm this person), '
        '<b>Location</b> (record their last known location), and <b>Check Out</b> (see 21.10). '
        'A <b>Check All Out</b> button at the top of this tab checks everyone out at once for '
        'end-of-operation demobilization.'))
    s.append(SP(6))

    s.append(P('21.5  Conducting a Personnel Accountability Report (PAR)', H2))
    s.append(P(
        'A Personnel Accountability Report is a deliberate, time-stamped roll call confirming that '
        'every person is accounted for. Run one at every operational-period change and shift change, '
        'whenever a hazard escalates, and immediately whenever anyone cannot be located.'))
    s.append(SP(4))
    s += steps([
        'Open <b>Personnel Accountability</b> from the dashboard and choose the incident and period.',
        'Click <b>Conduct PAR</b>. The time is stamped, the PAR badge reads "PAR in progress...", '
        'and the board switches to the ICS-211 list with unconfirmed people sorted to the top.',
        'Contact each supervisor or crew boss by radio and have them confirm every person on their '
        'resource.',
        'As each person is confirmed, click <b>PAR</b> on their row. The counts update immediately '
        'and the row turns green.',
        'Check the <b>UNACCOUNTED</b> tab to see who is still outstanding (see 21.6). Work it down '
        'to zero.',
        'When everyone is confirmed, the Unaccounted tile reads 0 and the PAR badge shows '
        '"All accounted for".',
        'To begin the next roll call, click <b>Reset PAR</b> and confirm. Every confirmation is '
        'cleared and a new cycle begins.',
    ])
    s.append(SP(6))

    s.append(P('21.6  The Unaccounted Tab', H2))
    s.append(P(
        'The UNACCOUNTED tab is the Safety Officer working list during a PAR. It shows only the '
        'people who are checked in but not yet confirmed in the current cycle, under a red banner '
        'telling you to contact their supervisor immediately and to escalate to the Incident '
        'Commander if you cannot make contact. Each row carries the same three actions -- '
        '<b>PAR -- Confirmed</b>, <b>Check Out</b>, and <b>Location</b> -- so you can clear a '
        'person without leaving the tab. When the list empties, it shows "All personnel accounted for".'))
    s.append(SP(4))
    s.append(note(
        'If a person cannot be accounted for after you have exhausted radio contact, treat it as a '
        'missing-responder emergency: notify the IC, halt operations in the affected area, and start '
        'a search. Do not wait for the next scheduled PAR.', 'warn'))
    s.append(SP(6))

    s.append(P('21.7  The T-Card Personnel Tab', H2))
    s.append(P(
        'This tab is resource-level accountability. It lists personnel grouped under the resource '
        'they are assigned to -- so instead of just "Jones is on this incident" you see "Jones is on '
        'Engine 12". Each resource group has a header showing the resource name, its assignment, and '
        'a running PAR count such as <b>3/4 PAR</b> -- how many of that crew are confirmed out of the '
        'total. Each person row shows name and callsign, ICS position, agency, and contact, plus a '
        '<b>PAR</b> button and a <b>Location</b> button. Confirming people here counts toward the '
        'same PAR cycle as the ICS-211 tab, so a large incident can be worked resource by resource.'))
    s.append(SP(4))
    s.append(note(
        'Adding someone to a T-card does NOT check them into the ICS-211, and checking someone in '
        'does NOT put them on a T-card -- the two lists are separate records. Keep both current, and '
        'use Cross-Reference (21.9) to catch anyone who is in only one of them.', 'warn'))
    s.append(SP(6))

    s.append(P('21.8  Last Known Location', H2))
    s.append(P(
        'The last known location adds a layer of situational awareness to a PAR: when a supervisor '
        'confirms a crew, they can also report where that crew is. Click the <b>Location</b> button '
        'on any row -- on either the ICS-211 or the T-Card tab -- and the <b>UPDATE LAST KNOWN '
        'LOCATION</b> box opens. Type the location in the field (the placeholder suggests the style: '
        '"Division Alpha - Sector 3 - Base Camp") and click <b>Save</b>. The location is stamped with '
        'the time and then shows on that person\'s row with a marker. Click <b>Cancel</b> to close '
        'without saving.'))
    s.append(SP(6))

    s.append(P('21.9  Cross-Reference -- Closing the Accountability Gap', H2))
    s.append(P(
        'The CROSS-REFERENCE tab compares the ICS-211 check-in list against the T-card personnel '
        'rosters and flags two specific gaps. A clean cross-reference -- no flags either way -- means '
        'both lists are in sync.'))
    s.append(SP(4))
    s.append(tbl(['CONDITION', 'WHAT IT MEANS', 'ACTION REQUIRED'], [
        ['Checked in -- not on any T-card',
         'The person completed ICS-211 check-in but is not on any resource T-card. They may be '
         'floating staff, a late arrival, or the T-card was never updated.',
         'Assign them to a resource and add them to its T-card, or confirm they are intentionally '
         'unassigned (for example, Safety Officer or PIO) and note their location.'],
        ['On T-card -- no ICS-211 check-in',
         'The person is on a resource T-card but has no ICS-211 entry. This is a <b>safety gap</b>: '
         'they are on the incident, possibly in a hazardous area, but not in the formal '
         'accountability system.',
         'Direct them to complete ICS-211 check-in immediately. If they cannot be located, '
         'escalate to the IC.'],
    ], widths=[1.7*inch, CW-3.8*inch, 2.1*inch]))
    s.append(SP(4))
    s.append(note(
        'Run the cross-reference at the start of each operational period and any time new personnel '
        'arrive. When it is clean, everyone on the incident is both in the formal check-in system '
        'and assigned to a resource.', 'note'))
    s.append(SP(6))

    s.append(P('21.10  Checking Personnel Out', H2))
    s.append(P(
        'Check-out matters as much as check-in. When a person leaves the incident for any reason, '
        'check them out so the board reflects who is actually present. People who leave without being '
        'checked out inflate the PAR count and can trigger an unnecessary search. To check one person '
        'out, click <b>Check Out</b> on their row and confirm. The check-out time is stamped, the row '
        'fades to gray, and they drop out of the active count -- their record is kept, not deleted. '
        'At the end of an operation, use the <b>Check All Out</b> button at the top of the ICS-211 '
        'tab to check out everyone still shown as present in one step, after confirming the count.'))
    s.append(SP(6))

    s.append(P('21.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The lists are empty and say "Select an incident above"',
         'Choose an incident from the "Select incident..." menu in the control bar. Nothing loads '
         'until an incident is selected.'],
        ['The ICS-211 tab says "No check-ins for this period"',
         'People check in on the Incident Check-In / camera-scan pages, not here. Confirm they '
         'checked in, and that you have the right operational period selected.'],
        ['The Unaccounted tab says "Conduct a PAR first"',
         'The Unaccounted list only fills once a PAR is running. Click <b>Conduct PAR</b> to start '
         'a roll call.'],
        ['Cross-Reference flags someone whose name is spelled two ways',
         'The match is by name. Fix the spelling so the ICS-211 entry and the T-card entry read '
         'the same, then Refresh -- the flag clears.'],
        ['A checked-out person still shows in the list',
         'That is expected -- checked-out records are retained (grayed out) for documentation. They '
         'no longer count toward Checked In or Unaccounted.'],
        ['The counts look stale during a fast-moving incident',
         'Click <b>Refresh</b>, or tick <b>Auto 60s</b> so the board reloads itself every minute.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch22():
    s = chapter(22, 'ICS-213 General Message',
                'http://192.168.50.1/ics213.html')
    s.append(P(
        'The ICS-213 General Message is the standard Incident Command System (ICS) form for '
        'short written messages that pass between sections, agencies, or individuals during an '
        'incident. It is the paper (or, here, on-screen) note that carries a request, an order, '
        'a status update, or a question from one person to another, with a clean record of who '
        'sent it, who it was for, when, and what came back. FieldCommand IMS gives you a '
        'fillable ICS-213 that auto-fills a sender name from the Federal Communications '
        'Commission (FCC) database, captures a drawn signature, produces a print-ready form, '
        'keeps a running log of the messages you have sent, and can hand a completed message to '
        'a Winlink radio-email client for delivery over the air.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: fill in the boxes, press Generate Form, then print it, save it to the '
        'log, or send it over Winlink.', 'tip'))
    s.append(SP(6))

    s.append(P('22.1  Opening the Form and What You See', H2))
    s.append(P(
        'Open <b>ICS-213</b> from the dashboard or from the top navigation bar (the link reads '
        '<b>ICS-213</b>, sitting between <b>NTS Radiogram</b> and <b>ICS-214</b>). The page '
        'opens on the entry form, which is split into three titled cards you fill top to bottom, '
        'a row of action buttons, and a <b>Saved ICS-213 Messages</b> log at the bottom. A live '
        'Coordinated Universal Time (UTC) clock ticks in the top-right corner. The three cards '
        'are:'))
    s.append(P('<b>Incident &amp; Routing</b> - who the message is to and from, and the '
               'incident, number, date, time, and subject.', Bullet))
    s.append(P('<b>Message</b> - the message text itself and the Reply Requested checkbox.', Bullet))
    s.append(P('<b>Approved / Received</b> - the approving signature and the reply block the '
               'recipient fills in.', Bullet))
    s.append(SP(6))

    s.append(P('22.2  The Incident & Routing Card', H2))
    s.append(P(
        'This card is where the message is addressed. Every field is optional, but the more you '
        'fill in the more complete the finished form is.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident Name', 'The name of the incident this message belongs to, for example '
         '"Operation Winter Storm 2026". It prints in box 1 at the top of the form.'],
        ['To (Name / Title)', 'The person or role the message is going to, such as "Operations '
         'Section Chief".'],
        ['To (Position / Agency)', 'The position or agency of the recipient, such as "Franklin '
         'County EMA".'],
        ['Message Number', 'A tracking number for this message, such as "ICS-213-001". '
         'Auto-fill can generate the next number for you (see 22.5).'],
        ['From Callsign', 'Your amateur radio callsign. Type it and press Tab (or click out of '
         'the box) and the From name below fills in automatically from the FCC database. It '
         'forces itself to capital letters as you type. Leave it blank if you are not a licensed '
         'ham - the field is optional.'],
        ['From (Name / Title)', 'Your name or role, such as "Communications Unit Leader". Fills '
         'itself from the callsign if you left it empty.'],
        ['From (Position / Agency)', 'Your position or agency, such as "ARES / RACES".'],
        ['Date', 'The message date, such as "Jun 7, 2026". Auto-fill can set this to today.'],
        ['Time', 'The message time, such as "0930 UTC". Auto-fill can set this to now.'],
        ['Subject', 'A one-line subject, such as "Communications Status Update".'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        'The callsign lookup only works when the offline FCC database is installed on the '
        'server. If the name does not fill in, type it by hand - the message is not held up by '
        'a missing lookup.', 'note'))
    s.append(SP(6))

    s.append(P('22.3  The Message Card', H2))
    s.append(P(
        'The <b>Message Text</b> box is the body of the message - the actual thing you are '
        'telling the recipient. Write it clearly and concisely: say who needs to act, what '
        'action is needed, and by when. Below the message is one checkbox:'))
    s.append(P('<b>Reply Requested</b> - tick this when the recipient must send an answer back. '
               'When ticked, the printed form marks the reply block with "REPLY REQUESTED" in '
               'red so it is obvious a reply is expected.', Bullet))
    s.append(SP(6))

    s.append(P('22.4  The Approved / Received Card', H2))
    s.append(P(
        'This card holds the approval (the sender side) and the reply (the recipient side). All '
        'of it is optional.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Approved By (Name)', 'The name of the person who approved sending the message, such as '
         '"Incident Commander". Prints in box 7.'],
        ['Approved By (Title / Position)', 'That person\'s title or position, such as "Incident '
         'Command".'],
        ['Approved By (Signature)', 'A signature pad you sign with a mouse, stylus, or finger. '
         'Use <b>Clear Signature</b> to erase and start over. Optional - leave it blank to sign '
         'the printed copy by hand.'],
        ['Reply (if applicable)', 'The recipient\'s written reply. Usually filled in by whoever '
         'receives the message, not the sender.'],
        ['Replied By (Name / Signature)', 'The name of the person who replied.'],
        ['Reply Date / Time', 'When the reply was made.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(note(
        'The signature is captured as a small image and prints on the form. If you sign, draw '
        'the whole signature in one continuous view before pressing Generate Form; a blank pad '
        'simply prints no signature.', 'tip'))
    s.append(SP(6))

    s.append(P('22.5  Auto-fill and Generating the Form', H2))
    s.append(P(
        'Two buttons sit under the entry cards. <b>Auto-fill Date/Time</b> stamps the current '
        'UTC date and time into the Date and Time boxes and, if the Message Number is empty, '
        'fills in the next number in sequence (for example "ICS-213-004" when three are already '
        'saved). <b>Generate Form</b> builds the print-ready ICS-213 from everything you typed. '
        'To create a message:'))
    s += steps([
        'Fill in the <b>Incident &amp; Routing</b>, <b>Message</b>, and (if needed) '
        '<b>Approved / Received</b> cards.',
        'Click <b>Auto-fill Date/Time</b> to stamp the date, time, and a message number, or '
        'type your own.',
        'Sign the <b>Approved By</b> pad if a signature is wanted.',
        'Click <b>Generate Form</b>. The entry cards hide and a clean, black-on-white ICS-213 '
        'appears, laid out in the standard numbered boxes, and the page scrolls to it.',
        'If something is wrong, click <b>Edit</b> (the left-arrow button in the preview bar) to '
        'go back to the entry cards without losing anything.',
    ])
    s.append(SP(6))

    s.append(P('22.6  Printing, Saving, and Exporting', H2))
    s.append(P(
        'Once the form is generated, a bar of buttons appears above it. Each does one thing with '
        'the finished message.'))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['Print Form', 'Opens your browser\'s print dialog. Only the ICS-213 itself prints - the '
         'navigation bar, entry cards, and log are hidden on paper.'],
        ['Save to Log', 'Stores the message in the Saved ICS-213 Messages log on this device and '
         'also sends a copy to the server so it becomes part of the incident record.'],
        ['Export (.txt)', 'Downloads the message as a plain text file named after the message '
         'number, for archiving or pasting elsewhere.'],
        ['Send via Winlink', 'Prepares the message as a Winlink text file (see 22.7).'],
        ['Edit', 'Returns to the entry cards to make changes.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(note(
        'A new blank form is one click away at any time: the <b>New</b> button (the circular '
        'arrow, top-right of the page header) clears every field, wipes the signature, and '
        'returns you to an empty entry form.', 'note'))
    s.append(SP(6))

    s.append(P('22.7  Sending via Winlink', H2))
    s.append(P(
        'Winlink is amateur radio email - a way to move messages when there is no internet. '
        'FieldCommand does not connect to the radio itself; instead <b>Send via Winlink</b> '
        'writes the completed ICS-213 into a ready-to-send text file (named "winlink_" plus the '
        'message number) and downloads it. A short pop-up reminds you what to do next.'))
    s += steps([
        'Generate the form, then click <b>Send via Winlink</b>.',
        'A text file downloads with the To line, Subject line, and full message already filled '
        'in.',
        'Open that file in your Winlink client - Pat (the Winlink software on the Pi, covered in '
        'Chapter 29) or Winlink Express on a laptop.',
        'Put the recipient\'s Winlink address in the To line and send it over the radio from the '
        'Winlink client.',
    ])
    s.append(note(
        'FieldCommand only prepares the message; it never transmits. You still need a working '
        'Winlink session and a licensed operator to actually put it on the air.', 'warn'))
    s.append(SP(6))

    s.append(P('22.8  Receiving a Winlink ICS-213', H2))
    s.append(P(
        'The flow also runs the other way. When an ICS-213 arrives over Winlink, the Winlink '
        'import tool (winlink-import.html) can push it straight into this page: the ICS-213 '
        'opens with every field - incident, to, from, number, date, time, subject, message, '
        'approval, and reply - already filled from the received message, and jumps directly to '
        'the print-ready view so you can read, print, or save it. You do not retype anything.'))
    s.append(SP(6))

    s.append(P('22.9  The Saved Messages Log', H2))
    s.append(P(
        'The <b>Saved ICS-213 Messages</b> table at the bottom of the page lists every message '
        'you have saved with <b>Save to Log</b>, newest first. It is your quick history of '
        'outgoing traffic on this device. The columns are:'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT SHOWS'], [
        ['#', 'The message number, such as "ICS-213-002".'],
        ['Subject', 'The subject line of the message.'],
        ['To', 'Who the message was addressed to.'],
        ['From', 'Who sent it.'],
        ['Date', 'The date and time it carried.'],
        ['(remove)', 'The X button on the right of each row deletes that one saved message '
         'after a confirmation.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P(
        'The log keeps up to fifty of your most recent messages on this device; the '
        '<b>Clear All</b> button beside the log heading empties the whole list after a '
        'confirmation. Because <b>Save to Log</b> also sends a copy to the server, a saved '
        'message is preserved in the incident record even if you later clear this local list.'))
    s.append(SP(6))

    s.append(P('22.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['I typed my callsign but the From name did not fill in',
         'The offline FCC database may not be installed, or the callsign was mistyped. Type the '
         'name in the From (Name / Title) box by hand - the lookup is only a convenience.'],
        ['I clicked Print and got the whole web page',
         'Print from the generated form, not the entry cards. Click Generate Form first; only '
         'then does the print output show just the ICS-213.'],
        ['My signature did not print',
         'The pad was empty when you generated the form, or you cleared it. Go back with Edit, '
         'sign the Approved By pad, then Generate Form again.'],
        ['Send via Winlink did nothing on the radio',
         'That is expected - it only prepares and downloads a file. Open that file in Pat or '
         'Winlink Express and send it from there with an active Winlink session.'],
        ['A saved message vanished from the log',
         'The local log holds only your fifty most recent, and Clear All empties it. A copy was '
         'still sent to the server when you saved it, so the incident record keeps it.'],
        ['Auto-fill gave a message number I did not want',
         'Just type over the Message Number box with your own value; auto-fill only fills it '
         'when the box is empty.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch23():
    s = chapter(23, 'ICS-214 Activity Log & ICS-309 Communications Log',
                'http://192.168.50.1/ics214.html')
    s.append(P(
        'Two of the most-used records on any incident are the ICS-214 Activity Log and the '
        'ICS-309 Communications Log. The ICS-214 is a running diary: it records the notable '
        'activities and significant events for one unit or resource during an operational '
        'period, plus who was assigned and what equipment they used. The ICS-309 is a message '
        'log: it records the traffic that passed on a net or station - who called whom, when, '
        'and about what. FieldCommand gives you a clean fill-in-the-blanks screen for each, a '
        'print-ready federal form, and a way to save the finished record into the incident. '
        'The ICS-214 can also push its personnel straight into the Federal Emergency '
        'Management Agency (FEMA) labor-cost paperwork, so hours you already logged do not '
        'have to be retyped for reimbursement.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: the ICS-214 says what your unit did and who was there; the ICS-309 '
        'says what messages moved on the radio - and FieldCommand prints both on the official '
        'forms.', 'tip'))
    s.append(SP(6))

    s.append(P('23.1  When to Use Each Log', H2))
    s.append(P(
        'The two logs answer different questions. Fill in whichever one - or both - matches '
        'the record you need to leave behind.'))
    s.append(SP(4))
    s.append(tbl(['USE THIS', 'WHEN YOU NEED TO RECORD'], [
        ['ICS-214 Activity Log',
         'What a unit or section actually did during a shift - the timeline of significant '
         'events, decisions, and actions, plus the people and gear assigned to that period.'],
        ['ICS-309 Communications Log',
         'The message traffic that moved on a net or at a station - each call, the from and '
         'to stations, the time, and the subject or message text.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(P(
        'Open either form from the top navigation bar, which carries links for '
        '<b>Dashboard</b>, <b>ICS-213</b>, <b>ICS-214</b>, and <b>ICS-309</b>. The clock at '
        'the right of the bar shows the current time in Coordinated Universal Time (UTC), '
        'which is the time base these logs use.'))
    s.append(SP(6))

    s.append(P('23.2  ICS-214: Incident and Unit Information', H2))
    s.append(P(
        'The ICS-214 screen is built as four numbered cards. The first card, '
        '<b>1. Incident &amp; Unit Information</b>, sets the header of the form. Fill in what '
        'applies; blank fields simply print empty.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident Name', 'The name of the incident this log belongs to, such as '
         '"Operation Winter Storm 2026".'],
        ['Operational Period Date From / To', 'The calendar dates the shift covers. The two '
         'boxes combine into the printed "Operational Period".'],
        ['Time From', 'The clock time the operational period began, in 24-hour form '
         '(for example 0600).'],
        ['Unit Name / Designator', 'The unit or resource this log is for, such as '
         '"ARES Communications Unit".'],
        ['Unit Leader Name', 'The person in charge of the unit for this period, name and '
         'callsign if they have one.'],
        ['Unit Leader Position', 'That leader\'s ICS role, such as "Communications Unit '
         'Leader (COML)".'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(SP(4))
    s.append(note(
        'The <b>Auto-fill Dates</b> button (a clock icon) drops today\'s UTC date into the '
        '"Date From" box if it is empty and stamps the "Date / Time Prepared" field, so you '
        'do not have to look up the date by hand.', 'tip'))
    s.append(SP(6))

    s.append(P('23.3  Personnel and Resources Assigned', H2))
    s.append(P(
        'The next two cards record who worked and what equipment they used - the information '
        'the ICS-214 needs, and the information FEMA later wants for cost recovery.'))
    s.append(SP(4))
    s.append(P('23.3.1  Personnel Assigned to This Period', H3))
    s.append(P(
        'Card <b>2. Personnel Assigned to This Period</b> is a small table. Click '
        '<b>+ Add Person</b> for each new row; click the red X at the end of a row to remove '
        'it. The screen starts you with three blank rows.'))
    s.append(tbl(['COLUMN', 'WHAT TO ENTER'], [
        ['Name', 'The person\'s name (and callsign if licensed).'],
        ['ICS Position', 'Their assignment on the incident, such as "COML" or "NET".'],
        ['Affiliation', 'The group they belong to, such as "ARES" or "EMA".'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P('23.3.2  Resources Involved', H3))
    s.append(P(
        'Card <b>2b. Resources Involved</b> is optional. Use it to note the equipment, '
        'vehicles, and other resources the unit used this period - radios, generators, '
        'go-boxes, vehicles. Click <b>+ Add Resource</b> for each item.'))
    s.append(tbl(['COLUMN', 'WHAT TO ENTER'], [
        ['Resource', 'The item, such as "Generator", "Go-Box 1", or "Vehicle".'],
        ['Type / Kind', 'The category, such as "Equipment" or "Vehicle".'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'If you leave the Resources card empty, it simply does not appear on the printed '
        'form - it prints only when at least one resource is filled in.', 'note'))
    s.append(SP(6))

    s.append(P('23.4  The Activity Log Itself', H2))
    s.append(P(
        'Card <b>3. Activity Log</b> is the heart of the form: a time-stamped list of the '
        'notable things that happened. Each entry has a time and a one-line description.'))
    s.append(SP(4))
    s += steps([
        'To add a blank line, click <b>+ Add Entry</b>, then type the time and the activity.',
        'To add a line already stamped with the current UTC time, click <b>+ Add '
        'Timestamped Entry</b> (the clock icon). The cursor jumps to the description box so '
        'you can start typing at once. The <b>Add Entry Now</b> button at the top of the page '
        'does the same thing.',
        'Type a short, plain description in the box - for example, "Established contact with '
        'EOC on primary net".',
        'To delete a line, click the red X at the right of that row.',
    ])
    s.append(note(
        'Times are stamped in UTC and shown with a trailing "Z" (for example 1430Z). Keep '
        'every entry in the same time base so the timeline reads correctly later.', 'tip'))
    s.append(SP(6))

    s.append(P('23.5  Signing and Generating the ICS-214', H2))
    s.append(P(
        'Card <b>4. Prepared By</b> captures who completed the form. Fill in <b>Prepared By '
        '(Name)</b>, <b>Position / Title</b>, and <b>Date / Time Prepared</b>. Below those is '
        'a <b>Signature</b> pad - sign it with a mouse, stylus, or finger, or click '
        '<b>Clear Signature</b> to start over. The signature is optional; leave it blank to '
        'sign the printed copy by hand.'))
    s.append(SP(4))
    s += steps([
        'When the form is complete, click <b>Generate Form</b> (the page icon). The screen '
        'switches to a black-and-white, print-ready ICS 214 that matches the official layout.',
        'Review it. To go back and change anything, click <b>Edit</b> (the back arrow) to '
        'return to the fill-in cards.',
        'Click <b>Print Form</b> (the printer icon) to send it to a printer or save it as a '
        'PDF through your browser\'s print dialog.',
        'Click <b>Save</b> to store the ICS-214 in the incident record on the server so it '
        'is archived with the rest of the incident.',
    ])
    s.append(note(
        'Use <b>New</b> (the top-of-page circular-arrow button) to clear the whole form and '
        'start a fresh ICS-214. It wipes the fields, the tables, and the signature.', 'note'))
    s.append(SP(6))

    s.append(P('23.6  Export to FEMA Labor', H2))
    s.append(P(
        'On the print preview there is a <b>Export to FEMA Labor</b> button (a money icon). '
        'It takes the people you listed in the Personnel card and adds each of them to the '
        'FEMA Force Account Labor cost sheet for the active incident, carrying their name, '
        'position, affiliation, and the operational-period date. This is the bridge between '
        'day-to-day activity logging and the reimbursement paperwork - you do not retype the '
        'roster.'))
    s.append(SP(4))
    s += steps([
        'Make sure the incident you are working is selected on the dashboard, so the labor '
        'entries attach to the right incident.',
        'Fill in at least one person in the Personnel card - the export refuses to run with '
        'an empty roster.',
        'Click <b>Generate Form</b>, then <b>Export to FEMA Labor</b>.',
        'A message confirms how many people were exported. Open the FEMA cost page to enter '
        'each person\'s hours and pay rate - only the names and roles cross over; the hours '
        'and dollars are entered there.',
    ])
    s.append(note(
        'If no incident is selected, the people are still added to the labor sheet but '
        'without an incident link. The confirmation message warns you when that happens - '
        'select the incident first to avoid it.', 'warn'))
    s.append(SP(6))

    s.append(P('23.7  ICS-309: Two Ways to Produce It', H2))
    s.append(P(
        'There are two ways to make an ICS-309 Communications Log, and they suit different '
        'situations.'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'HOW IT WORKS'], [
        ['Automatic - from the Net Logger',
         'On the Net Logger (netcontrol.html), the <b>ICS-309</b> button (a page icon, titled '
         '"Export ICS-309 for currently selected net") builds a Communications Log from the '
         'net you have open. It lists the message traffic first (number, time, from station, '
         'to station, handling, and message text), then the station check-in list, with the '
         'net name, frequency and mode, and net open and close times in the header. It opens '
         'a print view you can save or print. A net flagged as a drill prints with a DRILL / '
         'EXERCISE watermark.'],
        ['Manual - the ICS-309 page',
         'The ics309.html screen is a blank ICS-309 you fill in by hand, for traffic a Net '
         'Logger did not capture - a single station, an informal exchange, or a paper log '
         'you are transcribing.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(note(
        'If you ran the traffic on a logged net, always prefer the automatic export - it is '
        'faster and cannot miss a check-in. Use the manual page only for traffic the net '
        'never recorded.', 'tip'))
    s.append(SP(6))

    s.append(P('23.8  Filling In the Manual ICS-309', H2))
    s.append(P(
        'The manual ICS-309 page opens with a <b>Log Header</b> card, then a <b>Log '
        'Entries</b> table. Fill in the header first:'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident / Event Name', 'The incident or event this traffic belongs to.'],
        ['Operational Period - From / To', 'The start and end of the shift the log covers, '
         'date and time.'],
        ['Task No.', 'An optional task or assignment number.'],
        ['Operator (Name / Callsign)', 'The operator who kept the log, such as '
         '"J. Smith W9XYZ".'],
        ['Station / Net', 'The station or net position, such as "Net Control" or "EOC".'],
        ['Page', 'The page count, such as "1 of 1". Left blank, it prints as "1 of 1".'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(SP(6))

    s.append(P('23.9  ICS-309 Log Entries and Saving', H2))
    s.append(P(
        'Each row of the <b>Log Entries</b> table is one message. The rows are numbered for '
        'you. Add rows with the two buttons below the table.'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT TO ENTER'], [
        ['#', 'The line number, filled in automatically.'],
        ['Date / Time', 'When the message passed, in "DD HHMMZ" form (day, then UTC time).'],
        ['From', 'The callsign or station the message came from.'],
        ['To', 'The callsign or station the message went to.'],
        ['Subject / Message', 'A short description of the traffic, or the message text '
         'itself.'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(4))
    s += steps([
        'Click <b>+ Add Entry</b> for a blank line, or <b>+ Add (timestamp now)</b> to add a '
        'line already stamped with the current UTC date and time (the cursor jumps to the '
        'Subject box).',
        'Remove any line with the red X at the right of that row.',
        'Click <b>Generate Form</b> to see the print-ready ICS-309, then <b>Print</b> to '
        'print or save it. <b>Back to Edit</b> returns you to the table.',
        'To file the log with an incident, pick the incident from the drop-down next to '
        '<b>Save to Incident</b>, then click that button. The log is stored on the server '
        'under that incident.',
    ])
    s.append(note(
        'If the server cannot be reached when you click <b>Save to Incident</b>, the log is '
        'saved locally on the device instead and you are told so. Save it again to the '
        'incident once the server is back, so it lands in the permanent archive.', 'warn'))
    s.append(SP(6))

    s.append(P('23.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['"Add at least one person before exporting to FEMA Labor."',
         'The Personnel card is empty. Add at least one row with a name in the ICS-214, then '
         'run Export to FEMA Labor again.'],
        ['FEMA Labor entries are not linked to my incident',
         'No incident was selected when you exported. Select the incident on the dashboard '
         'first, then re-export; the entries will attach to it.'],
        ['The Resources section is missing from my printed ICS-214',
         'It prints only when at least one resource is filled in. Add a row in card 2b, then '
         'Generate Form again.'],
        ['My typed times look out of order on the log',
         'Mixed time bases. Keep every entry in UTC (shown with a trailing "Z") - use the '
         'timestamp buttons rather than typing local time.'],
        ['"Server unreachable - saved locally on this device." on the ICS-309',
         'The log is safe on this device but not yet in the incident archive. When the '
         'server is reachable, open the form and click Save to Incident again.'],
        ['The ICS-309 export from the Net Logger is grayed out or empty',
         'No net is selected. Open the net you want on the Net Logger first, then click the '
         'ICS-309 button; it builds the log from the selected net.'],
    ], widths=[2.5*inch, CW-2.5*inch]))
    s.append(PB())
    return s


def ch24():
    s = chapter(24, 'Wide Area Network (WAN) Settings & Dual-Source Internet Configuration',
                'http://192.168.50.1/wan_settings.html')
    s.append(P(
        'FieldCommand IMS is built to run with no internet at all, but when a Wide Area '
        'Network (WAN) connection is available it lights up the online-only extras: live '
        'weather radar, callsign and map lookups, and off-site backup. The WAN / Internet '
        'Settings page lets you tell the system about two internet sources at once - a '
        '<b>preferred</b> one that is tried first, and a <b>fallback</b> that takes over '
        'automatically if the preferred source goes down. No carrier names or hardware '
        'brands are wired into the system: either source can be a cellular modem, a phone '
        'hotspot, a satellite dish, or fixed home broadband. What matters is the role you '
        'give it, not the brand. This same page also sets which status cards appear on the '
        'dashboard and names the Universal Serial Bus (USB) drive used for automatic '
        'backups.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: fill in up to two internet sources, mark one Preferred and one '
        'Fallback, click Save Settings, and FieldCommand switches between them on its own.',
        'tip'))
    s.append(SP(6))

    s.append(P('24.1  Opening the Page and What You See', H2))
    s.append(P(
        'Open <b>WAN / Internet Settings</b> from the dashboard (it carries an <b>ADMIN</b> '
        'badge in the page header). The page is laid out top to bottom as two source cards, '
        'a swap button between them, a Dashboard Display box, a USB Backup Drive box, and the '
        'Save Settings row. The blue banner at the top restates the rule: the preferred '
        'source is tried first, the fallback is used automatically if the preferred one is '
        'down, and changes take effect within 30 seconds.'))
    s.append(SP(4))
    s.append(P(
        'The top card is <b>Source A</b> and starts as Preferred (a green stripe down its '
        'left edge). The lower card is <b>Source B</b> and starts as Fallback (an amber '
        'stripe). Each card header shows a type icon, the display name you give it, a colored '
        'role badge, and an <b>Enabled</b> checkbox.'))
    s.append(SP(6))

    s.append(P('24.2  The Source Card Fields', H2))
    s.append(P(
        'Both cards carry the same fields. Fill them in for each internet source you have. '
        'You do not have to use both cards - a group with a single hotspot only fills in '
        'Source A.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Enabled (checkbox)',
         'Turns the source on or off without erasing what you typed. A disabled card dims '
         'and its badge reads <b>Disabled</b>.'],
        ['Display Name',
         'The plain name shown on the dashboard status bar - for example "Cellular", '
         '"Satellite", or "Office Wi-Fi". The card header updates as you type.'],
        ['Role',
         'A drop-down: <b>Preferred - use this first</b> or <b>Fallback - use if preferred '
         'is down</b>. This is the setting that decides failover order.'],
        ['Type',
         'A drop-down that picks the icon and category. Choices are listed in 24.3.'],
        ['Provider / Carrier (optional)',
         'A free-text label for your own reference, such as "T-Mobile", "Starlink", or '
         '"Comcast". It has no effect on detection - leave it blank if you like.'],
        ['Detection Method',
         'How FieldCommand decides whether this source is up right now. The three methods '
         'are explained in 24.4.'],
        ['Gateway IP to Ping',
         'Appears only when the method is <b>Ping a gateway IP</b>. The address to ping.'],
        ['Admin URL',
         'Appears only when the method is <b>Modem admin page responds</b>. The web address '
         'of the modem or router admin page.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('24.3  Source Type Options', H2))
    s.append(P(
        'The <b>Type</b> drop-down only changes the icon and the category label - it does '
        'not change how the source is detected. Pick the closest match.'))
    s.append(SP(4))
    s.append(tbl(['OPTION', 'MEANING'], [
        ['Cellular (modem, router, dongle)',
         'A dedicated cellular internet device - a modem, a cellular router, or a USB LTE '
         'dongle plugged into the Pi.'],
        ['Phone / mobile hotspot',
         'A smartphone or tablet sharing its data connection over Wi-Fi or USB.'],
        ['Satellite (Starlink, HughesNet, ViaSat...)',
         'A satellite internet dish and its indoor router.'],
        ['Fixed ISP (cable, fiber, DSL, WISP)',
         'Wired home or venue broadband - cable, fiber, Digital Subscriber Line (DSL), or a '
         'Wireless Internet Service Provider (WISP).'],
        ['Other',
         'Anything that does not fit the categories above.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(SP(6))

    s.append(P('24.4  Detection Methods', H2))
    s.append(P(
        'The detection method is how the WAN monitor tests whether a source is really '
        'working. When you choose a method, a help box under the card fills in with example '
        'addresses for common devices. Pick the method that fits your hardware.'))
    s.append(SP(4))
    s.append(tbl(['METHOD', 'HOW IT WORKS', 'BEST FOR'], [
        ['Internet reachable - no device check',
         'Simply tests whether the internet is reachable. Needs no IP address. If both '
         'sources use this method, Preferred wins.',
         'Phone hotspots, a USB Long Term Evolution (LTE) dongle, or a single WAN source.'],
        ['Ping a gateway IP',
         'Pings an address that answers only when this path is active - usually the modem or '
         'hotspot gateway. Enter it in the Gateway IP field.',
         'Any source with a known gateway, such as Starlink on 192.168.100.1.'],
        ['Modem admin page responds',
         'Checks that the modem or router admin web page answers. May also read the carrier '
         'name and signal strength. Enter the Admin URL.',
         'Cellular modems and routers that have a local admin web page.'],
    ], widths=[1.8*inch, CW-3.6*inch, 1.8*inch]))
    s.append(SP(4))
    s.append(P(
        'The help box lists real example addresses. Common ones: an Android hotspot gateway '
        'is usually <b>192.168.43.1</b>, an iPhone hotspot <b>172.20.10.1</b>, Starlink '
        '<b>192.168.100.1</b>, and HughesNet <b>192.168.0.1</b>. For a modem admin page, try '
        '<b>http://192.168.1.1</b> or <b>http://192.168.0.1</b>. Use your own device manual '
        'if it differs - do not type the examples blindly.'))
    s.append(SP(6))

    s.append(P('24.5  Setting Up Your Two Sources', H2))
    s += steps([
        'On <b>Source A</b>, tick <b>Enabled</b>, type a <b>Display Name</b> (for example '
        '"Cellular"), and choose the <b>Type</b> that matches your device.',
        'Set the <b>Role</b> to <b>Preferred - use this first</b> for the source you want '
        'used whenever it is available.',
        'Choose a <b>Detection Method</b>. If you pick <b>Ping a gateway IP</b>, fill in the '
        '<b>Gateway IP to Ping</b>; if you pick <b>Modem admin page responds</b>, fill in the '
        '<b>Admin URL</b>. Otherwise no address is needed.',
        'Repeat on <b>Source B</b> for your backup source, setting its <b>Role</b> to '
        '<b>Fallback - use if preferred is down</b>.',
        'Click <b>Save Settings</b>. A green "Saved - changes active within 30s" message '
        'appears; the failover takes effect on the next monitor cycle.',
    ])
    s.append(note(
        'If you only have one internet source, fill in Source A, leave Source B disabled, and '
        'set Source A to the <b>Internet reachable - no device check</b> method. That gives '
        'you simple up/down status with no address to configure.', 'note'))
    s.append(SP(6))

    s.append(P('24.6  Swapping Preferred and Fallback', H2))
    s.append(P(
        'Between the two cards is the <b>Swap preferred and fallback roles between the two '
        'sources</b> button (marked with an up/down arrows icon). Click it to flip the two '
        'roles at once - whichever card was Preferred becomes Fallback and vice versa. The '
        'card stripes and badges update immediately so you can see the new order before you '
        'save. Use it when you want to manually favor, say, satellite over cellular for a '
        'while without touching any physical connections. The change is not stored until you '
        'click <b>Save Settings</b>.'))
    s.append(SP(6))

    s.append(P('24.7  Dashboard Display', H2))
    s.append(P(
        'The <b>Dashboard Display</b> box controls which status cards appear on the main '
        'dashboard. Tick only the cards you want operators to see.'))
    s.append(SP(4))
    s.append(tbl(['CHECKBOX', 'WHAT IT DOES'], [
        ['Show Source A card on dashboard',
         'Shows the Source A internet status card on the dashboard. On by default.'],
        ['Show Source B card on dashboard',
         'Shows the Source B (fallback) status card. Off by default - turn it on when you '
         'actually run a second source.'],
        ['Show AMPRNet / 44Net status card',
         'Shows the amateur-radio 44Net (AMPRNet) gateway status card. On by default.'],
    ], widths=[2.6*inch, CW-2.6*inch]))
    s.append(SP(6))

    s.append(P('24.8  USB Backup Drive', H2))
    s.append(P(
        'The <b>USB Backup Drive</b> box names the external drive that triggers an automatic '
        'backup when it is plugged in. Any USB drive formatted and labeled <b>FIELDCOMMAND</b> '
        '(all capitals) starts a backup on insertion - any brand, any size, in ext4 or exFAT '
        'format.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Drive Label (udev trigger)',
         'The volume label the system watches for. Defaults to <b>FIELDCOMMAND</b>. The drive '
         'itself must carry this exact label for the automatic backup to fire.'],
        ['Display Name',
         'A friendly name shown in the app for the drive, such as "LaCie Rugged" or '
         '"WD Passport". For your reference only.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(SP(4))
    s.append(note(
        'If you change the trigger label away from FIELDCOMMAND, you must also edit the file '
        '<b>/etc/udev/rules.d/99-fieldcommand-backup.rules</b> and run '
        '<b>sudo udevadm control --reload-rules</b> at the command line, or the drive will no '
        'longer be recognized. Most groups should leave the label as FIELDCOMMAND.', 'warn'))
    s.append(SP(6))

    s.append(P('24.9  Saving and Applying Changes', H2))
    s.append(P(
        'At the bottom are two buttons. <b>Save Settings</b> writes the whole page - both '
        'sources, the dashboard choices, and the USB drive names - to the server. A status '
        'message confirms the save in green, or shows a red "Save failed" message if the '
        'server rejected it. <b>Reload</b> (the circular-arrow button) throws away unsaved '
        'edits and reloads the last saved values from the server, which is handy if you have '
        'changed things and want to start over. After a successful save, allow up to 60 '
        'seconds for the WAN monitor to pick up the new configuration and update the '
        'dashboard status bar.'))
    s.append(SP(6))

    s.append(P('24.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['My changes did not seem to take effect right away',
         'The monitor polls on a cycle. Wait up to 60 seconds after Save; the dashboard '
         'status bar updates on the next poll.'],
        ['The Gateway IP field never appears',
         'That field only shows when the Detection Method is "Ping a gateway IP". Choose that '
         'method and the field appears; choose "Modem admin page responds" for the Admin URL '
         'field instead.'],
        ['A source shows down even though the internet works',
         'The detection method may be wrong for that device. If it has no admin page or fixed '
         'gateway, switch it to "Internet reachable - no device check". If you ping a '
         'gateway, confirm the IP is correct for that device.'],
        ['Both sources are set to Preferred (or both Fallback)',
         'Roles are independent per card. Set one to Preferred and one to Fallback, or use '
         'the Swap button. If both use the internet-only method, Preferred wins.'],
        ['I plugged in my USB drive but no backup started',
         'The drive must be labeled exactly FIELDCOMMAND in all capitals and be ext4 or '
         'exFAT. Relabel the drive, or match the Drive Label field to the drive and update '
         'the udev rule as noted in 24.8.'],
        ['Save failed with a red message',
         'The page could not reach the platform server (port 5055). Confirm you are on '
         '192.168.50.1, the ics-platform service is running, then click Reload and try Save '
         'again.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch25():
    s = chapter(25, 'National Weather Service (NWS) Animated Radar',
                'http://192.168.50.1/radar.html')
    s.append(P(
        'The Next Generation Radar (NEXRAD) page is your live weather picture. It plays an '
        'animated loop of the last few hours of national radar over a dark map, so you can '
        'watch a line of storms move toward the incident area and brief command before it '
        'arrives. The page pulls fresh radar from an internet source, so it works only when '
        'the server has a Wide Area Network (WAN) connection - cellular, satellite, or site '
        'internet. When the internet is gone it keeps the last picture on screen and quietly '
        'tries to reconnect. You can open the radar from any of the three dashboard modes.',
        Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: press Play to watch a radar loop of the incoming weather - it needs '
        'internet, and it holds the last frame if the internet drops.', 'tip'))
    s.append(SP(6))

    s.append(P('25.1  What You Need to Use It', H2))
    s.append(P(
        'Radar imagery is downloaded live, so this is one of the few FieldCommand pages that '
        'is <b>not</b> fully offline. The server must have a working WAN link at the moment you '
        'open the page. FieldCommand checks the WAN status for you before it tries to load '
        'anything, so you will get a clear message rather than a blank map if the internet is '
        'down. The map, the controls, and the timeline all live on one full-screen view; there '
        'is nothing to install and no login. The header reads <b>NEXRAD RADAR</b> (with a '
        'storm-cloud icon) and a reminder that it <b>Requires internet connection</b>.'))
    s.append(SP(6))

    s.append(P('25.2  How the Screen Is Laid Out', H2))
    s.append(P(
        'The whole page is one big radar map with small control strips floating over it. '
        'Knowing where each strip sits makes the rest of this chapter quick to follow.'))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IS THERE'], [
        ['Header (top)',
         'The <b>NEXRAD RADAR</b> title, the station drop-down, the <b>Reflectivity</b> and '
         '<b>Velocity</b> view buttons, and a <b>Dashboard</b> link back to the home page.'],
        ['Info bar (over the map, top)',
         'A pulsing loading dot, a status line (for example "NEXRAD CONUS composite"), the '
         'frame count, and the three <b>Palette</b> color swatches on the right.'],
        ['Legend (top-right corner)',
         'The <b>Reflectivity (dBZ)</b> color scale that translates the on-screen colors into '
         'storm intensity.'],
        ['Control bar (bottom)',
         'The <b>Play / Pause</b> button, the step-back and step-forward buttons, the timeline '
         'scrubber, the frame time, and the <b>Speed</b> buttons.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('25.3  The Playback Controls', H2))
    s.append(P(
        'The control bar along the bottom of the map runs the animation. It behaves like a '
        'video player.'))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Play / Pause',
         'Starts or stops the loop. The button shows <b>Pause</b> while running and <b>Play</b> '
         'when stopped. The loop repeats from the start automatically.'],
        ['Step back (left arrow)',
         'Stops the loop and moves back one frame, so you can study one moment of a storm.'],
        ['Step forward (right arrow)',
         'Stops the loop and moves forward one frame.'],
        ['Timeline scrubber',
         'The slider across the middle. Drag it to jump to any point in the loaded loop; the '
         'oldest frame is on the left, the newest on the right.'],
        ['Frame time',
         'Shows the date and time of the frame you are looking at. The newest frame is '
         'highlighted in amber so you can tell "now" from history at a glance.'],
        ['Speed (Slow / Med / Fast)',
         'Sets how fast the loop plays. <b>Med</b> is the default; <b>Fast</b> is good for a '
         'quick trend, <b>Slow</b> for a careful look at storm rotation.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('25.4  Reflectivity vs. Velocity', H2))
    s.append(P(
        'Two buttons in the header choose what the radar colors mean. Pick the one that answers '
        'the question you have.'))
    s.append(SP(4))
    s.append(tbl(['VIEW', 'WHAT IT SHOWS'], [
        ['Reflectivity',
         'The default. Shows how heavy the precipitation is - light rain through heavy rain, '
         'hail, and the strongest cores. This is the everyday "where is the rain and how bad is '
         'it" view. The dBZ legend applies to this view.'],
        ['Velocity',
         'Shows the motion of the precipitation toward or away from the radar, which is what '
         'forecasters use to spot rotation and possible severe weather. The reflectivity legend '
         'hides while this view is selected.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('25.5  Reading the Reflectivity Legend', H2))
    s.append(P(
        'The color bar in the top-right corner is labeled <b>Reflectivity (dBZ)</b>. "dBZ" is '
        'the radar strength number - the bigger the number, the heavier the precipitation. You '
        'do not need to memorize numbers; read the colors.'))
    s.append(SP(4))
    s.append(tbl(['COLOR', 'WHAT IT MEANS'], [
        ['Green', 'Light rain - drizzle to a steady light shower.'],
        ['Yellow', 'Moderate rain - a noticeable rain, worth watching.'],
        ['Red', 'Heavy rain - a strong cell; expect downpours and reduced visibility.'],
        ['Purple / White', 'Extreme returns - the most intense cores, possible hail or a '
         'severe storm. Treat these as the priority to brief.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(note(
        'The legend numbers 5, 20, 35, 50, and 65+ are the dBZ scale. Anything in the red-to-'
        'purple end (roughly 50 dBZ and up) is the part of the storm to warn field teams about.',
        'note'))
    s.append(SP(6))

    s.append(P('25.6  Color Palettes', H2))
    s.append(P(
        'The three round swatches on the info bar, next to the word <b>Palette</b>, change only '
        'the colors used to draw the radar - not the data. Use whichever is easiest to read on '
        'your screen and lighting.'))
    s.append(SP(4))
    s.append(tbl(['PALETTE', 'BEST FOR'], [
        ['Default', 'The standard green-to-red scale most people recognize from television '
         'weather. The everyday choice.'],
        ['Dark', 'A muted blue-to-orange scheme that is easier on the eyes on a big screen in '
         'a dim operations room.'],
        ['NOAA', 'The blue-to-magenta National Oceanic and Atmospheric Administration (NOAA) '
         'style, familiar to anyone who works from official NWS products.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('25.7  Centering on a NEXRAD Station', H2))
    s.append(P(
        'The drop-down in the header (it starts on <b>Composite (National)</b>) is a quick way '
        'to jump the map to a part of the country. Choosing a station - for example '
        '<b>KLOT - Chicago, IL</b> - recenters and zooms the map on the coverage area of that '
        'radar. The imagery stays the national composite; this is a "look here" shortcut, not a '
        'switch to a single-site radar. Pick <b>Composite (National)</b> again to zoom back out '
        'to the default view.'))
    s.append(note(
        'You can also just drag the map with your finger or mouse and scroll to zoom, exactly '
        'like any other map in FieldCommand. The station list is only there to save you the '
        'panning.', 'tip'))
    s.append(SP(6))

    s.append(P('25.8  Watching a Storm Move In', H2))
    s.append(P(
        'The point of the loop is to see where the weather is going, not just where it is. A '
        'quick routine:'))
    s.append(SP(4))
    s += steps([
        'Open <b>NEXRAD Radar</b> from the dashboard. It centers on the incident area and '
        'begins playing automatically.',
        'Use the station drop-down or drag the map so your incident area is in the middle.',
        'Watch a full loop at <b>Med</b> speed to see the overall direction the storms are '
        'traveling.',
        'When a heavy (red or purple) cell is heading your way, click <b>Pause</b>, then use '
        'the step-forward button to walk through the last few frames one at a time and judge '
        'how fast it is closing in.',
        'Read the amber <b>frame time</b> to confirm how recent the newest picture is before '
        'you brief command.',
    ])
    s.append(SP(6))

    s.append(P('25.9  How Fresh the Data Is', H2))
    s.append(P(
        'FieldCommand reloads new radar frames on its own about every five minutes, so a page '
        'left open on a wall display stays current without anyone touching it. The status line '
        'on the info bar tells you what is loaded (for example "NEXRAD CONUS composite" from the '
        'primary source, or "Using IEM NEXRAD WMS (fallback)" if the main source is briefly '
        'down). The frame count shows how many frames are in the current loop. Always trust the '
        '<b>frame time</b> over your assumptions: it is the timestamp of the actual image on '
        'screen.'))
    s.append(SP(6))

    s.append(P('25.10  When the Internet Is Down', H2))
    s.append(P(
        'Because radar comes from the internet, FieldCommand handles a lost WAN gracefully '
        'instead of showing a broken page. If no WAN link is present when you open the page, a '
        'full-screen overlay reads <b>RADAR UNAVAILABLE OFFLINE</b> with the note that radar '
        'requires an internet connection and a <b>Check WAN Status</b> button that jumps you to '
        'the WAN status page. If the internet drops <b>after</b> radar has already loaded, the '
        'last frames stay drawn on the map and the status line changes to something like '
        '"Showing last radar (from 2:45 PM) - reconnecting every 30 s". FieldCommand rechecks '
        'the connection every thirty seconds and resumes live loading the moment the internet '
        'returns - you do not have to reload the page.'))
    s.append(note(
        'A stale radar picture can be dangerous if it is mistaken for live weather. When the '
        'status line says "Showing last radar", tell anyone reading the display that the loop '
        'is frozen until the internet is back.', 'warn'))
    s.append(SP(6))

    s.append(P('25.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['A full-screen "RADAR UNAVAILABLE OFFLINE" message appears',
         'The server has no internet. Click <b>Check WAN Status</b> and restore the cellular, '
         'satellite, or site internet link, then return to the radar page.'],
        ['The map shows storms but the time is old / says "Showing last radar"',
         'The internet dropped after loading. The picture is frozen; FieldCommand reconnects '
         'every 30 seconds. Do not brief it as live until the time updates.'],
        ['The loop is not moving',
         'It may be paused. The button reads <b>Play</b> when stopped - click it. If it still '
         'will not play, only one frame may have loaded; wait for the next 5-minute refresh.'],
        ['Status line reads "Using IEM NEXRAD WMS (fallback)"',
         'The primary radar source was briefly unavailable, so FieldCommand switched to the '
         'backup. This is normal - the radar is still current; no action needed.'],
        ['The colors are hard to read on the big screen',
         'Try a different <b>Palette</b> swatch (Default, Dark, or NOAA). Dark is usually '
         'easiest in a dim operations room.'],
        ['The map is centered on the wrong part of the country',
         'Pick your area from the station drop-down, or drag the map and scroll to zoom. Choose '
         '<b>Composite (National)</b> to zoom back to the default view.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch26():
    s = chapter(26, 'High Frequency (HF) Propagation Tool',
                'http://192.168.50.1/propagation.html')
    s.append(P(
        'The High Frequency (HF) Propagation tool tells you, at a glance, which amateur radio '
        'bands are likely to work right now and which are dead. HF is the part of the radio '
        'spectrum that bounces signals off the upper atmosphere to reach across a county, a '
        'state, or the country when nothing local is left standing. Whether a band carries or '
        'fails changes hour by hour with the Sun. This page pulls the current solar numbers '
        'from an online space-weather source, turns them into plain "good / fair / poor" band '
        'ratings, and draws a set of reference charts so a net control operator or a '
        'Communications Unit Leader can pick a working frequency without guessing.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: open the page, read the color of each band, and steer your HF '
        'traffic to the green ones.', 'tip'))
    s.append(SP(6))

    s.append(P('26.1  What This Tool Shows and What It Needs', H2))
    s.append(P(
        'The page has one job: convert space-weather data into a usable band plan. It fetches '
        'live solar indices from HamQSL (the well-known N0NBH feed at hamqsl.com) every 15 '
        'minutes and, from those numbers, estimates how each band is behaving by day and by '
        'night. It is a <b>read-only reference</b> — there is nothing to fill in, save, or '
        'submit. Nothing here is stored with the incident; it is a live look at the sky.'))
    s.append(P(
        'This tool is one of the few features in FieldCommand IMS that <b>works better with '
        'internet.</b> The solar numbers come from the internet. When the deployment has a '
        'Wide Area Network (WAN) connection, the page shows real, current data. When the '
        'deployment is fully offline, the page cannot fetch the Sun\'s numbers and instead '
        'shows a model-based estimate and a plain "Offline" notice. The estimate is still '
        'useful as a rough guide, but it is not live.', ))
    s.append(SP(6))

    s.append(P('26.2  Reading the Page: Header and Refresh Bar', H2))
    s.append(P(
        'At the very top is the page header. On the left is a <b>Home</b> link back to the '
        'dashboard. In the center is the title <b>HF PROPAGATION</b>. On the right is a status '
        'line that reads <b>Fetching data...</b> while the page loads, then changes to '
        '<b>Updated</b> with a timestamp when live data arrives, or <b>Offline - internet '
        'unavailable</b> when it cannot reach the source.'))
    s.append(P(
        'Just below is the <b>refresh bar</b>. It carries a one-line reminder that solar data '
        'updates every 15 minutes when internet is available and that band conditions are '
        'model-estimated from the solar indices. On the right of that bar is a <b>Refresh</b> '
        'button (a circular-arrow icon). The page refreshes itself automatically every 15 '
        'minutes; press <b>Refresh</b> only when you want the newest numbers immediately.'))
    s.append(SP(6))

    s.append(P('26.3  The Solar Indices Strip', H2))
    s.append(P(
        'The first block of content, under the <b>Solar Indices</b> heading, is a strip of '
        'seven cards. Each shows one space-weather number with its full name underneath. '
        'These are the raw inputs; everything else on the page is derived from them.'))
    s.append(SP(4))
    s.append(tbl(['CARD', 'WHAT IT MEANS'], [
        ['SFI (Solar Flux)',
         'Solar Flux Index. The overall strength of the Sun\'s radio energy. Higher is '
         'better for HF. Above 130 the high bands (20m and up) open; below 70 you are '
         'limited to the low bands. The number turns green when high, amber mid, red low.'],
        ['SN (Sunspot #)',
         'The sunspot count. More sunspots generally means stronger high-band propagation. '
         'It moves with the SFI.'],
        ['A-Index (Geomagnetic)',
         'A daily measure of how disturbed the Earth\'s magnetic field has been. Low is '
         'calm and good; a high A-index means bands have been rough. Green under 10, amber '
         'to 30, red above.'],
        ['K-Index (3-hr Planetary)',
         'The most immediately useful number. A right-now, 0-to-9 measure of geomagnetic '
         'activity updated every three hours. 0-2 is excellent, 3-4 is fair, 5 or more '
         'signals a storm that degrades HF. Green, amber, or red accordingly.'],
        ['X-Ray (Flux Class)',
         'The current solar X-ray level, shown as a letter class (A, B, C, M, or X). A '
         'class M or X flare shown in red or amber can cause a sudden radio blackout on the '
         'daylight side of the Earth.'],
        ['Proton (Event)',
         'Whether a solar proton event is in progress. "None" (green) is normal; a flagged '
         'event (red) can knock out paths that cross the polar regions.'],
        ['Signal (Noise Level)',
         'The reported background radio noise level. Higher noise makes weak signals harder '
         'to copy.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(note(
        'When the page is offline, all seven cards read <b>N/A</b> instead of a number. That '
        'is your cue that the ratings below are the built-in estimate, not live data.', 'note'))
    s.append(SP(6))

    s.append(P('26.4  The K-Index Scale', H2))
    s.append(P(
        'Below the strip is a panel titled <b>K-Index Scale (Geomagnetic Activity)</b>. It '
        'draws ten cells labeled K0 through K9. The cells up to the current K value are '
        'filled in with color that runs from green at the calm end to deep red at the stormy '
        'end, and the current level is outlined in white. A one-line legend under the cells '
        'spells out the bands: <b>K0-K2</b> Quiet (good HF), <b>K3-K4</b> Unsettled, '
        '<b>K5-K7</b> Storm (degraded HF), and <b>K8-K9</b> Severe storm (HF blackout '
        'possible). This is the quickest single check on the page: if the white-outlined cell '
        'is in the green, HF is worth trying.'))
    s.append(SP(6))

    s.append(P('26.5  Band Conditions (Day/Night Model)', H2))
    s.append(P(
        'The <b>Band Conditions (Day/Night Model)</b> section is a grid of cards, one per '
        'band group. Each card shows the band name, its frequency span, and two colored bars '
        '- a <b>Day</b> bar and a <b>Night</b> bar - each labeled with a word rating. The '
        'bar\'s length and color both encode the rating, so you can read the card from across '
        'a room.'))
    s.append(SP(4))
    s.append(tbl(['BAND GROUP', 'FREQUENCY SPAN AND TYPICAL EMCOMM USE'], [
        ['80m-40m', '3.5 to 7.3 MHz. The regional and national workhorses. 80m carries '
         'local and regional traffic at night; 40m is the backbone band, reliable day and '
         'night out to a few hundred miles and beyond.'],
        ['30m-20m', '10.1 to 14.35 MHz. Longer-haul daytime bands. 20m reaches across the '
         'country and farther when the Sun is up.'],
        ['17m-15m', '18.1 to 21.45 MHz. High bands that open only when solar flux is strong; '
         'good for long distances by day, usually closed at night.'],
        ['10m', '28 to 29.7 MHz. Opens only under high solar flux. When it is open it is '
         'excellent; most of the time it is closed.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(4))
    s.append(P('The word ratings and their colors mean:'))
    s.append(tbl(['RATING', 'WHAT IT TELLS YOU'], [
        ['Good (green)', 'The band is open and reliable. Use it.'],
        ['Fair (amber)', 'The band is workable but marginal; expect fading and weaker signals.'],
        ['Poor (orange-red)', 'The band is mostly unusable; try only if nothing else works.'],
        ['Closed or a dash (gray)', 'The band is effectively dead for that time of day.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(6))

    s.append(P('26.6  MUF / LUF Estimates', H2))
    s.append(P(
        'In the left panel of the two-column row is <b>MUF / LUF Estimates</b>, labeled for '
        'the deployment\'s reference location (shown as Columbus OH, grid EN90, in the '
        'shipped build). Maximum Usable Frequency (MUF) is the highest frequency that will '
        'still bounce back to you for a given distance; Lowest Usable Frequency (LUF) is the '
        'lowest that will get through. You want to work between the two. The table has one row '
        'per path distance.'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['Path', 'The distance category - Local (0 to 500 km), Regional (500 to 2000 km), '
         'DX (2000 to 5000 km), or Long Path (over 5000 km).'],
        ['LUF (MHz)', 'The lowest frequency that will complete that path. Below this, signals '
         'are absorbed and never return.'],
        ['MUF (MHz)', 'The highest frequency that will still bounce back for that path. Above '
         'this, signals punch through and are lost to space.'],
        ['Best Band', 'The recommended amateur band for that path right now, picked from the '
         'estimated MUF.'],
        ['Reliability', 'A rough percentage confidence, colored green (strong), amber '
         '(marginal), or red (weak).'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(P(
        'A small note under the table reminds you these are estimates from a simplified '
        'ionospheric model - confirm with propagation beacons or an actual on-air call before '
        'you rely on a path for critical traffic.'))
    s.append(SP(6))

    s.append(P('26.7  Ionosphere Layers Diagram', H2))
    s.append(P(
        'The right panel, <b>Ionosphere Layers</b>, is a drawn diagram, not a control. It '
        'shows the atmospheric layers that reflect HF signals, stacked by altitude above the '
        'Earth\'s surface, with a sketched skip path arcing off the top layer. It is here to '
        'explain <b>why</b> the bands behave as they do.'))
    s.append(SP(4))
    s.append(tbl(['LAYER', 'ROLE IN HF PROPAGATION'], [
        ['F2 (~300 km)', 'The main reflecting layer for long-distance HF, roughly 14 to 30 '
         'MHz. It is what makes coast-to-coast contacts possible.'],
        ['F1 (~200 km)', 'A daytime-only layer reflecting roughly 10 to 20 MHz.'],
        ['E (~110 km)', 'A daytime layer; also the source of short-lived "sporadic-E" '
         'openings.'],
        ['D (~70 km)', 'The daytime absorber. It soaks up the low bands during the day, '
         'which is why 80m works at night but not at noon.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(6))

    s.append(P('26.8  24-Hour Band Activity Guide', H2))
    s.append(P(
        'Below the two panels is the <b>24-Hour Band Activity Guide</b>, a timeline chart. '
        'The rows are the major bands (80m, 40m, 20m, 15m, 10m); the horizontal axis is the '
        'hour of the day in Coordinated Universal Time (UTC), 00 through 24. A colored block '
        'marks the hours each band is typically open, and a white dashed vertical line marked '
        '<b>NOW</b> shows the current UTC time so you can read straight down it to see what is '
        'open this minute. The chart scrolls sideways on a narrow screen. As with the other '
        'estimates, the openings shift with season and solar activity - the guide is typical, '
        'not guaranteed.'))
    s.append(SP(6))

    s.append(P('26.9  EmComm Propagation Quick Reference', H2))
    s.append(P(
        'The last panel, <b>EmComm Propagation Quick Reference</b>, is a printed cheat sheet '
        'that does not change with the data. On the left it lists each band from 160m through '
        '10m with a plain day-use and night-use rating. On the right it lists the space-'
        'weather conditions (SFI ranges, K-index thresholds, X-ray flares, proton events, '
        'gray line) and what each one does to HF. A closing note states the emergency-'
        'communications priorities: 40m is the backbone for regional-to-national paths day '
        'and night, 80m covers local and regional at night, and the 60m channels support '
        'interoperability with served agencies.'))
    s.append(SP(6))

    s.append(P('26.10  Using It During an Incident', H2))
    s.append(P(
        'A net control operator or Communications Unit Leader can plan an HF net in under a '
        'minute:'))
    s += steps([
        'Open <b>HF Propagation</b> from the dashboard and confirm the top-right status reads '
        '<b>Updated</b> with a recent time. If it reads <b>Offline</b>, treat the ratings as '
        'a rough model estimate only.',
        'Glance at the <b>K-Index Scale</b>. If the current cell is in the green (K0-K2), HF '
        'is worth using; if it is red (K5 or higher), expect degraded or failed paths.',
        'Read the <b>Band Conditions</b> cards for the distance you need to cover, using the '
        'Day or Night bar that matches the current time.',
        'Cross-check the <b>MUF / LUF Estimates</b> row for your path distance and note the '
        '<b>Best Band</b> it recommends.',
        'Pick the band your radio and license privileges support that is rated best, set up '
        'the net on it, and confirm with an actual on-air check before committing traffic.',
    ])
    s.append(note(
        'Amateur HF transmission requires a properly licensed operator with privileges on the '
        'band and mode in use. This tool tells you which bands are open; it does not grant '
        'anyone the authority to transmit on them.', 'warn'))
    s.append(SP(6))

    s.append(P('26.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Every card reads N/A and the top says "Offline"',
         'The deployment has no internet, so the live solar feed cannot load. The band '
         'ratings shown are a built-in model estimate. Connect a WAN if you need live data, '
         'or use the estimate as a rough guide.'],
        ['The status stays on "Fetching data..." and never updates',
         'The source (hamqsl.com) may be slow or unreachable. Wait a moment, then press the '
         'Refresh button. If it still hangs, the internet path is down - treat it as offline.'],
        ['The numbers look old',
         'The page refreshes on its own every 15 minutes. To force the newest data now, press '
         'the Refresh button in the refresh bar.'],
        ['All bands show Poor even though it is daytime',
         'Check the K-Index. A geomagnetic storm (K5 or higher) forces the model to rate '
         'bands Poor regardless of the hour. Wait for the storm to pass or try 40m/80m.'],
        ['The 24-hour chart is cut off on the side',
         'On a narrow screen the timeline scrolls. Swipe or drag it sideways, or view the '
         'page on a wider display, to see the full 00-to-24 UTC span.'],
        ['The recommended band is one my radio cannot use',
         'The tool assumes full HF access. Choose the next-best band your equipment and '
         'license privileges actually support from the Band Conditions cards.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch27():
    s = chapter(27, 'Winlink Radio Email',
                'http://192.168.50.1/winlink-import.html')
    s.append(P(
        'Winlink is the worldwide amateur radio email network. It carries email-style '
        'messages, including standard Incident Command System (ICS) forms, over radio '
        'when the internet is down. FieldCommand IMS does not send or receive Winlink '
        'itself - you run a separate Winlink program (Winlink Express on a Windows '
        'laptop, or Pat on the Raspberry Pi) connected to a radio. What FieldCommand '
        'gives you is the <b>Winlink Form Import</b> page: it takes the ICS form that '
        'arrived (or that you sent) in Winlink and files it into the permanent incident '
        'record on the server, so the traffic that came in over the air becomes part of '
        'the same archive as everything else the incident produced. This chapter is '
        'about that import page and how to feed it.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: get the ICS form out of your Winlink program as a file or as '
        'copied text, drop it on the Winlink Form Import page, check the fields, tag it '
        'to the incident, and save it into the record.', 'tip'))
    s.append(SP(6))

    s.append(P('27.1  What This Page Is For', H2))
    s.append(P(
        'Open <b>Winlink Form Import</b> from the dashboard. The banner at the top reads '
        '<b>WINLINK FORM IMPORT</b>, with the line "Bring Winlink Express ICS form data '
        'into the incident record on the server." The page is a simple three-step column: '
        '<b>Step 1</b> - provide the form data, <b>Step 2</b> - review and correct the '
        'extracted data, and <b>Step 3</b> - tag to incident and file. Steps 2 and 3 stay '
        'hidden until you have parsed a form in Step 1, so at first you only see Step 1.'))
    s.append(P(
        'The page understands three ICS forms it can fully re-render: the <b>ICS-213 '
        'General Message</b>, the <b>ICS-214 Activity Log</b>, and the <b>ICS-309 '
        'Communications Log</b>. Any other Winlink form is still captured and archived - '
        'you just cannot open it back into a printable ICS page.'))
    s.append(SP(6))

    s.append(P('27.2  Getting the Form Out of Winlink', H2))
    s.append(P(
        'Before you touch FieldCommand, you need the form data out of your Winlink '
        'program. You have two ways to hand it over, and both work for messages you '
        'received and messages you sent.'))
    s.append(SP(4))
    s += steps([
        'In Winlink Express, open the message that carries the ICS form.',
        'Either <b>save the attached file</b> - it is named like '
        '<code>RMS_Express_Form_*.xml</code>; right-click the attachment and choose '
        '<b>Save</b> - <b>or</b> select and <b>copy the message text</b>.',
        'Keep that file handy (or keep the text on the clipboard) for the next step.',
    ])
    s.append(note(
        'The saved <b>XML</b> file is the better choice when you have it: it carries the '
        'form field-by-field, so FieldCommand fills every box cleanly. Copied message '
        'text still works, but the page has to guess the fields from the layout, so check '
        'the result more carefully.', 'note'))
    s.append(SP(6))

    s.append(P('27.3  Step 1 - Provide the Form Data', H2))
    s.append(P(
        'Step 1 has a dashed <b>drop box</b> that reads "Drop an '
        '<code>RMS_Express_Form_*.xml</code> file here, or click to browse," a line that '
        'says "- or paste below -," and a large paste box under it.'))
    s.append(SP(4))
    s += steps([
        'To use the saved file: drag it onto the drop box, or click the drop box to open '
        'a file picker and choose it. The page reads the file and parses it right away.',
        'To use copied text instead: click in the paste box (its placeholder reads "Paste '
        'the form XML or the Winlink message text here...") and paste, then click '
        '<b>Parse Form Data</b>.',
        'If you picked the wrong thing, click <b>Clear</b> to empty the box and start over.',
    ])
    s.append(P(
        'The moment a form is recognized, Step 2 and Step 3 appear below.'))
    s.append(SP(6))

    s.append(P('27.4  Step 2 - Review and Correct the Data', H2))
    s.append(P(
        'Step 2 is where you make sure the machine read the form correctly before it goes '
        'into the permanent record. At the top is a colored <b>detection banner</b> that '
        'tells you what kind of form the page thinks it is:'))
    s.append(SP(4))
    s.append(tbl(['BANNER COLOR', 'WHAT IT MEANS'], [
        ['Green (recognized)',
         'The page identified the form - "Detected an ICS-213 General Message form," or '
         'the ICS-214 or ICS-309 equivalent. The fields below are filled in and ready to '
         'check.'],
        ['Amber (not recognized)',
         'The form type could not be identified automatically. The data is still captured '
         'and can be archived, but re-rendering back into a printable ICS page works only '
         'for the ICS-213, ICS-214, and ICS-309.'],
        ['Red (nothing found)',
         'No form data was found at all. You probably pasted the wrong thing - go back to '
         'Step 1 with the RMS_Express_Form XML or the actual form message.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        'Under the banner is a grid of the form fields, each already filled in with what '
        'the page extracted. Every box is editable - correct anything that came across '
        'wrong or blank, exactly as you would fix a typo, before you file it. The long '
        'fields (the message body, activities, reply, and log) are shown as multi-line '
        'boxes.'))
    s.append(SP(6))

    s.append(P('27.5  The Three Recognized Forms and Their Fields', H2))
    s.append(P(
        'Which fields appear in the review grid depends on the form the page detected. '
        'The tables below list them with a plain-language meaning.'))
    s.append(SP(4))

    s.append(P('27.5.1  ICS-213 General Message', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident', 'The incident this message belongs to.'],
        ['To (Name) / To (Position)', 'Who the message is addressed to, and their ICS role.'],
        ['From (Name) / From (Position)', 'Who sent it, and their ICS role.'],
        ['Message #', 'The message number the sender assigned.'],
        ['Date / Time', 'When the message was written.'],
        ['Subject', 'The one-line subject of the message.'],
        ['Message Text', 'The body - the actual message.'],
        ['Approved By / Approver Position', 'Who released the message, and their role.'],
        ['Reply / Replied By / Reply Date/Time',
         'The reply half of the ICS-213, if the form carried one.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))

    s.append(P('27.5.2  ICS-214 Activity Log', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident', 'The incident this log belongs to.'],
        ['Unit Name', 'The unit or position the log covers.'],
        ['Unit Leader / Leader Position', 'Who led the unit, and their title.'],
        ['Op Period From / To', 'The operational period the log covers.'],
        ['Time From / Time To', 'The start and end clock times within that period.'],
        ['Prepared By / Prep Position', 'Who filled the log out, and their role.'],
        ['Activities', 'The chronological list of what happened.'],
        ['Personnel', 'The people assigned to the unit.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))

    s.append(P('27.5.3  ICS-309 Communications Log', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Incident', 'The incident this radio log belongs to.'],
        ['Op Period From / To', 'The operational period the log covers.'],
        ['Task No.', 'The task or assignment number, if used.'],
        ['Operator', 'The radio operator who kept the log.'],
        ['Station / Net', 'The station or net name the log came from.'],
        ['Page', 'The page number.'],
        ['Log Entries (raw)',
         'The block of log lines. When you open this into the ICS-309 page, FieldCommand '
         'splits it into date/time, from, to, and subject columns automatically.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('27.6  Fields Not Automatically Mapped', H2))
    s.append(P(
        'Winlink forms vary by version, so some fields may not line up with a known ICS '
        'box. When that happens, an amber panel titled <b>Fields not automatically '
        'mapped</b> appears under the grid, listing each leftover field and its value. '
        'These are <b>not lost</b> - the page keeps them and stores them with the archived '
        'record. Read the list in case one of them really belongs in a box above; if so, '
        'copy the value up into the correct field by hand before you file. Pure Winlink '
        'plumbing (version stamps and the like) is filtered out and never shown here.'))
    s.append(SP(6))

    s.append(P('27.7  Step 3 - Tag to Incident and File', H2))
    s.append(P(
        'Step 3 decides where the form lands and what you do with it. It has two drop-down '
        'menus and two action buttons.'))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Incident',
         'Choose which incident this form is filed under. The list is pulled live from '
         'the ICS platform. If there is no active incident, it files to the general '
         'archive instead.'],
        ['Direction',
         'Mark the traffic as <b>Received (incoming traffic)</b> or <b>Sent (outgoing '
         'traffic)</b>, so the record shows which way the message went.'],
        ['Open in ICS form (print)',
         'Opens the form back into its matching ICS page (ICS-213, ICS-214, or ICS-309) '
         'in a new tab, filled in and ready to print. Available for those three forms '
         'only.'],
        ['Archive to incident',
         'Saves the reviewed form - fields, unmapped extras, direction, and the original '
         'raw text - into the permanent incident record on the server.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(P(
        'After you click <b>Archive to incident</b>, a line under the buttons confirms it '
        'was filed and names the form type and direction. Archiving is the step that makes '
        'the message a durable part of the incident record - do it even when you also open '
        'the form to print, because printing alone does not save anything to the server.'))
    s.append(note(
        'The two buttons do different jobs. <b>Open in ICS form</b> gives you a printable '
        'page. <b>Archive to incident</b> writes it into the record. For traffic you want '
        'to keep - which, on an incident, is all of it - always archive.', 'tip'))
    s.append(SP(6))

    s.append(P('27.8  If the Server Cannot Be Reached', H2))
    s.append(P(
        'If you click <b>Archive to incident</b> and the server is unreachable, the page '
        'does not throw the form away. It saves a local copy on the device you are using '
        'and shows an amber line telling you the server was unreachable and to re-archive '
        'when it is back. When the server returns, open the form again and archive it so '
        'the permanent record on the server is complete - the local copy is only a safety '
        'net on that one device, not the archive.'))
    s.append(SP(6))

    s.append(P('27.9  Winlink Client Options (Background)', H2))
    s.append(P(
        'FieldCommand imports the form; a separate Winlink program does the sending and '
        'receiving over radio. The common choices, for reference:'))
    s.append(SP(4))
    s.append(tbl(['CLIENT', 'RUNS ON', 'TYPICAL PATHS'], [
        ['Winlink Express', 'Windows laptop',
         'VARA HF, VARA FM, Telnet, Pactor'],
        ['Pat', 'Raspberry Pi / Linux',
         'VARA FM (via Wine), Telnet, packet (AX.25)'],
    ], widths=[1.4*inch, 1.5*inch, CW-2.9*inch]))
    s.append(P(
        'Whichever client you use, the import step is the same: get the ICS form out as a '
        'file or copied text, then bring it into this page.'))
    s.append(SP(6))

    s.append(P('27.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Red banner - "Could not find any form data"',
         'You pasted the wrong text. Go back to Winlink, save the '
         'RMS_Express_Form_*.xml attachment (or copy the actual form message), and try '
         'Step 1 again.'],
        ['Amber banner - form type not recognized',
         'The form is not one of the three the page re-renders. You can still Archive it '
         '- the data is captured - but the "Open in ICS form" button will not work for it.'],
        ['Fields came across blank or wrong',
         'Use the saved XML file rather than copied message text; if you only have text, '
         'fix each box by hand in Step 2 before archiving.'],
        ['An amber "Fields not automatically mapped" panel appeared',
         'That is normal for some form versions. The data is preserved with the archive; '
         'copy anything that belongs in a real field up into the grid before you file.'],
        ['Incident menu shows "no active incident"',
         'The ICS platform has no incident running, or is unreachable. The form files to '
         'the general archive; start or open an incident first if you want it tagged there.'],
        ['Amber line - "Server unreachable - saved a local copy"',
         'Nothing is lost, but it is only on this device. When the server is back, open '
         'the form again and click Archive to incident so the server record is complete.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch28():
    s = chapter(28, 'Amateur Packet Radio Network (AMPRNet) / 44Net Gateway',
                'http://192.168.50.1/amprgate.html')

    # -- Does this apply to your deployment? ------------------------------------
    s.append(note(
        '<b>This chapter applies only to deployments that include an amateur radio '
        'group as the lead or a key partner.</b> '
        'If your deployment is operated entirely by a public safety agency, '
        'municipality, or served organization without a licensed amateur radio group '
        'involved, the AMPRNet gateway does not apply to you -- skip this chapter. '
        'FieldCommand IMS runs fully and completely without AMPRNet. '
        'All tools, ICS forms, net loggers, FEMA documentation, personnel '
        'accountability, and every other feature operate on EMCOMM-NET with '
        'no dependency on AMPRNet whatsoever.',
        'warn'))
    s.append(SP(6))

    s.append(P(
        "The AMPRNet / 44Net Gateway page is a live status board for a completely "
        "separate piece of hardware: a second, dedicated gateway Raspberry Pi at address "
        "192.168.50.2 that carries amateur radio internet traffic. AMPRNet -- the Amateur "
        "Packet Radio Network -- is the global amateur radio Internet Protocol (IP) network "
        "operating on the 44.0.0.0/8 address block permanently assigned by the Internet "
        "Assigned Numbers Authority (IANA) to Amateur Radio Digital Communications (ARDC) "
        "for amateur radio use. The ARDC gateway (<b>amprgw.ampr.org:51820</b>) provides a "
        "WireGuard-encrypted tunnel into that network over the internet. When the gateway Pi "
        "is configured and the tunnel is up, every device on EMCOMM-NET can reach AMPRNet "
        "resources -- Winlink gateways, APRS Internet Service (APRS-IS) servers, and other "
        "amateur stations worldwide that live on 44.x.x.x addresses. This page is where you "
        "watch that tunnel, read its traffic counters, see who is connected, and (only from "
        "the gateway Pi keyboard) bring the tunnel up or down.", Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: this page tells you at a glance whether the amateur radio '
        'internet gateway is up, how much data it is moving, and who is connected -- '
        'and it is the only place, from the gateway Pi itself, to control that tunnel.',
        'tip'))
    s.append(SP(4))
    s.append(P(
        'The gateway Pi is completely isolated from the primary FieldCommand server. '
        'If it goes down or is never deployed, nothing else on EMCOMM-NET is affected -- '
        'the dashboard, ICS forms, and every other tool keep working normally.'))
    s.append(SP(8))

    s.append(P('28.1  Who Should Deploy AMPRNet?', H2))
    s.append(tbl(['SITUATION', 'DEPLOY AMPRNET?'], [
        ['ARES/RACES group leads or co-leads the deployment',
         'Yes -- Winlink via the AMPRNet path, APRS-IS, and inter-node data. '
         'Licensed operators handle the registration under their callsign.'],
        ['Amateur radio club operates the EOC comms section',
         "Yes -- same benefits. A club callsign (for example, W9XYZ) is preferable "
         "for organizational deployments."],
        ['Licensed amateurs are supporting partners with the served agency',
         'Consider -- only if the licensed operators take full ownership '
         'of the AMPRNet registration and its ongoing maintenance.'],
        ['Public safety agency only -- no amateur radio group involved',
         'Not applicable -- an FCC amateur license is required for registration. '
         'AMPRNet is a Part 97 resource; it cannot be registered or operated '
         'by a non-licensed agency.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(8))

    s.append(P('28.2  The Amateur Radio Group Must Lead This', H2))
    s.append(P(
        'AMPRNet IP addresses are assigned to a licensed amateur callsign and governed '
        'by Part 97 of the Federal Communications Commission (FCC) rules. The registration '
        'process, the ongoing maintenance, and all operational use must be led by the '
        'amateur radio group -- not the served agency, not the EOC information technology '
        '(IT) department, and not the municipality. The practical steps are:'))
    s.append(SP(4))
    s.append(tbl(['STEP', 'WHO'], [
        ['Designate a licensed technical lead (any FCC license class)',
         'ARES EC or club President'],
        ['Contact the regional AMPRNet coordinator before registering',
         'Technical lead'],
        ['Register at portal.ampr.org using the club or personal callsign',
         'Technical lead'],
        ['Request a /29 subnet (6 usable IPs) or a /28 (14 IPs)',
         'Technical lead -- allow 2 to 6 weeks for approval'],
        ['Download the WireGuard config and set up the gateway Pi',
         'Technical lead -- see Installation Guide Step 11'],
        ['Maintain the portal account and license going forward',
         'Technical lead plus a designated backup'],
    ], widths=[3.5*inch, CW-3.5*inch]))
    s.append(SP(8))

    s.append(P('28.3  What AMPRNet Enables', H2))
    s.append(tbl(['CAPABILITY', 'DESCRIPTION'], [
        ['Winlink via AMPRNet path',
         'Reach Winlink Radio Message Server (RMS) gateways at 44.x.x.x addresses without '
         'using the commercial internet -- keeps message handling within the amateur network.'],
        ['APRS-IS via AMPRNet',
         'APRS-IS servers are reachable on 44.x.x.x. Direwolf can use the AMPRNet path '
         'instead of the public internet.'],
        ['Inter-node FieldCommand',
         'Two FieldCommand deployments, each with a 44Net gateway, can share net log data '
         'and resource status over AMPRNet -- no commercial internet required.'],
        ['Global amateur station reach',
         'Any amateur station worldwide with a 44.x.x.x address is directly '
         'reachable from any EMCOMM-NET device.'],
        ['Permanent static IPs',
         'Your 44.x.x.x block is yours permanently -- fixed addresses that never '
         'change regardless of internet provider or location.'],
    ], widths=[1.8*inch, CW-1.8*inch]))
    s.append(SP(6))
    s.append(note(
        '<b>Part 97 applies to all AMPRNet traffic:</b> no encryption of message content '
        '(the WireGuard tunnel encryption of the transport layer is permitted), '
        'no commercial traffic, and station identification is required. '
        'All use must comply with Part 97 rules.',
        'note'))
    s.append(SP(8))

    s.append(P('28.4  Opening the Page and Reading the Hero Banner', H2))
    s.append(P(
        'Open the gateway page from the dashboard, or type '
        'http://192.168.50.1/amprgate.html into any browser on EMCOMM-NET. '
        'The header reads <b>AMPRNet / 44Net Gateway</b>; the <b>Dashboard</b> link at the '
        'top right returns you to the main menu. The page fetches status the moment it '
        'loads and again every 30 seconds on its own -- the line <b>Last polled</b> at the '
        'top right tells you when the figures were last refreshed.'))
    s.append(SP(4))
    s.append(P(
        'The large colored banner near the top -- the hero banner -- is the one thing to '
        'read first. Its color and words tell you the tunnel state at a glance:'))
    s.append(SP(4))
    s.append(tbl(['BANNER', 'WHAT IT MEANS'], [
        ['Green -- TUNNEL UP, AMPRNet Connected',
         'The WireGuard tunnel is established. The banner also shows your assigned '
         'AMPRNet address. AMPRNet resources are reachable from EMCOMM-NET.'],
        ['Red -- TUNNEL DOWN',
         'The gateway Pi is responding but the tunnel is not established. '
         'AMPRNet is not reachable. Bring it up from the gateway Pi keyboard (28.8).'],
        ['Gray -- Gateway Unreachable',
         'The gateway Pi at 192.168.50.2 is not responding at all. Check that it is '
         'powered on and connected. The banner reads "not responding -- is it powered on?"'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(SP(8))

    s.append(P('28.5  The Status Cards', H2))
    s.append(P(
        'Below the banner is a grid of small cards, each a single live figure read from the '
        'gateway Pi. A dash (-) means the value is not available yet -- usually because the '
        'tunnel is down or the gateway is unreachable.'))
    s.append(SP(4))
    s.append(tbl(['CARD', 'WHAT IT SHOWS'], [
        ['AMPRNet Address',
         'The 44.x.x.x/29 address assigned to your gateway. Blank until the tunnel comes '
         'up and an address is assigned.'],
        ['Last Handshake',
         'When the WireGuard peer was last in contact. A recent time means the tunnel is '
         'alive and passing keep-alives.'],
        ['Data Received',
         'Total bytes received through the AMPRNet tunnel, shown in B, KB, MB, or GB.'],
        ['Data Sent',
         'Total bytes sent through the AMPRNet tunnel.'],
        ['Gateway CPU Temp',
         'The gateway Pi processor temperature in degrees Celsius -- a health check on the '
         'gateway hardware.'],
        ['Gateway Memory',
         'Memory used versus total on the gateway Pi, in megabytes (MB).'],
        ['IP Forwarding',
         'Shows Enabled (green) or DISABLED (red). This must be Enabled for the gateway to '
         'route 44Net traffic; DISABLED in red means routing is broken even if the tunnel is up.'],
        ['Gateway Uptime',
         'How long the gateway Pi has been running since its last reboot.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))
    s.append(note(
        'If <b>IP Forwarding</b> shows <b>DISABLED</b> in red while the tunnel is UP, '
        'devices on EMCOMM-NET still will not reach 44Net. Forwarding is set on the gateway '
        'Pi during Installation Guide Step 11; have the technical lead check it there.',
        'warn'))
    s.append(SP(8))

    s.append(P('28.6  Active Routes and Connected Peers', H2))
    s.append(P(
        'Two tables in the middle of the page show the plumbing behind the tunnel.'))
    s.append(SP(4))
    s.append(P('28.6.1  Active Routes', H3))
    s.append(P(
        'The <b>Active Routes</b> table lists the network routes the gateway is advertising. '
        'A green dot and <b>Active</b> means the route is in place; a red dot and '
        '<b>Not routed</b> means it is missing. If the table reads '
        '"No 44Net routes found," the tunnel is most likely down.'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['NETWORK', 'The destination network being routed, such as the 44.0.0.0/8 block.'],
        ['VIA', 'The interface or next hop the traffic travels through.'],
        ['STATUS', 'Green dot with Active, or red dot with Not routed.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(4))
    s.append(P('28.6.2  Connected Peers', H3))
    s.append(P(
        'The <b>Connected Peers</b> table lists the WireGuard peers. When the tunnel is down '
        'or no peers are configured, it reads "No peers configured."'))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT MEANS'], [
        ['PEER', 'The peer public key that identifies the far end.'],
        ['ENDPOINT', 'The internet address and port of the peer.'],
        ['ALLOWED IPs', 'The IP ranges this peer is allowed to carry.'],
        ['LAST HANDSHAKE', 'When this peer was last in contact.'],
        ['STATUS', 'Green dot with Connected, or red dot with Idle.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(8))

    s.append(P('28.7  The Access Log and Part 97 Access Control', H2))
    s.append(P(
        'The <b>Access Log</b> section shows the recent gateway logins and station '
        'identifications, kept for Part 97 record-keeping. The gateway enforces access '
        'control: only a licensed amateur operator with a valid FCC callsign may '
        'authenticate, and each callsign is validated against the offline FCC database. '
        'Every access attempt is recorded -- callsign, IP address, timestamp, and result -- '
        'and a login session lasts 8 hours before it must be renewed. When there is nothing '
        'to show, the section reads "No access-log entries yet."'))
    s.append(SP(8))

    s.append(P('28.8  Tunnel Control (Gateway Pi Only)', H2))
    s.append(P(
        'The <b>Tunnel Control</b> section holds the buttons that start and stop the tunnel. '
        'By deliberate design, these buttons only work when this page is open in the '
        'Chromium browser on the gateway Pi itself -- never from an operator laptop or phone '
        'on EMCOMM-NET. A valid callsign login is also required. This keeps a single, '
        'physically present, licensed operator in control of the amateur radio link.'))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['Bring Tunnel UP', 'Establishes the WireGuard tunnel to AMPRNet.'],
        ['Bring Tunnel DOWN', 'Tears the tunnel down and stops carrying 44Net traffic.'],
        ['Restart Tunnel', 'Brings the tunnel down and back up -- the usual first fix.'],
        ['Refresh Status', 'Re-reads the gateway now instead of waiting for the 30-second poll.'],
        ['Open Gateway Dashboard',
         'Opens the gateway Pi own status page directly at http://192.168.50.2:9000 '
         'in a new tab.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P('To actually control the tunnel:'))
    s += steps([
        'Sit down at the <b>gateway Pi</b> keyboard (the second Pi, at 192.168.50.2).',
        'Open the <b>Chromium</b> browser on that Pi.',
        'Go to <b>http://localhost:9001</b> and log in with your amateur radio callsign.',
        'Use <b>Bring Tunnel UP</b>, <b>Bring Tunnel DOWN</b>, or <b>Restart Tunnel</b> '
        'as needed. The message line under the buttons reports the result.',
    ])
    s.append(note(
        'If you press a control button from an operator laptop or phone, the page tells you '
        'the control requires physical access to the gateway Pi keyboard, or asks you to log '
        'in with your callsign first. This is expected -- it is not a fault. Only the '
        'read-only status view (port 9000) is available from other EMCOMM-NET devices.',
        'note'))
    s.append(SP(8))

    s.append(P('28.9  About This Gateway', H2))
    s.append(P(
        'The <b>About This Gateway</b> table at the bottom of the page is a quick reference '
        'card of the fixed facts about your gateway:'))
    s.append(SP(4))
    s.append(tbl(['ITEM', 'VALUE'], [
        ['Gateway Pi IP', '192.168.50.2'],
        ['Gateway status API', 'http://192.168.50.2:9000/api/status'],
        ['AMPRNet block', 'Your assigned 44.x.x.x/29 (fills in once the tunnel is up)'],
        ['WireGuard endpoint', 'amprgw.ampr.org:51820'],
        ['What it routes', 'All 44.0.0.0/8 traffic for every device on EMCOMM-NET'],
        ['AMPRNet portal', 'https://portal.ampr.org'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(note(
        'Full AMPRNet setup procedures -- WireGuard configuration, IP forwarding, '
        'route advertisement, and the verification checklist -- are in '
        'Installation Guide Step 11. Portal registration: portal.ampr.org. '
        'WireGuard gateway endpoint: amprgw.ampr.org:51820.',
        'note'))
    s.append(SP(8))

    s.append(P('28.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The banner is gray and says "Gateway Unreachable / not responding."',
         'The gateway Pi at 192.168.50.2 is off or disconnected. Check that it is powered '
         'on and on the same network, then press Refresh Status. Remember the gateway is a '
         'second, separate Pi from the main FieldCommand server.'],
        ['The banner is red -- TUNNEL DOWN -- but the cards show gateway temp and memory.',
         'The gateway Pi is up but the tunnel is not established. At the gateway Pi keyboard, '
         'open http://localhost:9001, log in with your callsign, and use Restart Tunnel.'],
        ['IP Forwarding shows DISABLED in red even though the tunnel is UP.',
         'Routing is off, so EMCOMM-NET devices still cannot reach 44Net. Forwarding is set '
         'on the gateway Pi in Installation Guide Step 11 -- have the technical lead re-check it.'],
        ['I press a control button from my laptop and nothing happens.',
         'Tunnel control only works from the Chromium browser on the gateway Pi itself '
         '(port 9001, localhost). This is by design. Use the gateway Pi keyboard, or just '
         'watch the read-only status from your laptop.'],
        ['The control buttons say "Login required -- enter your callsign first."',
         'You are on the gateway Pi but not logged in. Log in at http://localhost:9001 with '
         'a valid FCC amateur callsign; sessions last 8 hours and then need renewing.'],
        ['Active Routes reads "No 44Net routes found" and Connected Peers is empty.',
         'These both point to a tunnel that is down or never brought up. Bring the tunnel up '
         'from the gateway Pi, then press Refresh Status; the routes and peers should populate.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(PB())
    return s


def ch29():
    s = chapter(29, 'JS8Call — High Frequency (HF) Digital Messaging',
                'http://192.168.50.1/')
    s.append(P(
        "JS8Call is a weak-signal High Frequency (HF) digital mode for keyboard-to-keyboard "
        "messaging and store-and-forward relay. When the local infrastructure is gone and "
        "even Very High Frequency (VHF) repeaters are down, JS8Call can still carry short "
        "text messages hundreds or thousands of miles on HF, using signals so weak a human "
        "ear could not hear them. It does not run inside FieldCommand. It runs on a separate "
        "Windows laptop that is wired to the incident HF transceiver and joined to the same "
        "EMCOMM-NET network, and FieldCommand gives you a one-tap link to reach it. This "
        "chapter explains what JS8Call does, how the laptop fits into your station, how to "
        "point the dashboard card at that laptop, and how to fold the messages it receives "
        "into the permanent incident record.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: JS8Call is your long-haul text lifeline on HF radio, run from a "
        "Windows laptop next to the radio, and the FieldCommand dashboard has a card that "
        "opens it.", 'tip'))
    s.append(SP(6))

    s.append(P('29.1  What JS8Call Does for Emergency Communications (EMCOMM)', H2))
    s.append(P(
        "JS8Call was built for exactly the kind of long-distance, no-infrastructure "
        "messaging an incident needs when everything else fails. Its main capabilities are "
        "below."))
    s.append(SP(4))
    s.append(tbl(['CAPABILITY', 'WHAT IT GIVES YOU'], [
        ['Keyboard messaging',
         'Real-time, chat-style text between stations. You type a message, the radio sends '
         'it as tones, and the receiving station reads it on screen.'],
        ['Store and forward',
         'A message can be held at a relay station and passed along automatically when the '
         'destination station is finally heard, so you reach places you cannot hear directly.'],
        ['Heartbeat beacons',
         'The software sends a short automatic beacon every few minutes that announces your '
         'station and shows who can hear whom, which reveals live propagation.'],
        ['Group messages',
         'A message addressed to a group name such as @EMCOMM, @ARES, or @RACES reaches '
         'every station monitoring that group at once.'],
        ['Extreme sensitivity',
         'Copies signals down to roughly -24 decibels signal-to-noise ratio (SNR) — far '
         'weaker than a Single Sideband (SSB) voice signal you could understand by ear.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('29.2  How the JS8Call Laptop Fits Into Your Station', H2))
    s.append(P(
        "JS8Call is not part of the Raspberry Pi that runs FieldCommand. It lives on its own "
        "Windows laptop for one practical reason: the laptop is what is physically wired to "
        "the HF radio through a Universal Serial Bus (USB) sound-and-control interface. A "
        "typical setup is an IC-7300 transceiver connected to the laptop with a Digirig or a "
        "similar USB audio interface, with JS8Call installed on the laptop. The laptop then "
        "joins the same EMCOMM-NET Wi-Fi as everything else, so operators at other "
        "FieldCommand screens can reach it over the network."))
    s.append(SP(4))
    s.append(tbl(['PIECE', 'ROLE'], [
        ['HF transceiver',
         'The radio that actually transmits and receives on the HF bands (for example an '
         'IC-7300).'],
        ['USB audio interface',
         'The Digirig (or similar) that carries receive audio, transmit audio, and '
         'push-to-talk keying between the radio and the laptop.'],
        ['Windows laptop',
         'Runs the JS8Call program itself. This is the machine whose network address you '
         'give to the dashboard card.'],
        ['EMCOMM-NET network',
         'The shared Wi-Fi. Both the laptop and every FieldCommand screen sit on it, which '
         'is what lets the dashboard reach the laptop.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(note(
        "JS8Call transmits on the amateur radio bands, so it may be operated only by a "
        "properly licensed operator with privileges on the bands and modes in use. A group "
        "with no licensed operator leaves the callsign blank and does not use this feature.",
        'warn'))
    s.append(SP(6))

    s.append(P('29.3  The JS8Call Card on the Dashboard', H2))
    s.append(P(
        "On the FieldCommand dashboard, switch to <b>Amateur Radio</b> mode. Among the "
        "operator cards you will see a purple <b>JS8Call</b> card with a radio-antenna icon. "
        "It is a shortcut, not the program — tapping it opens the JS8Call laptop in a new "
        "browser tab. The card shows the parts below."))
    s.append(SP(4))
    s.append(tbl(['CARD ELEMENT', 'WHAT IT SHOWS'], [
        ['Name',
         'JS8Call — the label of the card.'],
        ['Description',
         '"HF digital messaging via keyboard" — a one-line reminder of what it is.'],
        ['Port label',
         'Reads <b>Port 2442</b> until you configure the laptop address. Once set, it shows '
         'the laptop address and port, such as 192.168.50.2:2442.'],
        ['Status line',
         'A small line under the port. Before setup it warns "Windows laptop — tap to '
         'configure IP". After setup it shows "Windows:" and the address you entered.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(note(
        "The Amateur Radio mode button is grayed out until a station callsign is set in "
        "Setup. If you do not see the JS8Call card, add a callsign first (see the Setup "
        "chapter), then return to the dashboard and choose Amateur Radio mode.", 'note'))
    s.append(SP(6))

    s.append(P('29.4  Telling the Card Where the Laptop Is', H2))
    s.append(P(
        "The card cannot guess which laptop on the network is running JS8Call, so the first "
        "time you use it you tell it the laptop network address. You do this once per screen; "
        "the address is remembered in that browser."))
    s += steps([
        "On the JS8Call laptop, find its network address: click the Start menu, type "
        "<b>cmd</b>, press Enter, type <b>ipconfig</b>, and press Enter. Read the "
        "<b>IPv4 Address</b> line — it looks like 192.168.50.2.",
        "On the FieldCommand dashboard, in Amateur Radio mode, tap the <b>JS8Call</b> card.",
        "A small box asks for the address of the Windows laptop running JS8Call. Type the "
        "IPv4 Address you just read (for example 192.168.50.2) and click OK.",
        "The card now remembers that address: its port label changes to that address with "
        ":2442 after it, and the status line reads \"Windows:\" and the address. JS8Call "
        "also opens in a new browser tab.",
    ])
    s.append(note(
        "To clear a wrong address, tap the card again and leave the box empty, then click "
        "OK. The card returns to showing \"Port 2442\" and the configure-IP warning, ready "
        "for you to enter the correct address.", 'tip'))
    s.append(SP(6))

    s.append(P('29.5  Opening JS8Call from the Dashboard', H2))
    s.append(P(
        "Once the address is set, tapping the card opens the JS8Call laptop at port 2442 in "
        "a new browser tab. Port 2442 is the address JS8Call listens on. Note that the "
        "keyboard operating — typing and reading messages — is done at the laptop itself, on "
        "the JS8Call program window. The dashboard card is the quick way to jump to that "
        "machine and to keep its address handy for everyone at the incident."))
    s.append(SP(4))
    s.append(note(
        "If the new tab does not open, your browser may have blocked the pop-up. Allow "
        "pop-ups for the FieldCommand address (192.168.50.1) and tap the card again, or "
        "simply walk to the laptop and use JS8Call there.", 'note'))
    s.append(SP(6))

    s.append(P('29.6  Sending a Message on HF Digital', H2))
    s.append(P(
        "Operating happens in the JS8Call program on the laptop. The general flow of a "
        "single message is the same every time."))
    s += steps([
        "Make sure the radio is on the agreed HF frequency and band for your net, and that "
        "JS8Call shows signals scrolling in its waterfall display (the moving picture of "
        "activity across the channel).",
        "In the message box, type the callsign of the station you are calling, then your "
        "text. Keep it short — HF digital is slow, so every extra word costs time on the air.",
        "Send the message. The radio keys up and plays the tones; a progress indicator shows "
        "the message going out.",
        "Watch the receive area for the other station to answer. Their reply appears as text "
        "as it decodes.",
        "For a message to a whole group, address it to the group name (for example @EMCOMM) "
        "instead of a single callsign, so every monitoring station in that group receives it.",
    ])
    s.append(SP(6))

    s.append(P('29.7  Directed Calls and Group Names', H2))
    s.append(P(
        "JS8Call lets you aim a message at one station or at a named group. The common "
        "emergency group names are below; your net may agree on others."))
    s.append(SP(4))
    s.append(tbl(['ADDRESS', 'WHO RECEIVES IT'], [
        ['A single callsign',
         'Only the station with that callsign is being called, though others can still see '
         'the exchange.'],
        ['@EMCOMM',
         'Every station monitoring the general emergency-communications group.'],
        ['@ARES',
         'Stations monitoring the Amateur Radio Emergency Service group.'],
        ['@RACES',
         'Stations monitoring the Radio Amateur Civil Emergency Service group.'],
        ['@ALLCALL',
         'A general call to any station hearing you — used to find out who is on frequency.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('29.8  Bringing JS8Call Traffic Into the Incident Record', H2))
    s.append(P(
        "Incident data is permanent, so a message that arrives by HF digital should not live "
        "only on the laptop. Today the bridge between JS8Call and the incident record is "
        "done by hand, and that is deliberate: an operator reads the message and decides "
        "where it belongs."))
    s += steps([
        "Read the incoming message in JS8Call on the laptop.",
        "If it is formal traffic — a request, a report, a message with a sender and an "
        "addressee — open the <b>ICS-213 Message</b> page on the dashboard and type the "
        "message into a new ICS-213 General Message form, so it is saved and can be "
        "re-printed with the rest of the incident paperwork.",
        "If it is routine net traffic — a check-in, a status, a short exchange — enter it in "
        "the Net Control Logger instead, so it lands in the running log for the operational "
        "period.",
        "Note the time and the sending station exactly as JS8Call shows them, so the record "
        "matches what was on the air.",
    ])
    s.append(note(
        "A future FieldCommand release is planned to ingest JS8Call messages into the "
        "incident log directly. Until then, the manual copy step above is the correct "
        "practice — it keeps a person in control of what becomes an official record.", 'note'))
    s.append(SP(6))

    s.append(P('29.9  Good Operating Practice on HF Digital', H2))
    s.append(P(
        "HF digital rewards patience and short messages. A few habits keep a net running "
        "cleanly."))
    s.append(P("<b>Keep it short.</b> The mode is slow. Say only what is needed; abbreviate "
               "where your net has agreed abbreviations.", Bullet))
    s.append(P("<b>Listen before you transmit.</b> Watch the waterfall and the decode area "
               "so you do not send on top of another station.", Bullet))
    s.append(P("<b>Let heartbeats do their job.</b> The automatic beacons show who can hear "
               "whom; use that picture to pick a relay station when you cannot reach a "
               "destination directly.", Bullet))
    s.append(P("<b>Log as you go.</b> Copy anything that matters into the ICS-213 page or "
               "the Net Control Logger while it is fresh, not at the end of the shift.", Bullet))
    s.append(SP(6))

    s.append(P('29.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The JS8Call card is missing from the dashboard',
         'You are not in Amateur Radio mode, or no callsign is set. Choose Amateur Radio '
         'mode; if that button is grayed out, add a station callsign in Setup first.'],
        ['Tapping the card opens nothing',
         'The browser blocked the new tab. Allow pop-ups for 192.168.50.1 and tap again, or '
         'operate at the laptop directly.'],
        ['The card still says "Port 2442" and warns to configure the IP',
         'No laptop address is saved on this screen yet. Tap the card and enter the laptop '
         'IPv4 Address (find it with ipconfig on the laptop).'],
        ['The new tab opens but shows an error or blank page',
         'The address is wrong, JS8Call is not running, or the laptop is off the network. '
         'Confirm JS8Call is open on the laptop and re-check the address with ipconfig.'],
        ['No signals scroll in the JS8Call waterfall',
         'The radio audio is not reaching the laptop. Check the USB audio interface cabling '
         'and that JS8Call is set to the correct sound device and radio.'],
        ['A message came in but is not in the incident record',
         'JS8Call does not log to the incident automatically yet. Copy the message into the '
         'ICS-213 page (formal traffic) or the Net Control Logger (net traffic) by hand.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch30():
    s = chapter(30, 'National Traffic System (NTS) Radiogram Generator',
                'http://192.168.50.1/nts.html')
    s.append(P(
        "The National Traffic System (NTS) Radiogram Generator builds a properly "
        "formatted American Radio Relay League (ARRL) radiogram - the standard "
        "form for passing formal written messages by radio. When telephones, cell "
        "service, and the internet are down, a radiogram is how a short, exact "
        "message about a person's safety or an urgent request moves across the "
        "country, operator to operator, until it reaches the person it is for. "
        "This page fills in the message number, precedence, check (word count), and "
        "address for you, shows a clean printable form, and keeps a running log of "
        "every radiogram you have handled so nothing is lost.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: type the message, click Generate Radiogram, and you get a "
        "correctly formatted, printable NTS form with the word count filled in for you.",
        'tip'))
    s.append(SP(6))

    s.append(P('30.1  What a Radiogram Is and When to Use One', H2))
    s.append(P(
        "A radiogram carries one short message in a fixed format that every traffic "
        "handler in the country understands. Because the format never changes, an "
        "operator who receives your message can relay it word for word to the next "
        "station without confusion. Radiograms are used most heavily right after a "
        "disaster, when families outside the area want to know that relatives are "
        "safe (Health and Welfare traffic) and when officials need to move an urgent "
        "request that has no other path out."))
    s.append(P(
        "The message text is kept short on purpose - 25 words or fewer. Short "
        "messages relay quickly and accurately, and a whole net full of them clears "
        "faster. The generator counts your words as you type and warns you the moment "
        "you go over 25.", Body))
    s.append(SP(6))

    s.append(P('30.2  The Preamble (Header)', H2))
    s.append(P(
        "The <b>Preamble</b> card is the message header - the bookkeeping that "
        "travels ahead of the actual words. Fields marked with a star (*) are "
        "required. The <b>Check</b> field is filled in for you and cannot be typed "
        "into."))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Message Number *',
         'The sequential number of this message from your station, such as 001. '
         'Click Auto-fill Msg # to take the next number after your last saved one.'],
        ['Precedence *',
         'How urgent the message is - Routine, Welfare, Priority, or Emergency '
         '(see the table in 30.3). Choosing one shows a plain-language reminder of '
         'what it is for.'],
        ['Handling Instructions',
         'An optional service instruction (the HX codes) telling the delivering '
         'station how to handle the message - see 30.4. Leave it on None if there '
         'is no special instruction.'],
        ['HX Supplement (if any)',
         'The extra detail some handling codes need, such as a number of hours or a '
         "person's name. Leave blank when the chosen code needs nothing extra."],
        ['Station of Origin *',
         'The callsign of the station that first put the message into the system. '
         'Typed in capital letters automatically.'],
        ['Check (word count) *',
         'The number of words in the message text. Filled in and updated for you as '
         'you type; you cannot edit it by hand.'],
        ['Place of Origin *',
         'The city and state the message started from, such as COLUMBUS OH.'],
        ['Date / Time Filed *',
         'When the message was filed, such as 0930 JUN 7. Click Auto-fill '
         'Date/Time to insert the current time in Coordinated Universal Time (UTC).'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('30.3  Precedence - How Urgent the Message Is', H2))
    s.append(P(
        "Precedence tells every operator who touches the message how quickly it must "
        "move and which messages to pass first when a net is busy. The generator "
        "shows the matching reminder under the drop-down as soon as you pick one."))
    s.append(SP(4))
    s.append(tbl(['PRECEDENCE', 'WHAT IT IS FOR'], [
        ['R - Routine',
         'Normal message traffic with no urgency. The everyday default.'],
        ['W - Welfare',
         "A message about the health and welfare of a person, or an inquiry from a "
         "family member. Common after a disaster."],
        ['P - Priority',
         'Important traffic with some urgency - for example official or government '
         'messages that should not wait behind routine traffic.'],
        ['E - Emergency',
         'Any message with life-or-death urgency, a disaster declaration, or official '
         'government communications. Handled ahead of everything else.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('30.4  Handling Instructions (HX Codes)', H2))
    s.append(P(
        "The optional <b>Handling Instructions</b> drop-down carries the standard "
        "ARRL service codes. They tell the station that finally delivers the message "
        "what the sender wants done. Pick one only when it applies; most messages "
        "leave this on None."))
    s.append(SP(4))
    s.append(tbl(['CODE', 'WHAT IT ASKS THE DELIVERING STATION TO DO'], [
        ['HXA', 'Collect on delivery (a phone-call charge limit may apply).'],
        ['HXB', 'Cancel the message if it is not delivered within a set number of hours '
         '(put the hours in HX Supplement).'],
        ['HXC', 'Report the date and time of delivery back to the station of origin.'],
        ['HXD', 'Report the identity of the station the message came from, and the '
         'delivery route, back to the originating station.'],
        ['HXE', 'Ask the addressee whether there is a reply, and report it back.'],
        ['HXF', 'Hold the message for arrival of the addressee (put the date in '
         'HX Supplement).'],
        ['HXG', 'Deliver by mail or landline toll call. If that is not possible, cancel '
         'the message and report it back to the origin.'],
    ], widths=[1.0*inch, CW-1.0*inch]))
    s.append(note(
        "When a code needs a detail - hours for HXB, a name or date for HXF - type "
        "that detail into the HX Supplement box next to the drop-down.", 'note'))
    s.append(SP(6))

    s.append(P('30.5  Address, Message Text, and Signature', H2))
    s.append(P(
        "Below the preamble are three more cards that hold who the message is for, "
        "what it says, and who sent it."))
    s.append(SP(4))
    s.append(P('30.5.1  Address', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Addressee Name *', 'The person the message is for, such as John Smith. Required.'],
        ['Phone Number', 'The delivery phone number, if known - used by the station that '
         'finally delivers the message.'],
        ['Street Address', 'The street address for delivery.'],
        ['City', 'The delivery city.'],
        ['State / Zip', 'The delivery state and ZIP code, such as OH 43215.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P('30.5.2  Message Text', H3))
    s.append(P(
        "Type the message itself into the <b>Message Text</b> box. Use plain words "
        "and avoid punctuation - spell out the word X where you would put a period "
        "(for example, ARRIVED SAFELY X EVERYONE FINE X LOVE). Under the box a live "
        "<b>Word count</b> shows your total against the 25-word maximum; if you go "
        "over, the number turns red and the words over limit are flagged."))
    s.append(SP(4))
    s.append(P('30.5.3  Signature', H3))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Sender Name / Callsign', 'Who the message is from, such as Jane Smith / W8ABC. '
         'If left blank, the Station of Origin callsign is used.'],
        ['Phone / Email', 'A contact number or email for the sender, if wanted.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(6))

    s.append(P('30.6  Generating and Printing the Radiogram', H2))
    s.append(P(
        "The buttons at the bottom of the form build the finished radiogram. The "
        "generator will not proceed until the required fields are filled and the "
        "check is 25 words or fewer."))
    s.append(SP(4))
    s += steps([
        "Fill in at least the required fields: <b>Message Number</b>, "
        "<b>Station of Origin</b>, <b>Addressee Name</b>, and <b>Message Text</b>.",
        "Use <b>Auto-fill Date/Time</b> and <b>Auto-fill Msg #</b> if you want the "
        "current UTC time and the next message number filled in for you.",
        "Click <b>Generate Radiogram</b>. The form is replaced by a clean, black-on-"
        "white radiogram preview showing the preamble, the address, the message text "
        "in capitals, the signature, and blank received/sent tracking lines.",
        "Click <b>Print Radiogram</b> to print the form. Only the radiogram itself "
        "prints - the editing controls and the saved log are hidden on paper.",
        "To make a change, click <b>Edit</b> (the left-arrow button) to return to the "
        "form with your entries intact.",
    ])
    s.append(note(
        "If a required field is missing, or the check is over 25 words, a message "
        "tells you exactly what to fix. Shorten the text - spell out X for periods "
        "and drop non-essential words - until the check is 25 or fewer, then try "
        "again.", 'warn'))
    s.append(SP(6))

    s.append(P('30.7  Preview Actions - Save, Copy, and Send to the Net', H2))
    s.append(P(
        "Once the preview is showing, a row of action buttons appears beneath it:"))
    s.append(SP(4))
    s.append(tbl(['BUTTON', 'WHAT IT DOES'], [
        ['Print Radiogram', 'Opens your device print dialog and prints just the radiogram.'],
        ['Save to Log', 'Stores this radiogram in the Saved Radiograms table below and also '
         'sends a copy to the server forms record so the message is kept as part of the '
         'incident.'],
        ['Copy Text', 'Copies the full message - preamble, address, text, and signature - '
         'to the clipboard as plain text, ready to paste into another log or a digital mode.'],
        ['Send to Net Log', 'A reminder to record this message as a traffic entry in Net '
         'Control (open Net Control and use the Traffic Log tab).'],
        ['Edit (left arrow)', 'Returns to the form so you can change any field.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('30.8  The Saved Radiograms Log', H2))
    s.append(P(
        "At the bottom of the page the <b>Saved Radiograms</b> table lists every "
        "radiogram you have saved, newest first (the log keeps up to the most recent "
        "50). Each row shows the columns below. Use <b>Load Saved</b> at the top of "
        "the page to jump straight to this table."))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT SHOWS'], [
        ['#', 'The message number.'],
        ['Prec', 'The precedence, shown as a colored badge (R, W, P, or E).'],
        ['To', 'The addressee name.'],
        ['Origin', 'The station of origin callsign.'],
        ['Date Filed', 'The date and time the message was filed.'],
        ['Check', 'The word count.'],
        ['Load / X', 'Load reopens the saved radiogram in the form; the X button deletes '
         'that one row after you confirm.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(4))
    s.append(P(
        "The <b>Clear All</b> button on the Saved Radiograms header removes every "
        "saved radiogram after you confirm. The <b>New Form</b> button at the top of "
        "the page clears the current form and preview so you can start a fresh "
        "message without touching the log."))
    s.append(note(
        "Saving keeps a copy both on this device and on the FieldCommand server, so a "
        "radiogram you save is part of the permanent incident record even if this "
        "browser is later cleared.", 'note'))
    s.append(SP(6))

    s.append(P('30.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Generate Radiogram does nothing and a message pops up',
         'A required field is empty. Fill in Message Number, Station of Origin, '
         'Addressee Name, and Message Text, then click Generate again.'],
        ['The word count is red and it will not generate',
         'The message text is over the 25-word limit. Spell out X for periods and '
         'remove non-essential words until the count is 25 or fewer.'],
        ['The Check field will not let me type in it',
         'That is intended. The check is the word count and is filled in for you as '
         'you type the message; edit the message text to change it.'],
        ['The date/time or message number is blank',
         'Click Auto-fill Date/Time for the current UTC time, and Auto-fill Msg # for '
         'the next number after your last saved radiogram. You can also type either by '
         'hand.'],
        ['Printing shows the whole page, not just the form',
         'Click Generate Radiogram first so the preview is on screen, then Print. Only '
         'the radiogram preview is set to print; the form and log are hidden on paper.'],
        ['A saved radiogram disappeared from the log',
         'The log keeps the 50 most recent entries and older ones roll off. Radiograms '
         'you saved are also stored on the server as part of the incident record.'],
    ], widths=[2.6*inch, CW-2.6*inch]))
    s.append(PB())
    return s


def ch31():
    s = chapter(31, 'Repeater Database',
                'http://192.168.50.1/repeaters.html')
    s.append(P(
        "The Repeater Database is your offline directory of the VHF and UHF voice "
        "repeaters in and around your operating area. A repeater is an automated "
        "relay station on a hilltop or tower that listens on one frequency and "
        "re-transmits on another, greatly extending the range of a hand-held or "
        "mobile radio. This page lets you load a full county-or-region export from "
        "RepeaterBook, search and filter it in seconds, plot every machine on a map, "
        "and push the ones you will use straight into the Channel Library so they "
        "flow into your ICS-205 communications plan. Once the data is loaded it lives "
        "in this browser, so it keeps working with no internet at all.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: load a RepeaterBook export, filter to the repeaters you "
        "want, and one click sends any of them into your communications plan.", 'tip'))
    s.append(SP(6))

    s.append(P('31.1  How the Screen Is Laid Out', H2))
    s.append(P(
        "The page has five working areas, top to bottom. Knowing where each one "
        "lives makes the rest of this chapter quick to follow."))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IT IS'], [
        ['Source tabs',
         'A row of three tabs just under the title - <b>Offline File</b>, '
         '<b>Server API</b>, and <b>Demo Data</b> - that pick where the repeater '
         'data comes from. Each tab shows a small count of how many repeaters that '
         'source holds.'],
        ['Toolbar',
         'The search box, the filter drop-downs, and the action buttons '
         '(Add Repeater, Map View, CSV, Print). It stays hidden until data is loaded.'],
        ['Table',
         'The main list - one row per repeater, sortable by any column.'],
        ['Detail panel',
         'A slide-in panel on the right that shows everything about the one repeater '
         'you clicked, with Copy, Program, and Channel Library buttons.'],
        ['Status bar',
         'The thin strip pinned to the bottom of the window. On the left it shows '
         'how many repeaters match your filters out of the total; on the right it '
         'shows the current sort.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('31.2  Loading Repeater Data', H2))
    s.append(P(
        "The three source tabs are three different ways to get repeater data onto "
        "the page. For almost every deployment the <b>Offline File</b> tab is the "
        "right one - it needs only a free RepeaterBook account and no internet at "
        "the Pi."))
    s.append(SP(4))
    s.append(tbl(['SOURCE TAB', 'HOW TO USE IT', 'WHAT IT NEEDS'], [
        ['Offline File  (recommended)',
         'Log in at repeaterbook.com, search your county or area, and click '
         'Export then CSV. Drag the downloaded file onto the drop zone, or click '
         'the drop zone (or the "Load file" box) to browse for it.',
         'A free repeaterbook.com account. No API token - any logged-in user can '
         'download a CSV. RepeaterBook CSV, RepeaterBook JSON, and a FieldCommand '
         'repeaters.json file are all accepted.'],
        ['Server API  (optional)',
         'Switching to this tab calls the FieldCommand server, which serves '
         'whatever fetch_repeaters.py last downloaded. Place your token in '
         '/opt/fieldcommand/data/repeaterbook_token.txt, then run '
         'python3 scripts/fetch_repeaters.py on the Pi.',
         'An approved RepeaterBook API token - a separate application and approval, '
         'NOT the same as an account login. Apply at '
         'repeaterbook.com/api/token_request.php and allow several weeks.'],
        ['Demo Data',
         'Shows a handful of clearly-labeled SAMPLE placeholder entries so you can '
         'see how the page looks and behaves before real data is loaded.',
         'Nothing. These are not real repeaters and must never be used on the air.'],
    ], widths=[1.35*inch, 2.95*inch, CW-4.3*inch]))
    s.append(SP(4))
    s += steps([
        'Click the <b>Offline File</b> tab (it is selected by default).',
        'On your computer, open <b>repeaterbook.com</b>, sign in, search your area, '
        'and download the <b>Export - CSV</b> file.',
        'Drag that file onto the dashed drop zone, or click the drop zone to browse '
        'and pick it.',
        'A progress box reads the file and reports "Loaded N repeaters." The toolbar '
        'and table appear, and a green banner names the file and the import time.',
    ])
    s.append(note(
        "The RepeaterBook API token is not the same as a RepeaterBook login. It "
        "takes a separate application and staff approval. The CSV export works with "
        "any free account and is the method to use in the field. An imported file is "
        "remembered in this browser, so it is still there after a reload - but it is "
        "stored per-browser, not on the server, so each operator device imports its "
        "own copy (or use the Server API tab to share one).", 'note'))
    s.append(SP(6))

    s.append(P('31.3  Searching, Filtering, and Sorting', H2))
    s.append(P(
        "Once data is loaded the toolbar appears. A big RepeaterBook export can hold "
        "hundreds of machines, so the toolbar is how you cut it down to the few you "
        "care about. Every control narrows the table instantly as you use it, and "
        "they stack - set several at once to zero in."))
    s.append(SP(4))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Search',
         'Free-text box. Matches callsign, city, state, frequency, tone, sponsor, '
         'notes, and county all at once.'],
        ['Band',
         'Limits to one amateur band: 10m, 6m, 2m, 1.25m, 70cm, 33cm, or 23cm '
         '(the band is worked out from the output frequency).'],
        ['Mode',
         'Limits to one mode: FM / Analog, D-STAR, C4FM / Fusion, DMR, or P25.'],
        ['Status',
         'All, On-Air, or Off-Air - hide machines RepeaterBook lists as off the air.'],
        ['State',
         'All States, or one state. The list is built automatically from the data '
         'you loaded, so a two-state export offers both.'],
        ['Use',
         'All, Open, Closed, or Private - how the repeater owner allows access.'],
        ['EmComm',
         'All, ARES, SKYWARN, or RACES - show only repeaters flagged for that '
         'emergency-communications program.'],
        ['Sort by distance',
         'Off, Nearest first, or Farthest first. Turning it on reveals a Dist '
         'column of miles from your station location and orders the table by it.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(P(
        "To sort by any other column, click that column heading; click it again to "
        "reverse the direction. The status bar shows which column is sorting and "
        "which way."))
    s.append(SP(6))

    s.append(P('31.4  Reading the Table', H2))
    s.append(P(
        "Each row is one repeater. The columns, left to right:"))
    s.append(SP(4))
    s.append(tbl(['COLUMN', 'WHAT IT SHOWS'], [
        ['Output',   'The output frequency in megahertz - what you set your radio to '
                     'receive on. This is the number people mean by "the frequency."'],
        ['Input',    'The input frequency - what your radio transmits on. Dashed if '
                     'not known.'],
        ['Callsign', 'The repeater callsign (usually the trustee or club callsign).'],
        ['Tone',     'The access tone. A green badge is the transmit tone (CTCSS / PL); '
                     'a fainter "in:" badge appears when the input tone differs.'],
        ['Mode',     'A color badge for the mode - FM, D-STAR, C4FM, DMR, or P25.'],
        ['City',     'The nearest city or landmark.'],
        ['State',    'The state.'],
        ['EmComm',   'Emergency-program badges: ARES, RACES, SKY (SKYWARN), CAN (CANWARN).'],
        ['Links',    'Internet-linking badges: EL (EchoLink), AS (AllStar), WX (Wires-X). '
                     'Hover a badge to see the node number.'],
        ['Use',      'Open, Closed, or Private access.'],
        ['Status',   'A green dot for On-Air, a red dot for Off-Air.'],
        ['Dist',     'Miles from your station location. Hidden until you turn on '
                     '"Sort by distance."'],
    ], widths=[1.2*inch, CW-1.2*inch]))
    s.append(SP(6))

    s.append(P('31.5  The Detail Panel', H2))
    s.append(P(
        "Click any row and a panel slides in from the right with the full record for "
        "that repeater. The large green number at the top is the output frequency, "
        "with the callsign and the band, city, and state under it, then a row of "
        "mode and program badges. Below that is a labeled list:"))
    s.append(SP(4))
    s.append(tbl(['ROW', 'WHAT IT MEANS'], [
        ['Input',            'Transmit frequency in megahertz.'],
        ['CTCSS (out)',      'The tone your radio must send to open the repeater '
                             '("None / CSQ" means no tone needed).'],
        ['CTCSS (in)',       'The tone the repeater sends back, if any.'],
        ['Offset',           'The difference between input and output, worked out for '
                             'you (for example -0.600 MHz on 2 meters).'],
        ['Digital Code',     'The color code or digital ID for a digital repeater.'],
        ['County',           'The county the repeater is in.'],
        ['Distance',         'Miles from your station location.'],
        ['Status',           'On-Air or the status RepeaterBook lists.'],
        ['Use',              'Open, Closed, or Private.'],
        ['Trustee/Sponsor',  'The person or club that runs the repeater.'],
        ['Last Updated',     'When the RepeaterBook record was last changed.'],
        ['Website',          'A link to the sponsor site, when one is listed.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(P(
        "Any notes on the repeater appear in a shaded box under the list. Four "
        "buttons sit at the bottom of the panel:"))
    s.append(P('<b>Copy</b> - copies a one-line summary (callsign, frequencies, tone, '
               'mode, location) to the clipboard for pasting into a log or message.', Bullet))
    s.append(P('<b>Program</b> - opens a plain "Programming Summary" (RX, TX, offset, '
               'transmit and receive tones, mode, and a suggested name) to copy into a '
               'radio or a programming cable tool such as CHIRP.', Bullet))
    s.append(P('<b>Print</b> (the printer icon) - sends the current view to the printer.', Bullet))
    s.append(P('<b>+ Channel Lib</b> - adds this repeater to the Channel Library so it '
               'is available to drop into the ICS-205 communications plan (see 31.6).', Bullet))
    s.append(SP(6))

    s.append(P('31.6  Sending a Repeater to the Channel Library', H2))
    s.append(P(
        "The Repeater Database is a reference list; the Channel Library (Chapter 32) "
        "is the working set of channels that feeds your ICS-205. The <b>+ Channel "
        "Lib</b> button is the bridge between them. It saves the repeater to the "
        "server, so unlike an imported file it is shared with every operator device."))
    s.append(SP(4))
    s += steps([
        'Find the repeater you want and click its row to open the detail panel '
        '(or open the Map View and click its pin).',
        'Click <b>+ Channel Lib</b>. The button briefly reads "Added" in green.',
        'The channel now appears in the Channel Library, ready to insert into the '
        'ICS-205 communications plan.',
    ])
    s.append(note(
        "The saved channel is filed as an <b>Interop</b> channel when the repeater is "
        "flagged ARES or RACES, and as an <b>Amateur</b> channel otherwise, so it "
        "lands in a sensible group in the Channel Library. You can change that later "
        "in the Channel Library itself.", 'note'))
    s.append(SP(6))

    s.append(P('31.7  Adding a Repeater by Hand', H2))
    s.append(P(
        "For a machine that is not in RepeaterBook - a private club repeater, a "
        "temporary cross-band unit, or a single local repeater when you do not want "
        "a whole export - use manual entry. Click <b>Add Repeater</b> in the toolbar "
        "(or <b>Add a Repeater Manually</b> on the empty drop-zone screen). A small "
        "form opens with these fields:"))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['Callsign',            'The repeater callsign (typed in capitals).'],
        ['Output Freq (MHz) *', 'Required. The frequency you listen on, such as 146.940.'],
        ['Input Freq (MHz)',    'The frequency you transmit on. Leave blank for a simplex '
                                'machine or to work it out later.'],
        ['Tone / PL (Hz)',      'The access tone, such as 103.5. Leave blank for none.'],
        ['Mode',                'FM, D-STAR, C4FM, DMR, P25, or NXDN.'],
        ['City',                'The nearest city, such as Woodstock.'],
        ['State',               'The two-letter state, such as IL.'],
        ['Latitude / Longitude','Decimal coordinates, such as 42.32 and -88.38. Needed for '
                                'the repeater to appear on the map.'],
        ['Notes',               'Anything useful - "EOC primary, wide-area coverage."'],
        ['ARES / RACES / SKYWARN', 'Tick the box for each emergency program the repeater '
                                'supports.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s += steps([
        'Fill in at least the <b>Output Freq</b> - it is the only required field.',
        'Add the input frequency, tone, mode, location, and any flags you know.',
        'Click <b>Add to List</b>. The repeater joins the table immediately.',
    ])
    s.append(note(
        "A hand-added repeater is added to the list you are viewing but is not saved "
        "on its own. To keep it, click <b>CSV</b> in the toolbar to export the list "
        "(hand entries included), or open its detail panel and click <b>+ Channel "
        "Lib</b> to save it to the server as a channel.", 'warn'))
    s.append(SP(6))

    s.append(P('31.8  Map View', H2))
    s.append(P(
        "The <b>Map View</b> button in the toolbar opens a full-screen map of every "
        "repeater in the current filtered view that has coordinates. RepeaterBook "
        "exports include latitude and longitude for each repeater, so this usually "
        "means all of them. The button shows the plottable count in parentheses, for "
        "example <b>Map View (247)</b>."))
    s.append(SP(4))
    s.append(tbl(['MAP FEATURE', 'WHAT IT DOES'], [
        ['Pin color by mode',
         'Green FM, blue D-STAR, orange C4FM / Fusion, purple DMR, red P25. A repeater '
         'flagged ARES or RACES is drawn amber, overriding the mode color. The legend '
         'across the top names each color.'],
        ['Filter sync',
         'The map plots exactly the repeaters visible in the table. Set your band, '
         'mode, state, or EmComm filters first, then open the map to see only those.'],
        ['Pin popup',
         'Click a pin for the frequency, callsign, offset, mode, tone, location, '
         'county, sponsor, badges, and notes.'],
        ['Add to Channel Library',
         'Each popup has a "+ Add to Channel Library" button that imports that '
         'repeater as a channel without leaving the map.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s += steps([
        'Load repeater data and, if you want, apply filters to narrow the view.',
        'Click <b>Map View</b> in the toolbar. The map opens zoomed to fit every '
        'plotted pin.',
        'Click any pin to read its details or add it to the Channel Library.',
        'Press <b>Escape</b> or click <b>Close</b> to return to the table.',
    ])
    s.append(note(
        "Only repeaters with coordinates are plotted. A machine with no latitude and "
        "longitude still appears in the table but not on the map. The map draws its "
        "background from an online map service, so the streets fill in only when the "
        "Pi has internet; the pins themselves plot with or without a connection.", 'note'))
    s.append(SP(6))

    s.append(P('31.9  Repeater Overlays on the Tactical and Resource Maps', H2))
    s.append(P(
        "The same repeater data can be laid over the other two big maps in "
        "FieldCommand. Both read from the FieldCommand server, so import repeater "
        "data here first for the overlay to have anything to show."))
    s.append(SP(4))
    s.append(tbl(['MAP', 'HOW TO TURN IT ON', 'WHY'], [
        ['Tactical Map  (tactical.html)',
         'Click the <b>Repeaters</b> button in the map button bar. The first click '
         'loads and plots the repeaters; later clicks toggle the layer.',
         'See which repeaters cover the areas where APRS stations are active.'],
        ['Resource Map  (resource_map.html)',
         'Click the <b>Repeaters</b> button in the toolbar to toggle the layer on '
         'or off.',
         'Check repeater coverage over staging areas, shelters, and deployed '
         'resources.'],
    ], widths=[1.7*inch, 2.4*inch, CW-4.1*inch]))
    s.append(SP(6))

    s.append(P('31.10  Exporting and Printing', H2))
    s.append(P(
        "Two toolbar buttons get the list off the screen. <b>CSV</b> downloads the "
        "currently filtered list as a spreadsheet file (repeaters_fieldcommand.csv), "
        "which is the way to save hand-added entries or hand a channel plan to "
        "another operator. <b>Print</b> sends the current view to the printer for a "
        "paper cheat sheet to keep at the radio."))
    s.append(SP(6))

    s.append(P('31.11  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The import failed with an error',
         'The file is probably not a RepeaterBook export. Re-download it from '
         'repeaterbook.com as an Export - CSV, or use a RepeaterBook JSON file. The '
         'page accepts .csv, .json, and .txt.'],
        ['The Server API tab shows "unreachable" or is empty',
         'That tab needs an approved RepeaterBook API token and fetch_repeaters.py to '
         'have been run on the Pi. Use the Offline File tab instead - download a CSV '
         'and drag it in.'],
        ['Map View is grayed out or says "No repeaters with coordinates"',
         'The loaded repeaters have no latitude and longitude, or your filters hid '
         'them all. A RepeaterBook CSV includes coordinates; a hand-added repeater '
         'plots only if you filled in Latitude and Longitude.'],
        ['My hand-added repeater vanished after I reloaded',
         'Manual entries are added to the list, not saved on their own. Export the '
         'list to CSV, or click + Channel Lib to save it to the server as a channel.'],
        ['Another operator device does not see my imported repeaters',
         'An imported file is stored in that one browser. Either import the CSV on '
         'each device, or run fetch_repeaters.py and use the Server API tab so all '
         'devices share one server copy.'],
        ['Distances look wrong or are all blank',
         'Distance is measured from the station location built into the page, and '
         'needs each repeater to have coordinates. Turn on "Sort by distance" to '
         'reveal the Dist column; blanks mean that repeater has no coordinates.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch32():
    s = chapter(32, 'Channel Library',
                'http://192.168.50.1/channel_library.html')
    s.append(P(
        "The Channel Library is your agency's saved list of radio channels. Each entry "
        "holds one channel - its name, receive and transmit frequencies, tone, mode, the "
        "job it does, and which Division or Group uses it. The value of the library is not "
        "just storage: every channel you save here appears in the Channel Library picker on "
        "the ICS-205 Communications Plan, so building a communications plan becomes point "
        "and click instead of typing frequencies by hand while the clock is running. Enter a "
        "channel once, correctly, and reuse it on every incident.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: save your local repeaters, interop channels, and tactical "
        "frequencies here once, and they drop straight into the ICS-205 on every incident.",
        'tip'))
    s.append(SP(6))

    s.append(P('32.1  Universal Channels vs. Your Agency Channels', H2))
    s.append(P(
        "FieldCommand already knows the channels that are the same everywhere. Universal "
        "channels - National Simplex, Automatic Packet Reporting System (APRS), the National "
        "Interoperability Field Operations Guide (NIFOG) channels, and the standard Mutual "
        "Aid channels - are always available automatically and do not need to be entered. "
        "The Channel Library is for the channels that are specific to your jurisdiction: your "
        "local repeaters, your county interop and tactical frequencies, and your served "
        "agency talk paths. Only add your agency-specific channels here."))
    s.append(SP(4))
    s.append(P(
        "Channels that FieldCommand shipped with (rather than ones you typed) carry a small "
        "<b>seed</b> badge next to the name in the table, so you can tell a built-in starting "
        "channel from one your agency added."))
    s.append(SP(6))

    s.append(P('32.2  What a Channel Record Holds', H2))
    s.append(P(
        "Every channel is described by the same set of fields. These are the fields you fill "
        "in when adding or editing a channel, and the same fields shown as columns in the "
        "main table."))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Channel Name',
         'Required. The full, readable name - for example "McHenry County Command". This is '
         'what appears on the ICS-205.'],
        ['Alpha Tag',
         'A short code-plug label, up to ten characters, such as "MHCO CMD" - the kind of '
         'tag that fits a radio display. Optional.'],
        ['RX Freq',
         'Required. The receive frequency in megahertz (MHz) - what the radio listens on, '
         'for example 155.3400.'],
        ['TX Freq',
         'The transmit frequency in MHz - what the radio sends on. Leave it blank for a '
         'simplex channel; the library then shows "= RX" to mean transmit equals receive.'],
        ['PL/DCS',
         'The sub-audible tone the channel needs, if any - a Private Line (PL / CTCSS) tone '
         'like "100.0 Hz" or a Digital Coded Squelch (DCS) code like "D023N". Leave blank '
         'for none.'],
        ['Mode',
         'The radio mode - see the reference table in 32.6.'],
        ['Function',
         'The job the channel does - Command, Tactical, Medical, and so on (see 32.6).'],
        ['Division',
         'The Division or Group that uses this channel, such as "Div A", "Grp SAR", or '
         '"All". Optional.'],
        ['Notes',
         'Free text - repeater location, coverage area, or special instructions.'],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('32.3  Reading the Channel Table', H2))
    s.append(P(
        "The main screen is one wide table with a row per channel. The columns are, left to "
        "right: <b>Channel Name</b> (with the seed badge where it applies), <b>Alpha Tag</b>, "
        "<b>RX Freq</b> shown in green, <b>TX Freq</b> shown in amber when it differs from RX "
        "or as \"= RX\" when it is the same, <b>PL/DCS</b>, <b>Mode</b>, <b>Function</b> "
        "shown as a colored badge, <b>Division</b>, and <b>Notes</b>. The last column holds "
        "two small buttons on every row: a pencil to edit the channel and an X to delete it. "
        "A count at the right of the filter bar tells you how many channels are currently "
        "listed."))
    s.append(SP(6))

    s.append(P('32.4  Searching and Filtering', H2))
    s.append(P(
        "The filter bar sits just above the table:"))
    s.append(P('<b>Search box</b> - type any text (a name, a frequency, a function) and the '
               'table narrows as you type; it matches anywhere in the channel record.',
               Bullet))
    s.append(P('<b>All Functions drop-down</b> - pick one function (Command, Tactical, '
               'Interop, Medical, Data, Amateur, Calling, Mutual Aid, or Air) to show only '
               'channels with that job. Choose "All Functions" to clear it.', Bullet))
    s.append(P(
        "The two filters work together, so you can, for example, search for a repeater name "
        "and limit the result to Tactical channels at the same time."))
    s.append(SP(6))

    s.append(P('32.5  Adding or Editing a Channel', H2))
    s += steps([
        'Click <b>+ Add Channel</b> at the top right to create a new one, or click the '
        'pencil button on a row to change an existing one. The Add / Edit Channel window '
        'opens.',
        'Fill in the fields. <b>Channel Name</b> and <b>RX Frequency (MHz)</b> are required '
        '(marked with an asterisk); everything else is optional.',
        'Leave <b>TX Frequency</b> blank for a simplex channel - the library treats it as '
        'the same as RX.',
        'Choose the <b>Function</b> and <b>Mode</b> from their drop-downs, and set the '
        '<b>Division / Group Assignment</b> if this channel belongs to a specific part of '
        'the org.',
        'Click <b>SAVE CHANNEL</b>. The window closes and the table refreshes with your '
        'change. Click <b>Cancel</b> (or outside the window) to discard.',
    ])
    s.append(note(
        "A new channel defaults to Function \"Tactical\" and Mode \"FM\" so you can save a "
        "plain simplex frequency with only a name and RX. If you leave the required name or "
        "RX blank, the app warns you and does not save.", 'note'))
    s.append(SP(4))
    s.append(P(
        "The editor lays the fields out in a two-column grid. They are exactly the fields "
        "listed in 32.2, plus the required-field markers:"))
    s.append(SP(4))
    s.append(tbl(['EDITOR FIELD', 'NOTES'], [
        ['Channel Name *', 'Required. Full readable name.'],
        ['Alpha Tag', 'Up to ten characters; shown in a fixed-width font.'],
        ['Function', 'Command, Tactical, Interop, Medical, Data, Amateur, Calling, '
         'Mutual Aid, Air, or Other.'],
        ['RX Frequency (MHz) *', 'Required receive frequency.'],
        ['TX Frequency (MHz)', 'Leave blank if same as RX.'],
        ['PL Tone / DCS', 'For example "100.0 Hz" or "D023N".'],
        ['Mode', 'FM, NFM, P25, DMR, D-STAR, C4FM, AM, SSB, or Analog.'],
        ['Division / Group Assignment', 'For example "Div A", "Grp SAR", or "All".'],
        ['Notes', 'Repeater location, coverage area, special instructions.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(4))
    s.append(note(
        "Deleting a channel asks for confirmation and then hides it - it is a soft delete "
        "(the record is marked inactive, not erased), so an accidental delete does the least "
        "possible harm.", 'tip'))
    s.append(SP(6))

    s.append(P('32.6  Reference - Function and Mode Options', H2))
    s.append(P(
        "The drop-down choices for a channel, in plain language."))
    s.append(SP(4))
    s.append(P('32.6.1  Function', H3))
    s.append(tbl(['OPTION', 'MEANING'], [
        ['Command', 'The command net - command staff and unit leaders coordinate here.'],
        ['Tactical', 'A working channel for a specific job or team on the ground.'],
        ['Interop', 'An interoperability channel shared with other agencies.'],
        ['Medical', 'Medical coordination and patient traffic.'],
        ['Data', 'A data channel - packet, APRS, or another digital link.'],
        ['Amateur', 'An amateur (ham) radio channel or repeater.'],
        ['Calling', 'A calling / national simplex channel used to make first contact.'],
        ['Mutual Aid', 'A standard mutual aid channel for cross-agency response.'],
        ['Air', 'An air-to-ground or aircraft coordination channel.'],
        ['Other', 'Any purpose that does not fit the categories above.'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(4))
    s.append(P('32.6.2  Mode', H3))
    s.append(tbl(['MODE', 'MEANING'], [
        ['FM', 'Frequency Modulation - the standard analog voice mode on VHF/UHF.'],
        ['NFM', 'Narrow FM - FM at reduced deviation, where narrow channel spacing is required.'],
        ['P25', 'Project 25 - a public-safety digital voice standard.'],
        ['DMR', 'Digital Mobile Radio - a common commercial digital voice mode.'],
        ['D-STAR', 'An amateur digital voice and data mode.'],
        ['C4FM', 'Continuous 4-level FM - the amateur System Fusion digital mode.'],
        ['AM', 'Amplitude Modulation - for example, aircraft-band use.'],
        ['SSB', 'Single Sideband - a common voice mode on the HF bands.'],
        ['Analog', 'A generic analog channel when the exact mode is not specified.'],
    ], widths=[1.1*inch, CW-1.1*inch]))
    s.append(SP(6))

    s.append(P('32.7  Import and Export (CSV)', H2))
    s.append(P(
        "The whole library moves as a Comma-Separated Values (CSV) file - a plain "
        "spreadsheet file - so you can back it up, edit it in a spreadsheet program, or share "
        "it with another FieldCommand server."))
    s.append(P('<b>Export CSV</b> - downloads every channel as one file named '
               '<b>channel_library.csv</b>. Keep it as a backup or hand it to another agency.',
               Bullet))
    s.append(P('<b>Import CSV</b> - opens a file picker; choose a CSV file and its channels '
               'are added. The columns are the same field names used above (name, alpha_tag, '
               'rx_freq, tx_freq, pl_tone, mode, function, division, notes). A row missing a '
               'name or an RX frequency is skipped, and TX defaults to RX when blank.',
               Bullet))
    s.append(note(
        "Import adds channels; it does not replace your library. If you re-import a file you "
        "already have, expect duplicate rows. Export first if you want a clean backup before "
        "experimenting.", 'warn'))
    s.append(SP(6))

    s.append(P('32.8  Importing from RadioReference', H2))
    s.append(P(
        "If you have a RadioReference Premium subscription, you can pull your county's "
        "channels straight in instead of typing them. Click <b>Import from RadioReference</b> "
        "in the agency-configuration notice to open the import panel."))
    s.append(SP(4))
    s.append(P(
        "Enter your own <b>RR Username</b> and <b>RR Password</b> (they are used only for "
        "that one request and are never stored on the Pi), then either type your "
        "<b>County ID</b> directly or type a <b>ZIP Code</b> and click <b>Lookup ZIP</b> to "
        "find it. The <b>Filter by Tag</b> drop-down narrows what you fetch to one category:"))
    s.append(SP(4))
    s.append(tbl(['TAG', 'WHAT IT PULLS'], [
        ['All frequencies', 'Everything RadioReference lists for the county.'],
        ['Fire Dispatch / Fire-Tac', 'Fire main dispatch and fire tactical channels.'],
        ['EMS Dispatch / EMS-Tac', 'Emergency Medical Services dispatch and tactical channels.'],
        ['Law Dispatch / Law-Tac', 'Law enforcement dispatch and tactical channels.'],
        ['Interop', 'Interoperability channels shared across agencies.'],
        ['Emergency Ops', 'Emergency Operations Center and related channels.'],
        ['Amateur', 'Amateur (ham) repeaters and frequencies.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s += steps([
        'Enter your RadioReference username and password.',
        'Type a ZIP code and click <b>Lookup ZIP</b>; the County ID fills in and the status '
        'line shows the city it found. (Or type the County ID yourself.)',
        'Optionally choose a category in <b>Filter by Tag</b>, then click '
        '<b>Fetch Channels</b>.',
        'Review the results list. Tick the channels you want (the top checkbox selects all), '
        'then click <b>Import Selected</b> - or click <b>Import All</b> to take every '
        'result. Imported channels are tagged in their Notes as a RadioReference import.',
    ])
    s.append(note(
        "RadioReference import needs the internet - it is one of the features that lights up "
        "only when the Pi has a Wide Area Network (WAN) connection. Offline, type or CSV-"
        "import your channels instead.", 'note'))
    s.append(SP(6))

    s.append(P('32.9  How Channels Reach the ICS-205', H2))
    s.append(P(
        "The Channel Library is not a stand-alone list - it is the source for the "
        "communications plan. When you build an <b>ICS-205 Communications Plan</b> on an "
        "incident, the form has a Channel Library picker that lists everything saved here "
        "(plus the universal channels). Pick a channel and its name, frequencies, tone, "
        "mode, and function drop into the ICS-205 row for you. That is why it is worth "
        "getting each channel right once in the library: the effort pays off on every "
        "incident, and every operator reads the same correct frequency instead of a "
        "hand-copied one."))
    s.append(SP(6))

    s.append(P('32.10  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The table says "Cannot reach server"',
         'The ICS platform service (port 5055) is not responding. Check that the Pi is on '
         'and the ics-platform service is running, then reload the page.'],
        ['A channel I expected is not listed',
         'Check the filter bar - a search term or a Function filter may be hiding it. Clear '
         'the search box and set the drop-down back to "All Functions".'],
        ['I do not see the common simplex / NIFOG channels',
         'Those are universal and are added automatically on the ICS-205 - they are not '
         'stored in this library, so they will not appear in this table. Only agency-'
         'specific channels live here.'],
        ['TX shows "= RX" and I need a repeater offset',
         'That channel has no separate transmit frequency. Edit it and enter the correct TX '
         'Frequency in MHz; the table will then show the transmit value in amber.'],
        ['RadioReference lookup returns an error',
         'Confirm your Premium subscription username and password, that the Pi has internet '
         '(WAN) right now, and that the ZIP or County ID is correct. The status line under '
         'the buttons shows the exact message.'],
        ['I deleted a channel by mistake',
         'Delete is a soft delete, so the record still exists but is inactive. Re-add the '
         'channel (or re-import from your last CSV export) to bring it back.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch33():
    s = chapter(33, 'Hospital Proximity & Facilities Directory',
                'http://192.168.50.1/hospitals.html')
    s.append(P(
        'When someone is hurt, the first question is always the same: where do we take them, '
        'and how fast can they get there? The Hospital Proximity page answers it. You keep a '
        'list of the trauma centers, burn centers, and community emergency departments in your '
        'response area, type in where the incident is, and FieldCommand instantly ranks every '
        'hospital by air miles, helicopter flight time, driving distance, and drive time -- '
        'and flags which ones have a helipad, a burn unit, or a pediatric, stroke, or cardiac '
        'capability. It works entirely offline once the hospitals are entered, so it keeps '
        'working when the internet does not. The companion Facilities Directory does the same '
        'job for every other operational site: Emergency Operations Centers (EOCs), shelters, '
        'staging areas, supply depots, and command posts.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: type in the incident location, and the page sorts your hospital list '
        'nearest-first with air time, drive time, and capabilities shown on every card.', 'tip'))
    s.append(SP(6))

    s.append(P('33.1  How the Screen Is Laid Out', H2))
    s.append(P(
        'The Hospital Proximity page (hospitals.html) is one scrolling screen with four working '
        'areas stacked from top to bottom. Knowing where each lives makes the rest of this '
        'chapter quick to follow.'))
    s.append(SP(4))
    s.append(tbl(['AREA', 'WHAT IT IS FOR'], [
        ['Top bar',
         "The blue MEDICAL header. On the right are the buttons that act on the whole list: "
         "<b>+ Add Hospital</b>, <b>Import CSV</b>, <b>Export CSV</b>, <b>Import from CMS</b>, "
         "and the <b>Dashboard</b> link back home."],
        ['Incident Location bar',
         'The pale band with <b>Latitude</b> and <b>Longitude</b> boxes. This is where you tell '
         'the page where the incident is so it can measure distances.'],
        ['Air Transport bar',
         'The <b>Helicopter Type</b> picker. It sets the aircraft speed used to work out flight '
         'time to each hospital.'],
        ['Sort bar and list',
         'The row of <b>Sort by</b> buttons, the search box and filter checkboxes, and below '
         'them the list of hospital cards -- one card per hospital.'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(SP(6))

    s.append(P('33.2  Adding and Editing a Hospital', H2))
    s.append(P(
        'Click <b>+ Add Hospital</b> (top right) to open the Add Hospital form, or click the '
        '<b>Edit</b> button on any card to change one you already have. The form is one panel '
        'with the fields below. Only the name is required; fill in as much of the rest as you '
        'know. Latitude and longitude are what make the distance ranking work, so add them '
        'whenever you can.'))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT IT MEANS'], [
        ['Hospital Name *',
         'Required. The official facility name, for example "Northwestern Medicine McHenry '
         'Hospital".'],
        ['Address',
         'The street address. Used for reference and to build the address line on the card.'],
        ['City / State / County',
         'Location details. State is a two-letter code (for example IL); the card shows the '
         'county with the word "County" after it.'],
        ['Switchboard Phone',
         'The main hospital number. It becomes a tap-to-call link on the card.'],
        ['Emergency Dept (ED) Phone',
         'The direct emergency department line, if you have one. It becomes a separate '
         'tap-to-call link marked ED. Optional.'],
        ['Latitude / Longitude',
         'The hospital coordinates in decimal degrees (for example 42.3089 and -88.4356). '
         'Required for the distance, air time, and drive time to be calculated.'],
        ['Trauma Level',
         'A drop-down: None / Unknown, Level I, Level II, Level III, or Level IV. Level I is '
         'the highest trauma capability.'],
        ['Burn Center',
         'Tick if the hospital has a dedicated burn unit. Adds a Burn Center badge and enables '
         'the burn-first sort.'],
        ['Helipad',
         'Tick if the hospital can receive a medical helicopter. Ticked by default on a new '
         'hospital. Adds a Helipad badge.'],
        ['Peds Trauma',
         'Tick if the hospital has pediatric (child) trauma capability. Adds a Peds Trauma '
         'badge.'],
        ['Stroke Center / Cardiac Center',
         'Tick if the hospital is a designated stroke or cardiac center. Each adds its own '
         'badge to the card.'],
        ['Notes',
         'A free-text line for anything else -- diversion status, special capabilities, or '
         'current capacity.'],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        'Click <b>SAVE</b> to store the hospital on the server. When you are editing an '
        'existing hospital a <b>Delete</b> button also appears; it asks you to confirm before '
        'removing the record. <b>Cancel</b> closes the form without saving.'))
    s.append(note(
        'A hospital with no latitude and longitude still shows in the list, but it always sorts '
        'to the bottom and shows no distance block -- the page cannot measure a hospital it '
        "does not have coordinates for. Add them by editing the hospital.", 'note'))
    s.append(SP(6))

    s.append(P('33.3  Bringing In Hospitals in Bulk', H2))
    s.append(P(
        'Typing hospitals one at a time is fine for a handful, but there are faster ways to '
        'load a whole region. Three buttons in the top bar handle bulk data.'))
    s.append(SP(4))

    s.append(P('33.3.1  Import CSV', H3))
    s.append(P(
        'Click <b>Import CSV</b> and choose a comma-separated (spreadsheet) file. The page '
        'matches your column headings automatically -- it looks for headings that contain '
        'words like name, address, city, state, county, phone, lat, lon, trauma, burn, heli, '
        'peds, stroke, cardiac, and notes, so a spreadsheet exported from almost any registry '
        'usually loads without editing. The file must have a <b>name</b> column; any row '
        'without a name is skipped. When it finishes, a message tells you how many hospitals '
        'were imported and how many failed.'))
    s.append(SP(4))

    s.append(P('33.3.2  Export CSV', H3))
    s.append(P(
        'Click <b>Export CSV</b> to download your entire hospital list as a spreadsheet file '
        'named hospitals.csv. This is your backup and your sharing format -- hand the file to '
        'another FieldCommand server and it imports straight back in with Import CSV.'))
    s.append(SP(4))

    s.append(P('33.3.3  Import from CMS', H3))
    s.append(P(
        'Click <b>Import from CMS</b> to open a panel that pulls Medicare-certified hospitals '
        'from the public federal Centers for Medicare & Medicaid Services (CMS) dataset. '
        'Enter the two-letter <b>State</b> (required) and optionally a <b>County</b>, tick '
        '<b>Acute Care</b> and/or <b>Critical Access</b>, and click <b>Search CMS</b>. Results '
        'appear in a table with a tick box on each row; use <b>Import All</b> or tick the ones '
        'you want and use <b>Import Selected</b>.'))
    s.append(note(
        "The CMS dataset gives you names, addresses, and phone numbers, but it does NOT include "
        "coordinates or trauma level. Imported hospitals arrive with blank latitude, longitude, "
        "and trauma level -- you must edit each one to add them before distance ranking will "
        "work. This search also needs a working internet connection; the rest of the page does "
        "not.", 'warn'))
    s.append(SP(6))

    s.append(P('33.4  Setting the Incident Location', H2))
    s.append(P(
        'Distances are measured from one point: the incident location. Until you set it, the '
        'list is unsorted and no distance blocks appear. Set it in the Incident Location bar '
        'by any of three ways.'))
    s.append(SP(4))
    s += steps([
        'Type the <b>Latitude</b> and <b>Longitude</b> into the two boxes directly -- for '
        'example 42.3089 and -88.4356. The list re-sorts the moment you finish typing.',
        'Or click <b>From General Info</b> to pull the coordinates from the currently selected '
        "incident's General Info form. If that form has no coordinates yet, the page tells you "
        'to enter them there first.',
        'Or click <b>Use GPS</b> to take the coordinates from the device you are holding. Handy '
        'when you are standing at the scene. Your browser will ask permission to share '
        'location.',
    ])
    s.append(P(
        'When coordinates are set, a small confirmation line shows the numbers the page is '
        'measuring from, every card gains its distance block, and each card shows a rank number '
        '(#1, #2, and so on) in whatever order you are sorting by.'))
    s.append(SP(6))

    s.append(P('33.5  Air Transport -- the Helicopter Selector', H2))
    s.append(P(
        'Helicopter flight time depends on how fast the aircraft flies, so the Air Transport '
        'bar lets you pick the aircraft. The <b>Helicopter Type</b> drop-down lists common '
        'medical helicopters with their cruise speeds; the standard Bell 407 at 155 miles per '
        'hour is selected by default. Choose <b>Custom speed...</b> to type any speed between '
        '80 and 250 miles per hour if your local air-medical service flies something else.'))
    s.append(SP(4))
    s.append(tbl(['HELICOPTER TYPE', 'CRUISE SPEED'], [
        ['Air Methods / Metro (Bell 206)', '145 mph'],
        ['Helicopter EMS Midsize (EC135)', '150 mph'],
        ['Air Methods Standard (Bell 407) -- default', '155 mph'],
        ['Agusta AW109', '165 mph'],
        ['Sikorsky S-76', '170 mph'],
        ['MedStar / AirLife (EC145)', '180 mph'],
        ['Custom speed...', 'Any value you type, 80 to 250 mph'],
    ], widths=[CW-1.4*inch, 1.4*inch]))
    s.append(SP(4))
    s.append(note(
        'The Helo Time on each card is not pure flight time. FieldCommand adds a realistic '
        '8 minutes for scene arrival and liftoff plus 5 minutes for the hospital approach, so '
        'the number you see is a usable door-to-door estimate rather than a best-case straight '
        'line.', 'note'))
    s.append(SP(6))

    s.append(P('33.6  Sorting, Searching, and Filtering', H2))
    s.append(P(
        'The Sort bar controls the order of the list. Click a <b>Sort by</b> button and the '
        'list re-orders at once; the active button is highlighted. Hospitals with no '
        'coordinates always fall to the bottom of a distance sort because there is nothing to '
        'measure.'))
    s.append(SP(4))
    s.append(tbl(['SORT BUTTON', 'ORDERS THE LIST BY'], [
        ['Air Miles',      'Straight-line distance from the incident, nearest first. The default.'],
        ['Air Time',       'Estimated helicopter time (flight plus the scene and approach '
                            'minutes), soonest first.'],
        ['Ground Miles',   'Estimated road distance -- about 1.3 times the air miles, a standard '
                            'road multiplier.'],
        ['Drive Time',     'Estimated driving time, figured at an average 45 miles per hour, '
                            'soonest first.'],
        ['Trauma Level',   'Highest trauma capability first (Level I, then II, III, IV), with '
                            'nearer hospitals first inside each level.'],
        ['Burn Center First', 'Burn centers at the top, then ordered by trauma level.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(P(
        'On the right of the Sort bar are three narrowing tools. The <b>Search hospitals</b> '
        'box hides any card that does not contain the text you type -- a name, a city, a '
        'capability. The <b>Helipad only</b> checkbox hides hospitals with no helipad. The '
        '<b>Trauma only</b> checkbox hides hospitals with no trauma-level designation. A count '
        'line above the list shows how many hospitals match and which sort is active.'))
    s.append(SP(6))

    s.append(P('33.7  Reading a Hospital Card', H2))
    s.append(P(
        'Each hospital is one card. A colored stripe down the left edge shows its trauma level '
        'at a glance -- red for Level I, amber for Level II, blue for Level III, plain for the '
        'rest. The card carries these parts.'))
    s.append(SP(4))
    s.append(tbl(['PART OF THE CARD', 'WHAT IT SHOWS'], [
        ['Name and rank',
         'The hospital name, with its rank number (for example #1) when a sort is active.'],
        ['Edit and phone buttons',
         'An <b>Edit</b> button, plus tap-to-call links: a green switchboard link and, if '
         'entered, a red <b>ED</b> link for the emergency department.'],
        ['Address line',
         'The street, city, state, and county.'],
        ['Capability badges',
         'Small pills for each capability the hospital has: Trauma level, Burn Center, Helipad, '
         'Peds Trauma, Stroke, Cardiac, and ICU.'],
        ['Distance block',
         'A four-part strip -- Air Miles, Helo Time, Ground Mi, and Drive Est -- shown only '
         'when the incident location and the hospital both have coordinates.'],
        ['Notes',
         'Any note you entered, shown at the bottom of the card.'],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(6))

    s.append(P('33.8  The Facilities Directory', H2))
    s.append(P(
        'The Facilities Directory (facilities.html) is the sister page for every operational '
        'site that is not a hospital. Open it from the dashboard. It keeps EOCs, shelters, '
        'staging areas, supply depots, command posts, and anything else in one searchable '
        'directory, each shown as a colored card with a status dot -- green for active, amber '
        'for standby, gray for inactive. Because it records radio frequencies and an on-site '
        'callsign for each site, it doubles as a facility communications plan.'))
    s.append(SP(4))
    s.append(P(
        'A toolbar at the top lets you <b>Search</b> by name, address, or notes and filter by '
        '<b>Type</b> (EOC, Hospital, Shelter, Staging Area, Supply Depot, Command Post, Other) '
        'or by <b>Status</b>. The <b>CSV</b> button downloads the directory and <b>Print</b> '
        'sends it to your printer. Click <b>+ Add Facility</b> to open the form; click any card '
        'to see its full detail, where <b>Edit</b>, <b>Delete</b>, and <b>Copy Address</b> '
        'buttons wait.'))
    s.append(SP(4))
    s.append(tbl(['FACILITY FIELD', 'WHAT IT MEANS'], [
        ['Facility Name *',       'Required. The site name, for example "Franklin County EOC".'],
        ['Type *',                'What kind of site it is -- EOC, Hospital, Shelter, Staging '
                                  'Area, Supply Depot, Command Post, or Other. Sets the card '
                                  'color.'],
        ['Operational Status',    'Active, Standby, or Inactive -- the colored status dot.'],
        ['Address / City / State / ZIP', 'The location, used for reference and Copy Address.'],
        ['Latitude / Longitude',  'Decimal coordinates for the site.'],
        ['Primary / Secondary Phone', 'Up to two phone numbers for the site.'],
        ['Primary / Secondary Frequency', 'Radio frequencies in megahertz that reach this site.'],
        ['CTCSS Tone',            'The sub-audible tone the site repeater or channel uses, if any.'],
        ['Capacity',              'How many people or how much the site holds, for example '
                                  '"250 persons".'],
        ['Contact Person / Ham Callsign on Site', 'Who to reach at the site and the amateur '
                                  'radio callsign operating there.'],
        ['Generator / ADA Accessible', 'Backup power and accessibility status -- Yes, No, '
                                  'Partial, or Unknown.'],
        ['Notes',                 'Parking, access codes, gate instructions, and anything else.'],
    ], widths=[2.1*inch, CW-2.1*inch]))
    s.append(note(
        'Facility records, like hospitals, are stored on the server, so every operator on '
        'EMCOMM-NET sees the same directory and it survives a restart.', 'tip'))
    s.append(SP(6))

    s.append(P('33.9  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['The list is not sorting by distance',
         'No incident location is set. Type latitude and longitude into the Incident Location '
         'bar, or click From General Info or Use GPS.'],
        ['A hospital shows no distance block and sits at the bottom',
         'That hospital has no coordinates. Click Edit and fill in its Latitude and Longitude, '
         'then Save.'],
        ['I imported from CMS but nothing sorts by distance',
         'CMS data has no coordinates or trauma level. Edit each imported hospital to add '
         'latitude, longitude, and trauma level.'],
        ['Search CMS says it failed or timed out',
         'The CMS search needs the internet. Check your connection, or add the hospitals by '
         'hand or by CSV instead -- the rest of the page works offline.'],
        ['My CSV imported fewer hospitals than expected',
         'Rows with no name are skipped, and the file must have a name column. Open the file '
         'and confirm every hospital has a value in the name column.'],
        ['Cannot reach server appears in the list area',
         'The core service on port 5050 is not answering. Confirm you are on 192.168.50.1, then '
         'check the fcc-lookup service on the Health page.'],
        ['My changes vanished after I reloaded',
         'They should not -- hospitals and facilities are saved on the server. Confirm the Save '
         'button was clicked (not Cancel) and that you are on the right server.'],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch34():
    s = chapter(34, 'Reference Tools — Grid, Cheat Sheets, Resources, Print Center',
                '')
    s.append(P(
        "FieldCommand IMS gathers the small, everyday helper tools an operator reaches for "
        "again and again into one set of reference pages. None of them run an incident by "
        "themselves; they support the work you do everywhere else in the app. The Grid Square "
        "Calculator turns coordinates into a Maidenhead grid and back. The Radio Cheat Sheets "
        "give you the phonetic alphabet, Q-codes, prowords, band plans, and signal-report "
        "scales on one screen. The National Incident Management System (NIMS) Resource Typing "
        "Library holds the standard resource definitions that feed your T-cards. The Incident "
        "Command System (ICS) Position Checklists spell out the duties of every ICS job. The "
        "Print Center puts every form, reference card, and log one click from your printer. "
        "Every one of these tools works with the internet turned completely off.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: this chapter covers the reference and print helpers — grid math, "
        "radio cheat sheets, the resource-type library, position checklists, and the Print "
        "Center — that support the rest of FieldCommand and run fully offline.", 'tip'))
    s.append(SP(6))

    s.append(P('34.1  Grid Square Calculator', H2))
    s.append(P(
        "Open the Grid Square Calculator from the dashboard. Maidenhead grid squares are the "
        "short location codes hams use — for example EN52 or EN52ab. This page converts a "
        "grid to latitude and longitude, converts coordinates to a grid, and measures the "
        "distance and bearing between any two grids. The screen is divided into panels."))
    s.append(SP(4))
    s.append(tbl(['PANEL', 'WHAT IT DOES'], [
        ['Lat / Lon to Grid Square',
         "Type a decimal Latitude and Longitude, then click Calculate Grid. The big amber "
         "readout shows the 6-character grid, with the 4-character grid below it, and a "
         "detail list of Field, Square, Subsquare, decimal, and degrees-minutes-seconds "
         "(DMS) lines."],
        ['Use My Location (GPS)',
         "A button in that same panel. It asks your device for its location and fills the "
         "Latitude and Longitude for you, then calculates. Needs a device with location "
         "services turned on."],
        ['Grid Square to Lat / Lon',
         "Type a Maidenhead locator (4 or 6 characters) and click Decode Grid. The readout "
         "shows the center latitude and longitude of that square in both decimal and DMS."],
        ['Distance and Bearing Between Two Grids',
         "Type Grid 1 and Grid 2 and click Go. You get the great-circle distance in "
         "kilometers and miles, plus the true bearing each way with a compass label."],
        ['Grid Square Map (North America)',
         "A drawn map you can click or tap to look up a grid. Your current result is "
         "highlighted with an amber box and a green center dot."],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(P(
        "Grid input boxes force upper case as you type and accept 4, 6, or 8 characters. The "
        "Maidenhead Grid Reference panel at the bottom explains the precision levels: a Field "
        "(2 letters) is roughly 20 degrees by 10 degrees, a Square (add 2 digits) is 2 by 1 "
        "degrees, and a Subsquare (add 2 lowercase letters) narrows it to about 5 by 2.5 "
        "arc-minutes."))
    s.append(note(
        "The GPS button and the map only need your device — no internet. If Use My Location "
        "does nothing, your browser blocked location access; type the coordinates by hand "
        "instead.", 'note'))
    s.append(SP(6))

    s.append(P('34.2  Radio Cheat Sheets', H2))
    s.append(P(
        "The Cheat Sheets page is a tabbed quick-reference card for common amateur radio and "
        "ICS procedures. A row of tabs across the top switches between eight cards; the Print "
        "All button in the header prints every card at once, each on its own page, so you can "
        "laminate a full set."))
    s.append(SP(4))
    s.append(tbl(['TAB', 'WHAT IS ON IT'], [
        ['Phonetic Alphabet',
         "The full NATO phonetic alphabet A through Z with pronunciation, plus the ITU "
         "spoken numbers zero through nine."],
        ['Q-Codes',
         "Two columns — common HF and amateur Q-codes (QRM, QSY, QTH, and so on) and the "
         "emergency-communications net Q-codes (QNI, QND, QTC, and more)."],
        ['Prowords',
         "A table of procedure words such as SAY AGAIN, ROGER, WILCO, and BREAK, each with "
         "its meaning and an example of how it is used on the air."],
        ['Band Plan',
         "The 2-meter and 70-centimeter band segments, a table of HF emergency frequencies, "
         "and a Special Service Bands table (MURS, FRS, GMRS, marine, aviation)."],
        ['NTS Precedence',
         "The National Traffic System message precedence levels — EMERGENCY, PRIORITY, "
         "WELFARE, ROUTINE — plus the ICS triage priority colors."],
        ['ICS Structure',
         "A drawn ICS organization chart and a table of the key ICS forms (ICS-201 through "
         "ICS-309) with the section that owns each and its purpose."],
        ['CTCSS / DCS',
         "The full 42-tone CTCSS (Continuous Tone-Coded Squelch System) table and a table "
         "of common Digital Coded Squelch (DCS) codes."],
        ['Signal Reports',
         "The RST (Readability, Strength, Tone) scale, APCO P25 signal quality, FM "
         "voice-report shorthand, and a dBm-to-watts reference."],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(P(
        "Resource typing is deliberately NOT one of these cards — it is a large, searchable "
        "library of its own, described next in 34.3."))
    s.append(SP(6))

    s.append(P('34.3  NIMS Resource Typing Library', H2))
    s.append(P(
        "The Resource Typing Library holds the standard NIMS resource-type definitions — the "
        "kinds of teams, vehicles, and equipment you order and track on an incident. These "
        "are the same definitions that populate the T-card board, so keeping this library "
        "accurate keeps your resource ordering NIMS-compliant. The definitions are drawn from "
        "the Federal Emergency Management Agency (FEMA) Resource Typing Library Tool."))
    s.append(SP(4))
    s.append(P(
        "Resources appear as collapsed cards grouped by category (Fire, Search and Rescue, "
        "Medical, and so on). Click any card to expand its full definition. The header and "
        "filter bar give you these controls:"))
    s.append(tbl(['CONTROL', 'WHAT IT DOES'], [
        ['Search box', "Type any part of a name, capability, or description to filter the "
         "list as you type."],
        ['Category buttons', "Colored pills below the search box — click one to show only "
         "that category, or All to show everything."],
        ['Expand All / Collapse All', "Open or close every card at once."],
        ['+ Add Custom Type', "Opens the editor so you can add a resource type your "
         "organization uses that is not in the standard set."],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(P(
        "An expanded card can show up to five labeled sections: What It Is, Minimum Standards "
        "/ Specifications, Capability Summary, When to Order This Resource, and Common "
        "Confusion / Watch Points. When you add or edit a type, the same fields appear in the "
        "editor window."))
    s.append(SP(4))
    s.append(P('34.3.1  Adding or Editing a Resource Type', H3))
    s += steps([
        "Click <b>+ Add Custom Type</b> (or the pencil icon on a custom card you made "
        "earlier). The editor window opens.",
        "Fill in <b>Kind / Name</b> — this is the only required field, for example "
        '"Swiftwater Rescue Team".',
        "Set the <b>Category</b> from the drop-down and, if it applies, the <b>Type Level</b> "
        "(Type I, Type II, or N/A) and <b>Min Personnel</b>.",
        "Add any of the longer fields you want: Full Description, Capability Summary, Metrics "
        "/ Specifications, What It Is, Minimum Standards, When to Order, and Common Confusion.",
        "Click <b>Save Resource Type</b>. The card is saved on the FieldCommand server and "
        "becomes available on the T-card board immediately.",
    ])
    s.append(note(
        "Standard shipped types show no pencil icon and cannot be edited or deleted — only "
        "types you add carry a CUSTOM tag and the pencil. This protects the NIMS baseline "
        "from accidental changes.", 'note'))
    s.append(SP(6))

    s.append(P('34.4  ICS Position Checklists', H2))
    s.append(P(
        "The Position Checklists page is a job-duty book for every ICS position. Pick a "
        "position from the left sidebar and the main area fills with that job's duties, the "
        "forms it must produce, the meetings it attends, and who it reports to and "
        "supervises. Each duty is a checkbox you can tick off as you go and then print for "
        "the position binder."))
    s.append(SP(4))
    s.append(P(
        "The sidebar groups positions by section — Command, Operations, Planning, and the "
        "rest — and has a search box at the top. Positions include the Incident Commander "
        "(IC), Deputy IC, Safety Officer (SO), Public Information Officer (PIO), Liaison "
        "Officer (LNO), Operations Section Chief (OSC), Branch Director, Division/Group "
        "Supervisor, Strike Team / Task Force Leader, Planning Section Chief (PSC), Resources "
        "Unit Leader (RESL), Situation Unit Leader (SITL), Staging Area Manager, Technical "
        "Specialist, and the air-operations supervisors, among others."))
    s.append(SP(4))
    s.append(P("Each position screen is laid out the same way:"))
    s.append(tbl(['PART OF THE SCREEN', 'WHAT IT SHOWS'], [
        ['Position header card', "The job title, who it Reports To, and who it Supervises, "
         "with a plain-language description of the role."],
        ['Fallback box', "A red note explaining who absorbs the duties when this position is "
         "left unfilled — common on smaller incidents."],
        ['Activation checklist', "The tasks to do when you first take the position."],
        ['Operational checklist', "The recurring duties for each operational period. Small "
         "colored tags mark items tied to a Form, a Briefing, Coordination, Safety, or "
         "Documentation."],
        ['Deactivation checklist', "The tasks to close out and hand off the position."],
        ['Deliverables', "The ICS forms this position must produce, each with a short "
         "description and how often it is due."],
        ['Meetings', "The incident meetings and briefings this position attends."],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        "Click any checklist line to mark it done — it dims and a green check fills the box, "
        "and a progress bar tracks how far you are. The <b>Print This Position</b> button in "
        "the header prints just the position you are viewing, and <b>Reset Checks</b> clears "
        "all the ticks so the checklist is fresh for the next operational period or the next "
        "person."))
    s.append(SP(6))

    s.append(P('34.5  Print Center', H2))
    s.append(P(
        "The Print Center gathers every printable form, reference card, and log into one "
        "page of cards, grouped into sections. Each card has an Open (or Open Form) button "
        "that takes you to the live tool, and most also have a Preview button that loads the "
        "document into a preview pane on the same page so you can print it without leaving "
        "the Print Center."))
    s.append(SP(4))
    s.append(tbl(['SECTION', 'CARDS IT HOLDS'], [
        ['ICS / NTS Forms',
         "ICS-213 General Message, ICS-214 Activity Log, ICS-309 Communications Log, NTS "
         "Radiogram, and the Pre-Flight Checklist."],
        ['Reference Cards',
         "Phonetic Alphabet, Q-Codes & Prowords, ICS Structure & Forms, and CTCSS / DCS & "
         "Signal Reports — each opens the matching Cheat Sheet card (34.2)."],
        ['Operations',
         "Net Control Log (ICS-309), Starcom Net Log (ICS-309), Roster / Member Directory, "
         "and the Resource Board — each jumps to that live tool to print its current data."],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(SP(4))
    s.append(P(
        "When a Preview pane is open it has its own Print button (which prints just the "
        "framed document) and a Close button. Printing always uses your own device's browser "
        "print dialog, so you can send the page to any printer that device can reach, or "
        "choose Save as PDF. There is no server-side print spooling to set up."))
    s.append(SP(6))

    s.append(P('34.6  Incident Cover Sheet Generator', H2))
    s.append(P(
        "At the bottom of the Print Center is a Cover Sheet Generator that builds a clean "
        "title page for an incident packet. Fill in the boxes, click <b>Generate Cover "
        "Sheet</b> to see the formatted page, then click <b>Print</b>."))
    s.append(SP(4))
    s.append(tbl(['FIELD', 'WHAT TO ENTER'], [
        ['Incident Name', 'The incident title, for example "Winter Storm Alpha".'],
        ['Incident Number', 'Your local tracking number, such as "2026-001".'],
        ['Date / Time', "Pre-filled with the current date and time; edit if you need a "
         "different stamp."],
        ['Incident Commander', "The IC's name and, if a ham, callsign."],
        ['Agency', 'The agency or group running the incident.'],
        ['Operational Period', 'The period number and hours, e.g. "1 — 0800-2000".'],
        ['Location / Jurisdiction', "Where the incident is — city, county, or address."],
        ['Net Frequency', 'The primary net frequency and tone, e.g. "146.940 MHz / 100.0 Hz".'],
        ['Situation Summary', "A short paragraph describing the incident and current status."],
    ], widths=[1.9*inch, CW-1.9*inch]))
    s.append(SP(4))
    s.append(P(
        "The <b>Clear</b> button empties the form so you can start a fresh cover sheet. Like "
        "everything else here, the cover sheet prints through your device's own browser "
        "print dialog."))
    s.append(SP(6))

    s.append(P('34.7  Troubleshooting', H2))
    s.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
        ['Use My Location does nothing on the Grid page',
         "Your browser blocked location access, or the device has no location service. "
         "Allow location for this site, or just type the Latitude and Longitude by hand and "
         "click Calculate Grid."],
        ['Decode Grid says the grid is invalid',
         "Enter at least the first two letters, then the digits and letters in order (for "
         "example EN52 or EN52ab). The box forces upper case; spaces are not allowed."],
        ['The Resource Typing Library will not load',
         "It reads from the FieldCommand server. Confirm you are connected to EMCOMM-NET and "
         "on the server at 192.168.50.1, then reload the page."],
        ['A resource type has no pencil (edit) icon',
         "That is a standard shipped type and is protected. To change it, add your own "
         "Custom Type with the values you want using + Add Custom Type."],
        ['A checklist I filled in came back blank',
         "The Reset Checks button clears every tick for that position. Ticks are also "
         "per-device — another operator's device keeps its own set."],
        ['Print or Preview shows a blank or tiny page',
         "Wait a moment for the document to finish loading in the frame, then use the "
         "Print button inside the preview. In the print dialog, set paper to Letter and "
         "scale to Fit or 100%."],
    ], widths=[2.3*inch, CW-2.3*inch]))
    s.append(PB())
    return s


def ch35():
    s = chapter(35, 'Network Hardware — Routers, Switch, and Coverage Extension',
                '')
    s.append(P(
        "FieldCommand IMS lives on its own private network called EMCOMM-NET (short "
        "for emergency communications). Everything an operator does happens over this "
        "network: a phone, tablet, or laptop joins the EMCOMM-NET Wi-Fi, opens a browser "
        "to http://192.168.50.1, and reaches every tool. What makes that network exist is "
        "a small, deliberate set of gear — a portable Wi-Fi router, a wired network switch, "
        "and optional mesh nodes that stretch the signal further. This chapter names each "
        "box, tells you what it does, gives the exact port and address layout that keeps "
        "the system predictable, and explains how to add coverage when one room is not "
        "enough. Neither Raspberry Pi ever broadcasts the Wi-Fi — the router does that job, "
        "which frees the servers to run the incident.", Lead))
    s.append(SP(4))
    s.append(note(
        "In one sentence: the router makes the EMCOMM-NET Wi-Fi and hands out addresses, "
        "the switch wires the servers and workstations together, and extra routers act as "
        "mesh nodes to spread the same network across a larger site.", 'tip'))
    s.append(SP(6))

    s.append(P('35.1  The Three Pieces of EMCOMM-NET', H2))
    s.append(P(
        "EMCOMM-NET is self-contained. It does not need the internet, a phone company, or "
        "any outside service to exist — as long as the router and switch have power, the "
        "network is up and everyone on it can reach the FieldCommand server, even in a "
        "parking lot in the middle of nowhere. Three kinds of hardware build it:"))
    s.append(SP(4))
    s.append(tbl(['PIECE', 'WHAT IT DOES'], [
        ['Wi-Fi router',
         "The ASUS RT-BE58 Go. It broadcasts the EMCOMM-NET wireless network, hands every "
         "joining device an address automatically, and (when a WAN source is plugged in) "
         "routes the optional internet connection. This is the one box you must have."],
        ['Network switch',
         "The UniFi Switch Lite 16 PoE. A box of Ethernet sockets that wires the two "
         "servers, the operator workstations, a laptop, and a printer together at full "
         "speed, with power on some ports."],
        ['AiMesh nodes',
         "Extra RT-BE58 Go routers — identical to the primary — added to repeat the same "
         "EMCOMM-NET signal into more rooms or outdoor areas. Optional; add them only when "
         "the space is larger than one router covers."],
    ], widths=[1.4*inch, CW-1.4*inch]))
    s.append(SP(6))

    s.append(P('35.2  Recommended Router — ASUS RT-BE58 Go', H2))
    s.append(P(
        "The ASUS RT-BE58 Go is the recommended primary router for FieldCommand IMS. It is "
        "a compact, travel-sized Wi-Fi 7 router built for mobile deployments — it runs on "
        "USB-C power, supports AiMesh for seamless coverage extension, and can take a "
        "cellular or satellite internet source on its Wide Area Network (WAN) uplink port. "
        "It is available from most electronics retailers for roughly $100 to $130. In the "
        "FieldCommand kit it plays two roles at once: the access point (AP) that makes the "
        "Wi-Fi signal, and the Dynamic Host Configuration Protocol (DHCP) server that hands "
        "out addresses."))
    s.append(SP(4))
    s.append(tbl(['SPEC', 'RT-BE58 Go'], [
        ['Wi-Fi standard',  'Wi-Fi 7 (802.11be) — backward compatible with all older devices'],
        ['Bands',           '2.4 GHz + 5 GHz dual-band'],
        ['WAN uplink',      '2.5 gigabit port — takes an optional cellular or satellite internet source'],
        ['Power',           'USB-C, about 18 watts — runs from a USB-C adapter or a battery bank'],
        ['AiMesh support',  'Yes — extends EMCOMM-NET with additional identical RT-BE58 Go units'],
        ['Typical range',   'About 2,500 square feet indoors; larger outdoors'],
        ['Recommended qty', '3 (1 primary + 2 mesh nodes) for the standard kit'],
    ], widths=[1.5*inch, CW-1.5*inch]))
    s.append(note(
        "The router is set up once, at the bench, during the build — you do not touch it "
        "during an activation. Operators only ever join the Wi-Fi it broadcasts.", 'note'))
    s.append(SP(6))

    s.append(P('35.3  The Fixed Addresses on EMCOMM-NET', H2))
    s.append(P(
        "A handful of addresses are fixed on purpose so that fault-finding is easy and the "
        "address operators type never collides with anything. Internet Protocol (IP) "
        "addresses are just each device number on the network. Learn these four and the "
        "network holds no surprises:"))
    s.append(SP(4))
    s.append(tbl(['ADDRESS', 'WHAT IT IS'], [
        ['192.168.50.1',
         "The FieldCommand application server (the main Raspberry Pi 5). This is the "
         "address everyone opens in a browser — every tool lives here."],
        ['192.168.50.2',
         "The 44Net / Amateur Packet Radio Network (AMPRNet) gateway — the optional second "
         "Pi. Only amateur-radio groups use it; it is kept separate so it can never "
         "interfere with the main server."],
        ['192.168.50.254',
         "The ASUS router itself — its own admin page. Kept deliberately apart from the "
         "server so 192.168.50.1 stays clean. Reach it at http://192.168.50.254."],
        ['192.168.50.100 to .200',
         "The pool of addresses the router hands out automatically to phones, tablets, and "
         "laptops as they join EMCOMM-NET. The operator does nothing."],
    ], widths=[1.7*inch, CW-1.7*inch]))
    s.append(note(
        "If a device shows an address that is not in the 192.168.50.x range, it did not get "
        "one from the router. Turn its Wi-Fi off and on to rejoin EMCOMM-NET and pick up a "
        "fresh address, and remove any manually-set IP so it uses automatic (DHCP).", 'tip'))
    s.append(SP(6))

    s.append(P('35.4  UniFi Switch Lite 16 PoE — The Wiring Hub', H2))
    s.append(P(
        "The Ubiquiti UniFi Switch Lite 16 PoE is the central wiring hub. It has 16 gigabit "
        "Ethernet ports: 8 of them supply Power over Ethernet (PoE) — sending electricity "
        "down the same network cable that carries data, so a camera or an extra access "
        "point needs no separate power brick — and 8 are ordinary data-only ports. It also "
        "has 2 high-speed fiber uplink slots a basic build never needs. Wiring the ports in "
        "this exact order keeps every address predictable and makes fault-finding easy:"))
    s.append(SP(4))
    s.append(tbl(['PORT', 'WHAT PLUGS IN'], [
        ['Port 1',      'ASUS RT-BE58 Go router (LAN uplink) — the wired link to the router.'],
        ['Port 2',      'FieldCommand Pi 5 (the main server) — fixed 192.168.50.1.'],
        ['Port 3',      '44Net gateway Pi 5 — fixed 192.168.50.2. Optional; only if you run 44Net.'],
        ['Port 4',      'Windows laptop (Winlink / JS8Call station). Can join by Wi-Fi instead.'],
        ['Port 5',      'Shared color multifunction printer (MFP). Can join by Wi-Fi instead.'],
        ['Ports 6-9',   'Operator workstations — up to four Raspberry Pi 500 units, one per port.'],
        ['Port 10',     'Satellite dish (optional) — only if you use a satellite upstream source.'],
        ['Ports 11-12', 'AiMesh nodes — the wired backhaul for coverage extension (see 35.5).'],
        ['Ports 13-16', 'Spare — room to grow; plug in anything else you bring.'],
    ], widths=[1.1*inch, CW-1.1*inch]))
    s.append(P(
        "The UniFi management interface shows each port live — link status, speed, and PoE "
        "power draw — which makes it quick to see at a glance whether a cable is seated and "
        "a device is talking. The included 45-watt power supply runs the whole switch and "
        "budgets power across the eight PoE ports."))
    s.append(SP(6))

    s.append(P('35.5  Extending Coverage with AiMesh', H2))
    s.append(P(
        "One RT-BE58 Go covers a single room easily. For a multi-room emergency operations "
        "center (EOC), a whole building, or an outdoor staging area, add one or two more of "
        "the same routers as AiMesh nodes. AiMesh is ASUS's built-in mesh feature: because "
        "every node broadcasts the same EMCOMM-NET name (its Service Set Identifier, or "
        "SSID) and the same password, a phone or laptop moves from one node to the next "
        "automatically — no reconnecting and no re-entering the password. Nodes connect back "
        "to the primary through the switch with a real Ethernet cable, which is far faster "
        "and more reliable than letting them talk over Wi-Fi."))
    s.append(SP(4))
    s += steps([
        "Run a CAT 6 patch cable from a spare UniFi switch port (11 or 12) to the "
        "node's LAN port. This wired link between routers is called the backhaul.",
        "Power the node on with its USB-C supply. Give it about a minute to boot.",
        "Open the primary router's admin page at <b>http://192.168.50.254</b> and sign in "
        "(or use the ASUS Router app).",
        "Go to the <b>AiMesh</b> page and click <b>Add AiMesh Node</b>. The new node "
        "appears automatically once it is found.",
        "Click <b>Connect</b>. The node joins the mesh and begins broadcasting EMCOMM-NET "
        "within about 60 seconds; the primary pushes it the name, password, and settings.",
        "Place the node where coverage is needed, overlapping the primary by 20 to 30 "
        "percent, and confirm a phone still shows full signal at the farthest point.",
    ])
    s.append(SP(6))

    s.append(P('35.6  How Many Nodes Do I Need?', H2))
    s.append(P(
        "Match the number of routers to the size and shape of the space, then walk the far "
        "corners with a phone on EMCOMM-NET to confirm the signal holds. You do not have to "
        "deploy all three routers — bring what the space needs and leave the rest in the "
        "case."))
    s.append(SP(4))
    s.append(tbl(['YOUR SPACE', 'RECOMMENDED SETUP'], [
        ['Single-room EOC (under 2,500 sq ft)',
         '1 primary router only — no extension needed.'],
        ['Multi-room EOC or large shelter (2,500-7,500 sq ft)',
         '1 primary + 1 node, wired backhaul via switch Port 11.'],
        ['Large building or campus (7,500-20,000 sq ft)',
         '1 primary + 2 nodes, wired backhaul via switch Ports 11 and 12.'],
        ['Outdoor SAR staging area',
         '1 primary at the command post + 1-2 nodes at field positions, each on battery power.'],
    ], widths=[2.4*inch, CW-2.4*inch]))
    s.append(note(
        "Add a node only when a phone starts dropping bars at the edge of your coverage. A "
        "small activation in one room runs perfectly on the single primary router.", 'note'))
    s.append(SP(6))

    s.append(P('35.7  Keeping the Internet Side Separate', H2))
    s.append(P(
        "EMCOMM-NET runs fine with no internet at all — that is the whole point. If you do "
        "want an upstream connection for the features that use it (weather radar, "
        "propagation data, some lookups), the internet source plugs into the router's WAN "
        "uplink port, not the switch. The primary source is a cellular modem, with a "
        "satellite link as an automatic fallback. The router keeps the internet side and "
        "the operator side apart and bridges traffic across only when a WAN source is up. "
        "That separation is why unplugging the internet never disturbs the operators: they "
        "are on a different side of the router entirely, still reaching 192.168.50.1 as "
        "normal."))
    s.append(note(
        "Never wire an internet source into the UniFi switch. Internet always enters through "
        "the router's WAN port so the router can protect the local network. See the WAN "
        "Source Configuration page for switching and monitoring the upstream sources.", 'warn'))
    s.append(SP(6))

    s.append(P('35.8  Power Considerations', H2))
    s.append(P(
        "For field deployments without shore power, FieldCommand IMS can run from two Astron "
        "RS-35M-AP regulated linear power supplies (one per Pi cluster) fed from a portable "
        "generator, or from a high-capacity lithium iron phosphate (LiFePO4) battery with a "
        "pure-sine inverter. The complete system — both Pis, the router, and the switch — "
        "draws roughly 80 to 120 watts under typical load. For battery-only operation, a "
        "100 amp-hour 12-volt LiFePO4 battery gives about 8 to 10 hours of runtime. The "
        "router itself runs from any USB-C source, so a small power bank keeps EMCOMM-NET "
        "alive on its own even while you swap the main supply."))
    s.append(SP(6))

    s.append(P('35.9  Common Questions', H2))
    s.append(tbl(['QUESTION', 'ANSWER'], [
        ['Does the Raspberry Pi make the Wi-Fi?',
         "No. The ASUS router makes EMCOMM-NET. Both Pis are servers on the network; if the "
         "router loses power, the Wi-Fi goes down even though the Pis are still running."],
        ['I joined EMCOMM-NET but the page will not load.',
         "Confirm you typed the full address including http:// (for example "
         "http://192.168.50.1) and that you are on EMCOMM-NET, not a nearby Wi-Fi. Check "
         "that the router and the application-server Pi both have power."],
        ['Do the mesh nodes have to be cabled?',
         "It is strongly recommended. A wired backhaul (a cable from switch Port 11 or 12 "
         "to the node) is faster and far more reliable and does not eat into operator "
         "Wi-Fi speed. Nodes can link over Wi-Fi in a pinch, but cable them when you can."],
        ['Can I rename EMCOMM-NET to my group name?',
         "Yes. EMCOMM-NET is only the default network name. Change it on the router (or in "
         "the FieldCommand Setup screen). It is never tied to a callsign or a group."],
        ['A node will not join the AiMesh.',
         "Pair it the router maker's way — through the router's AiMesh page or app, not "
         "through FieldCommand. Then confirm the node hands out addresses in the "
         "192.168.50.x range before you rely on it."],
        ['Do I have to buy all three routers and four workstations?',
         "No. One primary router and one Pi cover the core system; nodes and workstations "
         "are recommended, not required. Any phone, tablet, or laptop on EMCOMM-NET is a "
         "full station."],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(PB())
    return s


def ch_appendix():
    s = chapter(36, 'Appendix — Quick Reference & Administration',
                '')
    s.append(P(
        'This appendix is the fold-out map at the back of the manual. It gathers, in one '
        'place, the facts you reach for again and again once FieldCommand IMS is running: '
        'the web address of every page, the network ports and background services that keep '
        'the system alive, the handful of routine administration tasks that keep it healthy, '
        'and a plain-language list of every abbreviation used in this book. Nothing here is '
        'new material — it is a fast lookup for things explained in full in the earlier '
        "chapters, arranged so a person who opens straight to this page still finds what "
        'they need.', Lead))
    s.append(SP(4))
    s.append(note(
        'In one sentence: keep this appendix open in a second browser tab during an '
        'activation, and you will rarely need to hunt through the rest of the manual.',
        'tip'))
    s.append(SP(6))

    s.append(P('36.1  How to Use This Appendix', H2))
    s.append(P(
        'Every device on the incident reaches FieldCommand IMS the same way. Join the '
        '<b>EMCOMM-NET</b> Wi-Fi network, open any web browser (Chrome, Safari, Edge, '
        'Firefox — any of them work), and type the server address into the address bar. '
        'The server address is <b>192.168.50.1</b>. There is no app to install, no account '
        'to create, and no password to the dashboard. The page tables below list every '
        'address, but you only ever need to remember the one number: 192.168.50.1.'))
    s.append(SP(4))
    s.append(note(
        'If you type 192.168.50.1 and nothing loads, you are almost always on the wrong '
        "Wi-Fi network. Check that your phone or laptop is connected to EMCOMM-NET and not "
        'to a cellular data connection or a different Wi-Fi, then reload the page.', 'warn'))
    s.append(SP(6))

    s.append(P('36.2  All Pages — Web Address (URL) Reference', H2))
    s.append(P(
        'Below is every page in FieldCommand IMS with its web address (Uniform Resource '
        'Locator, or URL) and what it does. To open any of them, type the address shown '
        'into the browser. For example, to open the main dashboard, type '
        '<b>192.168.50.1/index.html</b>. You can also reach every page from the buttons on '
        'the main dashboard, so you rarely need to type these by hand.'))
    s.append(SP(4))
    pages = [
        ('index.html',             'Main Dashboard'),
        ('incident.html',          'Incident Management / Command Section'),
        ('incident_mgmt.html',     'Incident Archive, Restore, Delete, Beta Reset'),
        ('event_templates.html',   'Pre-Planned Event Templates'),
        ('resources.html',         'Resource Board (flat list)'),
        ('ics/operations.html',    'T-Card Resource Board (drag-and-drop)'),
        ('resource_map.html',      'GPS-Tracked Resource Map'),
        ('resource_types.html',    'National Incident Management System (NIMS) Resource Typing Library'),
        ('checkin.html',           'Manual Check-In (ICS-211)'),
        ('scan_checkin.html',      'Quick Response (QR) code / Barcode Scan Check-In'),
        ('roster.html',            'Member Roster and QR Code Generator'),
        ('netcontrol.html',        'Amateur Radio Net Control Logger'),
        ('starcom.html',           'Public Safety Net Logger'),
        ('observer.html',          'Observer Mode — Read-Only Net View'),
        ('deadmans.html',          "Dead Man's Switch"),
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
        ('resmap.html',            'Public Safety Resource Map'),
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
    s.append(tbl(['WEB ADDRESS', 'PAGE'],
        [[f'192.168.50.1/{p}', d] for p, d in pages],
        widths=[2.1*inch, CW-2.1*inch]))
    s.append(SP(6))

    s.append(P('36.3  Network Ports — For the System Administrator', H2))
    s.append(P(
        'You do not need this table to use FieldCommand IMS. It is here for the person who '
        'maintains the server. Behind the scenes, the dashboard is served by the web server '
        '(nginx) on the standard web port, and several small Application Programming '
        'Interface (API) programs each handle one job on their own network port. If a '
        'feature stops working, this table tells the administrator which program to look at.'))
    s.append(SP(4))
    s.append(tbl(['PORT', 'PROGRAM', 'WHAT IT HANDLES'], [
        ['80',   'nginx',                  'Serves every HTML page and static file on the dashboard'],
        ['5050', 'fcc_lookup_server.py',   'Core API — FCC callsign lookup, nets and roster, hospitals, repeaters, resource types, facilities, GPS and dead-man switch, WAN configuration'],
        ['5051', 'health_monitor.py',      'System health — processor, memory, and disk use, service states, and the connectivity roll-up'],
        ['5055', 'ics_platform_server.py', 'ICS platform — incidents, ICS forms, T-cards, check-ins, the IAP, and FEMA cost documentation'],
        ['5056', 'reference_server.py',    'Offline reference library (renders the PDF documents)'],
        ['8083', 'tile_server.py',         'Offline map tiles (MBTiles), used by every map when there is no internet'],
        ['9000', 'amprgate_status.py',     '44Net status — read-only, on the gateway Pi at 192.168.50.2'],
        ['9001', 'amprgate_status.py',     '44Net tunnel control — reachable only on the gateway Pi itself'],
    ], widths=[0.55*inch, 1.75*inch, CW-2.3*inch]))
    s.append(SP(4))
    s.append(note(
        'The ICS platform lives on port <b>5055</b>. The health monitor is <b>5051</b>. '
        'These two are easy to confuse; they are different programs doing different jobs.',
        'note'))
    s.append(SP(6))

    s.append(P('36.4  Background Services', H2))
    s.append(P(
        'Each program above runs as a background service that starts by itself when the '
        'server powers on and restarts on its own if it ever stops. The administrator '
        'manages them by name. This is the list of service names and what each one keeps '
        'running.'))
    s.append(SP(4))
    s.append(tbl(['SERVICE NAME', 'WHAT IT KEEPS RUNNING'], [
        ['ics-platform.service',          'ICS platform server (port 5055)'],
        ['fcc-lookup.service',            'FCC lookup and configuration server (port 5050)'],
        ['health-monitor.service',        'System health monitor (port 5051)'],
        ['fieldcommand-refs.service',     'Offline reference library server (port 5056)'],
        ['fieldcommand-tiles.service',    'Offline map tile server (port 8083)'],
        ['deadmans.service',              'Per-net dead-man switch monitor'],
        ['wan-monitor.service',           'WAN source monitoring and failover'],
        ['aprs-rf.service',               'RF APRS receive by way of Direwolf or a Terminal Node Controller (TNC)'],
        ['amprgate-poll.service',         '44Net tunnel keepalive and reconnect (gateway Pi)'],
        ['backup.service / backup.timer', 'Nightly SQLite backup to the external Universal Serial Bus (USB) drive'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(SP(6))

    s.append(P('36.5  Everyday Administration Tasks', H2))
    s.append(P(
        'Almost everything in FieldCommand IMS is done from the browser, so day-to-day there '
        'is nothing to administer. The short list below covers the rare occasions when '
        'someone needs to touch the server itself. For the exact commands, see the '
        'FieldCommand Installation Guide; the steps here describe what to do in plain terms.'))
    s.append(SP(4))
    s.append(P('36.5.1  Checking That Everything Is Healthy', H3))
    s += steps([
        'Open the main dashboard at <b>192.168.50.1</b>.',
        'Look at the <b>System Health</b> panel. Green indicators mean the processor, '
        'memory, disk, and every background service are in good shape.',
        'For more detail, open <b>Preflight Deployment Checklist</b> '
        '(192.168.50.1/preflight.html), which walks through each service and reports any '
        'that need attention before you rely on the system in the field.',
    ])
    s.append(SP(4))
    s.append(P('36.5.2  Restarting the Server', H3))
    s.append(P(
        'A clean restart fixes most transient problems. Power the Raspberry Pi 5 server off '
        'and back on, wait about two minutes for it to finish starting, then reload the '
        'dashboard. Every background service starts automatically, so nothing needs to be '
        'launched by hand. Because all incident data is saved to disk, a restart never loses '
        'any of your work.'))
    s.append(SP(4))
    s.append(note(
        'If a single feature is misbehaving but the rest of the dashboard is fine, the '
        'administrator can restart just that one background service by name (from the table '
        'in 36.4) instead of restarting the whole server.', 'tip'))
    s.append(SP(6))

    s.append(P('36.6  Backups and Keeping Data Safe', H2))
    s.append(P(
        'Incident data in FieldCommand IMS is permanent — the system is built to save '
        'everything an incident produces (nets, logs, ICS forms, T-cards, the IAP, cost '
        'records, resources, roster snapshots, and attachments) and never treat any of it '
        'as throwaway. That data lives in a database on the server and is copied to an '
        'external USB drive automatically.'))
    s.append(SP(4))
    s.append(tbl(['WHAT', 'HOW IT IS PROTECTED'], [
        ['Live data',
         'Written to the server database as you work, using the standard SQLite storage '
         'engine. It survives a restart or a power loss.'],
        ['Nightly backup',
         'The backup service copies the whole database to the external USB drive every '
         'night on a timer, with no action needed from you.'],
        ['Archived incidents',
         'When an incident closes, you archive it from the Incident Archive page '
         '(192.168.50.1/incident_mgmt.html); the archive is kept and can be restored later.'],
    ], widths=[1.6*inch, CW-1.6*inch]))
    s.append(SP(4))
    s.append(note(
        'Confirm the external backup drive is plugged in and recognized before an '
        'activation. The nightly backup can only run if the drive is connected. Keeping a '
        'second copy of the drive off-site is good practice for records you must retain.',
        'warn'))
    s.append(SP(6))

    s.append(P('36.7  Two Networks and Two Maps — Quick Reference', H2))
    s.append(P(
        'Two pairs of things in FieldCommand IMS are commonly confused. This is the '
        'one-glance reminder of which is which.'))
    s.append(SP(4))
    s.append(P('36.7.1  The Two Servers', H3))
    s.append(P(
        'FieldCommand IMS runs on two Raspberry Pi 5 units. The <b>application server</b> '
        'is the one you reach at 192.168.50.1 — it serves the whole dashboard. The '
        '<b>44Net gateway</b> is a separate Pi at 192.168.50.2 that handles the Amateur '
        'Packet Radio Network (AMPRNet, also called 44Net) tunnel. Everyday users only ever '
        'talk to 192.168.50.1.'))
    s.append(SP(4))
    s.append(P('36.7.2  The Two Maps', H3))
    s.append(tbl(['MAP', 'WHAT FEEDS IT'], [
        ['Tactical APRS Map (tactical.html)',
         'Live amateur-radio APRS heard off the air. Direwolf decodes the packets, a feed '
         'program serves them, and the map shows the stations automatically. This is the '
         'big-screen situational-awareness display.'],
        ['Public Safety Resource Map (resmap.html)',
         'Objects you place by hand — "+ Add Unit" and "Draw Zone". It is not fed by radio '
         'and never connects to APRS. It is the public-safety side of the picture.'],
    ], widths=[2.0*inch, CW-2.0*inch]))
    s.append(SP(4))
    s.append(note(
        'The GPS-Tracked Resource Map (resource_map.html) is a third, separate map that '
        'tracks resources by their reported location; do not confuse it with either of the '
        'two above.', 'note'))
    s.append(SP(6))

    s.append(P('36.8  When the Internet Is and Is Not Available', H2))
    s.append(P(
        'FieldCommand IMS is offline-first: the full tool set works with zero internet. A '
        'few features simply add live data when a Wide Area Network (WAN) connection is '
        'present and quietly step aside when it is not. Knowing which is which prevents '
        '"is it broken?" questions in the field.'))
    s.append(SP(4))
    s.append(tbl(['FEATURE', 'NEEDS INTERNET?'], [
        ['Incidents, ICS forms, T-cards, IAP, cost documentation', 'No — always available'],
        ['Net loggers, roster, check-in, resource boards', 'No — always available'],
        ['Offline maps and the reference library', 'No — served locally from the Pi'],
        ['Animated NEXRAD radar', 'Yes — appears when a WAN is connected'],
        ['HF propagation data and some online lookups', 'Yes — appears when a WAN is connected'],
    ], widths=[CW-1.9*inch, 1.9*inch]))
    s.append(SP(4))
    s.append(P(
        'The WAN Source Configuration page (192.168.50.1/wan_settings.html) is where the '
        'administrator selects and monitors the internet source; the WAN Status page '
        '(192.168.50.1/wan-status.html) shows whether one is currently connected.'))
    s.append(SP(6))

    s.append(P('36.9  Abbreviations and Acronyms', H2))
    s.append(P(
        'Every abbreviation is spelled out in full the first time it appears in each '
        'chapter. This table repeats the common ones in one place, for a reader who opens '
        'the manual to the middle.'))
    s.append(SP(4))
    s.append(tbl(['SHORT FORM', 'FULL MEANING'], [
        ['APRS',    'Automatic Packet Reporting System'],
        ['AMPRNet', 'Amateur Packet Radio Network (the 44Net address range)'],
        ['API',     'Application Programming Interface'],
        ['CTCSS',   'Continuous Tone-Coded Squelch System (a sub-audible tone)'],
        ['EMCOMM',  'Emergency Communications'],
        ['EOC',     'Emergency Operations Center'],
        ['FCC',     'Federal Communications Commission'],
        ['FEMA',    'Federal Emergency Management Agency'],
        ['HF',      'High Frequency'],
        ['IAP',     'Incident Action Plan'],
        ['ICS',     'Incident Command System'],
        ['NEXRAD',  'Next Generation Radar'],
        ['NIMS',    'National Incident Management System'],
        ['NTS',     'National Traffic System'],
        ['NWS',     'National Weather Service'],
        ['PA',      'Public Assistance (the FEMA reimbursement program)'],
        ['PDF',     'Portable Document Format'],
        ['QR',      'Quick Response (code)'],
        ['SAR',     'Search and Rescue'],
        ['TNC',     'Terminal Node Controller'],
        ['UHF',     'Ultra High Frequency'],
        ['URL',     'Uniform Resource Locator (a web address)'],
        ['USB',     'Universal Serial Bus'],
        ['VHF',     'Very High Frequency'],
        ['WAN',     'Wide Area Network (an internet connection)'],
    ], widths=[1.3*inch, CW-1.3*inch]))
    s.append(SP(6))

    s.append(P('36.10  Copyright and License', H2))
    s.append(P(
        'FieldCommand IMS v1.0 — Copyright &copy; 2026 James Rospopo KE4CON. Developed for '
        'emergency management and amateur radio organizations. The software is released '
        'under the GNU Affero General Public License version 3 (AGPLv3); the documentation, '
        'including this manual, is released under the Creative Commons Attribution-ShareAlike '
        '4.0 (CC BY-SA 4.0) license. Source code and the latest documentation are available '
        'at https://github.com/KE4CON/FieldCommand-IMS.'))
    s.append(SP(6))

    s.append(P('36.11  Common Questions', H2))
    s.append(tbl(['QUESTION', 'ANSWER'], [
        ['What is the one address I need to remember?',
         '192.168.50.1 — type it into any browser after joining the EMCOMM-NET Wi-Fi.'],
        ['Do I need to install anything or log in?',
         'No. Any smartphone, tablet, or laptop reaches the whole dashboard through a web '
         'browser with no app and no account.'],
        ['A page will not load. What do I check first?',
         'Confirm your device is on the EMCOMM-NET Wi-Fi (not cellular or another network), '
         'then reload. This fixes the large majority of "cannot connect" reports.'],
        ['Will I lose my work if the power drops?',
         'No. Incident data is saved to disk as you work and backed up nightly to the '
         'external USB drive; a restart never loses saved work.'],
        ['Why is the radar blank?',
         'NEXRAD radar needs an internet (WAN) connection. With no WAN, it is expected to '
         'be blank while every offline tool keeps working.'],
        ['Which map is fed by radio?',
         'Only the Tactical APRS Map (tactical.html). The Public Safety Resource Map '
         '(resmap.html) is hand-entered and never touches radio.'],
    ], widths=[2.2*inch, CW-2.2*inch]))
    s.append(PB())
    return s

