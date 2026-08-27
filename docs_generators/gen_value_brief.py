#!/usr/bin/env python3
# SPDX-License-Identifier: CC-BY-SA-4.0
# FieldCommand IMS — Value, Cost & Capability Brief generator
# Copyright (C) 2026 James Rospopo KE4CON
"""
Generates a professional PDF brief on the value, replacement cost, and capability
of FieldCommand IMS — for agency briefings and grant applications.

Two editions from one source (same model as the manuals):
  * World edition — generic, agency-neutral (public).
  * ESV edition   — tailored to McHenry County ESV / MCEMA (PRIVATE: docs/internal,
                    gitignored). Only builds if docs/internal/editions_esv.json exists.

Run:  python gen_value_brief.py               -> builds both editions to the repo
      python gen_value_brief.py World|ESV     -> one edition
      python gen_value_brief.py --out FILE ED -> one edition to a specific path
"""
import os
import sys
import json
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, ListFlowable, ListItem)
from reportlab.pdfgen import canvas

EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
LGRAY  = HexColor('#f2f5f9')
GREEN  = HexColor('#1a7a3a')
AMBER_BG = HexColor('#fef3d8')
AMBER  = HexColor('#9a6a10')
MUTED  = HexColor('#4a6080')
INK    = HexColor('#16233a')

TODAY  = datetime.date.today().strftime('%B %d, %Y')
PAGE_W, PAGE_H = letter
M  = 0.8 * inch
CW = PAGE_W - 2 * M
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..'))

# Cover text is edition-specific; the canvas reads this global set before build.
COVER = {}


# ── Edition definitions ─────────────────────────────────────────────────────────
def load_editions():
    """World is built-in; ESV pulls names from the private editions file if present."""
    ed = {
        'World': {
            'label': 'World Edition', 'infix': '', 'private': False,
            'org_full': 'your agency', 'org_short': 'your agency',
            'served': 'the agency you support',
            'club_call': None,
            'cover_sub': 'built by one volunteer, with AI assistance, and given away free.',
            'cover_prepared': 'Prepared for agency leadership and grant review',
            'exis': 'a county emergency management agency or a public-safety / amateur-radio '
                    'emergency communications (EMCOMM) group',
            'exec_who': 'agencies and volunteer groups',
            'grant_intro': 'Talking points suitable for a board memo or a grant narrative:',
            'credit_line': '',
        },
    }
    priv = os.path.join(REPO, 'docs', 'internal', 'editions_esv.json')
    if os.path.exists(priv):
        try:
            t = json.load(open(priv, encoding='utf-8')).get('ESV', {}).get('tokens', {})
            ed['ESV'] = {
                'label': 'ESV Edition', 'infix': '_ESV', 'private': True,
                'org_full': t.get('org', 'McHenry County Emergency Services Volunteers (ESV)'),
                'org_short': t.get('org_abbr', 'MCESV'),
                'served': t.get('served', 'McHenry County Emergency Management Agency (MCEMA)'),
                'club_call': t.get('club', 'K9ESV'),
                'cover_sub': 'built by one volunteer, with AI assistance, and given to '
                             + t.get('org_abbr', 'MCESV') + ' and the EMCOMM community free.',
                'cover_prepared': 'Prepared for ' + t.get('org_abbr', 'MCESV')
                                  + ' leadership, ' + t.get('served_the', 'MCEMA') + ', and grant review',
                'exis': t.get('org', 'McHenry County ESV') + ', in support of '
                        + t.get('served', 'the McHenry County Emergency Management Agency (MCEMA)'),
                'exec_who': t.get('org', 'McHenry County ESV') + ' and its mutual-aid partners',
                'grant_intro': 'Talking points for ' + t.get('org_abbr', 'MCESV')
                               + ' leadership and for grant applications made on behalf of the organization:',
                'credit_line': ' Developed for ' + t.get('org', 'McHenry County ESV')
                               + ' (' + t.get('club', 'K9ESV') + ').',
            }
        except Exception as e:
            print('ESV edition skipped:', e)
    return ed


