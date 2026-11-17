"""Polls in coaches chats: create, vote, results, anonymity, ending, end time, access, and emails."""
import os
import re
import tempfile

os.environ["GRUNIONS_DB"] = tempfile.mktemp(suffix=".db")
os.environ["ADMIN_EMAIL"] = "polladmin@example.com"
os.environ["GRUNIONS_SCHEDULER"] = "0"
os.environ["GRUNIONS_SHEET_SYNC"] = "0"
os.environ["DEV_SHOW_LINKS"] = "1"

import app as A
import polls

SENT = []
A.send_email = lambda to, subject, text, html=None, ics=None: SENT.append((to, subject, text))


def _member(first, email, role="athlete", admin=0):
    with A.app.app_context():
        d = A.db()
        d.execute("INSERT INTO members(first, last, email, role, is_admin, joined) VALUES(?,?,?,?,?,1)", (first, "Tester", email, role, admin))
        mid = d.execute("SELECT id FROM members WHERE email=?", (email,)).fetchone()[0]
        d.commit()
        return mid


def _as(mid):
    c = A.app.test_client()
    with c.session_transaction() as s:
        s["mid"] = mid
    return c


def _csrf(c, path):
    html = c.get(path).get_data(as_text=True)
    return re.search(r'name=csrf value="([^"]+)"', html).group(1)


def _new_poll(c, ch="coaches", **extra):
    data = {"csrf": _csrf(c, "/polls/new?c=" + ch), "c": ch, "title": "Sunday?", "q0_text": "Add a Sunday practice?",
            "q0_multi": "0", "q0_opt": ["9am", "4pm", "No"], "q1_text": "Drills", "q1_multi": "1", "q1_opt": ["6 on 5", "Shooting"]}
    data.update(extra)
    r = c.post("/polls/new", data=data)
    if r.status_code != 302:
        return r
    # Preview -> back in the chat with the poll attached; it posts when they send.
    pid = int(r.headers["Location"].split("poll=")[1])
    token = _csrf(c, "/notifications")
    sent = c.post("/api/messages?c=" + ch, json={"body": "", "poll_id": pid}, headers={"X-CSRF": token})
    assert sent.status_code == 200, sent.get_data(as_text=True)
    return r


def _latest_poll():
    with A.app.app_context():
        d = A.db(); polls.ensure(d)
        return d.execute("SELECT * FROM polls ORDER BY id DESC LIMIT 1").fetchone()


def _qopts(pid):
    with A.app.app_context():
        d = A.db()
        return [(q["id"], [o["id"] for o in q["options"]]) for q in polls.questions(d, pid)]


ADMIN = _member("Ada", "polladmin@example.com", admin=1)
COACH = _member("Cole", "cole@example.com", role="coach")
COACH2 = _member("Cara", "cara@example.com", role="coach")
PLAYER = _member("Pat", "pat@example.com")


def test_create_vote_results_and_access():
    SENT.clear()
    admin = _as(ADMIN)
    r = _new_poll(admin)
    assert r.status_code == 302 and "/chat?c=coaches&poll=" in r.headers["Location"]
    p = _latest_poll()
    assert p["channel"] == "coaches" and p["title"] == "Sunday?"
    with A.app.app_context():
        msg = A.db().execute("SELECT * FROM messages WHERE id=?", (p["message_id"],)).fetchone()
    assert msg["poll_id"] == p["id"] and msg["channel"] == "coaches"
    # Emails go to people in the chat, not the creator, not players.
    to = {t for t, _s, _x in SENT}
    assert "cole@example.com" in to and "cara@example.com" in to
    assert "polladmin@example.com" not in to and "pat@example.com" not in to
    assert any("/polls/%d" % p["id"] in x for _t, _s, x in SENT)

    (q0, o0), (q1, o1) = _qopts(p["id"])
    coach = _as(COACH)
    r = coach.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach, "/polls/%d" % p["id"]), "q%d" % q0: [o0[0], o0[1]], "q%d" % q1: [o1[0], o1[1]]})
    assert r.status_code == 302
    with A.app.app_context():
        votes = A.db().execute("SELECT question_id, option_id FROM poll_votes WHERE member_id=?", (COACH,)).fetchall()
    picked = {(v[0], v[1]) for v in votes}
    assert picked == {(q0, o0[0]), (q1, o1[0]), (q1, o1[1])}  # single choice keeps one; multi keeps both

    page = coach.get("/polls/%d" % p["id"]).get_data(as_text=True)
    assert "Cole T." in page  # votes visible by default
    sticky = coach.get("/api/polls/sticky?c=coaches").get_json()["html"]
    assert "Results" in sticky  # answered: collapsed bar
    sticky2 = _as(COACH2).get("/api/polls/sticky?c=coaches").get_json()["html"]
    assert "Vote" in sticky2  # unanswered: asks for a vote

    player = _as(PLAYER)
    assert player.get("/polls/%d" % p["id"]).status_code == 404
    assert player.get("/polls/new?c=team").status_code == 404  # polls are only on in coaches chats for now
    assert admin.get("/polls/new?c=team").status_code == 404
    assert polls.enabled("coaches") and polls.enabled("coach:swimming") and not polls.enabled("team")


