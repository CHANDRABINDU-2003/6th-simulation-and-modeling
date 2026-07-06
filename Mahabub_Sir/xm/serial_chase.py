import math, random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---- Config ----
AMIN, AMAX = 0, 100
T_MIN = 30
DT = 1.0
T_SEC = T_MIN * 60
WIN = [6, 12, 18, 24, 30, 36]   # comm window per 5-min interval
ISEC = 5 * 60                   # interval length in seconds
WTOL, CTOL = 1.0, 0.5           # reach tolerances

class Node:
    def __init__(self, label, x, y, speed, last=False):
        self.label, self.x, self.y, self.speed = label, x, y, speed
        self.last = last
        if last:
            self.wx, self.wy = random.uniform(AMIN, AMAX), random.uniform(AMIN, AMAX)
        self.traj = [(x, y)]

    def move(self, tx, ty, tol):
        dx, dy = tx - self.x, ty - self.y
        d = math.hypot(dx, dy)
        if d <= tol or self.speed * DT >= d:
            self.x, self.y = tx, ty
            return True
        r = self.speed * DT / d
        self.x += dx * r; self.y += dy * r
        return False

    def step(self):
        if self.last:
            if self.move(self.wx, self.wy, WTOL):
                self.wx, self.wy = random.uniform(AMIN, AMAX), random.uniform(AMIN, AMAX)

    def chase(self, target):
        self.move(target.x, target.y, CTOL)

    def record(self):
        self.traj.append((self.x, self.y))


def labels(n):
    out = []
    for i in range(n):
        s, k = "", i
        while True:
            s = chr(65 + k % 26) + s
            k = k // 26 - 1
            if k < 0: break
        out.append(s)
    return out


def make_nodes(n, speeds):
    L = labels(n)
    return [Node(L[i], random.uniform(AMIN, AMAX), random.uniform(AMIN, AMAX),
                 speeds[i], last=(i == n - 1)) for i in range(n)]


def get_speeds(n):
    # Manually prompt the user for each node's speed (no auto-assignment)
    L = labels(n)
    s = []
    for lbl in L:
        while True:
            try:
                v = float(input(f"Speed of {lbl}: "))
                if v <= 0:
                    print("  Speed must be positive.")
                    continue
                s.append(v)
                break
            except ValueError:
                print("  Invalid number, try again.")
    return s


def simulate(nodes):
    steps = int(T_SEC / DT)
    for _ in range(steps):
        n = len(nodes)
        nodes[-1].step()
        for i in range(n - 2, -1, -1):
            nodes[i].chase(nodes[i + 1])
        for nd in nodes:
            nd.record()
    return steps


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


def collisions(nodes, s0, s1, w):
    n = len(nodes)
    state = {(i, j): False for i in range(n) for j in range(i + 1, n)}
    cnt, pts = 0, []
    for s in range(s0, s1 + 1):
        for i in range(n):
            for j in range(i + 1, n):
                p, q = nodes[i].traj[s], nodes[j].traj[s]
                inr = dist(p, q) <= w
                if inr and not state[(i, j)]:
                    cnt += 1
                    pts.append({"pair": (nodes[i].label, nodes[j].label), "step": s,
                                "x": (p[0]+q[0])/2, "y": (p[1]+q[1])/2})
                state[(i, j)] = inr
    return cnt, pts


def all_intervals(nodes, steps):
    spi = int(ISEC / DT)
    res, cum = [], 0
    for i in range(6):
        s0, s1 = i * spi, min((i + 1) * spi, steps)
        c, pts = collisions(nodes, s0, s1, WIN[i])
        cum += c
        res.append({"idx": i+1, "t0": i*5, "t1": (i+1)*5, "w": WIN[i],
                     "s0": s0, "s1": s1, "count": c, "cum": cum, "pts": pts})
    return res


def print_table(res, total):
    print(f"{'Int':<5}{'Time':<12}{'Win':<6}{'Coll':<6}{'Cum':<6}")
    for r in res:
        print(f"{r['idx']:<5}{r['t0']}-{r['t1']} min  {r['w']:<6}{r['count']:<6}{r['cum']:<6}")
    print(f"Total collisions: {total}")


def colors(nodes):
    c = plt.cm.tab10.colors
    return {nd.label: c[i % 10] for i, nd in enumerate(nodes)}


