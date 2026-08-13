"""Isolated, smoke-gated E06 M4 continuation-path diagnostics.

This module deliberately calls the maintained M4 state kernel without changing
its reward, Q-update, receptivity-update, or random-draw semantics.
"""
from __future__ import annotations

import csv, hashlib, json, math, platform, re, resource, subprocess, sys, time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import numpy as np

from gifted_masking.core import final_window_size, make_rng, softmax_sample, subjective_value
from gifted_masking.models.m4 import simulate_from_state, update_receptivity
from gifted_masking.repro import ensure_results_dirs, write_csv, write_json

RAW_FIELDS = "run_id,experiment_id,tier,model,component,scenario_id,scenario_role,path_type,master_seed,matched_family_id,policy_environment_seed_map_json,child_id,child_seed,rng_unit,n,segment_horizon,total_segments,final_window_fraction,final_window_start,final_window_end,p0,p_min,p_max,ka,kr,km_mode,nominal_km_values_json,actual_km_values_json,b,a,c,r,alpha,tau,lambda,q0,traversal_direction_json,traversal_nominal_km_json,traversal_actual_km_json,mask_rate_json,mask_count_json,auth_count_json,auth_accept_count_json,auth_reject_count_json,mean_objective_reward_json,p_start_json,p_end_json,q_mask_start_json,q_auth_start_json,q_mask_end_json,q_auth_end_json,bounds_violation_count_json,final_p,final_q_mask,final_q_auth".split(",")
CELL_FIELDS = "run_id,experiment_id,tier,scenario_id,path_type,direction,km,master_seed,n,mean_mask_rate,se_mask_rate,mean_p_end,se_p_end,mean_q_mask,mean_q_auth,mask_count,auth_count,auth_accept_count,auth_reject_count,bounds_violation_count".split(",")
PATH_FIELDS = "run_id,experiment_id,tier,scenario_id,path_type,master_seed,km,mask_up,mask_down,mask_down_minus_up,p_up,p_down,p_down_minus_up,decision_eligible".split(",")
LOOP_FIELDS = "run_id,experiment_id,tier,scenario_id,path_type,master_seed,response,signed_area,absolute_area,mean_vertical_separation,maximum_abs_separation,control_excess_area,direction,decision_eligible".split(",")
TRANSITION_FIELDS = "run_id,experiment_id,tier,scenario_id,path_type,master_seed,target,ascending_km,descending_km,width,status,decision_eligible,bootstrap_replicates,bootstrap_valid_fraction,ci_low,ci_high".split(",")
EFFECT_FIELDS = "run_id,experiment_id,tier,scenario_id,effect_name,level,master_seed,estimate,ci_low,ci_high,decision_eligible,notes".split(",")
PAYOFFS={"b":1.0,"a":.6,"c":.25,"r":2.0}; LEARNER={"alpha":.1,"tau":.25,"lambda":1.0,"q0":0.0}; BOUNDS={"p_min":.05,"p_max":.95}
SMOKE={"n":64,"segment_horizon":120,"final_window_fraction":.2,"master_seed":2026081699,"bootstrap_seed":2026081697,"bootstrap_replicates":0,"workers":1}
STANDARD_SEEDS=[2026081601,2026081602,2026081603,2026081604,2026081605]
CANONICAL_CONFIG_SHA256={
    "smoke":"475a8630acc73ab21520fd90024f85712b0002aec52d39d18e74e96cb8e4c40b",
    "standard":"58ebab7e6811369df90e14a697908eb0a106f6adcc1f897a4b201ca2a915cd7e",
    "qualification":"e252bc7901046249bc68f7b04c315177040c8e115273b56f19a163bf30f4b6c1",
}
SOURCE_FINGERPRINT_PATHS=(
    "src/gifted_masking/experiments/e06.py","src/gifted_masking/cli.py","src/gifted_masking/core.py","src/gifted_masking/models/m4.py","src/gifted_masking/repro.py",
    "configs/frontiers_article/e06_m4_paths_smoke.json","configs/frontiers_article/e06_m4_paths_standard.json","configs/frontiers_article/e06_m4_hysteresis_qualification.json",
    "tests/test_article_e06.py","projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md","projects/frontiers_article/E06_SECOND_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md","projects/frontiers_article/E06_FIX_IMPLEMENTATION_CODEX_INSTRUCTIONS.md","projects/frontiers_article/E06_CODEX_INSTRUCTION_SET.md","projects/frontiers_article/runbooks/E06_OPERATIONAL_INSTRUCTIONS.md","projects/frontiers_article/checkpoints/E06_SOL_SMOKE_REVIEW.md","projects/frontiers_article/RDS.md","projects/frontiers_article/STAGE2_EXPERIMENT_SPECIFICATIONS.md","ARCHITECTURE.md","pyproject.toml","scripts/verify.sh",
)

def _no_duplicates(text: str) -> object:
    def hook(pairs: list[tuple[str, object]]) -> dict[str, object]:
        out={}
        for k,v in pairs:
            if k in out: raise ValueError(f"duplicate JSON key: {k}")
            out[k]=v
        return out
    return json.loads(text, object_pairs_hook=hook)
def _canon(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",",":"), allow_nan=False,
                      default=lambda x: int(x) if isinstance(x, np.integer) else float(x) if isinstance(x, np.floating) else (_ for _ in ()).throw(TypeError(type(x).__name__)))
def _label(x: float) -> str: return f"{x:.4f}"
def _sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def _source_fingerprint(root:Path)->str:
    # Hash each source first, then bind the complete ordered path/hash map.  A
    # later sealer can therefore distinguish path-list drift from file drift.
    return _source_fingerprint_from_records(_source_records(root))
def _finite(x: object) -> float:
    y=float(x)
    if not math.isfinite(y): raise ValueError("nonfinite value")
    return y

