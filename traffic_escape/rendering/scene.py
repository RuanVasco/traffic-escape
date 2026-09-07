"""Composes the race frame: road, vehicles, effects and HUD."""

import random

import pygame

from ..config import Colors, CRASH_FLASH_FRAMES, SCREEN_HEIGHT, SCREEN_WIDTH
from .hud import HudRenderer
from .road_renderer import RoadRenderer

SHAKE_RANGE = 6


class SceneRenderer:
    def __init__(self, road_renderer: RoadRenderer, hud: HudRenderer, rng: random.Random | None = None) -> None:
        self._road_renderer = road_renderer
        self._hud = hud
        self._rng = rng or random.Random()
        self._frame = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    def draw(self, surface: pygame.Surface, world) -> None:
        self._road_renderer.draw(self._frame, world.road)
        for prop in world.roadside.props:
            self._frame.blit(prop.image, (prop.x, prop.y))
        for car in world.traffic:
            car.draw(self._frame)
        if not world.player_destroyed:
            world.player.draw(self._frame)
        for explosion in world.explosions:
            explosion.draw(self._frame)

        surface.fill(Colors.BLACK)
        surface.blit(self._frame, self._shake_offset(world.shake_frames))
        self._draw_flash(surface, world.flash_frames)
        self._hud.draw(surface, world)

    def _shake_offset(self, shake_frames: int) -> tuple[int, int]:
        if not shake_frames:
            return (0, 0)
        return (self._rng.randint(-SHAKE_RANGE, SHAKE_RANGE), self._rng.randint(-SHAKE_RANGE, SHAKE_RANGE))

    @staticmethod
    def _draw_flash(surface: pygame.Surface, flash_frames: int) -> None:
        if not flash_frames:
            return
        flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        flash.fill(Colors.WHITE)
        flash.set_alpha(int(200 * flash_frames / CRASH_FLASH_FRAMES))
        surface.blit(flash, (0, 0))
