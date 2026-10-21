"""Product mockup scenes + share (OG) cards, made locally from the real PDF page renders.

Nothing here is a stock photo or an AI picture: every page shown is the real page from the PDF
(img/<kit>-<page>.webp, made by assets.py). The props (clipboard, tablet, pen) are drawn in code.

Run:  python _src/mockups.py   (from D:\\Claude\\steady-focus-site, after assets.py)
Out:  img/scene-<kit>.webp (1200w), img/scene-<kit>-sm.webp (640w), transparent background
      img/og-<kit>.jpg 1200x630 (overwrites the old fanned-page OG cards), img/og-guide.jpg, img/og-about.jpg
"""
import math, pathlib, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops

ROOT = pathlib.Path(__file__).resolve().parents[1]
IMG = ROOT / "img"
FONTS = ROOT / "_src" / "fonts"
S = 2  # supersample

TEAL = (31, 111, 107)
TEAL_INK = (15, 53, 51)
CREAM = (251, 248, 243)
CLAY = (213, 121, 74)
CTA = (181, 83, 42)


def page(name, w):
    im = Image.open(IMG / f"{name}.webp").convert("RGBA")
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def rrect_mask(size, r):
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), r, fill=255)
    return m


def light(im, strength=26):
    """Soft top-left light falloff so flat paper reads as a lit object."""
    w, h = im.size
    n = int(math.hypot(w, h)) + 4
    g = Image.linear_gradient("L").resize((n, n)).rotate(-35, resample=Image.BICUBIC)
    g = g.crop(((n - w) // 2, (n - h) // 2, (n - w) // 2 + w, (n - h) // 2 + h))
    shade = Image.new("RGBA", (w, h), (20, 30, 30, 0))
    shade.putalpha(g.point(lambda v: int(v * strength / 255)))
    out = im.copy()
    out.alpha_composite(shade)
    out.putalpha(im.getchannel("A"))
    return out


def paper(name, w, curl=True):
    p = page(name, w)
    sheet = Image.new("RGBA", p.size, (255, 255, 255, 255))
    sheet.alpha_composite(p)
    return light(sheet, 22)


def grain(size, base, amp=10, seed=1):
    random.seed(seed)
    im = Image.new("RGB", size, base)
    n = Image.effect_noise(size, 40).convert("L")
    n = n.resize((size[0] // 3, size[1] // 3)).resize(size, Image.BICUBIC)
    # stretch noise into wood-ish fibres along x
    fib = Image.effect_noise((size[0] // 24 + 1, size[1]), 60).convert("L").resize(size, Image.BICUBIC)
    mix = ImageChops.add(n.point(lambda v: v * 0.5), fib.point(lambda v: v * 0.5))
    tint = Image.new("RGB", size, tuple(max(0, c - amp * 2) for c in base))
    return Image.composite(tint, im, mix.point(lambda v: int(max(0, v - 90) * 1.4)))


def clipboard(name, w):
    """Hardboard clipboard with a real page clipped on, metal clip on top."""
    pw = int(w * 0.86)
    pg = paper(name, pw)
    bh = int(pg.height + w * 0.19)
    board = grain((w, bh), (172, 126, 82), amp=9, seed=3).convert("RGBA")
    board.putalpha(rrect_mask((w, bh), int(w * 0.045)))
    # bevel edge
    edge = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
    d = ImageDraw.Draw(edge)
    d.rounded_rectangle((2, 2, w - 3, bh - 3), int(w * 0.045), outline=(110, 74, 40, 150), width=max(2, w // 220))
    board.alpha_composite(edge)
    board = light(board, 30)
    # page shadow on board
    px, py = (w - pw) // 2, int(w * 0.125)
    sh = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rectangle((px + 3, py + 6, px + pw + 3, py + pg.height + 8), fill=(40, 22, 8, 120))
    board.alpha_composite(sh.filter(ImageFilter.GaussianBlur(w // 90)))
    board.alpha_composite(pg, (px, py))
    # clip
    cw, ch = int(w * 0.36), int(w * 0.105)
    cx, cy = (w - cw) // 2, int(w * 0.03)
    clip = Image.new("RGBA", (cw, ch), (0, 0, 0, 0))
    grad = Image.linear_gradient("L").resize((cw, ch)).point(lambda v: 150 + v * 90 // 255)
    metal = Image.merge("RGBA", (grad, grad.point(lambda v: v + 4), grad.point(lambda v: v + 10), rrect_mask((cw, ch), ch // 3)))
    clip.alpha_composite(metal)
    cd = ImageDraw.Draw(clip)
    cd.rounded_rectangle((cw * .18, ch * .28, cw * .82, ch * .62), ch // 6, fill=(120, 126, 132, 255))
    cd.rounded_rectangle((cw * .18, ch * .28, cw * .82, ch * .40), ch // 8, fill=(205, 210, 214, 255))
    csh = Image.new("RGBA", (w, bh), (0, 0, 0, 0))
    m = Image.new("L", (w, bh), 0)
    m.paste(clip.getchannel("A"), (cx, cy + ch // 5))
    csh.putalpha(m.point(lambda v: v * 120 // 255))
    board.alpha_composite(csh.filter(ImageFilter.GaussianBlur(w // 120)))
    board.alpha_composite(clip, (cx, cy))
    return board


def tablet(name, w):
    """Plain tablet (no brand), the real page on screen."""
    h = int(w * 1.36)
    t = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(t)
    r = int(w * 0.075)
    d.rounded_rectangle((0, 0, w - 1, h - 1), r, fill=(36, 41, 44, 255))
    d.rounded_rectangle((w * .012, w * .012, w * .988 - 1, h - w * .012 - 1), int(r * .9), fill=(22, 25, 27, 255))
    bz = int(w * 0.06)
    sw, shh = w - 2 * bz, h - 2 * bz
    screen = Image.new("RGBA", (sw, shh), (250, 249, 246, 255))
    pg = page(name, int(sw * 0.94))
    if pg.height > shh * 0.97:
        pg = page(name, int(sw * 0.94 * shh * 0.97 / pg.height))
    screen.alpha_composite(pg, ((sw - pg.width) // 2, (shh - pg.height) // 2))
    screen.putalpha(rrect_mask((sw, shh), int(r * .35)))
    t.alpha_composite(screen, (bz, bz))
    # diagonal glare
    gl = Image.new("L", (w, h), 0)
    ImageDraw.Draw(gl).polygon([(0, h * .1), (w * .55, 0), (w, 0), (w, h * .05), (0, h * .62)], fill=26)
    glare = Image.new("RGBA", (w, h), (255, 255, 255, 0))
    glare.putalpha(ImageChops.multiply(gl.filter(ImageFilter.GaussianBlur(w // 40)), t.getchannel("A")))
    t.alpha_composite(glare)
    # camera dot
    d.ellipse((w / 2 - w * .008, bz * .42, w / 2 + w * .008, bz * .42 + w * .016), fill=(60, 66, 70, 255))
    return t


def pen(length, color=CTA):
    """A plain pen: barrel with a round highlight, a metal tip, a clip."""
    th = max(8, length // 13)
    im = Image.new("RGBA", (length, th * 3), (0, 0, 0, 0))
    body = Image.new("RGBA", (int(length * .86), th), color + (255,))
    shade = Image.linear_gradient("L").rotate(90).resize(body.size)
    hi = shade.point(lambda v: int(abs(v - 70) < 40 and (40 - abs(v - 70)) * 4))
    dark = shade.point(lambda v: int(max(0, v - 150) * .9))
    body.alpha_composite(Image.merge("RGBA", (*[Image.new("L", body.size, 255)] * 3, hi)))
    body.alpha_composite(Image.merge("RGBA", (*[Image.new("L", body.size, 0)] * 3, dark)))
    body.putalpha(rrect_mask(body.size, th // 2))
    y = th
    im.alpha_composite(body, (int(length * .14), y))
    d = ImageDraw.Draw(im)
    d.polygon([(int(length * .14) + 2, y), (int(length * .14) + 2, y + th), (int(length * .02), y + th // 2)], fill=(196, 198, 200, 255))
    d.polygon([(int(length * .04), y + th * .38), (int(length * .04), y + th * .62), (0, y + th // 2)], fill=(40, 40, 40, 255))
    d.rounded_rectangle((int(length * .70), y - th * .22, int(length * .93), y + th * .18), th // 5, fill=(214, 216, 219, 255))
    return im


def place(canvas, obj, xy, angle, shadow=(16, 30, 0.55, 26)):
    """Rotate obj, drop a soft cast shadow + a tight contact shadow, paste centred at xy."""
    o = obj.rotate(angle, expand=True, resample=Image.BICUBIC)
    a = o.getchannel("A")
    dx, dy, op, blur = shadow
    for (ox, oy, opac, bl) in ((dx * S, dy * S, op, blur * S), (2 * S, 4 * S, 0.35, 3 * S)):
        sh = Image.new("RGBA", o.size, (8, 28, 26, 0))
        sh.putalpha(a.point(lambda v: int(v * opac)))
        pad = bl * 3
        big = Image.new("RGBA", (o.width + pad * 2, o.height + pad * 2), (0, 0, 0, 0))
        big.alpha_composite(sh, (pad, pad))
        big = big.filter(ImageFilter.GaussianBlur(bl))
        canvas.alpha_composite(big, (int(xy[0] - o.width / 2 + ox - pad), int(xy[1] - o.height / 2 + oy - pad)))
    canvas.alpha_composite(o, (int(xy[0] - o.width / 2), int(xy[1] - o.height / 2)))


def scene(kit, front, tab, loose):
    W, H = 1320 * S, 1080 * S
    c = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    place(c, paper(loose, 470 * S), (980 * S, 480 * S), -11, (14, 26, .5, 24))
    place(c, tablet(tab, 500 * S), (360 * S, 480 * S), 7, (18, 34, .55, 30))
    place(c, clipboard(front, 560 * S), (670 * S, 570 * S), -3, (22, 40, .6, 34))
    place(c, pen(430 * S), (910 * S, 950 * S), 14, (10, 18, .5, 12))
    c = c.resize((1320, 1080), Image.LANCZOS)
    bbox = c.getchannel("A").point(lambda v: 255 if v > 6 else 0).getbbox()
    c = c.crop(bbox)
    c.save(IMG / f"scene-{kit}.webp", "WEBP", quality=80, method=6)
    sm = c.resize((640, round(c.height * 640 / c.width)), Image.LANCZOS)
    sm.save(IMG / f"scene-{kit}-sm.webp", "WEBP", quality=78, method=6)
    print("scene", kit, c.size, sm.size)
    return c


def font(kind, size):
    if kind == "display":
        f = ImageFont.truetype(str(FONTS / "Bricolage.ttf"), size)
        try:
            f.set_variation_by_axes([max(12, min(96, size)), 800, 100])
        except Exception:
            pass
        return f
    return ImageFont.truetype(str(FONTS / ("Atkinson-Bold.ttf" if kind == "bold" else "Atkinson-Regular.ttf")), size)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=f) <= maxw:
            cur = t
        else:
            lines.append(cur); cur = wd
    lines.append(cur)
    return lines


def og(slug, sc, title, mark, foot, price="$7"):
    W, H = 1200, 630
    bg = Image.new("RGBA", (W, H), TEAL + (255,))
    # soft vignette
    v = Image.radial_gradient("L").resize((W * 2, H * 2)).crop((W // 2, H // 2, W * 3 // 2, H * 3 // 2))
    dark = Image.new("RGBA", (W, H), TEAL_INK + (0,))
    dark.putalpha(v.point(lambda x: int(x * .55)))
    bg.alpha_composite(dark)
    s = sc.copy()
    s.thumbnail((640, 560), Image.LANCZOS)
    bg.alpha_composite(s, (W - s.width + 40, (H - s.height) // 2 + 20))
    d = ImageDraw.Draw(bg)
    # logo mark
    d.rounded_rectangle((60, 54, 100, 94), 10, fill=CREAM)
    d.line((69, 80, 91, 80), fill=TEAL, width=4); d.line((72, 70, 88, 70), fill=TEAL, width=4)
    d.ellipse((75, 75, 85, 85), fill=CLAY)
    d.text((114, 60), "Steady Focus Co.", font=font("display", 28), fill=CREAM)
    fz = 60
    f = font("display", fz)
    lines = title
    y = 138
    for i, ln in enumerate(lines):
        d.text((60, y), ln, font=f, fill=(255, 255, 255))
        y += int(fz * 1.02)
        if mark and i == len(lines) - 1:
            lw = d.textlength(ln, font=f)
            d.rectangle((60, y + 2, 60 + lw, y + 9), fill=CLAY)
    y += 44
    if price:
        d.rounded_rectangle((60, y, 60 + 120, y + 58), 12, fill=CTA)
        d.text((60 + 60, y + 29), price, font=font("display", 36), fill=(255, 255, 255), anchor="mm")
        d.text((200, y + 29), foot, font=font("bold", 24), fill=(220, 235, 232), anchor="lm")
    else:
        d.text((60, y + 20), foot, font=font("bold", 24), fill=(220, 235, 232), anchor="lm")
    bg.convert("RGB").save(IMG / f"og-{slug}.jpg", "JPEG", quality=86, optimize=True, progressive=True)
    print("og", slug)


if __name__ == "__main__":
    f = scene("focus", "focus-daily-focus-planner", "focus-dopamine-menu", "focus-weekly-habit-tracker")
    t = scene("task", "task-micro-step-breakdown", "task-five-minute-start-timer", "task-one-task-at-a-time")
    m = scene("time", "time-time-block-card", "time-stop-alarm-checklist", "time-time-cost-estimator")
    og("focus-bundle", f, ["Your planner", "isn't the problem.", "Its size is."], True, "11 printable pages · instant PDF")
    og("task-kit", t, ["Your to-do list", "is missing", "the first move."], True, "4 printable pages · instant PDF")
    og("time-kit", m, ["Time plans with", "the 50% buffer", "already built in."], True, "4 printable pages · instant PDF")
    og("guide", f, ["ADHD planners", "and focus tools,", "compared fairly."], False, "A plain guide · paper, apps and printables", price=None)
    og("about", f, ["Small printable", "pages.", "One job each."], False, "About Steady Focus Co.", price=None)
