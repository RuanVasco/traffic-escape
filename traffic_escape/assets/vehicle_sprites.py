"""Draws vehicle sprites at runtime, seen from above and facing up."""

import pygame

from ..config import Colors
from .shading import Color, darken, lighten
from .vehicle_kinds import VehicleKind

GLASS = (44, 62, 84)
GLASS_HIGHLIGHT = (92, 124, 156)
TYRE = (28, 28, 32)
HEADLIGHT = (255, 246, 200)
TAILLIGHT = (208, 52, 48)
CARGO = (222, 224, 228)
CARGO_LINE = (196, 198, 204)


class BodyPainter:
    """Paints the parts that differ between vehicle categories."""

    def paint(self, surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        raise NotImplementedError


class CarBody(BodyPainter):
    def paint(self, surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        height = body.height
        pygame.draw.rect(
            surface, GLASS,
            (body.x + 8, body.y + int(height * 0.20), body.width - 16, int(height * 0.16)),
            border_radius=8,
        )
        roof = pygame.Rect(body.x + 5, body.y + int(height * 0.38), body.width - 10, int(height * 0.26))
        pygame.draw.rect(surface, darken(color, 0.12), roof, border_radius=8)
        pygame.draw.rect(
            surface, GLASS,
            (body.x + 8, body.y + int(height * 0.68), body.width - 16, int(height * 0.13)),
            border_radius=8,
        )
        pygame.draw.line(
            surface, GLASS_HIGHLIGHT,
            (body.x + 12, body.y + int(height * 0.22)),
            (body.right - 12, body.y + int(height * 0.22)), 2,
        )


class PickupBody(CarBody):
    def paint(self, surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        super().paint(surface, body, color)
        bed = pygame.Rect(body.x + 5, body.y + int(body.height * 0.66), body.width - 10, int(body.height * 0.28))
        pygame.draw.rect(surface, darken(color, 0.45), bed, border_radius=6)


class TruckBody(BodyPainter):
    def paint(self, surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        cabin = self._paint_cabin(surface, body, color)
        cargo = pygame.Rect(body.x + 2, cabin.bottom + 4, body.width - 4, body.height - cabin.height - 12)
        pygame.draw.rect(surface, CARGO, cargo, border_radius=8)
        pygame.draw.rect(surface, darken(color, 0.4), cargo, width=2, border_radius=8)
        for y in range(cargo.y + 12, cargo.bottom - 6, 16):
            pygame.draw.line(surface, CARGO_LINE, (cargo.x + 6, y), (cargo.right - 6, y), 2)

    @staticmethod
    def _paint_cabin(surface: pygame.Surface, body: pygame.Rect, color: Color) -> pygame.Rect:
        cabin = pygame.Rect(body.x, body.y, body.width, int(body.height * 0.30))
        pygame.draw.rect(surface, darken(color, 0.15), cabin, border_radius=12)
        pygame.draw.rect(surface, GLASS, (cabin.x + 8, cabin.y + 8, cabin.width - 16, 18), border_radius=6)
        return cabin


class BusBody(TruckBody):
    def paint(self, surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        cabin = self._paint_cabin(surface, body, color)
        saloon = pygame.Rect(body.x + 2, cabin.bottom + 4, body.width - 4, body.height - cabin.height - 12)
        pygame.draw.rect(surface, darken(color, 0.08), saloon, border_radius=8)
        for y in range(saloon.y + 8, saloon.bottom - 16, 22):
            pygame.draw.rect(surface, GLASS, (saloon.x + 3, y, 9, 15), border_radius=3)
            pygame.draw.rect(surface, GLASS, (saloon.right - 12, y, 9, 15), border_radius=3)


class VehicleSpriteFactory:
    """Builds and caches one surface per colour, kind and role."""

    def __init__(self) -> None:
        self._painters: dict[str, BodyPainter] = {
            "car": CarBody(),
            "pickup": PickupBody(),
            "truck": TruckBody(),
            "bus": BusBody(),
        }
        self._cache: dict[tuple, pygame.Surface] = {}

    def register(self, kind_name: str, painter: BodyPainter) -> None:
        self._painters[kind_name] = painter

    def create(self, color: Color, kind: VehicleKind, is_player: bool = False) -> pygame.Surface:
        key = (color, kind.name, is_player)
        if key not in self._cache:
            self._cache[key] = self._render(color, kind, is_player)
        return self._cache[key]

    def _render(self, color: Color, kind: VehicleKind, is_player: bool) -> pygame.Surface:
        surface = pygame.Surface((kind.width, kind.height + 8), pygame.SRCALPHA)
        body = pygame.Rect(6, 2, kind.width - 12, kind.height)

        self._paint_shadow(surface, body)
        self._paint_wheels(surface, kind)
        pygame.draw.rect(surface, color, body, border_radius=14)
        pygame.draw.rect(surface, darken(color, 0.35), body, width=2, border_radius=14)
        pygame.draw.rect(surface, lighten(color, 0.22), (body.x + 4, body.y + 10, 6, body.height - 24), border_radius=3)

        self._painters[kind.name].paint(surface, body, color)
        self._paint_lights(surface, body)
        if is_player:
            self._paint_racing_trim(surface, body, color)
        return surface

    @staticmethod
    def _paint_shadow(surface: pygame.Surface, body: pygame.Rect) -> None:
        shadow = pygame.Surface((body.width, body.height), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 70), shadow.get_rect())
        surface.blit(shadow, (body.x + 2, body.y + 8))

    @staticmethod
    def _paint_wheels(surface: pygame.Surface, kind: VehicleKind) -> None:
        length = int(kind.height * 0.17)
        for y in (int(kind.height * 0.16), int(kind.height * 0.72)):
            pygame.draw.rect(surface, TYRE, (2, y, 8, length), border_radius=3)
            pygame.draw.rect(surface, TYRE, (kind.width - 10, y, 8, length), border_radius=3)

    @staticmethod
    def _paint_lights(surface: pygame.Surface, body: pygame.Rect) -> None:
        pygame.draw.rect(surface, HEADLIGHT, (body.x + 7, body.y + 3, 13, 7), border_radius=3)
        pygame.draw.rect(surface, HEADLIGHT, (body.right - 20, body.y + 3, 13, 7), border_radius=3)
        pygame.draw.rect(surface, TAILLIGHT, (body.x + 7, body.bottom - 10, 13, 7), border_radius=3)
        pygame.draw.rect(surface, TAILLIGHT, (body.right - 20, body.bottom - 10, 13, 7), border_radius=3)

    @staticmethod
    def _paint_racing_trim(surface: pygame.Surface, body: pygame.Rect, color: Color) -> None:
        pygame.draw.rect(surface, Colors.WHITE, (body.centerx - 11, body.y + 6, 7, body.height - 12))
        pygame.draw.rect(surface, Colors.WHITE, (body.centerx + 4, body.y + 6, 7, body.height - 12))
        pygame.draw.rect(surface, darken(color, 0.5), (body.x - 2, body.bottom - 16, body.width + 4, 7), border_radius=3)
