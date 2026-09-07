"""Scrolling road markings that create the illusion of speed."""

from ..config import DASH_HEIGHT, DASH_SPACING, GUARDRAIL_SPACING, SCREEN_HEIGHT


class Road:
    def __init__(self) -> None:
        self.dash_positions = list(range(-DASH_SPACING, SCREEN_HEIGHT + DASH_SPACING, DASH_SPACING))
        self.post_positions = list(range(-GUARDRAIL_SPACING, SCREEN_HEIGHT + GUARDRAIL_SPACING, GUARDRAIL_SPACING))

    def update(self, road_speed: float) -> None:
        for index, y in enumerate(self.dash_positions):
            y += road_speed
            if y > SCREEN_HEIGHT:
                y = -DASH_HEIGHT - 40
            self.dash_positions[index] = y

        for index, y in enumerate(self.post_positions):
            y += road_speed
            if y > SCREEN_HEIGHT:
                y -= SCREEN_HEIGHT + 2 * GUARDRAIL_SPACING
            self.post_positions[index] = y
