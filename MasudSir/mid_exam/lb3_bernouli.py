import random
import matplotlib.pyplot as plt

# Bernoulli generator
def bernoulli(p):
    u = random.random()
    return 1 if u < p else 0


# Parameters
p = 0.5
n_samples = 1000

# Generate samples
samples = [bernoulli(p) for _ in range(n_samples)]

# Theoretical probabilities
print("Bernoulli Distribution")
print(f"P(X=1) = {p}")
print(f"P(X=0) = {1-p}")

# Sample mean
sample_mean = sum(samples) / n_samples
print(f"Sample Mean ≈ {sample_mean:.4f}")

# Plot histogram
plt.figure()
plt.hist(samples, bins=3, density=True, edgecolor='black')
plt.xticks([0, 1])
plt.title(f'Bernoulli Distribution (p={p})')
plt.xlabel('Outcome')
plt.ylabel('Relative Frequency')
plt.grid()
plt.show()