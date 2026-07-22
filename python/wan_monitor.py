# SPDX-License-Identifier: AGPL-3.0-or-later
# FieldCommand IMS — Copyright (C) 2026 James Rospopo KE4CON
# Developed for McHenry County Emergency Services Volunteers (K9ESV)
# Licensed under the GNU Affero General Public License v3.0 or later.
# See LICENSE in the project root for full license text.
# https://github.com/KE4CON/FieldCommand-IMS

#!/usr/bin/env python3
"""
wan_monitor.py — WAN Status Monitor Service
Runs on the FieldCommand Pi (192.168.50.1).
Polls configured WAN sources every 30 seconds.
Reads configuration from /opt/fieldcommand/data/wan_config.json
(falls back to python/wan_config_defaults.json if not present).

Configuration drives all provider-specific behaviour — no hardcoded
provider names, IPs, or brands. Any cellular modem, satellite provider,
or fixed ISP can be configured without editing this file.
"""

import json
import re
import subprocess
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

BASE         = Path("/opt/fieldcommand")
DATA         = BASE / "data"
OUTPUT_FILE  = DATA / "wan_status.json"
CONFIG_FILE  = DATA / "wan_config.json"
DEFAULTS_FILE = Path(__file__).parent / "wan_config_defaults.json"
POLL_INTERVAL = 30  # seconds


def load_config():
    """Load WAN config — site config first, fallback to defaults."""
    for path in [CONFIG_FILE, DEFAULTS_FILE]:
        try:
            with open(path) as f:
                return json.load(f)
        except Exception:
            pass
    # Bare minimum if no config file exists at all
    return {
        "primary_wan":   {"enabled": True,  "label": "Primary WAN",   "admin_url": "http://10.1.1.1",      "detection_method": "admin_reachable"},
        "secondary_wan": {"enabled": False, "label": "Secondary WAN", "ping_host": "",           "detection_method": "ping"},
        "dashboard":     {"show_primary_wan": True, "show_secondary_wan": False},
    }


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
    """Return (reachable, response_ms)."""
    try:
        start = time.time()
        req = urllib.request.Request(url, headers={"User-Agent": "FieldCommand/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(8192).decode(errors="ignore")
            ms   = round((time.time() - start) * 1000, 1)
            return True, ms, body
    except Exception:
        return False, None, ""


def detect_wan_source(cfg):
    """
    Determine active WAN source using config-driven detection.
    Returns: ('primary'|'secondary'|'site'|'none', latency_ms)
    """
    internet_ok, latency = ping_test("1.1.1.1")
    if not internet_ok:
        return "none", None

    primary = cfg.get("primary_wan", {})
    secondary = cfg.get("secondary_wan", {})

    # Check primary WAN
    if primary.get("enabled", True):
        method = primary.get("detection_method", "admin_reachable")
        if method == "admin_reachable" and primary.get("admin_url"):
            ok, _, _ = http_test(primary["admin_url"], timeout=primary.get("admin_timeout_s", 3))
            if ok:
                return "primary", latency
        elif method == "ping" and primary.get("ping_host"):
            ok, _ = ping_test(primary["ping_host"], count=1, timeout=2)
            if ok:
                return "primary", latency

    # Check secondary WAN
    if secondary.get("enabled", False):
        method = secondary.get("detection_method", "ping")
        if method == "ping" and secondary.get("ping_host"):
            ok, _ = ping_test(secondary["ping_host"], count=1, timeout=2)
            if ok:
                return "secondary", latency
        elif method == "admin_reachable" and secondary.get("admin_url"):
            ok, _, _ = http_test(secondary["admin_url"], timeout=secondary.get("admin_timeout_s", 3))
            if ok:
                return "secondary", latency

    # Internet is up but neither primary nor secondary detected
    return "site", latency


def get_primary_status(cfg):
    """Poll primary WAN admin interface for signal/carrier details."""
    primary = cfg.get("primary_wan", {})
    admin_url = primary.get("admin_url")
    result = {
        "connected": False,
        "label":     primary.get("label", "Primary WAN"),
        "provider":  primary.get("provider", ""),
        "icon":      primary.get("icon", "📡"),
    }
    if not admin_url:
        return result

    ok, _, body = http_test(admin_url, timeout=primary.get("admin_timeout_s", 4))
    if not ok:
        return result

    result["connected"] = True

    # Generic carrier detection — looks for common carrier names in page body.
    # Works with most cellular router and modem admin pages regardless of brand.
    # (InstyConnect, Cradlepoint, Sierra Wireless, Pepwave, etc. all expose this)
    common_carriers = ["T-Mobile", "Verizon", "AT&T", "FirstNet", "US Cellular",
                       "C Spire", "Sprint", "Dish", "Band 14", "CBRS"]
    for carrier in common_carriers:
        if carrier.lower() in body.lower():
            result["carrier"] = carrier
            break
    else:
        result["carrier"] = primary.get("provider", "Unknown carrier")

    # Technology detection
    for tech in ["5G NR", "5G", "LTE", "4G", "3G", "2G"]:
        if tech in body:
            result["technology"] = tech
            break

    # Signal strength (RSSI)
    rssi_m = re.search(r"rssi[\":\s]+(-?\d+)", body, re.I)
    if rssi_m:
        rssi = int(rssi_m.group(1))
        result["signal_dbm"] = rssi
        result["signal_strength"] = (
            f"Excellent ({rssi} dBm)" if rssi >= -70 else
            f"Good ({rssi} dBm)"     if rssi >= -85 else
            f"Fair ({rssi} dBm)"     if rssi >= -100 else
            f"Poor ({rssi} dBm)"
        )

    return result


def get_secondary_status(cfg):
    """Poll secondary WAN (satellite or other) for status details."""
    secondary = cfg.get("secondary_wan", {})
    result = {
        "connected":    False,
        "dish_present": False,
        "label":        secondary.get("label", "Secondary WAN"),
        "provider":     secondary.get("provider", ""),
        "icon":         secondary.get("icon", "🛰"),
    }
    if not secondary.get("enabled", False):
        return result

    ping_host = secondary.get("ping_host")
    if not ping_host:
        return result

    ok, _ = ping_test(ping_host, count=1, timeout=2)
    if not ok:
        return result

    result["dish_present"] = True

    # Try generic HTTP status endpoint
    admin_url = secondary.get("admin_url")
    if admin_url:
        ok2, _, body = http_test(admin_url, timeout=secondary.get("admin_timeout_s", 4))
        if ok2:
            result["connected"] = True
            # Parse satellite provider metrics if present.
            # Starlink gRPC JSON format — also check for Hughes/ViaSat equivalents.
            lat_m = re.search(r'"popPingLatencyMs":\s*([\d.]+)', body)
            dl_m  = re.search(r'"downlinkThroughputBps":\s*([\d.]+)', body)
            ul_m  = re.search(r'"uplinkThroughputBps":\s*([\d.]+)', body)
            obs_m = re.search(r'"fractionObstructed":\s*([\d.]+)', body)
            up_m  = re.search(r'"uptimeS":\s*(\d+)', body)
            if lat_m: result["latency_ms"]     = round(float(lat_m.group(1)), 1)
            if dl_m:  result["download_mbps"]  = round(float(dl_m.group(1)) / 1e6, 1)
            if ul_m:  result["upload_mbps"]    = round(float(ul_m.group(1)) / 1e6, 1)
            if obs_m: result["obstruction_pct"] = round(float(obs_m.group(1)) * 100, 1)
            if up_m:
                secs = int(up_m.group(1))
                result["uptime"] = f"{secs//3600}h {(secs%3600)//60}m"
        else:
            result["connected"] = True  # ping worked, API not responding

    return result


def write_status(data):
    """Write status atomically."""
    try:
        OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        tmp = OUTPUT_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2))
        tmp.replace(OUTPUT_FILE)
    except Exception as e:
        print(f"[wan-monitor] Write error: {e}")


