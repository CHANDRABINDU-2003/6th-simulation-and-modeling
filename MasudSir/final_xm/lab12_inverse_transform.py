"""
==============================================================================
Lab 12: Random Variates using the Inverse Transform Function
==============================================================================
Question:
    There are several general approaches to generating univariate Random
    Variables from the distribution function. Write a program which generates
    the desired number of random variates using the inverse transform function.
==============================================================================

The Inverse Transform method works like this:
    1. Generate U, a uniform random number between 0 and 1.
    2. Plug U into the inverse of the distribution's CDF, F^-1(U).
    3. The result is a random variate following that distribution.

Here we demonstrate it for the Exponential distribution, whose inverse CDF is:
    X = -(1 / lambda) * ln(1 - U)

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter the rate parameter lambda (e.g. 0.5):              -> 0.5
    Enter the number of random variates to generate:        -> 1000

WHY: lambda = 0.5 matches the example hint and gives an expected mean of
     1/lambda = 2.0. Generating 1000 variates makes the sample mean converge
     to 2.0 and lets the histogram clearly trace the theoretical exponential
     PDF curve.
------------------------------------------------------------------------------
"""

import random
import math
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: the inverse CDF (quantile function) of the exponential distribution.
# ---------------------------------------------------------------------------
def inverse_exponential(u, lam):
    # F^-1(u) = -(1/lambda) * ln(1 - u). We feed it a uniform u in [0,1).
    return -(1.0 / lam) * math.log(1.0 - u)


def main():
    # ---- Step 1: Get the rate parameter and how many variates we want ------
    lam = float(input("Enter the rate parameter lambda (e.g. 0.5): "))
    count = int(input("Enter the number of random variates to generate: "))

    print(f"\nGenerating {count} exponential variates (lambda = {lam}):\n")
    print("  n |     U (uniform)    |   X (variate)")
    print("----+--------------------+----------------")

    variates = []           # we collect them here in case they are needed later

    # ---- Step 2: Generate each variate one at a time -----------------------
    for n in range(1, count + 1):
        # 2a. Draw a uniform random number between 0 and 1.
        u = random.random()

        # 2b. Pass it through the inverse CDF to get our distributed variate.
        x = inverse_exponential(u, lam)

        variates.append(x)
        print(f"{n:3} | {u:.6f}          | {x:.6f}")

    # ---- Step 3: Quick sanity check ----------------------------------------
    # The average of exponential variates should be close to 1/lambda.
    average = sum(variates) / len(variates)
    print(f"\nSample mean    = {average:.4f}")
    print(f"Expected mean  = {1.0 / lam:.4f} (which is 1/lambda)")

    # ---- Step 4: Graphical representation of the output --------------------
    # Histogram of the generated variates as a density, overlaid with the
    # theoretical exponential PDF f(x) = lambda * e^(-lambda * x) in red.
    plt.figure(figsize=(10, 6))
    plt.hist(variates, bins=30, density=True, color="steelblue",
             edgecolor="black", label="Generated variates (density)")

    # Smooth x range from 0 up to the largest variate for the PDF curve.
    x_curve = np.linspace(0, max(variates), 200)
    pdf_curve = lam * np.exp(-lam * x_curve)
    plt.plot(x_curve, pdf_curve, color="red", linewidth=2,
             label="Theoretical exponential PDF")

    plt.title("Inverse Transform: Generated Variates vs Exponential PDF")
    plt.xlabel("x (variate value)")
    plt.ylabel("Density")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
