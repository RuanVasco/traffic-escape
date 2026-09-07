"""Paused race."""

import pygame

from ..config import Colors
from ..rendering.overlay import OverlayLine
from .base import BaseState, StateName

RESUME_KEYS = (pygame.K_p, pygame.K_SPACE)


class PausedState(BaseState):
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in RESUME_KEYS:
            self.host.set_state(StateName.PLAYING)

    def update(self, delta: float) -> None:
        self.world.drift()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.host.overlay.draw(
            surface,
            "PAUSED",
            [OverlayLine("Press P or SPACE to resume", "medium")],
            title_color=Colors.WHITE,
        )
