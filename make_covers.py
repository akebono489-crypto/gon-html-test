from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 2560
GOTHIC = "/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf"
MINCHO = "/usr/share/fonts/opentype/ipaexfont-mincho/ipaexm.ttf"


def f(path, size):
    return ImageFont.truetype(path, size)


def grad(w, h, top, bottom):
    img = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)
    return img


def cx(draw, text, y, fnt, fill, stroke=0, sc=(0, 0, 0)):
    tw = draw.textlength(text, font=fnt)
    x = (W - tw) / 2
    kw = {"stroke_width": stroke, "stroke_fill": sc} if stroke else {}
    draw.text((x, y), text, font=fnt, fill=fill, **kw)
    bb = fnt.getbbox(text)
    return y + bb[3] - bb[1]


def text_h(fnt, text="A"):
    bb = fnt.getbbox(text)
    return bb[3] - bb[1]


# ══════════════════════════════════════════════════════════════════
#  COVER 1: Kindle
#  白地に近い薄クリーム → 鮮烈オレンジ帯でタイトルを強調
#  参考書と同じ「白背景 + カラー帯 + 極太ゴシック」スタイル
# ══════════════════════════════════════════════════════════════════
def make_kindle():
    # 背景：クリームホワイト
    img = Image.new("RGB", (W, H), (255, 252, 242))
    draw = ImageDraw.Draw(img)

    # ── 最上部オレンジ帯（キャッチ） ──────────────────────────
    draw.rectangle([(0, 0), (W, 140)], fill=(230, 80, 0))
    fc = f(GOTHIC, 62)
    cw = draw.textlength("年金・生活保護・AIを使いこなす！", font=fc)
    draw.text(((W - cw) / 2, 38), "年金・生活保護・AIを使いこなす！",
              font=fc, fill=(255, 255, 255))

    # ── メインタイトルブロック（赤帯背景） ────────────────────
    # 「老後破綻からの」小さめ
    y = 180
    f_small = f(GOTHIC, 100)
    draw.rectangle([(0, y - 10), (W, y + text_h(f_small) + 20)], fill=(200, 40, 0))
    cx(draw, "老後破綻からの", y, f_small, (255, 255, 255))
    y += text_h(f_small) + 20

    # 「リスタート」超巨大
    f_big = f(GOTHIC, 290)
    bh = text_h(f_big, "リ")
    draw.rectangle([(0, y), (W, y + bh + 30)], fill=(220, 50, 0))
    cx(draw, "リスタート", y + 10, f_big, (255, 255, 255),
       stroke=4, sc=(120, 20, 0))
    y += bh + 50

    # ── 黄色ライン ──────────────────────────────────────────
    draw.rectangle([(0, y), (W, y + 14)], fill=(255, 200, 0))
    y += 30

    # ── 数字インパクトゾーン ─────────────────────────────────
    # 「知らないと損する　3つの制度」
    f_m = f(GOTHIC, 72)
    cx(draw, "知らないと損する", y, f_m, (180, 30, 0))
    y += text_h(f_m) + 10

    f_num = f(GOTHIC, 220)
    nh = text_h(f_num, "3")
    cx(draw, "３", y, f_num, (220, 50, 0), stroke=3, sc=(140, 20, 0))
    # "つの制度" を右横に
    f_unit = f(GOTHIC, 90)
    num_w = draw.textlength("３", font=f_num)
    unit_w = draw.textlength("つの制度", font=f_unit)
    nx = (W - num_w - unit_w - 20) / 2
    draw.text((nx + num_w + 20, y + nh - text_h(f_unit) - 10),
              "つの制度", font=f_unit, fill=(50, 50, 50))
    y += nh + 20

    draw.rectangle([(0, y), (W, y + 14)], fill=(255, 200, 0))
    y += 30

    # ── サブタイトル ──────────────────────────────────────────
    f_sub = f(GOTHIC, 68)
    draw.rectangle([(60, y), (W - 60, y + text_h(f_sub) * 2 + 50)], fill=(255, 240, 200))
    draw.rectangle([(60, y), (W - 60, y + 6)], fill=(220, 80, 0))
    draw.rectangle([(60, y + text_h(f_sub) * 2 + 44), (W - 60, y + text_h(f_sub) * 2 + 50)], fill=(220, 80, 0))
    y += 20
    cx(draw, "年金があっても申請できる", y, f_sub, (30, 30, 30))
    y += text_h(f_sub) + 10
    cx(draw, "「死なない暮らし」のつくり方", y, f_sub, (30, 30, 30))
    y += text_h(f_sub) + 50

    # ── 著者名エリア ──────────────────────────────────────────
    f_auth_label = f(GOTHIC, 52)
    f_auth = f(GOTHIC, 88)
    draw.rectangle([(0, H - 200), (W, H)], fill=(40, 20, 10))
    cx(draw, "著者", H - 188, f_auth_label, (180, 140, 80))
    cx(draw, "中川 昌風", H - 128, f_auth, (255, 220, 100))

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print("cover_kindle.jpg saved")


