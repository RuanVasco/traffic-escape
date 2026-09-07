"""Player controlled car, locked to the bottom of the screen."""

import math

import pygame

from ..assets.vehicle_kinds import PLAYER_KIND
from ..config import Colors, LANE_CENTERS, LANE_CHANGE_SPEED, PLAYER_Y
from ..interfaces import AudioPlayer, Sound, VehicleSpriteSource
from .vehicle import Vehicle

TILT_PER_PIXEL = 0.75
TILT_SMOOTHING = 0.25
TILT_THRESHOLD = 0.4
ENGINE_SHAKE = 1.2
ENGINE_SHAKE_RATE = 0.25


class PlayerCar(Vehicle):
    def __init__(self, sprites: VehicleSpriteSource, audio: AudioPlayer, lane: int = 1) -> None:
        self._base_image = sprites.create(Colors.PLAYER, PLAYER_KIND, is_player=True)
        super().__init__(self._base_image, (LANE_CENTERS[lane], PLAYER_Y))
        self._audio = audio
        self.lane = lane
        self._tilt = 0.0
        self._ticks = 0
        self._bounce = 0.0

    def steer(self, direction: int) -> None:
        target = self.lane + direction
        if 0 <= target < len(LANE_CENTERS):
            self.lane = target
            self._audio.play(Sound.LANE_CHANGE)

    def update(self, *_args) -> None:
        step = self._lane_step()
        self.rect.centerx += step
        self._tilt += (-step * TILT_PER_PIXEL - self._tilt) * TILT_SMOOTHING
        self._ticks += 1
        self._bounce = math.sin(self._ticks * ENGINE_SHAKE_RATE) * ENGINE_SHAKE
        self.image = (
            pygame.transform.rotozoom(self._base_image, self._tilt, 1.0)
            if abs(self._tilt) > TILT_THRESHOLD
            else self._base_image
        )

    def draw(self, surface: pygame.Surface) -> None:
        position = self.image.get_rect(center=(self.rect.centerx, self.rect.centery + self._bounce))
        surface.blit(self.image, position)

    def _lane_step(self) -> int:
        distance = LANE_CENTERS[self.lane] - self.rect.centerx
        if abs(distance) <= LANE_CHANGE_SPEED:
            return distance
        return LANE_CHANGE_SPEED if distance > 0 else -LANE_CHANGE_SPEED
