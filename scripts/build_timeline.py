import os
import re
import json
import subprocess
from pathlib import Path

# Master script data with dialogue text
SCRIPT_DATA = [
    {"cue": 1, "scene": "S1", "character": "WHITE RABBIT", "text": "[panicked] Oh, dear! Oh, dear! I shall be too late!"},
    {"cue": 2, "scene": "S1", "character": "ALICE", "text": "[amazed] A rabbit wearing a waistcoat and carrying a watch? How curious! [excitedly] Oh wait! Mr. Rabbit! Where are you going? What's the hurry?"},
    {"cue": 3, "scene": "S1", "character": "WHITE RABBIT", "text": "[rushed] The Queen will be furious if I don't reach the palace!"},
    {"cue": 4, "scene": "S2", "character": "CHESHIRE CAT", "text": "[mischievously] Welcome to Wonderland, little girl! Looking for someone?"},
    {"cue": 5, "scene": "S2", "character": "ALICE", "text": "I'm looking for my way home."},
    {"cue": 6, "scene": "S2", "character": "CHESHIRE CAT", "text": "[chuckles] That depends on where you want to go! [mischievously] We're all mad here!"},
    {"cue": 7, "scene": "S2", "character": "ALICE", "text": "Everybody seems so strange here!"},
    {"cue": 8, "scene": "S2", "character": "CHESHIRE CAT", "text": "[playfully] Follow the music to the tea party!"},
    {"cue": 9, "scene": "S3", "character": "DORMOUSE", "text": "[sleepily][yawning][sings softly] Twinkle, twinkle, little bat..."},
    {"cue": 10, "scene": "S3", "character": "MAD HATTER", "text": "[excitedly] No room! No room! [playfully] Welcome to our tea party!"},
    {"cue": 11, "scene": "S3", "character": "ALICE", "text": "But there's plenty of room!"},
    {"cue": 12, "scene": "S3", "character": "MARCH HARE", "text": "[playfully] Have some tea! Or perhaps some imaginary wine!"},
    {"cue": 13, "scene": "S3", "character": "ALICE", "text": "Why is this tea party so strange?"},
    {"cue": 14, "scene": "S3", "character": "MAD HATTER", "text": "Because in Wonderland, nothing makes sense!"},
    {"cue": 15, "scene": "S3", "character": "DORMOUSE", "text": "[sleepily] Please stop! I'm trying to sleep!"},
    {"cue": 16, "scene": "S3", "character": "ALICE", "text": "Don't you ever wake up?"},
    {"cue": 17, "scene": "S3", "character": "DORMOUSE", "text": "Only when someone mentions cake!"},
    {"cue": 18, "scene": "S3", "character": "MARCH HARE", "text": "[playfully] Wake up, Dormouse! It's tea time!"},
    {"cue": 19, "scene": "S3", "character": "DORMOUSE", "text": "[yawn] Oh! Then I'm wide awake!"},
    {"cue": 20, "scene": "S4", "character": "RED QUEEN", "text": "[furious] Who dares enter my garden? Off with their heads!"},
    {"cue": 21, "scene": "S4", "character": "ALICE", "text": "Why are you so angry?"},
    {"cue": 22, "scene": "S4", "character": "RED QUEEN", "text": "[roaring] How dare you question the Queen of Hearts!"},
    {"cue": 23, "scene": "S4", "character": "CARD SOLDIER", "text": "[stiffly] Yes, Your Majesty! Nobody questions the Queen of Hearts!"},
    {"cue": 24, "scene": "S4", "character": "ALICE", "text": "Do you always follow orders without thinking?"},
    {"cue": 25, "scene": "S4", "character": "CARD SOLDIER", "text": "[defensive] Well, I'm a soldier, not a thinker!"},
    {"cue": 26, "scene": "S4", "character": "RED QUEEN", "text": "[shouting] Enough talking! Seize her immediately!"},
    {"cue": 27, "scene": "S4", "character": "CARD SOLDIER", "text": "[marching] Yes, Your Majesty!"},
    {"cue": 28, "scene": "S4", "character": "ALICE", "text": "[defiant] I'm not afraid of you! You're nothing but a pack of cards!"}
]

