"""
경제캘린더 Pro — Play Store 기능 그래픽 (1024 x 500)
네이비 배경 + 골드 PRO 강조 + 아이콘 배치
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.dirname(__file__)
W, H = 1024, 500
NAVY = (29, 78, 216)
NAVY_DK = (17, 46, 130)
GOLD = (212, 160, 23)
WHITE = (251, 250, 247)

def font(px, bold=True):
    for p in ([r"C:\Windows\Fonts\malgunbd.ttf"] if bold else []) + [r"C:\Windows\Fonts\malgun.ttf"]:
        try:
            return ImageFont.truetype(p, px)
        except Exception:
            pass
    return ImageFont.load_default()

img = Image.new('RGB', (W, H), NAVY)
d = ImageDraw.Draw(img)
# 세로 그라데이션 (위 밝→아래 진)
for y in range(H):
    t = y / H
    r = int(NAVY[0]*(1-t) + NAVY_DK[0]*t)
    g = int(NAVY[1]*(1-t) + NAVY_DK[1]*t)
    b = int(NAVY[2]*(1-t) + NAVY_DK[2]*t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# 오른쪽 아이콘 배치
try:
    ic = Image.open(os.path.join(OUT, 'icon-512.png')).convert('RGBA').resize((320, 320))
    img.paste(ic, (W - 320 - 70, (H - 320)//2), ic)
except Exception as e:
    print('icon paste skip:', e)

# 왼쪽 텍스트
x = 70
# 골드 작은 라벨
lbl = "PREMIUM"
lf = font(26, bold=True)
lb = d.textbbox((0,0), lbl, font=lf)
d.rounded_rectangle([x, 120, x + (lb[2]-lb[0]) + 36, 120 + (lb[3]-lb[1]) + 22], radius=18, fill=GOLD)
d.text((x+18, 120+8), lbl, font=lf, fill=NAVY_DK)

# 타이틀: 경제캘린더 (흰) + Pro (골드)
tf = font(78, bold=True)
ty = 178
t1 = "경제캘린더 "
d.text((x, ty), t1, font=tf, fill=WHITE)
w1 = d.textbbox((0,0), t1, font=tf)[2]
d.text((x + w1, ty), "Pro", font=tf, fill=GOLD)

# 서브타이틀
sf = font(36, bold=False)
d.text((x, ty + 110), "FOMC · CPI · 2027 미리보기", font=sf, fill=WHITE)
sf2 = font(30, bold=False)
d.text((x, ty + 162), "광고 없는 프리미엄 매크로 캘린더", font=sf2, fill=(200, 215, 255))

img.save(os.path.join(OUT, 'feature-graphic-pro-1024x500.png'), 'PNG')
print('OK feature-graphic-pro-1024x500.png')
