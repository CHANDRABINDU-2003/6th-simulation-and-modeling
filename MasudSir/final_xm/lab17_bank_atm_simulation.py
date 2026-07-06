"""
==============================================================================
Lab 17: Bank ATM System Simulation
==============================================================================
Question:
    Model an ATM vestibule where customers arrive at random, use one of several
    machines, and leave. Calculate the maximum queue lengths.
==============================================================================

This is a multi-server queue. Several ATMs share one waiting line (FIFO). A
customer arrives, takes a free ATM if one exists, otherwise waits. We track the
queue length over time and report the MAXIMUM queue length reached, which tells
the bank how much waiting space it might need.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1 -> "Enter mean time between arrivals (e.g. 2): "          type:  2
    Prompt 2 -> "Enter mean ATM usage time (e.g. 5): "                 type:  5
    Prompt 3 -> "Enter number of ATMs (e.g. 3): "                      type:  3
    Prompt 4 -> "Enter number of customers to simulate (e.g. 200): "   type: 200
WHY: total service capacity (3 ATMs / 5 = 0.6 served per unit time) exceeds the
arrival rate (1/2 = 0.5 per unit time), so the system is stable and the queue
length stays bounded -- you get a real, finite MAXIMUM queue length instead of
an ever-growing line; 200 customers is long enough to see the peak form.
------------------------------------------------------------------------------
"""

import random
import math
import matplotlib.pyplot as plt


def exponential(mean):
    # Inverse-transform exponential for arrivals and ATM usage times.
    return -mean * math.log(1.0 - random.random())


def main():
    # ---- Step 1: Read the parameters ---------------------------------------
    mean_interarrival = float(input("Enter mean time between arrivals (e.g. 2): "))
    mean_service = float(input("Enter mean ATM usage time (e.g. 5): "))
    num_atms = int(input("Enter number of ATMs (e.g. 3): "))
    max_customers = int(input("Enter number of customers to simulate (e.g. 200): "))

    # ---- Step 2: Set up state ----------------------------------------------
    clock = 0.0
    num_in_queue = 0                 # customers currently waiting (not on an ATM)
    busy_atms = 0                    # how many ATMs are currently in use
    INF = float("inf")

    # We keep a separate scheduled finish time for each ATM. INF = that ATM idle.
    atm_finish_times = [INF] * num_atms

    queue = []                       # arrival times of waiting customers
    time_next_arrival = exponential(mean_interarrival)

    # Statistics we care about.
    max_queue_length = 0             # the headline result
    total_delay = 0.0
    num_delayed = 0
    served = 0

    # We record (clock, num_in_queue) at every event to plot the queue over time.
    trace_times = []
    trace_queue = []

    # ---- Step 3: Main event loop -------------------------------------------
    while served < max_customers:
        # The next event is either the next arrival or the soonest ATM finish.
        soonest_atm = min(atm_finish_times)

        if time_next_arrival <= soonest_atm:
            # ----- ARRIVAL EVENT -----
            clock = time_next_arrival
            time_next_arrival = clock + exponential(mean_interarrival)

            if busy_atms < num_atms:
                # A machine is free: start service immediately, no waiting.
                busy_atms += 1
                num_delayed += 1
                # Find the first idle ATM and assign this customer's finish time.
                idle_index = atm_finish_times.index(INF)
                atm_finish_times[idle_index] = clock + exponential(mean_service)
            else:
                # All ATMs busy: the customer joins the waiting line.
                num_in_queue += 1
                queue.append(clock)
                # Update the running maximum queue length.
                if num_in_queue > max_queue_length:
                    max_queue_length = num_in_queue
        else:
            # ----- ATM-FINISH (DEPARTURE) EVENT -----
            atm_index = atm_finish_times.index(soonest_atm)
            clock = soonest_atm
            served += 1

            if num_in_queue > 0:
                # Pull the next waiting customer onto this freed ATM.
                num_in_queue -= 1
                arrival_time = queue.pop(0)
                total_delay += clock - arrival_time
                num_delayed += 1
                atm_finish_times[atm_index] = clock + exponential(mean_service)
            else:
                # No one waiting: this ATM goes idle.
                busy_atms -= 1
                atm_finish_times[atm_index] = INF

        # Record the queue length at this event for the visual trace.
        trace_times.append(clock)
        trace_queue.append(num_in_queue)

    # ---- Step 4: Report results --------------------------------------------
    average_delay = total_delay / num_delayed
    print("\n--------- ATM Vestibule Simulation Results ---------")
    print(f"Customers served        : {served}")
    print(f"Maximum queue length    : {max_queue_length}")
    print(f"Average waiting time    : {average_delay:.4f}")
    print(f"Simulation end time     : {clock:.4f}")

    # ---- Step 5: Graphical view of queue length over time ------------------
    # A step plot suits a queue: the length holds steady between events and
    # jumps at each event. The dashed line marks the headline MAXIMUM.
    plt.figure()
    plt.plot(trace_times, trace_queue, drawstyle="steps-post",
             color="tab:blue", label="Number in queue")
    plt.axhline(max_queue_length, color="tab:red", linestyle="--",
                label=f"Maximum queue length = {max_queue_length}")
    plt.title("Lab 17: ATM Vestibule -- Queue Length Over Time")
    plt.xlabel("Simulation clock")
    plt.ylabel("Number in queue")
    plt.legend()
    plt.grid(True, linestyle=":", alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
