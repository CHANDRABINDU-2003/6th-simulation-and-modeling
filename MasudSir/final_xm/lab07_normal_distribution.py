"""
==============================================================================
Lab 07: Normal Distribution
==============================================================================
Question:
    To show unimodal and multimodal density curves of normal distribution.
    To generate a random sample of size 200 which follows a normal distribution
    with mean 100 and standard deviation 20. The distribution of diastolic blood
    pressure for men is normally distributed with a mean of about 80 and a
    standard deviation of 20. A histogram of the distribution of blood pressures
    for all men displays a normal distribution with a bell shape.
==============================================================================

A normal distribution is the classic "bell curve". It is unimodal (one peak)
and symmetric around its mean. Mixing two normals with different means can give
a multimodal (more than one peak) curve.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1: "Enter mean (e.g. 100): "                -> 100
    Prompt 2: "Enter standard deviation (e.g. 20): "   -> 20
    Prompt 3: "Enter sample size (e.g. 200): "         -> 200
    WHY: mean=100, std=20, size=200 reproduce the Question's scenario exactly,
    so the histogram fills out a clear bell shape and the unimodal/multimodal
    density curves are well-formed with a meaningful sample summary.
------------------------------------------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Get the parameters from the user --------------------------
    mean = float(input("Enter mean (e.g. 100): "))
    std = float(input("Enter standard deviation (e.g. 20): "))
    sample_size = int(input("Enter sample size (e.g. 200): "))

    # ---- Step 2: Generate the random normal sample ------------------------
    # np.random.normal draws random numbers that follow the bell curve.
    sample = np.random.normal(mean, std, sample_size)

    # ---- Step 3: Show the sample as a histogram (the bell shape) ----------
    plt.figure()
    plt.hist(sample, bins=20, color="lightgreen", edgecolor="black", density=True)
    plt.title(f"Histogram of {sample_size} normal samples (mean={mean}, std={std})")
    plt.xlabel("Value")
    plt.ylabel("Density")

    # ---- Step 4: Draw a UNIMODAL density curve -----------------------------
    # We build a smooth set of x-values and apply the normal density formula:
    #   f(x) = 1/(std*sqrt(2*pi)) * e^(-(x-mean)^2 / (2*std^2))
    x = np.linspace(mean - 4 * std, mean + 4 * std, 500)
    unimodal = (1.0 / (std * np.sqrt(2 * np.pi))) * \
        np.exp(-((x - mean) ** 2) / (2 * std ** 2))

    plt.figure()
    plt.plot(x, unimodal, color="blue")
    plt.title("Unimodal Normal Density Curve (single peak)")
    plt.xlabel("Value")
    plt.ylabel("Density")

    # ---- Step 5: Draw a MULTIMODAL density curve ---------------------------
    # Adding two normal curves with different means produces two peaks.
    mean2 = mean + 4 * std           # a second peak well to the right
    x2 = np.linspace(mean - 4 * std, mean2 + 4 * std, 500)
    curve_a = (1.0 / (std * np.sqrt(2 * np.pi))) * \
        np.exp(-((x2 - mean) ** 2) / (2 * std ** 2))
    curve_b = (1.0 / (std * np.sqrt(2 * np.pi))) * \
        np.exp(-((x2 - mean2) ** 2) / (2 * std ** 2))
    multimodal = curve_a + curve_b   # the mixture has two humps

    plt.figure()
    plt.plot(x2, multimodal, color="red")
    plt.title("Multimodal Normal Density Curve (two peaks)")
    plt.xlabel("Value")
    plt.ylabel("Density")

    # ---- Step 6: Print a quick summary of the generated sample ------------
    print(f"\nSample mean    : {np.mean(sample):.4f}")
    print(f"Sample std dev : {np.std(sample):.4f}")

    plt.show()


if __name__ == "__main__":
    main()
