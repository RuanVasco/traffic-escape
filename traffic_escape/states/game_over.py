"""Result screen shown once the crash animation has finished."""

import pygame

from ..config import Colors
from ..rendering.overlay import OverlayLine
from .base import BaseState, StateName


class GameOverState(BaseState):
    def __init__(self, host) -> None:
        super().__init__(host)
        self._new_record = False

    def enter(self) -> None:
        self._new_record = self.world.commit_score()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            self.world.reset()
            self.host.set_state(StateName.PLAYING)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        best = f"Best: {self.world.high_score:06d}" + ("   NEW RECORD" if self._new_record else "")
        self.host.overlay.draw(
            surface,
            "GAME OVER",
            [
                OverlayLine(f"Score: {self.world.score.value:06d}", "medium"),
                OverlayLine(f"Overtakes: {self.world.score.overtakes}"),
                OverlayLine(best, color=Colors.YELLOW if self._new_record else Colors.GREY),
                OverlayLine("", "tiny"),
                OverlayLine("PRESS R TO RACE AGAIN", "medium", Colors.YELLOW),
                OverlayLine("ESC to quit", color=Colors.GREY),
            ],
            title_color=Colors.RED,
        )
