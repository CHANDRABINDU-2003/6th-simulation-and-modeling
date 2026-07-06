import random
import numpy as np
import matplotlib.pyplot as plt


class RandomWalk:
    def __init__(self, steps=100):
        self.steps = steps
        self.x = 0
        self.y = 0
        self.path = [(0, 0)]

    def reset(self):
        self.x = 0
        self.y = 0
        self.path = [(0, 0)]

    def run(self):
        for _ in range(self.steps):
            r = random.randint(0, 9)

            if r <= 5:
                self.y += 1
            elif r <= 8:
                self.x -= 1
            else:
                self.x += 1

            self.path.append((self.x, self.y))

        return self.x, self.y

    def plot_path(self):
        x, y = zip(*self.path)

        plt.plot(x, y, marker='o', alpha=0.6)

        # red dot for final position
        plt.scatter(x[-1], y[-1], color='red', s=120, label="Final Position")

        plt.title("Random Walk Path")
        plt.legend()
        plt.grid()
        plt.show()

    def multi_run(self, runs=1000):
        results = []

        for _ in range(runs):
            results.append(self.run())
            self.reset()

        results = np.array(results)

        plt.scatter(results[:, 0], results[:, 1], alpha=0.3)

        # red dot for mean final position
        plt.scatter(np.mean(results[:, 0]), np.mean(results[:, 1]),
                    color='red', s=150, label="Mean Final Position")

        plt.title("Final Positions of Random Walks")
        plt.legend()
        plt.grid()
        plt.show()

        return results


if __name__ == "__main__":
    walk = RandomWalk(steps=100)

    print("Final position:", walk.run())
    walk.plot_path()

    results = walk.multi_run(1000)

    print("Mean X:", np.mean(results[:, 0]))
    print("Mean Y:", np.mean(results[:, 1]))