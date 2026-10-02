# =====================================================================
# CS344L - AI Lab | Week 4 | PART 6 of 8
# Topic : ONE ENGINE, THREE ALGORITHMS (UCS vs Greedy vs A*)
# Teacher: Raja Faisal Umar
# Run : python part6_compare_three.py
# =====================================================================
# The search loop never changes. Only f(n) changes:
# f = g -> uniform-cost search (Week 3, blind)
# f = h -> greedy best-first (Week 4, fast but careless)
# f = g + h -> A* (Week 4, fast AND optimal)
# A chart window opens at the end - close it to finish the program.
# =====================================================================

import matplotlib.pyplot as plt

from part4_greedy_search import (ROADS, SLD_TO_LAHORE, build_graph,
                                 RouteProblem, best_first_search, f_greedy)
from part5_astar_search import f_astar

def f_uniform_cost(problem, node):
    return node.path_cost  # only g: Week 3 behaviour

if __name__ == "__main__":
    problem = RouteProblem(build_graph(ROADS), "Peshawar", "Lahore",
                           SLD_TO_LAHORE)

    print("PART 6: comparing the three evaluation functions")
    print("=" * 66)

    results = {}

    for name, f in (("UCS (f=g)", f_uniform_cost),
                    ("Greedy (f=h)", f_greedy),
                    ("A* (f=g+h)", f_astar)):
        node, stats = best_first_search(problem, f)
        results[name] = (node, stats)

        print(f"\n{name}")
        print(" path : " + " -> ".join(node.path()))
        print(f" distance : {node.path_cost} km")
        print(f" expanded : {stats['expanded']} nodes, "
              f"generated {stats['generated']}")

    print("\n" + "=" * 66)
    print(f"{'Algorithm':<16}{'Expanded':>10}{'Generated':>11}{'Km':>7}")

    for name, (node, stats) in results.items():
        print(f"{name:<16}{stats['expanded']:>10}"
              f"{stats['generated']:>11}{node.path_cost:>7}")

    print("\nREAD THE TABLE:")
    print(" Greedy expands the fewest nodes but drives the longest route.")
    print(" A* expands fewer nodes than UCS and still finds 495 km.")

    # ---------------- simple bar chart -------------------------------

    labels = [n.split()[0] for n in results]
    expanded = [s["expanded"] for _, s in results.values()]
    kms = [n.path_cost for n, _ in results.values()]

    figure, (left, right) = plt.subplots(1, 2, figsize=(10, 4))

    left.bar(labels, expanded, color="#3A4D73")
    left.set_title("Nodes expanded (less work is better)")

    right.bar(labels, kms, color="#C8553D")
    right.set_title("Route distance in km (shorter is better)")

    for axis, values in ((left, expanded), (right, kms)):
        for x, value in zip(labels, values):
            axis.text(x, value, str(value), ha="center", va="bottom")

    figure.tight_layout()
    figure.savefig("part6_comparison.png", dpi=120)

    print("\nChart saved as part6_comparison.png")
    plt.show()