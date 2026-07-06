"""
==============================================================================
Lab 08: Exponential Distribution
==============================================================================
Question:
    There were few waves in the COVID-19 pandemic. Let a wave occur every 100
    days in Bangladesh, on average. After a wave occurs, find the probability
    using the Exponential distribution that it will take more than 120 days for
    the next wave to occur. Simulate several Exponential distributions using rate
    parameters 0.5, 1.0, 2.0, and 4.0.
==============================================================================

The Exponential distribution models the waiting time between events that happen
at a constant average rate. Its rate parameter is lambda = 1 / mean.
    P(X > x) = e^(-lambda * x)        (the "survival" probability)

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    1) "Enter average days between waves (e.g. 100): "   ->  100
    2) "Enter the waiting time to test, in days (e.g. 120): "   ->  120

    WHY: These match the Question exactly (a wave every 100 days on average,
    testing P(wait > 120 days)). mean=100 gives lambda = 1/100 = 0.01, so the
    survival probability P(X > 120) = e^(-0.01*120) ~ 0.301 is a meaningful,
    non-trivial value, and the PDF curve spans a sensible 0-400 day range.
------------------------------------------------------------------------------
"""

import math
import numpy as np
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Read the average wave gap and the target waiting time -----
    mean_days = float(input("Enter average days between waves (e.g. 100): "))
    target_days = float(input("Enter the waiting time to test, in days (e.g. 120): "))

    # ---- Step 2: Compute the rate and the "more than" probability ----------
    # The rate lambda is the reciprocal of the mean.
    lam = 1.0 / mean_days
    # Probability the next wave takes MORE than target_days = e^(-lambda*x).
    prob_more_than = math.exp(-lam * target_days)

    print(f"\nRate parameter lambda = {lam:.5f}")
    print(f"P(wait > {target_days} days) = {prob_more_than:.5f}")

    # ---- Step 3: Plot the survival/PDF curve for the wave scenario ---------
    # The exponential probability density is f(x) = lambda * e^(-lambda*x).
    x = np.linspace(0, mean_days * 4, 500)
    pdf = lam * np.exp(-lam * x)

    plt.figure()
    plt.plot(x, pdf, color="purple")
    plt.title(f"Exponential PDF for waves (mean = {mean_days} days)")
    plt.xlabel("Days until next wave")
    plt.ylabel("Density")

    # ---- Step 4: Simulate exponentials with several rate parameters --------
    # We overlay the PDFs for the requested rates so their shapes compare.
    rates = [0.5, 1.0, 2.0, 4.0]
    plt.figure()
    for rate in rates:
        xs = np.linspace(0, 8, 500)
        ys = rate * np.exp(-rate * xs)       # PDF for this rate
        plt.plot(xs, ys, label=f"lambda = {rate}")
    plt.title("Exponential Distributions for Different Rates")
    plt.xlabel("x")
    plt.ylabel("Density")
    plt.legend()

    # ---- Step 5: Also generate random samples to confirm the theory --------
    # We draw 1000 samples for each rate and report the sample mean, which
    # should be close to 1/lambda.
    print("\nRandom-sample check (mean should be near 1/lambda):")
    for rate in rates:
        # numpy uses "scale" = 1/lambda for the exponential generator.
        samples = np.random.exponential(scale=1.0 / rate, size=1000)
        print(f"lambda = {rate}: sample mean = {np.mean(samples):.4f}, "
              f"expected = {1.0 / rate:.4f}")

    plt.show()


if __name__ == "__main__":
    main()