def _strict_json(text: object) -> object:
    """Decode compact packed JSON without accepting duplicate keys or NaN."""
    if not isinstance(text, str):
        raise ValueError("packed JSON must be a string")
    try:
        return json.loads(text, object_pairs_hook=lambda pairs: _duplicate_free_object(pairs),
                          parse_constant=lambda token: (_ for _ in ()).throw(ValueError(f"invalid JSON constant: {token}")))
    except (TypeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid packed JSON") from exc

def _duplicate_free_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def _strict_int(value: object, *, csv_value: bool) -> int:
    if csv_value:
        if not isinstance(value, str) or not re.fullmatch(r"-?(?:0|[1-9][0-9]*)", value):
            raise ValueError("integer CSV field is not an exact integer")
        return int(value)
    if type(value) is not int:
        raise ValueError("materialized integer field has wrong type")
    return value

def _strict_float(value: object, *, csv_value: bool) -> float:
    if csv_value:
        if not isinstance(value, str) or not value or value.strip()!=value:
            raise ValueError("float CSV field has wrong type")
        try: result=float(value)
        except ValueError as exc: raise ValueError("invalid float CSV field") from exc
    else:
        if type(value) is not float:
            raise ValueError("materialized float field has wrong type")
        result=value
    if not math.isfinite(result):
        raise ValueError("nonfinite numeric field")
    return result

def _semantic_equal(observed: object, expected: object, *, tolerance: float=1e-12) -> bool:
    """Typed recursive comparison; booleans never stand in for numeric values."""
    if type(expected) is int:
        return type(observed) is int and observed==expected
    if type(expected) is float:
        return type(observed) is float and math.isfinite(observed) and math.isclose(observed,expected,rel_tol=0,abs_tol=tolerance)
    if type(expected) is str:
        return type(observed) is str and observed==expected
    if type(expected) is list:
        return type(observed) is list and len(observed)==len(expected) and all(_semantic_equal(a,b,tolerance=tolerance) for a,b in zip(observed,expected,strict=True))
    if type(expected) is dict:
        return type(observed) is dict and list(observed)==list(expected) and all(_semantic_equal(observed[key],value,tolerance=tolerance) for key,value in expected.items())
    raise TypeError(f"unsupported expected raw type: {type(expected).__name__}")

def load_e06_config(path: Path) -> dict[str, Any]:
    c=_no_duplicates(path.read_text())
    if not isinstance(c,dict): raise ValueError("E06 config must be an object")
    required={"experiment_id","run_id","tier","model","n","segment_horizon","final_window_fraction","master_seed","bootstrap_seed","bootstrap_replicates","workers","payoffs","learner","bounds","km_values","scenarios"}
    if required-set(c) or set(c)-required-{"master_seeds","approved_standard","approved_qualification"}: raise ValueError("E06 config keys are frozen")
    if c["experiment_id"]!="E06" or c["model"]!="M4" or c["tier"] not in {"smoke","standard","qualification"}: raise ValueError("unsupported E06 config")
    for k in ("n","segment_horizon","master_seed","bootstrap_seed","bootstrap_replicates","workers"):
        if type(c[k]) is not int: raise ValueError(f"{k} must be an exact JSON integer")
    if type(c["final_window_fraction"]) is not float or c["workers"]!=1: raise ValueError("E06 exact types/workers required")
    if c["payoffs"]!=PAYOFFS or c["learner"]!=LEARNER or c["bounds"]!=BOUNDS: raise ValueError("frozen M4 parameters differ")
    xs=c["km_values"]
    if not isinstance(xs,list) or any(type(x) is not float for x in xs) or xs != sorted(xs) or len(set(xs))!=len(xs): raise ValueError("km grid must be ordered JSON floats")
    if c["tier"]=="smoke":
        if {k:c[k] for k in SMOKE}!={k:SMOKE[k] for k in SMOKE} or c["run_id"]!="frontiers_m4_path_diagnostics_v1_smoke" or xs != [0.,.001,.002,.003,.004] or len(c["scenarios"])!=1: raise ValueError("smoke differs from approval")
    elif c["tier"]=="standard":
        if c.get("approved_standard") is not False or c.get("master_seeds")!=STANDARD_SEEDS: raise ValueError("standard config is non-executable and frozen")
    elif c.get("approved_qualification") is not False: raise ValueError("qualification config is non-executable and frozen")
    # The three approved payloads are immutable scientific contracts.  The
    # canonical hash comparison is recursive (and type-sensitive because JSON
    # was parsed above with exact type checks), so unknown, missing, reordered,
    # or nested-mutated fields fail before dispatch.
    if hashlib.sha256(_canon(c).encode()).hexdigest()!=CANONICAL_CONFIG_SHA256[c["tier"]]:
        raise ValueError("E06 configuration differs from its complete frozen canonical payload")
    return c

def segment_id(master: int, scenario: str, direction: str, position: int, km: float) -> str:
    return f"E06|master={master}|scenario={scenario}|direction={direction}|position={position}|km={_label(km)}|policy_environment"
def derive_segment_seed(master: int, scenario: str, direction: str, position: int, km: float) -> int:
    words=np.frombuffer(hashlib.sha256(segment_id(master,scenario,direction,position,km).encode()).digest()[:16],dtype="<u4")
    return int(np.random.SeedSequence([master,6,*map(int,words)]).spawn(1)[0].generate_state(1,dtype=np.uint64)[0])

def loop_area(xs: Iterable[float], up: Iterable[float], down: Iterable[float]) -> tuple[float,float]:
    x=np.asarray(list(xs),float); u=np.asarray(list(up),float); d=np.asarray(list(down),float)
    if len(x)<2 or x.shape!=u.shape or x.shape!=d.shape or not np.isfinite(np.r_[x,u,d]).all() or np.any(np.diff(x)<=0): raise ValueError("loop inputs must be finite and strictly increasing")
    gap=d-u; return float(np.trapezoid(gap,x)),float(np.trapezoid(np.abs(gap),x))
def nondecreasing_pava(values: Iterable[float]) -> np.ndarray:
    vals=list(map(float,values))
    if not vals or not all(math.isfinite(x) for x in vals): raise ValueError("PAVA requires finite values")
    blocks: list[list[float]]=[]
    for value in vals:
        blocks.append([value,1.,1.])
        while len(blocks)>1 and blocks[-2][0]>blocks[-1][0]:
            b=blocks.pop(); a=blocks.pop(); w=a[1]+b[1]; blocks.append([(a[0]*a[1]+b[0]*b[1])/w,w,a[2]+b[2]])
    return np.array([m for m,_,n in blocks for _ in range(int(n))])
def invert_transition(xs: Iterable[float], response: Iterable[float], target: float) -> tuple[float|None,str]:
    x=list(map(float,xs)); y=list(map(float,response))
    if len(x)!=len(y) or not x or not math.isfinite(target) or not all(math.isfinite(z) for z in x+y) or any(b<=a for a,b in zip(x,x[1:])): raise ValueError("transition inputs invalid")
    if all(v<target for v in y): return None,"no_crossing_below"
    if all(v>target for v in y): return None,"no_crossing_above"
    hits=[a for a,b in zip(x,y) if abs(b-target)<=1e-15]
    if hits: value=(min(hits)+max(hits))/2
    else:
        value=None
        for a,b,c,d in zip(x,x[1:],y,y[1:]):
            if c<target<d: value=a+(target-c)*(b-a)/(d-c); break
        if value is None: return None,"boundary_or_undefined"
    return (value,"valid") if x[0]<value<x[-1] else (None,"boundary_or_undefined")


T_CRITICAL_95_DF4=2.7764451051977987
def paired_student_t_effect(values: Iterable[float]) -> dict[str,float]:
    vals=np.asarray(list(values),dtype=float)
    if vals.shape!=(5,) or not np.isfinite(vals).all(): raise ValueError("E06 paired effect requires exactly five finite masters")
    mean=float(vals.mean()); half=T_CRITICAL_95_DF4*float(vals.std(ddof=1))/math.sqrt(5)
    return {"estimate":mean,"ci_low":mean-half,"ci_high":mean+half,"df":4.0}

def derive_bootstrap_seed(bootstrap_seed:int,scenario_id:str,response:str,target:float|None)->int:
    target_text="none" if target is None else f"{target:g}"
    semantic=f"E06|bootstrap|scenario={scenario_id}|response={response}|target={target_text}"
    words=np.frombuffer(hashlib.sha256(semantic.encode()).digest()[:16],dtype="<u4")
    return int(np.random.SeedSequence([bootstrap_seed,60,*map(int,words)]).spawn(1)[0].generate_state(1,dtype=np.uint64)[0])

def linear_percentile(values: Iterable[float],q:float)->float:
    data=sorted(float(x) for x in values)
    if not data or not 0<=q<=1 or not all(math.isfinite(x) for x in data): raise ValueError("invalid percentile input")
    h=(len(data)-1)*q; lo,hi=math.floor(h),math.ceil(h)
    return data[lo]+(data[hi]-data[lo])*(h-lo)

def bootstrap_paired_transition_width(up_curves: Iterable[Iterable[float]],down_curves: Iterable[Iterable[float]],xs: Iterable[float],*,bootstrap_seed:int,scenario_id:str,response:str,target:float,replicates:int=10000)->dict[str,object]:
    up=np.asarray(list(up_curves),float); down=np.asarray(list(down_curves),float); x=np.asarray(list(xs),float)
    if up.shape!=(5,len(x)) or down.shape!=up.shape or replicates!=10000 or not np.isfinite(np.r_[up.ravel(),down.ravel(),x]).all(): raise ValueError("E06 bootstrap requires five complete finite paired curves and 10000 draws")
    pooled_u,us=invert_transition(x,nondecreasing_pava(up.mean(axis=0)),target); pooled_d,ds=invert_transition(x,nondecreasing_pava(down.mean(axis=0)),target)
    rng=make_rng(derive_bootstrap_seed(bootstrap_seed,scenario_id,response,target)); widths=[]
    for _ in range(replicates):
        pick=rng.integers(0,5,size=5); u,su=invert_transition(x,nondecreasing_pava(up[pick].mean(axis=0)),target); d,sd=invert_transition(x,nondecreasing_pava(down[pick].mean(axis=0)),target)
        if su==sd=="valid": widths.append(float(u-d))
    fraction=len(widths)/replicates; valid_pool=us==ds=="valid"
    return {"pooled_valid":valid_pool,"pooled_status":f"ascending:{us};descending:{ds}","valid":len(widths),"fraction":fraction,"estimable":bool(valid_pool and fraction>=.95),"ci_low":"" if not(valid_pool and fraction>=.95) else linear_percentile(widths,.025),"ci_high":"" if not(valid_pool and fraction>=.95) else linear_percentile(widths,.975)}


def phase_separated_core_projection(smoke_config: dict[str,Any], phase: dict[str,float], raw_bytes:int, total_bytes:int, rss_mib:float, root:Path) -> dict[str,object]:
    """Project frozen core cost from measured n=400 segment phases.

    The M4 implementation is vectorized, so multiplying a 64-learner smoke
    wall time by scalar learner steps is demonstrably conservative in the
    wrong direction.  This readiness-only probe measures one exact n=400
    segment for each frozen core horizon and scales by the *known segment
    count*.  It neither dispatches a standard configuration nor writes a
    standard scientific artifact.
    """
    standard=load_e06_config(root/"configs/frontiers_article/e06_m4_paths_standard.json")
    segment_counts:dict[int,int]=defaultdict(int)
    for scenario in standard["scenarios"]:
        h=int(scenario.get("segment_horizon",standard["segment_horizon"]))
        for path in scenario["path_types"]:
            segment_counts[h]+= (2*len(standard["km_values"]) if path!="cold_start" else len(standard["km_values"])) * len(standard["master_seeds"])
    probe_seconds={}
    for h in sorted(segment_counts):
        scenario=next(s for s in standard["scenarios"] if int(s.get("segment_horizon",standard["segment_horizon"]))==h)
        probe_config={**smoke_config,"n":400}; probe_s={**scenario,"segment_horizon":h}
        p=np.full(400,float(scenario["p0"]));q=np.full((400,2),float(standard["learner"]["q0"]))
        measurements=[]
        for repeat in range(3):
            began=time.perf_counter(); _run_segment(p,q,0.002,1000+h+repeat,probe_config,probe_s); measurements.append(time.perf_counter()-began)
        probe_seconds[h]=min(measurements)
    simulated=math.fsum(probe_seconds[h]*segment_counts[h] for h in segment_counts)
    serialization=float(phase["serialization"])*(52000/320); derived=float(phase["derived"])*10; figure=float(phase["figure"]); startup=float(phase.get("startup",0.0))
    projected=simulated+serialization+derived+figure+startup
    result={"rows":52000,"learner_steps":913000000,"method":"phase_separated_vectorized_n400_segment_benchmark_v1","smoke_phase_seconds":phase,"segment_counts":dict(segment_counts),"n400_probe_seconds":probe_seconds,"projected_components_seconds":{"simulation":simulated,"serialization":serialization,"derived":derived,"figure":figure,"startup":startup},"seconds":projected,"raw_mib":raw_bytes*(52000/320)/1024**2,"total_mib":total_bytes*(52000/320)/1024**2,"peak_rss_mib":rss_mib*1.5,"limits":{"seconds":600,"raw_mib":400,"total_mib":500,"rss_mib":2048}}
    result["within_limits"]=result["seconds"]<=600 and result["raw_mib"]<=400 and result["total_mib"]<=500 and result["peak_rss_mib"]<=2048
    return result

def _run_segment(p: np.ndarray,q: np.ndarray,actual: float, seed: int, config: dict[str,Any], s:dict[str,Any], *, trajectory: bool=False) -> tuple[dict[str,np.ndarray],np.ndarray,np.ndarray,np.ndarray|None]:
    """Replay the maintained M4 kernel while retaining final-window evidence.

    This deliberately duplicates no policy semantics: it uses the same shared
    softmax, subjective-value, and receptivity helpers in the maintained order.
    It exists only because ``simulate_from_state`` intentionally exposes no
    action/outcome/reward trace.
    """
    h=int(s.get("segment_horizon",config["segment_horizon"])); n=len(p)
    pay=config["payoffs"]; learn=config["learner"]; bounds=config["bounds"]
    q2=q.copy(); p2=np.clip(p.copy(),bounds["p_min"],bounds["p_max"])
    window=final_window_size(h,float(config["final_window_fraction"])); start=h-window
    idx=np.arange(n); rng=make_rng(seed)
    mc=np.zeros(n,dtype=int); ac=np.zeros(n,dtype=int); aa=np.zeros(n,dtype=int); ar=np.zeros(n,dtype=int); reward_sum=np.zeros(n); violations=np.zeros(n,dtype=int)
    trace=np.empty((h,n),dtype=float) if trajectory else None
    for t in range(h):
        action=softmax_sample(q2,float(s.get("tau",learn["tau"])),rng)
        authentic=action==1
        accepted=rng.random(n)<p2  # deliberately consumed for masking too
        reward=np.where(~authentic,pay["b"]-pay["c"],np.where(accepted,pay["b"]+pay["a"],pay["a"]-pay["r"]))
        q2[idx,action]+=learn["alpha"]*(subjective_value(reward,float(s.get("lambda",learn["lambda"]))) - q2[idx,action])
        p2=update_receptivity(p2,authentic,accepted,km=actual,ka=s["ka"],kr=s["kr"],p_min=bounds["p_min"],p_max=bounds["p_max"])
        violations += (p2 < bounds["p_min"]) | (p2 > bounds["p_max"])
        if trace is not None: trace[t]=p2
        if t>=start:
            mc += ~authentic; ac += authentic; aa += authentic & accepted; ar += authentic & ~accepted; reward_sum += reward
    return {"mask":mc/window,"mc":mc,"ac":ac,"aa":aa,"ar":ar,"reward":reward_sum/window,"bv":violations},p2,q2,trace


def replay_segment_parity(p: np.ndarray,q: np.ndarray,actual: float,seed: int,config: dict[str,Any],scenario: dict[str,Any]) -> None:
    """Fail loudly if the E06 diagnostic replay diverges from maintained M4."""
    metrics,p2,q2,trace=_run_segment(p,q,actual,seed,config,scenario,trajectory=True)
    h=int(scenario.get("segment_horizon",config["segment_horizon"])); kwargs={**config["payoffs"],**config["bounds"],"ka":scenario["ka"],"kr":scenario["kr"],"alpha":config["learner"]["alpha"],"temp":scenario.get("tau",config["learner"]["tau"]),"lam":scenario.get("lambda",config["learner"]["lambda"]),"horizon":h,"final_window_fraction":config["final_window_fraction"],"seed":seed,"ntraj":len(p)}
    mask,mp,mtrace,mq=simulate_from_state(p,q,actual,**kwargs)
    np.testing.assert_allclose(metrics["mask"],mask,rtol=0,atol=1e-12)
    np.testing.assert_allclose(p2,mp,rtol=0,atol=1e-12); np.testing.assert_allclose(q2,mq,rtol=0,atol=1e-12)
    np.testing.assert_allclose(trace,mtrace,rtol=0,atol=1e-12)

def _family(config:dict[str,Any], s:dict[str,Any], master:int, path:str) -> list[dict[str,object]]:
    xs=[float(x) for x in config["km_values"]]; n=int(config["n"]); initial_p=np.full(n,s["p0"]); initial_q=np.full((n,2),config["learner"]["q0"])
    if path in {"inherited_loop","km_disabled_inherited_loop"}: traversal=[("up",i,x) for i,x in enumerate(xs)]+[("down",i,x) for i,x in enumerate(reversed(xs))]
    elif path in {"reversal_only","km_disabled_reversal_only"}: traversal=[("up",i,x) for i,x in enumerate(xs)]+[("down",i,x) for i,x in enumerate(reversed(xs))]
    elif path=="cold_start": traversal=[("cold",i,x) for i,x in enumerate(xs)]
    else: raise ValueError("unknown path")
    per=[defaultdict(list) for _ in range(n)]; p,q=initial_p.copy(),initial_q.copy(); seeds=[]
    for direction,pos,nominal in traversal:
        seed=derive_segment_seed(master,s["id"],direction,pos,nominal); seeds.append({"direction":direction,"position":pos,"km":_label(nominal),"seed":seed})
        reset=path in {"reversal_only","km_disabled_reversal_only","cold_start"}
        if reset: p,q=initial_p.copy(),initial_q.copy()
        actual=0. if path.startswith("km_disabled_") or s.get("actual_km_mode")=="disabled" else nominal
        startp,startq=p.copy(),q.copy(); metrics,p,q,_=_run_segment(p,q,actual,seed,config,s)
        for i in range(n):
            for key,value in {"direction":direction,"nominal":nominal,"actual":actual,"mask":metrics["mask"][i],"mc":metrics["mc"][i],"ac":metrics["ac"][i],"aa":metrics["aa"][i],"ar":metrics["ar"][i],"reward":metrics["reward"][i],"bv":metrics["bv"][i],"pstart":startp[i],"pend":p[i],"qmstart":startq[i,0],"qastart":startq[i,1],"qmend":q[i,0],"qaend":q[i,1]}.items(): per[i][key].append(float(value) if isinstance(value,np.floating) else value)
    rows=[]; h=int(s.get("segment_horizon",config["segment_horizon"])); start=h-int(math.ceil(h*config["final_window_fraction"]))
    for child,d in enumerate(per):
        fields={"run_id":config["run_id"],"experiment_id":"E06","tier":config["tier"],"model":"M4","component":"primary","scenario_id":s["id"],"scenario_role":s["role"],"path_type":path,"master_seed":master,"matched_family_id":f"E06|master={master}|scenario={s['id']}|path={path}","policy_environment_seed_map_json":_canon(seeds),"child_id":child,"child_seed":"vectorized_segment_streams","rng_unit":"vectorized_policy_environment_segment_stream","n":n,"segment_horizon":h,"total_segments":len(traversal),"final_window_fraction":config["final_window_fraction"],"final_window_start":start,"final_window_end":h-1,"p0":s["p0"],**config["bounds"],"ka":s["ka"],"kr":s["kr"],"km_mode":"disabled" if path.startswith("km_disabled_") else s.get("actual_km_mode","active"),"nominal_km_values_json":_canon(xs),"actual_km_values_json":_canon([0. if path.startswith("km_disabled_") else x for x in xs]),**config["payoffs"],"alpha":config["learner"]["alpha"],"tau":s.get("tau",config["learner"]["tau"]),"lambda":s.get("lambda",config["learner"]["lambda"]),"q0":config["learner"]["q0"],"traversal_direction_json":_canon(d["direction"]),"traversal_nominal_km_json":_canon(d["nominal"]),"traversal_actual_km_json":_canon(d["actual"]),"mask_rate_json":_canon(d["mask"]),"mask_count_json":_canon(d["mc"]),"auth_count_json":_canon(d["ac"]),"auth_accept_count_json":_canon(d["aa"]),"auth_reject_count_json":_canon(d["ar"]),"mean_objective_reward_json":_canon(d["reward"]),"p_start_json":_canon(d["pstart"]),"p_end_json":_canon(d["pend"]),"q_mask_start_json":_canon(d["qmstart"]),"q_auth_start_json":_canon(d["qastart"]),"q_mask_end_json":_canon(d["qmend"]),"q_auth_end_json":_canon(d["qaend"]),"bounds_violation_count_json":_canon(d["bv"]),"final_p":d["pend"][-1],"final_q_mask":d["qmend"][-1],"final_q_auth":d["qaend"][-1]}
        rows.append({k:fields[k] for k in RAW_FIELDS})
    return rows

def expected_rows(config:dict[str,Any])->int:
    return sum(len(s["path_types"])*int(config["n"]) for s in config["scenarios"]) * (1 if config["tier"]=="smoke" else len(config.get("master_seeds",[])))

_RAW_JSON_FIELDS=frozenset((
    "policy_environment_seed_map_json","nominal_km_values_json","actual_km_values_json",
    "traversal_direction_json","traversal_nominal_km_json","traversal_actual_km_json",
    "mask_rate_json","mask_count_json","auth_count_json","auth_accept_count_json",
    "auth_reject_count_json","mean_objective_reward_json","p_start_json","p_end_json",
    "q_mask_start_json","q_auth_start_json","q_mask_end_json","q_auth_end_json",
    "bounds_violation_count_json",
))
_RAW_INT_FIELDS=frozenset(("master_seed","child_id","n","segment_horizon","total_segments","final_window_start","final_window_end"))
_RAW_FLOAT_FIELDS=frozenset(("final_window_fraction","p0","p_min","p_max","ka","kr","b","a","c","r","alpha","tau","lambda","q0","final_p","final_q_mask","final_q_auth"))
_EXPECTED_RAW_CACHE: dict[str, tuple[dict[str,object],...]] = {}

def _expected_raw_rows(config:dict[str,Any])->list[dict[str,object]]:
    """Rebuild ordered frozen rows without reading a candidate row.

    This boundary intentionally starts from the complete approved config and
    semantic segment seed derivation.  ``_family`` owns the maintained-M4
    replay and never receives candidate identity, seeds, parameters, traversal,
    reset state, or Q-continuity values.
    """
    _validate_frozen_e06_config(config)
    cache_key=_canon(config)
    cached=_EXPECTED_RAW_CACHE.get(cache_key)
    if cached is not None:
        # Deep-copying the authoritative baseline prevents a caller from
        # mutating the cached reconstruction between validation calls.
        return [dict(row) for row in cached]
    masters=[int(config["master_seed"])] if config["tier"]=="smoke" else [int(x) for x in config["master_seeds"]]
    rebuilt=[]
    for master in masters:
        for scenario in config["scenarios"]:
            for path in scenario["path_types"]:
                rebuilt.extend(_family(config,scenario,master,path))
    _EXPECTED_RAW_CACHE[cache_key]=tuple(dict(row) for row in rebuilt)
    return rebuilt

def _canonical_candidate_raw_value(field:str, value:object, expected:object)->object:
    """Accept exact materialized types or production CSV text, never coercion."""
    csv_value=isinstance(value,str) and field not in {"run_id","experiment_id","tier","model","component","scenario_id","scenario_role","path_type","matched_family_id","child_seed","rng_unit","km_mode"}
    if field in _RAW_JSON_FIELDS:
        return _strict_json(value)
    if field in _RAW_INT_FIELDS:
        return _strict_int(value,csv_value=csv_value)
    if field in _RAW_FLOAT_FIELDS:
        return _strict_float(value,csv_value=csv_value)
    if type(expected) is str:
        if type(value) is not str:
            raise ValueError(f"raw string field {field} has wrong type")
        return value
    raise AssertionError(f"unclassified raw field: {field}")

def validate_e06_raw(rows:list[dict[str,object]],config:dict[str,Any])->None:
    if type(rows) is not list or len(rows)!=expected_rows(config):
        raise ValueError("E06 raw schema/cardinality mismatch")
    expected_rows_from_config=_expected_raw_rows(config)
    for index,(candidate,expected) in enumerate(zip(rows,expected_rows_from_config,strict=True)):
        if type(candidate) is not dict or list(candidate)!=RAW_FIELDS or any(value is None for value in candidate.values()):
            raise ValueError(f"E06 raw schema/overflow mismatch at row {index}")
        for field in RAW_FIELDS:
            observed=_canonical_candidate_raw_value(field,candidate[field],expected[field])
            wanted=_strict_json(expected[field]) if field in _RAW_JSON_FIELDS else expected[field]
            if not _semantic_equal(observed,wanted):
                raise ValueError(f"E06 raw frozen reconstruction mismatch at row {index}, field {field}")

def _derive_tables_from_validated_raw(rows:list[dict[str,object]],config:dict[str,Any])->tuple[list[dict[str,object]],list[dict[str,object]],list[dict[str,object]],list[dict[str,object]],list[dict[str,object]]]:
    """Pure E06 derived reconstruction; callers must validate packed raw rows first."""
    cells=[]; paths=[]; loops=[]; transitions=[]; effects=[]; xs=[float(x) for x in config["km_values"]]
    grouped=defaultdict(list)
    for r in rows:
        for d,x,m,p,qm,qa,mc,ac,aa,ar,bv in zip(*[json.loads(str(r[k])) for k in ("traversal_direction_json","traversal_nominal_km_json","mask_rate_json","p_end_json","q_mask_end_json","q_auth_end_json","mask_count_json","auth_count_json","auth_accept_count_json","auth_reject_count_json","bounds_violation_count_json")],strict=True): grouped[(str(r["scenario_id"]),str(r["path_type"]),int(r["master_seed"]),d,float(x))].append((float(m),float(p),float(qm),float(qa),int(mc),int(ac),int(aa),int(ar),int(bv)))
    for (sid,path,master,d,x),v in sorted(grouped.items()):
        a=np.asarray(v,float); cells.append(dict(zip(CELL_FIELDS,[config["run_id"],"E06",config["tier"],sid,path,d,x,master,len(v),a[:,0].mean(),a[:,0].std(ddof=1)/math.sqrt(len(v)),a[:,1].mean(),a[:,1].std(ddof=1)/math.sqrt(len(v)),a[:,2].mean(),a[:,3].mean(),int(a[:,4].sum()),int(a[:,5].sum()),int(a[:,6].sum()),int(a[:,7].sum()),int(a[:,8].sum())])))
    loop_values:dict[tuple[object,...],dict[str,float]]={}
    for sid in sorted({str(r["scenario_id"]) for r in rows}):
      for path in ("inherited_loop","reversal_only","km_disabled_inherited_loop","km_disabled_reversal_only"):
       for master in sorted({int(r["master_seed"]) for r in rows if r["scenario_id"]==sid and r["path_type"]==path}):
        up=[next(float(c["mean_mask_rate"]) for c in cells if c["scenario_id"]==sid and c["path_type"]==path and c["master_seed"]==master and c["direction"]=="up" and c["km"]==x) for x in xs]; down=[next(float(c["mean_mask_rate"]) for c in cells if c["scenario_id"]==sid and c["path_type"]==path and c["master_seed"]==master and c["direction"]=="down" and c["km"]==x) for x in xs]; pu=[next(float(c["mean_p_end"]) for c in cells if c["scenario_id"]==sid and c["path_type"]==path and c["master_seed"]==master and c["direction"]=="up" and c["km"]==x) for x in xs]; pd=[next(float(c["mean_p_end"]) for c in cells if c["scenario_id"]==sid and c["path_type"]==path and c["master_seed"]==master and c["direction"]=="down" and c["km"]==x) for x in xs]
        for x,u,d,up_p,down_p in zip(xs,up,down,pu,pd): paths.append(dict(zip(PATH_FIELDS,[config["run_id"],"E06",config["tier"],sid,path,master,x,u,d,d-u,up_p,down_p,down_p-up_p,"False"])))
        for response,u,d in (("mask",up,down),("receptivity",pu,pd)):
            signed,absolute=loop_area(xs,u,d); loop_values[(sid,path,master,response)]={"signed":signed,"absolute":absolute,"mean":signed/(xs[-1]-xs[0]),"maximum":max(abs(np.asarray(d)-np.asarray(u)))}
        for target in (.5,.75):
            au,sa=invert_transition(xs,nondecreasing_pava(up),target); ad,sd=invert_transition(xs,nondecreasing_pava(down),target); status="valid" if sa==sd=="valid" else f"ascending:{sa};descending:{sd}"; transitions.append(dict(zip(TRANSITION_FIELDS,[config["run_id"],"E06",config["tier"],sid,path,master,target,"" if au is None else au,"" if ad is None else ad,"" if au is None or ad is None else au-ad,status,"False",0,"","",""])))
    controls={"inherited_loop":"reversal_only","km_disabled_inherited_loop":"km_disabled_reversal_only"}
    for (sid,path,master,response), values in sorted(loop_values.items()):
        control=controls.get(str(path)); excess="" if control is None else values["signed"]-loop_values[(sid,control,master,response)]["signed"]
        loops.append(dict(zip(LOOP_FIELDS,[config["run_id"],"E06",config["tier"],sid,path,master,response,values["signed"],values["absolute"],values["mean"],values["maximum"],excess,"positive" if response=="mask" else "negative","False"])))
    # Smoke effects are descriptive scalar reconstructions only: never intervals,
    # inference, or a substituted zero for an unavailable quantity.
    for sid in sorted({str(r["scenario_id"]) for r in rows}):
      for master in sorted({int(r["master_seed"]) for r in rows if r["scenario_id"]==sid}):
       cold=sorted((c for c in cells if c["scenario_id"]==sid and c["path_type"]=="cold_start" and c["master_seed"]==master),key=lambda c:float(c["km"]))
       if len(cold)!=len(xs): raise ValueError("cold-start endpoint reconstruction incomplete")
       for field,label in (("mean_mask_rate","mask"),("mean_p_end","receptivity")):
           effects.append(dict(zip(EFFECT_FIELDS,[config["run_id"],"E06",config["tier"],sid,f"cold_start_{label}_km_004_minus_0","master_seed",master,float(cold[-1][field])-float(cold[0][field]),"","","False","diagnostic only"])))
       for inherited,control,prefix in (("inherited_loop","reversal_only","active"),("km_disabled_inherited_loop","km_disabled_reversal_only","disabled_feedback_placebo")):
           for response in ("mask","receptivity"):
               estimate=loop_values[(sid,inherited,master,response)]["signed"]-loop_values[(sid,control,master,response)]["signed"]
               effects.append(dict(zip(EFFECT_FIELDS,[config["run_id"],"E06",config["tier"],sid,f"{prefix}_inherited_minus_reversal_{response}_control_excess_area","master_seed",master,estimate,"","","False","diagnostic only"])))
    return cells,paths,loops,transitions,effects

def derive_tables(rows:list[dict[str,object]],config:dict[str,Any])->tuple[list[dict[str,object]],list[dict[str,object]],list[dict[str,object]],list[dict[str,object]],list[dict[str,object]]]:
    """Return E06 tables only after raw packed-row validation succeeds."""
    validate_e06_raw(rows,config)
    return _derive_tables_from_validated_raw(rows,config)

def _validate_frozen_e06_config(config:dict[str,Any])->None:
    """Require the exact canonical config even for programmatic validator calls."""
    tier=config.get("tier") if isinstance(config,dict) else None
    if tier not in CANONICAL_CONFIG_SHA256 or hashlib.sha256(_canon(config).encode()).hexdigest()!=CANONICAL_CONFIG_SHA256[tier]:
        raise ValueError("derived validation requires the exact frozen E06 configuration")

def _compare_derived_table(name:str, actual:list[dict[str,object]], expected:list[dict[str,object]], fields:list[str], *, abs_tolerance:float)->None:
    if len(actual)!=len(expected): raise ValueError(f"E06 {name} cardinality mismatch")
    for index,(observed,want) in enumerate(zip(actual,expected,strict=True)):
        if list(observed)!=fields: raise ValueError(f"E06 {name} schema/order mismatch at row {index}")
        for field in fields:
            value=observed[field]; target=want[field]
            if isinstance(target,str):
                if value!=target: raise ValueError(f"E06 {name} identity/status mismatch at row {index}, field {field}")
            elif type(target) is int:
                if isinstance(value,bool) or not math.isfinite(_finite(value)) or not _finite(value).is_integer() or int(_finite(value))!=target:
                    raise ValueError(f"E06 {name} integer mismatch at row {index}, field {field}")
            else:
                numeric=_finite(value)
                if not math.isclose(numeric,float(target),rel_tol=0,abs_tol=abs_tolerance):
                    raise ValueError(f"E06 {name} numerical mismatch at row {index}, field {field}")

def validate_e06_derived(raw_rows:list[dict[str,object]],cells:list[dict[str,object]],paths:list[dict[str,object]],loops:list[dict[str,object]],transitions:list[dict[str,object]],effects:list[dict[str,object]],config:dict[str,Any],*,abs_tolerance:float=1e-12)->None:
    """Fail-closed, raw-grounded validation of every E06 derived artifact.

    This deliberately reconstructs expected rows independently from validated
    packed raw rows.  Ordered row-by-row comparison rejects missing, duplicate,
    foreign, reordered, nonfinite, and numerically altered derived values.
    """
    if not math.isfinite(abs_tolerance) or abs_tolerance<0: raise ValueError("invalid E06 derived tolerance")
    _validate_frozen_e06_config(config)
    validate_e06_raw(raw_rows,config)
    expected=_derive_tables_from_validated_raw(raw_rows,config)
    for name,actual,want,fields in zip(("cells","paths","loops","transitions","effects"),(cells,paths,loops,transitions,effects),expected,(CELL_FIELDS,PATH_FIELDS,LOOP_FIELDS,TRANSITION_FIELDS,EFFECT_FIELDS),strict=True):
        _compare_derived_table(name,actual,want,fields,abs_tolerance=abs_tolerance)
    if config["tier"]=="smoke":
        for table in (paths,loops,transitions,effects):
            if any(row["decision_eligible"]!="False" for row in table): raise ValueError("smoke E06 derived row is decision eligible")
        for row in transitions:
            if row["bootstrap_replicates"] not in (0,"0") or any(row[field]!="" for field in ("bootstrap_valid_fraction","ci_low","ci_high")):
                raise ValueError("smoke E06 inference must remain unavailable, not zero-filled")

def _figure(path:Path,paths:list[dict[str,object]])->None:
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig,ax=plt.subplots(1,2,figsize=(9,3.5))
    for kind,axis,field in (("inherited_loop",ax[0],"mask_up"),("inherited_loop",ax[1],"p_up")):
        rows=[r for r in paths if r["path_type"]==kind]; axis.plot([r["km"] for r in rows],[r[field] for r in rows],label="ascending"); axis.plot([r["km"] for r in rows],[r[field.replace("up","down")] for r in rows],label="descending"); axis.legend(); axis.set_xlabel("km")
    ax[0].set_ylabel("mask rate"); ax[1].set_ylabel("end receptivity"); fig.suptitle("E06 M4 continuation-path diagnostics (smoke; noninferential)"); fig.tight_layout(); fig.savefig(path,dpi=150); plt.close(fig)
def _rss()->float:
    x=float(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss); return x/(1024**2) if sys.platform=="darwin" else x/1024

def _read_e06_csv(path:Path, fields:list[str])->list[dict[str,object]]:
    """Parse an emitted E06 table without weakening its ordered CSV schema."""
    with path.open(newline="") as handle:
        reader=csv.DictReader(handle)
        if reader.fieldnames!=fields: raise ValueError(f"E06 emitted {path.name} schema/order mismatch")
        rows=list(reader)
    if any(None in row for row in rows): raise ValueError(f"E06 emitted {path.name} contains foreign CSV fields")
    return rows

def run_e06_experiment(config_path:Path, output_dir:Path|None=None, approval_record:Path|None=None)->dict[str,Path]:
    c=load_e06_config(config_path); root=Path(__file__).resolve().parents[3]
    if c["tier"]!="smoke": raise PermissionError("E06 standard and qualification require future canonical GO records")
    if approval_record is not None: raise PermissionError("smoke accepts no approval record")
    dirs=ensure_results_dirs(output_dir or root/"results"); rid=c["run_id"]; out={"manifest":dirs["manifests"]/f"{rid}.json","raw":dirs["raw"]/f"{rid}_units.csv","cells":dirs["summaries"]/f"{rid}_cells.csv","paths":dirs["summaries"]/f"{rid}_paths.csv","loops":dirs["summaries"]/f"{rid}_loops.csv","transitions":dirs["summaries"]/f"{rid}_transitions.csv","effects":dirs["summaries"]/f"{rid}_effects.csv","figure":dirs["figures"]/f"{rid}_m4_path_diagnostics.png","report":dirs["reports"]/f"{rid}_report.md","warnings":dirs["reports"]/f"{rid}_warnings.log"}
    begun=datetime.now(timezone.utc).isoformat(); t=time.perf_counter(); rows=[]
    phase_start=t
    for s in c["scenarios"]:
        for path in s["path_types"]: rows.extend(_family(c,s,int(c["master_seed"]),path))
    simulation_seconds=time.perf_counter()-phase_start
    phase_start=time.perf_counter(); validate_e06_raw(rows,c); write_csv(out["raw"],rows); serialization_seconds=time.perf_counter()-phase_start
    phase_start=time.perf_counter(); cells,paths,loops,transitions,effects=derive_tables(rows,c); validate_e06_derived(rows,cells,paths,loops,transitions,effects,c); derived_seconds=time.perf_counter()-phase_start
    phase_start=time.perf_counter(); write_csv(out["cells"],cells); write_csv(out["paths"],paths); write_csv(out["loops"],loops); write_csv(out["transitions"],transitions); write_csv(out["effects"],effects)
    parsed_raw=_read_e06_csv(out["raw"],RAW_FIELDS); parsed_cells=_read_e06_csv(out["cells"],CELL_FIELDS); parsed_paths=_read_e06_csv(out["paths"],PATH_FIELDS); parsed_loops=_read_e06_csv(out["loops"],LOOP_FIELDS); parsed_transitions=_read_e06_csv(out["transitions"],TRANSITION_FIELDS); parsed_effects=_read_e06_csv(out["effects"],EFFECT_FIELDS)
    validate_e06_derived(parsed_raw,parsed_cells,parsed_paths,parsed_loops,parsed_transitions,parsed_effects,c)
    _figure(out["figure"],paths); figure_seconds=time.perf_counter()-phase_start
    elapsed=time.perf_counter()-t; out["warnings"].write_text("")
    raw_bytes=out["raw"].stat().st_size; total_bytes=sum(v.stat().st_size for k,v in out.items() if k not in {"manifest","report"})
    phase={"simulation":simulation_seconds,"serialization":serialization_seconds,"derived":derived_seconds,"figure":figure_seconds,"startup":0.0}
    proj=phase_separated_core_projection(c,phase,raw_bytes,total_bytes,_rss(),root)
    qratio=660000000/345600; qual={"rows":30000,"learner_steps":660000000,"method":"separate_non_authorizing_projection","seconds":simulation_seconds*qratio+serialization_seconds*(30000/320)+derived_seconds*6+figure_seconds,"raw_mib":raw_bytes*(30000/320)/1024**2,"total_mib":total_bytes*(30000/320)/1024**2,"peak_rss_mib":_rss()*1.5,"refused":True}
    out["report"].write_text(f"""# E06 canonical diagnostic-smoke report

1. **Identity and authorization.** Run `{rid}` is the frozen E06 smoke under `{config_path}`; only smoke execution is authorized.
2. **Frozen design.** It contains 320 packed rows, n=64, 120-step segments, a ceiling final window of steps 96--119, five km values, and 345,600 learner steps.
3. **Maintained M4 parity.** The E06 recorder uses maintained softmax, one acceptance draw per learner, objective reward, selected-Q update, then clipped receptivity update; replay parity is required.
4. **Packed diagnostics.** Final-window mask/authentic/accept/reject counts and objective rewards reconcile from the raw rows.
5. **Seeds and state.** Semantic segment seeds, matched reuse/isolation, traversal, p continuity, both-Q continuity, and reset controls are frozen and validated.
6. **Derived outputs.** Cells, paths, loops, transitions, and effects reconstruct from raw; smoke is decision-ineligible and smoke intervals are unavailable.
7. **Fail-closed validation.** Materialized and production parsed-CSV raw validation compare the complete reconstructed 55-field rows; adversarial coverage is recorded in the preverification index.
8. **Determinism.** Fresh-process regenerations must byte-match every scientific artifact; their comparison evidence is recorded outside this report.
9. **Resources.** Wall={elapsed:.3f}s; raw={raw_bytes} bytes; RSS={_rss():.3f} MiB. Frozen core projection={_canon(proj)}.
10. **Qualification.** Qualification projection={_canon(qual)}. Qualification is unconditionally refused.
11. **Provenance.** The manifest binds normalized config, approval, source fingerprints, Git state, schema, seed maps, and artifact hashes.
12. **Verification status.** `pending_user_full_verification`: historical user verification does not seal this corrected source; a new user-owned full verification is required.
13. **Warnings and next gate.** No C8/C9 support, bistability, or hysteresis claim is made. Standard and qualification remain unexecuted/refused; the next gate is user-owned full verification followed by fresh independent review.
""")
    status=subprocess.run(["git","-C",str(root),"status","--porcelain"],capture_output=True,text=True).stdout
    hashes={k:{"sha256":_sha(v),"bytes":v.stat().st_size} for k,v in out.items() if k!="manifest"}
    git_head=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],capture_output=True,text=True).stdout.strip()
    git_branch=subprocess.run(["git","-C",str(root),"branch","--show-current"],capture_output=True,text=True).stdout.strip()
    seed_maps={f"{row['scenario_id']}|{row['path_type']}":_strict_json(row["policy_environment_seed_map_json"]) for row in rows if row["child_id"]==0}
    output_records={}
    output_rows={"cells":len(cells),"paths":len(paths),"loops":len(loops),"transitions":len(transitions),"effects":len(effects)}
    for name,path in out.items():
        if name!="manifest": output_records[name]={"path":str(path),"rows":len(rows) if name=="raw" else output_rows.get(name),"bytes":path.stat().st_size,"sha256":_sha(path)}
    source_records=_source_records(root)
    scientific_artifacts={name:output_records[name] for name in SCIENTIFIC_OUTPUT_NAMES}
    manifest={"run_id":rid,"experiment_id":"E06","tier":"smoke","config_path":str(config_path),"normalized_config":_canon(c),"config_sha256":hashlib.sha256(_canon(c).encode()).hexdigest(),"source_fingerprint_paths":list(SOURCE_FINGERPRINT_PATHS),"source_fingerprints":source_records,"source_fingerprint_sha256":_source_fingerprint_from_records(source_records),"authorization":{"approval_path":str(root/"projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md"),"approval_sha256":_sha(root/"projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md"),"standard_execution":"refused","qualification_execution":"refused"},"parameters":c,"command":f"PYTHONPATH=src {sys.executable} -m gifted_masking.cli article-experiment --config {config_path} --output-dir {output_dir or root/'results'}","environment":{"python":sys.version,"platform":platform.platform(),"numpy":np.__version__,"matplotlib":__import__('matplotlib').__version__},"git":{"head":git_head,"branch":git_branch,"dirty":bool(status),"porcelain_sha256":hashlib.sha256(status.encode()).hexdigest()},"seed_hierarchy":{"segment_derivation":"SHA-256 semantic ID -> SeedSequence([master,6,*little_endian_words]).spawn(1)","bootstrap_derivation":"SHA-256 scenario/response/target ID -> SeedSequence([bootstrap_seed,60,*little_endian_words]).spawn(1)","complete_segment_seed_maps":seed_maps},"schemas":{"raw":RAW_FIELDS,"cell":CELL_FIELDS,"path":PATH_FIELDS,"loop":LOOP_FIELDS,"transition":TRANSITION_FIELDS,"effect":EFFECT_FIELDS,"sort_keys":["master_seed","scenario_id","path_type","child_id"]},"derived_validation":{"status":"passed","interface":"validate_e06_derived(raw_rows,cells,paths,loops,transitions,effects,config)","materialized":"passed","post_artifact_parsed_csv":"passed","tolerance":1e-12,"streaming_validation":"not_applicable_materialized_packed_rows","streaming_reason":"projected raw and peak RSS remain within frozen limits; no streaming writer exists"},"outputs":output_records,"scientific_artifacts":scientific_artifacts,"output_hashes":hashes,"timing":{"wall_seconds":elapsed,"peak_rss_mib":_rss(),"raw_bytes":raw_bytes,"phase_seconds":phase},"standard_projection":proj,"qualification_projection":qual,"focused_verification":{"status":"pending_external_focused_logs"},"deterministic_regeneration":{"status":"pending_external_fresh_runs"},"warnings":[],"verification":{"status":"pending_user_full_verification","full_verification_command":"MPLCONFIGDIR=/private/tmp/e06_user_verify_round2 ./scripts/verify.sh","seal_state":"unsealed"},"timestamps":{"start_utc":begun,"end_utc":datetime.now(timezone.utc).isoformat()}}
    write_json(out["manifest"],manifest); return out

