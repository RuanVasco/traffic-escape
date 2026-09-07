"""Pre-renders the frames of the crash animation."""

import math
import random

import pygame

FIRE_STAGES = ((0.25, (255, 250, 210)), (0.45, (255, 190, 60)), (0.65, (230, 96, 34)))


class ExplosionFrameFactory:
    def __init__(self, size: int = 190, frame_count: int = 20, seed: int = 2024) -> None:
        self._size = size
        self._frame_count = frame_count
        self._seed = seed
        self._frames: list[pygame.Surface] | None = None

    def frames(self) -> list[pygame.Surface]:
        if self._frames is None:
            self._frames = [self._render(index / (self._frame_count - 1)) for index in range(self._frame_count)]
        return self._frames

    def _render(self, progress: float) -> pygame.Surface:
        frame = pygame.Surface((self._size, self._size), pygame.SRCALPHA)
        center = self._size // 2
        self._paint_shockwave(frame, center, progress)
        self._paint_particles(frame, center, progress)
        self._paint_core(frame, center, progress)
        return frame

    def _particles(self) -> list[tuple[float, float, int, float]]:
        rng = random.Random(self._seed)
        return [
            (rng.uniform(0, math.tau), rng.uniform(0.15, 1.0), rng.randint(9, 22), rng.uniform(0.8, 1.3))
            for _ in range(30)
        ]

    @staticmethod
    def _paint_shockwave(frame: pygame.Surface, center: int, progress: float) -> None:
        if progress >= 0.55:
            return
        radius = int(center * (0.25 + 1.45 * progress))
        alpha = int(220 * (1 - progress / 0.55))
        pygame.draw.circle(frame, (255, 240, 190, alpha), (center, center), radius, max(2, int(8 * (1 - progress))))

    def _paint_particles(self, frame: pygame.Surface, center: int, progress: float) -> None:
        fire_radius = center * (0.20 + 0.80 * min(1.0, progress * 1.7))
        color = self._flame_color(progress)
        alpha = int(255 * (1 - progress) ** 0.8)
        if alpha <= 0:
            return
        for angle, distance, size, drift in self._particles():
            x = center + math.cos(angle) * distance * fire_radius * drift
            y = center + math.sin(angle) * distance * fire_radius * drift
            radius = int(size * (0.55 + 1.1 * progress))
            if radius > 0:
                pygame.draw.circle(frame, color + (alpha,), (int(x), int(y)), radius)

    @staticmethod
    def _flame_color(progress: float) -> tuple[int, int, int]:
        for limit, color in FIRE_STAGES:
            if progress < limit:
                return color
        grey = int(70 + 60 * (progress - 0.65))
        return (grey, grey - 6, grey - 10)

    @staticmethod
    def _paint_core(frame: pygame.Surface, center: int, progress: float) -> None:
        if progress >= 0.4:
            return
        alpha = int(255 * (1 - progress / 0.4))
        pygame.draw.circle(frame, (255, 255, 235, alpha), (center, center), int(center * 0.42 * (1 - progress)))
