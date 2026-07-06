"""
==============================================================================
Lab 20: Statistical Output Analysis and Precision Estimation
         (Drive-Thru Pharmacy Simulation)
==============================================================================
Question:
    This lab evaluates customer flow at an automated drive-thru pharmacy kiosk
    operating as a terminating simulation until 50 cars are served. Students are
    given average customer waiting times across five independent replication runs
    (3.2, 4.3, 5.1, 4.2, and 4.6 minutes) and must apply output data analysis:
      - Calculate the overall point estimate (sample mean).
      - Compute the sample variance and standard error (stochastic variability).
      - Construct a 95% confidence interval using the Student's t-distribution.
      - Determine the total number of replications required to achieve a desired
        half-width precision of no more than 0.5 minutes.
==============================================================================

Key formulas:
    sample mean        Xbar = (sum of values) / n
    sample variance    s^2  = sum((x - Xbar)^2) / (n - 1)
    standard error     SE   = s / sqrt(n)
    half-width (CI)    h    = t * SE
    required reps      n*   = ( t * s / desired_half_width )^2

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1: "Enter replication waiting times (Enter for lab data ...): "
              -> press Enter  (uses the lab data 3.2 4.3 5.1 4.2 4.6)
    Prompt 2: "Enter desired half-width precision (e.g. 0.5): "  -> 0.5
    WHY: Pressing Enter loads the exact five replication values from the
    Question, so the mean, variance, CI and required-replication results match
    the intended scenario; 0.5 is the precision target stated in the Question.
------------------------------------------------------------------------------
"""

import math
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Get the replication data from the user --------------------
    # User can press Enter to use the lab's given data: 3.2 4.3 5.1 4.2 4.6
    raw = input("Enter replication waiting times (Enter for lab data 3.2 4.3 5.1 4.2 4.6): ")
    if raw.strip() == "":
        data = [3.2, 4.3, 5.1, 4.2, 4.6]
    else:
        data = [float(x) for x in raw.split()]

    desired_half_width = float(input("Enter desired half-width precision (e.g. 0.5): "))

    n = len(data)

    # ---- Step 2: Point estimate (sample mean) ------------------------------
    mean = sum(data) / n

    # ---- Step 3: Sample variance and standard error ------------------------
    # Variance uses (n - 1) in the denominator -- the unbiased sample estimator.
    variance = sum((x - mean) ** 2 for x in data) / (n - 1)
    std_dev = math.sqrt(variance)
    # Standard error measures how precise our mean estimate is.
    standard_error = std_dev / math.sqrt(n)

    # ---- Step 4: 95% confidence interval using Student's t -----------------
    # We look up the t critical value for 95% confidence at df = n - 1.
    t_table = {1: 12.71, 2: 4.30, 3: 3.18, 4: 2.78, 5: 2.57, 6: 2.45,
               7: 2.36, 8: 2.31, 9: 2.26, 10: 2.23, 15: 2.13, 20: 2.09,
               30: 2.04, 60: 2.00, 120: 1.98}
    df = n - 1
    t_value = t_table.get(df, 1.96)   # default 1.96 for large samples

    # Half-width = t * SE; the CI spans mean +/- half_width.
    half_width = t_value * standard_error
    lower = mean - half_width
    upper = mean + half_width

    # ---- Step 5: Required number of replications for desired precision -----
    # Rearranging h = t * s / sqrt(n*) gives n* = (t * s / h)^2.
    # We round UP because we cannot run a fraction of a replication.
    required_n = (t_value * std_dev / desired_half_width) ** 2
    required_n_rounded = math.ceil(required_n)

    # ---- Step 6: Report all the results ------------------------------------
    print("\n--------- Output Analysis Results ---------")
    print(f"Number of replications (n) : {n}")
    print(f"Sample mean (point est.)   : {mean:.4f} minutes")
    print(f"Sample variance (s^2)      : {variance:.4f}")
    print(f"Sample std deviation (s)   : {std_dev:.4f}")
    print(f"Standard error (SE)        : {standard_error:.4f}")
    print(f"t-value (df={df}, 95%)       : {t_value}")
    print(f"Half-width of 95% CI       : {half_width:.4f}")
    print(f"95% Confidence Interval    : ({lower:.4f}, {upper:.4f})")
    print(f"\nDesired half-width         : {desired_half_width}")
    print(f"Required replications      : {required_n:.2f}  -> round up to "
          f"{required_n_rounded}")

    # ---- Step 7: Graphical representation ----------------------------------
    # Plot each replication's waiting time as a marker, the sample mean as a
    # horizontal line, and the 95% CI as a shaded band.
    replications = list(range(1, n + 1))
    plt.figure()
    plt.plot(replications, data, "o", color="blue", label="Replication wait time")
    plt.axhline(mean, color="red", linestyle="--", label=f"Sample mean = {mean:.2f}")
    plt.axhspan(lower, upper, color="green", alpha=0.2,
                label=f"95% CI ({lower:.2f}, {upper:.2f})")
    plt.title("Replication Waiting Times with Mean and 95% CI")
    plt.xlabel("Replication index")
    plt.ylabel("Average waiting time (minutes)")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
