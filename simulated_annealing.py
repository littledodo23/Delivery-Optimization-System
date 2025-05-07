# simulated_annealing.py
import copy
import math
import random
from utils import calculate_total_distance



def swap_packages_between_vehicles(vehicles):
    v1, v2 = random.sample(vehicles, 2)
    if not v1.packages or not v2.packages:
        return

    p1 = random.choice(v1.packages)
    p2 = random.choice(v2.packages)

    if (v1.get_total_weight() - p1.weight + p2.weight <= v1.capacity and
            v2.get_total_weight() - p2.weight + p1.weight <= v2.capacity):
        v1.packages.remove(p1)
        v2.packages.remove(p2)
        v1.packages.append(p2)
        v2.packages.append(p1)


def calculate_priority_weighted_distance(vehicles):
    total = 0
    for v in vehicles:
        if not v.packages:
            continue

        route = [(0, 0)] + [pkg.destination for pkg in v.packages] + [(0, 0)]
        dist = sum(math.dist(route[i], route[i + 1]) for i in range(len(route) - 1))

        # Apply a light penalty based on total priority to encourage better ordering
        priority_penalty = sum(pkg.priority for pkg in v.packages) * 0.1
        total += dist + priority_penalty
    return total


def simulated_annealing(initial_vehicles, packages, initial_temp=1000, cooling_rate=0.98, stop_temp=1,
                        iterations_per_temp=100):
    current_solution = copy.deepcopy(initial_vehicles)
    current_cost = calculate_priority_weighted_distance(current_solution)
    best_solution = copy.deepcopy(current_solution)
    best_cost = current_cost

    T = initial_temp

    while T > stop_temp:
        for _ in range(iterations_per_temp):
            new_solution = copy.deepcopy(current_solution)
            swap_packages_between_vehicles(new_solution)

            new_cost = calculate_priority_weighted_distance(new_solution)
            delta = new_cost - current_cost

            if delta < 0 or random.random() < math.exp(-delta / T):
                current_solution = new_solution
                current_cost = new_cost
                if current_cost < best_cost:
                    best_solution = copy.deepcopy(current_solution)
                    best_cost = current_cost

        T *= cooling_rate

    return best_solution
