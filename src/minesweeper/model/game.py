from minesweeper.model.basic_types import Cell
from minesweeper.model.board import Board


class Game:
    """
    The playable state of a board: which cells are revealed and flagged.
    """

    def __init__(self, board: Board) -> None:
        self.board = board
        self.revealed: set[Cell] = set()
        self.flagged: set[Cell] = set()
        self.exploded = False

    def reveal(self, cell: Cell) -> None:
        """
        Reveal a cell; revealing a zero cell flood-fills its neighbours.
        """
        if cell in self.revealed or cell in self.flagged:
            return
        if cell in self.board.mines:
            self.exploded = True
            return
        stack = [cell]
        while stack:
            current = stack.pop()
            if current in self.revealed:
                continue
            self.revealed.add(current)
            if self.board.count(current) == 0:
                stack.extend(
                    n
                    for n in self.board.neighbors(current)
                    if n not in self.revealed and n not in self.flagged
                )

    def flag(self, cell: Cell) -> None:
        if cell not in self.revealed:
            self.flagged.add(cell)

    @property
    def won(self) -> bool:
        return not self.exploded and len(self.revealed) == self.board.n_safe
