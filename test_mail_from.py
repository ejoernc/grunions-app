"""From display name on transactional mail. The address stays the verified one."""
import os, tempfile
D = tempfile.mkdtemp()
os.environ.update(DATA_DIR=D, ADMIN_EMAIL="eli@example.com", DEV_SHOW_LINKS="0", GRUNIONS_SCHEDULER="0",
                  SMTP_HOST="smtp.test", SMTP_PORT="587", SMTP_USER="u", SMTP_PASSWORD="p",
                  MAIL_FROM="info@regulars.team", ORG_NAME="Grunions Water Polo")
os.environ.pop("GRUNIONS_DB", None)
import app as A


def test_grunions_from_uses_the_club_name_and_the_same_address():
    header = A.format_from_header(A.org_name(), "info@regulars.team")
    assert header == "Grunions Water Polo <info@regulars.team>"


def test_an_existing_display_name_is_replaced_and_the_address_is_kept():
    header = A.format_from_header("Grunions Water Polo", "Someone <info@regulars.team>")
    assert header == "Grunions Water Polo <info@regulars.team>"


def test_quotes_and_commas_are_quoted():
    header = A.format_from_header('Say "Hi", Team', "info@regulars.team")
    assert header == '"Say \\"Hi\\", Team" <info@regulars.team>'


def test_emoji_and_non_ascii_use_encoded_words():
    wave = A.format_from_header("Grunions 🌊", "info@regulars.team")
    accent = A.format_from_header("Åsa's Club", "info@regulars.team")
    assert wave.startswith("=?utf-8?") and wave.endswith("<info@regulars.team>")
    assert "🌊" not in wave
    assert accent.startswith("=?utf-8?") and accent.endswith("<info@regulars.team>")


def test_a_long_name_is_trimmed():
    from email.utils import parseaddr
    header = A.format_from_header("A" * 90, "info@regulars.team")
    name, addr = parseaddr(header)
    assert len(name) == 78 and name.endswith("...") and addr == "info@regulars.team"


def test_missing_team_falls_back_to_regulars():
    for missing in (None, "", "   "):
        assert A.format_from_header(missing, "info@regulars.team") == "Regulars <info@regulars.team>"


def test_send_email_puts_the_team_on_the_message_and_regulars_when_absent():
    import smtplib
    class Rec:
        def __init__(self, *a, **k):
            self.esmtp_features = {"starttls": "", "auth": "PLAIN"}
            Rec.inst = self
        def ehlo(self, name=""): pass
        def has_extn(self, name): return name.lower() in self.esmtp_features
        def starttls(self, context=None): pass
        def login(self, u, p): pass
        def send_message(self, msg): self.msg = msg
        def quit(self): pass
        def close(self): pass
    saved, real = dict(A.SMTP), smtplib.SMTP
    A.SMTP = {"SMTP_HOST": "127.0.0.1", "SMTP_PORT": "587", "SMTP_USER": "u", "SMTP_PASSWORD": "pw", "MAIL_FROM": "info@regulars.team"}
    smtplib.SMTP = Rec
    try:
        A.send_email("person@example.com", "You're signed up", "Hi", sender="Grunions Water Polo")
        assert Rec.inst.msg["From"] == "Grunions Water Polo <info@regulars.team>"
        assert Rec.inst.msg["To"] == "person@example.com"
        assert Rec.inst.msg["Reply-To"] is None
        A.send_email("person@example.com", "Your Grunions login link", "Hi")
        assert Rec.inst.msg["From"] == "Regulars <info@regulars.team>"
    finally:
        smtplib.SMTP = real
        A.SMTP = saved