def animate(nodes, res, col):
    s0, s1, w = res["s0"], res["s1"], res["w"]
    pts_by_step = {}
    for p in res["pts"]:
        pts_by_step.setdefault(p["step"], []).append(p)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.set_xlim(AMIN-5, AMAX+5); ax.set_ylim(AMIN-5, AMAX+5)
    ax.set_title(f"Live - Interval {res['idx']} ({res['t0']}-{res['t1']} min) win={w}")
    ax.grid(True)

    dots = {nd.label: ax.plot([], [], 'o', color=col[nd.label], ms=10,
                               mec='black')[0] for nd in nodes}
    txts = {nd.label: ax.text(0, 0, nd.label, fontweight='bold', color=col[nd.label])
            for nd in nodes}
    lines = [ax.plot([], [], '-', color='gray', alpha=0.6)[0] for _ in range(len(nodes)-1)]
    ctext = ax.text(0.02, 0.98, "Collisions: 0", transform=ax.transAxes, va='top',
                     fontweight='bold', bbox=dict(boxstyle="round", fc="white"))

    frames = list(range(s0, s1 + 1))
    active, hi_until, state = [], {nd.label: -1 for nd in nodes}, {"n": 0}

    def update(fi):
        step = frames[fi]
        for nd in nodes:
            x, y = nd.traj[step]
            dots[nd.label].set_data([x], [y])
            txts[nd.label].set_position((x+1, y+1))
        for i in range(len(nodes)-1):
            x1, y1 = nodes[i].traj[step]
            x2, y2 = nodes[i+1].traj[step]
            lines[i].set_data([x1, x2], [y1, y2])
        if step in pts_by_step:
            for p in pts_by_step[step]:
                state["n"] += 1
                m = ax.scatter(p["x"], p["y"], marker='X', s=200, color='red', edgecolor='black')
                t = ax.text(p["x"]+1, p["y"]+1, f"{p['pair'][0]}-{p['pair'][1]}", color='darkred')
                active.append([m, fi+10]); active.append([t, fi+10])
                for lbl in p["pair"]:
                    hi_until[lbl] = fi + 10
        for nd in nodes:
            dots[nd.label].set_markersize(18 if fi <= hi_until[nd.label] else 10)
        keep = []
        for a, exp in active:
            if fi > exp: a.remove()
            else: keep.append([a, exp])
        active[:] = keep
        ctext.set_text(f"Collisions: {state['n']}")
        return list(dots.values()) + list(txts.values()) + lines + [ctext]

    # Slower frame interval (150ms) so movement/chasing/collisions are clearly visible
    anim = animation.FuncAnimation(fig, update, frames=len(frames), interval=150, repeat=False)
    plt.show()
    return anim


def plot_trajectories(nodes, res, col):
    s0, s1, w, pts = res["s0"], res["s1"], res["w"], res["pts"]
    fig, ax = plt.subplots(figsize=(7, 7))
    for nd in nodes:
        seg = nd.traj[s0:s1+1]
        xs, ys = [p[0] for p in seg], [p[1] for p in seg]
        ax.plot(xs, ys, '-o', ms=2, color=col[nd.label], label=f"Node {nd.label}")
        ax.scatter(xs[0], ys[0], color=col[nd.label], marker='s', s=60, edgecolor='black')
        ax.scatter(xs[-1], ys[-1], color=col[nd.label], marker='^', s=70, edgecolor='black')
        ax.annotate(nd.label, (xs[-1], ys[-1]), fontweight='bold', color=col[nd.label])
    if pts:
        ax.scatter([p["x"] for p in pts], [p["y"] for p in pts], marker='X', s=160,
                   color='red', edgecolor='black', label=f"Collisions ({len(pts)})")
    ax.set_xlim(AMIN-5, AMAX+5); ax.set_ylim(AMIN-5, AMAX+5)
    ax.set_xlabel("X"); ax.set_ylabel("Y")
    ax.set_title(f"Trajectory - Interval {res['idx']} ({res['t0']}-{res['t1']} min) win={w}")
    ax.grid(True); ax.legend(loc='upper left', bbox_to_anchor=(1.02, 1), fontsize=8)
    fig.tight_layout()
    plt.show()


def visualize_all(nodes, results):
    col = colors(nodes)
    for r in results:
        animate(nodes, r, col)
        plot_trajectories(nodes, r, col)
    # Final summary: collisions vs communication window size
    w = [r["w"] for r in results]
    c = [r["count"] for r in results]
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(w, c, '-o', color='steelblue', ms=8)
    for wi, ci in zip(w, c):
        ax.annotate(str(ci), (wi, ci), textcoords="offset points", xytext=(0, 8),
                    ha='center', fontweight='bold')
    ax.set_title("Collision Count vs Communication Window Size")
    ax.set_xlabel("Communication Window Size (units)")
    ax.set_ylabel("Collision Count")
    ax.grid(True)
    fig.tight_layout()
    plt.show()


def main():
    n = int(input("Number of nodes: "))
    s = get_speeds(n)
    nodes = make_nodes(n, s)
    steps = simulate(nodes)
    results = all_intervals(nodes, steps)
    total = results[-1]["cum"]
    print_table(results, total)
    visualize_all(nodes, results)


if __name__ == "__main__":
    main()
