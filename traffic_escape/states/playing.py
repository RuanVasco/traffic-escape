"""Active race: reads input and advances the simulation."""

import pygame

from .base import BaseState, StateName

STEER_KEYS = {pygame.K_LEFT: -1, pygame.K_a: -1, pygame.K_RIGHT: 1, pygame.K_d: 1}


class PlayingState(BaseState):
    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if event.key in STEER_KEYS:
            self.world.player.steer(STEER_KEYS[event.key])
        elif event.key == pygame.K_p:
            self.host.set_state(StateName.PAUSED)

    def update(self, delta: float) -> None:
        if self.world.advance(delta):
            self.host.set_state(StateName.CRASHING)
