# models.py

class Package:
    def __init__(self, id, destination, weight, priority):
        self.id = id  # unique identifier
        self.destination = destination  # (x, y)
        self.weight = weight  # in kg
        self.priority = priority  # 1 (highest) to 5 (lowest)

    def __repr__(self):
        return f"Package(id={self.id}, dest={self.destination}, weight={self.weight}, priority={self.priority})"


class Vehicle:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.packages = []  # list of Package objects

    def add_package(self, package):
        if self.get_total_weight() + package.weight <= self.capacity:
            self.packages.append(package)
            return True
        return False

    def get_total_weight(self):
        return sum(p.weight for p in self.packages)

    def clear_packages(self):
        self.packages = []

    def __repr__(self):
        return f"Vehicle(id={self.id}, capacity={self.capacity}, total_weight={self.get_total_weight()})"