def normalize_e06_machine_artifacts(out:dict[str,Path])->dict[str,str]:
    r={k:v.read_text() for k,v in out.items() if k not in {"figure","report","warnings"}}
    m=json.loads(r["manifest"]); m["timing"]="NORMALIZED";m["timestamps"]="NORMALIZED";m["output_hashes"]="NORMALIZED";m["git"]="NORMALIZED";m["command"]="NORMALIZED";m["standard_projection"]="NORMALIZED";m["qualification_projection"]="NORMALIZED";m["outputs"]={k:{**v,"path":k} for k,v in m["outputs"].items()};r["manifest"]=_canon(m);return r

def normalize_e06_report(path:Path)->str:
    """Compare reports without hiding science, seed, or decision content."""
    text=path.read_text()
    text=re.sub(r"Wall=[^\n]*?Frozen core projection=", "Wall=NORMALIZED; Frozen core projection=", text)
    text=re.sub(r"\{\"learner_steps\":913000000.*?\}\.", "NORMALIZED.", text)
    text=re.sub(r"Qualification projection=\{.*?\}\.", "Qualification projection=NORMALIZED.", text)
    return text

EXPECTED_USER_FULL_COMMAND="MPLCONFIGDIR=/private/tmp/e06_user_verify_round2 ./scripts/verify.sh"
EXPECTED_WORKSPACE_PYTHON="/Users/omer/workspace/venvs/venv314/bin/python"
EXPECTED_FULL_VERIFICATION_SUITES=(
    "repository_discovery", "manifest_completeness", "primary_raw_schema", "summary_matches_raw",
)
SCIENTIFIC_OUTPUT_NAMES=("raw", "cells", "paths", "loops", "transitions", "effects", "figure", "warnings")
FOCUSED_EVIDENCE_ORDER=("E06", "M4", "core_and_determinism", "post_artifact")
EXPECTED_FOCUSED_COMMANDS={
    "E06":"MPLCONFIGDIR=/private/tmp/e06_second_fix_mpl PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m unittest tests/test_article_e06.py -v",
    "M4":"MPLCONFIGDIR=/private/tmp/e06_second_fix_mpl PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m unittest tests/test_m4.py -v",
    "core_and_determinism":"MPLCONFIGDIR=/private/tmp/e06_second_fix_mpl PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m unittest tests/test_core.py tests/test_determinism.py -v",
    "post_artifact":"MPLCONFIGDIR=/private/tmp/e06_second_fix_mpl PYTHONPATH=src /Users/omer/workspace/venvs/venv314/bin/python -m unittest tests/test_manifest_completeness.py tests/test_primary_raw_schema.py tests/test_summary_matches_raw.py -v",
}
NONDETERMINISTIC_NORMALIZATION_RULES=(
    "manifest.timing", "manifest.timestamps", "manifest.git", "manifest.standard_projection", "manifest.qualification_projection",
    "manifest.command output-root only", "manifest.outputs.*.path output-root only", "manifest.outputs.report bytes/sha256", "manifest.output_hashes.report",
    "report item 9 runtime/projection", "report item 10 qualification projection",
)

