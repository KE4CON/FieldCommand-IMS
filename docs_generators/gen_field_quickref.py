#!/usr/bin/env python3
"""
FieldCommand Field Quick-Reference — PDF Generator
FieldCommand IMS
8-page lean field guide. Print double-sided and hand out at check-in.
Output: /mnt/user-data/outputs/FieldCommand_Field_Quick_Reference.pdf
"""
import datetime
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.pdfgen import canvas

# ── Palette ──────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
EOC_BG = HexColor('#eef2f7')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#b0c4dc')
LGRAY  = HexColor('#f0f3f6')
MUTED  = HexColor('#4a6080')
GREEN  = HexColor('#1a7a3a')
SGREEN = HexColor('#1a6b2a')
SGREEN_BG = HexColor('#e0f0e4')
AMBER  = HexColor('#c8760a')
AMBER_BG = HexColor('#fef3d8')
PURPLE = HexColor('#5b2d8c')
RED_BG = HexColor('#fde8e8')
RED    = HexColor('#b82020')

ORG   = 'FieldCommand IMS — FieldCommand Incident Management System'
PROD  = 'FieldCommand IMS v1.0 — Field Quick-Reference'
TODAY = datetime.date.today().strftime('%B %Y')
PAGE_W, PAGE_H = letter
M  = 0.60 * inch
CW = PAGE_W - 2*M

# ── Canvas ────────────────────────────────────────────────────────────────────
class NC(canvas.Canvas):
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
                self._chrome(total)
            super().showPage()
        super().save()

    def _draw_cover(self):
        """Full-page canvas-drawn cover."""
        # ── Pull org identity from station_config if DB is available ──────────
        line1 = 'FieldCommand Incident Management System'
        line2 = 'Open-Source  ·  Offline-First  ·  Field-Deployable'
        try:
            import sqlite3, os
            db_path = os.environ.get(
                'FIELDCOMMAND_DB',
                '/opt/fieldcommand/data/fieldcommand.db'
            )
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                row = conn.execute(
                    "SELECT callsign, org_name, org_short, agency_name FROM station_config WHERE id=1"
                ).fetchone()
                conn.close()
                if row:
                    callsign, org_name, org_short, agency_name = row
                    if org_name and callsign:
                        line1 = f'{callsign}  ·  {org_name}'
                        line2 = agency_name if agency_name else 'Emergency Communications  ·  ICS/NIMS'
                    elif org_name:
                        line1 = org_name
                        line2 = agency_name if agency_name else 'Emergency Communications  ·  ICS/NIMS'
        except Exception:
            pass  # fall through to universal defaults
        # ─────────────────────────────────────────────────────────────────────
        self.setFillColor(HexColor('#1a3a6b'))
        self.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        self.setFillColor(HexColor('#f0c040'))
        self.rect(0, PAGE_H - 0.18*inch, PAGE_W, 0.18*inch, fill=1, stroke=0)
        self.setFillColor(HexColor('#f0c040'))
        self.rect(0, 0, PAGE_W, 0.18*inch, fill=1, stroke=0)
        self.setFillColor(HexColor('#1e4480'))
        self.rect(0, PAGE_H*0.38, PAGE_W, PAGE_H*0.36, fill=1, stroke=0)
        self.setFillColor(HexColor('#f0c040'))
        self.setFont('Helvetica-Bold', 10)
        self.drawCentredString(PAGE_W/2, PAGE_H - 0.70*inch, line1)
        self.setFillColor(HexColor('#c0d4f0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H - 0.88*inch, line2)
        self.setFillColor(HexColor('#ffffff'))
        self.setFont('Helvetica-Bold', 58)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.60, 'FIELDCOMMAND')
        self.setFillColor(HexColor('#f0c040'))
        self.setFont('Helvetica-Bold', 15)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.545,
            'Incident Management System  v1.0')
        self.setStrokeColor(HexColor('#f0c040'))
        self.setLineWidth(1.5)
        self.line(M*2, PAGE_H*0.505, PAGE_W - M*2, PAGE_H*0.505)
        self.setFillColor(HexColor('#ffffff'))
        self.setFont('Helvetica-Bold', 26)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.448, 'FIELD QUICK REFERENCE')
        self.setFillColor(HexColor('#c0d4f0'))
        self.setFont('Helvetica', 10)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.395, 'Operator Quick Reference Card')
        self.setFillColor(HexColor('#8090c0'))
        self.setFont('Helvetica', 9.5)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.30,
            'RACES  ·  ARES  ·  ICS/NIMS  ·  Amateur Radio EMCOMM  ·  Public Safety')
        self.setFillColor(HexColor('#6070a0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.25, TODAY)
        self.setFillColor(HexColor('#1a3a6b'))
        self.setFont('Helvetica', 7)
        self.drawCentredString(PAGE_W/2, 0.05*inch,
            f'FieldCommand IMS v1.0  ·  Open-Source Field-Deployable ICS Platform  ·  {TODAY}')


    def _chrome(self, total):
        n = self._pageNumber
        LOGO = Path('/home/claude/esv-logo.png')
        if n > 1:
            self.setFillColor(EOC)
            self.rect(0, PAGE_H-0.44*inch, PAGE_W, 0.44*inch, fill=1, stroke=0)
            self.setFillColor(GOLD)
            self.rect(0, PAGE_H-0.46*inch, PAGE_W, 0.02*inch, fill=1, stroke=0)
            if LOGO.exists():
                try:
                    self.drawImage(str(LOGO), M, PAGE_H-0.41*inch,
                                   width=0.85*inch, height=0.34*inch,
                                   preserveAspectRatio=True, mask='auto')
                except Exception:
                    pass
            self.setFillColor(white)
            self.setFont('Helvetica-Bold', 9)
            self.drawString(M+1.0*inch, PAGE_H-0.21*inch, PROD)
            self.setFont('Helvetica', 7)
            self.drawString(M+1.0*inch, PAGE_H-0.34*inch, ORG)
        self.setFillColor(EOC)
        self.rect(0, 0, PAGE_W, 0.38*inch, fill=1, stroke=0)
        self.setFillColor(GOLD)
        self.rect(0, 0.38*inch, PAGE_W, 0.013*inch, fill=1, stroke=0)
        self.setFillColor(white)
        self.setFont('Helvetica', 6.5)
        if n > 1:
            self.drawString(M, 0.17*inch,
                'EMCOMM-NET  ·  http://192.168.50.1  ·  For Authorized Personnel Only  ·  '
                '© 2026 James Rospopo KE4CON  ·  CC BY-SA 4.0')
            self.drawString(M, 0.06*inch,
                f'Page {n} of {total}  ·  {TODAY}  ·  creativecommons.org/licenses/by-sa/4.0')
        else:
            self.drawCentredString(PAGE_W/2, 0.10*inch,
                f'FieldCommand IMS v1.0  ·  {ORG}  ·  {TODAY}')

# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=black,
             leading=12, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

def P(t, s=None):  return Paragraph(t, s or S('b'))
def SP(n=4):       return Spacer(1, n)
def HR(c=LINE, t=0.4):
    return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=2, spaceAfter=2)
def PB():          return PageBreak()

def section_hdr(icon, title, url, color, bg):
    inner = Table([[
        P(f'{icon}  {title}',
          S('sh', fontName='Helvetica-Bold', fontSize=13, textColor=color, leading=16)),
        P(f'<font color="#888888" size="8">{url}</font>',
          S('su', fontSize=8, textColor=MUTED, alignment=TA_LEFT, leading=10)),
    ]], colWidths=[CW*0.55, CW*0.45])
    inner.setStyle(TableStyle([
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))
    outer = Table([[inner]], colWidths=[CW])
    outer.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
        ('LINEBELOW',     (0,0), (-1,-1), 1.5, color),
    ]))
    return outer

