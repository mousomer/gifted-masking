"""Six revised scientific figures, assembled only from frozen archived evidence.

No experiment modules, random draws, estimator fitting, or bootstrap refitting.
Edit visible wording in figure_text.py. Run without arguments to rebuild all
six canonical figures, or use --preview-dir PATH for isolated text previews.
Use --list to see the figure registry without reading data or writing files.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from string import Formatter
import tempfile

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

if __package__:
    from .figure_text import FIGURE_TEXT, SHARED_TEXT
else:
    from figure_text import FIGURE_TEXT, SHARED_TEXT

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
TEXT_SOURCE = HERE / "figure_text.py"
CANONICAL_OUT = HERE / "figures"
CANONICAL_PDF_OUT = ROOT / "output" / "pdf" / "revision_20260929"
OUT = CANONICAL_OUT
PDF_OUT = CANONICAL_PDF_OUT
PUB = "projects/frontiers_article/publication_v1/data/"
SUMMARY = "results/summaries/"
HASHES = {
    PUB+"e01_lambda_response.csv": "df70c4f9b15d4c90b16fe1cff1d99a451464331ee1b01d3489c3b7442e3d8ae3",
    PUB+"e01_primary_effects.csv": "9b9227f43146b96ae7000f572d2249ae6bd4d39bf414715bdd780203afa38d36",
    PUB+"e01_intervention_effects.csv": "12a1f4befa1ade1a9065a3782fc40a20d9bbed2f91d31a1d3d4dd5771d55a42b",
    PUB+"e02_primary_effects.csv": "fe37531296d986f0662ce74d6e3976680163e4f19da7240deef5f8e5d97f966f",
    PUB+"e02_arm_expected_rewards.csv": "e58f0603e27a34ab7b94309f8576e96c67c4e8dc4c25e02b7312aed48c021fb9",
    PUB+"e03_objective_thresholds.csv": "a43d066f98987a7fd0e326c70929fe442b70134b1ee7ba1b8dbee779cfb91ce5",
    PUB+"e05_response_vs_bf.csv": "0d47aeae4dc4c15e08176c7ff44466740712f3a47000a68d2b7a1231d48a7e10",
    PUB+"e05_crossings.csv": "866697afb0cdd66f6e6d008cc6b06e52786d1e27f7ba3f71601a56512349076b",
    SUMMARY+"frontiers_m2_regime_replication_v1_cells.csv": "198cb7be9b2a93aa89569d9dd656326f521b7a2ec99543733fd6e779e0508851",
    SUMMARY+"frontiers_m3_search_architectures_v1_curves.csv": "33f245b36ba6d78489cd9b88948d07d4d3aaf58ef7f8395b4394431df2dd39b4",
    SUMMARY+"frontiers_m3_bflpe_crossover_v1_cells.csv": "59d780f3feb3ed03e665de0a75eabd8975fb394d58cbd9c2193a03bb68d73ab7",
}
NAVY, RED, TEAL, GREY = "#245077", "#ac433c", "#287769", "#60666e"
COLORS = {"flat_2k": NAVY, "hierarchical": RED, "global_mask": TEAL}
LABELS = SHARED_TEXT["architectures"]
MARKERS = {"flat_2k": "o", "hierarchical": "s", "global_mask": "^"}
def new_provenance(mode="canonical", selected_figures=None):
    """Return fresh per-render bookkeeping; never carry prior output hashes."""
    return {
        "revision": "20260929", "method": "Deterministic display of archived data and exact algebra; no simulations or refitting",
        "inputs": dict(HASHES), "panels": {}, "outputs": {},
        "uncertainty": "Imported archived confidence intervals only. Master minima/maxima, where displayed, are descriptive ranges, not confidence intervals.",
        "mode": mode, "selected_figures": list(selected_figures or range(1,7)),
    }


PROVENANCE = new_provenance()


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(name):
    with (ROOT / name).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def record(panel, source, selector, values, note=""):
    PROVENANCE["panels"][panel] = {"source": source, "selector": selector, "values": values, "note": note}


def style():
    plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9,
        "axes.titlesize": 10, "axes.titleweight": "bold", "axes.titlelocation": "left",
        "axes.labelsize": 9, "xtick.labelsize": 8, "ytick.labelsize": 8,
        "legend.fontsize": 8, "legend.frameon": False, "axes.spines.top": False,
        "axes.spines.right": False, "axes.linewidth": .7, "lines.linewidth": 1.6,
        "pdf.fonttype": 42, "savefig.dpi": 240, "figure.dpi": 130})


def title(ax, letter, text):
    ax.set_title(SHARED_TEXT["panel_title_format"].format(letter=letter, text=text), pad=12)


def save(fig, stem):
    OUT.mkdir(parents=True,exist_ok=True)
    PDF_OUT.mkdir(parents=True,exist_ok=True)
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    bounds = fig.bbox
    clipped = []
    # AutoLocator may retain off-axis tick artists that are never drawn; check
    # authored text, titles, and axis labels without those false positives.
    authored = list(fig.texts)
    for ax in fig.axes:
        authored.extend([*ax.texts, ax.title, ax._left_title, ax._right_title,
                         ax.xaxis.label, ax.yaxis.label])
    for artist in authored:
        if artist.get_visible() and artist.get_text().strip():
            box = artist.get_window_extent(renderer=renderer)
            if box.x0 < -1 or box.y0 < -1 or box.x1 > bounds.width+1 or box.y1 > bounds.height+1:
                clipped.append(artist.get_text())
    assert not clipped, f"Text exceeds figure canvas in {stem}: {clipped}"
    for ext in ("png", "pdf"):
        path = (PDF_OUT if ext == "pdf" else OUT) / f"{stem}.{ext}"
        metadata = {"CreationDate": None, "ModDate": None, "Creator": "Frozen-evidence scientific revision"} if ext == "pdf" else {"Software": "Frozen-evidence scientific revision"}
        fig.savefig(path, metadata=metadata, facecolor="white")
        output_key = str(path.relative_to(ROOT)) if PROVENANCE["mode"] == "canonical" else str(path)
        PROVENANCE["outputs"][output_key] = sha(path)
    plt.close(fig)


def forest(ax, entries, xlabel, xlim=None):
    ax.axvline(0, color=GREY, lw=.8, ls="--")
    for i, (label, est, lo, hi, color) in enumerate(entries):
        y = len(entries)-1-i
        ax.plot([lo, hi], [y,y], color=color, lw=2)
        ax.plot(est, y, "o", color=color, ms=6)
    ax.set_yticks(range(len(entries)), [e[0] for e in entries[::-1]])
    ax.tick_params(axis="y", length=0)
    ax.set_ylim(-.55,len(entries)-.4)
    ax.set_xlabel(xlabel)
    if xlim: ax.set_xlim(*xlim)


def fig1():
    """Draw the mechanism/opportunity-use diagram; edit FIGURE_TEXT[1]."""
    t = FIGURE_TEXT[1]
    fig, ax = plt.subplots(figsize=(8.5,5.3))
    ax.axis("off"); ax.set_xlim(0,1); ax.set_ylim(0,1)
    def box(x,y,w,h,text,fill="#f1f5f8",edge=NAVY):
        ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=.012,rounding_size=.012",fc=fill,ec=edge,lw=1))
        ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=9)
    def arrow(start,end,color=GREY):
        ax.add_patch(FancyArrowPatch(start,end,arrowstyle="-|>",mutation_scale=12,lw=1,color=color))
    ax.text(.02,.97,t["A"]["heading"],weight="bold",fontsize=11,va="top")
    boxes=[(.02,.74,.27,t["A"]["valuation_box"]),(.365,.74,.27,t["A"]["action_box"]),(.71,.74,.27,t["A"]["social_box"])]
    for x,y,w,box_text in boxes: box(x,y,w,.12,box_text); arrow((x+w/2,y),(.5,.62))
    box(.22,.47,.56,.14,t["A"]["allocation_box"],fill="#e1edf4")
    ax.text(.5,.405,t["A"]["crossing_note"],ha="center",fontsize=9,color=NAVY)
    ax.text(.02,.335,t["B"]["heading"],weight="bold",fontsize=11)
    for x,box_text in [(.02,t["B"]["available_box"]),(.37,t["B"]["encountered_box"]),(.72,t["B"]["used_box"])]:
        box(x,.145,.26,.13,box_text,fill="#edf4f0",edge=TEAL)
    arrow((.28,.21),(.355,.21),TEAL); arrow((.63,.21),(.705,.21),TEAL)
    ax.text(.5,.055,t["B"]["footer"],ha="center",fontsize=9)
    fig.subplots_adjust(left=.04,right=.96,bottom=.03,top=.98)
    record("1A-1B",[],"conceptual synthesis C01-C23",[],"No quantitative values; arrows organize model mechanisms, not estimated causal effects in children.")
    save(fig,FIGURES[1][1])


def fig2():
    """Plot E01 weighting, history and information; edit FIGURE_TEXT[2]."""
    t = FIGURE_TEXT[2]
    lam = rows(PUB+"e01_lambda_response.csv")
    levels = [r for r in lam if r["lambda"] in ("0.5","2.5")]
    primary = {r["claim_id"]:r for r in rows(PUB+"e01_primary_effects.csv")}
    info = {r["claim_id"]:r for r in rows(PUB+"e01_intervention_effects.csv")}
    fig, axes=plt.subplots(2,2,figsize=(8.5,6.8))
    a,b,c,d=axes.flat
    vals=[100*float(r["mean_final_window_mask_rate"]) for r in levels]
    assert np.allclose(vals,[58.8935,99.1925])
    a.bar([0,1],vals,color=[NAVY,RED],width=.52)
    for i,v in enumerate(vals):a.text(i,v+2,t["A"]["bar_format"].format(value=v),ha="center",fontsize=9)
    a.set_xticks([0,1],t["A"]["ticks"]);a.set_ylim(0,112)
    a.set_ylabel(SHARED_TEXT["final_window_masking_percent"]); title(a,"A",t["A"]["title"])
    a.text(.04,.91,t["A"]["effect_note"],transform=a.transAxes,fontsize=8,color=GREY)
    ls=np.linspace(.5,2.5,101); threshold=(.75+1.4*ls)/(1.6+1.4*ls)
    b.plot(ls,threshold,color=RED,label=t["B"]["transformed_legend"])
    b.axhline(43/60,color=GREY,ls="--",label=t["B"]["objective_legend"])
    b.scatter([.5,2.5],[threshold[0],threshold[-1]],color=RED,zorder=3)
    b.set(xlabel=t["B"]["xlabel"],ylabel=t["B"]["ylabel"],ylim=(.6,.87))
    b.legend(loc="lower right",fontsize=7);title(b,"B",t["B"]["title"])
    entries=[]
    for key,label,col in [("E01-C2-SAMPLING",t["C"]["sampling_outcome"],NAVY),("E01-C2-FINAL-MASK",t["C"]["masking_outcome"],GREY)]:
        r=primary[key];entries.append((label,*[100*float(r[k]) for k in ("estimate","ci_low","ci_high")],col))
    forest(c,entries,t["C"]["xlabel"],(-4.2,1.6));title(c,"C",t["C"]["title"])
    entries2=[]
    for key,label,col in [("E01-C2-FORCED-MASK",t["D"]["forced_outcome"],NAVY),("E01-C2-CF-MASK",t["D"]["counterfactual_outcome"],RED)]:
        r=info[key];entries2.append((label,*[100*float(r[k]) for k in ("estimate","ci_low","ci_high")],col))
    forest(d,entries2,t["D"]["xlabel"],(0,14));title(d,"D",t["D"]["title"])
    fig.subplots_adjust(left=.20,right=.97,top=.87,bottom=.12,hspace=.68,wspace=.90)
    record("2A",PUB+"e01_lambda_response.csv","lambda in {0.5,2.5}; p=.65; equal-weight means of five masters",levels)
    record("2B",PUB+"e01_lambda_response.csv","reference payoff algebra",{"lambda":ls.tolist(),"threshold":threshold.tolist(),"objective":43/60},"Exact formula (.75+1.4*lambda)/(1.6+1.4*lambda).")
    record("2C",PUB+"e01_primary_effects.csv","claim_id E01-C2-SAMPLING and E01-C2-FINAL-MASK",entries)
    record("2D",PUB+"e01_intervention_effects.csv","claim_id E01-C2-FORCED-MASK and E01-C2-CF-MASK",entries2)
    save(fig,FIGURES[2][1])


def fig3():
    """Plot E02 expected reward, variance and effects; edit FIGURE_TEXT[3]."""
    t = FIGURE_TEXT[3]
    rewards=rows(PUB+"e02_arm_expected_rewards.csv")
    effects={r["claim_id"]:r for r in rows(PUB+"e02_primary_effects.csv")}
    fig=plt.figure(figsize=(8.5,6.7));gs=fig.add_gridspec(2,2,height_ratios=[1,1.18])
    a=fig.add_subplot(gs[0,0]);b=fig.add_subplot(gs[0,1]);c=fig.add_subplot(gs[1,:])
    variance=[]
    for p,col,marker in [(.75,NAVY,"o"),(.85,TEAL,"s")]:
        selected=sorted([r for r in rewards if float(r["p"])==p],key=lambda r:float(r["d"]))
        ds=np.array([float(r["d"]) for r in selected]); ev=np.array([float(r["expected_reward"]) for r in selected])
        a.plot(ds,ev,marker=marker,color=col,label=t["shared"]["receptivity_legend_format"].format(p=p))
        var=9*(1-p)*ds*(1-(1-p)*ds)
        b.plot(ds,var,marker=marker,color=col,label=t["shared"]["receptivity_legend_format"].format(p=p))
        variance.append({"p":p,"d":ds.tolist(),"variance":var.tolist()})
    for ax in (a,b):ax.set_xlabel(t["shared"]["xlabel"]);ax.set_xticks([0,.25,.5,.75,1]);ax.legend(loc="upper left")
    a.set_ylabel(t["A"]["ylabel"]);title(a,"A",t["A"]["title"])
    b.set_ylabel(t["B"]["ylabel"]);title(b,"B",t["B"]["title"])
    entries=[]
    for key,label,col in [("E02-C4-EXPLORATION",t["C"]["engagement_outcome"],TEAL),("E02-C4-FULL-ENDPOINT",t["C"]["endpoint_outcome"],RED),("E02-C4-MODAL",t["C"]["modal_outcome"],NAVY),("E02-C4-REGRET",t["C"]["intensity_outcome"],GREY)]:
        r=effects[key];entries.append((label,*[100*float(r[k]) for k in ("estimate","ci_low","ci_high")],col))
    forest(c,entries,t["C"]["xlabel"],(-40,31))
    title(c,"C",t["C"]["title"])
    fig.subplots_adjust(left=.34,right=.97,bottom=.10,top=.93,hspace=.65,wspace=.55)
    # Top panels use the full width; the forest reserves room for outcome labels.
    a.set_position([.11,.61,.36,.30]);b.set_position([.61,.61,.36,.30])
    record("3A",PUB+"e02_arm_expected_rewards.csv","p in {.75,.85}; all five disclosure levels",rewards)
    record("3B",PUB+"e02_arm_expected_rewards.csv","exact reward variance at plotted disclosure levels",variance,"Var(R)=9(1-p)d[1-(1-p)d]; does not establish a learner variance preference.")
    record("3C",PUB+"e02_primary_effects.csv","all four claims, with REGRET re-expressed as mean-disclosure difference",entries,"Archived REGRET is binary-minus-graded normalized regret, exactly graded-minus-binary mean disclosure. Units multiply the unit-scale quantities by 100; time windows differ by outcome.")
    save(fig,FIGURES[3][1])


def fig4():
    """Plot E03 dynamic boundaries and long-horizon sentinels; edit FIGURE_TEXT[4]."""
    t = FIGURE_TEXT[4]
    source=SUMMARY+"frontiers_m2_regime_replication_v1_cells.csv"
    table=rows(source);th=rows(PUB+"e03_objective_thresholds.csv")
    sentinels=[(.4,0),(.55,0),(.75,0),(.55,.2),(.9,.2)]
    detail=[]
    for p,eta in sentinels:
        selected=[r for r in table if r["component"]=="sentinels" and r["sensitivity_name"]=="T" and r["T"]=="5000" and float(r["p"])==p and float(r["eta"])==eta]
        assert len(selected)==5 and all(r["classification"]=="learned_suboptimal_masking" for r in selected)
        values=[100*float(r["neutral_mask_probability"]) for r in selected]
        detail.append({"p":p,"eta":eta,"master_values":values,"mean":float(np.mean(values))})
    assert np.allclose([r["mean"] for r in detail],[99.67,98.22,95.42,97.12,89.97],atol=.01)
    fig,(a,b)=plt.subplots(1,2,figsize=(8.5,4.25),gridspec_kw={"width_ratios":[1,1.25]})
    labels=[t["A"]["static_tick"]]+[t["A"]["dynamic_tick_format"].format(eta=float(r['eta'])) for r in th]
    values=[43/60]+[float(r["midpoint_p"]) for r in th]
    ys=np.arange(4)[::-1]
    a.barh(ys,values,color=[GREY,NAVY,NAVY,NAVY],height=.55)
    for y,v in zip(ys,values):a.text(v+.012,y,t["A"]["bar_format"].format(value=v),va="center",fontsize=9)
    a.set_yticks(ys,labels);a.set_xlim(0,.85);a.set_xlabel(t["A"]["xlabel"])
    title(a,"A",t["A"]["title"])
    means=[r["mean"] for r in detail];x=np.arange(5)
    b.bar(x,means,color=RED,width=.6,alpha=.85)
    for i,r in enumerate(detail):
        b.scatter([i]*5,r["master_values"],color="#3d2020",s=14,zorder=3)
        b.text(i,r["mean"]+3.5,t["B"]["bar_format"].format(value=r['mean']),ha="center",fontsize=8)
    b.set_xticks(x,[t["B"]["sentinel_tick_format"].format(p=p,eta=eta) for p,eta in sentinels]);b.set_ylim(0,114)
    b.set_xlabel(t["B"]["xlabel"]);b.set_ylabel(t["B"]["ylabel"])
    title(b,"B",t["B"]["title"])
    b.text(.03,.13,t["B"]["optimality_note"],transform=b.transAxes,fontsize=9,color="white",bbox={"fc":RED,"ec":"none","pad":3})
    fig.subplots_adjust(left=.20,right=.97,bottom=.20,top=.86,wspace=.55)
    record("4A",PUB+"e03_objective_thresholds.csv","all three bracketed thresholds plus exact static boundary",th,"Bars use midpoint; numerical brackets have width 0.00006103515625, not statistical confidence intervals.")
    record("4B",source,"component=sentinels;sensitivity_name=T;T=5000;five listed (p,eta) pairs;five masters each",detail,"Bars equal-weight master means; dots show individual archived master values.")
    save(fig,FIGURES[4][1])


def fig5():
    """Plot E04 context-search outcomes and abundance; edit FIGURE_TEXT[5]."""
    t = FIGURE_TEXT[5]
    labels = SHARED_TEXT["architectures"]
    source=SUMMARY+"frontiers_m3_search_architectures_v1_curves.csv";data=rows(source);ks=[1,2,4,8,16]
    metrics=["mean_final_window_mask_rate","mean_settled_any_good_auth_argmax","mean_ever_accepted_good_auth","mean_expected_static_regret","mean_time_to_first_accepted_good_auth_capped"]
    combined={}
    for arch in COLORS:
        combined[arch]={}
        for k in ks:
            sel=[r for r in data if r["architecture"]==arch and r["canonical_identity_mode"]=="fixed" and int(r["effective_good_count"])==1 and int(r["K"])==k]
            assert len(sel)==5
            combined[arch][k]={m:float(np.mean([float(r[m]) for r in sel])) for m in metrics}
    assert np.isclose(combined["flat_2k"][16][metrics[0]],.841906)
    assert np.isclose(combined["hierarchical"][16][metrics[2]],.9964)
    fig,axes=plt.subplots(3,2,figsize=(9,10.3));a,b,c,d,e,f=axes.flat
    for ax,metric,scale in [(a,metrics[0],100),(b,metrics[1],100),(e,metrics[3],1),(f,metrics[4],1)]:
        for arch,col in COLORS.items():
            ax.plot(ks,[scale*combined[arch][k][metric] for k in ks],marker=MARKERS[arch],color=col,label=labels[arch])
        ax.set_xscale("log",base=2);ax.set_xticks(ks,[t["shared"]["context_tick_format"].format(k=k) for k in ks]);ax.set_xlabel(t["shared"]["xlabel"])
    a.set_ylabel(SHARED_TEXT["final_window_masking_percent"]);a.set_ylim(0,105);title(a,"A",t["A"]["title"])
    b.set_ylabel(SHARED_TEXT["good_authentic_modal_percent"]);b.set_ylim(0,105);title(b,"B",t["B"]["title"])
    a.legend(loc="upper left",fontsize=8)
    x=np.arange(2);w=.33
    for offset,metric,label,col in [(-w/2,metrics[2],t["C"]["encounter_legend"],TEAL),(w/2,metrics[0],t["C"]["masking_legend"],RED)]:
        vals=[100*combined[arch][16][metric] for arch in ("flat_2k","hierarchical")]
        c.bar(x+offset,vals,w,label=label,color=col)
        for xx,v in zip(x+offset,vals):c.text(xx,v+1.5,t["shared"]["bar_format"].format(value=v),ha="center",fontsize=8)
    c.set_xticks(x,[labels["flat_2k"],labels["hierarchical"]]);c.set_ylim(0,133);c.set_yticks(range(0,101,20));c.set_ylabel(t["C"]["ylabel"])
    c.legend(loc="upper left",fontsize=7.5);title(c,"C",t["C"]["title"])
    abundance=[]
    for offset,count,col in [(-w/2,1,GREY),(w/2,4,TEAL)]:
        vals=[]
        for arch in ("flat_2k","hierarchical"):
            sel=[r for r in data if r["architecture"]==arch and r["canonical_identity_mode"]=="fixed" and int(r["effective_good_count"])==count and int(r["K"])==16]
            assert len(sel)==5
            mean=100*float(np.mean([float(r[metrics[1]]) for r in sel]));vals.append(mean)
            abundance.append({"architecture":arch,"K":16,"good_count":count,"modal_percent":mean})
        legend_key = "one_context_legend_format" if count == 1 else "many_contexts_legend_format"
        d.bar(x+offset,vals,w,label=t["D"][legend_key].format(count=count),color=col)
        for xx,v in zip(x+offset,vals):d.text(xx,v+1.5,t["shared"]["bar_format"].format(value=v),ha="center",fontsize=8)
    d.set_xticks(x,[labels["flat_2k"],labels["hierarchical"]]);d.set_ylim(0,133);d.set_yticks(range(0,101,20));d.set_ylabel(SHARED_TEXT["good_authentic_modal_percent"])
    d.legend(loc="upper left",fontsize=7.5);title(d,"D",t["D"]["title"])
    e.set_ylabel(t["E"]["ylabel"]);title(e,"E",t["E"]["title"])
    f.set_ylabel(t["F"]["ylabel"]);title(f,"F",t["F"]["title"])
    fig.subplots_adjust(left=.12,right=.97,bottom=.07,top=.95,wspace=.36,hspace=.63)
    record("5A-5C,5E-5F",source,"canonical_identity_mode=fixed;effective_good_count=1;K in {1,2,4,8,16};flat_2k,hierarchical,global_mask;five masters per cell",combined,"Equal-weight descriptive master means; connected lines guide the eye and do not imply intermediate K values. First success is zero-based and capped at T=2000 for non-events.")
    record("5D",source,"canonical_identity_mode=fixed;K=16;effective_good_count in {1,4};flat_2k,hierarchical;five masters per cell",abundance)
    save(fig,FIGURES[5][1])


def fig6():
    """Plot E05 archived crossings and actual action use; edit FIGURE_TEXT[6]."""
    t = FIGURE_TEXT[6]
    labels = SHARED_TEXT["architectures"]
    response=rows(PUB+"e05_response_vs_bf.csv");cross=rows(PUB+"e05_crossings.csv")
    flat=next(r for r in cross if r["architecture"]=="flat_2k")
    learned,lo,hi,obj=[float(flat[k]) for k in ("transition_bf","ci_low","ci_high","analytic_threshold_bf")]
    assert np.isclose(learned,.31285211267605634)
    source=SUMMARY+"frontiers_m3_bflpe_crossover_v1_cells.csv";cells=rows(source)
    vals=[]
    for bf in [0,.30,.325,obj]:
        sel=[r for r in cells if r["architecture"]=="flat_2k" and abs(float(r["bf"])-bf)<1e-12]
        assert len(sel)==5
        vals.append({"bf":bf,"mask":100*float(np.mean([float(r["mean_final_window_mask_rate"]) for r in sel])),"modal":100*float(np.mean([float(r["modal_good_auth_argmax_fraction"]) for r in sel]))})
    assert np.allclose([v["mask"] for v in vals],[58.8217,77.6073,78.9508,85.2005])
    fig,(a,b)=plt.subplots(1,2,figsize=(8.5,4.4),gridspec_kw={"width_ratios":[1.15,1]})
    for arch,col,marker in [("flat_2k",NAVY,"o"),("hierarchical",RED,"s")]:
        sel=sorted([r for r in response if r["architecture"]==arch and r["in_dense_range"]=="True"],key=lambda r:float(r["bf"]))
        a.plot([float(r["bf"]) for r in sel],[float(r["pooled_response"]) for r in sel],marker=marker,ms=4,color=col,label=labels[arch])
    a.axhline(.5,color=GREY,ls=":",lw=1);a.axvspan(learned,obj,color=NAVY,alpha=.07)
    a.axvspan(lo,hi,color=NAVY,alpha=.20);a.axvline(learned,color=NAVY,lw=1);a.axvline(obj,color=GREY,ls="--")
    a.text(.345,.92,t["A"]["crossing_note_format"].format(learned=learned,lo=lo,hi=hi),fontsize=8,color=NAVY,va="top",bbox={"facecolor":"white","edgecolor":"none","pad":2})
    a.text(obj+.005,.65,t["A"]["objective_note"],fontsize=8,color=GREY)
    a.text(.64,.13,t["A"]["hierarchical_note"],ha="right",fontsize=7.5,color=RED)
    a.set(xlim=(.29,.66),ylim=(-.025,1),xlabel=SHARED_TEXT["comparison_cost"],ylabel=t["A"]["ylabel"])
    a.legend(loc="upper right",fontsize=7.5);title(a,"A",t["A"]["title"])
    x=np.arange(4);w=.34
    for offset,key,label,col in [(-w/2,"mask",t["B"]["masking_legend"],RED),(w/2,"modal",t["B"]["modal_legend"],NAVY)]:
        values=[r[key] for r in vals];b.bar(x+offset,values,w,color=col,label=label)
        for xx,v in zip(x+offset,values):b.text(xx,v+1.5,t["B"]["bar_format"].format(value=v),ha="center",fontsize=7.5)
    b.set_xticks(x,t["B"]["ticks"]);b.set_ylim(0,120);b.set_yticks(range(0,101,20))
    b.set_ylabel(t["B"]["ylabel"]);b.set_xlabel(SHARED_TEXT["comparison_cost"]);b.legend(loc="upper right",fontsize=7.5)
    title(b,"B",t["B"]["title"])
    fig.subplots_adjust(left=.10,right=.98,bottom=.22,top=.86,wspace=.38)
    record("6A",[PUB+"e05_response_vs_bf.csv",PUB+"e05_crossings.csv"],"dense-range archived pooled responses by architecture; frozen crossing and CI",{"crossings":cross,"response":[r for r in response if r["in_dense_range"]=="True"]},"No isotonic refit or bootstrap. Lines connect observed pooled points only; shaded strip is the archived crossing CI.")
    record("6B",source,"architecture=flat_2k;bf in {0,.30,.325,8/17};five masters per cell",vals,"Descriptive master means; masking has action denominator, modal classification has learner denominator.")
    save(fig,FIGURES[6][1])


FIGURES = {
    1: (fig1, "Figure_1_mechanisms_and_opportunity_use"),
    2: (fig2, "Figure_2_weighting_history_information"),
    3: (fig3, "Figure_3_graded_engagement_intensity"),
    4: (fig4, "Figure_4_dynamic_thresholds_persistence"),
    5: (fig5, "Figure_5_context_encounter_sustained_use"),
    6: (fig6, "Figure_6_learned_boundary_actual_masking"),
}

# Structural contract only: editable wording is never duplicated here. This
# schema catches renamed/missing keys before even the first output is written.
_TEXT_KEYS = {
    1: {"A": "heading valuation_box action_box social_box allocation_box crossing_note", "B": "heading available_box encountered_box used_box footer"},
    2: {
        "A": "title ticks bar_format effect_note",
        "B": "title transformed_legend objective_legend xlabel ylabel",
        "C": "title sampling_outcome masking_outcome xlabel",
        "D": "title forced_outcome counterfactual_outcome xlabel",
    },
    3: {
        "shared": "receptivity_legend_format xlabel",
        "A": "title ylabel", "B": "title ylabel",
        "C": "title engagement_outcome endpoint_outcome modal_outcome intensity_outcome xlabel",
    },
    4: {"A": "title static_tick dynamic_tick_format bar_format xlabel", "B": "title bar_format sentinel_tick_format xlabel ylabel optimality_note"},
    5: {
        "shared": "xlabel context_tick_format bar_format",
        "A": "title", "B": "title", "C": "title encounter_legend masking_legend ylabel",
        "D": "title one_context_legend_format many_contexts_legend_format",
        "E": "title ylabel", "F": "title ylabel",
    },
    6: {"A": "title crossing_note_format objective_note hierarchical_note ylabel", "B": "title masking_legend modal_legend bar_format ticks ylabel"},
}
_FORMAT_FIELDS = {
    (2,"A","bar_format"): {"value": 58.8935},
    (3,"shared","receptivity_legend_format"): {"p": .75},
    (4,"A","dynamic_tick_format"): {"eta": .2},
    (4,"A","bar_format"): {"value": .7167},
    (4,"B","bar_format"): {"value": 99.67},
    (4,"B","sentinel_tick_format"): {"p": .4, "eta": 0},
    (5,"shared","context_tick_format"): {"k": 16},
    (5,"shared","bar_format"): {"value": 84.1906},
    (5,"D","one_context_legend_format"): {"count": 1},
    (5,"D","many_contexts_legend_format"): {"count": 4},
    (6,"A","crossing_note_format"): {"learned": .313, "lo": .310, "hi": .315},
    (6,"B","bar_format"): {"value": 58.8217},
}


def validate_text_catalog(shared=None, figures=None):
    """Validate keys, string/list types and named format fields; raise ValueError.

    Optional catalogs support in-memory tests. Validation does not check whether
    wording is scientifically correct or fits the fixed figure geometry.
    """
    shared = SHARED_TEXT if shared is None else shared
    figures = FIGURE_TEXT if figures is None else figures

    def keys(value, expected, path):
        if not isinstance(value, dict) or set(value) != set(expected):
            raise ValueError(f"{path}: expected keys {sorted(expected, key=str)}")

    def string(value, path):
        if not isinstance(value, str):
            raise ValueError(f"{path}: expected a string")

    def template(value, arguments, path):
        try:
            fields = {field for _,field,_,_ in Formatter().parse(value) if field is not None}
            if fields != set(arguments):
                raise ValueError(f"expected placeholders {sorted(arguments)}; found {sorted(fields)}")
            value.format(**arguments)
        except (ValueError, KeyError, IndexError, TypeError, AttributeError) as exc:
            raise ValueError(f"{path}: invalid format template ({exc})") from exc

    keys(shared, {"panel_title_format", "architectures", "final_window_masking_percent", "good_authentic_modal_percent", "comparison_cost"}, "SHARED_TEXT")
    keys(shared["architectures"], COLORS, "SHARED_TEXT.architectures")
    for key,value in shared.items():
        if key == "architectures":
            for architecture,label in value.items():
                string(label, f"SHARED_TEXT.architectures.{architecture}")
        else:
            string(value, f"SHARED_TEXT.{key}")
    template(shared["panel_title_format"], {"letter": "A", "text": "Title"}, "SHARED_TEXT.panel_title_format")
    keys(figures, _TEXT_KEYS, "FIGURE_TEXT")
    for number,panels in _TEXT_KEYS.items():
        keys(figures[number], panels, f"FIGURE_TEXT[{number}]")
        for panel,field_names in panels.items():
            block = figures[number][panel]
            keys(block, field_names.split(), f"FIGURE_TEXT[{number}].{panel}")
            for key,value in block.items():
                path = f"FIGURE_TEXT[{number}].{panel}.{key}"
                if key == "ticks":
                    count = 2 if number == 2 else 4
                    if not isinstance(value, list) or len(value) != count:
                        raise ValueError(f"{path}: expected a list of {count} strings")
                    for label in value:
                        string(label, path)
                else:
                    string(value, path)
                if key.endswith("_format"):
                    template(value, _FORMAT_FIELDS[number,panel,key], path)


def resolve_preview_dir(preview_dir):
    """Accept an absolute, isolated child of repo/tmp or a system temp root.

    Paths are resolved through symlinks before checking. The allowed root itself,
    the repository's sources/results, and all canonical outputs are forbidden.
    No directory is created by this check.
    """
    candidate = Path(preview_dir).expanduser()
    if not candidate.is_absolute():
        raise ValueError("Preview directory must be an absolute path")
    candidate = candidate.resolve()
    repo_tmp = (ROOT / "tmp").resolve()
    allowed_roots = {repo_tmp, Path("/private/tmp").resolve(), Path(tempfile.gettempdir()).resolve()}
    if not any(candidate != allowed and candidate.is_relative_to(allowed) for allowed in allowed_roots):
        raise ValueError("Preview directory must be a child of repo/tmp, /private/tmp, or the system temporary directory")
    if candidate.is_relative_to(ROOT) and not candidate.is_relative_to(repo_tmp):
        raise ValueError("Preview directory overlaps protected repository content")
    protected = (HERE, CANONICAL_OUT, CANONICAL_PDF_OUT, ROOT / "results", ROOT / "projects", ROOT / "output", ROOT / ".git", ROOT / "src", ROOT / "tests", ROOT / "scripts")
    if any(candidate.is_relative_to(path.resolve()) or path.resolve().is_relative_to(candidate) for path in protected):
        raise ValueError("Preview directory overlaps protected source, evidence, or canonical output directories")
    if candidate.exists() and not candidate.is_dir():
        raise ValueError("Preview directory is an existing non-directory path")
    # Check existing child symlinks too: a safe preview root must not hide a
    # png/ or individual output link that redirects writes into the paper.
    destinations = [candidate / "png", candidate / "pdf", candidate / "FIGURE_PROVENANCE.json"]
    destinations.extend(candidate / extension / f"{stem}.{extension}"
                        for _,stem in FIGURES.values() for extension in ("png", "pdf"))
    if any(not destination.resolve().is_relative_to(candidate) for destination in destinations):
        raise ValueError("Preview output symlink escapes the isolated preview directory")
    return candidate


def render_figures(figure_numbers=None, preview_dir=None):
    """Render canonical all-six outputs or an isolated selected preview.

    ``figure_numbers`` is an iterable of integers 1..6; supplying it requires
    ``preview_dir``. Repeated numbers are de-duplicated in numeric order. With no
    selection, all six are rendered. Preview destinations contain png/, pdf/
    and FIGURE_PROVENANCE.json. Returns the fresh provenance dictionary.
    """
    global OUT, PDF_OUT, PROVENANCE, LABELS
    if figure_numbers is not None and preview_dir is None:
        raise ValueError("Selecting figures requires --preview-dir; canonical builds always include all six")
    selected = list(FIGURES) if figure_numbers is None else list(figure_numbers)
    if not selected or any(type(number) is not int or number not in FIGURES for number in selected):
        raise ValueError("Figure numbers must be integers from 1 through 6")
    selected = sorted(set(selected))
    preview = resolve_preview_dir(preview_dir) if preview_dir is not None else None
    validate_text_catalog()
    for name,expected in HASHES.items():
        assert sha(ROOT/name)==expected,f"Source hash mismatch: {name}"
    OUT = preview / "png" if preview is not None else CANONICAL_OUT
    PDF_OUT = preview / "pdf" if preview is not None else CANONICAL_PDF_OUT
    PROVENANCE = new_provenance("preview" if preview is not None else "canonical", selected)
    LABELS = SHARED_TEXT["architectures"]
    style()
    for number in selected:
        FIGURES[number][0]()
    PROVENANCE["generator_sha256"]=sha(Path(__file__))
    PROVENANCE["text_source"] = str(TEXT_SOURCE.relative_to(ROOT))
    PROVENANCE["text_sha256"] = sha(TEXT_SOURCE)
    manifest_dir = preview if preview is not None else HERE
    manifest_dir.mkdir(parents=True,exist_ok=True)
    (manifest_dir/"FIGURE_PROVENANCE.json").write_text(json.dumps(PROVENANCE,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    return PROVENANCE


def main(argv=None):
    """CLI entry point; --list is read-only, partial builds are preview-only."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List numbered figures and editable catalog sections; write nothing")
    parser.add_argument("--figure", type=int, choices=tuple(FIGURES), action="append", help="Preview only this figure (repeatable; requires --preview-dir)")
    parser.add_argument("--preview-dir", type=Path, help="Absolute isolated child of repo/tmp or a system temporary directory")
    args = parser.parse_args(argv)
    if args.list:
        if args.figure is not None or args.preview_dir is not None:
            parser.error("--list cannot be combined with rendering options")
        for number,(builder,stem) in FIGURES.items():
            print(f"{number}: {builder.__name__}() -> {stem} [FIGURE_TEXT[{number}]]")
        return 0
    try:
        provenance = render_figures(args.figure, args.preview_dir)
    except ValueError as exc:
        parser.error(str(exc))
    count = len(provenance["selected_figures"])
    print(f"REVISION_FIGURES_OK: {count} PNG + {count} PDF outputs; {provenance['mode']} mode; 11 hash-pinned inputs; no simulations or estimator refits")
    return 0


if __name__=="__main__":
    raise SystemExit(main())
