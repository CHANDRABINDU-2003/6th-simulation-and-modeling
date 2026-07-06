import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


class RandomWalk3D:
    def __init__(self, steps=100):
        self.steps = steps
        self.x = 0
        self.y = 0
        self.z = 0
        self.path = [(0, 0, 0)]

    def reset(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.path = [(0, 0, 0)]

    def run(self):
        for _ in range(self.steps):
            r = random.randint(0, 11)

            if r <= 2:
                self.y += 1
            elif r <= 5:
                self.x -= 1
            elif r <= 8:
                self.x += 1
            else:
                self.z += 1

            self.path.append((self.x, self.y, self.z))

        return self.x, self.y, self.z

    def plot_path(self):
        x, y, z = zip(*self.path)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.plot(x, y, z, alpha=0.7)

        # final position (red dot)
        ax.scatter(x[-1], y[-1], z[-1], color='red', s=120, label="Final Position")

        ax.set_title("3D Random Walk Path")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        plt.legend()
        plt.show()

    def multi_run(self, runs=1000):
        results = []

        for _ in range(runs):
            results.append(self.run())
            self.reset()

        results = np.array(results)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        ax.scatter(results[:, 0], results[:, 1], results[:, 2], alpha=0.3)

        # mean final position (red dot)
        ax.scatter(np.mean(results[:, 0]),
                   np.mean(results[:, 1]),
                   np.mean(results[:, 2]),
                   color='red', s=150, label="Mean Position")

        ax.set_title("3D Final Positions of Random Walks")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")

        plt.legend()
        plt.show()

        return results


# ---------------- main ----------------
if __name__ == "__main__":
    walk = RandomWalk3D(steps=100)

    print("Final position:", walk.run())
    walk.plot_path()

    results = walk.multi_run(1000)

    print("Mean X:", np.mean(results[:, 0]))
    print("Mean Y:", np.mean(results[:, 1]))
    print("Mean Z:", np.mean(results[:, 2]))