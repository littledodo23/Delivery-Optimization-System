from utils import assign_packages_to_vehicles, calculate_total_distance, plot_vehicles
from simulated_annealing import simulated_annealing
from ga import genetic_algorithm
from models import Package, Vehicle
import time
import random


def display_assignments(vehicles, title):
    print(f"\n{title}")
    for v in vehicles:
        print(f"Vehicle {v.id} has {len(v.packages)} packages, Total Weight: {v.get_total_weight():.2f} kg")
        for pkg in v.packages:
            print(f"  - {pkg}")

def main():
    print("Welcome to the Delivery Optimization System 🤝🏻\n")

    # Predefined inputs for scalability test
    num_packages = 100
    num_vehicles = 10
    vehicle_capacity = 100

    # Create random packages
    packages = []
    for i in range(num_packages):
        x = random.uniform(0, 100)
        y = random.uniform(0, 100)
        weight = round(random.uniform(1, vehicle_capacity), 2)
        priority = random.randint(1, 5)
        packages.append(Package(id=i, destination=(x, y), weight=weight, priority=priority))

    # Display all generated packages
    print("\n✅ Generated 100 random packages:")
    for pkg in packages:
        print(pkg)

    # Create vehicles
    vehicles = [Vehicle(id=i, capacity=vehicle_capacity) for i in range(num_vehicles)]

    print("\n✅ Generated Vehicles:")
    for v in vehicles:
        print(v)

    # Initial assignment
    vehicles = assign_packages_to_vehicles(packages, vehicles)

    initial_distance = calculate_total_distance(vehicles)
    print(f"\n📏 Initial total distance: {initial_distance:.2f} km")

    display_assignments(vehicles, "Initial Vehicle Assignments")
    plot_vehicles(vehicles, "Initial Routes")

    # Optimization method selection
    while True:
        print("\nChoose Optimization Method:")
        print("1. Simulated Annealing")
        print("2. Genetic Algorithm")
        print("E. Exit")

        algo_choice = input("Enter 1, 2 or E to exit: ").strip().lower()

        if algo_choice == "1":
            start_time = time.time()
            optimized_vehicles = simulated_annealing(vehicles, packages)
            end_time = time.time()
            method = "Simulated Annealing"

        elif algo_choice == "2":
            start_time = time.time()
            optimized_vehicles = genetic_algorithm(packages, num_vehicles, vehicle_capacity)
            end_time = time.time()
            method = "Genetic Algorithm"

        elif algo_choice == "e":
            print("Exiting the system. Goodbye 👋")
            break
        else:
            print("❌ Invalid input. Please enter 1, 2, or E.")
            continue

        print(f"\nOptimized Vehicle Assignments using {method}:")
        display_assignments(optimized_vehicles, "Optimized Vehicle Assignments")

        optimized_distance = calculate_total_distance(optimized_vehicles)
        print(f"\nOptimized total distance: {optimized_distance:.2f} km")

        improvement = ((initial_distance - optimized_distance) / initial_distance) * 100
        print(f"Improvement: {improvement:.2f}%")

        elapsed_time = end_time - start_time
        print(f"⏱ Execution Time: {elapsed_time:.6f} seconds")

        plot_vehicles(optimized_vehicles, f"Optimized Routes - {method}")


if __name__ == "__main__":
    main()
