"""
==============================================================================
Lab 14: Debugging and Traceability (Verification)
==============================================================================
Question:
    Write a trace program to step through a discrete-event model and log system
    states, ensuring it adheres exactly to the logical model rules.
==============================================================================

Verification means: "did we build the model correctly?" The best way to check
is to TRACE it — print the full system state after every single event so we can
read the log line by line and confirm each rule was followed.

We trace a simple single-server queue. After each event we log:
    - the simulation clock
    - which event happened
    - whether the server is busy
    - how many customers are waiting
This lets us hand-verify the logic against the model rules.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1 -> "Enter mean inter-arrival time (e.g. 4): "   type:  4
    Prompt 2 -> "Enter mean service time (e.g. 3): "         type:  3
    Prompt 3 -> "Enter number of customers to trace (e.g. 5): "  type: 5
WHY: service mean (3) < inter-arrival mean (4) keeps the queue stable, so the
trace shows a healthy mix of ARRIVAL/DEPARTURE events without the queue blowing
up; 5 customers gives a short, readable trace you can verify by hand.
------------------------------------------------------------------------------
"""

import random
import math
import matplotlib.pyplot as plt


def exponential(mean):
    # Inverse-transform exponential, used for arrivals and service times.
    return -mean * math.log(1.0 - random.random())


def main():
    # ---- Step 1: Read the parameters ---------------------------------------
    mean_interarrival = float(input("Enter mean inter-arrival time (e.g. 4): "))
    mean_service = float(input("Enter mean service time (e.g. 3): "))
    max_customers = int(input("Enter number of customers to trace (e.g. 5): "))

    # ---- Step 2: Initialise the system state -------------------------------
    clock = 0.0
    server_busy = False
    num_in_queue = 0
    queue = []                          # arrival times of waiting customers
    served = 0
    INF = float("inf")

    # The two scheduled events.
    time_next_arrival = exponential(mean_interarrival)
    time_next_departure = INF

    # ---- Step 3: Helper to print one trace line ----------------------------
    # Keeping the logging in one place makes the trace tidy and consistent.
    # We also record (clock, num_in_queue) after each event so the trace can be
    # plotted visually at the end.
    trace_times = []
    trace_queue = []

    def log_state(event_name):
        busy_text = "BUSY" if server_busy else "IDLE"
        print(f"clock={clock:7.3f} | event={event_name:10} | "
              f"server={busy_text} | queue={num_in_queue}")
        # Record the state for the visual trace.
        trace_times.append(clock)
        trace_queue.append(num_in_queue)

    print("\n========== DISCRETE-EVENT TRACE ==========")
    log_state("START")

    # ---- Step 4: Step through events one at a time -------------------------
    while served < max_customers:
        # Pick whichever event comes first.
        if time_next_arrival <= time_next_departure:
            # ----- ARRIVAL EVENT -----
            clock = time_next_arrival
            # Schedule the following arrival immediately.
            time_next_arrival = clock + exponential(mean_interarrival)

            if not server_busy:
                # Rule: free server -> serve at once, no waiting.
                server_busy = True
                time_next_departure = clock + exponential(mean_service)
            else:
                # Rule: busy server -> join the back of the queue.
                num_in_queue += 1
                queue.append(clock)
            log_state("ARRIVAL")

        else:
            # ----- DEPARTURE EVENT -----
            clock = time_next_departure
            served += 1

            if num_in_queue == 0:
                # Rule: empty queue -> server becomes idle.
                server_busy = False
                time_next_departure = INF
            else:
                # Rule: queue not empty -> pull the front customer into service.
                num_in_queue -= 1
                queue.pop(0)
                time_next_departure = clock + exponential(mean_service)
            log_state("DEPARTURE")

    # ---- Step 5: Final state for verification ------------------------------
    print("==========================================")
    print(f"Trace complete. Customers served = {served}")

    # ---- Step 6: Graphical trace of the queue over time --------------------
    # A step plot is the right shape here: the queue length stays constant
    # between events and jumps at each logged event.
    plt.figure()
    plt.plot(trace_times, trace_queue, drawstyle="steps-post",
             marker="o", color="tab:blue", label="Number in queue")
    plt.title("Lab 14: Discrete-Event Trace -- Queue Length Over Time")
    plt.xlabel("Simulation clock")
    plt.ylabel("Number in queue")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
