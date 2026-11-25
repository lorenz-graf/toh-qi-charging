# Overview image of the Qi cover (make_qi_cover.py), inside view with labels.
# Base render (from this project's folder):
#   blender -b --python ../toh-devkit/scripts/measure_render.py -- model/default-bump/qi-cover.stl <in.png> 0 -0.3 8 84 166
# Usage: python3 qi_cover_sheet.py <in.png> ../renders/qi-cover.png [<model path for the title>]
import sys, math
from PIL import Image, ImageDraw, ImageFont
fin, res = sys.argv[1:3]
MODEL = sys.argv[3] if len(sys.argv) > 3 else "model/default-bump/qi-cover.stl"   # path shown in the title
F = "/usr/share/fonts/TTF/DejaVuSans.ttf"; FB = "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"
f20, b22, b26, b34 = ImageFont.truetype(F, 20), ImageFont.truetype(FB, 22), ImageFont.truetype(FB, 26), ImageFont.truetype(FB, 34)
RED, BLUE, INK, GREY, COP, GRN, PUR = (210, 30, 80), (30, 90, 200), (25, 25, 30), (110, 110, 120), (190, 110, 40), (20, 130, 60), (130, 60, 170)
im = Image.open(fin).convert("RGB")
OX, OY = 40, 130
W = OX + im.width + 900; H = OY + im.height + 40
cv = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(cv)
cv.paste(im, (OX, OY))
X = lambda u: OX + im.width / 2 + (u - 37.0) * 8            # inside view: connector side on the left
Y = lambda v: OY + im.height / 2 - (-78.8 + v + 0.3) * 8
d.text((40, 20), "Qi cover: " + MODEL, fill=INK, font=b34)
d.text((40, 70), "INSIDE (the side facing the phone), seen looking into the cover; print the outside face down", fill=BLUE, font=b22)

def dim(p, q, txt, col, side=-1):
    d.line([p, q], fill=col, width=2)
    for a, b in ((p, q), (q, p)):
        g = math.atan2(a[1] - b[1], a[0] - b[0])
        d.polygon([a, (a[0] - 11 * math.cos(g - 0.4), a[1] - 11 * math.sin(g - 0.4)),
                   (a[0] - 11 * math.cos(g + 0.4), a[1] - 11 * math.sin(g + 0.4))], fill=col)
    d.text(((p[0] + q[0]) / 2 + (0 if p[1] == q[1] else side * 8), (p[1] + q[1]) / 2 + (side * 6 if p[1] == q[1] else 0)),
           txt, fill=col, font=b22, anchor=("mb" if side < 0 else "mt") if p[1] == q[1] else ("rm" if side < 0 else "lm"))

# coil pocket 30.4 x 42.4, board pocket 25.5 x 14.8 (incl. 0.2 clearance per side)
d.rounded_rectangle([X(21.85), Y(99.8), X(52.25), Y(57.4)], radius=64, outline=COP, width=4)
d.rectangle([X(24.3), Y(54.1), X(49.8), Y(39.3)], outline=GRN, width=4)
d.rectangle([X(27.0), Y(39.3), X(30.0), Y(12.5)], outline=RED, width=3)
d.rectangle([X(25.0), Y(14.5), X(34.0), Y(9.5)], outline=RED, width=3)
for r in (21.85, 28.65):
    d.ellipse([X(37.05 - r), Y(78.6 + r), X(37.05 + r), Y(78.6 - r)], outline=PUR, width=2)
dim((X(21.85), Y(101.5)), (X(52.25), Y(101.5)), "30.4", COP)
dim((X(53.8), Y(99.8)), (X(53.8), Y(57.4)), "42.4", COP, side=1)
dim((X(24.3), Y(37.6)), (X(49.8), Y(37.6)), "25.5", GRN, side=1)
# contact board's upper edge (14.3) to the receiver board's lower edge (39.5)
d.line([(X(36.4), Y(14.3)), (X(46), Y(14.3))], fill=BLUE, width=1); d.line([(X(49.8), Y(39.5)), (X(46), Y(39.5))], fill=BLUE, width=1)
dim((X(44), Y(39.5)), (X(44), Y(14.3)), "25.2", BLUE, side=1)

tx = OX + im.width + 30; ty = OY + 10
def para(title, col, lines):
    global ty
    d.text((tx, ty), title, fill=col, font=b26); ty += 36
    for l in lines:
        d.text((tx, ty), l, fill=INK, font=f20); ty += 27
    ty += 18
para("Coil pocket (copper)", COP, ["30.4 × 42.4, 0.9 deep → floor 0.5 mm", "coil 0.4 + black sheet 0.5 = 0.9",
     "copper side down (towards the pad),", "black sheet up (towards the phone)", "centred on the back (on the ring)"])
para("Board pocket (green)", GRN, ["25.5 × 14.8, 1.0 deep → floor 0.4 mm", "25.2 above the contact board (blue),", "3.7 below the coil, joined by a",
     "10 mm channel for the coil leads"])
para("Wire groove + wire space (red)", RED, ["groove 3 wide, 1.0 deep: two wires from", "the board down to the contact board",
     "under the contact board: 9 × 5 pocket,", "0.5 below the indent floor (floor 0.3),", "not through: room for the solder joints,", "the 0805 resistor and the wires going up"])
para("Magnet-ring recess (purple)", PUR, ["already in cTOH-M: Ø 43.7 – 57.3, 0.7 deep", "(for a MagSafe-style magnet ring).",
     "Coil corners and the board reach into it:", "no magnet ring in this cover"])
para("Thickness", INK, ["plate stays 1.4 mm (same as the DevKit", "cover); nothing sticks out"])
cv.save(res)
