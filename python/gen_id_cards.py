# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""
FieldCommand — Member ID / Accountability Card Generator

Prints laminate-ready photo ID cards, one per roster member, on Avery 5371 /
5874 / 8371 business-card stock (10 cards per sheet, 3.5" x 2"). Each card shows:
  - Organization logo + short name + station callsign   (from Setup / station_config)
  - Member photo (if on file)
  - Name, role, and identifiers (callsign / member ID / radio ID)
  - A REAL, scannable QR code (generated locally with ReportLab — fully offline)
    encoding the member's barcode_id, so it works with the Scan Check-In page and
    any USB/Bluetooth 2D barcode scanner.

AGENCY-NEUTRAL: every branding value (org name, callsign, logo, and the ID-field
labels) is read from station_config, which the Setup screen fills in. Nothing is
hardcoded to any one group — the same code prints correct cards for any agency.

Who gets a card: roster MEMBERS. Walk-ins / mutual-aid are skipped UNLESS they
already have a photo on file (e.g. a partner agency that pre-loaded credentials).

Usage:
  python3 gen_id_cards.py                         # all members from the live DB
  python3 gen_id_cards.py --db fieldcommand.db --out cards.pdf
  python3 gen_id_cards.py --id m-1712345678901    # a single member's card
  python3 gen_id_cards.py --demo                  # sample cards, no DB needed
