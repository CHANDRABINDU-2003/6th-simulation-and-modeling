import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SIM_TIME = 120.0
K = 32.0
i = 3.0
h = 1.0
p = 5.0
INIT_INVENTORY = 60
DEMAND_SIZES = [1, 2, 3, 4]
DEMAND_WEIGHTS = [1/6, 1/3, 1/3, 1/6]
MEAN_INTERDEMAND = 0.10
LEAD_TIME_MIN = 0.5
LEAD_TIME_MAX = 1.0
policies = [(20, 40), (20, 60), (20, 80), (20, 100), (40, 60), (40, 80), (40, 100), (60, 80), (60, 100)]

random.seed(1)
np.random.seed(1)

def demand_size():
    return random.choices(DEMAND_SIZES, weights=DEMAND_WEIGHTS)[0]

def simulate_policy(s, S):
    inventory = INIT_INVENTORY
    outstanding_order = 0
    order_arrival_time = None
    time = 0.0
    area_holding = 0.0
    area_backlog = 0.0
    total_order_cost = 0.0
    time_points = [0.0]
    inventory_levels = [inventory]
    while time < SIM_TIME:
        time_to_demand = np.random.exponential(MEAN_INTERDEMAND)
        next_demand_time = time + time_to_demand
        next_event_time = next_demand_time
        if order_arrival_time is not None:
            next_event_time = min(next_demand_time, order_arrival_time)
        holding = max(inventory, 0)
        backlog = max(-inventory, 0)
        area_holding += holding * (next_event_time - time)
        area_backlog += backlog * (next_event_time - time)
        time = next_event_time
        if order_arrival_time is not None and time == order_arrival_time:
            inventory += outstanding_order
            outstanding_order = 0
            order_arrival_time = None
        else:
            inventory -= demand_size()
        if outstanding_order == 0 and inventory < s:
            Z = S - inventory
            total_order_cost += K + i * Z
            lead_time = random.uniform(LEAD_TIME_MIN, LEAD_TIME_MAX)
            order_arrival_time = time + lead_time
            outstanding_order = Z
        time_points.append(time)
        inventory_levels.append(inventory)
    avg_holding_cost = h * area_holding / SIM_TIME
    avg_backlog_cost = p * area_backlog / SIM_TIME
    avg_order_cost = total_order_cost / SIM_TIME
    total_cost = avg_holding_cost + avg_backlog_cost + avg_order_cost
    return total_cost, avg_order_cost, avg_holding_cost, avg_backlog_cost, time_points, inventory_levels

results = []
all_graphs = []
for s, S in policies:
    total_c, order_c, hold_c, back_c, times, levels = simulate_policy(s, S)
    results.append([f"({s},{S})", round(total_c,2), round(order_c,2), round(hold_c,2), round(back_c,2)])
    all_graphs.append((f"({s},{S})", times, levels))

df = pd.DataFrame(results, columns=["Policy (s,S)", "Average Total Cost", "Average Ordering Cost", "Average Holding Cost", "Average Shortage Cost"])
print(df)

plt.figure(figsize=(12,6))
colors = plt.cm.get_cmap('tab10', len(all_graphs))
for idx, (label, times, levels) in enumerate(all_graphs):
    plt.step(times, levels, where='post', linewidth=2, label=label, color=colors(idx))
plt.xlabel("Time (months)")
plt.ylabel("Inventory Level")
plt.title("Comparison of Inventory Levels for Different (s,S) Policies")
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(title="Policy", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
