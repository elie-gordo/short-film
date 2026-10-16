"""TENSION teaser: dark studio, 30 s master timeline, one camera per shot, EEVEE renders.

Runs on assets/3d/tensil_lamp.blend (copied from blender-studio-object, built in the work pose).
The source .blend is never overwritten: the film scene is saved to blender/tensil_film.blend.

Usage (from the repo root):
  B="C:/Program Files/Blender Foundation/Blender 5.2/blender.exe"
  "$B" -b assets/3d/tensil_lamp.blend --python blender/film.py -- build
  "$B" -b blender/tensil_film.blend --python blender/film.py -- still P04 196 out.png [--preview]
  "$B" -b blender/tensil_film.blend --python blender/film.py -- shot P02 [--preview] [--ref]
  "$B" -b blender/tensil_film.blend --python blender/film.py -- probe
"""
import math
import os
import sys

import bpy
from mathutils import Vector

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FILM_BLEND = os.path.join(ROOT, "blender", "tensil_film.blend")
FPS = 30
FRAME_END = 900  # 30 s

# Storyboard (frame = seconds * 30 + 1). "use" = frames kept in the edit, "ref" = frames sent to
# Seedance as motion reference (Seedance clips are 4 s minimum, so short shots get handles).
SHOTS = {
    "P02": {"use": (46, 135), "route": "eevee"},
    "P03": {"use": (136, 195), "route": "eevee"},
    "P04": {"use": (196, 300), "ref": (181, 330), "route": "seedance"},
    "P05": {"use": (301, 420), "ref": (286, 435), "route": "seedance"},
    "P06": {"use": (421, 480), "route": "eevee"},
    "P07": {"use": (481, 540), "ref": (466, 585), "route": "seedance"},
    "P08": {"use": (541, 660), "ref": (526, 675), "route": "seedance"},
    "P09": {"use": (661, 705), "route": "eevee"},
    "P10": {"use": (706, 900), "ref": (706, 855), "route": "seedance"},
}

# Lamp motion, degrees per joint: folded until 1 s into P05, then one joint per beat
# (shoulder P05, elbow P06, head P07), a damped settle in P08, still afterwards.
JOINT_KEYS = {
    "RIG_Yaw": ("z", [(1, 0), (300, 0), (560, -20)]),
    "RIG_Shoulder": ("x", [(1, -10), (320, -10), (405, 17), (420, 15), (560, 16.2), (585, 14.6), (610, 15)]),
    "RIG_Elbow": ("x", [(1, 130), (345, 130), (470, 64), (486, 68), (565, 67), (590, 68.4), (615, 68)]),
    "RIG_Wrist": ("x", [(1, 30), (486, 30), (528, 86), (545, 78), (560, 80)]),
}
SWITCH_PRESS = [(1, 0.0), (684, 0.0), (687, 1.0), (694, 1.0), (698, 0.0)]  # fraction of travel
SWITCH_TRAVEL = 0.0018  # metres, into the base
BULB_ON = {"emission": 30.0, "spot": 28.0}  # same values as blender-studio-object/build.py
BULB_KEYS = [(706, 0.0), (712, 0.7), (716, 0.12), (722, 0.9), (726, 0.45), (733, 1.0)]
STUDIO_KEYS = [(1, 1.0), (712, 1.0), (745, 0.25)]  # the room light gives way to the lamp


def _ease(owner, interpolation="BEZIER"):
    anim = owner.animation_data
    if not anim or not anim.action:
        return
    action = anim.action
    curves = list(action.fcurves) if hasattr(action, "fcurves") and len(action.fcurves) else []
    for layer in getattr(action, "layers", []):
        for strip in layer.strips:
            bag = strip.channelbag(anim.action_slot)
            if bag:
                curves.extend(bag.fcurves)
    for fc in curves:
        for kp in fc.keyframe_points:
            kp.interpolation = interpolation
            kp.handle_left_type = kp.handle_right_type = "AUTO_CLAMPED"


def _clear_animation():
    for block in list(bpy.data.objects) + list(bpy.data.lights) + list(bpy.data.materials):
        if block.animation_data:
            block.animation_data_clear()
        tree = getattr(block, "node_tree", None)
        if tree and tree.animation_data:
            tree.animation_data_clear()


def animate_lamp():
    for name, (axis, keys) in JOINT_KEYS.items():
        obj, idx = bpy.data.objects[name], "xyz".index(axis)
        for frame, deg in keys:
            obj.rotation_euler[idx] = math.radians(deg)
            obj.keyframe_insert("rotation_euler", index=idx, frame=frame)
        _ease(obj)


