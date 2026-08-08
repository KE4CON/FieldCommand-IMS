#!/usr/bin/env python3
"""
gen_private_docs_setup.py — printable how-to for Option A:
keeping docs/internal in a separate PRIVATE git repo (nested inside the public
repo) for cross-machine sync. Output: docs/internal/FieldCommand_Private_Docs_Setup.pdf
(docs/internal is git-ignored, so the PDF itself stays private.)
"""
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, ListFlowable, ListItem)
from reportlab.pdfgen import canvas

EOC=HexColor('#1a3a6b'); EOC_LT=HexColor('#2d6ab4'); EOC_BG=HexColor('#eef2f7')
GOLD=HexColor('#f0c040'); LINE=HexColor('#c0cfe0'); CODEBG=HexColor('#f4f6f9')
CODEBD=HexColor('#c7d2e0'); GREEN=HexColor('#1a7a3a'); GREEN_BG=HexColor('#e6f4ea')
AMBER=HexColor('#c8760a'); AMBER_BG=HexColor('#fef3d8'); RED=HexColor('#b82020')
RED_BG=HexColor('#fbe9e9'); MUTED=HexColor('#4a6080')
PAGE_W,PAGE_H=letter; M=0.7*inch; CW=PAGE_W-2*M

def S(name,**kw):
    b=dict(fontName='Helvetica',fontSize=10,leading=14,textColor=HexColor('#1a1a1a')); b.update(kw)
    return ParagraphStyle(name,**b)
BODY=S('body',spaceAfter=5)
H1S=S('h1',fontName='Helvetica-Bold',fontSize=15,leading=19,textColor=EOC,spaceBefore=10,spaceAfter=6)
H2S=S('h2',fontName='Helvetica-Bold',fontSize=12,leading=16,textColor=EOC_LT,spaceBefore=9,spaceAfter=3)
STEPS=S('steps',fontSize=10,leading=15)
CODES=S('code',fontName='Courier',fontSize=8.8,leading=12.5,textColor=HexColor('#12233a'))
NOTES=S('note',fontSize=9.2,leading=12.5)
SMALL=S('small',fontSize=8.5,leading=11,textColor=MUTED)
COVERT=S('ct',fontName='Helvetica-Bold',fontSize=25,leading=29,textColor=white)
COVERS=S('cs',fontSize=13,leading=18,textColor=HexColor('#dfe8f5'))

def P(t,st=BODY): return Paragraph(t,st)
def SP(h=6): return Spacer(1,h)
def HR(): return HRFlowable(width='100%',thickness=0.5,color=LINE,spaceBefore=3,spaceAfter=5)

def Code(lines):
    txt='<br/>'.join((l.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') or '&nbsp;') for l in lines)
    t=Table([[Paragraph(txt,CODES)]],colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),CODEBG),('BOX',(0,0),(-1,-1),0.6,CODEBD),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def Note(text,kind='note'):
    cfg={'note':(EOC_LT,EOC_BG,'NOTE'),'tip':(GREEN,GREEN_BG,'TIP'),
         'warn':(AMBER,AMBER_BG,'IMPORTANT'),'stop':(RED,RED_BG,'CAUTION')}
    c,bg,label=cfg.get(kind,cfg['note'])
    t=Table([[Paragraph('<b>%s.</b> %s'%(label,text),NOTES)]],colWidths=[CW])
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),bg),('LINEBEFORE',(0,0),(0,-1),3,c),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    return t

def steps(items,start=1):
    li=[ListItem(Paragraph(x,STEPS),value=start+i) for i,x in enumerate(items)]
    return ListFlowable(li,bulletType='1',bulletFormat='%s.',leftIndent=16,bulletFontName='Helvetica-Bold')

