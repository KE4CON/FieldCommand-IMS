#!/usr/bin/env python3
"""
gen_testing_runbook.py — FieldCommand IMS internal TESTING runbook.
A complete, step-by-step guide for the author to test the automated
insert-and-go setup (Windows prep, Mac prep, full install, pull-a-drive,
reset/re-run). Not a shipped end-user document.
Output: docs/FieldCommand_Testing_Runbook.pdf
"""
import datetime, os
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, HRFlowable, ListFlowable,
                                ListItem)
from reportlab.pdfgen import canvas

# ── Palette ──────────────────────────────────────────────────────────────────
EOC    = HexColor('#1a3a6b')
EOC_LT = HexColor('#2d6ab4')
EOC_BG = HexColor('#eef2f7')
GOLD   = HexColor('#f0c040')
LINE   = HexColor('#c0cfe0')
CODEBG = HexColor('#f4f6f9')
CODEBD = HexColor('#c7d2e0')
GREEN  = HexColor('#1a7a3a')
GREEN_BG = HexColor('#e6f4ea')
AMBER  = HexColor('#c8760a')
AMBER_BG = HexColor('#fef3d8')
RED    = HexColor('#b82020')
RED_BG = HexColor('#fbe9e9')
MUTED  = HexColor('#4a6080')

TODAY  = datetime.date.today().strftime('%B %d, %Y')
PAGE_W, PAGE_H = letter
M  = 0.7*inch
CW = PAGE_W - 2*M

# ── Styles ─────────────────────────────────────────────────────────────────
def S(name, **kw):
    base = dict(fontName='Helvetica', fontSize=10, leading=14, textColor=HexColor('#1a1a1a'))
    base.update(kw); return ParagraphStyle(name, **base)

BODY = S('body', spaceAfter=5)
H1S  = S('h1', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=EOC, spaceBefore=10, spaceAfter=6)
H2S  = S('h2', fontName='Helvetica-Bold', fontSize=12.5, leading=16, textColor=EOC_LT, spaceBefore=10, spaceAfter=4)
H3S  = S('h3', fontName='Helvetica-Bold', fontSize=10.5, leading=14, textColor=HexColor('#25344a'), spaceBefore=6, spaceAfter=2)
STEPS= S('steps', fontSize=10, leading=15, leftIndent=2)
CODES= S('code', fontName='Courier', fontSize=8.8, leading=12, textColor=HexColor('#12233a'))
NOTES= S('note', fontSize=9.2, leading=12.5)
SMALL= S('small', fontSize=8.5, leading=11, textColor=MUTED)
COVERT = S('covert', fontName='Helvetica-Bold', fontSize=26, leading=30, textColor=white, alignment=TA_LEFT)
COVERS = S('covers', fontSize=13, leading=18, textColor=HexColor('#dfe8f5'), alignment=TA_LEFT)

def P(t, st=BODY): return Paragraph(t, st)
def SP(h=6): return Spacer(1, h)
def HR(c=LINE, t=0.5): return HRFlowable(width='100%', thickness=t, color=c, spaceBefore=3, spaceAfter=5)

def Code(lines):
    txt = '<br/>'.join(l.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;') or '&nbsp;' for l in lines)
    t = Table([[Paragraph(txt, CODES)]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),CODEBG), ('BOX',(0,0),(-1,-1),0.6,CODEBD),
        ('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return t

def Note(text, kind='note'):
    cfg = {'note':(EOC_LT,EOC_BG,'NOTE'),'tip':(GREEN,GREEN_BG,'TIP'),
           'warn':(AMBER,AMBER_BG,'IMPORTANT'),'stop':(RED,RED_BG,'CAUTION')}
    c,bg,label = cfg.get(kind, cfg['note'])
    inner = Paragraph('<b>%s.</b> %s' % (label, text), NOTES)
    t = Table([[inner]], colWidths=[CW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),bg), ('LINEBEFORE',(0,0),(0,-1),3,c),
        ('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),
        ('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6),
    ]))
    return t

def steps(items, start=1):
    li = [ListItem(Paragraph(x, STEPS), value=start+i) for i,x in enumerate(items)]
    return ListFlowable(li, bulletType='1', bulletFormat='%s.', leftIndent=16, bulletFontName='Helvetica-Bold')

def checks(items):
    rows = [[Paragraph('&#9744;', S('cb', fontSize=12)), Paragraph(x, STEPS)] for x in items]
    t = Table(rows, colWidths=[0.3*inch, CW-0.3*inch])
    t.setStyle(TableStyle([
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('TOPPADDING',(0,0),(-1,-1),2),('BOTTOMPADDING',(0,0),(-1,-1),2),
        ('LEFTPADDING',(0,0),(0,-1),2),
    ]))
    return t

def tbl(headers, rows, widths):
    data = [[Paragraph('<b>%s</b>'%h, S('th', fontSize=9, textColor=white)) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), S('td', fontSize=9, leading=12)) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),EOC),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[white, EOC_BG]),
        ('GRID',(0,0),(-1,-1),0.5,LINE),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
    ]))
    return t

