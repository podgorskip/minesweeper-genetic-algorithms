import random
from collections.abc import Iterable, Iterator

from minesweeper.model.basic_types import Cell


class Board:
    """
    A fixed Minesweeper board: its size, the mine positions and a safe start cell.
    """

    def __init__(
        self,
        rows: int,
        cols: int,
        mines: Iterable[Cell],
        start: Cell | None = None,
    ) -> None:
        """
        :param rows: Number of rows.
        :type rows: int
        :param cols: Number of columns.
        :type cols: int
        :param mines: Positions of the mines.
        :type mines: Iterable[Cell]
        :param start: The cell clicked first; never a mine. Defaults to the centre.
        :type start: Cell | None
        """
        self.rows = rows
        self.cols = cols
        self.mines = frozenset(mines)
        self.start = start if start is not None else (rows // 2, cols // 2)
        if self.start in self.mines:
            raise ValueError("start cell must not be a mine")
        if not all(self.in_bounds(cell) for cell in self.mines):
            raise ValueError("mine out of bounds")
        self._counts = {
            cell: sum(n in self.mines for n in self.neighbors(cell))
            for cell in self.cells()
        }

    @classmethod
    def random(
        cls,
        rows: int,
        cols: int,
        n_mines: int,
        rng: random.Random,
        start: Cell | None = None,
    ) -> Board:
        """
        Create a board with ``n_mines`` mines placed uniformly at random,
        keeping the start cell mine-free.
        """
        start = start if start is not None else (rows // 2, cols // 2)
        free = [cell for cell in product_cells(rows, cols) if cell != start]
        return cls(rows, cols, rng.sample(free, n_mines), start)

    @classmethod
    def from_strings(cls, lines: list[str], start: Cell | None = None) -> Board:
        """
        Create a board from a picture, where ``*`` is a mine and anything else is empty.
        """
        mines = [
            (r, c)
            for r, line in enumerate(lines)
            for c, ch in enumerate(line)
            if ch == "*"
        ]
        return cls(len(lines), len(lines[0]), mines, start)

    def in_bounds(self, cell: Cell) -> bool:
        return 0 <= cell[0] < self.rows and 0 <= cell[1] < self.cols

    def cells(self) -> Iterator[Cell]:
        return product_cells(self.rows, self.cols)

    def neighbors(self, cell: Cell) -> Iterator[Cell]:
        r, c = cell
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                neighbor = (r + dr, c + dc)
                if neighbor != cell and self.in_bounds(neighbor):
                    yield neighbor

    def count(self, cell: Cell) -> int:
        """
        The number of mines around a cell.
        """
        return self._counts[cell]

    @property
    def n_safe(self) -> int:
        return self.rows * self.cols - len(self.mines)

    def __str__(self) -> str:
        return "\n".join(
            "".join(
                "*" if (r, c) in self.mines else str(self._counts[(r, c)] or ".")
                for c in range(self.cols)
            )
            for r in range(self.rows)
        )


def product_cells(rows: int, cols: int) -> Iterator[Cell]:
    for r in range(rows):
        for c in range(cols):
            yield (r, c)
