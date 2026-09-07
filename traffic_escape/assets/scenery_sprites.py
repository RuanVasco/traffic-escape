"""Roadside decorations drawn at runtime."""

import pygame

from ..config import Colors, FONT_NAMES


class ScenerySpriteFactory:
    def __init__(self) -> None:
        self._tree: pygame.Surface | None = None
        self._signs: list[pygame.Surface] | None = None

    def tree(self) -> pygame.Surface:
        if self._tree is None:
            self._tree = self._render_tree()
        return self._tree

    def signs(self) -> list[pygame.Surface]:
        if self._signs is None:
            self._signs = [self._render_speed_sign(), self._render_warning_sign(), self._render_route_sign()]
        return self._signs

    @staticmethod
    def _render_tree() -> pygame.Surface:
        surface = pygame.Surface((58, 62), pygame.SRCALPHA)
        pygame.draw.ellipse(surface, (0, 0, 0, 60), (10, 44, 40, 14))
        pygame.draw.rect(surface, (92, 66, 44), (26, 34, 7, 20), border_radius=2)
        for x, y, radius, color in ((20, 28, 15, (38, 92, 48)), (38, 26, 15, (46, 110, 56)), (29, 18, 17, (56, 128, 64))):
            pygame.draw.circle(surface, color, (x, y), radius)
        return surface

    @staticmethod
    def _new_post() -> pygame.Surface:
        surface = pygame.Surface((52, 66), pygame.SRCALPHA)
        pygame.draw.rect(surface, Colors.GUARDRAIL_POST, (24, 30, 5, 34))
        return surface

    @classmethod
    def _render_speed_sign(cls) -> pygame.Surface:
        surface = cls._new_post()
        pygame.draw.circle(surface, Colors.WHITE, (26, 22), 20)
        pygame.draw.circle(surface, (198, 46, 42), (26, 22), 20, 5)
        label = pygame.font.SysFont(FONT_NAMES, 17, bold=True).render("110", True, Colors.BLACK)
        surface.blit(label, label.get_rect(center=(26, 22)))
        return surface

    @classmethod
    def _render_warning_sign(cls) -> pygame.Surface:
        surface = cls._new_post()
        points = [(26, 2), (48, 34), (4, 34)]
        pygame.draw.polygon(surface, Colors.YELLOW, points)
        pygame.draw.polygon(surface, Colors.BLACK, points, 3)
        pygame.draw.rect(surface, Colors.BLACK, (24, 12, 5, 12))
        pygame.draw.rect(surface, Colors.BLACK, (24, 26, 5, 4))
        return surface

    @classmethod
    def _render_route_sign(cls) -> pygame.Surface:
        surface = cls._new_post()
        pygame.draw.rect(surface, (34, 106, 62), (2, 4, 48, 30), border_radius=4)
        pygame.draw.rect(surface, Colors.WHITE, (2, 4, 48, 30), 2, border_radius=4)
        label = pygame.font.SysFont(FONT_NAMES, 12, bold=True).render("BR-101", True, Colors.WHITE)
        surface.blit(label, label.get_rect(center=(26, 19)))
        return surface
