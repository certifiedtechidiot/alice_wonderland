"""
🎭 Alice in Wonderland - Live Stage Production Assembly Pipeline
Merges background video loops, BGM/SFX, normalized ElevenLabs voiceovers,
and stage-safe subtitles into the final theatrical projection video.
"""

import os
import sys
import json
import subprocess
from pathlib import Path
import numpy as np
import scipy.io.wavfile as wavfile

# Configuration & Constants
WORKSPACE_DIR = Path(r"C:\new projects")
OUTPUT_VO_DIR = WORKSPACE_DIR / "output"
ASSETS_DIR = WORKSPACE_DIR / "assets"
BG_DIR = ASSETS_DIR / "backgrounds"
AUDIO_DIR = ASSETS_DIR / "audio"
SUBTITLES_DIR = WORKSPACE_DIR / "subtitles"
SCRIPTS_DIR = WORKSPACE_DIR / "scripts"
FINAL_VIDEO_PATH = WORKSPACE_DIR / "final_alice_in_wonderland_stage.mp4"
CUE_SHEET_PATH = WORKSPACE_DIR / "cue_sheet.txt"
TIMELINE_JSON_PATH = WORKSPACE_DIR / "timeline_config.json"

SAMPLE_RATE = 44100
FPS = 30
VIDEO_WIDTH = 1920
VIDEO_HEIGHT = 1080

def run_command(cmd, desc="Running command"):
    print(f"  • {desc}...")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Error during {desc}:")
        print(res.stderr[:800])
        raise RuntimeError(f"Command failed: {' '.join(str(x) for x in cmd[:5])}...")
    return res.stdout

def step1_verify_audio_files():
    print("\n" + "=" * 80)
    print("STEP 1: DISCOVER & VERIFY AUDIO FILES")
    print("=" * 80)
    valid_chars = {"alice", "white_rabbit", "cheshire_cat", "mad_hatter", "march_hare", "dormouse", "red_queen", "card_soldier"}
    mp3_files = [f for f in OUTPUT_VO_DIR.rglob("*.mp3") if f.parent.name in valid_chars and not f.name.startswith("test_")]
    print(f"Found {len(mp3_files)} total valid character MP3 files in {OUTPUT_VO_DIR}")

    cue_map = {}
    for f in mp3_files:
        prefix = f.name[:2]
        if prefix.isdigit():
            cue_num = int(prefix)
            if f.stat().st_size == 0:
                raise ValueError(f"Cue file is empty (0 bytes): {f}")
            cue_map[cue_num] = f

    missing = [i for i in range(1, 29) if i not in cue_map]
    if missing:
        print(f"❌ CRITICAL ERROR: Missing {len(missing)} cue(s): {missing}")
        sys.exit(1)

    print(f"✓ All 28 cue audio files successfully verified (Cues 01 to 28 non-empty).")
    return cue_map

def step2_load_timeline(cue_map):
    print("\n" + "=" * 80)
    print("STEP 2: LOAD TIMELINE & STAGE PACING")
    print("=" * 80)

    # Re-run build_timeline to ensure all timings are up to date
    if str(SCRIPTS_DIR) not in sys.path:
        sys.path.insert(0, str(SCRIPTS_DIR))
    import build_timeline as bt
    config = bt.build_timeline()
    
    total_sec = config["total_runtime_sec"]
    print(f"✓ Timeline loaded. Total runtime: {int(total_sec//60):02d}:{total_sec%60:05.2f} ({total_sec:.2f}s)")
    return config

def read_audio_file(file_path):
    cmd = [
        "ffmpeg", "-v", "error",
        "-i", str(file_path),
        "-f", "f32le",
        "-ac", "2",
        "-ar", str(SAMPLE_RATE),
        "-"
    ]
    res = subprocess.run(cmd, capture_output=True, check=True)
    audio = np.frombuffer(res.stdout, dtype=np.float32).reshape(-1, 2)
    return audio

