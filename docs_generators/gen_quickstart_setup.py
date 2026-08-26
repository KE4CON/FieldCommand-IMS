#!/usr/bin/env python3
"""
gen_quickstart_setup.py — render the One-Command Setup Quick Start Markdown into
a navy+gold house-style PDF.

Markdown is the living source of truth:
    docs/guides/FieldCommand_One_Command_Setup_QuickStart.md
This script renders it to:
    docs/guides/FieldCommand_One_Command_Setup_QuickStart.pdf

It handles the Markdown subset used by that guide: #/##/### headings, paragraphs,
bulleted lists, pipe tables, > blockquote callouts, fenced code blocks, and
inline **bold**, *italic*, and `code`. Standard library + reportlab only.

    python docs_generators/gen_quickstart_setup.py            # default in/out
    python docs_generators/gen_quickstart_setup.py IN.md OUT.pdf
"""
import os
import re
import sys

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Preformatted, Spacer,
    Table, TableStyle, HRFlowable, KeepTogether,
)

# ── House palette (matches the other FieldCommand generators) ────────────────
NAVY     = HexColor('#1a3a6b')
NAVY_LT  = HexColor('#1e4480')
GOLD     = HexColor('#f0c040')
LINE     = HexColor('#b0c4dc')
LGRAY    = HexColor('#f0f3f6')
MUTED    = HexColor('#4a6080')
AMBER    = HexColor('#c8760a')
AMBER_BG = HexColor('#fef3d8')
CODE_BG  = HexColor('#eef2f7')

PAGE_W, PAGE_H = letter
MARGIN = 0.85 * inch
CONTENT_W = PAGE_W - 2 * MARGIN

# ── Unicode → font-safe normalization (Helvetica/WinAnsi) ────────────────────
_NORM = {
    '‑': '-',    # non-breaking hyphen → hyphen
    '→': ' -> ',  # right arrow → ASCII arrow
    ' ': ' ',    # nbsp → space
    '…': '...',  # ellipsis
}


def norm(s: str) -> str:
    for k, v in _NORM.items():
        s = s.replace(k, v)
    # Backstop: drop anything the base fonts can't encode (keeps em/en dash, ×).
    return s.encode('cp1252', 'replace').decode('cp1252')


# ── Paragraph styles ─────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10.5, leading=15, textColor=HexColor('#222222'))
    base.update(kw)
    return ParagraphStyle(name, **base)


ST = {
    'title':   S('title', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=white),
    'subtitle': S('subtitle', fontSize=12, leading=16, textColor=HexColor('#dce6f2')),
    'h1':      S('h1', fontName='Helvetica-Bold', fontSize=17, leading=21, textColor=NAVY, spaceBefore=16, spaceAfter=6),
    'h2':      S('h2', fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=NAVY, spaceBefore=14, spaceAfter=5),
    'h3':      S('h3', fontName='Helvetica-Bold', fontSize=11.5, leading=15, textColor=NAVY_LT, spaceBefore=10, spaceAfter=3),
    'body':    S('body', spaceAfter=6),
    'bullet':  S('bullet', leftIndent=16, bulletIndent=4, spaceAfter=3),
    'callout': S('callout', fontSize=10, leading=14, textColor=HexColor('#5a4a1a')),
    'cell':    S('cell', fontSize=9, leading=12.5),
    'cellh':   S('cellh', fontName='Helvetica-Bold', fontSize=9, leading=12.5, textColor=white),
    'code':    S('code', fontName='Courier', fontSize=8.7, leading=12, textColor=HexColor('#12305a')),
    'caption': S('caption', fontSize=9.5, leading=13, textColor=MUTED),
}


# ── Inline Markdown → reportlab mini-markup ──────────────────────────────────
def inline(text: str) -> str:
    text = norm(text)
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # `code`
    text = re.sub(r'`([^`]+)`', r'<font face="Courier" color="#12305a">\1</font>', text)
    # **bold**
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    # *italic* (avoid touching ** already consumed)
    text = re.sub(r'(?<!\*)\*(?!\s)([^*]+?)\*(?!\*)', r'<i>\1</i>', text)
    return text


