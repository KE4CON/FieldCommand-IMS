import json
# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""
FieldCommand — Unified SQLite Database Layer
/opt/fieldcommand/data/fieldcommand.db

Provides:
  - Schema creation and migration
  - Thread-safe connection pool (one per thread)
  - JSON-from-file migration (runs once on first startup)
  - Helper functions used by all three API servers

fcc.db stays separate — it is huge (~600 MB), rebuild-only, and never
written to by the application.
"""

import json
import sqlite3
import threading
import time
import shutil
import logging
from datetime import datetime, timezone
from pathlib import Path

log = logging.getLogger("fieldcommand.db")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE      = Path("/opt/fieldcommand")
DATA      = BASE / "data"
DB_PATH   = DATA / "fieldcommand.db"
REFS_DIR  = DATA / "refs"
FILES_DIR = REFS_DIR / "files"
THUMB_DIR = REFS_DIR / "thumbs"

for _d in [DATA, DATA / "nets", DATA / "forms", DATA / "ics" / "forms",
           REFS_DIR, FILES_DIR, THUMB_DIR]:
    _d.mkdir(parents=True, exist_ok=True)

# ── Thread-local connection pool ───────────────────────────────────────────────
_local = threading.local()


def get_conn() -> sqlite3.Connection:
    """Return a thread-local connection to fieldcommand.db."""
    if not hasattr(_local, "conn") or _local.conn is None:
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA synchronous=NORMAL")
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA cache_size=-8000")   # 8 MB per thread
        conn.execute("PRAGMA temp_store=MEMORY")
        _local.conn = conn
    return _local.conn


def db() -> sqlite3.Connection:
    """Shorthand for get_conn()."""
    return get_conn()


# ── Utilities ──────────────────────────────────────────────────────────────────
def utcnow() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def jdump(obj) -> str:
    return json.dumps(obj, default=str)


def jload(s, default=None):
    if not s:
        return default
    try:
        return json.loads(s)
    except Exception:
        return default


def row_to_dict(row) -> dict:
    if row is None:
        return None
    return dict(row)


def rows_to_list(rows) -> list:
    return [dict(r) for r in rows]


# ── Schema ─────────────────────────────────────────────────────────────────────
SCHEMA = """

-- ── Amateur / Starcom nets ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS nets (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL DEFAULT '',
    type        TEXT NOT NULL DEFAULT 'Amateur',
    starcom     INTEGER NOT NULL DEFAULT 0,   -- 1 = Starcom public safety net
    drill       INTEGER NOT NULL DEFAULT 0,
    active      INTEGER NOT NULL DEFAULT 1,
    freq        TEXT DEFAULT '',
    ncs         TEXT DEFAULT '',              -- net control station callsign
    created     TEXT NOT NULL,
    net_opened  TEXT,                         -- timestamp when net control opens net
    net_closed  TEXT,                         -- timestamp when net control closes net
    closed      TEXT,
    roster_chips TEXT DEFAULT '[]'           -- JSON array of callsigns
);

-- ── Net check-in entries ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS net_entries (
    id          TEXT PRIMARY KEY,
    net_id      TEXT NOT NULL REFERENCES nets(id) ON DELETE CASCADE,
    -- Identifier columns: at least one will be populated
    callsign    TEXT DEFAULT '',             -- amateur callsign (hams only)
    member_id   TEXT DEFAULT '',             -- ESV member ID
    radio_id    TEXT DEFAULT '',             -- Starcom radio ID (all ESV members)
    visitor_agency TEXT DEFAULT '',          -- for mutual aid / visitor
    -- Person info
    name        TEXT DEFAULT '',
    city        TEXT DEFAULT '',
    state       TEXT DEFAULT '',
    -- Log data
    precedence  TEXT DEFAULT 'ROUTINE',
    traffic     TEXT DEFAULT '',
    remarks     TEXT DEFAULT '',
    walk_in     INTEGER NOT NULL DEFAULT 0,  -- 1 = not in roster at check-in
    visitor     INTEGER NOT NULL DEFAULT 0,  -- 1 = mutual aid / outside org
    promoted    INTEGER NOT NULL DEFAULT 0,  -- 1 = promoted to roster
    timestamp   TEXT NOT NULL,
    checkout_time TEXT,                       -- NULL = still on net; set when checked out
    ema_id      TEXT DEFAULT '',              -- EMA/ESV member ID if found in roster
    ics_position TEXT DEFAULT ''              -- ICS position assigned at check-in
);
CREATE INDEX IF NOT EXISTS idx_ne_net    ON net_entries(net_id);
CREATE INDEX IF NOT EXISTS idx_ne_call   ON net_entries(callsign);
CREATE INDEX IF NOT EXISTS idx_ne_time   ON net_entries(timestamp);

