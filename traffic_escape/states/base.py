"""Shared plumbing for the game states."""

from typing import Protocol

import pygame

from ..rendering.overlay import OverlayRenderer
from ..rendering.scene import SceneRenderer
from ..world import RaceWorld


class StateName:
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    CRASHING = "crashing"
    GAME_OVER = "game_over"


class StateHost(Protocol):
    world: RaceWorld
    scene: SceneRenderer
    overlay: OverlayRenderer

    def set_state(self, name: str) -> None: ...


class BaseState:
    def __init__(self, host: StateHost) -> None:
        self.host = host

    @property
    def world(self) -> RaceWorld:
        return self.host.world

    def enter(self) -> None:
        return

    def handle_event(self, event: pygame.event.Event) -> None:
        return

    def update(self, delta: float) -> None:
        return

    def draw(self, surface: pygame.Surface) -> None:
        self.host.scene.draw(surface, self.world)