def test_anonymous_hides_names_and_end_poll():
    admin = _as(ADMIN)
    _new_poll(admin, anonymous="1", title="Secret")
    p = _latest_poll()
    (q0, o0), (q1, o1) = _qopts(p["id"])
    coach = _as(COACH)
    coach.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach, "/polls/%d" % p["id"]), "q%d" % q0: o0[2], "q%d" % q1: o1[0]})
    page = coach.get("/polls/%d" % p["id"]).get_data(as_text=True)
    assert "Anonymous" in page and "Cole T." not in page
    # Only the creator or an admin can end it.
    coach2 = _as(COACH2)
    assert coach2.post("/polls/%d/end" % p["id"], data={"csrf": _csrf(coach2, "/notifications")}).status_code == 403
    assert admin.post("/polls/%d/end" % p["id"], data={"csrf": _csrf(admin, "/polls/%d" % p["id"])}).status_code == 302
    r = coach2.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach2, "/notifications"), "q%d" % q0: o0[0], "q%d" % q1: o1[0]})
    with A.app.app_context():
        assert not A.db().execute("SELECT 1 FROM poll_votes WHERE member_id=? AND question_id=?", (COACH2, q0)).fetchone()
    listing = coach.get("/chat/polls?c=coaches").get_data(as_text=True)
    assert "Closed" in listing and "Secret" in listing


def test_end_time_and_validation_and_email_opt_out():
    admin = _as(ADMIN)
    r = _new_poll(admin, ends_at="2001-01-01T09:00")
    assert r.status_code == 200 and "future" in r.get_data(as_text=True)
    r = _new_poll(admin, q0_opt=["only one"], q1_text="", q1_opt=[])
    assert r.status_code == 200 and "at least two options" in r.get_data(as_text=True)
    with A.app.app_context():
        d = A.db(); polls.ensure(d)
        d.execute("UPDATE members SET poll_email=0 WHERE id=?", (COACH,)); d.commit()
    SENT.clear()
    _new_poll(admin, title="Timed", ends_at="2099-01-01T09:00")
    assert "cole@example.com" not in {t for t, _s, _x in SENT} and "cara@example.com" in {t for t, _s, _x in SENT}
    p = _latest_poll()
    with A.app.app_context():
        d = A.db()
        d.execute("UPDATE polls SET ends_at='2001-01-01T09:00' WHERE id=?", (p["id"],)); d.commit()
        assert polls.is_closed(polls.get(d, p["id"]), A.wall_pt())


def test_edit_keeps_votes_and_others_can_add_options_without_new_emails():
    admin = _as(ADMIN)
    _new_poll(admin, title="Editable", allow_add="1")
    p = _latest_poll()
    assert p["allow_add"] == 1
    (q0, o0), (q1, o1) = _qopts(p["id"])
    coach = _as(COACH)
    coach.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach, "/polls/%d" % p["id"]), "q%d" % q0: o0[0], "q%d" % q1: o1[0]})
    # Only the creator or an admin can edit.
    assert coach.get("/polls/%d/edit" % p["id"]).status_code == 403
    SENT.clear()
    r = admin.post("/polls/%d/edit" % p["id"], data={"csrf": _csrf(admin, "/polls/%d/edit" % p["id"]), "title": "Renamed",
                                                      "qt%d" % q0: "Sunday practice time?", "ot%d" % o0[0]: "9:00 AM",
                                                      "new%d" % q0: ["Noon"], "allow_add": "1"})
    assert r.status_code == 302
    with A.app.app_context():
        d = A.db()
        assert d.execute("SELECT title FROM polls WHERE id=?", (p["id"],)).fetchone()[0] == "Renamed"
        assert d.execute("SELECT text FROM poll_options WHERE id=?", (o0[0],)).fetchone()[0] == "9:00 AM"
        # The vote on the renamed option is still there.
        assert d.execute("SELECT 1 FROM poll_votes WHERE member_id=? AND option_id=?", (COACH, o0[0])).fetchone()
        assert d.execute("SELECT COUNT(*) FROM poll_options WHERE question_id=?", (q0,)).fetchone()[0] == 4
    # A voter adds their own option; it becomes their pick. No emails go out for edits or added options.
    coach2 = _as(COACH2)
    coach2.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach2, "/polls/%d" % p["id"]), "add%d" % q0: "Sunday 6pm", "q%d" % q1: o1[1]})
    with A.app.app_context():
        d = A.db()
        new_id = d.execute("SELECT id FROM poll_options WHERE question_id=? AND text='Sunday 6pm'", (q0,)).fetchone()[0]
        assert d.execute("SELECT 1 FROM poll_votes WHERE member_id=? AND option_id=?", (COACH2, new_id)).fetchone()
    assert SENT == []
    # When the poll doesn't allow it, typed options are ignored.
    _new_poll(admin, title="Closed list")
    p2 = _latest_poll()
    (a0, b0), (a1, b1) = _qopts(p2["id"])
    coach2.post("/polls/%d" % p2["id"], data={"csrf": _csrf(coach2, "/polls/%d" % p2["id"]), "add%d" % a0: "Sneaky", "q%d" % a0: b0[0], "q%d" % a1: b1[0]})
    with A.app.app_context():
        assert not A.db().execute("SELECT 1 FROM poll_options WHERE question_id=? AND text='Sneaky'", (a0,)).fetchone()


