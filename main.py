from utils import assign_packages_to_vehicles, calculate_total_distance, plot_vehicles
from simulated_annealing import simulated_annealing
from ga import genetic_algorithm
from models import Package, Vehicle
from inputValidation import get_int, get_float,get_valid_weight
import time



def display_assignments(vehicles, title):
    print(f"\n{title}")
    for v in vehicles:
        print(f"Vehicle {v.id} has {len(v.packages)} packages, Total Weight: {v.get_total_weight():.2f} kg")
        for pkg in v.packages:
            print(f"  - {pkg}")


def main():
    print("Welcome to the Delivery Optimization System 🤝🏻\n")

    # User inputs
    num_packages = get_int("enter the number of packages you would like deliver:",1,100)
    while True:
        num_vehicles = get_int("enter the number of vehicles :",1,100)
        if num_vehicles < 2:
            print("⚠️ Optimization methods require at least 2 vehicles to work properly. Please enter 2 or more.")
        else:
            break

    vehicle_capacity = get_float("enter the capacity of the vehicles(kg) :",1,100)


    # Collect package details from user
    packages = []
    for i in range(num_packages):
        print(f"\nEnter details for Package {i + 1}:")
        x = get_float("  Destination X (0–100): ", 0, 100)
        y = get_float("  Destination Y (0–100): ", 0, 100)
        weight = get_valid_weight("  Weight (kg): ", 1, 1000, vehicle_capacity)

        # Assuming max weight reasonable
        priority = get_int("  Priority (1–5): ", 1, 5)
        packages.append(Package(id=i, destination=(x, y), weight=weight, priority=priority))

    # Create vehicles
    vehicles = [Vehicle(id=i, capacity=vehicle_capacity) for i in range(num_vehicles)]

    print("\nGenerated Packages:")
    for pkg in packages:
        print(pkg)

    print("\nGenerated Vehicles:")
    for v in vehicles:
        print(v)

    # Initial assignment
    vehicles = assign_packages_to_vehicles(packages, vehicles)

    initial_distance = calculate_total_distance(vehicles)
    print(f"\nInitial total distance: {initial_distance:.2f} km")

    plot_vehicles(vehicles, "Initial Routes")

    # Optimization method selection




    while True:
        print("\nChoose Optimization Method:")
        print("1. Simulated Annealing")
        print("2. Genetic Algorithm")

        print("E. Exit")

        algo_choice = input("Enter 1, 2 or  to exit: ").strip().lower()

        if algo_choice == "1":
            optimized_vehicles = simulated_annealing(vehicles, packages)
            method = "Simulated Annealing"
            start_time = time.time()

        elif algo_choice == "2":
            optimized_vehicles = genetic_algorithm(packages, num_vehicles, vehicle_capacity)
            method = "Genetic Algorithm"
            start_time = time.time()
      ##  elif algo_choice =="r":
         ##   optimized_vehicles=assign_packages_to_vehicles(packages, vehicles)



        elif algo_choice == "e":
            print("Exiting the system. Goodbye 👋")
            break
        else:
            print("❌ Invalid input. Please enter 1, 2,  or E.")
            continue

        print(f"\nOptimized Vehicle Assignments using {method}:")
        display_assignments(optimized_vehicles, "Optimized Vehicle Assignments")

        optimized_distance = calculate_total_distance(optimized_vehicles)
        print(f"\nOptimized total distance: {optimized_distance:.2f} km")

        improvement = ((initial_distance - optimized_distance) / initial_distance) * 100
        print(f"Improvement: {improvement:.2f}%")
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"⏱ Execution Time: {elapsed_time:.6f} seconds")

        plot_vehicles(optimized_vehicles, f"Optimized Routes - {method}")


if __name__ == "__main__":
    main()
