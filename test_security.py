"""Login-link throttle and browser security headers."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "eli@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"
os.environ["DEV_SHOW_LINKS"] = "1"

import app as A


def _csrf(browser):
    html = browser.get("/login").get_data(as_text=True)
    return re.search(r'name=csrf value="([^"]+)"', html).group(1)


def _issued(email):
    with A.app.app_context():
        d = A.db()
        return d.execute("SELECT COUNT(*) FROM login_tokens t JOIN members m ON m.id=t.member_id WHERE m.email=?", (email,)).fetchone()[0]


def test_login_links_are_throttled_per_address_and_per_device():
    A._link_hits.clear()
    browser = A.app.test_client()
    browser.get("/login")
    with A.app.app_context():
        d = A.db()
        d.execute("INSERT INTO members(first, last, email) VALUES('Eli','J','eli@example.com')"); d.commit()
    token = _csrf(browser)
    for _ in range(A.LINK_MAX_PER_EMAIL + 3):
        page = browser.post("/login", data=dict(email="eli@example.com", csrf=token), follow_redirects=True).get_data(as_text=True)
        assert "If that email is on the team" in page  # same answer whether or not it was sent
    assert _issued("eli@example.com") == A.LINK_MAX_PER_EMAIL
    for i in range(A.LINK_MAX_PER_IP + 2):
        browser.post("/login", data=dict(email="nobody%d@example.com" % i, csrf=token))
    assert len(A._link_hits["127.0.0.1"]) == A.LINK_MAX_PER_IP
    A._link_hits.clear()


def test_security_headers():
    browser = A.app.test_client()
    r = browser.get("/login")
    assert r.headers["X-Content-Type-Options"] == "nosniff"
    assert r.headers["X-Frame-Options"] == "SAMEORIGIN"
    assert "frame-ancestors 'self'" in r.headers["Content-Security-Policy"]
    assert "geolocation=(self)" in r.headers["Permissions-Policy"]
    assert "Strict-Transport-Security" in browser.get("/login", base_url="https://example.com").headers
    w = browser.get("/widget?preview=1")
    assert "X-Frame-Options" not in w.headers
