from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 2560
GOTHIC = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"
MINCHO = "/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf"


def f(size, mincho=False):
    return ImageFont.truetype(MINCHO if mincho else GOTHIC, size)


def tw(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def th(fnt, ch="字"):
    b = fnt.getbbox(ch)
    return b[3] - b[1]


def cx(draw, text, y, fnt, fill, stroke=0, sc=(0, 0, 0)):
    x = (W - tw(draw, text, fnt)) / 2
    kw = {"stroke_width": stroke, "stroke_fill": sc} if stroke else {}
    draw.text((x, y), text, font=fnt, fill=fill, **kw)
    return y + th(fnt, text[0])


def grad(w, h, top, bot):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


# ══════════════════════════════════════════════════════════════
#  KINDLE COVER — 文字圧力全振り版
#  構造：著者帯 / 老後破綻 / からの / リスタート（最大）/ 区切り / サブタイトル
# ══════════════════════════════════════════════════════════════
def make_kindle():
    # 背景：黒 → 極深ダークレッド（重厚感）
    img = grad(W, H, (18, 8, 0), (80, 15, 0))
    draw = ImageDraw.Draw(img)

    # ── 著者帯（最上部）──────────────────────────────────────
    draw.rectangle([(0, 0), (W, 100)], fill=(200, 60, 0))
    fa = f(60)
    draw.text(((W - tw(draw, "中川 昌風 著", fa)) / 2, 20),
              "中川 昌風 著", font=fa, fill=(255, 255, 255))

    # ── ゴールドライン ─────────────────────────────────────
    draw.rectangle([(0, 100), (W, 116)], fill=(255, 195, 0))

    # ──「老後破綻」──────────────────────────────────────────
    # 幅いっぱいに収まる最大サイズを計算
    f1_size = 10
    while tw(draw, "老後破綻", f(f1_size)) < W - 40:
        f1_size += 2
    f1_size -= 2
    fnt1 = f(f1_size)

    y = 130
    cx(draw, "老後破綻", y, fnt1, (255, 255, 255), stroke=6, sc=(180, 40, 0))
    y += th(fnt1, "老") + 0   # ほぼ詰める

    # ──「からの」──────────────────────────────────────────
    f2_size = 10
    while tw(draw, "からの", f(f2_size)) < W * 0.55:
        f2_size += 2
    f2_size -= 2
    fnt2 = f(f2_size)

    # 「からの」は中央寄せ、オレンジ
    cx(draw, "からの", y, fnt2, (255, 160, 0), stroke=4, sc=(100, 20, 0))
    y += th(fnt2, "か") + 10

    # ──「リスタート」最大サイズ ─────────────────────────────
    f3_size = 10
    while tw(draw, "リスタート", f(f3_size)) < W - 20:
        f3_size += 2
    f3_size -= 2
    fnt3 = f(f3_size)

    # 白抜き + 厚めストローク
    cx(draw, "リスタート", y, fnt3, (255, 255, 255), stroke=8, sc=(180, 40, 0))
    y += th(fnt3, "リ") + 20

    # ── 太いゴールド仕切り ──────────────────────────────────
    draw.rectangle([(0, y), (W, y + 18)], fill=(255, 195, 0))
    y += 18

    # ── オレンジ背景ゾーン（サブタイトルエリア） ───────────
    sub_zone_h = H - y - 160
    draw.rectangle([(0, y), (W, y + sub_zone_h)], fill=(210, 70, 0))

    # サブタイトル
    fs = f(72)
    margin = 30
    y += margin
    cx(draw, "年金・生活保護・AIで", y, fs, (255, 255, 255))
    y += th(fs) + 14
    cx(draw, "「死なない暮らし」をつくる", y, fs, (255, 255, 220))
    y += th(fs) + 30

    # ミニキャッチ
    fm = f(54)
    cx(draw, "誰も教えてくれなかった制度の使い方", y, fm, (255, 230, 160))
    y += th(fm) + 10
    cx(draw, "崖っぷちから這い上がった著者が語る", y, fm, (255, 230, 160))

    # ── 最下部帯 ─────────────────────────────────────────
    draw.rectangle([(0, H - 160), (W, H)], fill=(10, 4, 0))
    draw.rectangle([(0, H - 160), (W, H - 148)], fill=(255, 195, 0))
    fp = f(54)
    cx(draw, "産業能率大学出版部", H - 110, fp, (160, 130, 80))

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print(f"cover_kindle.jpg  f1={f1_size} f2={f2_size} f3={f3_size}")


# ══════════════════════════════════════════════════════════════
#  PAPERBACK COVER — 同じ構造・白背景バリエーション
# ══════════════════════════════════════════════════════════════
def make_paperback():
    img = Image.new("RGB", (W, H), (252, 248, 238))
    draw = ImageDraw.Draw(img)

    # ── 著者帯 ───────────────────────────────────────────
    draw.rectangle([(0, 0), (W, 100)], fill=(20, 10, 0))
    fa = f(60)
    draw.text(((W - tw(draw, "中川 昌風 著", fa)) / 2, 20),
              "中川 昌風 著", font=fa, fill=(255, 195, 0))

    draw.rectangle([(0, 100), (W, 116)], fill=(220, 60, 0))

    # ──「老後破綻」──────────────────────────────────────
    f1_size = 10
    while tw(draw, "老後破綻", f(f1_size)) < W - 40:
        f1_size += 2
    f1_size -= 2
    fnt1 = f(f1_size)

    y = 130
    cx(draw, "老後破綻", y, fnt1, (20, 8, 0), stroke=3, sc=(200, 60, 0))
    y += th(fnt1, "老") + 0

    # ──「からの」──────────────────────────────────────
    f2_size = 10
    while tw(draw, "からの", f(f2_size)) < W * 0.55:
        f2_size += 2
    f2_size -= 2
    fnt2 = f(f2_size)

    cx(draw, "からの", y, fnt2, (210, 60, 0))
    y += th(fnt2, "か") + 10

    # ──「リスタート」最大 ──────────────────────────────
    f3_size = 10
    while tw(draw, "リスタート", f(f3_size)) < W - 20:
        f3_size += 2
    f3_size -= 2
    fnt3 = f(f3_size)

    cx(draw, "リスタート", y, fnt3, (200, 40, 0), stroke=5, sc=(255, 160, 0))
    y += th(fnt3, "リ") + 16

    # ── 仕切り ────────────────────────────────────────
    draw.rectangle([(0, y), (W, y + 18)], fill=(220, 60, 0))
    y += 18

    # ── 黒帯ゾーン：サブタイトル ──────────────────────
    sub_zone_h = H - y - 140
    draw.rectangle([(0, y), (W, y + sub_zone_h)], fill=(20, 8, 0))

    fs = f(72)
    y += 40
    cx(draw, "年金・生活保護・AIで", y, fs, (255, 255, 255))
    y += th(fs) + 14
    cx(draw, "「死なない暮らし」をつくる", y, fs, (255, 210, 80))
    y += th(fs) + 36

    fm = f(56)
    for line in ["✓ 年金受給者でも生活保護は申請できる",
                 "✓ 持ち家・車があってもOK",
                 "✓ AIで60代から収入を再建する方法"]:
        lw = tw(draw, line, fm)
        draw.text(((W - lw) / 2, y), line, font=fm, fill=(255, 235, 160))
        y += th(fm) + 12

    # ── 最下部 ────────────────────────────────────────
    draw.rectangle([(0, H - 140), (W, H)], fill=(20, 8, 0))
    draw.rectangle([(0, H - 140), (W, H - 128)], fill=(220, 60, 0))
    fp = f(48)
    cx(draw, "ISBN 978-X-XXXX-XXXX-X", H - 96, fp, (130, 110, 80))

    img.save("cover_paperback_temp.jpg", "JPEG", quality=95)
    print(f"cover_paperback_temp.jpg  f1={f1_size} f2={f2_size} f3={f3_size}")


make_kindle()
make_paperback()