# ── Canvas with cover + footer ──────────────────────────────────────────────
class NC(canvas.Canvas):
    def __init__(self, *a, **kw):
        super().__init__(*a, **kw); self._saved=[]
    def showPage(self): self._saved.append(dict(self.__dict__)); self._startPage()
    def save(self):
        total=len(self._saved)
        for st in self._saved:
            self.__dict__.update(st); self.TOTAL=total; n=self._pageNumber
            if n==1: self._cover()
            else: self._chrome(n,total)
            super().showPage()
        super().save()
    def _cover(self):
        self.setFillColor(EOC); self.rect(0,0,PAGE_W,PAGE_H,fill=1,stroke=0)
        self.setFillColor(GOLD); self.rect(0,PAGE_H-0.18*inch,PAGE_W,0.18*inch,fill=1,stroke=0)
        self.setFillColor(GOLD); self.rect(M,PAGE_H-3.5*inch,1.4*inch,0.06*inch,fill=1,stroke=0)
    def _chrome(self,n,total):
        self.setFillColor(EOC); self.rect(0,PAGE_H-0.05*inch,PAGE_W,0.05*inch,fill=1,stroke=0)
        self.setStrokeColor(LINE); self.setLineWidth(0.5)
        self.line(M,0.55*inch,PAGE_W-M,0.55*inch)
        self.setFont('Helvetica',7.5); self.setFillColor(MUTED)
        self.drawString(M,0.4*inch,'FieldCommand IMS — Testing Runbook (internal)')
        self.drawRightString(PAGE_W-M,0.4*inch,'Page %d of %d'%(n-1,total-1))

# ── Build ────────────────────────────────────────────────────────────────────
story=[]

# Cover content (placed over the navy canvas)
story.append(SP(2.1*inch))
story.append(P('FieldCommand IMS', COVERT))
story.append(P('Testing Runbook', COVERT))
story.append(SP(0.5*inch))
story.append(P('Step-by-step guide to test the automated<br/>insert-and-go field-server setup', COVERS))
story.append(SP(0.35*inch))
story.append(P('Windows prep &bull; Mac prep &bull; full install &bull; failover &bull; reset', COVERS))
story.append(SP(1.7*inch))
story.append(P('Internal / author use &bull; %s' % TODAY, S('cd', fontSize=10, textColor=HexColor('#aebfd6'))))
story.append(PageBreak())

# ── 0. Read me first ─────────────────────────────────────────────────────────
story.append(P('0.  Read this first', H1S)); story.append(HR())
story.append(P('This runbook tests the automated setup you built: a single Pironman 5 MAX (Raspberry Pi 5) '
               'with two NVMe SSDs, prepared from either Windows or a Mac, that installs FieldCommand IMS by '
               'itself on first boot.', BODY))
story.append(Note('You have ONE Pironman and TWO SSDs, and a full install erases both SSDs. You do NOT need to '
                  'wipe and reinstall twice to test both preppers. The Windows and Mac preppers do the exact '
                  'same job and only write to the SD card&rsquo;s boot partition &mdash; they never touch the SSDs. '
                  'So: verify both preppers by inspecting the prepared card (Phase 1, non-destructive), then run '
                  'the full install on the Pi just once (Phase 2).', 'tip'))
story.append(Note('The first-boot auto-run relies on a Raspberry Pi boot mechanism that could not be tested '
                  'before shipping. Treat this whole run as the first real validation. Use the <b>--dry-run</b> '
                  'previews where offered, and keep this sheet handy to record what happens.', 'warn'))

story.append(P('What you need on hand', H3S))
story.append(checks([
    'Raspberry Pi 5 (16 GB) in the Pironman 5 MAX, with BOTH NVMe SSDs installed and the SunFounder ribbon cable seated.',
    'One microSD card (16 GB+; 64 GB is fine) and an SD card reader for your computer.',
    'A monitor, keyboard, and mouse connected to the Pi.',
    'A Windows PC and a Mac (to test both preppers).',
    'Raspberry Pi Imager installed on each computer (raspberrypi.com/software).',
    'The FieldCommand-IMS files (Code &rarr; Download ZIP on GitHub, or git clone).',
    'Internet for the Pi during install (Ethernet or Wi-Fi) — packages and data download during setup.',
]))
story.append(PageBreak())

