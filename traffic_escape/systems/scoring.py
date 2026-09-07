"""Score tracking and high score persistence."""

from pathlib import Path

from ..config import OVERTAKE_BONUS, POINTS_PER_DISTANCE, POINTS_PER_LEVEL
from ..interfaces import HighScoreRepository


class Score:
    def __init__(self) -> None:
        self.points = 0.0
        self.overtakes = 0

    @property
    def level(self) -> int:
        return 1 + int(self.points // POINTS_PER_LEVEL)

    @property
    def value(self) -> int:
        return int(self.points)

    def add_distance(self, road_speed: float, delta: float) -> None:
        self.points += road_speed * delta * POINTS_PER_DISTANCE

    def add_overtake(self) -> None:
        self.overtakes += 1
        self.points += OVERTAKE_BONUS * self.level


class FileHighScoreRepository(HighScoreRepository):
    def __init__(self, path: Path) -> None:
        self._path = path

    def load(self) -> int:
        try:
            return int(self._path.read_text(encoding="utf-8").strip())
        except (OSError, ValueError):
            return 0

    def save(self, score: int) -> None:
        try:
            self._path.write_text(str(int(score)), encoding="utf-8")
        except OSError:
            pass


class InMemoryHighScoreRepository(HighScoreRepository):
    def __init__(self, score: int = 0) -> None:
        self._score = score

    def load(self) -> int:
        return self._score

    def save(self, score: int) -> None:
        self._score = int(score)
