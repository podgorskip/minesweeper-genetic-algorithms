import random
from itertools import combinations
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.patches import Rectangle

from minesweeper.model.basic_types import Cell
from minesweeper.model.board import Board, product_cells
from minesweeper.model.game import Game
from minesweeper.solver.logic_solver import solve
from minesweeper.solver.rules import basic_rule, subset_rule

DOCS_DIR = Path(__file__).resolve().parents[2] / "docs"
NUMBER_COLORS = {
    1: "#1f4fd8",
    2: "#2e8b3d",
    3: "#d62828",
    4: "#1a1a7a",
    5: "#7a1a1a",
    6: "#1a7a7a",
    7: "#222222",
    8: "#777777",
}
HIDDEN = "#b8c0cc"
REVEALED = "#f4f1ea"
HIGHLIGHT = "#ffd166"


def draw_board(
    ax: Axes,
    board: Board,
    game: Game | None = None,
    show_all: bool = False,
    highlight: set[Cell] | None = None,
    title: str = "",
) -> None:
    """
    Draw a board; hidden cells are grey, flags are red triangles. With
    ``show_all`` every cell is uncovered (mines included).
    """
    highlight = highlight or set()
    for r, c in board.cells():
        cell = (r, c)
        uncovered = show_all or (game is not None and cell in game.revealed)
        face = REVEALED if uncovered else HIDDEN
        if cell in highlight:
            face = HIGHLIGHT
        ax.add_patch(
            Rectangle((c, board.rows - 1 - r), 1, 1, fc=face, ec="#7d8794", lw=1)
        )
        center = (c + 0.5, board.rows - 1 - r + 0.5)
        if uncovered and cell in board.mines:
            ax.plot(*center, "o", color="#222", ms=11)
        elif uncovered and board.count(cell) > 0:
            n = board.count(cell)
            ax.text(
                *center,
                str(n),
                color=NUMBER_COLORS[n],
                ha="center",
                va="center",
                fontsize=15,
                fontweight="bold",
            )
        elif game is not None and cell in game.flagged:
            ax.plot(*center, "^", color="#d62828", ms=11)
    if show_all and board.start is not None:
        r, c = board.start
        ax.add_patch(
            Rectangle(
                (c + 0.06, board.rows - 1 - r + 0.06),
                0.88,
                0.88,
                fc="none",
                ec="#2e8b3d",
                lw=3,
            )
        )
    ax.set_xlim(0, board.cols)
    ax.set_ylim(0, board.rows)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, fontsize=11)


def rules_figure() -> None:
    board = Board.from_strings(
        ["..1*1.", "..1111", "112*21", "1*2*2.", "11111."], start=(0, 0)
    )
    # make the picture consistent: rebuild from mines so numbers are right
    board = Board(5, 6, [(0, 3), (2, 3), (3, 1), (3, 3)], start=(0, 0))
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    draw_board(
        axes[0],
        board,
        show_all=True,
        highlight={(3, 2)},
        title="A finished board: black dots are mines,\ngreen frame is the safe first click",
    )
    focus = (3, 2)
    for n in board.neighbors(focus):
        axes[0].add_patch(
            Rectangle(
                (n[1] + 0.04, board.rows - 1 - n[0] + 0.04),
                0.92,
                0.92,
                fc="none",
                ec="#d62828" if n in board.mines else "#7d8794",
                lw=2.5 if n in board.mines else 1,
                ls="--",
            )
        )
    axes[1].axis("off")
    axes[1].text(
        0,
        0.97,
        "How to read it",
        fontsize=15,
        fontweight="bold",
        va="top",
        transform=axes[1].transAxes,
    )
    axes[1].text(
        0,
        0.88,
        "• Every cell is either a mine or safe.\n"
        "• You click a hidden cell. A mine ends the game.\n"
        "• A safe cell shows a number: how many of its\n"
        "  8 neighbours are mines.\n"
        f"• The yellow cell shows {board.count(focus)} - its dashed red\n"
        "  neighbours are mines.\n"
        "• A cell showing nothing has 0 mine neighbours,\n"
        "  so its neighbours open automatically.\n"
        "• You win by opening every safe cell.\n\n"
        "Our setting: 9x9 board, 10 mines, first click\n"
        "always safe.",
        fontsize=11.5,
        va="top",
        linespacing=1.5,
        transform=axes[1].transAxes,
    )
    fig.tight_layout()
    fig.savefig(DOCS_DIR / "01_rules.png", dpi=140)
    plt.close(fig)


def find_boards() -> tuple[Board, Board]:
    """
    Find a board solved with the help of the subset rule and a board on which
    the solver gets stuck after making real progress.
    """
    solvable: Board | None = None
    stuck: Board | None = None
    rng = random.Random(3)
    while solvable is None or stuck is None:
        board = Board.random(9, 9, 10, rng)
        result = solve(board)
        if (
            solvable is None
            and result.solved
            and 1 <= result.steps["subset"] <= 3
            and result.steps["basic"] >= 3
        ):
            solvable = board
        if stuck is None and not result.solved and result.fitness > 0.55:
            stuck = board
    return solvable, stuck


def replay(board: Board) -> list[tuple[Game, str, set[Cell]]]:
    """
    Replay the solver, recording a snapshot after every deduction step:
    the game state, the rule used and the cells that step touched.
    """
    game = Game(board)
    game.reveal(board.start)
    frames = [(snapshot(game), "start: click the safe cell", {board.start})]
    while not game.won:
        rule = "basic rule"
        safe, mines = basic_rule(game)
        if not safe and not mines:
            rule = "subset rule"
            safe, mines = subset_rule(game)
        if not safe and not mines:
            frames.append((snapshot(game), "stuck: only a guess is left", set()))
            break
        game.flagged |= mines
        for cell in safe:
            game.reveal(cell)
        frames.append((snapshot(game), rule, safe | mines))
    return frames


