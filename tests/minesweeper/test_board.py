import random

import pytest

from minesweeper.model.board import Board


def test_counts_and_str() -> None:
    board = Board.from_strings(["*..", "...", "..."], start=(2, 2))
    assert board.count((1, 1)) == 1
    assert board.count((2, 2)) == 0
    assert board.n_safe == 8
    assert str(board).splitlines()[0] == "*1."


def test_start_cannot_be_mine() -> None:
    with pytest.raises(ValueError):
        Board(3, 3, [(1, 1)], start=(1, 1))


def test_mine_must_be_in_bounds() -> None:
    with pytest.raises(ValueError):
        Board(3, 3, [(3, 0)])


def test_random_board_keeps_start_safe_and_mine_count() -> None:
    rng = random.Random(0)
    for _ in range(50):
        board = Board.random(9, 9, 10, rng)
        assert len(board.mines) == 10
        assert board.start not in board.mines
