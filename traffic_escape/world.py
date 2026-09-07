"""Mutable state of a race and the simulation step that advances it."""

import random

import pygame

from .assets.explosion_frames import ExplosionFrameFactory
from .assets.scenery_sprites import ScenerySpriteFactory
from .assets.vehicle_sprites import VehicleSpriteFactory
from .config import (
    CRASH_BRAKE,
    CRASH_FLASH_FRAMES,
    CRASH_SHAKE_FRAMES,
    MAX_TRAFFIC_CARS,
    MIN_TRAFFIC_CARS,
    ROAD_ACCELERATION,
    ROAD_SPEED_MAX,
    ROAD_SPEED_START,
    SCREEN_HEIGHT,
)
from .entities.explosion import Explosion
from .entities.player_car import PlayerCar
from .entities.road import Road
from .entities.roadside import Roadside
from .entities.traffic_car import TrafficCar
from .interfaces import AudioPlayer, HighScoreRepository, Sound
from .systems.collision import CollisionDetector
from .systems.scoring import Score
from .systems.spawner import TrafficSpawner

IDLE_SCROLL_FACTOR = 0.4


class RaceWorld:
    def __init__(
        self,
        sprites: VehicleSpriteFactory,
        scenery: ScenerySpriteFactory,
        explosions: ExplosionFrameFactory,
        audio: AudioPlayer,
        high_scores: HighScoreRepository,
        rng: random.Random | None = None,
    ) -> None:
        self._sprites = sprites
        self._scenery = scenery
        self._explosion_frames = explosions
        self._audio = audio
        self._high_scores = high_scores
        self._rng = rng or random.Random()
        self._spawner = TrafficSpawner(self._rng)
        self._collisions = CollisionDetector()
        self.high_score = high_scores.load()
        self.reset()

    def reset(self) -> None:
        self.player = PlayerCar(self._sprites, self._audio)
        self.traffic: pygame.sprite.Group = pygame.sprite.Group()
        self.explosions: pygame.sprite.Group = pygame.sprite.Group()
        self.road = Road()
        self.roadside = Roadside(self._scenery, self._rng)
        self.score = Score()
        self.road_speed = ROAD_SPEED_START
        self.flash_frames = 0
        self.shake_frames = 0
        for index in range(MIN_TRAFFIC_CARS):
            car = TrafficCar(self._sprites, self._rng)
            self.traffic.add(car)
            self._spawner.place(car, self.traffic, self.score.level, bottom=-160 - index * 230)

    @property
    def traffic_capacity(self) -> int:
        return min(MIN_TRAFFIC_CARS + (self.score.level - 1) // 2, MAX_TRAFFIC_CARS)

    @property
    def crash_finished(self) -> bool:
        return all(explosion.finished for explosion in self.explosions)

    def drift(self) -> None:
        """Background motion for the menu and pause screens."""
        idle_speed = self.road_speed * IDLE_SCROLL_FACTOR
        self.road.update(idle_speed)
        self.roadside.update(idle_speed)

    def advance(self, delta: float) -> bool:
        self.road_speed = min(ROAD_SPEED_MAX, self.road_speed + ROAD_ACCELERATION * delta)
        self.score.add_distance(self.road_speed, delta)
        self._fill_traffic()

        self.player.update()
        self.traffic.update(self.road_speed)
        self.road.update(self.road_speed)
        self.roadside.update(self.road_speed)
        self._recycle_traffic()
        self.flash_frames = max(0, self.flash_frames - 1)

        victim = self._collisions.first_hit(self.player, self.traffic)
        if victim is None:
            return False
        self._crash(victim)
        return True

    def coast(self, delta: float) -> None:
        """Slows the road down while the crash animation plays."""
        self.road_speed = max(0.0, self.road_speed - CRASH_BRAKE * delta)
        self.explosions.update()
        self.traffic.update(self.road_speed)
        self.road.update(self.road_speed)
        self.roadside.update(self.road_speed)
        self.flash_frames = max(0, self.flash_frames - 1)
        self.shake_frames = max(0, self.shake_frames - 1)

    def commit_score(self) -> bool:
        if self.score.value <= self.high_score:
            return False
        self.high_score = self.score.value
        self._high_scores.save(self.high_score)
        return True

    def _fill_traffic(self) -> None:
        while len(self.traffic) < self.traffic_capacity:
            car = TrafficCar(self._sprites, self._rng)
            self.traffic.add(car)
            self._spawner.place(car, self.traffic, self.score.level, bottom=-self._rng.randint(200, 600))

    def _recycle_traffic(self) -> None:
        for car in self.traffic:
            if car.rect.top > SCREEN_HEIGHT:
                self._spawner.place(car, self.traffic, self.score.level)
                self.score.add_overtake()
                self._audio.play(Sound.OVERTAKE)

    def _crash(self, victim: TrafficCar) -> None:
        frames = self._explosion_frames.frames()
        impact = (
            (self.player.rect.centerx + victim.rect.centerx) // 2,
            (self.player.rect.centery + victim.rect.centery) // 2,
        )
        self.explosions.add(Explosion(frames, impact))
        self.explosions.add(Explosion(frames, self.player.rect.center, ticks_per_frame=4))
        self._audio.play(Sound.CRASH)
        self.player.wreck()
        self.flash_frames = CRASH_FLASH_FRAMES
        self.shake_frames = CRASH_SHAKE_FRAMES
