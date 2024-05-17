import random

# Number of items
num_items = 100

# Generate random weights and values for each item
items = [(random.randint(1, 100), random.randint(1, 100)) for _ in range(num_items)]

# Write the data to a file
with open('data.txt', 'w') as file:
    for weight, value in items:
        file.write(f"{weight} {value}\n")

print("Data file generated successfully.")