def _sha_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()

def _parse_exit_record(path: Path) -> int:
    """Accept one and only one canonical, newline-terminated zero exit record."""
    try:
        payload=path.read_bytes()
    except OSError as exc:
        raise ValueError("external verification exit record is unavailable") from exc
    if payload != b"verification_exit_code=0\n":
        raise ValueError("external verification exit record is not exactly verification_exit_code=0\\n")
    return 0

def _parse_full_verification_log(path: Path) -> list[dict[str, object]]:
    """Reconstruct full-verification suite outcomes from the authoritative log."""
    try:
        text=path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError("external verification log is unavailable or not UTF-8") from exc
    python_lines=re.findall(rf"(?m)^Verification Python: {re.escape(EXPECTED_WORKSPACE_PYTHON)}$",text)
    if len(python_lines)!=1:
        raise ValueError("verification log does not name the exact workspace Python exactly once")
    if re.search(r"(?im)^(?:FAILED|ERROR|Traceback)\b|\buncaught exception\b|\bfailure summary\b",text):
        raise ValueError("verification log contains a failed or errored termination")
    matches=list(re.finditer(r"(?m)^Ran ([1-9][0-9]*) tests? in ([0-9]+(?:\.[0-9]+)?)s\n\nOK$",text))
    if len(matches)!=len(EXPECTED_FULL_VERIFICATION_SUITES):
        raise ValueError("verification log has missing, extra, or incomplete suite completion records")
    suites=[]
    for expected_name,match in zip(EXPECTED_FULL_VERIFICATION_SUITES,matches,strict=True):
        runtime=float(match.group(2))
        if not math.isfinite(runtime) or runtime<0:
            raise ValueError("verification log contains an invalid suite runtime")
        suites.append({"name":expected_name,"test_count":int(match.group(1)),"runtime_seconds":runtime,"passed":True})
    return suites

