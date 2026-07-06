"""
==============================================================================
Lab 04: Bernoulli Data Distribution
==============================================================================
Question:
    A Manufacturing and Reliability Lab is testing a newly produced batch of
    microchips. Each chip undergoes a strict operational test and either works
    perfectly (Success = 1) or fails (Failure = 0). Historical data shows that
    the probability of any given chip passing this test is p = 0.85.

    This problem models a Bernoulli distribution using a Quality-Control Test:
      - State the values of X and what they represent.
      - Calculate the probability of a defect, P(X = 0).
      - Find the mean: the expected value E[X].
      - Find the spread: the variance Var(X).
==============================================================================

A Bernoulli random variable X has only two outcomes:
    X = 1  ->  Success (the chip passes the test)
    X = 0  ->  Failure (the chip fails / is defective)

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter probability of success p (e.g. 0.85): : 0.85

    WHY: p must be a valid probability between 0 and 1; using 0.85 (the value
    from the problem statement) gives q = 0.15, mean = 0.85, and variance =
    0.1275, reproducing the chip-testing scenario described in the Question.
==============================================================================
"""

import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Get the success probability p from the user ---------------
    p = float(input("Enter probability of success p (e.g. 0.85): "))

    # ---- Step 2: Work out the failure probability q ------------------------
    # In a Bernoulli trial the two outcomes must add up to 1,
    # so the chance of failure is simply 1 minus the chance of success.
    q = 1 - p

    # ---- Step 3: Probability of a defect, P(X = 0) -------------------------
    # A defect is the "failure" outcome, which is exactly q.
    prob_defect = q

    # ---- Step 4: The mean (expected value) E[X] ----------------------------
    # For a Bernoulli variable the expected value is just p, because
    # E[X] = 1*p + 0*q = p. It tells us the long-run average outcome.
    mean = p

    # ---- Step 5: The variance Var(X) ---------------------------------------
    # Variance measures how spread out the outcomes are.
    # For a Bernoulli variable the formula is p * q.
    variance = p * q

    # ---- Step 6: Show all the results --------------------------------------
    print("\n--------- Bernoulli Distribution Results ---------")
    print("X = 1 represents SUCCESS (chip passes the test)")
    print("X = 0 represents FAILURE (chip is defective)")
    print(f"Probability of success p          : {p}")
    print(f"Probability of failure q          : {q}")
    print(f"Probability of a defect P(X=0)    : {prob_defect}")
    print(f"Mean / Expected value E[X]        : {mean}")
    print(f"Variance Var(X)                   : {variance}")

    # ---- Step 7: Graphical representation of the output --------------------
    # Bar chart of the Bernoulli PMF: P(X=0) = q and P(X=1) = p.
    plt.figure("Bernoulli PMF")
    outcomes = ["X = 0\n(Failure)", "X = 1\n(Success)"]
    probabilities = [q, p]
    bars = plt.bar(outcomes, probabilities, color=["tab:red", "tab:green"])
    plt.title(f"Bernoulli PMF  (Mean E[X] = {mean:.4f},  Var(X) = {variance:.4f})")
    plt.xlabel("Outcome")
    plt.ylabel("Probability")
    plt.ylim(0, 1)
    # Annotate each bar with its probability value.
    for bar, prob in zip(bars, probabilities):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{prob:.4f}", ha="center", va="bottom")

    plt.show()


if __name__ == "__main__":
    main()
