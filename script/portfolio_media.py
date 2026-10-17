"""Build the web media used on the portfolio page (export/web/).

Usage (from the repo root, after `npm install` in edit/):
  python script/portfolio_media.py
Outputs: muted teaser MP4, 1200x675 card, 1600 px WebP stills, previz-vs-final and shot-sheet boards.
"""
import os
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
EDIT = os.path.join(ROOT, "edit")
WEB = os.path.join(ROOT, "export", "web")
TMP = tempfile.mkdtemp(prefix="tension_")

# (output name, master frame) — frames chosen where each chapter's text is fully on screen
STILLS = [
    ("01-repos", 250),
    ("02-ressort", 100),
    ("03-tension", 360),
    ("04-equilibre", 600),
    ("05-lumiere", 790),
    ("06-fin", 870),
]
CARD_FRAME = 790
# (shot, source clip, time in s) for the shot sheet, in edit order
SHEET = [
    ("P02", "P02.mp4", 1.5), ("P03", "P03.mp4", 1.0), ("P04", "P04.mp4", 2.0),
    ("P05", "P05.mp4", 3.5), ("P06", "P06.mp4", 1.0), ("P07", "P07.mp4", 2.5),
    ("P08", "P08.mp4", 3.0), ("P09", "P09.mp4", 0.8), ("P10", "P10.mp4", 4.5),
]
WEBP_WIDTH = 1600
WEBP_QUALITY = 85


def run(*args):
    subprocess.run(args, cwd=EDIT, check=True, shell=os.name == "nt")


def still(frame, path):
    run("npx", "remotion", "still", "src/index.ts", "Tension", path, "--frame", str(frame), "--log=error")


def grab(clip, seconds, path):
    run("npx", "remotion", "ffmpeg", "-v", "error", "-y", "-ss", str(seconds),
        "-i", os.path.join(EDIT, "public", clip), "-frames:v", "1", path)


def save_webp(img, name, width=WEBP_WIDTH):
    h = round(img.height * width / img.width)
    img.convert("RGB").resize((width, h), Image.LANCZOS).save(
        os.path.join(WEB, f"{name}.webp"), "WEBP", quality=WEBP_QUALITY, method=6)


def label(img, text):
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("consola.ttf", 28)
    except OSError:
        font = ImageFont.load_default()
    draw.rectangle((0, 0, img.width, 52), fill=(0, 0, 0))
    draw.text((20, 12), text, fill=(239, 235, 228), font=font)
    return img


def previz_board():
    """Blender previz reference next to the Seedance result, same shot and moment."""
    ref = Image.open(os.path.join(ROOT, "export", "shots", "ref", "P05_last.png")).convert("RGB")
    out = os.path.join(TMP, "p05_draft.png")
    grab("P05.mp4", 4.9, out)
    gen = Image.open(out).convert("RGB").resize(ref.size, Image.LANCZOS)
    board = Image.new("RGB", (ref.width * 2 + 24, ref.height), (15, 14, 13))
    board.paste(label(ref, "PRÉVIZ BLENDER (EEVEE)"), (0, 0))
    board.paste(label(gen, "SEEDANCE 2.5 (BROUILLON 480P)"), (ref.width + 24, 0))
    save_webp(board, "07-previz-vs-seedance", 2000)


def shot_sheet():
    frames = []
    for shot, clip, t in SHEET:
        path = os.path.join(TMP, f"{shot}.png")
        grab(clip, t, path)
        frames.append(label(Image.open(path).convert("RGB").resize((960, 540), Image.LANCZOS), shot))
    gap = 12
    sheet = Image.new("RGB", (960 * 3 + gap * 2, 540 * 3 + gap * 2), (15, 14, 13))
    for i, img in enumerate(frames):
        sheet.paste(img, ((i % 3) * (960 + gap), (i // 3) * (540 + gap)))
    save_webp(sheet, "08-planche-plans", 2000)


def main():
    os.makedirs(WEB, exist_ok=True)
    for name, frame in STILLS:
        path = os.path.join(TMP, f"{name}.png")
        still(frame, path)
        save_webp(Image.open(path), name)
        if frame == CARD_FRAME:
            Image.open(path).convert("RGB").resize((1200, 675), Image.LANCZOS).save(
                os.path.join(WEB, "card.webp"), "WEBP", quality=WEBP_QUALITY, method=6)
    previz_board()
    shot_sheet()
    run("npx", "remotion", "render", "src/index.ts", "Tension", os.path.join(WEB, "tension-teaser.mp4"),
        "--codec", "h264", "--crf", "28", "--muted", "--log=error", "--overwrite")
    for f in sorted(os.listdir(WEB)):
        print(f"{f}: {os.path.getsize(os.path.join(WEB, f)) // 1024} Ko")


if __name__ == "__main__":
    main()
