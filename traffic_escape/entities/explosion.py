"""Frame based crash animation."""

import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, frames: list[pygame.Surface], center: tuple[int, int], ticks_per_frame: int = 3) -> None:
        super().__init__()
        self._frames = frames
        self._ticks_per_frame = ticks_per_frame
        self._index = 0
        self._ticks = 0
        self.image = frames[0]
        self.rect = self.image.get_rect(center=center)
        self.finished = False

    def update(self, *_args) -> None:
        self._ticks += 1
        if self._ticks < self._ticks_per_frame:
            return
        self._ticks = 0
        self._index += 1
        if self._index >= len(self._frames):
            self._index = len(self._frames) - 1
            self.finished = True
        self.image = self._frames[self._index]

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.image.get_rect(center=self.rect.center))
