"""
==============================================================================
Lab 16: Steady-State Analysis
==============================================================================
Question:
    Analyze the warm-up period of a non-terminating simulation (like a
    continuous manufacturing line) and calculate the steady-state mean time.
==============================================================================

A non-terminating simulation never naturally "ends" (a factory line runs all
day). At the very start the system is empty and unrealistic, so the early data
is biased -- this is the WARM-UP period. We must throw it away (this is called
deletion) and only average the data AFTER the system settles into its long-run
"steady state".

Here we simulate a continuous single-server line, record the number in system
at many time points, then delete the warm-up portion before averaging.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    1) "Enter mean inter-arrival time (e.g. 1.0): "       ->  1.0
    2) "Enter mean service time (e.g. 0.8): "             ->  0.8
    3) "Enter total simulation time (e.g. 2000): "        ->  2000
    4) "Enter warm-up (deletion) time (e.g. 200): "       ->  200

    WHY: Service time 0.8 < inter-arrival 1.0 gives utilization rho = 0.8 < 1,
    so the queue is STABLE and reaches a true steady state (otherwise it grows
    without bound and no steady-state mean exists). Total time 2000 produces
    plenty of events for a smooth time-series plot, and a 200 warm-up cutoff
    discards the biased empty-start transient, leaving a clean steady-state
    average.
------------------------------------------------------------------------------
"""

import random
import math
import matplotlib.pyplot as plt


def exponential(mean):
    # Inverse-transform exponential for arrival gaps and service times.
    return -mean * math.log(1.0 - random.random())


def main():
    # ---- Step 1: Read the parameters ---------------------------------------
    mean_interarrival = float(input("Enter mean inter-arrival time (e.g. 1.0): "))
    mean_service = float(input("Enter mean service time (e.g. 0.8): "))
    total_time = float(input("Enter total simulation time (e.g. 2000): "))
    warmup_time = float(input("Enter warm-up (deletion) time (e.g. 200): "))

    # ---- Step 2: Set up the system state -----------------------------------
    clock = 0.0
    num_in_system = 0
    INF = float("inf")
    time_next_arrival = exponential(mean_interarrival)
    time_next_departure = INF

    # We sample the "number in system" over time to study the warm-up trend.
    sample_times = []
    sample_values = []

    # ---- Step 3: Run the continuous (non-terminating) simulation -----------
    while clock < total_time:
        # Whichever event is sooner happens next.
        next_event_time = min(time_next_arrival, time_next_departure)
        clock = next_event_time

        if time_next_arrival <= time_next_departure:
            # Arrival: one more unit enters the line.
            num_in_system += 1
            time_next_arrival = clock + exponential(mean_interarrival)
            # If the server was free, start serving this unit right away.
            if num_in_system == 1:
                time_next_departure = clock + exponential(mean_service)
        else:
            # Departure: a unit finishes and leaves.
            num_in_system -= 1
            if num_in_system > 0:
                time_next_departure = clock + exponential(mean_service)
            else:
                time_next_departure = INF

        # Record the state at this moment for later analysis.
        sample_times.append(clock)
        sample_values.append(num_in_system)

    # ---- Step 4: Delete the warm-up period and average the rest ------------
    # Average over ALL the data (biased, includes the empty-start period).
    overall_mean = sum(sample_values) / len(sample_values)

    # Average only AFTER the warm-up time (this is the steady-state estimate).
    steady_values = [v for t, v in zip(sample_times, sample_values)
                     if t >= warmup_time]
    steady_mean = sum(steady_values) / len(steady_values)

    # ---- Step 5: Report and plot -------------------------------------------
    print("\n--------- Steady-State Analysis ---------")
    print(f"Mean WITH warm-up (biased)     : {overall_mean:.4f}")
    print(f"Steady-state mean (warm-up cut): {steady_mean:.4f}")
    print(f"Data points kept after deletion: {len(steady_values)} of "
          f"{len(sample_values)}")

    # Plot the time series with a line marking where warm-up ends. The early
    # transient before the line is what we deliberately discard.
    plt.figure()
    plt.plot(sample_times, sample_values, color="steelblue", linewidth=0.7,
             label="Number in system")
    plt.axvline(warmup_time, color="red", linestyle="--",
                label="End of warm-up")
    plt.axhline(steady_mean, color="green", linestyle=":",
                label="Steady-state mean")
    plt.title("Warm-up Period and Steady State")
    plt.xlabel("Simulation time")
    plt.ylabel("Number in system")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
