import random

from minesweeper.model.board import Board
from minesweeper.solver.logic_solver import solve

ROWS = 9
COLS = 9
MINES = 10
N_BOARDS = 1000
SEED = 0


def main() -> None:
    rng = random.Random(SEED)
    results = [solve(Board.random(ROWS, COLS, MINES, rng)) for _ in range(N_BOARDS)]
    solvable = sum(result.solved for result in results)
    mean_fitness = sum(result.fitness for result in results) / N_BOARDS
    print(f"{ROWS}x{COLS} with {MINES} mines, {N_BOARDS} random boards")
    print(f"solvable without guessing: {solvable / N_BOARDS:.1%}")
    print(f"mean fraction of safe cells opened: {mean_fitness:.3f}")


if __name__ == "__main__":
    main()
