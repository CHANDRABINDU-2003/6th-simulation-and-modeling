import numpy as np
import matplotlib.pyplot as plt

# monte carlo pi estimation
def pi_estimation(N=1000000):

    # generate points
    x = np.random.random(N)
    y = np.random.random(N)

    # inside circle condition
    inside = (x*x + y*y <= 1)

    # estimate pi
    pi = 4 * np.sum(inside) / N

    return pi, x, y, inside


# run simulation
pi_value, x, y, inside = pi_estimation()

print("Estimated Pi:", pi_value)


# optional plot (small sample for speed)
sample = 5000

plt.scatter(x[:sample][inside[:sample]],
            y[:sample][inside[:sample]],
            color="blue", alpha=0.3, label="Inside")

plt.scatter(x[:sample][~inside[:sample]],
            y[:sample][~inside[:sample]],
            color="gray", alpha=0.3, label="Outside")

plt.title("Monte Carlo Pi Estimation")
plt.legend()
plt.grid()
plt.show()