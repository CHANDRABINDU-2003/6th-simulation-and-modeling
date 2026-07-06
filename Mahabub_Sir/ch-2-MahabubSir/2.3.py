import numpy as np
import matplotlib.pyplot as plt

# function to integrate
def fun(x):
    return x ** 3

# exact value of integral
def exact_value():
    return (5**4 - 2**4) / 4


class MonteCarloIntegration:
    def __init__(self, x_min, x_max, y_min, y_max, N=10000):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.N = N

        self.errors = []  # store error
        self.steps = []   # store iteration steps

    def run(self):
        # generate random points (vectorized)
        x = np.random.uniform(self.x_min, self.x_max, self.N)
        y = np.random.uniform(self.y_min, self.y_max, self.N)

        # true function values
        f_x = fun(x)

        # inside condition
        inside = np.sum(y <= f_x)

        # rectangle area
        box_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)

        # final estimate
        estimate = (inside / self.N) * box_area

        return estimate

    def convergence_test(self):
        # test accuracy for increasing N
        for i in range(200, self.N + 1, 200):
            x = np.random.uniform(self.x_min, self.x_max, i)
            y = np.random.uniform(self.y_min, self.y_max, i)

            inside = np.sum(y <= fun(x))

            box_area = (self.x_max - self.x_min) * (self.y_max - self.y_min)

            estimate = (inside / i) * box_area
            error = abs(estimate - exact_value())

            self.steps.append(i)
            self.errors.append(error)

            print(f"N={i}, Estimate={estimate:.4f}, Error={error:.4f}")

    def plot_error(self):
        # plot error vs N
        plt.plot(self.steps, self.errors, color="purple")
        plt.title("Error decreases with N (Monte Carlo)")
        plt.xlabel("Iterations (N)")
        plt.ylabel("Error")
        plt.grid()
        plt.show()


# ---------------- main ----------------
if __name__ == "__main__":

    mc = MonteCarloIntegration(2, 5, 0, 140, 10000)

    # compute final estimate
    estimate = mc.run()

    # exact value
    actual = exact_value()

    # print results
    print("\nFINAL RESULT")
    print("------------")
    print(f"Actual   : {actual:.4f}")
    print(f"Estimate : {estimate:.4f}")
    print(f"Error    : {abs(actual - estimate):.4f}")

    # convergence study
    mc.convergence_test()

    # error plot
    mc.plot_error()