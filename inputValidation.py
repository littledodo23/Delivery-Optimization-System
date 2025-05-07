def get_float(prompt, min_val=0.0, max_val=100.0):
    while True:
        user_input = input(prompt)
        try:
            value = float(user_input)
            if not min_val <= value <= max_val:
                print(f"❌ Value out of range. Please enter a number between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print(f"❌ Invalid input: '{user_input}' is not a valid number.")

def get_int(prompt, min_val=1, max_val=5):
    while True:
        user_input = input(prompt)
        try:
            value = int(user_input)
            if not min_val <= value <= max_val:
                print(f"❌ Value out of range. Please enter an integer between {min_val} and {max_val}.")
            else:
                return value
        except ValueError:
            print(f"❌ Invalid input: '{user_input}' is not a valid integer.")

def get_valid_weight(prompt, min_val, max_val, vehicle_capacity):
    while True:
        try:
            weight = float(input(prompt))
            if not (min_val <= weight <= max_val):
                print(f"❌ Value out of range. Please enter a number between {min_val} and {max_val}.")
            elif weight > vehicle_capacity:
                print("⚠️ This package exceeds vehicle capacity. Please enter a lighter weight.")
            else:
                return weight
        except ValueError:
            print("❌ Invalid input. Please enter a numeric value.")