def snapshot(game: Game) -> Game:
    copy = Game(game.board)
    copy.revealed = set(game.revealed)
    copy.flagged = set(game.flagged)
    return copy


def solver_figure(board: Board, name: str, suptitle: str) -> None:
    frames = replay(board)
    if len(frames) > 6:  # keep the picture readable: first, subset steps, then the last
        subset = [i for i, f in enumerate(frames) if f[1] == "subset rule"]
        keep = {0, 1, len(frames) - 1} | set(subset[:2])
        for i in range(2, len(frames)):
            if len(keep) >= 6:
                break
            keep.add(i)
        frames = [frames[i] for i in sorted(keep)]
    cols = 3
    rows = (len(frames) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4.2 * cols, 4.3 * rows))
    flat = list(axes.flat)
    for ax, (game, rule, touched) in zip(flat, frames):
        draw_board(
            ax,
            board,
            game,
            highlight=touched - game.flagged
            if rule != "stuck: only a guess is left"
            else None,
            title=f"{rule}\n{len(game.revealed)}/{board.n_safe} safe cells open",
        )
    for ax in flat[len(frames) :]:
        ax.axis("off")
    fig.suptitle(suptitle, fontsize=14, fontweight="bold")
    fig.text(
        0.5,
        0.005,
        "grey = hidden, red triangle = deduced mine, yellow = cells decided in that step",
        ha="center",
        fontsize=10,
    )
    fig.tight_layout(rect=(0, 0.02, 1, 0.95))
    fig.savefig(DOCS_DIR / name, dpi=130)
    plt.close(fig)


def find_forced_guess() -> tuple[Board, Board]:
    """
    Find a small board where the solver ends with two hidden cells, one of them
    a mine, plus the twin board with the mine moved to the other cell. Both
    boards look identical to the player.
    """
    start = (0, 0)
    for size, n_mines in ((4, 2), (4, 3), (4, 4), (5, 3)):
        free = [c for c in product_cells(size, size) if c != start]
        for mines in combinations(free, n_mines):
            board = Board(size, size, mines, start)
            game = replay(board)[-1][0]
            hidden = [
                c
                for c in board.cells()
                if c not in game.revealed and c not in game.flagged
            ]
            if len(hidden) != 2 or sum(c in board.mines for c in hidden) != 1:
                continue
            mine = next(c for c in hidden if c in board.mines)
            other = next(c for c in hidden if c != mine)
            twin = Board(size, size, (board.mines - {mine}) | {other}, start)
            if all(board.count(c) == twin.count(c) for c in game.revealed):
                return board, twin
    raise RuntimeError("no forced guess found")


def fifty_fifty_figure() -> None:
    board, twin = find_forced_guess()
    game = replay(board)[-1][0]
    hidden = {
        c for c in board.cells() if c not in game.revealed and c not in game.flagged
    }
    fig, axes = plt.subplots(1, 3, figsize=(13, 4.8))
    draw_board(
        axes[0],
        board,
        game,
        highlight=hidden,
        title="What the player sees\n(yellow: one mine, two candidates)",
    )
    draw_board(axes[1], board, show_all=True, title="Possible truth 1")
    draw_board(axes[2], twin, show_all=True, title="Possible truth 2")
    fig.suptitle(
        "A forced guess: both boards look identical to the player, "
        "so logic cannot tell which yellow cell is the mine",
        fontsize=13,
        fontweight="bold",
    )
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(DOCS_DIR / "04_forced_guess.png", dpi=130)
    plt.close(fig)


def baseline_figure() -> None:
    rng = random.Random(0)
    results = [solve(Board.random(9, 9, 10, rng)) for _ in range(1000)]
    fitness = [r.fitness for r in results]
    solvable = sum(r.solved for r in results) / len(results)
    fig, ax = plt.subplots(figsize=(8, 4.2))
    ax.hist(fitness, bins=25, color="#5b7db1", edgecolor="white")
    stuck_at_start = sum(f < 0.1 for f in fitness)
    ax.annotate(
        f"{stuck_at_start} boards: the first click shows a number,\n"
        "so nothing opens and the solver cannot start",
        xy=(0.04, stuck_at_start * 0.8),
        xytext=(0.2, stuck_at_start * 0.8),
        arrowprops={"arrowstyle": "->"},
        fontsize=10,
        va="center",
    )
    ax.set_xlabel("fitness = fraction of safe cells the solver opens without guessing")
    ax.set_ylabel("number of random boards (out of 1000)")
    ax.set_title(
        f"Random 9x9 boards, 10 mines: only {solvable:.0%} are fully solvable "
        "(the bar at 1.0)\n- this is what evolution has to improve",
        fontsize=11,
    )
    fig.tight_layout()
    fig.savefig(DOCS_DIR / "05_random_baseline.png", dpi=140)
    plt.close(fig)


def main() -> None:
    DOCS_DIR.mkdir(exist_ok=True)
    rules_figure()
    solvable, stuck = find_boards()
    solver_figure(
        solvable,
        "02_solver_solves.png",
        "The logic solver solves a board with no guessing",
    )
    solver_figure(
        stuck, "03_solver_stuck.png", "The solver gets stuck - this board needs a guess"
    )
    fifty_fifty_figure()
    baseline_figure()
    print(f"images written to {DOCS_DIR}")


if __name__ == "__main__":
    main()
