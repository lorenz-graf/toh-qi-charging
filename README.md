# TOH Qi

Wireless charging for the Jolla Phone 2026: a Qi receiver in a TOH ("The Other Half") back cover feeds the TOH's power input pin, so the phone charges on any Qi pad.

> [!WARNING]
> **Working prototype.** Charging works with the receiver wired to the [TOH DevKit](https://github.com/lorenz-graf/toh-devkit)'s contact board: the phone shows "Charging…" on my Qi pad, with no extra software. The 3D-printed covers here are **not printed or tested yet**, and neither is cover detection with the ID resistor. Use at your own risk.

## What it does

Put the phone on a Qi pad and it charges, no cable. With a 5 V / 1 A receiver I expect about 5 W: enough to keep the battery topped up while it lies on a desk.

## Hardware

- **Qi receiver:** a generic 5 V / 1 A module (mine: a 30 × 42 × 0.4 mm coil, a 0.5 mm black sheet that goes between coil and phone, and a 25 × 14.4 × 1 mm board). The coil only works copper side towards the pad (upside down I measured ~1 V)
- **Wiring** ([renders/wiring.png](renders/wiring.png)): receiver **+** → contact board **VIN** (pin 1), **−** → **GND**. **VIN must never touch the cover's 5V (pin 7)**: that is the phone's power output
- **Pin 1** takes 5–9 V; the docs say the phone limits charging from it to 1 A and turns it off while USB power is connected. A 9 V receiver should charge about twice as fast, as long as its output never overshoots 9 V
- **Detection (planned, not tested):** a 6.2 kΩ 1 % 0805 resistor from ID to INT and INT bridged to GND, all on the contact board's wire pads. 6.2 kΩ is the TOH spec's development ID (vendor/product 0000/0000)

## Case (`model/`, not printed yet)

The community **cTOH-M** frame with pockets on the inside: the coil (+ black sheet) centred on the back, the receiver board below it, a wire groove down to the contact board and a pocket under its wire pads for the solder joints and the resistor. The plate stays 1.4 mm, so nothing should stick out. Two versions, each folder has every part (STEP files in `step/`):

- **`model/default-bump/`:** `qi-cover.stl` + the stock camera bump `ctohm-bump-roof-down.stl` ([overview](renders/qi-cover.png))
- **`model/wide-bump/`:** `qi-cover-wide-bump.stl` + `wide-bump.stl`, a wider camera bump with the same distance to both long edges. The stock bump is off-centre, so a phone lying on its back rocks when you press the screen; the wide one should stop that ([cover](renders/qi-cover-wide-bump.png), [bump](renders/wide-bump.png), [how it goes in](renders/wide-bump-exploded.png)). The bump goes into the cover's cutout from the inside, like the stock one

**Printing:** covers outside face down; bumps roof down, no supports. ASA as recommended for cTOH-M. The floors under the coil (0.5 mm) and the board (0.4 mm) are thin, so I'd use a fine layer height (~0.1 mm).

## How it works

- Power on pin 1 shows up on the same charger as USB (`/sys/class/power_supply/primary_chg`); according to the usb-moded source it reports `usb_type` `DCP` (like a wall charger), so the phone treats it as a charger. I haven't read these values while charging yet
- usb-moded reads `usb_type` since 0.86.0+mer70 ([sailfishos/usb-moded#28](https://github.com/sailfishos/usb-moded/pull/28))

## Files

- `model/`: see Case
- `scripts/`: FreeCAD and Blender scripts for the models and images (`make_qi_cover.py`, `make_qi_cover_wide_bump.py`, `make_wide_bump.py`; run from `scripts/`). The cTOH-M source files come from Jolla's [toh-designs](https://github.com/sailfishos/toh-designs) (set `TOH_DESIGNS` to a clone)
- `renders/`: overview images, receiver measurements, wiring

## Licences

- This repo: BSD-3-Clause ([LICENSE](LICENSE))
- `model/` files are derived from Jolla's [toh-designs](https://github.com/sailfishos/toh-designs) (the cTOH-M community frame and camera bump), © 2026 Jolla Mobile Ltd, also BSD-3-Clause. Not affiliated with or endorsed by Jolla

Made with the help of Claude.
