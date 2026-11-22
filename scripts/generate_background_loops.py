import cv2
import numpy as np
import subprocess
from pathlib import Path

def create_seamless_loop(base_img, effect_func, duration_sec=6.0, fps=30, out_path="out.mp4"):
    num_frames = int(duration_sec * fps)
    h, w, _ = base_img.shape
    
    # Resize base image to exact 1920x1080 if not already
    if (w, h) != (1920, 1080):
        base_img = cv2.resize(base_img, (1920, 1080), interpolation=cv2.INTER_LANCZOS4)
        h, w = 1080, 1920

    temp_raw = Path(out_path).with_suffix(".raw")
    
    with open(temp_raw, "wb") as f_raw:
        for f_idx in range(num_frames):
            t = f_idx / num_frames  # normalized 0.0 to 1.0 (loopable)
            frame = effect_func(base_img, t, f_idx, num_frames)
            f_raw.write(frame.tobytes())

    # Encode with FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", "1920x1080",
        "-pix_fmt", "bgr24",
        "-r", str(fps),
        "-i", str(temp_raw),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",
        "-preset", "fast",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    temp_raw.unlink(missing_ok=True)
    print(f"Generated {out_path} ({duration_sec}s @ {fps}fps)")

# --- EFFECT 1: Scene 1 (Meadow & Rabbit Hole) ---
# Subtle breathing/sway + golden floating pollen/sun dust particles
np.random.seed(42)
s1_num_particles = 140
s1_particles = [
    {
        "x": np.random.uniform(100, 1820),
        "y": np.random.uniform(100, 980),
        "speed_y": np.random.uniform(-40, -15),
        "speed_x": np.random.uniform(5, 25),
        "rad": np.random.uniform(1.8, 4.0),
        "phase": np.random.uniform(0, np.pi * 2),
        "alpha": np.random.uniform(0.3, 0.7)
    }
    for _ in range(s1_num_particles)
]

def effect_scene1(base_img, t, f_idx, total_f):
    # Gentle breathing zoom/pan (scale 1.0 to 1.015 seamlessly using sin)
    scale = 1.0 + 0.012 * np.sin(2 * np.pi * t)
    dx = 4.0 * np.sin(2 * np.pi * t)
    dy = 2.0 * np.cos(2 * np.pi * t)
    M = np.float32([
        [scale, 0, (1 - scale) * 960 + dx],
        [0, scale, (1 - scale) * 540 + dy]
    ])
    frame = cv2.warpAffine(base_img, M, (1920, 1080), borderMode=cv2.BORDER_REFLECT)

    # Particle layer
    overlay = np.zeros_like(frame)
    for p in s1_particles:
        px = (p["x"] + p["speed_x"] * (f_idx / 30.0) + 15 * np.sin(p["phase"] + 2 * np.pi * t)) % 1920
        py = (p["y"] + p["speed_y"] * (f_idx / 30.0) + 8 * np.cos(p["phase"] + 2 * np.pi * t)) % 1080
        curr_alpha = p["alpha"] * (0.6 + 0.4 * np.sin(p["phase"] + 2 * np.pi * t))
        color = (
            int(150 * curr_alpha),
            int(220 * curr_alpha),
            int(255 * curr_alpha)
        )  # BGR golden-yellow
        cv2.circle(overlay, (int(px), int(py)), int(p["rad"]), color, -1, cv2.LINE_AA)

    # Add overlay
    frame = cv2.add(frame, overlay)
    return frame

# --- EFFECT 2: Scene 2 (Twilight Forest) ---
# Bioluminescent glowing fireflies + pulsing mushroom luminosity
np.random.seed(101)
s2_num_fireflies = 160
s2_fireflies = [
    {
        "x": np.random.uniform(80, 1840),
        "y": np.random.uniform(150, 950),
        "vx": np.random.uniform(-18, 18),
        "vy": np.random.uniform(-15, 15),
        "rad": np.random.uniform(2.0, 5.0),
        "phase": np.random.uniform(0, np.pi * 2),
        "color_type": np.random.choice(["cyan", "violet", "emerald"])
    }
    for _ in range(s2_num_fireflies)
]

