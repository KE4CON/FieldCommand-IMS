# SPDX-License-Identifier: AGPL-3.0-or-later
# Regression tests for the member ID / QR check-in feature:
#   - offline QR generation (replaces the dead chart.googleapis.com dependency)
#   - member photo storage flag (never leak the Base64 blob in list JSON)
#   - agency-neutral ID-card generation (branding from station_config)
#   - who-gets-a-card rules (members always; walk-ins/mutual-aid only with a photo)
#
# Run:  python -m pytest tests/           (or)  python tests/test_id_qr.py
import os, sys, base64, sqlite3, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
sys.path.insert(0, os.path.join(ROOT, "python"))

import gen_id_cards as gic

# A valid 8x10 JPEG, embedded so these tests need no Pillow at runtime — the same
# reason the app encodes member photos as JPEG (ReportLab embeds JPEG without PIL).
JPEG_B64 = ("/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQ"
            "YGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGh"
            "YaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wA"
            "ARCAAKAAgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtR"
            "AAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2Jyggk"
            "KFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIW"
            "Gh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+T"
            "l5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtRE"
            "AAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYk"
            "NOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEh"
            "YaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5e"
            "bn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwChRRRX0R5J/9k=")

ROSTER_SQL = """
CREATE TABLE station_config(id INTEGER PRIMARY KEY, org_short TEXT, org_name TEXT,
  callsign TEXT, ps_member_id_label TEXT, ps_id_label TEXT, logo_data TEXT, logo_mime TEXT);
CREATE TABLE roster(id TEXT PRIMARY KEY, member_id TEXT, callsign TEXT, radio_id TEXT,
  first_name TEXT, last_name TEXT, role TEXT, member_type TEXT, barcode_id TEXT,
  license_class TEXT, photo_data TEXT, photo_mime TEXT);
"""


def make_db(members, cfg=("ACME EMA", "Acme County EMA", "W1ACM", "Member ID", "Radio ID")):
    fd, path = tempfile.mkstemp(suffix=".db"); os.close(fd)
    con = sqlite3.connect(path)
    con.executescript(ROSTER_SQL)
    con.execute("INSERT INTO station_config(id,org_short,org_name,callsign,"
                "ps_member_id_label,ps_id_label,logo_data,logo_mime) VALUES(1,?,?,?,?,?,'','')", cfg)
    for m in members:
        con.execute("INSERT INTO roster(id,member_id,callsign,radio_id,first_name,last_name,"
                    "role,member_type,barcode_id,license_class,photo_data,photo_mime) "
                    "VALUES(:id,:member_id,:callsign,:radio_id,:first_name,:last_name,"
                    ":role,:member_type,:barcode_id,:license_class,:photo_data,:photo_mime)",
                    {**BLANK, **m})
    con.commit(); con.close()
    return path


BLANK = dict(id="", member_id="", callsign="", radio_id="", first_name="", last_name="",
             role="Operator", member_type="member", barcode_id="", license_class="",
             photo_data="", photo_mime="")


class CardEligibility(unittest.TestCase):
    def test_member_included(self):
        self.assertTrue(gic._include({"member_type": "member"}))

    def test_visitor_without_photo_excluded(self):
        self.assertFalse(gic._include({"member_type": "visitor", "photo_data": ""}))
        self.assertFalse(gic._include({"member_type": "mutual_aid"}))

    def test_visitor_with_photo_included(self):
        self.assertTrue(gic._include({"member_type": "visitor", "photo_data": JPEG_B64}))


class ImageReader(unittest.TestCase):
    def test_empty_is_none(self):
        self.assertIsNone(gic._img_reader(""))
        self.assertIsNone(gic._img_reader(None))

    def test_jpeg_base64_reads(self):
        self.assertIsNotNone(gic._img_reader(JPEG_B64))

    def test_data_url_reads(self):
        self.assertIsNotNone(gic._img_reader("data:image/jpeg;base64," + JPEG_B64))


class CardGeneration(unittest.TestCase):
    def test_pdf_produced_and_filters(self):
        db = make_db([
            dict(id="m-1", member_id="MEM-1", callsign="W1ABC", radio_id="1001",
                 first_name="Pat", last_name="Jones", member_type="member", barcode_id="MEM-1"),
            dict(id="m-2", member_id="MEM-2", first_name="Sam", last_name="Walk",
                 member_type="visitor", barcode_id="MEM-2"),                     # no photo -> excluded
            dict(id="m-3", member_id="MEM-3", first_name="Lee", last_name="Aid",
                 member_type="mutual_aid", barcode_id="MEM-3",
                 photo_data=JPEG_B64, photo_mime="image/jpeg"),                  # photo -> included
        ])
        try:
            con = sqlite3.connect(db); con.row_factory = sqlite3.Row
            ids = [m["id"] for m in gic.load_members(con)]
            con.close()
            self.assertEqual(sorted(ids), ["m-1", "m-3"])
            out = os.path.join(tempfile.gettempdir(), "fc_test_cards.pdf")
            gic.generate_from_db(db, out)
            with open(out, "rb") as f:
                self.assertEqual(f.read(5), b"%PDF-")
        finally:
            os.remove(db)

    def test_only_id(self):
        db = make_db([
            dict(id="m-1", member_id="MEM-1", first_name="Pat", barcode_id="MEM-1"),
            dict(id="m-2", member_id="MEM-2", first_name="Sam", barcode_id="MEM-2"),
        ])
        try:
            con = sqlite3.connect(db); con.row_factory = sqlite3.Row
            ids = [m["id"] for m in gic.load_members(con, only_id="m-2")]
            con.close()
            self.assertEqual(ids, ["m-2"])
        finally:
            os.remove(db)

    def test_empty_raises(self):
        db = make_db([dict(id="v", member_type="visitor", first_name="No", barcode_id="v")])
        try:
            with self.assertRaises(ValueError):
                gic.generate_from_db(db, os.path.join(tempfile.gettempdir(), "x.pdf"))
        finally:
            os.remove(db)


class OfflineQR(unittest.TestCase):
    """The dead chart.googleapis.com API must be gone; QR must render locally."""

    def test_no_dead_google_chart_api(self):
        bad = "googleapis.com/" + "chart"   # split so this test file never self-matches
        for sub in ("html", "python"):      # the shipped app code (not tests/docs)
            for root, _dirs, files in os.walk(os.path.join(ROOT, sub)):
                if "__pycache__" in root:
                    continue
                for fn in files:
                    if fn.endswith((".html", ".js", ".py")):
                        p = os.path.join(root, fn)
                        with open(p, encoding="utf-8", errors="ignore") as f:
                            self.assertNotIn(bad, f.read(), f"dead QR API still referenced in {p}")

    def test_qr_svg_renders(self):
        try:
            import fcc_lookup_server as fcc
        except Exception as e:
            self.skipTest(f"server import unavailable here: {e}")
        svg = fcc.qr_svg("MEM-1")
        self.assertIn("<svg", svg)
        self.assertGreater(len(svg), 1000)   # a real QR has many modules

    def test_member_to_dict_hides_photo(self):
        try:
            import fcc_lookup_server as fcc
        except Exception as e:
            self.skipTest(f"server import unavailable here: {e}")
        d = fcc.member_to_dict({"id": "1", "first_name": "A", "photo_data": "xxxx"})
        self.assertTrue(d["has_photo"])
        self.assertNotIn("photo_data", d)


if __name__ == "__main__":
    unittest.main(verbosity=2)
