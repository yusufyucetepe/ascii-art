from PIL import Image, ImageEnhance

chars = "█▓▒░ "      # darkest to lightest
width = 100           # characters per line; bigger = more detail

img = Image.open("geisha_clean.png").convert("L")
height = int(img.height / img.width * width * 0.45)
img = img.resize((width, height))
img = ImageEnhance.Contrast(img).enhance(1.8)

pixels = img.tobytes()
lines = []
for y in range(height):
    row = pixels[y * width:(y + 1) * width]
    lines.append("".join(chars[p * len(chars) // 256] for p in row))

art = "\n".join(lines)
print(art)

with open("geisha_ascii.txt", "w", encoding="utf-8") as f:
    f.write(art)