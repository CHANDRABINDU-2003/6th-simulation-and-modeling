"""
==============================================================================
Lab 02: Inventory Management
==============================================================================
Question:
    Inventory management is a crucial aspect of any business that deals with
    physical goods. Write a program to simulate an inventory system.

    In this simulation we model a shop over a number of days. Each day a random
    customer demand arrives. We sell what we can from stock, and whatever we
    cannot sell becomes a "shortage". Whenever the stock drops to or below a
    reorder level, we place an order that arrives after a fixed lead time. We
    track holding cost (cost of storing leftover stock) and ordering cost.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter number of days to simulate:        : 30
    Enter starting inventory level:          : 100
    Enter reorder point (when to order):     : 20
    Enter order quantity (how much to order):: 80
    Enter lead time in days (delivery delay):: 3
    Enter holding cost per unit per day:     : 0.50
    Enter fixed cost per order placed:       : 50
    Enter maximum possible daily demand:     : 10

    WHY: with a max daily demand of 10, a 30-day run consumes roughly 150 units,
    so a starting stock of 100 plus reorders (quantity 80, reorder point 20,
    short 3-day lead time) keeps the shelf stocked, triggers a few clear reorder
    events, and yields meaningful, non-trivial holding and ordering costs.
==============================================================================
"""

import random
import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Get all the inventory parameters from the user ------------
    num_days = int(input("Enter number of days to simulate: "))
    starting_stock = int(input("Enter starting inventory level: "))
    reorder_point = int(input("Enter reorder point (when to order): "))
    order_quantity = int(input("Enter order quantity (how much to order): "))
    lead_time = int(input("Enter lead time in days (delivery delay): "))
    holding_cost = float(input("Enter holding cost per unit per day: "))
    ordering_cost = float(input("Enter fixed cost per order placed: "))
    max_daily_demand = int(input("Enter maximum possible daily demand: "))

    # ---- Step 2: Initialise the running totals -----------------------------
    stock = starting_stock          # how many units we currently have on the shelf
    total_holding_cost = 0.0        # accumulates storage cost across all days
    total_ordering_cost = 0.0       # accumulates the cost of placing orders
    total_shortage = 0              # total units of demand we could NOT meet
    total_demand = 0                # total customer demand seen over the period

    # When an order is "in transit" we remember the day it should arrive.
    # A value of None means there is currently no pending order.
    pending_order_arrival_day = None
    pending_order_amount = 0

    # For the graph: record the stock level at the end of each day.
    daily_stock_levels = []

    # ---- Step 3: Walk through each day of the simulation -------------------
    for day in range(1, num_days + 1):

        # 3a. First, check if a previously placed order arrives today.
        if pending_order_arrival_day == day:
            stock += pending_order_amount          # add delivered units to stock
            print(f"Day {day}: Order of {pending_order_amount} units arrived.")
            pending_order_arrival_day = None       # clear the pending order
            pending_order_amount = 0

        # 3b. Generate today's random customer demand (0 .. max_daily_demand).
        demand = random.randint(0, max_daily_demand)
        total_demand += demand

        # 3c. Try to satisfy the demand from current stock.
        if demand <= stock:
            stock -= demand                        # we sell everything requested
        else:
            # Not enough stock: we sell what we have and record the shortfall.
            shortage = demand - stock
            total_shortage += shortage
            stock = 0                              # shelf is now empty

        # 3d. At the end of the day, pay holding cost on whatever is left over.
        total_holding_cost += stock * holding_cost

        # 3e. Reorder logic: if stock fell to/below the reorder point and there
        #     is no order already on the way, place a new order now.
        if stock <= reorder_point and pending_order_arrival_day is None:
            pending_order_arrival_day = day + lead_time
            pending_order_amount = order_quantity
            total_ordering_cost += ordering_cost
            print(f"Day {day}: Stock low ({stock}). Ordered {order_quantity} "
                  f"units, arriving day {pending_order_arrival_day}.")

        # 3f. Record today's end-of-day stock level for the graph.
        daily_stock_levels.append(stock)

    # ---- Step 4: Report the final summary ----------------------------------
    total_cost = total_holding_cost + total_ordering_cost

    print("\n--------- Inventory Simulation Summary ---------")
    print(f"Total customer demand    : {total_demand} units")
    print(f"Total unmet demand       : {total_shortage} units")
    print(f"Total holding cost       : {total_holding_cost:.2f}")
    print(f"Total ordering cost      : {total_ordering_cost:.2f}")
    print(f"Total inventory cost     : {total_cost:.2f}")
    print(f"Final stock on hand      : {stock} units")

    # ---- Step 5: Graphical representation of the output --------------------
    days = list(range(1, num_days + 1))

    # Figure 1: end-of-day stock level over time, with the reorder point shown
    # as a horizontal dashed line so we can see when reorders are triggered.
    plt.figure("Stock Level Over Time")
    plt.plot(days, daily_stock_levels, marker="o", color="tab:blue",
             label="End-of-day stock")
    plt.axhline(y=reorder_point, color="tab:red", linestyle="--",
                label=f"Reorder point ({reorder_point})")
    plt.title("Inventory Stock Level vs Day")
    plt.xlabel("Day")
    plt.ylabel("Stock on hand (units)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)

    # Figure 2: bar chart breaking the total cost into holding vs ordering.
    plt.figure("Cost Breakdown")
    cost_labels = ["Holding cost", "Ordering cost"]
    cost_values = [total_holding_cost, total_ordering_cost]
    bars = plt.bar(cost_labels, cost_values,
                   color=["tab:green", "tab:orange"])
    plt.title("Inventory Cost Breakdown")
    plt.xlabel("Cost type")
    plt.ylabel("Total cost")
    for bar, value in zip(bars, cost_values):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                 f"{value:.2f}", ha="center", va="bottom")

    plt.show()


if __name__ == "__main__":
    main()