def clean_dialogue(text):
    # Strip ElevenLabs performance tags e.g. [panicked], [amazed], etc.
    cleaned = re.sub(r'\[.*?\]', '', text).strip()
    # Normalize double spaces
    cleaned = re.sub(r'\s+', ' ', cleaned)
    return cleaned

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "json",
        str(file_path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return float(json.loads(res.stdout)["format"]["duration"])

def format_timestamp_ass(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    centis = int(round((secs - int(secs)) * 100))
    if centis >= 100:
        centis = 99
    return f"{hours}:{minutes:02d}:{int(secs):02d}.{centis:02d}"

def format_timestamp_mmss(seconds):
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes:02d}:{secs:05.2f}"

def build_timeline():
    output_dir = Path("output")
    valid_chars = {"alice", "white_rabbit", "cheshire_cat", "mad_hatter", "march_hare", "dormouse", "red_queen", "card_soldier"}
    mp3_files = [f for f in output_dir.rglob("*.mp3") if f.parent.name in valid_chars and not f.name.startswith("test_")]
    cue_map = {}
    for f in mp3_files:
        prefix = f.name[:2]
        if prefix.isdigit():
            cue_map[int(prefix)] = f

    missing = [i for i in range(1, 29) if i not in cue_map]
    if missing:
        raise RuntimeError(f"Missing cues: {missing}")

    # Group by scene
    scene_groups = {"S1": [], "S2": [], "S3": [], "S4": []}
    for item in SCRIPT_DATA:
        scene_groups[item["scene"]].append(item)

    timeline_cues = []
    scenes_meta = {}
    current_time = 0.0

    scene_names = {
        "S1": "Scene 1: Enchanted Garden & Rabbit Hole",
        "S2": "Scene 2: Twilight Wonderland Forest",
        "S3": "Scene 3: The Mad Tea Party",
        "S4": "Scene 4: The Queen of Hearts' Rose Garden"
    }

    for s_idx, (s_code, cues) in enumerate(scene_groups.items()):
        scene_start = current_time
        # Scene opening: 1.2s before first line
        current_time += 1.2

        for c_idx, cue_data in enumerate(cues):
            c_num = cue_data["cue"]
            f_path = cue_map[c_num]
            dur = get_audio_duration(f_path)
            c_start = current_time
            c_end = c_start + dur
            clean_text = clean_dialogue(cue_data["text"])
            sub_line = f"{cue_data['character']}: {clean_text}"

            current_time = c_end

            # Pacing pauses (snappy theatrical turn-taking for ~1:45 runtime)
            if c_idx < len(cues) - 1:
                pause = 0.65 if c_num == 9 else 0.35
                current_time += pause
            elif s_code == "S4":
                # Dramatic freeze after cue 28: 1.5s hold (no 'THE END' card as play continues)
                freeze_start = c_end
                current_time += 1.5
                freeze_end = current_time

            timeline_cues.append({
                "cue": c_num,
                "scene": s_code,
                "character": cue_data["character"],
                "raw_text": cue_data["text"],
                "clean_text": clean_text,
                "subtitle_text": sub_line,
                "file_path": str(f_path),
                "file_name": f_path.name,
                "start_time": c_start,
                "end_time": c_end,
                "duration": dur
            })

        scene_end = current_time
        scenes_meta[s_code] = {
            "name": scene_names[s_code],
            "start_time": scene_start,
            "end_time": scene_end,
            "duration": scene_end - scene_start
        }

        # Between scenes: 1.5s transition
        if s_code != "S4":
            current_time += 1.5

    total_runtime = current_time

    # 1. Save timeline_config.json
    config = {
        "total_runtime_sec": total_runtime,
        "scenes": scenes_meta,
        "cues": timeline_cues,
        "stage_pacing": {
            "scene_opening_lead_sec": 1.2,
            "dialogue_pause_default_sec": 0.35,
            "cue09_dormouse_pause_sec": 0.65,
            "inter_scene_transition_sec": 1.5,
            "final_freeze_sec": 1.5
        }
    }
    with open("timeline_config.json", "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)
    print("Saved timeline_config.json")

    # 2. Generate stage_subtitles.ass
    ass_lines = [
        "[Script Info]",
        "Title: Alice in Wonderland - Stage Projection Subtitles",
        "ScriptType: v4.00+",
        "PlayResX: 1920",
        "PlayResY: 1080",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        "Style: StageSafeTop,Trebuchet MS,40,&H00FFFFFF,&H000000FF,&H00000000,&H99141414,-1,0,0,0,100,100,1,0,3,10,0,8,70,70,55,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"
    ]

    for item in timeline_cues:
        start_str = format_timestamp_ass(item["start_time"])
        end_str = format_timestamp_ass(item["end_time"])
        # Format: CHARACTER NAME: Dialogue
        text_ass = item["subtitle_text"]
        ass_lines.append(f"Dialogue: 0,{start_str},{end_str},StageSafeTop,,0,0,0,,{text_ass}")

    with open("subtitles/stage_subtitles.ass", "w", encoding="utf-8") as f:
        f.write("\n".join(ass_lines))
    print("Saved subtitles/stage_subtitles.ass")

    # 3. Generate cue_sheet.txt
    cue_sheet_lines = [
        "=" * 95,
        "🎭 ALICE IN WONDERLAND - LIVE STAGE PRODUCTION CUE SHEET",
        f"Total Runtime: {format_timestamp_mmss(total_runtime)} ({total_runtime:.2f} seconds)",
        "Projection: 16:9 Widescreen (1920x1080) | Subtitles: Upper 15% Safe-Zone",
        "=" * 95,
        "",
        f"{'Cue':<6} | {'Scene':<4} | {'Start':<8} | {'End':<8} | {'Dur':<6} | {'Character':<14} | {'Clean Line':<40}",
        "-" * 95
    ]

    for c in timeline_cues:
        short_line = c["clean_text"] if len(c["clean_text"]) <= 38 else c["clean_text"][:35] + "..."
        cue_sheet_lines.append(
            f"Cue {c['cue']:02d} | {c['scene']:<4} | {format_timestamp_mmss(c['start_time']):<8} | {format_timestamp_mmss(c['end_time']):<8} | {c['duration']:<5.2f}s | {c['character']:<14} | {short_line:<40}"
        )

    cue_sheet_lines.extend([
        "-" * 95,
        "",
        "🎬 SCENE RUNTIMES & STAGE TRANSITIONS:",
        "-" * 95
    ])
    for s_code, s_info in scenes_meta.items():
        cue_sheet_lines.append(
            f"  • {s_info['name']:<50} : {format_timestamp_mmss(s_info['start_time'])} -> {format_timestamp_mmss(s_info['end_time'])} (Duration: {s_info['duration']:.2f}s)"
        )

    cue_sheet_lines.extend([
        "",
        "⏱️ STAGE PACING & TIMING RULES (~1:45 Runtime):",
        "  • Scene 1 Opening: 1.2s pre-dialogue lead-in with Meadow visuals & Pocket Watch ticking.",
        "  • Scene 2 Opening: 1.2s pre-dialogue lead-in with Twilight Forest ambiance.",
        "  • Scene 3 Opening: 1.2s pre-dialogue lead-in with Mad Tea Party whimsical waltz.",
        "  • Scene 4 Opening: 1.2s Royal Trumpet Fanfare before Cue 20.",
        "  • Dialogue Pacing : 0.35s turn-taking pause (0.65s after Cue 09 Dormouse singing).",
        "  • Scene Changes   : 1.5s smooth crossfade transition between scenes.",
        "  • Dramatic Freeze : 1.5s freeze hold after Cue 28 (scene fades out cleanly; play continues, no 'THE END' card).",
        "=" * 95
    ])

    with open("cue_sheet.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(cue_sheet_lines))
    print("Saved cue_sheet.txt")

    return config

if __name__ == "__main__":
    build_timeline()
