"""WCAG 2.2 AA checks that do not need a browser."""
import os, re, tempfile
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="boss@example.com", DEV_SHOW_LINKS="0", GRUNIONS_SCHEDULER="0")
os.environ.pop("GRUNIONS_DB", None)
import app as A


def test_forbidden_page_is_in_the_app_not_the_stock_white_page():
    c = A.app.test_client()
    # A signed-out visitor is sent to log in. A member is refused.
    c.post("/join", data={"csrf": _csrf(c, "/join"), "first": "No", "last": "Access",
                          "email": "no.access@example.com", "phone": "1", "birth_date": "1990-04-04"},
           follow_redirects=True)
    page = c.get("/admin")
    body = page.get_data(as_text=True)
    assert page.status_code == 403
    assert "No access" in body and 'lang=en' in body and "#0B0B0C" in body
    assert "read-protected" not in body


def test_missing_page_uses_the_same_dark_screen():
    page = A.app.test_client().get("/no-such-a11y-page")
    body = page.get_data(as_text=True)
    assert page.status_code == 404
    assert "Page not found" in body and "#0B0B0C" in body


def test_date_of_birth_error_is_tied_to_the_fields():
    html = A.app.test_client().get("/join").get_data(as_text=True)
    assert 'id=dob-help-birth_date' in html or 'id="dob-help-birth_date"' in html
    assert html.count('aria-describedby="dob-help-birth_date"') == 3 or html.count("aria-describedby=dob-help-birth_date") == 3


def test_embed_tabs_expose_selection_not_pressed():
    import publicfeed
    html = publicfeed.widget_document({"org": "Grunions", "chips": ["all", "schedule"], "events": []})
    assert 'role=tab aria-selected="true"' in html
    assert "aria-pressed" not in html


def test_api_forbidden_stays_json():
    c = A.app.test_client()
    c.post("/join", data={"csrf": _csrf(c, "/join"), "first": "No", "last": "Api",
                          "email": "no.api@example.com", "phone": "1", "birth_date": "1990-04-04"},
           follow_redirects=True)
    res = c.get("/api/expiring")
    assert res.status_code == 403
    assert res.is_json


def _csrf(c, path):
    html = c.get(path).get_data(as_text=True)
    m = re.search(r'name=csrf value="([^"]+)"', html) or re.search(r"name=csrf value='([^']+)'", html)
    assert m, html[:400]
    return m.group(1)
