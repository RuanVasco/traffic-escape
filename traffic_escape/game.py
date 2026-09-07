"""Game loop, dependency wiring and state machine."""

import random
from pathlib import Path

import pygame

from .assets.audio import create_audio
from .assets.explosion_frames import ExplosionFrameFactory
from .assets.scenery_sprites import ScenerySpriteFactory
from .assets.vehicle_sprites import VehicleSpriteFactory
from .config import FPS, HIGH_SCORE_FILE, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE
from .interfaces import HighScoreRepository
from .rendering.fonts import FontBook
from .rendering.hud import HudRenderer
from .rendering.overlay import OverlayRenderer
from .rendering.road_renderer import RoadRenderer
from .rendering.scene import SceneRenderer
from .states import CrashingState, GameOverState, MenuState, PausedState, PlayingState, StateName
from .systems.scoring import FileHighScoreRepository
from .world import RaceWorld


class Game:
    def __init__(self, high_scores: HighScoreRepository | None = None, seed: int | None = None) -> None:
        pygame.init()
        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self._clock = pygame.time.Clock()
        self._running = False

        rng = random.Random(seed)
        fonts = FontBook()
        self.world = RaceWorld(
            sprites=VehicleSpriteFactory(),
            scenery=ScenerySpriteFactory(),
            explosions=ExplosionFrameFactory(),
            audio=create_audio(),
            high_scores=high_scores or FileHighScoreRepository(Path(__file__).resolve().parent.parent / HIGH_SCORE_FILE),
            rng=rng,
        )
        self.scene = SceneRenderer(RoadRenderer(), HudRenderer(fonts), rng)
        self.overlay = OverlayRenderer(fonts)

        self._states = {
            StateName.MENU: MenuState(self),
            StateName.PLAYING: PlayingState(self),
            StateName.PAUSED: PausedState(self),
            StateName.CRASHING: CrashingState(self),
            StateName.GAME_OVER: GameOverState(self),
        }
        self._state = self._states[StateName.MENU]
        self._state.enter()

    def set_state(self, name: str) -> None:
        self._state = self._states[name]
        self._state.enter()

    def run(self) -> None:
        self._running = True
        while self._running:
            delta = self._clock.tick(FPS) / 1000.0
            self._process_events()
            self._state.update(delta)
            self._state.draw(self._screen)
            pygame.display.flip()
        pygame.quit()

    def _process_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self._running = False
                return
            self._state.handle_event(event)
