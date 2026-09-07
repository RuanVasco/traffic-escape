"""Base sprite for every vehicle on the highway."""

import pygame

from ..config import HITBOX_SHRINK


class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image: pygame.Surface, center: tuple[int, int]) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=center)

    @property
    def hitbox(self) -> pygame.Rect:
        """Slightly smaller than the sprite so near misses are forgiving."""
        return self.rect.inflate(*HITBOX_SHRINK)

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)
