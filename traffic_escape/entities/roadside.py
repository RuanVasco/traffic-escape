"""Trees and traffic signs scrolling along both sides of the road."""

import random
from dataclasses import dataclass

import pygame

from ..assets.scenery_sprites import ScenerySpriteFactory
from ..config import PROP_COUNT, PROP_SPACING, ROAD_LEFT, ROAD_RIGHT, SCREEN_HEIGHT, SCREEN_WIDTH

SIGN_CHANCE = 0.35
PARALLAX = 1.05


@dataclass
class Prop:
    image: pygame.Surface
    x: int
    y: float


class Roadside:
    def __init__(self, scenery: ScenerySpriteFactory, rng: random.Random) -> None:
        self._scenery = scenery
        self._rng = rng
        self.props = [self._spawn(-index * PROP_SPACING) for index in range(PROP_COUNT)]

    def update(self, road_speed: float) -> None:
        for prop in self.props:
            prop.y += road_speed * PARALLAX
            if prop.y > SCREEN_HEIGHT + 40:
                fresh = self._spawn(-self._rng.randint(60, 220))
                prop.image, prop.x, prop.y = fresh.image, fresh.x, fresh.y

    def _spawn(self, y: float) -> Prop:
        on_left = self._rng.random() < 0.5
        if self._rng.random() < SIGN_CHANCE:
            image = self._rng.choice(self._scenery.signs())
            x = ROAD_LEFT - 44 if on_left else ROAD_RIGHT + 12
        else:
            image = self._scenery.tree()
            x = self._rng.randint(2, ROAD_LEFT - 62) if on_left else self._rng.randint(ROAD_RIGHT + 8, SCREEN_WIDTH - 60)
        return Prop(image, x, y)
