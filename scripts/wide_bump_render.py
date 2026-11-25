# Blender: the Qi cover (model/wide-bump/qi-cover-wide-bump.stl) with the wide camera bump (model/wide-bump/wide-bump.stl, print pose) put back
# where it sits on the phone. Two images: outside straight on (orthographic) and a low side view (tilt check).
# Usage (from this project's folder): blender -b --python scripts/wide_bump_render.py -- <out_dir>
import os, sys, math, bpy, mathutils
out = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=os.path.abspath("model/wide-bump/qi-cover-wide-bump.stl")); frame = bpy.context.selected_objects[0]
bpy.ops.wm.stl_import(filepath=os.path.abspath("model/wide-bump/wide-bump.stl")); bump = bpy.context.selected_objects[0]
# print pose (make_wide_bump.py: roof down at Z 0; assembled Z -6.2..-1.8) -> phone frame: z - 6.2
bump.matrix_world = mathutils.Matrix.Translation((0, 0, -6.2))
rot = mathutils.Matrix.Rotation(math.pi, 4, "Y")          # outside face (Z -3) towards +Z
for o in (frame, bump): o.matrix_world = rot @ o.matrix_world
m1 = bpy.data.materials.new("f"); m2 = bpy.data.materials.new("b")
frame.data.materials.append(m1); bump.data.materials.append(m2)
m1.diffuse_color = (0.72, 0.74, 0.78, 1); m2.diffuse_color = (0.95, 0.55, 0.25, 1)
sc = bpy.context.scene
try: sc.render.engine = "BLENDER_WORKBENCH"
except TypeError: pass
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"
sh.show_cavity = True; sh.cavity_type = "BOTH"; sh.show_object_outline = True
sh.show_shadows = True; sh.shadow_intensity = 0.35
sh.background_type = "VIEWPORT"; sh.background_color = (1, 1, 1)
sc.view_settings.view_transform = "Standard"
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); sc.collection.objects.link(co); sc.camera = co
def shot(name, loc, look, ortho, rx, ry):
    cam.type = "ORTHO"; cam.ortho_scale = ortho
    co.location = loc
    co.rotation_euler = (mathutils.Vector(look) - mathutils.Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    sc.render.resolution_x, sc.render.resolution_y = rx, ry
    sc.render.filepath = os.path.join(out, name); bpy.ops.render.render(write_still=True)
shot("outside.png", (0, -0.3, 60), (0, -0.3, 0), 166, 840, 1660)
# side view from the phone's bottom edge, along the plate: bump height vs. the plate
shot("side.png", (0, -200, 3.5), (0, 0, 3.5), 84, 1680, 300)