# ── Canvas (cover + running chrome) ─────────────────────────────────────────────
class Brief(canvas.Canvas):
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
            if self._pageNumber == 1:
                self._cover()
            else:
                self._chrome(self._pageNumber, total)
            super().showPage()
        super().save()

    def _cover(self):
        self.setFillColor(EOC); self.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        self.setFillColor(GOLD); self.rect(0, PAGE_H - 0.22 * inch, PAGE_W, 0.22 * inch, fill=1, stroke=0)
        self.setFillColor(GOLD); self.rect(0, 0, PAGE_W, 0.22 * inch, fill=1, stroke=0)
        self.setFillColor(HexColor('#1e4480')); self.rect(0, PAGE_H * 0.40, PAGE_W, PAGE_H * 0.34, fill=1, stroke=0)
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 11)
        self.drawCentredString(PAGE_W / 2, PAGE_H - 0.78 * inch, 'FIELDCOMMAND INCIDENT MANAGEMENT SYSTEM')
        self.setFillColor(HexColor('#c0d4f0')); self.setFont('Helvetica', 9.5)
        self.drawCentredString(PAGE_W / 2, PAGE_H - 0.98 * inch, COVER.get('org_line', 'Open-Source  ·  Offline-First  ·  Field-Deployable'))
        self.setFillColor(white); self.setFont('Helvetica-Bold', 50)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.605, 'Value & Cost Brief')
        self.setFillColor(GOLD); self.setFont('Helvetica-Bold', 14)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.55, 'Capability, Replacement Cost, and Return on Investment')
        self.setStrokeColor(GOLD); self.setLineWidth(1.5)
        self.line(M * 1.5, PAGE_H * 0.51, PAGE_W - M * 1.5, PAGE_H * 0.51)
        self.setFillColor(white); self.setFont('Helvetica', 11)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.455, 'A six-figure-class emergency management platform —')
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.428, COVER.get('sub', ''))
        self.setFillColor(HexColor('#8090c0')); self.setFont('Helvetica', 9.5)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.30, COVER.get('prepared', ''))
        self.setFillColor(HexColor('#9fb0d8')); self.setFont('Helvetica-Bold', 9)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.335, COVER.get('label', ''))
        self.setFillColor(HexColor('#6070a0')); self.setFont('Helvetica', 9)
        self.drawCentredString(PAGE_W / 2, PAGE_H * 0.265, f'James Rospopo  ·  KE4CON  ·  {TODAY}')
        self.setFillColor(white); self.setFont('Helvetica', 7)
        self.drawCentredString(PAGE_W / 2, 0.09 * inch,
                               'Figures are good-faith planning estimates, not vendor quotes — see Methodology & Assumptions.')

    def _chrome(self, n, total):
        self.setFillColor(EOC); self.rect(0, PAGE_H - 0.42 * inch, PAGE_W, 0.42 * inch, fill=1, stroke=0)
        self.setFillColor(GOLD); self.rect(0, PAGE_H - 0.44 * inch, PAGE_W, 0.02 * inch, fill=1, stroke=0)
        self.setFillColor(white); self.setFont('Helvetica-Bold', 8)
        self.drawString(M, PAGE_H - 0.27 * inch, 'FieldCommand IMS')
        self.setFont('Helvetica', 7.5)
        self.drawRightString(PAGE_W - M, PAGE_H - 0.27 * inch, 'Value & Cost Brief  ·  ' + COVER.get('label', ''))
        self.setFillColor(EOC); self.rect(0, 0, PAGE_W, 0.34 * inch, fill=1, stroke=0)
        self.setFillColor(GOLD); self.rect(0, 0.34 * inch, PAGE_W, 0.015 * inch, fill=1, stroke=0)
        self.setFillColor(white); self.setFont('Helvetica', 6.8)
        self.drawString(M, 0.12 * inch, '© 2026 James Rospopo KE4CON  ·  CC BY-SA 4.0  ·  Planning estimates, not vendor quotes')
        self.drawRightString(PAGE_W - M, 0.12 * inch, f'Page {n} of {total}')


