import random
import math

users = [
    (2, 3),
    (5, 17),
    (12, 8),
    (18, 4),
    (17, 18)
]

particles = 30
iterations = 100
w = 0.7
c1 = 1.5
c2 = 1.5
MIN = 0
MAX = 20
def signal_strength(x, y, ux, uy):
    d = math.sqrt((x - ux)**2 + (y - uy)**2)
    d = max(d, 0.5)
    return -30 - 25 * math.log10(d)

def fitness(position):
    x, y = position
    cost = 0

    for ux, uy in users:
        d = math.sqrt((x - ux)**2 + (y - uy)**2)
        rssi = signal_strength(x, y, ux, uy)

        cost += d ** 2

        if rssi < -55:
            cost += 500

    return cost

positions = [
    [random.uniform(MIN, MAX),
     random.uniform(MIN, MAX)]
    for _ in range(particles)
]

velocities = [
    [random.uniform(-1, 1),
     random.uniform(-1, 1)]
    for _ in range(particles)
]

pbest = [p.copy() for p in positions]
pbest_fitness = [fitness(p) for p in positions]

best_index = pbest_fitness.index(min(pbest_fitness))
gbest = pbest[best_index].copy()

for iteration in range(iterations):

    for i in range(particles):

        for j in range(2):

            r1 = random.random()
            r2 = random.random()

            velocities[i][j] = (
                w * velocities[i][j]
                + c1 * r1 * (pbest[i][j] - positions[i][j])
                + c2 * r2 * (gbest[j] - positions[i][j])
            )

            positions[i][j] += velocities[i][j]

            positions[i][j] = max(
                MIN, min(MAX, positions[i][j])
            )

        current_fitness = fitness(positions[i])

        if current_fitness < pbest_fitness[i]:
            pbest[i] = positions[i].copy()
            pbest_fitness[i] = current_fitness

    best_index = pbest_fitness.index(min(pbest_fitness))

    if pbest_fitness[best_index] < fitness(gbest):
        gbest = pbest[best_index].copy()

print("WIFI ROUTER OPTIMIZATION USING PSO")
print("----------------------------------")

print("Optimal Router Position:")
print("X =", round(gbest[0], 2))
print("Y =", round(gbest[1], 2))

print("----------------------------------")

covered = 0

for i, (ux, uy) in enumerate(users):
    rssi = signal_strength(
        gbest[0], gbest[1], ux, uy
    )

    print("User", i + 1,
          "Signal Strength:", round(rssi, 2), "dBm")

    if rssi >= -55:
        covered += 1

print("----------------------------------")
print("Total Users:", len(users))
print("Users with Good Signal:", covered)
print("Coverage Percentage:",
      round(covered / len(users) * 100, 2), "%")