import os
import subprocess
from pathlib import Path
from PIL import Image

BASE_DIR = Path(r"E:\esp-idf-fun\FYP-Folder")
ASSETS_DIR = BASE_DIR / "assets"
IMG_DIR = ASSETS_DIR / "images"
GIF_DIR = ASSETS_DIR / "gifs"

IMG_DIR.mkdir(parents=True, exist_ok=True)
GIF_DIR.mkdir(parents=True, exist_ok=True)

print("Created assets directories.")

# 1. Process and convert images to webp
def convert_image(src_path: Path, dest_name: str):
    try:
        dest_path = IMG_DIR / f"{dest_name}.webp"
        with Image.open(src_path) as im:
            # Convert RGBA / CMYK / P to RGB if saving as webp unless transparency is needed
            if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
                im = im.convert("RGBA")
            else:
                im = im.convert("RGB")
            
            # Resize if excessively large (e.g. > 1920)
            max_size = 1920
            if max(im.size) > max_size:
                im.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                
            im.save(dest_path, "WEBP", quality=85, method=4)
            print(f"[IMG] Converted: {src_path.name} -> {dest_path.name} ({dest_path.stat().st_size // 1024} KB)")
            return f"assets/images/{dest_name}.webp"
    except Exception as e:
        print(f"[IMG ERR] {src_path.name}: {e}")
        return None

# Convert selected videos to GIF using ffmpeg
def convert_video_to_gif(src_path: Path, dest_name: str, duration=6, fps=12, width=480):
    try:
        dest_path = GIF_DIR / f"{dest_name}.gif"
        if dest_path.exists() and dest_path.stat().st_size > 0:
            print(f"[GIF EXISTS] {dest_path.name}")
            return f"assets/gifs/{dest_name}.gif"
            
        print(f"[GIF] Converting {src_path.name} to {dest_name}.gif...")
        # FFmpeg two-pass palette generation for high quality, small gif
        vf = f"fps={fps},scale={width}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128[p];[s1][p]paletteuse=dither=bayer"
        cmd = [
            "ffmpeg", "-y",
            "-ss", "0",
            "-t", str(duration),
            "-i", str(src_path),
            "-vf", vf,
            str(dest_path)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode == 0 and dest_path.exists():
            print(f"[GIF OK] {dest_name}.gif ({dest_path.stat().st_size // 1024} KB)")
            return f"assets/gifs/{dest_name}.gif"
        else:
            print(f"[GIF FAIL] {src_path.name}: {res.stderr[:200]}")
            return None
    except Exception as e:
        print(f"[GIF ERR] {src_path.name}: {e}")
        return None

manifest = {}

# Images to convert:
image_tasks = [
    # Version 1
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/boost converter added.jpg", "v1-boost-converter-added"),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/bread board setup.jpg", "v1-breadboard-setup"),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/desk setup.jpg", "v1-desk-setup"),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/vero board back.jpg", "v1-veroboard-back"),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/vero board setup.jpg", "v1-veroboard-setup"),
    
    # Version 2
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/two pcbs of version 2.jpg", "v2-two-pcbs"),
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/version 2 after assembly.jpg", "v2-assembled-pcb"),
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/version 2 pcb in easy eda.png", "v2-easyeda-pcb-design"),
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/version 2 weight full drone.jpg", "v2-weight-full-drone"),
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/version 2 weight.jpg", "v2-weight-board"),
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/weight of version 2.jpg", "v2-drone-weight-scale"),

    # Version 3
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/top bottom version3 pcb.jpg", "v3-top-bottom-pcb"),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/All-videos/PCBs size.jpg", "v3-pcbs-size-comparison"),

    # Research Paper figures
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/3D-Printed-real.png", "3d-printed-airframe-real"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Both-drones.png", "both-drones-comparison"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Confusion_matrix,.JPG", "confusion-matrix-tinyml"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Custom-Drone-final-bottom.jpg", "custom-drone-final-bottom"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Custom-Drone-final-top.jpg", "custom-drone-final-top"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/DRONE-3d-frame-rendering.jpg", "drone-3d-cad-frame-rendering"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/DRONE-single-vs-swarm-converage-Comparison.png", "swarm-vs-single-drone-coverage"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Drone-Architecture.png", "dual-mcu-drone-architecture"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/ESP32-schm.jpg", "esp32-schematic-eda"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/ESP32S3-ONboard-pixhawk-based-drone.jpg", "esp32s3-pixhawk-mounted"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/LIVE-DASHboard-(feed-and-arm-disarm-buttons).jpg", "live-telemetry-dashboard"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/LIve-multiple-persons-detection.jpg", "live-multiple-persons-detection"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/Live-person-detection-drone-in-flight.jpg", "live-person-detection-in-flight"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/PIXHAWK-Based-drone-labeled.png", "pixhawk-based-drone-labeled"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/custom-fc-soldered-bottom.png", "custom-fc-soldered-bottom"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/custom-fc-soldered-top.png", "custom-fc-soldered-top"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/p2-pcb-render-bottom.png", "p2-pcb-render-bottom"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/p2-pcb-render-top.png", "p2-pcb-render-top"),
    (BASE_DIR / "stuff-related-to-fyp/Research-Paper/figures/stm32-schm.jpg", "stm32-schematic-eda"),

    # Backgrounds & Slides
    (BASE_DIR / "firstpagebackground/slide1.jpg", "bg-slide1"),
    (BASE_DIR / "firstpagebackground/slide2.jpg", "bg-slide2"),
    (BASE_DIR / "firstpagebackground/slide3.jpg", "bg-slide3"),
    (BASE_DIR / "prototyping.jpg", "prototyping-workbench"),

    # Designing & Prototyping
    (BASE_DIR / "designing-media/designing-1.png", "cad-design-assembly"),
    (BASE_DIR / "designing-media/designing-2.png", "cad-rotor-clearance"),
    (BASE_DIR / "designing-media/designing-3.png", "cad-center-of-gravity"),
    (BASE_DIR / "prototyping,multimedia/veroboard1.jpg", "veroboard-soldered-prototype"),
    (BASE_DIR / "prototyping,multimedia/PXL_20250820_084742945.jpg", "oscilloscope-bench-validation"),

    # Team Images
    (BASE_DIR / "teamimages/laraib.jpg", "team-laraib"),
    (BASE_DIR / "teamimages/saad karim.jpg", "team-saad"),
    (BASE_DIR / "teamimages/khuzaifa.jpg", "team-khuzaifa"),
    (BASE_DIR / "teamimages/dr waqas.png", "team-dr-waqas"),
    (BASE_DIR / "teamimages/cosupervisor.jpg", "team-arham-hassan"),
]