def effect_scene2(base_img, t, f_idx, total_f):
    frame = base_img.copy()

    # Subtle ambient mystical pulse
    pulse = 1.0 + 0.04 * np.sin(2 * np.pi * t)
    # Apply slight brightness modulation to highlights
    frame = cv2.convertScaleAbs(frame, alpha=pulse, beta=0)

    # Fireflies overlay
    overlay = np.zeros_like(frame)
    for ff in s2_fireflies:
        fx = (ff["x"] + ff["vx"] * (f_idx / 30.0) + 22 * np.sin(ff["phase"] + 2 * np.pi * t)) % 1920
        fy = (ff["y"] + ff["vy"] * (f_idx / 30.0) + 14 * np.cos(ff["phase"] + 2 * np.pi * t)) % 1080
        brightness = (0.5 + 0.5 * np.sin(ff["phase"] + 4 * np.pi * t)) ** 2
        
        if ff["color_type"] == "cyan":
            col = (int(255 * brightness), int(230 * brightness), int(40 * brightness))  # BGR
        elif ff["color_type"] == "violet":
            col = (int(240 * brightness), int(80 * brightness), int(220 * brightness))
        else:
            col = (int(180 * brightness), int(255 * brightness), int(80 * brightness))

        # Soft glow halo
        cv2.circle(overlay, (int(fx), int(fy)), int(ff["rad"] * 2.2), (int(col[0]*0.3), int(col[1]*0.3), int(col[2]*0.3)), -1, cv2.LINE_AA)
        # Bright core
        cv2.circle(overlay, (int(fx), int(fy)), int(ff["rad"]), col, -1, cv2.LINE_AA)

    frame = cv2.add(frame, overlay)
    return frame

# --- EFFECT 3: Scene 3 (Mad Tea Party) ---
# Lantern flicker + curling steam rising from teapots + warm amber fairy dust
np.random.seed(303)
s3_num_steam = 180
s3_steam = [
    {
        "base_x": np.random.choice([780, 960, 1140, 1300]) + np.random.uniform(-40, 40),
        "base_y": np.random.uniform(580, 680),
        "drift_speed": np.random.uniform(-50, -25),
        "wobble": np.random.uniform(10, 30),
        "phase": np.random.uniform(0, np.pi * 2),
        "rad": np.random.uniform(4.0, 10.0),
        "alpha": np.random.uniform(0.15, 0.35)
    }
    for _ in range(s3_num_steam)
]

def effect_scene3(base_img, t, f_idx, total_f):
    # Warm lantern flicker (subtle multi-frequency sine)
    flicker = 1.0 + 0.03 * np.sin(4 * np.pi * t) + 0.015 * np.sin(10 * np.pi * t)
    frame = cv2.convertScaleAbs(base_img, alpha=flicker, beta=int(4 * np.sin(2 * np.pi * t)))

    # Rising steam overlay
    overlay = np.zeros_like(frame)
    for s in s3_steam:
        time_offset = (f_idx / 30.0) % 3.0
        sy = s["base_y"] + s["drift_speed"] * time_offset
        sx = s["base_x"] + s["wobble"] * np.sin(s["phase"] + 2 * np.pi * (sy / 200.0))
        grow = 1.0 + (s["base_y"] - sy) / 120.0
        fade = max(0.0, 1.0 - (s["base_y"] - sy) / 200.0)
        curr_alpha = s["alpha"] * fade
        steam_col = (int(210 * curr_alpha), int(230 * curr_alpha), int(240 * curr_alpha))
        cv2.circle(overlay, (int(sx), int(sy)), int(s["rad"] * grow), steam_col, -1, cv2.LINE_AA)

    # Warm amber fairy dust
    for i in range(50):
        dx = (200 + (i * 35) + 30 * np.sin(i + 2 * np.pi * t)) % 1920
        dy = (300 + (i * 25) - 20 * (f_idx / 30.0)) % 1080
        col = (40, 160, 240)
        cv2.circle(overlay, (int(dx), int(dy)), 2, col, -1, cv2.LINE_AA)

    frame = cv2.add(frame, overlay)
    return frame

# --- EFFECT 4: Scene 4 (Queen of Hearts Rose Garden) ---
# Drifting crimson rose petals fluttering diagonally + sky glow
np.random.seed(404)
s4_num_petals = 90
s4_petals = [
    {
        "x": np.random.uniform(0, 1920),
        "y": np.random.uniform(-100, 1080),
        "vx": np.random.uniform(-45, -20),
        "vy": np.random.uniform(30, 60),
        "size": np.random.uniform(7, 15),
        "rot_speed": np.random.uniform(2, 6),
        "phase": np.random.uniform(0, np.pi * 2)
    }
    for _ in range(s4_num_petals)
]

