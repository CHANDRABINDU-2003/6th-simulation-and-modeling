import math
import random
import matplotlib.pyplot as plt


# Poisson PMF

def poisson_pmf(x, lam):
    return math.exp(-lam) * (lam ** x) / math.factorial(x)



# Part 1: Probability table (λ = 5)

lam = 5
print("Poisson Probabilities (λ = 5)\n")

for x in range(11):  # 0 to 10
    p = poisson_pmf(x, lam)
    print(f"P(X = {x}) = {p:.5f}")


# Part 2: Simulate Poisson

def simulate_poisson(lam):
    u = random.random()
    x = 0
    cumulative = poisson_pmf(0, lam)

    while u > cumulative:
        x += 1
        cumulative += poisson_pmf(x, lam)

    return x


samples = [simulate_poisson(5) for _ in range(1000)]

plt.figure()
plt.hist(samples, bins=range(0, max(samples) + 2), density=True, edgecolor='black')
plt.title('Simulated Poisson Distribution (λ = 5)')
plt.xlabel('Number of calls')
plt.ylabel('Relative Frequency')
plt.grid()



# Part 3: PMF graph λ = 10

x_vals = list(range(25))
pmf_10 = [poisson_pmf(x, 10) for x in x_vals]

plt.figure()
plt.stem(x_vals, pmf_10, basefmt=" ")
plt.title('Poisson PMF (λ = 10)')
plt.xlabel('Number of calls')
plt.ylabel('Probability')
plt.grid()



# Part 4: PMF graph λ = 15

pmf_15 = [poisson_pmf(x, 15) for x in x_vals]

plt.figure()
plt.stem(x_vals, pmf_15, basefmt=" ")
plt.title('Poisson PMF (λ = 15)')
plt.xlabel('Number of calls')
plt.ylabel('Probability')
plt.grid()

plt.show()