def step3_mix_audio(config, cue_map):
    print("\n" + "=" * 80)
    print("STEP 3: AUDITORIUM-READY AUDIO MIXING & NORMALIZATION")
    print("=" * 80)

    total_sec = config["total_runtime_sec"]
    total_samples = int(np.ceil(total_sec * SAMPLE_RATE)) + SAMPLE_RATE  # extra 1s buffer

    vo_master = np.zeros((total_samples, 2), dtype=np.float32)
    bgm_master = np.zeros((total_samples, 2), dtype=np.float32)
    dialogue_mask = np.zeros(total_samples, dtype=np.float32)

    # 1. Normalize & place voiceover clips (-15.0 dB target)
    print("Normalizing 28 voiceover cues to consistent -15.0 dB RMS loudness...")
    for c in config["cues"]:
        cue_num = c["cue"]
        f_path = Path(c["file_path"])
        clip = read_audio_file(f_path)
        
        # Measure RMS
        rms = np.sqrt(np.mean(clip ** 2) + 1e-12)
        cur_db = 20 * np.log10(rms)
        target_db = -15.0
        gain = 10 ** ((target_db - cur_db) / 20.0)
        norm_clip = clip * gain

        # Soft peak limit
        peak = np.max(np.abs(norm_clip))
        if peak > 0.98:
            norm_clip = norm_clip * (0.98 / peak)

        start_samp = int(c["start_time"] * SAMPLE_RATE)
        end_samp = start_samp + len(norm_clip)
        vo_master[start_samp:end_samp] += norm_clip

        # Mark dialogue active for ducking (with 0.15s pre/post margin)
        pad_pre = max(0, start_samp - int(0.15 * SAMPLE_RATE))
        pad_post = min(total_samples, end_samp + int(0.15 * SAMPLE_RATE))
        dialogue_mask[pad_pre:pad_post] = 1.0

    print("✓ All voice clips normalized and placed.")

    # 2. Build BGM track per scene
    print("Constructing scene BGM layers...")
    scenes = config["scenes"]
    
    # Scene 1 BGM: from 0.0s to S1 end + transition (23.88s)
    s1_audio = read_audio_file(AUDIO_DIR / "bgm_scene1.mp3")
    s1_start = int(scenes["S1"]["start_time"] * SAMPLE_RATE)
    s1_end = int(scenes["S2"]["start_time"] * SAMPLE_RATE)
    s1_len = s1_end - s1_start
    # Loop s1_audio if needed
    repeats = int(np.ceil(s1_len / len(s1_audio)))
    s1_looped = np.tile(s1_audio, (repeats, 1))[:s1_len]
    # Fade out last 1.5s of transition
    fade_len = int(1.5 * SAMPLE_RATE)
    s1_looped[-fade_len:] *= np.linspace(1, 0, fade_len)[:, None]
    bgm_master[s1_start:s1_end] += s1_looped

    # Scene 2 BGM: from S2 start to S3 start (23.88s to 52.68s)
    s2_audio = read_audio_file(AUDIO_DIR / "bgm_scene2.mp3")
    s2_start = int(scenes["S2"]["start_time"] * SAMPLE_RATE)
    s2_end = int(scenes["S3"]["start_time"] * SAMPLE_RATE)
    s2_len = s2_end - s2_start
    repeats = int(np.ceil(s2_len / len(s2_audio)))
    s2_looped = np.tile(s2_audio, (repeats, 1))[:s2_len]
    # Fade in 1.5s, Fade out 1.5s
    s2_looped[:fade_len] *= np.linspace(0, 1, fade_len)[:, None]
    s2_looped[-fade_len:] *= np.linspace(1, 0, fade_len)[:, None]
    bgm_master[s2_start:s2_end] += s2_looped

    # Scene 3 BGM: from S3 start to S4 start (52.68s to 105.30s)
    s3_audio = read_audio_file(AUDIO_DIR / "bgm_scene3.mp3")
    s3_start = int(scenes["S3"]["start_time"] * SAMPLE_RATE)
    s3_end = int(scenes["S4"]["start_time"] * SAMPLE_RATE)
    s3_len = s3_end - s3_start
    repeats = int(np.ceil(s3_len / len(s3_audio)))
    s3_looped = np.tile(s3_audio, (repeats, 1))[:s3_len]
    s3_looped[:fade_len] *= np.linspace(0, 1, fade_len)[:, None]
    s3_looped[-fade_len:] *= np.linspace(1, 0, fade_len)[:, None]
    bgm_master[s3_start:s3_end] += s3_looped

    # Scene 4 BGM: from S4 start to Cue 28 End
    # Royal Fanfare starts immediately at S4 start, then dramatic march, stops DEAD at Cue 28 end!
    s4_audio = read_audio_file(AUDIO_DIR / "bgm_scene4.mp3")
    s4_start = int(scenes["S4"]["start_time"] * SAMPLE_RATE)
    cue28 = [c for c in config["cues"] if c["cue"] == 28][0]
    cue28_end_samp = int(cue28["end_time"] * SAMPLE_RATE)
    s4_len = cue28_end_samp - s4_start
    repeats = int(np.ceil(s4_len / len(s4_audio)))
    s4_looped = np.tile(s4_audio, (repeats, 1))[:s4_len]
    bgm_master[s4_start:cue28_end_samp] += s4_looped
    # STRICT SILENCE from cue28_end_samp to scene end (1.5s dramatic freeze!)
    s4_end_samp = int(scenes["S4"]["end_time"] * SAMPLE_RATE)
    bgm_master[cue28_end_samp:s4_end_samp] = 0.0
    print(f"✓ Scene 4 dramatic freeze enforced: 1.50s complete silence from {cue28['end_time']:.2f}s to {scenes['S4']['end_time']:.2f}s.")

    # 3. Dynamic Sidechain Ducking (-6 dB duck under dialogue)
    print("Applying dynamic sidechain ducking (-6 dB duck under dialogue lines)...")
    # Smooth dialogue mask using moving average filter (~0.25s window)
    filter_window = int(0.25 * SAMPLE_RATE)
    kernel = np.ones(filter_window) / filter_window
    smooth_mask = np.convolve(dialogue_mask, kernel, mode="same")
    smooth_mask = np.clip(smooth_mask, 0.0, 1.0)[:, None]

    # Ducking curve: 1.0 (0 dB) when no speech -> 0.50 (-6 dB) when speech
    duck_gain = 1.0 - 0.50 * smooth_mask
    bgm_ducked = bgm_master * duck_gain

    # 4. Master Mix: VO + Ducked BGM
    final_mix = vo_master + bgm_ducked
    peak_mix = np.max(np.abs(final_mix))
    if peak_mix > 0.98:
        final_mix = final_mix * (0.98 / peak_mix)

    temp_wav = WORKSPACE_DIR / "temp_master_audio.wav"
    wav_data = (final_mix * 32767).astype(np.int16)
    wavfile.write(str(temp_wav), SAMPLE_RATE, wav_data)
    print(f"✓ Master audio track generated: {temp_wav.name} ({len(wav_data)/SAMPLE_RATE:.2f}s)")
    return temp_wav