# ── Style helpers ────────────────────────────────────────────────────────────────
def St(name, **kw):
    d = dict(fontName='Helvetica', fontSize=10, textColor=INK, leading=14, spaceAfter=0, spaceBefore=0)
    d.update(kw); return ParagraphStyle(name, **d)

def P(t, s=None): return Paragraph(t, s or St('b'))
def body(t): return Paragraph(t, St('body', fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6))
def SP(n=6): return Spacer(1, n)
def H1(t): return P(t, St('h1', fontName='Helvetica-Bold', fontSize=16, textColor=EOC, leading=20, spaceBefore=12, spaceAfter=5))
def H2(t): return P(t, St('h2', fontName='Helvetica-Bold', fontSize=11.5, textColor=EOC_LT, leading=15, spaceBefore=8, spaceAfter=3))
def HR(c=GOLD, t=1.0): return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=2, spaceAfter=6)

def bullets(items):
    return ListFlowable(
        [ListItem(P(i, St('li', fontSize=9.8, leading=13.5)), leftIndent=6, value='•') for i in items],
        bulletType='bullet', start='•', leftIndent=14, bulletColor=EOC_LT, spaceAfter=6)

def tbl(headers, rows, widths):
    data = [[P(str(h), St('th', fontName='Helvetica-Bold', fontSize=8.5, textColor=white, leading=11)) for h in headers]]
    for r in rows:
        data.append([P(str(cell), St('td', fontSize=8.8, leading=12)) for cell in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), EOC),
                           ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LGRAY]),
                           ('GRID', (0, 0), (-1, -1), 0.3, LINE),
                           ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                           ('TOPPADDING', (0, 0), (-1, -1), 5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                           ('LEFTPADDING', (0, 0), (-1, -1), 7), ('RIGHTPADDING', (0, 0), (-1, -1), 7)]))
    return t

def callout(text, kind='note'):
    cfg = {'note': (EOC_LT, LGRAY), 'tip': (GREEN, HexColor('#e6f5ec')), 'key': (AMBER, AMBER_BG)}
    c, bg = cfg.get(kind, cfg['note'])
    t = Table([[P(text, St('c', fontSize=9.5, leading=13.5))]], colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, -1), bg),
                           ('LEFTPADDING', (0, 0), (-1, -1), 12), ('RIGHTPADDING', (0, 0), (-1, -1), 12),
                           ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                           ('LINEBEFORE', (0, 0), (0, -1), 3, c)]))
    return t


