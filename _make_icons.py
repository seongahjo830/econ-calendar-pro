"""
경제캘린더 — 앱 아이콘 생성기
파란 그라데이션 배경 + 흰색 캘린더 그리드 + 컬러 도트
"""
from PIL import Image, ImageDraw, ImageFilter
import os

OUT = os.path.dirname(__file__)

def make(size, maskable=False):
    # Maskable은 safe zone 안에 그려야 함 (외곽 ~20%는 잘릴 수 있음)
    pad = int(size * 0.18) if maskable else int(size * 0.06)
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # 1) 배경 — 둥근 사각형 그라데이션 (단색으로 단순화)
    bg = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    radius = int(size * (0.22 if not maskable else 0))
    bd.rounded_rectangle([0, 0, size-1, size-1], radius=radius, fill=(29, 78, 216, 255))
    # 위쪽 약간 밝게 — 가짜 그라데이션
    for i in range(size//3):
        alpha = int(60 * (1 - i/(size/3)))
        bd.line([(0, i), (size, i)], fill=(255, 255, 255, alpha))
    img = bg

    d = ImageDraw.Draw(img)

    # 2) 흰 캘린더 카드 (중앙)
    card_x0 = pad
    card_y0 = pad + int(size * 0.10)
    card_x1 = size - pad
    card_y1 = size - pad
    card_r = int((card_x1 - card_x0) * 0.10)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y1],
                        radius=card_r, fill=(251, 250, 247, 255))

    # 3) 상단 헤더 바 (파란 띠)
    head_h = int((card_y1 - card_y0) * 0.18)
    d.rounded_rectangle([card_x0, card_y0, card_x1, card_y0 + head_h],
                        radius=card_r, fill=(29, 78, 216, 255))
    # 헤더 아래쪽 모서리는 직각으로
    d.rectangle([card_x0, card_y0 + head_h - card_r, card_x1, card_y0 + head_h],
                fill=(29, 78, 216, 255))

    # 4) 캘린더 그리드 — 7열 4행 도트
    grid_x0 = card_x0 + int((card_x1 - card_x0) * 0.10)
    grid_x1 = card_x1 - int((card_x1 - card_x0) * 0.10)
    grid_y0 = card_y0 + head_h + int((card_y1 - card_y0) * 0.10)
    grid_y1 = card_y1 - int((card_y1 - card_y0) * 0.10)
    cols, rows = 7, 4
    cw = (grid_x1 - grid_x0) / cols
    rh = (grid_y1 - grid_y0) / rows
    dot_r = min(cw, rh) * 0.18

    # 등급 색깔별 점 배치 (시각적 강조)
    grade_pos = {
        # (row, col): color
        (0, 0): (200, 200, 200),
        (0, 1): (200, 200, 200),
        (0, 4): (220, 38, 38),    # S
        (1, 2): (236, 72, 153),   # A
        (1, 6): (220, 38, 38),    # S
        (2, 1): (249, 115, 22),   # B
        (2, 3): (220, 38, 38),    # S
        (2, 5): (234, 179, 8),    # C
        (3, 0): (200, 200, 200),
        (3, 4): (236, 72, 153),   # A
    }
    for r in range(rows):
        for c in range(cols):
            cx = grid_x0 + cw * (c + 0.5)
            cy = grid_y0 + rh * (r + 0.5)
            color = grade_pos.get((r, c), (220, 215, 200))
            d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=color)

    return img


for sz in [192, 512]:
    img = make(sz, maskable=False)
    img.save(os.path.join(OUT, f'icon-{sz}.png'), 'PNG')
    print(f'✅ icon-{sz}.png')

mask = make(512, maskable=True)
mask.save(os.path.join(OUT, 'icon-maskable-512.png'), 'PNG')
print('✅ icon-maskable-512.png')

# 1024 — Play Store 등록용
big = make(1024, maskable=False)
big.save(os.path.join(OUT, 'icon-1024.png'), 'PNG')
print('✅ icon-1024.png (Play Store 등록용)')

print('\n생성 완료. 폴더:', OUT)
