"""Lazily built fonts shared by the renderers."""

import pygame

from ..config import FONT_NAMES

SIZES = {"large": 52, "medium": 28, "small": 20, "tiny": 15}


class FontBook:
    def __init__(self) -> None:
        self._fonts: dict[str, pygame.font.Font] = {}

    def get(self, name: str) -> pygame.font.Font:
        if name not in self._fonts:
            self._fonts[name] = pygame.font.SysFont(FONT_NAMES, SIZES[name], bold=True)
        return self._fonts[name]

    @property
    def large(self) -> pygame.font.Font:
        return self.get("large")

    @property
    def medium(self) -> pygame.font.Font:
        return self.get("medium")

    @property
    def small(self) -> pygame.font.Font:
        return self.get("small")

    @property
    def tiny(self) -> pygame.font.Font:
        return self.get("tiny")
