import random
import matplotlib.pyplot as plt

# Generic function to generate random variates using inverse transform
def generate_random_variates(inverse_cdf, n):
    """
    inverse_cdf : function
        A function representing the inverse CDF (F^-1) of the distribution
    n : int
        Number of random variates to generate
    """
    random_variates = []
    for _ in range(n):
        U = random.random()  # uniform random number between 0 and 1
        X = inverse_cdf(U)   # apply inverse CDF
        random_variates.append(X)
    return random_variates

# Example: Exponential distribution with rate lambda = 2
def exponential_inverse_cdf(u, rate_lambda=2):
    return - (1 / rate_lambda) * (math.log(1 - u))

# Generate 1000 exponential random variates
import math
n = 1000
exp_variates = generate_random_variates(lambda u: exponential_inverse_cdf(u, rate_lambda=2), n)

# Print first 10 variates
print("First 10 exponential variates:", exp_variates[:10])

# Plot histogram
plt.hist(exp_variates, bins=30, density=True, color="skyblue", edgecolor="black", alpha=0.6)
plt.title("Histogram of Exponential Random Variates")
plt.xlabel("Value")
plt.ylabel("Density")
plt.show()