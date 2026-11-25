import random
import math


cities = {
    "A": (0, 0),  
    "B": (2, 4),   
    "C": (5, 2),  
    "D": (6, 6),   
    "E": (8, 3),  
    "F": (1, 7)   
}

NUM_ANTS = 20
ITERATIONS = 100
ALPHA = 1.0
BETA = 2.0
EVAPORATION = 0.5
Q = 100

random.seed(42)

city_names = list(cities.keys())
n = len(city_names)

def distance(i, j):
    x1, y1 = cities[city_names[i]]
    x2, y2 = cities[city_names[j]]

    return math.sqrt(
        (x2 - x1)**2 + (y2 - y1)**2
    )

dist = [
    [distance(i, j) for j in range(n)]
    for i in range(n)
]

pheromone = [
    [1.0 for j in range(n)]
    for i in range(n)
]

visibility = [
    [
        1 / dist[i][j] if i != j else 0
        for j in range(n)
    ]
    for i in range(n)
]

def route_distance(route):
    total = 0

    for i in range(len(route)):
        current = route[i]
        next_city = route[(i + 1) % len(route)]

        total += dist[current][next_city]

    return total

def select_next_city(current, unvisited):

    probabilities = []

    for city in unvisited:

        probability = (
            (pheromone[current][city] ** ALPHA)
            *
            (visibility[current][city] ** BETA)
        )

        probabilities.append(probability)

    total = sum(probabilities)

    probabilities = [
        p / total for p in probabilities
    ]

    return random.choices(
        unvisited,
        weights=probabilities,
        k=1
    )[0]

def construct_route():

    start = 0
    route = [start]

    unvisited = list(range(1, n))

    while unvisited:

        current = route[-1]

        next_city = select_next_city(
            current, unvisited
        )

        route.append(next_city)
        unvisited.remove(next_city)

    return route

def update_pheromone(routes):

    for i in range(n):
        for j in range(n):

            pheromone[i][j] *= (
                1 - EVAPORATION
            )

    for route, length in routes:

        deposit = Q / length

        for i in range(n):

            current = route[i]
            next_city = route[(i + 1) % n]

            pheromone[current][next_city] += deposit
            pheromone[next_city][current] += deposit

def ant_colony_optimization():

    best_route = None
    best_distance = float("inf")

    for iteration in range(ITERATIONS):

        routes = []

        for ant in range(NUM_ANTS):

            route = construct_route()
            length = route_distance(route)

            routes.append((route, length))

            if length < best_distance:

                best_distance = length
                best_route = route.copy()

        update_pheromone(routes)

    return best_route, best_distance

if __name__ == "__main__":

    best_route, best_distance = (
        ant_colony_optimization()
    )

    delivery_route = [
        city_names[i] for i in best_route
    ]

    delivery_route.append("A")

    print("DELIVERY ROUTE OPTIMIZATION USING ACO")
    print("--------------------------------------")

    print("Best Delivery Route:")
    print(" -> ".join(delivery_route))

    print("--------------------------------------")

    print("Minimum Distance:",
          round(best_distance, 2), "km")

    print("Total Customers:",
          len(city_names) - 1)

    print("--------------------------------------")
    print("Optimization Completed Successfully!")