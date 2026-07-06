"""
==============================================================================
Lab 18: Fast-Food Drive-Thru Model
==============================================================================
Question:
    Simulate a drive-thru process (order, pay, pick up) to identify the system's
    operational bottlenecks.
==============================================================================

A drive-thru is a series of three stations a car passes through in order:
    1. ORDER   2. PAY   3. PICK-UP
Each station is its own single-server queue. A car cannot move to the next
station until the previous one is done. By measuring how long cars spend WAITING
at each station, we can spot the BOTTLENECK -- the station with the longest
waits is the one slowing the whole system down.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Prompt 1 -> "Enter mean time between car arrivals (e.g. 3): "  type:  3
    Prompt 2 -> "Enter mean ORDER time (e.g. 2): "                 type:  2
    Prompt 3 -> "Enter mean PAY time (e.g. 1.5): "                 type:  1.5
    Prompt 4 -> "Enter mean PICK-UP time (e.g. 2.5): "             type:  2.5
    Prompt 5 -> "Enter number of cars to simulate (e.g. 100): "    type: 100
WHY: every station's service mean is below the arrival mean (3), so all three
stations stay stable (no infinite queue); PICK-UP has the largest service mean
(2.5), so it clearly emerges as the BOTTLENECK -- giving a meaningful, easy-to-
read result. 100 cars is enough for the averages to settle.
------------------------------------------------------------------------------
"""

import random
import math
import matplotlib.pyplot as plt


def exponential(mean):
    # Inverse-transform exponential for arrivals and station service times.
    return -mean * math.log(1.0 - random.random())


def main():
    # ---- Step 1: Read the parameters ---------------------------------------
    mean_interarrival = float(input("Enter mean time between car arrivals (e.g. 3): "))
    mean_order = float(input("Enter mean ORDER time (e.g. 2): "))
    mean_pay = float(input("Enter mean PAY time (e.g. 1.5): "))
    mean_pickup = float(input("Enter mean PICK-UP time (e.g. 2.5): "))
    num_cars = int(input("Enter number of cars to simulate (e.g. 100): "))

    # ---- Step 2: Track when each station becomes free ----------------------
    # Because cars are served in order, we can process them sequentially. For
    # each station we remember the time it will be free for the next car.
    station_free = {"order": 0.0, "pay": 0.0, "pickup": 0.0}

    # Accumulators for total waiting time at each station.
    total_wait = {"order": 0.0, "pay": 0.0, "pickup": 0.0}

    arrival_time = 0.0

    # ---- Step 3: Push each car through the three stations ------------------
    for car in range(num_cars):
        # Work out when this car arrives at the drive-thru entrance.
        arrival_time += exponential(mean_interarrival)

        # ----- Station 1: ORDER -----
        # The car starts ordering at the later of (its arrival) and
        # (the moment the order station is free). The gap is its wait.
        start_order = max(arrival_time, station_free["order"])
        total_wait["order"] += start_order - arrival_time
        finish_order = start_order + exponential(mean_order)
        station_free["order"] = finish_order

        # ----- Station 2: PAY -----
        # The car reaches "pay" only after it finished ordering.
        start_pay = max(finish_order, station_free["pay"])
        total_wait["pay"] += start_pay - finish_order
        finish_pay = start_pay + exponential(mean_pay)
        station_free["pay"] = finish_pay

        # ----- Station 3: PICK-UP -----
        start_pickup = max(finish_pay, station_free["pickup"])
        total_wait["pickup"] += start_pickup - finish_pay
        finish_pickup = start_pickup + exponential(mean_pickup)
        station_free["pickup"] = finish_pickup

    # ---- Step 4: Compute average waits and find the bottleneck -------------
    avg_wait = {s: total_wait[s] / num_cars for s in total_wait}
    # The bottleneck is simply the station with the largest average wait.
    bottleneck = max(avg_wait, key=avg_wait.get)

    # ---- Step 5: Report -----------------------------------------------------
    print("\n--------- Drive-Thru Simulation Results ---------")
    print(f"Average wait at ORDER   : {avg_wait['order']:.4f}")
    print(f"Average wait at PAY     : {avg_wait['pay']:.4f}")
    print(f"Average wait at PICK-UP : {avg_wait['pickup']:.4f}")
    print(f"\nBOTTLENECK station      : {bottleneck.upper()} "
          f"(longest average wait)")

    # ---- Step 6: Graphical view of the average wait per station ------------
    # A bar chart makes the bottleneck pop out: we colour the bottleneck bar
    # red and the others a neutral grey.
    stations = ["order", "pay", "pickup"]
    labels = ["ORDER", "PAY", "PICK-UP"]
    heights = [avg_wait[s] for s in stations]
    colors = ["tab:red" if s == bottleneck else "tab:gray" for s in stations]

    plt.figure()
    plt.bar(labels, heights, color=colors)
    plt.title(f"Lab 18: Drive-Thru Average Wait per Station "
              f"(Bottleneck = {bottleneck.upper()})")
    plt.xlabel("Station")
    plt.ylabel("Average waiting time")
    plt.grid(True, axis="y", linestyle=":", alpha=0.5)
    plt.show()


if __name__ == "__main__":
    main()
