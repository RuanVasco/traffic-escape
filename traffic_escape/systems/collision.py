"""Rect based collision detection."""

from typing import Iterable

from ..entities.vehicle import Vehicle


class CollisionDetector:
    def first_hit(self, player: Vehicle, others: Iterable[Vehicle]) -> Vehicle | None:
        player_box = player.hitbox
        for other in others:
            if player_box.colliderect(other.hitbox):
                return other
        return None
