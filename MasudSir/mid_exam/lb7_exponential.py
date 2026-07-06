import math
import numpy as np
import matplotlib.pyplot as plt


# Part 1: Analytical probability

mean_days = 100
lam = 1 / mean_days
x = 150

prob_more_than_120 = math.exp(-lam * x)

print("Exponential Distribution")
print(f"Rate (lambda) = {lam:.4f}")
print(f"P(X > 80 days) = {prob_more_than_120:.5f}")


# Exponential PDF

def exponential_pdf(x, lam):
    return lam * np.exp(-lam * x)



# Part 2: Simulations for different rates

rates = [0.5, 1.0, 2.0, 4.0]
x_vals = np.linspace(0, 10, 1000)

plt.figure()

for r in rates:
    y = exponential_pdf(x_vals, r)
    plt.plot(x_vals, y, linewidth=2, label=f'λ = {r}')

plt.title('Exponential Distributions for Different Rates')
plt.xlabel('Time')
plt.ylabel('Density')
plt.legend()
plt.grid()



# Part 3: Random sample example

plt.figure()

for r in rates:
    samples = np.random.exponential(1/r, 1000)
    plt.hist(samples, bins=40, density=True, alpha=0.5, label=f'λ={r}')

plt.title('Simulated Exponential Samples')
plt.xlabel('Value')
plt.ylabel('Relative Frequency')
plt.legend()
plt.grid()

plt.show()