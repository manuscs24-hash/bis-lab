import random
import math

# Job processing times (minutes)
jobs = {
    "J1": 8,
    "J2": 4,
    "J3": 6,
    "J4": 3,
    "J5": 7
}

# Cuckoo Search parameters
NESTS = 20
ITERATIONS = 100
PA = 0.25

random.seed(42)

job_names = list(jobs.keys())
n = len(job_names)

# Calculate makespan for two machines
def fitness(order):
    machine1 = 0
    machine2 = 0

    for job in order:
        if machine1 <= machine2:
            machine1 += jobs[job]
        else:
            machine2 += jobs[job]

    return max(machine1, machine2)

# Generate random job sequences
def create_nest():
    order = job_names.copy()
    random.shuffle(order)
    return order

# Generate new solution using Levy-inspired swaps
def levy_flight(order):
    new_order = order.copy()

    # Heavy-tailed step size
    step = min(
        n,
        max(1, int(random.paretovariate(1.5)))
    )

    for _ in range(step):
        i, j = random.sample(range(n), 2)
        new_order[i], new_order[j] = (
            new_order[j], new_order[i]
        )

    return new_order

# Abandon worst nests and create new ones
def abandon_nests(nests):

    nests.sort(key=fitness)

    keep = int(NESTS * (1 - PA))

    new_nests = nests[:keep]

    while len(new_nests) < NESTS:
        new_nests.append(create_nest())

    return new_nests

# Cuckoo Search Algorithm
def cuckoo_search():

    nests = [create_nest() for _ in range(NESTS)]

    best_nest = min(nests, key=fitness).copy()

    for iteration in range(ITERATIONS):

        # Select a random nest
        index = random.randrange(NESTS)

        # Generate new solution
        new_solution = levy_flight(nests[index])

        # Compare and replace
        if fitness(new_solution) < fitness(nests[index]):
            nests[index] = new_solution

        # Abandon some nests
        nests = abandon_nests(nests)

        # Update best solution
        current_best = min(nests, key=fitness)

        if fitness(current_best) < fitness(best_nest):
            best_nest = current_best.copy()

    return best_nest

# Display machine schedules
def display_schedule(order):

    machines = [[], []]
    loads = [0, 0]

    for job in order:

        machine = 0 if loads[0] <= loads[1] else 1

        machines[machine].append(job)
        loads[machine] += jobs[job]

    for i in range(2):
        print("Machine", i + 1, ":", end=" ")

        for job in machines[i]:
            print(job, end=" ")

        print("| Total Time:", loads[i], "minutes")

    print("Makespan:", max(loads), "minutes")


# Main program
if __name__ == "__main__":

    best_order = cuckoo_search()

    print("JOB SCHEDULING USING CUCKOO SEARCH")
    print("----------------------------------")

    print("Optimized Job Order:")
    print(" -> ".join(best_order))

    print("----------------------------------")

    print("Job Processing Times:")

    for job in best_order:
        print(job, ":", jobs[job], "minutes")

    print("----------------------------------")

    print("Optimized Machine Schedule:")
    display_schedule(best_order)

    print("----------------------------------")
    print("Optimization Completed Successfully!")