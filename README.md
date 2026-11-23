# 🎭 Alice in Wonderland - Theatrical Projection & Audio Production Pipeline

Automated scenic video, ambient audio, and dialogue assembly pipeline for a live school stage play of **"Alice in Wonderland."**

Built for live theater projection with student actors performing in front of a 16:9 widescreen projector screen.

---

## 📌 Context & Critical Stage Rules

1. **Live Actors on Stage:** Students perform live on stage in front of the screen.
2. **STRICTLY NO CHARACTERS ON SCREEN:** All visuals are purely scenic, atmospheric, empty storybook environments. Zero characters, animals, or creatures appear on screen.
3. **Stage-Safe Subtitles (Upper 15% Safe-Zone):** Subtitles are locked to the top 12%–15% of the screen with a high-contrast dark semi-transparent banner and bold white text (`Trebuchet MS Bold`). This guarantees that student actors standing or moving on stage never occlude the audience's view of the text.
4. **Play Pacing (~1:45 Runtime):** Calibrated for crisp theatrical pacing (~105 seconds). The "THE END" outro card has been excluded so the visual transitions seamlessly into the subsequent live scenes of the play.

---

## 🎬 Scene Breakdown & Timings

Total Show Runtime: **01:42.90** (102.90 seconds)

| Scene | Name & Visual Setting | Ambient Audio / SFX | Timeline Range |
| :--- | :--- | :--- | :--- |
| **Scene 1** | **Enchanted Garden & Rabbit Hole**<br>Sunlit English meadow with oversized flowers, stone path, and dark rabbit hole burrow under an ancient hollow oak. | Curious pastoral woodwinds + ticking pocket watch SFX (`120 BPM`). | `00:00.00` – `00:17.26` |
| **Transition 1** | *Stage clearance & entrance transition* | Smooth audio & video crossfade. | `00:17.26` – `00:18.76` (1.5s) |
| **Scene 2** | **Twilight Wonderland Forest**<br>Deep mystical woods at dusk with bioluminescent teal/purple mushrooms and wooden directional signposts. | Ethereal glassy pads, playful chimes & pizzicato strings. | `00:18.76` – `00:35.12` |
| **Transition 2** | *Stage clearance & entrance transition* | Smooth audio & video crossfade. | `00:35.12` – `00:36.62` (1.5s) |
| **Scene 3** | **The Mad Tea Party**<br>Woodland glade under hanging fairy lanterns. Long banquet table stacked with teacups, teapots, top hats, and cakes—all chairs completely empty. | Quirky, upbeat offbeat tea party waltz (3/4 time) + porcelain clink SFX. | `00:36.62` – `01:11.46` |
| **Transition 3** | *Stage clearance & entrance transition* | Smooth audio & video crossfade. | `01:11.46` – `01:12.96` (1.5s) |
| **Scene 4** | **The Queen of Hearts' Rose Garden**<br>Checkered crimson-and-white marble courtyard, towering hedge maze, half-painted dripping white roses, and crimson palace gates. | Royal trumpet fanfare (first 1.2s), followed by tense military strings & timpani. | `01:12.96` – `01:42.86` |
| **Dramatic Freeze** | *Queen stamps feet / Soldier steps forward / Alice freeze* | Complete dead silence cutoff after Cue 28 for the freeze hold, then gentle fade out. | `01:41.36` – `01:42.86` (1.5s) |

---

## 🎙️ Character Voice Casting (ElevenLabs eleven_v3)

All voiceovers are generated via ElevenLabs targeting the high-expressivity `eleven_v3` model with bracketed performance tags:

| Character | ElevenLabs Voice ID | Voice Name & Style | Notes |
| :--- | :--- | :--- | :--- |
| **Alice** | `cgSgspJ2msm6clMCkdW9` | **Jessica** - Playful, Bright, Warm | Switched to young, natural, conversational voice (non-robotic). |
| **White Rabbit** | `IKne3meq5aSn9XLyUdCD` | **Charlie** - Deep, Confident, Energetic | Panicked, rushed delivery. |
| **Cheshire Cat** | `FGY2WhTYpPnrIDTdsKH5` | **Laura** - Enthusiast, Quirky Attitude | Female, sassy, mischievous, chuckling delivery. |
| **Mad Hatter** | `JBFqnCBsd6RMkjVDRZzb` | **George** - Warm Storyteller | Playful, eccentric theatrical cadence. |
| **March Hare** | `bIHbv24MWmeRgasZH58o` | **Will** - Relaxed Optimist | Bouncy, offbeat party host. |
| **Dormouse** | `pFZP5JQG7iQjIQuC4Bku` | **Lily** - Velvety Actress | Soft, sleepy, singing cadence. |
| **Red Queen** | `EXAVITQu4vr4xnSDxMaL` | **Sarah** - Mature, Confident | Bold, booming, commanding royal voice. |
| **Card Soldier** | `pNInz6obpgDQGcFmaJgB` | **Adam** - Dominant, Firm | Stiff military cadence. |

---

## 📜 Full 28 Cues Schedule

```text
Cue 01 | S1 | 00:01.20 -> 00:03.68 (2.48s) | WHITE RABBIT : Oh, dear! Oh, dear! I shall be too late!
Cue 02 | S1 | 00:04.03 -> 00:14.19 (10.16s)| ALICE        : A rabbit wearing a waistcoat and carrying a watch? How curious! Oh wait! Mr. Rabbit! Where are you going? What's the hurry?
Cue 03 | S1 | 00:14.54 -> 00:17.26 (2.72s) | WHITE RABBIT : The Queen will be furious if I don't reach the palace!
Cue 04 | S2 | 00:19.96 -> 00:24.20 (4.24s) | CHESHIRE CAT : Welcome to Wonderland, little girl! Looking for someone?
Cue 05 | S2 | 00:24.55 -> 00:26.15 (1.60s) | ALICE        : I'm looking for my way home.
Cue 06 | S2 | 00:26.50 -> 00:32.58 (6.08s) | CHESHIRE CAT : That depends on where you want to go! We're all mad here!
Cue 07 | S2 | 00:32.93 -> 00:35.33 (2.40s) | ALICE        : Everybody seems so strange here!
Cue 08 | S2 | 00:35.68 -> 00:38.00 (2.32s) | CHESHIRE CAT : Follow the music to the tea party!
Cue 09 | S3 | 00:40.70 -> 00:43.50 (2.80s) | DORMOUSE     : Twinkle, twinkle, little bat...
Cue 10 | S3 | 00:44.15 -> 00:47.51 (3.36s) | MAD HATTER   : No room! No room! Welcome to our tea party!
Cue 11 | S3 | 00:47.86 -> 00:49.46 (1.60s) | ALICE        : But there's plenty of room!
Cue 12 | S3 | 00:49.81 -> 00:53.57 (3.76s) | MARCH HARE   : Have some tea! Or perhaps some imaginary wine!
Cue 13 | S3 | 00:53.92 -> 00:56.24 (2.32s) | ALICE        : Why is this tea party so strange?
Cue 14 | S3 | 00:56.59 -> 00:59.79 (3.20s) | MAD HATTER   : Because in Wonderland, nothing makes sense!
Cue 15 | S3 | 01:00.14 -> 01:04.30 (4.16s) | DORMOUSE     : Please stop! I'm trying to sleep!
Cue 16 | S3 | 01:04.65 -> 01:06.09 (1.44s) | ALICE        : Don't you ever wake up?
Cue 17 | S3 | 01:06.44 -> 01:09.32 (2.88s) | DORMOUSE     : Only when someone mentions cake!
Cue 18 | S3 | 01:09.67 -> 01:11.75 (2.08s) | MARCH HARE   : Wake up, Dormouse! It's tea time!
Cue 19 | S3 | 01:12.10 -> 01:14.34 (2.24s) | DORMOUSE     : Oh! Then I'm wide awake!
Cue 20 | S4 | 01:17.04 -> 01:20.88 (3.84s) | RED QUEEN    : Who dares enter my garden? Off with their heads!
Cue 21 | S4 | 01:21.23 -> 01:22.59 (1.36s) | ALICE        : Why are you so angry?
Cue 22 | S4 | 01:22.94 -> 01:25.34 (2.40s) | RED QUEEN    : How dare you question the Queen of Hearts!
Cue 23 | S4 | 01:25.69 -> 01:29.61 (3.92s) | CARD SOLDIER : Yes, Your Majesty! Nobody questions the Queen of Hearts!
Cue 24 | S4 | 01:29.96 -> 01:32.52 (2.56s) | ALICE        : Do you always follow orders without thinking?
Cue 25 | S4 | 01:32.87 -> 01:35.03 (2.16s) | CARD SOLDIER : Well, I'm a soldier, not a thinker!
Cue 26 | S4 | 01:35.38 -> 01:38.02 (2.64s) | RED QUEEN    : Enough talking! Seize her immediately!
Cue 27 | S4 | 01:38.37 -> 01:39.89 (1.52s) | CARD SOLDIER : Yes, Your Majesty!
Cue 28 | S4 | 01:40.24 -> 01:44.24 (4.00s) | ALICE        : I'm not afraid of you! You're nothing but a pack of cards!
```