def step4_assemble_video(config, master_audio_wav):
    print("\n" + "=" * 80)
    print("STEP 4: VIDEO ASSEMBLY, SUBTITLE BURNING & FINAL EXPORT")
    print("=" * 80)

    scenes = config["scenes"]
    # Scene segment durations (4 scenes, no Outro):
    durations = [
        scenes["S2"]["start_time"] - scenes["S1"]["start_time"],
        scenes["S3"]["start_time"] - scenes["S2"]["start_time"],
        scenes["S4"]["start_time"] - scenes["S3"]["start_time"],
        scenes["S4"]["end_time"] - scenes["S4"]["start_time"]
    ]
    bg_files = [
        BG_DIR / "bg_scene1.mp4",
        BG_DIR / "bg_scene2.mp4",
        BG_DIR / "bg_scene3.mp4",
        BG_DIR / "bg_scene4.mp4"
    ]

    temp_segs = []
    print("Generating scene video segments from background loops...")

    for idx, (dur, bg_f) in enumerate(zip(durations, bg_files)):
        out_seg = WORKSPACE_DIR / f"temp_seg{idx+1}.mp4"
        temp_segs.append(out_seg)
        
        # Build filter for smooth transitions (1.0s crossfade transitions):
        fade_out_start = max(0.0, dur - 1.0)
        if idx == 0:
            vf = f"fade=type=out:start_time={fade_out_start:.2f}:duration=1.0"
        elif idx in (1, 2):
            vf = f"fade=type=in:start_time=0:duration=1.0,fade=type=out:start_time={fade_out_start:.2f}:duration=1.0"
        elif idx == 3:
            # S4: fade in 1.0s, fade out smoothly at end of dramatic freeze
            vf = f"fade=type=in:start_time=0:duration=1.0,fade=type=out:start_time={dur-0.8:.2f}:duration=0.8"

        cmd = [
            "ffmpeg", "-y",
            "-stream_loop", "-1",
            "-i", str(bg_f),
            "-t", f"{dur:.2f}",
            "-vf", vf,
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-r", str(FPS),
            "-crf", "18",
            "-preset", "fast",
            str(out_seg)
        ]
        run_command(cmd, f"Rendering Segment {idx+1} ({dur:.2f}s)")

    # Concatenate segments
    concat_list_file = WORKSPACE_DIR / "concat_list.txt"
    with open(concat_list_file, "w", encoding="utf-8") as f:
        for seg in temp_segs:
            # FFmpeg concat requires forward slashes or escaped backslashes
            clean_path = str(seg.resolve()).replace("\\", "/")
            f.write(f"file '{clean_path}'\n")

    temp_concat_video = WORKSPACE_DIR / "temp_concat_video.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list_file),
        "-c", "copy",
        str(temp_concat_video)
    ]
    run_command(cmd_concat, "Concatenating all 5 scene segments")

    # Final Composite: Concat Video + ASS Subtitles (Top Safe-Zone) + Master Audio -> Final MP4
    print("Muxing final video with top-aligned subtitles and master audio...")
    ass_path = SUBTITLES_DIR / "stage_subtitles.ass"
    # Format path for FFmpeg subtitles filter
    clean_ass_path = str(ass_path.resolve()).replace("\\", "/").replace(":", "\\:")

    final_cmd = [
        "ffmpeg", "-y",
        "-i", str(temp_concat_video),
        "-i", str(master_audio_wav),
        "-vf", f"ass='{clean_ass_path}'",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-r", str(FPS),
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        str(FINAL_VIDEO_PATH)
    ]
    run_command(final_cmd, "Rendering Final Show Video (final_alice_in_wonderland_stage.mp4)")

    # Cleanup temporary files
    for seg in temp_segs:
        seg.unlink(missing_ok=True)
    temp_concat_video.unlink(missing_ok=True)
    concat_list_file.unlink(missing_ok=True)
    master_audio_wav.unlink(missing_ok=True)
    print("✓ Intermediate temporary files cleaned up.")

