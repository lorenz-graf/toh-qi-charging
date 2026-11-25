# Where the 0805 ID resistor, the INT-GND bridge and the receiver wires go on the contact board's wire pads.
# View: the contact board's BACK side (wire pads), as seen from outside the cover (seen from behind the phone).
# Pad positions from ../../toh-devkit/pcb/contact/make_board.py. Run: python3 wiring_sheet.py -> ../renders/wiring.png
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyBboxPatch
from matplotlib.transforms import Affine2D

WIRE = {"5V": (32.9, 11.75), "SCL": (30.6, 11.75), "ID": (28.3, 11.75), "VIN": (26.0, 11.75),
        "SDA": (27.15, 10.25), "INT": (29.45, 10.25), "GND": (31.75, 10.25)}
POWER = {"5V", "VIN", "GND"}
X = lambda u: -u          # seen from behind: u (from the phone's right edge) grows to the left
fig, ax = plt.subplots(figsize=(11, 8), dpi=150)
ax.set_aspect("equal"); ax.axis("off"); ax.set_xlim(-36.5, -21.5); ax.set_ylim(6.5, 23.5)

# wire pocket under the board (u 25-34, v 9.5-14.5) and the groove going up (u 27-30)
ax.add_patch(FancyBboxPatch((X(34), 9.5), 9, 5, boxstyle="round,pad=0,rounding_size=0.8", fc="#fde8ec", ec="#d0234a", lw=1.5, ls="--"))
ax.add_patch(Rectangle((X(30), 14.5), 3, 5.8, fc="#fde8ec", ec="#d0234a", lw=1.5, ls="--"))
ax.text(X(30.3), 18.5, "groove up to\nthe Qi board", ha="right", va="center", fontsize=10, color="#d0234a")
ax.text(X(34) + 0.2, 14.3, "wire pocket (0.5 deep)", fontsize=9, color="#d0234a", va="top")
# contact board edge (indent upper edge)
ax.plot([X(36.4), X(21.6)], [14.3, 14.3], color="#2e7d32", lw=2)
ax.text(X(21.7), 14.45, "contact board edge", fontsize=9, color="#2e7d32", ha="right", va="bottom")

for n, (u, v) in WIRE.items():
    s = 1.2 if n in POWER else 1.0
    used = n in ("ID", "INT", "GND", "VIN")
    ax.add_patch(Rectangle((X(u) - s / 2, v - s / 2), s, s, fc="#e8b923" if used else "#ddd", ec="#8a6d00" if used else "#999"))
    ax.text(X(u), v + (0.85 if v > 11 else -0.85), n, ha="center", va="center", fontsize=11, fontweight="bold",
            color="#222" if used else "#999")

# 0805 resistor diagonally from ID to INT
(u1, v1), (u2, v2) = WIRE["ID"], WIRE["INT"]
cx, cy = (X(u1) + X(u2)) / 2, (v1 + v2) / 2
ang = math.degrees(math.atan2(v2 - v1, X(u2) - X(u1)))
r = Rectangle((cx - 1.0, cy - 0.625), 2.0, 1.25, fc="#222", ec="#000", zorder=5)
r.set_transform(Affine2D().rotate_deg_around(cx, cy, ang) + ax.transData); ax.add_patch(r)
ax.text(cx, cy, "6.2k", color="white", fontsize=8, ha="center", va="center", rotation=ang, zorder=6)
ax.annotate("0805 resistor 6.2 kΩ\nID → INT (diagonal)", xy=(cx - 0.6, cy - 0.5), xytext=(X(24.0), 7.4),
            fontsize=11, arrowprops=dict(arrowstyle="->"), ha="center")
# INT-GND bridge
(u3, v3) = WIRE["GND"]
ax.plot([X(u2) - 0.3, X(u3) + 0.4], [v2, v3], color="#9e9e9e", lw=7, solid_capstyle="round", zorder=4)
ax.annotate("solder bridge or wire offcut\nINT → GND", xy=((X(u2) + X(u3)) / 2, v2 - 0.2), xytext=(X(32.0), 7.4),
            fontsize=11, arrowprops=dict(arrowstyle="->"), ha="center")
# receiver wires: VIN (+) and GND (-) up into the groove
ax.plot([X(26.0), X(26.0), X(27.6), X(27.6)], [11.75, 13.6, 14.6, 20], color="#d32f2f", lw=3, zorder=3)
ax.plot([X(31.75), X(31.75), X(29.4), X(29.4)], [10.25, 13.6, 14.6, 20], color="#111", lw=3, zorder=3)
ax.text(X(25.6), 13.4, "Qi +", color="#d32f2f", fontsize=11, fontweight="bold", ha="left")
ax.text(X(32.2), 13.4, "Qi −", color="#111", fontsize=11, fontweight="bold", ha="right")
ax.text(-36.4, 23.3, "Contact board, wire-pad side (seen from outside the cover)", fontsize=14, fontweight="bold", va="top")
ax.text(-36.4, 22.4, "Everything sits in the wire pocket under the board: no extra indent needed", fontsize=11, va="top", color="#555")
plt.savefig("../renders/wiring.png", bbox_inches="tight", facecolor="white")
