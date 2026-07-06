import matplotlib.pyplot as plt

# LCG generator
def lcg(seed, a, c, m, n):
    numbers = []
    x = seed

    for _ in range(n):
        x = (a * x + c) % m
        numbers.append(x / m)  # normalize to (0,1)

    return numbers


# Parameters (standard example)
seed = 7
a = 1103515245
c = 12345
m = 2**31
n = 1000

# Generate numbers
random_numbers = lcg(seed, a, c, m, n)

# Print first 10 numbers
print("First 10 LCG random numbers:")
for i in range(10):
    print(f"{i+1}: {random_numbers[i]:.6f}")

# Plot histogram
plt.figure()
plt.hist(random_numbers, bins=20, edgecolor='black', density=True)
plt.title('LCG Random Number Distribution')
plt.xlabel('Random Number')
plt.ylabel('Relative Frequency')
plt.grid()

plt.show()