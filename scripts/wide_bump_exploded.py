# Blender: exploded view of the wide camera bump above the Qi cover's INSIDE, to show that it goes in from the inside.
# Usage (from this project's folder): blender -b --python scripts/wide_bump_exploded.py -- <out.png>
import os, sys, math, bpy, mathutils
out = os.path.abspath(sys.argv[sys.argv.index("--") + 1])
LIFT = 18.0
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.stl_import(filepath=os.path.abspath("model/wide-bump/qi-cover-wide-bump.stl")); frame = bpy.context.selected_objects[0]
bpy.ops.wm.stl_import(filepath=os.path.abspath("model/wide-bump/wide-bump.stl")); bump = bpy.context.selected_objects[0]
bump.matrix_world = mathutils.Matrix.Translation((0, 0, -6.2 + LIFT))   # print pose roof down at Z 0 -> phone frame
m1 = bpy.data.materials.new("f"); m2 = bpy.data.materials.new("b")
frame.data.materials.append(m1); bump.data.materials.append(m2)
m1.diffuse_color = (0.72, 0.74, 0.78, 1); m2.diffuse_color = (0.95, 0.55, 0.25, 1)
sc = bpy.context.scene
try: sc.render.engine = "BLENDER_WORKBENCH"
except TypeError: pass
sh = sc.display.shading
sh.light = "STUDIO"; sh.color_type = "MATERIAL"; sh.show_cavity = True; sh.cavity_type = "BOTH"
sh.show_object_outline = True; sh.background_type = "VIEWPORT"; sh.background_color = (1, 1, 1)
sc.view_settings.view_transform = "Standard"
cam = bpy.data.cameras.new("c"); cam.type = "ORTHO"; cam.ortho_scale = 120
co = bpy.data.objects.new("c", cam); sc.collection.objects.link(co); sc.camera = co
look = mathutils.Vector((0, 25, 8)); co.location = look + mathutils.Vector((90, -160, 130))
co.rotation_euler = (look - co.location).to_track_quat("-Z", "Y").to_euler()
sc.render.resolution_x, sc.render.resolution_y = 1400, 1400
sc.render.filepath = out; bpy.ops.render.render(write_still=True)