# ── Table builder ────────────────────────────────────────────────────────────
def col_widths(ncols: int):
    if ncols == 2:
        fr = [0.34, 0.66]
    elif ncols == 3:
        fr = [0.22, 0.40, 0.38]
    elif ncols == 4:
        fr = [0.25, 0.25, 0.25, 0.25]
    else:
        fr = [1.0 / ncols] * ncols
    return [f * CONTENT_W for f in fr]


def build_table(rows):
    header, body = rows[0], rows[1:]
    ncols = len(header)
    data = [[Paragraph(inline(c), ST['cellh']) for c in header]]
    for r in body:
        # pad/truncate to header width
        r = (r + [''] * ncols)[:ncols]
        data.append([Paragraph(inline(c), ST['cell']) for c in r])
    t = Table(data, colWidths=col_widths(ncols), repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), NAVY),
        ('LINEBELOW', (0, 0), (-1, 0), 1.2, GOLD),
        ('GRID', (0, 1), (-1, -1), 0.5, LINE),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, LGRAY]),
    ]
    t.setStyle(TableStyle(style))
    return t


def build_callout(text):
    p = Paragraph(inline(text), ST['callout'])
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), AMBER_BG),
        ('LINEBEFORE', (0, 0), (-1, -1), 3, GOLD),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


