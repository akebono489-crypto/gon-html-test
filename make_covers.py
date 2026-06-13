from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
GOTHIC = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"

BG      = (232, 66, 10)   # #E8420A
WHITE   = (255, 255, 255)
CREAM   = (255, 245, 220)


def f(size):
    return ImageFont.truetype(GOTHIC, size)


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def text_h(fnt, ch="字"):
    b = fnt.getbbox(ch)
    return b[3] - b[1]


def max_font(draw, text, max_px, start=40):
    """画面幅 max_px に収まる最大フォントサイズを返す"""
    size = start
    while text_w(draw, text, f(size + 2)) <= max_px:
        size += 2
    return size


def cx(draw, text, y, fnt, fill):
    x = (W - text_w(draw, text, fnt)) / 2
    draw.text((x, y), text, font=fnt, fill=fill)
    return y + text_h(fnt, text[0])


# ──────────────────────────────────────────────────────────────
def make_kindle():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    MARGIN = 30          # 左右余白
    INNER  = W - MARGIN * 2

    # ── 著者名（上部・小さく） ────────────────────────────
    y = 60
    fa = f(70)
    cx(draw, "中川昌風 著", y, fa, WHITE)
    y += text_h(fa) + 40

    # ── 区切りライン ─────────────────────────────────────
    draw.rectangle([(MARGIN, y), (W - MARGIN, y + 8)], fill=WHITE)
    y += 8 + 50

    # ── 「老後破綻」幅いっぱい ────────────────────────────
    s1 = max_font(draw, "老後破綻", INNER)
    fnt1 = f(s1)
    cx(draw, "老後破綻", y, fnt1, WHITE)
    y += text_h(fnt1, "老") + 20

    # ── 「からの」小さく中央 ──────────────────────────────
    s2 = max_font(draw, "からの", INNER * 0.46)
    fnt2 = f(s2)
    cx(draw, "からの", y, fnt2, CREAM)
    y += text_h(fnt2, "か") + 20

    # ── 「リスタート」最大・幅いっぱい ────────────────────
    s3 = max_font(draw, "リスタート", INNER)
    fnt3 = f(s3)
    cx(draw, "リスタート", y, fnt3, WHITE)
    y += text_h(fnt3, "リ") + 60

    # ── 区切りライン ─────────────────────────────────────
    draw.rectangle([(MARGIN, y), (W - MARGIN, y + 8)], fill=WHITE)
    y += 8 + 50

    # ── サブタイトル（下部・小さく白文字） ──────────────
    fs = f(68)
    cx(draw, "年金・生活保護・AIで", y, fs, WHITE)
    y += text_h(fs) + 16
    cx(draw, "「死なない暮らし」をつくる", y, fs, WHITE)

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print(f"saved  s1={s1} s2={s2} s3={s3}")


make_kindle()