---

## 🛠️ Project Directory Structure

```text
├── assets/
│   ├── audio/                      # Master BGM & SFX stems (-22 dB RMS)
│   │   ├── bgm_scene1.mp3
│   │   ├── bgm_scene2.mp3
│   │   ├── bgm_scene3.mp3
│   │   └── bgm_scene4.mp3
│   ├── backgrounds/                # 1080p seamless ambient video loops
│   │   ├── bg_scene1.mp4
│   │   ├── bg_scene2.mp4
│   │   ├── bg_scene3.mp4
│   │   └── bg_scene4.mp4
│   ├── images/                     # 16:9 scenic background base plates
│   │   ├── scene1_meadow.jpg
│   │   ├── scene2_forest.jpg
│   │   ├── scene3_teaparty.jpg
│   │   └── scene4_rosegarden.png
│   └── backups/                    # Original voice backups
├── output/                         # 28 ElevenLabs dialogue MP3s (organized by character)
│   ├── alice/
│   ├── card_soldier/
│   ├── cheshire_cat/
│   ├── dormouse/
│   ├── mad_hatter/
│   ├── march_hare/
│   ├── red_queen/
│   └── white_rabbit/
├── scripts/
│   ├── build_timeline.py           # Calculates timestamps, exports timeline_config & cue_sheet
│   ├── generate_audio_bgm.py       # Algorithmic synthesis for all 4 orchestral BGM stems
│   ├── generate_background_loops.py# OpenCV particle engine for seamless loop generation
│   └── render_scene4_and_outro.py  # Playwright renderer for Scene 4 rose garden
├── subtitles/
│   └── stage_subtitles.ass         # Top-aligned (upper 15%) stage subtitles
├── cue_sheet.txt                   # Human-readable stage manager timing sheet
├── timeline_config.json            # Master timeline JSON
├── generate_audio.py               # ElevenLabs voice generation script
├── merge_production.py             # Single-command production compiler
├── final_alice_in_wonderland_stage.mp4 # Full rendered 1080p show video (01:45.80)
├── requirements.txt                # Python dependencies
└── README.md                       # Documentation & instructions
```

---

## 🚀 Execution & Editing Guide

### 1. Re-Generate or Override Voices
To change any character's voice:
```bash
# Example: Change Alice's voice or force re-generation
python generate_audio.py --character alice --voice-override alice=Jessica --force

# Dry-run test without spending ElevenLabs credits:
python generate_audio.py --dry-run
```

### 2. Re-Assemble the Show Video
To re-calculate durations and compile the final video:
```bash
python merge_production.py
```
This automatically:
1. Measures every audio file with `ffprobe`.
2. Updates `timeline_config.json`, `cue_sheet.txt`, and `stage_subtitles.ass`.
3. Normalizes all dialogue clips to consistent `-15.0 dB RMS`.
4. Loops and trims scenic backdrops to fit each scene exactly.
5. Ducks BGM underneath dialogue (`-6 dB`) with smooth envelopes.
6. Burns top-aligned safe-zone subtitles and exports `final_alice_in_wonderland_stage.mp4`.
