# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""
FieldCommand EmComm Main API Server  —  Port 5050
All runtime data stored in /opt/fieldcommand/data/fieldcommand.db via db.py
FCC callsign lookup uses the separate fcc.db (read-only).
"""

import json, sqlite3, time, threading, subprocess, socket
import logging, sys, re, os
from datetime import datetime, timezone
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import db
from db import get_conn, utcnow, jdump, jload, row_to_dict, rows_to_list

_log_handlers = [logging.StreamHandler(sys.stdout)]
try:
    # File log is best-effort: on the Pi /var/log exists; off-Pi (dev/CI/import
    # for tests) it may not, and a missing directory must not crash startup.
    _log_handlers.append(logging.FileHandler('/var/log/fieldcommand-api.log', mode='a'))
except Exception:
    pass
logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [fcc-lookup] %(message)s',
    handlers=_log_handlers)
log = logging.getLogger('fcc-lookup')

BASE    = Path("/opt/fieldcommand")
DATA    = BASE / "data"
FCC_DB  = DATA / "fcc.db"

# ── FCC callsign lookup (separate read-only database) ────────────────────────
def fcc_search(filters, limit=100):
    """Search fcc.db by name/location/class for the callsign Advanced Search page."""
    if not FCC_DB.exists():
        return []
    where = []; params = []
    if filters.get("last_name"):
        where.append("UPPER(e.last_name) LIKE ?"); params.append(filters["last_name"].upper() + "%")
    if filters.get("first_name"):
        where.append("UPPER(e.first_name) LIKE ?"); params.append(filters["first_name"].upper() + "%")
    if filters.get("state"):
        where.append("UPPER(e.state) = ?"); params.append(filters["state"].upper())
    if filters.get("city"):
        where.append("UPPER(e.city) LIKE ?"); params.append(filters["city"].upper() + "%")
    if filters.get("license_class"):
        where.append("a.operator_class = ?"); params.append(filters["license_class"].upper())
    if not where:
        return []
    try:
        lim = max(1, min(500, int(limit)))
    except (ValueError, TypeError):
        lim = 100
    sql = (
        "SELECT e.callsign, e.first_name, e.last_name, e.city, e.state, "
        "h.license_status, h.expired_date, a.operator_class "
        "FROM en e "
        "LEFT JOIN hd h ON e.unique_system_id = h.unique_system_id "
        "LEFT JOIN am a ON e.unique_system_id = a.unique_system_id "
        "WHERE " + " AND ".join(where) + " ORDER BY e.last_name, e.first_name LIMIT ?"
    )
    try:
        conn = sqlite3.connect(str(FCC_DB)); conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params + [lim]).fetchall()
        conn.close()
        out = []
        for r in rows:
            nm = ((r['first_name'] or '') + ' ' + (r['last_name'] or '')).strip()
            out.append({
                "callsign": r["callsign"],
                "name": nm,
                "first_name": r["first_name"] or "", "last_name": r["last_name"] or "",
                "city": r["city"] or "", "state": r["state"] or "",
                "status": r["license_status"] or "",
                "license_class": r["operator_class"] or "",
                "expired_date": r["expired_date"] or "",
            })
        return out
    except Exception:
        return []


def fcc_lookup(callsign):
    if not FCC_DB.exists():
        return None
    call = callsign.upper().strip()
    try:
        conn = sqlite3.connect(str(FCC_DB))
        conn.row_factory = sqlite3.Row
        row = conn.execute("""
            SELECT e.callsign, e.first_name, e.last_name, e.city, e.state,
                   e.zip_code, h.license_status, h.grant_date, h.expired_date,
                   a.operator_class, a.group_code
            FROM en e
            LEFT JOIN hd h ON e.unique_system_id = h.unique_system_id
            LEFT JOIN am a ON e.unique_system_id = a.unique_system_id
            WHERE UPPER(e.callsign) = ?
            LIMIT 1
        """, (call,)).fetchone()
        conn.close()
        if row:
            classes = {"A":"Amateur Extra","G":"General","T":"Technician",
                       "N":"Novice","P":"Advanced"}
            return {
                "callsign":       row["callsign"],
                "name":           f"{row['first_name'] or ''} {row['last_name'] or ''}".strip(),
                "first_name":     row["first_name"] or "",
                "last_name":      row["last_name"] or "",
                "city":           row["city"] or "",
                "state":          row["state"] or "",
                "zip":            row["zip_code"] or "",
                "license_status": row["license_status"] or "",
                "operator_class": classes.get(row["operator_class"] or "",
                                              row["operator_class"] or "Unknown"),
                "class_code":     row["operator_class"] or "",
                "grant_date":     row["grant_date"] or "",
                "expired_date":   row["expired_date"] or "",
                "group_code":     row["group_code"] or "",
            }
    except Exception as e:
        log.warning(f"FCC lookup error: {e}")
    return None

# ── GPS / station position ────────────────────────────────────────────────────
_pos_cache = {"ts": 0}
_POS_TTL   = 10

def get_station_position():
    global _pos_cache
    now = time.time()
    if now - _pos_cache.get("ts", 0) < _POS_TTL:
        return _pos_cache
    c = get_conn()
    row = c.execute("SELECT callsign,lat,lon FROM station_config WHERE id=1").fetchone()
    cfg_call = row["callsign"] if row else "W8EOC"
    cfg_lat  = row["lat"]  if row else 42.3247
    cfg_lon  = row["lon"]  if row else -88.3822
    try:
        s = socket.socket()
        s.settimeout(1.5)
        s.connect(("127.0.0.1", 2947))
        s.send(b"?POLL;\n")
        time.sleep(0.3)
        data = b""
        s.settimeout(0.5)
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk: break
                data += chunk
        except Exception:
            pass
        s.close()
        for line in data.decode(errors="ignore").splitlines():
            if '"class":"TPV"' in line:
                tpv  = json.loads(line)
                mode = tpv.get("mode", 0)
                lat  = tpv.get("lat")
                lon  = tpv.get("lon")
                if mode >= 2 and lat and lon:
                    c.execute("UPDATE station_config SET lat=?,lon=?,gps_last_fix=? WHERE id=1",
                              (round(lat,6), round(lon,6), tpv.get("time","")))
                    c.commit()
                    _pos_cache = {"lat":round(lat,6),"lon":round(lon,6),
                        "alt":tpv.get("alt"),"speed":tpv.get("speed"),
                        "track":tpv.get("track"),"time":tpv.get("time"),
                        "fix":True,"mode":mode,
                        "mode_str":"3D Fix" if mode==3 else "2D Fix",
                        "source":"gps","callsign":cfg_call,"ts":now}
                    return _pos_cache
    except Exception:
        pass
    _pos_cache = {"lat":cfg_lat,"lon":cfg_lon,"alt":None,"speed":None,
        "track":None,"time":None,"fix":False,"mode":0,"mode_str":"No Fix",
        "source":"config" if cfg_lat!=42.3247 else "default",
        "callsign":cfg_call,"ts":now}
    return _pos_cache

# ── Roster helpers ────────────────────────────────────────────────────────────
CERT_COLS  = ["ics100","ics200","ics300","ics400","ics700","ics800",
              "emcomm1","emcomm2","cpr","first_aid","cert"]
EQUIP_COLS = ["hf","vhf","digital","packet","pactor","vara_hf","vara_fm",
              "aprs","winlink","go_box","generator","battery","vehicle"]
# UI labels <-> DB columns. The roster page speaks these labels; the DB uses the
# columns above. Normalize at the API boundary so certs/equipment actually persist.
CERT_LABELS  = {"ics100":"ICS-100","ics200":"ICS-200","ics300":"ICS-300","ics400":"ICS-400",
                "ics700":"ICS-700","ics800":"ICS-800","emcomm1":"EmComm I","emcomm2":"EmComm II",
                "cpr":"CPR/AED","first_aid":"First Aid","cert":"CERT"}
EQUIP_LABELS = {"hf":"HF","vhf":"VHF","digital":"Digital","packet":"Packet","pactor":"PACTOR",
                "vara_hf":"VARA HF","vara_fm":"VARA FM","aprs":"APRS","winlink":"Winlink",
                "go_box":"Go-Box","generator":"Generator","battery":"Battery","vehicle":"Vehicle"}

def member_to_dict(row):
    if row is None: return None
    d = dict(row)
    # Photos can be large; never ship the Base64 blob in list/detail JSON.
    # Expose only a flag — the actual image is served by GET /api/roster/photo.
    d["has_photo"] = bool(d.get("photo_data"))
    d.pop("photo_data", None); d.pop("photo_mime", None)
    d["certifications"] = {CERT_LABELS[c]:  bool(d.pop(f"cert_{c}", 0))  for c in CERT_COLS}
    d["equipment"]      = {EQUIP_LABELS[e]: bool(d.pop(f"equip_{e}", 0)) for e in EQUIP_COLS}
    # role column stores one-or-more roles joined with "; "; expose as a list too
    d["roles"] = [r.strip() for r in str(d.get("role") or "").split(";") if r.strip()]
    # Ensure member_id always present (may be missing on older rows)
    if not d.get("member_id"):
        d["member_id"] = d.get("id", "")
    # display_id priority: callsign → radio_id → member_id
    d["display_id"] = (d.get("callsign") or d.get("radio_id") or
                       d.get("member_id") or d.get("id",""))
    d["is_ham"]     = bool(d.get("callsign"))
    d["is_visitor"] = d.get("member_type","member") in ("visitor","mutual_aid")
    return d

def member_upsert_sql():
    cols  = (["id","member_id","callsign","radio_id","member_type",
               "visitor_agency","first_name","last_name",
               "role","phone","email","grid","lat","lon","notes"] +
             [f"cert_{c}" for c in CERT_COLS] +
             [f"equip_{e}" for e in EQUIP_COLS] +
             ["created","modified"])
    up    = [c for c in cols if c not in ("id","created")]
    ph    = ",".join("?"*len(cols))
    upd   = ",".join(f"{c}=excluded.{c}" for c in up)
    return f"INSERT INTO roster({','.join(cols)}) VALUES({ph}) ON CONFLICT(id) DO UPDATE SET {upd}"

def member_vals(m, mid, now):
    certs = m.get("certifications",{}) or {}
    equip = m.get("equipment",{}) or {}
    # Accept either the DB column key ("ics100") or the UI label ("ICS-100")
    cflag = lambda col: int(bool(certs.get(col,  certs.get(CERT_LABELS[col]))))
    eflag = lambda col: int(bool(equip.get(col, equip.get(EQUIP_LABELS[col]))))
    # roles may arrive as a list (checkboxes) or a single "role" string; store joined
    roles = m.get("roles")
    if isinstance(roles, list) and roles:
        role_val = "; ".join(str(r).strip() for r in roles if str(r).strip())
    else:
        role_val = m.get("role","Operator")
    # Generate member_id if not provided: ESV- + 4-digit sequence from id
    member_id = m.get("member_id","").strip()
    if not member_id:
        member_id = m.get("id", mid)
    mtype = m.get("member_type","member").strip() or "member"
    return [mid, member_id,
            (m.get("callsign","")).upper(),
            m.get("radio_id",""),
            mtype,
            m.get("visitor_agency",""),
            m.get("first_name",""), m.get("last_name",""),
            role_val, m.get("phone",""), m.get("email",""),
            m.get("grid",""), m.get("lat"), m.get("lon"), m.get("notes",""),
            *(cflag(c) for c in CERT_COLS),
            *(eflag(e) for e in EQUIP_COLS),
            m.get("created", now), now]

# ── QR + config helpers (agency-neutral, fully offline) ─────────────────────────
def qr_svg(data, size_px=220):
    """Render `data` as a scannable QR code and return it as an SVG string.
    Generated locally with ReportLab — no internet, no external service. This is
    what replaces the old (now-dead) chart.googleapis.com dependency."""
    from reportlab.graphics.barcode.qr import QrCodeWidget
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics import renderSVG
    q = QrCodeWidget(str(data), barLevel="M")
    x1, y1, x2, y2 = q.getBounds()
    w = (x2 - x1) or 1
    h = (y2 - y1) or 1
    d = Drawing(size_px, size_px)
    d.transform = [size_px / w, 0, 0, size_px / h, -x1 * size_px / w, -y1 * size_px / h]
    d.add(q)
    return renderSVG.drawToString(d)


def _org_short(c):
    """The deploying organization's short name from Setup (agency-neutral).
    Empty string if not configured — never a hardcoded agency."""
    try:
        row = c.execute("SELECT org_short FROM station_config WHERE id=1").fetchone()
        return (row["org_short"] or "") if row else ""
    except Exception:
        return ""


# ── HTTP Handler ──────────────────────────────────────────────────────────────

def _suggest_position(role):
    """Map roster role to suggested ICS position."""
    role = (role or "").lower()
    if "commander" in role or "director" in role: return "Incident Commander (IC)"
    if "safety" in role: return "Safety Officer (SOFR)"
    if "pio" in role or "public info" in role: return "Public Information Officer (PIO)"
    if "logistics" in role: return "Logistics Section Chief (LSC)"
    if "finance" in role: return "Finance/Admin Section Chief (FSC)"
    if "net control" in role or "net_control" in role: return "Net Control"
    if "operator" in role: return "Amateur Radio Operator"
    return ""

class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")

    def send_json(self, obj, code=200):
        body = json.dumps(obj, default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",len(body))
        self.cors(); self.end_headers(); self.wfile.write(body)

    def send_bytes(self, data, content_type, code=200, extra=None):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", len(data))
        if extra:
            for k, v in extra.items():
                self.send_header(k, v)
        self.cors(); self.end_headers()
        try:
            self.wfile.write(data)
        except Exception:
            pass

    def read_body(self):
        n = int(self.headers.get("Content-Length",0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        qs     = parse_qs(parsed.query)
        c      = get_conn()

        if path == "/api/fcc":
            call = qs.get("call",[""])[0]
            if not call: return self.send_json({"error":"Missing call"},400)
            r = fcc_lookup(call)
            return self.send_json(r) if r else self.send_json({"error":"Not found"},404)

        elif path == "/api/fcc/search":
            return self.send_json(fcc_search({
                "last_name":     qs.get("last_name",[""])[0],
                "first_name":    qs.get("first_name",[""])[0],
                "state":         qs.get("state",[""])[0],
                "city":          qs.get("city",[""])[0],
                "license_class": qs.get("license_class",[""])[0],
            }, qs.get("limit",["100"])[0]))

        elif path == "/api/fcc/status":
            if FCC_DB.exists():
                stat = FCC_DB.stat()
                age  = (time.time()-stat.st_mtime)/86400
                fc   = sqlite3.connect(str(FCC_DB))
                n    = fc.execute("SELECT COUNT(*) FROM en").fetchone()[0]
                fc.close()
                return self.send_json({"exists":True,"age_days":round(age,1),
                    "records":n,"path":str(FCC_DB),
                    "modified":datetime.fromtimestamp(stat.st_mtime).isoformat()})
            return self.send_json({"exists":False,"age_days":None,"records":0})

        elif path == "/api/config":
            row = c.execute("""SELECT callsign,personal_call,org_name,org_short,
                agency_name,agency_short,contact_email,contact_phone,
                city,state,county,lat,lon,ics_form_variant,
                logo_data,logo_mime,software_author,software_url,
                setup_complete,configured_at,active_modules,
                ps_system_name,ps_system_type,ps_id_label,ps_dispatch,
                ps_system2_name,ps_system2_type,ps_member_id_label,ps_member_lookup,
                grid,default_incident_name,wifi_ssid,wifi_pass,server_url,time_zone
                FROM station_config WHERE id=1""").fetchone()
            if row:
                keys = ['callsign','personal_call','org_name','org_short',
                        'agency_name','agency_short','contact_email','contact_phone',
                        'city','state','county','lat','lon','ics_form_variant',
                        'logo_data','logo_mime','software_author','software_url',
                        'setup_complete','configured_at','active_modules',
                        'ps_system_name','ps_system_type','ps_id_label','ps_dispatch',
                        'ps_system2_name','ps_system2_type','ps_member_id_label','ps_member_lookup',
                        'grid','default_incident_name','wifi_ssid','wifi_pass','server_url','time_zone']
                return self.send_json(dict(zip(keys, row)))
            return self.send_json({})

        elif path == "/api/position":
            return self.send_json(get_station_position())

        elif path == "/api/nets":
            sc = qs.get("starcom",[None])[0]
            sql = ("SELECT id,name,type,starcom,drill,active,created,closed,freq,mode,ncs,"
                   "(SELECT COUNT(*) FROM net_entries e WHERE e.net_id=n.id) entry_count"
                   " FROM nets n")
            if sc is not None:
                sql += " WHERE starcom=?"; params = [1 if sc.lower()=="true" else 0]
            else:
                params = []
            sql += " ORDER BY created DESC"
            return self.send_json(rows_to_list(c.execute(sql,params).fetchall()))

        elif path.startswith("/api/nets/"):
            parts  = path.split("/"); net_id = parts[3] if len(parts)>3 else ""
            sub    = "/".join(parts[4:]) if len(parts)>4 else ""
            row    = c.execute("SELECT * FROM nets WHERE id=?",(net_id,)).fetchone()
            if not row: return self.send_json({"error":"Not found"},404)
            if sub in ("",""):
                net = dict(row)
                net["roster_chips"] = jload(net.get("roster_chips"),[])
                net["entries"] = rows_to_list(c.execute(
                    "SELECT * FROM net_entries WHERE net_id=? ORDER BY timestamp",(net_id,)).fetchall())
                net["traffic"] = rows_to_list(c.execute(
                    "SELECT * FROM net_traffic WHERE net_id=? ORDER BY timestamp",(net_id,)).fetchall())
                return self.send_json(net)
            elif sub == "entries":
                return self.send_json(rows_to_list(c.execute(
                    "SELECT * FROM net_entries WHERE net_id=? ORDER BY timestamp",(net_id,)).fetchall()))
            elif sub == "traffic":
                return self.send_json(rows_to_list(c.execute(
                    "SELECT * FROM net_traffic WHERE net_id=? ORDER BY timestamp",(net_id,)).fetchall()))
            elif sub == "roster_chips":
                return self.send_json(jload(row["roster_chips"],[]))
            return self.send_json({"error":"Not found"},404)

        elif path == "/api/roster":
            members = [member_to_dict(r) for r in
                       c.execute("SELECT * FROM roster ORDER BY callsign").fetchall()]
            acts = rows_to_list(c.execute(
                "SELECT * FROM activations ORDER BY checked_in DESC").fetchall())
            return self.send_json({"members":members,"activations":acts})

        elif path == "/api/roster/members":
            return self.send_json([member_to_dict(r) for r in
                c.execute("SELECT * FROM roster ORDER BY callsign").fetchall()])

        elif path == "/api/roster/activations":
            return self.send_json(rows_to_list(c.execute(
                "SELECT * FROM activations ORDER BY checked_in DESC").fetchall()))

        elif path == "/api/resources":
            return self.send_json(rows_to_list(
                c.execute("SELECT * FROM resources ORDER BY name").fetchall()))

        elif path == "/api/mapstate":
            row = c.execute("SELECT * FROM map_state WHERE id=1").fetchone()
            return self.send_json({
                "shapes":  jload(row["shapes"],[]) if row else [],
                "markers": jload(row["markers"],[]) if row else []})

        elif path == "/api/resmap":
            row = c.execute("SELECT * FROM resmap_state WHERE id=1").fetchone()
            return self.send_json({"markers":jload(row["markers"],[]) if row else []})


        # ── Barcode / QR Check-In Lookup ────────────────────────────────────
        # GET /api/barcode_lookup?code=XXXX
        # Looks up a roster member by barcode_id, member_id, callsign, or radio_id
        # Returns pre-filled check-in data so the scan can auto-complete the form
        elif path == "/api/barcode_lookup":
            code = qs.get("code",[""])[0].strip().upper()
            if not code:
                return self.send_json({"found":False,"error":"No code provided"},400)

            # Try barcode_id first, then member_id, callsign, radio_id
            row = None
            for col in ["barcode_id","member_id","callsign","radio_id"]:
                row = c.execute(
                    f"SELECT * FROM roster WHERE UPPER({col})=? AND {col}!='' LIMIT 1",
                    (code,)
                ).fetchone()
                if row:
                    break

            if not row:
                # Not on the roster — if the scanned code is a callsign, fall back to
                # the FCC database so a scanned ham still auto-fills a name.
                if re.fullmatch(r"[A-Z0-9]{1,3}[0-9][A-Z]{1,3}", code):
                    fcc = fcc_lookup(code)
                    if fcc and fcc.get("name"):
                        return self.send_json({
                            "found":       True,
                            "source":      "fcc",
                            "on_roster":   False,
                            "member_id":   "",
                            "name":        fcc["name"],
                            "callsign":    code,
                            "radio_id":    "",
                            "agency":      "",
                            "role":        "",
                            "member_type": "visitor",
                            "license_class": fcc.get("operator_class",""),
                            "suggested_position": "Amateur Radio Operator",
                        })
                return self.send_json({"found":False,"error":f"No roster member or FCC record for code: {code}"})

            r = dict(row)
            # Build pre-fill data for the check-in form
            return self.send_json({
                "found":        True,
                "member_id":    r.get("member_id",""),
                "barcode_id":   r.get("barcode_id",""),
                "name":         f"{r.get('first_name','')} {r.get('last_name','')}".strip(),
                "callsign":     r.get("callsign",""),
                "radio_id":     r.get("radio_id",""),
                "agency":       r.get("visitor_agency","") or _org_short(c),
                "role":         r.get("role",""),
                "member_type":  r.get("member_type",""),
                # Suggest ICS position based on role
                "suggested_position": _suggest_position(r.get("role","")),
            })

        # ── QR code image (offline, ReportLab-generated SVG) ────────────────
        # GET /api/qr?data=XXXX  → scannable QR as image/svg+xml. Replaces the
        # dead chart.googleapis.com dependency; works with no internet.
        elif path == "/api/qr":
            data = qs.get("data",[qs.get("code",[""])[0]])[0]
            if not data:
                return self.send_json({"error":"missing data"},400)
            try:
                svg = qr_svg(data).encode("utf-8")
            except Exception as e:
                return self.send_json({"error":f"qr failed: {e}"},500)
            return self.send_bytes(svg, "image/svg+xml; charset=utf-8",
                                   extra={"Cache-Control":"no-store"})

        # ── Member photo (served separately so list JSON stays small) ───────
        elif path == "/api/roster/photo":
            mid = qs.get("id",[""])[0]
            if not mid:
                return self.send_json({"error":"missing id"},400)
            row = c.execute("SELECT photo_data,photo_mime FROM roster WHERE id=?",
                            (mid,)).fetchone()
            if not row or not row["photo_data"]:
                return self.send_json({"error":"no photo"},404)
            raw  = row["photo_data"]
            mime = row["photo_mime"] or "image/png"
            if isinstance(raw,str) and raw.startswith("data:"):
                head,_,raw = raw.partition(",")
                if ":" in head and ";" in head:
                    mime = head[head.find(":")+1:head.find(";")] or mime
            import base64 as _b64
            try:
                img = _b64.b64decode(raw)
            except Exception:
                return self.send_json({"error":"bad image"},500)
            return self.send_bytes(img, mime, extra={"Cache-Control":"no-store"})

        # ── Printable member ID cards (PDF, generated on demand) ────────────
        # GET /api/id_cards.pdf           → all eligible members
        # GET /api/id_cards.pdf?id=<mid>  → one member's card
        elif path == "/api/id_cards.pdf":
            mid = qs.get("id",[""])[0] or None
            backs = qs.get("backs",["1"])[0] not in ("0","false","no")
            import tempfile
            try:
                import gen_id_cards as _gen
            except Exception as e:
                return self.send_json({"error":f"card module unavailable: {e}"},500)
            out = os.path.join(tempfile.gettempdir(), "fc_member_id_cards.pdf")
            try:
                _gen.generate_from_db(out_path=out, only_id=mid, backs=backs)
                with open(out,"rb") as f:
                    data = f.read()
            except ValueError as e:
                return self.send_json({"error":str(e)},404)
            except Exception as e:
                return self.send_json({"error":f"card generation failed: {e}"},500)
            return self.send_bytes(data, "application/pdf",
                extra={"Content-Disposition":"inline; filename=member_id_cards.pdf"})

        elif path == "/api/hospitals":
            county = qs.get("county",[None])[0]
            state  = qs.get("state",[None])[0]
            srch   = qs.get("q",[""])[0].lower()
            sql    = "SELECT * FROM hospitals WHERE active=1"; params=[]
            if county: sql+=" AND UPPER(county) LIKE ?"; params.append(f"%{county.upper()}%")
            if state:  sql+=" AND UPPER(state)=?"; params.append(state.upper())
            rows = rows_to_list(c.execute(sql+" ORDER BY state,county,name",params).fetchall())
            if srch: rows=[r for r in rows if srch in json.dumps(r).lower()]
            return self.send_json(rows)

        elif path == "/api/facilities":
            rows = rows_to_list(c.execute("SELECT * FROM facilities ORDER BY name").fetchall())
            return self.send_json(rows)

        elif path == "/api/resource_types":
            cat    = qs.get("category",[None])[0]
            kind   = qs.get("kind",[None])[0]
            srch   = qs.get("q",[""])[0].lower()
            sql    = "SELECT * FROM resource_types WHERE active=1"; params=[]
            if cat:  sql+=" AND UPPER(category)=?"; params.append(cat.upper())
            if kind: sql+=" AND UPPER(kind) LIKE ?"; params.append(f"%{kind.upper()}%")
            rows = rows_to_list(c.execute(sql+" ORDER BY category,kind,type_level",params).fetchall())
            if srch: rows=[r for r in rows if srch in json.dumps(r).lower()]
            return self.send_json(rows)

        elif path == "/api/repeaters":
            band  = qs.get("band",[None])[0]
            state = qs.get("state",[None])[0]
            srch  = qs.get("q",[""])[0].lower()
            sql   = "SELECT * FROM repeaters WHERE 1=1"; params=[]
            if band:  sql+=" AND mode LIKE ?"; params.append(f"%{band}%")
            if state: sql+=" AND UPPER(state)=?"; params.append(state.upper())
            reps = rows_to_list(c.execute(sql+" ORDER BY state,city",params).fetchall())
            # Add page-friendly aliases so the web UI reads ARES/RACES/SKYWARN and Use.
            for r in reps:
                r["use"]     = r.get("use_type","Open")
                r["ARES"]    = "Yes" if r.get("ares") else ""
                r["RACES"]   = "Yes" if r.get("races") else ""
                r["SKYWARN"] = "Yes" if r.get("skywarn") else ""
                r["last_updated"] = r.get("updated","")
            if srch: reps=[r for r in reps if srch in json.dumps(r).lower()]
            return self.send_json(reps)

        elif path == "/api/dms":
            row = c.execute("SELECT * FROM dms_state WHERE id=1").fetchone()
            armed = jload(dict(row).get("armed_nets") if row else None, {})
            if not isinstance(armed, dict): armed = {}
            nets = {}
            for n in c.execute("SELECT id, name, net_opened FROM nets WHERE net_closed IS NULL OR net_closed=''").fetchall():
                nid = str(n["id"]); a = armed.get(nid, {})
                nets[nid] = {
                    "name": n["name"],
                    "threshold_minutes": a.get("threshold_min", 30),
                    "state": a.get("state", "disarmed"),
                    "armed_at": a.get("armed_at"),
                    "triggered_at": a.get("triggered_at"),
                    "last_activity": _net_last_activity(c, n["id"]) or n["net_opened"],
                }
            return self.send_json({"nets": nets})

        elif path == "/api/forms":
            ft = qs.get("type",["all"])[0]
            if ft=="all":
                rows=c.execute("SELECT id,form_type,incident_id,summary,created,updated FROM forms ORDER BY created DESC").fetchall()
            else:
                rows=c.execute("SELECT id,form_type,incident_id,summary,created,updated FROM forms WHERE form_type=? ORDER BY created DESC",(ft,)).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path.startswith("/api/forms/"):
            fid = path.split("/api/forms/")[1]
            row = c.execute("SELECT * FROM forms WHERE id=?",(fid,)).fetchone()
            if row:
                d=dict(row); d.update(jload(d.get("data"),{}))
                return self.send_json(d)
            return self.send_json({"error":"Not found"},404)

        elif path == "/api/preflight":
            return self.send_json(self._preflight_check())

        elif path == "/wan/status" or path == "/api/wan/status":
            # Serve WAN status written by wan_monitor.py
            wan_file = Path("/opt/fieldcommand/data/wan_status.json")
            try:
                if wan_file.exists():
                    return self.send_json(json.loads(wan_file.read_text()))
                return self.send_json({"active_source": "unknown",
                    "error": "wan_monitor has not written status yet"})
            except Exception as e:
                return self.send_json({"active_source": "unknown",
                    "error": str(e)}, 500)

        elif path == "/amprgate/status" or path == "/api/amprgate/status":
            # Serve AMPRNet gateway status written by amprgate_poll.py
            ampr_file = Path("/opt/fieldcommand/data/amprgate_status.json")
            try:
                if ampr_file.exists():
                    return self.send_json(json.loads(ampr_file.read_text()))
                return self.send_json({"tunnel": "unknown",
                    "error": "amprgate_poll has not written status yet"})
            except Exception as e:
                return self.send_json({"tunnel": "unknown",
                    "error": str(e)}, 500)

        elif path == "/api/status":
            return self.send_json({"service":"fcc-lookup","version":"2.0.0",
                "utc":utcnow(),"fcc_db":FCC_DB.exists(),"db":str(db.DB_PATH)})

        else:
            self.send_json({"error":"Not found"},404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        body   = self.read_body()
        c      = get_conn()
        now    = utcnow()

        if path == "/api/resource_types":
            rid = body.get("id")
            fields = ['kind','type_level','category','mission_area','description',
                      'min_personnel','capabilities','metric_notes','custom','active']
            if rid:
                sets = [f"{f}=?" for f in fields if f in body]
                vals = [body[f] for f in fields if f in body] + [rid]
                if sets:
                    c.execute(f"UPDATE resource_types SET {','.join(sets)} WHERE id=?", vals)
                    c.commit()
                return self.send_json({"ok":True,"id":rid})
            else:
                cols = [f for f in fields if f in body]
                vals = [body[f] for f in cols]
                c.execute(f"INSERT INTO resource_types ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", vals)
                c.commit()
                new_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
                return self.send_json({"ok":True,"id":new_id})

        # ── CMS Hospital Database Import ────────────────────────────────────
        # Fetches from CMS Provider Data Catalog — public, no account required.
        # Returns name/address/phone/type. Does NOT include lat/lon or trauma level.
        if path == "/api/hospitals/cms_search":
            import urllib.request as _ureq
            state  = body.get("state","").upper().strip()
            county = body.get("county","").upper().strip()
            q      = body.get("q","").lower().strip()
            types  = body.get("types",["Acute Care Hospitals","Critical Access Hospitals"])
            limit  = int(body.get("limit",200))
            if not state:
                return self.send_json({"error":"state is required"},400)
            try:
                url = (
                    "https://data.cms.gov/provider-data/api/1/datastore/query/"
                    f"xubh-q36u/0?filter%5BState%5D={state}&limit={min(limit,500)}&offset=0"
                )
                req = _ureq.Request(url,headers={
                    "Accept":"application/json",
                    "User-Agent":"FieldCommandIMS/1.0"
                })
                with _ureq.urlopen(req,timeout=15) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                results = data.get("results",[])
                hospitals = []
                for r in results:
                    htype = r.get("Hospital Type","")
                    if types and not any(t.lower() in htype.lower() for t in types):
                        continue
                    if r.get("Emergency Services","") == "No":
                        continue
                    if county and county not in r.get("County/Parish","").upper():
                        continue
                    if q and q not in json.dumps(r).lower():
                        continue
                    hospitals.append({
                        "name":       r.get("Facility Name","").title(),
                        "address":    r.get("Address","").title(),
                        "city":       r.get("City/Town","").title(),
                        "state":      r.get("State",""),
                        "county":     r.get("County/Parish","").title(),
                        "phone":      r.get("Telephone Number",""),
                        "zip":        r.get("ZIP Code",""),
                        "type":       htype,
                        "cms_rating": r.get("Hospital overall rating",""),
                        "lat":None,"lon":None,
                        "trauma_level":"","burn_center":0,"helipad":0,
                        "source":"CMS Provider Data"
                    })
                return self.send_json({
                    "hospitals":hospitals[:limit],
                    "count":len(hospitals),
                    "note":(
                        "CMS data includes name/address/phone/type. "
                        "Lat/lon and trauma level are NOT in CMS — add manually after import, "
                        "or use a pre-geocoded CSV from your state EMS office."
                    ),
                    "source":"data.cms.gov/provider-data"
                })
            except Exception as e:
                return self.send_json({"error":str(e),"hint":"CMS import requires WAN."},503)

        if path == "/api/hospitals":
            fields = ['name','address','city','state','county','phone','phone2','fax',
                      'lat','lon','trauma_level','burn_center','helipad','icu',
                      'peds_trauma','stroke_center','cardiac_center','travel_time_min',
                      'notes','active']
            hid = body.get("id")
            if hid:
                # Update existing
                sets = [f"{f}=?" for f in fields if f in body]
                vals = [body[f] for f in fields if f in body] + [hid]
                if sets:
                    c.execute(f"UPDATE hospitals SET {','.join(sets)} WHERE id=?", vals)
                    c.commit()
                return self.send_json({"ok":True,"id":hid})
            else:
                # Insert new
                cols = [f for f in fields if f in body]
                vals = [body[f] for f in cols]
                c.execute(f"INSERT INTO hospitals ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", vals)
                c.commit()
                new_id = c.execute("SELECT last_insert_rowid()").fetchone()[0]
                return self.send_json({"ok":True,"id":new_id})

        if path == "/api/facilities":
            # Upsert a facility (id is a client-generated string key).
            FAC_COLS = ['name','type','status','address','city','state_zip','lat','lon',
                        'phone','phone2','freq','freq2','tone','capacity','contact',
                        'callsign','generator','ada','notes']
            fid = str(body.get("id") or f"fac-{int(time.time()*1000)}")
            if c.execute("SELECT 1 FROM facilities WHERE id=?", (fid,)).fetchone():
                present = [k for k in FAC_COLS if k in body]
                sets = ",".join(f"{k}=?" for k in present) + (", " if present else "") + "updated=?"
                vals = [body[k] for k in present] + [now, fid]
                c.execute(f"UPDATE facilities SET {sets} WHERE id=?", vals)
            else:
                cols = ["id"] + FAC_COLS + ["updated"]
                vals = [fid] + [body.get(k) for k in FAC_COLS] + [now]
                c.execute(f"INSERT INTO facilities ({','.join(cols)}) VALUES ({','.join(['?']*len(cols))})", vals)
            c.commit()
            return self.send_json({"ok":True,"id":fid})

        if path == "/api/config":
            fields = ['callsign','personal_call','org_name','org_short',
                      'agency_name','agency_short','contact_email','contact_phone',
                      'city','state','county','lat','lon','ics_form_variant',
                      'logo_data','logo_mime','setup_complete','active_modules',
                      'ps_system_name','ps_system_type','ps_id_label','ps_dispatch',
                      'ps_system2_name','ps_system2_type','ps_member_id_label','ps_member_lookup',
                      'grid','default_incident_name','wifi_ssid','wifi_pass','server_url','time_zone']
            sets = [f"{f}=?" for f in fields if f in body]
            vals = [body[f] for f in fields if f in body]
            if sets:
                vals.append(now)
                vals.append(1)
                c.execute(
                    f"UPDATE station_config SET {','.join(sets)},configured_at=?,setup_complete=? WHERE id=1",
                    vals)
                c.commit()
            return self.send_json({"ok": True})

        if path == "/api/nets":
            net_id = body.get("id") or f"net-{int(time.time())}"
            sc = 1 if (body.get("starcom") or net_id.startswith("sc-")) else 0
            c.execute("""
                INSERT INTO nets(id,name,type,starcom,drill,active,freq,mode,ncs,created,net_opened,roster_chips)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(id) DO UPDATE SET name=excluded.name,type=excluded.type,
                drill=excluded.drill,active=excluded.active,freq=excluded.freq,mode=excluded.mode,
                ncs=excluded.ncs,roster_chips=excluded.roster_chips
            """,(net_id,body.get("name",f"Net {net_id}"),
                 body.get("type","SC Dispatch" if sc else "Amateur"),sc,
                 1 if body.get("drill") else 0,1 if body.get("active",True) else 0,
                 body.get("freq",""),body.get("mode",""),
                 body.get("ncs") or body.get("net_control",""),now,
                 body.get("net_opened") or now,
                 jdump(body.get("roster_chips",[]))))
            c.commit()
            return self.send_json({"ok":True,"id":net_id})

        elif path.startswith("/api/nets/"):
            parts  = path.split("/"); net_id=parts[3] if len(parts)>3 else ""
            sub    = parts[4] if len(parts)>4 else ""

            if sub == "entry":
                eid = body.get("id") or f"e-{int(time.time()*1000)}"
                # Look up EMA ID from roster by callsign (ham net) or radio_id (Starcom)
                ema_id = ""
                callsign = body.get("callsign","").strip().upper()
                radio_id = body.get("radio_id","").strip()
                if callsign:
                    row = c.execute(
                        "SELECT member_id FROM roster WHERE UPPER(callsign)=? AND member_type='member'",
                        (callsign,)).fetchone()
                    if row: ema_id = row[0]
                if not ema_id and radio_id:
                    row = c.execute(
                        "SELECT member_id FROM roster WHERE radio_id=? AND member_type='member'",
                        (radio_id,)).fetchone()
                    if row: ema_id = row[0]
                c.execute("""INSERT OR REPLACE INTO net_entries
                    (id,net_id,callsign,member_id,radio_id,visitor_agency,
                     name,city,state,precedence,traffic,remarks,
                     walk_in,visitor,timestamp,ema_id,ics_position)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (eid,net_id,
                     body.get("callsign",""),
                     body.get("member_id",""),
                     radio_id,
                     body.get("visitor_agency",""),
                     body.get("name",""),
                     body.get("city",""),body.get("state",""),
                     body.get("precedence","ROUTINE"),
                     body.get("traffic",""),body.get("remarks",""),
                     1 if body.get("walk_in") else 0,
                     1 if body.get("visitor") else 0,
                     now,ema_id,body.get("ics_position","")))
                c.execute("UPDATE dms_state SET last_activity=? WHERE id=1",(now,))
                c.commit()

                # ── ICS-211 sync ─────────────────────────────────────────────
                # When check-in is linked to an incident, write to ICS-211 record
                incident_id = body.get("incident_id","")
                if incident_id:
                    # Load existing ICS-211 data for this incident or start fresh
                    f211_id = f"ics211-{incident_id}"
                    existing = c.execute(
                        "SELECT data FROM ics_forms WHERE id=?", (f211_id,)).fetchone()
                    if existing:
                        import json as _json
                        try:
                            f211_data = _json.loads(existing[0])
                        except Exception:
                            f211_data = {}
                    else:
                        f211_data = {"incident_id": incident_id, "form_type": "ics211"}
                    # Find next available row index
                    idx = 0
                    while f211_data.get(f"ci211_name_{idx}") or f211_data.get(f"ci211_id_{idx}"):
                        idx += 1
                    # Write this check-in to the next available row
                    f211_data[f"ci211_name_{idx}"]   = body.get("name","")
                    f211_data[f"ci211_id_{idx}"]     = body.get("callsign","") or radio_id
                    f211_data[f"ci211_agency_{idx}"] = body.get("visitor_agency","")
                    f211_data[f"ci211_pos_{idx}"]    = body.get("ics_position","")
                    f211_data[f"ci211_rtype_{idx}"]  = "Personnel"
                    f211_data[f"ci211_in_{idx}"]     = now[:16]
                    f211_data[f"ci211_equip_{idx}"]  = body.get("remarks","")
                    f211_data["incident_id"]          = incident_id
                    f211_data["form_type"]            = "ics211"
                    import json as _json2
                    c.execute("""INSERT OR REPLACE INTO ics_forms
                        (id,incident_id,form_type,period,summary,data,created,updated)
                        VALUES(?,?,?,?,?,?,COALESCE(
                            (SELECT created FROM ics_forms WHERE id=?),?),?)""",
                        (f211_id, incident_id, "ics211", 1,
                         f"Check-In List — {body.get('name','')}",
                         _json2.dumps(f211_data), f211_id, now, now))
                    c.commit()

                return self.send_json({"ok":True,"entry":{**body,"id":eid,"timestamp":now,"ema_id":ema_id}})

            elif sub == "traffic":
                tid = body.get("id") or f"t-{int(time.time()*1000)}"
                c.execute("""INSERT OR REPLACE INTO net_traffic
                    (id,net_id,msg_number,from_call,to_call,precedence,handling,text,timestamp)
                    VALUES(?,?,?,?,?,?,?,?,?)""",
                    (tid,net_id,body.get("msg_number",""),body.get("from_call",""),
                     body.get("to_call",""),body.get("precedence","ROUTINE"),
                     body.get("handling",""),body.get("text",""),now))
                c.commit()
                return self.send_json({"ok":True,"msg":{**body,"id":tid,"timestamp":now}})

            elif sub == "update":
                updates={k:body[k] for k in("name","type","drill","active","freq","ncs") if k in body}
                if "roster_chips" in body: updates["roster_chips"]=jdump(body["roster_chips"])
                if updates:
                    sets=", ".join(f"{k}=?" for k in updates)
                    c.execute(f"UPDATE nets SET {sets} WHERE id=?",(*updates.values(),net_id))
                    c.commit()
                return self.send_json({"ok":True})

            elif sub == "checkout":
                # Check out a single entry before net closes
                entry_id = body.get("entry_id","")
                if not entry_id:
                    return self.send_json({"error":"entry_id required"},400)
                c.execute("UPDATE net_entries SET checkout_time=? WHERE id=? AND net_id=?",
                          (now,entry_id,net_id))
                c.commit()

                # ── ICS-211 checkout sync ─────────────────────────────────────
                # Update checkout time in ICS-211 record if linked to incident
                entry_row = c.execute(
                    "SELECT callsign,name,incident_id FROM net_entries WHERE id=?",
                    (entry_id,)).fetchone()
                if entry_row and entry_row[2]:  # has incident_id
                    incident_id = entry_row[2]
                    f211_id = f"ics211-{incident_id}"
                    existing = c.execute(
                        "SELECT data FROM ics_forms WHERE id=?", (f211_id,)).fetchone()
                    if existing:
                        import json as _json3
                        try:
                            f211_data = _json3.loads(existing[0])
                            callsign = entry_row[0]
                            name = entry_row[1]
                            # Find matching row by callsign or name
                            for i in range(100):
                                rid = f211_data.get(f"ci211_id_{i}","")
                                rname = f211_data.get(f"ci211_name_{i}","")
                                if (callsign and rid == callsign) or (name and rname == name):
                                    f211_data[f"ci211_out_{i}"] = now[:16]
                                    break
                            c.execute(
                                "UPDATE ics_forms SET data=?,updated=? WHERE id=?",
                                (_json3.dumps(f211_data), now, f211_id))
                            c.commit()
                        except Exception:
                            pass

                return self.send_json({"ok":True,"checkout_time":now})

            elif sub == "open":
                # Explicitly open net (record net_opened timestamp)
                c.execute("UPDATE nets SET net_opened=?,active=1 WHERE id=?",(now,net_id))
                c.commit()
                return self.send_json({"ok":True,"net_opened":now})

            elif sub == "close":
                # Auto-checkout any entries that haven't checked out
                c.execute("""UPDATE net_entries SET checkout_time=?
                             WHERE net_id=? AND checkout_time IS NULL""",(now,net_id))
                c.execute("UPDATE nets SET active=0,net_closed=?,closed=? WHERE id=?",
                          (now,now,net_id))
                c.commit()
                return self.send_json({"ok":True,"net_closed":now})

        elif path == "/api/roster/members":
            mid = body.get("id") or f"m-{int(time.time()*1000)}"
            c.execute(member_upsert_sql(), member_vals(body,mid,now))
            c.commit()
            return self.send_json({"ok":True,"member":member_to_dict(
                c.execute("SELECT * FROM roster WHERE id=?",(mid,)).fetchone())})

        # ── Member photo (stored separately from the member upsert, so an
        #    ordinary edit can never wipe a photo). POST {id, photo_data, photo_mime}.
        elif path == "/api/roster/photo":
            mid = body.get("id","")
            if not mid:
                return self.send_json({"error":"missing id"},400)
            if not c.execute("SELECT 1 FROM roster WHERE id=?",(mid,)).fetchone():
                return self.send_json({"error":"no such member"},404)
            raw  = body.get("photo_data","") or ""
            mime = body.get("photo_mime","") or "image/jpeg"
            # Accept a data: URL and split out the mime + bare base64 for storage.
            if raw.startswith("data:"):
                head,_,b64 = raw.partition(",")
                if ":" in head and ";" in head:
                    mime = head[head.find(":")+1:head.find(";")] or mime
                raw = b64
            c.execute("UPDATE roster SET photo_data=?,photo_mime=?,modified=? WHERE id=?",
                      (raw, mime, now, mid))
            c.commit()
            return self.send_json({"ok":True,"has_photo":bool(raw)})

        elif path == "/api/roster/activations":
            aid = body.get("id") or f"a-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO activations
                (id,callsign,net_id,incident_id,role,location,checked_in,checked_out,notes)
                VALUES(?,?,?,?,?,?,?,?,?)""",
                (aid,body.get("callsign",""),body.get("net_id",""),
                 body.get("incident_id",""),body.get("role",""),
                 body.get("location",""),body.get("checked_in",now),
                 body.get("checked_out"),body.get("notes","")))
            c.commit()
            return self.send_json({"ok":True,"activation":{**body,"id":aid}})

        elif path == "/api/roster/promote":
            # Promote a walk-in / visitor to the roster
            # Body: entry data from a net_entry (callsign/name/radio_id etc.)
            mid = body.get("id") or f"m-{int(time.time()*1000)}"
            # Assign visitor member_id if no ESV number
            member_id = body.get("member_id","").strip()
            mtype = body.get("member_type","member")
            if not member_id:
                if mtype in ("visitor","mutual_aid"):
                    member_id = f"VIS-{int(time.time()*1000) % 100000:05d}"
                else:
                    member_id = f"ESV-{int(time.time()*1000) % 10000:04d}"
            c.execute(member_upsert_sql(), member_vals({
                **body,
                "id": mid,
                "member_id": member_id,
                "member_type": mtype,
            }, mid, now))
            # Mark the net_entry as promoted
            entry_id = body.get("entry_id","")
            if entry_id:
                c.execute("UPDATE net_entries SET promoted=1 WHERE id=?", (entry_id,))
            c.commit()
            return self.send_json({"ok": True, "member_id": member_id,
                                   "roster_id": mid})

        elif path == "/api/roster/import":
            added=0
            for m in body.get("members",[]):
                mid=m.get("id") or f"m-{int(time.time()*1000)+added}"
                c.execute(member_upsert_sql(), member_vals(m,mid,now))
                added+=1
            c.commit()
            return self.send_json({"ok":True,"added":added})

        elif path == "/api/resources":
            rid = body.get("id") or f"r-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO resources
                (id,name,type,capability,status,assignment,contact,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (rid,body.get("name",""),body.get("type",""),body.get("capability",""),
                 body.get("status","Available"),body.get("assignment",""),
                 body.get("contact",""),body.get("notes",""),body.get("created",now),now))
            c.commit()
            return self.send_json({"ok":True,"resource":{**body,"id":rid,"updated":now}})

        elif path == "/api/mapstate":
            c.execute("UPDATE map_state SET shapes=?,markers=?,updated=? WHERE id=1",
                      (jdump(body.get("shapes",[])),jdump(body.get("markers",[])),now))
            c.commit(); return self.send_json({"ok":True})

        elif path == "/api/resmap":
            c.execute("UPDATE resmap_state SET markers=?,updated=? WHERE id=1",
                      (jdump(body.get("markers",[])),now))
            c.commit(); return self.send_json({"ok":True})

        elif path == "/api/forms":
            fid = body.get("id") or f"f-{int(time.time()*1000)}"
            body["id"]=fid; body.setdefault("created",now)
            c.execute("""INSERT OR REPLACE INTO forms
                (id,form_type,incident_id,summary,data,created,updated)
                VALUES(?,?,?,?,?,?,?)""",
                (fid,body.get("form_type","unknown"),body.get("incident_id",""),
                 body.get("summary",""),jdump(body),body.get("created",now),now))
            c.commit(); return self.send_json({"ok":True,"id":fid})

        elif path == "/api/dms/arm":
            nid = str(body.get("net_id","")).strip()
            if not nid: return self.send_json({"error":"net_id required"},400)
            row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
            armed = jload(row["armed_nets"] if row else None, {})
            if not isinstance(armed, dict): armed = {}
            try: thr = int(body.get("threshold", body.get("threshold_min", 30)) or 30)
            except (ValueError, TypeError): thr = 30
            armed[nid] = {"threshold_min": thr, "armed_at": now, "state": "armed", "triggered_at": None}
            c.execute("UPDATE dms_state SET state='armed', armed_nets=?, last_activity=? WHERE id=1", (jdump(armed), now))
            c.commit(); return self.send_json({"ok":True})

        elif path == "/api/dms/reset":
            nid = str(body.get("net_id","")).strip()
            row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
            armed = jload(row["armed_nets"] if row else None, {})
            if isinstance(armed, dict) and nid in armed:
                armed[nid]["state"] = "armed"; armed[nid]["triggered_at"] = None
                c.execute("UPDATE dms_state SET armed_nets=? WHERE id=1", (jdump(armed),)); c.commit()
            return self.send_json({"ok":True})

        elif path == "/api/dms/disarm":
            nid = str(body.get("net_id","")).strip()
            row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
            armed = jload(row["armed_nets"] if row else None, {})
            if isinstance(armed, dict) and nid in armed:
                del armed[nid]
                c.execute("UPDATE dms_state SET armed_nets=?, state=? WHERE id=1", (jdump(armed), "armed" if armed else "disarmed")); c.commit()
            return self.send_json({"ok":True})

        else:
            self.send_json({"error":"Not found"},404)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        c      = get_conn()

        if path.startswith("/api/hospitals/"):
            hid = path.split("/api/hospitals/")[1]
            c.execute("UPDATE hospitals SET active=0 WHERE id=?", (hid,))
            c.commit()
            return self.send_json({"ok":True})
        elif path.startswith("/api/facilities/"):
            c.execute("DELETE FROM facilities WHERE id=?", (path.split("/api/facilities/")[1],))
            c.commit()
            return self.send_json({"ok":True})
        elif path.startswith("/api/nets/"):
            c.execute("DELETE FROM nets WHERE id=?",(path.split("/api/nets/")[1],))
        elif path.startswith("/api/resources/"):
            c.execute("DELETE FROM resources WHERE id=?",(path.split("/api/resources/")[1],))
        elif path.startswith("/api/roster/members/"):
            c.execute("DELETE FROM roster WHERE id=?",(path.split("/api/roster/members/")[1],))
        elif path.startswith("/api/roster/activations/"):
            c.execute("DELETE FROM activations WHERE id=?",(path.split("/api/roster/activations/")[1],))
        elif path.startswith("/api/roster/photo/"):
            c.execute("UPDATE roster SET photo_data='',photo_mime='' WHERE id=?",
                      (path.split("/api/roster/photo/")[1],))
        elif path.startswith("/api/forms/"):
            c.execute("DELETE FROM forms WHERE id=?",(path.split("/api/forms/")[1],))
        else:
            return self.send_json({"error":"Not found"},404)
        c.commit()
        return self.send_json({"ok":True})

    def _preflight_check(self):
        results={}; c=get_conn(); now=utcnow()
        def svc(n):
            try:
                r=subprocess.run(["systemctl","is-active",n],capture_output=True,text=True,timeout=3)
                return r.stdout.strip()=="active"
            except: return False
        for n,lbl in [("nginx","Web Server"),("direwolf","Direwolf TNC"),
                      ("pat","Pat Winlink"),("fcc-lookup","FCC Lookup API"),
                      ("kiwix","Kiwix Library"),("gpsd","GPS Daemon"),
                      ("chrony","Time Sync"),("deadmans","Dead Man's Switch")]:
            results[n]={"ok":svc(n),"label":lbl}
        fcc_ok={"ok":False,"label":"FCC Database","detail":"Not found"}
        if FCC_DB.exists():
            try:
                fc=sqlite3.connect(str(FCC_DB))
                n=fc.execute("SELECT COUNT(*) FROM en").fetchone()[0]; fc.close()
                age=(time.time()-FCC_DB.stat().st_mtime)/86400
                fcc_ok={"ok":age<14,"label":"FCC Database","detail":f"{n:,} records, {age:.1f}d"}
            except Exception as e: fcc_ok["detail"]=str(e)
        results["fcc_db"]=fcc_ok
        gps_ok=False
        try:
            s=socket.socket(); s.settimeout(2); s.connect(("127.0.0.1",2947))
            s.send(b'?WATCH={"enable":true,"json":true}\n')
            d=s.recv(1024).decode(errors="ignore"); s.close()
            gps_ok='"class":"VERSION"' in d or '"class":"SKY"' in d
        except: pass
        results["gps_fix"]={"ok":gps_ok,"label":"GPS Fix"}
        ap_ok=False
        try:
            r=subprocess.run(["nmcli","-t","-f","NAME,TYPE,DEVICE","connection","show","--active"],
                             capture_output=True,text=True,timeout=3)
            ap_ok="wifi" in r.stdout.lower() and "EMCOMM" in r.stdout
        except: pass
        results["wifi_ap"]={"ok":ap_ok,"label":"EMCOMM-NET WiFi AP"}
        n_reps=c.execute("SELECT COUNT(*) FROM repeaters").fetchone()[0]
        n_reps_geo=c.execute("SELECT COUNT(*) FROM repeaters WHERE lat IS NOT NULL AND lat!=0").fetchone()[0]
        results["repeater_db"]={"ok":n_reps>0,"label":"Repeater Database",
                                 "detail":f"{n_reps} repeaters ({n_reps_geo} with coordinates)",
                                 "count":n_reps,"geo_count":n_reps_geo}
        n_roster=c.execute("SELECT COUNT(*) FROM roster").fetchone()[0]
        results["roster"]={"ok":n_roster>0,"label":"Member Roster",
                            "detail":f"{n_roster} members","count":n_roster}
        n_channels=c.execute("SELECT COUNT(*) FROM channel_library").fetchone()[0]
        results["channel_lib"]={"ok":n_channels>0,"label":"Channel Library",
                                 "detail":f"{n_channels} channels","count":n_channels}
        org=c.execute("SELECT org_name,callsign FROM station_config LIMIT 1").fetchone()
        org_ok=bool(org and org['org_name'] and org['callsign'])
        org_detail=f"{org['org_name']} ({org['callsign']})" if org_ok else "Not configured"
        results["org_setup"]={"ok":org_ok,"label":"Organization Setup","detail":org_detail}
        n_inc=c.execute("SELECT COUNT(*) FROM incidents WHERE status='active'").fetchone()[0]
        results["active_incident"]={"ok":n_inc>0,"label":"Active Incident",
                                     "detail":f"{n_inc} active incident{'s' if n_inc!=1 else ''}",
                                     "count":n_inc}
        dms=c.execute("SELECT state FROM dms_state WHERE id=1").fetchone()
        dms_s=dms["state"] if dms else "disarmed"
        results["dms_state"]={"ok":dms_s!="triggered","label":"Dead Man's Switch","state":dms_s}
        critical=["nginx","fcc-lookup","wifi_ap","org_setup"]; important=["direwolf","pat","fcc_db","gps_fix","roster","repeater_db"]
        crit_ok=all(results[k]["ok"] for k in critical)
        imp_ok=all(results[k]["ok"] for k in important if k in results)
        verdict="GO" if (crit_ok and imp_ok) else "CAUTION" if crit_ok else "NO-GO"
        c.execute("INSERT INTO preflight_runs(verdict,checks,timestamp) VALUES(?,?,?)",
                  (verdict,jdump(results),now)); c.commit()
        return {"verdict":verdict,"checks":results,"timestamp":now}


def _net_last_activity(c, net_id):
    """Latest check-in/traffic timestamp for a net (per-net dead-man's switch)."""
    key = str(net_id); ts = None
    for tbl in ("net_entries", "net_traffic"):
        try:
            r = c.execute(f"SELECT MAX(timestamp) FROM {tbl} WHERE CAST(net_id AS TEXT)=?", (key,)).fetchone()
            if r and r[0] and (ts is None or str(r[0]) > str(ts)): ts = r[0]
        except Exception:
            pass
    return ts


def dms_monitor():
    while True:
        try:
            c = get_conn()
            row = c.execute("SELECT armed_nets FROM dms_state WHERE id=1").fetchone()
            armed = jload(row["armed_nets"] if row else None, {})
            if isinstance(armed, dict) and armed:
                changed = False
                for nid, a in armed.items():
                    if a.get("state") == "triggered":
                        continue
                    thr = (a.get("threshold_min") or 30) * 60
                    last = _net_last_activity(c, nid)
                    if not last:
                        continue
                    try:
                        dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
                        if dt.tzinfo is None: dt = dt.replace(tzinfo=timezone.utc)
                        el = (datetime.now(timezone.utc) - dt).total_seconds()
                    except Exception:
                        continue
                    ns = "triggered" if el > thr else ("warning" if el > thr * 0.75 else "armed")
                    if ns != a.get("state"):
                        a["state"] = ns
                        if ns == "triggered": a["triggered_at"] = utcnow()
                        changed = True
                if changed:
                    gs = ("triggered" if any(x.get("state") == "triggered" for x in armed.values())
                          else "warning" if any(x.get("state") == "warning" for x in armed.values())
                          else "armed")
                    c.execute("UPDATE dms_state SET armed_nets=?, state=? WHERE id=1", (jdump(armed), gs))
                    c.commit()
        except Exception as e: log.warning(f"DMS monitor: {e}")
        time.sleep(30)


if __name__ == "__main__":
    db.startup()
    threading.Thread(target=dms_monitor, daemon=True).start()
    log.info("FCC Lookup API server on port 5050")
    HTTPServer(("0.0.0.0", 5050), Handler).serve_forever()
