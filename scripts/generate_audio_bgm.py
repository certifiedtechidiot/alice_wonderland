import numpy as np
import scipy.io.wavfile as wavfile
import subprocess
from pathlib import Path

SAMPLE_RATE = 44100

def envelope(n_samples, attack=0.01, decay=0.1, sustain=0.7, release=0.2):
    att_samples = int(attack * SAMPLE_RATE)
    dec_samples = int(decay * SAMPLE_RATE)
    rel_samples = int(release * SAMPLE_RATE)
    sus_samples = max(0, n_samples - att_samples - dec_samples - rel_samples)

    env = []
    if att_samples > 0:
        env.append(np.linspace(0, 1, att_samples))
    if dec_samples > 0:
        env.append(np.linspace(1, sustain, dec_samples))
    if sus_samples > 0:
        env.append(np.full(sus_samples, sustain))
    if rel_samples > 0:
        env.append(np.linspace(sustain, 0, rel_samples))
    
    res = np.concatenate(env) if env else np.ones(n_samples)
    if len(res) < n_samples:
        res = np.pad(res, (0, n_samples - len(res)))
    return res[:n_samples]

def synth_bell(freq, duration, gain=0.2):
    # Celesta / Chime / Bell tone (inharmonic partials)
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-t * (4.0 / max(0.2, duration)))
    # Harmonic & inharmonic overtones
    signal = (
        np.sin(2 * np.pi * freq * t) +
        0.5 * np.sin(2 * np.pi * freq * 2.76 * t) +
        0.3 * np.sin(2 * np.pi * freq * 4.07 * t) +
        0.15 * np.sin(2 * np.pi * freq * 5.4 * t)
    ) * env * gain
    return signal

def synth_pizzicato(freq, duration, gain=0.25):
    # Plucked string pizzicato
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    env = np.exp(-t * 9.0)
    signal = (
        np.sin(2 * np.pi * freq * t) +
        0.6 * np.sin(2 * np.pi * freq * 2 * t) +
        0.3 * np.sin(2 * np.pi * freq * 3 * t) +
        0.1 * np.sin(2 * np.pi * freq * 4 * t)
    ) * env * gain
    return signal

def synth_flute(freq, duration, gain=0.2):
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    env = envelope(n, attack=0.08, decay=0.1, sustain=0.8, release=0.15)
    # Vibrato
    vib = 1.0 + 0.008 * np.sin(2 * np.pi * 5.5 * t)
    signal = (
        np.sin(2 * np.pi * freq * vib * t) +
        0.2 * np.sin(2 * np.pi * freq * 2 * vib * t) +
        0.05 * np.sin(2 * np.pi * freq * 3 * vib * t)
    ) * env * gain
    return signal

def synth_brass(freq, duration, gain=0.3):
    # Herald trumpet fanfare with brassy harmonics
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    env = envelope(n, attack=0.04, decay=0.08, sustain=0.85, release=0.12)
    signal = (
        np.sin(2 * np.pi * freq * t) +
        0.8 * np.sin(2 * np.pi * freq * 2 * t) +
        0.6 * np.sin(2 * np.pi * freq * 3 * t) +
        0.4 * np.sin(2 * np.pi * freq * 4 * t) +
        0.25 * np.sin(2 * np.pi * freq * 5 * t)
    ) * env * gain
    return signal

def synth_timpani(duration, gain=0.35):
    n = int(duration * SAMPLE_RATE)
    t = np.linspace(0, duration, n, endpoint=False)
    pitch_env = 95.0 * np.exp(-t * 8.0) + 48.0
    phase = 2 * np.pi * np.cumsum(pitch_env) / SAMPLE_RATE
    amp_env = np.exp(-t * 3.5)
    signal = (np.sin(phase) + 0.3 * np.sin(phase * 1.5)) * amp_env * gain
    return signal

def add_tone(track, tone, start_time, pan=0.0):
    start_idx = int(start_time * SAMPLE_RATE)
    if start_idx >= len(track):
        return
    end_idx = min(len(track), start_idx + len(tone))
    actual_len = end_idx - start_idx
    if actual_len <= 0:
        return
    tone = tone[:actual_len]
    left_gain = np.sqrt(0.5 * (1.0 - pan))
    right_gain = np.sqrt(0.5 * (1.0 + pan))
    track[start_idx:end_idx, 0] += tone * left_gain
    track[start_idx:end_idx, 1] += tone * right_gain

