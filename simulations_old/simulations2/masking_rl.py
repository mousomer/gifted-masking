"""
Masking vs. authenticity in gifted children as a ladder of RL games.

Ladder (each rung adds exactly one mechanism):
  M0  two-armed bandit            : mask (safe) vs authentic (risky)        -> hot-stove lock-in
  M1  graded disclosure d in [0,1]: does action granularity rescue?         -> dimensionality (actions)
  M2  stigma MDP (3 states)       : revealing is informationally sticky     -> structural lock-in
  M3  K peer groups, one good pond: exploration burden of finding the pond  -> dimensionality (contexts)

Payoff primitives (all grounded in the literature review):
  b  belonging reward when accepted
  a  intrinsic authenticity reward (scales with disclosure)
  c  suppression cost paid while masking ("hiding is stress generating")
  r  rejection penalty when authenticity fails (jealousy / exclusion / bullying)
  p  peer receptivity (school culture, similar-ability peers)
  eta  stigma escape probability per step (stickiness of the label)
  bf BFLPE comparison cost inside the good pond

Learner ("person type") parameters:
  alpha learning rate (recency weighting)   temp  softmax temperature (boldness)
  lam   loss aversion (emotional intensity) q0    optimistic initialization (self-esteem prior)

All runs are vectorized across seeds (axis 0 = independent children).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------------------------------------------------------- shared core

def softmax_sample(Q, temp, rng):
    """Sample one action per row of Q (n, A) from a softmax policy."""
    z = Q / temp
    z -= z.max(axis=1, keepdims=True)
    P = np.exp(z)
    P /= P.sum(axis=1, keepdims=True)
    u = rng.random((Q.shape[0], 1))
    return (u > P.cumsum(axis=1)).sum(axis=1)


def loss_avert(rew, lam):
    """Loss-averse subjective value: negative outcomes weighted by lam >= 1."""
    return np.where(rew < 0, lam * rew, rew)


DEF = dict(b=1.0, a=0.6, c=0.25, r=2.0)          # environment defaults
AGENT = dict(alpha=0.1, temp=0.25, lam=1.0, q0=0.0)  # learner defaults

# ------------------------------------------------------------------ M0 bandit

def run_m0(p, b=1.0, a=0.6, c=0.25, r=2.0,
           n=300, T=1500, alpha=0.1, temp=0.25, lam=1.0, q0=0.0, seed=0):
    """Stateless 2-armed bandit. Returns per-seed mask rate in final window."""
    rng = np.random.default_rng(seed)
    Q = np.full((n, 2), float(q0))          # arm 0 = mask, arm 1 = authentic
    idx = np.arange(n)
    win = T // 5
    mask_cnt = np.zeros(n)
    for t in range(T):
        act = softmax_sample(Q, temp, rng)
        accept = rng.random(n) < p
        rew = np.where(act == 0, b - c, np.where(accept, b + a, a - r))
        Q[idx, act] += alpha * (loss_avert(rew, lam) - Q[idx, act])
        if t >= T - win:
            mask_cnt += (act == 0)
    return mask_cnt / win


def m0_expected_gap(p, b, a, c, r):
    """E[authentic] - E[mask]; >0 means authenticity is objectively better."""
    return (a + p * b - (1 - p) * r) - (b - c)

# ------------------------------------------------------- M1 graded disclosure

def run_m1(p, levels=5, b=1.0, a=0.6, c=0.25, r=2.0,
           n=300, T=1500, alpha=0.1, temp=0.25, lam=1.0, q0=0.0, seed=0):
    """Disclosure level d in {0..1}. Acceptance prob = 1-(1-p)d.
    Returns per-seed mean disclosure in final window."""
    rng = np.random.default_rng(seed)
    d = np.linspace(0.0, 1.0, levels)
    Q = np.full((n, levels), float(q0))
    idx = np.arange(n)
    win = T // 5
    dsum = np.zeros(n)
    for t in range(T):
        act = softmax_sample(Q, temp, rng)
        dd = d[act]
        accept = rng.random(n) < 1.0 - (1.0 - p) * dd
        base = a * dd - c * (1.0 - dd)
        rew = np.where(accept, base + b, base - r)
        Q[idx, act] += alpha * (loss_avert(rew, lam) - Q[idx, act])
        if t >= T - win:
            dsum += dd
    return dsum / win

# ----------------------------------------------------------- M2 stigma MDP

def run_m2(p, eta, b=1.0, a=0.6, c=0.25, r=2.0, b2=0.5, r2=2.5, delta=0.02,
           n=300, T=2000, alpha=0.1, temp=0.25, lam=1.0, q0=0.0,
           gamma=0.9, seed=0):
    """States: 0 neutral, 1 accepted-as-self, 2 stigmatized.
    Authentic in s=0: accepted w.p. p -> s=1, else rejected -> s=2 (sticky).
    Stigma: weaker belonging even when masking (b2<b), harsher rejection (r2),
    redemption attempts succeed only w.p. p/2; escapes w.p. eta per step.
    Accepted state decays w.p. delta (peer turnover). Q-learning (gamma).
    Returns per-seed mask rate in final window."""
    rng = np.random.default_rng(seed)
    Q = np.full((n, 3, 2), float(q0))
    s = np.zeros(n, dtype=int)
    idx = np.arange(n)
    win = T // 5
    mask_cnt = np.zeros(n)
    for t in range(T):
        act = softmax_sample(Q[idx, s], temp, rng)
        u = rng.random(n)
        rew = np.empty(n)
        s2 = s.copy()
        m_auth = act == 1
        # state 0 (neutral)
        st0 = s == 0
        rew[st0 & ~m_auth] = b - c
        acc = st0 & m_auth & (u < p)
        rej = st0 & m_auth & (u >= p)
        rew[acc] = b + a; s2[acc] = 1
        rew[rej] = a - r; s2[rej] = 2
        # state 1 (accepted as self)
        st1 = s == 1
        rew[st1 & ~m_auth] = b - c
        rew[st1 & m_auth] = b + a
        turn = st1 & (rng.random(n) < delta)
        s2[turn & (s2 == 1)] = 0
        # state 2 (stigmatized)
        st2 = s == 2
        rew[st2 & ~m_auth] = b2 - c
        red = st2 & m_auth & (u < p / 2)          # redemption succeeds
        rew[red] = b + a; s2[red] = 1
        fail = st2 & m_auth & (u >= p / 2)
        rew[fail] = a - r2
        esc = st2 & (rng.random(n) < eta)
        s2[esc & (s2 == 2)] = 0
        # Q-learning update
        target = loss_avert(rew, lam) + gamma * Q[idx, s2].max(axis=1)
        Q[idx, s, act] += alpha * (target - Q[idx, s, act])
        s = s2
        if t >= T - win:
            mask_cnt += (act == 0)
    return mask_cnt / win

# ------------------------------------------------- M3 peer-group selection

def run_m3(K, p_good=0.85, p_bad=0.2, bf=0.0, b=1.0, a=0.6, c=0.25, r=2.0,
           n=400, T=2000, alpha=0.1, temp=0.25, lam=1.0, q0=0.0, seed=0):
    """K peer groups; group 0 is the receptive 'good pond'.
    Arms: 2g = mask in group g, 2g+1 = authentic in group g.
    bf = BFLPE comparison cost inside the good pond (subtracted on acceptance).
    Returns (per-seed P(modal final arm is optimal), per-seed mask share)."""
    rng = np.random.default_rng(seed)
    pvec = np.full(K, p_bad); pvec[0] = p_good
    Q = np.full((n, 2 * K), float(q0))
    idx = np.arange(n)
    win = T // 5
    arm_cnt = np.zeros((n, 2 * K)); mask_cnt = np.zeros(n)
    OPT = 1                                       # authentic in good pond
    for t in range(T):
        act = softmax_sample(Q, temp, rng)
        g = act // 2
        is_auth = (act % 2) == 1
        accept = rng.random(n) < pvec[g]
        rew = np.where(~is_auth, b - c,
                       np.where(accept, b + a - bf * (g == 0), a - r))
        Q[idx, act] += alpha * (loss_avert(rew, lam) - Q[idx, act])
        if t >= T - win:
            arm_cnt[idx, act] += 1
            mask_cnt += (~is_auth)
    modal = arm_cnt.argmax(axis=1)                # most-used arm, final window
    return modal == OPT, mask_cnt / win, modal

# ----------------------------------------------------------------- figures

def heat(ax, Z, x, y, title, xlab, ylab, vmin=0, vmax=1):
    im = ax.pcolormesh(x, y, Z, shading="auto", cmap="RdYlBu_r",
                       vmin=vmin, vmax=vmax)
    ax.set(title=title, xlabel=xlab, ylabel=ylab)
    return im


def fig_m0(out):
    ps = np.linspace(0.05, 0.95, 19)
    rs = np.linspace(0.0, 4.0, 17)
    Z = np.empty((len(rs), len(ps)))
    for i, r in enumerate(rs):
        for j, p in enumerate(ps):
            Z[i, j] = run_m0(p, r=r, seed=i * 100 + j).mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    im = heat(axes[0], Z, ps, rs,
              "M0: mean mask rate (final phase)",
              "peer receptivity p", "rejection penalty r")
    # objective indifference curve: E[auth] = E[mask]
    pp = np.linspace(0.05, 0.95, 200)
    rstar = (DEF["a"] + DEF["c"]) / (1 - pp) - DEF["b"]
    ok = (rstar >= 0) & (rstar <= 4)
    axes[0].plot(pp[ok], rstar[ok], "k--", lw=2,
                 label="indifference (below: auth optimal)")
    axes[0].legend(loc="upper left", fontsize=8)
    fig.colorbar(im, ax=axes[0])
    # persona curves at r = 2
    personas = {
        "baseline":                 dict(),
        "loss-averse (lam=2.5)":    dict(lam=2.5),
        "bold explorer (temp=.6)":  dict(temp=0.6),
        "optimistic prior (q0=1.5)": dict(q0=1.5),
        "recency-driven (alpha=.5)": dict(alpha=0.5),
    }
    for k, (name, kw) in enumerate(personas.items()):
        y = [run_m0(p, seed=7 * k + 1, **kw).mean() for p in ps]
        axes[1].plot(ps, y, marker="o", ms=3, label=name)
    pstar = 1 - (DEF["a"] + DEF["c"]) / (DEF["b"] + DEF["r"])
    axes[1].axvline(pstar, color="k", ls="--", lw=1)
    axes[1].text(pstar + 0.01, 0.5, "auth optimal ->", fontsize=8)
    axes[1].set(title="M0: person types (r=2)", xlabel="peer receptivity p",
                ylabel="mask rate", ylim=(-0.02, 1.02))
    axes[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def fig_m1(out):
    ps = np.linspace(0.05, 0.95, 19)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    for lv, style in [(2, "-o"), (5, "-s"), (11, "-^")]:
        lock = [(run_m1(p, levels=lv, seed=int(p * 999)) < 0.2).mean()
                for p in ps]
        ax.plot(ps, lock, style, ms=4, label=f"{lv} disclosure levels")
    pstar = 1 - (DEF["a"] + DEF["c"]) / (DEF["b"] + DEF["r"])
    ax.axvline(pstar, color="k", ls="--", lw=1)
    ax.set(title="M1: P(mask-lock: final mean d < 0.2) vs action granularity",
           xlabel="peer receptivity p", ylabel="P(mask-lock)",
           ylim=(-0.02, 1.02))
    ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def fig_m2(out):
    ps = np.linspace(0.05, 0.95, 15)
    etas = np.linspace(0.0, 0.2, 13)
    Z = np.empty((len(etas), len(ps)))
    for i, eta in enumerate(etas):
        for j, p in enumerate(ps):
            Z[i, j] = run_m2(p, eta, seed=i * 53 + j).mean()
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    im = heat(ax, Z, ps, etas, "M2: mean mask rate with sticky stigma",
              "peer receptivity p", "stigma escape rate eta")
    fig.colorbar(im, ax=ax)
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def fig_m3(out):
    Ks = [1, 2, 4, 8, 16, 32]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for temp, style in [(0.15, "-o"), (0.4, "-s")]:
        opt, msk = [], []
        for K in Ks:
            o, m, _ = run_m3(K, temp=temp, seed=K)
            opt.append(o.mean())           # modal arm = authentic in good pond
            msk.append(m.mean())
        axes[0].plot(Ks, opt, style, label=f"temp={temp}")
        axes[1].plot(Ks, msk, style, label=f"temp={temp}")
    for ax, ttl, yl in [(axes[0], "M3: P(settle authentic in good pond)",
                         "probability"),
                        (axes[1], "M3: mean mask share", "mask share")]:
        ax.set(title=ttl, xlabel="number of peer groups K", ylabel=yl,
               xscale="log", ylim=(-0.02, 1.02))
        ax.set_xticks(Ks); ax.set_xticklabels(Ks); ax.legend()
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


# --------------------------------------- M4 endogenous peer receptivity

def run_m4(p0, km, ka=0.12, kr=0.04, p_min=0.05, p_max=0.95,
           b=1.0, a=0.6, c=0.25, r=2.0,
           n=300, T=2000, alpha=0.1, temp=0.25, lam=1.0, q0=0.0,
           seed=0, ntraj=0):
    """M0 payoffs, but receptivity p_t is per-child and endogenous:
      accepted authentic act : p += ka*(p_max - p)  (peers acclimate, resonance found)
      rejected authentic act : p -= kr*(p - p_min)  (reputation damage)
      masking                : p -= km*(p - p_min)  (entrenchment: the 'normal'
                               persona solidifies, later reveals land worse)
    Returns (final mask rate, final p, p-trajectories of first ntraj seeds)."""
    rng = np.random.default_rng(seed)
    Q = np.full((n, 2), float(q0))
    p = np.full(n, float(p0))
    idx = np.arange(n)
    win = T // 5
    mask_cnt = np.zeros(n)
    traj = np.empty((T, ntraj)) if ntraj else None
    for t in range(T):
        act = softmax_sample(Q, temp, rng)
        auth = act == 1
        accept = rng.random(n) < p
        rew = np.where(~auth, b - c, np.where(accept, b + a, a - r))
        Q[idx, act] += alpha * (loss_avert(rew, lam) - Q[idx, act])
        up = auth & accept
        dn = auth & ~accept
        p[up] += ka * (p_max - p[up])
        p[dn] -= kr * (p[dn] - p_min)
        p[~auth] -= km * (p[~auth] - p_min)
        if ntraj:
            traj[t] = p[:ntraj]
        if t >= T - win:
            mask_cnt += (~auth)
    return mask_cnt / win, p, traj

# ------------------------------------------------------- follow-up figures

def fig_m0_bistability(out, temp=0.10):
    """Same parameters, different fates: where do mask-lock and auth-lock
    basins coexist?  Bistability index = min(P(mask-lock), P(auth-lock))."""
    ps = np.linspace(0.05, 0.95, 19)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    # panel A: basin fractions along the r = 2 slice
    fr = []
    for p in ps:
        m = run_m0(p, n=600, temp=temp, seed=int(p * 1000) + 3)
        fr.append([(m > 0.8).mean(),
                   ((m >= 0.2) & (m <= 0.8)).mean(),
                   (m < 0.2).mean()])
    fr = np.array(fr).T
    axes[0].stackplot(ps, fr, labels=["mask-lock", "mixed", "auth-lock"],
                      colors=["#c0392b", "#f1c40f", "#2980b9"], alpha=0.85)
    pstar = 1 - (DEF["a"] + DEF["c"]) / (DEF["b"] + DEF["r"])
    axes[0].axvline(pstar, color="k", ls="--", lw=1.2)
    axes[0].text(pstar + 0.01, 0.05, "auth optimal ->", fontsize=8)
    axes[0].set(title=f"M0 basins of attraction (r=2, temp={temp})",
                xlabel="peer receptivity p", ylabel="fraction of children",
                xlim=(ps[0], ps[-1]), ylim=(0, 1))
    axes[0].legend(loc="center left", fontsize=8)
    # panel B: bistability index over (p, r)
    rs = np.linspace(0.0, 4.0, 17)
    Z = np.empty((len(rs), len(ps)))
    for i, r in enumerate(rs):
        for j, p in enumerate(ps):
            m = run_m0(p, r=r, temp=temp, seed=i * 211 + j)
            Z[i, j] = min((m > 0.8).mean(), (m < 0.2).mean())
    im = heat(axes[1], Z, ps, rs,
              "bistability index  min(P(mask-lock), P(auth-lock))",
              "peer receptivity p", "rejection penalty r", vmax=0.5)
    pp = np.linspace(0.05, 0.95, 200)
    rstar = (DEF["a"] + DEF["c"]) / (1 - pp) - DEF["b"]
    ok = (rstar >= 0) & (rstar <= 4)
    axes[1].plot(pp[ok], rstar[ok], "k--", lw=2)
    fig.colorbar(im, ax=axes[1])
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def fig_m3_bflpe(out, K=4):
    """Sweep the Big-Fish-Little-Pond comparison cost inside the good pond.
    Classify each child's modal final arm: authentic-in-good-pond,
    authentic-elsewhere, or masking (any group)."""
    bfs = np.linspace(0.0, 1.0, 11)
    cat = np.zeros((3, len(bfs)))
    for j, bf in enumerate(bfs):
        _, _, modal = run_m3(K, bf=bf, seed=17 + j)
        is_auth = (modal % 2) == 1
        cat[0, j] = (modal == 1).mean()              # authentic, good pond
        cat[1, j] = (is_auth & (modal != 1)).mean()  # authentic, elsewhere
        cat[2, j] = (~is_auth).mean()                # masking somewhere
    # analytic crossover: E[auth|good pond] = E[mask]
    p_g = 0.85
    bf_star = (p_g * (DEF["b"] + DEF["a"])
               + (1 - p_g) * (DEF["a"] - DEF["r"])
               - (DEF["b"] - DEF["c"])) / p_g
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    for row, lab, col in zip(cat,
                             ["authentic in good pond", "authentic elsewhere",
                              "masking"],
                             ["#2980b9", "#27ae60", "#c0392b"]):
        ax.plot(bfs, row, "-o", ms=4, color=col, label=lab)
    ax.axvline(bf_star, color="k", ls="--", lw=1.2)
    ax.text(bf_star + 0.02, 0.85, "mask becomes\nobjectively optimal ->",
            fontsize=8)
    ax.set(title=f"M3 + BFLPE (K={K}): modal final behavior vs comparison cost",
           xlabel="BFLPE comparison cost bf in good pond",
           ylabel="fraction of children", ylim=(-0.02, 1.02))
    ax.legend(fontsize=9)
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


def fig_m4(out):
    """Endogenous receptivity: outcome map over (initial p0, entrenchment km)
    plus example p-trajectories showing virtuous/vicious spirals."""
    p0s = np.linspace(0.1, 0.9, 15)
    kms = np.linspace(0.0, 0.003, 13)
    Z = np.empty((len(kms), len(p0s)))
    for i, km in enumerate(kms):
        for j, p0 in enumerate(p0s):
            mrate, _, _ = run_m4(p0, km, seed=i * 97 + j)
            Z[i, j] = mrate.mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    im = heat(axes[0], Z, p0s, kms,
              "M4: mean mask rate, endogenous receptivity",
              "initial receptivity p0", "entrenchment rate km")
    fig.colorbar(im, ax=axes[0])
    # trajectories at one bistable point
    p0, km, nt = 0.45, 0.001, 14
    mrate, _, traj = run_m4(p0, km, seed=42, ntraj=nt)
    for k in range(nt):
        col = "#c0392b" if mrate[k] > 0.5 else "#2980b9"
        axes[1].plot(traj[:, k], color=col, lw=1, alpha=0.8)
    axes[1].set(title=f"p-trajectories (p0={p0}, km={km}): "
                      "red=masker, blue=authentic",
                xlabel="time step", ylabel="peer receptivity p_t",
                ylim=(0, 1))
    fig.tight_layout(); fig.savefig(out, dpi=150); plt.close(fig)


if __name__ == "__main__":
    fig_m0("fig1_m0_phase.png");        print("fig1 done")
    fig_m1("fig2_m1_granularity.png");  print("fig2 done")
    fig_m2("fig3_m2_stigma.png");       print("fig3 done")
    fig_m3("fig4_m3_dimensionality.png"); print("fig4 done")
    fig_m0_bistability("fig5_m0_bistability.png"); print("fig5 done")
    fig_m3_bflpe("fig6_m3_bflpe.png");  print("fig6 done")
    fig_m4("fig7_m4_endogenous.png");   print("fig7 done")
