import numpy as np

N = 1_000_000

mu = 0
sigma = 0.5

x_random = np.random.normal(mu, sigma, N)
y_random = np.random.normal(mu, sigma, N)

x_val = 500 * x_random
y_val = 300 * y_random

hit = np.sum((np.abs(x_val) <= 500) & (np.abs(y_val) <= 300))
miss = N - hit

strike_percentage = (hit / N) * 100

print("Strike Percentage:", strike_percentage)