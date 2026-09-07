# Traffic Escape

2D highway dodging game built with Python and Pygame. The player drives a car on
a three-lane highway, switches lanes with the arrow keys and avoids slower
traffic moving in the same direction.

## Environment

The project uses a local virtual environment. Always run Python through it.

```bash
python -m venv .venv                        # only once
./.venv/Scripts/python.exe -m pip install -r requirements.txt
./.venv/Scripts/python.exe main.py          # run the game
```

`pygame-ce` is the dependency (it provides the `pygame` module and ships wheels
for the Python 3.14 interpreter installed on this machine).

## Layout

```
main.py                     entry point
traffic_escape/
  config.py                 screen, lane geometry, speeds, palette
  game.py                   game loop and state machine wiring
  world.py                  mutable race state (player, traffic, road, score)
  assets/                   procedural sprites, explosion frames, audio
  entities/                 player car, traffic car, explosion, road model
  systems/                  spawning, collision, scoring, high score storage
  rendering/                road, HUD and overlay renderers
  states/                   menu, playing, paused, crashing, game over
```

## Conventions

- Code, identifiers, docstrings and UI strings are in English.
- Comments only where the intent is not obvious from the code.
- Follow SOLID: one responsibility per module, depend on the abstractions in
  `traffic_escape/interfaces.py`, extend behaviour by adding classes instead of
  editing existing branches.
- All artwork and sound are generated at runtime; no binary assets in the repo.
- Commits follow Conventional Commits, written in English, one logical change
  per commit. Do not add co-author or generated-by trailers.