def _parse_focused_log(path: Path, command: str) -> dict[str, object]:
    """Bind each focused log to one exact command and successful unittest result."""
    try:
        text=path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise ValueError("focused verification log is unavailable or not UTF-8") from exc
    if not text.startswith(f"command={command}\n") or re.search(r"(?m)^exit_code=0$",text) is None:
        raise ValueError("focused verification log command or exit record is invalid")
    matches=list(re.finditer(r"(?m)^Ran ([1-9][0-9]*) tests? in ([0-9]+(?:\.[0-9]+)?)s\n\nOK$",text))
    if len(matches)!=1 or re.search(r"(?im)^(?:FAILED|ERROR|Traceback)\b|\buncaught exception\b",text):
        raise ValueError("focused verification log is incomplete or failed")
    runtime=float(matches[0].group(2))
    if not math.isfinite(runtime) or runtime<0:
        raise ValueError("focused verification runtime is invalid")
    return {"test_count":int(matches[0].group(1)),"runtime_seconds":runtime,"passed":True}

def _source_records(root: Path) -> list[dict[str, str]]:
    return [{"path":relative,"sha256":_sha(root/relative)} for relative in SOURCE_FINGERPRINT_PATHS]

def _source_fingerprint_from_records(records: list[dict[str, str]]) -> str:
    digest=hashlib.sha256()
    for record in records:
        digest.update(record["path"].encode()); digest.update(b"\0"); digest.update(bytes.fromhex(record["sha256"])); digest.update(b"\0")
    return digest.hexdigest()

