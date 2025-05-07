# utils.py
import math
import matplotlib.pyplot as plt

SHOP_LOCATION = (0, 0)


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def total_route_distance(route):
    if not route:
        return 0
    distance = euclidean_distance(SHOP_LOCATION, route[0].destination)
    for i in range(len(route) - 1):
        distance += euclidean_distance(route[i].destination, route[i + 1].destination)
    distance += euclidean_distance(route[-1].destination, SHOP_LOCATION)
    return distance


# utils.py

def assign_packages_to_vehicles(packages, vehicles):
    # Sort packages by priority (lowest number = highest priority)
    packages = sorted(packages, key=lambda p: p.priority)

    for package in packages:
        # Sort vehicles by current load (greedy fit)
        vehicles = sorted(vehicles, key=lambda v: v.get_total_weight())

        for vehicle in vehicles:
            if vehicle.get_total_weight() + package.weight <= vehicle.capacity:
                vehicle.packages.append(package)
                print(f"Package {package.id} assigned to Vehicle {vehicle.id}")
                break
    return vehicles


def plot_routes(vehicles):
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for i, vehicle in enumerate(vehicles):
        x = [SHOP_LOCATION[0]]
        y = [SHOP_LOCATION[1]]
        for pkg in vehicle.packages:
            x.append(pkg.destination[0])
            y.append(pkg.destination[1])
        x.append(SHOP_LOCATION[0])
        y.append(SHOP_LOCATION[1])
        plt.plot(x, y, marker='o', label=f'Vehicle {vehicle.id}', color=colors[i % len(colors)])
    plt.legend()
    plt.title("Vehicle Delivery Routes")
    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.grid(True)
    plt.show()


def calculate_total_distance(vehicles):
    total = 0
    for v in vehicles:
        if not v.packages:
            continue
        route = [(0, 0)] + [p.destination for p in v.packages]
        for i in range(len(route) - 1):
            total += euclidean_distance(route[i], route[i + 1])
    return total


def plot_vehicles(vehicles, title="Delivery Routes"):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta']
    shop_location = (0, 0)

    plt.figure(figsize=(8, 6))
    plt.title(title)

    # Plot shop
    plt.plot(shop_location[0], shop_location[1], 'ko', label='Shop (0,0)')

    for i, vehicle in enumerate(vehicles):
        color = colors[i % len(colors)]
        x = [shop_location[0]]
        y = [shop_location[1]]

        for pkg in vehicle.packages:
            x.append(pkg.destination[0])
            y.append(pkg.destination[1])
            plt.text(pkg.destination[0], pkg.destination[1], f'P{pkg.id}', fontsize=8)

        # Return to shop (optional)
        x.append(shop_location[0])
        y.append(shop_location[1])

        plt.plot(x, y, color=color, marker='o', label=f'Vehicle {vehicle.id}')

    plt.xlabel("X (km)")
    plt.ylabel("Y (km)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def display_assignments(vehicles, title="Vehicle Assignments"):
    print(f"\n{title}:")
    for vehicle in vehicles:
        print(
            f"Vehicle {vehicle.id} has {len(vehicle.packages)} packages, Total Weight: {vehicle.get_total_weight():.2f} kg")
        for pkg in vehicle.packages:
            print(f"  - Package(id={pkg.id}, dest={pkg.destination}, weight={pkg.weight}, priority={pkg.priority})")


def plot_progress(distances, title="Optimization Progress"):
    plt.figure(figsize=(10, 5))
    plt.plot(distances, marker='o')
    plt.title(title)
    plt.xlabel("Iteration / Generation")
    plt.ylabel("Total Distance")
    plt.grid(True)
    plt.show()
