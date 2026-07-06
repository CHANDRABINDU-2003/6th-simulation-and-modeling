import numpy as np


class ReliabilityProblem:
    def __init__(self, simulations=10000):
        self.simulations = simulations

        self.bearing_values = np.array([1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900])
        self.bearing_probs = np.array([0.10, 0.14, 0.24, 0.14, 0.12, 0.10, 0.06, 0.05, 0.03, 0.02])

        self.delay_values = np.array([4, 6, 8])
        self.delay_probs = np.array([0.30, 0.60, 0.10])

    def sample(self, values, probs, size):
        return np.random.choice(values, p=probs, size=size)

    def run_single_repair(self, time_limit=30000):
        total_cost = np.zeros(self.simulations)

        for i in range(self.simulations):
            clock = np.zeros(3)

            while True:
                life = self.sample(self.bearing_values, self.bearing_probs, 3)
                delay = self.sample(self.delay_values, self.delay_probs, 3)

                clock += life

                cost_bearings = 3 * 20
                total_delay = np.sum(delay)

                if np.all(clock == clock[0]):
                    repair_delay = 40
                elif clock[0] == clock[1] or clock[1] == clock[2] or clock[0] == clock[2]:
                    repair_delay = 50
                else:
                    repair_delay = 60

                downtime_cost = (total_delay + repair_delay) * 5
                repairman_cost = repair_delay * 25 / 60

                total_cost[i] += cost_bearings + downtime_cost + repairman_cost

                if np.min(clock) >= time_limit:
                    break

        return np.mean(total_cost)

    def run_all_repair(self, time_limit=30000):
        total_cost = np.zeros(self.simulations)

        for i in range(self.simulations):
            clock = 0
            total_delay = 0
            count = 0

            while clock < time_limit:
                life = self.sample(self.bearing_values, self.bearing_probs, 3)
                delay = self.sample(self.delay_values, self.delay_probs, 1)[0]

                clock += np.min(life)
                total_delay += delay
                count += 1

            cost_bearings = 3 * count * 20
            downtime_cost = (total_delay + count * 40) * 5
            repairman_cost = count * 40 * 25 / 60

            total_cost[i] = cost_bearings + downtime_cost + repairman_cost

        return np.mean(total_cost)


if __name__ == "__main__":
    model = ReliabilityProblem(simulations=5000)

    single_cost = model.run_single_repair(30000)
    all_cost = model.run_all_repair(30000)

    print("Single Repair Cost:", single_cost)
    print("All Repair Cost:", all_cost)