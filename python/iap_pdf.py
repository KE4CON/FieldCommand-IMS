# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# IAP PDF Compiler — generates printable PDFs for ICS forms

"""
iap_pdf.py — IAP One-Click PDF Compiler

Generates a single merged PDF of all completed IAP forms for an incident.
Uses ReportLab for rendering each form and pypdf for merging.

Standard IAP form order (FEMA ICS):
  ICS-202 Incident Objectives
  ICS-203 Organization Assignment List
  ICS-204 Assignment Lists (one per division, all periods)
  ICS-205 Radio Communications Plan
  ICS-205A Communications List
  ICS-206 Medical Plan
  ICS-207 Incident Organization Chart
  ICS-208 Site Safety Plan
  ICS-220 Air Operations Summary
  ICS-204 (additional pages)

Each form renders as a standard 8.5" x 11" page with the ICS chrome
(form number badge, incident name, op period) in the header.
"""

import io
import json
import textwrap
from datetime import datetime

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether,
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

try:
    from pypdf import PdfWriter, PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# ── Colours (matching FieldCommand dark theme for print) ─────────────
EOC      = HexColor('#1a3a6b')
EOC_LT   = HexColor('#2558a0')
GOLD     = HexColor('#c8760a')
LIGHT_BG = HexColor('#f0f4f8')
LINE     = HexColor('#c0c8d8')
DARK_TXT = HexColor('#1a1a2e')

W, H = letter  # 8.5 x 11 inches


# ── Page-level chrome ───────────────────────────────────────────────
def _header_footer(canvas, doc, form_num, form_title, incident_name, op_period):
    canvas.saveState()
    # Header bar
    canvas.setFillColor(EOC)
    canvas.rect(0, H - 0.6*inch, W, 0.6*inch, fill=1, stroke=0)
    # Form badge
    canvas.setFillColor(GOLD)
    canvas.rect(0.25*inch, H - 0.55*inch, 0.9*inch, 0.45*inch, fill=1, stroke=0)
    canvas.setFillColor(white)
    canvas.setFont('Helvetica-Bold', 10)
    canvas.drawCentredString(0.7*inch, H - 0.33*inch, form_num)
    # Form title
    canvas.setFont('Helvetica-Bold', 11)
    canvas.drawString(1.25*inch, H - 0.33*inch, form_title)
    # Incident name (right)
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(HexColor('#a0b8d8'))
    canvas.drawRightString(W - 0.3*inch, H - 0.24*inch, incident_name)
    canvas.drawRightString(W - 0.3*inch, H - 0.38*inch, f'Op Period {op_period}')
    # Footer
    canvas.setFillColor(EOC)
    canvas.rect(0, 0, W, 0.35*inch, fill=1, stroke=0)
    canvas.setFillColor(HexColor('#6080b0'))
    canvas.setFont('Helvetica', 7)
    canvas.drawString(0.35*inch, 0.12*inch,
        f'FieldCommand IMS · Generated {datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")}')
    canvas.drawRightString(W - 0.35*inch, 0.12*inch,
        f'Page {doc.page} · Copyright © 2026 James Rospopo KE4CON · CC-BY-SA 4.0')
    canvas.restoreState()


def make_doc(buf, form_num, form_title, incident_name, op_period):
    """Return a SimpleDocTemplate with header/footer already bound."""
    doc = SimpleDocTemplate(
        buf,
        pagesize=letter,
        leftMargin=0.5*inch,  rightMargin=0.5*inch,
        topMargin=0.8*inch,   bottomMargin=0.55*inch,
        title=f'{form_num} — {incident_name}',
        author='FieldCommand IMS',
    )
    doc.incident_name = incident_name
    doc.op_period     = op_period

    def _onPage(canvas, doc):
        _header_footer(canvas, doc, form_num, form_title,
                       doc.incident_name, doc.op_period)
    doc._onPage = _onPage
    doc.build = lambda story, **kw: SimpleDocTemplate.build(
        doc, story, onFirstPage=_onPage, onLaterPages=_onPage, **kw
    )
    return doc


