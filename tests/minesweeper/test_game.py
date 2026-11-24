from minesweeper.model.board import Board
from minesweeper.model.game import Game


def test_flood_fill_and_win() -> None:
    board = Board.from_strings(["*..", "...", "..."], start=(2, 2))
    game = Game(board)
    game.reveal((2, 2))
    assert game.revealed == set(board.cells()) - {(0, 0)}
    assert game.won


def test_revealing_mine_explodes() -> None:
    game = Game(Board.from_strings(["*."], start=(0, 1)))
    game.reveal((0, 0))
    assert game.exploded
    assert not game.won


def test_flagged_cell_is_not_revealed() -> None:
    game = Game(Board.from_strings(["*."], start=(0, 1)))
    game.flag((0, 0))
    game.reveal((0, 0))
    assert not game.exploded
