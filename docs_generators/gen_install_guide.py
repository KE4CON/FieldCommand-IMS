#!/usr/bin/env python3
"""
gen_install_guide.py — FieldCommand Installation Guide Generator
Complete installation guide covering hardware, software, configuration, and reference.
Output: /mnt/user-data/outputs/FieldCommand_Installation_Guide.pdf
"""
import datetime, io, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, KeepTogether)
from reportlab.pdfgen import canvas

# ── Palette ──────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
EOC_BG = HexColor('#eef2f7')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
LGRAY  = HexColor('#f0f3f6')
MGRAY  = HexColor('#e0e8f0')
GREEN  = HexColor('#1a7a3a')
AMBER  = HexColor('#c8760a')
AMBER_BG = HexColor('#fef3d8')
RED    = HexColor('#b82020')
PURPLE = HexColor('#5b2d8c')
MUTED  = HexColor('#4a6080')

ORG    = 'FieldCommand IMS'
SHORT  = 'FieldCommand IMS v1.0'
TODAY  = datetime.date.today().strftime('%B %d, %Y')
PAGE_W, PAGE_H = letter
M  = 0.65*inch
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
                self._draw_chrome(n, total)
            super().showPage()
        super().save()

    def _draw_cover(self):
        """Full-page cover drawn directly on canvas."""
        # Full-page deep navy background
        self.setFillColor(EOC)
        self.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

        # Gold accent stripe at top
        self.setFillColor(GOLD)
        self.rect(0, PAGE_H - 0.18*inch, PAGE_W, 0.18*inch, fill=1, stroke=0)

        # Gold accent stripe at bottom
        self.setFillColor(GOLD)
        self.rect(0, 0, PAGE_W, 0.18*inch, fill=1, stroke=0)

        # Subtle mid-tone band behind the title area
        self.setFillColor(HexColor('#1e4480'))
        self.rect(0, PAGE_H*0.38, PAGE_W, PAGE_H*0.36, fill=1, stroke=0)

        # ── Org / callsign header ──────────────────────────────────────────────
        self.setFillColor(GOLD)
        self.setFont('Helvetica-Bold', 10)
        self.drawCentredString(PAGE_W/2, PAGE_H - 0.70*inch,
            'FieldCommand Incident Management System')
        self.setFillColor(HexColor('#c0d4f0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H - 0.88*inch,
            'Open-Source · Offline-First · Field-Deployable')

        # ── FIELDCOMMAND main title ──────────────────────────────────────────────
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 58)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.60, 'FIELDCOMMAND')

        # ── Subtitle ──────────────────────────────────────────────────────────
        self.setFillColor(GOLD)
        self.setFont('Helvetica-Bold', 15)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.545,
            'Incident Management System  v1.0')

        # ── Gold rule ─────────────────────────────────────────────────────────
        self.setStrokeColor(GOLD)
        self.setLineWidth(1.5)
        self.line(M*2, PAGE_H*0.505, PAGE_W - M*2, PAGE_H*0.505)

        # ── Document type ─────────────────────────────────────────────────────
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 28)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.445, 'INSTALLATION GUIDE')

        # ── Hardware subtitle ──────────────────────────────────────────────────
        self.setFillColor(HexColor('#8090c0'))
        self.setFont('Helvetica', 9.5)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.30,
            'ASUS RT-BE58 Go  ·  UniFi Switch Flex 2.5G  ·  Raspberry Pi 5  ·  Pironman MAX 5')

        # ── Affiliation line ───────────────────────────────────────────────────
        self.setFillColor(HexColor('#6070a0'))
        self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W/2, PAGE_H*0.25,
            f'ICS/NIMS All-Hazards  ·  Amateur Radio EMCOMM  ·  {TODAY}')

        # ── Bottom footer ──────────────────────────────────────────────────────
        self.setFillColor(EOC)
        self.setFont('Helvetica', 7)
        self.drawCentredString(PAGE_W/2, 0.05*inch,
            f'FieldCommand IMS v1.0  ·  {ORG}  ·  {TODAY}')

    def _draw_chrome(self, n, total):
        """Header and footer for pages 2+."""
        # Header
        self.setFillColor(EOC)
        self.rect(0, PAGE_H-0.40*inch, PAGE_W, 0.40*inch, fill=1, stroke=0)
        self.setFillColor(GOLD)
        self.rect(0, PAGE_H-0.42*inch, PAGE_W, 0.02*inch, fill=1, stroke=0)
        self.setFillColor(white)
        self.setFont('Helvetica-Bold', 8)
        self.drawString(M, PAGE_H-0.22*inch, 'FieldCommand IMS v1.0')
        self.setFont('Helvetica', 7.5)
        self.drawRightString(PAGE_W-M, PAGE_H-0.22*inch, 'Installation Guide')
        # Footer
        self.setFillColor(EOC)
        self.rect(0, 0, PAGE_W, 0.32*inch, fill=1, stroke=0)
        self.setFillColor(GOLD)
        self.rect(0, 0.32*inch, PAGE_W, 0.015*inch, fill=1, stroke=0)
        self.setFillColor(white)
        self.setFont('Helvetica', 6.5)
        self.drawString(M, 0.11*inch,
            f'© 2026 James Rospopo KE4CON  ·  CC BY-SA 4.0  ·  creativecommons.org/licenses/by-sa/4.0')
        self.drawRightString(PAGE_W-M, 0.11*inch, f'Page {n} of {total}')

# ── Style helpers ─────────────────────────────────────────────────────────────
def S(name, **kw):
    d = dict(fontName='Helvetica', fontSize=9, textColor=black,
             leading=12, spaceAfter=0, spaceBefore=0)
    d.update(kw)
    return ParagraphStyle(name, **d)

def P(t, s=None):  return Paragraph(t, s or S('b'))
def SP(n=4):       return Spacer(1, n)
def PB():          return PageBreak()
def HR(c=LINE, t=0.4):
    return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=2, spaceAfter=2)

def H1(t): return P(t, S('h1', fontName='Helvetica-Bold', fontSize=14,
                           textColor=EOC, leading=18, spaceBefore=8, spaceAfter=4))
def H2(t): return P(t, S('h2', fontName='Helvetica-Bold', fontSize=11,
                           textColor=EOC_LT, leading=14, spaceBefore=6, spaceAfter=3))
def H3(t): return P(t, S('h3', fontName='Helvetica-Bold', fontSize=9.5,
                           textColor=EOC, leading=13, spaceBefore=4, spaceAfter=2))

def tbl(headers, rows, widths, hbg=EOC, extra_style=None):
    data = [[P(str(h), S('TH', fontName='Helvetica-Bold', fontSize=8,
                           textColor=white, leading=10, spaceAfter=0))\
             for h in headers]]
    for row in rows:
        data.append([P(str(c), S('TC', fontSize=8.5, leading=12, spaceAfter=0))\
                     for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ('BACKGROUND',    (0,0), (-1,0),  hbg),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7),
        ('RIGHTPADDING',  (0,0), (-1,-1), 7),
        ('WORDWRAP',      (0,0), (-1,-1), 'CJK'),
    ]
    if extra_style:
        style.extend(extra_style)
    t.setStyle(TableStyle(style))
    return t

def CodeBlock(lines):
    """Each line is a separate row — no text wrapping, no run-on lines."""
    CS = S('cs', fontName='Courier', fontSize=7.5, leading=10.5,
            textColor=HexColor('#1a1a2e'), spaceAfter=0, spaceBefore=0)
    rows = [[P(line if line.strip() else '\xa0', CS)] for line in lines]
    t = Table(rows, colWidths=[CW - 0.28*inch])
    style = [
        ('BACKGROUND',    (0,0), (-1,-1), LGRAY),
        ('LEFTPADDING',   (0,0), (-1,-1), 10),
        ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('TOPPADDING',    (0,0), (-1,-1), 1),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ('TOPPADDING',    (0,0), (0,0),   5),
        ('BOTTOMPADDING', (-1,-1), (-1,-1), 5),
        ('BOX',           (0,0), (-1,-1), 0.5, EOC_LT),
    ]
    t.setStyle(TableStyle(style))
    # Wrap in outer table with left accent bar
    outer = Table([[
        Table([['']], colWidths=[0.18*inch]),
        t,
    ]], colWidths=[0.18*inch, CW - 0.18*inch])
    outer.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), EOC_LT),
        ('LEFTPADDING',   (0,0), (-1,-1), 0),
        ('RIGHTPADDING',  (0,0), (-1,-1), 0),
        ('TOPPADDING',    (0,0), (-1,-1), 0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
    ]))
    return outer

def NoteBox(text, kind='note'):
    cfg = {'note': (EOC_LT, EOC_BG, '📝'), 'tip': (GREEN, HexColor('#e4f5ea'), '💡'),
           'warn': (AMBER, AMBER_BG, '⚠'), 'warning': (AMBER, AMBER_BG, '⚠')}
    c, bg, icon = cfg.get(kind, cfg['note'])
    t = Table([[
        P(icon, S('ni', fontSize=11, textColor=c, leading=13)),
        P(text, S('nt', fontSize=8.5, leading=12)),
    ]], colWidths=[0.28*inch, CW-0.28*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',  (0,0), (-1,-1), bg),
        ('LEFTPADDING', (0,0), (-1,-1), 8), ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING',  (0,0), (-1,-1), 5), ('BOTTOMPADDING',(0,0), (-1,-1), 5),
        ('VALIGN',      (0,0), (-1,-1), 'MIDDLE'),
        ('LINEAFTER',   (0,0), (0,-1),  2, c),
    ]))
    return t

def StepBox(num, title):
    t = Table([[
        P(str(num), S('sn', fontName='Helvetica-Bold', fontSize=22,
                       textColor=white, leading=26, alignment=TA_CENTER)),
        P(title, S('st', fontName='Helvetica-Bold', fontSize=13,
                    textColor=white, leading=17)),
    ]], colWidths=[0.55*inch, CW-0.55*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (0,-1), EOC_LT),
        ('BACKGROUND',    (1,0), (1,-1), EOC),
        ('TOPPADDING',    (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING',   (0,0), (-1,-1), 10), ('RIGHTPADDING',  (0,0), (-1,-1), 10),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW',     (0,0), (-1,-1), 2, GOLD),
    ]))
    return t

def steps(items):
    data = [[
        P('STEP', S('sh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=9)),
        P('ACTION', S('sh', fontName='Helvetica-Bold', fontSize=7.5, textColor=white, leading=9)),
    ]]
    for i, item in enumerate(items, 1):
        data.append([
            P(str(i), S('sn2', fontName='Helvetica-Bold', fontSize=9,
                          textColor=EOC_LT, alignment=TA_CENTER, leading=11)),
            P(item, S('sa', fontSize=8.5, leading=12)),
        ])
    t = Table(data, colWidths=[0.38*inch, CW-0.38*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 4), ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING',   (0,0), (-1,-1), 6), ('RIGHTPADDING',  (0,0), (-1,-1), 6),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
    ]))
    return t

def make_table_style(ncols):
    return TableStyle([
        ('BACKGROUND',    (0,0), (-1,0),  EOC),
        ('TEXTCOLOR',     (0,0), (-1,0),  white),
        ('FONTNAME',      (0,0), (-1,0),  'Helvetica-Bold'),
        ('FONTSIZE',      (0,0), (-1,-1), 8.5),
        ('FONTSIZE',      (0,0), (-1,0),  8.0),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [white, LGRAY]),
        ('GRID',          (0,0), (-1,-1), 0.3, LINE),
        ('VALIGN',        (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING',    (0,0), (-1,-1), 5), ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING',   (0,0), (-1,-1), 7), ('RIGHTPADDING',  (0,0), (-1,-1), 7),
    ])

