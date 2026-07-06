import math
import matplotlib.pyplot as plt

# -----------------------------
# Initial positions and speeds
# -----------------------------
xf = [0]
yf = [50]

xb = [100]
yb = [0]

fighter_speed = 20
bomber_speed = 15

capture_distance = 5      # fighter must come very close
danger_distance = 40      # bomber starts fleeing


# -----------------------------
# Helper functions
# -----------------------------
def calc_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def sin_theta(x1, y1, x2, y2):
    d = calc_distance(x1, y1, x2, y2)
    return (y2 - y1) / d

def cos_theta(x1, y1, x2, y2):
    d = calc_distance(x1, y1, x2, y2)
    return (x2 - x1) / d


# -----------------------------
# Simulation function
# -----------------------------
def simulate_flight():
    iteration = 0

    while True:
        # Fighter moves toward bomber
        xf.append(
            xf[-1] + fighter_speed *
            cos_theta(xf[-1], yf[-1], xb[-1], yb[-1])
        )
        yf.append(
            yf[-1] + fighter_speed *
            sin_theta(xf[-1], yf[-1], xb[-1], yb[-1])
        )

        distance = calc_distance(xf[-1], yf[-1], xb[-1], yb[-1])
        print(f"Iteration {iteration+1}, Distance = {distance:.2f}")

        # Bomber behavior
        if distance < danger_distance:
            # Bomber flees away from fighter
            xb.append(
                xb[-1] - bomber_speed *
                cos_theta(xf[-1], yf[-1], xb[-1], yb[-1])
            )
            yb.append(
                yb[-1] - bomber_speed *
                sin_theta(xf[-1], yf[-1], xb[-1], yb[-1])
            )
        else:
            # Bomber moves normally
            xb.append(xb[-1] + bomber_speed)
            yb.append(yb[-1] + 2)

        iteration += 1

        if distance <= capture_distance or iteration > 15:
            break


# -----------------------------
# Animation function
# -----------------------------
def plot_fight_animation():
    plt.ion()
    fig, ax = plt.subplots()

    ax.set_xlim(0, 300)
    ax.set_ylim(0, 150)

    fighter_line, = ax.plot([], [], 'b-', label='Fighter Path')
    bomber_line, = ax.plot([], [], 'r-', label='Bomber Path')

    fighter_point, = ax.plot([], [], 'bo')
    bomber_point, = ax.plot([], [], 'ro')

    ax.legend()
    ax.grid()

    for i in range(len(xf)):
        fighter_line.set_data(xf[:i+1], yf[:i+1])
        bomber_line.set_data(xb[:i+1], yb[:i+1])

        # IMPORTANT FIX: single points must be lists
        fighter_point.set_data([xf[i]], [yf[i]])
        bomber_point.set_data([xb[i]], [yb[i]])

        plt.pause(0.5)

    plt.ioff()
    plt.show()


# -----------------------------
# Run simulation
# -----------------------------
simulate_flight()
plot_fight_animation()
