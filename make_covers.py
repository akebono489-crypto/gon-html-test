from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1600, 2560

MINCHO = "/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf"
GOTHIC = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        draw.line([(0, y), (w, y)], fill=c)
    return img


def cx(draw, text, y, fnt, fill, width=W, stroke=0, stroke_fill=None):
    """Center text horizontally at given y (top of text)."""
    tw = draw.textlength(text, font=fnt)
    x = (width - tw) / 2
    kw = {}
    if stroke:
        kw = {"stroke_width": stroke, "stroke_fill": stroke_fill or (0, 0, 0)}
    draw.text((x, y), text, font=fnt, fill=fill, **kw)
    bb = fnt.getbbox(text)
    return y + (bb[3] - bb[1])


# ─────────────────────────────────────────────────────────────────
#  COVER 1: Kindle  — 深オレンジ→赤の濃グラデ、明朝極太タイトル
# ─────────────────────────────────────────────────────────────────
def make_kindle():
    img = gradient(W, H, (210, 70, 0), (120, 10, 10))
    draw = ImageDraw.Draw(img)

    # ── 上部ゴールドライン ──
    draw.rectangle([(0, 0), (W, 22)], fill=(255, 205, 40))

    # ── ジャンル帯 ──
    draw.rectangle([(0, 42), (W, 155)], fill=(0, 0, 0))
    f_label = font(GOTHIC, 54)
    cx(draw, "生活再建・年金・AI活用  完全ガイド", 62, f_label, (255, 210, 40))

    # ── メインタイトル（明朝・超大・白＋黒縁） ──
    f_t1 = font(MINCHO, 220)   # 「老後破綻」
    f_t2 = font(MINCHO, 130)   # 「からの」
    f_t3 = font(MINCHO, 220)   # 「リスタート」

    y = 230
    y = cx(draw, "老後破綻", y, f_t1, (255, 255, 255), stroke=6, stroke_fill=(80, 20, 0))
    y += 10
    y = cx(draw, "からの", y, f_t2, (255, 225, 140), stroke=4, stroke_fill=(80, 20, 0))
    y += 10
    y = cx(draw, "リスタート", y, f_t3, (255, 255, 255), stroke=6, stroke_fill=(80, 20, 0))

    # ── 仕切りライン ──
    sep_y = y + 50
    draw.rectangle([(60, sep_y), (W - 60, sep_y + 8)], fill=(255, 210, 40))

    # ── サブタイトル（明朝・中） ──
    f_sub = font(MINCHO, 68)
    sy = sep_y + 60
    sy = cx(draw, "年金・生活保護・AIで", sy, f_sub, (255, 245, 200))
    sy += 14
    sy = cx(draw, "「死なない暮らし」をつくる", sy, f_sub, (255, 245, 200))

    # ── 下部バー ──
    draw.rectangle([(0, H - 240), (W, H - 236)], fill=(255, 210, 40))
    draw.rectangle([(0, H - 236), (W, H)], fill=(15, 5, 0))

    # ── 著者名（明朝・大） ──
    f_auth = font(MINCHO, 90)
    cx(draw, "中川昌風", H - 186, f_auth, (255, 215, 50))

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print("cover_kindle.jpg saved")


# ─────────────────────────────────────────────────────────────────
#  COVER 2: Paperback — 黄→オレンジ、黒帯に白明朝タイトル
# ─────────────────────────────────────────────────────────────────
def make_paperback():
    img = gradient(W, H, (255, 210, 20), (215, 75, 0))
    draw = ImageDraw.Draw(img)

    # ── 著者名帯（上） ──
    draw.rectangle([(0, 0), (W, 180)], fill=(15, 5, 0))
    f_auth = font(MINCHO, 80)
    cx(draw, "中川昌風 著", 50, f_auth, (255, 215, 50))

    # ── タイトル黒帯 ──
    title_top = 220
    title_bot = 1160
    draw.rectangle([(0, title_top), (W, title_bot)], fill=(15, 5, 0))

    # 黒帯内にゴールドラインで枠
    draw.rectangle([(30, title_top + 20), (W - 30, title_top + 26)], fill=(255, 205, 40))
    draw.rectangle([(30, title_bot - 26), (W - 30, title_bot - 20)], fill=(255, 205, 40))

    # ── タイトル文字（明朝・超大・白） ──
    f_t1 = font(MINCHO, 230)
    f_t2 = font(MINCHO, 140)
    f_t3 = font(MINCHO, 230)

    y = title_top + 56
    y = cx(draw, "老後破綻", y, f_t1, (255, 255, 255), stroke=5, stroke_fill=(60, 15, 0))
    y += 8
    y = cx(draw, "からの", y, f_t2, (255, 220, 100), stroke=3, stroke_fill=(60, 15, 0))
    y += 8
    cx(draw, "リスタート", y, f_t3, (255, 255, 255), stroke=5, stroke_fill=(60, 15, 0))

    # ── 黄帯アクセント ──
    draw.rectangle([(0, title_bot), (W, title_bot + 16)], fill=(255, 205, 40))

    # ── サブタイトル（明朝・大・黒文字、暖色背景上） ──
    f_sub = font(MINCHO, 72)
    sy = title_bot + 80
    sy = cx(draw, "年金・生活保護・AIで", sy, f_sub, (30, 8, 0))
    sy += 16
    cx(draw, "「死なない暮らし」をつくる", sy, f_sub, (30, 8, 0))

    # ── キャッチコピー枠 ──
    box_top = 1600
    draw.rectangle([(60, box_top), (W - 60, box_top + 280)], fill=(15, 5, 0))
    draw.rectangle([(60, box_top), (W - 60, box_top + 4)], fill=(255, 205, 40))
    draw.rectangle([(60, box_top + 276), (W - 60, box_top + 280)], fill=(255, 205, 40))

    f_tag = font(MINCHO, 52)
    ty = box_top + 30
    for line in ["誰も教えてくれなかった制度の使い方を",
                 "崖っぷちから這い上がった著者が語る"]:
        ty = cx(draw, line, ty, f_tag, (255, 235, 180))
        ty += 12

    # ── 下部 ──
    draw.rectangle([(0, H - 180), (W, H)], fill=(15, 5, 0))
    f_small = font(GOTHIC, 46)
    cx(draw, "ISBN 978-X-XXXX-XXXX-X", H - 130, f_small, (140, 120, 80))

    img.save("cover_paperback_temp.jpg", "JPEG", quality=95)
    print("cover_paperback_temp.jpg saved")


make_kindle()
make_paperback()
