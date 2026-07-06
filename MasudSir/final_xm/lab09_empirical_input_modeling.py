"""
==============================================================================
Lab 09: Empirical Input Modeling
==============================================================================
Question:
    Given a raw dataset of customer arrival times at a call center, fit the data
    to theoretical distributions (e.g., Normal, Weibull, or Lognormal) using
    Maximum Likelihood Estimation (MLE). Validate the fit with Q-Q plots.
==============================================================================

Input modeling means: we have real-world data and we want to find which known
distribution best describes it. We use Maximum Likelihood Estimation (MLE) to
estimate each distribution's parameters, then judge the fit with Q-Q plots.
A Q-Q plot is "good" when the points lie close to a straight diagonal line.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    1) "Enter arrival times separated by spaces (or press Enter for demo data): "
       OPTION A (recommended): just press Enter (type nothing).
           -> The program generates 200 demo arrival times that are positive
              and right-skewed, exactly the kind of call-center data the
              Question describes. With 200 points the MLE fits and Q-Q plots
              are stable and meaningful.
       OPTION B: paste your own positive, right-skewed values, e.g.
           3.2 5.1 1.8 7.4 2.6 9.0 4.3 6.7 1.1 8.5 3.9 5.5 2.2 7.0 4.8
           -> Use many (20+) positive numbers so the fits are well-defined.

    WHY: Pressing Enter guarantees a clean, sufficiently large, right-skewed
    dataset so Normal/Weibull/Lognormal MLE fits converge and the Q-Q plots
    are interpretable; pasting too few or negative values can break the fits.
------------------------------------------------------------------------------
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def main():
    # ---- Step 1: Get the raw data from the user ----------------------------
    # The user can paste their own numbers, or press Enter to use sample data.
    raw = input("Enter arrival times separated by spaces (or press Enter for demo data): ")

    if raw.strip() == "":
        # If no data is given, generate some demo arrival times so the program
        # still runs. These look like typical positive, right-skewed times.
        data = np.random.exponential(scale=5.0, size=200)
        print("No data entered, using 200 randomly generated demo values.")
    else:
        data = np.array([float(x) for x in raw.split()])

    # ---- Step 2: Fit each candidate distribution using MLE -----------------
    # scipy's .fit() method performs Maximum Likelihood Estimation for us and
    # returns the best-fitting parameters for each distribution.
    norm_params = stats.norm.fit(data)        # (mean, std)
    weibull_params = stats.weibull_min.fit(data)   # (shape, loc, scale)
    lognorm_params = stats.lognorm.fit(data)  # (shape, loc, scale)

    print("\n--- MLE fitted parameters ---")
    print(f"Normal     : mean={norm_params[0]:.4f}, std={norm_params[1]:.4f}")
    print(f"Weibull    : shape={weibull_params[0]:.4f}, "
          f"loc={weibull_params[1]:.4f}, scale={weibull_params[2]:.4f}")
    print(f"Lognormal  : shape={lognorm_params[0]:.4f}, "
          f"loc={lognorm_params[1]:.4f}, scale={lognorm_params[2]:.4f}")

    # ---- Step 3: Measure goodness of fit with a quick KS test --------------
    # The Kolmogorov-Smirnov test gives a distance: smaller = better fit.
    # This helps us numerically pick which distribution describes the data best.
    print("\n--- Goodness of fit (KS statistic, smaller is better) ---")
    ks_norm = stats.kstest(data, "norm", args=norm_params).statistic
    ks_weib = stats.kstest(data, "weibull_min", args=weibull_params).statistic
    ks_logn = stats.kstest(data, "lognorm", args=lognorm_params).statistic
    print(f"Normal     : {ks_norm:.4f}")
    print(f"Weibull    : {ks_weib:.4f}")
    print(f"Lognormal  : {ks_logn:.4f}")

    # ---- Step 4: Validate each fit with a Q-Q plot -------------------------
    # We make three side-by-side Q-Q plots. If the points hug the red line,
    # that distribution is a good model for the data.
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    # Q-Q plot for the Normal fit.
    stats.probplot(data, dist="norm", sparams=norm_params, plot=axes[0])
    axes[0].set_title("Q-Q Plot: Normal")

    # Q-Q plot for the Weibull fit.
    stats.probplot(data, dist="weibull_min", sparams=weibull_params, plot=axes[1])
    axes[1].set_title("Q-Q Plot: Weibull")

    # Q-Q plot for the Lognormal fit.
    stats.probplot(data, dist="lognorm", sparams=lognorm_params, plot=axes[2])
    axes[2].set_title("Q-Q Plot: Lognormal")

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
