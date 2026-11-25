import numpy as np

def fitness(x):
    return x**2 - 4*x + 4

def parallel_cellular_algorithm():

    rows = 10
    cols = 10
    max_iterations = 10

    grid = np.random.uniform(-10, 10, (rows, cols))

    fit = fitness(grid)

    best_index = np.argmin(fit)
    best_solution = grid.flat[best_index]
    best_fitness = fit.flat[best_index]

    for iteration in range(max_iterations):

        best_neighbors = grid.copy()
        best_neighbor_fitness = fitness(grid)

        for i in range(-1, 2):
            for j in range(-1, 2):

                neighbor = np.roll(
                    np.roll(grid, i, axis=0),
                    j, axis=1
                )

                neighbor_fit = fitness(neighbor)

                mask = neighbor_fit < best_neighbor_fitness

                best_neighbor_fitness[mask] = neighbor_fit[mask]
                best_neighbors[mask] = neighbor[mask]

        mutation = (0.1 * (1 - iteration / max_iterations)
                    * np.random.randn(rows, cols))

        new_grid = best_neighbors + mutation

        new_grid = np.clip(new_grid, -10, 10)

        grid = new_grid

        fit = fitness(grid)

        current_index = np.argmin(fit)
        current_best = grid.flat[current_index]
        current_fitness = fit.flat[current_index]

        if current_fitness < best_fitness:
            best_fitness = current_fitness
            best_solution = current_best

        print("Iteration:", iteration + 1,
              "Best Solution:", round(best_solution, 6),
              "Fitness:", round(best_fitness, 6))

    print("\nFinal Results")
    print("Best Solution:", best_solution)
    print("Minimum Fitness:", best_fitness)

parallel_cellular_algorithm()