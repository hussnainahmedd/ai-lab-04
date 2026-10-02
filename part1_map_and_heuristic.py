ROADS = [
    ("Peshawar",    "Islamabad", 185),
    ("Islamabad",   "Rawalpindi", 15),
    ("Islamabad",   "Abbottabad", 120),
    ("Islamabad",   "Sargodha", 235),
    ("Rawalpindi",  "Murree", 60),
    ("Abbottabad",  "Murree", 70),
    ("Rawalpindi",  "Jhelum", 115),
    ("Jhelum",      "Gujranwala", 110),
    ("Gujranwala",  "Lahore", 70),
    ("Sargodha",    "Faisalabad", 95),
    ("Faisalabad",  "Lahore", 180),
    ("Faisalabad",  "Multan", 240),
    ("Lahore",      "Multan", 340),
]

# --- Step 2: the heuristic h(n) ----------------------------------------

SLD_TO_LAHORE = {
    "Peshawar": 375, "Islamabad": 265, "Rawalpindi": 255,
    "Abbottabad": 305, "Murree": 275, "Jhelum": 160,
    "Gujranwala": 65, "Lahore": 0, "Sargodha": 165,
    "Faisalabad": 120, "Multan": 310,
}

# --- Step 3: turn the road list into an adjacency dictionary --------

def build_graph(roads: list[tuple]) -> dict:
    """{'Islamabad': {'Peshawar': 185, 'Rawalpindi': 15, ...}, ...}"""
    graph = {}
    for city_a, city_b, km in roads:
        graph.setdefault(city_a, {})[city_b] = km   # road A -> B
        graph.setdefault(city_b, {})[city_a] = km   # same road B -> A
    return graph


# --- Step 4: show what we built -------------------------------------
if __name__ == "__main__":
    graph = build_graph(ROADS)

    print("PART 1: the map and the heuristic")
    print("-" * 58)
    print(f"Cities: {len(graph)}   Roads: {len(ROADS)}")

    print("\nNeighbours of Islamabad (city: km):")
    for city, km in graph["Islamabad"].items():
        print(f"  {city:<12} {km:>4} km")

    print("\nHeuristic h(n) = straight-line km to Lahore:")
    print(f"{'City':<12}{'h(n)':>7}")
    for city in sorted(SLD_TO_LAHORE):
        print(f"{city:<12}{SLD_TO_LAHORE[city]:>7}")

        # Why h is only a GUESS: compare one road with the two h values.
        print("\nQuick check (Jhelum -> Gujranwala):")
        print(f"   road cost c       = {graph['Jhelum']['Gujranwala']} km")
        print(f"   h(Jhelum)         = {SLD_TO_LAHORE['Jhelum']} km")
        print(f"   h(Gujranwala)     = {SLD_TO_LAHORE['Gujranwala']} km")
        print("   Driving 110 km reduced the estimate by only 95 km - fine.")