def effect_scene4(base_img, t, f_idx, total_f):
    frame = base_img.copy()

    # Subtle dramatic sky breath
    sky_pulse = 1.0 + 0.02 * np.sin(2 * np.pi * t)
    # Petals overlay
    overlay = np.zeros_like(frame)
    for p in s4_petals:
        px = (p["x"] + p["vx"] * (f_idx / 30.0) + 20 * np.sin(p["phase"] + 2 * np.pi * t)) % 1920
        py = (p["y"] + p["vy"] * (f_idx / 30.0)) % 1080
        angle = (p["phase"] + p["rot_speed"] * 2 * np.pi * t)
        
        # Draw curved rose petal
        pts = np.array([
            [px - p["size"] * np.cos(angle), py - p["size"] * np.sin(angle)],
            [px + p["size"] * 0.8 * np.sin(angle), py - p["size"] * 0.8 * np.cos(angle)],
            [px + p["size"] * np.cos(angle), py + p["size"] * np.sin(angle)],
            [px - p["size"] * 0.5 * np.sin(angle), py + p["size"] * 0.5 * np.cos(angle)]
        ], np.int32)
        cv2.fillPoly(overlay, [pts], (25, 20, 200))  # BGR crimson red
        cv2.polylines(overlay, [pts], True, (15, 10, 140), 1, cv2.LINE_AA)

    frame = cv2.add(frame, overlay)
    return frame

# --- EFFECT 5: Outro (Curtain Call / The End) ---
# Soft spotlight pulsation + shimmering golden dust in the spotlight beam
np.random.seed(505)
s5_num_motes = 120
s5_motes = [
    {
        "x": 960 + np.random.uniform(-400, 400),
        "y": 520 + np.random.uniform(-350, 350),
        "vx": np.random.uniform(-10, 10),
        "vy": np.random.uniform(-15, -5),
        "rad": np.random.uniform(1.5, 3.5),
        "phase": np.random.uniform(0, np.pi * 2)
    }
    for _ in range(s5_num_motes)
]

def effect_outro(base_img, t, f_idx, total_f):
    # Center spotlight pulse
    spot_pulse = 1.0 + 0.04 * np.sin(2 * np.pi * t)
    frame = base_img.copy()

    overlay = np.zeros_like(frame)
    for m in s5_motes:
        # Check distance to spotlight center
        mx = (m["x"] + m["vx"] * (f_idx / 30.0) + 12 * np.sin(m["phase"] + 2 * np.pi * t))
        my = (m["y"] + m["vy"] * (f_idx / 30.0))
        dist = np.sqrt((mx - 960)**2 + (my - 520)**2)
        if dist < 450:
            shimmer = (0.4 + 0.6 * np.sin(m["phase"] + 4 * np.pi * t)) ** 2
            fade = (1.0 - dist / 450.0) * shimmer
            col = (int(140 * fade), int(220 * fade), int(255 * fade))
            cv2.circle(overlay, (int(mx), int(my)), int(m["rad"]), col, -1, cv2.LINE_AA)

    frame = cv2.add(frame, overlay)
    return frame

def main():
    img_dir = Path("assets/images")
    bg_dir = Path("assets/backgrounds")
    bg_dir.mkdir(parents=True, exist_ok=True)

    scenes = [
        ("scene1_meadow.jpg", effect_scene1, "bg_scene1.mp4", 6.0),
        ("scene2_forest.jpg", effect_scene2, "bg_scene2.mp4", 6.0),
        ("scene3_teaparty.jpg", effect_scene3, "bg_scene3.mp4", 6.0),
        ("scene4_rosegarden.png", effect_scene4, "bg_scene4.mp4", 6.0),
        ("outro_the_end.png", effect_outro, "bg_outro.mp4", 5.0)
    ]

    for img_name, fx_func, out_video, dur in scenes:
        src = img_dir / img_name
        dest = bg_dir / out_video
        img = cv2.imread(str(src))
        if img is None:
            print(f"Error reading {src}")
            continue
        print(f"Rendering seamless loop for {src.name} -> {dest.name}...")
        create_seamless_loop(img, fx_func, duration_sec=dur, fps=30, out_path=str(dest))

if __name__ == "__main__":
    main()