def tbl(headers,rows,widths):
    data=[[Paragraph('<b>%s</b>'%h,S('th',fontSize=9,textColor=white)) for h in headers]]
    for r in rows: data.append([Paragraph(str(c),S('td',fontSize=9,leading=12)) for c in r])
    t=Table(data,colWidths=widths,repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),EOC),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,EOC_BG]),
        ('GRID',(0,0),(-1,-1),0.5,LINE),('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4)]))
    return t

class NC(canvas.Canvas):
    def __init__(self,*a,**k): super().__init__(*a,**k); self._saved=[]
    def showPage(self): self._saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self._saved)
        for st in self._saved:
            self.__dict__.update(st); n=self._pageNumber
            if n==1: self._cover()
            else: self._chrome(n,total)
            super().showPage()
        super().save()
    def _cover(self):
        self.setFillColor(EOC); self.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        self.setFillColor(GOLD); self.rect(0,PAGE_H-0.18*inch,PAGE_W,0.18*inch,fill=1,stroke=0)
        self.setFillColor(GOLD); self.rect(M,PAGE_H-3.4*inch,1.4*inch,0.06*inch,fill=1,stroke=0)
    def _chrome(self,n,total):
        self.setFillColor(EOC); self.rect(0,PAGE_H-0.05*inch,PAGE_W,0.05*inch,fill=1,stroke=0)
        self.setStrokeColor(LINE); self.setLineWidth(0.5); self.line(M,0.55*inch,PAGE_W-M,0.55*inch)
        self.setFont('Helvetica',7.5); self.setFillColor(MUTED)
        self.drawString(M,0.4*inch,'FieldCommand IMS — Private Docs Setup (Option A)')
        self.drawRightString(PAGE_W-M,0.4*inch,'Page %d of %d'%(n-1,total-1))

story=[]
story.append(SP(2.0*inch))
story.append(P('FieldCommand IMS',COVERT))
story.append(P('Private Docs Setup',COVERT))
story.append(SP(0.4*inch))
story.append(P('Option A — keep <b>docs/internal</b> in a separate<br/>PRIVATE git repo, synced across your machines',COVERS))
story.append(SP(1.9*inch))
story.append(P('Internal / author use',S('cd',fontSize=10,textColor=HexColor('#aebfd6'))))
story.append(PageBreak())

story.append(P('The idea',H1S)); story.append(HR())
story.append(P('Right now <b>docs/internal/</b> is an ordinary folder that the PUBLIC repo deliberately ignores. '
    'Option A turns that same folder into its OWN separate git repository with its own PRIVATE remote on GitHub. '
    'You end up with two independent repos that simply sit nested on disk:',BODY))
story.append(Code([
    'FieldCommand-IMS/                 <- PUBLIC repo (github.com/KE4CON/FieldCommand-IMS)',
    '  scripts/  html/  docs/guides/       tracked & public',
    '  .gitignore                          ignores docs/internal/* (except its README)',
    '  docs/internal/                  <- PRIVATE repo (…/FieldCommand-IMS-internal)',
    '    .git/                             the inner repo\'s own history',
    '    FieldCommand_ESV_*.pdf            tracked by the INNER repo only',
    '    FieldCommand_Price_*.pdf',
    '    …',
]))
story.append(P('<b>Why they don\'t collide:</b> the public repo\'s .gitignore says "ignore everything under '
    'docs/internal/," so the public repo never looks inside — it doesn\'t see the private PDFs or the inner .git '
    'folder. The inner repo only knows about the files in docs/internal/. Two repos, two remotes, zero overlap. '
    'The private files literally cannot be pushed to the public remote, because the public repo refuses to track them.',BODY))
story.append(Note('Why not a git "submodule"? A submodule records the PRIVATE repo\'s URL inside the PUBLIC repo '
    '(.gitmodules), which publicly advertises that the private repo exists and where it is. A plain independent '
    '(nested) repo keeps the private repo invisible from the public side — better for privacy.','note'))

story.append(P('Step 1 — Create the empty private repo (github.com, ~1 min)',H1S)); story.append(HR())
story.append(P('This is the one part only you can do (it is your account):',BODY))
story.append(steps([
    'Go to github.com and click <b>New repository</b>.',
    'Name it <b>FieldCommand-IMS-internal</b>.',
    'Set visibility to <b>Private</b> — this is the important part.',
    'Do NOT add a README, .gitignore, or license (leave it completely empty).',
    'Create it. Its URL will be: '
    '<font face="Courier">https://github.com/KE4CON/FieldCommand-IMS-internal.git</font>',
]))

