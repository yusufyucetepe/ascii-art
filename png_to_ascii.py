"""Trace geisha_clean.png into geisha_traced.txt: the PNG's ink becomes characters, its white areas become spaces."""
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).parent

CHARS = ".:-=+*#%@"     # least to most ink
ROWS = 150              # lines of art; more means finer detail but smaller characters
CELL_ASPECT = 0.52      # character width / line height, matching the page's font and line spacing
EMPTY_BELOW = 0.14      # cells with less ink than this become spaces; raise it for more empty space
FULL_INK = 0.42         # ink level that gets the densest character
SOFTEN = 2.0            # blur radius in PNG pixels

ink = Image.eval(Image.open(HERE / "geisha_clean.png").convert("L"), lambda p: 255 - p)
ink = ink.crop(ink.point(lambda p: 255 if p > 128 else 0).getbbox())

cols = round(ROWS * ink.width / ink.height / CELL_ASPECT)
# The PNG's hair is drawn in stripes about as wide as a character, so sampling it unblurred creates false bands.
cells = ink.filter(ImageFilter.GaussianBlur(SOFTEN)).resize((cols, ROWS), Image.BOX).tobytes()


def char_for(value):
    coverage = value / 255
    if coverage < EMPTY_BELOW:
        return " "
    level = (coverage - EMPTY_BELOW) / (FULL_INK - EMPTY_BELOW)
    return CHARS[min(len(CHARS) - 1, int(level * len(CHARS)))]


lines = ["".join(char_for(v) for v in cells[r * cols:(r + 1) * cols]).rstrip() for r in range(ROWS)]
(HERE / "geisha_traced.txt").write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote geisha_traced.txt: {cols} x {ROWS} characters")