# ── Story (edition-aware) ────────────────────────────────────────────────────────
def build_story(ED):
    org = ED['org_full']
    A = []; a = A.append
    a(PageBreak())  # cover

    a(H1('Executive Summary')); a(HR())
    a(body(
        'FieldCommand IMS is a complete, offline-first incident management platform for emergency '
        'operations — the kind of system ' + ED['exis'] + ' would normally license from a commercial '
        'vendor for tens of thousands of dollars per year. It runs entirely on inexpensive Raspberry Pi '
        'hardware, needs no internet connection, and is released as free, open-source software.'))
    a(body(
        'This brief documents three things a decision-maker or grant reviewer will want to know: '
        '<b>what the system does</b>, <b>what an equivalent capability would cost to buy or build</b>, and '
        '<b>how it was produced</b>. The headline is simple: a platform whose commercial or custom-build '
        'value is comfortably in the <b>six figures</b> was created by <b>one volunteer developer using '
        'artificial-intelligence (AI) assistance</b> for both the software and its documentation, and is '
        'provided at no licensing cost to ' + ED['exec_who'] + '.'))
    a(callout(
        '<b>Bottom line for budgeting and grants:</b> comparable commercial platforms typically cost an '
        'agency <b>$100,000–$300,000+ over five years</b>. A ground-up custom build of this scope would run '
        '<b>$250,000–$600,000+</b>. FieldCommand delivers that class of capability for the price of the '
        'hardware alone — roughly <b>$2,000–$5,000 one-time</b>, with <b>$0 software licensing</b>.', 'key'))

    a(H1('Purpose of This Document')); a(HR())
    a(body(
        'This brief supports two conversations. First, an <b>internal case</b> to '
        + (org if ED['infix'] else 'agency') + ' leadership for adopting, standardizing on, or continuing '
        'to invest in FieldCommand IMS. Second, an <b>external case</b> for grant applications, where '
        'reviewers reward demonstrated capability, responsible stewardship of funds, and innovative, '
        'low-overhead delivery.'))
    a(body(
        'All dollar figures are <b>good-faith planning estimates</b> derived from publicly understood '
        'market ranges and standard software-costing methods. They are illustrative, not vendor quotes, '
        'and establish an order of magnitude. The Methodology &amp; Assumptions section explains how each '
        'range was derived so the numbers can be defended or adjusted.'))

    a(H1('What FieldCommand IMS Is')); a(HR())
    a(body(
        'FieldCommand IMS is a self-contained incident-management server. Any phone, tablet, or laptop '
        'joins its field Wi-Fi network and reaches every tool through a web browser — no internet, no app '
        'install, and no per-device setup. It is built around the Incident Command System (ICS) and the '
        'National Incident Management System (NIMS), and it consolidates a stack of capabilities that '
        'agencies otherwise assemble from paper forms, spreadsheets, and several separate products:'))
    a(bullets([
        '<b>ICS forms and the Incident Action Plan (IAP)</b> — fillable ICS-201, 202, 205, 211, 213, 214, and 309 with cross-form auto-population and a compiled IAP package.',
        '<b>Net control &amp; communications logging</b> — amateur and public-safety net logs with automatic ICS-309 export; a dead-man\'s-switch inactivity monitor.',
        '<b>Roster, credentialing &amp; accountability</b> — member database with certifications and equipment, photo ID cards with scannable check-in codes, and QR / barcode-scanner check-in.',
        '<b>Resource &amp; personnel management</b> — resource board, ICS T-cards, and the NIMS resource-typing library.',
        '<b>FEMA cost documentation</b> — Schedule of Equipment Rates plus Public Assistance labor, equipment, and materials tracking for reimbursement.',
        '<b>Situational awareness &amp; mapping</b> — tactical map with fully offline map tiles, position feeds, hospitals, repeaters, and radio channel libraries.',
        '<b>Amateur-radio integration</b> — Automatic Packet Reporting System (APRS), Winlink email-over-radio, and an Amateur Packet Radio Network (AMPRNet / 44Net) gateway.',
        '<b>Offline reference &amp; printing</b> — an offline knowledge library (Kiwix) and shared network printing for forms, maps, and the IAP.',
    ]))
    a(callout(
        '<b>Scale of the build:</b> roughly <b>56 web pages</b>, <b>19 back-end services</b>, and an '
        'automated one-command installer — plus three full-length manuals (User, Installation, and '
        'Programming guides). It is designed to keep working when the grid and the internet do not.', 'note'))

    a(PageBreak())
    a(H1('How It Was Built — One Person, AI-Assisted')); a(HR())
    a(body(
        'FieldCommand IMS was designed and built by <b>a single volunteer developer</b> — James Rospopo '
        '(amateur radio callsign KE4CON)'
        + (' of ' + org if ED['infix'] else '')
        + ' — working with <b>AI assistance for both the code and the documentation</b>. This is central '
        'to the value story: work that has traditionally required a multi-person software team and a '
        'professional technical-writing team was delivered by one person who used modern AI tools as a '
        'force multiplier.'))
    a(H2('Why this matters'))
    a(bullets([
        '<b>Extraordinary cost efficiency.</b> The labor that dominates software cost — design, coding, testing, and writing hundreds of pages of documentation — was compressed dramatically, without hiring a team or paying license fees.',
        '<b>Responsible stewardship.</b> Capital goes to hardware and mission, not to seat licenses and consulting hours — a model of doing more with less.',
        '<b>Innovation on record.</b> A concrete, working example of AI-assisted development producing professional-grade public-safety software — a compelling narrative for grants that prioritize innovation.',
        '<b>Sustainability.</b> Because it is open-source and documented to a professional standard, the work is transferable; it does not depend on a vendor\'s continued existence or pricing.',
    ]))
    a(callout(
        '<b>The differentiator in one line:</b> a capability normally sold by companies with engineering '
        'teams and annual license fees was produced by one volunteer with AI assistance — and released '
        'free. The cost figures that follow measure what that is worth.', 'tip'))

    a(H1('Cost Analysis')); a(HR())
    a(body(
        'There are two standard ways to value software an agency did not pay for: what it would cost to '
        '<b>buy</b> a comparable commercial product, and what it would cost to <b>build</b> the same thing '
        'as a custom project. Both point to the same order of magnitude.'))
    a(H2('Option A — Buy a comparable commercial platform'))
    a(body(
        'Commercial incident-management and emergency-operations platforms are sold on annual '
        'subscriptions, usually priced by modules and number of users, with separate one-time '
        'implementation and recurring training costs. Representative planning ranges for a county-scale '
        'deployment:'))
    a(tbl(['Cost element', 'Typical range', '5-year subtotal'],
          [['Software subscription (annual)', '$15,000 – $40,000 / year', '$75,000 – $200,000'],
           ['Implementation &amp; configuration (one-time)', '$15,000 – $50,000', '$15,000 – $50,000'],
           ['Training &amp; support (annual)', '$5,000 – $12,000 / year', '$25,000 – $60,000'],
           ['<b>Five-year total cost of ownership</b>', '', '<b>$115,000 – $310,000</b>']],
          [3.0 * inch, 1.9 * inch, CW - 4.9 * inch]))
    a(SP(4))
    a(body(
        'For amateur-radio and volunteer EMCOMM operations specifically, there is often <b>no single '
        'commercial product</b> that fits — groups instead combine paper ICS forms, a spreadsheet roster, '
        'a separate net-logging tool, and separate mapping. FieldCommand replaces that entire assembled '
        'stack with one integrated, offline system.'))
    a(H2('Option B — Commission a custom build'))
    a(body(
        'Valued as bespoke software, the platform\'s breadth — dozens of screens, many back-end services, '
        'numerous integrations, an offline architecture, provisioning automation, and three manuals — '
        'represents a substantial engineering and documentation effort:'))
    a(tbl(['Work component', 'Estimated effort', 'Estimated cost'],
          [['Software design, development &amp; testing', '18 – 36 person-months', '$220,000 – $520,000'],
           ['Professional documentation (3 manuals)', '3 – 6 person-months', '$30,000 – $90,000'],
           ['<b>Ground-up build total</b>', '', '<b>$250,000 – $610,000</b>'],
           ['Ongoing maintenance (per year, typical)', '15 – 20% of build', '$40,000 – $120,000 / yr']],
          [3.0 * inch, 1.9 * inch, CW - 4.9 * inch]))
    a(callout(
        'Both methods independently land in the <b>hundreds of thousands of dollars</b>. That is the '
        'replacement value ' + (org if ED['infix'] else 'an agency') + ' receives at no software cost.', 'key'))

    a(PageBreak())
    a(H1('Five-Year Total Cost of Ownership — Side by Side')); a(HR())
    a(tbl(['Approach', 'Up-front', 'Recurring (annual)', '5-year total'],
          [['Commercial platform (buy)', '$15k – $50k', '$20k – $52k', '$115k – $310k'],
           ['Custom build (make)', '$250k – $610k', '$40k – $120k', '$450k – $1.2M'],
           ['<b>FieldCommand IMS</b>', '<b>$2k – $5k hardware</b>', '<b>~$0 software</b>', '<b>$2k – $5k</b>']],
          [1.9 * inch, 1.5 * inch, 1.7 * inch, CW - 5.1 * inch]))
    a(SP(4))
    a(body(
        'FieldCommand\'s only material cost is hardware: a pair of Raspberry Pi servers, networking, '
        'operator workstations, and a printer — roughly <b>$2,000–$5,000 one-time</b> depending on whether '
        'a group deploys a single server or a full multi-workstation kit. Software licensing is <b>$0</b>, '
        'and the documentation is included. There are no per-seat fees, so cost does not grow with the '
        'number of responders.'))
    a(callout(
        '<b>Return on investment:</b> against a conservative commercial five-year figure of ~$115,000, a '
        'FieldCommand deployment at ~$4,000 in hardware avoids on the order of <b>$110,000+</b> in '
        'licensing and implementation over the same period — capital ' + (org if ED['infix'] else 'an agency')
        + ' can redirect to training, equipment, and mission.', 'tip'))

    a(H1('Value &amp; Grant Justification')); a(HR())
    a(body(ED['grant_intro']))
    served = ED['served']
    a(bullets([
        '<b>Mission capability.</b> Delivers a professional, ICS/NIMS-aligned incident-management capability that many volunteer and small-agency operations otherwise cannot afford at all.',
        '<b>Resilience.</b> Offline-first and grid-independent — it functions during exactly the internet and power outages when commercial cloud tools fail.',
        '<b>Stewardship of funds.</b> Six-figure-class capability for low-thousands hardware cost; grant dollars buy equipment and readiness, not recurring licenses.',
        '<b>No vendor lock-in.</b> Open-source and fully documented; ' + (org if ED['infix'] else 'the agency') + ' owns its data and its stack, and can maintain or extend the system independently.',
        '<b>Interoperability &amp; mutual aid.</b> Because it is free and open, partner agencies'
        + (' — and ' + served + ' — ' if ED['infix'] else ' ') + 'can run the same system, easing coordination.',
        '<b>Innovation narrative.</b> A demonstrated, working example of AI-assisted development delivering public-safety software — attractive to grantors that reward efficiency and innovation.',
        '<b>Accountability built in.</b> Photo credentialing, scannable check-in, and ICS-214/211 logging support personnel accountability and after-action documentation.',
    ]))

    a(PageBreak())
    a(H1('Capability Inventory')); a(HR())
    a(body('A representative (not exhaustive) list of what is included, at no additional cost:'))
    a(tbl(['Domain', 'Included capabilities'],
          [['Command &amp; planning', 'ICS-201/202/205/211/213/214/309; IAP compiler; planning-cycle guide; meeting scheduler; activity log'],
           ['Communications', 'Amateur &amp; public-safety net logging; ICS-309 export; dead-man\'s-switch monitor; NTS radiogram'],
           ['Personnel &amp; accountability', 'Member roster with certs/equipment; photo ID cards; QR / barcode check-in; walk-in &amp; mutual-aid handling'],
           ['Resources', 'Resource board; ICS T-cards; NIMS resource-typing library'],
           ['Finance / recovery', 'FEMA Schedule of Equipment Rates; Public Assistance labor, equipment &amp; materials tracking'],
           ['Situational awareness', 'Tactical map with offline tiles; APRS position feeds; hospitals, repeaters &amp; channel libraries'],
           ['Amateur radio', 'APRS (Direwolf / APRS Command); Winlink (Pat &amp; Express); AMPRNet / 44Net gateway; FCC callsign lookup (offline)'],
           ['Platform', 'Offline-first web server; shared network printing; Kiwix offline library; GPS; one-command installer; auto-backup'],
           ['Documentation', 'Full User Manual, Installation Guide, and Programming Guide — professional, plain-language, dual-edition'],
           ],
          [1.7 * inch, CW - 1.7 * inch]))

    a(H1('Methodology &amp; Assumptions')); a(HR())
    a(body(
        'The estimates in this brief are planning figures intended to establish an order of magnitude; '
        'they are not vendor quotes and should be adjusted to a specific procurement or grant context.'))
    a(bullets([
        '<b>Commercial (buy) figures</b> reflect commonly understood market ranges for subscription-based emergency-operations / incident-management software at county scale, including typical one-time implementation and recurring training. Actual pricing is quote-based and varies by vendor, modules, and user count.',
        '<b>Custom (build) figures</b> apply standard software-costing: estimated effort in person-months for a platform of this breadth multiplied by blended market development rates, plus separate technical-writing effort for three manuals. Maintenance is estimated at a conventional 15–20% of build cost per year.',
        '<b>FieldCommand hardware</b> is based on the project\'s published bill of materials — two Raspberry Pi 5 servers, networking, operator workstations, and a printer — at consumer prices; a single-server deployment sits at the low end of the range.',
        '<b>Scope counts</b> (approximately 56 web pages and 19 back-end services) are taken from the project source tree at the date of this document.',
        '<b>What is excluded:</b> the value of volunteer operator time, and any agency-specific integration or training the agency chooses to add.',
    ]))

    a(H1('The Bottom Line')); a(HR())
    a(body(
        'FieldCommand IMS provides a capability that agencies routinely pay <b>six figures</b> to license '
        'or build. It was produced by <b>one volunteer, with AI assistance, for both the software and the '
        'documentation</b>, and is offered <b>free and open-source</b>, running on <b>low-thousands-of-'
        'dollars</b> of commodity hardware with <b>no per-seat fees</b>. For '
        + (org if ED['infix'] else 'an agency') + ', that is a rare combination of high capability, high '
        'resilience, and negligible cost. For a grant reviewer, it is a model of efficient, innovative, '
        'mission-focused stewardship.'))
    a(SP(6))
    a(callout(
        '<b>FieldCommand IMS</b> — © 2026 James Rospopo, KE4CON. Software licensed under the GNU Affero '
        'General Public License v3; documentation under Creative Commons Attribution-ShareAlike 4.0. '
        'Developed with AI assistance (Anthropic\'s Claude) for code and documentation.' + ED['credit_line']
        + ' This brief may be shared and adapted with attribution.', 'note'))
    return A


