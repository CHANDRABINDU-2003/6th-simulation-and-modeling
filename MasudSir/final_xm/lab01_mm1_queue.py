"""
==============================================================================
Lab 01: A Simple M/M/1 Queue Simulation
==============================================================================
Question:
    Write a program which performs a simple M/M/1 queue simulation. This program
    requires parameters for Mean Inter Arrival time of customers, Mean Service
    time as well as maximum number of customers. The simulation is started with a
    single-server queue with a FIFO queuing discipline. For M/M/1 queue, the
    customer inter-arrival time and the service time are both exponentially
    distributed. This simulation shows Average delay in queue, Average number in
    queue, Server utilization, and Time simulation ended.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter Mean Inter-Arrival time:  : 1.0
    Enter Mean Service time:        : 0.5
    Enter Maximum number of customers: : 1000

    WHY: keeping the Mean Service time (0.5) smaller than the Mean
    Inter-Arrival time (1.0) makes the traffic intensity rho = 0.5 < 1, so the
    queue stays stable and produces finite, meaningful averages. A large number
    of customers (1000) lets the time-averaged statistics settle near their
    true steady-state values.
==============================================================================
"""

import random
import math
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------------
# Helper: draw a random number from an exponential distribution.
# In an M/M/1 queue both the gaps between arrivals and the service times follow
# an exponential distribution. We generate one using the "inverse transform"
# trick: if U is uniform between 0 and 1, then -mean * ln(U) is exponential.
# ---------------------------------------------------------------------------
def exponential(mean):
    # random.random() gives a number in [0, 1). We avoid taking ln(0).
    u = random.random()
    return -mean * math.log(1.0 - u)


def main():
    # ---- Step 1: Ask the user for the simulation parameters ----------------
    mean_interarrival = float(input("Enter Mean Inter-Arrival time: "))
    mean_service = float(input("Enter Mean Service time: "))
    max_customers = int(input("Enter Maximum number of customers: "))

    # ---- Step 2: Set up the bookkeeping variables --------------------------
    clock = 0.0                 # the master simulation clock (current time)
    server_busy = False         # is the single server currently serving?
    num_in_queue = 0            # how many customers are waiting in line right now

    # These accumulators help us compute averages at the end.
    total_delay = 0.0           # sum of every customer's waiting time in queue
    num_delayed = 0             # how many customers have completed their wait
    area_num_in_queue = 0.0     # area under the "number in queue" curve over time
    area_server_busy = 0.0      # area under the "server busy" curve (for utilization)

    # ---- Step 3: Initialise the event list ---------------------------------
    # Two future events drive the simulation: the next arrival and the next
    # service completion (departure). We use a large number to mean "no event
    # scheduled yet".
    INFINITY = float("inf")
    time_next_arrival = exponential(mean_interarrival)  # first customer arrives
    time_next_departure = INFINITY                      # nobody being served yet

    # A simple FIFO queue holding the arrival time of each waiting customer.
    # We only store arrival times because that is all we need to compute delay.
    queue_arrival_times = []

    num_customers_served = 0    # stop the sim once this reaches max_customers

    # For the graph: record a sample of (clock, num_in_queue) at each event so
    # we can later draw how the queue length changed over the simulation time.
    time_samples = [clock]
    queue_length_samples = [num_in_queue]

    # ---- Step 4: The main simulation loop ----------------------------------
    # Keep processing events until the required number of customers is served.
    while num_customers_served < max_customers:

        # Decide which event happens next: whichever has the smaller time.
        next_event_time = min(time_next_arrival, time_next_departure)

        # Before moving the clock, update the time-weighted area statistics.
        # The gap is how long the system stayed in its current state.
        time_since_last_event = next_event_time - clock
        area_num_in_queue += num_in_queue * time_since_last_event
        if server_busy:
            area_server_busy += time_since_last_event

        # Advance the simulation clock to the time of this next event.
        clock = next_event_time

        # Record a sample of the queue length at this moment for the graph.
        time_samples.append(clock)
        queue_length_samples.append(num_in_queue)

        # ----- Case A: the next event is an ARRIVAL -----------------------
        if time_next_arrival <= time_next_departure:
            # Schedule the following arrival (unless we already have enough).
            time_next_arrival = clock + exponential(mean_interarrival)

            if not server_busy:
                # Server is free, so this customer is served immediately.
                # Their delay in queue is zero.
                num_delayed += 1
                total_delay += 0.0
                server_busy = True
                # Schedule when this customer will finish (a departure).
                time_next_departure = clock + exponential(mean_service)
            else:
                # Server is busy, so the customer must wait in line.
                num_in_queue += 1
                queue_arrival_times.append(clock)

        # ----- Case B: the next event is a DEPARTURE ----------------------
        else:
            # A customer just finished being served.
            num_customers_served += 1

            if num_in_queue == 0:
                # No one is waiting, so the server goes idle.
                server_busy = False
                time_next_departure = INFINITY
            else:
                # Pull the next customer (front of FIFO line) into service.
                num_in_queue -= 1
                arrival_time = queue_arrival_times.pop(0)
                # Their delay is how long they waited: now minus their arrival.
                delay = clock - arrival_time
                total_delay += delay
                num_delayed += 1
                # Schedule the new departure for this customer.
                time_next_departure = clock + exponential(mean_service)

        # After processing the event, record the updated queue length too so
        # the plotted curve shows the change caused by this event.
        time_samples.append(clock)
        queue_length_samples.append(num_in_queue)

    # ---- Step 5: Compute and display the final results ---------------------
    average_delay = total_delay / num_delayed          # average wait per customer
    average_num_in_queue = area_num_in_queue / clock   # time-averaged queue length
    server_utilization = area_server_busy / clock      # fraction of time busy

    print("\n--------- M/M/1 Simulation Results ---------")
    print(f"Average delay in queue      : {average_delay:.4f}")
    print(f"Average number in queue     : {average_num_in_queue:.4f}")
    print(f"Server utilization          : {server_utilization:.4f}")
    print(f"Time simulation ended       : {clock:.4f}")

    # ---- Step 6: Graphical representation of the output --------------------
    # Figure 1: how the number of customers in the queue evolved over time.
    # We use a step plot because the queue length only changes at events and
    # stays constant between them.
    plt.figure("Queue Length Over Time")
    plt.step(time_samples, queue_length_samples, where="post", color="tab:blue")
    plt.title("Number in Queue Over Simulation Time")
    plt.xlabel("Simulation time")
    plt.ylabel("Number of customers in queue")
    plt.grid(True, linestyle="--", alpha=0.5)

    # Figure 2: bar chart comparing the three summary metrics.
    plt.figure("Summary Metrics")
    metric_labels = ["Avg delay\nin queue",
                     "Avg number\nin queue",
                     "Server\nutilization"]
    metric_values = [average_delay, average_num_in_queue, server_utilization]
    bars = plt.bar(metric_labels, metric_values,
                   color=["tab:orange", "tab:green", "tab:red"])
    plt.title("M/M/1 Summary Metrics")
    plt.xlabel("Metric")
    plt.ylabel("Value")
    # Annotate each bar with its numeric value for readability.
    for bar, value in zip(bars, metric_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{value:.3f}", ha="center", va="bottom")

    plt.show()


if __name__ == "__main__":
    main()
