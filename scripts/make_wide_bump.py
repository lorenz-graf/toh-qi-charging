# Wide camera bump for the Qi cover (make_qi_cover_wide_bump.py cuts the matching wide cutout).
# Why (user, 2026-11-25): the stock bump sits off-centre (u 49.9-68.3), so a phone lying on its back rocks when
# the screen is pressed. This is a copy of the stock bump made wider: u 5.7-68.3, the same 5.7 mm from both long
# edges. Same height (3.2 mm above the outside face), same camera windows and cavity, same tapered flange: it goes
# into the cover's cutout from the inside, then the cover goes on the phone, like the stock bump. Shape:
# wide_bump_shape.py. Flash: a cone through the bump over the phone's flash (centre u 44.6, v 134.0).
# Outputs: model/wide-bump/step/wide-bump.step (assembled position, phone coords) and model/wide-bump/wide-bump.stl (print pose: roof on the
#          bed, like ../toh-devkit/model/ctohm-bump-roof-down.stl; no supports)
# Run from this folder: freecadcmd -c "exec(open('make_wide_bump.py').read())"
import os, math, Part, MeshPart, Mesh, FreeCAD as App
exec(open("wide_bump_shape.py").read())

REPO = os.path.dirname(os.getcwd())
assert os.path.exists(os.path.join(REPO, "STATUS.md")), "run from scripts/"
TOH_DESIGNS = os.environ.get("TOH_DESIGNS", os.path.join(REPO, "..", "3d", "og jolla stuff"))
def src(name):
    for sub in ("", "cTOH-M", "jolla"):
        p = os.path.join(TOH_DESIGNS, sub, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name + " (set TOH_DESIGNS to a clone of github.com/sailfishos/toh-designs)")
OUT = os.path.join(REPO, "model", "wide-bump"); os.makedirs(os.path.join(OUT, "step"), exist_ok=True)   # STLs; STEPs in step/
FLASH_U, FLASH_V, FLASH_R, CONE = 44.6, 134.0, 3.0, math.radians(25)
M = App.Matrix(-1, 0, 0, -0.23,  0, 0, -1, -78.65,  0, -1, 0, 0,  0, 0, 0, 1)   # cTOH-M -> phone frame

s = Part.read(src("2-Bump-Final2_with_integrated_supports.step"))
stock = max(s.Solids, key=lambda x: x.Volume).transformGeometry(M)   # drop the built-in print supports

# wide outer body: roof part + flange
body = prism(0, ROOF, FACE)
try:
    body = body.makeFillet(0.3, [e for e in body.Edges if abs(e.BoundBox.ZMax - ROOF) < 1e-6 and abs(e.BoundBox.ZMin - ROOF) < 1e-6])
except Exception as ex:
    print("roof edge fillet skipped:", ex)
body = body.fuse(loft(FACE, BUMP_IN)).removeSplitter()
# make room for the stock bump's inside (cavity + windows): cut its widest cavity outline per zone, then add the
# stock bump back, which brings its own walls, roof and windows
def inner_at(z, z0, z1):
    w = min(stock.slice(App.Vector(0, 0, 1), z), key=lambda w: w.BoundBox.DiagonalLength)
    w.translate(App.Vector(0, 0, z0 - z))
    return Part.Face(w).extrude(App.Vector(0, 0, z1 - z0))
body = body.cut(inner_at(-3.05, ROOF - 1, FACE)).cut(inner_at(-1.85, FACE, BUMP_IN + 1))
w = body.fuse(stock).removeSplitter()
r_top = FLASH_R + (BUMP_IN - ROOF) * math.tan(CONE)
w = w.cut(Part.makeCone(FLASH_R, r_top, BUMP_IN - ROOF + 0.2, P(FLASH_U, FLASH_V, BUMP_IN + 0.1), App.Vector(0, 0, -1)))
assert w.isValid() and len(w.Solids) == 1, (w.isValid(), len(w.Solids))
b = w.BoundBox
print("wide bump u %.2f-%.2f v %.2f-%.2f Z %.2f..%.2f, volume %.0f mm3 (~%.1f g ASA)" %
      (b.XMin + 37, b.XMax + 37, b.YMin + 78.8, b.YMax + 78.8, b.ZMin, b.ZMax, w.Volume, w.Volume * 1.07e-3))
print("flash cone Ø %.1f inside, Ø %.1f at the roof" % (2 * FLASH_R, 2 * r_top))
w.exportStep(os.path.join(OUT, "step", "wide-bump.step"))

# print pose: roof down (the roof is already the lowest Z in phone coords), roof at Z 0
p = w.copy(); p.translate(App.Vector(0, 0, -p.BoundBox.ZMin))
stl = os.path.join(OUT, "wide-bump.stl")
MeshPart.meshFromShape(Shape=p, LinearDeflection=0.02, AngularDeflection=0.15).write(stl)
m = Mesh.Mesh(stl); print("mesh solid", m.isSolid(), "nonmanifold", m.hasNonManifolds(), "components", m.countComponents())

f = os.path.join(OUT, "step", "qi-cover-wide-bump.step")
if os.path.exists(f): print("overlap with the cover: %.3f mm3" % w.common(Part.read(f)).Volume)
