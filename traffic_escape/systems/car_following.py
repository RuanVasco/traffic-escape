"""Keeps vehicles sharing a lane from driving through each other."""

from collections import defaultdict
from typing import Iterable

from ..entities.traffic_car import TrafficCar

MIN_GAP = 26


class CarFollowing:
    """A car that catches up with a slower one brakes to its speed."""

    def apply(self, cars: Iterable[TrafficCar]) -> None:
        lanes: dict[int, list[TrafficCar]] = defaultdict(list)
        for car in cars:
            lanes[car.lane].append(car)

        for queue in lanes.values():
            queue.sort(key=lambda car: car.rect.top)
            for leader, follower in zip(queue, queue[1:]):
                limit = leader.rect.bottom + MIN_GAP
                if follower.rect.top < limit:
                    follower.rect.top = limit
                    follower.own_speed = leader.own_speed
