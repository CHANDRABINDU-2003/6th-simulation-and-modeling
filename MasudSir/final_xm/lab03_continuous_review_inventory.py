"""
==============================================================================
Lab 03: Inventory System Simulation (Continuous Review)
==============================================================================
Question:
    Build a simulation for an inventory system where demand is normally
    distributed. Implement a reorder point (s) and reorder quantity (S) policy.
    Track total holding costs and shortage costs over a fiscal year.

    Note on the (s, S) policy used here:
      - s = reorder point. When stock drops to or below s, we place an order.
      - S = the "order up to" target level. We order enough to bring our
            position back up to S.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter number of days in fiscal year (e.g. 365): : 365
    Enter starting inventory level:                 : 100
    Enter reorder point s:                          : 20
    Enter order-up-to level S:                      : 100
    Enter lead time in days:                        : 5
    Enter mean daily demand:                        : 5
    Enter standard deviation of daily demand:       : 2
    Enter holding cost per unit per day:            : 0.50
    Enter shortage cost per unit:                   : 5

    WHY: with a mean daily demand of 5 and S = 100, an order-up-to level of 100
    covers about 20 days of demand, while s = 20 (about 4 days) sits comfortably
    above the 5-day lead-time demand (~25 units expected). This keeps shortages
    rare but non-zero, so both holding and shortage costs are meaningful over
    the full 365-day year.
==============================================================================
"""

import random
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Collect parameters from the user --------------------------
    # A fiscal year is treated as 365 days here.
    num_days = int(input("Enter number of days in fiscal year (e.g. 365): "))
    starting_stock = int(input("Enter starting inventory level: "))
    s_reorder_point = int(input("Enter reorder point s: "))
    S_order_up_to = int(input("Enter order-up-to level S: "))
    lead_time = int(input("Enter lead time in days: "))

    # Demand is normally distributed, so we need its mean and standard deviation.
    mean_demand = float(input("Enter mean daily demand: "))
    std_demand = float(input("Enter standard deviation of daily demand: "))

    holding_cost_per_unit = float(input("Enter holding cost per unit per day: "))
    shortage_cost_per_unit = float(input("Enter shortage cost per unit: "))

    # ---- Step 2: Initialise the trackers -----------------------------------
    stock = starting_stock          # units physically on hand
    total_holding_cost = 0.0        # accumulates cost of carrying leftover stock
    total_shortage_cost = 0.0       # accumulates penalty for unmet demand
    total_shortage_units = 0        # how many units of demand we missed

    pending_order_arrival_day = None  # day a placed order will be delivered
    pending_order_amount = 0          # size of that pending order

    # For the graph: record the stock level at the end of each day.
    daily_stock_levels = []

    # ---- Step 3: Simulate the fiscal year day by day -----------------------
    for day in range(1, num_days + 1):

        # 3a. Receive any order that is scheduled to arrive today.
        if pending_order_arrival_day == day:
            stock += pending_order_amount
            pending_order_arrival_day = None
            pending_order_amount = 0

        # 3b. Draw today's demand from a normal distribution.
        #     Demand cannot be negative, so we clamp it at 0 and round to a
        #     whole number of units.
        demand = round(random.gauss(mean_demand, std_demand))
        if demand < 0:
            demand = 0

        # 3c. Fulfil the demand from current stock.
        if demand <= stock:
            stock -= demand                       # everything is sold
        else:
            # Demand exceeds stock: the leftover demand is a shortage.
            shortage = demand - stock
            total_shortage_units += shortage
            total_shortage_cost += shortage * shortage_cost_per_unit
            stock = 0                             # we run out completely

        # 3d. Charge holding cost on the inventory remaining at day's end.
        total_holding_cost += stock * holding_cost_per_unit

        # 3e. Continuous review: every day we check the inventory position.
        #     If stock is at or below s, order enough to reach S.
        if stock <= s_reorder_point and pending_order_arrival_day is None:
            order_size = S_order_up_to - stock    # bring position up to S
            pending_order_arrival_day = day + lead_time
            pending_order_amount = order_size

        # 3f. Record today's end-of-day stock level for the graph.
        daily_stock_levels.append(stock)

    # ---- Step 4: Print the yearly cost report ------------------------------
    total_cost = total_holding_cost + total_shortage_cost

    print("\n--------- Continuous Review Inventory Report ---------")
    print(f"Total holding cost   : {total_holding_cost:.2f}")
    print(f"Total shortage cost  : {total_shortage_cost:.2f}")
    print(f"Total shortage units : {total_shortage_units}")
    print(f"Total cost for year  : {total_cost:.2f}")
    print(f"Final stock on hand  : {stock} units")

    # ---- Step 5: Graphical representation of the output --------------------
    days = list(range(1, num_days + 1))

    # Figure 1: end-of-day stock over time, with horizontal dashed lines at the
    # reorder point s and the order-up-to level S so the (s, S) policy is clear.
    plt.figure("Stock Level Over Time")
    plt.plot(days, daily_stock_levels, color="tab:blue", label="End-of-day stock")
    plt.axhline(y=s_reorder_point, color="tab:red", linestyle="--",
                label=f"Reorder point s ({s_reorder_point})")
    plt.axhline(y=S_order_up_to, color="tab:green", linestyle="--",
                label=f"Order-up-to S ({S_order_up_to})")
    plt.title("Continuous Review Inventory: Stock vs Day")
    plt.xlabel("Day")
    plt.ylabel("Stock on hand (units)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    # Figure 2: bar chart comparing holding cost against shortage cost.
    plt.figure("Cost Breakdown")
    cost_labels = ["Holding cost", "Shortage cost"]
    cost_values = [total_holding_cost, total_shortage_cost]
    bars = plt.bar(cost_labels, cost_values,
                   color=["tab:green", "tab:red"])
    plt.title("Holding Cost vs Shortage Cost")
    plt.xlabel("Cost type")
    plt.ylabel("Total cost")
    for bar, value in zip(bars, cost_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{value:.2f}", ha="center", va="bottom")

    plt.show()


if __name__ == "__main__":
    main()
