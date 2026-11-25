import random
import math

locations = {
    "Warehouse": (0, 0),
    "Customer 1": (2, 4),
    "Customer 2": (5, 2),
    "Customer 3": (6, 6),
    "Customer 4": (8, 3),
    "Customer 5": (1, 7)
}

def distance(a, b):
    x1, y1 = locations[a]
    x2, y2 = locations[b]
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def route_distance(route):
    total = 0
    for i in range(len(route)):
        total += distance(
            route[i],
            route[(i + 1) % len(route)]
        )
    return total
def create_population(size, customers):
    return [
        random.sample(customers, len(customers))
        for _ in range(size)
    ]
def fitness(route):
    return 1 / route_distance(route)

def selection(population):
    candidates = random.sample(population, 3)
    return min(candidates, key=route_distance)

def crossover(parent1, parent2):
    n = len(parent1)
    start, end = sorted(random.sample(range(n), 2))

    child = [None] * n
    child[start:end + 1] = parent1[start:end + 1]

    remaining = [
        city for city in parent2
        if city not in child
    ]

    j = 0
    for i in range(n):
        if child[i] is None:
            child[i] = remaining[j]
            j += 1

    return child

def mutation(route, rate):
    route = route.copy()

    if random.random() < rate:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

    return route

def genetic_algorithm():
    random.seed(42)

    customers = [
        city for city in locations
        if city != "Warehouse"
    ]

    population_size = 100
    generations = 300
    mutation_rate = 0.1

    population = create_population(
        population_size, customers
    )

    best_route = min(population, key=route_distance)
    best_distance = route_distance(best_route)

    for generation in range(generations):

        population.sort(key=route_distance)

        new_population = population[:2]

        while len(new_population) < population_size:

            parent1 = selection(population)
            parent2 = selection(population)

            child = crossover(parent1, parent2)
            child = mutation(child, mutation_rate)

            new_population.append(child)

        population = new_population

        current_best = min(population, key=route_distance)
        current_distance = route_distance(current_best)

        if current_distance < best_distance:
            best_route = current_best.copy()
            best_distance = current_distance

    return best_route, best_distance


if __name__ == "__main__":

    best_route, best_distance = genetic_algorithm()

    complete_route = (
        ["Warehouse"] + best_route + ["Warehouse"]
    )

    print("DELIVERY ROUTE OPTIMIZATION")
    print("--------------------------------")

    print("Optimized Delivery Route:")
    print(" -> ".join(complete_route))

    print("--------------------------------")
    print("Minimum Distance:",
          round(best_distance, 2), "km")

    print("Total Locations Visited:",
          len(locations) - 1)