# ── 1. Phase 1: test the preppers (non-destructive) ──────────────────────────
story.append(P('1.  Phase 1 &mdash; Test the Windows &amp; Mac preppers (no SSD wipe)', H1S)); story.append(HR())
story.append(P('Goal: prove each prepper correctly prepares an SD card. This never touches the SSDs and does not '
               'require booting the Pi.', BODY))

story.append(P('1A.  Windows prepper', H2S))
story.append(steps([
    'On the Windows PC, flash <b>Raspberry Pi OS (64-bit, Desktop)</b> to the SD card with Raspberry Pi Imager. '
    'In the Imager settings, set the username to <b>fieldcommand</b> (and optionally Wi-Fi/locale).',
    'Leave the card in the reader. Windows shows a drive named <b>bootfs</b>.',
    'Open the FieldCommand-IMS folder &rarr; <b>scripts</b> &rarr; double-click <b>prep-sd-card.bat</b>.',
    'When it lists the detected card, confirm it is the right drive and type <b>YES</b>.',
    'Wait for &ldquo;Card is ready.&rdquo;',
]))
story.append(P('Then verify the card &mdash; open the <b>bootfs</b> drive and confirm it now contains:', H3S))
story.append(checks([
    'A <b>FieldCommand-IMS</b> folder (with scripts, html, python, docs inside).',
    'A file <b>firstrun-fieldcommand.sh</b>.',
    'A file <b>cmdline.txt.fieldcommand-backup</b> (the safety backup).',
    'cmdline.txt ends with &ldquo;... systemd.run=/boot/firmware/firstrun-fieldcommand.sh ...&rdquo; '
    '&mdash; OR, if you used Imager customization, <b>firstrun.sh</b> contains a &ldquo;fieldcommand-setup.desktop&rdquo; block.',
]))
story.append(Note('To read cmdline.txt on Windows, right-click it &rarr; Open with &rarr; Notepad. It is one long '
                  'line; do not edit or re-save it.', 'note'))

story.append(P('1B.  Mac prepper', H2S))
story.append(steps([
    'On the Mac, flash the SAME card again with Raspberry Pi OS (64-bit, Desktop) using Raspberry Pi Imager '
    '(re-flashing wipes the previous test cleanly), username <b>fieldcommand</b>.',
    'The card mounts as <b>/Volumes/bootfs</b>.',
    'Open FieldCommand-IMS &rarr; <b>scripts</b> &rarr; double-click <b>prep-sd-card.command</b>. '
    'If macOS blocks it, right-click &rarr; Open &rarr; Open. (If double-click does nothing, it needs run '
    'permission: in Terminal run  chmod +x  on the file, then try again.)',
    'Confirm the card and type <b>YES</b>.',
]))
story.append(P('Verify the card the same way as 1A &mdash; the same four items should be present.', BODY))
story.append(Note('If both cards end up with the same four items, both preppers are proven. The SSDs were never '
                  'touched. You can now do the single full install (Phase 2) with either card.', 'tip'))
story.append(PageBreak())

# ── 2. Phase 2: full install ─────────────────────────────────────────────────
story.append(P('2.  Phase 2 &mdash; Full install on the Pi (the one destructive run)', H1S)); story.append(HR())
story.append(Note('This ERASES BOTH SSDs. Make sure they contain nothing you want to keep.', 'stop'))
story.append(P('Use either prepped card from Phase 1.', BODY))

story.append(P('2A.  Boot and start', H2S))
story.append(steps([
    'Insert the prepped card into the Pi (both SSDs installed). Connect monitor, keyboard, Ethernet, and power on.',
    'On first boot the Pi may run the Raspberry Pi OS welcome steps (country, Wi-Fi, updates) if you did not '
    'preset them in Imager. Complete them; they are normal.',
    'The <b>FieldCommand Setup</b> window should open by itself on the desktop. '
    '(If it does not, see Troubleshooting &mdash; you can launch it by hand.)',
]))
story.append(Note('Recommended for THIS first run: when the setup window opens, let it do a preview first. If it '
                  'went straight to the real run, you can always stop it before typing YES. A manual dry run is: '
                  'open a terminal and run  bash /boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh --dry-run', 'warn'))