def steps_tbl(rows):
    data = [[P('STEP', S('th', fontName='Helvetica-Bold', fontSize=7.5,
                          textColor=white, leading=9)),
             P('WHAT TO DO', S('th', fontName='Helvetica-Bold', fontSize=7.5,
                                textColor=white, leading=9))]]
    for num, desc in rows:
        data.append([
            P(str(num), S('tn', fontName='Helvetica-Bold', fontSize=9,
                           textColor=EOC_LT, alignment=TA_CENTER, leading=11)),
            P(desc, S('td', fontSize=8.5, leading=12)),
        ])
    t = Table(data, colWidths=[0.50*inch, CW-0.50*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('LINEBELOW',     (0,0), (-1,0),  1, EOC_LT),
    ]))
    return t

def ref_tbl(headers, rows, widths):
    data = [[P(h, S('th', fontName='Helvetica-Bold', fontSize=7.5,
                      textColor=white, leading=9)) for h in headers]]
    for row in rows:
        data.append([P(c, S('td', fontSize=8, leading=11)) for c in row])
    t = Table(data, colWidths=widths, repeatRows=1, splitByRow=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
        ('LINEBELOW',     (0,0), (-1,0),  1, EOC_LT),
    ]))
    return t

def tip(txt, color=EOC_LT, bg=EOC_BG):
    t = Table([[
        P('▶', S('ti', fontName='Helvetica-Bold', fontSize=9,
                  textColor=color, leading=11)),
        P(txt, S('tt', fontSize=8, leading=11, textColor=black)),
    ]], colWidths=[0.22*inch, CW-0.22*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,-1), bg),
        ('LEFTPADDING',   (0,0), (-1,-1), 6),
        ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('TOPPADDING',    (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LINEAFTER',     (0,0), (0,-1),  1.5, color),
    ]))
    return t

