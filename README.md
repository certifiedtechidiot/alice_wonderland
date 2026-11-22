# Alice in Wonderland - ElevenLabs Voiceover Generator

Automated voiceover generation pipeline using the official ElevenLabs Python SDK (`elevenlabs`), targeting the high-expressivity `eleven_v3` model with rich emotive and performance tags.

## Project Structure

```text
├── .env                    # ElevenLabs API Key (git-ignored)
├── .gitignore              # Ignores .env, output/, __pycache__/
├── generate_audio.py       # Main generation script with voice resolution & dry-run
├── requirements.txt        # Python dependencies (elevenlabs, python-dotenv)
├── README.md               # Documentation and execution instructions
└── output/                 # Generated audio & script lines per character
    ├── alice/
    │   ├── lines.txt
    │   └── [cue_scene_alice.mp3]
    ├── white_rabbit/
    │   ├── lines.txt
    │   └── [cue_scene_white_rabbit.mp3]
    ├── cheshire_cat/
    │   ├── lines.txt
    │   └── [cue_scene_cheshire_cat.mp3]
    ├── mad_hatter/
    ├── march_hare/
    ├── dormouse/
    ├── red_queen/
    └── card_soldier/
```

## Features
- **Dynamic Voice Resolution:** Queries `client.voices.get_all()` from the authenticated account and dynamically matches character voices (primary target -> fallback target -> closest curated account fallback).
- **Credit-Safe Execution:**
  - Includes `--dry-run` to test voice resolution, verify cues, and generate folders/lines without consuming credits.
  - Skips already generated files on disk to avoid wasting credits on re-runs.
- **Model & Audio Specs:**
  - Model: `eleven_v3`
  - Output Format: `mp3_44100_128`
  - Retains all Eleven v3 bracketed performance tags (`[panicked]`, `[amazed]`, `[mischievously]`, etc.).

## Voice Allocation Summary

| Character | Target Voice | Fallback | Account Status | Assigned Voice |
| :--- | :--- | :--- | :--- | :--- |
| **alice** | Amelia | Jade | Fallback assigned | **Alice** - Clear, Engaging Educator |
| **white_rabbit** | Lawrence | Archer | Fallback assigned | **Charlie** - Deep, Confident, Energetic |
| **cheshire_cat** | Callum | Edward | **Matched Primary** | **Callum** - Husky Trickster |
| **mad_hatter** | Eldrin | — | Fallback assigned | **George** - Warm, Captivating Storyteller |
| **march_hare** | Kaelen | Lucan | Fallback assigned | **Will** - Relaxed Optimist |
| **dormouse** | Talia | — | Fallback assigned | **Lily** - Velvety Actress |
| **red_queen** | Florence | Elara | Fallback assigned | **Sarah** - Mature, Reassuring, Confident |
| **card_soldier** | Darian | Wyatt | Fallback assigned | **Adam** - Dominant, Firm |

## Usage Commands

### 1. Dry Run (No credits spent)
```bash
python generate_audio.py --dry-run
```

### 2. Full Audio Generation
```bash
python generate_audio.py
```

### 3. Voice Overrides (Optional)
If you prefer a different voice from your account for any character:
```bash
python generate_audio.py --voice-override red_queen=Bella --voice-override white_rabbit=Liam
```

### 4. Single Character or Cue
```bash
python generate_audio.py --character alice
python generate_audio.py --cue 4
```

### 5. Force Re-generation
```bash
python generate_audio.py --force
```