story.append(P('2B.  What to expect, in order', H2S))
story.append(steps([
    '<b>Detect both SSDs.</b> If the Pi cannot yet see both drives, the script adds the two Pironman PCIe lines '
    'to config.txt and reboots ONCE. After that reboot the setup re-opens by itself and continues. '
    '(This is expected, not a failure.)',
    '<b>Answer the questions</b> on screen: callsign (or leave blank &mdash; see 2D), location, Wi-Fi name, and a '
    'few options.',
    '<b>Confirm the wipe.</b> The script shows the two SSDs and asks you to type <b>YES</b>. This is the only '
    'destructive confirmation.',
    '<b>Build + copy.</b> It partitions the drives, builds the RAID 1 mirror, formats, and copies the OS onto the '
    'mirror (this takes a while). It sets the boot order to NVMe-first.',
    '<b>Reboot into the mirror.</b> The Pi reboots and boots from the SSDs. On that first boot a one-time service '
    'runs the FieldCommand installer automatically (packages, services, web app).',
    '<b>Done.</b> It prints a completion message and the pull-a-drive instructions.',
]))

story.append(P('2C.  Verify the install worked', H2S))
story.append(checks([
    'After the final boot, on the Pi open a terminal and run  <b>cat /proc/mdstat</b>  &mdash; you should see '
    '&ldquo;md0 : active raid1&rdquo; with [UU] (both drives up).',
    'Run  <b>findmnt /</b>  &mdash; the root should be on <b>/dev/md0</b> (running from the mirror).',
    'From a device on the FieldCommand Wi-Fi network, browse to <b>http://192.168.50.1/</b> &mdash; the dashboard loads.',
    'Confirm services:  <b>systemctl --failed</b>  shows no critical FieldCommand services failed.',
]))

story.append(P('2D.  Test the callsign gating (do this twice if you can)', H2S))
story.append(tbl(['SETUP CHOICE', 'EXPECTED RESULT ON THE DASHBOARD'], [
    ['Callsign LEFT BLANK',
     'The &ldquo;Amateur Radio&rdquo; mode button is grayed out / disabled with a hint, and the dashboard opens '
     'in ICS mode. Public-safety and ICS tools all work. Later: open Setup, add a callsign, save &mdash; the '
     'Amateur Radio mode becomes available.'],
    ['Callsign ENTERED (e.g. K9ESV)',
     'The &ldquo;Amateur Radio&rdquo; mode button is active and its tools appear.'],
], [1.7*inch, CW-1.7*inch]))
story.append(Note('In the Setup wizard, also confirm you cannot switch on the Amateur / Winlink / APRS / 44Net '
                  'modules while the callsign field is blank &mdash; it should warn you and refuse.', 'note'))
story.append(PageBreak())

# ── 3. Pull-a-drive ──────────────────────────────────────────────────────────
story.append(P('3.  Pull-a-drive failover test (do not skip)', H1S)); story.append(HR())
story.append(P('This is the whole point of the mirror: prove the Pi keeps running on one drive. Only you can do '
               'it &mdash; it is physical.', BODY))
story.append(steps([
    'Run  <b>sudo poweroff</b>.  Remove the microSD card AND one SSD (call it drive A). Power on.',
    'The Pi MUST boot and FieldCommand MUST come up on drive B alone. Check  http://192.168.50.1/ .',
    'Run  <b>sudo poweroff</b>.  Re-insert A, remove drive B instead. Power on.',
    'The Pi MUST boot on drive A alone.',
    'Run  <b>sudo poweroff</b>.  Re-insert both. Power on. Re-add the drive that was out, e.g.  '
    'sudo mdadm /dev/md0 --add /dev/nvme1n1p2  (use whichever shows as missing in  cat /proc/mdstat ).',
    'Watch  <b>cat /proc/mdstat</b>  resync back to [UU].',
]))
story.append(Note('If the Pi does NOT boot with one drive removed, the mirror is not truly redundant yet &mdash; '
                  'usually the boot files were not written to that drive, or the boot order does not include NVMe. '
                  'Note exactly which case failed and report it.', 'stop'))
story.append(SP(4))

