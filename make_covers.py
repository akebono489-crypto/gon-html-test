from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
GOTHIC = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"

BLACK  = (10, 8, 8)
RED    = (210, 30, 20)
WHITE  = (255, 255, 255)
GRAY   = (180, 175, 170)


def f(size):
    return ImageFont.truetype(GOTHIC, size)


def tw(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def th(fnt, ch="字"):
    b = fnt.getbbox(ch)
    return b[3] - b[1]


def cx(draw, text, y, fnt, fill, stroke=0, sc=(0,0,0)):
    x = (W - tw(draw, text, fnt)) / 2
    kw = {"stroke_width": stroke, "stroke_fill": sc} if stroke else {}
    draw.text((x, y), text, font=fnt, fill=fill, **kw)
    return y + th(fnt, text[0] if text else "字")


def max_font(draw, text, max_px):
    size = 40
    while tw(draw, text, f(size + 2)) <= max_px:
        size += 2
    return size


def make_kindle():
    MARGIN = 60
    INNER  = W - MARGIN * 2

    img = Image.new("RGB", (W, H), BLACK)
    draw = ImageDraw.Draw(img)

    # ── タイトルブロック全体の高さを計算して垂直中央寄せ ──
    # 「老後破綻」
    s1 = max_font(draw, "老後破綻", INNER)
    fnt1 = f(s1)
    h1 = th(fnt1, "老")

    # 「からの」— 幅の45%
    s2 = max_font(draw, "からの", int(INNER * 0.44))
    fnt2 = f(s2)
    h2 = th(fnt2, "か")

    # 「リスタート」
    s3 = max_font(draw, "リスタート", INNER)
    fnt3 = f(s3)
    h3 = th(fnt3, "リ")

    GAP = 28   # 行間
    title_total = h1 + GAP + h2 + GAP + h3

    # サブタイトル
    fs = f(72)
    sub1 = "年金・生活保護・AIで"
    sub2 = "「死なない暮らし」をつくる"
    hs = th(fs)
    sub_total = hs + 20 + hs

    # 著者名
    fa_jp = f(80)
    fa_en = f(58)
    author_jp = "中川　昌風"
    author_en = "SHOFUU  NAKAGAWA"
    ha_jp = th(fa_jp)
    ha_en = th(fa_en)

    # 区切り線2本
    line_h = 6
    gap_after_line = 50

    # 全体レイアウト（上余白 / タイトル / 区切り / サブ / 余白 / 著者帯）
    author_band_h = ha_jp + 16 + ha_en + 60   # 著者帯
    top_content_h = (title_total + gap_after_line + line_h + gap_after_line
                     + sub_total + gap_after_line + line_h)

    # タイトル開始Y：画面上60%に収め、少し上寄り
    y_start = max(120, (H - author_band_h - 200 - top_content_h) // 2)

    # ── 赤い縦アクセントライン（左端）─────────────────────
    draw.rectangle([(0, 0), (18, H)], fill=RED)

    # ── タイトル ─────────────────────────────────────────
    y = y_start

    # 「老後破綻」白
    cx(draw, "老後破綻", y, fnt1, WHITE, stroke=0)
    y += h1 + GAP

    # 「からの」赤・小
    cx(draw, "からの", y, fnt2, RED)
    y += h2 + GAP

    # 「リスタート」白
    cx(draw, "リスタート", y, fnt3, WHITE, stroke=0)
    y += h3 + gap_after_line

    # ── 区切り線 ─────────────────────────────────────────
    draw.rectangle([(MARGIN, y), (W - MARGIN, y + line_h)], fill=RED)
    y += line_h + gap_after_line

    # ── サブタイトル（白・中サイズ） ─────────────────────
    cx(draw, sub1, y, fs, WHITE)
    y += hs + 20
    cx(draw, sub2, y, fs, WHITE)
    y += hs + gap_after_line

    # ── 区切り線 ─────────────────────────────────────────
    draw.rectangle([(MARGIN, y), (W - MARGIN, y + line_h)], fill=RED)

    # ── 著者名（下部・中央）──────────────────────────────
    # 著者帯は下から固定位置
    ay = H - author_band_h
    draw.rectangle([(0, ay - 30), (W, ay - 24)], fill=RED)

    ay += 30
    cx(draw, author_jp, ay, fa_jp, WHITE)
    ay += ha_jp + 16
    cx(draw, author_en, ay, fa_en, GRAY)

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print(f"saved  老後破綻:{s1}px  からの:{s2}px  リスタート:{s3}px")


make_kindle()
