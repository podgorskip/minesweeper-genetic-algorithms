from minesweeper.model.board import Board
from minesweeper.model.game import Game
from minesweeper.solver.rules import basic_rule, subset_rule
from minesweeper.solver.solve_result import SolveResult


def solve(board: Board) -> SolveResult:
    """
    Play the board using only safe deductions; the solver never guesses.
    It stops as soon as no rule finds a move.

    :param board: The board to play.
    :type board: Board
    :return: Whether the board was solved, with the fraction of safe cells opened.
    :rtype: SolveResult
    """
    game = Game(board)
    steps = {"basic": 0, "subset": 0}
    game.reveal(board.start)

    while not game.won:
        rule = "basic"
        safe, mines = basic_rule(game)
        if not safe and not mines:
            rule = "subset"
            safe, mines = subset_rule(game)
        if not safe and not mines:
            break
        steps[rule] += 1
        game.flagged |= mines
        for cell in safe:
            game.reveal(cell)

    opened = len(game.revealed)
    return SolveResult(game.won, opened / board.n_safe, opened, steps)