def _package_root(manifest: dict[str, object]) -> Path:
    config_path=manifest.get("config_path")
    if type(config_path) is not str:
        raise ValueError("pending package has no config path")
    return Path(config_path).resolve().parents[2]

def _require_exact_pending_binding(manifest: dict[str, object], *, include_preverification: bool) -> None:
    """Recompute every pending-package binding before its evidence is trusted."""
    root=_package_root(manifest)
    config_path=Path(str(manifest["config_path"]))
    config=load_e06_config(config_path)
    normalized=_canon(config); approval=root/"projects/frontiers_article/approvals/E06_SMOKE_APPROVAL.md"
    if manifest.get("normalized_config")!=normalized or manifest.get("config_sha256")!=_sha_bytes(normalized.encode()):
        raise ValueError("pending package config binding drift")
    authorization=manifest.get("authorization")
    if type(authorization) is not dict or authorization.get("approval_path")!=str(approval) or authorization.get("approval_sha256")!=_sha(approval):
        raise ValueError("pending package approval binding drift")
    records=manifest.get("source_fingerprints")
    expected_records=_source_records(root)
    if records!=expected_records or manifest.get("source_fingerprint_paths")!=list(SOURCE_FINGERPRINT_PATHS) or manifest.get("source_fingerprint_sha256")!=_source_fingerprint_from_records(expected_records):
        raise ValueError("pending package source-fingerprint binding drift")
    head=subprocess.run(["git","-C",str(root),"rev-parse","HEAD"],capture_output=True,text=True,check=True).stdout.strip()
    branch=subprocess.run(["git","-C",str(root),"branch","--show-current"],capture_output=True,text=True,check=True).stdout.strip()
    porcelain=subprocess.run(["git","-C",str(root),"status","--porcelain"],capture_output=True,text=True,check=True).stdout
    git=manifest.get("git")
    if type(git) is not dict or git!={"head":head,"branch":branch,"dirty":bool(porcelain),"porcelain_sha256":_sha_bytes(porcelain.encode())}:
        raise ValueError("pending package Git binding drift")
    outputs=manifest.get("outputs")
    scientific=manifest.get("scientific_artifacts")
    if type(outputs) is not dict or type(scientific) is not dict or set(scientific)!=set(SCIENTIFIC_OUTPUT_NAMES):
        raise ValueError("pending package scientific artifact inventory is incomplete")
    for name in SCIENTIFIC_OUTPUT_NAMES:
        record=scientific[name]
        if type(record) is not dict or record!=outputs.get(name):
            raise ValueError(f"pending package scientific artifact record drift: {name}")
        path=Path(str(record.get("path","")))
        if not path.is_file() or record.get("bytes")!=path.stat().st_size or record.get("sha256")!=_sha(path):
            raise ValueError(f"pending scientific artifact drift: {name}")
    report=Path(str(outputs.get("report",{}).get("path","")))
    if not report.is_file() or outputs["report"].get("bytes")!=report.stat().st_size or outputs["report"].get("sha256")!=_sha(report):
        raise ValueError("pending report binding drift")
    verification=manifest.get("verification")
    if type(verification) is not dict or verification.get("status")!="pending_user_full_verification" or verification.get("seal_state")!="unsealed":
        raise ValueError("canonical package is not consistently pending for external sealing")
    if include_preverification:
        _validate_focused_evidence(manifest.get("focused_verification"))
        _validate_deterministic_evidence(manifest.get("deterministic_regeneration"))

