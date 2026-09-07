"""Score panel drawn on top of the race."""

import pygame

from ..config import Colors, ROAD_SPEED_MAX, ROAD_SPEED_START, SCREEN_WIDTH, SPEEDOMETER_RATIO
from .fonts import FontBook

PANEL_HEIGHT = 52
BAR = pygame.Rect(14, 42, 200, 6)


class HudRenderer:
    def __init__(self, fonts: FontBook) -> None:
        self._fonts = fonts

    def draw(self, surface: pygame.Surface, world) -> None:
        panel = pygame.Surface((SCREEN_WIDTH, PANEL_HEIGHT), pygame.SRCALPHA)
        panel.fill((0, 0, 0, 130))
        surface.blit(panel, (0, 0))

        font = self._fonts.small
        entries = (
            (f"SCORE {world.score.value:06d}", 14),
            (f"{int(world.road_speed * SPEEDOMETER_RATIO):3d} km/h", 235),
            (f"LEVEL {world.score.level}", 345),
            (f"BEST {world.high_score:06d}", 445),
        )
        for text, x in entries:
            surface.blit(font.render(text, True, Colors.WHITE), (x, 16))

        self._draw_speed_bar(surface, world.road_speed)

    @staticmethod
    def _draw_speed_bar(surface: pygame.Surface, road_speed: float) -> None:
        span = ROAD_SPEED_MAX - ROAD_SPEED_START
        filled = max(0.0, min(1.0, (road_speed - ROAD_SPEED_START) / span))
        pygame.draw.rect(surface, (60, 62, 70), BAR, border_radius=3)
        pygame.draw.rect(surface, Colors.YELLOW, (BAR.x, BAR.y, int(BAR.width * filled), BAR.height), border_radius=3)