def normalize_and_export(track, wav_path, mp3_path, target_rms_db=-22.0):
    # Measure RMS
    rms = np.sqrt(np.mean(track ** 2) + 1e-12)
    current_db = 20 * np.log10(rms)
    gain = 10 ** ((target_rms_db - current_db) / 20.0)
    normalized = np.clip(track * gain, -0.98, 0.98)
    
    # Save 16-bit WAV
    wav_data = (normalized * 32767).astype(np.int16)
    wavfile.write(str(wav_path), SAMPLE_RATE, wav_data)

    # Convert to MP3 using FFmpeg
    cmd = [
        "ffmpeg", "-y",
        "-i", str(wav_path),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    wav_path.unlink(missing_ok=True)
    print(f"Exported {mp3_path.name} (target {target_rms_db} dB RMS)")

# -------------------------------------------------------------
# 1. SCENE 1 BGM & SFX: Light curious orchestral + pocket watch
# -------------------------------------------------------------
def build_bgm_scene1(total_sec=25.0):
    n_samples = int(total_sec * SAMPLE_RATE)
    track = np.zeros((n_samples, 2), dtype=np.float32)

    # Pocket Watch Ticking (every 0.5s = 120 ticks/min)
    tick_tone = np.exp(-np.linspace(0, 0.03, int(0.03 * SAMPLE_RATE)) * 250) * np.sin(2 * np.pi * 3200 * np.linspace(0, 0.03, int(0.03 * SAMPLE_RATE))) * 0.18
    tock_tone = np.exp(-np.linspace(0, 0.03, int(0.03 * SAMPLE_RATE)) * 250) * np.sin(2 * np.pi * 2400 * np.linspace(0, 0.03, int(0.03 * SAMPLE_RATE))) * 0.15

    for t_sec in np.arange(0.5, total_sec - 0.5, 0.5):
        if int(t_sec * 2) % 2 == 0:
            add_tone(track, tick_tone, t_sec, pan=0.25)
        else:
            add_tone(track, tock_tone, t_sec, pan=0.35)

    # Curious Celesta / Woodwind Theme in C Major (C4=261.63, D4=293.66, E4=329.63, G4=392.0, A4=440.0, C5=523.25)
    celesta_notes = [
        (0.8, 523.25, 0.6), (1.4, 440.0, 0.5), (2.0, 392.0, 0.8), (2.8, 329.63, 0.7),
        (3.6, 261.63, 1.2), (5.0, 293.66, 0.6), (5.6, 329.63, 0.6), (6.2, 392.0, 1.0),
        (7.5, 523.25, 0.8), (8.5, 587.33, 0.8), (9.5, 659.25, 1.2), (11.0, 523.25, 0.7),
        (12.5, 440.0, 0.8), (13.5, 392.0, 0.8), (14.5, 329.63, 1.0), (16.0, 261.63, 1.4),
        (18.0, 392.0, 0.7), (19.0, 440.0, 0.7), (20.0, 523.25, 1.5)
    ]
    for start, freq, dur in celesta_notes:
        if start < total_sec:
            add_tone(track, synth_bell(freq, dur, gain=0.22), start, pan=-0.15)

    # Soft Pizzicato Cello on beats
    pizz_bass = [
        (0.0, 130.81, 0.8), (2.0, 196.0, 0.8), (4.0, 130.81, 0.8), (6.0, 164.81, 0.8),
        (8.0, 174.61, 0.8), (10.0, 196.0, 0.8), (12.0, 130.81, 0.8), (14.0, 164.81, 0.8),
        (16.0, 174.61, 0.8), (18.0, 196.0, 0.8), (20.0, 130.81, 1.2)
    ]
    for start, freq, dur in pizz_bass:
        if start < total_sec:
            add_tone(track, synth_pizzicato(freq, dur, gain=0.26), start, pan=-0.2)

    return track

# -------------------------------------------------------------
# 2. SCENE 2 BGM: Mysterious, playful pizzicato / chimes
# -------------------------------------------------------------
def build_bgm_scene2(total_sec=30.0):
    n_samples = int(total_sec * SAMPLE_RATE)
    track = np.zeros((n_samples, 2), dtype=np.float32)

    # Ethereal Glassy Twilight Pad (D Minor / Dorian: D, F, A, C, E)
    t = np.linspace(0, total_sec, n_samples)
    pad = (
        np.sin(2 * np.pi * 146.83 * t) +
        0.5 * np.sin(2 * np.pi * 220.0 * t) +
        0.3 * np.sin(2 * np.pi * 349.23 * t)
    ) * 0.06 * (0.8 + 0.2 * np.sin(2 * np.pi * 0.2 * t))
    track[:, 0] += pad * 0.7
    track[:, 1] += pad * 0.7

    # Playful Chimes & Glass Glockenspiel Arpeggios
    chimes = [
        (1.0, 587.33), (1.4, 698.46), (1.8, 880.0), (2.2, 1046.5), (2.6, 880.0),
        (4.5, 523.25), (4.9, 659.25), (5.3, 783.99), (5.7, 987.77),
        (8.0, 587.33), (8.4, 783.99), (8.8, 880.0), (9.2, 1174.66), (9.6, 880.0),
        (12.0, 523.25), (12.4, 659.25), (12.8, 783.99), (13.2, 1046.5),
        (15.5, 587.33), (15.9, 698.46), (16.3, 880.0), (16.7, 1046.5),
        (19.0, 523.25), (19.4, 659.25), (19.8, 880.0), (20.2, 987.77),
        (23.0, 587.33), (23.5, 880.0), (24.0, 1174.66), (25.0, 880.0)
    ]
    for start, freq in chimes:
        if start < total_sec:
            add_tone(track, synth_bell(freq, 1.2, gain=0.2), start, pan=np.sin(start))

    # Staccato Pizzicato String Bass & Counterpoint
    pizz = [
        (0.5, 146.83), (1.5, 220.0), (2.5, 174.61), (3.5, 196.0),
        (4.5, 130.81), (5.5, 196.0), (6.5, 164.81), (7.5, 174.61),
        (8.5, 146.83), (9.5, 220.0), (10.5, 174.61), (11.5, 196.0),
        (12.5, 130.81), (13.5, 196.0), (14.5, 164.81), (15.5, 174.61),
        (16.5, 146.83), (17.5, 220.0), (18.5, 174.61), (19.5, 196.0),
        (20.5, 130.81), (21.5, 196.0), (22.5, 164.81), (23.5, 174.61),
        (24.5, 146.83), (26.0, 146.83)
    ]
    for start, freq in pizz:
        if start < total_sec:
            add_tone(track, synth_pizzicato(freq, 0.6, gain=0.24), start, pan=-0.25)

    return track

# -------------------------------------------------------------
# 3. SCENE 3 BGM: Quirky Upbeat Whimsical Waltz / Tea Party
# -------------------------------------------------------------
def build_bgm_scene3(total_sec=55.0):
    n_samples = int(total_sec * SAMPLE_RATE)
    track = np.zeros((n_samples, 2), dtype=np.float32)

    # 3/4 Waltz tempo: 135 BPM -> Beat length = 60/135 = 0.444s, Measure = 1.333s
    beat = 60.0 / 135.0
    measure = beat * 3.0

    # Bass on Beat 1, Chords on Beats 2 & 3
    # Progression: F - C - Dm - Bb - F - C - F - C
    chords = [
        # (Bass freq, chord freqs)
        (174.61, [349.23, 440.0, 523.25]),  # F
        (130.81, [261.63, 329.63, 392.0]),  # C
        (146.83, [293.66, 349.23, 440.0]),  # Dm
        (116.54, [233.08, 293.66, 349.23]), # Bb
        (174.61, [349.23, 440.0, 523.25]),  # F
        (130.81, [261.63, 329.63, 392.0]),  # C
        (174.61, [349.23, 440.0, 523.25]),  # F
        (196.00, [293.66, 392.0, 493.88])   # G/C
    ]

    total_measures = int(total_sec / measure) + 1
    for m in range(total_measures):
        m_start = m * measure
        c_idx = m % len(chords)
        bass_f, chord_fs = chords[c_idx]

        # Beat 1: Bassoon / Cello staccato bass
        add_tone(track, synth_pizzicato(bass_f, beat * 1.2, gain=0.28), m_start, pan=-0.3)

        # Beat 2: Pizzicato chords
        for cf in chord_fs:
            add_tone(track, synth_pizzicato(cf, beat * 0.8, gain=0.15), m_start + beat, pan=0.2)

        # Beat 3: Pizzicato chords
        for cf in chord_fs:
            add_tone(track, synth_pizzicato(cf, beat * 0.8, gain=0.15), m_start + beat * 2, pan=0.2)

    # Whimsical Woodwind / Flute Melody over waltz
    flute_notes = [
        (0.0, 523.25, beat*2), (beat*2, 587.33, beat), (beat*3, 659.25, beat*2), (beat*5, 523.25, beat),
        (beat*6, 698.46, beat*2), (beat*8, 659.25, beat), (beat*9, 587.33, beat*3),
        (beat*12, 523.25, beat*2), (beat*14, 659.25, beat), (beat*15, 783.99, beat*2), (beat*17, 698.46, beat),
        (beat*18, 659.25, beat*2), (beat*20, 587.33, beat), (beat*21, 523.25, beat*3),
        (beat*24, 698.46, beat*2), (beat*26, 783.99, beat), (beat*27, 880.0, beat*2), (beat*29, 698.46, beat),
        (beat*30, 783.99, beat*2), (beat*32, 659.25, beat), (beat*33, 587.33, beat*3)
    ]
    # Repeat melody loop across scene
    for loop in range(3):
        loop_offset = loop * (beat * 36)
        for rel_t, freq, dur in flute_notes:
            t_start = loop_offset + rel_t
            if t_start + dur < total_sec:
                add_tone(track, synth_flute(freq, dur, gain=0.22), t_start, pan=-0.1)

    # Delicate porcelain teapot clinks (bell tone accents)
    for clink_t in [4.5, 11.2, 18.4, 25.0, 32.8, 39.5, 46.2]:
        if clink_t < total_sec:
            add_tone(track, synth_bell(2489.0, 0.4, gain=0.14), clink_t, pan=0.35)

    return track

# -------------------------------------------------------------
# 4. SCENE 4 BGM: Royal Fanfare + Dramatic Tense March + Freeze
# -------------------------------------------------------------
def build_bgm_scene4(total_sec=48.0, freeze_time=43.12):
    n_samples = int(total_sec * SAMPLE_RATE)
    track = np.zeros((n_samples, 2), dtype=np.float32)

    # 1. Royal Trumpet Fanfare (0.0s to 2.5s) - C Minor/Major regal flourish
    fanfare = [
        (0.0, 261.63, 0.25), (0.28, 329.63, 0.25), (0.56, 392.0, 0.35),
        (0.95, 523.25, 0.7), (1.7, 392.0, 0.25), (1.98, 523.25, 1.0)
    ]
    for start, freq, dur in fanfare:
        add_tone(track, synth_brass(freq, dur, gain=0.32), start, pan=0.0)
        # Harmonizing trumpet (3rd above)
        add_tone(track, synth_brass(freq * 1.25, dur, gain=0.22), start, pan=0.2)

    # 2. Tense Dramatic Royal March (2.5s up to freeze_time)
    # Timpani & Dramatic Low Strings in C Minor (C, Eb, G, Ab)
    march_step = 0.55  # 110 BPM march tempo
    curr_t = 2.5
    step_count = 0
    while curr_t < freeze_time - 0.2:
        # Timpani beat
        add_tone(track, synth_timpani(0.5, gain=0.32), curr_t, pan=-0.1)
        
        # Staccato dramatic strings
        if step_count % 4 == 0:
            add_tone(track, synth_brass(130.81, 0.35, gain=0.25), curr_t, pan=-0.2)
        elif step_count % 4 == 1:
            add_tone(track, synth_pizzicato(196.0, 0.35, gain=0.22), curr_t, pan=0.2)
        elif step_count % 4 == 2:
            add_tone(track, synth_brass(155.56, 0.35, gain=0.25), curr_t, pan=-0.2)
        else:
            add_tone(track, synth_brass(196.0, 0.35, gain=0.26), curr_t, pan=0.1)
        
        # Tense high string tremolo / stabs
        if step_count % 2 == 1:
            add_tone(track, synth_bell(523.25, 0.3, gain=0.18), curr_t, pan=0.25)
            add_tone(track, synth_bell(622.25, 0.3, gain=0.16), curr_t, pan=-0.25)

        curr_t += march_step
        step_count += 1

    # Final Dramatic Staccato Stab right before freeze
    stab_t = freeze_time - 0.15
    add_tone(track, synth_brass(261.63, 0.2, gain=0.4), stab_t, pan=0.0)
    add_tone(track, synth_brass(392.0, 0.2, gain=0.35), stab_t, pan=0.2)
    add_tone(track, synth_timpani(0.3, gain=0.45), stab_t, pan=0.0)

    # STRICT ZERO AUDIO after freeze_time (dramatic stage freeze!)
    freeze_idx = int(freeze_time * SAMPLE_RATE)
    track[freeze_idx:, :] = 0.0

    return track

# -------------------------------------------------------------
# 5. OUTRO BGM: Warm Resolved Harp Cadence
# -------------------------------------------------------------
def build_bgm_outro(total_sec=6.0):
    n_samples = int(total_sec * SAMPLE_RATE)
    track = np.zeros((n_samples, 2), dtype=np.float32)

    # Resolved C Major Harp Arpeggio for Bows
    arpeggio = [
        (0.2, 130.81), (0.4, 196.0), (0.6, 261.63), (0.8, 329.63), (1.0, 392.0),
        (1.2, 523.25), (1.4, 659.25), (1.6, 783.99), (1.8, 1046.5)
    ]
    for start, freq in arpeggio:
        add_tone(track, synth_bell(freq, 2.5, gain=0.25), start, pan=np.sin(start * 2))

    # Warm resolved strings chord
    t = np.linspace(0, total_sec - 1.8, int((total_sec - 1.8) * SAMPLE_RATE))
    env = np.linspace(0, 1, int(0.5 * SAMPLE_RATE))
    env = np.concatenate([env, np.ones(len(t) - len(env))])
    fade_out = np.linspace(1, 0, int(1.5 * SAMPLE_RATE))
    env[-len(fade_out):] *= fade_out
    
    pad = (
        np.sin(2 * np.pi * 261.63 * t) +
        0.7 * np.sin(2 * np.pi * 329.63 * t) +
        0.5 * np.sin(2 * np.pi * 392.0 * t) +
        0.3 * np.sin(2 * np.pi * 523.25 * t)
    ) * 0.15 * env
    start_idx = int(1.8 * SAMPLE_RATE)
    track[start_idx:start_idx+len(pad), 0] += pad * 0.7
    track[start_idx:start_idx+len(pad), 1] += pad * 0.7

    return track

def main():
    audio_dir = Path("assets/audio")
    audio_dir.mkdir(parents=True, exist_ok=True)

    tracks = [
        ("bgm_scene1", build_bgm_scene1(total_sec=25.0), -22.0),
        ("bgm_scene2", build_bgm_scene2(total_sec=30.0), -22.0),
        ("bgm_scene3", build_bgm_scene3(total_sec=55.0), -22.0),
        ("bgm_scene4", build_bgm_scene4(total_sec=48.0, freeze_time=43.12), -21.0),
        ("bgm_outro", build_bgm_outro(total_sec=6.0), -20.0)
    ]

    for name, track_data, target_db in tracks:
        wav_path = audio_dir / f"{name}.wav"
        mp3_path = audio_dir / f"{name}.mp3"
        print(f"Mastering & exporting {mp3_path.name}...")
        normalize_and_export(track_data, wav_path, mp3_path, target_rms_db=target_db)

if __name__ == "__main__":
    main()