def build_edition(ED, out_path):
    global COVER
    COVER = {'label': ED['label'], 'sub': ED['cover_sub'], 'prepared': ED['cover_prepared'],
             'org_line': (ED['org_full'] if ED['infix'] else 'Open-Source  ·  Offline-First  ·  Field-Deployable')}
    doc = SimpleDocTemplate(out_path, pagesize=letter, leftMargin=M, rightMargin=M,
                            topMargin=0.72 * inch, bottomMargin=0.6 * inch,
                            title=f"FieldCommand IMS — Value & Cost Brief ({ED['label']})",
                            author='James Rospopo KE4CON')
    doc.build(build_story(ED), canvasmaker=Brief)
    return out_path


def default_out(ED):
    # The value/cost brief is a BUSINESS/FINANCIAL document — private by policy
    # (see .gitignore: "org-specific (ESV), business/financial, and dev-only").
    # BOTH the World and ESV editions go to the gitignored docs/internal, unlike
    # the manuals whose World edition is public.
    d = os.path.join(REPO, 'docs', 'internal')
    os.makedirs(d, exist_ok=True)
    return os.path.join(d, f"FieldCommand_Value_and_Cost_Brief{ED['infix']}.pdf")


def main():
    editions = load_editions()
    args = [a for a in sys.argv[1:]]
    out_override = None
    if '--out' in args:
        i = args.index('--out'); out_override = args[i + 1]; del args[i:i + 2]
    which = args or list(editions.keys())
    for key in which:
        if key not in editions:
            print('unknown edition:', key); continue
        ED = editions[key]
        out = out_override or default_out(ED)
        build_edition(ED, out)
        print(f"OK [{key}] -> {out}")


if __name__ == '__main__':
    main()
