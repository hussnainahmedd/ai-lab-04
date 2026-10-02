# =====================================================================
# CS344L - AI Lab | Week 4 | PART 2 of 8
# Topic : Is our heuristic ADMISSIBLE and CONSISTENT?
# Teacher: Raja Faisal Umar
# Run : python part2_check_heuristic.py
# =====================================================================
# Admissible : h(n) <= real cheapest cost from n to the goal (never too big)
# Consistent : h(n) <= cost(n, n') + h(n') for every road (triangle rule)
# If these fail, A* can return a WRONG (non-optimal) route.
# =====================================================================

import heapq

ROADS = [
    ("Peshawar", "Islamabad", 185), ("Islamabad", "Rawalpindi", 15),
    ("Islamabad", "Abbottabad", 120), ("Islamabad", "Sargodha", 235),
    ("Rawalpindi", "Murree", 60), ("Abbottabad", "Murree", 70),
    ("Rawalpindi", "Jhelum", 115), ("Jhelum", "Gujranwala", 110),
    ("Gujranwala", "Lahore", 70), ("Sargodha", "Faisalabad", 95),
    ("Faisalabad", "Lahore", 180), ("Faisalabad", "Multan", 240),
    ("Lahore", "Multan", 340),
]

SLD_TO_LAHORE = {
    "Peshawar": 375, "Islamabad": 265, "Rawalpindi": 255,
    "Abbottabad": 305, "Murree": 275, "Jhelum": 160,
    "Gujranwala": 65, "Lahore": 0, "Sargodha": 165,
    "Faisalabad": 120, "Multan": 310,
}

def build_graph(roads):
    graph = {}
    for a, b, km in roads:
        graph.setdefault(a, {})[b] = km
        graph.setdefault(b, {})[a] = km
    return graph

# --- Step 1: find the TRUE cheapest cost from every city to Lahore ----
# We run Dijkstra backwards from the goal. This is only for checking;
# a real agent does not know these numbers in advance.

def true_costs_to(graph, goal):
    dist = {goal: 0}
    pq = [(0, goal)]  # (cost so far, city)
    while pq:
        cost, city = heapq.heappop(pq)
        if cost > dist.get(city, float("inf")):
            continue  # old, worse copy
        for neighbour, km in graph[city].items():
            if cost + km < dist.get(neighbour, float("inf")):
                dist[neighbour] = cost + km
                heapq.heappush(pq, (cost + km, neighbour))
    return dist

# --- Step 2: admissibility test ---------------------------------------

def check_admissible(graph, heuristic, goal):
    true = true_costs_to(graph, goal)
    print(f"{'City':<12}{'h(n)':>7}{'true cost':>11}{'admissible?':>13}")
    all_ok = True
    for city in sorted(heuristic):
        ok = heuristic[city] <= true[city]  # must NEVER overestimate
        all_ok = all_ok and ok
        print(f"{city:<12}{heuristic[city]:>7}{true[city]:>11}"
              f"{('yes' if ok else 'NO'):>13}")
    return all_ok

# --- Step 3: consistency test -----------------------------------------

def check_consistent(roads, heuristic):
    all_ok = True
    for a, b, km in roads:
        for start, end in ((a, b), (b, a)):  # roads work both ways
            if heuristic[start] > km + heuristic[end]:
                print(f" BROKEN: h({start})={heuristic[start]} > "
                      f"{km} + h({end})={heuristic[end]}")
                all_ok = False
    return all_ok

if __name__ == "__main__":
    graph = build_graph(ROADS)

    print("PART 2: checking the heuristic")
    print("=" * 58)

    print("\n[A] Admissibility: h(n) must be <= the true cost")
    print("-" * 58)
    ok1 = check_admissible(graph, SLD_TO_LAHORE, "Lahore")
    print("RESULT:", "admissible" if ok1 else "OVERESTIMATES - not safe!")

    print("\n[B] Consistency: h(n) <= c(n, n') + h(n')")
    print("-" * 58)
    ok2 = check_consistent(ROADS, SLD_TO_LAHORE)
    print("RESULT:", "consistent" if ok2 else "NOT consistent")

    # Show students what a BAD heuristic looks like.
    print("\n[C] What if we triple every h value? (bad heuristic)")
    print("-" * 58)
    bad = {city: h * 3 for city, h in SLD_TO_LAHORE.items()}
    ok3 = check_admissible(graph, bad, "Lahore")
    print("RESULT:", "admissible" if ok3 else "OVERESTIMATES - A* may fail!")