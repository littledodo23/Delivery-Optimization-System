import random
import math
import copy

from models import Vehicle
from utils import calculate_total_distance


# Initialize population: randomly assign packages to vehicles
def initialize_population(packages, num_vehicles, capacity, population_size):
    population = []
    for _ in range(population_size):
        shuffled = random.sample(packages, len(packages))
        vehicles = [[] for _ in range(num_vehicles)]
        vehicle_weights = [0] * num_vehicles

        for package in shuffled:
            for i in range(num_vehicles):
                if vehicle_weights[i] + package.weight <= capacity:
                    vehicles[i].append(package)
                    vehicle_weights[i] += package.weight
                    break
        population.append(vehicles)
    return population


# Wrap raw vehicle lists and compute fitness
def calculate_fitness(vehicles_as_lists):
    wrapped_vehicles = []
    for i, pkg_list in enumerate(vehicles_as_lists):
        v = Vehicle(i, capacity=9999)  # Capacity doesn't matter here
        v.packages = pkg_list
        wrapped_vehicles.append(v)

    return -calculate_total_distance(wrapped_vehicles)


# Selection with fitness-shifting
def selection(population, fitnesses):
    min_fit = min(fitnesses)
    if min_fit <= 0:
        fitnesses = [f - min_fit + 1 for f in fitnesses]  # shift to positive
    return random.choices(population, weights=fitnesses, k=2)


# Crossover: try to merge unique packages from both parents
def crossover(parent1, parent2, num_vehicles, capacity):
    child = [[] for _ in range(num_vehicles)]
    used = set()

    for i in range(num_vehicles):
        for pkg in parent1[i]:
            if pkg.id not in used:
                if sum(p.weight for p in child[i]) + pkg.weight <= capacity:
                    child[i].append(pkg)
                    used.add(pkg.id)

    for i in range(num_vehicles):
        for pkg in parent2[i]:
            if pkg.id not in used:
                if sum(p.weight for p in child[i]) + pkg.weight <= capacity:
                    child[i].append(pkg)
                    used.add(pkg.id)

    return child


# Mutation: swap packages between vehicles
def mutate(vehicles, capacity, mutation_rate):
    if random.random() > mutation_rate:
        return vehicles

    v1, v2 = random.sample(range(len(vehicles)), 2)
    if vehicles[v1] and vehicles[v2]:
        p1 = random.choice(vehicles[v1])
        p2 = random.choice(vehicles[v2])
        w1 = sum(pkg.weight for pkg in vehicles[v1]) - p1.weight + p2.weight
        w2 = sum(pkg.weight for pkg in vehicles[v2]) - p2.weight + p1.weight
        if w1 <= capacity and w2 <= capacity:
            vehicles[v1].remove(p1)
            vehicles[v2].remove(p2)
            vehicles[v1].append(p2)
            vehicles[v2].append(p1)
    return vehicles


# Genetic Algorithm Main
def genetic_algorithm(packages, num_vehicles, capacity, pop_size=80, mutation_rate=0.05, generations=500):
    population = initialize_population(packages, num_vehicles, capacity, pop_size)

    for gen in range(generations):
        fitnesses = [calculate_fitness(v) for v in population]
        new_population = []

        for _ in range(len(population)):
            parent1, parent2 = selection(population, fitnesses)
            child = crossover(parent1, parent2, num_vehicles, capacity)
            child = mutate(child, capacity, mutation_rate)
            new_population.append(child)

        population = new_population

    # Return best solution
    fitnesses = [calculate_fitness(v) for v in population]
    best_index = fitnesses.index(max(fitnesses))
    best_solution = population[best_index]

    # Wrap package lists into Vehicle objects
    wrapped_vehicles = []
    for i, pkg_list in enumerate(best_solution):
        v = Vehicle(i, capacity)
        v.packages = pkg_list
        wrapped_vehicles.append(v)

    return wrapped_vehicles



# Convert from lists to Vehicle objects for consistency
def convert_to_vehicle_objects(vehicle_lists, capacity):
    final = []
    for i, pkgs in enumerate(vehicle_lists):
        v = Vehicle(i, capacity)
        v.packages = pkgs
        final.append(v)
    return final
