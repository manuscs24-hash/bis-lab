import random

north_south = 60
east_west = 30

CYCLE_TIME = 90
MIN_GREEN = 15

WOLVES = 20
ITERATIONS = 100

AVAILABLE_TIME = CYCLE_TIME - (2 * MIN_GREEN)

def fitness(position):

    green_ns = position
    green_ew = CYCLE_TIME - green_ns

    waiting_cost = (
        (north_south ** 2) / green_ns
        + (east_west ** 2) / green_ew
    )

    return waiting_cost

def initialize_wolves():

    return [
        random.uniform(
            MIN_GREEN,
            CYCLE_TIME - MIN_GREEN
        )
        for _ in range(WOLVES)
    ]

def gwo():

    random.seed(42)

    wolves = initialize_wolves()

    alpha = 0
    beta = 0
    delta = 0

    for iteration in range(ITERATIONS):

        wolves.sort(key=fitness)

        alpha = wolves[0]
        beta = wolves[1]
        delta = wolves[2]

        a = 2 - (2 * iteration / ITERATIONS)

        new_wolves = []

        for wolf in wolves:

            positions = []

            for leader in [alpha, beta, delta]:

                r1 = random.random()
                r2 = random.random()

                A = 2 * a * r1 - a
                C = 2 * r2

                D = abs(C * leader - wolf)

                X = leader - A * D

                positions.append(X)

            new_position = sum(positions) / 3

            new_position = max(
                MIN_GREEN,
                min(CYCLE_TIME - MIN_GREEN, new_position)
            )

            new_wolves.append(new_position)

        wolves = new_wolves

    wolves.sort(key=fitness)

    return wolves[0]

if __name__ == "__main__":

    best_position = gwo()

    green_ns = best_position
    green_ew = CYCLE_TIME - green_ns

    print("SMART TRAFFIC SIGNAL OPTIMIZATION")
    print("----------------------------------")

    print("North-South Vehicles:", north_south)
    print("East-West Vehicles:", east_west)

    print("----------------------------------")

    print("Optimized Green Signal Timing:")

    print("North-South:",
          round(green_ns, 2), "seconds")

    print("East-West:",
          round(green_ew, 2), "seconds")

    print("----------------------------------")

    print("Total Signal Cycle:",
          CYCLE_TIME, "seconds")

    print("Minimum Green Time:",
          MIN_GREEN, "seconds")

    print("Minimum Waiting Cost:",
          round(fitness(best_position), 2))

    print("----------------------------------")
    print("Optimization Completed Successfully!")