def animate_switch():
    knob = bpy.data.objects["Base_SwitchKnob"]
    rest = knob.location.copy()
    inward = -Vector((rest.x, rest.y, 0)).normalized()
    for frame, frac in SWITCH_PRESS:
        knob.location = rest + inward * SWITCH_TRAVEL * frac
        knob.keyframe_insert("location", frame=frame)
    _ease(knob, "LINEAR")


def animate_bulb_and_room(room_lights):
    mat = bpy.data.materials["MAT_Bulb"]
    socket = mat.node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    spot = bpy.data.objects["LGT_Bulb"].data
    for frame, frac in [(1, 0.0)] + BULB_KEYS:
        socket.default_value = BULB_ON["emission"] * frac
        socket.keyframe_insert("default_value", frame=frame)
        spot.energy = BULB_ON["spot"] * frac
        spot.keyframe_insert("energy", frame=frame)
    _ease(mat.node_tree, "LINEAR")
    _ease(spot, "LINEAR")
    for light in room_lights:
        base = light.data.energy
        for frame, mult in STUDIO_KEYS:
            light.data.energy = base * mult
            light.data.keyframe_insert("energy", frame=frame)
        _ease(light.data)


# ---------------------------------------------------------------- look: dark studio
BACKDROP_COLOR = (0.022, 0.021, 0.02, 1)  # charcoal, close to the site's night #0f0e0d once lit
BACKDROP_SHIFT_Y = -0.45  # back wall ~1.15 m behind the lamp; the floor curve starts 0.25 m behind it
# name: (location, size, energy W) — a hard raking key, a rim to cut the silhouette, almost no fill
ROOM_LIGHTS = {
    "LGT_Key": ((-0.95, -0.85, 0.55), 0.22, 30.0),
    "LGT_Rim": ((0.7, 0.45, 0.9), 0.5, 35.0),
    "LGT_Fill": ((1.6, -1.1, 0.7), 1.8, 0.0),
}
# Small moving source for the macros: a highlight travels along the spring (P02), then the cap (P03)
SWEEP_KEYS = [(40, (0.30, -0.30, 0.05)), (135, (0.30, 0.05, 0.26)), (195, (0.22, 0.25, 0.46))]
SWEEP_ENERGY = [(1, 0.0), (44, 0.0), (52, 2.0), (190, 2.0), (198, 0.0)]


def look():
    scene = bpy.context.scene
    bpy.data.materials["MAT_Backdrop"].node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = BACKDROP_COLOR
    bpy.data.objects["Studio_Cyclorama"].location.y = BACKDROP_SHIFT_Y
    scene.world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.008
    lights = []
    for name, (loc, size, energy) in ROOM_LIGHTS.items():
        obj = bpy.data.objects[name]
        obj.location = loc
        obj.data.size = size
        obj.data.energy = energy
        lights.append(obj)
    data = bpy.data.lights.get("LGT_Sweep") or bpy.data.lights.new("LGT_Sweep", "AREA")
    data.shape, data.size, data.color = "DISK", 0.05, (1.0, 0.95, 0.88)
    sweep = bpy.data.objects.get("LGT_Sweep") or bpy.data.objects.new("LGT_Sweep", data)
    if not sweep.users_collection:
        bpy.data.objects["LGT_Key"].users_collection[0].objects.link(sweep)
    track = sweep.constraints.get("Track To") or sweep.constraints.new("TRACK_TO")
    track.target = _empty("LGT_Sweep_Target", (0.029, 0.06, 0.25))
    track.track_axis, track.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
    for frame, loc in SWEEP_KEYS:
        sweep.location = loc
        sweep.keyframe_insert("location", frame=frame)
    for frame, energy in SWEEP_ENERGY:
        data.energy = energy
        data.keyframe_insert("energy", frame=frame)
    _ease(sweep)
    _ease(data, "LINEAR")
    return lights


def _empty(name, loc):
    obj = bpy.data.objects.get(name) or bpy.data.objects.new(name, None)
    if not obj.users_collection:
        bpy.context.scene.collection.objects.link(obj)
    obj.empty_display_size = 0.02
    obj.location = loc
    return obj