def poll():
    cfg = load_config()
    ts  = utcnow()

    active_source, internet_latency = detect_wan_source(cfg)
    primary_status   = get_primary_status(cfg)
    secondary_status = get_secondary_status(cfg)

    if active_source == "primary" and not primary_status.get("connected"):
        primary_status["connected"] = True

    dash = cfg.get("dashboard", {})

    return {
        "timestamp":           ts,
        "active_source":       active_source,
        "internet_latency_ms": internet_latency,
        # Keep legacy keys for dashboard backwards compat
        "instyconnect": primary_status,
        "starlink":     secondary_status,
        # New generic keys
        "primary_wan":  primary_status,
        "secondary_wan": secondary_status,
        "config": {
            "show_primary_wan":    dash.get("show_primary_wan", True),
            "show_secondary_wan":  dash.get("show_secondary_wan", False),
            "primary_wan_name":    dash.get("primary_wan_name", primary_status.get("label", "Cellular")),
            "secondary_wan_name":  dash.get("secondary_wan_name", secondary_status.get("label", "Satellite")),
        },
    }


if __name__ == "__main__":
    print(f"[wan-monitor] Starting — polling every {POLL_INTERVAL}s")
    print(f"[wan-monitor] Config: {CONFIG_FILE} (fallback: {DEFAULTS_FILE})")
    print(f"[wan-monitor] Output: {OUTPUT_FILE}")

    while True:
        try:
            data = poll()
            write_status(data)
            source  = data.get("active_source", "unknown")
            latency = data.get("internet_latency_ms")
            print(f"[wan-monitor] {utcnow()}  WAN={source}"
                  f"{'  ' + str(latency) + 'ms' if latency else ''}")
        except Exception as e:
            print(f"[wan-monitor] Poll error: {e}")
            write_status({
                "timestamp": utcnow(), "active_source": "unknown",
                "error": str(e),
                "instyconnect":  {"connected": False},
                "starlink":      {"connected": False, "dish_present": False},
                "primary_wan":   {"connected": False},
                "secondary_wan": {"connected": False},
            })
        time.sleep(POLL_INTERVAL)