story.append(P('Step 2 — Turn docs/internal into that repo and push (this machine)',H1S)); story.append(HR())
story.append(P('From inside the folder:',BODY))
story.append(Code([
    'cd docs/internal',
    'git init',
    'git add .',
    'git commit -m "Private FieldCommand docs"',
    'git branch -M main',
    'git remote add origin https://github.com/KE4CON/FieldCommand-IMS-internal.git',
    'git push -u origin main',
]))
story.append(P('That uploads all the ESV / business / dev docs to the PRIVATE repo.',BODY))
story.append(Note('On Windows, if a shell "git push" fails with an SSL error (as it does for your main repo), '
    'add this folder as a second repository in GitHub Desktop and push from there instead (see Step 4).','warn'))

story.append(P('Step 3 — Get them onto your Mac (or any other machine)',H1S)); story.append(HR())
story.append(P('On the Mac, after you pull the public repo, docs/internal/ will not exist yet (it is ignored). '
    'Create it by cloning the private repo into that exact spot:',BODY))
story.append(Code(['git clone https://github.com/KE4CON/FieldCommand-IMS-internal.git docs/internal']))
story.append(P('Now the Mac has the private docs too, and both machines stay in sync through the private repo.',BODY))

story.append(P('Step 4 — GitHub Desktop (your normal workflow)',H1S)); story.append(HR())
story.append(P('GitHub Desktop handles one repo at a time, so add the private one alongside the public one:',BODY))
story.append(steps([
    'File &rarr; Add Local Repository &rarr; point it at …/FieldCommand-IMS/docs/internal',
    'You now have TWO entries in the repo switcher: FieldCommand-IMS (public) and '
    'FieldCommand-IMS-internal (private).',
    'Switch between them to commit/push each. Regenerating an ESV or price doc shows up as a change in the '
    'PRIVATE repo\'s view; public code changes stay in the public repo\'s view. They never mix.',
]))

story.append(P('Ongoing use — the one habit to remember',H1S)); story.append(HR())
story.append(P('You now have two repos to push, not one:',BODY))
story.append(tbl(['YOU CHANGED…','COMMIT / PUSH IN…'],[
    ['Code, public docs, scripts','FieldCommand-IMS (public)'],
    ['Anything in docs/internal/ (ESV, price, tax, grant, audit, runbook…)','FieldCommand-IMS-internal (private)'],
],[3.0*inch,CW-3.0*inch]))
story.append(P('That is the only real "cost" of Option A — a second push for private material. In exchange you '
    'get version history plus cross-machine sync for the sensitive docs, fully separated from the public project.',BODY))

story.append(P('Gotchas',H1S)); story.append(HR())
story.append(steps([
    '<b>Keep it Private.</b> Double-check the repo\'s visibility is Private in its GitHub settings.',
    '<b>Don\'t force-add into the public repo.</b> Never run "git add -f docs/internal/…" from the outer repo — '
    'the ignore rule is your safety net; do not override it.',
    '<b>The public README stays public.</b> The outer repo tracks docs/internal/README.md (the explainer); the '
    'inner repo will also include it. Harmless — same safe meta-text in both.',
    '<b>History caveat.</b> Files committed to the PUBLIC repo before this folder was made private still live in '
    'the public repo\'s git history. Option A prevents FUTURE exposure; scrubbing the past is a separate '
    'git filter-repo + force-push job.',
]))
story.append(SP(6))
story.append(P('Quick reference — the whole Step 2 in one place:',H2S))
story.append(Code([
    'cd docs/internal',
    'git init && git add . && git commit -m "Private FieldCommand docs"',
    'git branch -M main',
    'git remote add origin https://github.com/KE4CON/FieldCommand-IMS-internal.git',
    'git push -u origin main',
]))

OUT=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 'docs','internal','FieldCommand_Private_Docs_Setup.pdf')
os.makedirs(os.path.dirname(OUT),exist_ok=True)
doc=SimpleDocTemplate(OUT,pagesize=letter,topMargin=0.7*inch,bottomMargin=0.7*inch,
    leftMargin=M,rightMargin=M,title='FieldCommand IMS — Private Docs Setup (Option A)',
    author='James Rospopo KE4CON')
doc.build(story,canvasmaker=NC)
print('BUILT:',OUT)
