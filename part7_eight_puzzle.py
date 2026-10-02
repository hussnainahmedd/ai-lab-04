# =====================================================================
# CS344L - AI Lab | Week 4 | PART 7 of 8
# Topic : SAME A*, TWO HEURISTICS (the 8-puzzle)
# Teacher: Raja Faisal Umar
# Run : python part7_eight_puzzle.py
# =====================================================================
# Here the ALGORITHM is fixed (A*) and only the HEURISTIC changes:
# h1 = number of misplaced tiles (weak guess)
# h2 = Manhattan distance of tiles (stronger guess)
# Both are admissible, so both give the same optimal 20 moves -
# but h2 does a fraction of the work. Takes a few seconds for h1.
# =====================================================================

import time

from part4_greedy_search import best_first_search
from part5_astar_search import f_astar

GOAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)  # 0 is the empty square

class EightPuzzle:
    """The same five parts as RouteProblem, for a different world."""

    def __init__(self, initial, goal=GOAL, heuristic="manhattan"):
        self.initial = initial
        self.goal = goal
        self.heuristic = heuristic

    def actions(self, state):
        """Which way can the blank move?"""
        blank = state.index(0)
        row, col = divmod(blank, 3)  # 9 tiles arranged as 3 x 3
        moves = []

        if row > 0:
            moves.append("Up")
        if row < 2:
            moves.append("Down")
        if col > 0:
            moves.append("Left")
        if col < 2:
            moves.append("Right")

        return moves

    def result(self, state, action):
        """Swap the blank with the neighbouring tile."""
        blank = state.index(0)
        step = {"Up": -3, "Down": 3, "Left": -1, "Right": 1}[action]
        tiles = list(state)
        tiles[blank], tiles[blank + step] = tiles[blank + step], tiles[blank]
        return tuple(tiles)

    def is_goal(self, state):
        return state == self.goal

    def step_cost(self, state, action):
        return 1  # every slide costs 1 move

    def h(self, state):
        if self.heuristic == "misplaced":
            # h1: count tiles sitting in the wrong square
            return sum(1 for i, tile in enumerate(state)
                       if tile != 0 and tile != self.goal[i])

        # h2: how many rows + columns each tile is away from home
        total = 0

        for i, tile in enumerate(state):
            if tile == 0:
                continue

            home = self.goal.index(tile)
            total += abs(i // 3 - home // 3) + abs(i % 3 - home % 3)

        return total

def show(state):
    """Print the board as 3 rows."""
    return " | ".join(" ".join(str(t) if t else "_" for t in state[r:r + 3])
                      for r in (0, 3, 6))

if __name__ == "__main__":
    start = (7, 2, 4, 5, 0, 6, 8, 3, 1)

    print("PART 7: one puzzle, two heuristics")
    print("=" * 62)
    print("start:", show(start))
    print("goal :", show(GOAL))

    # h values of the START state, so students see the two numbers.
    print("\nHeuristic values of the start state:")
    print(" h1 misplaced tiles :", EightPuzzle(start, heuristic="misplaced").h(start))
    print(" h2 Manhattan :", EightPuzzle(start, heuristic="manhattan").h(start))
    print(" h2 is bigger but still never overestimates -> h2 DOMINATES h1.")

    print("\nRunning A* with each heuristic ...")

    for name in ("misplaced", "manhattan"):
        puzzle = EightPuzzle(start, heuristic=name)

        begin = time.time()
        node, stats = best_first_search(puzzle, f_astar)
        seconds = time.time() - begin

        print(f"\n h = {name}")
        print(f" moves found : {node.depth}")
        print(f" expanded : {stats['expanded']} nodes")
        print(f" generated : {stats['generated']} nodes")
        print(f" time : {seconds:.2f} seconds")

    print("\nSAME answer, same A* - only the guess changed.")
    print("A better heuristic is worth more than a cleverer algorithm.")