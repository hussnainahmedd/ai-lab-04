# =====================================================================
# CS344L - AI Lab | Week 4 | PART 5 of 8
# Topic : A* SEARCH, f(n) = g(n) + h(n)
# Teacher: Raja Faisal Umar
# Run : python part5_astar_search.py
# =====================================================================
# A* = greedy + memory of what we already paid.
# g(n) = km driven from Peshawar to n (fact)
# h(n) = km still needed, estimated (guess)
# f(n) = g(n) + h(n) = estimated total (what A* sorts by)
#
# We REUSE the engine written in Part 4. Keep all part files in the
# same folder so this import works.
# =====================================================================

from part4_greedy_search import (ROADS, SLD_TO_LAHORE, build_graph,
                                 RouteProblem, best_first_search, f_greedy)

# ---------- the only new line of the whole lecture --------------------

def f_astar(problem, node):
    return node.path_cost + problem.h(node.state)  # g + h

if __name__ == "__main__":
    problem = RouteProblem(build_graph(ROADS), "Peshawar", "Lahore",
                           SLD_TO_LAHORE)

    print("PART 5: A* search, f(n) = g(n) + h(n)")
    print("=" * 62)

    goal_node, stats = best_first_search(problem, f_astar, trace=True)

    print("\nRESULT")
    print(" path : " + " -> ".join(goal_node.path()))
    print(f" distance : {goal_node.path_cost} km <-- OPTIMAL")
    print(f" expanded : {stats['expanded']} nodes "
          f"(generated {stats['generated']})")

    # Show the g, h, f of every city on the final route.
    print("\nf values along the route found by A*:")
    node = goal_node
    rows = []

    while node is not None:
        rows.append((node.state, node.path_cost, problem.h(node.state)))
        node = node.parent

    for city, g, h in reversed(rows):
        print(f" {city:<12} g={g:<5} h={h:<5} f={g + h}")

    print(" f never goes down along the path - that is CONSISTENCY.")

    # Same problem, greedy, for a direct comparison in one screen.
    greedy_node, greedy_stats = best_first_search(problem, f_greedy)

    print("\nSIDE BY SIDE")
    print(f" Greedy : {greedy_node.path_cost} km, "
          f"{greedy_stats['expanded']} nodes expanded")
    print(f" A* : {goal_node.path_cost} km, "
          f"{stats['expanded']} nodes expanded")
    print(" A* did a little more work and saved 200 km.")