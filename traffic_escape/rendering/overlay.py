"""Full screen panels used by the menu, pause and game over screens."""

from dataclasses import dataclass

import pygame

from ..config import Colors, SCREEN_HEIGHT, SCREEN_WIDTH
from .fonts import FontBook

TITLE_Y = SCREEN_HEIGHT // 2 - 150
LINE_PADDING = 8


@dataclass(frozen=True)
class OverlayLine:
    text: str
    font: str = "small"
    color: tuple[int, int, int] = Colors.WHITE


class OverlayRenderer:
    def __init__(self, fonts: FontBook) -> None:
        self._fonts = fonts

    def draw(self, surface: pygame.Surface, title: str, lines: list[OverlayLine], title_color=Colors.YELLOW) -> None:
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 165))
        surface.blit(shade, (0, 0))

        heading = self._fonts.large.render(title, True, title_color)
        surface.blit(heading, heading.get_rect(center=(SCREEN_WIDTH // 2, TITLE_Y)))

        y = TITLE_Y + 70
        for line in lines:
            font = self._fonts.get(line.font)
            image = font.render(line.text, True, line.color)
            surface.blit(image, image.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += font.get_height() + LINE_PADDING
