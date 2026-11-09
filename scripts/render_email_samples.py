"""Write sample branded emails to a folder. Does not send mail.

Usage: python scripts/render_email_samples.py [output_dir]
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mailhtml

def main():
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "tmp-email-samples")
    out = os.path.abspath(out)
    os.makedirs(out, exist_ok=True)
    org = os.environ.get("ORG_NAME") or mailhtml.ORG_NAME
    base = os.environ.get("PUBLIC_URL") or "https://grunions.regulars.team"
    for key, _title, html in mailhtml.preview_catalog(base, org):
        path = os.path.join(out, key + ".html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(path)

if __name__ == "__main__":
    main()
