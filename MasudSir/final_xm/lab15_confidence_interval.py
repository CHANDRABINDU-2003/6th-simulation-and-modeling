"""
==============================================================================
Lab 15: Confidence Interval Estimation
==============================================================================
Question:
    Calculate a 95% confidence interval for the mean system response (e.g.,
    average waiting time) by running multiple independent replications of a
    simulation model.
==============================================================================

Idea:
    A single simulation run gives only ONE noisy estimate. To trust the result
    we run the simulation many independent times (replications), collect the
    average waiting time from each, and then build a 95% confidence interval
    around the grand mean. The interval tells us the range in which the true
    mean waiting time most likely lies.

    Confidence interval formula:
        mean  ±  t * (s / sqrt(n))
    where s = sample standard deviation, n = number of replications, and t is
    the Student-t critical value for 95% confidence.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1 -> "Enter mean inter-arrival time (e.g. 4): "        type:  4
    Prompt 2 -> "Enter mean service time (e.g. 3): "              type:  3
    Prompt 3 -> "Enter customers per replication (e.g. 1000): "   type: 1000
    Prompt 4 -> "Enter number of replications (e.g. 10): "        type: 10
WHY: service mean (3) < inter-arrival mean (4) keeps the queue stable so each
replication's average wait is finite and meaningful; 1000 customers makes each
run's estimate fairly steady, and 10 replications gives a usable Student-t
confidence interval (df = 9 sits exactly in the t-table).
------------------------------------------------------------------------------
"""

import random
import math
import matplotlib.pyplot as plt


def exponential(mean):
    # Inverse-transform exponential generator for arrivals and service.
    return -mean * math.log(1.0 - random.random())


# ---------------------------------------------------------------------------
# Run ONE replication of a single-server queue and return its average wait.
# ---------------------------------------------------------------------------
def run_one_replication(mean_interarrival, mean_service, num_customers):
    clock = 0.0
    server_busy = False
    num_in_queue = 0
    queue = []
    total_delay = 0.0
    num_delayed = 0
    served = 0
    INF = float("inf")

    time_next_arrival = exponential(mean_interarrival)
    time_next_departure = INF

    # Process events until enough customers have completed service.
    while served < num_customers:
        if time_next_arrival <= time_next_departure:
            # Arrival event.
            clock = time_next_arrival
            time_next_arrival = clock + exponential(mean_interarrival)
            if not server_busy:
                server_busy = True
                num_delayed += 1            # served immediately, 0 wait
                time_next_departure = clock + exponential(mean_service)
            else:
                num_in_queue += 1
                queue.append(clock)
        else:
            # Departure event.
            clock = time_next_departure
            served += 1
            if num_in_queue == 0:
                server_busy = False
                time_next_departure = INF
            else:
                num_in_queue -= 1
                arrival_time = queue.pop(0)
                total_delay += clock - arrival_time   # this customer's wait
                num_delayed += 1
                time_next_departure = clock + exponential(mean_service)

    # The replication's result is the average waiting time over its customers.
    return total_delay / num_delayed


def main():
    # ---- Step 1: Read the model + experiment parameters --------------------
    mean_interarrival = float(input("Enter mean inter-arrival time (e.g. 4): "))
    mean_service = float(input("Enter mean service time (e.g. 3): "))
    num_customers = int(input("Enter customers per replication (e.g. 1000): "))
    num_reps = int(input("Enter number of replications (e.g. 10): "))

    # ---- Step 2: Run the simulation many independent times -----------------
    results = []
    for r in range(1, num_reps + 1):
        avg_wait = run_one_replication(mean_interarrival, mean_service, num_customers)
        results.append(avg_wait)
        print(f"Replication {r:2}: average wait = {avg_wait:.4f}")

    # ---- Step 3: Compute the grand mean and sample standard deviation ------
    n = len(results)
    mean = sum(results) / n
    # Sample variance uses (n - 1) in the denominator (unbiased estimator).
    variance = sum((x - mean) ** 2 for x in results) / (n - 1)
    std_dev = math.sqrt(variance)

    # ---- Step 4: Build the 95% confidence interval -------------------------
    # We use a small lookup of Student-t critical values for 95% confidence so
    # the program needs no extra libraries. The key is degrees of freedom = n-1.
    t_table = {1: 12.71, 2: 4.30, 3: 3.18, 4: 2.78, 5: 2.57, 6: 2.45,
               7: 2.36, 8: 2.31, 9: 2.26, 10: 2.23, 15: 2.13, 20: 2.09,
               30: 2.04, 60: 2.00, 120: 1.98}
    df = n - 1
    # Pick the closest available t-value; default to 1.96 for large samples.
    if df in t_table:
        t_value = t_table[df]
    else:
        t_value = 1.96

    # The margin of error is t * standard error, where SE = s / sqrt(n).
    margin = t_value * (std_dev / math.sqrt(n))
    lower = mean - margin
    upper = mean + margin

    # ---- Step 5: Report the confidence interval ----------------------------
    print("\n--------- 95% Confidence Interval Result ---------")
    print(f"Number of replications : {n}")
    print(f"Mean average wait      : {mean:.4f}")
    print(f"Sample std deviation   : {std_dev:.4f}")
    print(f"Margin of error        : {margin:.4f}")
    print(f"95% CI                 : ({lower:.4f}, {upper:.4f})")

    # ---- Step 6: Graphical view of replications, mean and CI ---------------
    # Each replication is a point; the grand mean is a solid line; the 95%
    # confidence interval is a shaded band so we can see where it sits.
    rep_numbers = list(range(1, n + 1))
    plt.figure()
    plt.plot(rep_numbers, results, "o", color="tab:blue",
             label="Replication average wait")
    plt.axhline(mean, color="tab:red", linewidth=2,
                label=f"Grand mean = {mean:.3f}")
    plt.axhspan(lower, upper, color="tab:orange", alpha=0.25,
                label=f"95% CI ({lower:.3f}, {upper:.3f})")
    plt.title("Lab 15: Per-Replication Average Wait with 95% Confidence Interval")
    plt.xlabel("Replication number")
    plt.ylabel("Average waiting time")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
