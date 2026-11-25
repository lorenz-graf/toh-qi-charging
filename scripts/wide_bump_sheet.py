# Overview image of the wide camera bump (make_wide_bump.py) on the Qi cover, from wide_bump_render.py's images.
# Usage (from this project's folder): python3 scripts/wide_bump_sheet.py <render_dir> renders/wide-bump.png
import sys, math
from PIL import Image, ImageDraw, ImageFont
rd, res = sys.argv[1:3]
F = "/usr/share/fonts/TTF/DejaVuSans.ttf"; FB = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
f20, b22, b26, b34 = ImageFont.truetype(F, 20), ImageFont.truetype(FB, 22), ImageFont.truetype(FB, 26), ImageFont.truetype(FB, 34)
RED, BLUE, INK, ORG = (210, 30, 80), (30, 90, 200), (25, 25, 30), (200, 100, 20)
top = Image.open(rd + "/outside.png").convert("RGB"); side = Image.open(rd + "/side.png").convert("RGB")
OX, OY = 40, 130; SY = OY + top.height + 60
W = OX + max(top.width + 760, side.width) + 40; H = SY + side.height + 60
cv = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(cv)
cv.paste(top, (OX, OY)); cv.paste(side, (OX, SY))
X = lambda u: OX + 420 + (37.0 - u) * 10                 # outside view, 10 px/mm
Y = lambda v: OY + 830 - (-78.8 + v + 0.3) * 10
SX = lambda u: OX + 840 + (37.0 - u) * 20                # side view, 20 px/mm
SZ = lambda z: SY + 150 - (z - 3.5) * 20                 # z = mm outwards from the plate's inner surface side (outside face 3.0)
d.text((40, 20), "Wide camera bump (model/wide-bump/wide-bump.stl) on the Qi cover", fill=INK, font=b34)
d.text((40, 70), "OUTSIDE (back of the phone); the cover's camera cutout is widened to match", fill=BLUE, font=b22)

def dim(p, q, txt, col, side=-1):
    d.line([p, q], fill=col, width=2)
    for a, b in ((p, q), (q, p)):
        g = math.atan2(a[1] - b[1], a[0] - b[0])
        d.polygon([a, (a[0] - 11 * math.cos(g - 0.4), a[1] - 11 * math.sin(g - 0.4)),
                   (a[0] - 11 * math.cos(g + 0.4), a[1] - 11 * math.sin(g + 0.4))], fill=col)
    d.text(((p[0] + q[0]) / 2 + (0 if p[1] == q[1] else side * 8), (p[1] + q[1]) / 2 + (side * 6 if p[1] == q[1] else 0)),
           txt, fill=col, font=b22, anchor=("mb" if side < 0 else "mt") if p[1] == q[1] else ("rm" if side < 0 else "lm"))

yv = Y(124)
dim((X(74), yv), (X(68.3), yv), "5.7", RED, side=1)
dim((X(5.7), yv), (X(0), yv), "5.7", RED, side=1)
dim((X(68.3), Y(158.5)), (X(5.7), Y(158.5)), "62.6", ORG)
dim((X(20), Y(151.35)), (X(20), Y(116.25)), "35.1", INK, side=-1)
for u in (0, 74): d.line([(X(u), yv - 14), (X(u), yv + 14)], fill=RED, width=2)
d.text((X(44.6) + 30, Y(134.0) + 40), "flash", fill=INK, font=b22)
dim((SX(5.7) + 30, SZ(3.0)), (SX(5.7) + 30, SZ(6.2)), "3.2", ORG, side=1)
d.text((OX, SY - 40), "Side view from the phone's bottom edge: the bump stands 3.2 mm on the flat outside face", fill=BLUE, font=b22)

tx = OX + top.width + 40; ty = OY + 10
def para(title, col, lines):
    global ty
    d.text((tx, ty), title, fill=col, font=b26); ty += 36
    for l in lines:
        d.text((tx, ty), l, fill=INK, font=f20); ty += 27
    ty += 18
para("Why", INK, ["the stock bump is off-centre, so the phone", "rocks on it when the screen is pressed;",
     "now it lies on a 62.6 mm wide bar", "with the same 5.7 mm to both long edges"])
para("Shape", ORG, ["copy of the stock bump, made wider:", "same 3.2 mm height, camera windows,", "cavity and tapered edge; one part",
     "cone over the flash (Ø 6 → 10.1)", "~8 g"])
para("Fitting (same as the stock bump)", RED, ["put it into the cover's cutout from the", "inside, then put the cover on the phone;",
     "its tapered edge can't pass the cutout,", "the phone keeps it from falling in; no glue"])
para("Print", BLUE, ["roof down on the bed (STL is in that pose),", "no supports"])
cv.save(res)
