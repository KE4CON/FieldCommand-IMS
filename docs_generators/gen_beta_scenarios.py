#!/usr/bin/env python3
"""
FieldCommand IMS v1.0 — Beta Test Scenarios Generator
Six step-by-step test scenarios covering all 49 web tools.
Output: /mnt/user-data/outputs/FieldCommand_BetaTest_Complete_Package.pdf
"""
import datetime, io
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.pdfgen import canvas

# ── Palette ───────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
LGRAY  = HexColor('#f0f3f6')
MGRAY  = HexColor('#e0e8f0')
GREEN  = HexColor('#1a7a3a')
GREEN_BG = HexColor('#e8f5ec')
AMBER  = HexColor('#c8760a')
AMBER_BG = HexColor('#fdf4e0')
RED    = HexColor('#b82020')
RED_BG = HexColor('#fdecea')
WARN_BG  = HexColor('#fff8e1')

SHORT = 'FieldCommand IMS v1.0'
TODAY = datetime.date.today().strftime('%B %d, %Y')
PAGE_W, PAGE_H = letter
M  = 0.65 * inch
CW = PAGE_W - 2*M

# ── Canvas with per-scenario headers ─────────────────────────────────────────
class NC(canvas.Canvas):
    SCENARIO_HEADER = ''   # set before building each scenario

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self._saved = []

    def showPage(self):
        self._saved.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved)
        for st in self._saved:
            self.__dict__.update(st)
            self.TOTAL = total
            n = self._pageNumber
            if n == 1:
                self._draw_cover()
            else:
                # Header bar
                self.setFillColor(EOC)
                self.rect(0, PAGE_H-0.38*inch, PAGE_W, 0.38*inch, fill=1, stroke=0)
                self.setFillColor(GOLD)
                self.rect(0, PAGE_H-0.40*inch, PAGE_W, 0.02*inch, fill=1, stroke=0)
                self.setFillColor(white)
                self.setFont('Helvetica-Bold', 8)
                self.drawString(M, PAGE_H-0.25*inch, SHORT)
                self.setFont('Helvetica', 8)
                self.drawRightString(PAGE_W-M, PAGE_H-0.25*inch,
                    'Beta Test Scenarios  ·  FOR BETA TESTING USE ONLY')
                # Footer bar
            self.setFillColor(EOC)
            self.rect(0, 0, PAGE_W, 0.30*inch, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, 0.30*inch, PAGE_W, 0.013*inch, fill=1, stroke=0)
            self.setFillColor(white)
            self.setFont('Helvetica', 6.5)
            if n > 1:
                self.drawString(M, 0.10*inch,
                    f'FieldCommand IMS v1.0  ·  Beta Test Package  ·  {TODAY}')
                self.drawString(M*5, 0.10*inch,
                    'Copyright \u00a9 2026 James Rospopo KE4CON')
                self.drawRightString(PAGE_W-M, 0.10*inch, f'Page {n} of {total}')
            super().showPage()
        super().save()

    def _draw_cover(self):
        self.setFillColor(HexColor('#1a3a6b'))
        self.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        self.setFillColor(HexColor('#f0c040'))
        self.rect(0, PAGE_H-0.18*inch, PAGE_W, 0.18*inch, fill=1, stroke=0)
        self.rect(0, 0, PAGE_W, 0.18*inch, fill=1, stroke=0)
        self.setFillColor(HexColor('#1e4480'))
        self.rect(0, PAGE_H*0.38, PAGE_W, PAGE_H*0.36, fill=1, stroke=0)
        self.setFillColor(HexColor('#f0c040'))
        self.setFont('Helvetica-Bold', 10)
        self.drawCentredString(PAGE_W/2, PAGE_H-0.70*inch, 'KE4CON  \u00b7  FieldCommand IMS')
        self.setFillColor(HexColor('#c0d4f0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H-0.88*inch,
            'McHenry County Emergency Services Volunteers  \u00b7  K9ESV')
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 58)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.60, 'FIELDCOMMAND')
        self.setFillColor(GOLD)
        self.setFont('Helvetica-Bold', 15)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.545, 'Incident Management System  v1.0')
        self.setStrokeColor(GOLD)
        self.setLineWidth(1.5)
        self.line(M*2, PAGE_H*0.505, PAGE_W-M*2, PAGE_H*0.505)
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 26)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.448, 'BETA TEST SCENARIOS')
        self.setFillColor(HexColor('#c0d4f0'))
        self.setFont('Helvetica', 10)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.395, 'Six Step-by-Step Scenarios \u00b7 All 49 Tools')
        self.setFillColor(HexColor('#8090c0'))
        self.setFont('Helvetica', 9.5)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.30,
            'Scenario 1: Setup  \u00b7  2: Personnel  \u00b7  3: ICS  \u00b7  4: Amateur Radio  \u00b7  5: FEMA  \u00b7  6: Multi-Op')
        self.setFillColor(HexColor('#6070a0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.25, TODAY)
        self.setFillColor(HexColor('#6070a0'))
        self.setFont('Helvetica', 7.5)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.08,
            'FOR BETA TESTING USE ONLY \u2014 NOT FOR OPERATIONAL USE')
        self.setFillColor(HexColor('#1a3a6b'))
        self.setFont('Helvetica', 7)
        self.drawCentredString(PAGE_W/2, 0.05*inch,
            f'Copyright \u00a9 2026 James Rospopo KE4CON  \u00b7  {TODAY}')


# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=black,
             leading=12, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

def P(t, s=None):  return Paragraph(t, s or S('b'))
def SP(n=4):       return Spacer(1, n)
def PB():          return PageBreak()
def HR(c=LINE, t=0.5):
    return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=2, spaceAfter=2)

def scenario_cover(num, title, duration, features, pages):
    """Full-page scenario divider/cover."""
    elements = []
    elements.append(SP(30))
    # Big scenario badge
    badge = Table([[
        P(f'FIELDCOMMAND', S('fc', fontName='Helvetica-Bold', fontSize=28,
                              textColor=white, alignment=TA_CENTER, leading=32)),
        SP(4),
        P('Incident Management System v1.0', S('fc2', fontName='Helvetica-Bold', fontSize=11,
                                                textColor=GOLD, alignment=TA_CENTER, leading=14)),
        SP(8),
        P('BETA TEST SCENARIOS', S('bts', fontName='Helvetica-Bold', fontSize=16,
                                    textColor=GOLD, alignment=TA_CENTER, leading=20)),
        SP(6),
        P(f'Scenario {num} of 6', S('sn', fontName='Helvetica-Bold', fontSize=20,
                                     textColor=white, alignment=TA_CENTER, leading=24)),
        SP(4),
        P(title, S('st', fontName='Helvetica-Bold', fontSize=13,
                   textColor=HexColor('#c0d4f0'), alignment=TA_CENTER, leading=16)),
    ]], colWidths=[CW])
    badge.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), EOC),
        ('TOPPADDING',    (0,0), (-1,-1), 24),
        ('BOTTOMPADDING', (0,0), (-1,-1), 24),
        ('LEFTPADDING',   (0,0), (-1,-1), 16),
        ('RIGHTPADDING',  (0,0), (-1,-1), 16),
    ]))
    elements.append(badge)
    elements.append(SP(12))
    # Summary strip
    strip_data = [[
        P('SCENARIO', S('sl', fontName='Helvetica-Bold', fontSize=7.5, textColor=EOC_LT, leading=10)),
        P('DURATION', S('sl', fontName='Helvetica-Bold', fontSize=7.5, textColor=EOC_LT, leading=10)),
        P('FEATURES TESTED', S('sl', fontName='Helvetica-Bold', fontSize=7.5, textColor=EOC_LT, leading=10)),
        P('PAGES EXERCISED', S('sl', fontName='Helvetica-Bold', fontSize=7.5, textColor=EOC_LT, leading=10)),
    ],[
        P(f'{num} of 6', S('sv', fontName='Helvetica-Bold', fontSize=9, leading=12)),
        P(duration, S('sv', fontSize=8.5, leading=12)),
        P(features, S('sv', fontSize=8, leading=11)),
        P(pages, S('sv', fontSize=7.5, leading=10, textColor=HexColor('#334466'))),
    ]]
    strip = Table(strip_data, colWidths=[0.7*inch, 0.9*inch, 2.6*inch, CW-4.2*inch],
                  repeatRows=1)
    strip.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  MGRAY),
        ('BACKGROUND',    (0,1), (-1,1),  LGRAY),
        ('GRID',          (0,0), (-1,-1), 0.4, LINE),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    elements.append(strip)
    elements.append(SP(8))
    # FOR BETA TESTING label
    label = Table([[P('FOR BETA TESTING USE ONLY \u2014 NOT FOR OPERATIONAL USE',
                      S('bt', fontName='Helvetica-Bold', fontSize=8, textColor=white,
                        alignment=TA_CENTER, leading=11))]],
                  colWidths=[CW])
    label.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), RED),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(label)
    elements.append(PB())
    return elements


def test_header(num, title):
    """Bold test section header."""
    t = Table([[
        P(f'TEST {num}', S('tn', fontName='Helvetica-Bold', fontSize=9,
                            textColor=white, alignment=TA_CENTER, leading=11)),
        P(f'\u2014  {title}', S('tt', fontName='Helvetica-Bold', fontSize=10,
                                  textColor=white, leading=13)),
    ]], colWidths=[0.65*inch, CW-0.65*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), EOC_LT),
        ('BACKGROUND',    (1,0), (1,-1), EOC),
        ('TOPPADDING',    (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('LINEBELOW',     (0,0), (-1,-1), 2, GOLD),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def step(num, action, expected, url=None):
    """One numbered test step with expected result."""
    url_str = f'<br/>Navigate to: <font face="Courier" size="8">{url}</font>' if url else ''
    action_txt = f'<b>Step {num}.</b> {action}{url_str}'
    exp_txt = f'\u2192 <i>Expected:</i> {expected}'
    t = Table([[
        P(action_txt, S('sa', fontSize=8.5, leading=12)),
        P(exp_txt, S('se', fontSize=8, leading=11,
                     textColor=HexColor('#1a5a2a'))),
    ]], colWidths=[CW*0.52, CW*0.48])
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, LGRAY]),
        ('GRID',           (0,0), (-1,-1), 0.3, LINE),
        ('TOPPADDING',     (0,0), (-1,-1), 4),
        ('BOTTOMPADDING',  (0,0), (-1,-1), 4),
        ('LEFTPADDING',    (0,0), (-1,-1), 6),
        ('RIGHTPADDING',   (0,0), (-1,-1), 6),
        ('VALIGN',         (0,0), (-1,-1), 'TOP'),
        ('LINEAFTER',      (0,0), (0,-1), 0.5, EOC_LT),
    ]))
    return t


def prereq(text):
    """Black-bordered prerequisite / warning box."""
    t = Table([[P(f'\u25a0 {text}', S('pr', fontSize=8, leading=11,
                                       textColor=HexColor('#2a2a2a')))]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), WARN_BG),
        ('BOX',           (0,0), (-1,-1), 0.8, EOC_LT),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 8),
    ]))
    return t