def _validate_focused_evidence(evidence: object) -> None:
    if type(evidence) is not dict or set(evidence)!={"status","records"} or evidence["status"]!="passed" or type(evidence["records"]) is not list:
        raise ValueError("focused verification evidence is missing or inconsistent")
    records=evidence["records"]
    if [record.get("name") if type(record) is dict else None for record in records] != list(FOCUSED_EVIDENCE_ORDER):
        raise ValueError("focused verification evidence is missing, duplicated, foreign, or reordered")
    for record in records:
        if set(record)!={"name","command","log_path","log_sha256","exit_code","test_count","runtime_seconds","passed"} or record["exit_code"]!=0:
            raise ValueError("focused verification evidence schema is invalid")
        if record["command"]!=EXPECTED_FOCUSED_COMMANDS[record["name"]]:
            raise ValueError("focused verification command differs from the contractual command")
        path=Path(str(record["log_path"]))
        if not path.is_file() or record["log_sha256"]!=_sha(path):
            raise ValueError("focused verification log hash drift")
        parsed=_parse_focused_log(path,str(record["command"]))
        if parsed["test_count"]!=record["test_count"] or parsed["runtime_seconds"]!=record["runtime_seconds"] or record["passed"] is not True:
            raise ValueError("focused verification caller count/runtime/status disagrees with log")

