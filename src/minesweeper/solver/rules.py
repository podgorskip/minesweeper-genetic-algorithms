from minesweeper.model.basic_types import Cell
from minesweeper.model.game import Game

type Constraint = tuple[frozenset[Cell], int]
"""Hidden neighbours of a revealed number and the number of mines still missing there."""

type Deduction = tuple[set[Cell], set[Cell]]
"""Cells deduced to be safe and cells deduced to be mines."""


def constraints(game: Game) -> list[Constraint]:
    """
    For each revealed number touching hidden cells, collect its hidden neighbours
    and the number of mines that are still missing among them.
    """
    result: list[Constraint] = []
    for cell in game.revealed:
        neighbors = list(game.board.neighbors(cell))
        hidden = frozenset(
            n for n in neighbors if n not in game.revealed and n not in game.flagged
        )
        if hidden:
            missing = game.board.count(cell) - sum(n in game.flagged for n in neighbors)
            result.append((hidden, missing))
    return result


def basic_rule(game: Game) -> Deduction:
    """
    If a number has no mines missing, all its hidden neighbours are safe;
    if it misses as many mines as it has hidden neighbours, all of them are mines.
    """
    safe: set[Cell] = set()
    mines: set[Cell] = set()
    for hidden, missing in constraints(game):
        if missing == 0:
            safe |= hidden
        elif missing == len(hidden):
            mines |= hidden
    return safe, mines


def subset_rule(game: Game) -> Deduction:
    """
    If the hidden cells of constraint A are a subset of those of constraint B,
    then the difference B - A holds exactly ``missing(B) - missing(A)`` mines.
    """
    unique = list(set(constraints(game)))
    safe: set[Cell] = set()
    mines: set[Cell] = set()
    for a, missing_a in unique:
        for b, missing_b in unique:
            if a < b:
                difference, missing = b - a, missing_b - missing_a
                if missing == 0:
                    safe |= difference
                elif missing == len(difference):
                    mines |= difference
    return safe, mines
