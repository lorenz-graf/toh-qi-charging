# Qi cover: community cTOH-M frame (no-sanding version, as in the TOH DevKit's make_dev_cover.py), laid flat in
# phone coordinates, with pockets on the INSIDE for the Qi receiver coil and board, a wire groove from the board to
# the contact board, and a blind pocket under the contact board's wire pads (room for the solder joints, the 0805 ID
# resistor and the wires running up into the groove; no through slot, user 2026-11-23).
# Phone coords: u = mm from the phone's right edge, v = mm from its bottom edge (seen from behind; phone 74 x 157).
# Model frame = Jolla's toh-3d-model: X = -37 + u, Y = -78.8 + v, inside of the cover = +Z,
# outside face at Z = -3.0 (print this face on the bed). cTOH-M plate: inner surface Z = -1.6 (1.4 mm plate),
# contact-board indent floor Z = -2.2.
# Run from this folder: freecadcmd -c "exec(open('make_qi_cover.py').read())"
# Variant with the wide camera bump's cutout: make_qi_cover_wide_bump.py (sets WIDE_BUMP and runs this script).
import os, Part, MeshPart, FreeCAD as App
WIDE_BUMP = globals().get("WIDE_BUMP", False)
NAME = "qi-cover-wide-bump" if WIDE_BUMP else "qi-cover"

REPO = os.path.dirname(os.getcwd())
assert os.path.exists(os.path.join(REPO, "STATUS.md")) or os.path.exists(os.path.join(REPO, "README.md")), "run from scripts/"
TOH_DESIGNS = os.environ.get("TOH_DESIGNS", os.path.join(REPO, "..", "3d", "og jolla stuff"))
def src(name):
    for sub in ("", "cTOH-M", "jolla"):
        p = os.path.join(TOH_DESIGNS, sub, name)
        if os.path.exists(p): return p
    raise FileNotFoundError(name + " (set TOH_DESIGNS to a clone of github.com/sailfishos/toh-designs)")
OUT = os.path.join(REPO, "model", "wide-bump" if globals().get("WIDE_BUMP", False) else "default-bump")   # STLs; STEPs in step/
os.makedirs(os.path.join(OUT, "step"), exist_ok=True)

# --- receiver (measured 2026-11-23) ---
COIL_W, COIL_H, COIL_T = 30.0, 42.0, 0.4 + 0.5     # coil + the black sheet that came with it
BOARD_W, BOARD_H, BOARD_T = 25.1, 14.4, 1.0
GAP = 3.7                                          # coil lower edge -> board upper edge
CLEAR = 0.2                                        # per side
# --- placement (phone coords) ---
COIL_CU, COIL_CV = 37.05, 78.6   # coil centred on the back (= centre of cTOH-M's magnet-ring recess); user 2026-11-23
# (a try with the board 1 cm above the contact board put the coil 15 mm low; the user chose the centre instead)
CONTACT_TOP = 14.3        # upper edge of the contact board, for the printout of the gap below
# cTOH-M has a ring recess on the inside (MagSafe-style magnet ring): centre (37.05, 78.6), radius 21.85-28.65,
# 0.7 deep (Z -2.3). The coil's corners and the board reach into it, so no magnet ring in this cover.
# --- depths below the inner surface (Z = -1.6); plate is 1.4 ---
INNER = -1.6
COIL_D, BOARD_D, GROOVE_D = 0.9, 1.0, 1.0          # floors: 0.5, 0.4, 0.4
GROOVE_U = (27.0, 30.0)                            # 3 mm wide, between the VIN (u 26.0) and GND (u 31.75) wire pads
SLOT_U, SLOT_V = (25.0, 34.0), (9.5, 14.5)         # under the wire pads, up to the indent's upper edge
SLOT_Z = -2.7                                      # 0.5 below the indent floor (-2.2), floor 0.3

P = lambda u, v, z: App.Vector(-37.0 + u, -78.8 + v, z)

def box(u0, u1, v0, v1, z0, z1, r=0.0):
    f = Part.Face(Part.makePolygon([P(u0, v0, z0), P(u1, v0, z0), P(u1, v1, z0), P(u0, v1, z0), P(u0, v0, z0)]))
    t = f.extrude(App.Vector(0, 0, z1 - z0))
    if r > 0:
        t = t.makeFillet(r, [e for e in t.Edges if abs(e.tangentAt(e.FirstParameter).normalize().z) > 0.99])
    return t

s = Part.read(src("Optional_Frame-Final1-no sanding.step"))
s = s.transformGeometry(App.Matrix(-1, 0, 0, -0.23,  0, 0, -1, -78.65,  0, -1, 0, 0,  0, 0, 0, 1))

cw, ch = COIL_W + 2 * CLEAR, COIL_H + 2 * CLEAR
cu0, cv0 = COIL_CU - cw / 2, COIL_CV - ch / 2
bw, bh = BOARD_W + 2 * CLEAR, BOARD_H + 2 * CLEAR
bu0 = COIL_CU - bw / 2
bv1 = COIL_CV - COIL_H / 2 - GAP + CLEAR            # board upper edge (+ clearance)
bv0 = bv1 - bh
TOP = INNER + 1.0                                   # tools stick out above the inner surface
tools = [
    box(cu0, cu0 + cw, cv0, cv0 + ch, INNER - COIL_D, TOP, r=8.0),                   # coil
    box(bu0, bu0 + bw, bv0, bv1, INNER - BOARD_D, TOP, r=1.0),                       # board
    box(COIL_CU - 5, COIL_CU + 5, bv1 - 1, cv0 + 1, INNER - COIL_D, TOP),            # coil leads
    box(GROOVE_U[0], GROOVE_U[1], SLOT_V[1] - 1, bv0 + 1, INNER - GROOVE_D, TOP, r=0.5),  # wires to the contact board
    box(SLOT_U[0], SLOT_U[1], SLOT_V[0], SLOT_V[1], SLOT_Z, TOP, r=1.0),             # blind pocket under the wire pads
]
if WIDE_BUMP:
    exec(open("wide_bump_shape.py").read())
    tools.append(cutout())                                                           # wide camera bump
r = s
for t in tools: r = r.cut(t)
sol = r.Solids
if len(sol) > 1:
    fused = sol[0].fuse(sol[1:]).removeSplitter()
    if fused.isValid() and len(fused.Solids) == 1: r = fused
print("solids:", len(r.Solids), "volume before", round(s.Volume, 1), "after", round(r.Volume, 1))
print("gap contact board -> receiver board: %.1f" % (COIL_CV - COIL_H / 2 - GAP - BOARD_H - CONTACT_TOP))
print("coil pocket u %.2f-%.2f v %.2f-%.2f; board pocket u %.2f-%.2f v %.2f-%.2f" %
      (cu0, cu0 + cw, cv0, cv0 + ch, bu0, bu0 + bw, bv0, bv1))
r.exportStep(os.path.join(OUT, "step", NAME + ".step"))
MeshPart.meshFromShape(Shape=r, LinearDeflection=0.02, AngularDeflection=0.15).write(os.path.join(OUT, NAME + ".stl"))
if not WIDE_BUMP:   # the stock bump belongs to this version: copy it in so the folder has every part
    import shutil
    shutil.copyfile(os.path.join(REPO, "..", "toh-devkit", "model", "default-bump", "ctohm-bump-roof-down.stl"), os.path.join(OUT, "ctohm-bump-roof-down.stl"))
