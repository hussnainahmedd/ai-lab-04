# =====================================================================
# CS344L - AI Lab | Week 4 | PART 4 of 8
# Topic : GREEDY BEST-FIRST SEARCH, f(n) = h(n)
# Teacher: Raja Faisal Umar
# Run : python part4_greedy_search.py
# =====================================================================
# Greedy looks ONLY at h: "which city looks nearest to Lahore?"
# It forgets g, the money already spent. That is its weakness.
# =====================================================================

import heapq
from itertools import count

# ---------- same map, heuristic, Problem and Node as Part 3 ----------

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

class RouteProblem:
    def __init__(self, graph, initial, goal, heuristic):
        self.graph, self.initial = graph, initial
        self.goal, self.heuristic = goal, heuristic

    def actions(self, state):
        return sorted(self.graph[state].keys())

    def result(self, state, action):
        return action

    def is_goal(self, state):
        return state == self.goal

    def step_cost(self, state, action):
        return self.graph[state][action]

    def h(self, state):
        return self.heuristic.get(state, 0)

class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state, self.parent = state, parent
        self.path_cost = path_cost
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self, problem):
        out = []
        for action in problem.actions(self.state):
            cost = self.path_cost + problem.step_cost(self.state, action)
            out.append(Node(problem.result(self.state, action), self, cost))
        return out

    def path(self):
        node, route = self, []
        while node is not None:
            route.append(node.state)
            node = node.parent
        return list(reversed(route))

# ---------- the search engine (same loop for greedy, A* and UCS) -----

def best_first_search(problem, f, trace=False):
    """Always expand the node with the SMALLEST f value."""
    tie = count()  # counter: breaks ties in the heap
    start = Node(problem.initial)
    frontier = [(f(problem, start), next(tie), start)]  # priority queue
    best_f = {problem.initial: f(problem, start)}  # best f per city
    stats = {"expanded": 0, "generated": 1}
    step = 0

    while frontier:
        fn, _, node = heapq.heappop(frontier)  # cheapest f comes out

        if fn > best_f.get(node.state, float("inf")):
            continue  # an old, worse copy

        if problem.is_goal(node.state):
            if trace:
                print(f" pop {node.state} with f={fn} --> GOAL")
            return node, stats

        stats["expanded"] += 1
        step += 1

        for child in node.expand(problem):  # generate children
            stats["generated"] += 1
            fc = f(problem, child)

            if fc < best_f.get(child.state, float("inf")):
                best_f[child.state] = fc
                heapq.heappush(frontier, (fc, next(tie), child))

        if trace:
            waiting = sorted((v, s) for v, _, n in frontier
                             for s in [n.state] if v == best_f[s])
            print(f" step {step}: expand {node.state:<11} f={fn:<4} "
                  f"frontier = {[f'{s}:{v}' for v, s in waiting]}")

    return None, stats

# ---------- the evaluation function that makes it GREEDY -------------

def f_greedy(problem, node):
    return problem.h(node.state)  # only h, g is ignored

if __name__ == "__main__":
    problem = RouteProblem(build_graph(ROADS), "Peshawar", "Lahore",
                           SLD_TO_LAHORE)

    print("PART 4: greedy best-first search, f(n) = h(n)")
    print("=" * 62)

    goal_node, stats = best_first_search(problem, f_greedy, trace=True)

    print("\nRESULT")
    print(" path : " + " -> ".join(goal_node.path()))
    print(f" distance : {goal_node.path_cost} km")
    print(f" expanded : {stats['expanded']} nodes "
          f"(generated {stats['generated']})")

    print("\nWHY IS IT 695 km AND NOT 495 km?")
    print(" At Islamabad greedy compared only h values:")
    print(f" Sargodha h={SLD_TO_LAHORE['Sargodha']} (road costs 235 km)")
    print(f" Rawalpindi h={SLD_TO_LAHORE['Rawalpindi']} (road costs 15 km)")
    print(" It chose Sargodha because 165 < 255 - and paid 235 km for it.")