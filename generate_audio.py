"""
Alice in Wonderland - Voiceover Audio Generation Script
Using ElevenLabs Python SDK with eleven_v3 model and performance tags.
"""

import os
import sys
import argparse
import difflib
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables from .env
dotenv.load_dotenv()

# Script dialogue dataset
SCRIPT_DATA: List[Dict[str, Any]] = [
    {
        "cue": 1,
        "scene": "S1",
        "character": "white_rabbit",
        "text": "[panicked] Oh, dear! Oh, dear! I shall be too late!",
    },
    {
        "cue": 2,
        "scene": "S1",
        "character": "alice",
        "text": "[amazed] A rabbit wearing a waistcoat and carrying a watch? How curious! [excitedly] Oh wait! Mr Rabbit! Where are you going! What's the hurry?",
    },
    {
        "cue": 3,
        "scene": "S1",
        "character": "white_rabbit",
        "text": "[rushed] The Queen will be furious if I don't reach the palace!",
    },
    {
        "cue": 4,
        "scene": "S2",
        "character": "cheshire_cat",
        "text": "[mischievously] Welcome to Wonderland, little girl! Looking for someone?",
    },
    {
        "cue": 5,
        "scene": "S2",
        "character": "alice",
        "text": "I'm looking for my way home.",
    },
    {
        "cue": 6,
        "scene": "S2",
        "character": "cheshire_cat",
        "text": "[chuckles] That depends on where you want to go! [mischievously] We're all mad here!",
    },
    {
        "cue": 7,
        "scene": "S2",
        "character": "alice",
        "text": "Everybody seems so strange here!",
    },
    {
        "cue": 8,
        "scene": "S2",
        "character": "cheshire_cat",
        "text": "[playfully] Follow the music to the tea party!",
    },
    {
        "cue": 9,
        "scene": "S3",
        "character": "dormouse",
        "text": "[sings] Twinkle twinkle little bat...",
    },
    {
        "cue": 10,
        "scene": "S3",
        "character": "mad_hatter",
        "text": "[excitedly] No room! No room! [playfully] Welcome to our tea party!",
    },
    {
        "cue": 11,
        "scene": "S3",
        "character": "alice",
        "text": "But there's plenty of room!",
    },
    {
        "cue": 12,
        "scene": "S3",
        "character": "march_hare",
        "text": "[playfully] Have some tea! Or perhaps some imaginary wine!",
    },
    {
        "cue": 13,
        "scene": "S3",
        "character": "alice",
        "text": "Why is this tea party so strange?",
    },
    {
        "cue": 14,
        "scene": "S3",
        "character": "mad_hatter",
        "text": "[laughs] Because in Wonderland, nothing makes sense!",
    },
    {
        "cue": 15,
        "scene": "S3",
        "character": "dormouse",
        "text": "[yawning] Please stop! [whispers] I'm trying to sleep!",
    },
    {
        "cue": 16,
        "scene": "S3",
        "character": "alice",
        "text": "Don't you ever wake up?",
    },
    {
        "cue": 17,
        "scene": "S3",
        "character": "dormouse",
        "text": "[sleepily] Only when someone mentions cake!",
    },
    {
        "cue": 18,
        "scene": "S3",
        "character": "march_hare",
        "text": "[excitedly] Wake up, Dormouse! It's tea time!",
    },
    {
        "cue": 19,
        "scene": "S3",
        "character": "dormouse",
        "text": "[excitedly] Oh! Then I'm wide awake!",
    },
    {
        "cue": 20,
        "scene": "S4",
        "character": "red_queen",
        "text": "[furiously] Who dares enter my garden? [shouting] Off with their heads!",
    },
    {
        "cue": 21,
        "scene": "S4",
        "character": "alice",
        "text": "Why are you so angry?",
    },
    {
        "cue": 22,
        "scene": "S4",
        "character": "red_queen",
        "text": "[furiously] How dare you question the Queen of Hearts!",
    },
    {
        "cue": 23,
        "scene": "S4",
        "character": "card_soldier",
        "text": "[stiffly] Yes, Your Majesty! Nobody questions the Queen of Hearts!",
    },
    {
        "cue": 24,
        "scene": "S4",
        "character": "alice",
        "text": "Do you always follow orders without thinking?",
    },
    {
        "cue": 25,
        "scene": "S4",
        "character": "card_soldier",
        "text": "[matter-of-factly] Well, I'm a soldier, not a thinker!",
    },
    {
        "cue": 26,
        "scene": "S4",
        "character": "red_queen",
        "text": "[shouting] Enough talking! Seize her immediately!",
    },
    {
        "cue": 27,
        "scene": "S4",
        "character": "card_soldier",
        "text": "[stiffly] Yes, Your Majesty!",
    },
    {
        "cue": 28,
        "scene": "S4",
        "character": "alice",
        "text": "[firmly] I'm not afraid of you! You're nothing but a pack of cards!",
    },
]

