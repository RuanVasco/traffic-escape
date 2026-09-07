"""Sound effects synthesised at startup, with a silent fallback."""

import array
import math
import random

import pygame

from ..interfaces import AudioPlayer, Sound

SAMPLE_RATE = 44100
EFFECT_RECIPES = {
    Sound.LANE_CHANGE: (660.0, 980.0, 0.09, 0.22, 0.0),
    Sound.OVERTAKE: (320.0, 180.0, 0.10, 0.16, 0.0),
    Sound.CRASH: (180.0, 40.0, 0.85, 0.55, 0.9),
}


class SilentAudio(AudioPlayer):
    """Used when no audio device is available."""

    def play(self, effect: str) -> None:
        return


class SynthAudio(AudioPlayer):
    def __init__(self) -> None:
        self._effects = {name: self._synthesise(*recipe) for name, recipe in EFFECT_RECIPES.items()}

    def play(self, effect: str) -> None:
        sound = self._effects.get(effect)
        if sound is not None:
            sound.play()

    @staticmethod
    def _synthesise(start_hz: float, end_hz: float, duration: float, volume: float, noise: float) -> pygame.mixer.Sound:
        rng = random.Random(9)
        samples = array.array("h")
        total = int(SAMPLE_RATE * duration)
        phase = 0.0
        for index in range(total):
            position = index / total
            phase += 2 * math.pi * (start_hz + (end_hz - start_hz) * position) / SAMPLE_RATE
            wave = math.sin(phase)
            if noise:
                wave = wave * (1 - noise) + rng.uniform(-1, 1) * noise
            envelope = min(1.0, position * 25) * (1 - position) ** 1.6
            samples.append(int(max(-1.0, min(1.0, wave)) * envelope * volume * 32767))
        return pygame.mixer.Sound(buffer=samples.tobytes())


def create_audio() -> AudioPlayer:
    try:
        pygame.mixer.init(frequency=SAMPLE_RATE, size=-16, channels=1, buffer=512)
        return SynthAudio()
    except pygame.error:
        return SilentAudio()