def ref_tbl_2col(headers, rows, widths):
    data = [[P(str(h), S('TH', fontName='Helvetica-Bold', fontSize=8.5,
                           textColor=white, leading=11)) for h in headers]]
    for row in rows:
        data.append([P(str(c), S('TC', fontSize=8.5, leading=12, spaceAfter=0))
                     for c in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(make_table_style(2))
    return t

# ══════════════════════════════════════════════════════════════════════════════
story = []

# ── COVER ─────────────────────────────────────────────────────────────────────
# Cover drawn by NC._draw_cover() — page 1 is blank in the story
story.append(PB())

# ── TABLE OF CONTENTS ─────────────────────────────────────────────────────────
story.append(H1('Table of Contents'))
story.append(HR(GOLD, 1.0))
story.append(SP(8))

TOC = [
    ('1.', 'Overview & What\'s Included', '3'),
    ('2.', 'Hardware Requirements', '4'),
    ('3.', 'Before You Begin — Prerequisites', '11'),
    ('4.', 'Step 1: Network Hardware Setup', '13'),
    ('5.', 'Step 2: Download & Run the Installer', '16'),
    ('6.', 'Step 3: Installer Configuration Options', '19'),
    ('7.', 'Step 4: Raspberry Pi 5 — Static IP Configuration', '20'),
    ('7b.', 'Step 4b: RAID 1 NVMe Setup — Pironman MAX 5', '22'),
    ('8.', 'Step 5: Kiwix Offline Library Setup', '24'),
    ('9.', 'Step 6: FCC Amateur Database', '26'),
    ('10.', 'Step 7: APRS Setup (Graywolf + YAAC)', '27'),
    ('11.', 'Step 8: Printer Setup', '31'),
    ('12.', 'Step 9: Pat Winlink — Verify & Configure', '36'),
    ('12.', 'Step 10: Windows Laptop — Winlink Express + JS8Call', '37'),
    ('13.', 'Step 11: First Boot Verification', '41'),
    ('14.', 'Network Architecture Reference', '43'),
    ('14.', 'Web Dashboard Reference', '45'),
    ('14.', 'Service & Port Reference', '46'),
    ('15.', 'Maintenance & Updates', '47'),
    ('16.', 'Troubleshooting', '48'),
    ('17.', 'Quick Reference Card', '50'),
]
for num, title, pg in TOC:
    row = Table([[
        P(num, S('tn', fontName='Helvetica-Bold', fontSize=8.5,
                  textColor=EOC_LT, alignment=TA_CENTER, leading=11)),
        P(title, S('tt', fontSize=8.5, leading=11)),
        P(pg, S('tp', fontSize=8.5, leading=11, alignment=TA_CENTER)),
    ]], colWidths=[0.4*inch, CW-0.8*inch, 0.4*inch])
    row.setStyle(TableStyle([
        ('LINEBELOW',     (0,0), (-1,-1), 0.2, LINE),
        ('TOPPADDING',    (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('LEFTPADDING',   (0,0), (-1,-1), 4), ('RIGHTPADDING',  (0,0), (-1,-1), 4),
        ('VALIGN',        (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(row)
story.append(PB())

# ── SECTION 1 — OVERVIEW ──────────────────────────────────────────────────────
story.append(H1('1. Overview & What\'s Included'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P(
    'FieldCommand is a complete off-grid emergency communications server built on two Raspberry Pi 5 units '
    '— one running all 32 EmComm tools, one dedicated to the AMPRNet / 44Net gateway. '
    'A cellular modem is the primary WAN source with a satellite dish '
    'as automatic failover, both managed by the ASUS RT-BE58 Go Wi-Fi 7 router. '
    'Two additional ASUS RT-BE58 Go routers extend EMCOMM-NET as AiMesh nodes for large venues. '
    'Any phone, tablet, or laptop connects to EMCOMM-NET and reaches all tools at '
    'http://192.168.50.1 — no internet, no app, no per-device setup required. '
    'When WAN is available, NWS alerts, APRS-IS, and HF propagation data activate automatically.',
    S('body', fontSize=9.5, leading=14, alignment=TA_JUSTIFY)))
story.append(SP(8))
story.append(NoteBox(
    'SAR Network Operations:  The Starcom Net Logger includes a dedicated SAR Net mode '
    '(Search & Rescue) accessible directly from the Starcom / Public Safety dashboard. '
    'It provides a SAR-specific check-in log with unit type tracking, zone assignments, '
    'and resource status.  The Starcom Resource Map provides the tactical overlay for SAR unit positions.  '
    'These features are integrated into the main FieldCommand platform — no separate module is required.',
    'note'))
story.append(SP(6))
story.append(tbl(['COMPONENT', 'DESCRIPTION', 'COMPONENT', 'DESCRIPTION'], [
    ['30 Web Pages', 'Full dashboard, net logs, ICS forms, maps, roster, cheat sheets',
     'Dead Man\'s Switch', 'Per-net inactivity monitor with warning and trigger states'],
    ['Net Control Logger', 'Amateur + Starcom nets, FCC autofill, ICS-309 export',
     'Pre-Flight Checklist', 'GO/CAUTION/NO-GO deployment readiness check'],
    ['ICS Platform', 'Command, Operations, Planning, Logistics, Finance sections',
     'HF Propagation', 'Solar indices, band conditions, A/K-index'],
    ['APRS Tactical Map', 'Graywolf + YAAC merged, offline tiles, overlays',
     'Repeater Database', 'RepeaterBook CSV, filter by band, mode, ARES affiliation'],
    ['Member Roster', 'your organization directory with certs, equipment, activations',
     'Reference Library', 'Upload and serve field reference docs across EMCOMM-NET'],
    ['NTS Radiogram', 'ARRL-formatted radiogram generator with traffic log',
     'Kiwix Library', 'WikiMed, Wikipedia, iFixit — offline at port 8081'],
    ['ICS-213/214/309', 'Fillable ICS forms with print output and incident archiving',
     'FCC Callsign Lookup', '~800K licensees — instant offline search'],
    ['Winlink Form Import', 'Import Winlink Express XML forms to incident archive',
     'Pat Winlink', 'Browser-based backup Winlink client at port 8090'],
    ['JS8Call Integration', 'Dashboard card opens JS8Call web API on Windows laptop',
     'ICS Planning P', 'Interactive 15-phase planning cycle guide'],
], [1.2*inch, 1.8*inch, 1.4*inch, CW-4.4*inch],
   extra_style=[('LINEAFTER', (1,0), (1,-1), 1.5, EOC_LT)]))
story.append(PB())

# ── SECTION 2 — HARDWARE REQUIREMENTS ────────────────────────────────────────
story.append(H1('2. Hardware Requirements'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(H2('Supported Hardware — Raspberry Pi Servers'))
story.append(P(
    'FieldCommand v1.0 uses two Raspberry Pi 5 units: one as the FieldCommand application server '
    'and one as the dedicated AMPRNet / 44Net gateway. '
    'Keeping them separate means the gateway can be rebooted, reconfigured, or upgraded '
    'without affecting the FieldCommand server, net logs, or active incidents.'))
story.append(SP(4))
story.append(tbl(['UNIT', 'HARDWARE', 'STORAGE', 'ROLE'], [
    ['FieldCommand Server',
     'Raspberry Pi 5  —  16 GB RAM  /  Pironman MAX 5 tower enclosure  (dual M.2 NVMe, OLED, active cooling)',
     '2× 1 TB NVMe SSD  /  configured as RAID 1',
     'Runs all FieldCommand services: web server, FCC database, net logging, ICS platform, '
     'APRS, Kiwix, Winlink, maps, and health monitor.  Static IP: 192.168.50.1'],
    ['44Net Gateway',
     'Raspberry Pi 5  —  16 GB RAM  /  Argon NEO 5 M.2 BRED case  (compact, passive-cooled, M.2 SATA slot)  /  Pi OS Desktop (64-bit)',
     '256 GB M.2 SATA SSD  (OS + WireGuard + routing + status service)',
     'Dedicated AMPRNet / 44Net gateway.  Runs WireGuard tunnel to amprgw.ampr.org, '
     'ip routing between EMCOMM-NET and 44.0.0.0/8, and a status page at 192.168.50.2.  '
     'Completely independent from the FieldCommand server.'],
    ], [1.4*inch, 1.8*inch, 1.5*inch, CW-4.7*inch]))
story.append(SP(6))
story.append(H2('Network Hardware'))
story.append(P(
    'Wi-Fi is provided by the ASUS RT-BE58 Go travel router — neither Pi runs a Wi-Fi hotspot. '
    'The UniFi Switch Lite 16 PoE provides 16 wired gigabit ports for both Pi servers, '
    'the Windows laptop, four operator workstations, a network printer, and room for expansion. '
    'This replaces the original 5-port Flex 2.5G which is too small for the full deployment.'))
story.append(SP(4))
story.append(tbl(['DEVICE', 'ROLE', 'NOTES'], [
    ['ASUS RT-BE58 Go',
     'Wi-Fi 7 access point  /  DHCP server  /  WAN gateway',
     'Dual-band Wi-Fi 7 (802.11be).  2.5G LAN uplink to switch.  USB-C 18W power.  '
     'Handles EMCOMM-NET Wi-Fi, DHCP for 192.168.50.100-200, and optional WAN routing.'],
    ['UniFi Switch Lite 16 PoE',
     '16-port gigabit managed switch  /  8x PoE + 8x non-PoE  /  2x 1G SFP uplink',
     'Replaces the 5-port Flex 2.5G.  Port layout: 1=ASUS router uplink, '
     '2=FieldCommand Pi, 3=44Net Gateway Pi, 4=Windows laptop, '
     '5=color MFP printer, 6-9=Pi 500 workstations, 10=Satellite dish (optional), 11-16=spare.  '
     '~$200.  PoE powers future UniFi APs without a separate injector.'],
        ], [1.6*inch, 1.8*inch, CW-3.4*inch]))
story.append(SP(8))
story.append(H2('Accessories & Cables'))
acc_data = [
    ['ITEM', 'REQUIRED?', 'PURPOSE'],
    ['USB-A drive (32 GB+, labeled FIELDCOMMAND)', 'Recommended',
     'Auto-backup trigger — insert to back up all runtime data instantly'],
    ['External USB hard drive 1 TB+ (e.g. LaCie Rugged or LaCie Mobile Drive)', 'Recommended',
     'Incident archive and full system backup. LaCie Rugged is shock/drop/crush resistant. '
     'Label FIELDCOMMAND for auto-backup compatibility.'],
    ['USB GPS receiver (u-blox or GlobalSat)', 'Optional',
     'Live position for tactical map and NWS alerts'],
    ['USB TNC — Digirig Mobile or SignaLink USB', 'Optional',
     'Required for APRS transmit/receive via Graywolf or YAAC. '
     'FieldCommand assigns a stable /dev/tnc0 device name via udev.'],
    ['Powered USB hub (4- or 7-port, with power supply)', 'Optional',
     'Recommended if connecting GPS + TNC + backup drive simultaneously. '
     'Must be powered — unpowered hubs can cause instability.'],
    ['USB Printer (e.g. Brother HL-L2350DW, HP LaserJet)', 'Optional',
     'Shared across EMCOMM-NET via CUPS (installed automatically). '
     'Or connect a Wi-Fi printer directly to EMCOMM-NET.'],
]
acc_table = Table([[P(c, S('TH' if i==0 else 'TC',
                            fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                            fontSize=8, textColor=white if i==0 else black, leading=11))
                    for c in row] for i, row in enumerate(acc_data)],
                   colWidths=[2.3*inch, 1.0*inch, CW-3.3*inch])
acc_table.setStyle(make_table_style(3))
story.append(acc_table)
story.append(SP(8))

# USB Hub section
story.append(H2('USB Hub & Multi-Device Setup'))
story.append(P('The Pi 5 has four USB ports. A powered USB hub lets you connect GPS, TNC, backup drive, '
               'and other peripherals simultaneously. FieldCommand uses udev rules to assign stable device '
               'names regardless of hub port or plug order.'))
story.append(SP(4))
hub_data = [['DEVICE', 'STABLE NAME', 'HOW ASSIGNED', 'SERVICE'],
    ['USB GPS receiver', '/dev/gps0', 'udev rule matches by USB vendor/product ID', 'gpsd → tactical map'],
    ['Digirig Mobile TNC', '/dev/tnc0\n/dev/digirig',
     'udev rule matches by vendor ID + product string "Digirig Mobile". Distinguished from GPS even though both use CP2102 chip.',
     'YAAC / Graywolf APRS'],
    ['SignaLink USB TNC', '/dev/tnc0\n/dev/signalink',
     'udev rule matches by Texas Instruments PCM2904 chip. No conflict with GPS.',
     'YAAC / Graywolf APRS'],
    ['LaCie / USB backup drive (labeled FIELDCOMMAND)', '/dev/sdX (auto-mounted)',
     'udev backup rule triggers on label FIELDCOMMAND. Drive letter assigned dynamically.',
     'fieldcommand-backup@.service'],
]
hub_t = Table([[P(c, S('TH' if i==0 else 'TC',
                        fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                        fontSize=8, textColor=white if i==0 else black, leading=11))
                for c in row] for i, row in enumerate(hub_data)],
               colWidths=[1.5*inch, 1.0*inch, 2.2*inch, CW-4.7*inch])
hub_t.setStyle(make_table_style(4))
story.append(hub_t)
story.append(SP(6))
story.append(NoteBox(
    'Both the Digirig Mobile TNC and GlobalSat BU-353-S4 GPS use the same USB chip '
    '(Silicon Labs CP2102, vendor 10c4:ea60). FieldCommand distinguishes them by USB product '
    'description string. The GPS rule excludes Digirig; the TNC rule requires the Digirig '
    'product string. Verify with: udevadm info -a -n /dev/ttyUSB0 | grep -E "idVendor|idProduct|product"',
    'note'))
story.append(SP(6))
story.append(CodeBlock([
    '# List all USB serial devices',
    'ls -la /dev/ttyUSB* /dev/ttyACM* 2>/dev/null',
    '# Check the stable symlinks',
    'ls -la /dev/gps0 /dev/tnc0 2>/dev/null',
    '# Confirm GPS is outputting NMEA sentences',
    'sudo cat /dev/gps0',
    '# Use /dev/tnc0 in YAAC → Configure → Ports → Serial TNC',
]))
story.append(SP(8))

# Complete BOM
story.append(H2('Complete Bill of Materials'))
story.append(SP(4))
bom_data = [['ITEM', 'MODEL / SPEC', 'WHERE TO BUY']]

def cat_row(title):
    return [P(f'<b>— {title} —</b>',
              S('cat', fontName='Helvetica-Bold', fontSize=8.5, textColor=EOC_LT)),
            P('', S('TC')), P('', S('TC'))]

bom_rows = [
    cat_row('FieldCommand Server  (Pi 5 — 16 GB)'),
    ['Raspberry Pi 5  —  16 GB RAM', 'Raspberry Pi 5 Model B  (16 GB)  —  note: DRAM shortage pricing, ~$305 as of mid-2026 (was $120)', 'raspberrypi.com · Adafruit · PiShop.us  (~$305)'],
    ['Pironman MAX 5 enclosure', 'Pironman MAX 5  (tower, dual M.2 NVMe, OLED display, active cooling fans)', '52pi.com · Amazon'],
    ['NVMe SSD × 2  (RAID 1)', '1 TB M.2 2280 PCIe Gen 3/4 NVMe  (e.g. WD Blue SN580 or Samsung 980)  —  NAND shortage pricing ~$180 each as of mid-2026 (was ~$75)', 'Amazon · B&H · Newegg  (~$180 each)'],
    ['Pi 5 USB-C power supply', 'Official Raspberry Pi 27W USB-C PD power supply', 'raspberrypi.com · Adafruit · Amazon'],
    ['MicroSD card  (boot / initial RAID setup)', '32 GB Class 10 / A1 microSD  (removed after RAID is built)', 'Amazon'],
    cat_row('44Net Gateway  (Pi 5 — 8 GB)'),
    ['Raspberry Pi 5  —  16 GB RAM', 'Raspberry Pi 5 Model B  (16 GB)  —  dedicated AMPRNet gateway  (matches FieldCommand Pi for spare-parts commonality)  —  8 GB variant (~$130) acceptable for gateway-only role', 'raspberrypi.com · Adafruit · PiShop.us  (~$305)'],
    ['Argon NEO 5 M.2 BRED case', 'Argon NEO 5 M.2 BRED  (compact, passive-cooled, M.2 SATA slot, aluminum)  —  fits Pi 5', 'argon40.com · Amazon  (~$35)'],
    ['M.2 SATA SSD  (gateway OS + config)', '256 GB M.2 2242 or 2280 SATA SSD  —  OS, WireGuard config, routing tables', 'Amazon · Newegg  (~$25)'],
    ['Pi 5 USB-C power supply', 'Official Raspberry Pi 27W USB-C PD power supply  —  one per Pi', 'raspberrypi.com · Adafruit · Amazon'],
    cat_row('Networking  (upgraded from 5-port to 16-port)'),
    ['ASUS RT-BE58 Go travel router', 'ASUS RT-BE58 Go  (Wi-Fi 7, 2.5G LAN uplink, USB-C 18W power)', 'Amazon · Best Buy · B&H'],
    ['UniFi Switch Lite 16 PoE', 'Ubiquiti USW-Lite-16-PoE  (16-port GbE, 8× PoE, 2× SFP uplink, 45W)  —  replaces Flex 2.5G-5', 'ui.com · Amazon · B&H  (~$200)'],
    ['CAT 6 Ethernet cables × 10', '1 ft – 6 ft CAT 6 patch cables  —  router to switch, both Pis, laptop, printer, 4× workstations', 'Amazon · Monoprice'],
    cat_row('Accessories — Backup & Connectivity'),
    ['USB-A drive (32 GB+, labeled FIELDCOMMAND)', '32 GB+ USB 3.0 drive — auto-backup trigger when inserted', 'Amazon'],
    ['External USB hard drive 1 TB+  (e.g. LaCie Rugged)', '1 TB+ USB 3.0/USB-C portable drive — label FIELDCOMMAND for auto-backup', 'B&H · Amazon · Best Buy'],
    ['USB GPS receiver  (optional)', 'GlobalSat BU-353-S4 or u-blox USB GPS puck — provides live position to tactical map and NWS alerts', 'Amazon'],
    ['Powered USB hub  (optional)', 'Anker 7-Port USB 3.0 with AC power adapter — must be powered hub, not bus-powered', 'Amazon · Best Buy'],
    ['Avery 5371 business card sheets  (operator access cards)', 'Avery 5371 — 10 cards per sheet, laser or inkjet — for printed operator access cards', 'Office Depot · Amazon · Staples'],
    cat_row('Printers — Monochrome Laser  (USB via CUPS or direct Wi-Fi)'),
    ['Brother HL-L2350DW  (recommended)', 'Monochrome laser — USB + Wi-Fi — excellent Linux driver — fast, duplex, durable', 'Best Buy · Amazon  (~$130)'],
    ['HP LaserJet Pro M15w  /  P1102w', 'Monochrome laser — USB + Wi-Fi — HPLIP driver auto-installs with CUPS', 'Best Buy · Amazon  (~$150)'],
    cat_row('Printers — Color Multifunction Laser  (USB, Wi-Fi, or Ethernet)'),
    ['Brother MFC-L3770CDW', 'Color laser MFP — print, scan, copy, fax — USB + Wi-Fi + Ethernet — full Linux CUPS support — prints color ICS maps and IAP packages', 'Amazon · Best Buy  (~$400)'],
    ['HP Color LaserJet Pro MFP M479fdw', 'Color laser MFP — print, scan, copy, fax — USB + Wi-Fi + Ethernet — HPLIP driver works out of the box with CUPS', 'Amazon · B&H  (~$500)'],
    ['Canon imageCLASS MF743Cdw', 'Color laser MFP — letter + legal — USB + Wi-Fi + Ethernet — Linux CAPT driver — good for permanent EOC installations', 'Amazon · Office Depot  (~$450)'],
    cat_row('Printers — Portable / Battery-Powered  (field deployments without shore power)'),
    ['Canon PIXMA TR150', 'Compact inkjet — built-in rechargeable battery — ~200 pages per charge — USB + Wi-Fi — letter size', 'Best Buy · Amazon  (~$200)'],
    ['HP OfficeJet 200', 'Portable inkjet — larger paper tray — optional battery accessory — USB + Wi-Fi — good for shelter stations', 'Best Buy · Amazon  (~$180)'],
    cat_row('Operator Workstations — Raspberry Pi 500 / 500+  (qty: 4 recommended)'),
    ['Raspberry Pi 500 keyboard computer  ×4', 'Pi 500 standalone — Pi 5 chip, 8 GB RAM, 32 GB A2 microSD, integrated keyboard — one per operator station', 'raspberrypi.com · Adafruit · Amazon  (~$130 each — DRAM shortage pricing)'],
    ['Raspberry Pi 500+  ×4  (alternative)', 'Pi 500+ — same as Pi 500 but with Pi 5 latest revision chip and 2× USB3 — specify if 501(c)(3) funding allows premium spec', 'raspberrypi.com · Adafruit  (~$410 each — significantly increased by DRAM shortage; standard Pi 500 recommended)'],
    ['Raspberry Pi Monitor 15.6"  ×4', '15.6" Full HD IPS touchscreen — built-in speakers — kickstand — VESA mount — USB-C powered from Pi 500 — one per station', 'raspberrypi.com · GigaParts · Amazon  (~$100 each)'],
    ['micro-HDMI to HDMI cable  ×4', '1m micro-HDMI to standard HDMI — Pi 500 to Monitor video connection — one per station', 'Included in Pi 500 Desktop Kit · Amazon  (~$8 each)'],
    ['USB-C power supply for Pi 500  ×4', 'Official Raspberry Pi 27W USB-C PD supply — one per station — Pi 500 can also be powered from Monitor USB-C port', 'raspberrypi.com · Adafruit  (~$12 each)'],
    ['Raspberry Pi 500 Desktop Kit  ×4  (bundle option)', 'Pi 500 + official mouse + micro-HDMI cable bundled — add Monitor separately — simpler ordering than individual parts', 'raspberrypi.com · Amazon  (~$160 each — DRAM shortage pricing)'],
]
all_bom = [bom_data[0]] + [[r[0], r[1], r[2]] if len(r)==3 else r for r in bom_rows]

# Build the BOM table properly handling both string rows and Paragraph rows (cat_row)
bom_table_data = []
for i, row in enumerate(all_bom):
    if i == 0:
        # Header row
        bom_table_data.append([P(str(c), S('TH', fontName='Helvetica-Bold',
                                             fontSize=8, textColor=white, leading=11))
                                for c in row])
    elif isinstance(row[0], str):
        # Normal data row - convert strings to Paragraphs
        bom_table_data.append([P(str(c), S('TC', fontSize=8.5, leading=12))
                                for c in row])
    else:
        # cat_row - already contains Paragraph objects
        bom_table_data.append(row)

bom_t = Table(bom_table_data, colWidths=[2.2*inch, 2.5*inch, CW-4.7*inch], repeatRows=1)
bom_style = make_table_style(3)
# Add span for category rows
from reportlab.platypus import TableStyle as TS2
for i, row in enumerate(all_bom):
    if i > 0 and not isinstance(row[0], str):
        bom_style.add('SPAN', (0, i), (2, i))
        bom_style.add('BACKGROUND', (0, i), (2, i), HexColor('#dce8f4'))
bom_t.setStyle(bom_style)
story.append(bom_t)
story.append(SP(8))

# Mesh BOM
story.append(H2('EMCOMM-NET Coverage Extension — 2× ASUS RT-BE58 Go Mesh Nodes'))
story.append(P(
    'FieldCommand uses two additional ASUS RT-BE58 Go routers as AiMesh nodes to extend '
    'EMCOMM-NET coverage across large EOC buildings, shelters, and outdoor staging areas. '
    'Using identical hardware for all three routers (primary + 2 nodes) simplifies deployment, '
    'eliminates compatibility issues, and means any unit can serve as the primary router if needed. '
    'All three broadcast the same EMCOMM-NET SSID — operators never know they switched nodes.'))
story.append(SP(6))
mesh_data = [['ITEM', 'MODEL / SPEC', 'WHERE TO BUY'],
    ['ASUS RT-BE58 Go  ×2  (mesh nodes)',
     'ASUS RT-BE58 Go — identical to primary router — '
     'pairs instantly as AiMesh node with no extra configuration — '
     'extends EMCOMM-NET at full Wi-Fi 7 speed — '
     'wired backhaul via UniFi switch ports 11 and 12',
     'Amazon · Best Buy · B&H  (~$120-150 each)'],
    ['USB-C power supply  ×2  (for mesh nodes)',
     'USB-C 18W PD adapter — one per node — '
     'or USB-C power bank (10,000+ mAh, 18W+) for field use without shore power',
     'Amazon  (~$15-25 each)'],
    ['CAT 6 Ethernet cable  ×2  (wired backhaul)',
     'CAT 6 patch cable from UniFi Switch Lite 16 PoE to each node LAN port — '
     'wired backhaul is strongly recommended — provides full throughput vs wireless backhaul — '
     'length as needed for the venue',
     'Amazon · Monoprice · Home Depot  (~$10-20 each)'],
]
mesh_t = Table([[P(c, S('TH' if i==0 else 'TC',
                         fontName='Helvetica-Bold' if i==0 else 'Helvetica',
                         fontSize=8, textColor=white if i==0 else black, leading=11))
                 for c in row] for i, row in enumerate(mesh_data)],
                colWidths=[1.8*inch, 3.0*inch, CW-4.8*inch], repeatRows=1)
mesh_t.setStyle(make_table_style(3))
story.append(mesh_t)
story.append(SP(6))
story.append(ref_tbl_2col(['DEPLOYMENT SCENARIO', 'RECOMMENDED SETUP'], [
    ['Single room EOC  (under 2,500 sq ft)',
     '1× RT-BE58 Go primary only — no extension needed'],
    ['Multi-room EOC or large shelter  (2,500–7,500 sq ft)',
     '1× primary + 1 RT-BE58 Go node  —  wired backhaul via switch Port 11'],
    ['Large building or campus  (7,500–20,000 sq ft)',
     '1× primary + 2 RT-BE58 Go nodes  —  wired backhaul via switch Ports 11 and 12'],
    ['Outdoor SAR staging area',
     '1× primary at command post + 1-2 RT-BE58 Go nodes at field positions on battery'],
], [2.5*inch, CW-2.5*inch]))
story.append(SP(4))
story.append(NoteBox(
    'All three ASUS RT-BE58 Go routers broadcast the same EMCOMM-NET SSID and password. '
    'Operators and devices roam between them automatically — no reconnection, '
    'no password re-entry, no awareness of which router they are connected to. '
    'Pairing a new node to the primary takes under 5 minutes on site.',
    'tip'))
story.append(SP(8))

# SD card sizing
story.append(H2('SD Card / Storage Sizing Guide'))
story.append(ref_tbl_2col(['TIER', 'WHAT FITS / REQUIREMENT'], [
    ['Minimum (boot only)', '8 GB — OS only, RAID boot loader. FieldCommand runs from NVMe RAID.'],
    ['Recommended', '32 GB — OS + swap + logs + temp files during initial RAID setup.'],
    ['Kiwix Tier 1', '~3 GB additional on RAID — WikiMed + Wikipedia Mini + Wikivoyage.'],
    ['Kiwix Tier 2', '~10 GB additional on RAID — adds iFixit, Wikibooks, Wikiversity.'],
    ['FCC Database', '~600 MB on RAID — full US amateur license database (~800K records).'],
], [1.2*inch, CW-1.2*inch]))
story.append(PB())

# ── SECTION 3 — PREREQUISITES ────────────────────────────────────────────────
story.append(StepBox(1, 'Flash OS  &  Build RAID 1 — Do This First'))
story.append(SP(8))
story.append(H1('Step 1:  Flash the OS and Build the RAID Array'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'These two tasks must be completed before anything else. '
    'The Raspberry Pi OS must be installed and the RAID 1 array assembled '
    'before the FieldCommand installer runs. '
    'If you are using a single NVMe drive (no RAID), flash the OS to it directly '
    'and skip the RAID build section.'))
story.append(SP(6))
story.append(H2('1A  Flash the Operating System'))
story.append(tbl(['OS EDITION', 'PROS', 'CONS'], [
    ['Raspberry Pi OS Lite (64-bit)  —  Recommended for production',
     'Minimal overhead.  All RAM available to FieldCommand.  Fast boot.  Smaller attack surface.',
     'No local browser or GUI.  All interaction via SSH or via EMCOMM-NET browser on another device.'],
    ['Raspberry Pi OS Desktop (64-bit)  —  Good for setup and troubleshooting',
     'Local browser for testing.  GUI for initial Wi-Fi setup and configuration.  Easier for new users.',
     'More RAM used by desktop environment.  Slightly longer install time.'],
    ['Ubuntu Server 24.04 LTS  —  Also supported',
     'LTS kernel.  Familiar to Linux admins.  Long-term package support.',
     'Some package names differ from Raspberry Pi OS.  Slightly more manual setup.'],
], [1.8*inch, 2.2*inch, CW-4.0*inch]))
story.append(SP(6))
story.append(P('Use <b>Raspberry Pi Imager</b> (download from raspberrypi.com/software) to flash the OS '
               'to either a microSD card (for single-drive setup) or directly to the NVMe SSD '
               '(if not using RAID). During the Imager advanced options, set:'))
story.append(SP(4))
story.append(tbl(['IMAGER OPTION', 'VALUE  /  REASON'], [
    ['Hostname',          'fieldcommand.local  — makes the Pi discoverable as fieldcommand.local on the network'],
    ['Username',          'fieldcommand  — the FieldCommand installer expects this username'],
    ['Password',          'Choose a strong password and record it  —  required for SSH and CUPS admin'],
    ['Enable SSH',        'Yes  —  required for remote access from your laptop during setup'],
    ['Wi-Fi',             'Set your home or lab Wi-Fi during initial OS setup.  EMCOMM-NET comes later.'],
    ['Locale / Timezone', 'US/Central for local operations'],
    ], [2.6*inch, CW-2.6*inch]))
story.append(SP(8))

story.append(H2('1B  Build the RAID 1 Array  (Pironman MAX 5 — Dual NVMe)'))
story.append(P(
    'The Pironman MAX 5 enclosure has two M.2 NVMe slots. '
    'Configuring them as a RAID 1 mirror means both drives always contain identical data. '
    'If one SSD fails, the Pi keeps running on the surviving drive with no data loss '
    'and no operator action required. '
    'Skip this section entirely if you are using a single NVMe drive.'))
story.append(SP(4))
story.append(NoteBox(
    'Complete the RAID build BEFORE running the FieldCommand installer. '
    'The installer must be run on the final storage configuration. '
    'If your OS is already running from a single drive, back it up before proceeding.',
    'warn'))
story.append(SP(6))
story.append(H3('Physical Installation'))
story.append(tbl(['SLOT', 'DRIVE', 'LINUX DEVICE NAME'], [
    ['M.2 Slot 1  (primary)',    '1 TB NVMe SSD  (e.g. WD Blue SN580)',  '/dev/nvme0n1'],
    ['M.2 Slot 2  (mirror)',     '1 TB NVMe SSD  —  identical model recommended',  '/dev/nvme1n1'],
    ], [1.5*inch, 2.8*inch, CW-4.3*inch]))
story.append(SP(6))
story.append(P('Boot from a microSD card with Raspberry Pi OS Lite to perform the initial RAID setup. '
               'After the array is built and the OS copied to it, the SD card is removed.'))
story.append(SP(4))
story.append(H3('Build the Array'))
story.append(CodeBlock([
    '# Install mdadm (RAID management tool)',
    'sudo apt-get update && sudo apt-get install -y mdadm',
    '',
    '# Create the RAID 1 array  (--run skips the "all zeroes" check for speed)',
    'sudo mdadm --create --verbose /dev/md0  \\',
    '    --level=1 --raid-devices=2  \\',
    '    /dev/nvme0n1 /dev/nvme1n1',
    '',
    '# Check build progress  (shows resync percentage — takes ~15 min for 1 TB)',
    'cat /proc/mdstat',
    '',
    '# Create a filesystem on the array',
    'sudo mkfs.ext4 -L fieldcommand-raid /dev/md0',
    '',
    '# Mount and copy the running OS to the RAID array',
    'sudo mkdir -p /mnt/raid',
    'sudo mount /dev/md0 /mnt/raid',
    'sudo apt-get install -y rsync',
    'sudo rsync -axv --progress / /mnt/raid/',
    '',
    '# Save the RAID config so it survives reboots',
    'sudo mdadm --detail --scan | sudo tee -a /mnt/raid/etc/mdadm/mdadm.conf',
    'sudo update-initramfs -u -k all',
    '',
    '# Update /boot/cmdline.txt to boot from the RAID array instead of the SD',
    'sudo nano /boot/cmdline.txt',
    '# Change:  root=PARTUUID=xxxx   →   root=/dev/md0',
    '# Then reboot — Pi boots from RAID.  Verify with:',
    'cat /proc/mdstat',
    '# Expected:  md0 : active raid1 nvme0n1[0] nvme1n1[1]  [UU]',
]))
story.append(SP(6))
story.append(tbl(['RAID STATUS', 'MEANING', 'ACTION REQUIRED'], [
    ['[UU]  (both drives active)',
     'Normal — both drives healthy and in sync',
     'None'],
    ['[U_] or [_U]  (one drive failed)',
     'One drive has failed.  Pi is still running on the other.',
     'Power down.  Replace failed drive.  Run:  sudo mdadm /dev/md0 --add /dev/nvme1n1.  Array rebuilds automatically.'],
    ['Resync in progress',
     'Array is rebuilding — normal after first setup or drive replacement',
     'Leave running.  Takes 15 – 30 minutes.  Pi is usable during rebuild.'],
    ], [1.6*inch, 2.0*inch, CW-3.6*inch]))
story.append(SP(4))
story.append(NoteBox(
    'RAID 1 protects against drive failure — it is NOT a backup. '
    'Both drives contain identical data, so accidental deletion affects both drives simultaneously. '
    'Continue to use the FIELDCOMMAND USB auto-backup for regular data backups.',
    'warn'))
story.append(PB())

story.append(H1('3. Before You Begin — Prerequisites'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P('Complete these prerequisites before running the installer. The installer requires an internet '
               'connection for package downloads, the FCC database, and Kiwix ZIM files. After installation, '
               'the server operates fully offline.'))
story.append(SP(8))
story.append(H2('3.1  Flash the Operating System'))
story.append(tbl(['OS EDITION', 'PROS', 'CONS'], [
    ['Raspberry Pi OS Lite (64-bit) — Recommended for production',
     'Minimal overhead, faster boot, all RAM available to FieldCommand services, smaller attack surface',
     'No local browser or GUI — all interaction via SSH or EMCOMM-NET browser'],
    ['Raspberry Pi OS Desktop (64-bit) — Good for setup and troubleshooting',
     'GUI for initial setup, Raspberry Pi Configuration tool, local browser for testing',
     'More RAM used by desktop environment; install takes longer'],
    ['Ubuntu Server 24.04 LTS — Also supported',
     'LTS kernel, familiar to Linux admins, good for organizations standardized on Ubuntu',
     'Slightly larger memory footprint; some package names differ'],
], [2.0*inch, 2.0*inch, CW-4.0*inch]))
story.append(SP(6))
story.append(H2('3.2  First Boot — Initial Setup'))
story.append(steps([
    'On first boot, complete the initial setup wizard: set username to <b>fieldcommand</b>, set a strong password, configure locale and keyboard, expand filesystem.',
    'If using Desktop edition: complete the initial desktop setup wizard.',
    'Enable SSH (Lite only): run <font face="Courier">sudo raspi-config → Interface Options → SSH → Enable</font>',
]))
story.append(SP(6))
story.append(P('Run a full system update before installing FieldCommand (works the same on both editions — Terminal or SSH):'))
story.append(SP(4))
story.append(CodeBlock([
    '# Update all packages to latest versions',
    'sudo apt-get update && sudo apt-get full-upgrade -y',
    '# Reboot to apply kernel updates',
    'sudo reboot',
]))
story.append(SP(6))
story.append(H2('3.3  Verify Disk Space'))
story.append(CodeBlock([
    '# Check available space — should show 20GB+ free for Tier 2 install',
    'df -h /',
    '# Verify RAM',
    'free -h',
]))
story.append(SP(6))
story.append(H2('3.4  Internet Connection'))
story.append(P(
    'Connect the Pi to the internet via Ethernet before running the installer. '
    'Wi-Fi can be used during initial setup but Ethernet is strongly preferred '
    'for downloading large files — the FCC database is ~600 MB and Kiwix ZIMs '
    'range from 500 MB to 25 GB.'))
story.append(SP(8))

story.append(H2('3.5  Operator Workstation — Browser Options'))
story.append(P(
    'FieldCommand runs entirely in a web browser. '
    'Any modern browser on any device connected to EMCOMM-NET works. '
    'For the Raspberry Pi 500 / 500+ used as an operator workstation, '
    'three browsers are available:'))
story.append(SP(6))
story.append(tbl(['BROWSER', 'HOW TO INSTALL', 'NOTES FOR FIELDCOMMAND'], [
    ['Chromium  (default)',
     'Pre-installed on Raspberry Pi OS.  No action needed.',
     'Best performance for FieldCommand. Discovers CUPS printers automatically via Bonjour. '
     'Set http://192.168.50.1 as the startup page under Settings → On startup.'],
    ['Firefox ESR',
     'sudo apt install firefox-esr',
     'Excellent compatibility with all FieldCommand pages. '
     'Good fallback if Chromium behaves unexpectedly. '
     'Also discovers network printers. Slightly lower memory footprint on the Pi 500.'],
    ['GNOME Web  (Epiphany)',
     'sudo apt install epiphany-browser',
     'Very lightweight WebKit browser. Good for Pi 500 with many tabs open. '
     'Best for dedicated check-in stations where memory is tight.'],
    ], [1.6*inch, 1.8*inch, CW-3.4*inch]))
story.append(SP(6))
story.append(NoteBox(
    'For dedicated FieldCommand operator stations running Pi 500:  '
    'set Chromium to open http://192.168.50.1 on startup. '
    'In Chromium: Settings → On startup → Open a specific page → enter http://192.168.50.1. '
    'The dashboard loads automatically every time the Pi 500 boots.',
    'tip'))
story.append(SP(4))
story.append(NoteBox(
    'Wi-Fi is provided by the ASUS RT-BE58 Go router — the Pi does NOT run hostapd. '
    'During installation, connect the Pi to the internet via Ethernet through the UniFi switch and ASUS router. '
    'After installation, the Pi is always reachable at 192.168.50.1 via wired Ethernet.', 'note'))
story.append(PB())

# ── STEP 1 — NETWORK SETUP ────────────────────────────────────────────────────
story.append(StepBox(2, 'Network Hardware Setup — ASUS Router + UniFi Switch'))
story.append(SP(8))
story.append(H1('Step 2:  Network Hardware Setup — ASUS Router + UniFi Switch'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('Complete this step before running the FieldCommand installer. The ASUS router must be configured '
               'with the correct LAN subnet (192.168.50.x) before FieldCommand is reachable at http://192.168.50.1.'))
story.append(SP(6))
story.append(H2('1.1  Physical Wiring'))
story.append(P(
    'The UniFi Switch Lite 16 PoE is the central wiring hub for the entire EMCOMM-NET deployment. '
    'Connect everything to the switch, and the switch connects up to the ASUS router. '
    'Use short CAT 6 patch cables (1 ft to 3 ft) to keep the rack or case tidy. '
    'The the cellular antenna unit Drum antenna connects directly to the ASUS WAN port via its PoE Ethernet cable '
    '— this is completely separate from the switch and does not use a switch port.'))
story.append(SP(4))
story.append(tbl(['CONNECTION', 'DEVICE', 'IP / NOTES'], [
    ['ASUS WAN port  (PoE Ethernet)',
     'Cellular antenna  (primary WAN)',
     'Primary internet — cellular via your cellular carrier.  '
     'PoE cable from outdoor antenna unit to ASUS WAN port directly.  '
     'the cellular antenna unit serves DHCP on its own subnet — ASUS bridges to EMCOMM-NET.'],
    ['ASUS USB WAN port  (USB-to-Ethernet)',
     'Satellite dish  (secondary WAN)',
     'Secondary internet — satellite.  '
     'satellite Ethernet adapter → USB-to-Ethernet adapter → ASUS USB port.  '
     'ASUS switches automatically when cellular WAN drops.'],
    ['Switch Port 1  (uplink)',
     'ASUS RT-BE58 Go LAN port',
     'Uplink from router to switch.  Router is DHCP server for 192.168.50.0/24.'],
    ['Port 2',
     'FieldCommand Pi 5  (Pironman MAX 5)', '192.168.50.1  —  All browser tools live here.'],
    ['Port 3',
     '44Net Gateway Pi 5  (Argon NEO 5)', '192.168.50.2  —  AMPRNet WireGuard gateway.'],
    ['Port 4',
     'Windows Laptop  (Winlink + JS8Call)', '192.168.50.3  (static reservation)  —  or via EMCOMM-NET Wi-Fi.'],
    ['Port 5',
     'Color MFP Network Printer', '192.168.50.10  (recommended static reservation)  —  auto-discovered by all devices via Bonjour.'],
    ['Ports 6 – 9',
     'Pi 500 Operator Workstations  (up to 4)', '192.168.50.20 – 192.168.50.23  (static DHCP reservations)'],
    ['Port 10',
     'Satellite dish router  (optional)', 'Optional — connect satellite Ethernet to switch as WAN source on ASUS router.'],
    ['Port 11',
     'ASUS RT-BE58 Go — Mesh Node 1',
     'Wired backhaul to first mesh node.  Extends EMCOMM-NET to secondary coverage zone.'],
    ['Port 12',
     'ASUS RT-BE58 Go — Mesh Node 2',
     'Wired backhaul to second mesh node.  Extends EMCOMM-NET to third coverage zone.'],
    ['Ports 13 – 16',
     'Spare',
     'Available for additional devices, IP radios, second TNC, or future expansion.'],
    ], [2.0*inch, 2.2*inch, CW-4.2*inch]))
story.append(SP(6))
story.append(tbl(['DEVICE', 'POWER SOURCE'], [
    ['ASUS RT-BE58 Go router',  'USB-C 18W PD adapter  —  or USB-C power bank for field use'],
    ['UniFi Switch Lite 16 PoE', 'Included 45W AC power supply'],
    ['FieldCommand Pi 5  (Pironman MAX 5)', 'Official Raspberry Pi 27W USB-C PD supply via Pironman MAX 5 power inlet'],
    ['44Net Gateway Pi 5  (Argon NEO 5)', 'Official Raspberry Pi 27W USB-C PD supply directly to Pi USB-C port'],
], [2.4*inch, CW-2.4*inch]))
story.append(SP(6))
story.append(H2('1.2  the cellular antenna unit — Physical Setup and Antenna Mounting'))
story.append(P(
    'The the cellular antenna unit system consists of an outdoor antenna/modem unit connected by a single PoE '
    'Ethernet cable to the ASUS router WAN port. '
    'The modem is built into the antenna enclosure — no separate modem box to install. '
    'A single cable carries both power to the outdoor unit and data back to the router.'))
story.append(SP(6))

story.append(H3('Drum Antenna  (Primary — Omnidirectional)'))
story.append(steps([
    '<b>Mount the Drum</b> on a standard 1.5" to 2" mast, pole, or tripod at the deployment site. '
    'Higher is better — roof edge, vehicle roof rack, or portable mast. '
    'The Drum is omnidirectional so pointing direction does not matter.',
    '<b>Run the PoE Ethernet cable</b> from the Drum down to the ASUS router location. '
    'The cable carries power to the Drum and data back to the router. '
    'Maximum cable length is typically 100 meters (328 ft) for PoE over CAT 6.',
    '<b>Connect the PoE cable</b> to the <b>ASUS RT-BE58 Go WAN port</b>. '
    'Do not connect to the switch — this goes directly to the router WAN port.',
    '<b>Power on the the cellular antenna unit system.</b> '
    'The Drum status LED will indicate cellular connection status. '
    'Open http://my.insty or http://10.1.1.1 on any device temporarily connected to the the cellular antenna unit '
    'Wi-Fi to verify the modem has cellular signal.',
    '<b>Verify the ASUS WAN port shows "Connected"</b> in the ASUS router admin at '
    'http://192.168.50.254 → WAN → Internet Status.',
]))
story.append(SP(6))

story.append(H3('Switchblade Antenna  (Backup — Directional)'))
story.append(P(
    'Deploy the Switchblade when the Drum cannot get adequate signal at a specific site — '
    'typically in areas with marginal cellular coverage or significant RF obstruction. '
    'The Switchblade folds flat for transport and deploys in under 5 minutes.'))
story.append(SP(4))
story.append(steps([
    '<b>Unfold the Switchblade</b> and mount it on the same mast or a portable tripod.',
    '<b>Open the the cellular antenna unit signal app</b> on a phone connected to the the cellular antenna unit Wi-Fi. '
    'Slowly rotate the Switchblade while watching signal strength in the app. '
    'Stop at the direction giving the highest signal — typically facing the nearest '
    'the nearest cellular tower.',
    '<b>Unplug the Drum PoE cable</b> from the ASUS WAN port.',
    '<b>Connect the Switchblade PoE cable</b> to the same ASUS WAN port.',
    '<b>Verify connection</b> in the ASUS router admin — WAN should show "Connected" '
    'with the the cellular modem IP.',
]))
story.append(SP(6))

story.append(H3('the cellular antenna unit Data Plan — Activation and Standby'))
story.append(tbl(['STATE', 'COST', 'WHEN TO USE', 'HOW TO CHANGE'], [
    ['Active — Multi-Network',
     '~$79-99/month',
     'During activations, exercises, and training events',
     'Log in to the cellular antenna unit portal — activate plan'],
    ['Standby mode',
     '$5/month',
     'Between activations — holds your plan and SIM active without full monthly charge',
     'Log in to the cellular antenna unit portal — pause plan (available after first month)'],
    ['Cancelled',
     '$0',
     'Extended periods of non-use  (re-activation required)',
     'Cancel in portal — re-activate and receive new SIM when needed'],
    ], [2.0*inch, 0.9*inch, 1.8*inch, CW-4.7*inch]))
story.append(SP(4))
story.append(NoteBox(
    'For your organization operations, the recommended approach is to keep the plan in '
    'Standby mode ($5/month) between activations. '
    'This maintains the SIM, the phone number, and the multi-network capability '
    'so you can activate at full speed the moment an emergency is declared. '
    'The standby cost is negligible for a 501(c)(3) organization and avoids the '
    'delay of re-activating a cancelled plan during an actual emergency.',
    'tip'))
story.append(SP(8))

story.append(H2('1.2  Configure the ASUS RT-BE58 Go'))
story.append(steps([
    'Power on the router. Connect a device to it via Wi-Fi (default SSID on label) or Ethernet. Open http://192.168.50.1 (or the default router IP on the label).',
    'Complete the router setup wizard. When it asks for WAN, choose Automatic IP (DHCP) or skip if no internet is connected.',
    'Go to <b>LAN → LAN IP</b>. Set the LAN IP to <b>192.168.50.1</b>, subnet <b>255.255.255.0</b>. Apply.',
    'Go to <b>LAN → DHCP Server</b>. Set IP pool: <b>192.168.50.100 – 192.168.50.200</b>. Apply.',
    'Change the ASUS router admin password to something strong. Record it on a piece of paper stored on the FIELDCOMMAND USB drive.',
    'Set Manually Assigned IP for the Pi: go to <b>LAN → DHCP Server → Manually Assigned IP</b>. Enter the Pi\'s MAC address → assign IP <b>192.168.50.1</b>. (Or set the Pi\'s static IP manually in Step 4.)',
    'Set the Wi-Fi SSID: go to <b>Wireless → General</b>. Set both the 2.4 GHz and 5 GHz SSIDs to <b>EMCOMM-NET</b>. Set a strong WPA3/WPA2 password. Apply.',
]))
story.append(SP(6))
story.append(P(
    'The ASUS RT-BE58 Go supports dual WAN with automatic failover. '
    'the cellular modem is the primary WAN source. '
    'satellite dish is the secondary — the ASUS switches automatically if cellular drops. '
    'When both are unavailable, FieldCommand continues operating on all local features '
    'without interruption — net logging, ICS platform, APRS, and all tools remain fully functional.'))
story.append(SP(6))
story.append(tbl(['PRIORITY', 'WAN SOURCE', 'ASUS CONNECTION', 'SETUP', 'ACTIVATES'], [
    ['1  — Primary', 'the cellular antenna unit Drum  (omnidirectional cellular)',
     'WAN Ethernet port  (PoE from modem)',
     'PoE Ethernet cable from the cellular antenna unit outdoor unit to ASUS WAN port.  '
     'Set WAN → Automatic IP (DHCP).  the cellular antenna unit modem serves DHCP.',
     'Always — deployed at every activation'],
    ['1b — Swap', 'the cellular antenna unit Switchblade  (directional cellular)',
     'Same WAN Ethernet port  (replaces Drum cable)',
     'Unplug Drum PoE cable.  Plug Switchblade PoE cable into same ASUS WAN port.  '
     'Aim Switchblade toward nearest tower using the cellular antenna unit signal app.',
     'Manual — when Drum signal is poor at the deployment site'],
    ['2  — Secondary', 'satellite internet',
     'ASUS USB WAN port  (via Ethernet adapter)',
     'satellite Ethernet adapter → USB-to-Ethernet adapter → ASUS USB WAN port.  '
     'Set ASUS WAN failover: primary = WAN port, secondary = USB port.  '
     'Automatic failover when cellular WAN drops.',
     'Automatic — when the cellular antenna unit WAN is down or degraded'],
    ['3  — Site network', 'EOC site Ethernet',
     'WAN Ethernet port  (replaces the cellular antenna unit)',
     'Plug site Ethernet directly into ASUS WAN port.  '
     'Set WAN → Automatic IP (DHCP).  Use when site has reliable wired internet.',
     'Manual — when site LAN is available at an EOC or shelter'],
    ['4  — Last resort', 'USB smartphone tether',
     'ASUS USB WAN port',
     'Enable hotspot on phone.  Plug USB into ASUS router USB port.  '
     'Set WAN → USB Tethering.',
     'Manual — last resort when all other WAN sources are unavailable'],
    ['5  — Site Wi-Fi', 'WISP (venue Wi-Fi)',
     'ASUS wireless WAN',
     'ASUS Web UI → Operation Mode → WISP.  '
     'Select venue Wi-Fi and enter password.',
     'Manual — hospital, shelter, or venue with existing guest Wi-Fi'],
], [0.9*inch, 1.5*inch, 1.4*inch, 1.8*inch, CW-5.6*inch]))
story.append(SP(8))
story.append(H2('1.3  Configure Dual WAN Failover  (the cellular antenna unit Primary  +  satellite dish Secondary)'))
story.append(P(
    'With the cellular antenna unit connected to the WAN port and satellite dish connected via USB, '
    'configure the ASUS router to switch automatically between them. '
    'This takes about 3 minutes and requires no changes to FieldCommand software.'))
story.append(SP(6))
story.append(steps([
    'Open the ASUS router admin: <b>http://192.168.50.254</b>',
    'Go to <b>WAN → Dual WAN</b>.',
    'Set <b>Enable Dual WAN</b> to ON.',
    'Set <b>Primary WAN</b> to <b>WAN</b> (the physical WAN port — the cellular antenna unit).',
    'Set <b>Secondary WAN</b> to <b>USB</b> (the USB port — satellite dish via adapter).',
    'Set <b>Dual WAN mode</b> to <b>Failover mode</b>.',
    'Under <b>Heartbeat server</b>, set the primary check target to <b>1.1.1.1</b> (Cloudflare) '
    'and secondary to <b>8.8.8.8</b> (Google). These are the IPs the router pings to confirm WAN is up.',
    'Set <b>Failback to primary WAN when primary WAN is recovered</b> to ON. '
    'This switches back to the cellular antenna unit automatically when cellular returns.',
    'Click <b>Apply</b>.',
    'Test failover: unplug the the cellular antenna unit PoE cable from the WAN port. '
    'Within 30-60 seconds, the ASUS should switch to satellite dish USB. '
    'Check WAN status in the router admin — it should show USB WAN active. '
    'Reconnect the cellular antenna unit — the router should failback to WAN port within 60 seconds.',
]))
story.append(SP(4))
story.append(tbl(['WAN STATE', 'WHAT EMCOMM-NET DEVICES SEE', 'FIELDCOMMAND IMPACT'], [
    ['Cellular WAN  UP  (primary)',
     'Full internet — 5G/LTE via cellular antenna',
     'NWS weather alerts live, APRS-IS active, FCC DB refresh available, Pat Winlink via internet'],
    ['Cellular DOWN → Satellite UP  (failover)',
     'Full internet via satellite — slightly higher latency (~20-40ms)',
     'All internet features remain active.  CGNAT on satellite dish means no inbound connections possible.'],
    ['Both WAN sources DOWN',
     'No internet — EMCOMM-NET still fully operational.',
     'All local FieldCommand features work normally.  NWS alerts, APRS-IS, FCC refresh paused until WAN returns.'],
], [2.0*inch, 2.0*inch, CW-4.0*inch]))
story.append(SP(8))

story.append(H2('1.4  AiMesh Mesh Node Setup — Extending EMCOMM-NET Coverage'))
story.append(P(
    'The standard FieldCommand deployment includes three ASUS RT-BE58 Go routers: '
    'one primary (connected to the cellular antenna unit WAN and the UniFi switch) '
    'and two mesh nodes that extend EMCOMM-NET to additional rooms, floors, or outdoor areas. '
    'All three use the same hardware, the same SSID, and the same password. '
    'Devices roam between them automatically.'))
story.append(SP(4))
story.append(NoteBox(
    'Connect the two mesh nodes via wired Ethernet backhaul (switch Ports 11 and 12) '
    'rather than wireless backhaul whenever possible. '
    'Wired backhaul provides full Wi-Fi 7 throughput on both upstream and downstream — '
    'wireless backhaul cuts bandwidth roughly in half because the node uses its radios '
    'for both the backhaul link and the client connections simultaneously.',
    'tip'))
story.append(SP(6))
story.append(P('<b>Repeat these steps for each of the two mesh nodes:</b>'))
story.append(SP(4))
story.append(steps([
    '<b>Connect the node Ethernet</b> — run a CAT 6 cable from UniFi Switch Port 11 '
    '(first node) or Port 12 (second node) to the LAN port of the mesh node router. '
    'This is the wired backhaul — it carries all traffic between the node and the primary.',
    '<b>Power on the node</b> — connect the USB-C power supply to the mesh node. '
    'For initial pairing, position the node within 30 feet of the primary router. '
    'After pairing it can be moved to its final location.',
    '<b>Open AiMesh on the primary router</b> — go to '
    '<b>http://192.168.50.254 → AiMesh → AiMesh Node</b>. '
    'The new node appears in the device list within 1-2 minutes.',
    '<b>Click Connect</b> on the new node. '
    'The primary router pushes the EMCOMM-NET SSID, password, and configuration '
    'to the node automatically. This takes 1-3 minutes.',
    '<b>Move the node to its final position</b> — mount or place it in the coverage '
    'area it needs to serve. The wired backhaul cable connects back to the UniFi switch. '
    'Test coverage with a phone on EMCOMM-NET at the furthest point in the area.',
    '<b>Verify in AiMesh dashboard</b> — on the primary router, '
    'AiMesh → AiMesh Node should show both nodes as Connected with backhaul type Ethernet. '
    'Green status on both nodes confirms the mesh is fully operational.',
]))
story.append(SP(6))
story.append(ref_tbl_2col(['NODE', 'SWITCH PORT', 'RECOMMENDED PLACEMENT'], [
    ['Primary RT-BE58 Go  (AiMesh controller)',
     'Uplink to ASUS 2.5G LAN port',
     'Central to the deployment — EOC command post or entrance area'],
    ['RT-BE58 Go — Mesh Node 1',
     'UniFi Switch Port 11',
     'Secondary room, opposite wing, or upper floor'],
    ['RT-BE58 Go — Mesh Node 2',
     'UniFi Switch Port 12',
     'Third coverage zone — outdoor staging, parking, or far building wing'],
    ], [2.0*inch, 1.4*inch, CW-3.4*inch]))
story.append(PB())

# ── STEP 2 — DOWNLOAD & INSTALL ──────────────────────────────────────────────
story.append(StepBox(3, 'Download & Run the FieldCommand Installer'))
story.append(SP(8))
story.append(H1('Step 3:  Download & Run the FieldCommand Installer'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(H2('Method A — Direct download to the Pi (requires internet on Pi)'))
story.append(P('<b>Lite:</b> SSH into the Pi and run these commands. '
               '<b>Desktop:</b> open a Terminal window (taskbar → Terminal) and run the same commands.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Create working directory',
    'mkdir -p ~/fieldcommand-install && cd ~/fieldcommand-install',
    '# Download the FieldCommand package from GitHub or your storage location',
    'wget -O fieldcommand-v1.zip https://github.com/KE4CON/CrossPlatformAPRS/releases/latest/download/fieldcommand-v1.zip',
    '# Unzip the package',
    'unzip fieldcommand-v1.zip',
    'cd fieldcommand',
]))
story.append(SP(8))
story.append(H2('Method B — Copy from your computer using SCP (Lite/headless)'))
story.append(CodeBlock([
    '# Run this on YOUR COMPUTER, not the Pi',
    'scp fieldcommand-v1.zip fieldcommand@[pi-ip-address]:~/',
    '# Then SSH into the Pi and unzip',
    'ssh fieldcommand@[pi-ip-address]',
    'mkdir -p ~/fieldcommand-install',
    'mv fieldcommand-v1.zip ~/fieldcommand-install/',
    'cd ~/fieldcommand-install && unzip fieldcommand-v1.zip',
    'cd fieldcommand',
]))
story.append(SP(8))
story.append(H2('Method B2 — Download directly on the Pi Desktop (Desktop edition)'))
story.append(tbl(['OPTION', 'HOW'], [
    ['Browser download',
     'Open Chromium on the Pi. Go to the GitHub releases page or download URL. '
     'Download fieldcommand-v1.zip — it saves to ~/Downloads/ automatically.'],
    ['USB drive',
     'Copy fieldcommand-v1.zip to a USB drive. Insert the USB into the Pi. '
     'Open File Manager, drag the zip to your home folder.'],
], [1.3*inch, CW-1.3*inch]))
story.append(SP(4))
story.append(CodeBlock([
    '# If downloaded to ~/Downloads/:',
    'mkdir -p ~/fieldcommand-install',
    'cp ~/Downloads/fieldcommand-v1.zip ~/fieldcommand-install/',
    '# Unzip (same for all methods):',
    'cd ~/fieldcommand-install && unzip fieldcommand-v1.zip',
    'cd fieldcommand',
]))
story.append(SP(8))
story.append(H2('Method C — USB drive transfer (fully offline)'))
story.append(P('<b>Lite:</b> commands below via SSH. '
               '<b>Desktop:</b> use File Manager to copy the zip from USB to your home folder, '
               'then open a Terminal for the unzip step.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Copy fieldcommand-v1.zip to a USB drive on your computer',
    '# Insert USB drive into the Pi, then:',
    'sudo mount /dev/sda1 /mnt   # or check lsblk for your device',
    'cp /mnt/fieldcommand-v1.zip ~/fieldcommand-install/',
    'cd ~/fieldcommand-install && unzip fieldcommand-v1.zip',
    'cd fieldcommand',
]))
story.append(SP(6))
story.append(H2('Launch the Installer'))
story.append(P('<b>Lite:</b> run via SSH. '
               '<b>Desktop:</b> open a Terminal window from the taskbar or Accessories → Terminal. '
               'The installer runs identically on both.'))
story.append(SP(4))
story.append(CodeBlock([
    'cd ~/fieldcommand-install/fieldcommand',
    'sudo bash scripts/install.sh',
]))
story.append(PB())

# ── STEP 3 — INSTALLER CONFIGURATION ─────────────────────────────────────────
story.append(StepBox(4, 'Installer Configuration Options'))
story.append(SP(8))
story.append(H1('Step 4:  Installer Configuration Options'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(tbl(['PROMPT', 'DEFAULT', 'DESCRIPTION'], [
    ['Station callsign', 'W8ABC', 'Your amateur callsign. Patched into all HTML pages.'],
    ['Station latitude', '42.3153', 'Decimal degrees. Used for APRS station marker, NWS alerts, propagation, distance calc.'],
    ['Station longitude', '-88.4473', 'Decimal degrees (negative = West). Default 0.0/0.0 — set to your deployment coordinates.'],
    ['Wi-Fi AP SSID', 'EMCOMM-NET', 'The Wi-Fi network name that field devices connect to.'],
    ['Wi-Fi AP password', 'fieldcommand2026', 'WPA2 password for EMCOMM-NET. Change this for operational security.'],
    ['Server IP address', '192.168.50.1', 'The Pi\'s static IP on EMCOMM-NET. Devices browse to http://192.168.50.1/'],
    ['Download FCC database', 'N', '~600 MB download of the FCC amateur license database. Recommended: Y'],
    ['Kiwix tier', '1', 'Tier 1: WikiMed + Wikipedia Mini + Wikivoyage (~2.5 GB). Tier 2 adds iFixit (~5 GB more).'],
], [1.6*inch, 1.2*inch, CW-2.8*inch]))
story.append(SP(6))
story.append(H2('What the Installer Does Automatically'))
for item in [
    'Installs system packages: Python 3, nginx, kiwix-tools, rsync, gpsd, ufw, mdadm, java',
    'Creates the <b>fieldcommand</b> system user and directory structure at /opt/fieldcommand/',
    'Creates a Python virtual environment and installs Flask, flask-cors, requests, gpsd-py3',
    'Deploys all 30 HTML pages to /opt/fieldcommand/html/ and patches your callsign and coordinates into each file',
    'Installs all 14 systemd service and timer units and enables them at boot',
    'Configures nginx with the correct web root (/opt/fieldcommand/html/) and proxy rules for all API ports',
    '<b>Does NOT configure a Wi-Fi access point</b> — Wi-Fi is handled by the ASUS RT-BE58 Go router. The Pi connects as a wired client only.',
    'Configures the Pi static IP (192.168.50.1/24) on the Ethernet interface (eth0) via NetworkManager',
    'Configures the firewall (ufw) — opens all required ports',
    'Downloads and installs YAAC (Java APRS client) and Graywolf to /opt/yaac/ and /opt/graywolf/',
    'Installs the USB backup udev rule (plug in a USB drive labeled FIELDCOMMAND to trigger auto-backup)',
    'Downloads and installs Pat Winlink (browser-based Winlink backup client, port 8090)',
    'Runs the Kiwix ZIM downloader for the selected content tier',
    'Downloads the FEMA ICS forms PDFs to /opt/fieldcommand/data/ics_forms/ (22 forms)',
    'Optionally downloads and builds the FCC amateur license database (~600 MB)',
    'Starts all services and verifies they are running',
]:
    story.append(P(f'• {item}', S('bl', fontSize=8.5, leading=12, leftIndent=14, firstLineIndent=-10)))
story.append(SP(4))
story.append(NoteBox(
    'The ASUS RT-BE58 Go router must be configured before running the installer — see Step 1. '
    'The Pi does NOT run hostapd or dnsmasq. All Wi-Fi, DHCP, and SSID management is handled by the ASUS router.',
    'warning'))
story.append(PB())

# ── STEP 4 — STATIC IP ───────────────────────────────────────────────────────
story.append(StepBox(5, 'Raspberry Pi 5 — Static IP Configuration'))
story.append(SP(8))
story.append(H1('Step 5:  Raspberry Pi 5 — Static IP Configuration'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Pi must always be reachable at 192.168.50.1. If the installer already set this via a DHCP '
               'reservation in the ASUS router, verify with <font face="Courier">ip addr show eth0</font> and '
               'skip to Step 5 if 192.168.50.1/24 is shown.'))
story.append(SP(6))
story.append(H2('Path A — Raspberry Pi OS Lite (SSH)'))
story.append(CodeBlock([
    '# SSH into the Pi (use the IP shown in your router DHCP table)',
    'ssh fieldcommand@[current-pi-ip]',
    '# Find the Ethernet connection name',
    'nmcli con show',
    '# Usually: "Wired connection 1" or "Preconfigured Connection 1"',
    '# Set static IP',
    'sudo nmcli con mod "Wired connection 1"  ipv4.addresses 192.168.50.1/24  ipv4.method manual',
    '  ipv4.method manual',
    '# Apply the change',
    'sudo nmcli con up "Wired connection 1"',
    '# Verify — should show inet 192.168.50.1/24',
    'ip addr show eth0',
]))
story.append(SP(6))
story.append(H2('Path B — Raspberry Pi OS Desktop (GUI)'))
story.append(steps([
    'Click the <b>network icon</b> in the taskbar (top-right corner).',
    'Click <b>Advanced Options → Edit Connections</b>.',
    'Select your <b>Wired connection</b> and click the gear/edit icon.',
    'Click the <b>IPv4 Settings</b> tab.',
    'Change <b>Method</b> from "Automatic (DHCP)" to <b>Manual</b>.',
    'Click <b>Add</b> and enter: Address: 192.168.50.1 · Netmask: 255.255.255.0 · Gateway: (leave blank)',
    'Click <b>Save</b>, then close the Network Connections window.',
    'Disconnect and reconnect the Ethernet cable, or reboot the Pi.',
    'Open the <b>Terminal</b> and verify: <font face="Courier">ip addr show eth0</font> — should show <b>inet 192.168.50.1/24</b>.',
    'Open <b>Chromium</b> on the Pi and go to http://192.168.50.1 to confirm FieldCommand loads locally.',
]))
story.append(SP(4))
story.append(NoteBox(
    'Alternatively, open a Terminal on the desktop and use the same nmcli commands shown in Path A. '
    'The terminal method works identically on the Desktop edition.', 'tip'))
story.append(SP(6))
story.append(H2('Path C — raspi-config (if available)'))
story.append(CodeBlock([
    '# Open raspi-config:',
    'sudo raspi-config',
    '# Navigate to: System Options → Network → (set static IP if option is present)',
    '# NOTE: Static IP configuration via raspi-config was removed in Raspberry Pi OS Bookworm.',
    '# If the option is not visible, use Path A (nmcli) or Path B (GUI Network Connections).',
]))
story.append(PB())

# ── STEP 4b — RAID ───────────────────────────────────────────────────────────
story.append(StepBox('4b', 'RAID 1 NVMe Setup — Pironman MAX 5'))
story.append(SP(8))
story.append(H1('7b. RAID 1 NVMe Setup — Pironman MAX 5'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Pironman MAX 5 enclosure has two M.2 NVMe slots. Configure them as a RAID 1 mirror so '
               'both drives contain identical data. If one drive fails, the system continues running on the '
               'surviving drive with no data loss and no operator action required.'))
story.append(SP(4))
story.append(NoteBox('Complete this step before running the FieldCommand installer. The RAID array must be '
                     'assembled and the OS installed on it before FieldCommand is deployed. If your Pi OS is '
                     'already on a single drive, back it up first.', 'warn'))
story.append(SP(6))
story.append(H2('Physical Installation'))
story.append(steps([
    'Install both 1 TB NVMe SSDs into the Pironman MAX 5 M.2 slots. Slot 1 (primary) → /dev/nvme0n1 · Slot 2 (mirror) → /dev/nvme1n1',
    'Boot from a Raspberry Pi OS microSD card for the initial RAID setup. After RAID is built and OS is installed, the SD card is removed.',
]))
story.append(SP(6))
story.append(H2('Build the RAID 1 Array'))
story.append(CodeBlock([
    '# Install mdadm (RAID management tool)',
    'sudo apt-get install -y mdadm',
    '# Create RAID 1 array from the two NVMe drives',
    'sudo mdadm --create --verbose /dev/md0 --level=1 --raid-devices=2 \\',
    '  /dev/nvme0n1 /dev/nvme1n1',
    '# Confirm array is building (will show [=>...............] resync progress)',
    'cat /proc/mdstat',
    '# Create a filesystem on the RAID array',
    'sudo mkfs.ext4 -L fieldcommand-raid /dev/md0',
    '# Mount it',
    'sudo mkdir -p /mnt/raid',
    'sudo mount /dev/md0 /mnt/raid',
    '# Copy running OS to RAID array',
    'sudo apt-get install -y rsync',
    'sudo rsync -axv --progress / /mnt/raid/',
    '# Save RAID configuration so it persists across reboots',
    'sudo mdadm --detail --scan | sudo tee -a /mnt/raid/etc/mdadm/mdadm.conf',
]))
story.append(SP(6))
story.append(H2('RAID Health Reference'))
story.append(ref_tbl_2col(['SITUATION', 'WHAT TO DO'], [
    ['Both drives show [UU]', 'Normal healthy state. No action needed.'],
    ['One drive fails — [_U] or [U_]',
     '1. Power down. 2. Remove failed drive. 3. Insert new 1 TB NVMe. 4. Power on. '
     '5. Run: sudo mdadm /dev/md0 --add /dev/nvme1n1. 6. Array rebuilds automatically (~30 min).'],
    ['Check RAID health anytime', 'cat /proc/mdstat  or  sudo mdadm --detail /dev/md0'],
], [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(NoteBox('RAID 1 protects against drive failure — it is NOT a backup. Both drives contain '
                     'identical data, so accidental deletion or corruption affects both drives simultaneously. '
                     'Continue to use the USB auto-backup (insert FIELDCOMMAND USB drive) for regular data backups.', 'warn'))
story.append(PB())

# ── STEP 5 — KIWIX ───────────────────────────────────────────────────────────
story.append(StepBox(5, 'Kiwix Offline Library Setup'))
story.append(SP(8))
story.append(H1('8. Step 5: Kiwix Offline Library Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('Kiwix provides an offline web library served on port 8081. All devices on EMCOMM-NET can browse '
               'it at http://192.168.50.1:8081. Content is packaged as ZIM files.'))
story.append(SP(6))
story.append(tbl(['TIER', 'NAME', 'SIZE', 'DESCRIPTION'], [
    ['Essential', 'WikiMed — Medical Encyclopedia', '~471 MB',
     'Offline medical encyclopedia: symptoms, treatments, drugs, procedures. Critical for mass-casualty events.'],
    ['Essential', 'Wikipedia (Mini)', '~1.2 GB',
     'Compact English Wikipedia — essential facts, geography, science.'],
    ['Essential', 'Wikivoyage', '~820 MB',
     'Emergency shelters, evacuation routes, local resources and travel logistics.'],
    ['Extended', 'Wikibooks — How-To & Field Manuals', '~4.2 GB',
     'First aid, survival, ham radio, electronics, cooking, field skills.'],
    ['Extended', 'iFixit — Equipment Repair Manuals', '~3.1 GB',
     'Step-by-step repair guides for electronics, tools, vehicles.'],
    ['Extended', 'Wikipedia (Full English)', '~22 GB',
     'Complete English Wikipedia. Large download — requires 30 GB+ free.'],
    ], [0.9*inch, 2.2*inch, 0.8*inch, CW-3.9*inch]))
story.append(SP(6))
story.append(CodeBlock([
    '# Check what is installed and service status',
    'sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh --status',
    '',
    '# Add Tier 2 content (resumes interrupted downloads automatically)',
    'sudo bash /opt/fieldcommand/scripts/kiwix_setup.sh --tier 2',
    '',
    '# Service management',
    'sudo systemctl status kiwix',
    'sudo systemctl restart kiwix    # required after adding new ZIM files',
]))
story.append(SP(4))
story.append(NoteBox('ZIM downloads are resumable. If a download is interrupted by power loss or '
                     'network drop, simply re-run kiwix_setup.sh with the same --tier flag. '
                     'curl resumes from where it stopped — no need to start over.', 'tip'))
story.append(SP(8))
story.append(H2('Additional Kiwix Content — Install Any ZIM File'))
story.append(P(
    'Kiwix.org (kiwix.org/en/content/) publishes hundreds of ZIM archives beyond the two built-in tiers. '
    'Any ZIM file can be added to FieldCommand. The following table lists the most useful '
    'additions for emergency communications and public safety operations:'))
story.append(SP(6))
story.append(tbl(['CONTENT', 'APPROX SIZE', 'BEST FOR'], [
    ['OpenStreetMap  (Wikimedia Maps)',
     '~500 MB',
     'Offline detailed maps for any region.  Download your county or state for SAR and shelter mapping.'],
    ['Stack Overflow  (programming Q&A)',
     '~3.5 GB',
     'Technical troubleshooting reference.  Useful for net managers debugging FieldCommand.'],
    ['Project Gutenberg  (public domain books)',
     '~65 GB (full) / ~1 GB (best-of)',
     'Field reference library.  Includes FCC regulations, ARRL handbook excerpts, first aid guides.'],
    ['Khan Academy  (education)',
     '~30 GB',
     'Training resource for shelter and EOC staff during extended activations.'],
    ['Red Cross First Aid  (WikiMed companion)',
     '~200 MB',
     'Practical first aid procedures in plain language — supplements WikiMed for non-medical staff.'],
    ['Wiktionary  (dictionary)',
     '~520 MB',
     'Reference for unfamiliar ICS terminology and acronyms.'],
    ['Amateur Radio Wiki  (if available)',
     'Variable',
     'Band plans, antenna theory, Winlink and APRS procedures.'],
    ], [2.3*inch, 0.9*inch, CW-3.2*inch]))
story.append(SP(6))
story.append(H3('How to Install Any ZIM File'))
story.append(CodeBlock([
    '# Step 1 — Find and download the ZIM from a device with internet',
    '#           Browse to:  https://library.kiwix.org',
    '#           Filter by language (English) and category.',
    '#           Download the .zim file to your laptop or phone.',
    '',
    '# Step 2 — Transfer the ZIM to the Pi',
    '#           Option A: USB drive (copy to USB, insert in Pi)',
    'sudo mount /dev/sda1 /mnt',
    'cp /mnt/my_content.zim /opt/kiwix/zim/',
    '',
    '#           Option B: SCP from your laptop over EMCOMM-NET',
    'scp my_content.zim fieldcommand@192.168.50.1:/opt/kiwix/zim/',
    '',
    '# Step 3 — Register the new ZIM with the Kiwix library index',
    'sudo kiwix-manage /opt/kiwix/library.xml add /opt/kiwix/zim/my_content.zim',
    '',
    '# Step 4 — Restart Kiwix to load the new content',
    'sudo systemctl restart kiwix',
    '',
    '# Step 5 — Verify it appears at http://192.168.50.1:8081',
    '# The new content appears in the Kiwix home page search bar.',
    '',
    '# To list all installed ZIM files:',
    'ls -lh /opt/kiwix/zim/',
    '',
    '# To remove a ZIM file:',
    'sudo rm /opt/kiwix/zim/my_content.zim',
    'sudo systemctl restart kiwix',
]))
story.append(SP(4))
story.append(NoteBox(
    'ZIM files can be large.  Check available disk space before downloading: '
    'df -h /opt/kiwix/  '
    'The RAID array provides 2× 1 TB = ~900 GB usable after OS and FieldCommand.  '
    'Tier 1 uses ~2.5 GB.  Tier 2 uses ~10 GB.  There is ample space for additional content.',
    'tip'))
story.append(PB())

# ── STEP 6 — FCC ─────────────────────────────────────────────────────────────
story.append(StepBox(6, 'FCC Amateur Database'))
story.append(SP(8))
story.append(H1('9. Step 6: FCC Amateur Database'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'The FCC database gives FieldCommand instant offline access to the entire US amateur '
    'radio license database — approximately 800,000 active licensees. '
    'When a net control operator types a callsign into the check-in field, '
    'FieldCommand looks up the licensee name, license class, and address automatically '
    'in under a millisecond, with no internet connection required. '
    'This is one of the most-used features during ARES/RACES net operations.'))
story.append(SP(4))
story.append(P(
    'The installer offers to download and build the database during Step 4 (answer Y). '
    'If you skipped it during installation, or if the database needs to be rebuilt, '
    'run the commands below. Building takes approximately 5 to 10 minutes '
    'on a Pi 5 and requires an active internet connection.'))
story.append(SP(6))
story.append(CodeBlock([
    '# If you selected "y" during install, it already ran.',
    '# To build or rebuild manually:',
    'sudo -u fieldcommand \\',
    '  /opt/fieldcommand/venv/bin/python \\',
    '  /opt/fieldcommand/python/build_fcc_db.py',
    '# Automatic weekly refresh timer:',
    'sudo systemctl status fcc-refresh.timer',
    '# Force immediate refresh:',
    'sudo systemctl start fcc-refresh.service',
]))
story.append(PB())

# ── STEP 7 — APRS ────────────────────────────────────────────────────────────
story.append(StepBox(7, 'APRS Setup — Graywolf + YAAC'))
story.append(SP(8))
story.append(H1('10. Step 7: APRS Setup (Graywolf + YAAC)'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'FieldCommand integrates two APRS client applications: '
    'Graywolf TNC (accessible on port 8080) and YAAC — Yet Another APRS Client (port 8082). '
    'Both run as background services and feed live station data to the Tactical APRS Map '
    'on the dashboard. The map merges data from both sources, deduplicates by callsign, '
    'and maintains a live WebSocket feed to all connected browsers simultaneously.'))
story.append(SP(4))
story.append(P(
    'APRS is entirely optional. FieldCommand runs fully without it — '
    'you simply will not see live APRS stations on the tactical map. '
    'If you are not planning to use a TNC or radio interface, skip this step entirely '
    'and proceed to Step 8 (Printer Setup).'))
story.append(SP(4))
story.append(NoteBox('The FieldCommand installer attempts to download and install both YAAC and Graywolf automatically. '
                     'If internet was available during installation, they should already be present. '
                     'Skip to Section 9.3 (YAAC port configuration) if the installer succeeded.', 'info'))
story.append(SP(6))
story.append(H2('9.1  Verify Automatic Installation'))
story.append(CodeBlock([
    '# Check if Java is installed',
    'java -version',
    '# Check if YAAC was installed',
    'ls -lh /opt/yaac/YAAC.jar',
    '# Check if Graywolf was installed',
    'ls -lh /opt/graywolf/graywolf.jar',
    '# Check service status',
    'sudo systemctl status yaac',
    'sudo systemctl status graywolf',
]))
story.append(SP(6))
story.append(H2('9.2  Manual Install — If Automatic Install Failed'))
story.append(CodeBlock([
    '# Step 1 — Install Java runtime (required by both clients)',
    'sudo apt install -y default-jre',
    '# Step 2 — Install YAAC',
    'sudo mkdir -p /opt/yaac',
    'cd /tmp && wget http://www.ka2ddo.org/ka2ddo/YAAC.zip',
    'sudo unzip YAAC.zip "*.jar" -d /opt/yaac/',
    'sudo mv /opt/yaac/YAAC*.jar /opt/yaac/YAAC.jar 2>/dev/null || true',
    'sudo chown -R fieldcommand:fieldcommand /opt/yaac',
    '# Step 3 — Install Graywolf',
    'sudo mkdir -p /opt/graywolf',
    'sudo wget -O /opt/graywolf/graywolf.jar \\',
    '  https://github.com/vk2tds/graywolf/releases/latest/download/graywolf.jar',
    'sudo chown -R fieldcommand:fieldcommand /opt/graywolf',
    '# Step 4 — Enable services',
    'sudo systemctl enable --now yaac',
    'sudo systemctl enable --now graywolf',
]))
story.append(SP(6))
story.append(H2('9.3  YAAC Port Configuration (Required — First Run)'))
story.append(steps([
    'Run YAAC once on a desktop/monitor: <font face="Courier">java -jar /opt/yaac/YAAC.jar</font>',
    'Go to <b>File → Configure → Web Server</b> tab.',
    'Set <b>Port: 8082</b> · Check <b>Enable REST API</b> · Check <b>Enable WebSocket</b> · Click Save.',
    'Close YAAC. The yaac.service will use these settings when running headlessly.',
]))
story.append(SP(6))
story.append(H2('9.4  Connect a TNC or Radio Interface'))
story.append(tbl(['INTERFACE TYPE', 'PORT TYPE IN YAAC', 'SETTINGS'], [
    ['USB TNC (Digirig, SignaLink, etc.)', 'Serial TNC', '/dev/tnc0, baud rate 9600 or 1200'],
    ['KISS TNC over TCP (Direwolf)', 'KISS TNC (TCP)', 'Host: localhost, Port: 8001'],
    ['AGW packet engine (Direwolf)', 'AGW', 'Host: localhost, Port: 8000'],
    ['APRS-IS internet (if WAN connected)', 'APRS-IS', 'Server: noam.aprs2.net:14580, Filter: r/42.31/-88.44/50'],
    ], [2.2*inch, 1.5*inch, CW-3.7*inch]))
story.append(SP(6))
story.append(H2('9.5  Verify APRS is Working'))
story.append(CodeBlock([
    '# Test YAAC REST API (should return JSON list of heard stations)',
    'curl http://localhost:8082/api/stations',
    '# Test Graywolf REST API',
    'curl http://localhost:8080/api/stations',
    '# Check service logs if no stations appear',
    'journalctl -u yaac -n 30',
    'journalctl -u graywolf -n 30',
]))
story.append(PB())

# ── STEP 8 — PRINTER ─────────────────────────────────────────────────────────
story.append(StepBox(8, 'Printer Setup — Three Connection Options'))
story.append(SP(8))
story.append(H1('11. Step 8: Printer Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('FieldCommand has print buttons on 17 pages. All printing uses the browser standard '
               'window.print() function, which sends the job to whatever printer the operator\'s browser '
               'can reach. Three printer connection methods are supported:'))
story.append(SP(6))
story.append(H2('Option A — Client Device Prints to Its Own Printer (Simplest)'))
story.append(P('Each operator\'s laptop or tablet prints to its own locally connected printer. '
               'No Pi configuration needed. Zero setup required — works immediately.'))
story.append(SP(6))
story.append(NoteBox('This is the simplest option and requires zero configuration on the Pi. '
                     'The only requirement is that the operator\'s device has a printer configured.', 'tip'))
story.append(SP(8))
story.append(H2('Option B — USB Printer Shared via Pi (CUPS)'))
story.append(P('A USB printer is connected directly to the Pi. CUPS shares it across EMCOMM-NET. '
               'Installed automatically by the FieldCommand installer. CUPS admin UI at http://192.168.50.1:631.'))
story.append(SP(4))
story.append(H3('B.2  Add the USB Printer via CUPS Web Admin'))
story.append(steps([
    'Plug the USB printer into one of the Pi\'s USB ports (or powered USB hub).',
    'On any device on EMCOMM-NET, open a browser and go to: <b>http://192.168.50.1:631</b>',
    'Click <b>Administration → Add Printer</b>.',
    'If prompted for credentials, enter the Pi username and password (e.g. fieldcommand / your password).',
    'Your USB printer appears in the <b>Local Printers</b> list. Select it and click <b>Continue</b>.',
    'Enter a Name (e.g. FieldCommand-Printer), Description, and Location. Check <b>Share This Printer</b>. Click Continue.',
    'Select the correct printer driver. Click <b>Add Printer</b>.',
    'Set default options (paper size: Letter) and click <b>Set Default Options</b>.',
    'Click <b>Print Test Page</b> to confirm the printer is working.',
]))
story.append(SP(6))
story.append(H3('B.3  Add the Shared Printer on Operator Devices'))
story.append(tbl(['DEVICE TYPE', 'HOW TO ADD THE SHARED PRINTER'], [
    ['Windows laptop  (Winlink / JS8Call station)',
     'Settings → Bluetooth & devices → Printers & scanners → Add a printer or scanner.  '
     'Windows discovers the CUPS shared printer automatically on EMCOMM-NET via Bonjour.  '
     'Select FieldCommand-Printer when it appears and click Add device.'],
    ['Mac / macOS',
     'System Settings → Printers & Scanners → click + (Add Printer).  '
     'Click the Default tab — the shared printer appears via Bonjour discovery.  '
     'Select it and click Add.'],
    ['iPad / iPhone  (AirPrint)',
     'No setup required.  CUPS + Avahi advertises the printer as AirPrint-compatible.  '
     'Open any FieldCommand page → tap the Share icon → tap Print → select the printer.  '
     'Works on any iOS device on EMCOMM-NET.'],
    ['Android tablet / phone',
     'Install the free CUPS Print app from Google Play.  '
     'Open the app → Add Printer → enter IP 192.168.50.1,  Port 631,  Protocol IPP.  '
     'The printer appears in the Android print dialog for all apps.'],
    ['Chromebook',
     'Settings → Advanced → Printing → Printers → Add Printer.  '
     'Enter:  Name = FieldCommand-Printer,  Address = 192.168.50.1,  Protocol = IPP,  '
     'Queue = /printers/FieldCommand-Printer.  Click Add.'],
    ['Raspberry Pi 500 / 500+  (operator workstation)',
     'Chromium browser  (pre-installed): the CUPS printer appears automatically in the print dialog.  '
     'No additional setup needed — Chromium on Pi OS discovers CUPS printers via Bonjour.  '
     'For Firefox ESR on the Pi 500:  install via  sudo apt install firefox-esr  '
     'then open Print → More Settings → select the printer from the destination list.  '
     'Alternatively, run:  sudo usermod -aG lpadmin fieldcommand  to give the Pi 500 user '
     'full access to the CUPS admin at http://192.168.50.1:631.'],
], [1.6*inch, CW-1.6*inch]))
story.append(SP(6))
story.append(H3('B.4  Recommended Printers for Field Use'))
story.append(P('<b>Monochrome Laser  (recommended for most EOC deployments)</b>',
               S('ph2', fontSize=9.5, fontName='Helvetica-Bold', textColor=EOC_LT, leading=13)))
story.append(SP(3))
story.append(tbl(['PRINTER', 'CONNECTION', 'WHY IT WORKS WELL'], [
    ['Brother HL-L2350DW',
     'USB  or  Wi-Fi',
     'Excellent Linux driver support out of the box.  Fast, compact, duplex, durable.  '
     'Best all-round choice for field EOC use.  Under $130.'],
    ['HP LaserJet Pro M15w  /  P1102w',
     'USB  or  Wi-Fi',
     'Full Linux support via HP HPLIP driver (installed automatically with CUPS).  '
     'Fast, reliable, very low cost per page.  Under $150.'],
], [1.8*inch, 1.3*inch, CW-3.1*inch]))
story.append(SP(6))
story.append(P('<b>Color Multifunction Laser  (ICS maps, colored forms, and chart printing)</b>',
               S('ph2', fontSize=9.5, fontName='Helvetica-Bold', textColor=EOC_LT, leading=13)))
story.append(SP(3))
story.append(tbl(['PRINTER', 'CONNECTION', 'WHY IT WORKS WELL'], [
    ['Brother MFC-L3770CDW',
     'USB,  Wi-Fi,  or  Ethernet',
     'Color laser all-in-one with duplex, scan, copy, fax.  '
     'Full Linux support via Brother driver.  '
     'Prints color ICS maps and resource boards clearly.  Under $400.'],
    ['HP Color LaserJet Pro MFP M479fdw',
     'USB,  Wi-Fi,  or  Ethernet',
     'Color laser multifunction — print, scan, copy, fax.  '
     'HPLIP driver works with CUPS out of the box.  '
     'Excellent for IAP packages with color-coded sections.  Under $500.'],
    ['Canon imageCLASS MF743Cdw',
     'USB,  Wi-Fi,  or  Ethernet',
     'Color laser multifunction with excellent Linux CUPS driver (CAPT driver).  '
     'Handles letter and legal paper.  Good choice for permanent EOC installations.  Under $450.'],
], [1.8*inch, 1.5*inch, CW-3.3*inch]))
story.append(SP(6))
story.append(P('<b>Portable / Battery-Powered  (mobile and field deployments without shore power)</b>',
               S('ph2', fontSize=9.5, fontName='Helvetica-Bold', textColor=EOC_LT, leading=13)))
story.append(SP(3))
story.append(tbl(['PRINTER', 'CONNECTION', 'WHY IT WORKS WELL'], [
    ['Canon PIXMA TR150',
     'USB  or  Wi-Fi  (battery built-in)',
     'Compact inkjet with rechargeable battery.  Prints ~200 pages per charge.  '
     'Letter size.  Wi-Fi connects directly to EMCOMM-NET.  Under $200.'],
    ['HP OfficeJet 200',
     'USB  or  Wi-Fi  (battery optional)',
     'Portable inkjet with larger paper tray than TR150.  Optional battery accessory.  '
     'Good for shelter check-in stations and mobile command posts.  Under $180.'],
], [1.8*inch, 1.5*inch, CW-3.3*inch]))
story.append(PB())

story.append(H2('Option C — Network Printer on EMCOMM-NET (Simplest Shared Setup)'))
story.append(P(
    'A Wi-Fi or Ethernet printer is connected directly to the ASUS router or UniFi switch — '
    'no Pi involvement required at all. '
    'All devices on EMCOMM-NET can discover and print to it automatically via Bonjour / mDNS. '
    'This works with any network-capable printer including color multifunction laser printers '
    'that have built-in Wi-Fi or Ethernet. '
    'This is the simplest option for permanent EOC installations where a color MFP is already on site.'))
story.append(SP(6))
story.append(P(
    'Option C works with any network-capable printer — including all three color multifunction '
    'laser printers listed in the BOM. These are the best choice for a permanent EOC installation '
    'because they connect directly to EMCOMM-NET with no Pi configuration, provide color printing '
    'for ICS maps and IAP packages, and are discoverable by every device on scene automatically.'))
story.append(SP(6))
story.append(tbl(['CONNECTION METHOD', 'COMPATIBLE PRINTERS', 'HOW TO SET UP'], [
    ['Wi-Fi  (wireless)',
     'Brother MFC-L3770CDW  /  HP Color LaserJet M479fdw  /  Canon MF743Cdw  /  Canon PIXMA TR150  /  HP OfficeJet 200',
     'Use the printer control panel to join EMCOMM-NET. '
     'Enter the Wi-Fi password when prompted. '
     'The printer receives a 192.168.50.x address from the ASUS router automatically. '
     'All EMCOMM-NET devices discover it via Bonjour — no driver installation needed.'],
    ['Ethernet  (wired)',
     'Brother MFC-L3770CDW  /  HP Color LaserJet M479fdw  /  Canon MF743Cdw',
     'Run a CAT 6 cable from the printer Ethernet port to any spare UniFi Switch port (Ports 3 through 5). '
     'The printer receives an IP automatically. '
     'Set a static DHCP reservation in the ASUS router so the IP never changes between activations.'],
    ], [1.7*inch, 1.8*inch, CW-3.5*inch]))
story.append(SP(6))
story.append(H3('Reserve a Static IP for the Printer (Recommended)'))
story.append(CodeBlock([
    '# On the ASUS router web UI (http://192.168.50.1):',
    '# LAN → DHCP Server → Manually Assigned IP',
    '# Enter the printer MAC address → assign a fixed IP, e.g.: 192.168.50.10',
    '# Reboot the printer to pick up the reservation',
    '# Confirm: ping 192.168.50.10',
]))
story.append(SP(6))
story.append(H2('Printer Option Comparison'))
story.append(tbl(['', 'Option A — Client Printer', 'Option B — USB via Pi / CUPS', 'Option C — Network Printer'], [
    ['Pi configuration needed', 'None', 'CUPS (auto-installed)', 'None'],
    ['One printer for all operators', 'Each device needs own printer', 'Shared across EMCOMM-NET', 'Shared across EMCOMM-NET'],
    ['Works without internet', 'Yes', 'Yes', 'Yes'],
    ['iOS / AirPrint support', 'Requires AirPrint printer', 'Yes via CUPS + Avahi', 'Yes if AirPrint printer'],
    ['Battery printer support', 'Yes', 'Yes (USB connected)', 'Yes (Wi-Fi connected)'],
    ['Best for', 'Single operator or tablet with own printer', 'Any USB printer, shared to all devices', 'Wi-Fi/Ethernet printer already on site'],
], [1.6*inch, 1.6*inch, 1.8*inch, CW-5.0*inch]))
story.append(SP(4))
story.append(NoteBox('For most your callsign field activations, Option B (USB printer via CUPS) is recommended. '
                     'A Brother HL-L2350DW or HP LaserJet plugged into the Pi USB hub covers all ICS forms, '
                     'net logs, and cheat sheets needed for a typical activation.', 'tip'))
story.append(PB())

# ── STEP 9 — PAT WINLINK ─────────────────────────────────────────────────────
story.append(StepBox(9, 'Pat Winlink — Verify & Configure'))
story.append(SP(8))
story.append(H1('12. Step 9: Pat Winlink — Verify & Configure'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'Pat is an open-source Winlink client that runs directly on the Pi and is accessible '
    'from any browser on EMCOMM-NET at http://192.168.50.1:8090. '
    'The FieldCommand installer downloads and configures Pat automatically, so this step '
    'is primarily about verifying it is running and adding your Winlink account password.'))
story.append(SP(4))
story.append(P(
    'Pat serves as the backup Winlink path when the Windows laptop is unavailable, '
    'or for VHF Packet operations when a TNC is connected directly to the Pi. '
    'your organization primary Winlink operations use Winlink Express on the Windows laptop '
    '(Step 10). Pat is the fallback.'))
story.append(SP(6))
story.append(CodeBlock([
    '# Check pat.service status',
    'sudo systemctl status pat',
    '# If not running:',
    'sudo systemctl start pat && sudo systemctl enable pat',
    '# Confirm port 8090 is listening',
    'ss -tlnp | grep 8090',
    '# Add your Winlink password:',
    'sudo nano /opt/fieldcommand/.config/pat/config.json',
    '# Verify / update these fields:',
    '#   "mycall": "your callsign"                 ← set by installer',
    '#   "secure_login_password": "xxxxx"   ← add your Winlink password',
    '#   "http_addr": "0.0.0.0:8090"       ← must be 0.0.0.0 for EMCOMM-NET access',
]))
story.append(PB())

# ── STEP 10 — WINDOWS LAPTOP ─────────────────────────────────────────────────
story.append(StepBox(10, 'Windows Laptop — Winlink Express + JS8Call'))
story.append(SP(8))
story.append(H1('12. Step 10: Windows Laptop Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P('The Windows laptop is the primary HF digital station. It runs Winlink Express and JS8Call '
               'with the IC-7300 connected via a single USB cable. Connect the laptop to EMCOMM-NET '
               '(Wi-Fi) or the UniFi switch Port 3 (wired Ethernet).'))
story.append(SP(6))
story.append(H2('9.1  IC-7300 One-Time Radio Setup'))
story.append(tbl(['IC-7300 MENU PATH', 'SETTING'], [
    ['SET → Connectors → CI-V Baud Rate', '115200'],
    ['SET → Connectors → CI-V Transceive', 'ON'],
    ['SET → Connectors → USB Send/Keying → USB Send', 'RTS'],
    ['SET → Connectors → MOD Input → USB MOD Level', '40–50%'],
    ['COMP button (speech compression)', 'OFF'],
    ['Mode for digital operation', 'USB-D'],
], [2.5*inch, CW-2.5*inch]))
story.append(SP(6))
story.append(H2('9.2  Install Winlink Express + VARA HF'))
story.append(steps([
    'Download Winlink Express from: <b>winlink.org/client-software</b>. Run installer, accept defaults.',
    'On first launch: enter your callsign, Winlink password, and grid square <your grid> (your county).',
    'Settings → Radio Setup: Radio=IC-7300, Control Port=(check Device Manager), Baud Rate=115200, PTT via CAT=checked.',
    'Settings → Sound Card: Input=USB Audio CODEC (IC-7300), Output=USB Audio CODEC (IC-7300).',
    'Download and install VARA HF from: winlink.org → VARA → VARA HF Modem. Set same audio devices in VARA HF Settings.',
    'Test: Open a VARA HF session in Winlink Express → connect to any Winlink RMS gateway on 40m to confirm audio and CAT control work.',
]))
story.append(SP(6))
story.append(H2('9.3  Install JS8Call'))
story.append(steps([
    'Download JS8Call from: <b>js8call.com</b> → Windows installer. Run installer, accept defaults.',
    'Launch JS8Call. Open File → Settings (F2). General tab: My Call=<your callsign>, My Grid=<your grid square>.',
    'Audio tab: Input=USB Audio CODEC (IC-7300), Output=USB Audio CODEC (IC-7300).',
    'Radio tab: Rig=IC-7300, PTT Method=CAT, Serial Port=(same COM port as Winlink), Baud Rate=115200.',
    'Reporting tab (CRITICAL): TCP Server Hostname=<b>0.0.0.0</b> (MUST change from 127.0.0.1). Enable TCP Server API=checked. TCP Server Port=<b>2442</b>. Accept TCP Requests=checked.',
    'Click OK. Restart JS8Call for API settings to take effect.',
    'Set VFO to 7.078 MHz (JS8 40m calling frequency). Mode → Normal.',
]))
story.append(SP(6))
story.append(H2('9.4  Windows Firewall — Allow JS8Call Port 2442'))
story.append(CodeBlock([
    '1. Search "Windows Defender Firewall" → Advanced Settings',
    '2. Inbound Rules → New Rule → Port → TCP → Specific port: 2442 → Allow → All profiles',
    '3. Name the rule: JS8Call API',
]))
story.append(SP(6))
story.append(H2('9.5  Find the Windows Laptop IP on EMCOMM-NET'))
story.append(CodeBlock([
    '# Run in Windows Command Prompt:',
    'ipconfig',
    '# Note the IPv4 Address for the EMCOMM-NET adapter (e.g. 192.168.50.105)',
    '# Set a DHCP reservation (recommended — gives laptop a fixed IP):',
    '# ASUS Web UI → LAN → DHCP Server → Manually Assigned IP',
    '# Enter laptop MAC address → assign 192.168.50.2',
    '',
    '# Configure the FieldCommand dashboard JS8Call card:',
    '# 1. Connect to EMCOMM-NET, open http://192.168.50.1',
    '# 2. Find the JS8Call card (purple) in Amateur Radio section',
    '# 3. Tap/click the card',
    '# 4. Enter the Windows laptop IP (e.g. 192.168.50.105)',
    '# 5. Card saves IP and opens http://192.168.50.105:2442',
]))
story.append(SP(6))
story.append(tbl(['SWITCHING TO...', 'PROCEDURE'], [
    ['Winlink Express  (from JS8Call)',
     'Click Disconnect in JS8Call or close it.  '
     'Open VARA HF — it automatically reclaims the USB audio device.  '
     'Open Winlink Express and connect normally.'],
    ['JS8Call  (from Winlink)',
     'Finish any active Winlink transmission.  '
     'Close VARA HF.  Minimize Winlink Express.  '
     'Open JS8Call and click Connect — it reclaims the COM port and audio.'],
    ['Both simultaneously  (two radios)',
     'Connect a second HF radio via a separate USB audio and CAT interface.  '
     'Configure JS8Call to use that radio\'s COM port and audio device.  '
     'Both run at the same time without conflicts.'],
], [1.6*inch, CW-1.6*inch]))
story.append(PB())

# ── STEP 10b — SCS PACTOR MODEM ──────────────────────────────────────────────
story.append(StepBox('10b', 'SCS PACTOR Modem Setup  (Optional — High-Performance HF)'))
story.append(SP(8))
story.append(H1('Step 10b:  SCS PACTOR Modem Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'PACTOR is a high-performance HF digital mode used extensively in Winlink operations. '
    'It provides significantly better throughput than VARA HF on marginal or noisy HF paths, '
    'and is the only mode that supports PACTOR 4 compression on Winlink. '
    'SCS (Special Communications Systems) manufactures the only PACTOR-licensed TNCs available. '
    'A PACTOR TNC connects between the IC-7300 and the Windows laptop. '
    'This step is optional — Winlink via VARA HF works well for most activations.'))
story.append(SP(6))

story.append(H2('Supported SCS PACTOR Modems'))
story.append(tbl(['MODEL', 'PACTOR LEVEL', 'INTERFACE', 'NOTES'], [
    ['SCS Tracker DSP TNC',
     'PACTOR 1 / 2 / 3',
     'USB (COM port)',
     'Entry-level PACTOR TNC.  Good for most Winlink operations.  '
     'Also supports PACKET and ROBUST PR.  ~$250.'],
    ['SCS PTC-IIIusb',
     'PACTOR 1 / 2 / 3',
     'USB (COM port)',
     'Full-featured controller with front-panel display.  '
     'Supports PACTOR, PACKET, AMTOR, RTTY.  ~$650.'],
    ['SCS P4dragon DR-7400',
     'PACTOR 1 / 2 / 3 / 4',
     'USB (COM port)',
     'Top-of-line PACTOR 4 TNC.  Maximum throughput on HF.  '
     'Required for PACTOR 4 sessions.  ~$1,100.  '
     'Recommended for permanent EOC and EMCOMM stations.'],
], [2.0*inch, 1.4*inch, 1.2*inch, CW-4.6*inch]))
story.append(SP(6))

story.append(H2('Physical Connection'))
story.append(tbl(['FROM', 'TO', 'CABLE / NOTE'], [
    ['SCS TNC  —  AFSK audio output',
     'IC-7300  —  ACC jack audio input  or  3.5mm mic input',
     'SCS-supplied audio cable  (included with TNC)'],
    ['SCS TNC  —  AFSK audio input',
     'IC-7300  —  ACC jack audio output  or  3.5mm speaker output',
     'SCS-supplied audio cable  (included with TNC)'],
    ['SCS TNC  —  PTT output',
     'IC-7300  —  remote jack  (ACC or SEND)',
     'SCS-supplied PTT cable  (check your TNC model)'],
    ['SCS TNC  —  USB port',
     'Windows laptop  —  any USB-A port',
     'USB-A to USB-B or USB-A to micro-USB  (included with TNC)'],
], [1.8*inch, 2.2*inch, CW-4.0*inch]))
story.append(SP(4))
story.append(NoteBox(
    'If you are also using VARA HF via the IC-7300 USB audio:  '
    'configure the PACTOR TNC to use the IC-7300 ACC jack for audio, '
    'not the USB sound card.  '
    'This allows VARA (USB audio path) and PACTOR (ACC audio path) to coexist on the same radio.  '
    'Never transmit both modes simultaneously.', 'warn'))
story.append(SP(6))

story.append(H2('Configure Winlink Express for PACTOR'))
story.append(steps([
    'In Winlink Express, go to <b>Settings → Radio Setup</b>.',
    'Click <b>Add</b> to create a new radio entry.',
    'Set <b>Template</b> to:  <b>SCS PTC-IIx</b>  (works for all SCS PACTOR TNCs including the Tracker and P4dragon).',
    'Set <b>Control Port</b> to the COM port assigned to your SCS TNC.  '
    'Check Windows Device Manager → Ports (COM & LPT) to find the correct number.  '
    'The TNC appears as  "USB Serial Port  (COM X)".',
    'Set <b>Baud Rate</b> to <b>115200</b>.',
    'Leave <b>PTT via CAT</b> unchecked  —  the TNC handles PTT directly via the ACC cable.',
    'Click <b>OK</b> to save the radio profile.',
]))
story.append(SP(6))

story.append(H2('Open a PACTOR Winlink Session'))
story.append(steps([
    'In Winlink Express, click the session type dropdown and select <b>Open Session → PACTOR Winlink</b>.',
    'The session window opens.  The TNC initializes and you will see the SCS banner text in the session log.',
    'Set your frequency on the IC-7300 to a known Winlink RMS gateway frequency for your region.  '
    'Common 40m PACTOR frequencies:  7.038 MHz,  7.040 MHz,  7.103 MHz.',
    'Click <b>Start</b>.  Winlink Express scans for and connects to the nearest RMS gateway.',
    'The PACTOR handshake completes automatically — the session connects at the highest common level '
    '(PACTOR 1 through 4) that both stations support.',
    'Send and receive messages as normal.  '
    'PACTOR 4 typically completes a full ICS-213 exchange in under 2 minutes on a good path.',
]))
story.append(SP(6))

story.append(H2('Verify the TNC is Responding'))
story.append(CodeBlock([
    '# Method: use PuTTY or Windows Terminal to open a direct serial session',
    '# Open PuTTY  →  Connection type: Serial  →  COM port: (your TNC port)',
    '# Speed: 115200  →  click Open',
    '',
    '# Type the following TNC command:',
    'cmd',
    '# The TNC responds with its command prompt:  cmd:',
    '',
    '# Useful TNC verification commands:',
    'ver              # shows firmware version and TNC model',
    'status           # shows current operating status',
    'mycall YOURCALL  # replace YOURCALL with your FCC callsign',
    '',
    '# If the TNC does not respond:',
    '#   1. Confirm the correct COM port in Device Manager',
    '#   2. Confirm no other application has the COM port open',
    '#   3. Try baud rate 9600 (some TNC models default lower)',
]))
story.append(SP(4))
story.append(NoteBox(
    'PACTOR levels 3 and 4 require a separate Winlink license fee beyond the standard Winlink account.  '
    'PACTOR 1 and 2 are available to all licensed amateur radio operators at no additional cost.  '
    'The SCS TNC also supports AX.25 Packet, which Pat Winlink on the Pi can use via a KISS TCP connection '
    '(typically for VHF packet via a separate TNC or via the Digirig).  '
    'This provides a VHF backup to the HF PACTOR path.', 'note'))
story.append(PB())

# ── STEP 11 — FIRST BOOT ─────────────────────────────────────────────────────
story.append(StepBox(11, 'AMPRNet  /  44Net Gateway Setup'))
story.append(SP(8))
story.append(H1('Step 11:  AMPRNet / 44Net Gateway Setup'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))

# ── 44Net Connect Overview ────────────────────────────────────────────────────
story.append(H2('What is AMPRNet and 44Net Connect?'))
story.append(P(
    'AMPRNet — Amateur Packet Radio Network — is the global amateur radio IP network '
    'operating on the 44.0.0.0/8 address block, an entire Class A range permanently '
    'assigned by IANA to ARRL specifically for amateur radio use. '
    'Every licensed amateur radio operator in the world can apply for a block of '
    '44.x.x.x IP addresses. These addresses are globally routable and reachable by '
    'any other AMPRNet participant, whether over RF (packet radio, APRS, mesh) '
    'or via an encrypted internet tunnel.'))
story.append(SP(4))
story.append(P(
    '<b>44Net Connect</b> (connect.44net.cloud) is the current WireGuard-based tunneling '
    'service that makes AMPRNet accessible over the internet. '
    'The AMPRNet portal (portal.ampr.org) manages IP allocations and generates the '
    'WireGuard configuration for each registered operator. '
    'Once configured, the tunnel brings 44.0.0.0/8 directly to your gateway Pi — '
    'every device on EMCOMM-NET can reach any AMPRNet address worldwide '
    'as if it were a local IP address.'))
story.append(SP(8))

story.append(H2('Is AMPRNet Right for Your Deployment?'))
story.append(P(
    '<b>AMPRNet is beneficial when an amateur radio group is the lead organization '
    'or a key partner in the EMCOMM-NET deployment.</b> '
    'If FieldCommand is being deployed by or with an ARES, RACES, Amateur Radio Club, '
    'or other FCC-licensed amateur radio group, AMPRNet adds significant value: '
    'Winlink via radio-path gateways, APRS connectivity, inter-node FieldCommand '
    'communication, and access to a global amateur radio data network — '
    'all without touching the commercial internet.'))
story.append(SP(4))
story.append(P(
    '<b>If the deployment is primarily for public safety or served agency personnel '
    'without an amateur radio group involved, the AMPRNet gateway adds hardware '
    'cost and complexity with limited benefit.</b> '
    'FieldCommand IMS runs entirely without AMPRNet — all 49 web pages, ICS forms, '
    'FEMA documentation, net loggers, personnel accountability, and all other tools '
    'operate locally on EMCOMM-NET with no dependency on AMPRNet. '
    'The 44Net Gateway Pi is an optional enhancement, not a requirement.'))
story.append(SP(6))
story.append(tbl(['SCENARIO', 'AMPRNet RECOMMENDED?', 'REASON'], [
    ['ARES/RACES group leads the deployment',
     '✓ Yes — strong benefit',
     'Winlink via AMPRNet path, APRS-IS, inter-node data, global amateur station reach'],
    ['Amateur radio club operates the EOC comms',
     '✓ Yes — strong benefit',
     'Same as above — the licensed operators can register and maintain the allocation'],
    ['Amateur radio operators are supporting partners',
     '△ Consider — moderate benefit',
     'Beneficial if the licensed operators take ownership of the AMPRNet registration'],
    ['Public safety agency only — no amateur radio group',
     '✗ Not recommended',
     'Requires FCC amateur license for registration. Adds complexity with limited payoff.'],
    ['Municipal EOC with some licensed staff',
     '△ Consider — if a licensed operator leads',
     'One designated licensed operator can register under their callsign and maintain it'],
], [2.0*inch, 1.5*inch, CW-3.5*inch]))
story.append(SP(8))

story.append(H2('The Amateur Radio Group Must Lead This Process'))
story.append(NoteBox(
    'The AMPRNet registration and maintenance process requires an FCC-licensed '
    'amateur radio operator. It cannot be done by a public safety agency, '
    'a municipality, or an IT department acting alone. '
    'The IP block is assigned to a callsign, maintained under that callsign, '
    'and all use is subject to Part 97 rules. '
    'The amateur radio group must own this — the served agency or EOC cannot.',
    'warn'))
story.append(SP(6))
story.append(P(
    'In practical terms, this means the process should be initiated and led by '
    'the ARES Emergency Coordinator (EC), club President, or a designated '
    'technical lead who holds an FCC amateur license. '
    'The following organizational steps should happen before any hardware is purchased '
    'or any software is configured:'))
story.append(SP(4))
story.append(tbl(['STEP', 'WHO DOES IT', 'WHAT HAPPENS'], [
    ['Designate the AMPRNet technical lead',
     'ARES EC or club President',
     'Identify a licensed amateur (any class) who will own the registration, '
     'maintain the allocation, and be the point of contact for AMPRNet administrators. '
     'Their callsign becomes the registered callsign for the subnet.'],
    ['Coordinate with the regional AMPRNet administrator',
     'Designated technical lead',
     'AMPRNet is regionally administered. In Illinois, contact the Illinois AMPRNet '
     'coordinator (reachable via ARRL Illinois or the AMPRNet mailing list) '
     'to understand what address blocks are available in your area '
     'and to establish a relationship before submitting the formal request.'],
    ['Agree on the subnet size and naming',
     'Technical lead + club leadership',
     'A /29 gives 6 usable addresses (enough for one FieldCommand deployment plus growth). '
     'A /28 gives 14 addresses (suitable for multiple fixed and portable stations). '
     'The technical lead proposes this in the registration justification.'],
    ['Establish a club or group callsign if needed',
     'Club leadership',
     'The allocation can be under a personal callsign (e.g. KE4CON) or a club '
     'callsign (e.g. K9ESV). A club callsign is preferable for organizational '
     'deployments — it survives individual license changes and transfers more easily.'],
    ['Plan for long-term maintenance',
     'Club leadership + technical lead',
     'AMPRNet allocations are permanent but require the license to remain active '
     'and the portal account to be maintained. Identify a backup technical lead '
     'in case the primary moves or is unavailable at activation time.'],
], [0.9*inch, 1.6*inch, CW-2.5*inch]))
story.append(SP(8))

story.append(H2('What AMPRNet Enables — Capabilities and Restrictions'))
story.append(tbl(['CAPABILITY', 'DESCRIPTION', 'REQUIRES WAN?'], [
    ['Winlink via AMPRNet path',
     'Connect to Winlink RMS gateways that have 44.x.x.x addresses. '
     'Keeps Winlink traffic within the amateur radio network rather than the commercial internet. '
     'Useful when you want to avoid commercial internet dependency for message handling.',
     'Yes — WireGuard tunnel requires internet to establish, but once up, '
     'Winlink sessions travel over the 44-net tunnel'],
    ['APRS-IS via AMPRNet',
     'APRS-IS network servers are reachable on 44.x.x.x addresses. '
     'Configure Graywolf or YAAC to use the AMPRNet path instead of the public internet.',
     'Yes — same tunnel dependency'],
    ['Inter-node FieldCommand',
     'Two FieldCommand systems with 44Net gateways can share net log data, '
     'resource board status, and incident information over AMPRNet '
     'without routing through the commercial internet. '
     'Useful for multi-site EOC deployments.',
     'Yes — tunnel required'],
    ['Direct 44.x.x.x station access',
     'Any amateur station worldwide reachable on 44.x.x.x — '
     'whether via RF packet, mesh networking, or WireGuard — '
     'is directly addressable from any EMCOMM-NET device.',
     'Yes — tunnel required'],
    ['Static globally routable IP addresses',
     'Your 44.x.x.x block is permanently yours and globally routable. '
     'Other AMPRNet participants can reach your stations at a fixed address '
     'that never changes, regardless of your ISP or location.',
     'No — addresses are permanent; reachability requires tunnel'],
], [1.6*inch, 3.3*inch, CW-4.9*inch]))
story.append(SP(6))
story.append(NoteBox(
    '<b>Part 97 restrictions apply to all AMPRNet traffic:</b> '
    'No encryption of content (WireGuard tunnel encryption of transport is permitted). '
    'No commercial traffic. '
    'Station identification required. '
    'No third-party traffic unless authorized. '
    'AMPRNet is a tool for the amateur radio community — '
    'public safety agencies using it through an amateur radio group '
    'must ensure all traffic complies with Part 97.',
    'warn'))
story.append(SP(8))

story.append(H2('How to Get Your AMPRNet IP Allocation — Overview'))
story.append(P(
    'The process is straightforward but not fast. '
    'Allow <b>2–6 weeks</b> from initial registration to receiving a confirmed allocation. '
    'Regional administrators are volunteers and response times vary. '
    'Start this process well before your planned activation date.'))
story.append(SP(6))
story.append(tbl(['PHASE', 'ACTION', 'TIMELINE'], [
    ['1 — Coordinate locally',
     'Contact your regional AMPRNet coordinator before registering. '
     'Ask what blocks are available in your area, introduce your organization, '
     'and confirm they are aware of the incoming request. '
     'Illinois: check ARRL Illinois Section or the AMPRNet-Illinois mailing list.',
     '1–2 days'],
    ['2 — Create portal account',
     'Go to https://portal.ampr.org and register. '
     'Use your FCC callsign as your username. '
     'The portal verifies your license automatically against the FCC ULS database.',
     '1 day'],
    ['3 — Request subnet',
     'Log in → Subnets → Request Subnet. '
     'Select your region. '
     'Request a /29 (6 addresses) or /28 (14 addresses). '
     'In the justification field, describe your organization, your role in EMCOMM, '
     'the number of fixed and portable stations, and intended use. '
     'A clear, detailed justification speeds approval.',
     '1 day to submit'],
    ['4 — Wait for approval',
     'The regional AMPRNet administrator reviews your request and may contact you '
     'with questions. Once approved, your allocation appears in '
     'portal.ampr.org → Subnets → My Subnets with status Active.',
     '1–6 weeks'],
    ['5 — Download WireGuard config',
     'After approval, the portal generates a WireGuard configuration specific to '
     'your subnet. Download it — it contains your private key, your 44.x.x.x address, '
     'and the connect.44net.cloud endpoint details. '
     'Store this securely — it is the credential for your tunnel.',
     'Immediate after approval'],
    ['6 — Configure gateway Pi',
     'Follow Part B of this installation guide to configure the gateway Pi '
     'with the WireGuard config from the portal.',
     '1–2 hours'],
], [0.9*inch, 4.0*inch, CW-4.9*inch]))
story.append(SP(4))
story.append(NoteBox(
    'Keep a printed copy of your portal login, assigned subnet, and WireGuard '
    'configuration in your FieldCommand go-kit. '
    'If the gateway Pi needs to be rebuilt at a future activation, '
    'you will need these credentials. '
    'The portal generates a new WireGuard private key if needed — '
    'store the portal login credentials, not just the key file.',
    'tip'))
story.append(SP(8))

story.append(H2('AMPRNet in FieldCommand — What the Software Does'))

story.append(SP(4))
story.append(P(
    'The following files are part of FieldCommand and work together to provide '
    'integrated 44Net gateway support across both Pis:'))
story.append(SP(4))
story.append(tbl(['FILE', 'RUNS ON', 'PURPOSE'], [
    ['scripts/setup_44net.sh',
     'Gateway Pi  (192.168.50.2)',
     'Installer for the gateway Pi.  Sets up WireGuard, static IP, IP forwarding, '
     'status service, and Desktop autostart.  Run once on the gateway Pi.'],
    ['python/amprgate_status.py',
     'Gateway Pi  (192.168.50.2)',
     'Flask status service on port 9000.  Serves the gateway dashboard UI and '
     '/api/status JSON endpoint.  Installed by setup_44net.sh.'],
    ['systemd/amprgate-status.service',
     'Gateway Pi  (192.168.50.2)',
     'Systemd unit that keeps amprgate_status.py running.  '
     'Installed by setup_44net.sh.  Starts after wg-quick@ampr0.'],
    ['python/amprgate_poll.py',
     'FieldCommand Pi  (192.168.50.1)',
     'Polls the gateway Pi every 30 seconds and writes status to '
     '/opt/fieldcommand/data/amprgate_status.json for the dashboard.'],
    ['systemd/amprgate-poll.service',
     'FieldCommand Pi  (192.168.50.1)',
     'Systemd unit for the poll service.  '
     'Installed automatically by the FieldCommand install.sh.'],
    ['html/amprgate.html',
     'FieldCommand Pi  (192.168.50.1)',
     'Dashboard page at http://192.168.50.1/amprgate.html.  '
     'Shows tunnel state, AMPRNet address, traffic stats, and tunnel controls.'],
], [1.6*inch, 1.8*inch, CW-3.4*inch]))
story.append(SP(8))
story.append(P(
    'AMPRNet (Amateur Packet Radio Network) is the global amateur radio IP network '
    'using the reserved 44.0.0.0/8 address block assigned by IANA to ARRL. '
    'It provides licensed amateur radio operators with globally routable IP addresses '
    'reachable over RF links or via encrypted internet tunnels to the AMPRNet gateway. '
    'Adding a dedicated 44Net gateway Pi to FieldCommand gives every device on EMCOMM-NET '
    'full access to the AMPRNet — Winlink gateways, APRS-IS servers, Mesh networking '
    'nodes, and other amateur stations worldwide that are reachable on 44.x.x.x addresses.'))
story.append(SP(4))
story.append(NoteBox(
    'The 44Net Gateway Pi is completely separate from the FieldCommand server Pi. '
    'It runs WireGuard, ip routing, and a status page only. '
    'If the gateway goes down or needs reconfiguring, FieldCommand continues operating normally. '
    'This isolation was an intentional design choice — keep routing infrastructure '
    'separate from the communications server.',
    'note'))
story.append(SP(8))

story.append(H2('Part A  —  Get Your AMPRNet Allocation  (Do This First — Allow 2-4 Weeks)'))
story.append(P(
    'Before configuring any software, you need an AMPRNet IP address block assigned to your callsign. '
    'This is a one-time registration process managed by the AMPRNet administrators at ampr.org. '
    'The block you receive will be something like 44.x.x.x/29 (6 usable addresses) '
    'or 44.x.x.x/28 (14 usable addresses) depending on what is available in your region.'))
story.append(SP(6))
story.append(steps([
    '<b>Create an account at portal.ampr.org</b> — go to https://portal.ampr.org and click Register. '
    'You must use your callsign your callsign as your username. '
    'Verify your license via the FCC ULS lookup that the portal performs automatically.',
    '<b>Request a subnet allocation</b> — after logging in, click Subnets → Request Subnet. '
    'Select your region (Illinois — typically 44.24.x.x or 44.172.x.x range). '
    'Request a /29 block for a small deployment or a /28 if you anticipate growth. '
    'In the justification field, explain the your organization EMCOMM-NET deployment and intended use.',
    '<b>Coordinate with your regional AMPRNet administrator</b> — Illinois AMPRNet administration '
    'is coordinated through ARRL. You may be contacted by the regional admin for verification. '
    'Response times vary from days to several weeks. Be patient.',
    '<b>Receive your allocation</b> — you will get an email with your assigned 44.x.x.x/29 block. '
    'The portal will also show your allocation under Subnets → My Subnets. '
    'Record this allocation — you will need it in Part B.',
    '<b>Note your WireGuard endpoint credentials</b> — the portal provides a WireGuard '
    'configuration for your specific subnet. Download or copy this — it contains your '
    'private key, allowed IPs, and the amprgw.ampr.org endpoint address.',
]))
story.append(SP(4))
story.append(NoteBox(
    'ARRL membership is not required for an AMPRNet allocation, but a valid FCC amateur '
    'radio license (any class) is required. The your club or personal callsign is valid for this purpose. '
    'The allocation is tied to the callsign and is permanent as long as the license remains active.',
    'note'))
story.append(SP(8))

story.append(H2('Part B  —  Set Up the 44Net Gateway Pi'))
story.append(P(
    'Once you have your AMPRNet allocation, the following steps configure the dedicated '
    'gateway Pi running in the Argon NEO 5 case. '
    'This Pi should be freshly flashed with Raspberry Pi OS Lite (64-bit). '
    'It does not need the FieldCommand installer — it runs WireGuard and routing only.'))
story.append(SP(6))

story.append(H3('B.1  Initial OS Setup'))
story.append(P(
    'Flash Raspberry Pi OS Desktop (64-bit) to the M.2 SATA SSD using Raspberry Pi Imager. '
    'Desktop is used on the gateway Pi so any team member can check tunnel status '
    'from the local keyboard and monitor without SSH. '
    'Chromium opens the status page automatically on login. '
    'During Imager advanced options set:'))
story.append(SP(4))
story.append(tbl(['OPTION', 'VALUE'], [
    ['Hostname',  'amprgate.local  —  discoverable as amprgate.local on EMCOMM-NET'],
    ['Username',  'amprgate  —  used by the gateway setup script'],
    ['Password',  'Choose a strong password and record it with the FieldCommand credentials'],
    ['Enable SSH','Yes  —  useful for remote diagnostics if the monitor is not available'],
    ['Wi-Fi',     'Your home or lab Wi-Fi for initial package downloads  —  switched to wired EMCOMM-NET after setup'],
    ['Locale',    'US/Central  —  matches the FieldCommand Pi for consistent log timestamps'],
], [1.6*inch, CW-1.6*inch]))
story.append(SP(6))

story.append(H3('B.2  Assign Static IP and Install WireGuard'))
story.append(CodeBlock([
    '# SSH into the gateway Pi',
    'ssh amprgate@[current-pi-ip]',
    '',
    '# Update packages',
    'sudo apt-get update && sudo apt-get full-upgrade -y',
    '',
    '# Install WireGuard',
    'sudo apt-get install -y wireguard wireguard-tools',
    '',
    '# Set static IP on eth0',
    'sudo nmcli con mod "Wired connection 1",' +
    '    ipv4.addresses 192.168.50.2/24,' +
    '    ipv4.gateway 192.168.50.254,' +
    '    ipv4.dns "8.8.8.8 8.8.4.4",' +
    '    ipv4.method manual',
    'sudo nmcli con up "Wired connection 1"',
    '',
    '# Verify',
    'ip addr show eth0',
    '# Expected: inet 192.168.50.2/24',
]))
story.append(SP(6))

story.append(H3('B.3  Configure the WireGuard Tunnel'))
story.append(P(
    'The AMPRNet portal provides a WireGuard configuration specific to your subnet. '
    'The following is the general structure — replace the placeholder values with '
    'the actual values from your portal allocation.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Create the WireGuard config directory',
    'sudo mkdir -p /etc/wireguard',
    'sudo chmod 700 /etc/wireguard',
    '',
    '# Create the tunnel config file',
    'sudo nano /etc/wireguard/ampr0.conf',
    '',
    '# Paste the following — replace ALL values in [brackets] with your portal values:',
    '[Interface]',
    'PrivateKey = [your-private-key-from-portal]',
    'Address = [your-44.x.x.x/29-address]',
    'ListenPort = 51820',
    'PostUp   = ip route add 44.0.0.0/8 dev ampr0',
    'PostUp   = iptables -A FORWARD -i ampr0 -j ACCEPT',
    'PostUp   = iptables -A FORWARD -o ampr0 -j ACCEPT',
    'PostUp   = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE',
    'PostDown = ip route del 44.0.0.0/8 dev ampr0',
    'PostDown = iptables -D FORWARD -i ampr0 -j ACCEPT',
    'PostDown = iptables -D FORWARD -o ampr0 -j ACCEPT',
    'PostDown = iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE',
    '',
    '[Peer]',
    'PublicKey = [amprnet-gateway-public-key-from-portal]',
    'Endpoint  = amprgw.ampr.org:51820',
    'AllowedIPs = 44.0.0.0/8',
    'PersistentKeepalive = 25',
]))
story.append(SP(6))

story.append(H3('B.4  Enable IP Forwarding and Start the Tunnel'))
story.append(CodeBlock([
    '# Enable IP forwarding (required for routing between EMCOMM-NET and AMPRNet)',
    'echo "net.ipv4.ip_forward = 1" | sudo tee -a /etc/sysctl.conf',
    'sudo sysctl -p',
    '',
    '# Start the WireGuard tunnel',
    'sudo wg-quick up ampr0',
    '',
    '# Enable at boot',
    'sudo systemctl enable wg-quick@ampr0',
    '',
    '# Check tunnel status',
    'sudo wg show ampr0',
    '# Expected: shows latest handshake, transfer stats, allowed IPs',
    '',
    '# Test reachability into AMPRNet',
    'ping 44.0.0.1 -c 4',
    '# Expected: replies from 44.0.0.1 (AMPRNet gateway)',
]))
story.append(SP(6))

story.append(H3('B.5  Access Control — Who Can Reach What'))
story.append(P(
    'FieldCommand restricts access to the 44Net gateway on two levels. '
    'This is both a security measure and a Part 97 compliance measure — '
    'only licensed amateur radio operators should be able to view or control '
    'the AMPRNet gateway.'))
story.append(SP(4))
story.append(tbl(['PORT', 'ACCESSIBLE FROM', 'AUTH REQUIRED', 'PROVIDES'], [
    ['Port 9000  (0.0.0.0)',
     'Any EMCOMM-NET device  (192.168.50.x)',
     'None for /api/status  (machine poll).  Valid FCC callsign for web UI.',
     'Read-only status JSON.  Callsign-authenticated web dashboard.'],
    ['Port 9001  (127.0.0.1)',
     'Gateway Pi keyboard only  (localhost — not reachable from network)',
     'Valid callsign session from port 9000 login.  Physical presence required.',
     'Tunnel control: up / down / restart.'],
    ], [1.4*inch, 1.6*inch, 1.8*inch, CW-4.8*inch]))
story.append(SP(4))
story.append(NoteBox(
    'Tunnel controls (up/down/restart) are intentionally inaccessible from the network. '
    'An operator who wants to restart the WireGuard tunnel must sit at the gateway Pi keyboard, '
    'open Chromium, log in with their FCC callsign, and use the local control interface. '
    'This prevents accidental or unauthorized tunnel disruption from operator laptops or phones. '
    'The FieldCommand Pi polling service reads /api/status on port 9000 without authentication '
    '— this is a read-only machine-to-machine call and is intentional.',
    'note'))
story.append(SP(6))
story.append(H3('B.5  Advertise the 44Net Route to EMCOMM-NET Devices'))
story.append(P(
    'For other devices on EMCOMM-NET to use the 44Net gateway automatically, '
    'the ASUS router needs to push a static route to all DHCP clients. '
    'This tells every device: "to reach anything in 44.0.0.0/8, use 192.168.50.2".'))
story.append(SP(4))
story.append(steps([
    'Open the ASUS router admin at <b>http://192.168.50.254</b>.',
    'Go to <b>LAN → Route</b>.',
    'Click <b>Add</b> and enter: Network/Host IP = <b>44.0.0.0</b>, '
    'Netmask = <b>255.0.0.0</b>, Gateway = <b>192.168.50.2</b>, Interface = <b>LAN</b>.',
    'Click <b>Apply</b>.',
    'On any EMCOMM-NET device, verify the route was received:',
]))
story.append(CodeBlock([
    '# On any EMCOMM-NET device (Pi 500, Windows laptop, etc.)',
    'ip route show | grep 44',
    '# Expected: 44.0.0.0/8 via 192.168.50.2 dev eth0',
    '',
    '# Windows equivalent (Command Prompt)',
    'route print | find "44."',
    '# Expected: 44.0.0.0  0.0.0.0  192.168.50.2  ...',
    '',
    '# Test from the FieldCommand Pi',
    'ping 44.0.0.1 -c 4',
    '# If reachable, FieldCommand can now connect to AMPRNet resources',
]))
story.append(SP(6))

story.append(H3('B.6  Gateway Status Page'))
story.append(P(
    'Install a lightweight status page on the 44Net Pi so operators can verify '
    'the tunnel state from any EMCOMM-NET browser without SSH access. '
    'This is a small Flask application that displays tunnel status, '
    'connected peers, and recent handshake times.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Install Python and Flask on the 44Net Pi',
    'sudo apt-get install -y python3 python3-pip python3-venv',
    'python3 -m venv /opt/amprgate/venv',
    '/opt/amprgate/venv/bin/pip install flask',
    '',
    '# Create the status app',
    'sudo mkdir -p /opt/amprgate',
    'sudo nano /opt/amprgate/status.py',
    '',
    '# Paste the following into status.py:',
    '# ---',
    'from flask import Flask, jsonify',
    'import subprocess, json',
    'app = Flask(__name__)',
    '',
    '@app.route("/")',
    'def index():',
    '    return open("/opt/amprgate/status.html").read()',
    '',
    '@app.route("/api/status")',
    'def status():',
    '    wg = subprocess.run(["sudo","wg","show","ampr0","dump"],',
    '        capture_output=True, text=True).stdout',
    '    lines = [l.split("\t") for l in wg.strip().split("\n") if l]',
    '    return jsonify({"tunnel":"up" if lines else "down","peers":len(lines)-1})',
    '',
    'if __name__ == "__main__":',
    '    app.run(host="0.0.0.0", port=9000)',
    '# ---',
    '',
    '# Create systemd service',
    'sudo nano /etc/systemd/system/amprgate-status.service',
    '# Paste:',
    '[Unit]',
    'Description=AMPRNet Gateway Status Page',
    'After=network.target wg-quick@ampr0.service',
    '',
    '[Service]',
    'User=amprgate',
    'ExecStart=/opt/amprgate/venv/bin/python /opt/amprgate/status.py',
    'Restart=always',
    '',
    '[Install]',
    'WantedBy=multi-user.target',
    '',
    'sudo systemctl enable --now amprgate-status',
    '# Status page now at: http://192.168.50.2:9000',
]))
story.append(SP(8))

story.append(H2('Part C  —  What You Can Do on AMPRNet'))
story.append(P(
    'Once the gateway is operational and the route is advertised to EMCOMM-NET, '
    'every device on EMCOMM-NET has full access to the AMPRNet. '
    'Here are the most useful applications for your organization operations:'))
story.append(SP(6))
story.append(tbl(['APPLICATION', 'HOW IT USES 44NET', 'ACCESS FROM EMCOMM-NET'], [
    ['Winlink via AMPRNet',
     'Some Winlink RMS gateways have 44.x.x.x addresses. '
     'Pat Winlink on the FieldCommand Pi can connect to them directly over the AMPRNet tunnel '
     'rather than the commercial internet — useful when only amateur radio paths are available.',
     'Pat Winlink at http://192.168.50.1:8090  Add AMPRNet RMS in Pat settings'],
    ['APRS-IS via AMPRNet',
     'The APRS-IS network has servers reachable on 44.x.x.x. '
     'Graywolf and YAAC can connect to APRS-IS via the AMPRNet path, '
     'keeping APRS traffic within the amateur radio network.',
     'Configure APRS-IS server address in Graywolf or YAAC settings'],
    ['Inter-node FieldCommand',
     'If another your organization station runs a second FieldCommand system with its own 44Net gateway, '
     'the two systems can share net data and resource boards over AMPRNet '
     'without routing traffic through the commercial internet.',
     'Future capability — requires second FieldCommand deployment'],
    ['HamSphere / Echolink via AMPRNet',
     'Some VoIP amateur radio nodes are reachable on 44.x.x.x addresses, '
     'providing RF-to-AMPRNet linking without commercial internet dependency.',
     'Direct connection to 44.x.x.x node addresses'],
    ['Direct amateur station communication',
     'Any amateur station worldwide with a 44.x.x.x address '
     '(whether via RF packet or WireGuard tunnel) is directly reachable '
     'from any EMCOMM-NET device for data exchange, file transfer, or status checking.',
     'Direct TCP/IP connections to 44.x.x.x addresses'],
    ], [2.1*inch, CW-2.1*inch]))
story.append(SP(6))
story.append(NoteBox(
    'AMPRNet does not carry voice traffic and is not a replacement for your radio links. '
    'It is a data network for IP-based amateur radio applications. '
    'All traffic on AMPRNet is subject to Part 97 rules — no encryption of content, '
    'no commercial traffic, licensed operator identification required. '
    'WireGuard encryption of the tunnel itself is permitted as it is the transport, '
    'not the content.',
    'note'))
story.append(SP(8))

story.append(H2('Part D  —  Verification Checklist'))
story.append(tbl(['CHECK', 'COMMAND / METHOD', 'EXPECTED RESULT'], [
    ['AMPRNet portal shows allocation',
     'Login to portal.ampr.org → Subnets → My Subnets',
     'Your 44.x.x.x/29 block shows Status: Active'],
    ['WireGuard tunnel is up on gateway Pi',
     'SSH to 192.168.50.2 then: sudo wg show ampr0',
     'Shows latest handshake within last 2 minutes'],
    ['AMPRNet gateway reachable from gateway Pi',
     'ping 44.0.0.1 -c 4',
     'Replies received — round trip time typically 10-50 ms'],
    ['EMCOMM-NET devices have 44 route',
     'ip route show | grep 44  (on any EMCOMM-NET device)',
     '44.0.0.0/8 via 192.168.50.2'],
    ['AMPRNet reachable from FieldCommand Pi',
     'ping 44.0.0.1 -c 4  (on FieldCommand Pi)',
     'Replies received'],
    ['Status page accessible',
     'Open http://192.168.50.2:9000 in any browser on EMCOMM-NET',
     'Shows callsign login page — enter a valid FCC callsign to proceed'],
    ['Callsign login works',
     'Enter your callsign at http://192.168.50.2:9000 login page',
     'FCC database validates callsign — dashboard loads showing tunnel status'],
    ['Access log recording',
     'SSH to gateway Pi: tail /var/log/amprgate-access.log',
     'Shows LOGIN-OK entry with your callsign, IP, and license class'],
    ['Tunnel control blocked from network',
     'From a laptop on EMCOMM-NET: curl http://192.168.50.2:9001',
     'Connection refused — port 9001 is localhost-only'],
    ['AMPRNet reachable from Pi 500 workstation',
     'Open http://192.168.50.2:9000 in Chromium on Pi 500',
     'Status page loads and shows tunnel UP'],
], [1.8*inch, 1.6*inch, 1.5*inch, CW-4.9*inch]))
story.append(PB())

story.append(StepBox(12, 'First Boot Verification  —  Full System'))
story.append(SP(8))
story.append(H1('Step 12:  First Boot Verification'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(4))
story.append(P(
    'After the installer completes and the Pi reboots, run through this verification checklist '
    'before handing off the system. Every service should show "active" and the dashboard '
    'should load cleanly from another device on EMCOMM-NET. '
    'If anything is not running, the troubleshooting section at the end of this guide '
    'covers the most common issues and their fixes.'))
story.append(SP(6))
story.append(CodeBlock([
    '# Check all FieldCommand services',
    'for svc in fcc-lookup health-monitor deadmans ics-platform kiwix nginx pat; do',
    '  echo "$svc: $(systemctl is-active $svc)"',
    'done',
    '',
    '# Test the dashboard from the Pi itself',
    'curl -s http://localhost/ | head -5',
    '# Test API endpoints',
    'curl http://localhost:5050/health      # FCC API health check',
    'curl http://localhost:5051/health      # System health monitor',
    '# Verify Pi has the correct static IP',
    'ip addr show eth0',
    '# Should show: inet 192.168.50.1/24',
]))
story.append(PB())

# ── REFERENCE SECTIONS ────────────────────────────────────────────────────────
story.append(H1('14. Network Architecture Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(H2('Full Network Topology'))
story.append(P(
    'The EMCOMM-NET deployment uses the ASUS RT-BE58 Go as the Wi-Fi access point and DHCP server. '
    'The the cellular antenna unit Drum provides primary cellular WAN (your cellular carrier) via a PoE Ethernet '
    'cable directly to the ASUS WAN port. '
    'satellite dish provides automatic secondary WAN failover via the ASUS USB WAN port. '
    'The UniFi Switch Lite 16 PoE distributes wired connections to both Pi servers, '
    'all operator workstations, the network printer, and additional field devices. '
    'The 44Net Gateway Pi routes the 44.0.0.0/8 AMPRNet address block for all EMCOMM-NET devices '
    'via a WireGuard tunnel to amprgw.ampr.org.'))
story.append(SP(6))
story.append(tbl(['DEVICE', 'IP ADDRESS', 'ROLE', 'CONNECTION'], [
    ['ASUS RT-BE58 Go', '192.168.50.254  (LAN gateway)',
     'Wi-Fi 7 AP + DHCP server + WAN gateway',
     'WAN: site Ethernet, satellite dish, or USB tether (optional).  EMCOMM-NET SSID on 2.4 GHz and 5 GHz.'],
    ['UniFi Switch Lite 16 PoE', 'N/A  (Layer 2 switch)',
     'Wired distribution hub  —  16 ports',
     'Port 1 uplink to ASUS router.  Ports 2-16 to all wired devices.'],
    ['FieldCommand Pi 5  (Pironman MAX 5)', '192.168.50.1  (static)',
     'FieldCommand application server  All EmComm tools and services',
     'Wired GbE via UniFi Switch Port 2.  Does not run Wi-Fi.'],
    ['44Net Gateway Pi 5  (Argon NEO 5)', '192.168.50.2  (static)',
     'AMPRNet / 44Net WireGuard gateway  Routes 44.0.0.0/8 for EMCOMM-NET',
     'Wired GbE via UniFi Switch Port 3.  WireGuard tunnel to amprgw.ampr.org.'],
    ['Windows Laptop', '192.168.50.3  (DHCP reservation)',
     'Winlink Express + JS8Call  IC-7300 HF station',
     'Wired via Port 4 or Wi-Fi (EMCOMM-NET).'],
    ['Color MFP Printer', '192.168.50.10  (DHCP reservation)',
     'Network printer shared to all devices',
     'Wired via Port 5 or Wi-Fi (EMCOMM-NET).'],
    ['Pi 500 Workstations x4', '192.168.50.20-23  (DHCP reservations)',
     'Operator browser stations',
     'Wired via Ports 6-9 or Wi-Fi (EMCOMM-NET).'],
    ['ASUS RT-BE58 Go  Mesh Node 1', 'Managed by AiMesh',
     'EMCOMM-NET extension  (same SSID, seamless roaming)',
     'Wired backhaul via UniFi Port 11.  Extends coverage to secondary zone.'],
    ['ASUS RT-BE58 Go  Mesh Node 2', 'Managed by AiMesh',
     'EMCOMM-NET extension  (same SSID, seamless roaming)',
     'Wired backhaul via UniFi Port 12.  Extends coverage to third zone.'],
    ['Field Devices  (phones, tablets, laptops)', '192.168.50.100-200  (DHCP)',
     'Additional operator browsers',
     'Wi-Fi — EMCOMM-NET — roam between primary and mesh nodes automatically.'],
], [1.6*inch, 1.1*inch, 1.6*inch, CW-4.3*inch]))
story.append(SP(6))
story.append(NoteBox(
    'Recommended: set the ASUS router LAN IP to 192.168.50.254 and the Pi static IP to 192.168.50.1. '
    'This keeps the FieldCommand URL clean and the router admin clearly separate at http://192.168.50.254.',
    'tip'))
story.append(PB())

story.append(H1('13. Web Dashboard Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P(
    'FieldCommand IMS serves 49 web pages from the Pi. All are accessible at '
    'http://192.168.50.1/[page]. Pages marked WAN require internet for live data '
    'but load and display cached data when offline.',
    S('B', fontSize=9, leading=13)))
story.append(SP(6))
story.append(tbl(['PAGE', 'URL', 'NOTES'], [
    ['Dashboard (All-Hazards ICS)',  '/', 'Main hub — 3 modes, WAN status bar, tool cards. Default entry point.'],
    ['Organization Setup',           '/setup.html', 'Configure org name, callsign, grid square, time zone, SSID'],
    ['Preflight Check',              '/preflight.html', 'GO/CAUTION/NO-GO readiness. Run before every activation.'],
    ['Incident Management',          '/incident.html', 'Create/manage incidents, operational periods, incident type'],
    ['Incident Archive/Reset',       '/incident_mgmt.html', 'Archive to USB · Restore · Hard delete · Beta/Scenario Reset'],
    ['Event Templates',              '/event_templates.html', '6 built-in templates (Shelter/SAR/HazMat/Weather/Gathering/Exercise)'],
    ['General Info / ICS-201',       '/general_info.html', 'Initial incident briefing — situation summary, initial actions'],
    ['ICS Platform — Overview',      '/ics/index.html', 'Five-section ICS structure navigator'],
    ['ICS — Command Section',        '/ics/command.html', 'ICS-202 objectives, ICS-208 safety, staff roster, position checklists'],
    ['ICS — Operations Section',     '/ics/operations.html', 'T-card board, resource status, assignment, T-card personnel roster'],
    ['ICS — Planning Section',       '/ics/planning.html', 'IAP assembly, ICS-205/206/209/211/221 forms, Planning P cycle'],
    ['ICS — Logistics Section',      '/ics/logistics.html', 'ICS-205 comms (COML), ICS-206 medical (MEDL), channel library'],
    ['ICS — Finance/Admin',          '/ics/finance.html', 'FEMA PA cost tracking, ICS-214 log, expenditure summary'],
    ['Planning P Cycle Guide',       '/ics/planningp.html', '15-phase IAP cycle with agenda, required forms, attendees per phase'],
    ['T-Card Resource Board',        '/resources.html', 'Add/status/assign resources. T-card personnel roster per card.'],
    ['NIMS Resource Types',          '/resource_types.html', 'Pre-loaded NIMS types + custom types. Available in T-card board.'],
    ['GPS Resource Map',             '/resource_map.html', 'Live GPS pins per T-card — 3 placement methods, auto-refresh 30s'],
    ['Starcom Resource Map',         '/resmap.html', 'Public safety unit positioning map with zone drawing tools'],
    ['ICS-213 General Message',      '/ics213.html', 'Formal message with digital signature, print, Winlink export'],
    ['ICS-214 Activity Log',         '/ics214.html', 'Unit activity log — export hours directly to FEMA labor costs'],
    ['ICS-309 Comms Log',            '/ics309.html', 'Manual communications log with incident archiving'],
    ['ICS-204A Briefing Sheet',      '/briefing_204a.html', 'Assignment briefing for branch/division supervisors'],
    ['ICS Form Suite',               '/ics-form.html', 'Full ICS form set: ICS-202 through ICS-221 with digital signatures'],
    ['IAP Assembly',                 '/iap.html', 'IAP tracker — all forms for active incident with completion status'],
    ['IAP Compile (PDF)',            '/iap_compile.html', 'One-click IAP PDF: title page + section dividers + all forms'],
    ['FEMA PA Cost Documentation',   '/fema_costs.html', 'Force Account Labor, Equipment, Materials, Contracts, PW export'],
    ['FEMA Equipment Rates',         '/fema_rates.html', '44 FEMA equipment categories — edit rates, track rate year'],
    ['Cost Dashboard',               '/cost_dashboard.html', 'Live cost totals by category, burn rate, budget tracker, by period'],
    ['Personnel Accountability',     '/accountability.html', 'PAR board — ICS-211, T-card personnel, Unaccounted, Cross-Reference'],
    ['ICS-211 Check-In',             '/checkin.html', 'Manual ICS-211 check-in form with active list and Check Out buttons'],
    ['QR/Barcode Scan Check-In',     '/scan_checkin.html', 'Camera scan or manual ID fallback. BarcodeDetector API, no library.'],
    ['Member Roster',                '/roster.html', 'Directory with certs, equipment, QR code generation, CSV import/export'],
    ['Amateur Net Control Logger',   '/netcontrol.html', 'Multi-net, FCC autofill, check-in/out, traffic, ICS-309, observer link'],
    ['Public Safety Net Logger',     '/starcom.html', 'Radio ID check-in, Starcom/P25 nets, ICS-309 export'],
    ['Net Observer Mode',            '/observer.html', 'Read-only net view, auto-refresh 15s. Share URL with EOC.'],
    ['Dead Man\x27s Switch',        '/deadmans.html', 'Audible alert if net goes silent beyond configured interval'],
    ['Tactical APRS Map',            '/tactical.html', 'Leaflet — RF APRS always, APRS-IS when WAN up, SARTopo overlay'],
    ['SARTopo GeoJSON Import',       '/sartopo_import.html', 'Import planning overlays from SARTopo — persists on tactical map'],
    ['NEXRAD Radar',                 '/radar.html', 'WAN REQUIRED. Animated NEXRAD loop — play/pause/scrub/speed/palette'],
    ['NWS/HF Propagation',          '/propagation.html', 'WAN: SFI, K-index, A-index from NOAA SWPC. Band-by-band conditions.'],
    ['FCC Callsign Lookup',          '/callsign.html', 'Offline — 800K+ US licensees in local SQLite. Instant results.'],
    ['NTS Radiogram Generator',      '/nts.html', 'ARRL-format traffic with auto word count. Print or log.'],
    ['Winlink Form Import',          '/winlink-import.html', 'Import Winlink Express XML forms into incident archive'],
    ['AMPRNet Gateway Status',       '/amprgate.html', '44Net WireGuard tunnel status, callsign auth, Part 97 access log'],
    ['WAN Status Detail',            '/wan-status.html', 'Both WAN sources, detection method, last check, event log'],
    ['WAN Settings',                 '/wan_settings.html', 'Configure WAN sources: role, type, detection method, enable/disable'],
    ['Hospital Directory',           '/hospitals.html', 'Trauma level, helipad, phone. Feeds ICS-206 medical plan.'],
    ['Facilities Directory',         '/facilities.html', 'ICP, staging, shelters, supply depots. Links to T-card assignments.'],
    ['Repeater Database',            '/repeaters.html', 'Filter by band/mode/CTCSS. Feeds ICS-205 channel picker.'],
    ['Channel Library',              '/channel_library.html', 'Pre-loaded interop channels (NIFOG/VTAC). Add custom agency channels.'],
    ['Grid Square Calculator',       '/grid.html', 'Grid ↔ lat/lon · distance and bearing between two grids'],
    ['Radio Cheat Sheets',           '/cheatsheets.html', 'Phonetic alphabet, Q-codes, RST scale, ICS structure, HF frequencies'],
    ['ICS Position Checklists',      '/position_checklists.html', 'NIMS activation checklists for all ICS positions'],
    ['Meeting Scheduler',            '/meetings.html', 'Schedule operational briefings — time, location, attendees'],
    ['Print Center',                 '/printcenter.html', 'Print any ICS form or document to any CUPS printer on EMCOMM-NET'],
    ['Reference Library',            '/refs.html', 'Kiwix offline — WikiMed, Wikipedia, iFixit. No internet needed.'],
    ['Health Monitor',               ':5051/health', 'Live CPU/memory/disk/temp, all service status, GPS, internet'],
    ['Pat Winlink Client',           ':8090', 'Browser-based Winlink client (Packet, VARA HF, Telnet)'],
    ['Kiwix Library',                ':8080/', 'Offline Wikipedia, WikiMed, iFixit, Wikivoyage'],
], [1.8*inch, 1.65*inch, CW-3.45*inch]))

story.append(H1('14. Service & Port Reference'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P(
    'All services run on the FieldCommand Pi (192.168.50.1) unless noted. '
    'The AMPRNet gateway runs on a separate Pi (192.168.50.2).',
    S('B', fontSize=9, leading=13)))
story.append(SP(6))
story.append(tbl(['PORT', 'SERVICE', 'SYSTEMD UNIT', 'DESCRIPTION'], [
    ['80',   'nginx',             'nginx.service',              'Web frontend — all 49 HTML pages, static assets'],
    ['5050', 'FCC Lookup Server', 'fieldcommand-fcc.service',   'FCC callsign lookup, org config, incidents, net logs'],
    ['5051', 'ICS Platform',      'fieldcommand-main.service',  'ICS forms, T-cards, check-ins, FEMA costs, GPS, PAR'],
    ['8080', 'Kiwix Library',     'kiwix.service',              'Offline reference — WikiMed, Wikipedia, iFixit'],
    ['8090', 'Pat Winlink',       'pat.service',                'Winlink email-over-radio — Packet, VARA HF, VARA FM'],
    ['631',  'CUPS Printer',      'cups.service',               'USB printer shared to all EMCOMM-NET devices'],
    ['2442', 'JS8Call',           '(laptop app)',               'HF digital keyboard messaging — web API on Windows laptop'],
    ['9000', 'AMPRNet Status',    'amprgate-status.service',    'AMPRNet gateway read-only status — public on EMCOMM-NET'],
    ['9001', 'AMPRNet Control',   'amprgate-status.service',    'Tunnel control — localhost only on gateway Pi'],
], [0.6*inch, 1.8*inch, 2.0*inch, CW-4.4*inch]))
story.append(SP(6))
story.append(H2('Background Services'))
story.append(SP(4))
story.append(tbl(['SYSTEMD UNIT', 'FUNCTION'], [
    ['fieldcommand-main.service',    'ICS platform server (port 5051) — T-cards, FEMA, PAR, GPS, check-in'],
    ['fieldcommand-fcc.service',     'FCC lookup + org config server (port 5050)'],
    ['wan-monitor.service',          'WAN source monitoring and automatic failover every 30 seconds'],
    ['wan-monitor.timer',            'Timer that keeps wan-monitor running on schedule'],
    ['amprgate-status.service',      '44Net gateway status API (ports 9000/9001 on gateway Pi)'],
    ['amprgate-poll.service',        '44Net WireGuard tunnel keepalive and reconnect on gateway Pi'],
    ['backup.service / backup.timer','Nightly SQLite backup to labelled USB drive'],
    ['kiwix.service',                'Kiwix offline reference library server (port 8080)'],
    ['pat.service',                  'Pat Winlink radio email client (port 8090)'],
    ['nginx.service',                'Web frontend — serves all HTML pages and static assets (port 80)'],
    ['cups.service',                 'CUPS print server — shares USB printer to EMCOMM-NET'],
], [2.4*inch, CW-2.4*inch]))


story.append(H1('15. New Feature Configuration'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(P(
    'FieldCommand IMS v1.0 includes the following features beyond the base ICS platform. '
    'Most require no additional setup — they are available immediately after installation. '
    'Items that require initial configuration are noted below.',
    S('B', fontSize=9, leading=13)))
story.append(SP(8))

story.append(H2('15.1  Personnel Accountability (PAR)'))
story.append(P(
    'The Personnel Accountability page (/accountability.html) is available immediately '
    'after installation. No additional setup is required. '
    'It reads from the same checkin_entries and tcard_personnel database tables '
    'that are created during normal installation.', S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(tbl(['FEATURE', 'SETUP REQUIRED'], [
    ['ICS-211 check-in with Check Out button', 'None — available at /checkin.html immediately'],
    ['QR/barcode scan check-in', 'None — available at /scan_checkin.html. Camera permission required on device.'],
    ['PAR board with cross-reference', 'None — available at /accountability.html immediately'],
    ['T-card personnel roster', 'None — Personnel tab appears on every T-card detail panel'],
    ['Check-out recording', 'None — Check Out button on every check-in row in checkin.html and accountability.html'],
], [2.8*inch, CW-2.8*inch]))
story.append(SP(8))

story.append(H2('15.2  FEMA PA Cost Documentation'))
story.append(P(
    'FEMA cost tracking is available immediately. The 2025 FEMA Schedule of Equipment Rates '
    '(44 categories) is pre-loaded during installation. '
    'Update rates annually at /fema_rates.html when FEMA publishes a new schedule.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(tbl(['FEATURE', 'NOTES'], [
    ['Force Account Labor with fringe calculation', 'Available immediately. ICS-214 import available from the Labor tab.'],
    ['Equipment with FEMA rate schedule lookup', '44 rates pre-loaded for 2025. Edit at /fema_rates.html annually.'],
    ['Materials and Contracts tracking', 'Available immediately. Source documentation required for FEMA PW.'],
    ['Project Worksheet text export', 'Click Export PW Text on any incident for a formatted PW summary.'],
    ['Real-time cost dashboard', 'Available at /cost_dashboard.html. Auto-refreshes every 2 minutes.'],
], [2.5*inch, CW-2.5*inch]))
story.append(SP(8))

story.append(H2('15.3  Pre-Planned Event Templates'))
story.append(P(
    'Six built-in templates are pre-loaded during installation: Emergency Shelter Operations, '
    'Search and Rescue, Severe Weather Response, Mass Gathering, HazMat Response, and '
    'Exercise/Training Scenario. Templates can be edited and new ones created at /event_templates.html.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(steps([
    'Navigate to http://192.168.50.1/event_templates.html',
    'Click the <b>Activate</b> tab — browse the template gallery',
    'Click a template — enter incident name and any custom details',
    'Click <b>Activate Template</b> — a new incident is created pre-loaded with objectives, '
    'resource types, channels, and ICS organization structure',
    'To edit a template: click <b>Manage Templates</b> → Edit → modify Objectives, '
    'Resources, Channels, or Organization tabs → Save Template',
    'Export as JSON to share with other FieldCommand systems: click <b>Export JSON</b>',
]))
story.append(SP(8))

story.append(H2('15.4  GPS-Tracked Resource Map'))
story.append(P(
    'The GPS resource map (/resource_map.html) displays color-coded pins for all resources '
    'that have a GPS position set. Three placement methods are available.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(tbl(['METHOD', 'HOW TO USE'], [
    ['Device GPS (browser)', 'Click Set Position on any resource → click 📍 Use Device GPS. '
                             'Browser requests location permission. Accuracy shown in meters.'],
    ['Click map to place',   'Click 🗺 Click Map to Place → crosshair cursor appears → '
                             'click anywhere on the map to drop the resource pin.'],
    ['Manual coordinates',   'Type decimal lat/lon directly into the fields. '
                             'Negative longitude for western hemisphere.'],
], [1.8*inch, CW-1.8*inch]))
story.append(SP(8))

story.append(H2('15.5  IAP One-Click PDF Compilation'))
story.append(P(
    'The IAP compiler (/iap_compile.html) generates a print-ready PDF containing all '
    'selected ICS forms for the active incident. Digital signatures are embedded. '
    'Generated server-side using ReportLab and pypdf — no browser PDF library needed.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(steps([
    'Ensure the active incident has completed ICS forms with signatures',
    'Navigate to http://192.168.50.1/iap_compile.html',
    'Check the forms to include (ICS-202, 203, 204, 205, 206, and 207 minimum)',
    'Click <b>📄 Compile IAP PDF</b> — server generates the PDF (5–15 seconds)',
    'PDF downloads automatically with title page, section dividers, and all forms',
    'Print from any device using the Print Center (/printcenter.html)',
]))
story.append(SP(8))

story.append(H2('15.6  NEXRAD Animated Radar'))
story.append(P(
    'The radar page (/radar.html) requires an active internet connection for radar tile loading. '
    'When offline, it displays the last loaded frame with a timestamp. '
    'No installation configuration is required — it pulls tiles from NWS RIDGE II directly.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(NoteBox(
    'The radar page auto-detects WAN status and resumes loading new tiles automatically '
    'when internet connectivity is restored. No manual action is required after a WAN outage.',
    'note'))
story.append(SP(8))

story.append(H2('15.7  Dual-Source WAN Configuration'))
story.append(P(
    'FieldCommand IMS supports two simultaneous WAN sources with automatic failover. '
    'Configure both sources at /wan_settings.html after installation.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(tbl(['FIELD', 'OPTIONS & DESCRIPTION'], [
    ['Role',             'Preferred (used first) · Fallback (used when preferred fails)'],
    ['Type',             'Cellular · Satellite · Hotspot · Fixed broadband · Other'],
    ['Detection method', 'internet_only — any internet path works (best for hotspots and USB dongles) | '
                         'ping — checks a specific gateway IP | '
                         'admin_reachable — checks modem admin interface URL'],
    ['Label',            'Human-readable name shown on dashboard: "Cellular", "Satellite", etc.'],
    ['Enabled',          'Toggle a source on or off without deleting configuration'],
], [1.5*inch, CW-1.5*inch]))
story.append(SP(4))
story.append(steps([
    'Navigate to http://192.168.50.1/wan_settings.html',
    'Click <b>+ Add WAN Source</b> to add a source, or click Edit on an existing one',
    'Set Role to <b>Preferred</b> for your primary source (e.g. cellular antenna)',
    'Set Role to <b>Fallback</b> for your secondary source (e.g. satellite dish)',
    'Choose the Detection Method appropriate for each source type',
    'Click Save. The WAN monitor applies the new configuration within 60 seconds.',
    'Use <b>⇄ Swap Roles</b> to swap preferred and fallback without editing.',
]))
story.append(SP(8))

story.append(H2('15.8  Digital Signature Capture'))
story.append(P(
    'All 16 Prepared By and Approved By signature fields across the ICS form set '
    'support digital signature capture. Signatures are stored as PNG images in the database '
    'and are embedded in printed forms and compiled IAP PDFs. No setup required.',
    S('B', fontSize=9, leading=13)))
story.append(SP(4))
story.append(P(
    'To sign: click any Prepared By or Approved By field → signature pad appears → '
    'sign with mouse, touchscreen, or stylus → click Accept. '
    'Signatures persist through page reloads and appear in the IAP PDF compilation.',
    S('B', fontSize=9, leading=13)))
story.append(SP(8))

story.append(H2('15.9  Incident Archive and Beta Reset'))
story.append(tbl(['FUNCTION', 'HOW TO USE', 'NOTES'], [
    ['Archive to USB',
     'incident_mgmt.html → select incident → Archive to USB',
     'USB drive must be labelled FIELDCOMMAND. JSON written to /media/fieldcommand/backup/incidents/'],
    ['Restore from USB',
     'incident_mgmt.html → Restore from USB → select JSON file',
     'Restores incident to fully active status with all forms, T-cards, costs, and check-ins'],
    ['Hard delete from Pi',
     'incident_mgmt.html → select archived incident → Hard Delete',
     'Permanent — confirm archive exists on USB before deleting'],
    ['Beta/Scenario Reset',
     'incident_mgmt.html → Beta/Scenario Reset → Confirm',
     'Wipes all incidents, forms, T-cards, costs, check-ins. Preserves roster, channels, repeaters.'],
], [1.5*inch, 2.0*inch, CW-3.5*inch]))
story.append(SP(4))
story.append(NoteBox(
    'The USB drive must have volume label FIELDCOMMAND (all capitals). '
    'Format as FAT32 or exFAT. Label with: '
    'sudo mlabel -i /dev/sdX1 ::FIELDCOMMAND  (replace sdX1 with actual USB device).',
    'note'))

story.append(H1('16. Maintenance & Updates'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(CodeBlock([
    '# Interactive maintenance menu:',
    'sudo bash /opt/fieldcommand/scripts/update.sh',
    '',
    '# Menu options:',
    '#  1) Restart all services',
    '#  2) Stop all services',
    '#  3) Check service status',
    '#  4) View live logs',
    '#  5) Refresh FCC database',
    '#  6) Fetch repeater data',
    '#  7) Update web files from current directory',
    '#  8) Backup data to /tmp',
    '#  9) Show disk usage',
]))
story.append(SP(6))
story.append(H2('USB Auto-Backup'))
story.append(P('Insert a USB drive formatted with the label <b>FIELDCOMMAND</b> to trigger an automatic backup '
               'of all runtime data. The backup copies /opt/fieldcommand/data/ to a timestamped folder on the USB drive.'))
story.append(SP(4))
story.append(CodeBlock([
    '# Format a USB drive with label FIELDCOMMAND (Linux):',
    'sudo mkfs.vfat -n FIELDCOMMAND /dev/sda1',
    '# Or on Windows: format as FAT32, set volume label to FIELDCOMMAND',
    '# Backup destination on USB:',
    '# /media/fieldcommand/backup/YYYYMMDD_HHMMSS',
]))
story.append(PB())

story.append(H1('17. Troubleshooting'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(ref_tbl_2col(['SYMPTOM', 'LIKELY CAUSE / FIX'], [
    ['http://192.168.50.1 not reachable', 'Pi not running, or ASUS router not configured with 192.168.50.x subnet. Check Pi power LED. Verify router LAN IP is 192.168.50.1.'],
    ['Dashboard loads but cards give errors', 'Not connected to EMCOMM-NET — device is on a different network. Check Wi-Fi — must show EMCOMM-NET.'],
    ['FCC lookup returns no results', 'FCC database not yet built. Run: sudo systemctl start fcc-refresh.service (needs internet)'],
    ['APRS map shows no stations', 'Graywolf or YAAC not running, or no RF received yet. Check Health Monitor for service status. Confirm antenna connected.'],
    ['Winlink form import fails', 'Wrong file type — must be the XML attachment, not the message body. In Winlink Express, right-click .xml attachment → Save As → then import.'],
    ['Service dot is red on Health Monitor', 'Background service has stopped. SSH to Pi: sudo systemctl restart <service-name>'],
    ['Pat Winlink not accessible at port 8090', 'pat.service not running. Run: sudo systemctl start pat && sudo systemctl enable pat'],
    ['JS8Call card does not open', 'TCP Server API not enabled in JS8Call, or wrong IP entered. Verify: File → Settings → Reporting → Enable TCP Server API, port 2442, hostname 0.0.0.0.'],
    ['Printer not visible on EMCOMM-NET', 'avahi-daemon not running, or CUPS printer not shared. Check: sudo systemctl status avahi-daemon cups. Verify Share This Printer is checked in CUPS UI.'],
    ['Issue: Services crash on startup', 'Low disk space or permission error. Check: df -h / and ls -la /opt/fieldcommand/. Verify fieldcommand user owns /opt/fieldcommand/.'],
], [1.8*inch, CW-1.8*inch]))
story.append(SP(4))
story.append(NoteBox('For any issue not covered here — open the Health Monitor at http://192.168.50.1:5051/health '
                     'or check the system log with: journalctl -u fcc-lookup -n 50', 'tip'))
story.append(PB())

story.append(H1('17. Quick Reference Card'))
story.append(HR(EOC_LT, 0.5))
story.append(SP(6))
story.append(tbl(['ITEM', 'VALUE'], [
    ['FieldCommand dashboard',   'http://192.168.50.1'],
    ['Wi-Fi network (SSID)',   'EMCOMM-NET'],
    ['WAN status dashboard',   'http://192.168.50.1/wan-status.html'],
    ['FieldCommand Pi static IP','192.168.50.1'],
    ['the cellular antenna unit modem admin','http://10.1.1.1  or  http://my.insty  (connect to the cellular antenna unit Wi-Fi first)'],
    ['the cellular antenna unit data plan', 'instyconnect.com  —  Multi-Network Unlimited  —  pause in portal between activations'],
    ['satellite dish admin',         'http://192.168.10.1  (satellite dish app or browser)'],
    ['44Net Gateway Pi IP',    '192.168.50.2'],
    ['44Net gateway status',   'http://192.168.50.2:9000'],
    ['AMPRNet tunnel check',   'ping 44.0.0.1  (from any EMCOMM-NET device)'],
    ['ASUS router admin',      'http://192.168.50.254'],
    ['CUPS printer admin',     'http://192.168.50.1:631'],
    ['Pat Winlink (backup)',   'http://192.168.50.1:8090'],
    ['Kiwix offline library',  'http://192.168.50.1:8081'],
    ['Health monitor (raw)',   'http://192.168.50.1:5051/health'],
    ['JS8Call TCP API (laptop)','http://[laptop-ip]:2442'],
    ['Your callsign', 'your organization'],
    ['your county grid', '<your grid>'],
    ['Default coordinates', 'your deployment coordinates (decimal degrees)'],
    ['Install log', '/var/log/fieldcommand-install.log'],
    ['Application data', '/opt/fieldcommand/data/'],
    ['HTML pages', '/opt/fieldcommand/html/'],
    ['Update script', 'sudo bash /opt/fieldcommand/scripts/update.sh'],
], [2.0*inch, CW-2.0*inch]))

# ── Build ─────────────────────────────────────────────────────────────────────
out = '/mnt/user-data/outputs/FieldCommand_Installation_Guide.pdf'
doc = SimpleDocTemplate(
    out, pagesize=letter,
    leftMargin=M, rightMargin=M,
    topMargin=0.55*inch, bottomMargin=0.42*inch,
    title='FieldCommand IMS v1.0 — Installation Guide',
    author='your organization')
doc.build(story, canvasmaker=NC)

# Append Pi 500 addendum
from pypdf import PdfReader, PdfWriter
addendum = '/home/claude/pi500_addendum.pdf'
if os.path.exists(addendum):
    base = PdfReader(out); add = PdfReader(addendum)
    w = PdfWriter()
    for p in base.pages: w.add_page(p)
    for p in add.pages:  w.add_page(p)
    buf = io.BytesIO()
    w.write(buf)
    with open(out, 'wb') as f: f.write(buf.getvalue())

r = PdfReader(out)
print(f'BUILT: {out}')
print(f'Pages: {len(r.pages)}')