# ---------------------------------------------------------------- cameras, one per shot
# shot: (lens mm, f-stop, [(frame, camera loc)], [(frame, aim point)])
CAMERAS = {
    # macro, lateral travel up the lower spring while the lamp sleeps folded
    "P02": (100, 2.8, [(46, (0.165, -0.07, 0.095)), (135, (0.16, -0.03, 0.165))],
            [(46, (0.029, 0.057, 0.105)), (135, (0.029, 0.052, 0.165))]),
    # macro on the brass cap of the elbow pivot, almost still
    "P03": (100, 2.8, [(136, (0.135, -0.005, 0.40)), (195, (0.125, 0.008, 0.395))],
            [(136, (0.02, 0.082, 0.385)), (195, (0.02, 0.082, 0.385))]),
    # folded silhouette, slow dolly in, shadow on the wall behind
    "P04": (50, 5.6, [(181, (-0.78, -1.30, 0.32)), (330, (-0.62, -1.04, 0.30))],
            [(181, (0.0, 0.0, 0.20)), (330, (0.0, 0.0, 0.21))]),
    # low three-quarter, the shoulder lifts the arm
    "P05": (35, 5.6, [(286, (1.10, -0.30, 0.13)), (435, (1.05, -0.36, 0.15))],
            [(286, (0.0, -0.12, 0.20)), (435, (-0.02, -0.18, 0.25))]),
    # close-up on the upper spring while the elbow opens
    "P06": (85, 2.8, [(421, (0.23, -0.10, 0.31)), (480, (0.22, -0.08, 0.29))],
            [(421, (0.022, -0.012, 0.29)), (480, (0.02, -0.006, 0.27))]),
    # the head tips down, the brass rim catches the light
    "P07": (70, 4.0, [(466, (0.22, -1.0, 0.30)), (585, (0.19, -0.96, 0.32))],
            [(466, (-0.11, -0.37, 0.38)), (585, (-0.13, -0.34, 0.38))]),
    # wide profile, the lamp settles, very slow push
    "P08": (60, 8.0, [(526, (1.62, -0.76, 0.30)), (675, (1.48, -0.71, 0.29))],
            [(526, (-0.06, -0.15, 0.24)), (675, (-0.06, -0.15, 0.24))]),
    # macro on the brass switch
    "P09": (100, 2.8, [(661, (0.135, -0.245, 0.05)), (705, (0.13, -0.24, 0.048))],
            [(661, (0.05, -0.094, 0.016)), (705, (0.05, -0.094, 0.016))]),
    # three-quarter hero, locked off: flicker, the cone lands on the floor
    "P10": (65, 8.0, [(706, (1.05, -2.0, 0.55)), (900, (1.03, -1.97, 0.55))],
            [(706, (-0.10, -0.12, 0.22)), (900, (-0.10, -0.12, 0.22))]),
}


def cameras():
    scene = bpy.context.scene
    coll = bpy.data.objects["CAM_Hero"].users_collection[0]
    scene.timeline_markers.clear()
    for shot, (lens, fstop, locs, aims) in CAMERAS.items():
        name = f"CAM_{shot}"
        data = bpy.data.cameras.get(name) or bpy.data.cameras.new(name)
        data.lens, data.sensor_width = lens, 36
        data.clip_start = 0.01
        cam = bpy.data.objects.get(name) or bpy.data.objects.new(name, data)
        if not cam.users_collection:
            coll.objects.link(cam)
        target = _empty(f"{name}_Target", aims[0][1])
        track = cam.constraints.get("Track To") or cam.constraints.new("TRACK_TO")
        track.target = target
        track.track_axis, track.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"
        data.dof.use_dof, data.dof.focus_object, data.dof.aperture_fstop = True, target, fstop
        for frame, loc in locs:
            cam.location = loc
            cam.keyframe_insert("location", frame=frame)
        for frame, loc in aims:
            target.location = loc
            target.keyframe_insert("location", frame=frame)
        _ease(cam)
        _ease(target)
        start = 1 if shot == "P02" else SHOTS[shot]["use"][0]
        scene.timeline_markers.new(shot, frame=start).camera = cam
    scene.camera = bpy.data.objects["CAM_P02"]


def render_settings(preview):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    eevee = scene.eevee
    eevee.taa_render_samples = 16 if preview else 96
    for attr, value in (("use_raytracing", True), ("use_shadows", True), ("use_gtao", True)):
        if hasattr(eevee, attr):
            setattr(eevee, attr, value)
    if hasattr(eevee, "ray_tracing_options"):
        eevee.ray_tracing_options.resolution_scale = "2" if preview else "1"
    scene.render.resolution_x, scene.render.resolution_y = (1280, 720) if preview else (1920, 1080)
    scene.render.resolution_percentage = 100
    scene.render.film_transparent = False
    scene.render.use_motion_blur = not preview
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"


def workbench_settings():
    """Solid-shaded preview: enough for Seedance to read camera, pose and timing, near-instant."""
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_WORKBENCH"
    shading = scene.display.shading
    shading.light, shading.color_type = "STUDIO", "MATERIAL"
    shading.show_shadows, shading.shadow_intensity = True, 0.6
    shading.show_cavity = True
    scene.display.shadow_shift = 0.05
    scene.world.color = (0.16, 0.16, 0.16)
    scene.render.resolution_x, scene.render.resolution_y = 1280, 720
    scene.render.resolution_percentage = 100
    scene.render.use_motion_blur = False
    scene.view_settings.view_transform = "Standard"
    scene.view_settings.look = "None"


