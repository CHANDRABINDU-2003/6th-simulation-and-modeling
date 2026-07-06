import math
import matplotlib.pyplot as plt

Arrival = [0.4, 1.2, 0.5, 1.7, 0.2, 1.6, 0.2, 1.4, 1.9]
Service = [2.0, 0.7, 0.2, 1.1, 3.7, 0.6]
ServiceNum = len(Service)

server_status = 0
number_in_queue = 0
times_of_arrival = []
time_of_last_event = 0.0

clock = 0.0
event_list_arrival = 0.0
event_list_departure = math.inf

number_delayed = 0
total_delay = 0.0
area_under_q = 0.0
area_under_b = 0.0

queue_times = []

def handle_arrival():
    global server_status, number_in_queue, number_delayed
    global event_list_departure, area_under_b, area_under_q

    area_under_b += server_status * (clock - time_of_last_event)
    area_under_q += number_in_queue * (clock - time_of_last_event)

    if server_status == 0:
        server_status = 1
        number_delayed += 1
        event_list_departure = clock + Service.pop(0)
    else:
        number_in_queue += 1
        times_of_arrival.append(clock)

def handle_departure():
    global server_status, number_in_queue, number_delayed
    global event_list_departure, total_delay
    global area_under_b, area_under_q

    area_under_b += server_status * (clock - time_of_last_event)
    area_under_q += number_in_queue * (clock - time_of_last_event)

    if number_in_queue == 0:
        server_status = 0
        event_list_departure = math.inf
    else:
        number_in_queue -= 1
        delay = clock - times_of_arrival.pop(0)
        total_delay += delay
        number_delayed += 1
        event_list_departure = clock + Service.pop(0)

def event_handler():
    global clock, event_list_arrival, event_list_departure, time_of_last_event

    queue_times.append((clock, number_in_queue))

    if event_list_arrival <= event_list_departure:
        time_of_last_event = clock
        clock = event_list_arrival
        event_list_arrival = clock + Arrival.pop(0) if Arrival else math.inf
        handle_arrival()
    else:
        time_of_last_event = clock
        clock = event_list_departure
        handle_departure()

event_list_arrival = Arrival.pop(0)

while number_delayed < ServiceNum:
    event_handler()

print("Single-Server Queueing System Simulation Results")
print("-" * 60)
print("Average Delay in Queue:", total_delay / number_delayed)
print("Average Number in Queue:", area_under_q / clock)
print("Server Utilization:", area_under_b / clock)
print("Simulation End Time:", clock)

times, queue_lengths = zip(*queue_times)

plt.figure(figsize=(10, 5))
plt.step(times, queue_lengths, where='post', linewidth=2.8, color='black', label='Queue Length')
plt.scatter(times, queue_lengths, color='red', s=28, zorder=3, label='Event Points')
plt.xlabel('Simulation Time')
plt.ylabel('Number in Queue')
plt.title('Discrete-Event Queue Length Evolution')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend(frameon=False)
plt.tight_layout()
plt.show()
