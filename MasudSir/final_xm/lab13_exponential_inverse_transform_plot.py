"""
==============================================================================
Lab 13: Exponential Random Numbers via Inverse Transform (with Plot)
==============================================================================
Question:
    Generate 5,000 exponentially distributed random numbers using the Inverse
    Transform technique. Plot a histogram of the resulting numbers and overlay
    the theoretical exponential probability density function.
==============================================================================

We reuse the Inverse Transform idea:
    X = -(1 / lambda) * ln(1 - U)
Then we compare our generated data (histogram) against the true exponential
density curve f(x) = lambda * e^(-lambda * x). A good generator makes the bars
follow the curve closely.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    1) "Enter the rate parameter lambda (e.g. 1.0): "        ->  1.0
    2) "Enter how many numbers to generate (e.g. 5000): "    ->  5000

    WHY: lambda = 1.0 gives a standard exponential (mean = 1/lambda = 1.0) that
    is easy to read on the plot, and 5000 samples (as the Question asks) is a
    large enough count for the histogram bars to closely track the theoretical
    PDF and for the sample mean to land near the expected 1.0.
------------------------------------------------------------------------------
"""

import math
import random
import numpy as np
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Read the parameters ---------------------------------------
    lam = float(input("Enter the rate parameter lambda (e.g. 1.0): "))
    count = int(input("Enter how many numbers to generate (e.g. 5000): "))

    # ---- Step 2: Generate the random numbers via inverse transform ---------
    data = []
    for _ in range(count):
        # Draw a uniform number, then map it through the inverse CDF.
        u = random.random()
        x = -(1.0 / lam) * math.log(1.0 - u)
        data.append(x)

    # ---- Step 3: Plot the histogram of the generated numbers ---------------
    # density=True scales the bars so the histogram area is 1, allowing a fair
    # comparison against the theoretical density curve.
    plt.figure()
    plt.hist(data, bins=50, density=True, color="lightblue",
             edgecolor="black", label="Generated data")

    # ---- Step 4: Overlay the theoretical exponential PDF -------------------
    # Build smooth x-values and apply f(x) = lambda * e^(-lambda*x).
    x_values = np.linspace(0, max(data), 500)
    pdf = lam * np.exp(-lam * x_values)
    plt.plot(x_values, pdf, color="red", linewidth=2, label="Theoretical PDF")

    plt.title(f"Inverse Transform Exponential (lambda = {lam}, n = {count})")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()

    # ---- Step 5: Print a quick numeric comparison --------------------------
    print(f"\nSample mean    = {np.mean(data):.4f}")
    print(f"Expected mean  = {1.0 / lam:.4f} (1/lambda)")

    plt.show()


if __name__ == "__main__":
    main()
