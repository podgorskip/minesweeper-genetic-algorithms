from dataclasses import dataclass, field


@dataclass
class SolveResult:
    """
    The outcome of a logic solver run on one board.

    :param solved: Whether every safe cell was opened without guessing.
    :type solved: bool
    :param fitness: The fraction of safe cells opened (1.0 means solvable).
    :type fitness: float
    :param opened: The number of safe cells opened.
    :type opened: int
    :param steps: How many deduction steps each rule made.
    :type steps: dict[str, int]
    """

    solved: bool
    fitness: float
    opened: int
    steps: dict[str, int] = field(default_factory=lambda: {"basic": 0, "subset": 0})