# ── 4. Reset & re-run ────────────────────────────────────────────────────────
story.append(P('4.  Reset &amp; run again (only if you want another full run)', H1S)); story.append(HR())
story.append(P('After a successful install the Pi boots from the SSDs. To wipe and re-test:', BODY))
story.append(P('4A.  Get back to booting the SD card', H3S))
story.append(steps([
    'On the running FieldCommand (SSD) system, open a terminal and run  <b>sudo rpi-eeprom-config --edit</b>.',
    'Change the BOOT_ORDER line to  <b>BOOT_ORDER=0xf461</b>  (SD first), save (Ctrl+O, Enter, Ctrl+X), and reboot.',
]))
story.append(P('4B.  Wipe the SSDs from the SD-booted system', H3S))
story.append(Code([
    '# preview first (changes nothing):',
    'sudo bash /boot/firmware/FieldCommand-IMS/scripts/fc-reset-drives.sh --dry-run',
    '',
    '# then wipe for real (asks you to type YES):',
    'sudo bash /boot/firmware/FieldCommand-IMS/scripts/fc-reset-drives.sh',
]))
story.append(P('It stops the RAID, erases both SSDs, and clears the saved setup state. Then run the setup again '
               'for a fresh install. A successful setup run resets the boot order back to NVMe-first on its own.', BODY))
story.append(Note('If the auto-start setup pops up first and says the array already exists, that is the safety '
                  'guard &mdash; close it, run the reset above, then relaunch the setup.', 'note'))
story.append(SP(4))

# ── 5. Troubleshooting + command reference ───────────────────────────────────
story.append(P('5.  Troubleshooting', H1S)); story.append(HR())
story.append(tbl(['SYMPTOM', 'WHAT TO DO'], [
    ['Setup did not open by itself on the desktop',
     'Launch it by hand: File Manager &rarr; boot drive &rarr; FieldCommand-IMS &rarr; scripts &rarr; desktop &rarr; '
     'double-click &ldquo;1. Preview&rdquo; then &ldquo;2. Install&rdquo;. Or a terminal:  '
     'bash /boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh'],
    ['&ldquo;Only 1 NVMe drive detected&rdquo;',
     'Power off; reseat both SSDs and the SunFounder FFC ribbon cable; power on and retry. The script also '
     'reboots once to enable PCIe &mdash; let it.'],
    ['&ldquo;/dev/md0 already exists&rdquo;',
     'A previous array is still there. Run fc-reset-drives.sh (Section 4B), then retry.'],
    ['Pi boots to SD even after install',
     'Boot order may not include NVMe. Check  rpi-eeprom-config ; it should be BOOT_ORDER=0xf416 after a '
     'successful run.'],
    ['Prepper can&rsquo;t find the card',
     'Make sure the freshly-imaged card is inserted and shows as bootfs. Re-run the prepper.'],
    ['Desktop icon looks inactive',
     'Right-click it &rarr; Allow Launching (Pi OS marks new launchers untrusted).'],
], [1.9*inch, CW-1.9*inch]))

story.append(P('6.  Command &amp; file reference', H1S)); story.append(HR())
story.append(tbl(['ITEM', 'PATH / COMMAND'], [
    ['Card prepper (Windows)', 'FieldCommand-IMS\\scripts\\prep-sd-card.bat'],
    ['Card prepper (Mac)', 'FieldCommand-IMS/scripts/prep-sd-card.command'],
    ['Setup script (on the Pi)', '/boot/firmware/FieldCommand-IMS/scripts/fieldcommand-setup.sh'],
    ['Setup preview (safe)', 'bash .../fieldcommand-setup.sh --dry-run'],
    ['Reset / wipe SSDs', 'bash /boot/firmware/FieldCommand-IMS/scripts/fc-reset-drives.sh'],
    ['RAID health', 'cat /proc/mdstat'],
    ['Which disk is root', 'findmnt /'],
    ['Boot order (EEPROM)', 'sudo rpi-eeprom-config --edit   (NVMe-first 0xf416, SD-first 0xf461)'],
    ['Dashboard', 'http://192.168.50.1/'],
], [1.9*inch, CW-1.9*inch]))
story.append(SP(6))
story.append(P('Record results (date, which prepper, pass/fail at each phase, anything unexpected) and send back '
               'anything that looks wrong &mdash; especially the exact on-screen text of any error.', SMALL))

# ── Emit ─────────────────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'docs', 'FieldCommand_Testing_Runbook.pdf')
doc = SimpleDocTemplate(OUT, pagesize=letter, topMargin=0.7*inch, bottomMargin=0.7*inch,
                        leftMargin=M, rightMargin=M, title='FieldCommand IMS — Testing Runbook',
                        author='James Rospopo KE4CON')
doc.build(story, canvasmaker=NC)
print('BUILT:', OUT)
