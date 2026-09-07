"""Opponent vehicle moving in the same direction as the player."""

import random

from ..assets.vehicle_kinds import TRAFFIC_KINDS
from ..config import LANE_CENTERS, TRAFFIC_COLORS
from ..interfaces import VehicleSpriteSource
from .vehicle import Vehicle


class TrafficCar(Vehicle):
    def __init__(self, sprites: VehicleSpriteSource, rng: random.Random) -> None:
        self._sprites = sprites
        self._rng = rng
        self.lane = 0
        self.own_speed = 0.0
        super().__init__(sprites.create(TRAFFIC_COLORS[0], TRAFFIC_KINDS[0]), (-200, -400))
        self._randomise()

    def place(self, lane: int, bottom: int) -> None:
        self._randomise()
        self.lane = lane
        self.rect.centerx = LANE_CENTERS[lane]
        self.rect.bottom = bottom

    def update(self, road_speed: float) -> None:
        """The road scrolls down, so faster vehicles fall behind more slowly."""
        self.rect.y += road_speed - self.own_speed

    def _randomise(self) -> None:
        kind = self._rng.choice(TRAFFIC_KINDS)
        color = self._rng.choice(TRAFFIC_COLORS)
        center = self.rect.center
        self.image = self._sprites.create(color, kind)
        self.rect = self.image.get_rect(center=center)
        self.own_speed = self._rng.uniform(*kind.speed_range)
