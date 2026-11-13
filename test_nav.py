"""Regulars 2.0 navigation model (Figma 60). Run: .venv/bin/python -m pytest -q test_nav.py"""
import os, re, tempfile
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="boss@example.com", DEV_SHOW_LINKS="0")
os.environ.pop("GRUNIONS_DB", None)
import app as A
import nav

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = {"pid": 1, "eid": 1, "sid": 1, "mid": 1, "slug": "water-polo", "area": "people", "role": "athletes",
          "rule_id": 1, "div_id": 1, "role_id": 1, "day_id": 1, "req_id": 1, "plan_id": 1, "venue_id": 1,
          "member_id": 1, "tok": "x", "token": "x", "kind": "x", "filename": "x"}


def _get_rules():
    return [r for r in A.app.url_map.iter_rules() if "GET" in r.methods and not r.rule.startswith("/api/")]


def test_every_get_route_is_in_the_tree():
    missing = [(r.rule, r.endpoint) for r in _get_rules() if r.endpoint not in nav.ROUTES]
    assert not missing, missing


def test_every_page_reaches_a_root_in_4_hops_without_cycles():
    deep = []
    for ep, e in nav.ROUTES.items():
        if e["kind"] in ("asset",):
            continue
        args = dict(SAMPLE)
        k = nav.kind(ep, args)
        if k == "root":
            assert nav.parent(ep, args) is None, ep
            continue
        assert nav.parent(ep, args), "%s has no parent" % ep
        n = nav.depth(ep, args)
        if n > 4:
            deep.append((ep, n))
    assert not deep, deep
    # Threads: a channel or practice chat goes up to the Chat inbox.
    assert nav.kind("chat", {"c": "practice:3"}) == "thread" and nav.parent("chat", {"c": "practice:3"})[0] == "chat"


def test_parent_hrefs_carry_restore_state():
    with A.app.test_request_context():
        url_for = A.url_for
        assert nav.parent_url("availability_fit", {}, url_for) == "/calendar?when=availability"
        assert nav.parent_url("member_page", {"mid": 4, "view": "coaches"}, url_for) == "/members?view=coaches"
        assert nav.parent_url("practice_rides", {"pid": 7}, url_for) == "/practices/7"
        assert nav.parent_url("sport_role_rules", {"slug": "water-polo", "role": "athletes"}, url_for) == "/manage/club/programs/water-polo"
        assert nav.parent_title("sport_role_rules", {"slug": "water-polo", "role": "athletes", "_sport_name": "Water Polo"}) == "Water Polo"
        assert nav.parent_url("manage_schedule", {}, url_for) == "/manage/area/activities"


def test_no_history_back_referrer_or_hand_rolled_back_links():
    bad = []
    for name in ("ui.py", "flows2.py", "components.py", "app.py", "clubadmin.py"):
        src = open(os.path.join(HERE, name), encoding="utf-8").read()
        for i, line in enumerate(src.splitlines(), 1):
            if "document.referrer" in line or "javascript:back" in line:
                bad.append((name, i, "referrer/javascript back"))
            if "history.back(" in line and "function grunionsPopOverlay" not in line:
                bad.append((name, i, "history.back"))
            if re.search(r">\s*(←|&larr;)\s*\w", line):
                bad.append((name, i, "← link text"))
            if "rg-backlink" in line or "hubback" in line:
                bad.append((name, i, "hand-rolled back"))
    assert not bad, bad
