# Evolving Solvable Minesweeper Boards

Minesweeper boards generated at random often force the player to guess. The goal of this project is to use evolutionary algorithms to generate boards that can be solved by pure logic, and to compare two ways of doing it: evolving the board directly and evolving a neural-network generator of boards. See `minesweeper_project_plan.md` for the full plan.

New to Minesweeper? Start with the illustrated introduction in `docs/README.md`.

## Structure

  * `docs` - illustrated explanation of the game and the solver (images regenerated with `uv run examples/minesweeper/generate_docs_images.py`),
  * `src/minesweeper/model` - the board and the game rules,
  * `src/minesweeper/solver` - the logic solver (the fitness judge): the basic and the subset rules,
  * `tests` - unit tests,
  * `examples` - runnable experiments.

## Progress

  * [x] board and rules
  * [x] first logic solver (basic and subset rules)
  * [x] random-board baseline: `uv run examples/minesweeper/random_baseline.py`
  * [ ] Method A - direct encoding GA
  * [ ] Method B - neural-network generator
  * [ ] experiments and statistics

## Usage

Refer to the `examples/` directory for examples of the API.

The project depends on a fairly recent Python interpreter (version >= `3.14` is required). All dependencies are listed in `pyproject.toml`. Use [uv](https://docs.astral.sh/uv/) to manage the Python version and dependencies automatically.

Short reminder:
- `uv run <command>` will run `<command>` within the correct environment;
- alternatively: `uv sync` will synchronize the environment and then `source .venv/bin/activate` will activate the Python environment.

## Unit Tests

The `tests` folder contains unit tests written using `pytest`.
Run them via `uv run pytest`.