# ── Style helpers ────────────────────────────────────────────────────
def _styles():
    s = getSampleStyleSheet()
    return {
        'heading': ParagraphStyle('h', fontName='Helvetica-Bold', fontSize=9,
                    textColor=EOC, spaceBefore=8, spaceAfter=3,
                    borderPad=2, borderColor=EOC, borderWidth=0,
                    backColor=LIGHT_BG, leftIndent=4),
        'body':    ParagraphStyle('b', fontName='Helvetica', fontSize=8.5,
                    textColor=DARK_TXT, leading=12, spaceAfter=2),
        'small':   ParagraphStyle('sm', fontName='Helvetica', fontSize=7.5,
                    textColor=HexColor('#506080'), leading=10),
        'bold':    ParagraphStyle('bd', fontName='Helvetica-Bold', fontSize=8.5,
                    textColor=DARK_TXT),
        'label':   ParagraphStyle('lbl', fontName='Helvetica-Bold', fontSize=7,
                    textColor=HexColor('#607090'), spaceAfter=1),
    }


def _field_table(pairs, col_widths=None):
    """Render a list of (label, value) pairs as a 2-col table."""
    styles = _styles()
    rows = []
    for label, value in pairs:
        rows.append([
            Paragraph(label, styles['label']),
            Paragraph(str(value or '—'), styles['body']),
        ])
    cw = col_widths or [1.4*inch, W - 2.3*inch]
    t = Table(rows, colWidths=cw, repeatRows=0)
    t.setStyle(TableStyle([
        ('VALIGN',     (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [white, LIGHT_BG]),
        ('GRID',       (0,0), (-1,-1), 0.25, LINE),
        ('LEFTPADDING',(0,0), (-1,-1), 5),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    return t


def _section(title):
    s = _styles()
    return Paragraph(title, s['heading'])


# ── Form renderers ───────────────────────────────────────────────────

def render_ics202(d, incident_name, period):
    """ICS-202 Incident Objectives."""
    buf = io.BytesIO()
    doc = make_doc(buf, 'ICS-202', 'Incident Objectives', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident / Date / Time'))
    story.append(_field_table([
        ('Incident Name',   d.get('incident_name', incident_name)),
        ('Op Period #',     d.get('operational_period_number', str(period))),
        ('From',            d.get('operational_period_from','')),
        ('To',              d.get('operational_period_to','')),
        ('Date Prepared',   d.get('date_prepared','')),
    ]))
    story.append(Spacer(1, 8))

    story.append(_section('2. Incident Objectives'))
    objectives = d.get('objectives','')
    for line in objectives.split('\n'):
        if line.strip():
            story.append(Paragraph(line.strip(), S['body']))
    story.append(Spacer(1, 6))

    story.append(_section('3. Weather / Hazards'))
    story.append(_field_table([
        ('Temperature',   d.get('weather_temp','')),
        ('Wind',          d.get('weather_wind','')),
        ('Sky/Precip',    d.get('weather_sky','')),
        ('Humidity/Vis',  d.get('weather_humidity','')),
        ('Forecast',      d.get('weather_forecast','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('4. Safety Message'))
    safety = d.get('safety_message','')
    for line in textwrap.wrap(safety, 100) or ['—']:
        story.append(Paragraph(line, S['body']))
    story.append(Spacer(1, 8))

    story.append(_section('5. Prepared / Approved By'))
    story.append(_field_table([
        ('Prepared By',  d.get('prepared_by','')),
        ('Date/Time',    d.get('date_time_prepared','')),
        ('Approved By',  d.get('approved_by','')),
        ('Date/Time',    d.get('date_time_approved','')),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf


def render_ics203(d, incident_name, period):
    """ICS-203 Organization Assignment List."""
    buf = io.BytesIO()
    doc = make_doc(buf, 'ICS-203', 'Organization Assignment List', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident Information'))
    story.append(_field_table([
        ('Incident Name',   d.get('incident_name', incident_name)),
        ('Op Period',       d.get('operational_period_number', str(period))),
        ('Date Prepared',   d.get('date_prepared','')),
    ]))
    story.append(Spacer(1, 6))

    # Command
    story.append(_section('2. Incident Command'))
    cmd_pairs = [
        ('Incident Commander', d.get('incident_commander','')),
        ('Deputy IC (Ops)',    d.get('deputy_ic_1','')),
        ('Deputy IC (Other)',  d.get('deputy_ic_2','')),
        ('Safety Officer',     d.get('safety_officer','')),
        ('PIO',               d.get('public_info_officer','')),
        ('Liaison Officer',   d.get('liaison_officer','')),
    ]
    story.append(_field_table(cmd_pairs))
    story.append(Spacer(1, 6))

    # Section chiefs
    story.append(_section('3. Section Chiefs'))
    story.append(_field_table([
        ('Operations',      d.get('ops_section_chief','')),
        ('Planning',        d.get('planning_section_chief','')),
        ('Logistics',       d.get('logistics_section_chief','')),
        ('Finance/Admin',   d.get('finance_section_chief','')),
    ]))
    story.append(Spacer(1, 6))

    # Branches/Divisions
    story.append(_section('4. Operations Section — Branch / Division Assignments'))
    branch_rows = [['Branch/Division','Supervisor/Leader','Contact']]
    for key, label in [
        ('div_a_sup','Division A'), ('div_b_sup','Division B'), ('div_c_sup','Division C'),
        ('div_d_sup','Division D'), ('div_e_sup','Division E'), ('div_f_sup','Division F'),
    ]:
        if d.get(key):
            branch_rows.append([label, d.get(key,''), d.get(key+'_contact','')])
    bt = Table(branch_rows, colWidths=[1.8*inch, 2.8*inch, 2.2*inch], repeatRows=1)
    bt.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,0), EOC),
        ('TEXTCOLOR',   (0,0),(-1,0), white),
        ('FONTNAME',    (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',    (0,0),(-1,-1), 8),
        ('GRID',        (0,0),(-1,-1), 0.25, LINE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_BG]),
        ('LEFTPADDING', (0,0),(-1,-1), 5),
        ('TOPPADDING',  (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    story.append(bt)
    story.append(Spacer(1, 6))

    story.append(_section('5. Prepared By'))
    story.append(_field_table([
        ('Prepared By',  d.get('prepared_by','')),
        ('Date/Time',    d.get('date_time_prepared','')),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf


def render_ics204(d, incident_name, period, div_label=''):
    """ICS-204 Assignment List."""
    buf = io.BytesIO()
    div = d.get('division_group', div_label or 'Division')
    doc = make_doc(buf, 'ICS-204', f'Assignment List — {div}', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident / Branch / Division'))
    story.append(_field_table([
        ('Incident Name',    d.get('incident_name', incident_name)),
        ('Op Period',        d.get('operational_period_number', str(period))),
        ('Branch',           d.get('branch','')),
        ('Division/Group',   d.get('division_group','')),
        ('Staging Area',     d.get('staging_area','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('2. Operations Personnel'))
    story.append(_field_table([
        ('Ops Section Chief',       d.get('ops_section_chief','')),
        ('Branch Director',         d.get('branch_director','')),
        ('Division/Group Supervisor', d.get('division_group_supervisor','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('3. Resources Assigned'))
    res_rows = [['Resource ID / Designator', 'Leader', 'Type', '# Personnel', 'Contact']]
    for i in range(30):
        rid  = d.get(f'res204_id_{i}','')
        rldr = d.get(f'res204_leader_{i}','')
        rtyp = d.get(f'res204_type_{i}','')
        rnum = d.get(f'res204_num_{i}','')
        rcon = d.get(f'res204_contact_{i}','')
        if not rid and not rldr:
            if i > 5: break
            continue
        is_placeholder = rid.endswith('+')
        row = [rid or '—', rldr or '—', rtyp or '—', str(rnum or ''), rcon or '']
        res_rows.append(row)
    rt = Table(res_rows, colWidths=[1.4*inch,1.8*inch,1.0*inch,0.8*inch,1.8*inch], repeatRows=1)
    rt.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,0), EOC),
        ('TEXTCOLOR',    (0,0),(-1,0), white),
        ('FONTNAME',     (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,-1), 7.5),
        ('GRID',         (0,0),(-1,-1), 0.25, LINE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_BG]),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    story.append(rt)
    story.append(Spacer(1, 6))

    story.append(_section('4. Work Assignments'))
    work = d.get('work_assignments','')
    for line in (work.split('\n') if work else ['—']):
        if line.strip():
            story.append(Paragraph(line.strip(), S['body']))
    story.append(Spacer(1, 6))

    story.append(_section('5. Special Instructions'))
    special = d.get('special_instructions','')
    for line in (special.split('\n') if special else ['None']):
        if line.strip():
            story.append(Paragraph(line.strip(), S['body']))
    story.append(Spacer(1, 6))

    story.append(_section('6. Communications'))
    story.append(_field_table([
        ('Primary Frequency',  d.get('primary_freq','')),
        ('Medical Frequency',  d.get('medical_freq','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('7. Prepared By'))
    story.append(_field_table([
        ('Prepared By',  d.get('prepared_by','')),
        ('Date/Time',    d.get('date_time_prepared','')),
        ('Approved By (OSC)', d.get('approved_by_osc','')),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf


def render_ics205(d, incident_name, period):
    """ICS-205 Radio Communications Plan."""
    buf = io.BytesIO()
    doc = make_doc(buf, 'ICS-205', 'Radio Communications Plan', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident Information'))
    story.append(_field_table([
        ('Incident Name', d.get('incident_name', incident_name)),
        ('Op Period',     d.get('operational_period_number', str(period))),
        ('Date Prepared', d.get('date_prepared','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('2. Basic Radio Channel Use'))
    ch_rows = [['Ch #','Function','Channel Name','RX Freq','RX Tone',
                'TX Freq','TX Tone','Mode','Remarks']]
    for i in range(20):
        name = d.get(f'ch205_name_{i}','')
        if not name: break
        ch_rows.append([
            str(i+1),
            d.get(f'ch205_function_{i}',''),
            name,
            d.get(f'ch205_rx_{i}',''),
            d.get(f'ch205_rx_tone_{i}',''),
            d.get(f'ch205_tx_{i}',''),
            d.get(f'ch205_tone_{i}',''),
            d.get(f'ch205_mode_{i}','FM'),
            d.get(f'ch205_remarks_{i}',''),
        ])
    ct = Table(ch_rows,
               colWidths=[0.35*inch,0.75*inch,1.2*inch,0.75*inch,0.55*inch,
                          0.75*inch,0.55*inch,0.45*inch,1.3*inch],
               repeatRows=1)
    ct.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,0), EOC),
        ('TEXTCOLOR',    (0,0),(-1,0), white),
        ('FONTNAME',     (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,-1), 7),
        ('GRID',         (0,0),(-1,-1), 0.25, LINE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_BG]),
        ('LEFTPADDING',  (0,0),(-1,-1), 3),
        ('TOPPADDING',   (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    story.append(ct)
    story.append(Spacer(1, 8))

    story.append(_section('3. Prepared By'))
    story.append(_field_table([
        ('Prepared By (COML)',  d.get('prepared_by_coml', d.get('prepared_by',''))),
        ('Date/Time',           d.get('date_time_prepared','')),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf


def render_ics206(d, incident_name, period):
    """ICS-206 Medical Plan."""
    buf = io.BytesIO()
    doc = make_doc(buf, 'ICS-206', 'Medical Plan', incident_name, period)
    S = _styles()
    story = []

    story.append(_section('1. Incident Information'))
    story.append(_field_table([
        ('Incident Name', d.get('incident_name', incident_name)),
        ('Op Period',     d.get('operational_period_number', str(period))),
        ('Date Prepared', d.get('date_prepared','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('2. Medical Aid Stations'))
    med_rows = [['Station Name','Location','Personnel','Contact / Channel','Paramedic?']]
    for i in range(8):
        name = d.get(f'med_station_{i}','')
        if not name and i > 2: break
        med_rows.append([
            name or '—',
            d.get(f'med_location_{i}',''),
            d.get(f'med_personnel_{i}',''),
            d.get(f'med_contact_{i}',''),
            d.get(f'med_paramedic_{i}',''),
        ])
    mt = Table(med_rows, colWidths=[1.3*inch,1.5*inch,1.5*inch,1.5*inch,0.8*inch], repeatRows=1)
    mt.setStyle(TableStyle([
        ('BACKGROUND',   (0,0),(-1,0), EOC),
        ('TEXTCOLOR',    (0,0),(-1,0), white),
        ('FONTNAME',     (0,0),(-1,0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0,0),(-1,-1), 8),
        ('GRID',         (0,0),(-1,-1), 0.25, LINE),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white,LIGHT_BG]),
        ('LEFTPADDING',  (0,0),(-1,-1), 4),
        ('TOPPADDING',   (0,0),(-1,-1), 3),
        ('BOTTOMPADDING',(0,0),(-1,-1), 3),
    ]))
    story.append(mt)
    story.append(Spacer(1, 6))

    story.append(_section('3. Evacuation Routes'))
    routes = d.get('evacuation_routes','') or d.get('evac_routes','')
    for line in (routes.split('\n') if routes else ['See incident map']):
        if line.strip():
            story.append(Paragraph(line.strip(), S['body']))
    story.append(Spacer(1, 6))

    story.append(_section('4. Hospitals'))
    story.append(_field_table([
        ('Hospital 1', d.get('hospital_1','')),
        ('Address',    d.get('hospital_1_addr','')),
        ('Phone',      d.get('hospital_1_phone','')),
        ('Travel Time',d.get('hospital_1_time','')),
        ('Hospital 2', d.get('hospital_2','')),
        ('Address',    d.get('hospital_2_addr','')),
    ]))
    story.append(Spacer(1, 6))

    story.append(_section('5. Medical Emergency Procedures'))
    procs = d.get('med_procedures','') or d.get('emergency_procedures','')
    for line in (procs.split('\n') if procs else ['Follow standard EMS protocols']):
        if line.strip():
            story.append(Paragraph(line.strip(), S['body']))
    story.append(Spacer(1, 6))

    story.append(_section('6. Prepared By'))
    story.append(_field_table([
        ('Prepared By (MEDL)', d.get('prepared_by_medl', d.get('prepared_by',''))),
        ('Date/Time',          d.get('date_time_prepared','')),
        ('Approved By (LSC)',  d.get('approved_by_lsc','')),
    ]))

    doc.build(story)
    buf.seek(0)
    return buf


def render_generic(d, form_num, form_title, incident_name, period):
    """Generic fallback renderer for forms without a specific template."""
    buf = io.BytesIO()
    doc = make_doc(buf, form_num.upper(), form_title, incident_name, period)
    S = _styles()
    story = []

    story.append(_section('Form Data'))
    skip_keys = {'incident_id','form_type','period','summary','created','updated','id'}
    pairs = [(k.replace('_',' ').title(), str(v))
             for k, v in sorted(d.items())
             if k not in skip_keys and v and str(v).strip()]
    if pairs:
        story.append(_field_table(pairs))
    else:
        story.append(Paragraph('No data entered for this form.', S['body']))

    doc.build(story)
    buf.seek(0)
    return buf


# ── IAP title page ───────────────────────────────────────────────────
def render_title_page(incident_name, period, prepared_by='', date_str=''):
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=letter,
        leftMargin=inch, rightMargin=inch,
        topMargin=1.5*inch, bottomMargin=inch,
    )
    S = _styles()
    story = []

    # Big navy block
    title_style = ParagraphStyle('title',
        fontName='Helvetica-Bold', fontSize=28,
        textColor=white, alignment=TA_CENTER,
        spaceAfter=12, backColor=EOC,
        borderPad=20,
    )
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph('INCIDENT ACTION PLAN', title_style))
    story.append(Spacer(1, 0.4*inch))

    sub_style = ParagraphStyle('sub',
        fontName='Helvetica', fontSize=18,
        textColor=EOC, alignment=TA_CENTER, spaceAfter=8,
    )
    story.append(Paragraph(incident_name, sub_style))
    story.append(Paragraph(f'Operational Period {period}', ParagraphStyle(
        'per', fontName='Helvetica', fontSize=13,
        textColor=HexColor('#607090'), alignment=TA_CENTER, spaceAfter=40,
    )))

    story.append(HRFlowable(width='80%', color=GOLD, thickness=2))
    story.append(Spacer(1, 0.4*inch))

    info_style = ParagraphStyle('info',
        fontName='Helvetica', fontSize=11,
        textColor=HexColor('#404060'), alignment=TA_CENTER, leading=20,
    )
    if prepared_by:
        story.append(Paragraph(f'Prepared by: {prepared_by}', info_style))
    if date_str:
        story.append(Paragraph(f'Date: {date_str}', info_style))

    story.append(Spacer(1, 1*inch))
    story.append(Paragraph(
        'FieldCommand IMS · Copyright © 2026 James Rospopo KE4CON\n'
        'Developed for McHenry County Emergency Services Volunteers (K9ESV)',
        ParagraphStyle('foot', fontName='Helvetica', fontSize=7.5,
                       textColor=HexColor('#909090'), alignment=TA_CENTER, leading=11)
    ))

    doc.build(story)
    buf.seek(0)
    return buf


# ── Main compile function ─────────────────────────────────────────────
IAP_FORM_ORDER = [
    ('ics202', 'ICS-202 Incident Objectives'),
    ('ics203', 'ICS-203 Organization Assignment List'),
    ('ics204', 'ICS-204 Assignment Lists'),
    ('ics205', 'ICS-205 Radio Communications Plan'),
    ('ics205a','ICS-205A Communications List'),
    ('ics206', 'ICS-206 Medical Plan'),
    ('ics208', 'ICS-208 Site Safety Plan'),
    ('ics220', 'ICS-220 Air Operations Summary'),
    ('ics230', 'ICS-230 Meeting Schedule'),
]

RENDERERS = {
    'ics202': render_ics202,
    'ics203': render_ics203,
    'ics204': render_ics204,
    'ics205': render_ics205,
    'ics206': render_ics206,
}


def compile_iap(forms_by_type, incident_name, period,
                prepared_by='', date_str='', include_title=True):
    """
    Compile all IAP forms into a single merged PDF.

    Args:
        forms_by_type: dict of {form_type: [form_data_dict, ...]}
        incident_name: str
        period: int or str
        prepared_by: str (for title page)
        date_str: str (for title page)
        include_title: bool

    Returns:
        bytes — the merged PDF
    """
    if not HAS_PYPDF:
        raise RuntimeError('pypdf not installed — cannot merge PDFs')

    writer = PdfWriter()

    # Title page
    if include_title:
        title_buf = render_title_page(incident_name, period, prepared_by, date_str)
        writer.append(PdfReader(title_buf))

    # Render forms in IAP order
    for form_type, form_title in IAP_FORM_ORDER:
        form_list = forms_by_type.get(form_type, [])
        if not form_list:
            continue

        renderer = RENDERERS.get(form_type)

        for fdata in form_list:
            try:
                if renderer:
                    buf = renderer(fdata, incident_name, period)
                else:
                    buf = render_generic(fdata, form_type,
                                         form_title, incident_name, period)
                writer.append(PdfReader(buf))
            except Exception as e:
                # Log and continue — don't let one bad form break the whole IAP
                import traceback
                traceback.print_exc()

    # Render any forms not in IAP_FORM_ORDER that were requested
    ordered_types = {ft for ft, _ in IAP_FORM_ORDER}
    for form_type, form_list in forms_by_type.items():
        if form_type in ordered_types or not form_list:
            continue
        for fdata in form_list:
            try:
                buf = render_generic(fdata, form_type,
                                     form_type.upper(), incident_name, period)
                writer.append(PdfReader(buf))
            except Exception:
                pass

    out = io.BytesIO()
    writer.write(out)
    return out.getvalue()
