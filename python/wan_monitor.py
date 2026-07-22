# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""
wan_monitor.py — WAN Status Monitor
Polls configured WAN sources every 30 seconds.
Config: /opt/fieldcommand/data/wan_config.json
Fallback: python/wan_config_defaults.json

Each WAN source has a role — 'preferred' or 'fallback'.
The preferred source is tried first. If it's down or not detected,
the fallback source is used. Either source can be cellular, satellite,
fixed ISP, hotspot, or any other type. No assumptions about which
slot is which technology.

Supports up to 2 WAN sources (easily extended to 3+).
"""

import json
import re
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE          = Path("/opt/fieldcommand")
DATA          = BASE / "data"
OUTPUT_FILE   = DATA / "wan_status.json"
CONFIG_FILE   = DATA / "wan_config.json"
DEFAULTS_FILE = Path(__file__).parent / "wan_config_defaults.json"
POLL_INTERVAL = 30  # seconds

TYPE_ICONS = {
    "cellular":  "📡",
    "satellite": "🛰",
    "fixed":     "🌐",
    "hotspot":   "📱",
    "other":     "🔗",
}


def load_config():
    """Load WAN config — site config first, fallback to defaults."""
    for path in [CONFIG_FILE, DEFAULTS_FILE]:
        try:
            with open(path) as f:
                cfg = json.load(f)
            # Migrate old primary_wan/secondary_wan format to wan_sources array
            if "primary_wan" in cfg and "wan_sources" not in cfg:
                cfg = _migrate_old_config(cfg)
            return cfg
        except Exception:
            pass
    # Absolute bare minimum
    return {
        "wan_sources": [
            {"id": "source_a", "enabled": True, "role": "preferred",
             "label": "Internet", "type": "cellular", "icon": "📡",
             "detection_method": "internet_only"},
        ],
        "dashboard": {"show_wan_a": True, "show_wan_b": False, "show_amprnet": True},
    }


def _migrate_old_config(cfg):
    """Convert old primary_wan/secondary_wan keys to wan_sources array."""
    p = cfg.get("primary_wan", {})
    s = cfg.get("secondary_wan", {})
    sources = [
        {
            "id": "source_a",
            "enabled":          p.get("enabled", True),
            "role":             "preferred",
            "label":            p.get("label", "Primary WAN"),
            "type":             "cellular",
            "provider":         p.get("provider", ""),
            "icon":             p.get("icon", "📡"),
            "detection_method": p.get("detection_method", "internet_only"),
            "ping_host":        p.get("ping_host", ""),
            "admin_url":        p.get("admin_url", ""),
            "admin_timeout_s":  p.get("admin_timeout_s", 3),
        },
        {
            "id": "source_b",
            "enabled":          s.get("enabled", False),
            "role":             "fallback",
            "label":            s.get("label", "Secondary WAN"),
            "type":             "satellite",
            "provider":         s.get("provider", ""),
            "icon":             s.get("icon", "🛰"),
            "detection_method": s.get("detection_method", "ping"),
            "ping_host":        s.get("ping_host", ""),
            "admin_url":        s.get("admin_url", ""),
            "admin_timeout_s":  s.get("admin_timeout_s", 2),
        },
    ]
    cfg["wan_sources"] = sources
    return cfg


def utcnow():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ping_test(host, count=2, timeout=3):
    """Return (success, avg_ms)."""
    try:
        result = subprocess.run(
            ["ping", "-c", str(count), "-W", str(timeout), host],
            capture_output=True, text=True, timeout=timeout * count + 2
        )
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "avg" in line and "/" in line:
                    try:
                        return True, round(float(line.split("/")[4]), 1)
                    except (IndexError, ValueError):
                        pass
            return True, None
        return False, None
    except Exception:
        return False, None


def http_test(url, timeout=5):
    """Return (reachable, response_ms, body)."""
    try:
        start = time.time()
        req   = urllib.request.Request(url, headers={"User-Agent": "FieldCommand/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(8192).decode(errors="ignore")
            return True, round((time.time() - start) * 1000, 1), body
    except Exception:
        return False, None, ""


def check_source(source):
    """
    Test whether a WAN source is currently reachable.
    Returns True/False based on detection_method.
    """
    method = source.get("detection_method", "internet_only")
    if method == "internet_only":
        return True   # caller already confirmed internet is up
    elif method == "ping":
        host = source.get("ping_host", "")
        if not host:
            return False
        ok, _ = ping_test(host, count=1, timeout=2)
        return ok
    elif method == "admin_reachable":
        url = source.get("admin_url", "")
        if not url:
            return False
        ok, _, _ = http_test(url, timeout=source.get("admin_timeout_s", 3))
        return ok
    return False


def get_source_details(source):
    """
    Poll a WAN source for signal/carrier/throughput details.
    Returns a status dict — works for any source type.
    """
    result = {
        "id":        source.get("id", ""),
        "label":     source.get("label", "WAN"),
        "type":      source.get("type", "other"),
        "provider":  source.get("provider", ""),
        "role":      source.get("role", "preferred"),
        "icon":      source.get("icon") or TYPE_ICONS.get(source.get("type", "other"), "🔗"),
        "connected": False,
        "enabled":   source.get("enabled", True),
        "detection_method": source.get("detection_method", "internet_only"),
    }

    # Try admin page for richer detail
    admin_url = source.get("admin_url", "")
    if admin_url:
        ok, _, body = http_test(admin_url, timeout=source.get("admin_timeout_s", 4))
        if ok:
            result["connected"] = True
            result["admin_reachable"] = True

            # Carrier name (cellular sources)
            common_carriers = ["T-Mobile", "Verizon", "AT&T", "FirstNet",
                               "US Cellular", "C Spire", "Sprint", "Dish"]
            for carrier in common_carriers:
                if carrier.lower() in body.lower():
                    result["carrier"] = carrier
                    break

            # Technology (cellular)
            for tech in ["5G NR", "5G", "LTE", "4G", "3G", "2G"]:
                if tech in body:
                    result["technology"] = tech
                    break

            # RSSI signal strength
            rssi_m = re.search(r"rssi[\":\s]+(-?\d+)", body, re.I)
            if rssi_m:
                rssi = int(rssi_m.group(1))
                result["signal_dbm"] = rssi
                result["signal_strength"] = (
                    f"Excellent ({rssi} dBm)" if rssi >= -70 else
                    f"Good ({rssi} dBm)"      if rssi >= -85 else
                    f"Fair ({rssi} dBm)"      if rssi >= -100 else
                    f"Poor ({rssi} dBm)"
                )

            # Satellite throughput (Starlink gRPC / similar JSON APIs)
            lat_m = re.search(r'"popPingLatencyMs":\s*([\d.]+)', body)
            dl_m  = re.search(r'"downlinkThroughputBps":\s*([\d.]+)', body)
            ul_m  = re.search(r'"uplinkThroughputBps":\s*([\d.]+)', body)
            obs_m = re.search(r'"fractionObstructed":\s*([\d.]+)', body)
            up_m  = re.search(r'"uptimeS":\s*(\d+)', body)
            if lat_m: result["latency_ms"]      = round(float(lat_m.group(1)), 1)
            if dl_m:  result["download_mbps"]   = round(float(dl_m.group(1)) / 1e6, 1)
            if ul_m:  result["upload_mbps"]     = round(float(ul_m.group(1)) / 1e6, 1)
            if obs_m: result["obstruction_pct"] = round(float(obs_m.group(1)) * 100, 1)
            if up_m:
                secs = int(up_m.group(1))
                result["uptime"] = f"{secs//3600}h {(secs%3600)//60}m"

    # Ping-reachable fallback (sets connected without admin details)
    elif source.get("ping_host"):
        ok, _ = ping_test(source["ping_host"], count=1, timeout=2)
        if ok:
            result["connected"] = True

    # internet_only — connected is set by caller based on WAN detection
    elif source.get("detection_method") == "internet_only":
        pass   # connected set below by poll()

    return result


def poll():
    """Run one complete WAN status poll cycle."""
    cfg     = load_config()
    ts      = utcnow()
    sources = cfg.get("wan_sources", [])

    # Only consider enabled sources
    enabled = [s for s in sources if s.get("enabled", True)]

    # Test internet connectivity first
    internet_ok, internet_latency = ping_test("1.1.1.1")

    active_source_id = None
    active_label     = "None"
    source_details   = {}

    if internet_ok:
        # Sort: preferred role first, then fallback
        ordered = sorted(enabled, key=lambda s: (0 if s.get("role") == "preferred" else 1))

        for source in ordered:
            if check_source(source):
                active_source_id = source.get("id")
                active_label     = source.get("label", "WAN")
                break

        # If no specific source matched (e.g. all internet_only), use first preferred
        if not active_source_id and enabled:
            pref = [s for s in ordered if s.get("role") == "preferred"]
            if pref:
                active_source_id = pref[0].get("id")
                active_label     = pref[0].get("label", "WAN")
            else:
                active_source_id = ordered[0].get("id")
                active_label     = ordered[0].get("label", "WAN")

    # Get details for all enabled sources
    for source in enabled:
        details = get_source_details(source)
        # Mark connected if this is the active source
        if source.get("id") == active_source_id and internet_ok:
            details["connected"] = True
        source_details[source.get("id", "")] = details

    # Determine simple active_source string for dashboard backwards compat
    active_src_cfg = next((s for s in sources if s.get("id") == active_source_id), {})
    src_type = active_src_cfg.get("type", "site") if internet_ok else "none"
    # Map type to legacy dashboard keys
    legacy_src = (
        "cellular"  if src_type in ("cellular", "hotspot") else
        "satellite" if src_type == "satellite" else
        "site"      if src_type in ("fixed", "other")     else
        "none"
    ) if internet_ok else "none"

    dash = cfg.get("dashboard", {})

    # Build source_a / source_b for backwards-compat with wan-status.html
    src_list = cfg.get("wan_sources", [])
    wa = source_details.get(src_list[0]["id"] if src_list else "source_a", {})
    wb = source_details.get(src_list[1]["id"] if len(src_list) > 1 else "source_b", {})

    return {
        "timestamp":           ts,
        "active_source":       legacy_src,
        "active_source_id":    active_source_id,
        "active_label":        active_label,
        "internet_latency_ms": internet_latency,
        # New structured keys
        "wan_sources": source_details,
        # Legacy keys (dashboard/wan-status.html backwards compat)
        "instyconnect": wa,
        "starlink":     wb,
        "primary_wan":  wa,
        "secondary_wan": wb,
        "config": {
            "show_wan_a":          dash.get("show_wan_a", True),
            "show_wan_b":          dash.get("show_wan_b", False),
            "show_amprnet":        dash.get("show_amprnet", True),
            # Legacy label keys
            "show_primary_wan":    dash.get("show_wan_a", True),
            "show_secondary_wan":  dash.get("show_wan_b", False),
            "primary_wan_name":    wa.get("label", "WAN A"),
            "secondary_wan_name":  wb.get("label", "WAN B"),
            "wan_sources":         [
                {"id": s.get("id"), "label": s.get("label"),
                 "role": s.get("role"), "type": s.get("type"),
                 "enabled": s.get("enabled", True),
                 "icon": s.get("icon") or TYPE_ICONS.get(s.get("type","other"),"🔗")}
                for s in src_list
            ],
        },
    }


def write_status(data):
    """Write status atomically."""
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(OUTPUT_FILE)
    except Exception as e:
        print(f"[wan-monitor] Write error: {e}")


if __name__ == "__main__":
    print(f"[wan-monitor] Starting — polling every {POLL_INTERVAL}s")
    print(f"[wan-monitor] Config:  {CONFIG_FILE}")
    print(f"[wan-monitor] Output:  {OUTPUT_FILE}")

    while True:
        try:
            data = poll()
            write_status(data)
            src     = data.get("active_label", "none")
            latency = data.get("internet_latency_ms")
            print(f"[wan-monitor] {utcnow()}  active={src}"
                  f"{'  ' + str(latency) + 'ms' if latency else ''}")
        except Exception as e:
            print(f"[wan-monitor] Poll error: {e}")
            write_status({
                "timestamp": utcnow(), "active_source": "none",
                "error": str(e),
                "instyconnect": {"connected": False},
                "starlink":     {"connected": False},
                "primary_wan":  {"connected": False},
                "secondary_wan": {"connected": False},
                "wan_sources":  {},
            })
        time.sleep(POLL_INTERVAL)