# ══════════════════════════════════════════════════════════════════════════════
story = []

#
# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — COVER  (drawn by NC canvas class)
# ══════════════════════════════════════════════════════════════════════════════
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — GETTING STARTED & DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('🖥', 'Getting Started & Dashboard',
                         'http://192.168.50.1', EOC, EOC_BG))
story.append(SP(6))
story.append(steps_tbl([
    ('1', '<b>Connect to EMCOMM-NET</b> — open Wi-Fi on your device and select EMCOMM-NET.'),
    ('2', '<b>Open any browser</b> — type <b>http://192.168.50.1</b> and press Enter.'),
    ('3', '<b>Select a mode</b> — three tabs at the top: Amateur Radio · Public Safety · All-Hazards ICS.'),
    ('4', '<b>Bookmark it</b> — on a phone tap Share → Add to Home Screen for one-tap access.'),
]))
story.append(SP(6))
story.append(ref_tbl(
    ['MODE', 'USE IT FOR'],
    [
        ['All-Hazards ICS',       'Incident management, IAP, T-cards, FEMA costs, personnel check-in'],
        ['Amateur Radio EMCOMM',  'ARES/RACES nets, APRS, Winlink, JS8Call, AMPRNet, callsign lookup'],
        ['Public Safety',         'Starcom/P25 nets, resource map, weather radar, hospital directory'],
    ],
    [1.6*inch, CW-1.6*inch]))