def test_results_post_once_when_poll_closes_and_tracker_bar():
    admin = _as(ADMIN)
    _new_poll(admin, title="Auto results", post_results="1")
    p = _latest_poll()
    (q0, o0), (q1, o1) = _qopts(p["id"])
    coach = _as(COACH)
    coach.post("/polls/%d" % p["id"], data={"csrf": _csrf(coach, "/polls/%d" % p["id"]), "q%d" % q0: o0[1], "q%d" % q1: o1[0]})
    import components
    with A.app.app_context():
        d = A.db()
        s = polls.summary(d, polls.get(d, p["id"]), COACH, A.wall_pt(), lambda i: "x")
    bar = str(components.poll_bar(s))
    assert "rg-polltrk" in bar and "100%" in bar  # answered and live: tracker of the leading answer
    admin.post("/polls/%d/end" % p["id"], data={"csrf": _csrf(admin, "/polls/%d" % p["id"])})
    with A.app.app_context():
        d = A.db()
        rows = d.execute("SELECT body FROM messages WHERE poll_id=? ORDER BY id", (p["id"],)).fetchall()
        assert [r[0] for r in rows] == ["📊 Poll: Auto results", "📊 Results: Auto results"]
        A.post_poll_results(d)  # running again doesn't post twice
        assert d.execute("SELECT COUNT(*) FROM messages WHERE poll_id=?", (p["id"],)).fetchone()[0] == 2
    # By end time: the scheduled job posts once the time passes.
    _new_poll(admin, title="Timed results", post_results="1", ends_at="2099-01-01T09:00")
    p2 = _latest_poll()
    with A.app.app_context():
        d = A.db()
        A.post_poll_results(d)
        assert d.execute("SELECT COUNT(*) FROM messages WHERE poll_id=?", (p2["id"],)).fetchone()[0] == 1
        d.execute("UPDATE polls SET ends_at='2001-01-01T09:00' WHERE id=?", (p2["id"],)); d.commit()
        A.post_poll_results(d)
        assert d.execute("SELECT COUNT(*) FROM messages WHERE poll_id=?", (p2["id"],)).fetchone()[0] == 2
    # Closed polls drop off the sticky bar.
    assert "Timed results" not in coach.get("/api/polls/sticky?c=coaches").get_json()["html"]


def test_preview_is_private_until_sent_and_title_can_be_the_question():
    admin = _as(ADMIN)
    SENT.clear()
    r = admin.post("/polls/new", data={"csrf": _csrf(admin, "/polls/new?c=coaches"), "c": "coaches",
                                         "title": "Sunday practice at 9am?", "q0_text": "", "q0_multi": "0", "q0_opt": ["Yes", "No"]})
    assert r.status_code == 302 and "poll=" in r.headers["Location"]
    pid = int(r.headers["Location"].split("poll=")[1])
    with A.app.app_context():
        d = A.db()
        assert polls.questions(d, pid)[0]["text"] == "Sunday practice at 9am?"  # title used as the question
        assert polls.get(d, pid)["message_id"] is None
    assert SENT == []  # nothing goes out on preview
    coach = _as(COACH)
    assert "Sunday practice at 9am?" not in coach.get("/api/polls/sticky?c=coaches").get_json()["html"]
    assert coach.get("/api/polls/%d/draft?c=coaches" % pid).status_code == 404  # only the creator sees the preview
    assert admin.get("/api/polls/%d/draft?c=coaches" % pid).status_code == 200
    token = _csrf(admin, "/notifications")
    r = admin.post("/api/messages?c=coaches", json={"body": "Thoughts on adding Sundays?", "poll_id": pid}, headers={"X-CSRF": token})
    assert r.status_code == 200
    with A.app.app_context():
        d = A.db()
        p = polls.get(d, pid)
        msg = d.execute("SELECT body, poll_id FROM messages WHERE id=?", (p["message_id"],)).fetchone()
        assert msg["body"] == "Thoughts on adding Sundays?" and msg["poll_id"] == pid
    assert "cara@example.com" in {t for t, _s, _x in SENT}  # emails go out when it's sent (Cole opted out earlier)
    # A sent poll can't be sent again.
    again = admin.post("/api/messages?c=coaches", json={"body": "x", "poll_id": pid}, headers={"X-CSRF": token})
    assert again.status_code == 400
