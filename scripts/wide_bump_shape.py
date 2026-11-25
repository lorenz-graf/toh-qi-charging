# Shared shape of the wide camera bump, used by make_wide_bump.py (the bump) and make_qi_cover.py (its cutout).
# The stock cTOH-M bump, made wider towards the phone's other long edge; same profile as the stock one:
# roof at Z -6.2, straight walls down to the frame's outside face (Z -3.0), then a flange inside the plate that
# grows outwards towards the phone (stock: ~0.92 mm per mm) and is caught by the cover's tapered cutout.
# The bump is put into the cutout from the inside, then the cover goes on the phone (like the stock bump).
# Phone coords: u = mm from the phone's right edge, v = mm from its bottom edge (seen from behind).
import Part, FreeCAD as App

PHONE_W = 74.0
U_MAX = 68.3                      # stock bump's far edge at the roof
U_MIN = PHONE_W - U_MAX           # 5.7: same distance from the other long edge
V0, V1 = 116.25, 151.35           # stock bump's extent along the phone
R = 3.0                           # corner radius at the roof outline
ROOF, FACE, BUMP_IN, INNER = -6.2, -3.0, -1.8, -1.6   # roof, outside face, bump's inner end, plate's inner surface
FL0, SLOPE = 1.15, 0.92           # flange: offset from the roof outline at the outside face, growth per mm inwards
CLEAR = 0.1                       # cutout clearance per side

P = lambda u, v, z: App.Vector(-37.0 + u, -78.8 + v, z)

def outline(off, z):
    """Roof outline grown by off (rounded rectangle), as a wire at height z (same topology for any off)."""
    u0, u1, v0, v1, r = U_MIN - off, U_MAX + off, V0 - off, V1 + off, R + off
    e = [Part.LineSegment(P(u0 + r, v0, z), P(u1 - r, v0, z)),
         Part.ArcOfCircle(Part.Circle(P(u1 - r, v0 + r, z), App.Vector(0, 0, 1), r), -1.5708, 0),
         Part.LineSegment(P(u1, v0 + r, z), P(u1, v1 - r, z)),
         Part.ArcOfCircle(Part.Circle(P(u1 - r, v1 - r, z), App.Vector(0, 0, 1), r), 0, 1.5708),
         Part.LineSegment(P(u1 - r, v1, z), P(u0 + r, v1, z)),
         Part.ArcOfCircle(Part.Circle(P(u0 + r, v1 - r, z), App.Vector(0, 0, 1), r), 1.5708, 3.14159),
         Part.LineSegment(P(u0, v1 - r, z), P(u0, v0 + r, z)),
         Part.ArcOfCircle(Part.Circle(P(u0 + r, v0 + r, z), App.Vector(0, 0, 1), r), 3.14159, 4.71239)]
    return Part.Wire(Part.Shape(e).Edges)

def flange_off(z):
    return FL0 + (z - FACE) * SLOPE                  # z grows towards the inside

def prism(off, z0, z1):
    return Part.Face(outline(off, z0)).extrude(App.Vector(0, 0, z1 - z0))

def loft(z0, z1, extra=0.0):
    return Part.makeLoft([outline(flange_off(z0) + extra, z0), outline(flange_off(z1) + extra, z1)], True, True)

def cutout():
    """Tool for the cover: the bump's footprint through the plate, tapered like the stock cutout, + clearance."""
    below = prism(FL0 + CLEAR, FACE - 1.0, FACE)
    taper = loft(FACE, INNER, CLEAR)
    above = prism(flange_off(INNER) + CLEAR, INNER, INNER + 0.1)
    return below.fuse([taper, above]).removeSplitter()