"""

import sys, os, argparse, sqlite3, base64, io
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

# ── Palette (house navy + gold) ─────────────────────────────────────────────────
EOC      = HexColor('#1a3a6b')
EOC_LT   = HexColor('#2d6ab4')
GOLD     = HexColor('#f0c040')
PANEL_BG = HexColor('#eef2f7')
LINE     = HexColor('#b0c4dc')
MUTED    = HexColor('#4a6080')
PURPLE   = HexColor('#5b2d8c')

DEFAULT_DB = '/opt/fieldcommand/data/fieldcommand.db'

# Avery 5371 / 5874 / 8371 layout
PAGE_W, PAGE_H = letter
CARD_W  = 3.5 * inch
CARD_H  = 2.0 * inch
COLS    = 2
ROWS    = 5
LEFT_M  = (PAGE_W - COLS * CARD_W) / 2
TOP_M   = (PAGE_H - ROWS * CARD_H) / 2


# ── Helpers ─────────────────────────────────────────────────────────────────────
def _img_reader(b64_or_dataurl):
    """Return a ReportLab ImageReader from base64 (or a data: URL), or None.
    Photos are stored/exported as JPEG so ReportLab embeds them without needing
    the Python Imaging Library (PIL)."""
    raw = (b64_or_dataurl or '').strip()
    if not raw:
        return None
    if raw.startswith('data:'):
        raw = raw.split(',', 1)[-1]
    try:
        return ImageReader(io.BytesIO(base64.b64decode(raw)))
    except Exception:
        return None


def _qr_drawing(data, size_pt):
    """A ReportLab Drawing of a real, scannable QR for `data`, size_pt square."""
    q = QrCodeWidget(str(data), barLevel='M')
    b = q.getBounds()
    w = (b[2] - b[0]) or 1
    h = (b[3] - b[1]) or 1
    d = Drawing(size_pt, size_pt)
    d.transform = [size_pt / w, 0, 0, size_pt / h, -b[0] * size_pt / w, -b[1] * size_pt / h]
    d.add(q)
    return d


def _fit(c, text, font, max_w, start_sz, min_sz=6):
    """Largest font size (<= start_sz) at which text fits max_w."""
    sz = start_sz
    while sz > min_sz and c.stringWidth(text, font, sz) > max_w:
        sz -= 0.5
    return sz


# ── Draw one card ───────────────────────────────────────────────────────────────
def _labeled_field(c, x, y, w, label, value):
    """A small uppercase micro-label with the value beneath — the credential look."""
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 4.6)
    c.drawString(x, y, label.upper()[:18])
    c.setFillColor(HexColor('#16233a'))
    vsz = _fit(c, value, 'Helvetica-Bold', w, 8.5, 6)
    c.setFont('Helvetica-Bold', vsz)
    c.drawString(x, y - 0.115 * inch, value[:22])


def draw_id_card(c, x, y, member, cfg):
    """Draw a single 3.5" x 2" member ID card. (x, y) is the bottom-left corner."""
    org_short  = (cfg.get('org_short') or cfg.get('org_name') or 'FieldCommand').strip()
    org_full   = (cfg.get('org_name') or org_short).strip()
    call_org   = (cfg.get('callsign') or '').strip()
    mid_label  = (cfg.get('ps_member_id_label') or 'Member ID').strip()
    rid_label  = (cfg.get('ps_id_label') or 'Radio ID').strip()

    M   = 0.12 * inch
    HB  = 0.33 * inch          # header band
    FB  = 0.15 * inch          # footer band
    INK = HexColor('#16233a')

    # Member fields
    name = (member.get('name') or
            f"{member.get('first_name','')} {member.get('last_name','')}").strip() or 'Member'
    callsign  = (member.get('callsign') or '').upper().strip()
    member_id = (member.get('member_id') or '').strip()
    radio_id  = (member.get('radio_id') or '').strip()
    role      = (member.get('role') or 'Operator').strip()
    mtype     = (member.get('member_type') or 'member')
    barcode   = (member.get('barcode_id') or member_id or callsign or
                 member.get('id') or '').strip()
    is_ham    = bool(callsign)
    type_tag  = {'visitor': 'MUTUAL AID', 'mutual_aid': 'MUTUAL AID'}.get(mtype, 'MEMBER')

    # ── Card body + rounded border ──────────────────────────────────────────────
    c.setFillColor(white)
    c.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch, fill=1, stroke=0)

    # ── Header band ─────────────────────────────────────────────────────────────
    c.saveState()
    p = c.beginPath()
    p.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(EOC)
    c.rect(x, y + CARD_H - HB, CARD_W, HB, fill=1, stroke=0)
    c.setFillColor(GOLD)
    c.rect(x, y + CARD_H - HB - 0.022 * inch, CARD_W, 0.022 * inch, fill=1, stroke=0)
    c.restoreState()

    text_x = x + M
    logo = _img_reader(cfg.get('logo_data'))
    if logo is not None:
        try:
            c.drawImage(logo, x + 0.09 * inch, y + CARD_H - HB + 0.05 * inch,
                        width=0.40 * inch, height=0.23 * inch,
                        preserveAspectRatio=True, anchor='sw', mask='auto')
            text_x = x + 0.56 * inch
        except Exception:
            pass

    # membership-type tag (right side of header)
    c.setFont('Helvetica-Bold', 6)
    tag_w = c.stringWidth(type_tag, 'Helvetica-Bold', 6) + 10
    c.setFillColor(GOLD)
    c.roundRect(x + CARD_W - M - tag_w, y + CARD_H - 0.225 * inch, tag_w, 0.135 * inch,
                0.02 * inch, fill=1, stroke=0)
    c.setFillColor(EOC)
    c.drawCentredString(x + CARD_W - M - tag_w / 2, y + CARD_H - 0.185 * inch, type_tag)

    avail = (x + CARD_W - M - tag_w - 0.06 * inch) - text_x
    c.setFillColor(white)
    osz = _fit(c, org_short, 'Helvetica-Bold', avail, 9.5, 6.5)
    c.setFont('Helvetica-Bold', osz)
    c.drawString(text_x, y + CARD_H - 0.155 * inch, org_short)
    c.setFillColor(HexColor('#b9cdec'))
    c.setFont('Helvetica', 5)
    c.drawString(text_x, y + CARD_H - 0.265 * inch,
                 ('EMCOMM / ICS CREDENTIAL' + (f'  ·  {call_org}' if call_org else '')))

    # ── Photo (left) ────────────────────────────────────────────────────────────
    PW, PH = 0.82 * inch, 1.18 * inch
    px = x + M
    py = y + FB + (CARD_H - HB - FB - PH) / 2.0
    photo = _img_reader(member.get('photo_data'))
    drew = False
    if photo is not None:
        try:
            c.drawImage(photo, px, py, width=PW, height=PH,
                        preserveAspectRatio=True, anchor='c', mask='auto')
            drew = True
        except Exception:
            drew = False
    if not drew:
        c.setFillColor(PANEL_BG)
        c.rect(px, py, PW, PH, fill=1, stroke=0)
        initials = ((member.get('first_name', ' ')[:1] +
                     member.get('last_name', ' ')[:1]).strip() or '?').upper()
        c.setFillColor(HexColor('#9db4d0'))
        c.setFont('Helvetica-Bold', 26)
        c.drawCentredString(px + PW / 2, py + PH / 2 - 10, initials)
    c.setStrokeColor(EOC_LT)
    c.setLineWidth(0.6)
    c.rect(px, py, PW, PH, fill=0, stroke=1)

    # ── Right column ────────────────────────────────────────────────────────────
    tx    = px + PW + 0.14 * inch
    right = x + CARD_W - M
    colw  = right - tx

    # Name
    c.setFillColor(INK)
    nsz = _fit(c, name, 'Helvetica-Bold', colw, 13, 8)
    c.setFont('Helvetica-Bold', nsz)
    c.drawString(tx, y + CARD_H - HB - 0.20 * inch, name)
    # Role
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 7.5)
    c.drawString(tx, y + CARD_H - HB - 0.34 * inch, role[:38])

    # ID panel — light rounded strip with up to three labeled fields
    panel_y = y + 0.86 * inch
    c.setFillColor(HexColor('#f2f5f9'))
    c.roundRect(tx, panel_y, colw, 0.42 * inch, 0.03 * inch, fill=1, stroke=0)
    fields = []
    if callsign:
        fields.append(('Callsign', callsign))
    if member_id:
        fields.append((mid_label, member_id))
    if radio_id:
        fields.append((rid_label, radio_id))
    fields = fields[:3] or [('ID', barcode or '—')]
    fw = colw / len(fields)
    for i, (lbl, val) in enumerate(fields):
        _labeled_field(c, tx + 0.06 * inch + i * fw, panel_y + 0.28 * inch,
                       fw - 0.08 * inch, lbl, val)

    # ── QR (bottom-right) ───────────────────────────────────────────────────────
    QSZ = 0.62 * inch
    qx = right - QSZ
    qy = y + FB + 0.05 * inch
    if barcode:
        c.setFillColor(white)
        c.setStrokeColor(LINE)
        c.setLineWidth(0.5)
        c.rect(qx - 0.03 * inch, qy - 0.03 * inch, QSZ + 0.06 * inch, QSZ + 0.06 * inch,
               fill=1, stroke=1)
        try:
            renderPDF.draw(_qr_drawing(barcode, QSZ), c, qx, qy)
        except Exception:
            pass
    # left of QR: license/ID note + scan prompt
    c.setFillColor(EOC)
    c.setFont('Helvetica-Bold', 5.5)
    c.drawString(tx, qy + 0.30 * inch, 'SCAN TO CHECK IN')
    c.setFillColor(MUTED)
    c.setFont('Helvetica', 5)
    if is_ham and member.get('license_class'):
        c.drawString(tx, qy + 0.19 * inch, f"FCC: {str(member.get('license_class'))[:22]}")
    c.setFont('Helvetica', 4.6)
    c.setFillColor(HexColor('#9aa7b8'))
    c.drawString(tx, qy + 0.05 * inch, (barcode or '')[:26])

    # ── Footer band ─────────────────────────────────────────────────────────────
    c.saveState()
    p2 = c.beginPath()
    p2.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch)
    c.clipPath(p2, stroke=0, fill=0)
    c.setFillColor(EOC)
    c.rect(x, y, CARD_W, FB, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(HexColor('#c7d6ec'))
    c.setFont('Helvetica', 5)
    c.drawString(x + M, y + 0.052 * inch, org_full[:52])
    c.setFont('Helvetica-Oblique', 4.8)
    c.drawRightString(x + CARD_W - M, y + 0.052 * inch, 'Property of issuing organization — return if found')

    # ── Cut guide ───────────────────────────────────────────────────────────────
    c.setStrokeColor(HexColor('#c8c8c8'))
    c.setLineWidth(0.25)
    c.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch, fill=0, stroke=1)


def draw_card_back(c, x, y, cfg):
    """The card back: EMCOMM-NET access details (agency-neutral, from Setup)."""
    org_full = (cfg.get('org_name') or cfg.get('org_short') or 'FieldCommand').strip()
    ssid     = (cfg.get('wifi_ssid') or 'EMCOMM-NET').strip()
    wpass    = (cfg.get('wifi_pass') or '').strip()
    url      = (cfg.get('server_url') or 'http://192.168.50.1').strip()
    M  = 0.14 * inch
    HB = 0.30 * inch
    FB = 0.15 * inch

    c.setFillColor(white)
    c.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch, fill=1, stroke=0)

    # Header
    c.saveState()
    p = c.beginPath(); p.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch)
    c.clipPath(p, stroke=0, fill=0)
    c.setFillColor(EOC); c.rect(x, y + CARD_H - HB, CARD_W, HB, fill=1, stroke=0)
    c.setFillColor(GOLD); c.rect(x, y + CARD_H - HB - 0.022 * inch, CARD_W, 0.022 * inch, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(white); c.setFont('Helvetica-Bold', 8.5)
    c.drawString(x + M, y + CARD_H - 0.205 * inch, 'NETWORK ACCESS')

    # Access fields
    def field(fy, label, value, mono=True):
        c.setFillColor(MUTED); c.setFont('Helvetica', 5.2)
        c.drawString(x + M, fy, label.upper())
        c.setFillColor(HexColor('#16233a'))
        fnt = 'Courier-Bold' if mono else 'Helvetica-Bold'
        vsz = _fit(c, value, fnt, CARD_W - 2 * M, 11, 7)
        c.setFont(fnt, vsz)
        c.drawString(x + M, fy - 0.15 * inch, value)

    fy = y + CARD_H - HB - 0.28 * inch
    field(fy, 'Wi-Fi network', ssid)
    fy -= 0.40 * inch
    if wpass:
        field(fy, 'Wi-Fi password', wpass)
        fy -= 0.40 * inch
    field(fy, 'Dashboard', url, mono=False)

    # Instructions
    c.setFillColor(MUTED); c.setFont('Helvetica', 5.6)
    c.drawString(x + M, y + FB + 0.14 * inch,
                 'Join the Wi-Fi first, then open the dashboard in any browser. No app needed.')
    c.setFont('Helvetica-Oblique', 5.6)
    c.drawString(x + M, y + FB + 0.04 * inch, 'Scan the QR on the front to check in.')

    # Footer
    c.saveState()
    p2 = c.beginPath(); p2.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch)
    c.clipPath(p2, stroke=0, fill=0)
    c.setFillColor(EOC); c.rect(x, y, CARD_W, FB, fill=1, stroke=0)
    c.restoreState()
    c.setFillColor(HexColor('#c7d6ec')); c.setFont('Helvetica', 5)
    c.drawString(x + M, y + 0.052 * inch, org_full[:52])

    c.setStrokeColor(HexColor('#c8c8c8')); c.setLineWidth(0.25)
    c.roundRect(x, y, CARD_W, CARD_H, 0.09 * inch, fill=0, stroke=1)


# ── Data loading ────────────────────────────────────────────────────────────────
def load_config(conn):
    try:
        row = conn.execute("SELECT * FROM station_config WHERE id=1").fetchone()
        return dict(row) if row else {}
    except Exception:
        return {}


def _include(m):
    """Members get a card. Walk-ins / mutual-aid only if they have a photo."""
    mtype = (m.get('member_type') or 'member')
    if mtype in ('visitor', 'mutual_aid'):
        return bool(m.get('photo_data'))
    return True


def load_members(conn, only_id=None):
    conn.row_factory = sqlite3.Row
    if only_id:
        rows = conn.execute("SELECT * FROM roster WHERE id=?", (only_id,)).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM roster ORDER BY last_name, first_name, callsign").fetchall()
    out = []
    for r in rows:
        m = dict(r)
        m['name'] = f"{m.get('first_name','') or ''} {m.get('last_name','') or ''}".strip()
        if only_id or _include(m):
            out.append(m)
    return out


# ── Generate ────────────────────────────────────────────────────────────────────
def generate_cards(members, cfg, output, backs=True):
    """Render fronts (and, by default, matching backs for duplex printing).

    Backs are laid out with columns mirrored, so when the sheet is flipped on its
    LONG (left/right) edge to print the second side, each back lands behind its own
    front. Print all pages double-sided, flip on long edge."""
    c = canvas.Canvas(output, pagesize=letter)
    c.setTitle(f"{cfg.get('org_short') or 'FieldCommand'} — Member ID Cards")
    per = COLS * ROWS
    pages = [members[i:i + per] for i in range(0, len(members), per)] or [[]]
    sheets = []
    for pg in pages:
        sheets.append(('front', pg))
        if backs:
            sheets.append(('back', pg))
    for idx, (kind, pg) in enumerate(sheets):
        for i, m in enumerate(pg):
            col = i % COLS
            row = i // COLS
            if kind == 'back':
                col = COLS - 1 - col   # mirror for long-edge duplex flip
            x = LEFT_M + col * CARD_W
            y = PAGE_H - TOP_M - (row + 1) * CARD_H
            if kind == 'front':
                draw_id_card(c, x, y, m, cfg)
            else:
                draw_card_back(c, x, y, cfg)
        if idx < len(sheets) - 1:
            c.showPage()
    c.save()
    return output


def generate_from_db(db_path=DEFAULT_DB, out_path=None, only_id=None, backs=True):
    """Entry point for the web endpoint. Returns the output path."""
    if out_path is None:
        out_path = os.path.join(os.path.dirname(db_path) or '.', 'member_id_cards.pdf')
    conn = sqlite3.connect(db_path)
    try:
        cfg = load_config(conn)
        members = load_members(conn, only_id=only_id)
    finally:
        conn.close()
    if not members:
        raise ValueError("No eligible members to print.")
    return generate_cards(members, cfg, out_path, backs=backs)


# ── Demo data (no DB needed) ─────────────────────────────────────────────────────
DEMO_CFG = {'org_short': 'Your Org', 'org_name': 'Your Organization',
            'callsign': '', 'ps_member_id_label': 'Member ID', 'ps_id_label': 'Radio ID',
            'wifi_ssid': 'EMCOMM-NET', 'wifi_pass': 'fieldcommand2026',
            'server_url': 'http://192.168.50.1'}
DEMO_MEMBERS = [
    {'first_name': 'Sarah', 'last_name': 'Mitchell', 'name': 'Sarah Mitchell',
     'callsign': 'W9XYZ', 'member_id': 'MEM-002', 'radio_id': '1002',
     'role': 'Net Control Station', 'barcode_id': 'MEM-002', 'member_type': 'member'},
    {'first_name': 'Michael', 'last_name': 'Garcia', 'name': 'Michael Garcia',
     'callsign': '', 'member_id': 'MEM-007', 'radio_id': '1087',
     'role': 'Medical Support', 'barcode_id': 'MEM-007', 'member_type': 'member'},
]


def main():
    p = argparse.ArgumentParser(description='Generate FieldCommand member ID cards')
    p.add_argument('--db',   default=None, help='SQLite DB path')
    p.add_argument('--out',  default='member_id_cards.pdf', help='Output PDF path')
    p.add_argument('--id',   default=None, help='Only this member id')
    p.add_argument('--demo', action='store_true', help='Use demo data (no DB)')
    p.add_argument('--no-backs', action='store_true', help='Fronts only (skip the access-info back)')
    args = p.parse_args()
    backs = not args.no_backs

    if args.demo:
        generate_cards(DEMO_MEMBERS, DEMO_CFG, args.out, backs=backs)
        print(f'Done (demo): {args.out}')
        return
    db_path = args.db or DEFAULT_DB
    if not Path(db_path).exists():
        print(f'No database at {db_path}. Use --demo to preview, or --db PATH.')
        sys.exit(1)
    try:
        out = generate_from_db(db_path, args.out, only_id=args.id, backs=backs)
        print(f'Done: {out}')
    except ValueError as e:
        print(str(e)); sys.exit(1)


if __name__ == '__main__':
    main()