for src, name in image_tasks:
    if src.exists():
        res = convert_image(src, name)
        manifest[name] = res
    else:
        print(f"[MISSING] {src}")

# Videos to convert to GIFs:
video_tasks = [
    # V1
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/current test on one motor.mp4", "v1-motor-current-test", 4),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/final bread board test.mp4", "v1-breadboard-spin-test", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/wifi ui test and imu integrated.mp4", "v1-wifi-ui-imu-test", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 1/images videos version1/vero board test.mp4", "v1-veroboard-vibration-test", 5),

    # V2
    (BASE_DIR / "Micro drone saad laraib/Version 2/images videos version2/working video.mp4", "v2-drone-working-demo", 5),

    # V3
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/All-videos/test1-hover.mp4", "v3-test1-hover-flight", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/All-videos/test2-guided-mode.mp4", "v3-test2-guided-flight", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/DRONE-custom-arm-test-with-props.mp4", "v3-arm-propeller-spin", 4),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/ESP32-Human-DETECTION.mp4", "v3-esp32-human-detection", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/First-power-up-of custom-FC.mp4", "v3-custom-fc-first-powerup", 5),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/ONE-motor-test.mp4", "v3-single-motor-test", 4),
    (BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/Previous-video-with-2-drone-test.mp4", "v3-two-drone-bench-test", 5),

    # Multimedia videos
    (BASE_DIR / "prototyping,multimedia/veroboardvvvideo.mp4", "veroboard-telemetry-demo", 5),
    (BASE_DIR / "prototyping,multimedia/PXL_20251020_062310826~2.mp4", "drone-motor-spin-vibration", 5),
]

for src, name, dur in video_tasks:
    if src.exists():
        res = convert_video_to_gif(src, name, duration=dur, fps=10, width=440)
        manifest[name] = res
    else:
        print(f"[MISSING VID] {src}")

# Copy existing app-overview.gif if exists
existing_gif = BASE_DIR / "Micro drone saad laraib/Version 3/images videos version3/app-overview/app-overview.gif"
if existing_gif.exists():
    import shutil
    shutil.copy2(existing_gif, GIF_DIR / "v3-app-overview.gif")
    manifest["v3-app-overview"] = "assets/gifs/v3-app-overview.gif"
    print("[GIF COPIED] v3-app-overview.gif")

print(f"\nDone! Total items in manifest: {len(manifest)}")
