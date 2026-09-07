"""Colour helpers used by the procedural artwork."""

Color = tuple[int, int, int]


def lighten(color: Color, amount: float) -> Color:
    return tuple(min(255, int(c + (255 - c) * amount)) for c in color)


def darken(color: Color, amount: float) -> Color:
    return tuple(max(0, int(c * (1 - amount))) for c in color)
