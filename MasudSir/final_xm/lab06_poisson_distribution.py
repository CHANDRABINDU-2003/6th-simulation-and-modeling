"""
==============================================================================
Lab 06: Poisson Distribution
==============================================================================
Question:
    A customer care center receives 5 calls per hour. Compute the probability of
    attending zero calls, one call, two calls, ....., ten calls per hour.
    Simulate the probability mass function with respect to the number of
    received calls. Show the probability mass function graphs considering 10 and
    15 calls per hour.
==============================================================================

The Poisson distribution describes the number of events (calls) happening in a
fixed interval (one hour) when the events occur at a known average rate.
    P(X = k) = (lambda^k * e^(-lambda)) / k!
where lambda is the average number of events per interval.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1: "Enter average calls per hour (lambda, e.g. 5): "          -> 5
    Prompt 2: "Enter the maximum number of calls to compute (e.g. 10): " -> 10
    WHY: lambda = 5 matches the Question's call center (5 calls/hour), and
    computing up to 10 calls covers P(X=0)...P(X=10) as asked, giving a full,
    meaningful PMF table and bar chart around the peak.
------------------------------------------------------------------------------
"""

import math
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: the Poisson probability mass function for exactly k events.
# ---------------------------------------------------------------------------
def poisson_pmf(k, lam):
    # lam^k * e^(-lam) divided by k factorial (k!).
    return (lam ** k) * math.exp(-lam) / math.factorial(k)


def main():
    # ---- Step 1: Ask the user for the average call rate --------------------
    lam = float(input("Enter average calls per hour (lambda, e.g. 5): "))
    max_calls = int(input("Enter the maximum number of calls to compute (e.g. 10): "))

    # ---- Step 2: Build the PMF for 0, 1, 2, ..., max_calls -----------------
    k_values = list(range(0, max_calls + 1))     # the x-axis: number of calls
    probabilities = [poisson_pmf(k, lam) for k in k_values]  # matching y-values

    # ---- Step 3: Print each probability so the numbers are visible ---------
    print(f"\nPoisson probabilities for lambda = {lam}:")
    for k, prob in zip(k_values, probabilities):
        print(f"P(X = {k}) = {prob:.5f}")

    # ---- Step 4: Plot the PMF the user asked for ---------------------------
    plt.figure()
    plt.bar(k_values, probabilities, color="skyblue", edgecolor="black")
    plt.title(f"Poisson PMF (lambda = {lam})")
    plt.xlabel("Number of calls per hour")
    plt.ylabel("Probability")

    # ---- Step 5: As requested, also compare PMFs for 10 and 15 calls/hr ----
    # We draw both curves on one figure so their shapes can be compared.
    plt.figure()
    for rate in [10, 15]:
        ks = list(range(0, rate * 2 + 1))            # show a sensible range
        probs = [poisson_pmf(k, rate) for k in ks]
        plt.plot(ks, probs, marker="o", label=f"lambda = {rate}")
    plt.title("Poisson PMF for 10 and 15 calls per hour")
    plt.xlabel("Number of calls per hour")
    plt.ylabel("Probability")
    plt.legend()

    # Show both windows at once.
    plt.show()


if __name__ == "__main__":
    main()
