"""Title screen shown before the first run."""

import pygame

from ..config import Colors
from ..rendering.overlay import OverlayLine
from .base import BaseState, StateName

START_KEYS = (pygame.K_SPACE, pygame.K_RETURN)


class MenuState(BaseState):
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in START_KEYS:
            self.world.reset()
            self.host.set_state(StateName.PLAYING)

    def update(self, delta: float) -> None:
        self.world.drift()

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.host.overlay.draw(
            surface,
            "TRAFFIC ESCAPE",
            [
                OverlayLine("Dodge the traffic for as long as you can"),
                OverlayLine("", "tiny"),
                OverlayLine("LEFT / RIGHT or A / D to change lane", color=Colors.GREY),
                OverlayLine("P to pause      ESC to quit", color=Colors.GREY),
                OverlayLine("", "tiny"),
                OverlayLine("PRESS SPACE TO START", "medium", Colors.YELLOW),
                OverlayLine("", "tiny"),
                OverlayLine(f"Best: {self.world.high_score:06d}"),
            ],
        )
