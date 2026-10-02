# =====================================================================
# CS344L - AI Lab | Week 4 | PART 3 of 8
# Topic : The Problem class (now with h) and the Node class
# Teacher: Raja Faisal Umar
# Run : python part3_problem_and_node.py
# =====================================================================
# Week 3 Node remembered g(n) = cost already paid.
# Week 4 adds h(n) = guess of cost still left, and
# f(n) = g(n) + h(n) = guess of the TOTAL cost of the route.
# =====================================================================

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

# --- The problem: five parts from Week 3 + one new part, h() ----------

class RouteProblem:
    def __init__(self, graph, initial, goal, heuristic):
        self.graph = graph              # the map
        self.initial = initial          # 1. where we start
        self.goal = goal                # where we want to reach
        self.heuristic = heuristic      # NEW: the h table

    def actions(self, state):           # 2. moves available here
        return sorted(self.graph[state].keys())

    def result(self, state, action):     # 3. where a move takes us
        return action

    def is_goal(self, state):           # 4. are we done?
        return state == self.goal

    def step_cost(self, state, action):  # 5. price of one road
        return self.graph[state][action]

    def h(self, state):                  # 6. NEW: guess of remaining cost
        return self.heuristic.get(state, 0)

# --- The node: one entry in the search tree ---------------------------

class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state              # which city
        self.parent = parent            # node we came from
        self.path_cost = path_cost      # g(n): km paid so far
        self.depth = 0 if parent is None else parent.depth + 1

    def expand(self, problem):
        """Make one child node for every road leaving this city."""
        children = []
        for action in problem.actions(self.state):
            next_state = problem.result(self.state, action)
            cost = self.path_cost + problem.step_cost(self.state, action)
            children.append(Node(next_state, self, cost))
        return children

    def path(self):
        """Follow parent links back to the start city."""
        node, route = self, []
        while node is not None:
            route.append(node.state)
            node = node.parent
        return list(reversed(route))

if __name__ == "__main__":
    graph = build_graph(ROADS)
    problem = RouteProblem(graph, "Peshawar", "Lahore", SLD_TO_LAHORE)

    print("PART 3: problem, node, and f = g + h")
    print("=" * 58)

    # Build a small path by hand: Peshawar -> Islamabad -> Rawalpindi
    start = Node("Peshawar")
    islamabad = Node("Islamabad", start, 185)
    rawalpindi = Node("Rawalpindi", islamabad, 185 + 15)

    for node in (start, islamabad, rawalpindi):
        g = node.path_cost
        h = problem.h(node.state)
        print(f"{node.state:<12} g={g:<5} h={h:<5} f=g+h={g + h:<5} "
              f"depth={node.depth}")

    print("\nPath stored in the last node:")
    print(" " + " -> ".join(rawalpindi.path()))

    print("\nChildren of the Islamabad node (city, g, h, f):")
    for child in islamabad.expand(problem):
        g = child.path_cost
        h = problem.h(child.state)
        print(f" {child.state:<12} g={g:<5} h={h:<5} f={g + h}")

    print("\nNOTE: greedy will choose the smallest h, A* the smallest f.")