def build_code(lines):
    txt = norm('\n'.join(lines))
    p = Preformatted(txt, ST['code'])
    t = Table([[p]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CODE_BG),
        ('LINEBEFORE', (0, 0), (-1, -1), 3, NAVY_LT),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t


# ── Markdown parser → flowables ──────────────────────────────────────────────
def parse(md: str, title_holder: dict):
    lines = md.split('\n')
    flow = []
    i = 0
    n = len(lines)
    para_buf = []

    def flush_para():
        nonlocal para_buf
        if para_buf:
            text = ' '.join(x.strip() for x in para_buf).strip()
            if text:
                flow.append(Paragraph(inline(text), ST['body']))
            para_buf = []

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # fenced code
        if stripped.startswith('```'):
            flush_para()
            i += 1
            code = []
            while i < n and not lines[i].strip().startswith('```'):
                code.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            flow.append(build_code(code))
            flow.append(Spacer(1, 4))
            continue

        # table (pipe rows, with a separator line just after the header)
        if stripped.startswith('|') and i + 1 < n and re.match(r'^\s*\|[\s:|-]+\|\s*$', lines[i + 1]):
            flush_para()
            rows = []
            while i < n and lines[i].strip().startswith('|'):
                raw = lines[i].strip().strip('|')
                if re.match(r'^[\s:|-]+$', raw):  # separator row
                    i += 1
                    continue
                cells = [c.strip() for c in raw.split('|')]
                rows.append(cells)
                i += 1
            if rows:
                flow.append(build_table(rows))
                flow.append(Spacer(1, 6))
            continue

        # blockquote callout (join consecutive > lines)
        if stripped.startswith('>'):
            flush_para()
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(re.sub(r'^\s*>\s?', '', lines[i]))
                i += 1
            flow.append(build_callout(' '.join(x.strip() for x in buf).strip()))
            flow.append(Spacer(1, 6))
            continue

        # headings
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            flush_para()
            level = len(m.group(1))
            text = m.group(2).strip()
            if level == 1:
                if not title_holder.get('title'):
                    title_holder['title'] = text
                    i += 1
                    continue
                flow.append(Paragraph(inline(text), ST['h1']))
            elif level == 2:
                flow.append(Paragraph(inline(text), ST['h2']))
                flow.append(HRFlowable(width='100%', thickness=1, color=GOLD, spaceBefore=1, spaceAfter=5))
            else:
                flow.append(Paragraph(inline(text), ST['h3']))
            i += 1
            continue

        # horizontal rule
        if re.match(r'^(-{3,}|\*{3,}|_{3,})$', stripped):
            flush_para()
            flow.append(Spacer(1, 4))
            i += 1
            continue

        # bullet list
        if re.match(r'^[-*]\s+', stripped):
            flush_para()
            while i < n and re.match(r'^[-*]\s+', lines[i].strip()):
                item = re.sub(r'^[-*]\s+', '', lines[i].strip())
                flow.append(Paragraph(inline(item), ST['bullet'], bulletText='•'))
                i += 1
            flow.append(Spacer(1, 2))
            continue

        # italic-only caption line (e.g. the *subtitle* under the title)
        if stripped.startswith('*') and stripped.endswith('*') and not stripped.startswith('**'):
            flush_para()
            flow.append(Paragraph(inline(stripped), ST['caption']))
            i += 1
            continue

        # blank line → paragraph break
        if stripped == '':
            flush_para()
            i += 1
            continue

        para_buf.append(line)
        i += 1

    flush_para()
    return flow


# ── Page furniture (title banner + running header/footer) ────────────────────
def make_on_page(title_holder):
    def on_page(canvas, doc):
        canvas.saveState()
        pg = canvas.getPageNumber()
        if pg == 1:
            # Title banner
            band_h = 2.5 * inch
            canvas.setFillColor(NAVY)
            canvas.rect(0, PAGE_H - band_h, PAGE_W, band_h, stroke=0, fill=1)
            canvas.setFillColor(GOLD)
            canvas.rect(0, PAGE_H - band_h, PAGE_W, 6, stroke=0, fill=1)
            canvas.setFillColor(white)
            canvas.setFont('Helvetica-Bold', 24)
            canvas.drawString(MARGIN, PAGE_H - 1.15 * inch, 'FieldCommand IMS')
            canvas.setFillColor(GOLD)
            canvas.setFont('Helvetica-Bold', 15)
            canvas.drawString(MARGIN, PAGE_H - 1.5 * inch, 'One-Command Field Server Setup')
            canvas.setFillColor(HexColor('#dce6f2'))
            canvas.setFont('Helvetica', 11)
            canvas.drawString(MARGIN, PAGE_H - 1.85 * inch, 'Quick Start  -  Raspberry Pi 5 + Pironman 5 MAX (Dual NVMe RAID 1)')
        # Footer on every page
        canvas.setFillColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 0.6 * inch, PAGE_W - MARGIN, 0.6 * inch)
        canvas.setFillColor(MUTED)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(MARGIN, 0.42 * inch, 'FieldCommand IMS - One-Command Setup Quick Start')
        canvas.drawRightString(PAGE_W - MARGIN, 0.42 * inch, 'Page %d' % pg)
        canvas.restoreState()
    return on_page


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    repo = os.path.dirname(here)
    default_in = os.path.join(repo, 'docs', 'guides', 'FieldCommand_One_Command_Setup_QuickStart.md')
    default_out = os.path.join(repo, 'docs', 'guides', 'FieldCommand_One_Command_Setup_QuickStart.pdf')
    in_path = sys.argv[1] if len(sys.argv) > 1 else default_in
    out_path = sys.argv[2] if len(sys.argv) > 2 else default_out

    with open(in_path, encoding='utf-8') as fh:
        md = fh.read()

    title_holder = {}
    flow = parse(md, title_holder)
    # Push content below the title banner on page 1.
    flow.insert(0, Spacer(1, 1.9 * inch))

    doc = BaseDocTemplate(
        out_path, pagesize=letter,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=0.8 * inch,
        title='FieldCommand IMS - One-Command Field Server Setup (Quick Start)',
        author='James Rospopo, KE4CON',
    )
    frame = Frame(MARGIN, 0.7 * inch, CONTENT_W, PAGE_H - MARGIN - 0.7 * inch, id='body')
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=make_on_page(title_holder))])
    doc.build(flow)
    print('Wrote', out_path, '(%d flowables)' % len(flow))


if __name__ == '__main__':
    main()
