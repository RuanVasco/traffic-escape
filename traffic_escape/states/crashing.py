"""Plays the crash animation before the game over screen."""

from .base import BaseState, StateName


class CrashingState(BaseState):
    def update(self, delta: float) -> None:
        self.world.coast(delta)
        if self.world.crash_finished:
            self.host.set_state(StateName.GAME_OVER)
