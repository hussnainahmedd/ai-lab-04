# =====================================================================
# CS344L - AI Lab | Week 4 | PART 8 of 8 (in-lab experiment)
# Topic : WHAT HAPPENS IF THE HEURISTIC OVERESTIMATES?
# Teacher: Raja Faisal Umar
# Run : python part8_break_heuristic.py
# =====================================================================
# Theory says: A* is optimal ONLY with an admissible heuristic.
# Let us break that rule on purpose and watch A* return a worse route.
# =====================================================================

from part4_greedy_search import (ROADS, SLD_TO_LAHORE, build_graph,
                                 RouteProblem, best_first_search)
from part5_astar_search import f_astar

if __name__ == "__main__":
    graph = build_graph(ROADS)

    print("PART 8: breaking the heuristic on purpose")
    print("=" * 62)

    # --- Run 1: the good, admissible heuristic -----------------------

    good = SLD_TO_LAHORE
    problem_good = RouteProblem(graph, "Peshawar", "Lahore", good)
    node_good, stats_good = best_first_search(problem_good, f_astar)

    print("\n[1] GOOD heuristic (straight-line distance)")
    print(" path : " + " -> ".join(node_good.path()))
    print(f" distance : {node_good.path_cost} km")
    print(f" expanded : {stats_good['expanded']} nodes")

    # --- Run 2: multiply every h by 3 (now it overestimates) ---------

    bad = {city: value * 3 for city, value in SLD_TO_LAHORE.items()}
    problem_bad = RouteProblem(graph, "Peshawar", "Lahore", bad)
    node_bad, stats_bad = best_first_search(problem_bad, f_astar)

    print("\n[2] BAD heuristic (every h value x 3)")
    print(" path : " + " -> ".join(node_bad.path()))
    print(f" distance : {node_bad.path_cost} km")
    print(f" expanded : {stats_bad['expanded']} nodes")

    # --- What changed? ----------------------------------------------

    extra = node_bad.path_cost - node_good.path_cost

    print("\nCOMPARISON")
    print(f" extra distance driven : {extra} km")
    print(f" nodes saved : "
          f"{stats_good['expanded'] - stats_bad['expanded']}")

    print("\nLESSON")
    print(" An over-confident heuristic searches less but can lie.")
    print(" A* only guarantees the best route when h never overestimates.")

    # --- Where exactly did it go wrong? ------------------------------

    print("\nf values at Islamabad's children (good vs bad):")
    print(f"{'City':<12}{'g':>6}{'h good':>8}{'f good':>8}"
          f"{'h bad':>8}{'f bad':>8}")

    for city, km in sorted(graph["Islamabad"].items()):
        g = 185 + km  # Peshawar -> Islamabad -> city

        print(f"{city:<12}{g:>6}{good[city]:>8}{g + good[city]:>8}"
              f"{bad[city]:>8}{g + bad[city]:>8}")