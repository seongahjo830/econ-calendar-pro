"""
경제캘린더 Pro — 앱 아이콘 생성기
기존 무료 아이콘 디자인(네이비 + 캘린더 카드 + 등급 도트) 유지
+ 골드 "PRO" 배지 추가 (무료앱과 차별화)
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(__file__)
GOLD = (212, 160, 23, 255)   # #D4A017 — Pro 골드
NAVY = (29, 78, 216, 255)    # #1D4ED8 — 브랜드 네이비

def load_font(px):
    for path in [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\Arial.ttf"]:
        try:
            return ImageFont.truetype(path, px)
        except Exception:
            pass
    return ImageFont.load_default()

def make(size, maskable=False):
    pad = int(size * 0.18) if maskable else int(size * 0.06)
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    radius = int(size * (0.22 if not maskable else 0))
    bd.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=NAVY)
    for i in range(size//3):
        alpha = int(60 * (1 - i/(size/3)))
        bd.line([(0, i), (size, i)], fill=(255, 255, 255, alpha))
    img = bg
    d = ImageDraw.Draw(img)

    # 흰 캘린더 카드
    card_x0 = pad
    card_y0 = pad + int(size * 0.10)
    card_x1 = size - pad
    card_y1 = size - pad
    card_r = int((card_x1 - card_x0) * 0.10)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1], radius=card_r, fill=(251, 250, 247, 255))

    # 상단 헤더 바
    head_h = int((card_y1 - card_y0) * 0.18)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y0 + head_h], radius=card_r, fill=NAVY)
    d.rectangle([card_x0, card_y0 + head_h - card_r, card_x1, card_y0 + head_h], fill=NAVY)

    # 캘린더 그리드 도트 (Pro는 3행만 — 하단은 PRO 배지 자리)
    grid_x0 = card_x0 + int((card_x1 - card_x0) * 0.10)
    grid_x1 = card_x1 - int((card_x1 - card_x0) * 0.10)
    grid_y0 = card_y0 + head_h + int((card_y1 - card_y0) * 0.10)
    grid_y1 = card_y1 - int((card_y1 - card_y0) * 0.30)
    cols, rows = 7, 3
    cw = (grid_x1 - grid_x0) / cols
    rh = (grid_y1 - grid_y0) / rows
    dot_r = min(cw, rh) * 0.18
    grade_pos = {
        (0, 1): (200, 200, 200), (0, 4): (220, 38, 38),
        (1, 2): (236, 72, 153),  (1, 6): (220, 38, 38),
        (2, 3): (220, 38, 38),   (2, 5): (234, 179, 8),
    }
    for r in range(rows):
        for c in range(cols):
            cx = grid_x0 + cw * (c + 0.5)
            cy = grid_y0 + rh * (r + 0.5)
            color = grade_pos.get((r, c), (220, 215, 200))
            d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color)

    # ⭐ 골드 PRO 배지 (카드 하단 중앙 — maskable safe zone 안)
    pill_w = (card_x1 - card_x0) * 0.56
    pill_h = (card_y1 - card_y0) * 0.19
    cx = (card_x0 + card_x1) / 2
    pill_y1 = card_y1 - (card_y1 - card_y0) * 0.07
    pill_y0 = pill_y1 - pill_h
    d.rounded_rectangle([cx - pill_w/2, pill_y0, cx + pill_w/2, pill_y1],
                        radius=pill_h/2, fill=GOLD)
    font = load_font(int(pill_h * 0.62))
    txt = "PRO"
    tb = d.textbbox((0, 0), txt, font=font)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    d.text((cx - tw/2 - tb[0], (pill_y0+pill_y1)/2 - th/2 - tb[1]), txt, font=font, fill=NAVY)

    return img

for sz in [192, 512]:
    make(sz).save(os.path.join(OUT, f'icon-{sz}.png'), 'PNG'); print(f'OK icon-{sz}.png')
make(512, maskable=True).save(os.path.join(OUT, 'icon-maskable-512.png'), 'PNG'); print('OK maskable')
make(1024).save(os.path.join(OUT, 'icon-1024.png'), 'PNG'); print('OK icon-1024.png')
print('done', OUT)
