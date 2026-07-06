c1 = [0.0] * 200
c2 = [0.0] * 200
c3 = [0.0] * 200

k1 = 0.025
k2 = 0.01
delta = 0.1

c1[0] = 50.0
c2[0] = 25.0
c3[0] = 0.0

t = 0.0
time = 15.0
i = 0

print("\n Time     C1      C2      C3")

while t <= time:
    print(f"{t:5.2f}  {c1[i]:6.2f}  {c2[i]:6.2f}  {c3[i]:6.2f}")

    c1.append(0)
    c2.append(0)
    c3.append(0)

    c1[i+1] = c1[i] + (k2*c3[i] - k1*c1[i]*c2[i]) * delta
    c2[i+1] = c2[i] + (k2*c3[i] - k1*c1[i]*c2[i]) * delta
    c3[i+1] = c3[i] + 2.0 * (k1*c1[i]*c2[i] - k2*c3[i]) * delta

    i += 1
    t += delta

    if t >= 2.0:
        delta = 0.2
    if t >= 6.0:
        delta = 0.4

input("\nAny digit to exit...")