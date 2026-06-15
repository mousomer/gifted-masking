from __future__ import annotations

from pathlib import Path

import numpy as np

from gifted_masking.models import m0, m1, m2, m3, m4


def _load_pyplot():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "matplotlib is required for plotting. Install with: python -m pip install '.[plot]'"
        ) from exc
    return plt


def heat(ax, z_values, x_values, y_values, title, x_label, y_label, vmin=0.0, vmax=1.0):
    im = ax.pcolormesh(x_values, y_values, z_values, shading="auto", cmap="RdYlBu_r", vmin=vmin, vmax=vmax)
    ax.set(title=title, xlabel=x_label, ylabel=y_label)
    return im


def fig_m0(output_path: Path) -> None:
    plt = _load_pyplot()
    ps = np.linspace(0.05, 0.95, 19)
    rs = np.linspace(0.0, 4.0, 17)
    z_values = np.empty((len(rs), len(ps)))
    for i, r_value in enumerate(rs):
        for j, p_value in enumerate(ps):
            z_values[i, j] = m0.simulate(p_value, r=r_value, seed=i * 100 + j).mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    im = heat(axes[0], z_values, ps, rs, "M0: mean mask rate (final phase)", "peer receptivity p", "rejection penalty r")
    pp = np.linspace(0.05, 0.95, 200)
    rstar = m0.objective_indifference_r(pp)
    ok = (rstar >= 0) & (rstar <= 4)
    axes[0].plot(pp[ok], rstar[ok], "k--", lw=2, label="indifference (below: auth optimal)")
    axes[0].legend(loc="upper left", fontsize=8)
    fig.colorbar(im, ax=axes[0])
    personas = {
        "baseline": {},
        "loss-averse (lam=2.5)": {"lam": 2.5},
        "bold explorer (temp=.6)": {"temp": 0.6},
        "optimistic prior (q0=1.5)": {"q0": 1.5},
        "recency-driven (alpha=.5)": {"alpha": 0.5},
    }
    for index, (name, kwargs) in enumerate(personas.items()):
        series = [m0.simulate(p_value, seed=7 * index + 1, **kwargs).mean() for p_value in ps]
        axes[1].plot(ps, series, marker="o", ms=3, label=name)
    pstar = 1.0 - (0.6 + 0.25) / (1.0 + 2.0)
    axes[1].axvline(pstar, color="k", ls="--", lw=1)
    axes[1].text(pstar + 0.01, 0.5, "auth optimal ->", fontsize=8)
    axes[1].set(title="M0: person types (r=2)", xlabel="peer receptivity p", ylabel="mask rate", ylim=(-0.02, 1.02))
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m1(output_path: Path) -> None:
    plt = _load_pyplot()
    ps = np.linspace(0.05, 0.95, 19)
    fig, ax = plt.subplots(figsize=(6, 4.2))
    for levels, style in [(2, "-o"), (5, "-s"), (11, "-^")]:
        lock = [(m1.simulate(p_value, levels=levels, seed=int(p_value * 999)) < 0.2).mean() for p_value in ps]
        ax.plot(ps, lock, style, ms=4, label=f"{levels} disclosure levels")
    pstar = 1.0 - (0.6 + 0.25) / (1.0 + 2.0)
    ax.axvline(pstar, color="k", ls="--", lw=1)
    ax.set(title="M1: P(mask-lock: final mean d < 0.2) vs action granularity", xlabel="peer receptivity p", ylabel="P(mask-lock)", ylim=(-0.02, 1.02))
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m2(output_path: Path) -> None:
    plt = _load_pyplot()
    ps = np.linspace(0.05, 0.95, 15)
    etas = np.linspace(0.0, 0.2, 13)
    z_values = np.empty((len(etas), len(ps)))
    for i, eta in enumerate(etas):
        for j, p_value in enumerate(ps):
            z_values[i, j] = m2.simulate(p_value, eta, seed=i * 53 + j).mean()
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    im = heat(ax, z_values, ps, etas, "M2: mean mask rate with sticky stigma", "peer receptivity p", "stigma escape rate eta")
    fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m3(output_path: Path) -> None:
    plt = _load_pyplot()
    ks = [1, 2, 4, 8, 16, 32]
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    for temp, style in [(0.15, "-o"), (0.4, "-s")]:
        optimal, masking = [], []
        for k_groups in ks:
            settle, mask_rate, _ = m3.simulate(k_groups, temp=temp, seed=k_groups)
            optimal.append(settle.mean())
            masking.append(mask_rate.mean())
        axes[0].plot(ks, optimal, style, label=f"temp={temp}")
        axes[1].plot(ks, masking, style, label=f"temp={temp}")
    for ax, title, y_label in [
        (axes[0], "M3: P(settle authentic in good pond)", "probability"),
        (axes[1], "M3: mean mask share", "mask share"),
    ]:
        ax.set(title=title, xlabel="number of peer groups K", ylabel=y_label, xscale="log", ylim=(-0.02, 1.02))
        ax.set_xticks(ks)
        ax.set_xticklabels(ks)
        ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m0_bistability(output_path: Path, temp: float = 0.10) -> None:
    plt = _load_pyplot()
    ps = np.linspace(0.05, 0.95, 19)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    fractions = []
    for p_value in ps:
        mask_rate = m0.simulate(p_value, n=600, temp=temp, seed=int(p_value * 1000) + 3)
        fractions.append([(mask_rate > 0.8).mean(), ((mask_rate >= 0.2) & (mask_rate <= 0.8)).mean(), (mask_rate < 0.2).mean()])
    fractions = np.array(fractions).T
    axes[0].stackplot(ps, fractions, labels=["mask-lock", "mixed", "auth-lock"], colors=["#c0392b", "#f1c40f", "#2980b9"], alpha=0.85)
    pstar = 1.0 - (0.6 + 0.25) / (1.0 + 2.0)
    axes[0].axvline(pstar, color="k", ls="--", lw=1.2)
    axes[0].text(pstar + 0.01, 0.05, "auth optimal ->", fontsize=8)
    axes[0].set(title=f"M0 basins of attraction (r=2, temp={temp})", xlabel="peer receptivity p", ylabel="fraction of children", xlim=(ps[0], ps[-1]), ylim=(0, 1))
    axes[0].legend(loc="center left", fontsize=8)
    rs = np.linspace(0.0, 4.0, 17)
    z_values = np.empty((len(rs), len(ps)))
    for i, r_value in enumerate(rs):
        for j, p_value in enumerate(ps):
            mask_rate = m0.simulate(p_value, r=r_value, temp=temp, seed=i * 211 + j)
            z_values[i, j] = min((mask_rate > 0.8).mean(), (mask_rate < 0.2).mean())
    im = heat(axes[1], z_values, ps, rs, "bistability index  min(P(mask-lock), P(auth-lock))", "peer receptivity p", "rejection penalty r", vmax=0.5)
    pp = np.linspace(0.05, 0.95, 200)
    rstar = m0.objective_indifference_r(pp)
    ok = (rstar >= 0) & (rstar <= 4)
    axes[1].plot(pp[ok], rstar[ok], "k--", lw=2)
    fig.colorbar(im, ax=axes[1])
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m3_bflpe(output_path: Path, k_groups: int = 4) -> None:
    plt = _load_pyplot()
    bfs = np.linspace(0.0, 1.0, 11)
    categories = np.zeros((3, len(bfs)))
    for index, bf in enumerate(bfs):
        _, _, modal = m3.simulate(k_groups, bf=bf, seed=17 + index)
        authentic = (modal % 2) == 1
        categories[0, index] = (modal == 1).mean()
        categories[1, index] = (authentic & (modal != 1)).mean()
        categories[2, index] = (~authentic).mean()
    p_good = 0.85
    bf_star = (p_good * (1.0 + 0.6) + (1.0 - p_good) * (0.6 - 2.0) - (1.0 - 0.25)) / p_good
    fig, ax = plt.subplots(figsize=(6.5, 4.4))
    for row, label, color in zip(categories, ["authentic in good pond", "authentic elsewhere", "masking"], ["#2980b9", "#27ae60", "#c0392b"]):
        ax.plot(bfs, row, "-o", ms=4, color=color, label=label)
    ax.axvline(bf_star, color="k", ls="--", lw=1.2)
    ax.text(bf_star + 0.02, 0.85, "mask becomes\nobjectively optimal ->", fontsize=8)
    ax.set(title=f"M3 + BFLPE (K={k_groups}): modal final behavior vs comparison cost", xlabel="BFLPE comparison cost bf in good pond", ylabel="fraction of children", ylim=(-0.02, 1.02))
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m4(output_path: Path) -> None:
    plt = _load_pyplot()
    p0s = np.linspace(0.1, 0.9, 15)
    kms = np.linspace(0.0, 0.003, 13)
    z_values = np.empty((len(kms), len(p0s)))
    for i, km in enumerate(kms):
        for j, p0 in enumerate(p0s):
            mask_rate, _, _ = m4.simulate(p0, km, seed=i * 97 + j)
            z_values[i, j] = mask_rate.mean()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    im = heat(axes[0], z_values, p0s, kms, "M4: mean mask rate, endogenous receptivity", "initial receptivity p0", "entrenchment rate km")
    fig.colorbar(im, ax=axes[0])
    p0, km, ntraj = 0.45, 0.001, 14
    mask_rate, _, trajectories = m4.simulate(p0, km, seed=42, ntraj=ntraj)
    for index in range(ntraj):
        color = "#c0392b" if mask_rate[index] > 0.5 else "#2980b9"
        axes[1].plot(trajectories[:, index], color=color, lw=1, alpha=0.8)
    axes[1].set(title=f"p-trajectories (p0={p0}, km={km}): red=masker, blue=authentic", xlabel="time step", ylabel="peer receptivity p_t", ylim=(0, 1))
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def fig_m0_by_risk(output_path: Path) -> None:
    plt = _load_pyplot()
    ps = np.linspace(0.05, 0.95, 19)
    rs = np.linspace(0.0, 4.0, 17)
    pp = np.linspace(0.05, 0.95, 300)
    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.4))
    for ax, (name, lam) in zip(axes, [("risk-averse (lam=2.5)", 2.5), ("risk-taking (lam=0.5)", 0.5)]):
        z_values = np.empty((len(rs), len(ps)))
        for i, r_value in enumerate(rs):
            for j, p_value in enumerate(ps):
                z_values[i, j] = m0.simulate(p_value, r=r_value, lam=lam, seed=i * 100 + j).mean()
        im = heat(ax, z_values, ps, rs, f"M0 mask rate: {name}", "peer receptivity p", "rejection penalty r")
        objective = m0.objective_indifference_r(pp)
        ok = (objective >= 0) & (objective <= 4)
        ax.plot(pp[ok], objective[ok], "k--", lw=2, label="objective indifference")
        subjective = m0.subjective_indifference_r(pp, lam)
        ok = (subjective >= 0) & (subjective <= 4)
        ax.plot(pp[ok], subjective[ok], "w-", lw=2, label="subjective indifference")
        ax.legend(loc="upper left", fontsize=8)
        ax.set_ylim(0, 4)
    fig.colorbar(im, ax=axes, fraction=0.025)
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def fig_downstream_by_risk(output_path: Path) -> None:
    plt = _load_pyplot()
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    ks = [1, 2, 4, 8, 16, 32]
    risk_types = {
        "risk-averse (lam=2.5)": 2.5,
        "risk-neutral (lam=1.0)": 1.0,
        "risk-taking (lam=0.5)": 0.5,
    }
    for name, lam in risk_types.items():
        series = [m3.simulate(k_groups, lam=lam, seed=k_groups + int(lam * 10))[0].mean() for k_groups in ks]
        axes[0].plot(ks, series, "-o", ms=4, label=name)
    axes[0].set(title="M3: P(settle authentic in good pond)", xlabel="number of peer groups K", ylabel="probability", xscale="log", ylim=(-0.02, 1.02))
    axes[0].set_xticks(ks)
    axes[0].set_xticklabels(ks)
    axes[0].legend(fontsize=8)
    p0s = np.linspace(0.1, 0.9, 15)
    for name, lam in risk_types.items():
        series = [(m4.simulate(p0, 0.001, lam=lam, seed=int(p0 * 100))[0] < 0.2).mean() for p0 in p0s]
        axes[1].plot(p0s, series, "-o", ms=4, label=name)
    axes[1].set(title="M4 (km=0.001): P(authentic attractor reached)", xlabel="initial receptivity p0", ylabel="P(auth-lock)", ylim=(-0.02, 1.02))
    axes[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(output_path, dpi=150)
    plt.close(fig)


def generate_all(output_dir: Path) -> list[str]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    figures = [
        ("fig1_m0_phase.png", fig_m0),
        ("fig2_m1_granularity.png", fig_m1),
        ("fig3_m2_stigma.png", fig_m2),
        ("fig4_m3_dimensionality.png", fig_m3),
        ("fig5_m0_bistability.png", fig_m0_bistability),
        ("fig6_m3_bflpe.png", fig_m3_bflpe),
        ("fig7_m4_endogenous.png", fig_m4),
        ("fig8_m0_by_risk.png", fig_m0_by_risk),
        ("fig9_downstream_by_risk.png", fig_downstream_by_risk),
    ]
    generated = []
    for file_name, func in figures:
        path = output_dir / file_name
        func(path)
        generated.append(str(path))
    return generated
