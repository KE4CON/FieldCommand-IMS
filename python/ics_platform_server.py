# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""FieldCommand ICS Platform API — Port 5055 (SQLite via db.py)"""

import json, time, sys, logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import db
from db import get_conn, utcnow, jdump, jload, rows_to_list, row_to_dict

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [ics-platform] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout),
              logging.FileHandler('/var/log/fieldcommand-ics.log', mode='a')])
log = logging.getLogger('ics-platform')


def log_activity(incident_id, section, action, detail):
    get_conn().execute(
        "INSERT INTO activity_log(incident_id,section,action,detail,timestamp)"
        " VALUES(?,?,?,?,?)",
        (incident_id, section, action, detail, utcnow()))
    get_conn().commit()


def _rr_text(elem, tag):
    """Extract text from first matching XML child element."""
    import xml.etree.ElementTree as ET
    found = elem.find(".//" + tag)
    return (found.text or "").strip() if found is not None else ""

def _rr_mode(rr_mode_str):
    """Map RadioReference mode string to our standard."""
    m = (rr_mode_str or "").upper()
    if "P25" in m or "APCO" in m: return "P25"
    if "DMR"  in m:               return "DMR"
    if "NXDN" in m:               return "NXDN"
    if "DSTAR" in m or "D-STAR" in m: return "D-STAR"
    if "NFM"  in m:               return "NFM"
    if "FM"   in m:               return "FM"
    if "AM"   in m:               return "AM"
    return "FM"  # safe default

def _rr_tag_to_function(tag):
    """Map RadioReference tag to our function categories."""
    if not tag: return "Tactical"
    t = tag.lower()
    if "fire"    in t: return "Tactical"
    if "ems"     in t or "medical" in t: return "Medical"
    if "law"     in t or "police"  in t or "sheriff" in t: return "Command"
    if "interop" in t: return "Interop"
    if "command" in t: return "Command"
    if "dispatch" in t: return "Command"
    if "data"    in t: return "Data"
    if "air"     in t: return "Air"
    return "Tactical"


class ICSHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")

    def send_json(self, obj, code=200):
        body=json.dumps(obj,default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",len(body))
        self.cors(); self.end_headers(); self.wfile.write(body)

    def read_body(self):
        n=int(self.headers.get("Content-Length",0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()

    def do_GET(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/")
        qs=parse_qs(parsed.query); c=get_conn()

        if path == "/api/ics/incidents":
            return self.send_json(rows_to_list(
                c.execute("SELECT * FROM incidents ORDER BY started DESC").fetchall()))

        elif path.startswith("/api/ics/incidents/"):
            inc_id=path.split("/api/ics/incidents/")[1].split("/")[0]
            sub=path[len(f"/api/ics/incidents/{inc_id}"):]
            row=c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()
            if not row: return self.send_json({"error":"Not found"},404)
            if sub in ("","/"): return self.send_json(row_to_dict(row))
            elif sub=="/periods":
                return self.send_json(rows_to_list(c.execute(
                    "SELECT * FROM ics_periods WHERE incident_id=? ORDER BY period_num",(inc_id,)).fetchall()))
            elif sub=="/stats":
                obj_count  = c.execute("SELECT COUNT(*) FROM ics_periods WHERE incident_id=?",(inc_id,)).fetchone()[0]
                res_count  = c.execute("SELECT COUNT(*) FROM ics_resources WHERE incident_id=?",(inc_id,)).fetchone()[0]
                form_count = c.execute("SELECT COUNT(*) FROM ics_forms WHERE incident_id=?",(inc_id,)).fetchone()[0]
                inc_d = row_to_dict(row)
                return self.send_json({"objectives":obj_count,"current_period":inc_d.get("current_period",1),"resources":res_count,"forms":form_count})
            elif sub=="/planningp":
                inc_d = row_to_dict(row)
                periods = rows_to_list(c.execute(
                    "SELECT * FROM ics_periods WHERE incident_id=? ORDER BY period_num",(inc_id,)).fetchall())
                resources = rows_to_list(c.execute(
                    "SELECT callsign,name,role,status FROM ics_resources WHERE incident_id=?",(inc_id,)).fetchall())
                return self.send_json({"incident":inc_d,"periods":periods,"resources":resources})
            return self.send_json({"error":"Not found"},404)

        elif path.startswith("/api/ics/forms/"):
            parts=path.split("/api/ics/forms/")[1].split("/")
            form_type=parts[0]
            if len(parts)==1:
                inc_id=qs.get("incident_id",[None])[0]
                if inc_id:
                    rows=c.execute(
                        "SELECT id,incident_id,form_type,period,summary,created,updated"
                        " FROM ics_forms WHERE form_type=? AND incident_id=? ORDER BY created DESC",
                        (form_type,inc_id)).fetchall()
                else:
                    rows=c.execute(
                        "SELECT id,incident_id,form_type,period,summary,created,updated"
                        " FROM ics_forms WHERE form_type=? ORDER BY created DESC",
                        (form_type,)).fetchall()
                return self.send_json(rows_to_list(rows))
            else:
                fid=parts[1]
                row=c.execute("SELECT * FROM ics_forms WHERE id=?",(fid,)).fetchone()
                if row:
                    d=dict(row); d.update(jload(d.get("data"),{}))
                    return self.send_json(d)
                return self.send_json({"error":"Not found"},404)

        elif path == "/api/ics/tcards":
            inc_id=qs.get("incident_id",[None])[0]
            if inc_id:
                rows=c.execute("SELECT * FROM ics_tcards WHERE incident_id=? ORDER BY status,resource_name",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_tcards ORDER BY status,resource_name").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path.startswith("/api/ics/tcards/"):
            card_id=path.split("/api/ics/tcards/")[1]
            row=c.execute("SELECT * FROM ics_tcards WHERE id=?",(card_id,)).fetchone()
            return self.send_json(row_to_dict(row)) if row else self.send_json({"error":"Not found"},404)

        elif path == "/api/ics/resources":
            inc_id=qs.get("incident_id",[None])[0]
            if inc_id:
                rows=c.execute("SELECT * FROM ics_resources WHERE incident_id=? ORDER BY name",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_resources ORDER BY name").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/activity":
            inc_id=qs.get("incident_id",[None])[0]
            limit=int(qs.get("limit",[50])[0])
            if inc_id:
                rows=c.execute("SELECT * FROM activity_log WHERE incident_id=? ORDER BY timestamp DESC LIMIT ?",(inc_id,limit)).fetchall()
            else:
                rows=c.execute("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT ?",(limit,)).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/status":
            incs=c.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
            active=c.execute("SELECT COUNT(*) FROM incidents WHERE status='active'").fetchone()[0]
            return self.send_json({"service":"ics-platform","version":"2.0.0",
                "utc":utcnow(),"incidents":incs,"active":active,"db":str(db.DB_PATH)})

        elif path == "/api/ics/assignments":
            inc_id=qs.get("incident_id",[None])[0]
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            rows=c.execute("""
                SELECT e.callsign,e.name,e.ics_position,e.ema_id,
                       e.timestamp,e.checkout_time,n.name as net_name
                FROM net_entries e
                JOIN nets n ON e.net_id=n.id
                WHERE e.incident_id=? AND e.ics_position!=''
                ORDER BY e.timestamp
            """,(inc_id,)).fetchall()
            roster_rows=c.execute("""
                SELECT callsign,radio_id,
                       first_name||' '||last_name as name,
                       role,member_id
                FROM roster WHERE role!='' AND role!='Operator'
                ORDER BY role
            """).fetchall()
            return self.send_json({
                "assignments":rows_to_list(rows),
                "roster_roles":rows_to_list(roster_rows)
            })

        elif path == "/api/ics/meetings":
            inc_id=qs.get("incident_id",[None])[0]
            period=qs.get("period",[None])[0]
            if inc_id and period:
                rows=c.execute("SELECT * FROM ics_meetings WHERE incident_id=? AND period=? ORDER BY scheduled_time",(inc_id,int(period))).fetchall()
            elif inc_id:
                rows=c.execute("SELECT * FROM ics_meetings WHERE incident_id=? ORDER BY scheduled_time",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_meetings ORDER BY scheduled_time DESC LIMIT 50").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path.startswith("/api/ics/meetings/"):
            mid=path.split("/api/ics/meetings/")[1]
            row=c.execute("SELECT * FROM ics_meetings WHERE id=?",(mid,)).fetchone()
            if not row: return self.send_json({"error":"Not found"},404)
            return self.send_json(row_to_dict(row))


        # ── Resource History ────────────────────────────────────────────────
        elif path == "/api/ics/resource_history":
            inc_id = qs.get("incident_id",[""])[0]
            res_id = qs.get("resource_id",[""])[0]
            if inc_id:
                rows = c.execute(
                    "SELECT * FROM resource_history WHERE incident_id=? ORDER BY created DESC",
                    (inc_id,)).fetchall()
            elif res_id:
                rows = c.execute(
                    "SELECT * FROM resource_history WHERE resource_id=? ORDER BY created DESC",
                    (res_id,)).fetchall()
            else:
                rows = []
            return self.send_json(rows_to_list(rows))

        # ── Channel Library ─────────────────────────────────────────────────
        elif path == "/api/ics/channel_library":
            q = qs.get("q",[""])[0].lower()
            if q:
                rows = c.execute(
                    "SELECT * FROM channel_library WHERE active=1 AND "
                    "(LOWER(name) LIKE ? OR LOWER(alpha_tag) LIKE ? OR rx_freq LIKE ?) "
                    "ORDER BY name LIMIT 50",
                    (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
            else:
                rows = c.execute(
                    "SELECT * FROM channel_library WHERE active=1 ORDER BY name"
                ).fetchall()
            return self.send_json(rows_to_list(rows))


        # ── Active Channels — unified comms lookup ──────────────────────────
        # Returns merged channel list: ICS-205 for incident + channel_library
        # Used by net loggers, tactical map, cheat sheets for channel picker
        elif path == "/api/ics/active_channels":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            channels = []

            # 1. Pull from ICS-205 saved form for this incident/period
            if inc_id:
                row = c.execute(
                    "SELECT data FROM ics_forms "
                    "WHERE form_type=? AND incident_id=? AND period=? "
                    "ORDER BY updated DESC LIMIT 1",
                    ("ics205", inc_id, period)).fetchone()
                if row:
                    try:
                        import json as _json
                        fd = _json.loads(row[0] or "{}")
                        for i in range(30):
                            name = fd.get(f"ch205_name_{i}","").strip()
                            rx   = fd.get(f"ch205_rx_{i}","").strip()
                            if not name and not rx:
                                if i > 15: break
                                continue
                            channels.append({
                                "id":        f"205-{inc_id}-{i}",
                                "name":      name or rx,
                                "alpha_tag": fd.get(f"ch205_zone_{i}",""),
                                "rx_freq":   rx,
                                "tx_freq":   fd.get(f"ch205_tx_{i}","") or rx,
                                "pl_tone":   fd.get(f"ch205_pl_{i}",""),
                                "mode":      fd.get(f"ch205_mode_{i}","FM"),
                                "function":  fd.get(f"ch205_assign_{i}","Tactical"),
                                "division":  fd.get(f"ch205_division_{i}",""),
                                "notes":     fd.get(f"ch205_notes_{i}",""),
                                "source":    "ICS-205",
                                "incident_id": inc_id,
                                "period":    period,
                            })
                    except Exception:
                        pass

            # 2. Append channel_library entries (skip duplicates by freq)
            existing_freqs = {ch["rx_freq"] for ch in channels}
            lib_rows = c.execute(
                "SELECT * FROM channel_library WHERE active=1 ORDER BY name"
            ).fetchall()
            for lr in lib_rows:
                d = row_to_dict(lr)
                if d.get("rx_freq") not in existing_freqs:
                    d["source"] = "Library"
                    channels.append(d)

            # 3. Also pull active repeaters tagged ARES/RACES
            rep_rows = c.execute(
                "SELECT * FROM repeaters WHERE active=1 AND (ares=1 OR races=1) "
                "ORDER BY callsign LIMIT 50"
            ).fetchall()
            existing_freqs = {ch["rx_freq"] for ch in channels}
            for rr in rep_rows:
                d = row_to_dict(rr)
                freq = d.get("output_freq","")
                if freq and freq not in existing_freqs:
                    channels.append({
                        "id":        f"rep-{d.get('id','')}",
                        "name":      f"{d.get('callsign','')} Repeater",
                        "alpha_tag": d.get("callsign",""),
                        "rx_freq":   freq,
                        "tx_freq":   d.get("input_freq","") or freq,
                        "pl_tone":   d.get("tone",""),
                        "mode":      d.get("mode","FM"),
                        "function":  "Amateur" if not d.get("races") else "Interop",
                        "division":  "",
                        "notes":     d.get("city","") + " " + d.get("state",""),
                        "source":    "Repeater DB",
                    })

            return self.send_json({
                "channels": channels,
                "count":    len(channels),
                "incident_id": inc_id,
                "period":   period,
            })




        # ── WAN Configuration GET/POST ────────────────────────────────────────
        elif path == "/api/ics/wan_config":
            import json as _json
            cfg_path = Path("/opt/fieldcommand/data/wan_config.json")
            defaults_path = Path(__file__).parent / "wan_config_defaults.json"
            for p in [cfg_path, defaults_path]:
                if p.exists():
                    try:
                        return self.send_json(_json.loads(p.read_text()))
                    except Exception:
                        pass
            return self.send_json({})


        # ── IAP PDF Compile ─────────────────────────────────────────────────
        # GET  /api/ics/iap_status?incident_id=X&period=N
        #      Returns which forms are saved for this incident/period
        # POST /api/ics/iap_compile
        #      Compiles all saved forms into a single PDF download
        elif path == "/api/ics/iap_status":
            inc_id  = qs.get("incident_id",[""])[0]
            period  = int(qs.get("period",["1"])[0])
            rows    = rows_to_list(c.execute(
                "SELECT form_type, id, updated FROM ics_forms "
                "WHERE incident_id=? AND period=? ORDER BY form_type",
                (inc_id, period)
            ).fetchall())
            # Group by form_type
            by_type = {}
            for r in rows:
                by_type.setdefault(r["form_type"],[]).append(r)
            return self.send_json({
                "incident_id": inc_id,
                "period":      period,
                "forms":       by_type,
                "form_count":  len(rows),
                "pdf_available": HAS_PDF,
                "iap_order":   [ft for ft,_ in IAP_FORM_ORDER] if HAS_PDF else [],
            })

        # ── Incident Archive / Restore / Delete ─────────────────────────────
        # GET  /api/ics/incidents/archived     → list archived incidents on Pi
        # GET  /api/ics/incidents/lacie        → list archives on USB backup drive USB
        # POST /api/ics/incidents/archive      → archive incident to USB backup drive + mark Pi DB
        # POST /api/ics/incidents/restore      → restore from USB backup drive back to Pi DB
        # POST /api/ics/incidents/delete       → hard-delete incident from Pi DB
        # POST /api/ics/reset                  → beta reset: wipe all scenario data

        elif path == "/api/ics/incidents/archived":
            rows = c.execute(
                "SELECT * FROM incidents WHERE archived=1 ORDER BY archived_at DESC"
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/incidents/lacie":
            # List incident archives on the USB backup drive drive
            import os, json as _json
            lacie_base = "/media/fieldcommand/backup/incidents"
            archives = []
            if os.path.isdir(lacie_base):
                for folder in sorted(os.listdir(lacie_base), reverse=True):
                    folder_path = os.path.join(lacie_base, folder)
                    meta_path   = os.path.join(folder_path, "incident_meta.json")
                    if os.path.isfile(meta_path):
                        try:
                            with open(meta_path) as f:
                                meta = _json.load(f)
                            meta["folder"] = folder
                            meta["path"]   = folder_path
                            archives.append(meta)
                        except Exception:
                            archives.append({"folder":folder,"path":folder_path,"name":folder})
            return self.send_json({
                "lacie_mounted": os.path.isdir(lacie_base),
                "archives":      archives,
                "lacie_path":    lacie_base,
            })

        # ── ICS-211 Remote Check-In ─────────────────────────────────────────
        # GET: fetch pending entries for an incident/period




        # ── Incident Templates API ──────────────────────────────────────────
        # GET  /api/ics/templates              → list all enabled templates
        # GET  /api/ics/templates/<id>         → get single template
        # POST /api/ics/templates              → create or update template
        # POST /api/ics/templates/import       → import JSON array of templates
        # DELETE via do_DELETE /api/ics/templates/<id>

        elif path == "/api/ics/templates":
            rows = rows_to_list(
                c.execute("SELECT * FROM incident_templates WHERE enabled=1 ORDER BY sort_order,name").fetchall()
            )
            for r in rows:
                try: r["data"] = json.loads(r.get("data","{}"))
                except Exception: r["data"] = {}
            return self.send_json(rows)

        elif path.startswith("/api/ics/templates/") and path != "/api/ics/templates/import":
            tid = path.split("/api/ics/templates/")[1]
            row = c.execute("SELECT * FROM incident_templates WHERE id=?", (tid,)).fetchone()
            if not row:
                return self.send_json({"error":"Not found"},404)
            r = dict(row)
            try: r["data"] = json.loads(r.get("data","{}"))
            except Exception: r["data"] = {}
            return self.send_json(r)

        # ── FEMA Equipment Rates API ─────────────────────────────────────────
        elif path == "/api/ics/fema/rates":
            import datetime as _dt
            category = qs.get("category",[""])[0]
            q        = qs.get("q",[""])[0].lower()
            sql      = "SELECT * FROM fema_equipment_rates WHERE active=1"
            params   = []
            if category:
                sql += " AND category=?"; params.append(category)
            rows = rows_to_list(c.execute(sql + " ORDER BY category,description", params).fetchall())
            if q:
                rows = [r for r in rows if q in r.get("description","").lower()
                        or q in r.get("code","").lower() or q in r.get("category","").lower()]

            # Compute reminder: how old are the rates?
            max_year = max((r.get("rate_year",0) for r in rows), default=0)
            current_year = _dt.datetime.utcnow().year
            years_old    = current_year - max_year if max_year else None
            reminder     = None
            if years_old and years_old >= 1:
                reminder = (
                    f"Your FEMA equipment rates are from {max_year} — now {years_old} year(s) old. "
                    f"FEMA typically updates rates annually. Check "
                    f"fema.gov/assistance/public/tools-resources/schedule-equipment-rates "
                    f"and update if a newer schedule applies to your incident."
                )

            categories = sorted(set(r.get("category","") for r in rows))
            return self.send_json({
                "rates":       rows,
                "categories":  categories,
                "rate_year":   max_year,
                "years_old":   years_old,
                "reminder":    reminder,
                "source":      "FEMA Schedule of Equipment Rates",
                "source_url":  "https://www.fema.gov/assistance/public/tools-resources/schedule-equipment-rates",
            })


        # ── Resource GPS Update ─────────────────────────────────────────────
        # GET  /api/ics/resources/gps?incident_id=X  → all resource positions
        # POST /api/ics/resources/gps                → update position for one resource
        elif path == "/api/ics/resources/gps":
            inc_id = qs.get("incident_id",[""])[0]
            rows = rows_to_list(c.execute(
                """SELECT id, resource_name, resource_type, status, assignment,
                          lat, lon, gps_updated, gps_source, location_label,
                          num_personnel, leader, category
                   FROM ics_tcards
                   WHERE incident_id=? AND lat IS NOT NULL AND lon IS NOT NULL
                   ORDER BY resource_type, resource_name""",
                (inc_id,)
            ).fetchall())
            return self.send_json(rows)

        # ── Cost Dashboard API ──────────────────────────────────────────────
        # GET /api/ics/cost_summary?incident_id=X
        # Returns aggregated cost by category + burn rate
        elif path == "/api/ics/cost_summary":
            inc_id = qs.get("incident_id",[""])[0]
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)

            # Pull FEMA entered costs
            labor_rows  = rows_to_list(c.execute(
                "SELECT * FROM fema_labor WHERE incident_id=?", (inc_id,)).fetchall())
            equip_rows  = rows_to_list(c.execute(
                "SELECT * FROM fema_equipment WHERE incident_id=?", (inc_id,)).fetchall())
            mat_rows    = rows_to_list(c.execute(
                "SELECT * FROM fema_materials WHERE incident_id=?", (inc_id,)).fetchall())

            # Labor cost
            def labor_cost(r):
                base = (r.get("hours_reg",0) or 0)*(r.get("rate_reg",0) or 0) +                        (r.get("hours_ot",0) or 0)*(r.get("rate_ot",0) or 0)
                return base * (1 + (r.get("fringe_pct",0) or 0)/100)

            total_labor  = sum(labor_cost(r) for r in labor_rows)
            total_equip  = sum((r.get("hours_used",0) or 0)*(r.get("rate_hr",0) or 0)
                               for r in equip_rows)
            total_mat    = sum(r.get("total_cost",0) or 0 for r in mat_rows)
            total_fema   = total_labor + total_equip + total_mat

            # T-card resource counts by category
            tcards = rows_to_list(c.execute(
                "SELECT * FROM ics_tcards WHERE incident_id=?", (inc_id,)).fetchall())

            by_type = {}
            for t in tcards:
                rtype = t.get("resource_type") or t.get("category") or "Unknown"
                by_type.setdefault(rtype, {"count":0, "personnel":0, "daily_cost":0})
                by_type[rtype]["count"] += 1
                by_type[rtype]["personnel"] += t.get("num_personnel",0) or 0
                by_type[rtype]["daily_cost"] += t.get("daily_cost",0) or 0

            # Pull incident start time for elapsed time calculation
            inc_row = c.execute("SELECT started, current_period FROM incidents WHERE id=?",
                                (inc_id,)).fetchone()
            started = inc_row["started"] if inc_row else None
            current_period = inc_row["current_period"] if inc_row else 1

            import datetime
            elapsed_hours = None
            if started:
                try:
                    start_dt = datetime.datetime.fromisoformat(started.replace("Z",""))
                    elapsed  = datetime.datetime.utcnow() - start_dt
                    elapsed_hours = round(elapsed.total_seconds() / 3600, 1)
                except Exception:
                    pass

            # Burn rate: total costs / elapsed hours
            burn_per_hour = round(total_fema / elapsed_hours, 2)                 if elapsed_hours and elapsed_hours > 0 else None

            return self.send_json({
                "incident_id":    inc_id,
                "elapsed_hours":  elapsed_hours,
                "current_period": current_period,
                "totals": {
                    "labor":       round(total_labor, 2),
                    "equipment":   round(total_equip, 2),
                    "materials":   round(total_mat,   2),
                    "total":       round(total_fema,  2),
                },
                "burn_rate": {
                    "per_hour": burn_per_hour,
                    "per_day":  round(burn_per_hour * 24, 2) if burn_per_hour else None,
                    "per_period": round(burn_per_hour * 12, 2) if burn_per_hour else None,
                },
                "resources_by_type": by_type,
                "counts": {
                    "labor_entries":    len(labor_rows),
                    "equipment_entries":len(equip_rows),
                    "material_entries": len(mat_rows),
                    "tcards":           len(tcards),
                    "total_personnel":  sum(t.get("num_personnel",0) or 0 for t in tcards),
                },
            })

        # ── FEMA PA Cost Tracking API ────────────────────────────────────────
        elif path == "/api/ics/fema/labor":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_labor WHERE incident_id=? ORDER BY date_worked,employee",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/fema/equipment":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_equipment WHERE incident_id=? ORDER BY date_used,equipment",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/fema/materials":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_materials WHERE incident_id=? ORDER BY date_purch,description",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/checkin":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            synced = qs.get("synced",[""])[0]
            sql    = "SELECT * FROM checkin_entries WHERE incident_id=? AND period=?"
            params = [inc_id, period]
            if synced == "0":
                sql    += " AND synced_to_211=0"
            rows = c.execute(sql + " ORDER BY created DESC", params).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/general_info":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            row = c.execute(
                "SELECT * FROM general_info WHERE incident_id=? AND period=?",
                (inc_id, period)).fetchone()
            if row:
                return self.send_json(row_to_dict(row))
            inc = c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()
            if inc:
                d = row_to_dict(inc)
                d["incident_location"] = d.get("location","")
                d["operational_period_number"] = period
                return self.send_json(d)
            return self.send_json({})


        # ── Resource History POST ───────────────────────────────────────────
        elif path == "/api/ics/resource_history":
            entries = body.get("entries", [])
            for e in entries:
                rh_id = f"rh-{int(time.time()*1000)}-{e.get('resource_id','')}"
                c.execute("""INSERT OR IGNORE INTO resource_history
                    (id, incident_id, period, resource_id, resource_name,
                     resource_type, assignment, date, created)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (rh_id, e.get("incident_id",""), e.get("period",1),
                     e.get("resource_id",""), e.get("resource_name",""),
                     e.get("resource_type",""), e.get("assignment",""),
                     e.get("date",""), now))
            c.commit()
            return self.send_json({"status":"ok","count":len(entries)})

        # ── Channel Library POST ─────────────────────────────────────────────
        elif path == "/api/ics/channel_library":
            ch_id = body.get("id") or f"ch-{int(time.time()*1000)}"
            existing = c.execute("SELECT id FROM channel_library WHERE id=?",(ch_id,)).fetchone()
            fields = ["name","alpha_tag","rx_freq","tx_freq","pl_tone","mode",
                      "function","division","notes","custom","active"]
            if existing:
                sets = ", ".join(f"{f}=?" for f in fields)
                vals = [body.get(f,"") for f in fields] + [ch_id]
                c.execute(f"UPDATE channel_library SET {sets} WHERE id=?", vals)
            else:
                cols = "id, " + ", ".join(fields) + ", created"
                phs  = ", ".join(["?"]*(len(fields)+2))
                vals = [ch_id] + [body.get(f,"") for f in fields] + [now]
                c.execute(f"INSERT INTO channel_library ({cols}) VALUES ({phs})", vals)
            c.commit()
            return self.send_json({"status":"ok","id":ch_id})


        # ── RadioReference SOAP Proxy ───────────────────────────────────────
        # Proxies requests to the RadioReference SOAP API on behalf of the
        # client — avoids CORS issues and keeps credentials server-side per session.
        # User supplies their own RR username/password (premium subscription required).
        # We never store credentials — they are passed per-request only.
        elif path == "/api/ics/rr_search":
            import urllib.request
            rr_username = body.get("username","")
            rr_password = body.get("password","")
            rr_appkey   = body.get("appkey","")
            search_type = body.get("type","county")   # county | zip | agency
            search_val  = body.get("value","")        # countyId, ZIP, agencyId
            tag_filter  = body.get("tag","")          # optional tag (Fire, EMS, Law, etc.)

            if not all([rr_username, rr_password, search_val]):
                return self.send_json({"error":"username, password, and value are required"},400)

            # Build SOAP envelope based on search type
            if search_type == "zip":
                method   = "getZipCodeInfo"
                body_xml = f"<cid>{search_val}</cid>"
            elif search_type == "county_freqs" and tag_filter:
                method   = "getCountyFreqsByTag"
                body_xml = f"<cid>{search_val}</cid><tagId>{tag_filter}</tagId>"
            elif search_type == "county_freqs":
                method   = "getCountyInfo"
                body_xml = f"<cid>{search_val}</cid>"
            elif search_type == "agency":
                method   = "getAgencyInfo"
                body_xml = f"<aid>{search_val}</aid>"
            else:
                return self.send_json({"error":f"unknown search type: {search_type}"},400)

            soap_env = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:ns1="http://api.radioreference.com/soap2">
  <SOAP-ENV:Body>
    <ns1:{method}>
      <authInfo>
        <appKey>{rr_appkey or "FieldCommandIMS"}</appKey>
        <username>{rr_username}</username>
        <password>{rr_password}</password>
        <version>latest</version>
        <style>rpc</style>
      </authInfo>
      {body_xml}
    </ns1:{method}>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

            try:
                req = urllib.request.Request(
                    "https://api.radioreference.com/soap2/",
                    data=soap_env.encode("utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8",
                        "SOAPAction": f"http://api.radioreference.com/soap2/#{method}",
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    xml_resp = resp.read().decode("utf-8")

                # Parse the SOAP XML response into something useful
                import xml.etree.ElementTree as ET
                root = ET.fromstring(xml_resp)
                ns   = {"s": "http://schemas.xmlsoap.org/soap/envelope/"}

                # Check for SOAP fault
                fault = root.find(".//faultstring")
                if fault is not None:
                    return self.send_json({"error": fault.text or "SOAP fault"}, 400)

                # Extract frequencies from getCountyInfo / getCountyFreqsByTag
                channels = []
                # Conventional frequencies
                for freq in root.iter("freqs"):
                    output   = _rr_text(freq, "output")
                    input_f  = _rr_text(freq, "input")
                    pl_tone  = _rr_text(freq, "pl")
                    desc     = _rr_text(freq, "descr")
                    alpha    = _rr_text(freq, "alpha")
                    mode     = _rr_text(freq, "mode") or "FM"
                    tag_name = _rr_text(freq, "tag")
                    if output:
                        channels.append({
                            "name":      desc or alpha or output,
                            "alpha_tag": alpha or "",
                            "rx_freq":   output,
                            "tx_freq":   input_f or output,
                            "pl_tone":   pl_tone or "",
                            "mode":      _rr_mode(mode),
                            "function":  _rr_tag_to_function(tag_name),
                            "notes":     tag_name or "",
                            "source":    "RadioReference",
                        })

                # For zip lookup — return county/state info
                if search_type == "zip":
                    result = {
                        "county_id": _rr_text(root, "cid"),
                        "state_id":  _rr_text(root, "stid"),
                        "city":      _rr_text(root, "ctName"),
                        "lat":       _rr_text(root, "lat"),
                        "lon":       _rr_text(root, "lon"),
                    }
                    return self.send_json(result)

                return self.send_json({
                    "channels": channels,
                    "count":    len(channels),
                    "source":   "RadioReference SOAP API",
                })

            except Exception as e:
                return self.send_json({"error": str(e)}, 503)


        # ── ICS-211 Remote Check-In POST ────────────────────────────────────



        # ── WAN Configuration POST ───────────────────────────────────────────
        elif path == "/api/ics/wan_config":
            import json as _json
            cfg_path = Path("/opt/fieldcommand/data/wan_config.json")
            try:
                cfg_path.parent.mkdir(parents=True, exist_ok=True)
                cfg_path.write_text(_json.dumps(body, indent=2))
                return self.send_json({"ok": True})
            except Exception as e:
                return self.send_json({"error": str(e)}, 500)


        # ── IAP PDF Compile POST ─────────────────────────────────────────────
        elif path == "/api/ics/iap_compile":
            if not HAS_PDF:
                return self.send_json({"error": "PDF compiler not available: " + _pdf_err_msg}, 503)

            inc_id  = body.get("incident_id","")
            period  = body.get("period", 1)
            form_types = body.get("form_types", [])  # empty = all
            include_title = body.get("include_title", True)

            if not inc_id:
                return self.send_json({"error": "incident_id required"}, 400)

            # Fetch incident name
            inc_row = c.execute("SELECT name FROM incidents WHERE id=?", (inc_id,)).fetchone()
            incident_name = inc_row["name"] if inc_row else "Unknown Incident"

            # Fetch all forms for this incident/period
            if form_types:
                placeholders = ",".join("?"*len(form_types))
                rows = rows_to_list(c.execute(
                    f"SELECT * FROM ics_forms WHERE incident_id=? AND period=? "
                    f"AND form_type IN ({placeholders}) ORDER BY form_type, created",
                    [inc_id, period] + form_types
                ).fetchall())
            else:
                rows = rows_to_list(c.execute(
                    "SELECT * FROM ics_forms WHERE incident_id=? AND period=? ORDER BY form_type, created",
                    (inc_id, period)
                ).fetchall())

            if not rows:
                return self.send_json({"error": "No forms found for this incident/period"}, 404)

            # Build forms_by_type dict
            forms_by_type = {}
            for r in rows:
                ft = r.get("form_type","")
                try:    fdata = json.loads(r.get("data","{}"))
                except: fdata = {}
                fdata["_form_id"]    = r.get("id","")
                fdata["_form_type"]  = ft
                fdata["_updated"]    = r.get("updated","")
                forms_by_type.setdefault(ft, []).append(fdata)

            # Compile
            try:
                pdf_bytes = compile_iap(
                    forms_by_type,
                    incident_name = incident_name,
                    period        = period,
                    prepared_by   = body.get("prepared_by",""),
                    date_str      = body.get("date_str", now[:10]),
                    include_title = include_title,
                )

                # Send as PDF download
                safe_name = "".join(c2 if c2.isalnum() else "_" for c2 in incident_name)[:30]
                filename  = f"IAP_{safe_name}_P{period}_{now[:10]}.pdf"
                self.send_response(200)
                self.send_header("Content-Type",        "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length",       str(len(pdf_bytes)))
                self.cors()
                self.end_headers()
                self.wfile.write(pdf_bytes)
                return
            except Exception as e:
                import traceback
                traceback.print_exc()
                return self.send_json({"error": str(e)}, 500)

        # ── Incident Archive POST ────────────────────────────────────────────
        elif path == "/api/ics/incidents/archive":
            import os, json as _json, shutil, sqlite3 as _sq
            inc_id = body.get("incident_id","")
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)

            lacie_base = "/media/fieldcommand/backup/incidents"
            if not os.path.isdir("/media/fieldcommand"):
                return self.send_json({"error":"USB backup drive not mounted — label drive FIELDCOMMAND and connect"},503)

            # Fetch incident from DB
            row = c.execute("SELECT * FROM incidents WHERE id=?", (inc_id,)).fetchone()
            if not row:
                return self.send_json({"error":"Incident not found"},404)
            inc = dict(row)

            # Create archive folder
            slug    = "".join(c2 if c2.isalnum() else "_" for c2 in inc["name"])[:30]
            folder  = f"{now[:10]}_{slug}_{inc_id[:8]}"
            dest    = os.path.join(lacie_base, folder)
            os.makedirs(dest, exist_ok=True)

            # Dump all related data to JSON
            tables = {
                "incident":  [inc],
                "forms":     rows_to_list(c.execute("SELECT * FROM ics_forms WHERE incident_id=?",    (inc_id,)).fetchall()),
                "labor":     rows_to_list(c.execute("SELECT * FROM fema_labor WHERE incident_id=?",   (inc_id,)).fetchall()),
                "equipment": rows_to_list(c.execute("SELECT * FROM fema_equipment WHERE incident_id=?",(inc_id,)).fetchall()),
                "materials": rows_to_list(c.execute("SELECT * FROM fema_materials WHERE incident_id=?",(inc_id,)).fetchall()),
                "checkins":  rows_to_list(c.execute("SELECT * FROM checkin_entries WHERE incident_id=?",(inc_id,)).fetchall()),
                "tcards":    rows_to_list(c.execute("SELECT * FROM ics_tcards WHERE incident_id=?",    (inc_id,)).fetchall()),
                "meetings":  rows_to_list(c.execute("SELECT * FROM ics_meetings WHERE incident_id=?",  (inc_id,)).fetchall()),
            }

            # Write full archive JSON
            archive_path = os.path.join(dest, "incident_data.json")
            with open(archive_path, "w") as f:
                _json.dump(tables, f, indent=2, default=str)

            # Write human-readable metadata
            meta_path = os.path.join(dest, "incident_meta.json")
            with open(meta_path, "w") as f:
                _json.dump({
                    "incident_id":   inc_id,
                    "name":          inc["name"],
                    "type":          inc.get("type",""),
                    "status":        inc.get("status",""),
                    "started":       inc.get("started",""),
                    "closed":        inc.get("closed",""),
                    "archived_at":   now,
                    "folder":        folder,
                    "form_count":    len(tables["forms"]),
                    "labor_count":   len(tables["labor"]),
                    "equip_count":   len(tables["equipment"]),
                    "mat_count":     len(tables["materials"]),
                    "checkin_count": len(tables["checkins"]),
                }, f, indent=2)

            # Mark incident as archived in Pi DB (keeps data, just flagged)
            c.execute(
                "UPDATE incidents SET archived=1, archive_path=?, archived_at=?, status=? WHERE id=?",
                (dest, now, "archived", inc_id)
            )
            c.commit()
            return self.send_json({"ok":True,"archive_path":dest,"folder":folder})

        # ── Restore archived incident from USB backup drive ────────────────────────────
        elif path == "/api/ics/incidents/restore":
            import os, json as _json
            folder = body.get("folder","")
            lacie_base = "/media/fieldcommand/backup/incidents"
            archive_path = os.path.join(lacie_base, folder)
            data_file    = os.path.join(archive_path, "incident_data.json")
            if not os.path.isfile(data_file):
                return self.send_json({"error":"Archive not found"},404)

            with open(data_file) as f:
                data = _json.load(f)

            # Restore incident row first
            for inc in data.get("incident",[]):
                inc["archived"] = 0  # mark as active again
                inc["status"]   = inc.get("status","active") if inc.get("status") != "archived" else "closed"
                cols = ",".join(inc.keys())
                ph   = ",".join("?"*len(inc))
                c.execute(f"INSERT OR REPLACE INTO incidents ({cols}) VALUES ({ph})",
                          list(inc.values()))

            # Restore forms
            for row in data.get("forms",[]):
                cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                c.execute(f"INSERT OR REPLACE INTO ics_forms ({cols}) VALUES ({ph})", list(row.values()))

            # Restore cost data
            for table, key in [("fema_labor","labor"),("fema_equipment","equipment"),("fema_materials","materials")]:
                for row in data.get(key,[]):
                    cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                    c.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})", list(row.values()))

            # Restore check-ins, tcards, meetings
            for table, key in [("checkin_entries","checkins"),("ics_tcards","tcards"),("ics_meetings","meetings")]:
                for row in data.get(key,[]):
                    cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                    try:
                        c.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})", list(row.values()))
                    except Exception: pass

            c.commit()
            inc_id = data.get("incident",[{}])[0].get("id","")
            return self.send_json({"ok":True,"incident_id":inc_id,
                "restored_forms": len(data.get("forms",[]))})

        # ── Hard-delete incident from Pi DB ─────────────────────────────────
        elif path == "/api/ics/incidents/delete":
            inc_id = body.get("incident_id","")
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            for table in ["ics_forms","fema_labor","fema_equipment","fema_materials",
                          "checkin_entries","ics_tcards","ics_meetings","general_info"]:
                try:
                    c.execute(f"DELETE FROM {table} WHERE incident_id=?", (inc_id,))
                except Exception: pass
            c.execute("DELETE FROM incidents WHERE id=?", (inc_id,))
            c.commit()
            return self.send_json({"ok":True,"deleted":inc_id})

        # ── Beta / Scenario Reset ────────────────────────────────────────────
        # Wipes all incident data, forms, costs, check-ins, T-cards.
        # Leaves intact: roster, hospitals, channel_library, resource_types,
        # repeaters, system config. Requires confirm="RESET" in body.
        elif path == "/api/ics/reset":
            if body.get("confirm") != "RESET":
                return self.send_json({"error":"Send confirm='RESET' to proceed"},400)
            wipe_tables = [
                "incidents","ics_forms","general_info",
                "fema_labor","fema_equipment","fema_materials",
                "checkin_entries","ics_tcards","ics_meetings",
                "resource_history","ics_periods",
            ]
            counts = {}
            for table in wipe_tables:
                try:
                    n = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                    c.execute(f"DELETE FROM {table}")
                    counts[table] = n
                except Exception as e:
                    counts[table] = f"error: {e}"
            c.commit()
            return self.send_json({"ok":True,"wiped":counts,
                "preserved":["roster","hospitals","channel_library",
                             "resource_types","repeaters","net_entries"]})



        # ── Incident Templates POST (create / update) ────────────────────────
        elif path == "/api/ics/templates":
            tid = body.get("id") or f"tmpl-{int(time.time()*1000)}"
            data_str = json.dumps(body.get("data", {}))
            existing = c.execute("SELECT id FROM incident_templates WHERE id=?", (tid,)).fetchone()
            if existing:
                c.execute("""UPDATE incident_templates SET
                    name=?,icon=?,type=?,summary=?,sort_order=?,enabled=?,data=?,updated=?
                    WHERE id=?""",
                    (body.get("name","Untitled"), body.get("icon","📋"),
                     body.get("type",""), body.get("summary",""),
                     body.get("sort_order",99), body.get("enabled",1),
                     data_str, now, tid))
            else:
                c.execute("""INSERT INTO incident_templates
                    (id,name,icon,type,summary,sort_order,is_builtin,enabled,data,created,updated)
                    VALUES (?,?,?,?,?,?,0,1,?,?,?)""",
                    (tid, body.get("name","Untitled"), body.get("icon","📋"),
                     body.get("type",""), body.get("summary",""),
                     body.get("sort_order",99), data_str, now, now))
            c.commit()
            return self.send_json({"ok":True,"id":tid})

        # ── Import templates from JSON ────────────────────────────────────────
        elif path == "/api/ics/templates/import":
            templates = body if isinstance(body, list) else body.get("templates", [])
            imported = 0
            for t in templates:
                tid = t.get("id") or f"tmpl-{int(time.time()*1000)}-{imported}"
                # Check for ID collision — append _imported if needed
                existing = c.execute("SELECT id FROM incident_templates WHERE id=?", (tid,)).fetchone()
                if existing:
                    tid = tid + "_imported"
                c.execute("""INSERT OR REPLACE INTO incident_templates
                    (id,name,icon,type,summary,sort_order,is_builtin,enabled,data,created,updated)
                    VALUES (?,?,?,?,?,?,0,1,?,?,?)""",
                    (tid, t.get("name","Imported"), t.get("icon","📋"),
                     t.get("type",""), t.get("summary",""),
                     t.get("sort_order",99),
                     json.dumps(t.get("data",{})), now, now))
                imported += 1
            c.commit()
            return self.send_json({"ok":True,"imported":imported})

        # ── FEMA Equipment Rates POST (add/update custom rate) ──────────────
        elif path == "/api/ics/fema/rates":
            rid = body.get("id")
            if rid:
                # Update existing
                fields = ["code","category","description","unit","rate","rate_year","notes","active"]
                sets   = [f"{f}=?" for f in fields if f in body]
                vals   = [body[f] for f in fields if f in body] + [rid]
                if sets:
                    c.execute(f"UPDATE fema_equipment_rates SET {','.join(sets)} WHERE id=?", vals)
            else:
                c.execute(
                    "INSERT INTO fema_equipment_rates (code,category,description,unit,rate,rate_year,notes) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (body.get("code",""), body.get("category",""), body.get("description",""),
                     body.get("unit","hour"), body.get("rate",0),
                     body.get("rate_year",2025), body.get("notes",""))
                )
                rid = c.lastrowid
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        # ── FEMA Rates bulk year update ──────────────────────────────────────
        elif path == "/api/ics/fema/rates/update_year":
            new_year = body.get("year")
            if not new_year:
                return self.send_json({"error":"year required"},400)
            c.execute("UPDATE fema_equipment_rates SET rate_year=? WHERE active=1", (new_year,))
            n = c.execute("SELECT changes()").fetchone()[0]
            c.commit()
            return self.send_json({"ok":True,"updated":n,"year":new_year})


        # ── Resource GPS Position POST ───────────────────────────────────────
        elif path == "/api/ics/resources/gps":
            card_id = body.get("id")
            lat     = body.get("lat")
            lon     = body.get("lon")
            if not card_id or lat is None or lon is None:
                return self.send_json({"error":"id, lat, lon required"},400)
            c.execute(
                """UPDATE ics_tcards SET lat=?, lon=?, gps_updated=?,
                   gps_source=?, location_label=?, updated=?
                   WHERE id=?""",
                (lat, lon, now,
                 body.get("gps_source","manual"),
                 body.get("location_label",""),
                 now, card_id)
            )
            c.commit()
            return self.send_json({"ok":True})

        # ── Clear GPS for a resource ─────────────────────────────────────────
        elif path == "/api/ics/resources/gps/clear":
            card_id = body.get("id")
            if not card_id:
                return self.send_json({"error":"id required"},400)
            c.execute(
                "UPDATE ics_tcards SET lat=NULL, lon=NULL, gps_source='', location_label='' WHERE id=?",
                (card_id,)
            )
            c.commit()
            return self.send_json({"ok":True})

        # ── FEMA PA Cost Tracking POST ───────────────────────────────────────
        elif path == "/api/ics/fema/labor":
            rid = body.get("id") or f"lab-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO fema_labor
                (id,incident_id,period,employee,position,dept,date_worked,
                 hours_reg,hours_ot,rate_reg,rate_ot,fringe_pct,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("period",0),
                 body.get("employee",""), body.get("position",""),
                 body.get("dept",""), body.get("date_worked",""),
                 body.get("hours_reg",0), body.get("hours_ot",0),
                 body.get("rate_reg",0), body.get("rate_ot",0),
                 body.get("fringe_pct",0), body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/fema/equipment":
            rid = body.get("id") or f"eq-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO fema_equipment
                (id,incident_id,period,equipment,equip_id,fema_code,
                 hours_used,rate_hr,operator,date_used,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("period",0),
                 body.get("equipment",""), body.get("equip_id",""),
                 body.get("fema_code",""), body.get("hours_used",0),
                 body.get("rate_hr",0), body.get("operator",""),
                 body.get("date_used",""), body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/fema/materials":
            rid = body.get("id") or f"mat-{int(time.time()*1000)}"
            total = body.get("total_cost") or (body.get("quantity",1) * body.get("unit_cost",0))
            c.execute("""INSERT OR REPLACE INTO fema_materials
                (id,incident_id,description,vendor,quantity,unit,
                 unit_cost,total_cost,po_number,date_purch,category,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("description",""),
                 body.get("vendor",""), body.get("quantity",1), body.get("unit",""),
                 body.get("unit_cost",0), total, body.get("po_number",""),
                 body.get("date_purch",""), body.get("category","Materials"),
                 body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/checkin":
            ci_id = body.get("id") or f"ci-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO checkin_entries
                (id, incident_id, period, name, callsign_id, agency,
                 ics_position, resource_type, check_in_time, equipment,
                 home_unit, status, synced_to_211, notes, created)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (ci_id,
                 body.get("incident_id",""), body.get("period",1),
                 body.get("name",""), body.get("callsign_id",""),
                 body.get("agency",""), body.get("ics_position",""),
                 body.get("resource_type",""), body.get("check_in_time", now),
                 body.get("equipment",""), body.get("home_unit",""),
                 body.get("status","Checked In"),
                 body.get("synced_to_211",0),
                 body.get("notes",""), now))
            c.commit()
            return self.send_json({"status":"ok","id":ci_id})

        # ── Mark check-in entries as synced to ICS-211 ─────────────────────
        elif path == "/api/ics/checkin/sync":
            ids = body.get("ids",[])
            for cid in ids:
                c.execute("UPDATE checkin_entries SET synced_to_211=1 WHERE id=?", (cid,))
            c.commit()
            return self.send_json({"status":"ok","synced":len(ids)})

        elif path == "/api/ics/general_info":
            inc_id = body.get("incident_id","")
            period = int(body.get("period",1))
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            gi_id  = f"{inc_id}-{period}"
            fields = [
                "incident_name","incident_number","incident_type","jurisdiction","incident_location","lat","lon","operational_period_from","operational_period_to","incident_commander","deputy_ic","safety_officer","public_info_officer","liaison_officer","ops_section_chief","planning_section_chief","logistics_section_chief","finance_section_chief","resources_unit_ldr","situation_unit_ldr","documentation_unit_ldr","demob_unit_ldr","coml_name","medical_unit_ldr","weather_forecast","weather_temp","weather_wind","weather_humidity","weather_sky","sunrise","sunset","prepared_by","approved_by","ics_variant"
            ]
            existing = c.execute(
                "SELECT id FROM general_info WHERE id=?",(gi_id,)).fetchone()
            if existing:
                sets = ", ".join(f"{f}=?" for f in fields) + ", updated=?"
                vals = [body.get(f,"") for f in fields] + [now, gi_id]
                c.execute(f"UPDATE general_info SET {sets} WHERE id=?", vals)
            else:
                cols = "id, incident_id, period, " + ", ".join(fields) + ", updated"
                phs  = ", ".join(["?"] * (len(fields) + 4))
                vals = [gi_id, inc_id, period] + [body.get(f,"") for f in fields] + [now]
                c.execute(f"INSERT INTO general_info ({cols}) VALUES ({phs})", vals)
            c.execute("""UPDATE incidents SET name=?, incident_commander=?,
                location=?, jurisdiction=?, ics_variant=?, updated=? WHERE id=?""",
                (body.get("incident_name",""),body.get("incident_commander",""),
                 body.get("incident_location",""),body.get("jurisdiction",""),
                 body.get("ics_variant","FEMA"),now, inc_id))
            c.commit()
            return self.send_json({"status":"ok","id":gi_id})

        else:
            self.send_json({"error":"Not found"},404)

    def do_POST(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/")
        body=self.read_body(); c=get_conn(); now=utcnow()

        if path == "/api/ics/incidents":
            inc_id=body.get("id") or f"inc-{int(time.time()*1000)}"
            c.execute("""INSERT INTO incidents
                (id,name,type,status,jurisdiction,incident_commander,
                 location,summary,current_period,started)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (inc_id,body.get("name",""),body.get("type",""),
                 "active",body.get("jurisdiction",""),
                 body.get("incident_commander",""),body.get("location",""),
                 body.get("summary",""),1,now))
            # Create period 1
            c.execute("INSERT INTO ics_periods(id,incident_id,period_num,started) VALUES(?,?,?,?)",
                      (f"per-{inc_id}-1",inc_id,1,now))
            c.commit()
            log_activity(inc_id,"Command","Incident Created",body.get("name",""))
            inc=row_to_dict(c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone())
            return self.send_json({"ok":True,"incident":inc})

        elif path.startswith("/api/ics/incidents/"):
            parts=path.split("/api/ics/incidents/")[1].split("/")
            inc_id=parts[0]; sub="/".join(parts[1:]) if len(parts)>1 else ""
            row=c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()

            if sub in ("","update"):
                if not row: return self.send_json({"error":"Not found"},404)
                allowed=["name","type","status","jurisdiction","incident_commander",
                         "location","summary"]
                sets=[]; vals=[]
                for k in allowed:
                    if k in body: sets.append(f"{k}=?"); vals.append(body[k])
                if sets:
                    vals+=[now,inc_id]
                    c.execute(f"UPDATE incidents SET {','.join(sets)},updated=? WHERE id=?",vals)
                    c.commit()
                log_activity(inc_id,"Command","Incident Updated","")
                return self.send_json({"ok":True})

            elif sub == "advance_period":
                if not row: return self.send_json({"error":"Not found"},404)
                new_period=row["current_period"]+1
                c.execute("UPDATE incidents SET current_period=?,updated=? WHERE id=?",
                          (new_period,now,inc_id))
                c.execute("INSERT INTO ics_periods(id,incident_id,period_num,started,objectives) VALUES(?,?,?,?,?)",
                          (f"per-{inc_id}-{new_period}",inc_id,new_period,now,
                           body.get("objectives","")))
                c.commit()
                log_activity(inc_id,"Command","Period Advanced",f"Period {new_period}")
                return self.send_json({"ok":True,"period":new_period})

            elif sub == "close":
                if not row: return self.send_json({"error":"Not found"},404)
                c.execute("UPDATE incidents SET status='closed',closed=?,updated=? WHERE id=?",
                          (now,now,inc_id)); c.commit()
                log_activity(inc_id,"Command","Incident Closed","")
                return self.send_json({"ok":True})

            elif sub == "command":
                # Save command section data (objectives, safety message, weather)
                fid = f"command-{inc_id}"
                c.execute("""INSERT OR REPLACE INTO ics_forms
                    (id,incident_id,form_type,period,summary,data,created,updated)
                    VALUES(?,?,?,?,?,?,COALESCE((SELECT created FROM ics_forms WHERE id=?),?),?)""",
                    (fid,inc_id,"command",body.get("period",1),"Command Section",jdump(body),fid,now,now))
                c.commit()
                log_activity(inc_id,"Command","Command Section Saved","")
                return self.send_json({"ok":True})

        elif path.startswith("/api/ics/forms/"):
            form_type=path.split("/api/ics/forms/")[1].split("/")[0]
            fid=body.get("id") or f"{form_type}-{int(time.time()*1000)}"
            body.update({"id":fid,"form_type":form_type,"updated":now})
            body.setdefault("created",now)
            c.execute("""INSERT OR REPLACE INTO ics_forms
                (id,incident_id,form_type,period,summary,data,created,updated)
                VALUES(?,?,?,?,?,?,?,?)""",
                (fid,body.get("incident_id",""),form_type,body.get("period",1),
                 body.get("summary",""),jdump(body),body.get("created",now),now))
            c.commit()
            log_activity(body.get("incident_id",""),form_type.upper(),"Form Saved",fid)
            return self.send_json({"ok":True,"id":fid})

        elif path == "/api/ics/tcards":
            cid=body.get("id") or f"tc-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_tcards
                (id,incident_id,resource_id,resource_name,resource_type,category,type,
                 status,assignment,leader,contact,num_personnel,eta,notes,
                 order_number,home_agency,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cid,body.get("incident_id",""),body.get("resource_id",""),
                 body.get("resource_name",""),body.get("resource_type",""),
                 body.get("category",""),body.get("type",""),
                 body.get("status","Available"),body.get("assignment",""),
                 body.get("leader",""),body.get("contact",""),
                 body.get("num_personnel",0),body.get("eta",""),
                 body.get("notes",""),body.get("order_number",""),
                 body.get("home_agency",""),body.get("created",now),now))
            c.commit()
            log_activity(body.get("incident_id",""),"Resources","T-Card Updated",
                         body.get("resource_name",""))
            return self.send_json({"ok":True,"card":row_to_dict(
                c.execute("SELECT * FROM ics_tcards WHERE id=?",(cid,)).fetchone())})

        elif path == "/api/ics/resources":
            rid=body.get("id") or f"icsres-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_resources
                (id,incident_id,resource_id,name,type,capability,
                 status,assignment,contact,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (rid,body.get("incident_id",""),body.get("resource_id",""),
                 body.get("name",""),body.get("type",""),body.get("capability",""),
                 body.get("status","Available"),body.get("assignment",""),
                 body.get("contact",""),body.get("created",now),now))
            c.commit()
            return self.send_json({"ok":True,"resource":row_to_dict(
                c.execute("SELECT * FROM ics_resources WHERE id=?",(rid,)).fetchone())})

        elif path == "/api/ics/meetings":
            mid=body.get("id") or f"meet-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_meetings
                (id,incident_id,period,meeting_type,title,scheduled_time,
                 location,chair,attendees,agenda_items,status,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,COALESCE(
                    (SELECT created FROM ics_meetings WHERE id=?),?),?)""",
                (mid,
                 body.get("incident_id",""),
                 body.get("period",1),
                 body.get("meeting_type","other"),
                 body.get("title",""),
                 body.get("scheduled_time",""),
                 body.get("location",""),
                 body.get("chair",""),
                 jdump(body.get("attendees",[])),
                 jdump(body.get("agenda_items",[])),
                 body.get("status","scheduled"),
                 body.get("notes",""),
                 mid,now,now))
            c.commit()
            log_activity(body.get("incident_id",""),"Planning",
                         "Meeting Scheduled",body.get("title",""))
            return self.send_json({"ok":True,"id":mid})

        elif path.startswith("/api/ics/meetings/"):
            mid=path.split("/api/ics/meetings/")[1]
            allowed=["title","scheduled_time","location","chair","attendees",
                     "agenda_items","status","notes","period"]
            sets=[]; vals=[]
            for k in allowed:
                if k in body:
                    sets.append(f"{k}=?")
                    vals.append(jdump(body[k]) if isinstance(body[k],list) else body[k])
            if sets:
                vals+=[now,mid]
                c.execute(f"UPDATE ics_meetings SET {','.join(sets)},updated=? WHERE id=?",vals)
                c.commit()
            log_activity("","Planning","Meeting Updated",mid)
            return self.send_json({"ok":True})

        else:
            self.send_json({"error":"Not found"},404)

    def do_DELETE(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/"); c=get_conn()
        if path.startswith("/api/ics/tcards/"):
            c.execute("DELETE FROM ics_tcards WHERE id=?",(path.split("/api/ics/tcards/")[1],))
        elif path.startswith("/api/ics/resources/"):
            c.execute("DELETE FROM ics_resources WHERE id=?",(path.split("/api/ics/resources/")[1],))
        elif path.startswith("/api/ics/meetings/"):
            c.execute("DELETE FROM ics_meetings WHERE id=?",(path.split("/api/ics/meetings/")[1],))
        elif path.startswith("/api/ics/incidents/"):
            inc_id=path.split("/api/ics/incidents/")[1]
            c.execute("DELETE FROM incidents WHERE id=?",(inc_id,))
        elif path.startswith("/api/ics/templates/"):
            tid = path.split("/api/ics/templates/")[1]
            c.execute("UPDATE incident_templates SET enabled=0 WHERE id=?", (tid,))
            c.commit()
            return self.send_json({"ok":True})

        elif path.startswith("/api/ics/fema/labor/"):
            c.execute("DELETE FROM fema_labor WHERE id=?",
                      (path.split("/api/ics/fema/labor/")[1],))
        elif path.startswith("/api/ics/fema/equipment/"):
            c.execute("DELETE FROM fema_equipment WHERE id=?",
                      (path.split("/api/ics/fema/equipment/")[1],))
        elif path.startswith("/api/ics/fema/materials/"):
            c.execute("DELETE FROM fema_materials WHERE id=?",
                      (path.split("/api/ics/fema/materials/")[1],))
        else:
            return self.send_json({"error":"Not found"},404)
        c.commit(); return self.send_json({"ok":True})


if __name__ == "__main__":
    db.startup()
    log.info("ICS Platform API on port 5055")
    HTTPServer(("0.0.0.0", 5055), ICSHandler).serve_forever()import json
import sys, os as _os
sys.path.insert(0, _os.path.dirname(__file__))
try:
    from iap_pdf import compile_iap, IAP_FORM_ORDER
    HAS_PDF = True
except Exception as _pdf_err:
    HAS_PDF = False
    _pdf_err_msg = str(_pdf_err)
    IAP_FORM_ORDER = []
nse-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""FieldCommand ICS Platform API — Port 5055 (SQLite via db.py)"""

import json, time, sys, logging
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

import db
from db import get_conn, utcnow, jdump, jload, rows_to_list, row_to_dict

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s [ics-platform] %(message)s',
    handlers=[logging.StreamHandler(sys.stdout),
              logging.FileHandler('/var/log/fieldcommand-ics.log', mode='a')])
log = logging.getLogger('ics-platform')


def log_activity(incident_id, section, action, detail):
    get_conn().execute(
        "INSERT INTO activity_log(incident_id,section,action,detail,timestamp)"
        " VALUES(?,?,?,?,?)",
        (incident_id, section, action, detail, utcnow()))
    get_conn().commit()


def _rr_text(elem, tag):
    """Extract text from first matching XML child element."""
    import xml.etree.ElementTree as ET
    found = elem.find(".//" + tag)
    return (found.text or "").strip() if found is not None else ""

def _rr_mode(rr_mode_str):
    """Map RadioReference mode string to our standard."""
    m = (rr_mode_str or "").upper()
    if "P25" in m or "APCO" in m: return "P25"
    if "DMR"  in m:               return "DMR"
    if "NXDN" in m:               return "NXDN"
    if "DSTAR" in m or "D-STAR" in m: return "D-STAR"
    if "NFM"  in m:               return "NFM"
    if "FM"   in m:               return "FM"
    if "AM"   in m:               return "AM"
    return "FM"  # safe default

def _rr_tag_to_function(tag):
    """Map RadioReference tag to our function categories."""
    if not tag: return "Tactical"
    t = tag.lower()
    if "fire"    in t: return "Tactical"
    if "ems"     in t or "medical" in t: return "Medical"
    if "law"     in t or "police"  in t or "sheriff" in t: return "Command"
    if "interop" in t: return "Interop"
    if "command" in t: return "Command"
    if "dispatch" in t: return "Command"
    if "data"    in t: return "Data"
    if "air"     in t: return "Air"
    return "Tactical"


class ICSHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args): pass

    def cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
        self.send_header("Access-Control-Allow-Methods","GET,POST,PUT,DELETE,OPTIONS")

    def send_json(self, obj, code=200):
        body=json.dumps(obj,default=str).encode()
        self.send_response(code)
        self.send_header("Content-Type","application/json")
        self.send_header("Content-Length",len(body))
        self.cors(); self.end_headers(); self.wfile.write(body)

    def read_body(self):
        n=int(self.headers.get("Content-Length",0))
        return json.loads(self.rfile.read(n)) if n else {}

    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()

    def do_GET(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/")
        qs=parse_qs(parsed.query); c=get_conn()

        if path == "/api/ics/incidents":
            return self.send_json(rows_to_list(
                c.execute("SELECT * FROM incidents ORDER BY started DESC").fetchall()))

        elif path.startswith("/api/ics/incidents/"):
            inc_id=path.split("/api/ics/incidents/")[1].split("/")[0]
            sub=path[len(f"/api/ics/incidents/{inc_id}"):]
            row=c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()
            if not row: return self.send_json({"error":"Not found"},404)
            if sub in ("","/"): return self.send_json(row_to_dict(row))
            elif sub=="/periods":
                return self.send_json(rows_to_list(c.execute(
                    "SELECT * FROM ics_periods WHERE incident_id=? ORDER BY period_num",(inc_id,)).fetchall()))
            elif sub=="/stats":
                obj_count  = c.execute("SELECT COUNT(*) FROM ics_periods WHERE incident_id=?",(inc_id,)).fetchone()[0]
                res_count  = c.execute("SELECT COUNT(*) FROM ics_resources WHERE incident_id=?",(inc_id,)).fetchone()[0]
                form_count = c.execute("SELECT COUNT(*) FROM ics_forms WHERE incident_id=?",(inc_id,)).fetchone()[0]
                inc_d = row_to_dict(row)
                return self.send_json({"objectives":obj_count,"current_period":inc_d.get("current_period",1),"resources":res_count,"forms":form_count})
            elif sub=="/planningp":
                inc_d = row_to_dict(row)
                periods = rows_to_list(c.execute(
                    "SELECT * FROM ics_periods WHERE incident_id=? ORDER BY period_num",(inc_id,)).fetchall())
                resources = rows_to_list(c.execute(
                    "SELECT callsign,name,role,status FROM ics_resources WHERE incident_id=?",(inc_id,)).fetchall())
                return self.send_json({"incident":inc_d,"periods":periods,"resources":resources})
            return self.send_json({"error":"Not found"},404)

        elif path.startswith("/api/ics/forms/"):
            parts=path.split("/api/ics/forms/")[1].split("/")
            form_type=parts[0]
            if len(parts)==1:
                inc_id=qs.get("incident_id",[None])[0]
                if inc_id:
                    rows=c.execute(
                        "SELECT id,incident_id,form_type,period,summary,created,updated"
                        " FROM ics_forms WHERE form_type=? AND incident_id=? ORDER BY created DESC",
                        (form_type,inc_id)).fetchall()
                else:
                    rows=c.execute(
                        "SELECT id,incident_id,form_type,period,summary,created,updated"
                        " FROM ics_forms WHERE form_type=? ORDER BY created DESC",
                        (form_type,)).fetchall()
                return self.send_json(rows_to_list(rows))
            else:
                fid=parts[1]
                row=c.execute("SELECT * FROM ics_forms WHERE id=?",(fid,)).fetchone()
                if row:
                    d=dict(row); d.update(jload(d.get("data"),{}))
                    return self.send_json(d)
                return self.send_json({"error":"Not found"},404)

        elif path == "/api/ics/tcards":
            inc_id=qs.get("incident_id",[None])[0]
            if inc_id:
                rows=c.execute("SELECT * FROM ics_tcards WHERE incident_id=? ORDER BY status,resource_name",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_tcards ORDER BY status,resource_name").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path.startswith("/api/ics/tcards/"):
            card_id=path.split("/api/ics/tcards/")[1]
            row=c.execute("SELECT * FROM ics_tcards WHERE id=?",(card_id,)).fetchone()
            return self.send_json(row_to_dict(row)) if row else self.send_json({"error":"Not found"},404)

        elif path == "/api/ics/resources":
            inc_id=qs.get("incident_id",[None])[0]
            if inc_id:
                rows=c.execute("SELECT * FROM ics_resources WHERE incident_id=? ORDER BY name",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_resources ORDER BY name").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/activity":
            inc_id=qs.get("incident_id",[None])[0]
            limit=int(qs.get("limit",[50])[0])
            if inc_id:
                rows=c.execute("SELECT * FROM activity_log WHERE incident_id=? ORDER BY timestamp DESC LIMIT ?",(inc_id,limit)).fetchall()
            else:
                rows=c.execute("SELECT * FROM activity_log ORDER BY timestamp DESC LIMIT ?",(limit,)).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/status":
            incs=c.execute("SELECT COUNT(*) FROM incidents").fetchone()[0]
            active=c.execute("SELECT COUNT(*) FROM incidents WHERE status='active'").fetchone()[0]
            return self.send_json({"service":"ics-platform","version":"2.0.0",
                "utc":utcnow(),"incidents":incs,"active":active,"db":str(db.DB_PATH)})

        elif path == "/api/ics/assignments":
            inc_id=qs.get("incident_id",[None])[0]
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            rows=c.execute("""
                SELECT e.callsign,e.name,e.ics_position,e.ema_id,
                       e.timestamp,e.checkout_time,n.name as net_name
                FROM net_entries e
                JOIN nets n ON e.net_id=n.id
                WHERE e.incident_id=? AND e.ics_position!=''
                ORDER BY e.timestamp
            """,(inc_id,)).fetchall()
            roster_rows=c.execute("""
                SELECT callsign,radio_id,
                       first_name||' '||last_name as name,
                       role,member_id
                FROM roster WHERE role!='' AND role!='Operator'
                ORDER BY role
            """).fetchall()
            return self.send_json({
                "assignments":rows_to_list(rows),
                "roster_roles":rows_to_list(roster_rows)
            })

        elif path == "/api/ics/meetings":
            inc_id=qs.get("incident_id",[None])[0]
            period=qs.get("period",[None])[0]
            if inc_id and period:
                rows=c.execute("SELECT * FROM ics_meetings WHERE incident_id=? AND period=? ORDER BY scheduled_time",(inc_id,int(period))).fetchall()
            elif inc_id:
                rows=c.execute("SELECT * FROM ics_meetings WHERE incident_id=? ORDER BY scheduled_time",(inc_id,)).fetchall()
            else:
                rows=c.execute("SELECT * FROM ics_meetings ORDER BY scheduled_time DESC LIMIT 50").fetchall()
            return self.send_json(rows_to_list(rows))

        elif path.startswith("/api/ics/meetings/"):
            mid=path.split("/api/ics/meetings/")[1]
            row=c.execute("SELECT * FROM ics_meetings WHERE id=?",(mid,)).fetchone()
            if not row: return self.send_json({"error":"Not found"},404)
            return self.send_json(row_to_dict(row))


        # ── Resource History ────────────────────────────────────────────────
        elif path == "/api/ics/resource_history":
            inc_id = qs.get("incident_id",[""])[0]
            res_id = qs.get("resource_id",[""])[0]
            if inc_id:
                rows = c.execute(
                    "SELECT * FROM resource_history WHERE incident_id=? ORDER BY created DESC",
                    (inc_id,)).fetchall()
            elif res_id:
                rows = c.execute(
                    "SELECT * FROM resource_history WHERE resource_id=? ORDER BY created DESC",
                    (res_id,)).fetchall()
            else:
                rows = []
            return self.send_json(rows_to_list(rows))

        # ── Channel Library ─────────────────────────────────────────────────
        elif path == "/api/ics/channel_library":
            q = qs.get("q",[""])[0].lower()
            if q:
                rows = c.execute(
                    "SELECT * FROM channel_library WHERE active=1 AND "
                    "(LOWER(name) LIKE ? OR LOWER(alpha_tag) LIKE ? OR rx_freq LIKE ?) "
                    "ORDER BY name LIMIT 50",
                    (f"%{q}%", f"%{q}%", f"%{q}%")).fetchall()
            else:
                rows = c.execute(
                    "SELECT * FROM channel_library WHERE active=1 ORDER BY name"
                ).fetchall()
            return self.send_json(rows_to_list(rows))


        # ── Active Channels — unified comms lookup ──────────────────────────
        # Returns merged channel list: ICS-205 for incident + channel_library
        # Used by net loggers, tactical map, cheat sheets for channel picker
        elif path == "/api/ics/active_channels":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            channels = []

            # 1. Pull from ICS-205 saved form for this incident/period
            if inc_id:
                row = c.execute(
                    "SELECT data FROM ics_forms "
                    "WHERE form_type=? AND incident_id=? AND period=? "
                    "ORDER BY updated DESC LIMIT 1",
                    ("ics205", inc_id, period)).fetchone()
                if row:
                    try:
                        import json as _json
                        fd = _json.loads(row[0] or "{}")
                        for i in range(30):
                            name = fd.get(f"ch205_name_{i}","").strip()
                            rx   = fd.get(f"ch205_rx_{i}","").strip()
                            if not name and not rx:
                                if i > 15: break
                                continue
                            channels.append({
                                "id":        f"205-{inc_id}-{i}",
                                "name":      name or rx,
                                "alpha_tag": fd.get(f"ch205_zone_{i}",""),
                                "rx_freq":   rx,
                                "tx_freq":   fd.get(f"ch205_tx_{i}","") or rx,
                                "pl_tone":   fd.get(f"ch205_pl_{i}",""),
                                "mode":      fd.get(f"ch205_mode_{i}","FM"),
                                "function":  fd.get(f"ch205_assign_{i}","Tactical"),
                                "division":  fd.get(f"ch205_division_{i}",""),
                                "notes":     fd.get(f"ch205_notes_{i}",""),
                                "source":    "ICS-205",
                                "incident_id": inc_id,
                                "period":    period,
                            })
                    except Exception:
                        pass

            # 2. Append channel_library entries (skip duplicates by freq)
            existing_freqs = {ch["rx_freq"] for ch in channels}
            lib_rows = c.execute(
                "SELECT * FROM channel_library WHERE active=1 ORDER BY name"
            ).fetchall()
            for lr in lib_rows:
                d = row_to_dict(lr)
                if d.get("rx_freq") not in existing_freqs:
                    d["source"] = "Library"
                    channels.append(d)

            # 3. Also pull active repeaters tagged ARES/RACES
            rep_rows = c.execute(
                "SELECT * FROM repeaters WHERE active=1 AND (ares=1 OR races=1) "
                "ORDER BY callsign LIMIT 50"
            ).fetchall()
            existing_freqs = {ch["rx_freq"] for ch in channels}
            for rr in rep_rows:
                d = row_to_dict(rr)
                freq = d.get("output_freq","")
                if freq and freq not in existing_freqs:
                    channels.append({
                        "id":        f"rep-{d.get('id','')}",
                        "name":      f"{d.get('callsign','')} Repeater",
                        "alpha_tag": d.get("callsign",""),
                        "rx_freq":   freq,
                        "tx_freq":   d.get("input_freq","") or freq,
                        "pl_tone":   d.get("tone",""),
                        "mode":      d.get("mode","FM"),
                        "function":  "Amateur" if not d.get("races") else "Interop",
                        "division":  "",
                        "notes":     d.get("city","") + " " + d.get("state",""),
                        "source":    "Repeater DB",
                    })

            return self.send_json({
                "channels": channels,
                "count":    len(channels),
                "incident_id": inc_id,
                "period":   period,
            })




        # ── WAN Configuration GET/POST ────────────────────────────────────────
        elif path == "/api/ics/wan_config":
            import json as _json
            cfg_path = Path("/opt/fieldcommand/data/wan_config.json")
            defaults_path = Path(__file__).parent / "wan_config_defaults.json"
            for p in [cfg_path, defaults_path]:
                if p.exists():
                    try:
                        return self.send_json(_json.loads(p.read_text()))
                    except Exception:
                        pass
            return self.send_json({})


        # ── IAP PDF Compile ─────────────────────────────────────────────────
        # GET  /api/ics/iap_status?incident_id=X&period=N
        #      Returns which forms are saved for this incident/period
        # POST /api/ics/iap_compile
        #      Compiles all saved forms into a single PDF download
        elif path == "/api/ics/iap_status":
            inc_id  = qs.get("incident_id",[""])[0]
            period  = int(qs.get("period",["1"])[0])
            rows    = rows_to_list(c.execute(
                "SELECT form_type, id, updated FROM ics_forms "
                "WHERE incident_id=? AND period=? ORDER BY form_type",
                (inc_id, period)
            ).fetchall())
            # Group by form_type
            by_type = {}
            for r in rows:
                by_type.setdefault(r["form_type"],[]).append(r)
            return self.send_json({
                "incident_id": inc_id,
                "period":      period,
                "forms":       by_type,
                "form_count":  len(rows),
                "pdf_available": HAS_PDF,
                "iap_order":   [ft for ft,_ in IAP_FORM_ORDER] if HAS_PDF else [],
            })

        # ── Incident Archive / Restore / Delete ─────────────────────────────
        # GET  /api/ics/incidents/archived     → list archived incidents on Pi
        # GET  /api/ics/incidents/lacie        → list archives on USB backup drive USB
        # POST /api/ics/incidents/archive      → archive incident to USB backup drive + mark Pi DB
        # POST /api/ics/incidents/restore      → restore from USB backup drive back to Pi DB
        # POST /api/ics/incidents/delete       → hard-delete incident from Pi DB
        # POST /api/ics/reset                  → beta reset: wipe all scenario data

        elif path == "/api/ics/incidents/archived":
            rows = c.execute(
                "SELECT * FROM incidents WHERE archived=1 ORDER BY archived_at DESC"
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/incidents/lacie":
            # List incident archives on the USB backup drive drive
            import os, json as _json
            lacie_base = "/media/fieldcommand/backup/incidents"
            archives = []
            if os.path.isdir(lacie_base):
                for folder in sorted(os.listdir(lacie_base), reverse=True):
                    folder_path = os.path.join(lacie_base, folder)
                    meta_path   = os.path.join(folder_path, "incident_meta.json")
                    if os.path.isfile(meta_path):
                        try:
                            with open(meta_path) as f:
                                meta = _json.load(f)
                            meta["folder"] = folder
                            meta["path"]   = folder_path
                            archives.append(meta)
                        except Exception:
                            archives.append({"folder":folder,"path":folder_path,"name":folder})
            return self.send_json({
                "lacie_mounted": os.path.isdir(lacie_base),
                "archives":      archives,
                "lacie_path":    lacie_base,
            })

        # ── ICS-211 Remote Check-In ─────────────────────────────────────────
        # GET: fetch pending entries for an incident/period




        # ── Incident Templates API ──────────────────────────────────────────
        # GET  /api/ics/templates              → list all enabled templates
        # GET  /api/ics/templates/<id>         → get single template
        # POST /api/ics/templates              → create or update template
        # POST /api/ics/templates/import       → import JSON array of templates
        # DELETE via do_DELETE /api/ics/templates/<id>

        elif path == "/api/ics/templates":
            rows = rows_to_list(
                c.execute("SELECT * FROM incident_templates WHERE enabled=1 ORDER BY sort_order,name").fetchall()
            )
            for r in rows:
                try: r["data"] = json.loads(r.get("data","{}"))
                except Exception: r["data"] = {}
            return self.send_json(rows)

        elif path.startswith("/api/ics/templates/") and path != "/api/ics/templates/import":
            tid = path.split("/api/ics/templates/")[1]
            row = c.execute("SELECT * FROM incident_templates WHERE id=?", (tid,)).fetchone()
            if not row:
                return self.send_json({"error":"Not found"},404)
            r = dict(row)
            try: r["data"] = json.loads(r.get("data","{}"))
            except Exception: r["data"] = {}
            return self.send_json(r)

        # ── FEMA Equipment Rates API ─────────────────────────────────────────
        elif path == "/api/ics/fema/rates":
            import datetime as _dt
            category = qs.get("category",[""])[0]
            q        = qs.get("q",[""])[0].lower()
            sql      = "SELECT * FROM fema_equipment_rates WHERE active=1"
            params   = []
            if category:
                sql += " AND category=?"; params.append(category)
            rows = rows_to_list(c.execute(sql + " ORDER BY category,description", params).fetchall())
            if q:
                rows = [r for r in rows if q in r.get("description","").lower()
                        or q in r.get("code","").lower() or q in r.get("category","").lower()]

            # Compute reminder: how old are the rates?
            max_year = max((r.get("rate_year",0) for r in rows), default=0)
            current_year = _dt.datetime.utcnow().year
            years_old    = current_year - max_year if max_year else None
            reminder     = None
            if years_old and years_old >= 1:
                reminder = (
                    f"Your FEMA equipment rates are from {max_year} — now {years_old} year(s) old. "
                    f"FEMA typically updates rates annually. Check "
                    f"fema.gov/assistance/public/tools-resources/schedule-equipment-rates "
                    f"and update if a newer schedule applies to your incident."
                )

            categories = sorted(set(r.get("category","") for r in rows))
            return self.send_json({
                "rates":       rows,
                "categories":  categories,
                "rate_year":   max_year,
                "years_old":   years_old,
                "reminder":    reminder,
                "source":      "FEMA Schedule of Equipment Rates",
                "source_url":  "https://www.fema.gov/assistance/public/tools-resources/schedule-equipment-rates",
            })


        # ── Resource GPS Update ─────────────────────────────────────────────
        # GET  /api/ics/resources/gps?incident_id=X  → all resource positions
        # POST /api/ics/resources/gps                → update position for one resource
        elif path == "/api/ics/resources/gps":
            inc_id = qs.get("incident_id",[""])[0]
            rows = rows_to_list(c.execute(
                """SELECT id, resource_name, resource_type, status, assignment,
                          lat, lon, gps_updated, gps_source, location_label,
                          num_personnel, leader, category
                   FROM ics_tcards
                   WHERE incident_id=? AND lat IS NOT NULL AND lon IS NOT NULL
                   ORDER BY resource_type, resource_name""",
                (inc_id,)
            ).fetchall())
            return self.send_json(rows)

        # ── Cost Dashboard API ──────────────────────────────────────────────
        # GET /api/ics/cost_summary?incident_id=X
        # Returns aggregated cost by category + burn rate
        elif path == "/api/ics/cost_summary":
            inc_id = qs.get("incident_id",[""])[0]
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)

            # Pull FEMA entered costs
            labor_rows  = rows_to_list(c.execute(
                "SELECT * FROM fema_labor WHERE incident_id=?", (inc_id,)).fetchall())
            equip_rows  = rows_to_list(c.execute(
                "SELECT * FROM fema_equipment WHERE incident_id=?", (inc_id,)).fetchall())
            mat_rows    = rows_to_list(c.execute(
                "SELECT * FROM fema_materials WHERE incident_id=?", (inc_id,)).fetchall())

            # Labor cost
            def labor_cost(r):
                base = (r.get("hours_reg",0) or 0)*(r.get("rate_reg",0) or 0) +                        (r.get("hours_ot",0) or 0)*(r.get("rate_ot",0) or 0)
                return base * (1 + (r.get("fringe_pct",0) or 0)/100)

            total_labor  = sum(labor_cost(r) for r in labor_rows)
            total_equip  = sum((r.get("hours_used",0) or 0)*(r.get("rate_hr",0) or 0)
                               for r in equip_rows)
            total_mat    = sum(r.get("total_cost",0) or 0 for r in mat_rows)
            total_fema   = total_labor + total_equip + total_mat

            # T-card resource counts by category
            tcards = rows_to_list(c.execute(
                "SELECT * FROM ics_tcards WHERE incident_id=?", (inc_id,)).fetchall())

            by_type = {}
            for t in tcards:
                rtype = t.get("resource_type") or t.get("category") or "Unknown"
                by_type.setdefault(rtype, {"count":0, "personnel":0, "daily_cost":0})
                by_type[rtype]["count"] += 1
                by_type[rtype]["personnel"] += t.get("num_personnel",0) or 0
                by_type[rtype]["daily_cost"] += t.get("daily_cost",0) or 0

            # Pull incident start time for elapsed time calculation
            inc_row = c.execute("SELECT started, current_period FROM incidents WHERE id=?",
                                (inc_id,)).fetchone()
            started = inc_row["started"] if inc_row else None
            current_period = inc_row["current_period"] if inc_row else 1

            import datetime
            elapsed_hours = None
            if started:
                try:
                    start_dt = datetime.datetime.fromisoformat(started.replace("Z",""))
                    elapsed  = datetime.datetime.utcnow() - start_dt
                    elapsed_hours = round(elapsed.total_seconds() / 3600, 1)
                except Exception:
                    pass

            # Burn rate: total costs / elapsed hours
            burn_per_hour = round(total_fema / elapsed_hours, 2)                 if elapsed_hours and elapsed_hours > 0 else None

            return self.send_json({
                "incident_id":    inc_id,
                "elapsed_hours":  elapsed_hours,
                "current_period": current_period,
                "totals": {
                    "labor":       round(total_labor, 2),
                    "equipment":   round(total_equip, 2),
                    "materials":   round(total_mat,   2),
                    "total":       round(total_fema,  2),
                },
                "burn_rate": {
                    "per_hour": burn_per_hour,
                    "per_day":  round(burn_per_hour * 24, 2) if burn_per_hour else None,
                    "per_period": round(burn_per_hour * 12, 2) if burn_per_hour else None,
                },
                "resources_by_type": by_type,
                "counts": {
                    "labor_entries":    len(labor_rows),
                    "equipment_entries":len(equip_rows),
                    "material_entries": len(mat_rows),
                    "tcards":           len(tcards),
                    "total_personnel":  sum(t.get("num_personnel",0) or 0 for t in tcards),
                },
            })

        # ── FEMA PA Cost Tracking API ────────────────────────────────────────
        elif path == "/api/ics/fema/labor":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_labor WHERE incident_id=? ORDER BY date_worked,employee",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/fema/equipment":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_equipment WHERE incident_id=? ORDER BY date_used,equipment",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/fema/materials":
            inc_id = qs.get("incident_id",[""])[0]
            rows = c.execute(
                "SELECT * FROM fema_materials WHERE incident_id=? ORDER BY date_purch,description",
                (inc_id,)
            ).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/checkin":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            synced = qs.get("synced",[""])[0]
            sql    = "SELECT * FROM checkin_entries WHERE incident_id=? AND period=?"
            params = [inc_id, period]
            if synced == "0":
                sql    += " AND synced_to_211=0"
            rows = c.execute(sql + " ORDER BY created DESC", params).fetchall()
            return self.send_json(rows_to_list(rows))

        elif path == "/api/ics/general_info":
            inc_id = qs.get("incident_id",[""])[0]
            period = int(qs.get("period",["1"])[0])
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            row = c.execute(
                "SELECT * FROM general_info WHERE incident_id=? AND period=?",
                (inc_id, period)).fetchone()
            if row:
                return self.send_json(row_to_dict(row))
            inc = c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()
            if inc:
                d = row_to_dict(inc)
                d["incident_location"] = d.get("location","")
                d["operational_period_number"] = period
                return self.send_json(d)
            return self.send_json({})


        # ── Resource History POST ───────────────────────────────────────────
        elif path == "/api/ics/resource_history":
            entries = body.get("entries", [])
            for e in entries:
                rh_id = f"rh-{int(time.time()*1000)}-{e.get('resource_id','')}"
                c.execute("""INSERT OR IGNORE INTO resource_history
                    (id, incident_id, period, resource_id, resource_name,
                     resource_type, assignment, date, created)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                    (rh_id, e.get("incident_id",""), e.get("period",1),
                     e.get("resource_id",""), e.get("resource_name",""),
                     e.get("resource_type",""), e.get("assignment",""),
                     e.get("date",""), now))
            c.commit()
            return self.send_json({"status":"ok","count":len(entries)})

        # ── Channel Library POST ─────────────────────────────────────────────
        elif path == "/api/ics/channel_library":
            ch_id = body.get("id") or f"ch-{int(time.time()*1000)}"
            existing = c.execute("SELECT id FROM channel_library WHERE id=?",(ch_id,)).fetchone()
            fields = ["name","alpha_tag","rx_freq","tx_freq","pl_tone","mode",
                      "function","division","notes","custom","active"]
            if existing:
                sets = ", ".join(f"{f}=?" for f in fields)
                vals = [body.get(f,"") for f in fields] + [ch_id]
                c.execute(f"UPDATE channel_library SET {sets} WHERE id=?", vals)
            else:
                cols = "id, " + ", ".join(fields) + ", created"
                phs  = ", ".join(["?"]*(len(fields)+2))
                vals = [ch_id] + [body.get(f,"") for f in fields] + [now]
                c.execute(f"INSERT INTO channel_library ({cols}) VALUES ({phs})", vals)
            c.commit()
            return self.send_json({"status":"ok","id":ch_id})


        # ── RadioReference SOAP Proxy ───────────────────────────────────────
        # Proxies requests to the RadioReference SOAP API on behalf of the
        # client — avoids CORS issues and keeps credentials server-side per session.
        # User supplies their own RR username/password (premium subscription required).
        # We never store credentials — they are passed per-request only.
        elif path == "/api/ics/rr_search":
            import urllib.request
            rr_username = body.get("username","")
            rr_password = body.get("password","")
            rr_appkey   = body.get("appkey","")
            search_type = body.get("type","county")   # county | zip | agency
            search_val  = body.get("value","")        # countyId, ZIP, agencyId
            tag_filter  = body.get("tag","")          # optional tag (Fire, EMS, Law, etc.)

            if not all([rr_username, rr_password, search_val]):
                return self.send_json({"error":"username, password, and value are required"},400)

            # Build SOAP envelope based on search type
            if search_type == "zip":
                method   = "getZipCodeInfo"
                body_xml = f"<cid>{search_val}</cid>"
            elif search_type == "county_freqs" and tag_filter:
                method   = "getCountyFreqsByTag"
                body_xml = f"<cid>{search_val}</cid><tagId>{tag_filter}</tagId>"
            elif search_type == "county_freqs":
                method   = "getCountyInfo"
                body_xml = f"<cid>{search_val}</cid>"
            elif search_type == "agency":
                method   = "getAgencyInfo"
                body_xml = f"<aid>{search_val}</aid>"
            else:
                return self.send_json({"error":f"unknown search type: {search_type}"},400)

            soap_env = f"""<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:ns1="http://api.radioreference.com/soap2">
  <SOAP-ENV:Body>
    <ns1:{method}>
      <authInfo>
        <appKey>{rr_appkey or "FieldCommandIMS"}</appKey>
        <username>{rr_username}</username>
        <password>{rr_password}</password>
        <version>latest</version>
        <style>rpc</style>
      </authInfo>
      {body_xml}
    </ns1:{method}>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

            try:
                req = urllib.request.Request(
                    "https://api.radioreference.com/soap2/",
                    data=soap_env.encode("utf-8"),
                    headers={
                        "Content-Type": "text/xml; charset=utf-8",
                        "SOAPAction": f"http://api.radioreference.com/soap2/#{method}",
                    },
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    xml_resp = resp.read().decode("utf-8")

                # Parse the SOAP XML response into something useful
                import xml.etree.ElementTree as ET
                root = ET.fromstring(xml_resp)
                ns   = {"s": "http://schemas.xmlsoap.org/soap/envelope/"}

                # Check for SOAP fault
                fault = root.find(".//faultstring")
                if fault is not None:
                    return self.send_json({"error": fault.text or "SOAP fault"}, 400)

                # Extract frequencies from getCountyInfo / getCountyFreqsByTag
                channels = []
                # Conventional frequencies
                for freq in root.iter("freqs"):
                    output   = _rr_text(freq, "output")
                    input_f  = _rr_text(freq, "input")
                    pl_tone  = _rr_text(freq, "pl")
                    desc     = _rr_text(freq, "descr")
                    alpha    = _rr_text(freq, "alpha")
                    mode     = _rr_text(freq, "mode") or "FM"
                    tag_name = _rr_text(freq, "tag")
                    if output:
                        channels.append({
                            "name":      desc or alpha or output,
                            "alpha_tag": alpha or "",
                            "rx_freq":   output,
                            "tx_freq":   input_f or output,
                            "pl_tone":   pl_tone or "",
                            "mode":      _rr_mode(mode),
                            "function":  _rr_tag_to_function(tag_name),
                            "notes":     tag_name or "",
                            "source":    "RadioReference",
                        })

                # For zip lookup — return county/state info
                if search_type == "zip":
                    result = {
                        "county_id": _rr_text(root, "cid"),
                        "state_id":  _rr_text(root, "stid"),
                        "city":      _rr_text(root, "ctName"),
                        "lat":       _rr_text(root, "lat"),
                        "lon":       _rr_text(root, "lon"),
                    }
                    return self.send_json(result)

                return self.send_json({
                    "channels": channels,
                    "count":    len(channels),
                    "source":   "RadioReference SOAP API",
                })

            except Exception as e:
                return self.send_json({"error": str(e)}, 503)


        # ── ICS-211 Remote Check-In POST ────────────────────────────────────



        # ── WAN Configuration POST ───────────────────────────────────────────
        elif path == "/api/ics/wan_config":
            import json as _json
            cfg_path = Path("/opt/fieldcommand/data/wan_config.json")
            try:
                cfg_path.parent.mkdir(parents=True, exist_ok=True)
                cfg_path.write_text(_json.dumps(body, indent=2))
                return self.send_json({"ok": True})
            except Exception as e:
                return self.send_json({"error": str(e)}, 500)


        # ── IAP PDF Compile POST ─────────────────────────────────────────────
        elif path == "/api/ics/iap_compile":
            if not HAS_PDF:
                return self.send_json({"error": "PDF compiler not available: " + _pdf_err_msg}, 503)

            inc_id  = body.get("incident_id","")
            period  = body.get("period", 1)
            form_types = body.get("form_types", [])  # empty = all
            include_title = body.get("include_title", True)

            if not inc_id:
                return self.send_json({"error": "incident_id required"}, 400)

            # Fetch incident name
            inc_row = c.execute("SELECT name FROM incidents WHERE id=?", (inc_id,)).fetchone()
            incident_name = inc_row["name"] if inc_row else "Unknown Incident"

            # Fetch all forms for this incident/period
            if form_types:
                placeholders = ",".join("?"*len(form_types))
                rows = rows_to_list(c.execute(
                    f"SELECT * FROM ics_forms WHERE incident_id=? AND period=? "
                    f"AND form_type IN ({placeholders}) ORDER BY form_type, created",
                    [inc_id, period] + form_types
                ).fetchall())
            else:
                rows = rows_to_list(c.execute(
                    "SELECT * FROM ics_forms WHERE incident_id=? AND period=? ORDER BY form_type, created",
                    (inc_id, period)
                ).fetchall())

            if not rows:
                return self.send_json({"error": "No forms found for this incident/period"}, 404)

            # Build forms_by_type dict
            forms_by_type = {}
            for r in rows:
                ft = r.get("form_type","")
                try:    fdata = json.loads(r.get("data","{}"))
                except: fdata = {}
                fdata["_form_id"]    = r.get("id","")
                fdata["_form_type"]  = ft
                fdata["_updated"]    = r.get("updated","")
                forms_by_type.setdefault(ft, []).append(fdata)

            # Compile
            try:
                pdf_bytes = compile_iap(
                    forms_by_type,
                    incident_name = incident_name,
                    period        = period,
                    prepared_by   = body.get("prepared_by",""),
                    date_str      = body.get("date_str", now[:10]),
                    include_title = include_title,
                )

                # Send as PDF download
                safe_name = "".join(c2 if c2.isalnum() else "_" for c2 in incident_name)[:30]
                filename  = f"IAP_{safe_name}_P{period}_{now[:10]}.pdf"
                self.send_response(200)
                self.send_header("Content-Type",        "application/pdf")
                self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
                self.send_header("Content-Length",       str(len(pdf_bytes)))
                self.cors()
                self.end_headers()
                self.wfile.write(pdf_bytes)
                return
            except Exception as e:
                import traceback
                traceback.print_exc()
                return self.send_json({"error": str(e)}, 500)

        # ── Incident Archive POST ────────────────────────────────────────────
        elif path == "/api/ics/incidents/archive":
            import os, json as _json, shutil, sqlite3 as _sq
            inc_id = body.get("incident_id","")
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)

            lacie_base = "/media/fieldcommand/backup/incidents"
            if not os.path.isdir("/media/fieldcommand"):
                return self.send_json({"error":"USB backup drive not mounted — label drive FIELDCOMMAND and connect"},503)

            # Fetch incident from DB
            row = c.execute("SELECT * FROM incidents WHERE id=?", (inc_id,)).fetchone()
            if not row:
                return self.send_json({"error":"Incident not found"},404)
            inc = dict(row)

            # Create archive folder
            slug    = "".join(c2 if c2.isalnum() else "_" for c2 in inc["name"])[:30]
            folder  = f"{now[:10]}_{slug}_{inc_id[:8]}"
            dest    = os.path.join(lacie_base, folder)
            os.makedirs(dest, exist_ok=True)

            # Dump all related data to JSON
            tables = {
                "incident":  [inc],
                "forms":     rows_to_list(c.execute("SELECT * FROM ics_forms WHERE incident_id=?",    (inc_id,)).fetchall()),
                "labor":     rows_to_list(c.execute("SELECT * FROM fema_labor WHERE incident_id=?",   (inc_id,)).fetchall()),
                "equipment": rows_to_list(c.execute("SELECT * FROM fema_equipment WHERE incident_id=?",(inc_id,)).fetchall()),
                "materials": rows_to_list(c.execute("SELECT * FROM fema_materials WHERE incident_id=?",(inc_id,)).fetchall()),
                "checkins":  rows_to_list(c.execute("SELECT * FROM checkin_entries WHERE incident_id=?",(inc_id,)).fetchall()),
                "tcards":    rows_to_list(c.execute("SELECT * FROM ics_tcards WHERE incident_id=?",    (inc_id,)).fetchall()),
                "meetings":  rows_to_list(c.execute("SELECT * FROM ics_meetings WHERE incident_id=?",  (inc_id,)).fetchall()),
            }

            # Write full archive JSON
            archive_path = os.path.join(dest, "incident_data.json")
            with open(archive_path, "w") as f:
                _json.dump(tables, f, indent=2, default=str)

            # Write human-readable metadata
            meta_path = os.path.join(dest, "incident_meta.json")
            with open(meta_path, "w") as f:
                _json.dump({
                    "incident_id":   inc_id,
                    "name":          inc["name"],
                    "type":          inc.get("type",""),
                    "status":        inc.get("status",""),
                    "started":       inc.get("started",""),
                    "closed":        inc.get("closed",""),
                    "archived_at":   now,
                    "folder":        folder,
                    "form_count":    len(tables["forms"]),
                    "labor_count":   len(tables["labor"]),
                    "equip_count":   len(tables["equipment"]),
                    "mat_count":     len(tables["materials"]),
                    "checkin_count": len(tables["checkins"]),
                }, f, indent=2)

            # Mark incident as archived in Pi DB (keeps data, just flagged)
            c.execute(
                "UPDATE incidents SET archived=1, archive_path=?, archived_at=?, status=? WHERE id=?",
                (dest, now, "archived", inc_id)
            )
            c.commit()
            return self.send_json({"ok":True,"archive_path":dest,"folder":folder})

        # ── Restore archived incident from USB backup drive ────────────────────────────
        elif path == "/api/ics/incidents/restore":
            import os, json as _json
            folder = body.get("folder","")
            lacie_base = "/media/fieldcommand/backup/incidents"
            archive_path = os.path.join(lacie_base, folder)
            data_file    = os.path.join(archive_path, "incident_data.json")
            if not os.path.isfile(data_file):
                return self.send_json({"error":"Archive not found"},404)

            with open(data_file) as f:
                data = _json.load(f)

            # Restore incident row first
            for inc in data.get("incident",[]):
                inc["archived"] = 0  # mark as active again
                inc["status"]   = inc.get("status","active") if inc.get("status") != "archived" else "closed"
                cols = ",".join(inc.keys())
                ph   = ",".join("?"*len(inc))
                c.execute(f"INSERT OR REPLACE INTO incidents ({cols}) VALUES ({ph})",
                          list(inc.values()))

            # Restore forms
            for row in data.get("forms",[]):
                cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                c.execute(f"INSERT OR REPLACE INTO ics_forms ({cols}) VALUES ({ph})", list(row.values()))

            # Restore cost data
            for table, key in [("fema_labor","labor"),("fema_equipment","equipment"),("fema_materials","materials")]:
                for row in data.get(key,[]):
                    cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                    c.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})", list(row.values()))

            # Restore check-ins, tcards, meetings
            for table, key in [("checkin_entries","checkins"),("ics_tcards","tcards"),("ics_meetings","meetings")]:
                for row in data.get(key,[]):
                    cols = ",".join(row.keys()); ph = ",".join("?"*len(row))
                    try:
                        c.execute(f"INSERT OR REPLACE INTO {table} ({cols}) VALUES ({ph})", list(row.values()))
                    except Exception: pass

            c.commit()
            inc_id = data.get("incident",[{}])[0].get("id","")
            return self.send_json({"ok":True,"incident_id":inc_id,
                "restored_forms": len(data.get("forms",[]))})

        # ── Hard-delete incident from Pi DB ─────────────────────────────────
        elif path == "/api/ics/incidents/delete":
            inc_id = body.get("incident_id","")
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            for table in ["ics_forms","fema_labor","fema_equipment","fema_materials",
                          "checkin_entries","ics_tcards","ics_meetings","general_info"]:
                try:
                    c.execute(f"DELETE FROM {table} WHERE incident_id=?", (inc_id,))
                except Exception: pass
            c.execute("DELETE FROM incidents WHERE id=?", (inc_id,))
            c.commit()
            return self.send_json({"ok":True,"deleted":inc_id})

        # ── Beta / Scenario Reset ────────────────────────────────────────────
        # Wipes all incident data, forms, costs, check-ins, T-cards.
        # Leaves intact: roster, hospitals, channel_library, resource_types,
        # repeaters, system config. Requires confirm="RESET" in body.
        elif path == "/api/ics/reset":
            if body.get("confirm") != "RESET":
                return self.send_json({"error":"Send confirm='RESET' to proceed"},400)
            wipe_tables = [
                "incidents","ics_forms","general_info",
                "fema_labor","fema_equipment","fema_materials",
                "checkin_entries","ics_tcards","ics_meetings",
                "resource_history","ics_periods",
            ]
            counts = {}
            for table in wipe_tables:
                try:
                    n = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                    c.execute(f"DELETE FROM {table}")
                    counts[table] = n
                except Exception as e:
                    counts[table] = f"error: {e}"
            c.commit()
            return self.send_json({"ok":True,"wiped":counts,
                "preserved":["roster","hospitals","channel_library",
                             "resource_types","repeaters","net_entries"]})



        # ── Incident Templates POST (create / update) ────────────────────────
        elif path == "/api/ics/templates":
            tid = body.get("id") or f"tmpl-{int(time.time()*1000)}"
            data_str = json.dumps(body.get("data", {}))
            existing = c.execute("SELECT id FROM incident_templates WHERE id=?", (tid,)).fetchone()
            if existing:
                c.execute("""UPDATE incident_templates SET
                    name=?,icon=?,type=?,summary=?,sort_order=?,enabled=?,data=?,updated=?
                    WHERE id=?""",
                    (body.get("name","Untitled"), body.get("icon","📋"),
                     body.get("type",""), body.get("summary",""),
                     body.get("sort_order",99), body.get("enabled",1),
                     data_str, now, tid))
            else:
                c.execute("""INSERT INTO incident_templates
                    (id,name,icon,type,summary,sort_order,is_builtin,enabled,data,created,updated)
                    VALUES (?,?,?,?,?,?,0,1,?,?,?)""",
                    (tid, body.get("name","Untitled"), body.get("icon","📋"),
                     body.get("type",""), body.get("summary",""),
                     body.get("sort_order",99), data_str, now, now))
            c.commit()
            return self.send_json({"ok":True,"id":tid})

        # ── Import templates from JSON ────────────────────────────────────────
        elif path == "/api/ics/templates/import":
            templates = body if isinstance(body, list) else body.get("templates", [])
            imported = 0
            for t in templates:
                tid = t.get("id") or f"tmpl-{int(time.time()*1000)}-{imported}"
                # Check for ID collision — append _imported if needed
                existing = c.execute("SELECT id FROM incident_templates WHERE id=?", (tid,)).fetchone()
                if existing:
                    tid = tid + "_imported"
                c.execute("""INSERT OR REPLACE INTO incident_templates
                    (id,name,icon,type,summary,sort_order,is_builtin,enabled,data,created,updated)
                    VALUES (?,?,?,?,?,?,0,1,?,?,?)""",
                    (tid, t.get("name","Imported"), t.get("icon","📋"),
                     t.get("type",""), t.get("summary",""),
                     t.get("sort_order",99),
                     json.dumps(t.get("data",{})), now, now))
                imported += 1
            c.commit()
            return self.send_json({"ok":True,"imported":imported})

        # ── FEMA Equipment Rates POST (add/update custom rate) ──────────────
        elif path == "/api/ics/fema/rates":
            rid = body.get("id")
            if rid:
                # Update existing
                fields = ["code","category","description","unit","rate","rate_year","notes","active"]
                sets   = [f"{f}=?" for f in fields if f in body]
                vals   = [body[f] for f in fields if f in body] + [rid]
                if sets:
                    c.execute(f"UPDATE fema_equipment_rates SET {','.join(sets)} WHERE id=?", vals)
            else:
                c.execute(
                    "INSERT INTO fema_equipment_rates (code,category,description,unit,rate,rate_year,notes) "
                    "VALUES (?,?,?,?,?,?,?)",
                    (body.get("code",""), body.get("category",""), body.get("description",""),
                     body.get("unit","hour"), body.get("rate",0),
                     body.get("rate_year",2025), body.get("notes",""))
                )
                rid = c.lastrowid
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        # ── FEMA Rates bulk year update ──────────────────────────────────────
        elif path == "/api/ics/fema/rates/update_year":
            new_year = body.get("year")
            if not new_year:
                return self.send_json({"error":"year required"},400)
            c.execute("UPDATE fema_equipment_rates SET rate_year=? WHERE active=1", (new_year,))
            n = c.execute("SELECT changes()").fetchone()[0]
            c.commit()
            return self.send_json({"ok":True,"updated":n,"year":new_year})


        # ── Resource GPS Position POST ───────────────────────────────────────
        elif path == "/api/ics/resources/gps":
            card_id = body.get("id")
            lat     = body.get("lat")
            lon     = body.get("lon")
            if not card_id or lat is None or lon is None:
                return self.send_json({"error":"id, lat, lon required"},400)
            c.execute(
                """UPDATE ics_tcards SET lat=?, lon=?, gps_updated=?,
                   gps_source=?, location_label=?, updated=?
                   WHERE id=?""",
                (lat, lon, now,
                 body.get("gps_source","manual"),
                 body.get("location_label",""),
                 now, card_id)
            )
            c.commit()
            return self.send_json({"ok":True})

        # ── Clear GPS for a resource ─────────────────────────────────────────
        elif path == "/api/ics/resources/gps/clear":
            card_id = body.get("id")
            if not card_id:
                return self.send_json({"error":"id required"},400)
            c.execute(
                "UPDATE ics_tcards SET lat=NULL, lon=NULL, gps_source='', location_label='' WHERE id=?",
                (card_id,)
            )
            c.commit()
            return self.send_json({"ok":True})

        # ── FEMA PA Cost Tracking POST ───────────────────────────────────────
        elif path == "/api/ics/fema/labor":
            rid = body.get("id") or f"lab-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO fema_labor
                (id,incident_id,period,employee,position,dept,date_worked,
                 hours_reg,hours_ot,rate_reg,rate_ot,fringe_pct,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("period",0),
                 body.get("employee",""), body.get("position",""),
                 body.get("dept",""), body.get("date_worked",""),
                 body.get("hours_reg",0), body.get("hours_ot",0),
                 body.get("rate_reg",0), body.get("rate_ot",0),
                 body.get("fringe_pct",0), body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/fema/equipment":
            rid = body.get("id") or f"eq-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO fema_equipment
                (id,incident_id,period,equipment,equip_id,fema_code,
                 hours_used,rate_hr,operator,date_used,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("period",0),
                 body.get("equipment",""), body.get("equip_id",""),
                 body.get("fema_code",""), body.get("hours_used",0),
                 body.get("rate_hr",0), body.get("operator",""),
                 body.get("date_used",""), body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/fema/materials":
            rid = body.get("id") or f"mat-{int(time.time()*1000)}"
            total = body.get("total_cost") or (body.get("quantity",1) * body.get("unit_cost",0))
            c.execute("""INSERT OR REPLACE INTO fema_materials
                (id,incident_id,description,vendor,quantity,unit,
                 unit_cost,total_cost,po_number,date_purch,category,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (rid, body.get("incident_id",""), body.get("description",""),
                 body.get("vendor",""), body.get("quantity",1), body.get("unit",""),
                 body.get("unit_cost",0), total, body.get("po_number",""),
                 body.get("date_purch",""), body.get("category","Materials"),
                 body.get("notes",""), now, now))
            c.commit()
            return self.send_json({"ok":True,"id":rid})

        elif path == "/api/ics/checkin":
            ci_id = body.get("id") or f"ci-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO checkin_entries
                (id, incident_id, period, name, callsign_id, agency,
                 ics_position, resource_type, check_in_time, equipment,
                 home_unit, status, synced_to_211, notes, created)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (ci_id,
                 body.get("incident_id",""), body.get("period",1),
                 body.get("name",""), body.get("callsign_id",""),
                 body.get("agency",""), body.get("ics_position",""),
                 body.get("resource_type",""), body.get("check_in_time", now),
                 body.get("equipment",""), body.get("home_unit",""),
                 body.get("status","Checked In"),
                 body.get("synced_to_211",0),
                 body.get("notes",""), now))
            c.commit()
            return self.send_json({"status":"ok","id":ci_id})

        # ── Mark check-in entries as synced to ICS-211 ─────────────────────
        elif path == "/api/ics/checkin/sync":
            ids = body.get("ids",[])
            for cid in ids:
                c.execute("UPDATE checkin_entries SET synced_to_211=1 WHERE id=?", (cid,))
            c.commit()
            return self.send_json({"status":"ok","synced":len(ids)})

        elif path == "/api/ics/general_info":
            inc_id = body.get("incident_id","")
            period = int(body.get("period",1))
            if not inc_id:
                return self.send_json({"error":"incident_id required"},400)
            gi_id  = f"{inc_id}-{period}"
            fields = [
                "incident_name","incident_number","incident_type","jurisdiction","incident_location","lat","lon","operational_period_from","operational_period_to","incident_commander","deputy_ic","safety_officer","public_info_officer","liaison_officer","ops_section_chief","planning_section_chief","logistics_section_chief","finance_section_chief","resources_unit_ldr","situation_unit_ldr","documentation_unit_ldr","demob_unit_ldr","coml_name","medical_unit_ldr","weather_forecast","weather_temp","weather_wind","weather_humidity","weather_sky","sunrise","sunset","prepared_by","approved_by","ics_variant"
            ]
            existing = c.execute(
                "SELECT id FROM general_info WHERE id=?",(gi_id,)).fetchone()
            if existing:
                sets = ", ".join(f"{f}=?" for f in fields) + ", updated=?"
                vals = [body.get(f,"") for f in fields] + [now, gi_id]
                c.execute(f"UPDATE general_info SET {sets} WHERE id=?", vals)
            else:
                cols = "id, incident_id, period, " + ", ".join(fields) + ", updated"
                phs  = ", ".join(["?"] * (len(fields) + 4))
                vals = [gi_id, inc_id, period] + [body.get(f,"") for f in fields] + [now]
                c.execute(f"INSERT INTO general_info ({cols}) VALUES ({phs})", vals)
            c.execute("""UPDATE incidents SET name=?, incident_commander=?,
                location=?, jurisdiction=?, ics_variant=?, updated=? WHERE id=?""",
                (body.get("incident_name",""),body.get("incident_commander",""),
                 body.get("incident_location",""),body.get("jurisdiction",""),
                 body.get("ics_variant","FEMA"),now, inc_id))
            c.commit()
            return self.send_json({"status":"ok","id":gi_id})

        else:
            self.send_json({"error":"Not found"},404)

    def do_POST(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/")
        body=self.read_body(); c=get_conn(); now=utcnow()

        if path == "/api/ics/incidents":
            inc_id=body.get("id") or f"inc-{int(time.time()*1000)}"
            c.execute("""INSERT INTO incidents
                (id,name,type,status,jurisdiction,incident_commander,
                 location,summary,current_period,started)
                VALUES(?,?,?,?,?,?,?,?,?,?)""",
                (inc_id,body.get("name",""),body.get("type",""),
                 "active",body.get("jurisdiction",""),
                 body.get("incident_commander",""),body.get("location",""),
                 body.get("summary",""),1,now))
            # Create period 1
            c.execute("INSERT INTO ics_periods(id,incident_id,period_num,started) VALUES(?,?,?,?)",
                      (f"per-{inc_id}-1",inc_id,1,now))
            c.commit()
            log_activity(inc_id,"Command","Incident Created",body.get("name",""))
            inc=row_to_dict(c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone())
            return self.send_json({"ok":True,"incident":inc})

        elif path.startswith("/api/ics/incidents/"):
            parts=path.split("/api/ics/incidents/")[1].split("/")
            inc_id=parts[0]; sub="/".join(parts[1:]) if len(parts)>1 else ""
            row=c.execute("SELECT * FROM incidents WHERE id=?",(inc_id,)).fetchone()

            if sub in ("","update"):
                if not row: return self.send_json({"error":"Not found"},404)
                allowed=["name","type","status","jurisdiction","incident_commander",
                         "location","summary"]
                sets=[]; vals=[]
                for k in allowed:
                    if k in body: sets.append(f"{k}=?"); vals.append(body[k])
                if sets:
                    vals+=[now,inc_id]
                    c.execute(f"UPDATE incidents SET {','.join(sets)},updated=? WHERE id=?",vals)
                    c.commit()
                log_activity(inc_id,"Command","Incident Updated","")
                return self.send_json({"ok":True})

            elif sub == "advance_period":
                if not row: return self.send_json({"error":"Not found"},404)
                new_period=row["current_period"]+1
                c.execute("UPDATE incidents SET current_period=?,updated=? WHERE id=?",
                          (new_period,now,inc_id))
                c.execute("INSERT INTO ics_periods(id,incident_id,period_num,started,objectives) VALUES(?,?,?,?,?)",
                          (f"per-{inc_id}-{new_period}",inc_id,new_period,now,
                           body.get("objectives","")))
                c.commit()
                log_activity(inc_id,"Command","Period Advanced",f"Period {new_period}")
                return self.send_json({"ok":True,"period":new_period})

            elif sub == "close":
                if not row: return self.send_json({"error":"Not found"},404)
                c.execute("UPDATE incidents SET status='closed',closed=?,updated=? WHERE id=?",
                          (now,now,inc_id)); c.commit()
                log_activity(inc_id,"Command","Incident Closed","")
                return self.send_json({"ok":True})

            elif sub == "command":
                # Save command section data (objectives, safety message, weather)
                fid = f"command-{inc_id}"
                c.execute("""INSERT OR REPLACE INTO ics_forms
                    (id,incident_id,form_type,period,summary,data,created,updated)
                    VALUES(?,?,?,?,?,?,COALESCE((SELECT created FROM ics_forms WHERE id=?),?),?)""",
                    (fid,inc_id,"command",body.get("period",1),"Command Section",jdump(body),fid,now,now))
                c.commit()
                log_activity(inc_id,"Command","Command Section Saved","")
                return self.send_json({"ok":True})

        elif path.startswith("/api/ics/forms/"):
            form_type=path.split("/api/ics/forms/")[1].split("/")[0]
            fid=body.get("id") or f"{form_type}-{int(time.time()*1000)}"
            body.update({"id":fid,"form_type":form_type,"updated":now})
            body.setdefault("created",now)
            c.execute("""INSERT OR REPLACE INTO ics_forms
                (id,incident_id,form_type,period,summary,data,created,updated)
                VALUES(?,?,?,?,?,?,?,?)""",
                (fid,body.get("incident_id",""),form_type,body.get("period",1),
                 body.get("summary",""),jdump(body),body.get("created",now),now))
            c.commit()
            log_activity(body.get("incident_id",""),form_type.upper(),"Form Saved",fid)
            return self.send_json({"ok":True,"id":fid})

        elif path == "/api/ics/tcards":
            cid=body.get("id") or f"tc-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_tcards
                (id,incident_id,resource_id,resource_name,resource_type,category,type,
                 status,assignment,leader,contact,num_personnel,eta,notes,
                 order_number,home_agency,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (cid,body.get("incident_id",""),body.get("resource_id",""),
                 body.get("resource_name",""),body.get("resource_type",""),
                 body.get("category",""),body.get("type",""),
                 body.get("status","Available"),body.get("assignment",""),
                 body.get("leader",""),body.get("contact",""),
                 body.get("num_personnel",0),body.get("eta",""),
                 body.get("notes",""),body.get("order_number",""),
                 body.get("home_agency",""),body.get("created",now),now))
            c.commit()
            log_activity(body.get("incident_id",""),"Resources","T-Card Updated",
                         body.get("resource_name",""))
            return self.send_json({"ok":True,"card":row_to_dict(
                c.execute("SELECT * FROM ics_tcards WHERE id=?",(cid,)).fetchone())})

        elif path == "/api/ics/resources":
            rid=body.get("id") or f"icsres-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_resources
                (id,incident_id,resource_id,name,type,capability,
                 status,assignment,contact,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                (rid,body.get("incident_id",""),body.get("resource_id",""),
                 body.get("name",""),body.get("type",""),body.get("capability",""),
                 body.get("status","Available"),body.get("assignment",""),
                 body.get("contact",""),body.get("created",now),now))
            c.commit()
            return self.send_json({"ok":True,"resource":row_to_dict(
                c.execute("SELECT * FROM ics_resources WHERE id=?",(rid,)).fetchone())})

        elif path == "/api/ics/meetings":
            mid=body.get("id") or f"meet-{int(time.time()*1000)}"
            c.execute("""INSERT OR REPLACE INTO ics_meetings
                (id,incident_id,period,meeting_type,title,scheduled_time,
                 location,chair,attendees,agenda_items,status,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,COALESCE(
                    (SELECT created FROM ics_meetings WHERE id=?),?),?)""",
                (mid,
                 body.get("incident_id",""),
                 body.get("period",1),
                 body.get("meeting_type","other"),
                 body.get("title",""),
                 body.get("scheduled_time",""),
                 body.get("location",""),
                 body.get("chair",""),
                 jdump(body.get("attendees",[])),
                 jdump(body.get("agenda_items",[])),
                 body.get("status","scheduled"),
                 body.get("notes",""),
                 mid,now,now))
            c.commit()
            log_activity(body.get("incident_id",""),"Planning",
                         "Meeting Scheduled",body.get("title",""))
            return self.send_json({"ok":True,"id":mid})

        elif path.startswith("/api/ics/meetings/"):
            mid=path.split("/api/ics/meetings/")[1]
            allowed=["title","scheduled_time","location","chair","attendees",
                     "agenda_items","status","notes","period"]
            sets=[]; vals=[]
            for k in allowed:
                if k in body:
                    sets.append(f"{k}=?")
                    vals.append(jdump(body[k]) if isinstance(body[k],list) else body[k])
            if sets:
                vals+=[now,mid]
                c.execute(f"UPDATE ics_meetings SET {','.join(sets)},updated=? WHERE id=?",vals)
                c.commit()
            log_activity("","Planning","Meeting Updated",mid)
            return self.send_json({"ok":True})

        else:
            self.send_json({"error":"Not found"},404)

    def do_DELETE(self):
        parsed=urlparse(self.path); path=parsed.path.rstrip("/"); c=get_conn()
        if path.startswith("/api/ics/tcards/"):
            c.execute("DELETE FROM ics_tcards WHERE id=?",(path.split("/api/ics/tcards/")[1],))
        elif path.startswith("/api/ics/resources/"):
            c.execute("DELETE FROM ics_resources WHERE id=?",(path.split("/api/ics/resources/")[1],))
        elif path.startswith("/api/ics/meetings/"):
            c.execute("DELETE FROM ics_meetings WHERE id=?",(path.split("/api/ics/meetings/")[1],))
        elif path.startswith("/api/ics/incidents/"):
            inc_id=path.split("/api/ics/incidents/")[1]
            c.execute("DELETE FROM incidents WHERE id=?",(inc_id,))
        elif path.startswith("/api/ics/templates/"):
            tid = path.split("/api/ics/templates/")[1]
            c.execute("UPDATE incident_templates SET enabled=0 WHERE id=?", (tid,))
            c.commit()
            return self.send_json({"ok":True})

        elif path.startswith("/api/ics/fema/labor/"):
            c.execute("DELETE FROM fema_labor WHERE id=?",
                      (path.split("/api/ics/fema/labor/")[1],))
        elif path.startswith("/api/ics/fema/equipment/"):
            c.execute("DELETE FROM fema_equipment WHERE id=?",
                      (path.split("/api/ics/fema/equipment/")[1],))
        elif path.startswith("/api/ics/fema/materials/"):
            c.execute("DELETE FROM fema_materials WHERE id=?",
                      (path.split("/api/ics/fema/materials/")[1],))
        else:
            return self.send_json({"error":"Not found"},404)
        c.commit(); return self.send_json({"ok":True})


if __name__ == "__main__":
    db.startup()
    log.info("ICS Platform API on port 5055")
    HTTPServer(("0.0.0.0", 5055), ICSHandler).serve_forever()
