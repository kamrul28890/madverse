"""
MadVerse Sound Manager
Generates and plays sound effects using Qt's multimedia or fallback beeps.
"""

import os
import math
import struct
import wave
import tempfile
from typing import Optional

try:
    from PyQt6.QtMultimedia import QSoundEffect
    from PyQt6.QtCore import QUrl
    HAS_SOUND = True
except ImportError:
    HAS_SOUND = False

try:
    from PyQt6.QtCore import QTimer
    HAS_QT = True
except ImportError:
    HAS_QT = False


SOUNDS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sounds")


def _generate_wav(filename: str, freq: float, duration: float,
                  volume: float = 0.5, waveform: str = "sine",
                  decay: bool = True):
    """Generate a simple WAV file programmatically."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        if waveform == "sine":
            val = math.sin(2 * math.pi * freq * t)
        elif waveform == "square":
            val = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
        elif waveform == "sawtooth":
            val = 2 * (t * freq - math.floor(t * freq + 0.5))
        else:
            val = math.sin(2 * math.pi * freq * t)

        # Envelope: attack + decay
        if decay:
            envelope = max(0.0, 1.0 - (i / num_samples) ** 0.5)
        else:
            attack = min(1.0, i / (sample_rate * 0.01))
            envelope = attack
        val = val * volume * envelope

        # Convert to 16-bit PCM
        samples.append(int(val * 32767))

    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(packed)


def _generate_chord_wav(filename: str, freqs: list, duration: float, volume: float = 0.4):
    """Generate a WAV with multiple frequencies (chord)."""
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    samples = []
    for i in range(num_samples):
        t = i / sample_rate
        val = sum(math.sin(2 * math.pi * f * t) for f in freqs) / len(freqs)
        envelope = max(0.0, 1.0 - (i / num_samples))
        val = val * volume * envelope
        samples.append(int(val * 32767))
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with wave.open(filename, "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        packed = struct.pack(f"<{len(samples)}h", *samples)
        wf.writeframes(packed)


def generate_all_sounds():
    """Pre-generate all sound effect WAV files."""
    os.makedirs(SOUNDS_DIR, exist_ok=True)

    # UI sounds
    _generate_wav(f"{SOUNDS_DIR}/click.wav",       freq=800,  duration=0.08,  volume=0.3)
    _generate_wav(f"{SOUNDS_DIR}/select.wav",      freq=1200, duration=0.12,  volume=0.35)
    _generate_chord_wav(f"{SOUNDS_DIR}/reveal.wav",   freqs=[523, 659, 784], duration=0.5,  volume=0.4)
    _generate_chord_wav(f"{SOUNDS_DIR}/complete.wav", freqs=[523, 659, 784, 1047], duration=0.8, volume=0.45)
    _generate_wav(f"{SOUNDS_DIR}/achievement.wav", freq=1047, duration=1.0,   volume=0.5, waveform="sine")
    _generate_wav(f"{SOUNDS_DIR}/error.wav",       freq=200,  duration=0.3,   volume=0.4, waveform="square")
    _generate_wav(f"{SOUNDS_DIR}/save.wav",        freq=660,  duration=0.2,   volume=0.35)
    _generate_wav(f"{SOUNDS_DIR}/typing.wav",      freq=400,  duration=0.04,  volume=0.2)

    # Genre theme sounds (ambient stingers)
    _generate_wav(f"{SOUNDS_DIR}/horror_theme.wav",      freq=80,  duration=1.5,  volume=0.4, waveform="sawtooth")
    _generate_chord_wav(f"{SOUNDS_DIR}/scifi_theme.wav",       freqs=[440, 550, 880], duration=0.6, volume=0.4)
    _generate_chord_wav(f"{SOUNDS_DIR}/fantasy_theme.wav",     freqs=[392, 494, 587], duration=1.0, volume=0.4)
    _generate_wav(f"{SOUNDS_DIR}/romance_theme.wav",     freq=494, duration=0.8,  volume=0.35, waveform="sine", decay=False)
    _generate_wav(f"{SOUNDS_DIR}/academic_theme.wav",    freq=330, duration=0.3,  volume=0.25)
    _generate_wav(f"{SOUNDS_DIR}/existential_theme.wav", freq=110, duration=2.0,  volume=0.3, waveform="sine")
    _generate_chord_wav(f"{SOUNDS_DIR}/ai_theme.wav",          freqs=[220, 440, 660, 880], duration=0.5, volume=0.4)

    # Story reveal per-sentence stinger
    _generate_wav(f"{SOUNDS_DIR}/sentence_pop.wav", freq=600, duration=0.06, volume=0.2)
    _generate_wav(f"{SOUNDS_DIR}/fourth_wall.wav",  freq=300, duration=0.4,  volume=0.35, waveform="square")


class SoundManager:
    """Manages sound playback for MadVerse."""

    def __init__(self):
        self._enabled = True
        self._volume = 0.7
        self._effects = {}
        self._ensure_sounds()
        self._load_effects()

    def _ensure_sounds(self):
        if not os.path.exists(f"{SOUNDS_DIR}/click.wav"):
            generate_all_sounds()

    def _load_effects(self):
        if not HAS_SOUND:
            return
        sound_names = [
            "click", "select", "reveal", "complete", "achievement",
            "error", "save", "typing", "sentence_pop", "fourth_wall",
            "horror_theme", "scifi_theme", "fantasy_theme", "romance_theme",
            "academic_theme", "existential_theme", "ai_theme",
        ]
        for name in sound_names:
            path = f"{SOUNDS_DIR}/{name}.wav"
            if os.path.exists(path):
                try:
                    fx = QSoundEffect()
                    fx.setSource(QUrl.fromLocalFile(os.path.abspath(path)))
                    fx.setVolume(self._volume)
                    self._effects[name] = fx
                except Exception:
                    pass

    def play(self, name: str):
        if not self._enabled:
            return
        if not HAS_SOUND:
            return
        fx = self._effects.get(name)
        if fx:
            try:
                fx.setVolume(self._volume)
                fx.play()
            except Exception:
                pass

    def play_genre_theme(self, genre_id: str):
        self.play(f"{genre_id}_theme")

    def set_enabled(self, enabled: bool):
        self._enabled = enabled

    def set_volume(self, volume: float):
        self._volume = max(0.0, min(1.0, volume))

    def is_enabled(self) -> bool:
        return self._enabled


# Singleton
_manager: Optional[SoundManager] = None

def get_sound_manager() -> SoundManager:
    global _manager
    if _manager is None:
        _manager = SoundManager()
    return _manager
