import random
import math
import matplotlib.pyplot as plt

# Bernoulli trial
def bernoulli(p):
    return 1 if random.random() < p else 0


# Binomial random variable
def binomial(n, p):
    return sum(bernoulli(p) for _ in range(n))


# Binomial PMF
def binomial_pmf(x, n, p):
    comb = math.comb(n, x)
    return comb * (p ** x) * ((1 - p) ** (n - x))


# Parameters
n = 10
p = 0.5
num_samples = 1000

# Generate samples
samples = [binomial(n, p) for _ in range(num_samples)]

# Print theoretical probabilities
print("Binomial Distribution (n=10, p=0.5)\n")
for x in range(n + 1):
    print(f"P(X={x}) = {binomial_pmf(x, n, p):.5f}")

# Plot simulated histogram
plt.figure()
plt.hist(samples, bins=range(0, n + 2), density=True, edgecolor='black')
plt.title(f'Simulated Binomial Distribution (n={n}, p={p})')
plt.xlabel('Number of successes')
plt.ylabel('Relative Frequency')
plt.grid()

# Plot theoretical PMF
x_vals = list(range(n + 1))
pmf_vals = [binomial_pmf(x, n, p) for x in x_vals]

plt.figure()
plt.stem(x_vals, pmf_vals, basefmt=" ")
plt.title(f'Binomial PMF (n={n}, p={p})')
plt.xlabel('Number of successes')
plt.ylabel('Probability')
plt.grid()

plt.show()