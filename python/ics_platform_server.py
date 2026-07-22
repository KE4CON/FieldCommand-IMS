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
        else:
            return self.send_json({"error":"Not found"},404)
        c.commit(); return self.send_json({"ok":True})


if __name__ == "__main__":
    db.startup()
    log.info("ICS Platform API on port 5055")
    HTTPServer(("0.0.0.0", 5055), ICSHandler).serve_forever()