# Character Voice Specifications
TARGET_VOICES = {
    "alice": {
        "target": "Amelia",
        "fallback": "Jade",
        "closest_default": "Alice",
        "role": "Curious, adventurous young girl",
    },
    "white_rabbit": {
        "target": "Lawrence",
        "fallback": "Archer",
        "closest_default": "Charlie",
        "role": "Anxious, hurried, fast-talking rabbit",
    },
    "cheshire_cat": {
        "target": "Laura",
        "fallback": "Jessica",
        "closest_default": "Laura",
        "role": "Mischievous, sassy grinning female trickster",
    },
    "mad_hatter": {
        "target": "Eldrin",
        "fallback": None,
        "closest_default": "George",
        "role": "Eccentric, playful, theatrical host",
    },
    "march_hare": {
        "target": "Kaelen",
        "fallback": "Lucan",
        "closest_default": "Will",
        "role": "Zany, energetic tea companion",
    },
    "dormouse": {
        "target": "Talia",
        "fallback": None,
        "closest_default": "Lily",
        "role": "Sleepy, tiny, sweet-voiced mouse",
    },
    "red_queen": {
        "target": "Florence",
        "fallback": "Elara",
        "closest_default": "Sarah",
        "role": "Fierce, imperious, commanding queen",
    },
    "card_soldier": {
        "target": "Darian",
        "fallback": "Wyatt",
        "closest_default": "Adam",
        "role": "Stiff, obedient royal guard",
    },
}


def find_voice(target_name: str, available_voices: list) -> Optional[Any]:
    """Search for voice matching target_name (case-insensitive substring match)."""
    target_clean = target_name.strip().lower()
    for v in available_voices:
        v_name = v.name.lower()
        if target_clean in v_name:
            return v
    return None


def resolve_character_voices(
    client: ElevenLabs, overrides: Optional[Dict[str, str]] = None
) -> Tuple[Dict[str, Any], List[str]]:
    """
    Fetch all voices in the account and match them to target characters.
    Returns (resolved_mapping, warnings).
    """
    if overrides is None:
        overrides = {}

    print("\n🔍 Fetching available voices from your ElevenLabs account...")
    voices_response = client.voices.get_all()
    available_voices = voices_response.voices
    print(f"   Found {len(available_voices)} voices in your account.\n")

    # Build quick lookup by name/id
    voice_names = [v.name.split(" - ")[0].strip() for v in available_voices]

    resolved = {}
    warnings = []

    for char, spec in TARGET_VOICES.items():
        # 0. Check CLI override first
        if char in overrides:
            override_val = overrides[char].strip().lower()
            matched = None
            for v in available_voices:
                if override_val in v.name.lower() or override_val == v.voice_id.lower():
                    matched = v
                    break
            if matched:
                resolved[char] = {
                    "voice": matched,
                    "status": f"CLI Override ({overrides[char]})",
                    "status_code": "OVERRIDE",
                }
                continue
            else:
                warnings.append(
                    f"CLI override '{overrides[char]}' for '{char}' not found in account voices!"
                )

        target = spec["target"]
        fallback = spec["fallback"]
        closest_default = spec.get("closest_default")

        # 1. Match primary target
        matched_voice = find_voice(target, available_voices)
        if matched_voice:
            resolved[char] = {
                "voice": matched_voice,
                "status": f"Matched Primary ('{target}')",
                "status_code": "PRIMARY",
            }
            continue

        # 2. Match secondary fallback if defined
        if fallback:
            matched_voice = find_voice(fallback, available_voices)
            if matched_voice:
                resolved[char] = {
                    "voice": matched_voice,
                    "status": f"Matched Fallback ('{fallback}')",
                    "status_code": "FALLBACK",
                }
                warnings.append(
                    f"'{char}': Primary target '{target}' not found. Using fallback '{fallback}' -> '{matched_voice.name}'"
                )
                continue

        # 3. Not found: Look for curated closest account voice or string similarity
        selected_fallback = None
        if closest_default:
            selected_fallback = find_voice(closest_default, available_voices)

        if not selected_fallback:
            # Algorithmic fallback using difflib
            close = difflib.get_close_matches(target, voice_names, n=1, cutoff=0.1)
            if close:
                selected_fallback = find_voice(close[0], available_voices)

        if not selected_fallback and available_voices:
            selected_fallback = available_voices[0]

        fb_name = selected_fallback.name if selected_fallback else "None"
        msg = (
            f"'{char}': Target '{target}'"
            + (f" and fallback '{fallback}'" if fallback else "")
            + f" not found in account. Fell back to closest available voice: '{fb_name}'"
        )
        warnings.append(msg)

        resolved[char] = {
            "voice": selected_fallback,
            "status": f"Auto-Assigned Fallback ('{fb_name.split(' - ')[0]}')",
            "status_code": "AUTO_FALLBACK",
        }

    return resolved, warnings


