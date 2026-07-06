import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class ReliabilityProblem:
    def __init__(self, simulations=300):
        self.simulations = simulations

        # Life distribution
        self.life_vals = np.array([1200, 1400, 1600, 1800, 2000])
        self.life_probs = np.array([0.10, 0.25, 0.30, 0.25, 0.10])

        # Repair delay distribution
        self.delay_vals = np.array([2, 3, 4, 8])
        self.delay_probs = np.array([0.2, 0.3, 0.3, 0.2])

    def simulate(self, policy, time_limit=50000):
        total_cost = np.zeros(self.simulations)

        for i in range(self.simulations):
            clock = 0

            # 4 system components
            lives = np.random.choice(
                self.life_vals, size=4, p=self.life_probs
            ).astype(float)

            step_limit = 2000
            steps = 0

            while clock < time_limit and steps < step_limit:
                steps += 1

                # next failure
                idx = np.argmin(lives)
                fail_time = lives[idx]

                clock += fail_time
                lives -= fail_time

                delay = np.random.choice(self.delay_vals, p=self.delay_probs)

                # Policy decision
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

                # cost model
                total_cost[i] += (
                    downtime * 5 + downtime * 0.5 + len(replace) * 30
                )

                # replace components
                for j in replace:
                    lives[j] = np.random.choice(self.life_vals, p=self.life_probs)

        return np.mean(total_cost)


if __name__ == "__main__":
    np.random.seed(42)

    model = ReliabilityProblem(simulations=300)

    policies = {}
    runs = 10

    # Run multiple times for stability
    for p in [1, 2, 3, 4]:
        results = []
        for _ in range(runs):
            results.append(model.simulate(policy=p))
        policies[f"Policy {p}"] = np.mean(results)

    # Best / worst
    best_policy = min(policies, key=policies.get)
    worst_policy = max(policies, key=policies.get)

    print("\n--- RESULTS ---")
    for k, v in policies.items():
        print(f"{k}: {v:.2f}")

    print("\nBest Policy:", best_policy)
    print("Worst Policy:", worst_policy)

    
    # 1. MAIN COMPARISON PLOT
   
    labels = list(policies.keys())
    values = list(policies.values())

    colors = [
        "green" if k == best_policy else
        "red" if k == worst_policy else
        "blue"
        for k in labels
    ]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(labels, values, color=colors)

    plt.title("Reliability Policy Cost Comparison")
    plt.ylabel("Average Cost")
    plt.xticks(rotation=20)

    # value labels
    for bar in bars:
        y = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            y,
            f"{y:.1f}",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.savefig("policy_comparison.png")

  
    # 2. DIFFERENCE FROM BEST
    
    best_value = policies[best_policy]
    diff = {k: v - best_value for k, v in policies.items()}

    plt.figure(figsize=(8, 5))
    diff_values = list(diff.values())

    plt.bar(labels, diff_values, color=colors)
    plt.axhline(0, color="black", linewidth=1)

    plt.title("Difference from Best Policy")
    plt.ylabel("Extra Cost Compared to Best")
    plt.xticks(rotation=20)

    plt.tight_layout()
    plt.savefig("policy_difference.png")