# ══════════════════════════════════════════════════════════════════
#  COVER 2: Paperback（表表紙）
#  オレンジグラデ背景 + 白帯タイトル。別バリエーション
# ══════════════════════════════════════════════════════════════════
def make_paperback():
    img = grad(W, H, (255, 155, 0), (200, 40, 0))
    draw = ImageDraw.Draw(img)

    # ── 上部白帯：著者 ──────────────────────────────────────
    draw.rectangle([(0, 0), (W, 130)], fill=(255, 255, 255))
    fa = f(GOTHIC, 62)
    cx(draw, "中川 昌風 著", 34, fa, (40, 20, 0))

    # ── メインタイトル（白帯に黒字） ─────────────────────────
    y = 160
    draw.rectangle([(0, y), (W, y + 16)], fill=(255, 220, 0))
    y += 16

    # 白帯背景
    title_bg_h = 950
    draw.rectangle([(0, y), (W, y + title_bg_h)], fill=(255, 255, 255))

    # 「老後破綻からの」
    f_pre = f(GOTHIC, 108)
    y += 40
    cx(draw, "老後破綻からの", y, f_pre, (200, 40, 0))
    y += text_h(f_pre) + 10

    # 「リスタート」超大
    f_main = f(GOTHIC, 280)
    cx(draw, "リスタート", y, f_main, (20, 10, 0), stroke=2, sc=(180, 60, 0))
    y += text_h(f_main, "リ") + 20

    # 黄ライン
    draw.rectangle([(60, y), (W - 60, y + 10)], fill=(255, 180, 0))
    y += 10

    # サブ
    f_sub2 = f(GOTHIC, 66)
    y += 20
    cx(draw, "年金・生活保護・AIで", y, f_sub2, (50, 20, 0))
    y += text_h(f_sub2) + 8
    cx(draw, "「死なない暮らし」をつくる", y, f_sub2, (50, 20, 0))
    y += text_h(f_sub2) + 30

    draw.rectangle([(0, y), (W, y + 16)], fill=(255, 220, 0))
    y += 16

    # ── オレンジ背景ゾーン：インパクト数字 ──────────────────
    y += 60
    f_tag = f(GOTHIC, 72)
    cx(draw, "崖っぷちからでも間に合う！", y, f_tag, (255, 255, 255),
       stroke=2, sc=(150, 30, 0))
    y += text_h(f_tag) + 30

    # 大きな箇条書きポイント
    bullets = [
        "✓ 持ち家・車があっても生活保護申請OK",
        "✓ 年金受給者でも生活保護は受けられる",
        "✓ AIで60代から収入を再建する方法",
    ]
    f_bul = f(GOTHIC, 58)
    for b in bullets:
        bw = draw.textlength(b, font=f_bul)
        draw.text(((W - bw) / 2, y), b, font=f_bul, fill=(255, 255, 230),
                  stroke_width=1, stroke_fill=(120, 30, 0))
        y += text_h(f_bul) + 18

    # ── 下部帯 ──────────────────────────────────────────────
    draw.rectangle([(0, H - 160), (W, H)], fill=(20, 8, 0))
    f_isbn = f(GOTHIC, 48)
    cx(draw, "ISBN 978-X-XXXX-XXXX-X", H - 110, f_isbn, (130, 110, 80))

    img.save("cover_paperback_temp.jpg", "JPEG", quality=95)
    print("cover_paperback_temp.jpg saved")


make_kindle()
make_paperback()