-- ── NTS traffic messages ──────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS net_traffic (
    id          TEXT PRIMARY KEY,
    net_id      TEXT NOT NULL REFERENCES nets(id) ON DELETE CASCADE,
    msg_number  TEXT DEFAULT '',
    from_call   TEXT DEFAULT '',
    to_call     TEXT DEFAULT '',
    precedence  TEXT DEFAULT 'ROUTINE',
    handling    TEXT DEFAULT '',
    text        TEXT DEFAULT '',
    timestamp   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_nt_net ON net_traffic(net_id);

-- ── Member roster ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS roster (
    id          TEXT PRIMARY KEY,
    member_id   TEXT NOT NULL DEFAULT '', -- ESV member ID (all members)
    callsign    TEXT DEFAULT '',           -- amateur callsign (hams only, may be blank)
    radio_id    TEXT DEFAULT '',           -- Starcom/public safety radio ID (if applicable)
    first_name  TEXT DEFAULT '',
    last_name   TEXT DEFAULT '',
    role        TEXT DEFAULT 'Operator',
    member_type TEXT NOT NULL DEFAULT 'member',  -- 'member' | 'visitor' | 'mutual_aid'
    visitor_agency TEXT DEFAULT '',              -- agency name for non-ESV members
    phone       TEXT DEFAULT '',
    email       TEXT DEFAULT '',
    grid        TEXT DEFAULT '',
    lat         REAL,
    lon         REAL,
    notes       TEXT DEFAULT '',
    -- Certifications (boolean)
    cert_ics100    INTEGER DEFAULT 0,
    cert_ics200    INTEGER DEFAULT 0,
    cert_ics300    INTEGER DEFAULT 0,
    cert_ics400    INTEGER DEFAULT 0,
    cert_ics700    INTEGER DEFAULT 0,
    cert_ics800    INTEGER DEFAULT 0,
    cert_emcomm1   INTEGER DEFAULT 0,
    cert_emcomm2   INTEGER DEFAULT 0,
    cert_cpr       INTEGER DEFAULT 0,
    cert_first_aid INTEGER DEFAULT 0,
    cert_cert      INTEGER DEFAULT 0,
    -- Equipment capabilities (boolean)
    equip_hf       INTEGER DEFAULT 0,
    equip_vhf      INTEGER DEFAULT 0,
    equip_digital  INTEGER DEFAULT 0,
    equip_packet   INTEGER DEFAULT 0,
    equip_pactor   INTEGER DEFAULT 0,
    equip_vara_hf  INTEGER DEFAULT 0,
    equip_vara_fm  INTEGER DEFAULT 0,
    equip_aprs     INTEGER DEFAULT 0,
    equip_winlink  INTEGER DEFAULT 0,
    equip_go_box   INTEGER DEFAULT 0,
    equip_generator INTEGER DEFAULT 0,
    equip_battery  INTEGER DEFAULT 0,
    equip_vehicle  INTEGER DEFAULT 0,
    created     TEXT NOT NULL,
    modified    TEXT NOT NULL
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_roster_member ON roster(member_id);
CREATE INDEX IF NOT EXISTS idx_roster_call ON roster(UPPER(callsign))
    WHERE callsign != '';
CREATE INDEX IF NOT EXISTS idx_roster_role ON roster(role);

-- ── Activations ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS activations (
    id          TEXT PRIMARY KEY,
    member_id   TEXT REFERENCES roster(id) ON DELETE SET NULL,
    callsign    TEXT DEFAULT '',            -- denormalised for speed
    net_id      TEXT DEFAULT '',
    incident_id TEXT DEFAULT '',
    role        TEXT DEFAULT '',
    location    TEXT DEFAULT '',
    checked_in  TEXT NOT NULL,
    checked_out TEXT,
    notes       TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_act_member   ON activations(member_id);
CREATE INDEX IF NOT EXISTS idx_act_incident ON activations(incident_id);

-- ── Resource board ────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resources (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL DEFAULT '',
    type        TEXT DEFAULT '',            -- Personnel/Vehicle/Equipment/Facility
    capability  TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'Available',
    assignment  TEXT DEFAULT '',
    contact     TEXT DEFAULT '',
    notes       TEXT DEFAULT '',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_res_status ON resources(status);

-- ── ICS Incidents ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS incidents (
    id                  TEXT PRIMARY KEY,
    name                TEXT NOT NULL DEFAULT '',
    type                TEXT DEFAULT '',
    status              TEXT NOT NULL DEFAULT 'active',
    jurisdiction        TEXT DEFAULT '',
    incident_commander  TEXT DEFAULT '',
    location            TEXT DEFAULT '',
    summary             TEXT DEFAULT '',
    current_period      INTEGER NOT NULL DEFAULT 1,
    ics_variant         TEXT DEFAULT 'FEMA',    -- FEMA, USCG, NWCG
    started             TEXT NOT NULL,
    updated             TEXT,
    closed              TEXT
);
CREATE INDEX IF NOT EXISTS idx_inc_status ON incidents(status);

-- ── General Info (cross-form auto-population) ───────────────────────────────
CREATE TABLE IF NOT EXISTS general_info (
    id                      TEXT PRIMARY KEY,  -- "{incident_id}-{period}"
    incident_id             TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    period                  INTEGER NOT NULL DEFAULT 1,
    -- Incident header fields
    incident_name           TEXT DEFAULT '',
    incident_number         TEXT DEFAULT '',
    incident_type           TEXT DEFAULT '',
    jurisdiction            TEXT DEFAULT '',
    incident_location       TEXT DEFAULT '',
    lat                     TEXT DEFAULT '',
    lon                     TEXT DEFAULT '',
    -- Operational period
    operational_period_from TEXT DEFAULT '',
    operational_period_to   TEXT DEFAULT '',
    -- Command and General Staff
    incident_commander      TEXT DEFAULT '',
    deputy_ic               TEXT DEFAULT '',
    safety_officer          TEXT DEFAULT '',
    public_info_officer     TEXT DEFAULT '',
    liaison_officer         TEXT DEFAULT '',
    ops_section_chief       TEXT DEFAULT '',
    planning_section_chief  TEXT DEFAULT '',
    logistics_section_chief TEXT DEFAULT '',
    finance_section_chief   TEXT DEFAULT '',
    -- Key unit leaders (for signature auto-fill)
    resources_unit_ldr      TEXT DEFAULT '',
    situation_unit_ldr      TEXT DEFAULT '',
    documentation_unit_ldr  TEXT DEFAULT '',
    demob_unit_ldr          TEXT DEFAULT '',
    coml_name               TEXT DEFAULT '',
    medical_unit_ldr        TEXT DEFAULT '',
    -- Weather (fetched or manual)
    weather_forecast        TEXT DEFAULT '',
    weather_temp            TEXT DEFAULT '',
    weather_wind            TEXT DEFAULT '',
    weather_humidity        TEXT DEFAULT '',
    weather_sky             TEXT DEFAULT '',
    sunrise                 TEXT DEFAULT '',
    sunset                  TEXT DEFAULT '',
    -- IAP meta
    prepared_by             TEXT DEFAULT '',
    approved_by             TEXT DEFAULT '',
    ics_variant             TEXT DEFAULT 'FEMA',
    updated                 TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_gi_incident ON general_info(incident_id);
-- ── Resource Assignment History ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resource_history (
    id           TEXT PRIMARY KEY,
    incident_id  TEXT NOT NULL,
    period       INTEGER NOT NULL DEFAULT 1,
    resource_id  TEXT NOT NULL DEFAULT '',
    resource_name TEXT DEFAULT '',
    resource_type TEXT DEFAULT '',
    assignment   TEXT DEFAULT '',   -- Division/Group assigned to
    date         TEXT DEFAULT '',
    created      TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rh_incident ON resource_history(incident_id);
CREATE INDEX IF NOT EXISTS idx_rh_resource ON resource_history(resource_id);

-- ── Radio Channel Library (for ICS-205 pre-loaded channels) ─────────────────
CREATE TABLE IF NOT EXISTS channel_library (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL DEFAULT '',   -- e.g. "McHenry County Command"
    alpha_tag   TEXT DEFAULT '',            -- e.g. "MHCO CMD"
    rx_freq     TEXT DEFAULT '',            -- e.g. "155.340"
    tx_freq     TEXT DEFAULT '',            -- e.g. "155.340"
    pl_tone     TEXT DEFAULT '',            -- e.g. "100.0 Hz"
    mode        TEXT DEFAULT 'FM',          -- FM, NFM, P25, DMR, etc.
    function    TEXT DEFAULT 'Tactical',    -- Command, Tactical, Air, Medical, etc.
    division    TEXT DEFAULT '',            -- which division this channel is assigned to
    notes       TEXT DEFAULT '',
    custom      INTEGER DEFAULT 1,
    active      INTEGER DEFAULT 1,
    created     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_cl_name ON channel_library(name);



-- ── Hospital Database ───────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS hospitals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL DEFAULT '',
    address     TEXT DEFAULT '',
    city        TEXT DEFAULT '',
    state       TEXT DEFAULT '',
    county      TEXT DEFAULT '',
    phone       TEXT DEFAULT '',
    phone2      TEXT DEFAULT '',
    fax         TEXT DEFAULT '',
    lat         REAL,
    lon         REAL,
    trauma_level TEXT DEFAULT '',   -- Level I, II, III, IV, None
    burn_center  INTEGER DEFAULT 0,
    helipad      INTEGER DEFAULT 1,
    icu          INTEGER DEFAULT 0,
    peds_trauma  INTEGER DEFAULT 0,
    stroke_center INTEGER DEFAULT 0,
    cardiac_center INTEGER DEFAULT 0,
    travel_time_min INTEGER DEFAULT 0,
    notes       TEXT DEFAULT '',
    active      INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_hosp_state ON hospitals(state);
CREATE INDEX IF NOT EXISTS idx_hosp_county ON hospitals(county);

-- ── NIMS Resource Typing Library ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS resource_types (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    nims_id         TEXT DEFAULT '',    -- FEMA RTLT identifier e.g. "1-508-1001"
    kind            TEXT NOT NULL,      -- Engine, Crew, Helicopter, Personnel, etc.
    type_level      TEXT DEFAULT '',    -- Type I, II, III, IV, N (no type), varies
    category        TEXT NOT NULL,      -- Fire, SAR, Medical, Public Works, etc.
    mission_area    TEXT DEFAULT '',    -- FEMA mission area
    description     TEXT DEFAULT '',    -- Full NIMS name/description
    min_personnel   INTEGER DEFAULT 0,
    capabilities    TEXT DEFAULT '',    -- Key capability summary
    metric_notes    TEXT DEFAULT '',    -- Specific metrics (speed, capacity, etc.)
    custom          INTEGER DEFAULT 0,  -- 1 = user-added, 0 = NIMS standard
    definition_what TEXT DEFAULT '',    -- Plain English: what it is
    definition_std  TEXT DEFAULT '',    -- Minimum standards
    definition_order TEXT DEFAULT '',   -- When to order this vs others
    definition_conf TEXT DEFAULT '',    -- Common confusion points
    active          INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_rt_category ON resource_types(category);
CREATE INDEX IF NOT EXISTS idx_rt_kind     ON resource_types(kind);

-- ── ICS Operational Periods ───────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ics_periods (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    period_num  INTEGER NOT NULL,
    started     TEXT NOT NULL,
    ended       TEXT,
    shift_hours INTEGER DEFAULT 12,
    objectives  TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_per_inc ON ics_periods(incident_id);

-- ── ICS Resources ─────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ics_resources (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    resource_id TEXT DEFAULT '',            -- link to resources table (optional)
    name        TEXT NOT NULL DEFAULT '',
    type        TEXT DEFAULT '',
    capability  TEXT DEFAULT '',
    status      TEXT NOT NULL DEFAULT 'Available',
    assignment  TEXT DEFAULT '',
    contact     TEXT DEFAULT '',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_icsres_inc ON ics_resources(incident_id);

-- ── ICS T-Cards ───────────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ics_tcards (
    id              TEXT PRIMARY KEY,
    incident_id     TEXT NOT NULL REFERENCES incidents(id) ON DELETE CASCADE,
    resource_id     TEXT DEFAULT '',
    resource_name   TEXT NOT NULL DEFAULT '',
    resource_type   TEXT DEFAULT '',   -- Crew, Engine, Helicopter, Dozer, etc.
    category        TEXT DEFAULT '',   -- Personnel, Equipment, Supply, Aircraft
    type            TEXT DEFAULT '',   -- Type I, II, III, IV
    status          TEXT NOT NULL DEFAULT 'Available', -- Available, Assigned, Out of Service, Staging
    assignment      TEXT DEFAULT '',   -- Division/Group assigned to
    leader          TEXT DEFAULT '',   -- crew/unit leader name
    contact         TEXT DEFAULT '',   -- radio channel or phone
    num_personnel   INTEGER DEFAULT 0,
    eta             TEXT DEFAULT '',   -- ETA if en route
    notes           TEXT DEFAULT '',
    order_number    TEXT DEFAULT '',   -- resource order number
    home_agency     TEXT DEFAULT '',
    created         TEXT NOT NULL,
    updated         TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tc_inc    ON ics_tcards(incident_id);
CREATE INDEX IF NOT EXISTS idx_tc_status ON ics_tcards(status);

-- ── ICS Forms (flexible — all form types stored here) ─────────────────────────
CREATE TABLE IF NOT EXISTS ics_forms (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL DEFAULT '',
    form_type   TEXT NOT NULL,              -- ics201, ics202, ics205, etc.
    period      INTEGER DEFAULT 1,
    summary     TEXT DEFAULT '',
    data        TEXT NOT NULL DEFAULT '{}', -- full form JSON blob
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_icsf_inc  ON ics_forms(incident_id);
CREATE INDEX IF NOT EXISTS idx_icsf_type ON ics_forms(form_type);

-- ── ICS Activity Feed ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS activity_log (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    incident_id TEXT NOT NULL DEFAULT '',
    section     TEXT DEFAULT '',
    action      TEXT DEFAULT '',
    detail      TEXT DEFAULT '',
    timestamp   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_act_inc  ON activity_log(incident_id);
CREATE INDEX IF NOT EXISTS idx_act_time ON activity_log(timestamp);

-- ── ICS Meetings (Planning Section scheduler) ───────────────────────────────
CREATE TABLE IF NOT EXISTS ics_meetings (
    id              TEXT PRIMARY KEY,
    incident_id     TEXT NOT NULL DEFAULT '',
    period          INTEGER NOT NULL DEFAULT 1,
    meeting_type    TEXT NOT NULL,          -- incident_briefing, tactics, planning, ops_briefing, etc.
    title           TEXT NOT NULL DEFAULT '',
    scheduled_time  TEXT,                   -- ISO datetime
    location        TEXT DEFAULT '',
    chair           TEXT DEFAULT '',        -- who runs the meeting
    attendees       TEXT DEFAULT '[]',      -- JSON array of names/roles
    agenda_items    TEXT DEFAULT '[]',      -- JSON array of agenda items
    status          TEXT DEFAULT 'scheduled', -- scheduled, completed, cancelled
    notes           TEXT DEFAULT '',        -- minutes / action items
    created         TEXT NOT NULL,
    updated         TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_meet_inc  ON ics_meetings(incident_id);
CREATE INDEX IF NOT EXISTS idx_meet_type ON ics_meetings(meeting_type);

-- ── Standalone forms (ICS-213, ICS-214, NTS, etc.) ───────────────────────────
CREATE TABLE IF NOT EXISTS forms (
    id          TEXT PRIMARY KEY,
    form_type   TEXT NOT NULL,
    incident_id TEXT DEFAULT '',
    summary     TEXT DEFAULT '',
    data        TEXT NOT NULL DEFAULT '{}',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_forms_type ON forms(form_type);

-- ── ICS-211 Remote Check-In Entries ────────────────────────────────────────────
-- Populated by checkin.html when field personnel self-check in from any LAN device
CREATE TABLE IF NOT EXISTS checkin_entries (
    id            TEXT PRIMARY KEY,
    incident_id   TEXT NOT NULL DEFAULT '',
    period        INTEGER NOT NULL DEFAULT 1,
    name          TEXT DEFAULT '',
    callsign_id   TEXT DEFAULT '',
    agency        TEXT DEFAULT '',
    ics_position  TEXT DEFAULT '',
    resource_type TEXT DEFAULT '',
    check_in_time TEXT DEFAULT '',
    equipment     TEXT DEFAULT '',
    home_unit     TEXT DEFAULT '',
    status        TEXT DEFAULT 'Checked In',
    synced_to_211 INTEGER DEFAULT 0,
    notes         TEXT DEFAULT '',
    created       TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_ci_incident ON checkin_entries(incident_id);
CREATE INDEX IF NOT EXISTS idx_ci_status   ON checkin_entries(status);
-- ── Incident Event Templates ────────────────────────────────────────────────────
-- User-editable pre-planned event templates. Agencies can edit the built-in
-- templates, add their own, delete ones they don't use, and import/export JSON.
-- The 'data' column holds the full template definition as JSON.
-- Built-in templates are seeded on first run; is_builtin=1 distinguishes them
-- from agency-created ones (cosmetic only — both are fully editable/deletable).

CREATE TABLE IF NOT EXISTS incident_templates (
    id          TEXT PRIMARY KEY,           -- e.g. 'shelter', 'sar', or uuid for custom
    name        TEXT NOT NULL DEFAULT '',   -- display name
    icon        TEXT DEFAULT '📋',
    type        TEXT DEFAULT '',            -- incident type label
    summary     TEXT DEFAULT '',
    sort_order  INTEGER DEFAULT 99,
    is_builtin  INTEGER DEFAULT 0,          -- 1 = seeded with system, 0 = agency-created
    enabled     INTEGER DEFAULT 1,
    data        TEXT NOT NULL DEFAULT '{}', -- full JSON: objectives, resources, channels, org
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

-- ── FEMA Schedule of Equipment Rates ──────────────────────────────────────────
-- Pre-populated with common emergency management equipment from the current
-- FEMA Schedule of Equipment Rates. These are eligible reimbursement rates
-- for applicant-owned equipment under the Stafford Act.
--
-- IMPORTANT: FEMA updates this schedule periodically (roughly annually).
-- You must use the rates in effect at the time of the disaster declaration.
-- Rate year is stored per-row so historic incidents retain correct rates.
-- Update source: https://www.fema.gov/assistance/public/tools-resources/schedule-equipment-rates
--
-- Labor costs are NOT included in these rates — track separately in fema_labor table.

CREATE TABLE IF NOT EXISTS fema_equipment_rates (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    code        TEXT DEFAULT '',         -- FEMA schedule code (e.g. "2-7-1")
    category    TEXT DEFAULT '',         -- broad category (Vehicles, Generators, etc.)
    description TEXT NOT NULL DEFAULT '', -- equipment name as in FEMA schedule
    unit        TEXT DEFAULT 'hour',     -- hour / day / mile
    rate        REAL NOT NULL DEFAULT 0, -- $/unit eligible reimbursement rate
    rate_year   INTEGER DEFAULT 2025,    -- year this rate is from
    notes       TEXT DEFAULT '',
    active      INTEGER DEFAULT 1
);
CREATE INDEX IF NOT EXISTS idx_fer_category ON fema_equipment_rates(category);
CREATE INDEX IF NOT EXISTS idx_fer_code     ON fema_equipment_rates(code);

-- ── FEMA PA Reimbursement Cost Tracking ────────────────────────────────────────
-- Supports FEMA Public Assistance documentation: Force Account Labor,
-- Force Account Equipment, Materials, and Project Worksheet summary.
-- Reference: FEMA Public Assistance Program and Policy Guide (PAPPG)

CREATE TABLE IF NOT EXISTS fema_labor (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL DEFAULT '',
    period      INTEGER DEFAULT 0,           -- 0 = all periods / incident total
    employee    TEXT NOT NULL DEFAULT '',
    position    TEXT DEFAULT '',
    dept        TEXT DEFAULT '',
    date_worked TEXT DEFAULT '',
    hours_reg   REAL DEFAULT 0,
    hours_ot    REAL DEFAULT 0,
    rate_reg    REAL DEFAULT 0,              -- $/hr regular
    rate_ot     REAL DEFAULT 0,              -- $/hr overtime
    fringe_pct  REAL DEFAULT 0,              -- fringe benefits %
    notes       TEXT DEFAULT '',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fema_equipment (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL DEFAULT '',
    period      INTEGER DEFAULT 0,
    equipment   TEXT NOT NULL DEFAULT '',    -- e.g. "Pickup Truck (< 1T)"
    equip_id    TEXT DEFAULT '',             -- agency unit ID
    fema_code   TEXT DEFAULT '',             -- FEMA schedule code e.g. "2-7-1"
    hours_used  REAL DEFAULT 0,
    rate_hr     REAL DEFAULT 0,              -- FEMA eligible $/hr
    operator    TEXT DEFAULT '',
    date_used   TEXT DEFAULT '',
    notes       TEXT DEFAULT '',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS fema_materials (
    id          TEXT PRIMARY KEY,
    incident_id TEXT NOT NULL DEFAULT '',
    description TEXT NOT NULL DEFAULT '',
    vendor      TEXT DEFAULT '',
    quantity    REAL DEFAULT 1,
    unit        TEXT DEFAULT '',
    unit_cost   REAL DEFAULT 0,
    total_cost  REAL DEFAULT 0,
    po_number   TEXT DEFAULT '',
    date_purch  TEXT DEFAULT '',
    category    TEXT DEFAULT '',             -- Supplies, Materials, Contracts
    notes       TEXT DEFAULT '',
    created     TEXT NOT NULL,
    updated     TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_labor_incident   ON fema_labor(incident_id);
CREATE INDEX IF NOT EXISTS idx_equip_incident   ON fema_equipment(incident_id);
CREATE INDEX IF NOT EXISTS idx_mat_incident     ON fema_materials(incident_id);


-- ── Dead Man's Switch (singleton row id=1) ────────────────────────────────────
CREATE TABLE IF NOT EXISTS dms_state (
    id              INTEGER PRIMARY KEY DEFAULT 1,
    state           TEXT NOT NULL DEFAULT 'disarmed',
    armed_nets      TEXT NOT NULL DEFAULT '[]',  -- JSON array
    threshold_min   INTEGER NOT NULL DEFAULT 30,
    last_activity   TEXT,
    armed_at        TEXT,
    triggered_at    TEXT
);
INSERT OR IGNORE INTO dms_state(id) VALUES(1);

-- ── APRS Tactical Map state (singleton) ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS map_state (
    id      INTEGER PRIMARY KEY DEFAULT 1,
    shapes  TEXT NOT NULL DEFAULT '[]',
    markers TEXT NOT NULL DEFAULT '[]',
    updated TEXT
);
INSERT OR IGNORE INTO map_state(id) VALUES(1);

-- ── Starcom Resource Map state (singleton) ────────────────────────────────────
CREATE TABLE IF NOT EXISTS resmap_state (
    id      INTEGER PRIMARY KEY DEFAULT 1,
    markers TEXT NOT NULL DEFAULT '[]',
    updated TEXT
);
INSERT OR IGNORE INTO resmap_state(id) VALUES(1);

-- ── Station / Organization configuration (singleton) ────────────────────────
CREATE TABLE IF NOT EXISTS station_config (
    id              INTEGER PRIMARY KEY DEFAULT 1,
    -- Callsign & identity
    callsign        TEXT NOT NULL DEFAULT 'W8EOC',
    personal_call   TEXT DEFAULT '',          -- personal callsign of operator/developer
    org_name        TEXT DEFAULT '',          -- full organization name
    org_short       TEXT DEFAULT '',          -- abbreviation (e.g. MCESV)
    agency_name     TEXT DEFAULT '',          -- associated agency (e.g. McHenry County EMA)
    agency_short    TEXT DEFAULT '',          -- agency abbreviation
    -- Contact
    contact_email   TEXT DEFAULT '',
    contact_phone   TEXT DEFAULT '',
    -- Location
    city            TEXT DEFAULT '',
    state           TEXT DEFAULT '',
    county          TEXT DEFAULT '',
    lat             REAL NOT NULL DEFAULT 42.3247,
    lon             REAL NOT NULL DEFAULT -88.3822,
    gps_enabled     INTEGER NOT NULL DEFAULT 1,
    gps_device      TEXT DEFAULT '/dev/gps0',
    gps_last_fix    TEXT,
    -- ICS form defaults
    ics_form_variant TEXT DEFAULT 'FEMA',    -- FEMA, USCG, or NWCG
    -- Branding
    logo_data       TEXT DEFAULT '',          -- base64 encoded logo image
    logo_mime       TEXT DEFAULT '',          -- image/png, image/jpeg, image/svg+xml
    -- Attribution (read-only display)
    software_author TEXT DEFAULT 'James Rospopo KE4CON',
    software_url    TEXT DEFAULT 'https://github.com/KE4CON/FieldCommand-IMS',
    -- Setup state
    setup_complete  INTEGER NOT NULL DEFAULT 0,
    -- Active modules (JSON object)
    active_modules  TEXT DEFAULT '{}',
    -- Public safety radio configuration
    ps_system_name  TEXT DEFAULT '',      -- e.g. Starcom21, MABAS, P25 Zone 1
    ps_system_type  TEXT DEFAULT 'P25',   -- P25, DMR, Analog, Mixed, LTE, Other
    ps_id_label     TEXT DEFAULT 'Radio ID', -- Unit #, Badge #, Apparatus #, etc.
    ps_dispatch     TEXT DEFAULT '',      -- dispatch center name
    ps_system2_name TEXT DEFAULT '',      -- secondary system
    ps_system2_type TEXT DEFAULT '',
    ps_member_id_label TEXT DEFAULT 'EMA ID',
    ps_member_lookup   TEXT DEFAULT 'radio_id',
    configured_at   TEXT
);
INSERT OR IGNORE INTO station_config(id) VALUES(1);

-- ── Repeater database ─────────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS repeaters (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    callsign    TEXT DEFAULT '',
    output_freq TEXT DEFAULT '',
    input_freq  TEXT DEFAULT '',
    tone        TEXT DEFAULT '',
    tone_input  TEXT DEFAULT '',
    mode        TEXT DEFAULT 'FM',
    digital_code TEXT DEFAULT '',
    city        TEXT DEFAULT '',
    state       TEXT DEFAULT '',
    county      TEXT DEFAULT '',
    lat         REAL,
    lon         REAL,
    status      TEXT DEFAULT 'On-Air',
    use_type    TEXT DEFAULT 'Open',
    ares        INTEGER DEFAULT 0,
    races       INTEGER DEFAULT 0,
    skywarn     INTEGER DEFAULT 0,
    echolink    INTEGER DEFAULT 0,
    allstar     INTEGER DEFAULT 0,
    sponsor     TEXT DEFAULT '',
    notes       TEXT DEFAULT '',
    updated     TEXT,
    source      TEXT DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_rep_state  ON repeaters(state);
CREATE INDEX IF NOT EXISTS idx_rep_call   ON repeaters(callsign);
CREATE INDEX IF NOT EXISTS idx_rep_ares   ON repeaters(ares);

-- ── Reference library documents ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_documents (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL DEFAULT '',
    filename        TEXT NOT NULL DEFAULT '',
    stored_name     TEXT NOT NULL DEFAULT '',
    category        TEXT NOT NULL DEFAULT 'other',
    sections        TEXT NOT NULL DEFAULT '["amateur"]',  -- JSON array
    description     TEXT DEFAULT '',
    tags            TEXT NOT NULL DEFAULT '[]',            -- JSON array
    source          TEXT DEFAULT '',
    applies_to      TEXT DEFAULT '',
    revision        TEXT DEFAULT '',
    expires         TEXT,
    content_type    TEXT DEFAULT '',
    size_bytes      INTEGER DEFAULT 0,
    sha256          TEXT DEFAULT '',
    uploaded        TEXT NOT NULL,
    modified        TEXT,
    downloads       INTEGER NOT NULL DEFAULT 0,
    last_downloaded TEXT
);
CREATE INDEX IF NOT EXISTS idx_refdoc_cat  ON ref_documents(category);
CREATE INDEX IF NOT EXISTS idx_refdoc_date ON ref_documents(uploaded);

-- ── Preflight run history ─────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS preflight_runs (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    verdict     TEXT NOT NULL,
    checks      TEXT NOT NULL DEFAULT '{}',   -- JSON blob
    timestamp   TEXT NOT NULL
);

"""



def seed_channel_library(conn):
    """Seed channel_library with example local channels on first run.
    These are McHenry County IL defaults — any agency should replace
    these with their own channels via the Channel Library management page."""
    try:
        existing = conn.execute("SELECT COUNT(*) FROM channel_library").fetchone()[0]
        if existing == 0:
            import time
            now = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            channels = [
                # Agency-specific — configure for your jurisdiction
                ('cl-001','MHEMA Command',       'MHEMA CMD',  '155.3400','155.3400','100.0 Hz','FM', 'Command',  '', 'McHenry County EMA primary command net', 0, 1, now),
                ('cl-002','MHEMA Tactical',      'MHEMA TAC',  '154.3700','154.3700','100.0 Hz','FM', 'Tactical', '', 'McHenry County EMA tactical net',        0, 1, now),
                ('cl-003','McHenry Co. Fire Disp','MHCO FIRE', '154.3700','154.3700','100.0 Hz','FM', 'Tactical', '', 'McHenry County fire dispatch',           0, 1, now),
                ('cl-004','Starcom21 Interop',   'STCM INTR',  '155.3400','155.3400','100.0 Hz','FM', 'Interop',  '', 'Illinois Starcom21 interoperability',     0, 1, now),
                ('cl-005','ILEMS Statewide',     'ILEMS',      '155.3400','155.3400','100.0 Hz','FM', 'Tactical', '', 'Illinois EMS statewide channel',          0, 1, now),
                ('cl-006','EMS Med 10 (IDPH)',   'EMS MED10',  '155.3400','155.3400','',        'FM', 'Medical',  '', 'Illinois Dept of Public Health Med 10',   0, 1, now),
                ('cl-007','McHenry ARES/RACES',  'K9ESV',      '147.0750','147.0750','107.2 Hz','FM', 'Amateur',  '', 'K9ESV ARES/RACES primary repeater',       0, 1, now),
            ]
            conn.executemany("""INSERT INTO channel_library
                (id,name,alpha_tag,rx_freq,tx_freq,pl_tone,mode,function,
                 division,notes,custom,active,created)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)""", channels)
            conn.commit()
            log.info(f"Seeded {len(channels)} example channels into channel_library")
    except Exception as e:
        log.warning(f"Channel library seeding skipped: {e}")

def init_db():
    """Create all tables and indexes. Safe to call multiple times."""
    conn = db()
    conn.executescript(SCHEMA)
    # Migration: add new columns to existing databases (idempotent)
    migrations = [
        "ALTER TABLE nets ADD COLUMN net_opened TEXT",
        "ALTER TABLE nets ADD COLUMN net_closed TEXT",
        "ALTER TABLE net_entries ADD COLUMN checkout_time TEXT",
        "ALTER TABLE net_entries ADD COLUMN ema_id TEXT DEFAULT ''",
        # station_config expansions
        "ALTER TABLE station_config ADD COLUMN personal_call TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN org_name TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN org_short TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN agency_name TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN agency_short TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN contact_email TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN contact_phone TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN city TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN state TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN county TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN ics_form_variant TEXT DEFAULT 'FEMA'",
        "ALTER TABLE station_config ADD COLUMN logo_data TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN logo_mime TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN software_author TEXT DEFAULT 'James Rospopo KE4CON'",
        "ALTER TABLE station_config ADD COLUMN software_url TEXT DEFAULT 'https://github.com/KE4CON/FieldCommand-IMS'",
        "ALTER TABLE station_config ADD COLUMN setup_complete INTEGER NOT NULL DEFAULT 0",
        "ALTER TABLE station_config ADD COLUMN active_modules TEXT DEFAULT '{}'",
        "ALTER TABLE station_config ADD COLUMN ps_system_name TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN ps_system_type TEXT DEFAULT 'P25'",
        "ALTER TABLE station_config ADD COLUMN ps_id_label TEXT DEFAULT 'Radio ID'",
        "ALTER TABLE station_config ADD COLUMN ps_dispatch TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN ps_system2_name TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN ps_system2_type TEXT DEFAULT ''",
        "ALTER TABLE station_config ADD COLUMN ps_member_id_label TEXT DEFAULT 'EMA ID'",
        "ALTER TABLE station_config ADD COLUMN ps_member_lookup TEXT DEFAULT 'radio_id'",
        "ALTER TABLE incidents ADD COLUMN ics_variant TEXT DEFAULT 'FEMA'",
        "ALTER TABLE net_entries ADD COLUMN ics_position TEXT DEFAULT ''",
        "ALTER TABLE resource_history ADD COLUMN resource_type TEXT DEFAULT ''",
        "ALTER TABLE channel_library ADD COLUMN division TEXT DEFAULT ''",
        "ALTER TABLE channel_library ADD COLUMN function TEXT DEFAULT 'Tactical'",
        "ALTER TABLE general_info ADD COLUMN lat TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN lon TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN sunrise TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN sunset TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN weather_sky TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN deputy_ic TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN resources_unit_ldr TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN situation_unit_ldr TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN documentation_unit_ldr TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN demob_unit_ldr TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN coml_name TEXT DEFAULT ''",
        "ALTER TABLE general_info ADD COLUMN medical_unit_ldr TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN resource_type TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN category TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN leader TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN num_personnel INTEGER DEFAULT 0",
        "ALTER TABLE ics_tcards ADD COLUMN eta TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN notes TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN order_number TEXT DEFAULT ''",
        "ALTER TABLE ics_tcards ADD COLUMN home_agency TEXT DEFAULT ''",
        "ALTER TABLE resource_types ADD COLUMN definition_what TEXT DEFAULT ''",
        "ALTER TABLE resource_types ADD COLUMN definition_std TEXT DEFAULT ''",
        "ALTER TABLE resource_types ADD COLUMN definition_order TEXT DEFAULT ''",
        "ALTER TABLE resource_types ADD COLUMN definition_conf TEXT DEFAULT ''",
        """CREATE TABLE IF NOT EXISTS resource_types (id INTEGER PRIMARY KEY AUTOINCREMENT, nims_id TEXT DEFAULT '', kind TEXT NOT NULL, type_level TEXT DEFAULT '', category TEXT NOT NULL, mission_area TEXT DEFAULT '', description TEXT DEFAULT '', min_personnel INTEGER DEFAULT 0, capabilities TEXT DEFAULT '', metric_notes TEXT DEFAULT '', custom INTEGER DEFAULT 0, active INTEGER DEFAULT 1)""",
        """CREATE TABLE IF NOT EXISTS hospitals (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL DEFAULT '', address TEXT DEFAULT '', city TEXT DEFAULT '', state TEXT DEFAULT '', county TEXT DEFAULT '', phone TEXT DEFAULT '', phone2 TEXT DEFAULT '', fax TEXT DEFAULT '', lat REAL, lon REAL, trauma_level TEXT DEFAULT '', burn_center INTEGER DEFAULT 0, helipad INTEGER DEFAULT 1, icu INTEGER DEFAULT 0, peds_trauma INTEGER DEFAULT 0, stroke_center INTEGER DEFAULT 0, cardiac_center INTEGER DEFAULT 0, travel_time_min INTEGER DEFAULT 0, notes TEXT DEFAULT '', active INTEGER DEFAULT 1)""",
        """CREATE TABLE IF NOT EXISTS ics_meetings (id TEXT PRIMARY KEY, incident_id TEXT NOT NULL DEFAULT '', period INTEGER NOT NULL DEFAULT 1, meeting_type TEXT NOT NULL, title TEXT NOT NULL DEFAULT '', scheduled_time TEXT, location TEXT DEFAULT '', chair TEXT DEFAULT '', attendees TEXT DEFAULT '[]', agenda_items TEXT DEFAULT '[]', status TEXT DEFAULT 'scheduled', notes TEXT DEFAULT '', created TEXT NOT NULL, updated TEXT NOT NULL)""",
    ]
    for sql in migrations:
        try:
            conn.execute(sql)
        except Exception:
            pass  # column already exists
    conn.commit()
    seed_hospitals(conn)
    seed_resource_types(conn)
    seed_channel_library(conn)
    log.info(f"Database initialised: {DB_PATH}")




# ── NIMS Resource Type seeding ────────────────────────────────────────────────
def seed_resource_types(conn)
    seed_channel_library(conn):
    try:
        existing = conn.execute("SELECT COUNT(*) FROM resource_types").fetchone()[0]
        if existing == 0:
            from nims_resource_types import NIMS_RESOURCE_TYPES
            from nims_definitions import NIMS_DEFINITIONS
            for rt in NIMS_RESOURCE_TYPES:
                nims_id = rt[0]
                defn = NIMS_DEFINITIONS.get(nims_id, {})
                conn.execute("""INSERT INTO resource_types
                    (nims_id,kind,type_level,category,mission_area,description,
                     min_personnel,capabilities,metric_notes,
                     definition_what,definition_std,definition_order,definition_conf,
                     custom)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,0)""",
                    (*rt,
                     defn.get('what_it_is',''),
                     defn.get('minimum_standards',''),
                     defn.get('ordering_guidance',''),
                     defn.get('common_confusion','')))
            conn.commit()
            log.info(f"Seeded {len(NIMS_RESOURCE_TYPES)} NIMS resource types with definitions")
    except Exception as e:
        log.warning(f"Resource type seeding skipped: {e}")

# ── JSON migration ─────────────────────────────────────────────────────────────
def _migrate_json_file(path: Path, label: str, fn):
    """Load a JSON file, call fn(data), rename file to .migrated."""
    if not path.exists():
        return 0
    try:
        data = json.loads(path.read_text())
        count = fn(data)
        path.rename(path.with_suffix(".migrated"))
        log.info(f"  Migrated {label}: {count} records → {path.name}.migrated")
        return count
    except Exception as e:
        log.warning(f"  Migration error for {label}: {e}")
        return 0


def migrate_from_json():
    """
    One-time migration: import all legacy JSON files into SQLite.
    Each file is renamed to .migrated after import so this only runs once.
    """
    conn = db()
    total = 0
    log.info("Checking for legacy JSON data to migrate…")

    # ── Nets + entries ────────────────────────────────────────────────────────
    nets_dir = DATA / "nets"
    if nets_dir.exists():
        for jf in sorted(nets_dir.glob("*.json")):
            try:
                nd = json.loads(jf.read_text())
                net_id = nd.get("id", jf.stem)
                conn.execute("""
                    INSERT OR IGNORE INTO nets
                    (id,name,type,starcom,drill,active,freq,ncs,created,closed,roster_chips)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    net_id,
                    nd.get("name", ""),
                    nd.get("type", "Amateur"),
                    1 if nd.get("starcom") else 0,
                    1 if nd.get("drill") else 0,
                    1 if nd.get("active", True) else 0,
                    nd.get("freq", ""),
                    nd.get("ncs", ""),
                    nd.get("created", utcnow()),
                    nd.get("closed"),
                    jdump(nd.get("roster_chips", [])),
                ))
                for e in nd.get("entries", []):
                    conn.execute("""
                        INSERT OR IGNORE INTO net_entries
                        (id,net_id,callsign,name,city,state,radio_id,
                         precedence,traffic,remarks,walk_in,timestamp)
                        VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        e.get("id", f"e-{int(time.time()*1000)}"),
                        net_id,
                        e.get("callsign", ""),
                        e.get("name", ""),
                        e.get("city", ""),
                        e.get("state", ""),
                        e.get("radio_id", ""),
                        e.get("precedence", "ROUTINE"),
                        e.get("traffic", ""),
                        e.get("remarks", ""),
                        1 if e.get("walk_in") else 0,
                        e.get("timestamp", utcnow()),
                    ))
                for t in nd.get("traffic", []):
                    conn.execute("""
                        INSERT OR IGNORE INTO net_traffic
                        (id,net_id,msg_number,from_call,to_call,
                         precedence,handling,text,timestamp)
                        VALUES(?,?,?,?,?,?,?,?,?)
                    """, (
                        t.get("id", f"t-{int(time.time()*1000)}"),
                        net_id,
                        t.get("msg_number", ""),
                        t.get("from_call", ""),
                        t.get("to_call", ""),
                        t.get("precedence", "ROUTINE"),
                        t.get("handling", ""),
                        t.get("text", ""),
                        t.get("timestamp", utcnow()),
                    ))
                conn.commit()
                jf.rename(jf.with_suffix(".migrated"))
                total += 1
                log.info(f"  Migrated net: {net_id}")
            except Exception as e:
                log.warning(f"  Net migration error {jf}: {e}")

    # ── Roster ────────────────────────────────────────────────────────────────
    def migrate_roster(data):
        count = 0
        for m in data.get("members", []):
            certs = m.get("certifications", {}) or {}
            equip = m.get("equipment", {}) or {}
            conn.execute("""
                INSERT OR IGNORE INTO roster
                (id,member_id,callsign,radio_id,first_name,last_name,role,phone,email,
                 grid,lat,lon,notes,
                 cert_ics100,cert_ics200,cert_ics300,cert_ics400,
                 cert_ics700,cert_ics800,cert_emcomm1,cert_emcomm2,
                 cert_cpr,cert_first_aid,cert_cert,
                 equip_hf,equip_vhf,equip_digital,equip_packet,equip_pactor,
                 equip_vara_hf,equip_vara_fm,equip_aprs,equip_winlink,
                 equip_go_box,equip_generator,equip_battery,equip_vehicle,
                 created,modified)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,
                       ?,?,?,?,?,?,?,?,?,?,?,
                       ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                m.get("id", f"m-{int(time.time()*1000)}"),
                m.get("member_id", m.get("id", f"m-{int(time.time()*1000)}")),
                m.get("callsign", "").upper(),
                m.get("radio_id", ""),
                m.get("first_name", ""),
                m.get("last_name", ""),
                m.get("role", "Operator"),
                m.get("phone", ""),
                m.get("email", ""),
                m.get("grid", ""),
                m.get("lat"),
                m.get("lon"),
                m.get("notes", ""),
                int(bool(certs.get("ics100"))),
                int(bool(certs.get("ics200"))),
                int(bool(certs.get("ics300"))),
                int(bool(certs.get("ics400"))),
                int(bool(certs.get("ics700"))),
                int(bool(certs.get("ics800"))),
                int(bool(certs.get("emcomm1"))),
                int(bool(certs.get("emcomm2"))),
                int(bool(certs.get("cpr"))),
                int(bool(certs.get("first_aid"))),
                int(bool(certs.get("cert"))),
                int(bool(equip.get("hf"))),
                int(bool(equip.get("vhf"))),
                int(bool(equip.get("digital"))),
                int(bool(equip.get("packet"))),
                int(bool(equip.get("pactor"))),
                int(bool(equip.get("vara_hf"))),
                int(bool(equip.get("vara_fm"))),
                int(bool(equip.get("aprs"))),
                int(bool(equip.get("winlink"))),
                int(bool(equip.get("go_box"))),
                int(bool(equip.get("generator"))),
                int(bool(equip.get("battery"))),
                int(bool(equip.get("vehicle"))),
                m.get("created", utcnow()),
                m.get("modified", utcnow()),
            ))
            count += 1
        for a in data.get("activations", []):
            conn.execute("""
                INSERT OR IGNORE INTO activations
                (id,callsign,net_id,incident_id,role,location,
                 checked_in,checked_out,notes)
                VALUES(?,?,?,?,?,?,?,?,?)
            """, (
                a.get("id", f"a-{int(time.time()*1000)}"),
                a.get("callsign", ""),
                a.get("net_id", ""),
                a.get("incident_id", ""),
                a.get("role", ""),
                a.get("location", ""),
                a.get("checked_in", utcnow()),
                a.get("checked_out"),
                a.get("notes", ""),
            ))
        conn.commit()
        return count

    total += _migrate_json_file(DATA / "roster.json", "roster", migrate_roster)

    # ── Resources ────────────────────────────────────────────────────────────
    def migrate_resources(data):
        for r in (data if isinstance(data, list) else []):
            conn.execute("""
                INSERT OR IGNORE INTO resources
                (id,name,type,capability,status,assignment,contact,notes,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (
                r.get("id", f"r-{int(time.time()*1000)}"),
                r.get("name", ""),
                r.get("type", ""),
                r.get("capability", ""),
                r.get("status", "Available"),
                r.get("assignment", ""),
                r.get("contact", ""),
                r.get("notes", ""),
                r.get("created", utcnow()),
                r.get("updated", utcnow()),
            ))
        conn.commit()
        return len(data) if isinstance(data, list) else 0

    total += _migrate_json_file(DATA / "resources.json", "resources", migrate_resources)

    # ── Map state ─────────────────────────────────────────────────────────────
    def migrate_mapstate(data):
        conn.execute("""
            UPDATE map_state SET shapes=?, markers=?, updated=? WHERE id=1
        """, (jdump(data.get("shapes", [])), jdump(data.get("markers", [])), utcnow()))
        conn.commit()
        return 1

    _migrate_json_file(DATA / "mapstate.json", "mapstate", migrate_mapstate)

    def migrate_resmap(data):
        conn.execute("""
            UPDATE resmap_state SET markers=?, updated=? WHERE id=1
        """, (jdump(data.get("markers", [])), utcnow()))
        conn.commit()
        return 1

    _migrate_json_file(DATA / "resmap.json", "resmap", migrate_resmap)

    # ── DMS state ─────────────────────────────────────────────────────────────
    def migrate_dms(data):
        conn.execute("""
            UPDATE dms_state SET
                state=?, armed_nets=?, threshold_min=?,
                last_activity=?, armed_at=?, triggered_at=?
            WHERE id=1
        """, (
            data.get("state", "disarmed"),
            jdump(data.get("armed_nets", [])),
            data.get("threshold_min", 30),
            data.get("last_activity"),
            data.get("armed_at"),
            data.get("triggered_at"),
        ))
        conn.commit()
        return 1

    _migrate_json_file(DATA / "dms_state.json", "dms_state", migrate_dms)

    # ── Station config ────────────────────────────────────────────────────────
    def migrate_station(data):
        conn.execute("""
            UPDATE station_config SET
                callsign=?, lat=?, lon=?, gps_enabled=?,
                gps_device=?, gps_last_fix=?, configured_at=?
            WHERE id=1
        """, (
            data.get("callsign", "W8EOC"),
            data.get("lat", 42.3247),
            data.get("lon", -88.3822),
            1 if data.get("gps_enabled", True) else 0,
            data.get("gps_device", "/dev/gps0"),
            data.get("gps_last_fix"),
            data.get("configured_at", utcnow()),
        ))
        conn.commit()
        return 1

    _migrate_json_file(DATA / "station_config.json", "station_config", migrate_station)

    # ── Repeaters ────────────────────────────────────────────────────────────
    def migrate_repeaters(data):
        reps = data if isinstance(data, list) else []
        for r in reps:
            conn.execute("""
                INSERT OR IGNORE INTO repeaters
                (callsign,output_freq,input_freq,tone,tone_input,mode,
                 digital_code,city,state,county,lat,lon,status,use_type,
                 ares,races,skywarn,echolink,allstar,sponsor,notes,updated,source)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                r.get("callsign", r.get("Callsign", "")),
                r.get("output_freq", r.get("Frequency", "")),
                r.get("input_freq", r.get("Input", "")),
                r.get("tone", r.get("PL Tone", r.get("Tone", ""))),
                r.get("tone_input", ""),
                r.get("mode", r.get("Mode", "FM")),
                r.get("digital_code", r.get("Digital Code", "")),
                r.get("city", r.get("City", "")),
                r.get("state", r.get("State", "")),
                r.get("county", r.get("County", "")),
                r.get("lat", r.get("Lat")),
                r.get("lon", r.get("Long")),
                r.get("status", r.get("Status", "On-Air")),
                r.get("use", r.get("Use", "Open")),
                1 if r.get("ares", r.get("ARES", "No")) not in ("No", "", False, 0) else 0,
                1 if r.get("races", r.get("RACES", "No")) not in ("No", "", False, 0) else 0,
                1 if r.get("skywarn", r.get("SKYWARN", "No")) not in ("No", "", False, 0) else 0,
                1 if r.get("echolink", r.get("EchoLink", "No")) not in ("No", "", False, 0) else 0,
                1 if r.get("allstar", r.get("AllStar", "No")) not in ("No", "", False, 0) else 0,
                r.get("sponsor", ""),
                r.get("notes", r.get("Notes", "")),
                r.get("updated", utcnow()),
                r.get("source", ""),
            ))
        conn.commit()
        return len(reps)

    total += _migrate_json_file(DATA / "repeaters.json", "repeaters", migrate_repeaters)

    # ── Standalone forms (forms/*.json) ───────────────────────────────────────
    forms_dir = DATA / "forms"
    if forms_dir.exists():
        for jf in forms_dir.glob("*.json"):
            try:
                fd = json.loads(jf.read_text())
                fid = jf.stem
                conn.execute("""
                    INSERT OR IGNORE INTO forms
                    (id,form_type,incident_id,summary,data,created,updated)
                    VALUES(?,?,?,?,?,?,?)
                """, (
                    fid,
                    fd.get("form_type", "unknown"),
                    fd.get("incident_id", ""),
                    fd.get("summary", ""),
                    jdump(fd),
                    fd.get("created", utcnow()),
                    fd.get("updated", fd.get("created", utcnow())),
                ))
                conn.commit()
                jf.rename(jf.with_suffix(".migrated"))
                total += 1
            except Exception as e:
                log.warning(f"  Form migration error {jf}: {e}")

    # ── ICS data ──────────────────────────────────────────────────────────────
    ics_data = DATA / "ics"

    def migrate_incidents(data):
        incs = data if isinstance(data, list) else []
        for inc in incs:
            conn.execute("""
                INSERT OR IGNORE INTO incidents
                (id,name,type,status,jurisdiction,incident_commander,
                 location,summary,current_period,started,updated,closed)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                inc["id"],
                inc.get("name", ""),
                inc.get("type", ""),
                inc.get("status", "active"),
                inc.get("jurisdiction", ""),
                inc.get("incident_commander", ""),
                inc.get("location", ""),
                inc.get("summary", ""),
                inc.get("current_period", 1),
                inc.get("created", utcnow()),
                inc.get("updated"),
                inc.get("closed"),
            ))
        conn.commit()
        return len(incs)

    _migrate_json_file(ics_data / "incidents.json", "incidents", migrate_incidents)

    def migrate_periods(data):
        count = 0
        for inc_id, periods in (data if isinstance(data, dict) else {}).items():
            for p in periods:
                pid = f"per-{inc_id}-{p.get('period', count)}"
                conn.execute("""
                    INSERT OR IGNORE INTO ics_periods
                    (id,incident_id,period_num,started,objectives)
                    VALUES(?,?,?,?,?)
                """, (
                    pid, inc_id,
                    p.get("period", 1),
                    p.get("started", utcnow()),
                    p.get("objectives", ""),
                ))
                count += 1
        conn.commit()
        return count

    _migrate_json_file(ics_data / "periods.json", "ics_periods", migrate_periods)

    def migrate_tcards(data):
        cards = data if isinstance(data, list) else []
        for c in cards:
            conn.execute("""
                INSERT OR IGNORE INTO ics_tcards
                (id,incident_id,resource_id,resource_name,type,
                 status,assignment,contact,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?)
            """, (
                c.get("id", f"tc-{int(time.time()*1000)}"),
                c.get("incident_id", ""),
                c.get("resource_id", ""),
                c.get("resource_name", ""),
                c.get("type", ""),
                c.get("status", "Available"),
                c.get("assignment", ""),
                c.get("contact", ""),
                c.get("created", utcnow()),
                c.get("updated", utcnow()),
            ))
        conn.commit()
        return len(cards)

    _migrate_json_file(ics_data / "tcards.json", "ics_tcards", migrate_tcards)

    def migrate_ics_resources(data):
        items = data if isinstance(data, list) else []
        for r in items:
            conn.execute("""
                INSERT OR IGNORE INTO ics_resources
                (id,incident_id,resource_id,name,type,capability,
                 status,assignment,contact,created,updated)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """, (
                r.get("id", f"icsres-{int(time.time()*1000)}"),
                r.get("incident_id", ""),
                r.get("resource_id", ""),
                r.get("name", ""),
                r.get("type", ""),
                r.get("capability", ""),
                r.get("status", "Available"),
                r.get("assignment", ""),
                r.get("contact", ""),
                r.get("created", utcnow()),
                r.get("updated", utcnow()),
            ))
        conn.commit()
        return len(items)

    _migrate_json_file(ics_data / "ics_resources.json", "ics_resources", migrate_ics_resources)

    def migrate_activity(data):
        entries = data if isinstance(data, list) else []
        for e in entries:
            conn.execute("""
                INSERT INTO activity_log(incident_id,section,action,detail,timestamp)
                VALUES(?,?,?,?,?)
            """, (
                e.get("incident_id", ""),
                e.get("section", ""),
                e.get("action", ""),
                e.get("detail", ""),
                e.get("timestamp", utcnow()),
            ))
        conn.commit()
        return len(entries)

    _migrate_json_file(ics_data / "activity_feed.json", "activity_log", migrate_activity)

    # ── ICS form files ────────────────────────────────────────────────────────
    ics_forms_dir = ics_data / "forms"
    if ics_forms_dir.exists():
        for type_dir in ics_forms_dir.iterdir():
            if type_dir.is_dir():
                form_type = type_dir.name
                for jf in type_dir.glob("*.json"):
                    try:
                        fd = json.loads(jf.read_text())
                        conn.execute("""
                            INSERT OR IGNORE INTO ics_forms
                            (id,incident_id,form_type,period,summary,data,created,updated)
                            VALUES(?,?,?,?,?,?,?,?)
                        """, (
                            jf.stem,
                            fd.get("incident_id", ""),
                            form_type,
                            fd.get("period", 1),
                            fd.get("summary", ""),
                            jdump(fd),
                            fd.get("created", utcnow()),
                            fd.get("updated", fd.get("created", utcnow())),
                        ))
                        conn.commit()
                        jf.rename(jf.with_suffix(".migrated"))
                        total += 1
                    except Exception as e:
                        log.warning(f"  ICS form migration error {jf}: {e}")

    # ── Reference library ─────────────────────────────────────────────────────
    ref_index = DATA / "refs" / "index.json"

    def migrate_refs(data):
        docs = data if isinstance(data, list) else []
        for d in docs:
            conn.execute("""
                INSERT OR IGNORE INTO ref_documents
                (id,title,filename,stored_name,category,sections,description,
                 tags,source,applies_to,revision,expires,content_type,
                 size_bytes,sha256,uploaded,modified,downloads,last_downloaded)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (
                d.get("id", f"ref_{int(time.time()*1000):x}"),
                d.get("title", ""),
                d.get("filename", ""),
                d.get("stored_name", ""),
                d.get("category", "other"),
                jdump(d.get("sections", [d.get("section", "amateur")])),
                d.get("description", ""),
                jdump(d.get("tags", [])),
                d.get("source", ""),
                d.get("applies_to", ""),
                d.get("revision", ""),
                d.get("expires"),
                d.get("content_type", ""),
                d.get("size_bytes", 0),
                d.get("sha256", ""),
                d.get("uploaded", utcnow()),
                d.get("modified"),
                d.get("downloads", 0),
                d.get("last_downloaded"),
            ))
        conn.commit()
        return len(docs)

    _migrate_json_file(ref_index, "ref_documents", migrate_refs)

    # ── Preflight history ─────────────────────────────────────────────────────
    def migrate_preflight(data):
        if isinstance(data, dict):
            data = [data]
        for p in (data if isinstance(data, list) else []):
            conn.execute("""
                INSERT INTO preflight_runs(verdict,checks,timestamp)
                VALUES(?,?,?)
            """, (
                p.get("verdict", "?"),
                jdump(p.get("checks", {})),
                p.get("timestamp", utcnow()),
            ))
        conn.commit()
        return len(data) if isinstance(data, list) else 0

    _migrate_json_file(DATA / "preflight.json", "preflight", migrate_preflight)

    if total:
        log.info(f"Migration complete — {total} records imported")
    else:
        log.info("No legacy JSON files found — starting fresh")


# ── Startup ────────────────────────────────────────────────────────────────────
def startup():
    """Call once at server startup: create schema, run migration."""
    init_db()
    _alter_existing_tables()
    migrate_from_json()
    _seed_defaults()




BUILTIN_TEMPLATES = [
  {
    "id": "shelter",
    "name": "Shelter Activation",
    "icon": "\ud83c\udfe0",
    "type": "Mass Care \u2014 Shelter",
    "sort_order": 1,
    "is_builtin": 1,
    "summary": "Emergency shelter activation for displaced residents.",
    "data": {
      "objectives": [
        "Open and staff emergency shelter within 2 hours of notification.",
        "Register all shelter occupants using ARC or agency registration system.",
        "Provide cots, blankets, food, and water to all occupants.",
        "Screen all occupants for medical needs; refer to medical unit.",
        "Establish security perimeter and check-in/check-out procedure.",
        "Coordinate with Red Cross / voluntary agencies for feeding and supplies.",
        "Provide daily situation reports to EOC every 12 hours."
      ],
      "safety_message": "Ensure all shelter workers complete sign-in. No media access to shelter floor without PIO escort. Report any security concerns immediately to the Shelter Manager.",
      "resources": [
        {
          "name": "Shelter Manager",
          "type": "Personnel",
          "qty": 1
        },
        {
          "name": "Registration Team",
          "type": "Personnel",
          "qty": 4
        },
        {
          "name": "Medical Screener",
          "type": "Personnel",
          "qty": 2
        },
        {
          "name": "Security Personnel",
          "type": "Personnel",
          "qty": 2
        },
        {
          "name": "Cots (sets of 50)",
          "type": "Equipment",
          "qty": 4
        },
        {
          "name": "Blanket Packs",
          "type": "Equipment",
          "qty": 200
        }
      ],
      "channels": [
        {
          "name": "Shelter Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "Medical",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Medical"
        }
      ],
      "org": {
        "ops_section_chief": "Shelter Manager",
        "safety_officer": "Safety Officer",
        "public_info_officer": "PIO \u2014 coordinate all media at EOC",
        "branch1_label": "Shelter Operations",
        "div_a_label": "Registration / Check-In",
        "div_b_label": "Feeding / Supplies",
        "div_c_label": "Medical Screening",
        "div_d_label": "Security"
      }
    }
  },
  {
    "id": "sar",
    "name": "Search & Rescue",
    "icon": "\ud83d\udd26",
    "type": "SAR",
    "sort_order": 2,
    "is_builtin": 1,
    "summary": "Search and Rescue operation for missing subject(s).",
    "data": {
      "objectives": [
        "Establish ICP and communications within 30 minutes of activation.",
        "Obtain all available information on missing subject(s): description, last known point (LKP), travel plans.",
        "Assign search teams to high-probability areas first.",
        "Maintain radio contact with all field teams at minimum 30-minute intervals.",
        "Establish medical staging area and coordinate with receiving hospital.",
        "Preserve evidence integrity in all search areas.",
        "Brief family liaison every hour on search progress.",
        "Document all negative search areas with GPS track logs."
      ],
      "safety_message": "All field teams must check in and check out with Base Camp. No solo searchers. All personnel must have personal locator beacon or GPS tracker. Establish STOP protocol if searcher is overdue.",
      "resources": [
        {
          "name": "SAR Team Alpha",
          "type": "Crew",
          "qty": 6
        },
        {
          "name": "SAR Team Bravo",
          "type": "Crew",
          "qty": 6
        },
        {
          "name": "K9 Unit",
          "type": "Crew",
          "qty": 2
        },
        {
          "name": "Medical Unit",
          "type": "Personnel",
          "qty": 2
        },
        {
          "name": "Family Liaison",
          "type": "Personnel",
          "qty": 1
        },
        {
          "name": "Base Camp ATV",
          "type": "Vehicle",
          "qty": 2
        }
      ],
      "channels": [
        {
          "name": "SAR Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "SAR Tactical",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Tactical"
        },
        {
          "name": "Medical",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Medical"
        }
      ],
      "org": {
        "ops_section_chief": "Operations Section Chief",
        "safety_officer": "SAR Safety Officer",
        "public_info_officer": "PIO \u2014 no subject info to media without IC approval",
        "branch1_label": "Field Search",
        "div_a_label": "Grid Search Alpha (High Probability Area)",
        "div_b_label": "Grid Search Bravo",
        "div_c_label": "K9 Search",
        "div_d_label": "Medical / Base Camp"
      }
    }
  },
  {
    "id": "severe_weather",
    "name": "Severe Weather",
    "icon": "\u26c8",
    "type": "Severe Weather Response",
    "sort_order": 3,
    "is_builtin": 1,
    "summary": "Response to severe weather event \u2014 tornado, flooding, or winter storm.",
    "data": {
      "objectives": [
        "Activate EOC to Level 2 / Level 3 as warranted by NWS warnings.",
        "Monitor NWS alerts continuously; brief IC on all new watches and warnings.",
        "Coordinate shelter-in-place or evacuation orders with jurisdiction leadership.",
        "Establish damage assessment teams for post-event windshield survey.",
        "Coordinate road closures with Public Works and law enforcement.",
        "Assess utility outages; coordinate with electric, gas, and water utilities.",
        "Activate warming / cooling centers as weather dictates.",
        "Submit initial damage report to state EM within 4 hours of event."
      ],
      "safety_message": "No personnel in the field during tornado warning. All outdoor operations suspend during lightning within 10 miles. Use Wireless Emergency Alerts as primary public warning system.",
      "resources": [
        {
          "name": "EOC Team",
          "type": "Personnel",
          "qty": 6
        },
        {
          "name": "Damage Assessment",
          "type": "Personnel",
          "qty": 4
        },
        {
          "name": "Field Liaison",
          "type": "Vehicle",
          "qty": 2
        },
        {
          "name": "Generator (50kW)",
          "type": "Equipment",
          "qty": 1
        }
      ],
      "channels": [
        {
          "name": "EOC Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "Field Ops",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Tactical"
        }
      ],
      "org": {
        "ops_section_chief": "Operations Chief",
        "safety_officer": "Safety Officer",
        "public_info_officer": "PIO \u2014 coordinate with NWS for public messaging",
        "branch1_label": "Field Operations",
        "div_a_label": "Damage Assessment North",
        "div_b_label": "Damage Assessment South",
        "div_c_label": "Road Closures / Traffic",
        "div_d_label": "Utilities Coordination"
      }
    }
  },
  {
    "id": "mass_gathering",
    "name": "Mass Gathering / Event",
    "icon": "\ud83d\udc65",
    "type": "Mass Gathering \u2014 Planned Event",
    "sort_order": 4,
    "is_builtin": 1,
    "summary": "Medical and safety coverage for a planned mass gathering event.",
    "data": {
      "objectives": [
        "Establish first aid stations at designated locations prior to event start.",
        "Maintain adequate EMS staffing for anticipated crowd size.",
        "Coordinate with venue security and law enforcement on crowd management plan.",
        "Establish direct communication link with receiving hospitals.",
        "Conduct patient transport to hospital when first aid capacity is exceeded.",
        "Monitor crowd density and advise IC on ingress / egress issues.",
        "Brief all medical personnel on mass casualty protocol prior to event."
      ],
      "safety_message": "Know the MCI activation threshold for this event. All first aid personnel must have valid CPR and first aid certification. Identify nearest AED locations at event start.",
      "resources": [
        {
          "name": "First Aid Station Alpha",
          "type": "Personnel",
          "qty": 3
        },
        {
          "name": "First Aid Station Bravo",
          "type": "Personnel",
          "qty": 3
        },
        {
          "name": "Roving Medical",
          "type": "Personnel",
          "qty": 2
        },
        {
          "name": "EMS Unit",
          "type": "Vehicle",
          "qty": 1
        },
        {
          "name": "Security Liaison",
          "type": "Personnel",
          "qty": 1
        }
      ],
      "channels": [
        {
          "name": "Medical Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "Venue Security",
          "rx": "",
          "tx": "",
          "tone": "",
          "mode": "FM",
          "function": "Liaison"
        }
      ],
      "org": {
        "ops_section_chief": "Event Medical Director",
        "safety_officer": "Safety Officer",
        "public_info_officer": "Venue PIO (coordinate)",
        "branch1_label": "Medical Operations",
        "div_a_label": "First Aid Stations",
        "div_b_label": "EMS Transport",
        "div_c_label": "Security Liaison"
      }
    }
  },
  {
    "id": "hazmat",
    "name": "HazMat / Spill",
    "icon": "\u2623",
    "type": "HazMat Response",
    "sort_order": 5,
    "is_builtin": 1,
    "summary": "Hazardous materials release \u2014 chemical, biological, or radiological.",
    "data": {
      "objectives": [
        "Identify material(s) involved using placards, shipping papers, MSDS, or CHEMTREC.",
        "Establish hot / warm / cold zones; keep all non-HazMat personnel out of hot zone.",
        "Establish decontamination corridor before any entry team deployment.",
        "Notify CHEMTREC (1-800-424-9300), state environmental agency, and EPA as required.",
        "Coordinate evacuation or shelter-in-place for affected area.",
        "Establish medical monitoring for all entry personnel.",
        "Document all personnel entries into hot zone on ICS-214."
      ],
      "safety_message": "Level A / B / C PPE required in hot and warm zones as determined by HazMat Group Supervisor. No personnel enter hot zone without buddy system and backup team staged. Decon all personnel before leaving warm zone.",
      "resources": [
        {
          "name": "HazMat Entry Team",
          "type": "Crew",
          "qty": 4
        },
        {
          "name": "Decon Team",
          "type": "Crew",
          "qty": 4
        },
        {
          "name": "Medical Monitor",
          "type": "Personnel",
          "qty": 2
        },
        {
          "name": "HazMat Unit",
          "type": "Vehicle",
          "qty": 1
        },
        {
          "name": "Decon Trailer",
          "type": "Vehicle",
          "qty": 1
        }
      ],
      "channels": [
        {
          "name": "HazMat Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "Entry Team",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Tactical"
        },
        {
          "name": "Medical",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Medical"
        }
      ],
      "org": {
        "ops_section_chief": "HazMat Group Supervisor",
        "safety_officer": "HazMat Safety Officer",
        "public_info_officer": "PIO \u2014 no material ID to media without IC clearance",
        "branch1_label": "HazMat Operations",
        "div_a_label": "Entry Team",
        "div_b_label": "Decontamination",
        "div_c_label": "Medical Monitoring",
        "div_d_label": "Evacuation / Perimeter"
      }
    }
  },
  {
    "id": "planned_exercise",
    "name": "Planned Exercise / Drill",
    "icon": "\ud83c\udfaf",
    "type": "Exercise / Training",
    "sort_order": 6,
    "is_builtin": 1,
    "summary": "Training exercise or tabletop drill with scenario objectives.",
    "data": {
      "objectives": [
        "EXERCISE \u2014 THIS IS AN EXERCISE \u2014 ALL TRANSMISSIONS ARE EXERCISE TRAFFIC ONLY.",
        "Evaluate capability: [specify capability being tested].",
        "Identify gaps in plans, procedures, or equipment.",
        "Test interoperability with partner agencies.",
        "Complete all exercise injects on schedule.",
        "Conduct hot wash with all participants within 1 hour of exercise conclusion.",
        "Submit After-Action Report (AAR) within 30 days of exercise."
      ],
      "safety_message": "EXERCISE \u2014 THIS IS AN EXERCISE. All radio traffic must include EXERCISE at beginning and end. If a real emergency occurs during the exercise, use code word REAL WORLD and all exercise activity ceases immediately.",
      "resources": [
        {
          "name": "Exercise Director",
          "type": "Personnel",
          "qty": 1
        },
        {
          "name": "Evaluators",
          "type": "Personnel",
          "qty": 3
        },
        {
          "name": "Players",
          "type": "Personnel",
          "qty": 10
        },
        {
          "name": "Safety Officer",
          "type": "Personnel",
          "qty": 1
        }
      ],
      "channels": [
        {
          "name": "Exercise Command",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Command"
        },
        {
          "name": "Control Net",
          "rx": "155.3400",
          "tx": "155.3400",
          "tone": "",
          "mode": "FM",
          "function": "Other"
        }
      ],
      "org": {
        "ops_section_chief": "Exercise Director",
        "safety_officer": "Safety Officer",
        "public_info_officer": "Exercise Controller",
        "branch1_label": "Exercise Play",
        "div_a_label": "Functional Area Alpha",
        "div_b_label": "Functional Area Bravo"
      },
      "is_scenario": true
    }
  }
]


def seed_incident_templates(conn):
    """Seed built-in event templates if table is empty."""
    if conn.execute("SELECT COUNT(*) FROM incident_templates").fetchone()[0] > 0:
        return
    now = datetime.utcnow().isoformat()
    for t in BUILTIN_TEMPLATES:
        conn.execute(
            "INSERT INTO incident_templates "
            "(id,name,icon,type,summary,sort_order,is_builtin,enabled,data,created,updated) "
            "VALUES (?,?,?,?,?,?,1,1,?,?,?)",
            (t["id"], t["name"], t["icon"], t["type"], t["summary"],
             t.get("sort_order",99), json.dumps(t["data"]), now, now)
        )
    conn.commit()
    log.info(f"Seeded {len(BUILTIN_TEMPLATES)} built-in event templates")

def seed_fema_equipment_rates(conn):
    """
    Seed common emergency management equipment rates from the
    FEMA 2025 Schedule of Equipment Rates (effective July 1, 2025).
    Rates cover applicant-owned equipment — labor NOT included.
    Source: fema.gov/assistance/public/tools-resources/schedule-equipment-rates
    Only runs if the table is empty; does not overwrite agency customizations.
    """
    if conn.execute("SELECT COUNT(*) FROM fema_equipment_rates").fetchone()[0] > 0:
        return

    RATE_YEAR = 2025
    RATES = [
        # (code, category, description, unit, rate)
        # Vehicles
        ("5-1-1",  "Vehicles",    "Pickup Truck, < 1 Ton",                        "hour", 17.95),
        ("5-1-2",  "Vehicles",    "Pickup Truck, 1 Ton 4WD",                      "hour", 21.58),
        ("5-1-3",  "Vehicles",    "Pickup Truck, w/ Service Body",                 "hour", 25.64),
        ("5-2-1",  "Vehicles",    "SUV / Patrol Vehicle",                          "hour", 22.41),
        ("5-3-1",  "Vehicles",    "Cargo Van",                                     "hour", 19.87),
        ("5-4-1",  "Vehicles",    "Bus, School Type (< 35 passengers)",            "hour", 34.20),
        ("5-4-2",  "Vehicles",    "Bus, Transit Type (> 35 passengers)",           "hour", 52.15),
        ("5-5-1",  "Vehicles",    "ATV / UTV, 2-Seat",                             "hour", 14.35),
        ("5-5-2",  "Vehicles",    "ATV / UTV, 4-6 Seat",                           "hour", 19.40),
        # Trucks
        ("8-7-1",  "Trucks",      "Truck, Dump, 7 CY",                             "hour", 55.28),
        ("8-8-1",  "Trucks",      "Truck, Flatbed",                                "hour", 31.47),
        ("8-9-1",  "Trucks",      "Truck, Tanker",                                 "hour", 38.95),
        # Generators
        ("6-1-1",  "Generators",  "Generator, < 2 kW, portable",                  "hour",  3.50),
        ("6-1-2",  "Generators",  "Generator, 2-5 kW",                             "hour",  5.20),
        ("6-1-3",  "Generators",  "Generator, 5-10 kW",                            "hour",  7.85),
        ("6-1-4",  "Generators",  "Generator, 10-25 kW",                           "hour", 12.40),
        ("6-1-5",  "Generators",  "Generator, 25-50 kW",                           "hour", 18.30),
        ("6-1-6",  "Generators",  "Generator, 50-100 kW",                          "hour", 28.65),
        ("6-1-7",  "Generators",  "Generator, 100-200 kW",                         "hour", 41.20),
        ("6-1-8",  "Generators",  "Generator, 200-500 kW",                         "hour", 72.45),
        # Pumps
        ("6-5-1",  "Pumps",       "Pump, Trash, 2-inch",                           "hour",  7.60),
        ("6-5-2",  "Pumps",       "Pump, Trash, 4-inch",                           "hour", 11.35),
        ("6-5-3",  "Pumps",       "Pump, Trash, 6-inch",                           "hour", 18.90),
        ("6-5-4",  "Pumps",       "Pump, Centrifugal, 4-inch",                     "hour", 12.45),
        # Boats
        ("9-1-1",  "Watercraft",  "Boat, Aluminum, < 14 ft (tiller)",              "hour", 14.20),
        ("9-1-2",  "Watercraft",  "Boat, Aluminum, 14-20 ft",                      "hour", 22.65),
        ("9-1-3",  "Watercraft",  "Boat, Inflatable / Zodiac",                     "hour", 19.40),
        ("9-2-1",  "Watercraft",  "Jet Ski / PWC, < 3 passengers",                 "hour", 21.85),
        # Heavy equipment
        ("1-1-1",  "Heavy",       "Bulldozer / Dozer, < 75 HP",                   "hour", 89.50),
        ("1-1-2",  "Heavy",       "Bulldozer / Dozer, 75-150 HP",                 "hour",139.75),
        ("1-1-3",  "Heavy",       "Bulldozer / Dozer, > 150 HP",                  "hour",189.40),
        ("1-3-1",  "Heavy",       "Excavator / Trackhoe, < 60 HP",                "hour", 95.20),
        ("1-3-2",  "Heavy",       "Excavator / Trackhoe, 60-130 HP",              "hour",148.60),
        ("1-5-1",  "Heavy",       "Loader, Wheel, < 80 HP",                        "hour", 87.30),
        ("1-5-2",  "Heavy",       "Loader, Wheel, 80-150 HP",                      "hour",118.45),
        ("1-7-1",  "Heavy",       "Skid Steer Loader",                             "hour", 48.75),
        # Communications / misc
        ("7-1-1",  "Communications", "Radio, Portable (handheld)",                 "day",   5.40),
        ("7-1-2",  "Communications", "Radio, Mobile (vehicle mounted)",            "day",   9.85),
        ("7-2-1",  "Communications", "Satellite Phone / Terminal",                 "day",  42.00),
        ("7-3-1",  "Communications", "Generator, Light Tower",                     "hour", 14.85),
        # Trailers
        ("8-1-1",  "Trailers",    "Trailer, Utility, < 1 Ton",                     "hour",  4.25),
        ("8-1-2",  "Trailers",    "Trailer, Utility, 1-3 Ton",                     "hour",  7.40),
        ("8-2-1",  "Trailers",    "Trailer, Equipment (flatbed)",                  "hour", 12.75),
        # Chainsaws / hand tools
        ("3-1-1",  "Tools",       "Chainsaw, < 20-inch bar",                       "hour",  4.85),
        ("3-1-2",  "Tools",       "Chainsaw, > 20-inch bar",                       "hour",  6.40),
    ]

    for code, cat, desc, unit, rate in RATES:
        conn.execute(
            "INSERT INTO fema_equipment_rates (code,category,description,unit,rate,rate_year) "
            "VALUES (?,?,?,?,?,?)",
            (code, cat, desc, unit, rate, RATE_YEAR)
        )
    conn.commit()
    log.info(f"Seeded {len(RATES)} FEMA 2025 equipment rates")

def _seed_defaults():
    """Seed default McHenry County facilities if facilities table is empty."""
    conn = db()
    # Facilities are stored as resources with type='Facility'
    n = conn.execute(
        "SELECT COUNT(*) FROM resources WHERE type='Facility'"
    ).fetchone()[0]
    if n > 0:
        return  # Already seeded

    defaults = [
        ("McHenry County EOC", "Facility",
         "Primary Emergency Operations Center",
         "667 Ware Rd, Woodstock IL 60098 · Sheriff frequency: 154.785 MHz / 107.2 Hz",
         "available"),
        ("Centegra Hospital — Woodstock", "Facility",
         "Hospital / Mass Casualty staging",
         "3701 Doty Rd, Woodstock IL 60098 · ER entrance on north side",
         "available"),
        ("McHenry County Fairgrounds — Staging", "Facility",
         "Primary staging area / personnel assembly",
         "11900 IL-Route 14, Woodstock IL 60098 · Use Gate 3",
         "available"),
        ("Centegra Hospital — McHenry", "Facility",
         "Secondary hospital / alternate staging",
         "4201 Medical Center Dr, McHenry IL 60050",
         "available"),
    ]
    now = utcnow()
    for name, rtype, capability, notes, status in defaults:
        rid = f"fac-{int(__import__('time').time()*1000) % 1000000}"
        conn.execute("""
            INSERT OR IGNORE INTO resources
            (id,name,type,capability,status,assignment,contact,notes,created,updated)
            VALUES(?,?,?,?,?,?,?,?,?,?)
        """, (rid, name, rtype, capability, status, "", "", notes, now, now))
        __import__('time').sleep(0.001)  # ensure unique IDs
    conn.commit()
    log.info("Seeded 4 default McHenry County facilities")


def _alter_existing_tables():
    """Add new columns to existing databases that predate this version."""
    conn = db()
    existing = {r[1] for r in conn.execute("PRAGMA table_info(roster)").fetchall()}
    additions = [
        ("member_id",      "TEXT NOT NULL DEFAULT ''"),
        ("radio_id",       "TEXT DEFAULT ''"),
        ("member_type",    "TEXT NOT NULL DEFAULT 'member'"),
        ("visitor_agency", "TEXT DEFAULT ''"),
    ]
    for col, defn in additions:
        if col not in existing:
            try:
                conn.execute(f"ALTER TABLE roster ADD COLUMN {col} {defn}")
                conn.commit()
                log.info(f"Added column roster.{col}")
            except Exception as e:
                log.warning(f"Could not add column {col}: {e}")

    # ics_tcards — GPS tracking fields
    tc2_existing = {r[1] for r in conn.execute("PRAGMA table_info(ics_tcards)").fetchall()}
    gps_additions = [
        ("lat",           "REAL DEFAULT NULL"),   -- current GPS latitude
        ("lon",           "REAL DEFAULT NULL"),   -- current GPS longitude
        ("gps_updated",   "TEXT DEFAULT ''"),     -- timestamp of last GPS update
        ("gps_source",    "TEXT DEFAULT ''"),     -- 'device','manual','aprs'
        ("location_label","TEXT DEFAULT ''"),     -- human label e.g. 'Division Alpha staging'
    ]
    for col, defn in gps_additions:
        if col not in tc2_existing:
            try:
                conn.execute(f"ALTER TABLE ics_tcards ADD COLUMN {col} {defn.split('--')[0].strip()}")
                conn.commit()
            except Exception as e:
                log.warning(f"ics_tcards.{col}: {e}")

    # ics_tcards — cost rate fields for cost dashboard
    tc_existing = {r[1] for r in conn.execute("PRAGMA table_info(ics_tcards)").fetchall()}
    tc_additions = [
        ("daily_cost",   "REAL DEFAULT 0"),   -- $/day for this resource
        ("hourly_rate",  "REAL DEFAULT 0"),   -- $/hr (alternative to daily)
        ("cost_basis",   "TEXT DEFAULT ''"),  -- 'daily','hourly','contract','donated'
        ("hours_on_incident", "REAL DEFAULT 0"),
    ]
    for col, defn in tc_additions:
        if col not in tc_existing:
            try:
                conn.execute(f"ALTER TABLE ics_tcards ADD COLUMN {col} {defn.split('--')[0].strip()}")
                conn.commit()
            except Exception as e:
                log.warning(f"ics_tcards.{col}: {e}")

    # incidents — archive support
    inc_existing = {r[1] for r in conn.execute("PRAGMA table_info(incidents)").fetchall()}
    inc_additions = [
        ("archived",      "INTEGER NOT NULL DEFAULT 0"),
        ("archive_path",  "TEXT DEFAULT ''"),
        ("archived_at",   "TEXT DEFAULT ''"),
        ("is_scenario",   "INTEGER NOT NULL DEFAULT 0"),  -- beta/training scenario flag
    ]
    for col, defn in inc_additions:
        if col not in inc_existing:
            try:
                conn.execute(f"ALTER TABLE incidents ADD COLUMN {col} {defn.split('--')[0].strip()}")
                conn.commit()
            except Exception as e:
                log.warning(f"incidents.{col}: {e}")

    # roster — barcode/QR check-in support
    ros_existing = {r[1] for r in conn.execute("PRAGMA table_info(roster)").fetchall()}
    if 'barcode_id' not in ros_existing:
        try:
            # barcode_id: unique scan code for this member — defaults to member_id
            # Can be overridden with a facility badge number or custom ID
            conn.execute("ALTER TABLE roster ADD COLUMN barcode_id TEXT DEFAULT ''")
            # Backfill: set barcode_id = member_id for existing members
            conn.execute("UPDATE roster SET barcode_id = member_id WHERE barcode_id = '' OR barcode_id IS NULL")
            conn.commit()
            log.info("Added roster.barcode_id column and backfilled from member_id")
        except Exception as e:
            log.warning(f"roster.barcode_id: {e}")

    # net_entries new columns
    ne_existing = {r[1] for r in conn.execute("PRAGMA table_info(net_entries)").fetchall()}
    ne_additions = [
        ("member_id",      "TEXT DEFAULT ''"),
        ("visitor_agency", "TEXT DEFAULT ''"),
        ("visitor",        "INTEGER NOT NULL DEFAULT 0"),
        ("promoted",       "INTEGER NOT NULL DEFAULT 0"),
    ]
    for col, defn in ne_additions:
        if col not in ne_existing:
            try:
                conn.execute(f"ALTER TABLE net_entries ADD COLUMN {col} {defn}")
                conn.commit()
                log.info(f"Added column net_entries.{col}")
            except Exception as e:
                log.warning(f"Could not add net_entries.{col}: {e}")

# ── Default hospital seeding ──────────────────────────────────────────────────
DEFAULT_HOSPITALS = []
# Hospital database is empty by default.
# Add your local hospitals via the Hospital Proximity page (hospitals.html)
# or import from CSV using the Export/Import buttons.
# Any agency deploying FieldCommand IMS should populate this with
# hospitals relevant to their jurisdiction — trauma centers, burn centers,
# and community EDs within their typical response area.
# Fields: name, address, city, state, county, phone, lat, lon,
#         trauma_level, burn_center, helipad, travel_time_min, notes


def seed_hospitals(conn):
    try:
        existing = conn.execute("SELECT COUNT(*) FROM hospitals").fetchone()[0]
        if existing == 0:
            for h in DEFAULT_HOSPITALS:
                conn.execute(
                    "INSERT INTO hospitals (name,address,city,state,county,phone,lat,lon,"
                    "trauma_level,burn_center,helipad,travel_time_min,notes) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", h)
            conn.commit()
            log.info(f"Seeded {len(DEFAULT_HOSPITALS)} default hospitals")
    except Exception as e:
        log.warning(f"Hospital seeding skipped: {e}")
