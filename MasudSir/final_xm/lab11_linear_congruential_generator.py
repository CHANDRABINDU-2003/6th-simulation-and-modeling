"""
==============================================================================
Lab 11: Linear Congruential Generator (LCG)
==============================================================================
Question:
    LCG is considered one of the basic yet best methods to generate
    Pseudo-Random Numbers. Write a program which generates the random number
    using the LCG.
==============================================================================

The LCG produces a sequence of numbers using this recurrence relation:
    X(next) = (a * X(current) + c) mod m
where:
    X0 = the seed (the starting value)
    a  = the multiplier
    c  = the increment
    m  = the modulus
To turn each integer into a number between 0 and 1, we divide it by m.

------------------------------------------------------------------------------
SAMPLE / RECOMMENDED INPUT
------------------------------------------------------------------------------
    Enter the seed X0 (e.g. 7):                  -> 7
    Enter the multiplier a (e.g. 1103515245):    -> 1103515245
    Enter the increment c (e.g. 12345):          -> 12345
    Enter the modulus m (e.g. 2147483648):       -> 2147483648
    Enter how many random numbers to generate:   -> 100

WHY: These a, c, m values are the well-known glibc LCG constants, which have a
     full period and good statistical spread. Generating 100 numbers gives a
     long enough sequence for the scatter/histogram plots to show the
     approximate uniformity over [0, 1).
------------------------------------------------------------------------------
"""

import matplotlib.pyplot as plt


def main():
    # ---- Step 1: Read the four LCG parameters plus the seed ----------------
    seed = int(input("Enter the seed X0 (e.g. 7): "))
    a = int(input("Enter the multiplier a (e.g. 1103515245): "))
    c = int(input("Enter the increment c (e.g. 12345): "))
    m = int(input("Enter the modulus m (e.g. 2147483648): "))
    count = int(input("Enter how many random numbers to generate: "))

    # ---- Step 2: Generate the sequence -------------------------------------
    x = seed                # x holds the "current" value in the sequence
    indices = []            # store n values for the scatter plot
    normalized_values = []  # collect the normalized Xn/m values for plotting
    print("\n  n |      Xn       |  Xn / m (0 to 1)")
    print("----+---------------+------------------")

    for n in range(1, count + 1):
        # Apply the LCG formula to get the next integer in the sequence.
        x = (a * x + c) % m

        # Normalise to a value in [0, 1) by dividing by the modulus.
        normalized = x / m

        # Keep the values so we can graph the sequence afterwards.
        indices.append(n)
        normalized_values.append(normalized)

        # Show both the raw integer and its 0-to-1 version.
        print(f"{n:3} | {x:13} | {normalized:.6f}")

    # ---- Step 3: Graphical representation of the output --------------------
    # Figure 1: scatter of index n vs normalized value (shows the sequence).
    plt.figure(figsize=(10, 5))
    plt.scatter(indices, normalized_values, color="steelblue", s=20)
    plt.title("LCG Sequence: Normalized Value vs Index")
    plt.xlabel("n (index in the sequence)")
    plt.ylabel("Xn / m  (value in [0, 1))")

    # Figure 2: histogram of the normalized values (shows uniformity).
    plt.figure(figsize=(10, 5))
    plt.hist(normalized_values, bins=10, range=(0, 1),
             color="seagreen", edgecolor="black")
    plt.title("Histogram of Normalized LCG Values (Uniformity Check)")
    plt.xlabel("Xn / m  (value in [0, 1))")
    plt.ylabel("Frequency")

    plt.show()


if __name__ == "__main__":
    main()
