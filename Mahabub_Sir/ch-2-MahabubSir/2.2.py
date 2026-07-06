import random

class GamblingGame:
    def __init__(self):
        self.serial = 0
        self.cum_head = 0
        self.cum_tail = 0

    def play_one_round(self):
        """
        Simulates one game round.
        Stops when the difference between heads and tails is 3.
        Returns revenue = 8 - number of tosses.
        """
        while True:
            self.serial += 1
            random_num = random.randint(0, 1)
            if random_num == 0:
                self.cum_head += 1
            else:
                self.cum_tail += 1
            
            diff = abs(self.cum_head - self.cum_tail)
            if diff == 3:
                return 8 - self.serial  # Revenue for this game

if __name__ == "__main__":
    total_runs = 100       # Total number of games
    cumulative_profit = 0  # Cumulative profit tracker
    total_cost = 0
    total_earn = 0

    profits_per_game = []  # List to store cumulative profit after each game

    # Play games
    for i in range(1, total_runs + 1):
        game = GamblingGame()
        revenue = game.play_one_round()
        cost = 1  # Each game costs 1 unit

        total_cost += cost
        total_earn += revenue
        cumulative_profit = total_earn - total_cost
        profits_per_game.append(cumulative_profit)

        print(f"Game {i}: Cost = {cost}, Revenue = {revenue}, Cumulative Profit = {cumulative_profit}")

    # Find the best iteration to leave
    max_profit = max(profits_per_game)
    best_iteration = profits_per_game.index(max_profit) + 1  # +1 because list index starts at 0

    print("\n==============================")
    print(f"Total Games Played  : {total_runs}")
    print(f"Total Cost          : {total_cost}")
    print(f"Total Revenue       : {total_earn}")
    print(f"Final Cumulative Profit : {cumulative_profit}")
    print("==============================")
    print(f"Maximum Profit of {max_profit} occurred at Game {best_iteration}")
    print(f"Suggestion: You should consider leaving after Game {best_iteration} for maximum profit.")