def _image_output(path):
    scene = bpy.context.scene
    settings = scene.render.image_settings
    if hasattr(settings, "media_type"):
        settings.media_type = "IMAGE"
    settings.file_format, settings.color_mode, settings.color_depth = "PNG", "RGB", "8"
    scene.render.filepath = path


def _video_output(path):
    scene = bpy.context.scene
    settings = scene.render.image_settings
    if hasattr(settings, "media_type"):
        settings.media_type = "VIDEO"
    settings.file_format = "FFMPEG"
    ff = scene.render.ffmpeg
    ff.format, ff.codec = "MPEG4", "H264"
    ff.constant_rate_factor, ff.ffmpeg_preset = "HIGH", "GOOD"
    ff.audio_codec = "NONE"
    scene.render.filepath = path


def _lock_camera(shot):
    """Single-shot renders: drop the edit markers, or they switch cameras inside the handles."""
    scene = bpy.context.scene
    scene.timeline_markers.clear()
    scene.camera = bpy.data.objects[f"CAM_{shot}"]


def render_still(shot, frame, out, preview):
    scene = bpy.context.scene
    _lock_camera(shot)
    render_settings(preview)
    scene.camera = bpy.data.objects[f"CAM_{shot}"]
    scene.frame_set(frame)
    _image_output(os.path.abspath(out))
    bpy.ops.render.render(write_still=True)


def render_shot(shot, preview, ref):
    """EEVEE shot: PNG frames + MP4. With --ref, the Seedance motion reference range instead."""
    scene = bpy.context.scene
    spec = SHOTS[shot]
    first, last = spec["ref"] if ref else spec["use"]
    _lock_camera(shot)
    render_settings(preview)
    scene.frame_start, scene.frame_end = first, last
    kind = "ref" if ref else ("preview" if preview else "final")
    out_dir = os.path.join(ROOT, "export", "shots", kind)
    os.makedirs(out_dir, exist_ok=True)
    if ref:
        # Look comes from these two full-quality EEVEE stills; the video only carries motion.
        render_settings(preview=False)
        for suffix, frame in (("first", first), ("last", last)):
            _image_output(os.path.join(out_dir, f"{shot}_{suffix}.png"))
            scene.frame_set(frame)
            bpy.ops.render.render(write_still=True)
        workbench_settings()
        _video_output(os.path.join(out_dir, f"{shot}_ref.mp4"))
    elif preview:
        _video_output(os.path.join(out_dir, f"{shot}.mp4"))
    else:
        _image_output(os.path.join(out_dir, shot, "f_####"))
    bpy.ops.render.render(animation=True)


def render_animatic():
    """Whole 30 s timeline, solid shading; timeline markers switch the camera at each cut."""
    scene = bpy.context.scene
    workbench_settings()
    scene.frame_start, scene.frame_end = 1, FRAME_END
    out_dir = os.path.join(ROOT, "export", "animatic")
    os.makedirs(out_dir, exist_ok=True)
    _video_output(os.path.join(out_dir, "tensil_animatic_blender.mp4"))
    bpy.ops.render.render(animation=True)


def world_pos(name, frame):
    bpy.context.scene.frame_set(frame)
    return bpy.data.objects[name].matrix_world.translation.copy()


def probe():
    names = ["ANC_Lower_A_L", "ANC_Lower_B_L", "ANC_Upper_A_L", "ANC_Upper_B_L", "RIG_Shoulder",
             "RIG_Elbow", "RIG_Wrist", "Head_Bulb", "Base_SwitchKnob", "Base_Logo"]
    for frame in (1, 300, 420, 480, 540, 660):
        print("PROBE", frame, {n: tuple(round(v, 3) for v in world_pos(n, frame)) for n in names})


def build():
    scene = bpy.context.scene
    _clear_animation()
    scene.render.fps = FPS
    scene.frame_start, scene.frame_end = 1, FRAME_END
    animate_lamp()
    animate_switch()
    animate_bulb_and_room(look())
    cameras()
    render_settings(preview=True)
    scene.frame_set(1)


def main():
    args = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    cmd = args[0] if args else "build"
    preview = "--preview" in args
    if cmd == "build":
        build()
        bpy.ops.wm.save_as_mainfile(filepath=FILM_BLEND)
    elif cmd == "probe":
        build()
        probe()
    elif cmd == "still":
        render_still(args[1], int(args[2]), args[3], preview)
    elif cmd == "shot":
        render_shot(args[1], preview, "--ref" in args)
    elif cmd == "animatic":
        render_animatic()
    else:
        raise SystemExit(f"unknown command {cmd}")


if __name__ == "__main__":
    main()
