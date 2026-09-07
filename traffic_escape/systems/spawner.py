"""Places traffic cars back at the top of the road."""

import random
from typing import Iterable

from ..config import LANE_COUNT
from ..entities.traffic_car import TrafficCar

MAX_ATTEMPTS = 30
BASE_GAP = 300
GAP_PER_LEVEL = 12
MIN_GAP = 150
LOOKBACK = 240
LOOKAHEAD = 120


class TrafficSpawner:
    """Keeps at least one lane open so the player always has an escape."""

    def __init__(self, rng: random.Random) -> None:
        self._rng = rng

    def place(self, car: TrafficCar, others: Iterable[TrafficCar], level: int, bottom: int | None = None) -> None:
        gap = max(MIN_GAP, BASE_GAP - level * GAP_PER_LEVEL)
        neighbours = [other for other in others if other is not car]
        for _ in range(MAX_ATTEMPTS):
            lane = self._rng.randrange(LANE_COUNT)
            y = bottom if bottom is not None else -self._rng.randint(40, 40 + gap)
            if self._is_free(lane, y, neighbours):
                car.place(lane, y)
                return
        car.place(self._rng.randrange(LANE_COUNT), -self._rng.randint(200, 500))

    @staticmethod
    def _is_free(lane: int, y: int, neighbours: Iterable[TrafficCar]) -> bool:
        occupied = {lane}
        for other in neighbours:
            if other.rect.bottom <= y - LOOKBACK or other.rect.top >= y + LOOKAHEAD:
                continue
            if other.lane == lane:
                return False
            occupied.add(other.lane)
        return len(occupied) < LANE_COUNT
