
import numpy as np
import matplotlib.pyplot as plt
import math

# =====================================================
# 1. TRAFFIC INPUT
# =====================================================

np.random.seed(42)

directions = ["North", "South", "East", "West"]

# Number of vehicles waiting in each direction
traffic = np.array([40, 30, 70, 50], dtype=float)

# Traffic signal configuration
CYCLE_TIME = 120
LOST_TIME = 12
TOTAL_GREEN = CYCLE_TIME - LOST_TIME

MIN_GREEN = 10
MAX_GREEN = 60

# Vehicles discharged per second of green time
SATURATION_FLOW = 1.8

# Penalty for vehicles remaining in queue
QUEUE_PENALTY = 100


# =====================================================
# 2. CUCKOO SEARCH PARAMETERS
# =====================================================

NEST_COUNT = 25
DISCOVERY_PROBABILITY = 0.25
MAX_ITERATIONS = 100

LEVY_SCALE = 3.0
BETA = 1.5


# =====================================================
# 3. FITNESS FUNCTION
# =====================================================

def fitness(green_times):

    total_delay = 0
    total_queue = 0

    for i in range(4):

        vehicles = traffic[i]
        green = green_times[i]

        # Estimate signal waiting delay
        waiting = (
            vehicles * (CYCLE_TIME - green) ** 2
            / (2 * CYCLE_TIME)
        )

        # Calculate vehicle discharge capacity
        capacity = SATURATION_FLOW * green

        # Calculate remaining queue
        remaining = max(0, vehicles - capacity)

        total_delay += waiting
        total_queue += remaining

    # Objective: minimize delay and remaining queue
    return total_delay + QUEUE_PENALTY * total_queue


# =====================================================
# 4. REPAIR SOLUTION
# =====================================================

def repair_solution(solution):

    solution = np.asarray(solution, dtype=float)

    # Ensure green timings satisfy all constraints
    # while keeping their total equal to TOTAL_GREEN.

    low = np.min(solution - MAX_GREEN)
    high = np.max(solution - MIN_GREEN)

    for _ in range(100):

        middle = (low + high) / 2

        candidate = np.clip(
            solution - middle,
            MIN_GREEN,
            MAX_GREEN
        )

        if np.sum(candidate) > TOTAL_GREEN:
            low = middle
        else:
            high = middle

    result = np.clip(
        solution - (low + high) / 2,
        MIN_GREEN,
        MAX_GREEN
    )

    return result


# =====================================================
# 5. INITIALIZE POPULATION
# =====================================================

def initialize_nests():

    nests = []

    for _ in range(NEST_COUNT):

        random_solution = np.random.uniform(
            MIN_GREEN,
            MAX_GREEN,
            size=4
        )

        random_solution = repair_solution(
            random_solution
        )

        nests.append(random_solution)

    return np.array(nests)


# =====================================================
# 6. LEVY FLIGHT USING MANTEGNA METHOD
# =====================================================

def levy_flight():

    sigma = (
        math.gamma(1 + BETA)
        * math.sin(math.pi * BETA / 2)
        /
        (
            math.gamma((1 + BETA) / 2)
            * BETA
            * 2 ** ((BETA - 1) / 2)
        )
    ) ** (1 / BETA)

    u = np.random.normal(
        0, sigma, size=4
    )

    v = np.random.normal(
        0, 1, size=4
    )

    step = u / (
        np.abs(v) ** (1 / BETA) + 1e-12
    )

    return step


# =====================================================
# 7. CUCKOO SEARCH OPTIMIZATION
# =====================================================

def cuckoo_search():

    nests = initialize_nests()

    fitness_values = np.array([
        fitness(nest) for nest in nests
    ])

    best_index = np.argmin(fitness_values)

    best_nest = nests[best_index].copy()
    best_fitness = fitness_values[best_index]

    convergence = []

    print("\nCUCKOO SEARCH OPTIMIZATION STARTED\n")

    for iteration in range(MAX_ITERATIONS):

        # ---------------------------------------------
        # Generate new solutions using Levy flights
        # ---------------------------------------------

        for i in range(NEST_COUNT):

            step = levy_flight()

            new_solution = (
                nests[i] + LEVY_SCALE * step
            )

            new_solution = repair_solution(
                new_solution
            )

            new_fitness = fitness(new_solution)

            # Replace the current nest if better
            if new_fitness < fitness_values[i]:

                nests[i] = new_solution.copy()
                fitness_values[i] = new_fitness

        # ---------------------------------------------
        # Find current best nest
        # ---------------------------------------------

        best_index = np.argmin(fitness_values)

        if fitness_values[best_index] < best_fitness:

            best_fitness = fitness_values[best_index]

            best_nest = nests[best_index].copy()

        # ---------------------------------------------
        # Abandon a fraction of worst nests
        # ---------------------------------------------

        abandon_count = max(
            1,
            int(DISCOVERY_PROBABILITY * NEST_COUNT)
        )

        # Protect the current best nest
        worst_indices = np.argsort(
            fitness_values
        )[::-1]

        worst_indices = [
            index for index in worst_indices
            if index != best_index
        ][:abandon_count]

        for index in worst_indices:

            if np.random.rand() < DISCOVERY_PROBABILITY:

                new_nest = np.random.uniform(
                    MIN_GREEN,
                    MAX_GREEN,
                    size=4
                )

                new_nest = repair_solution(new_nest)

                nests[index] = new_nest

                fitness_values[index] = fitness(
                    new_nest
                )

        # ---------------------------------------------
        # Update global best
        # ---------------------------------------------

        best_index = np.argmin(fitness_values)

        if fitness_values[best_index] < best_fitness:

            best_fitness = fitness_values[best_index]

            best_nest = nests[best_index].copy()

        convergence.append(best_fitness)

        print(
            "Iteration:", iteration + 1,
            "| Best Fitness:", round(best_fitness, 2)
        )

    return best_nest, best_fitness, convergence


