# SPDX-License-Identifier: AGPL-3.0-or-later
# Guards for the HTTPS same-origin routing:
#   - the front end must not call the core services (5050/5051/5055/5056) by
#     absolute http://host:port — that would break HTTPS (mixed content) and put
#     PII on the wire in cleartext. It must use same-origin /svc/<port>.
#   - the four core services must bind 127.0.0.1 (reached only via nginx).
import os, re, glob, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
CORE_PORTS = ("5050", "5051", "5055", "5056")


class FrontEndSameOrigin(unittest.TestCase):
    def test_no_absolute_core_service_urls(self):
        pat = re.compile(r"http://(?:192\.168\.50\.1|localhost|127\.0\.0\.1):(?:5050|5051|5055|5056)")
        offenders = []
        for f in glob.glob(os.path.join(ROOT, "html", "**", "*.*"), recursive=True):
            if not f.endswith((".html", ".js")):
                continue
            with open(f, encoding="utf-8", errors="ignore") as fh:
                for i, line in enumerate(fh, 1):
                    if pat.search(line):
                        offenders.append(f"{os.path.relpath(f, ROOT)}:{i}")
        self.assertEqual(offenders, [], "front end must call /svc/<port>, not absolute http://host:port -> " + "; ".join(offenders))

    def test_svc_paths_present(self):
        # sanity: the routing actually happened (roster uses /svc/5050)
        with open(os.path.join(ROOT, "html", "roster.html"), encoding="utf-8") as f:
            self.assertIn("/svc/5050", f.read())


class ServicesBindLocalhost(unittest.TestCase):
    SERVICES = {
        "fcc_lookup_server.py": "5050",
        "health_monitor.py": "5051",
        "ics_platform_server.py": "5055",
        "reference_server.py": "5056",
    }

    def test_core_services_bind_localhost(self):
        for fn, port in self.SERVICES.items():
            src = open(os.path.join(ROOT, "python", fn), encoding="utf-8").read()
            self.assertRegex(src, r'HTTPServer\(\(["\']127\.0\.0\.1["\'] *, *' + port,
                             f"{fn} must bind 127.0.0.1:{port} (reached via nginx /svc/{port})")
            self.assertNotRegex(src, r'HTTPServer\(\(["\']0\.0\.0\.0["\'] *, *' + port,
                                f"{fn} must NOT bind 0.0.0.0:{port} (would expose PII in cleartext)")


if __name__ == "__main__":
    unittest.main(verbosity=2)