def pf_table(tests):
    """Pass/Fail summary table for end of each scenario."""
    data = [[
        P('TEST', S('ph', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
        P('RESULT', S('ph', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
        P('NOTES / DEFECTS', S('ph', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    ]]
    for t in tests:
        data.append([
            P(t, S('pr', fontSize=8.5, leading=11)),
            P('\u25a0 Pass    \u25a0 Fail    \u25a0 Skip',
              S('pr', fontSize=8, leading=11, textColor=HexColor('#334466'))),
            P('', S('pr', fontSize=8, leading=11)),
        ])
    tbl = Table(data, colWidths=[2.4*inch, 1.4*inch, CW-3.8*inch], repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.4, LINE),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return tbl


def overall_result():
    t = Table([[
        P('Overall Scenario Result:', S('or', fontName='Helvetica-Bold', fontSize=9,
                                        textColor=EOC, leading=12)),
        P('\u25a0 PASS \u2014 All tests passed or only minor cosmetic issues noted\n'
          '\u25a0 CONDITIONAL \u2014 Passes with workaround (document defects above)\n'
          '\u25a0 FAIL \u2014 Critical defect found (document and halt further testing)',
          S('orv', fontSize=8.5, leading=13)),
    ]], colWidths=[1.8*inch, CW-1.8*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
        ('BOX',           (0,0), (-1,-1), 0.8, EOC_LT),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LEFTPADDING',   (0,0), (-1,-1), 8),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    return t


def tester_line(next_scenario=None):
    elems = []
    elems.append(SP(8))
    row = Table([[
        P('Tester (name / callsign):', S('tl', fontSize=8.5)),
        P('_______________________________', S('tl', fontSize=8.5)),
        P('Date:', S('tl', fontSize=8.5)),
        P('____________', S('tl', fontSize=8.5)),
        P('Time:', S('tl', fontSize=8.5)),
        P('____________', S('tl', fontSize=8.5)),
    ]], colWidths=[1.6*inch, 2.0*inch, 0.4*inch, 0.9*inch, 0.4*inch, CW-5.3*inch])
    row.setStyle(TableStyle([
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    elems.append(row)
    if next_scenario:
        elems.append(SP(6))
        elems.append(P(f'\u2713 Proceed to Scenario {next_scenario} only after this scenario passes.',
                       S('ns', fontSize=8.5, textColor=GREEN, fontName='Helvetica-Bold')))
    elems.append(PB())
    return elems


# ── Story ─────────────────────────────────────────────────────────────────────
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
story.append(SP(1))  # triggers cover page


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 1 — System Setup, Organization Configuration & Incident Creation
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(1,
    'System Setup, Organization Configuration & Incident Creation',
    '45\u201360 min',
    'Setup \u00b7 Dashboard \u00b7 Incident creation \u00b7 Templates \u00b7 Archive/Restore \u00b7 Beta reset',
    'setup.html \u00b7 index.html \u00b7 incident.html \u00b7 incident_mgmt.html \u00b7 event_templates.html \u00b7 preflight.html \u00b7 wan_settings.html'
)

story.append(P(
    'This scenario tests the complete first-run experience: connecting to FieldCommand IMS for the '
    'first time, configuring the organization identity, verifying the dashboard in all three modes, '
    'creating a new incident from scratch and from a pre-planned template, and testing the archive, '
    'restore, and scenario reset functions. Complete this scenario first before running any other.',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'Use a clean FieldCommand system with no prior data for this scenario. '
    'If the system has been used previously, run Beta Reset first '
    '(incident_mgmt.html \u2192 Beta/Scenario Reset) before starting.'))
story.append(SP(6))

# PRE-TEST CHECKLIST
story.append(P('<b>PRE-TEST CHECKLIST</b> \u2014 Verify the following before starting:',
               S('ptc', fontSize=9, textColor=EOC, fontName='Helvetica-Bold')))
story.append(SP(3))
for item in [
    'FieldCommand Pi 5 is powered on and has been running for at least 60 seconds',
    'Your test device (phone, tablet, or laptop) is connected to EMCOMM-NET Wi-Fi',
    'Browser is open to http://192.168.50.1',
    'No active incidents exist (or Beta Reset has been performed)',
    'Test roster CSV is prepared with at least 5 members (see Appendix A)',
    'Note the current time \u2014 you will need it for incident timestamps',
]:
    story.append(P(f'\u25a0  {item}', S('pc', fontSize=8.5, leading=12, leftIndent=12)))
story.append(SP(8))

# TEST 1
story.append(test_header(1, 'Organization Setup (setup.html)'))
story.append(SP(3))
story.append(P(
    'The Organization Setup page configures the station identity that appears on all ICS forms, '
    'net logs, and printed documents. Test that all fields save correctly and persist after a browser refresh.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
for n, action, expected in [
    (1, 'Navigate to the Organization Setup page.', 'Page loads with empty or default fields.',
     ),
    (2, 'Enter your organization name: <i>Beta Test Emergency Services</i>', 'Field accepts text input.'),
    (3, 'Enter short name: <i>BTES</i>', 'Field accepts 4-character abbreviation.'),
    (4, 'Enter primary callsign: <i>W8TEST</i>', 'Field accepts callsign format.'),
    (5, 'Enter agency name: <i>Beta County Emergency Management</i>', 'Field accepts text.'),
    (6, 'Enter city: <i>Testville</i> and state: <i>IL</i>', 'Location fields accept input.'),
    (7, 'Enter grid square: <i>EN52ab</i>', 'Grid square field accepts 6-character Maidenhead format.'),
    (8, 'Set time zone to your local time zone.', 'Dropdown shows all US time zones.'),
    (9, 'Click <b>Save Configuration</b>.', 'Success message appears. No error.'),
    (10, 'Press F5 to refresh the browser. Return to setup.html.', 'All fields still show the values you entered \u2014 data persisted to database.'),
    (11, 'Navigate to the main dashboard.', 'Dashboard header shows your organization name.'),
]:
    url = 'http://192.168.50.1/setup.html' if n in (1, 10) else ('http://192.168.50.1/index.html' if n == 11 else None)
    story.append(step(n, action, expected, url))
story.append(prereq('Record any fields that do NOT persist after refresh.'))
story.append(SP(8))

# TEST 2
story.append(test_header(2, 'Dashboard Navigation & WAN Status (index.html)'))
story.append(SP(4))
for n, action, expected in [
    (12, 'On the main dashboard, verify the WAN status bar is visible at the top.', 'WAN status bar shows \u2014 either green (Cellular), blue (Satellite), or red (Offline). Color matches actual internet availability.'),
    (13, 'Click the <b>All-Hazards ICS</b> mode tab.', 'Tool card grid changes to show ICS platform tools: Incident Management, T-Card Board, ICS Forms, FEMA costs, etc.'),
    (14, 'Click the <b>Amateur Radio EMCOMM</b> mode tab.', 'Grid shows Net Control Logger, FCC Callsign Lookup, APRS Map, Winlink, JS8Call, etc.'),
    (15, 'Click the <b>Public Safety</b> mode tab.', 'Grid shows Starcom Net Logger, Resource Map, WAN Status, Weather Radar, Hospitals.'),
    (16, 'Click every tool card visible in any mode and confirm each page loads. Note any cards that produce a 404 or error.', 'All cards navigate to the correct page. No 404 errors.'),
    (17, 'Wait 30 seconds and observe the WAN status bar.', 'Status bar refreshes automatically without a manual page reload.'),
]:
    url = 'http://192.168.50.1/index.html' if n == 12 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3
story.append(test_header(3, 'Preflight Deployment Checklist (preflight.html)'))
story.append(SP(3))
story.append(P(
    'The Preflight page auto-checks six data readiness items on page load: organization setup, '
    'FCC database (count + age), roster member count, repeater database (count + coordinates), '
    'channel library, and active incident. Verify both the auto-checks and the manual sections.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
for n, action, expected in [
    (18, 'Navigate to the Preflight Check page.', 'Page loads. <b>Data Readiness</b> section auto-runs 6 checks: org setup, FCC DB, roster count, repeater DB (with coordinate count), channel library, active incident.'),
    (19, 'Review the Data Readiness auto-check results.', 'Each item shows \u2713 (green) or \u2717 (red) with count/detail. Items with issues link directly to the fix page.'),
    (20, 'Work through each manual checklist section (Power, Comms, Computing, Personnel, Logistics, Safety, Coordination). Check every applicable item.', 'Each checkbox toggles and remains checked.'),
    (21, 'Add a note in the Notes field: <i>Beta test run \u2014 all hardware nominal</i>', 'Note field accepts free text.'),
    (22, 'Click <b>Save Preflight</b> or submit the form.', 'Success confirmation. Data saved.'),
    (23, 'Refresh the page.', 'Checked items and notes persist. Auto-checks re-run on reload.'),
    (24, 'Click <b>Print</b>.', 'Print dialog opens with a clean single-page preflight layout.'),
]:
    url = 'http://192.168.50.1/preflight.html' if n == 18 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 4
story.append(test_header(4, 'Pre-Planned Event Templates (event_templates.html)'))
story.append(SP(4))
for n, action, expected in [
    (25, 'Navigate to Event Templates.', 'Six built-in templates visible: Emergency Shelter, SAR, Severe Weather, Mass Gathering, HazMat, Exercise.'),
    (26, 'Click on the <b>Exercise / Training Scenario</b> template card.', 'Configuration panel opens with incident name field and template details.'),
    (27, 'Enter incident name: <i>Beta Test Exercise Alpha</i>. Click <b>Activate Template</b>.', 'New incident created. Browser navigates to incident dashboard. Incident marked with \ud83e\uddea scenario badge.'),
    (28, 'Verify the ICS-202 objectives pre-filled from the template.', 'Training objectives appear in the incident objectives list.'),
    (29, 'Return to Event Templates. Click <b>Manage Templates</b> tab.', 'All six templates listed with Edit buttons.'),
    (30, 'Click <b>Edit</b> on Emergency Shelter Operations.', 'Edit modal opens with four tabs: Objectives, Resources, Channels, Organization.'),
    (31, 'Add a new objective: <i>Establish shelter registration within 30 minutes</i>. Save.', 'Objective appears in the list. Save succeeds.'),
    (32, 'Click <b>Export JSON</b> on any template.', 'JSON file downloads to your device.'),
    (33, 'Click <b>Import JSON</b> and import the file you just exported.', 'Template imports successfully. Appears in list.'),
]:
    url = 'http://192.168.50.1/event_templates.html' if n in (25, 29) else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 5
story.append(test_header(5, 'Manual Incident Creation (incident.html)'))
story.append(SP(4))
for n, action, expected in [
    (34, 'Navigate to Incident Management.', 'Any existing incidents are listed.'),
    (35, 'Click <b>+ New Incident</b>.', 'New incident form opens.'),
    (36, 'Enter: Name = <i>Scenario 1 Test Incident</i>, Type = <i>All-Hazards</i>, IC = <i>Beta Tester One</i>', 'Fields accept input.'),
    (37, 'Click <b>Create Incident</b>.', 'Incident opens immediately. Incident name appears in dashboard header.'),
    (38, 'Open a new operational period. Click <b>+ New Period</b>.', 'Period 2 created. Period selector updates.'),
    (39, 'Switch back to Period 1. Verify Period 1 data still shows.', 'Data is period-specific and switching periods changes the displayed data.'),
    (40, 'Create a second incident with type <i>Search and Rescue</i>.', 'Second incident created and listed alongside the first.'),
    (41, 'Set the first incident as Active by clicking it and selecting <b>Set Active</b>.', 'Active incident badge updates in dashboard header.'),
]:
    url = 'http://192.168.50.1/incident.html' if n == 34 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 6
story.append(test_header(6, 'Incident Archive, Restore & Hard Delete (incident_mgmt.html)'))
story.append(SP(3))
story.append(prereq(
    'A USB drive labelled FIELDCOMMAND must be connected to the Pi for archive/restore tests. '
    'If no USB is available, skip Steps 42\u201346 and note as skipped.'))
story.append(SP(4))
for n, action, expected in [
    (42, 'Navigate to Incident Management.', 'All created incidents are listed.'),
    (43, 'Select the SAR incident. Click <b>Archive to USB</b>.', 'Success message confirms archive written to /media/fieldcommand/backup/incidents/ on USB.'),
    (44, 'Verify the USB drive \u2014 confirm the JSON archive file exists at /media/fieldcommand/backup/incidents/ on the Pi.', 'JSON file present with incident name in filename.'),
    (45, 'Click <b>Hard Delete from Pi</b> on the archived SAR incident. Confirm the deletion prompt.', 'Incident removed from the Pi database. No longer listed.'),
    (46, 'Click <b>Restore from USB</b>. Select the JSON file you archived.', 'Incident restored to fully active status. All data intact.'),
    (47, 'Navigate to Incident Management. Click <b>Beta/Scenario Reset</b>.', 'Confirmation prompt appears warning this will wipe all incident data.'),
    (48, 'Confirm the Beta Reset.', 'All incidents, forms, costs, check-ins, and T-cards wiped. Roster, hospitals, channels, and repeaters preserved.'),
    (49, 'Navigate to roster.html to verify roster is intact after reset.', 'Roster still shows any members previously entered.'),
]:
    url = ('http://192.168.50.1/incident_mgmt.html' if n in (42, 47) else
           'http://192.168.50.1/roster.html' if n == 49 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 7
story.append(test_header(7, 'WAN Source Configuration (wan_settings.html)'))
story.append(SP(3))
story.append(P(
    'FieldCommand supports any WAN source your group chooses \u2014 cellular modem, satellite dish, '
    'site Ethernet, USB tether, or venue Wi-Fi. The WAN Settings page lets you configure which source '
    'is preferred, which is fallback, and how each is detected.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
for n, action, expected in [
    (50, 'Navigate to WAN Settings.', 'Current WAN sources listed with their roles (Preferred/Fallback).'),
    (51, 'Note the current Preferred source. Click <b>\u21c4 Swap Roles</b>.', 'Preferred and Fallback roles swap immediately.'),
    (52, 'Swap roles back.', 'Original configuration restored.'),
    (53, 'Change the detection method on one source to <i>ping</i>. Enter a gateway IP (use 8.8.8.8 for testing).', 'Detection method updates. Field for gateway IP appears.'),
    (54, 'Save the change. Wait 60 seconds.', 'WAN status on dashboard updates to reflect new detection.'),
    (55, 'Disable one source using the Enabled toggle.', 'Source shows as disabled. WAN monitor no longer checks it.'),
    (56, 'Re-enable the source.', 'Source re-enabled. WAN monitor resumes.'),
]:
    url = 'http://192.168.50.1/wan_settings.html' if n == 50 else None
    story.append(step(n, action, expected, url))
story.append(SP(10))

# Scenario 1 summary
story.append(P('<b>SCENARIO 1 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 Organization Setup',
    'Test 2 \u2014 Dashboard Navigation',
    'Test 3 \u2014 Preflight Checklist',
    'Test 4 \u2014 Event Templates',
    'Test 5 \u2014 Incident Creation',
    'Test 6 \u2014 Archive / Restore',
    'Test 7 \u2014 WAN Settings',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line(next_scenario=2)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 2 — Roster, Check-In, QR Scanning & Personnel Accountability
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(2,
    'Roster, Check-In, QR Scanning & Personnel Accountability',
    '60\u201390 min',
    'Roster \u00b7 QR codes \u00b7 Manual check-in \u00b7 Scan check-in \u00b7 PAR \u00b7 Checkout \u00b7 Cross-reference \u00b7 Dead Man\u2019s Switch',
    'roster.html \u00b7 checkin.html \u00b7 scan_checkin.html \u00b7 accountability.html \u00b7 deadmans.html \u00b7 position_checklists.html'
)

story.append(P(
    'This scenario stress-tests every aspect of personnel management: building and importing the '
    'member roster, generating QR check-in codes, checking personnel in and out using both the manual '
    'form and the QR/barcode scanner, conducting a Personnel Accountability Report (PAR), and testing '
    'the Dead Man\u2019s Switch. Minimum 5 test personnel required.',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'PREREQUISITE: An active incident must exist from Scenario 1 (or create a new one). '
    'You need at least 5 people available as test subjects \u2014 they can be co-located or you can '
    'simulate them by creating roster entries and checking them in yourself.'))
story.append(SP(8))

# TEST 1 — Roster
story.append(test_header(1, 'Member Roster (roster.html)'))
story.append(SP(4))
for n, action, expected in [
    (1, 'Navigate to the Member Roster.', 'Roster page loads. Empty if first run.'),
    (2, 'Click <b>+ Add Member</b>. Enter: Member ID = ESV-001, First Name = Alpha, Last Name = Tester, Callsign = KD9TEST, Role = Net Control.', 'Member saves successfully. Appears in roster list.'),
    (3, 'Add a second member WITHOUT a callsign (non-licensed): ID = ESV-002, Name = Bravo Tester, Role = Logistics.', 'Non-licensed member saves successfully without callsign.'),
    (4, 'Add a third member with both callsign AND radio ID: ID = ESV-003, Callsign = KD9BETA, Radio ID = 412.', 'Member with both identifiers saves correctly.'),
    (5, 'Click the <b>QR</b> button on ESV-001\u2019s card.', 'QR modal opens. QR code renders (online) or ID displayed (offline).'),
    (6, 'Click <b>\u25a0 Print</b> on the QR modal.', 'Print preview opens with QR code, member name, and check-in URL.'),
    (7, 'Click <b>\u25a0 Save PNG</b>.', 'PNG file downloads to your device.'),
    (8, 'Click <b>\u25a0 Import CSV</b>. Use CSV with columns member_id, callsign, first_name, last_name, role and 2 rows: ESV-004/KD9FOUR/Delta/Tester/Operator and ESV-005//Echo/Tester/Logistics.', 'Both members import successfully. Roster now shows 5 members.'),
    (9, 'Click <b>\u25a0 Export CSV</b>.', 'CSV file downloads containing all 5 roster members.'),
    (10, 'Search for \u201cTester\u201d using the roster search field.', 'All 5 members matching \u201cTester\u201d appear. Non-matches hidden.'),
    (11, 'Edit ESV-001. Check certifications: ICS-100, ICS-200, ICS-700.', 'Certification checkboxes save. Badges appear on roster card.'),
]:
    url = 'http://192.168.50.1/roster.html' if n == 1 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 2 — Manual check-in
story.append(test_header(2, 'Manual ICS-211 Check-In (checkin.html)'))
story.append(SP(4))
for n, action, expected in [
    (12, 'Navigate to Incident Check-In.', 'Check-in form loads with current incident and period.'),
    (13, 'Enter callsign <i>KD9TEST</i> in the Callsign/ID field.', 'Name auto-fills from roster: \u201cAlpha Tester\u201d.'),
    (14, 'Select ICS Position: Net Control. Click <b>Check In</b>.', 'ESV-001 appears in the active check-in list below the form.'),
    (15, 'Check in ESV-002 using radio ID 412.', 'Bravo Tester appears in check-in list.'),
    (16, 'Check in ESV-003 using member ID ESV-003.', 'ESV-003 appears in check-in list.'),
    (17, 'Check in a walk-in visitor NOT in the roster: Name = Victor Visitor, Agency = Red Cross, Position = Volunteer.', 'Visitor check-in succeeds without a roster match.'),
    (18, 'In the active check-in list, click <b>Check Out</b> on Victor Visitor.', 'Victor Visitor moves to Checked Out section. Timestamp recorded.'),
    (19, 'Refresh the page.', 'All check-in records persist. Checked-out entries remain in list.'),
]:
    url = 'http://192.168.50.1/checkin.html' if n == 12 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3 — QR scan
story.append(test_header(3, 'QR/Barcode Scan Check-In (scan_checkin.html)'))
story.append(SP(3))
story.append(prereq(
    'This test requires a device with a camera (smartphone or tablet). Use the QR code PNG saved in Test 1, '
    'or display it on another screen. If no camera device is available, skip Steps 20\u201324 and test the manual fallback only.'))
story.append(SP(4))
for n, action, expected in [
    (20, 'Navigate to Scan Check-In on a camera-equipped device.', 'Page loads with camera area and manual entry fallback field.'),
    (21, 'Click <b>\u25a0 Start Camera</b>.', 'Camera activates. Viewfinder shows. Scan frame appears.'),
    (22, 'Hold the QR code for ESV-004 in front of the camera.', 'Code detected automatically using BarcodeDetector API. Name \u201cDelta Tester\u201d auto-fills with green borders.'),
    (23, 'Click <b>\u2713 Check In</b>.', 'Full-screen success confirmation appears with name and time. Device vibrates briefly (if supported).'),
    (24, 'Click <b>Scan Next Person</b>. Test manual entry fallback: type ESV-005 in the manual entry field and press Enter.', '\u201cEcho Tester\u201d auto-fills from roster. Check-in completes.'),
    (25, 'Scan a code NOT in the roster (use any random barcode \u2014 cereal box, ID badge, etc.).', 'Not-found banner appears. Manual form shown with scanned code pre-filled. Name field blank for manual entry.'),
    (26, 'Verify session history panel shows the last 10 check-ins.', 'Recent check-ins listed at bottom of page.'),
]:
    url = 'http://192.168.50.1/scan_checkin.html' if n == 20 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 4 — PAR
story.append(test_header(4, 'Personnel Accountability Report / PAR (accountability.html)'))
story.append(SP(4))
for n, action, expected in [
    (27, 'Navigate to Personnel Accountability.', 'Page loads. Select the active incident.'),
    (28, 'Review the summary tiles at the top.', 'Total Personnel, Checked In, Checked Out counts match actual check-in data.'),
    (29, 'Click the <b>ICS-211 CHECK-IN LIST</b> tab.', 'All checked-in personnel displayed. Unconfirmed in default sort order.'),
    (30, 'Click <b>\u25a0 Conduct PAR</b>.', 'PAR timestamp recorded in header badge. Unconfirmed personnel sorted to top.'),
    (31, 'Click <b>\u2713 PAR</b> on ESV-001.', 'ESV-001 moves to PAR confirmed state. Green border appears. Count updates.'),
    (32, 'Click <b>\u25a0 Location</b> on ESV-002. Enter: Division Alpha, east staging.', 'Location saved. Shows under ESV-002\u2019s entry.'),
    (33, 'Click <b>\u25a0 UNACCOUNTED</b> tab.', 'Personnel not yet PAR-confirmed are listed with red background.'),
    (34, 'Click <b>T-CARD PERSONNEL</b> tab.', 'Grouped by resource. Each resource shows PAR count (e.g. 0/3 PAR).'),
    (35, 'Click <b>CROSS-REFERENCE</b> tab.', 'Shows personnel checked in but not on T-cards, and T-card personnel without ICS-211 check-in.'),
    (36, 'Click <b>\u25a0 Reset PAR</b> and confirm.', 'All PAR confirmations cleared. PAR badge resets.'),
    (37, 'Click <b>\u25a0 Print</b>.', 'Print dialog opens. Print buttons and controls hidden in print view.'),
    (38, 'Enable <b>Auto 60s</b> checkbox. Wait 60 seconds.', 'Data refreshes automatically without manual reload.'),
]:
    url = 'http://192.168.50.1/accountability.html' if n == 27 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 5 — Dead Man's Switch
story.append(test_header(5, 'Dead Man\u2019s Switch (deadmans.html)'))
story.append(SP(4))
for n, action, expected in [
    (39, 'Navigate to the Dead Man\u2019s Switch page.', 'Page loads with net selector and interval configuration.'),
    (40, 'Set check-in interval to 1 minute for testing.', 'Interval field accepts numeric input.'),
    (41, 'Click <b>Start Monitoring</b>.', 'Countdown timer begins. Shows time remaining before alert.'),
    (42, 'Wait 60 seconds without logging a check-in.', 'Audible alert fires. Page flashes red. Alert message displayed.'),
    (43, 'Go to Net Control Logger and log a check-in. Return to Dead Man\u2019s Switch.', 'Timer resets automatically after check-in is logged.'),
    (44, 'Click <b>Stop Monitoring</b>.', 'Timer stops. Page returns to idle state.'),
]:
    url = 'http://192.168.50.1/deadmans.html' if n == 39 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 6 — Position Checklists
story.append(test_header(6, 'ICS Position Checklists (position_checklists.html)'))
story.append(SP(4))
for n, action, expected in [
    (45, 'Navigate to ICS Position Checklists.', 'Checklist page loads with position selector.'),
    (46, 'Select <b>Incident Commander (IC)</b> position.', 'IC activation checklist displays.'),
    (47, 'Check off the first 5 items on the IC checklist.', 'Items check and remain checked.'),
    (48, 'Select a different position (e.g. Safety Officer).', 'SOFR checklist loads. IC checklist state saved separately.'),
    (49, 'Click <b>Print</b>.', 'Print-ready checklist layout opens.'),
]:
    url = 'http://192.168.50.1/position_checklists.html' if n == 45 else None
    story.append(step(n, action, expected, url))
story.append(SP(10))

story.append(P('<b>SCENARIO 2 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 Member Roster',
    'Test 2 \u2014 Manual ICS-211 Check-In',
    'Test 3 \u2014 QR/Barcode Scan Check-In',
    'Test 4 \u2014 Personnel Accountability',
    'Test 5 \u2014 Dead Man\u2019s Switch',
    'Test 6 \u2014 Position Checklists',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line(next_scenario=3)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 3 — Full ICS Platform, T-Cards, IAP & Digital Signatures
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(3,
    'Full ICS Platform \u2014 Five Sections, T-Cards & IAP',
    '90\u2013120 min',
    'Five ICS sections \u00b7 T-cards \u00b7 GPS resource map \u00b7 All ICS forms \u00b7 Digital signatures \u00b7 Planning P \u00b7 IAP export \u00b7 Print center \u00b7 Meetings',
    'ics/* \u00b7 resources.html \u00b7 resource_map.html \u00b7 ics-form.html \u00b7 iap.html \u00b7 iap_compile.html \u00b7 ics213.html \u00b7 ics214.html \u00b7 meetings.html \u00b7 printcenter.html'
)

story.append(P(
    'This scenario exercises the complete ICS/NIMS incident management workflow from initial briefing '
    'through IAP compilation. Every ICS section is visited, every standard form is completed, the T-card '
    'resource board is fully populated, GPS positions are set on resources, digital signatures are captured, '
    'and the IAP is exported in all three formats: Print, PDF (server-generated), and HTML (fallback).',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'PREREQUISITE: An active incident and at least 3 roster members must exist. '
    'Use the incident and roster created in Scenarios 1 and 2.'))
story.append(SP(8))

# TEST 1
story.append(test_header(1, 'ICS Overview & Five-Section Navigation (ics/)'))
story.append(SP(4))
for n, action, expected in [
    (1, 'Navigate to the ICS Overview.', 'Five-section navigation bar visible: Overview, Command, Operations, Planning, Logistics, Finance.'),
    (2, 'Click each section in the nav bar: Command, Operations, Planning, Logistics, Finance.', 'Each section loads correctly. Nav highlights the active section.'),
    (3, 'Navigate to ICS Command. Review the Command Structure section (5.2).', 'IC info, incident name, period, objectives visible. Note: select Single IC or Unified Command as appropriate.'),
    (4, 'Navigate to Planning P.', 'Planning cycle wheel or timeline displays with all 15 phases.'),
]:
    url = ('http://192.168.50.1/ics/index.html' if n == 1 else
           'http://192.168.50.1/ics/command.html' if n == 3 else
           'http://192.168.50.1/ics/planningp.html' if n == 4 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 2
story.append(test_header(2, 'General Info / ICS-201 Initial Briefing (general_info.html)'))
story.append(SP(4))
for n, action, expected in [
    (5, 'Navigate to General Info.', 'ICS-201 form loads with current incident fields.'),
    (6, 'Enter Situation Summary: <i>Beta test exercise \u2014 simulated severe weather response. Three shelters activated. No actual emergency.</i>', 'Text field accepts multi-line input.'),
    (7, 'Enter Initial Actions: <i>Shelter teams deployed. Resource check-in underway.</i>', 'Field accepts input.'),
    (8, 'Fill in Incident Commander: <i>Beta Tester One</i> and Safety Officer: <i>Beta Tester Two</i>.', 'Fields accept text.'),
    (9, 'Save the form.', 'Success confirmation. Data persists on refresh.'),
]:
    url = 'http://192.168.50.1/general_info.html' if n == 5 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3
story.append(test_header(3, 'T-Card Resource Board (resources.html)'))
story.append(SP(4))
for n, action, expected in [
    (10, 'Navigate to the T-Card Resource Board.', 'Board loads. Empty or shows existing resources.'),
    (11, 'Click <b>+ Add Resource</b>. Create: Name = Engine 12, Type = Engine, Status = Staging, Assignment = Division Alpha, Leader = KD9TEST, Personnel = 4.', 'T-card appears on the board in correct status column.'),
    (12, 'Add a second resource: Name = Medical Team 1, Type = Medical Unit, Status = Available, Personnel = 2.', 'Second T-card appears.'),
    (13, 'Add a third resource: Name = Rescue 3, Type = Crew, Status = Assigned, Assignment = Division Bravo.', 'Third T-card appears.'),
    (14, 'Click Engine 12\u2019s T-card to open the detail panel.', 'Detail panel opens with INFO and PERSONNEL tabs.'),
    (15, 'Click the <b>PERSONNEL</b> tab.', 'Personnel tab shows empty list and Add Personnel form.'),
    (16, 'Type <i>Alpha</i> in the Name field.', 'Roster autocomplete suggests \u201cAlpha Tester\u201d.'),
    (17, 'Click the \u201cAlpha Tester\u201d suggestion chip.', 'Name, callsign, and agency auto-fill from roster.'),
    (18, 'Select ICS position: <i>Crew Boss</i>. Click <b>\u2713 Add to Resource</b>.', 'Alpha Tester added to Engine 12 personnel list. Count badge on T-card updates.'),
    (19, 'Add 2 more personnel to Engine 12.', 'Personnel count badge shows 3.'),
    (20, 'Remove one person using the \u2715 button.', 'Person removed. Count decrements.'),
    (21, 'Change Engine 12 status to <i>Assigned</i>.', 'T-card moves to Assigned column on board.'),
    (22, 'Navigate to ICS Operations section.', 'T-card board visible within ICS Operations context.'),
]:
    url = ('http://192.168.50.1/resources.html' if n == 10 else
           'http://192.168.50.1/ics/operations.html' if n == 22 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 4
story.append(test_header(4, 'GPS-Tracked Resource Map (resource_map.html)'))
story.append(SP(4))
for n, action, expected in [
    (23, 'Navigate to Resource Map.', 'Map loads (dark CartoDB tiles). Select the active incident. Repeater overlay (\ud83d\udce1) available in layer toggle.'),
    (24, 'Verify all three T-cards appear in the sidebar.', 'Resources with GPS show green left border. Without GPS show dim border.'),
    (25, 'Click Engine 12 in the sidebar to open the Set Position modal.', 'Modal opens with three placement methods.'),
    (26, 'Click <b>\u25a0 Use Device GPS</b>.', 'Browser requests location permission. If granted, coordinates fill automatically with accuracy estimate.'),
    (27, 'Enter manual coordinates: Lat = 42.3089, Lon = -88.4356. Add location label: <i>Division Alpha staging, north parking lot</i>.', 'Coordinate fields accept decimal input.'),
    (28, 'Click <b>Save Position</b>.', 'Engine 12 pin appears on map. Sidebar entry shows green border and coordinates.'),
    (29, 'Click <b>\u25a0 Click Map to Place</b> for Medical Team 1.', 'Modal closes. Cursor changes to crosshair.'),
    (30, 'Click anywhere on the map.', 'Coordinates fill automatically. Modal reopens with the clicked location.'),
    (31, 'Save the position.', 'Medical Team 1 pin appears on map.'),
    (32, 'Click a resource pin on the map.', 'Popup shows: resource name, status, assignment, coordinates, GPS source, timestamp, and Update Position button.'),
    (33, 'Click <b>\u25a0 My Location</b>.', 'Your device location marked on map with amber circle.'),
    (34, 'Enable <b>Auto-refresh 30s</b>.', 'Map refreshes automatically every 30 seconds.'),
    (35, 'Click <b>Clear GPS</b> on one resource.', 'Pin removed from map. Sidebar reverts to dim border.'),
]:
    url = 'http://192.168.50.1/resource_map.html' if n == 23 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 5 — ICS forms table
story.append(test_header(5, 'ICS Form Set with Digital Signatures (ics-form.html)'))
story.append(SP(3))
story.append(P(
    'Complete one entry on each ICS form below. On every form with a Prepared By or Approved By field, '
    'capture a digital signature. Save each form and verify data persists.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))

form_data = [[
    P('FORM', S('fh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=10)),
    P('KEY FIELDS TO TEST', S('fh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=10)),
    P('SIG?', S('fh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=10, alignment=TA_CENTER)),
    P('RESULT', S('fh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=10, alignment=TA_CENTER)),
]]
forms = [
    ('ICS-202 Incident Objectives', 'Enter 3 objectives, tactical priorities, weather', True),
    ('ICS-203 Org Assignment List', 'Enter IC, OSC, PSC, LSC, FSC names; fill 3 divisions', True),
    ('ICS-204 Assignment List', 'Add branch, division, assignment, resources needed', True),
    ('ICS-205 Radio Comms Plan', 'Add 3 channels from channel library; fill function/frequency', True),
    ('ICS-205A Comms List', 'Add 3 contact entries', False),
    ('ICS-206 Medical Plan', 'Add 2 medical facilities; fill trauma level', True),
    ('ICS-207 Org Chart', 'Verify org chart renders from org assignment data', False),
    ('ICS-208 Safety Message', 'Enter safety message text; fill hazards', True),
    ('ICS-209 Status Summary', 'Fill incident status; enter resource summary counts', True),
    ('ICS-211 Check-In List', 'Verify check-in entries sync from checkin.html', False),
    ('ICS-213 General Message', 'See Test 6 below', True),
    ('ICS-214 Activity Log', 'See Test 7 below', True),
    ('ICS-215A Safety Analysis', 'Enter 3 hazards; fill mitigation measures', True),
    ('ICS-218 Support Vehicle', 'Add 2 vehicles with mileage/hours', False),
    ('ICS-221 Demob Check-Out', 'Enter demob instructions; add 1 resource', True),
]
for form, fields, sig in forms:
    form_data.append([
        P(form, S('fc', fontSize=8, leading=11, fontName='Helvetica-Bold')),
        P(fields, S('fc', fontSize=7.5, leading=10)),
        P('\u2713 Prepared By' if sig else '', S('fc', fontSize=7.5, leading=10, alignment=TA_CENTER,
                                                   textColor=GREEN if sig else black)),
        P('\u25a0 Pass  \u25a0 Fail', S('fc', fontSize=7.5, leading=10, alignment=TA_CENTER)),
    ])
form_t = Table(form_data, colWidths=[1.5*inch, 2.6*inch, 1.0*inch, CW-5.1*inch], repeatRows=1)
form_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(form_t)
story.append(SP(6))

# Signature procedure
story.append(P('<b>Digital Signature Test Procedure</b> \u2014 apply to every form with SIG REQUIRED:',
               S('sp', fontSize=8.5, textColor=EOC, fontName='Helvetica-Bold')))
story.append(SP(3))
for n, action, expected in [
    (36, 'On any ICS form, locate the <b>Prepared By</b> field.', 'Signature pad canvas appears below the field.'),
    (37, 'Sign using mouse (desktop), finger (touchscreen), or stylus.', 'Signature appears as drawn stroke in the pad.'),
    (38, 'Click <b>Accept</b>.', 'Signature preview appears below the field as a PNG image.'),
    (39, 'Save the form. Reload the page.', 'Signature image persists after reload \u2014 restored from database.'),
    (40, 'Click <b>Clear</b> on the signature pad.', 'Signature removed. Pad is blank.'),
    (41, 'Re-sign and accept.', 'New signature replaces the cleared one.'),
]:
    story.append(step(n, action, expected))
story.append(SP(8))

# TEST 6 — ICS-213
story.append(test_header(6, 'ICS-213 General Message (ics213.html)'))
story.append(SP(4))
for n, action, expected in [
    (42, 'Navigate to ICS-213 General Message.', 'Blank message form loads.'),
    (43, 'Fill in: To = Logistics Section Chief, From callsign = KD9TEST (name auto-fills), Subject = Supply Request \u2014 Cots, Message = Request 50 cots for Shelter Alpha by 1800.', 'Callsign auto-fills name from FCC/roster. All fields accept input.'),
    (44, 'Check <b>Reply Requested</b>.', 'Reply checkbox toggles.'),
    (45, 'Sign <b>Prepared By</b> field.', 'Signature captured.'),
    (46, 'Click <b>Print</b>.', 'Print-ready ICS-213 form opens in new tab with all fields filled.'),
    (47, 'Save the message. Verify it appears in the message history.', 'Message saved and listed.'),
]:
    url = 'http://192.168.50.1/ics213.html' if n == 42 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 7 — ICS-214
story.append(test_header(7, 'ICS-214 Activity Log (ics214.html)'))
story.append(SP(4))
for n, action, expected in [
    (48, 'Navigate to ICS-214 Activity Log.', 'Activity log form loads.'),
    (49, 'Select resource: <i>Engine 12</i>.', 'Resource populates from T-card data.'),
    (50, 'Click <b>+ Add Entry</b>. Enter time 0900, Activity = <i>Engine 12 arrived at staging area, crew briefed.</i>', 'Entry added to log.'),
    (51, 'Add second entry: time 1000, Activity = <i>Deployed to Division Alpha. Crew began structure assessment.</i>', 'Second entry added.'),
    (52, 'Click <b>Export to FEMA Labor</b>.', 'Hours from this log push to FEMA Force Account Labor for the active incident.'),
    (53, 'Sign <b>Prepared By</b> field.', 'Signature captured.'),
    (54, 'Print the ICS-214.', 'Print-ready log with both entries and signature.'),
]:
    url = 'http://192.168.50.1/ics214.html' if n == 48 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 8 — IAP
story.append(test_header(8, 'IAP Assembly & Export (iap.html, iap_compile.html)'))
story.append(SP(3))
story.append(P(
    'FieldCommand provides three IAP output options from iap.html, plus a full PDF compiler '
    'at iap_compile.html. Test all three output methods.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
for n, action, expected in [
    (55, 'Navigate to IAP Assembly.', 'IAP summary shows all completed forms for the active incident with completion status indicators.'),
    (56, 'Select operational period and check forms: ICS-202, ICS-203, ICS-204, ICS-205, ICS-206, ICS-208. Click <b>\ud83d\uddc8 Print IAP</b>.', 'Print-ready IAP opens in new browser tab. Browser print dialog opens automatically.'),
    (57, 'Return to iap.html. Click <b>\ud83d\udcc4 Save as PDF</b>.', 'Server generates a proper 8.5\u00d711 PDF (via ReportLab). Downloads as IAP_[Incident]_Period[N]_[Date].pdf. Opens correctly in any PDF viewer.'),
    (58, 'Return to iap.html. Click <b>\ud83d\udcbe Save as HTML</b>.', 'Browser generates HTML file directly (no server call). File downloads. Open in any browser and use File \u2192 Print to print.'),
    (59, 'Navigate to IAP Compile. Select forms: ICS-202, 203, 204, 205, 206, 208. Click <b>\u25a0 Compile IAP PDF</b>.', 'Server generates full PDF (5\u201315 seconds). Progress indicator shown. PDF contains: title page with incident name and period, section dividers, all six forms in order, embedded signatures.'),
    (60, 'Verify the compiled PDF downloads and opens correctly.', 'PDF displays all selected forms in FEMA standard order. Signatures embedded in Prepared By fields.'),
]:
    url = ('http://192.168.50.1/iap.html' if n in (55, 56, 57, 58) else
           'http://192.168.50.1/iap_compile.html' if n == 59 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 9
story.append(test_header(9, 'Meeting Scheduler & Print Center'))
story.append(SP(4))
for n, action, expected in [
    (61, 'Navigate to Meeting Scheduler.', 'Meeting calendar/list loads.'),
    (62, 'Create a meeting: Name = Operational Period Briefing, Time = 1800, Location = ICP Main Room.', 'Meeting saves and appears in list.'),
    (63, 'Navigate to Print Center.', 'Document list shows all printable items.'),
    (64, 'Select the IAP PDF and click <b>Print</b>.', 'Print job routes to configured printer via CUPS, or browser print dialog opens.'),
]:
    url = ('http://192.168.50.1/meetings.html' if n == 61 else
           'http://192.168.50.1/printcenter.html' if n == 63 else None)
    story.append(step(n, action, expected, url))
story.append(SP(10))

story.append(P('<b>SCENARIO 3 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 ICS Five-Section Navigation',
    'Test 2 \u2014 General Info / ICS-201',
    'Test 3 \u2014 T-Card Resource Board',
    'Test 4 \u2014 GPS Resource Map',
    'Test 5 \u2014 All ICS Forms & Signatures',
    'Test 6 \u2014 ICS-213 General Message',
    'Test 7 \u2014 ICS-214 Activity Log',
    'Test 8 \u2014 IAP Export (Print / PDF / HTML / Compile)',
    'Test 9 \u2014 Meetings & Print Center',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line(next_scenario=4)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 4 — Amateur Radio EMCOMM
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(4,
    'Amateur Radio EMCOMM \u2014 Net Loggers, FCC Database & AMPRNet',
    '60\u201390 min',
    'Amateur net logger \u00b7 Public safety net logger \u00b7 FCC lookup \u00b7 APRS map \u00b7 Observer mode \u00b7 NTS radiogram \u00b7 Winlink import \u00b7 AMPRNet \u00b7 HF propagation \u00b7 Repeaters \u00b7 Channel library \u00b7 ICS-309 \u00b7 PACTOR modem',
    'netcontrol.html \u00b7 starcom.html \u00b7 callsign.html \u00b7 tactical.html \u00b7 observer.html \u00b7 nts.html \u00b7 winlink-import.html \u00b7 amprgate.html \u00b7 propagation.html \u00b7 repeaters.html \u00b7 channel_library.html \u00b7 ics309.html'
)

story.append(P(
    'This scenario tests all amateur radio emergency communications features: opening and operating both '
    'net loggers, FCC callsign validation against the offline database, the tactical APRS map, NTS '
    'radiogram generation, Winlink form import, the AMPRNet gateway, HF propagation tool, repeater '
    'database, channel library, and ICS-309 export. An FCC amateur license is required for some test steps.',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'FCC CALLSIGN REQUIRED for callsign lookup tests. Use your own FCC callsign or any valid active '
    'callsign from the FCC ULS database. The offline database contains 800,000+ licensees.'))
story.append(SP(8))

# TEST 1
story.append(test_header(1, 'Amateur Radio Net Control Logger (netcontrol.html)'))
story.append(SP(4))
for n, action, expected in [
    (1, 'Navigate to Net Control Logger.', 'Net logger loads. Fields: Net Name, Frequency, Mode.'),
    (2, 'Enter: Net Name = <i>Beta Test EMCOMM Net</i>, Frequency = 146.520, Mode = FM.', 'Fields accept input.'),
    (3, 'Click <b>Open Net</b>.', 'Net opens with timestamp. Timer starts. Green status banner shows elapsed time.'),
    (4, 'Type your FCC callsign in the Check-In field.', 'Name auto-fills from offline FCC database. License class shown.'),
    (5, 'Press Enter or click <b>Check In</b>.', 'Your callsign entry appears in the log with timestamp.'),
    (6, 'Type a second callsign (valid FCC callsign from any licensed amateur).', 'Name fills automatically.'),
    (7, 'Check in 3 more callsigns. Mix valid and one intentionally invalid callsign.', 'Valid callsigns fill name. Invalid callsign shows red border or \u201cNot Found\u201d.'),
    (8, 'For one check-in, enter remarks: <i>QRM on .520 \u2014 switching to .540</i>.', 'Remarks field accepts text.'),
    (9, 'Click <b>Check Out</b> on one station.', 'Checkout time recorded. Duration shown rounded to nearest quarter hour.'),
    (10, 'Click <b>\u25a0 Observer Link</b>.', 'URL copied to clipboard or displayed.'),
    (11, 'Open the observer URL in a second browser tab or different device.', 'Observer view shows live net status. Updates every 15 seconds. No edit controls visible.'),
    (12, 'Log a traffic entry: Precedence = ROUTINE, From = your callsign, To = BTES EOC, Info = <i>Check-in net closed, 5 stations logged.</i>', 'Traffic entry appears in the traffic log.'),
    (13, 'Click <b>Close Net</b>.', 'All remaining stations automatically checked out. Net close time recorded. Duration displayed in header.'),
    (14, 'Click <b>\u25a0 Export ICS-309</b>.', 'ICS-309 document downloads. Contains: net name, frequency, mode, open/close times, duration, all check-ins with individual durations (rounded to \u00bc hour).'),
]:
    url = 'http://192.168.50.1/netcontrol.html' if n == 1 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 2
story.append(test_header(2, 'Public Safety Net Logger (starcom.html)'))
story.append(SP(4))
for n, action, expected in [
    (15, 'Navigate to Public Safety Net Logger.', 'Net logger loads. Configured for radio ID check-in.'),
    (16, 'Open a net: Name = <i>Beta Test Starcom Net</i>.', 'Net opens with timestamp.'),
    (17, 'Check in using radio ID 412 (from ESV-003 in roster).', 'Name auto-fills from roster by radio ID match.'),
    (18, 'Check in radio ID 999 (not in roster).', 'Check-in succeeds without roster match. Name field blank for manual entry. Enter name manually.'),
    (19, 'Check in a callsign KD9TEST.', 'Check-in succeeds. Callsign appears in the log.'),
    (20, 'Close the net and export ICS-309.', 'ICS-309 downloaded. Radio IDs appear in station column.'),
]:
    url = 'http://192.168.50.1/starcom.html' if n == 15 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3
story.append(test_header(3, 'FCC Callsign Lookup (callsign.html)'))
story.append(SP(4))
for n, action, expected in [
    (21, 'Navigate to Callsign Lookup.', 'Search field loads.'),
    (22, 'Search for your own callsign.', 'Returns: callsign, full name, license class, expiration date, grid square, city/state. Instant result \u2014 no internet.'),
    (23, 'Search for a callsign that does not exist: <i>ZZ9ZZZ</i>.', '\u201cNot found\u201d result displayed.'),
    (24, 'Search for a partial callsign (type 3 letters).', 'Auto-complete or results filter as you type.'),
    (25, 'Click <b>Add to Roster</b> on a search result.', 'Roster entry created from FCC data.'),
]:
    url = 'http://192.168.50.1/callsign.html' if n == 21 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 4
story.append(test_header(4, 'Tactical APRS Map (tactical.html)'))
story.append(SP(4))
for n, action, expected in [
    (26, 'Navigate to the Tactical Map.', 'Leaflet map loads with dark tile layer. Controls visible. Repeater overlay (\ud83d\udce1) available in layer toggle.'),
    (27, 'Verify map tiles load (either online or from local cache).', 'Map displays geographic features.'),
    (28, 'Enable the Repeater overlay (\ud83d\udce1). Verify repeater pins appear on map.', 'Repeater markers visible showing callsign, frequency, and tone on click.'),
    (29, 'If APRS-IS is active (WAN up), verify live stations appear as icons.', 'APRS station symbols visible on map. Click a station for popup.'),
    (30, 'If RF APRS TNC is connected, verify RF stations appear.', 'RF stations visible independent of WAN state.'),
    (31, 'Click a station marker to open the popup.', 'Popup shows: callsign, last beacon time, speed, course, altitude, comment.'),
    (32, 'Navigate to SARTopo Import. Test GeoJSON import with a minimal valid file.', 'File imports without error. Returns to tactical map.'),
]:
    url = ('http://192.168.50.1/tactical.html' if n == 26 else
           'http://192.168.50.1/sartopo_import.html' if n == 32 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 5
story.append(test_header(5, 'NTS Radiogram Generator (nts.html)'))
story.append(SP(4))
for n, action, expected in [
    (33, 'Navigate to NTS Radiogram.', 'Radiogram form loads with all standard NTS fields.'),
    (34, 'Fill in: Precedence = ROUTINE, Station of origin = your callsign, Place = Testville IL, To = John Smith, Phone = 555-0100.', 'Fields accept input.'),
    (35, 'Enter text: <i>ALL WELL STOP ARRIVED SAFELY STOP</i>', 'Word count (check) calculates automatically.'),
    (36, 'Click <b>Generate Radiogram</b>.', 'Formatted NTS radiogram displays with correct prosign format.'),
    (37, 'Click <b>Print</b>.', 'Print-ready traffic form opens.'),
]:
    url = 'http://192.168.50.1/nts.html' if n == 33 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 6
story.append(test_header(6, 'Winlink Form Import (winlink-import.html)'))
story.append(SP(4))
for n, action, expected in [
    (38, 'Navigate to Winlink Form Import.', 'Import page loads with file chooser and paste area.'),
    (39, 'Attempt to import a test file. If no Winlink XML is available, attempt with a plain text file to confirm graceful error handling.', 'Either: import succeeds and ICS form created; OR clear error message if format is invalid. No crash or blank screen.'),
]:
    url = 'http://192.168.50.1/winlink-import.html' if n == 38 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 7
story.append(test_header(7, 'AMPRNet (44Net) Gateway (amprgate.html)'))
story.append(SP(3))
story.append(prereq(
    'The AMPRNet gateway requires the 44Net Gateway Pi to be running at 192.168.50.2 and an AMPRNet '
    'allocation assigned to your callsign. If gateway Pi is not deployed, skip Steps 40\u201343 and note as \u201cGateway not deployed.\u201d'))
story.append(SP(4))
for n, action, expected in [
    (40, 'Navigate to AMPRNet Gateway Status.', 'Page loads. Shows tunnel status. Dashboard AMPRNet card shows \ud83d\udfe2 Green (tunnel UP) or \ud83d\udd34 Red (tunnel DOWN).'),
    (41, 'Verify public read-only port 9000 is accessible at http://192.168.50.2:9000.', 'Callsign login page loads. Enter valid FCC callsign to access status dashboard.'),
    (42, 'Verify the access log shows entries for recent connections.', 'Log shows callsign, IP, timestamp, and result for each access attempt.'),
    (43, 'Attempt to access tunnel control functions from a network device.', 'Control functions require localhost access \u2014 port 9001 unavailable from browser. Connection refused.'),
]:
    url = 'http://192.168.50.1/amprgate.html' if n == 40 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 8
story.append(test_header(8, 'HF Propagation, Repeaters & Channel Library'))
story.append(SP(4))
for n, action, expected in [
    (44, 'Navigate to HF Propagation.', 'Tool loads. If WAN available, current SFI/A/K-index shown with band conditions (10m\u201380m).'),
    (45, 'If offline, verify last cached data displays.', 'Stale data shown with fetch timestamp. No crash.'),
    (46, 'Navigate to Repeater Database. Import a RepeaterBook CSV (Offline File tab \u2192 download from repeaterbook.com free account \u2192 drag onto drop zone). Verify map view shows repeater pins (\ud83d\udce1 Map View button).', 'Repeaters load and display. Map view shows pins at correct geographic locations. Click a pin for details.'),
    (47, 'Add a manual test repeater: Callsign = W8RPT, Output = 146.940, Offset = -0.6, CTCSS = 127.3, Mode = FM. Edit it to change CTCSS to 100.0. Delete it.', 'Add, edit, and delete all work correctly.'),
    (48, 'Navigate to Channel Library.', 'Pre-loaded interoperability channels visible.'),
    (49, 'Add a custom channel: Name = EOC Primary, Frequency = 155.3400, Mode = FM, Function = Command.', 'Channel saves. Appears in library.'),
    (50, 'Open an ICS-205 form. Verify the channel library picker shows your new channel.', 'Custom channel selectable in ICS-205 channel entry.'),
]:
    url = ('http://192.168.50.1/propagation.html' if n == 44 else
           'http://192.168.50.1/repeaters.html' if n == 46 else
           'http://192.168.50.1/channel_library.html' if n == 48 else None)
    story.append(step(n, action, expected, url))
story.append(SP(10))

story.append(P('<b>SCENARIO 4 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 Amateur Net Control Logger',
    'Test 2 \u2014 Public Safety Net Logger',
    'Test 3 \u2014 FCC Callsign Lookup',
    'Test 4 \u2014 Tactical APRS Map',
    'Test 5 \u2014 NTS Radiogram',
    'Test 6 \u2014 Winlink Form Import',
    'Test 7 \u2014 AMPRNet Gateway',
    'Test 8 \u2014 HF Propagation, Repeaters & Channels',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line(next_scenario=5)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 5 — FEMA Cost Documentation, Radar & Situational Awareness
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(5,
    'FEMA Documentation, Cost Tracking & Situational Awareness',
    '60\u201390 min',
    'FEMA labor/equipment/materials \u00b7 Cost dashboard \u00b7 NEXRAD radar \u00b7 Hospitals \u00b7 Facilities \u00b7 NIMS resource types \u00b7 Grid calc \u00b7 Cheat sheets \u00b7 Reference library \u00b7 WAN status',
    'fema_costs.html \u00b7 fema_rates.html \u00b7 cost_dashboard.html \u00b7 radar.html \u00b7 hospitals.html \u00b7 facilities.html \u00b7 resource_types.html \u00b7 grid.html \u00b7 cheatsheets.html \u00b7 refs.html \u00b7 wan-status.html'
)

story.append(P(
    'This scenario tests FEMA Public Assistance (PA) cost documentation, the real-time cost dashboard, '
    'the animated NEXRAD radar, hospital and facilities directories, NIMS resource typing, the grid square '
    'calculator, radio cheat sheets, the offline reference library, and all WAN status tools. '
    'Several tests require internet connectivity.',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'NEXRAD radar test requires active internet (WAN) connection. '
    'Run offline tests first, then WAN-dependent tests when connected.'))
story.append(SP(8))

# TEST 1
story.append(test_header(1, 'FEMA Equipment Rate Schedule (fema_rates.html)'))
story.append(SP(4))
for n, action, expected in [
    (1, 'Navigate to FEMA Equipment Rates.', 'Table loads with 44 standard equipment categories and current-year rates.'),
    (2, 'Search for <i>Generator</i>.', 'Generator entries filter into view.'),
    (3, 'Click \u270f Edit on one entry. Change the rate by $1.00. Click Save.', 'Rate updates. Change visible in table.'),
    (4, 'Verify the Rate Year badge shows the current year.', 'Badge shows current year. No stale-data warning.'),
]:
    url = 'http://192.168.50.1/fema_rates.html' if n == 1 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 2
story.append(test_header(2, 'FEMA PA Cost Documentation \u2014 Labor (fema_costs.html)'))
story.append(SP(4))
for n, action, expected in [
    (5, 'Navigate to FEMA PA Cost Documentation.', 'Three tabs visible: Force Account Labor, Equipment, Materials/Contracts.'),
    (6, 'Click <b>+ Add Labor Entry</b>. Enter: Employee = Alpha Tester, Title = Emergency Management Coordinator, Regular Hours = 8, Overtime Hours = 4, Hourly Rate = 32.50, Fringe % = 28.', 'Fields accept numeric and text input.'),
    (7, 'Verify the Total with Fringe calculates automatically: (8+4) \u00d7 $32.50 \u00d7 1.28 = $499.20', 'Calculated total matches expected value.'),
    (8, 'Save the labor entry.', 'Entry saved. Appears in labor list.'),
    (9, 'Add a second labor entry with different fringe rate.', 'Both entries appear. Individual totals correct.'),
    (10, 'Click <b>Import from ICS-214</b>.', 'ICS-214 import dialog or picker opens.'),
]:
    url = 'http://192.168.50.1/fema_costs.html' if n == 5 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3
story.append(test_header(3, 'FEMA PA Cost Documentation \u2014 Equipment'))
story.append(SP(4))
for n, action, expected in [
    (11, 'Click the <b>Equipment</b> tab.', 'Equipment cost form loads.'),
    (12, 'Click <b>+ Add Equipment Entry</b>. Click <b>\u25a0 Lookup</b>.', 'FEMA rate picker opens. Searchable list of 44 equipment categories.'),
    (13, 'Search for <i>Generator</i>. Select a 15 kW generator entry.', 'FEMA rate fills automatically from the rate schedule.'),
    (14, 'Enter: Hours = 16, Equipment ID = GEN-001.', 'Total calculates: 16 \u00d7 (FEMA rate).'),
    (15, 'Save the equipment entry.', 'Entry saved. Total shown.'),
]:
    story.append(step(n, action, expected))
story.append(SP(8))

# TEST 4
story.append(test_header(4, 'FEMA PA Cost Documentation \u2014 Materials & Contracts'))
story.append(SP(4))
for n, action, expected in [
    (16, 'Click the <b>Materials</b> tab. Add: Vendor = Home Depot, Description = Sandbags 50lb, PO = PO-2026-001, Unit Cost = 4.50, Qty = 200.', 'Total calculates: 200 \u00d7 $4.50 = $900.00'),
    (17, 'Save materials entry.', 'Entry saved.'),
    (18, 'Click the <b>Contracts</b> tab. Add: Vendor = Cleanup Contractors LLC, Description = Debris removal 4 hours, Contract # = C-001, Amount = 2400.00.', 'Entry saved with contract number.'),
    (19, 'Click <b>\u25a0 Export PW Text</b>.', 'Project Worksheet text downloads. Contains itemized costs by category and total claimed amount.'),
]:
    story.append(step(n, action, expected))
story.append(SP(8))

# TEST 5
story.append(test_header(5, 'Real-Time Cost Dashboard (cost_dashboard.html)'))
story.append(SP(4))
for n, action, expected in [
    (20, 'Navigate to Cost Dashboard.', 'All cost panels load showing data from Tests 2\u20134.'),
    (21, 'Verify Total Incident Cost tile shows the sum of all entries.', 'Total = Labor total + Equipment total + Materials total + Contracts total.'),
    (22, 'Verify Cost by Category breakdown bars are proportional.', 'Labor, Equipment, Materials, Contracts bars visible with $ amounts and %.'),
    (23, 'Enter a budget amount in the Budget Tracker panel.', 'Remaining balance and percentage used calculate correctly.'),
    (24, 'Verify the Per-Period Breakdown shows costs attributed to the active period.', 'Period 1 costs listed.'),
    (25, 'Wait 2 minutes. Verify dashboard auto-refreshes.', 'Data refreshes without manual reload.'),
]:
    url = 'http://192.168.50.1/cost_dashboard.html' if n == 20 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 6 — Radar
story.append(test_header(6, 'Animated NEXRAD Radar (radar.html) \u2014 WAN REQUIRED'))
story.append(SP(3))
story.append(prereq(
    'This test requires active internet. If offline, verify the offline banner appears and test the fallback display only.'))
story.append(SP(4))
for n, action, expected in [
    (26, 'Navigate to NEXRAD Radar.', 'Page loads. If WAN up: radar tiles begin loading. If WAN down: offline banner shown.'),
    (27, 'Select your nearest NEXRAD station from the dropdown.', 'Radar station changes. New tiles load for selected station.'),
    (28, 'Click <b>\u25a0 Play</b>.', 'Radar animates as a loop.'),
    (29, 'Click <b>\u25a0 Pause</b>.', 'Animation stops on current frame.'),
    (30, 'Use the timeline scrubber to jump to an earlier frame.', 'Radar updates to that frame.'),
    (31, 'Change speed to 2\u00d7.', 'Animation plays faster.'),
    (32, 'Switch palette to Dual-pol.', 'Color scheme changes.'),
    (33, 'Click <b>\u25a0 Step backward</b> one frame.', 'Moves exactly one frame back.'),
    (34, 'Verify the reflectivity legend is visible.', 'Color scale with dBZ values shown.'),
    (35, 'Turn off WAN (unplug ethernet/disable hotspot). Reload the radar page.', 'Offline banner appears. Last loaded frame displayed with timestamp.'),
]:
    url = 'http://192.168.50.1/radar.html' if n == 26 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 7
story.append(test_header(7, 'Hospital Proximity & Facilities Directory'))
story.append(SP(4))
for n, action, expected in [
    (36, 'Navigate to Hospital Proximity.', 'Hospital directory loads.'),
    (37, 'Add a hospital: Name = Beta General Hospital, Address = 100 Main St Testville IL, Trauma Level = Level II, Helipad = Yes.', 'Hospital saves and appears in list.'),
    (38, 'Navigate to Facilities Directory.', 'Facilities list loads.'),
    (39, 'Add a facility: Name = Incident Command Post, Type = ICP, Address = 200 Park Ave Testville IL, Capacity = 50 personnel.', 'Facility saves. Appears in list.'),
    (40, 'Edit the facility. Add Notes: <i>Generator on site. Porta-johns deployed.</i>', 'Notes save correctly.'),
]:
    url = ('http://192.168.50.1/hospitals.html' if n == 36 else
           'http://192.168.50.1/facilities.html' if n == 38 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 8
story.append(test_header(8, 'NIMS Resource Typing Library (resource_types.html)'))
story.append(SP(4))
for n, action, expected in [
    (41, 'Navigate to NIMS Resource Types.', 'Pre-loaded NIMS types visible: Engine, Crew, Helicopter, etc.'),
    (42, 'Add a custom resource type: Name = Amateur Radio Go-Box, Category = Communications.', 'Custom type saves. Appears in list.'),
    (43, 'Navigate to T-Card board. Click <b>+ Add Resource</b>. Verify new type appears in the Type dropdown.', 'Custom type \u201cAmateur Radio Go-Box\u201d selectable.'),
    (44, 'Delete the custom resource type from the type library.', 'Type removed from library.'),
]:
    url = ('http://192.168.50.1/resource_types.html' if n in (41, 44) else
           'http://192.168.50.1/resources.html' if n == 43 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 9
story.append(test_header(9, 'Grid Calculator, Cheat Sheets, Reference Library & WAN Status'))
story.append(SP(4))
for n, action, expected in [
    (45, 'Navigate to Grid Square Calculator.', 'Calculator loads.'),
    (46, 'Enter grid square EN52ab. Click Convert.', 'Decimal coordinates returned: approx 42.31\u00b0N, 88.44\u00b0W.'),
    (47, 'Enter two grid squares and calculate distance/bearing.', 'Distance in km and miles plus true bearing returned.'),
    (48, 'Navigate to Radio/ICS Cheat Sheets.', 'Quick reference cards visible: phonetic alphabet, Q-codes, RST scale, ICS structure, NIMS resource types, HF calling frequencies.'),
    (49, 'Click Print on any cheat sheet card.', 'Print layout opens. Card fits on one page.'),
    (50, 'Navigate to Reference Library (Kiwix).', 'Kiwix interface loads. Offline content available.'),
    (51, 'Navigate to WAN Status detail page.', 'Detailed WAN status shows both configured sources, detection method, role, last check time, and current state.'),
    (52, 'Verify both WAN sources are listed with their roles.', 'Preferred and Fallback sources both displayed. Your group\u2019s chosen primary and secondary clearly identified.'),
]:
    url = ('http://192.168.50.1/grid.html' if n == 45 else
           'http://192.168.50.1/cheatsheets.html' if n == 48 else
           'http://192.168.50.1/refs.html' if n == 50 else
           'http://192.168.50.1/wan-status.html' if n == 51 else None)
    story.append(step(n, action, expected, url))
story.append(SP(10))

story.append(P('<b>SCENARIO 5 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 FEMA Equipment Rates',
    'Test 2 \u2014 FEMA Force Account Labor',
    'Test 3 \u2014 FEMA Equipment Cost',
    'Test 4 \u2014 FEMA Materials & Contracts',
    'Test 5 \u2014 Cost Dashboard',
    'Test 6 \u2014 NEXRAD Radar',
    'Test 7 \u2014 Hospitals & Facilities',
    'Test 8 \u2014 NIMS Resource Types',
    'Test 9 \u2014 Grid, Cheat Sheets, Refs, WAN',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line(next_scenario=6)


# ══════════════════════════════════════════════════════════════════════════════
# SCENARIO 6 — Full Multi-Operator Simulation, Stress Testing & Edge Cases
# ══════════════════════════════════════════════════════════════════════════════
story += scenario_cover(6,
    'Full Multi-Operator Simulation, Stress Testing & Edge Cases',
    '90\u2013120 min',
    'Multi-device access \u00b7 WAN failover under load \u00b7 Sustained 60-min simulation \u00b7 Edge cases \u00b7 Error handling \u00b7 Performance measurements \u00b7 Final cleanup',
    '3 devices minimum \u00b7 2 operators minimum \u00b7 All major tools'
)

story.append(P(
    'This is the final and most demanding scenario. It simulates a real multi-operator activation with '
    'several devices simultaneously accessing the system, exercises WAN failover under load, tests every '
    'edge case and error condition, and verifies system stability over a sustained 2-hour operational period. '
    'Minimum 2 operators and 3 devices required.',
    S('intro', fontSize=9, leading=13, alignment=TA_JUSTIFY)))
story.append(SP(6))
story.append(prereq(
    'PREREQUISITE: All previous scenarios must pass before running Scenario 6. '
    'This scenario assumes a fully configured system with roster, channels, repeaters, and at least one '
    'completed incident from prior scenarios.'))
story.append(SP(4))
story.append(prereq(
    'SETUP: Assign roles before starting. Suggested: Device 1 = Incident Commander / Net Control; '
    'Device 2 = Operations / T-Cards / Resource Map; Device 3 = Logistics / FEMA Costs / Check-In Station. '
    'All three devices connect to EMCOMM-NET simultaneously.'))
story.append(SP(8))

# TEST 1
story.append(test_header(1, 'Multi-Device Simultaneous Access'))
story.append(SP(4))
for n, action, expected in [
    (1, 'Connect all 3 devices to EMCOMM-NET simultaneously.', 'All devices receive IP addresses via DHCP. Network shows 3+ connected clients.'),
    (2, 'On each device, navigate to http://192.168.50.1 simultaneously.', 'All three dashboards load without delay. No timeout or error.'),
    (3, 'On Device 1: open the Net Control Logger and start a net.', 'Net opens on Device 1.'),
    (4, 'On Device 2: open the T-Card Resource Board.', 'T-Card board loads on Device 2.'),
    (5, 'On Device 3: open Personnel Accountability.', 'Accountability page loads on Device 3.'),
    (6, 'While all three tools are open and active, perform simultaneously: Device 1 logs a check-in; Device 2 changes a T-card status; Device 3 refreshes the PAR page.', 'All three operations complete without conflict. No 500 errors, no database lock errors, no timeouts.'),
    (7, 'On Device 2, open the Observer Link from Device 1\u2019s net.', 'Observer view loads on Device 2 and shows live net status.'),
]:
    url = ('http://192.168.50.1/netcontrol.html' if n == 3 else
           'http://192.168.50.1/resources.html' if n == 4 else
           'http://192.168.50.1/accountability.html' if n == 5 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 2
story.append(test_header(2, 'WAN Failover Under Load'))
story.append(SP(4))
for n, action, expected in [
    (8, 'Verify WAN is active (green status on dashboard).', 'Primary WAN indicator green.'),
    (9, 'Load the NEXRAD Radar page on Device 3 and start playback.', 'Radar animates normally.'),
    (10, 'Disconnect the primary WAN source (unplug antenna or disable hotspot).', 'Dashboard WAN status changes to Fallback (blue) or Offline (red) within 60 seconds. Radar page shows offline banner.'),
    (11, 'Verify all ICS tools on Devices 1 and 2 continue working.', 'Net logger, T-cards, check-in, accountability \u2014 all fully functional offline.'),
    (12, 'Reconnect primary WAN.', 'Dashboard WAN status returns to primary (green) within 60 seconds. Radar resumes automatically.'),
    (13, 'Repeat failover 3 times in succession.', 'System recovers correctly each time. No data loss. No session drops.'),
]:
    url = 'http://192.168.50.1/radar.html' if n == 9 else None
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 3 — Sustained simulation table
story.append(test_header(3, 'Sustained 60-Minute Operational Period Simulation'))
story.append(SP(3))
story.append(P(
    'Run the following activities continuously for 60 minutes as a simulated real activation. '
    'Record any errors, slowdowns, or unexpected behavior.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
sim_data = [[
    P('MINUTE', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('ACTIVITY', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('DEVICE', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
    P('RESULT', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
]]
sim_rows = [
    ('0\u20135', 'Net Control: Open net and log 5 check-ins', '1', '\u25a0 OK  \u25a0 Issue'),
    ('5\u201310', 'Operations: Add 3 resources to T-card board', '2', '\u25a0 OK  \u25a0 Issue'),
    ('10\u201315', 'Check-In: QR scan check-in for 3 personnel', '3', '\u25a0 OK  \u25a0 Issue'),
    ('15\u201320', 'IC: Complete ICS-202 objectives', '1', '\u25a0 OK  \u25a0 Issue'),
    ('20\u201325', 'Operations: Set GPS position on 2 resources', '2', '\u25a0 OK  \u25a0 Issue'),
    ('25\u201330', 'Conduct PAR on all checked-in personnel', '3', '\u25a0 OK  \u25a0 Issue'),
    ('30\u201335', 'Net Control: Log traffic entry; export ICS-309', '1', '\u25a0 OK  \u25a0 Issue'),
    ('35\u201340', 'Finance: Add 2 FEMA labor entries', '2', '\u25a0 OK  \u25a0 Issue'),
    ('40\u201345', 'IC: Compile IAP PDF (ICS-202, 203, 205)', '1', '\u25a0 OK  \u25a0 Issue'),
    ('45\u201350', 'Operations: Update T-card status changes', '2', '\u25a0 OK  \u25a0 Issue'),
    ('50\u201355', 'Net Control: Close net; open new period', '1', '\u25a0 OK  \u25a0 Issue'),
    ('55\u201360', 'All devices: Navigate dashboard; verify no lag', 'All', '\u25a0 OK  \u25a0 Issue'),
]
for minute, activity, device, result in sim_rows:
    sim_data.append([
        P(minute, S('sv', fontSize=8, leading=11)),
        P(activity, S('sv', fontSize=8, leading=11)),
        P(device, S('sv', fontSize=8, leading=11, alignment=TA_CENTER)),
        P(result, S('sv', fontSize=7.5, leading=11, textColor=HexColor('#334466'))),
    ])
sim_data.append([
    P('', S('sv', fontSize=8)),
    P('<b>Total errors/issues during sustained period: ______</b>', S('sv', fontName='Helvetica-Bold', fontSize=8, leading=11)),
    P('', S('sv')),
    P('\u25a0 Fast  \u25a0 OK  \u25a0 Slow  \u25a0 Unacceptable', S('sv', fontSize=7.5, leading=11)),
])
sim_t = Table(sim_data, colWidths=[0.65*inch, 3.0*inch, 0.6*inch, CW-4.25*inch], repeatRows=1)
sim_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-2), [white, LGRAY]),
    ('BACKGROUND',    (0,-1),(-1,-1), MGRAY),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(sim_t)
story.append(SP(8))

# TEST 4 — Edge cases
story.append(test_header(4, 'Edge Cases & Error Handling'))
story.append(SP(3))
story.append(P(
    'Test each edge case. Record whether the system handles it gracefully '
    '(no crash, clear error message, data preserved).',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
edge_data = [[
    P('EDGE CASE', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('HOW TO TEST', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('EXPECTED BEHAVIOR', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('RESULT', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
]]
edges = [
    ('Empty incident \u2014 no data', 'Create new incident, immediately open IAP Compile', 'Empty state shown gracefully. No crash.'),
    ('Very long text in form fields', 'Enter 500+ character string in ICS-202 objectives', 'Text accepted. Truncated or wrapped in PDF. No crash.'),
    ('Special characters in fields', 'Enter: & \" \' < > / \\ # @ ! in roster name', 'Characters stored and displayed correctly. No XSS or SQL error.'),
    ('Duplicate callsign check-in', 'Check in the same callsign twice to the same net', 'Either: duplicate warning shown, OR both entries logged with timestamps.'),
    ('Check out before checking in', 'Try to click Check Out on a person already checked out', 'Button disabled or graceful no-op. No duplicate checkout.'),
    ('Invalid coordinates in GPS', 'Enter lat = 999, lon = 999 in resource map modal', 'Validation error: \u201cCoordinates out of range.\u201d No pin placed.'),
    ('Zero-cost FEMA entries', 'Add labor entry with 0 hours and 0 rate', 'Entry saves. Total = $0.00. No division-by-zero error.'),
    ('Delete active incident', 'Attempt to delete/archive the currently active incident', 'Either: warning shown before proceeding, OR deleted cleanly.'),
    ('QR scan \u2014 camera permission denied', 'Click Start Camera then deny permission', 'Clear error message. Manual entry fallback still usable.'),
    ('Very large roster import (50+ members)', 'Import a CSV with 50 entries', 'All 50 import successfully. No timeout. Page remains responsive.'),
    ('Simultaneous form saves from two devices', 'Two devices edit and save the same ICS-202 form at the same time', 'Last-write wins. No crash. Data coherent.'),
    ('API server unreachable (localStorage fallback)', 'Kill the API server from the Pi terminal. Try to use a form.', 'localStorage fallback activates. Warning shown. Data preserved locally.'),
    ('Disconnect from EMCOMM-NET mid-session', 'Disconnect Wi-Fi on one device. Reconnect. Resume work.', 'Page reloads and recovers. No data lost.'),
    ('Browser back button from ICS form', 'Fill out ICS-205, navigate back, navigate forward', 'Data retained. No data loss from browser navigation.'),
]
for case, method, expected in edges:
    edge_data.append([
        P(case, S('ev', fontSize=7.5, leading=10, fontName='Helvetica-Bold')),
        P(method, S('ev', fontSize=7.5, leading=10)),
        P(expected, S('ev', fontSize=7.5, leading=10, textColor=HexColor('#1a4a1a'))),
        P('\u25a0 Pass  \u25a0 Fail', S('ev', fontSize=7.5, leading=10, alignment=TA_CENTER)),
    ])
edge_t = Table(edge_data, colWidths=[1.3*inch, 1.6*inch, 2.3*inch, CW-5.2*inch], repeatRows=1)
edge_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(edge_t)
story.append(SP(8))

# TEST 5
story.append(test_header(5, 'ICS-204A Briefing Sheet & Starcom Resource Map'))
story.append(SP(4))
for n, action, expected in [
    (14, 'Navigate to ICS-204A Briefing Sheet.', 'Form loads with assignment briefing fields.'),
    (15, 'Fill in Branch, Division, operational period, and 2 resources assigned.', 'Fields accept input.'),
    (16, 'Save and print.', 'Print layout opens with all data.'),
    (17, 'Navigate to Starcom Resource Map.', 'Public safety resource map loads. Different from ICS resource map.'),
    (18, 'Add a Starcom unit position to the map.', 'Unit marker appears on map.'),
]:
    url = ('http://192.168.50.1/briefing_204a.html' if n == 14 else
           'http://192.168.50.1/resmap.html' if n == 17 else None)
    story.append(step(n, action, expected, url))
story.append(SP(8))

# TEST 6 — Performance
story.append(test_header(6, 'System Performance Measurements'))
story.append(SP(3))
story.append(P(
    'Measure and record the following performance metrics. These establish a baseline for v1.0 '
    'and identify any performance issues.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
perf_data = [[
    P('MEASUREMENT', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('HOW TO MEASURE', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('RESULT (sec)', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
    P('ACCEPTABLE?', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
]]
perfs = [
    ('Dashboard load time', 'Hard refresh (Ctrl+Shift+R) on index.html. Time to full load.', '\u25a0 Yes (<3s)  \u25a0 No'),
    ('FCC callsign lookup', 'Time from typing callsign to name appearing in Net Logger.', '\u25a0 Yes (<1s)  \u25a0 No'),
    ('T-card board with 10 resources', 'Time for T-card board to load with 10 resources.', '\u25a0 Yes (<2s)  \u25a0 No'),
    ('IAP PDF compilation (6 forms)', 'Time from clicking Compile to PDF download beginning.', '\u25a0 Yes (<20s) \u25a0 No'),
    ('IAP Save as PDF (iap.html)', 'Time from clicking Save as PDF to PDF download beginning.', '\u25a0 Yes (<15s) \u25a0 No'),
    ('Personnel Accountability load', 'Time for PAR page to load with 10 check-ins.', '\u25a0 Yes (<3s)  \u25a0 No'),
    ('QR scan detection time', 'Time from holding QR to camera to detection confirmation.', '\u25a0 Yes (<2s)  \u25a0 No'),
    ('GPS resource map with 5 pins', 'Time for map to load and display 5 resource markers.', '\u25a0 Yes (<3s)  \u25a0 No'),
    ('Cost dashboard with 10 entries', 'Time for cost dashboard to load and calculate totals.', '\u25a0 Yes (<3s)  \u25a0 No'),
]
for measurement, method, acceptable in perfs:
    perf_data.append([
        P(measurement, S('pv', fontSize=8, leading=11, fontName='Helvetica-Bold')),
        P(method, S('pv', fontSize=7.5, leading=10)),
        P('____s', S('pv', fontSize=9, leading=11, alignment=TA_CENTER)),
        P(acceptable, S('pv', fontSize=7.5, leading=10, alignment=TA_CENTER)),
    ])
perf_t = Table(perf_data, colWidths=[1.7*inch, 2.6*inch, 0.7*inch, CW-5.0*inch], repeatRows=1)
perf_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 4),
    ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ('LEFTPADDING',   (0,0), (-1,-1), 5),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(perf_t)
story.append(SP(8))

# TEST 7
story.append(test_header(7, 'Final Cleanup & Beta Reset'))
story.append(SP(4))
for n, action, expected in [
    (19, 'Archive all test incidents to USB before reset.', 'JSON archive files written to USB for records.'),
    (20, 'Run Beta/Scenario Reset.', 'All test data cleared. Roster and config preserved.'),
    (21, 'Verify the system is in clean state for handover or next activation.', 'Dashboard shows no active incident. Roster intact.'),
    (22, 'Document any unresolved defects in the Defect Log on the final page.', 'All defects captured for developer review.'),
]:
    url = 'http://192.168.50.1/incident_mgmt.html' if n == 19 else None
    story.append(step(n, action, expected, url))
story.append(SP(10))

story.append(P('<b>SCENARIO 6 \u2014 PASS / FAIL SUMMARY</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(4))
story.append(pf_table([
    'Test 1 \u2014 Multi-Device Simultaneous Access',
    'Test 2 \u2014 WAN Failover Under Load',
    'Test 3 \u2014 Sustained 60-Minute Simulation',
    'Test 4 \u2014 Edge Cases & Error Handling',
    'Test 5 \u2014 204A Briefing & Starcom Map',
    'Test 6 \u2014 Performance Measurements',
    'Test 7 \u2014 Final Cleanup',
]))
story.append(SP(6))
story.append(overall_result())
story += tester_line()


# ══════════════════════════════════════════════════════════════════════════════
# OVERALL SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
story.append(P('<b>OVERALL BETA TEST SUMMARY \u2014 ALL SIX SCENARIOS</b>',
               S('pfs', fontName='Helvetica-Bold', fontSize=11, textColor=EOC)))
story.append(SP(4))
overall_data = [[
    P('SCENARIO', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('TITLE', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('RESULT', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10, alignment=TA_CENTER)),
    P('CRITICAL DEFECTS', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
]]
scenario_list = [
    ('1', 'System Setup & Incident Creation'),
    ('2', 'Roster, Check-In & Personnel Accountability'),
    ('3', 'Full ICS Platform, T-Cards & IAP'),
    ('4', 'Amateur Radio EMCOMM & Net Loggers'),
    ('5', 'FEMA Documentation & Situational Awareness'),
    ('6', 'Multi-Operator Simulation & Stress Test'),
]
for num, title in scenario_list:
    overall_data.append([
        P(num, S('ov', fontName='Helvetica-Bold', fontSize=9, leading=11, alignment=TA_CENTER)),
        P(title, S('ov', fontSize=8.5, leading=11)),
        P('\u25a0 Pass  \u25a0 Fail', S('ov', fontSize=8, leading=11, alignment=TA_CENTER)),
        P('', S('ov', fontSize=8, leading=11)),
    ])
ov_t = Table(overall_data, colWidths=[0.55*inch, 2.8*inch, 1.0*inch, CW-4.35*inch], repeatRows=1)
ov_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.4, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('LEFTPADDING',   (0,0), (-1,-1), 8),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(ov_t)
story.append(SP(8))

# Final verdict
verdict = Table([[
    P('<b>FINAL BETA TEST VERDICT:</b>', S('fv', fontName='Helvetica-Bold', fontSize=10,
                                            textColor=EOC, leading=13)),
    P('\u25a0  PASS \u2014 System ready for operational deployment\n'
      '\u25a0  CONDITIONAL PASS \u2014 Passes with documented workarounds. Critical defects must be resolved before operational use.\n'
      '\u25a0  FAIL \u2014 Critical defects prevent operational deployment.',
      S('fvv', fontSize=9, leading=14)),
]], colWidths=[1.8*inch, CW-1.8*inch])
verdict.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
    ('BOX',           (0,0), (-1,-1), 1.2, EOC),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING',   (0,0), (-1,-1), 10),
    ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
]))
story.append(verdict)
story.append(SP(10))

# Defect log
story.append(P('<b>DEFECT LOG</b>',
               S('dl', fontName='Helvetica-Bold', fontSize=10, textColor=EOC)))
story.append(SP(3))
story.append(P(
    'Document all defects found during testing. Include: Scenario #, Test #, Step #, '
    'description of behavior, expected vs. actual, and severity.',
    S('td', fontSize=8.5, leading=12)))
story.append(SP(4))
defect_data = [[
    P('ID', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('SCENARIO / TEST / STEP', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('DESCRIPTION', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('SEVERITY', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
    P('STATUS', S('sh2', fontName='Helvetica-Bold', fontSize=8, textColor=white, leading=10)),
]]
for i in range(1, 9):
    defect_data.append([
        P(f'D-{i:03d}', S('dv', fontName='Helvetica-Bold', fontSize=8.5, leading=11)),
        P('', S('dv', fontSize=8)),
        P('', S('dv', fontSize=8)),
        P('\u25a0 Critical\n\u25a0 Major\n\u25a0 Minor', S('dv', fontSize=7.5, leading=12)),
        P('\u25a0 Open\n\u25a0 Fixed', S('dv', fontSize=7.5, leading=12)),
    ])
def_t = Table(defect_data, colWidths=[0.55*inch, 1.4*inch, 2.6*inch, 0.9*inch, CW-5.45*inch],
              repeatRows=1)
def_t.setStyle(TableStyle([
    ('BACKGROUND',    (0,0), (-1,0),  EOC),
    ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
    ('GRID',          (0,0), (-1,-1), 0.3, LINE),
    ('TOPPADDING',    (0,0), (-1,-1), 10),
    ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ('LEFTPADDING',   (0,0), (-1,-1), 6),
    ('VALIGN',        (0,0), (-1,-1), 'TOP'),
]))
story.append(def_t)
story.append(SP(12))

# Sign-off
signoff = Table([[
    P('Lead Beta Tester:', S('so', fontSize=9)),
    P('_______________________________', S('so', fontSize=9)),
    P('Callsign:', S('so', fontSize=9)),
    P('____________', S('so', fontSize=9)),
],[
    P('Organization:', S('so', fontSize=9)),
    P('_______________________________', S('so', fontSize=9)),
    P('Date:', S('so', fontSize=9)),
    P('____________', S('so', fontSize=9)),
]], colWidths=[1.2*inch, 2.2*inch, 0.8*inch, CW-4.2*inch])
signoff.setStyle(TableStyle([
    ('LINEBELOW', (1,0), (1,0), 0.5, LINE),
    ('LINEBELOW', (3,0), (3,0), 0.5, LINE),
    ('LINEBELOW', (1,1), (1,1), 0.5, LINE),
    ('LINEBELOW', (3,1), (3,1), 0.5, LINE),
    ('TOPPADDING', (0,0), (-1,-1), 6),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
]))
story.append(signoff)
story.append(SP(8))
story.append(P(
    'Submit completed beta test package (photo or scan) to: '
    '<b>James Rospopo KE4CON</b>  \u00b7  '
    'https://github.com/KE4CON/FieldCommand-IMS/issues',
    S('sub', fontSize=8.5, textColor=EOC_LT, leading=12)))
story.append(SP(4))
story.append(P(
    'FieldCommand IMS v1.0 Beta Test Scenarios  \u00b7  '
    'Copyright \u00a9 2026 James Rospopo KE4CON  \u00b7  FOR BETA TESTING USE ONLY',
    S('cr', fontSize=7.5, textColor=HexColor('#8090b0'), leading=11)))


# ── Build ─────────────────────────────────────────────────────────────────────
out = '/mnt/user-data/outputs/FieldCommand_BetaTest_Complete_Package.pdf'
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=M, rightMargin=M,
    topMargin=0.55*inch, bottomMargin=0.42*inch,
    title='FieldCommand IMS v1.0 \u2014 Beta Test Scenarios',
    author='James Rospopo KE4CON')
doc.build(story, canvasmaker=NC)

from pypdf import PdfReader
r = PdfReader(out)
print(f'BUILT: {out}')
print(f'Pages: {len(r.pages)}')