# =====================================================
# 8. EXECUTE CUCKOO SEARCH
# =====================================================

best_green, best_fitness, convergence = cuckoo_search()


# =====================================================
# 9. NORMAL TRAFFIC SIGNAL TIMING
# =====================================================

normal_green = np.full(
    4,
    TOTAL_GREEN / 4
)

normal_fitness = fitness(normal_green)


# =====================================================
# 10. CALCULATE TRAFFIC RESULTS
# =====================================================

def calculate_results(green_times):

    results = []

    for i in range(4):

        capacity = SATURATION_FLOW * green_times[i]

        remaining = max(
            0,
            traffic[i] - capacity
        )

        waiting = (
            traffic[i]
            * (CYCLE_TIME - green_times[i]) ** 2
            / (2 * CYCLE_TIME)
        )

        results.append([
            traffic[i],
            green_times[i],
            capacity,
            remaining,
            waiting
        ])

    return np.array(results)


normal_results = calculate_results(normal_green)

optimized_results = calculate_results(best_green)


# =====================================================
# 11. DISPLAY FINAL RESULTS
# =====================================================

print("\n")
print("=" * 65)
print("       SMART TRAFFIC MANAGEMENT SYSTEM")
print("          CUCKOO SEARCH ALGORITHM")
print("=" * 65)

print("\nTRAFFIC DENSITY")

for i in range(4):

    print(
        directions[i],
        ":",
        int(traffic[i]),
        "vehicles"
    )

print("\nOPTIMIZED TRAFFIC SIGNAL TIMINGS")

for i in range(4):

    print(
        directions[i],
        ":",
        round(best_green[i], 2),
        "seconds"
    )

print("\nDETAILED TRAFFIC RESULTS")

print(
    f"{'Direction':<12}"
    f"{'Vehicles':<12}"
    f"{'Green Time':<14}"
    f"{'Remaining':<12}"
)

for i in range(4):

    print(
        f"{directions[i]:<12}"
        f"{traffic[i]:<12.0f}"
        f"{best_green[i]:<14.2f}"
        f"{optimized_results[i][3]:<12.2f}"
    )

print("\nNORMAL FITNESS:", round(normal_fitness, 2))

print("OPTIMIZED FITNESS:", round(best_fitness, 2))

improvement = (
    (normal_fitness - best_fitness)
    / normal_fitness
) * 100

print(
    "FITNESS IMPROVEMENT:",
    round(improvement, 2),
    "%"
)

print("\nTOTAL GREEN TIME:",
      round(np.sum(best_green), 2), "seconds")

print("=" * 65)


# =====================================================
# 12. GRAPH 1: CONVERGENCE GRAPH
# =====================================================

plt.figure(figsize=(9, 5))

plt.plot(
    range(1, MAX_ITERATIONS + 1),
    convergence,
    color="blue",
    linewidth=2
)

plt.title("Cuckoo Search Convergence")
plt.xlabel("Iterations")
plt.ylabel("Best Fitness Value")

plt.grid(True)
plt.tight_layout()
plt.show()


# =====================================================
# 13. GRAPH 2: SIGNAL TIMING COMPARISON
# =====================================================

x = np.arange(4)
width = 0.35

plt.figure(figsize=(9, 5))

plt.bar(
    x - width / 2,
    normal_green,
    width,
    color="orange",
    label="Normal Signal"
)

plt.bar(
    x + width / 2,
    best_green,
    width,
    color="green",
    label="Cuckoo Search"
)

plt.xticks(x, directions)

plt.title("Normal vs Optimized Signal Timings")
plt.xlabel("Traffic Directions")
plt.ylabel("Green Time (Seconds)")

plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


# =====================================================
# 14. GRAPH 3: TRAFFIC DENSITY
# =====================================================

plt.figure(figsize=(9, 5))

plt.bar(
    directions,
    traffic,
    color=["blue", "green", "red", "orange"]
)

plt.title("Traffic Density at Four-Way Intersection")
plt.xlabel("Traffic Directions")
plt.ylabel("Number of Vehicles")

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


# =====================================================
# 15. GRAPH 4: REMAINING VEHICLES COMPARISON
# =====================================================

plt.figure(figsize=(9, 5))

plt.bar(
    x - width / 2,
    normal_results[:, 3],
    width,
    color="orange",
    label="Normal Signal"
)

plt.bar(
    x + width / 2,
    optimized_results[:, 3],
    width,
    color="green",
    label="Cuckoo Search"
)

plt.xticks(x, directions)

plt.title("Remaining Queue Comparison")
plt.xlabel("Traffic Directions")
plt.ylabel("Remaining Vehicles")

plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()


print("\nTRAFFIC OPTIMIZATION COMPLETED SUCCESSFULLY!")
