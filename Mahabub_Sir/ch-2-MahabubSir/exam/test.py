import numpy as np
import matplotlib.pyplot as plt


class ReliabilityProblem:
    def __init__(self, simulations=1000):
        self.simulations = simulations

        self.life_vals = np.array([1200, 1400, 1600, 1800, 2000])
        self.life_probs = np.array([0.10, 0.25, 0.30, 0.25, 0.10])

        self.delay_vals = np.array([2, 3, 4, 8])
        self.delay_probs = np.array([0.2, 0.3, 0.3, 0.2])

    def sample(self, values, probs):
        return np.random.choice(values, p=probs)

    def simulate(self, policy, time_limit=50000):
        total_cost = np.zeros(self.simulations)

        for i in range(self.simulations):
            clock = 0

            lives = np.random.choice(
                self.life_vals,
                size=4,
                p=self.life_probs
            ).astype(float)

            while clock < time_limit:
                idx = np.argmin(lives)
                fail_time = lives[idx]

                clock += fail_time
                lives -= fail_time

                delay = np.random.choice(self.delay_vals, p=self.delay_probs)

                # POLICY DEFINITIONS
                if policy == 1:
                    replace = [idx]
                    repair = 15

                elif policy == 2:
                    others = [j for j in range(4) if j != idx]
                    extra = np.random.choice(others)
                    replace = [idx, extra]
                    repair = 25

                elif policy == 3:
                    others = [j for j in range(4) if j != idx]
                    extra = list(np.random.choice(others, 2, replace=False))
                    replace = [idx] + extra
                    repair = 30

                else:
                    replace = [0, 1, 2, 3]
                    repair = 35

                downtime = delay + repair

                cost = downtime * 5 + downtime * 0.5 + len(replace) * 30
                total_cost[i] += cost

                # reset replaced bearings
                for j in replace:
                    lives[j] = np.random.choice(self.life_vals, p=self.life_probs)

        return np.mean(total_cost)


if __name__ == "__main__":
    model = ReliabilityProblem(simulations=500)

    c1 = model.simulate(policy=1)
    c2 = model.simulate(policy=2)
    c3 = model.simulate(policy=3)
    c4 = model.simulate(policy=4)

    print("\n--- COST RESULTS ---")
    print("Policy 1 (1 bearing):", c1)
    print("Policy 2 (2 bearings):", c2)
    print("Policy 3 (3 bearings):", c3)
    print("Policy 4 (4 bearings):", c4)

    # Store results
    policies = {
        "Policy 1 (1 bearing)": c1,
        "Policy 2 (2 bearings)": c2,
        "Policy 3 (3 bearings)": c3,
        "Policy 4 (4 bearings)": c4
    }

    # Find best policy (minimum cost)
    best_policy = min(policies, key=policies.get)

    print("\n--- RECOMMENDED POLICY ---")
    print("Best strategy is:", best_policy)
    print("Minimum expected cost:", policies[best_policy])

    # Plot results
    labels = list(policies.keys())
    values = list(policies.values())

    plt.figure()
    plt.bar(labels, values)
    plt.xlabel("Policy")
    plt.ylabel("Total Cost")
    plt.title("Policy Comparison")
    plt.xticks(rotation=20)
    plt.show()