def step5_verify_export():
    print("\n" + "=" * 80)
    print("STEP 5: FINAL EXPORT VERIFICATION")
    print("=" * 80)
    if not FINAL_VIDEO_PATH.exists():
        raise RuntimeError("Final video export failed; file does not exist!")

    size_bytes = FINAL_VIDEO_PATH.stat().st_size
    size_mb = size_bytes / (1024 * 1024)

    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration,size,bit_rate:stream=codec_name,width,height,r_frame_rate,channels,sample_rate",
        "-of", "json",
        str(FINAL_VIDEO_PATH)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    meta = json.loads(res.stdout)
    duration = float(meta["format"]["duration"])

    video_stream = next(s for s in meta["streams"] if s.get("width"))
    audio_stream = next(s for s in meta["streams"] if s.get("channels"))

    print(f"🎉 FINAL VIDEO ASSEMBLED SUCCESSFULLY!")
    print(f"  • File Location : {FINAL_VIDEO_PATH}")
    print(f"  • File Size     : {size_mb:.2f} MB ({size_bytes:,} bytes)")
    print(f"  • Total Runtime : {int(duration//60):02d}:{duration%60:05.2f} ({duration:.2f} seconds)")
    print(f"  • Video Stream  : {video_stream['codec_name'].upper()} | {video_stream['width']}x{video_stream['height']} @ {video_stream['r_frame_rate']} fps")
    print(f"  • Audio Stream  : {audio_stream['codec_name'].upper()} | {audio_stream['channels']} Channels | {audio_stream['sample_rate']} Hz")
    print(f"  • Cue Sheet     : {CUE_SHEET_PATH}")
    print("=" * 80)

def main():
    cue_map = step1_verify_audio_files()
    config = step2_load_timeline(cue_map)
    master_audio_wav = step3_mix_audio(config, cue_map)
    step4_assemble_video(config, master_audio_wav)
    step5_verify_export()

if __name__ == "__main__":
    main()
