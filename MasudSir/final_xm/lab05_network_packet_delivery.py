"""
==============================================================================
Lab 05: Network Packet Delivery (Binomial Distribution)
==============================================================================
Question:
    A network router transmits data packets in batches. Each individual packet
    has a success probability of p = 0.90 of reaching its destination. A single
    batch consists of n = 15 independent packets.

    Example Data: A simulation of 5 separate batches reveals the number of
    successfully delivered packets per batch: 14, 13, 15, 12, 14.

    Tasks:
      - Identify parameters: define n, p, and q (failure probability).
      - Exact Probability: probability that exactly 13 packets arrive safely.
      - Expected Value & Variance: theoretical mean mu and variance sigma^2.
      - Data Verification: average successful packets from the example data,
        compared to the theoretical mean.
==============================================================================

Because we count the number of successes out of n independent trials, this is
a Binomial distribution: X ~ Binomial(n, p).

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter number of packets per batch n (e.g. 15):            -> 15
    Enter success probability p (e.g. 0.90):                  -> 0.90
    Enter k for the exact probability P(X=k) (e.g. 13):       -> 13
    Enter example batch results separated by spaces:          -> 14 13 15 12 14

WHY: These values reproduce the exact scenario in the Question (n=15, p=0.90,
     k=13 with the 5 example batches), so the printed probabilities, mean,
     variance and empirical average all match the intended teaching example.
------------------------------------------------------------------------------
"""

import math
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: the binomial probability formula.
#   P(X = k) = C(n, k) * p^k * q^(n-k)
# where C(n, k) is "n choose k" (the number of ways to pick k successes).
# ---------------------------------------------------------------------------
def binomial_probability(n, k, p):
    q = 1 - p
    # math.comb gives the combination C(n, k) directly.
    combinations = math.comb(n, k)
    # Multiply by p^k (the k successes) and q^(n-k) (the remaining failures).
    return combinations * (p ** k) * (q ** (n - k))


def main():
    # ---- Step 1: Read the parameters from the user -------------------------
    n = int(input("Enter number of packets per batch n (e.g. 15): "))
    p = float(input("Enter success probability p (e.g. 0.90): "))
    k = int(input("Enter k for the exact probability P(X=k) (e.g. 13): "))

    # Read the example batch data. The user types the numbers separated by
    # spaces, e.g.:  14 13 15 12 14
    data_line = input("Enter example batch results separated by spaces: ")
    example_data = [int(x) for x in data_line.split()]

    # ---- Step 2: Identify the parameters -----------------------------------
    # q is the failure probability, the complement of success.
    q = 1 - p

    # ---- Step 3: Exact probability that exactly k packets arrive -----------
    prob_exact = binomial_probability(n, k, p)

    # ---- Step 4: Theoretical mean and variance -----------------------------
    # For a binomial distribution:
    #   mean (mu)        = n * p
    #   variance (sigma^2) = n * p * q
    #   std dev (sigma)  = square root of the variance
    mean = n * p
    variance = n * p * q
    std_dev = math.sqrt(variance)

    # ---- Step 5: Verify against the example data ---------------------------
    # The empirical average is just the sum of the data divided by its count.
    empirical_average = sum(example_data) / len(example_data)

    # ---- Step 6: Display everything ----------------------------------------
    print("\n--------- Network Packet Delivery Results ---------")
    print(f"Parameters: n = {n}, p = {p}, q = {q}")
    print(f"P(X = {k}) exactly               : {prob_exact:.4f}")
    print(f"Theoretical mean  (mu)           : {mean}")
    print(f"Theoretical variance (sigma^2)   : {variance}")
    print(f"Theoretical std dev (sigma)      : {std_dev:.4f}")
    print(f"Empirical average from data      : {empirical_average}")
    print(f"Difference (empirical - theory)  : {empirical_average - mean:.4f}")

    # ---- Step 7: Graphical representation of the output --------------------
    # Build the full Binomial PMF for every possible k from 0 up to n.
    ks = list(range(n + 1))
    pmf = [binomial_probability(n, kk, p) for kk in ks]

    # Colour each bar grey, but highlight the user's chosen k in orange.
    colors = ["orange" if kk == k else "steelblue" for kk in ks]

    plt.figure(figsize=(10, 6))
    plt.bar(ks, pmf, color=colors, edgecolor="black",
            label="Binomial PMF P(X=k)")

    # Vertical dashed lines for the theoretical mean and empirical average.
    plt.axvline(mean, color="red", linestyle="--",
                label=f"Theoretical mean n*p = {mean:.2f}")
    plt.axvline(empirical_average, color="green", linestyle="--",
                label=f"Empirical average = {empirical_average:.2f}")

    plt.title("Binomial PMF of Successful Packet Delivery")
    plt.xlabel("k (number of successfully delivered packets)")
    plt.ylabel("Probability P(X = k)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
