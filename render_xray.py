"""X-ray render of the assembly, as Blender shows it with X-ray on: docs/xray.png.

Run after `dragy_mount.py out` (it reads out/dragy_assembly_v<VERSION>.obj):
    blender -b -P render_xray.py
Workbench engine, solid shading coloured by material, X-ray at ALPHA, object outlines; the camera looks
from above the rider's left, toward the nose, so the screws, the push-out hole and the cap's gasket show.
"""
import math
import pathlib
import sys

import bpy
from mathutils import Vector

ROOT = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
VERSION = next(int(line.split("=")[1]) for line in open(ROOT / "dragy_mount.py") if line.startswith("VERSION ="))
OBJ = ROOT / "out" / f"dragy_assembly_v{VERSION}.obj"
OUT = ROOT / "docs" / "xray.png"

ALPHA = 0.5                 # X-ray opacity
AZ, EL = -35.0, 38.0        # camera: degrees round from the tail (-y) toward the rider's right (+x); above the horizon
SIZE = (1400, 1100)

bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.wm.obj_import(filepath=str(OBJ))   # written Y-up, so the default import is sky-up

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.render.resolution_x, scene.render.resolution_y = SIZE
scene.render.film_transparent = False
sh = scene.display.shading
sh.light = "STUDIO"
sh.color_type = "MATERIAL"
sh.show_xray = True
sh.xray_alpha = ALPHA
sh.show_object_outline = True
sh.object_outline_color = (1.0, 0.45, 0.1)
sh.background_type = "VIEWPORT"
sh.background_color = (0.23, 0.23, 0.23)
scene.view_settings.view_transform = "Standard"

# Camera: aim at the assembly's centre and fit everything in frame.
pts = [o.matrix_world @ Vector(c) for o in scene.objects if o.type == "MESH" for c in o.bound_box]
centre = sum(pts, Vector()) / len(pts)
az, el = math.radians(AZ), math.radians(EL)
direction = Vector((math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)))
cam_data = bpy.data.cameras.new("cam")
cam_data.lens = 50
cam = bpy.data.objects.new("cam", cam_data)
scene.collection.objects.link(cam)
scene.camera = cam
cam.location = centre + direction * 300
cam.rotation_euler = (-direction).to_track_quat("-Z", "Y").to_euler()
bpy.context.view_layer.update()
co, _ = cam.camera_fit_coords(bpy.context.evaluated_depsgraph_get(), [c for p in pts for c in p])
cam.location = Vector(co) + direction * 12   # a little margin

scene.render.filepath = str(OUT)
bpy.ops.render.render(write_still=True)
print(f"wrote {OUT}")
