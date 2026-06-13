from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1600, 2560

def get_font(size, bold=False):
    paths = [
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJKjp-Bold.otf",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
        "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf",
        "/usr/share/fonts/truetype/takao-gothic/TakaoPGothic.ttf",
        "/usr/share/fonts/truetype/vlgothic/VL-Gothic-Regular.ttf",
    ]
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def draw_text_centered(draw, text, y, font, color, max_width=None, img_w=W):
    if max_width and draw.textlength(text, font=font) > max_width:
        # word wrap by character
        lines = []
        line = ""
        for ch in text:
            test = line + ch
            if draw.textlength(test, font=font) > max_width:
                lines.append(line)
                line = ch
            else:
                line = test
        if line:
            lines.append(line)
    else:
        lines = [text]

    bbox = font.getbbox("A")
    line_h = bbox[3] - bbox[1]
    spacing = int(line_h * 0.3)
    total_h = len(lines) * line_h + (len(lines) - 1) * spacing
    cur_y = y - total_h // 2

    for ln in lines:
        tw = draw.textlength(ln, font=font)
        x = (img_w - tw) / 2
        draw.text((x, cur_y), ln, font=font, fill=color)
        cur_y += line_h + spacing

    return cur_y


def make_gradient(w, h, top_color, bottom_color):
    img = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))
    return img


# ── Cover 1: Kindle (electric orange → deep red gradient) ──────────────────
def make_kindle_cover():
    img = make_gradient(W, H, (230, 80, 10), (150, 20, 10))
    draw = ImageDraw.Draw(img)

    # accent bar top
    draw.rectangle([(0, 0), (W, 18)], fill=(255, 200, 50))

    # top label band
    draw.rectangle([(0, 60), (W, 160)], fill=(0, 0, 0, 180))
    label_font = get_font(52)
    lw = draw.textlength("生活再建ガイド決定版", font=label_font)
    draw.text(((W - lw) / 2, 78), "生活再建ガイド決定版", font=label_font, fill=(255, 220, 60))

    # main title
    title_font = get_font(148)
    draw_text_centered(draw, "老後破綻", 620, title_font, (255, 255, 255), max_width=W - 80)
    draw_text_centered(draw, "からの", 820, get_font(100), (255, 235, 180), max_width=W - 80)
    draw_text_centered(draw, "リスタート", 1000, title_font, (255, 255, 255), max_width=W - 80)

    # divider line
    draw.rectangle([(80, 1130), (W - 80, 1142)], fill=(255, 210, 50))

    # subtitle
    sub_font = get_font(62)
    draw_text_centered(draw, "年金・生活保護・AIで", 1260, sub_font, (255, 240, 200), max_width=W - 120)
    draw_text_centered(draw, "「死なない暮らし」をつくる", 1360, sub_font, (255, 240, 200), max_width=W - 120)

    # bottom accent band
    draw.rectangle([(0, H - 260), (W, H - 258)], fill=(255, 210, 50))
    draw.rectangle([(0, H - 258), (W, H)], fill=(20, 10, 5))

    # author
    auth_font = get_font(72)
    aw = draw.textlength("中川昌風", font=auth_font)
    draw.text(((W - aw) / 2, H - 200), "中川昌風", font=auth_font, fill=(255, 220, 60))

    img.save("cover_kindle.jpg", "JPEG", quality=95)
    print("cover_kindle.jpg saved")


# ── Cover 2: Paperback (warm yellow → orange, bolder layout) ───────────────
def make_paperback_cover():
    img = make_gradient(W, H, (255, 200, 30), (220, 80, 0))
    draw = ImageDraw.Draw(img)

    # dark overlay strip at top
    draw.rectangle([(0, 0), (W, 220)], fill=(30, 10, 0))

    top_font = get_font(54)
    tw = draw.textlength("中川昌風 著", font=top_font)
    draw.text(((W - tw) / 2, 80), "中川昌風 著", font=top_font, fill=(255, 220, 60))

    # large title block — white on dark band
    draw.rectangle([(0, 300), (W, 1100)], fill=(20, 10, 5))

    t1 = get_font(160)
    draw_text_centered(draw, "老後破綻", 530, t1, (255, 255, 255), max_width=W - 60)
    draw_text_centered(draw, "からの", 730, get_font(110), (255, 210, 50), max_width=W - 60)
    draw_text_centered(draw, "リスタート", 940, t1, (255, 255, 255), max_width=W - 60)

    # yellow accent
    draw.rectangle([(0, 1100), (W, 1126)], fill=(255, 210, 50))

    # subtitle on warm background
    s_font = get_font(66)
    draw_text_centered(draw, "年金・生活保護・AIで", 1280, s_font, (30, 10, 0), max_width=W - 100)
    draw_text_centered(draw, "「死なない暮らし」をつくる", 1390, s_font, (30, 10, 0), max_width=W - 100)

    # tag line box
    draw.rectangle([(80, 1520), (W - 80, 1720)], fill=(30, 10, 0))
    tag_font = get_font(54)
    draw_text_centered(draw, "誰も教えてくれなかった制度の使い方", 1590, tag_font, (255, 220, 60), max_width=W - 200)
    draw_text_centered(draw, "崖っぷちから這い上がった著者が語る", 1670, tag_font, (255, 255, 255), max_width=W - 200)

    # bottom strip
    draw.rectangle([(0, H - 220), (W, H)], fill=(30, 10, 0))
    b_font = get_font(56)
    bw = draw.textlength("ISBN 978-X-XXXX-XXXX-X", font=b_font)
    draw.text(((W - bw) / 2, H - 160), "ISBN 978-X-XXXX-XXXX-X", font=b_font, fill=(150, 130, 100))

    img.save("cover_paperback_temp.jpg", "JPEG", quality=95)
    print("cover_paperback_temp.jpg saved")


make_kindle_cover()
make_paperback_cover()
