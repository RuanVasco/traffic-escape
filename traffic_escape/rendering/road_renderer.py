"""Draws the highway: grass, shoulders, asphalt, markings and guardrails."""

import pygame

from ..config import (
    Colors,
    DASH_HEIGHT,
    LANE_DIVIDERS,
    ROAD_LEFT,
    ROAD_RIGHT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SHOULDER_WIDTH,
)
from ..entities.road import Road

GRASS_STRIPE = 26
GUARDRAIL_OFFSETS = (ROAD_LEFT - 22, ROAD_RIGHT + 18)


class RoadRenderer:
    def __init__(self) -> None:
        self._background = self._build_background()

    def draw(self, surface: pygame.Surface, road: Road) -> None:
        surface.blit(self._background, (0, 0))
        self._draw_lane_markings(surface, road)
        self._draw_guardrails(surface, road)

    @staticmethod
    def _build_background() -> pygame.Surface:
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        background.fill(Colors.GRASS)
        for y in range(0, SCREEN_HEIGHT, GRASS_STRIPE):
            pygame.draw.rect(background, Colors.GRASS_LIGHT, (0, y, SCREEN_WIDTH, GRASS_STRIPE // 2))

        pygame.draw.rect(background, Colors.SHOULDER, (ROAD_LEFT - SHOULDER_WIDTH, 0, SHOULDER_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(background, Colors.SHOULDER, (ROAD_RIGHT, 0, SHOULDER_WIDTH, SCREEN_HEIGHT))
        pygame.draw.rect(background, Colors.ASPHALT, (ROAD_LEFT, 0, ROAD_RIGHT - ROAD_LEFT, SCREEN_HEIGHT))
        for x in (ROAD_LEFT + 6, ROAD_RIGHT - 10):
            pygame.draw.rect(background, Colors.ASPHALT_DARK, (x, 0, 4, SCREEN_HEIGHT))
        pygame.draw.rect(background, Colors.EDGE_MARK, (ROAD_LEFT + 12, 0, 5, SCREEN_HEIGHT))
        pygame.draw.rect(background, Colors.EDGE_MARK, (ROAD_RIGHT - 17, 0, 5, SCREEN_HEIGHT))
        return background

    @staticmethod
    def _draw_lane_markings(surface: pygame.Surface, road: Road) -> None:
        for x in LANE_DIVIDERS:
            for y in road.dash_positions:
                pygame.draw.rect(surface, Colors.LANE_MARK, (x - 4, y, 8, DASH_HEIGHT), border_radius=3)

    @staticmethod
    def _draw_guardrails(surface: pygame.Surface, road: Road) -> None:
        for x in GUARDRAIL_OFFSETS:
            pygame.draw.rect(surface, Colors.GUARDRAIL, (x, 0, 5, SCREEN_HEIGHT))
            for y in road.post_positions:
                pygame.draw.rect(surface, Colors.GUARDRAIL_POST, (x - 1, y, 7, 12))