def print_available_voices(client: ElevenLabs) -> None:
    """Print all available voices in the account."""
    voices_response = client.voices.get_all()
    print("=" * 80)
    print("AVAILABLE VOICES IN YOUR ACCOUNT:")
    print("=" * 80)
    for idx, v in enumerate(voices_response.voices, 1):
        print(f" {idx:2d}. {v.name:<45} (ID: {v.voice_id})")
    print("=" * 80 + "\n")


def setup_character_directories(
    output_dir: Path, script_data: List[Dict[str, Any]]
) -> Dict[str, Path]:
    """
    Create output directory and character subfolders.
    Populate lines.txt in each subfolder.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    characters = sorted(list({item["character"] for item in script_data}))

    char_dirs = {}
    for char in characters:
        char_dir = output_dir / char
        char_dir.mkdir(parents=True, exist_ok=True)
        char_dirs[char] = char_dir

        # Generate lines.txt for this character
        char_lines = [item for item in script_data if item["character"] == char]
        lines_file = char_dir / "lines.txt"

        lines_content = []
        lines_content.append(f"# Script lines for character: {char.upper()}")
        lines_content.append(f"# Total lines: {len(char_lines)}\n")
        for line in char_lines:
            lines_content.append(
                f"Cue {line['cue']:02d} | {line['scene']} | {line['text']}"
            )

        with open(lines_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines_content) + "\n")

    return char_dirs


def main():
    parser = argparse.ArgumentParser(
        description="Generate ElevenLabs voiceovers for Alice in Wonderland."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Test voice resolution, folder creation, and line counting without calling ElevenLabs TTS API.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing MP3 files instead of skipping them.",
    )
    parser.add_argument(
        "--character",
        type=str,
        default=None,
        help="Generate audio only for a specific character (e.g. 'alice', 'cheshire_cat').",
    )
    parser.add_argument(
        "--cue",
        type=int,
        default=None,
        help="Generate audio only for a specific cue number (e.g. 1).",
    )
    parser.add_argument(
        "--voice-override",
        action="append",
        help="Override a character voice mapping (format: character=voice_name, e.g. --voice-override red_queen=Bella)",
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="List all voices in the ElevenLabs account and exit.",
    )
    args = parser.parse_args()

    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ Error: ELEVENLABS_API_KEY is not set in environment or .env file.")
        sys.exit(1)

    client = ElevenLabs(api_key=api_key)

    if args.list_voices:
        print_available_voices(client)
        sys.exit(0)

    # Process voice overrides
    overrides = {}
    if args.voice_override:
        for item in args.voice_override:
            if "=" in item:
                k, v = item.split("=", 1)
                overrides[k.strip().lower()] = v.strip()

    print("=" * 80)
    print("🎭 ALICE IN WONDERLAND - VOICEOVER GENERATOR (ElevenLabs eleven_v3)")
    print("=" * 80)
    if args.dry_run:
        print("🔹 RUNNING IN DRY-RUN MODE: No ElevenLabs audio credits will be used!")
    print(f"Model ID      : eleven_v3")
    print(f"Output Format : mp3_44100_128")
    print(f"Total Cues    : {len(SCRIPT_DATA)}")

    # 1. Voice Resolution
    resolved_voices, warnings = resolve_character_voices(client, overrides)

    # Print warnings if any
    if warnings:
        print("⚠️  VOICE RESOLUTION NOTICES / WARNINGS:")
        print("-" * 80)
        for w in warnings:
            print(f"  • {w}")
        print("-" * 80 + "\n")

    # 2. Display Character Voice Resolution Table
    print("📋 CHARACTER VOICE RESOLUTION TABLE:")
    print(
        f"{'Character':<15} | {'Target (Fallback)':<24} | {'Status':<22} | {'Assigned Voice':<30}"
    )
    print("-" * 98)
    for char, data in resolved_voices.items():
        spec = TARGET_VOICES[char]
        target_str = f"{spec['target']} ({spec['fallback'] or 'None'})"
        voice_name = data["voice"].name if data["voice"] else "NONE"
        status_str = data["status"]
        print(f"{char:<15} | {target_str:<24} | {status_str:<22} | {voice_name:<30}")
    print("-" * 98 + "\n")

    # 3. Setup Folders and lines.txt
    output_dir = Path("output")
    char_dirs = setup_character_directories(output_dir, SCRIPT_DATA)
    print(f"📁 Output directories and lines.txt generated in: {output_dir.resolve()}/")
    for char, path in char_dirs.items():
        print(f"   ✓ {path.name}/ (lines.txt created)")
    print()

    # 4. Filter cues if requested
    cues_to_process = SCRIPT_DATA
    if args.character:
        char_filter = args.character.lower()
        cues_to_process = [c for c in cues_to_process if c["character"] == char_filter]
        if not cues_to_process:
            print(f"❌ No cues found for character: {args.character}")
            sys.exit(1)

    if args.cue:
        cues_to_process = [c for c in cues_to_process if c["cue"] == args.cue]
        if not cues_to_process:
            print(f"❌ No cue found with number: {args.cue}")
            sys.exit(1)

    print(f"🎬 Processing {len(cues_to_process)} cue(s):")
    print("=" * 80)

    generated_count = 0
    skipped_count = 0

    for item in cues_to_process:
        cue_num = item["cue"]
        scene = item["scene"]
        char = item["character"]
        text = item["text"]

        voice_info = resolved_voices.get(char)
        if not voice_info or not voice_info["voice"]:
            print(f"❌ Cue {cue_num:02d} | No voice assigned for {char}. Skipping.")
            continue

        voice = voice_info["voice"]
        voice_id = voice.voice_id
        voice_name = voice.name.split(" - ")[0]

        char_dir = char_dirs[char]
        filename = f"{cue_num:02d}_{scene}_{char}.mp3"
        dest_file = char_dir / filename

        # Preview line text (truncated if long)
        preview_text = text if len(text) <= 55 else text[:52] + "..."

        if dest_file.exists() and not args.force:
            print(
                f"⏭️  Cue {cue_num:02d} [{scene}] {char:<13} -> {filename:<25} [ALREADY EXISTS - SKIPPED]"
            )
            skipped_count += 1
            continue

        if args.dry_run:
            print(
                f"🧪 Cue {cue_num:02d} [{scene}] {char:<13} -> {filename:<25} (Voice: {voice_name:<8}) \"{preview_text}\""
            )
            generated_count += 1
            continue

        # Actual Generation
        print(
            f"🎙️  Cue {cue_num:02d} [{scene}] Generating for {char} using '{voice_name}'...",
            end=" ",
            flush=True,
        )
        try:
            audio_stream = client.text_to_speech.convert(
                voice_id=voice_id,
                text=text,
                model_id="eleven_v3",
                output_format="mp3_44100_128",
            )
            with open(dest_file, "wb") as f:
                for chunk in audio_stream:
                    if chunk:
                        f.write(chunk)
            print("✓ Saved")
            generated_count += 1
        except Exception as e:
            print(f"❌ FAILED: {e}")

    print("=" * 80)
    print("📊 SUMMARY:")
    if args.dry_run:
        print(f"  • Mode: DRY RUN (0 API credits used)")
        print(f"  • Cues verified: {generated_count}")
        print(f"  • Output folders ready: {len(char_dirs)}")
        print(f"  • All character lines.txt created successfully.")
    else:
        print(f"  • Total Generated: {generated_count}")
        print(f"  • Total Skipped:   {skipped_count}")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
