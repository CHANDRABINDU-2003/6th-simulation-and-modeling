import random
import matplotlib.pyplot as plt
import numpy as np
from shapely.geometry import Point, Polygon

# define polygon shape
coords = [(1, 1), (10, 95), (40, 70), (50, 50), (30, 20)]
polygon = Polygon(coords)

# plot polygon boundary
x, y = zip(*coords)
plt.plot(x + (x[0],), y + (y[0],), color="black")

# initialize counters
inside = 0

# store inside points
x_inside, y_inside = [], []
# store outside points
x_outside, y_outside = [], []

# set iterations
TOTAL_ITERATIONS = 1000
AREA_BOX = 60 * 100

# track error over time
errors = []
iterations = []

# actual polygon area
actual_area = polygon.area

# monte carlo simulation
for i in range(1, TOTAL_ITERATIONS + 1):

    # generate random point
    x_rand = random.uniform(0, 60)
    y_rand = random.uniform(0, 100)
    point = Point(x_rand, y_rand)

    # check inside polygon
    if polygon.contains(point):
        inside += 1
        x_inside.append(x_rand)
        y_inside.append(y_rand)
    else:
        x_outside.append(x_rand)
        y_outside.append(y_rand)

    # estimate area
    estimated_area = (inside / i) * AREA_BOX

    # compute error
    error = abs(estimated_area - actual_area)

    # store values
    errors.append(error)
    iterations.append(i)

    # print progress every 100 steps
    if i % 100 == 0:
        print(f"N={i}, Estimated Area={estimated_area:.2f}, Error={error:.2f}")

# final estimation
final_estimated_area = (inside / TOTAL_ITERATIONS) * AREA_BOX

# print final results
print("\nFINAL RESULT")
print("-------------")
print(f"Actual Area     : {actual_area:.2f}")
print(f"Estimated Area  : {final_estimated_area:.2f}")
print(f"Final Error     : {abs(final_estimated_area - actual_area):.2f}")

# plot monte carlo points
plt.figure()
plt.plot(x_inside, y_inside, 'yo', alpha=0.2, label="Inside (Yellow)")
plt.plot(x_outside, y_outside, 'ro', alpha=0.2, label="Outside (Red)")
plt.title("Monte Carlo Area Estimation")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.show()

# plot error convergence
plt.figure()
plt.plot(iterations, errors, label="Error", color="blue")

# theoretical trend
theory = [1000 / np.sqrt(n) for n in iterations]
plt.plot(iterations, theory, label="1/sqrt(N) trend", color="green")

plt.title("Error vs Iterations")
plt.xlabel("Iterations (N)")
plt.ylabel("Error")
plt.legend()
plt.show()