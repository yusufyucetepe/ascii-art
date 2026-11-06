"""Build geisha.html by embedding an ASCII art text file into geisha_template.html."""
import json
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).parent
art_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "geisha_art.txt"

# Blank margins in the file would push her off-centre, since the page centres the whole block of text.
text = textwrap.dedent(art_path.read_text(encoding="utf-8").expandtabs())
art = "\n".join(line.rstrip() for line in text.splitlines()).strip("\n")
if not art.strip():
    sys.exit(f"{art_path} is empty. Paste your art into it, save, and run this again.")

# Embedding inline lets the page open by double-click; fetch() is blocked on file:// URLs.
embedded = json.dumps(art, ensure_ascii=False).replace("</", "<\\/")
html = (HERE / "geisha_template.html").read_text(encoding="utf-8").replace("__ART__", embedded)
(HERE / "geisha.html").write_text(html, encoding="utf-8")

lines = art.splitlines()
print(f"Built geisha.html from {art_path.name}: {max(map(len, lines))} x {len(lines)} characters")
