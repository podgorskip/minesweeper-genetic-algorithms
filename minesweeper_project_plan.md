# Project plan: Evolving Solvable Minesweeper Boards (Topic #15)

## 1. The idea in one paragraph

In Minesweeper, a randomly generated board often forces the player to **guess**
(for example a 50/50 situation). That is frustrating and unfair. We want to use
**evolutionary algorithms** to *generate* boards that can be solved **using pure
logic, without any guessing**. We will try two different ways of generating boards
and compare them with a statistical test. Then, as a bonus, we will try to
generate boards of a chosen **difficulty**.

---

## 2. What we will do (the goals)

1. **Build a logic solver.** A program that plays Minesweeper using only safe
   deductions and tells us: "this board is solvable without guessing" or
   "the solver got stuck".
2. **Method A - direct encoding.** A genetic algorithm (GA) where one individual
   *is* a board (the list of mine positions). Mutation moves a mine; crossover mixes
   two boards.
3. **Method B - neural-network generator.** A small neural network (evolved with
   neuroevolution, e.g. NEAT or a simple evolved MLP) that *produces* a board:
   for each cell it outputs "how likely is a mine here", and we place the mines
   on the top-scoring cells. Here an individual is a *network*, not a board.
4. **Baseline - random boards.** Boards with random mines, to show that evolution
   actually helps.
5. **Compare A vs B vs random** with the same budget and a statistical test.
6. **Bonus:** evolve boards for a *target difficulty* (easy / medium / hard
   solvable boards), and make a small visual demo. Further optional
   extensions: **#BON1** novelty search, **#BON2** multiobjective (NSGA-II),
   **#BON3** coevolution (details in 4.8).

---

## 3. Why we are doing it

- **A real problem:** game designers and puzzle generators need levels that are
  guaranteed fair. Guessing-free Minesweeper boards are exactly that.
- **Hard for plain random search:** on bigger boards, random boards are rarely
  fully solvable, so a smarter search (evolution) makes sense.
- **Interesting comparison:** is it better to evolve *the board itself*, or to
  evolve a *generator* that can then make many boards quickly? The generator is
  more expensive to train, but afterwards it produces boards instantly.
- **Easy to measure:** "solvable or not" is a clear yes/no, so the statistics are
  simple and clean.
- **Good demo:** boards are visual, so the final presentation can show them.

---

## 4. How we will do it (step by step)

### 4.1 Board and rules
- Start with **9x9 with 10 mines**, later maybe **16x16 with 40 mines**.
- The first click is always safe (we fix a start cell, e.g. the centre, and
  keep it mine-free) so that every board has a fair start.

### 4.2 The solver (the "judge")
The solver repeatedly applies simple logic:
1. **Basic rule:** if a number equals the count of hidden neighbours, all of them
   are mines; if a number already has all its mines flagged, the rest are safe.
2. **Subset rule:** compare two neighbouring numbers to deduce more cells.
3. *(Optional)* **Full constraint check:** try all consistent mine placements
   around the frontier to find cells that are safe/mined in *every* case.

If the solver opens every safe cell without guessing -> board is **solvable**.

### 4.3 Fitness function (how we score a board)
Simple version:

> fitness = fraction of safe cells that the solver opens without guessing
> (1.0 = perfectly solvable)

For the bonus (difficulty), we also measure *how hard* the solution is, e.g.
how many steps need the harder rules (subset / constraint check).

### 4.4 Method A - direct encoding
- Individual = set of 10 mine coordinates (the count of mines is fixed).
- Mutation: move one mine to another free cell.
- Crossover: take some mines from parent 1, rest from parent 2, repair if the
  count is wrong.
- Selection: tournament selection, a bit of elitism.

### 4.5 Method B - neural-network generator
- Individual = small neural network (a few dozen weights).
- Input: cell position (x, y), distance to centre/start cell (and maybe a random
  noise value so the same network can make *different* boards).
- Output: a "mine score" for each cell. The 10 cells with the highest scores
  become mines.
- Fitness = average solvability of several boards made by that network
  (so it learns to produce *good boards in general*, not just one lucky board).

### 4.6 Fair comparison
- **Same budget:** the same number of fitness evaluations (solver runs) for
  every method.
- **Same seeds:** run number *i* of each method uses the same random seed
  and the same board size.
- **Many runs:** at least **30 independent runs** per method.

### 4.7 Statistical analysis
- Measure: **solvable-rate** = share of *newly generated* test boards (e.g. 200
  per run) that the solver solves without guessing.
- Because runs are paired by seed, we use a **paired test**:
  - **paired sign test** (the one recommended in the class description), and
  - **Wilcoxon signed-rank test** as a second check.
- Comparisons: A vs B, A vs random, B vs random.
- Also report: time to generate a board, learning curves (best fitness per
  generation), and the effect of board size.
- As the class says: showing a *significant* effect is not the point - a clean,
  simple, honest analysis is.

### 4.8 Bonus: target difficulty
- Define difficulty = how many "hard" logic steps the solver needs.
- Fitness = how close the board's difficulty is to the target AND that it is
  solvable.
- Check: do boards from the "hard" setting really need more hard steps than the
  "easy" ones? (again a paired/statistical comparison).

Optional extensions on top of the bonus (only if time allows; everything else
in section 4 is required):
- **#BON1 - Novelty search (topic 13):** add a diversity score (e.g. distance
  between mine layouts, or between solver "behaviour" such as the step counts)
  so the evolved boards are not all alike. Check: are boards from the novelty
  run more diverse than from the plain run, with similar solvable-rate?
- **#BON2 - Multiobjective (topic 5):** run NSGA-II on several goals at once -
  solvable, difficulty, variety - and report the Pareto front instead of one
  fitness value.
- **#BON3 - Coevolution (topic 7):** coevolve the generator against a
  population of solvers (e.g. solvers with different rule sets) so boards must
  be solvable by logic but hard for weaker solvers. Needs the most extra work.

### 4.9 Demo
A small visual (matplotlib or pygame) showing a generated board and the solver
playing it step by step.

---

## 5. Tools

- **Python** with `numpy`, `scipy` (statistical tests), `matplotlib` (plots).
- Evolution: our own simple GA, or `DEAP`; for the network - `neat-python`
  or a small hand-written MLP evolved with a GA/ES.
- Optional: `pygame` for the demo.

---

## 6. Risks and how we handle them

- **Solver too slow** -> use only the basic + subset rules first, start with a
  small board (9x9).
- **Neural generator learns nothing** -> start with simple inputs, more
  generations, or a simpler network; it is fine to report that it is *worse*
  than direct encoding - that is a result too.
- **Too few runs** -> keep boards small so 30 runs are cheap.

---

## 7. What will be verified at the end (our checklist)

- [ ] Solver correctly identifies solvable vs. unsolvable boards (tested on known boards)
- [ ] Fitness function is clearly defined and explained
- [ ] Both methods + random baseline use the same budget and seeds
- [ ] At least 30 runs per method
- [ ] Paired sign test (and Wilcoxon) with p-values reported
- [ ] Plots: learning curves, solvable-rate per method
- [ ] Visual demo of a generated board
- [ ] Short description + results sent after the last meeting
