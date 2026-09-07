"""Abstractions the concrete modules depend on."""

from typing import Protocol, runtime_checkable

import pygame


class Sound(Protocol):
    """Named sound effects the game can request."""

    LANE_CHANGE = "lane_change"
    OVERTAKE = "overtake"
    CRASH = "crash"


@runtime_checkable
class AudioPlayer(Protocol):
    def play(self, effect: str) -> None: ...


@runtime_checkable
class HighScoreRepository(Protocol):
    def load(self) -> int: ...

    def save(self, score: int) -> None: ...


@runtime_checkable
class VehicleSpriteSource(Protocol):
    def create(self, color: tuple[int, int, int], kind, is_player: bool = False) -> pygame.Surface: ...


@runtime_checkable
class Drawable(Protocol):
    def draw(self, surface: pygame.Surface) -> None: ...


class GameState(Protocol):
    """One screen of the state machine driven by the game loop."""

    def enter(self) -> None: ...

    def handle_event(self, event: pygame.event.Event) -> None: ...

    def update(self, delta: float) -> None: ...

    def draw(self, surface: pygame.Surface) -> None: ...
