import random
import math
import numpy as np
import matplotlib.pyplot as plt


# Normal PDF
def normal_distribution(x, mu, sigma):
    exponent = math.exp(-((x - mu) ** 2) / (2 * sigma ** 2))
    coefficient = 1 / (sigma * math.sqrt(2 * math.pi))
    return coefficient * exponent


# --- Unimodal Normal ---
x_values = np.linspace(-4, 4, 1000)
density_values = [normal_distribution(x, 0, 1) for x in x_values]

plt.figure()
plt.plot(x_values, density_values, linewidth=2, label='Unimodal (μ=0, σ=1)')
plt.title('Normal Distribution Density Function')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()


# --- Multimodal ---
multimodal_density = [
    0.5 * normal_distribution(x, -1, 0.5)
    + 0.5 * normal_distribution(x, 1, 0.7)
    for x in x_values
]

plt.figure()
plt.plot(x_values, multimodal_density, linewidth=2, label='Multimodal')
plt.title('Multimodal Distribution Density Function')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.legend()
plt.grid()


# Exponential PDF
def exponential_distribution(x, beta):
    return (1 / beta) * math.exp(-(x / beta)) if x >= 0 else 0


x_values = np.linspace(0, 20, 1000)
density_values = [exponential_distribution(x, 5) for x in x_values]

plt.figure()
plt.plot(x_values, density_values, linewidth=2)
plt.title('Exponential Distribution Density Function (beta=5)')
plt.xlabel('Value')
plt.ylabel('Probability Density')
plt.grid()


# Bernoulli
def bernoulli(u, p):
    return 1 if u < p else 0


bernoulli_values = [bernoulli(random.random(), 0.5) for _ in range(1000)]

plt.figure()
plt.hist(bernoulli_values, bins=3, edgecolor='black', density=True)
plt.xticks([0, 1])
plt.title('Bernoulli Distribution (p=0.5)')
plt.xlabel('Value')
plt.ylabel('Relative Frequency')


# Binomial
def binomial(uniform_randoms, p):
    return sum(bernoulli(ur, p) for ur in uniform_randoms)


binomial_values = [
    binomial([random.random() for _ in range(10)], 0.5)
    for _ in range(1000)
]

plt.figure()
plt.hist(binomial_values, bins=20, edgecolor='black', density=True)
plt.title('Binomial Distribution (n=10, p=0.5)')
plt.xlabel('Number of successes')
plt.ylabel('Relative Frequency')


# Poisson PMF
def get_mass(x, lam):
    numerator = math.exp(-lam) * (lam ** x)
    denominator = math.factorial(x)
    return numerator / denominator


poisson_values = [get_mass(x, 5) for x in range(20)]

plt.figure()
plt.plot(range(20), poisson_values, marker='o', linestyle='-')
plt.title('Poisson Distribution PMF (lambda=5)')
plt.xlabel('x')
plt.ylabel('P(X=x)')


# Simulated Poisson
def simulate_poisson(lam):
    u = random.random()
    x = 0
    running_total = get_mass(0, lam)

    while u > running_total:
        x += 1
        running_total += get_mass(x, lam)

    return x


poisson_samples = [simulate_poisson(5) for _ in range(1000)]

plt.figure()
plt.hist(
    poisson_samples,
    bins=range(0, max(poisson_samples) + 2),
    edgecolor='black',
    density=True,
)
plt.title('Simulated Poisson Distribution (lambda=5)')
plt.xlabel('Number of calls')
plt.ylabel('Relative Frequency')

plt.show()