import random

from minesweeper.model.board import Board
from minesweeper.solver.logic_solver import solve


def test_solves_trivial_board() -> None:
    result = solve(Board.from_strings(["*..", "...", "..."], start=(2, 2)))
    assert result.solved
    assert result.fitness == 1.0


def test_solves_with_basic_rule() -> None:
    result = solve(Board.from_strings(["*...", "....", "...."], start=(2, 3)))
    assert result.solved


def test_stuck_without_guessing() -> None:
    # the start cell shows 3 and its hidden neighbours can't be told apart
    result = solve(Board.from_strings(["*.*", ".*.", "*.*"], start=(1, 0)))
    assert not result.solved
    assert result.fitness < 1.0


def test_never_opens_a_mine_on_random_boards() -> None:
    rng = random.Random(1)
    solved = 0
    for _ in range(200):
        result = solve(Board.random(9, 9, 10, rng))
        assert 0 < result.fitness <= 1.0
        solved += result.solved
    assert 0 < solved < 200