def _normalize_manifest_for_deterministic_comparison(path: Path) -> str:
    manifest=_strict_json(path.read_text())
    if type(manifest) is not dict:
        raise ValueError("deterministic manifest is not an object")
    for key in ("timing","timestamps","git","standard_projection","qualification_projection"):
        manifest[key]="NORMALIZED_NONDETERMINISTIC"
    manifest["command"]="NORMALIZED_OUTPUT_ROOT_ONLY"
    outputs=manifest.get("outputs")
    if type(outputs) is not dict:
        raise ValueError("deterministic manifest has no outputs")
    for name,record in outputs.items():
        if type(record) is not dict:
            raise ValueError("deterministic manifest output record is invalid")
        record["path"]=name
        if name=="report":
            record["bytes"]="NORMALIZED_REPORT_RUNTIME_BYTES"; record["sha256"]="NORMALIZED_REPORT_RUNTIME_SHA256"
    hashes=manifest.get("output_hashes")
    if type(hashes) is not dict:
        raise ValueError("deterministic manifest has no output hashes")
    hashes["report"]="NORMALIZED_REPORT_RUNTIME_SHA256"
    scientific=manifest.get("scientific_artifacts")
    if type(scientific) is not dict:
        raise ValueError("deterministic manifest has no scientific artifact inventory")
    for name,record in scientific.items():
        if type(record) is not dict:
            raise ValueError("deterministic scientific artifact record is invalid")
        record["path"]=name
    return _canon(manifest)

def _validate_deterministic_evidence(evidence: object) -> None:
    required={"status","runs","scientific_byte_comparison","normalized_manifest_report","normalization_rules"}
    if type(evidence) is not dict or set(evidence)!=required or evidence["status"]!="passed" or evidence["scientific_byte_comparison"]!="passed" or evidence["normalized_manifest_report"]!="passed" or evidence["normalization_rules"]!=list(NONDETERMINISTIC_NORMALIZATION_RULES):
        raise ValueError("deterministic-regeneration evidence is missing or inconsistent")
    runs=evidence["runs"]
    if type(runs) is not list or len(runs)!=2:
        raise ValueError("deterministic-regeneration evidence must name exactly two fresh runs")
    normalized=[]; reports=[]; scientific=[]
    for run in runs:
        if type(run) is not dict or set(run)!={"manifest_path","report_path","scientific_artifacts"}:
            raise ValueError("deterministic-regeneration run record is invalid")
        manifest_path=Path(str(run["manifest_path"])); report_path=Path(str(run["report_path"]))
        if not manifest_path.is_file() or not report_path.is_file() or type(run["scientific_artifacts"]) is not dict or set(run["scientific_artifacts"])!=set(SCIENTIFIC_OUTPUT_NAMES):
            raise ValueError("deterministic-regeneration run evidence is incomplete")
        normalized.append(_normalize_manifest_for_deterministic_comparison(manifest_path)); reports.append(normalize_e06_report(report_path)); scientific.append(run["scientific_artifacts"])
        for name,record in run["scientific_artifacts"].items():
            path=Path(str(record.get("path","")))
            if not path.is_file() or record.get("bytes")!=path.stat().st_size or record.get("sha256")!=_sha(path):
                raise ValueError(f"deterministic-regeneration artifact drift: {name}")
    scientific_identity=[{name:{"bytes":record["bytes"],"sha256":record["sha256"]} for name,record in inventory.items()} for inventory in scientific]
    if normalized[0]!=normalized[1] or reports[0]!=reports[1] or scientific_identity[0]!=scientific_identity[1]:
        raise ValueError("deterministic-regeneration comparison no longer matches")

def _atomic_package_write(updates: dict[Path, bytes]) -> None:
    """Stage both package documents before replacement and roll back a write failure."""
    originals={path:path.read_bytes() for path in updates}
    temporaries={path:path.with_name(path.name+".e06tmp") for path in updates}
    try:
        for path,temporary in temporaries.items():
            temporary.write_bytes(updates[path])
        replaced=[]
        try:
            for path,temporary in temporaries.items():
                temporary.replace(path); replaced.append(path)
        except Exception:
            for path in replaced:
                path.write_bytes(originals[path])
            raise
    finally:
        for temporary in temporaries.values():
            if temporary.exists(): temporary.unlink()

def _replace_report_item_12(report: str, replacement: str) -> str:
    result,count=re.subn(r"(?m)^12\. .*?$",replacement,report,count=1)
    if count!=1:
        raise ValueError("canonical report does not contain exactly one item 12")
    return result

def _update_report_hash(manifest: dict[str, object], report_bytes: bytes) -> None:
    outputs=manifest.get("outputs")
    hashes=manifest.get("output_hashes")
    if type(outputs) is not dict or type(hashes) is not dict or type(outputs.get("report")) is not dict:
        raise ValueError("canonical manifest cannot bind its report")
    outputs["report"]["bytes"]=len(report_bytes); outputs["report"]["sha256"]=_sha_bytes(report_bytes)
    hashes["report"]={"sha256":_sha_bytes(report_bytes),"bytes":len(report_bytes)}

def record_e06_preverification(out: dict[str, Path], focused: dict[str, object], deterministic: dict[str, object]) -> None:
    """Complete a pending package with independently checked preverification evidence."""
    manifest=_strict_json(out["manifest"].read_text())
    if type(manifest) is not dict:
        raise ValueError("canonical manifest is not an object")
    _require_exact_pending_binding(manifest,include_preverification=False)
    _validate_focused_evidence(focused); _validate_deterministic_evidence(deterministic)
    updated=dict(manifest); updated["focused_verification"]=focused; updated["deterministic_regeneration"]=deterministic
    report_path=out["report"]; report=_replace_report_item_12(report_path.read_text(),"12. **Verification status.** Focused verification and deterministic-regeneration evidence are validated in the pending package; `pending_user_full_verification` remains required before an external seal.")
    report_bytes=report.encode(); _update_report_hash(updated,report_bytes)
    manifest_bytes=(json.dumps(updated,indent=2,allow_nan=False)+"\n").encode()
    _atomic_package_write({out["manifest"]:manifest_bytes,report_path:report_bytes})

def build_e06_full_verification_evidence(log_path: Path, exit_path: Path) -> dict[str, object]:
    """Build, rather than trust, external verification totals from its immutable files."""
    suites=_parse_full_verification_log(log_path); _parse_exit_record(exit_path)
    return {"command":EXPECTED_USER_FULL_COMMAND,"log_path":str(log_path),"log_sha256":_sha(log_path),"exit_path":str(exit_path),"exit_sha256":_sha(exit_path),"suites":suites,"test_count":sum(int(item["test_count"]) for item in suites),"runtime_seconds":math.fsum(float(item["runtime_seconds"]) for item in suites)}

def seal_e06_verification(out:dict[str,Path], evidence:dict[str,object]) -> None:
    """Seal only a fully bound pending package from strictly parsed external evidence."""
    manifest=_strict_json(out["manifest"].read_text())
    if type(manifest) is not dict:
        raise ValueError("canonical manifest is not an object")
    _require_exact_pending_binding(manifest,include_preverification=True)
    required={"command","log_path","log_sha256","exit_path","exit_sha256","suites","test_count","runtime_seconds"}
    if type(evidence) is not dict or set(evidence)!=required or evidence["command"]!=EXPECTED_USER_FULL_COMMAND:
        raise ValueError("external seal evidence is incomplete or has the wrong command")
    log=Path(str(evidence["log_path"])); exit_record=Path(str(evidence["exit_path"]))
    if not log.is_file() or not exit_record.is_file() or evidence["log_sha256"]!=_sha(log) or evidence["exit_sha256"]!=_sha(exit_record):
        raise ValueError("external verification evidence hash mismatch")
    parsed=_parse_full_verification_log(log); _parse_exit_record(exit_record)
    if evidence["suites"]!=parsed or type(evidence["test_count"]) is not int or evidence["test_count"]!=sum(int(item["test_count"]) for item in parsed) or type(evidence["runtime_seconds"]) is not float or not math.isfinite(evidence["runtime_seconds"]) or evidence["runtime_seconds"]!=math.fsum(float(item["runtime_seconds"]) for item in parsed):
        raise ValueError("external verification caller count/runtime evidence disagrees with parsed log")
    # Freshness is supplementary.  Content hashes above are the integrity binding.
    latest_source=max(((_package_root(manifest)/relative).stat().st_mtime for relative in SOURCE_FINGERPRINT_PATHS),default=0.0)
    if latest_source>min(log.stat().st_mtime,exit_record.stat().st_mtime):
        raise ValueError("verification evidence is stale relative to fingerprinted source")
    updated=dict(manifest)
    updated["verification"]={"status":"passed","seal_state":"external_evidence_verified","command":evidence["command"],"log_path":str(log),"log_sha256":evidence["log_sha256"],"exit_path":str(exit_record),"exit_sha256":evidence["exit_sha256"],"suites":parsed,"test_count":evidence["test_count"],"runtime_seconds":evidence["runtime_seconds"]}
    suite_text=", ".join(f"{item['name']}={item['test_count']} tests/{item['runtime_seconds']:.3f}s" for item in parsed)
    report_path=out["report"]; report=_replace_report_item_12(report_path.read_text(),f"12. **Verification status.** External seal verified `{evidence['command']}`; log SHA-256 `{evidence['log_sha256']}`, exit SHA-256 `{evidence['exit_sha256']}`, parsed suites: {suite_text}; external-seal status `passed`.")
    report_bytes=report.encode(); _update_report_hash(updated,report_bytes)
    manifest_bytes=(json.dumps(updated,indent=2,allow_nan=False)+"\n").encode()
    _atomic_package_write({out["manifest"]:manifest_bytes,report_path:report_bytes})