story.append(SP(6))
story.append(ref_tbl(
    ['INDICATOR', 'MEANING'],
    [
        ['🟢 Green — Cellular',  'Primary internet active — all live features enabled'],
        ['🔵 Blue — Satellite',  'Satellite failover active — all live features enabled'],
        ['🔴 Red — Offline',     'No internet — ALL core ICS tools still fully operational'],
        ['🟢 AMPRNet UP',        '44Net WireGuard tunnel active (gateway Pi)'],
    ],
    [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(tip('A red WAN indicator does NOT mean FieldCommand is down. '
                 'Net loggers, ICS forms, T-cards, roster, check-in, and all local tools run offline.'))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — NET LOGGERS (AMATEUR + PUBLIC SAFETY)
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('📻', 'Amateur Net Control Logger',
                         'http://192.168.50.1/netcontrol.html', EOC, EOC_BG))
story.append(SP(6))
story.append(steps_tbl([
    ('1', '<b>Open a net</b> — enter net name, frequency, and mode. Click <b>Open Net</b>.'),
    ('2', '<b>Check in a station</b> — type callsign and press Enter. Name auto-fills from offline FCC database.'),
    ('3', '<b>Log traffic</b> — click <b>+ Traffic</b> — enter precedence, from, to, and message info.'),
    ('4', '<b>Check out a station</b> — click <b>Check Out</b>. Duration recorded to nearest ¼ hour.'),
    ('5', '<b>Close the net</b> — click <b>Close Net</b>. All remaining stations auto-checked out.'),
    ('6', '<b>Export ICS-309</b> — downloads formatted comms log with all check-ins and durations.'),
    ('7', '<b>Observer link</b> — click 🔗 to share a read-only live view with EOC or served agency.'),
]))
story.append(SP(6))
story.append(section_hdr('🚔', 'Public Safety Net Logger',
                         'http://192.168.50.1/starcom.html', SGREEN, SGREEN_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['FIELD', 'DESCRIPTION'],
    [
        ['Radio ID',      'Trunked/P25 unit number — required for every check-in'],
        ['Unit Name',     'Agency and unit description. Roster auto-fills if Radio ID matches.'],
        ['Dispatch Ctr',  'Dispatching agency (e.g. MCECC, IDOT)'],
        ['Export ICS-309','Radio IDs appear in station column — same export as amateur logger'],
    ],
    [1.2*inch, CW-1.2*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — ROSTER, QR CHECK-IN & PERSONNEL ACCOUNTABILITY
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('👥', 'Member Roster & QR Check-In Codes',
                         'http://192.168.50.1/roster.html', EOC, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['ACTION', 'HOW'],
    [
        ['Add member',        'Click + Add Member — enter Member ID, name, callsign or Radio ID, role'],
        ['Import CSV',        'Click 📥 Import CSV — required column: member_id. All others optional.'],
        ['Generate QR code',  'Click QR button on any member card — print or save PNG for their badge'],
        ['Export roster',     'Click 📤 Export CSV — downloads all members for backup or transfer'],
    ],
    [1.5*inch, CW-1.5*inch]))
story.append(SP(6))
story.append(section_hdr('📷', 'Scan Check-In (QR/Barcode)',
                         'http://192.168.50.1/scan_checkin.html', EOC_LT, EOC_BG))
story.append(SP(4))
story.append(steps_tbl([
    ('1', '<b>Open Scan Check-In</b> on a camera device. Click <b>📷 Start Camera</b>.'),
    ('2', '<b>Scan QR code</b> — point camera at member\'s QR. Name auto-fills from roster.'),
    ('3', '<b>Manual fallback</b> — type member ID, callsign, or Radio ID and press Enter.'),
    ('4', '<b>Check In</b> — confirm fields and click ✓ Check In. Success screen appears.'),
]))
story.append(SP(6))
story.append(section_hdr('🔴', 'Personnel Accountability (PAR)',
                         'http://192.168.50.1/accountability.html', RED, HexColor('#fef2f2')))
story.append(SP(4))
story.append(ref_tbl(
    ['TAB', 'WHAT IT SHOWS'],
    [
        ['ICS-211 Check-In List', 'All checked-in personnel · Check Out button · PAR confirm button'],
        ['T-Card Personnel',      'Personnel grouped by resource · PAR per resource group'],
        ['⚠ Unaccounted',         'Personnel not yet confirmed in current PAR — contact supervisor immediately'],
        ['Cross-Reference',       'Checked-in but no T-card · On T-card but no check-in (safety gap)'],
    ],
    [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(tip('Click 🔴 Conduct PAR to start a PAR cycle. '
                 'Click ✓ PAR on each person as supervisors report in. '
                 'Reset PAR to begin a new cycle.'))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — T-CARD RESOURCE BOARD & GPS RESOURCE MAP
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('📦', 'T-Card Resource Board & Personnel',
                         'http://192.168.50.1/resources.html', AMBER, AMBER_BG))
story.append(SP(4))
story.append(steps_tbl([
    ('1', '<b>Add resource</b> — click + Add Resource. Enter name, type, status, assignment, leader.'),
    ('2', '<b>Change status</b> — click status badge to cycle: Available → Assigned → Staging → Out of Service.'),
    ('3', '<b>Add personnel</b> — click any T-card → 👤 PERSONNEL tab → type name → select from roster suggestion.'),
    ('4', '<b>Set ICS position</b> — choose the person\'s role on THIS resource (Crew Boss, EMT, Operator, etc.).'),
]))
story.append(SP(4))
story.append(ref_tbl(
    ['STATUS', 'COLOR', 'MEANING'],
    [
        ['Available',      'Green',  'On scene and ready for assignment'],
        ['Assigned',       'Blue',   'Actively tasked to a division or group'],
        ['Staging',        'Lt Blue','En route or waiting at staging area'],
        ['Out of Service', 'Red',    'Unavailable — mechanical, medical, or released'],
    ],
    [1.2*inch, 0.8*inch, CW-2.0*inch]))
story.append(SP(6))
story.append(section_hdr('📍', 'GPS-Tracked Resource Map',
                         'http://192.168.50.1/resource_map.html', SGREEN, SGREEN_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['METHOD', 'HOW TO SET POSITION'],
    [
        ['Device GPS',     'Click 📍 Use Device GPS — browser gets your GPS coordinates automatically'],
        ['Click map',      'Click 🗺 Click Map to Place — crosshair cursor, click the map to set position'],
        ['Manual coords',  'Type decimal latitude and longitude directly into the fields'],
    ],
    [1.3*inch, CW-1.3*inch]))
story.append(SP(4))
story.append(tip('Resource pins are color-coded by status. '
                 'Resources without GPS show as dashed circles in the sidebar. '
                 'Enable Auto-refresh 30s for moving resources.'))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — ICS PLATFORM — FIVE SECTIONS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('🏛', 'ICS Platform — Five-Section Structure',
                         'http://192.168.50.1/ics/', EOC, EOC_BG))
story.append(SP(4))
story.append(steps_tbl([
    ('1', '<b>Create incident</b> — go to http://192.168.50.1/incident.html → + New Incident.'),
    ('2', '<b>Navigate sections</b> — tabs at top: ⭐ Command · 🔴 Operations · 📋 Planning · 🟢 Logistics · 💜 Finance.'),
    ('3', '<b>Advance period</b> — click + New Period at start of each operational period.'),
    ('4', '<b>Use event template</b> — event_templates.html → Activate → select type → instant pre-built incident.'),
]))
story.append(SP(4))
story.append(ref_tbl(
    ['SECTION', 'KEY TOOLS & FORMS'],
    [
        ['⭐ Command',
         'ICS-201 briefing · ICS-202 objectives · ICS-203 org chart · '
         'ICS-208 safety message · Position checklists · Meeting scheduler'],
        ['🔴 Operations',
         'T-card resource board · ICS-204 assignment lists · '
         'GPS resource map · Resource personnel rosters'],
        ['📋 Planning',
         'IAP assembly · ICS-205 comms plan · ICS-206 medical plan · '
         'ICS-209 status summary · ICS-211 check-in list · Planning P cycle'],
        ['🟢 Logistics',
         'ICS-205 radio comms (COML develops) · ICS-205A comms list · '
         'ICS-206 medical plan (MEDL develops) · Channel library · Facilities · ICS-218'],
        ['💜 Finance/Admin',
         'FEMA PA cost tracking · Force Account Labor · Equipment · '
         'Materials · Contracts · Cost dashboard · ICS-214 activity log'],
    ],
    [1.15*inch, CW-1.15*inch]))
story.append(SP(4))
story.append(tip('Under Unified Command (UC): enter "Unified Command" in the IC field. '
                 'List UC members in the ICS-203 Organization Assignment List. '
                 'All forms and T-cards work identically under UC.'))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — ICS FORMS, SIGNATURES & IAP PDF
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('📋', 'ICS Forms, Digital Signatures & IAP Compilation',
                         'http://192.168.50.1/ics-form.html', PURPLE, HexColor('#f0e8fc')))
story.append(SP(4))
story.append(ref_tbl(
    ['FORM', 'TITLE', 'DEVELOPED BY'],
    [
        ['ICS-202', 'Incident Objectives',           'Planning Section Chief / IC'],
        ['ICS-203', 'Org Assignment List',           'Resources Unit Leader (RESL)'],
        ['ICS-204', 'Assignment List',               'RESL — distributed to Operations'],
        ['ICS-205', 'Radio Comms Plan',              'Comms Unit Leader (COML) — Logistics'],
        ['ICS-206', 'Medical Plan',                  'Medical Unit Leader (MEDL) — Logistics'],
        ['ICS-207', 'Org Chart',                     'Resources Unit Leader (RESL)'],
        ['ICS-208', 'Safety Message',                'Safety Officer (SOFR) — Command Staff'],
        ['ICS-209', 'Status Summary',                'Situation Unit Leader (SITL)'],
        ['ICS-211', 'Check-In List',                 'Resources Unit Leader (RESL)'],
        ['ICS-213', 'General Message',               'Any ICS position'],
        ['ICS-214', 'Activity Log',                  'All supervisors — every section'],
        ['ICS-215A','IAP Safety Analysis',           'Safety Officer (SOFR) with Ops input'],
        ['ICS-218', 'Support Vehicle Inventory',     'Ground Support Unit Leader (GSUL)'],
        ['ICS-221', 'Demobilization Check-Out',      'Demob Unit Leader (DMOB)'],
        ['ICS-309', 'Communications Log',            'Comms Unit Leader (COML) / any operator'],
    ],
    [0.75*inch, 1.55*inch, CW-2.3*inch]))
story.append(SP(4))
story.append(ref_tbl(
    ['TASK', 'HOW'],
    [
        ['Digital signature',   'Click any Prepared By / Approved By field — sign with mouse, touch, or stylus → Accept'],
        ['Compile IAP PDF',     'Go to iap_compile.html → check forms to include → click 📄 Compile IAP PDF (5–15 sec)'],
        ['Print IAP',           'Go to printcenter.html → select IAP PDF → print to any CUPS printer on the network'],
    ],
    [1.4*inch, CW-1.4*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — FEMA DOCUMENTATION & COST DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('💰', 'FEMA PA Cost Documentation',
                         'http://192.168.50.1/fema_costs.html', AMBER, AMBER_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['CATEGORY', 'WHAT TO ENTER', 'FEMA REQUIREMENT'],
    [
        ['Force Account Labor',
         'Employee name, title, regular hours, overtime hours, hourly rate, fringe %',
         'Only overtime is reimbursable for employees; all hours for volunteers'],
        ['Equipment',
         'Click 📋 Lookup → select FEMA category → rate auto-fills → enter hours and unit ID',
         'Must use FEMA Schedule of Equipment Rates (44 categories pre-loaded)'],
        ['Materials',
         'Vendor, description, PO number, unit cost, quantity',
         'Source documentation required — attach receipts to Project Worksheet'],
        ['Contracts',
         'Vendor, description, contract number, total amount',
         'Contract documentation required — competitive bid or sole-source justification'],
    ],
    [1.3*inch, 2.1*inch, CW-3.4*inch]))
story.append(SP(4))
story.append(steps_tbl([
    ('1', '<b>Update FEMA rates</b> — go to fema_rates.html annually when FEMA publishes new schedule.'),
    ('2', '<b>Import ICS-214</b> — on Force Account Labor tab, click Import from ICS-214 to pull hours.'),
    ('3', '<b>Export PW text</b> — click 📄 Export PW Text for a formatted Project Worksheet summary.'),
]))
story.append(SP(6))
story.append(section_hdr('📊', 'Real-Time Cost Dashboard',
                         'http://192.168.50.1/cost_dashboard.html', EOC_LT, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['PANEL', 'WHAT IT SHOWS'],
    [
        ['Total incident cost',     'Running total — updates every 2 minutes automatically'],
        ['Cost by category',        'Labor · Equipment · Materials · Contracts — amount and % of total'],
        ['Cost projection',         'Extrapolated cost based on current burn rate × remaining periods'],
        ['Budget tracker',          'Enter authorized budget to see remaining balance and % used'],
        ['Per-period breakdown',    'Costs attributed by operational period — for AAR documentation'],
    ],
    [1.6*inch, CW-1.6*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 9 — SITUATIONAL AWARENESS: RADAR, APRS, WEATHER
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('🌩', 'NEXRAD Animated Radar',
                         'http://192.168.50.1/radar.html', EOC_LT, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['CONTROL', 'FUNCTION'],
    [
        ['▶ / ⏸ Play/Pause',  'Start or stop animation loop'],
        ['◀ ▶ Step',          'Advance one frame at a time'],
        ['Scrubber',          'Jump to any point in the loop'],
        ['Speed',             '0.5× · 1× · 2× · 4× playback speed'],
        ['Station',           'Select nearest NEXRAD radar station for your area'],
        ['Palette',           'Standard (reflectivity) · Dual-pol · Enhanced'],
        ['Auto-refresh',      'New tiles load every 5 minutes when WAN is active'],
    ],
    [1.4*inch, CW-1.4*inch]))
story.append(SP(4))
story.append(tip('WAN REQUIRED for radar tiles. '
                 'When offline, last loaded frame displays with timestamp. '
                 'Radar resumes automatically when WAN returns.'))
story.append(SP(6))
story.append(section_hdr('🗺', 'Tactical APRS Map',
                         'http://192.168.50.1/tactical.html', EOC, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['SOURCE', 'REQUIRES WAN?', 'NOTES'],
    [
        ['RF APRS (TNC/direwolf)',  '✗ Always offline', 'Live RF stations from local TNC — always available'],
        ['APRS-IS internet feed',   '✓ WAN required',   'Internet feed pauses when offline; RF continues'],
        ['SARTopo GeoJSON overlay', '✗ Once imported',  'Import at sartopo_import.html — persists on map'],
        ['NWS weather polygons',    '✓ WAN required',   'Alert polygons overlay on the map'],
    ],
    [1.8*inch, 1.1*inch, CW-2.9*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 10 — AMATEUR RADIO EMCOMM TOOLS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('📡', 'Amateur Radio EMCOMM Tools',
                         'http://192.168.50.1/', EOC, EOC_BG))
story.append(SP(4))
story.append(tip(
    '<b>AMPRNet / 44Net Gateway applies only when an amateur radio group '
    'leads or is a key partner in the deployment.</b> '
    'FCC amateur license required for registration — '
    'a public safety agency or served organization cannot register independently. '
    'All other tools on this page work for any deployment. '
    'See User Manual Ch. 28 and Installation Guide Step 11 for full details.',
    RED, RED_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['TOOL', 'URL', 'QUICK USE'],
    [
        ['FCC Callsign Lookup',  '/callsign.html',
         'Type callsign → Enter. 800K+ licensees, fully offline. Click + Add to Roster.'],
        ['NTS Radiogram',        '/nts.html',
         'Fill preamble fields — word count auto-calculates. Print for traffic handling.'],
        ['Winlink Import',       '/winlink-import.html',
         'Drag Winlink XML form attachment → Review → Archive to active incident.'],
        ['JS8Call',              'Windows laptop',
         'Click JS8Call dashboard card → enter laptop IP → opens JS8Call web interface.'],
        ['HF Propagation',       '/propagation.html',
         'SFI · K-index · A-index from NOAA SWPC. Band-by-band conditions. WAN required.'],
        ['AMPRNet Gateway',      '192.168.50.2',
         '44Net WireGuard tunnel status · callsign-authenticated · Part 97 access log.'],
        ['Observer Mode',        '/observer.html',
         'Read-only live net view. Share URL with EOC — auto-refreshes every 15 seconds.'],
        ['Dead Man\'s Switch',   '/deadmans.html',
         'Arm next to a net. Audible alert if net goes silent beyond configured interval.'],
        ['ICS-309 Manual',       '/ics309.html',
         'Manual comms log entries. Add timestamp · from · to · subject · precedence.'],
        ['ICS-213 Message',      '/ics213.html',
         'Formal written message with digital signature. Print or send via Winlink.'],
    ],
    [1.5*inch, 1.15*inch, CW-2.65*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 11 — REFERENCE TOOLS & ADMIN URLS
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('🔧', 'Reference Tools',
                         'http://192.168.50.1/', EOC, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['TOOL', 'URL', 'QUICK USE'],
    [
        ['Repeater Database',     '/repeaters.html',
         'Filter by band/mode/CTCSS. Add local repeaters. Feeds ICS-205 channel picker.'],
        ['Channel Library',       '/channel_library.html',
         'Pre-loaded interop channels (NIFOG/VTAC). Add custom agency channels.'],
        ['Grid Square Calc',      '/grid.html',
         'Grid ↔ lat/lon · distance and bearing between two grids.'],
        ['Hospital Directory',    '/hospitals.html',
         'Trauma level · helipad · phone. Feeds ICS-206 medical plan.'],
        ['Facilities Directory',  '/facilities.html',
         'ICP · staging areas · shelters · supply depots. Links to T-card assignments.'],
        ['NIMS Resource Types',   '/resource_types.html',
         'Pre-loaded NIMS types. Add custom types — available instantly in T-card board.'],
        ['Radio Cheat Sheets',    '/cheatsheets.html',
         'Phonetic alphabet · Q-codes · RST scale · ICS structure · HF calling frequencies.'],
        ['Position Checklists',   '/position_checklists.html',
         'NIMS activation checklists for IC, SOFR, OSC, PSC, LSC, FSC and unit leaders.'],
        ['Reference Library',     '/refs.html',
         'Kiwix offline Wikipedia, WikiMed, iFixit. No internet needed.'],
        ['Pre-Flight Check',      '/preflight.html',
         'GO/CAUTION/NO-GO readiness verdict. Run before every activation.'],
        ['Event Templates',       '/event_templates.html',
         '6 built-in templates (Shelter/SAR/HazMat/Weather/Mass Gathering/Exercise). '
         'Activate → incident pre-loaded with objectives, resources, channels, org.'],
        ['Incident Archive',      '/incident_mgmt.html',
         'Archive to USB · Restore from USB · Hard delete · Beta/Scenario Reset.'],
    ],
    [1.55*inch, 1.15*inch, CW-2.7*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 12 — WAN, NETWORK & ADMIN
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('📶', 'WAN Configuration & Network Reference',
                         'http://192.168.50.1/wan_settings.html', EOC_LT, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['SETTING', 'OPTIONS'],
    [
        ['Role',            'Preferred (used first) · Fallback (used when preferred fails)'],
        ['Type',            'Cellular · Satellite · Hotspot · Fixed broadband · Other'],
        ['Detection',       'internet_only (hotspots/dongles) · ping (gateway IP) · admin_reachable (modem UI)'],
        ['Swap roles',      'Click ⇄ Swap Roles — preferred and fallback swap immediately'],
        ['Enable/disable',  'Toggle a source on or off without deleting its configuration'],
    ],
    [1.3*inch, CW-1.3*inch]))
story.append(SP(6))
story.append(section_hdr('🌐', 'Admin URLs & IP Reference',
                         'http://192.168.50.1/', EOC, EOC_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['DEVICE / SERVICE', 'ADDRESS', 'NOTES'],
    [
        ['FieldCommand dashboard',     'http://192.168.50.1',          'Main entry — all tools'],
        ['WAN status detail',          '/wan-status.html',              'Both sources · last check · event log'],
        ['ICS platform',               'http://192.168.50.1/ics/',      'Five-section ICS structure'],
        ['AMPRNet gateway status',     'http://192.168.50.2',           'Read-only port 9000'],
        ['Primary router admin',       'http://192.168.50.254',         'ASUS RT-BE58 Go · AiMesh · WAN config'],
        ['CUPS printer admin',         'http://192.168.50.1:631',       'Add/manage USB printers'],
        ['Health monitor',             'http://192.168.50.1:5051/health','CPU · disk · service dots · GPS'],
        ['FCC lookup API',             'http://192.168.50.1:5050',      'Port 5050 — callsign, roster, WAN config'],
        ['ICS platform API',           'http://192.168.50.1:5051',      'Port 5051 — forms, T-cards, FEMA, GPS'],
        ['Kiwix library',              'http://192.168.50.1:8080',      'Offline Wikipedia and reference docs'],
        ['AMPRNet gateway',            'http://192.168.50.2',           '44Net status · callsign auth · Part 97 log'],
        ['Planning P cycle',           '/ics/planningp.html',           '15-phase IAP cycle guide with agenda and required forms'],
        ['Starcom resource map',       '/resmap.html',                  'Public safety unit positions — separate from ICS resource map'],
        ['ICS-214 Activity Log',       '/ics214.html',                  'Unit log — export hours directly to FEMA Force Account Labor'],
        ['Meeting scheduler',          '/meetings.html',                'Schedule operational briefings — time, location, attendees'],
        ['Org setup',                  '/setup.html',                   'Configure org name, callsign, grid square, time zone'],
        ['ICS-204A Briefing Sheet',    '/briefing_204a.html',           'Assignment briefing sheet for branch/division supervisors'],
    ],
    [1.9*inch, 1.9*inch, CW-3.8*inch]))
story.append(SP(4))
story.append(ref_tbl(
    ['MESH NODE', 'SWITCH PORT', 'PLACEMENT'],
    [
        ['FieldCommand Pi 5',          'Port 1',  'Primary server — rack or case shelf'],
        ['44Net Gateway Pi 5',         'Port 2',  'AMPRNet gateway — rack or case shelf'],
        ['ASUS RT-BE58 Go (primary)',  'Port 3',  'ICP primary Wi-Fi · AiMesh controller'],
        ['RT-BE58 Go (node 1)',        'Port 4',  'Coverage extension — second room or floor'],
        ['RT-BE58 Go (node 2)',        'Port 5',  'Coverage extension — outdoor or staging'],
    ],
    [1.9*inch, 0.9*inch, CW-2.8*inch]))
story.append(PB())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE 13 — TROUBLESHOOTING
# ══════════════════════════════════════════════════════════════════════════════
story.append(section_hdr('🛠', 'Troubleshooting',
                         'http://192.168.50.1/', RED, RED_BG))
story.append(SP(4))
story.append(ref_tbl(
    ['SYMPTOM', 'LIKELY CAUSE', 'FIX'],
    [
        ['Cannot reach 192.168.50.1',
         'Not on EMCOMM-NET Wi-Fi',
         'Check Wi-Fi — must show EMCOMM-NET. Some devices auto-switch networks.'],
        ['Page loads but tools error',
         'API server not running',
         'SSH to Pi: sudo systemctl restart fieldcommand-main fieldcommand-fcc'],
        ['Callsign lookup fails',
         'FCC database missing or callsign not US licensed',
         'Run: sudo python3 /opt/fieldcommand/scripts/build_fcc_db.py'],
        ['APRS map shows no stations',
         'No RF or APRS-IS unavailable',
         'Check TNC/direwolf connection. WAN needed for APRS-IS feed.'],
        ['Radar shows offline',
         'No internet connection',
         'Red WAN indicator means no radar tiles. All other tools still work.'],
        ['QR scan not working',
         'Browser does not support BarcodeDetector',
         'Use Chrome or Edge. Use manual ID entry on Firefox/Safari.'],
        ['IAP PDF takes too long',
         'Many forms or large signatures',
         'Normal 5–20 sec. If over 60 sec check server health at :5051/health.'],
        ['WAN shows red but internet works',
         'Detection method misconfigured',
         'Go to wan_settings.html. Change detection to internet_only.'],
        ['T-card personnel not saving',
         'No active incident selected',
         'Confirm incident is active at incident.html before adding personnel.'],
        ['Gateway Pi unreachable',
         'Gateway Pi off or not on switch',
         'Check gateway Pi power (green LED). Confirm connected to UniFi switch.'],
        ['PAR shows wrong count',
         'Personnel checked in without ICS-211',
         'Run Cross-Reference tab on accountability.html to find gaps.'],
    ],
    [1.55*inch, 1.85*inch, CW-3.4*inch]))
story.append(SP(4))
story.append(tip(
    'For any issue not covered here — open the Health Monitor at '
    'http://192.168.50.1:5051/health or check the service log: '
    'journalctl -u fieldcommand-main -n 50',
    RED, RED_BG))
story.append(PB())


out = '/mnt/user-data/outputs/FieldCommand_Field_Quick_Reference.pdf'
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=M, rightMargin=M,
    topMargin=0.58*inch, bottomMargin=0.40*inch,
    title='FieldCommand IMS v1.0 — Field Quick-Reference',
    author='James Rospopo KE4CON — Open-Source Field-Deployable ICS Platform')
doc.build(story, canvasmaker=NC)

from pypdf import PdfReader, PdfWriter
import io

# Append the Pi 500 addendum if it exists
addendum = '/home/claude/pi500_addendum.pdf'
import os
if os.path.exists(addendum):
    base = PdfReader(out)
    add  = PdfReader(addendum)
    w = PdfWriter()
    for p in base.pages: w.add_page(p)
    for p in add.pages:  w.add_page(p)
    buf = io.BytesIO()
    w.write(buf)
    with open(out, 'wb') as f: f.write(buf.getvalue())

r = PdfReader(out)
print(f'BUILT: {out}')
print(f'Pages: {len(r.pages)}')
