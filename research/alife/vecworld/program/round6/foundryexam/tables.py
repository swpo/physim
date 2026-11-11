"""tables -- study foundryexam: the README's tables as markdown from results/analysis*.json (CPU, instant).

    python -B tables.py [--analysis results/analysis.json] [--other results/analysis_job003.json]

With --other, a between-job table is added for arm P (the same hidden worlds; other items, Labs and training seeds).
"""
from __future__ import annotations

import argparse
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ARMS = ("P", "N30", "N10")
POL = [("O", "O: simulator from the hidden state"), ("C", "C: net at the true weights (the ceiling)"),
       ("Cscratch", "the other ceiling candidate"), ("Cft", "the other ceiling candidate (fine-tuned P0)"),
       ("Csm", "C on 1,024 episodes only"), ("FT@512", "FT(512): P0 fine-tuned on 512 Lab episodes"),
       ("FT@128", "FT(128)"), ("FT@32", "FT(32)"), ("FT@8", "FT(8)"), ("D@512", "D(512): net on 512 Lab episodes alone"),
       ("D@128", "D(128)"), ("D@32", "D(32)"), ("D@8", "D(8)"), ("Dr@512", "Dr(512): local ridge on 512 Lab episodes"),
       ("Dr@8", "Dr(8): local ridge on 8 Lab episodes"), ("S@512", "S(512): amortised inference from 512 Lab episodes"),
       ("S@8", "S(8)"), ("S@0", "S(0): the amortised net without a Lab"), ("P0", "P0: prior simulations, own history"),
       ("P0s", "P0s: prior simulations, last two frames"), ("P0w64", "P0[64]: 64 prior worlds"),
       ("P0w16", "P0[16]: 16 prior worlds"), ("Kp", "persistence"), ("K", "K: climatology")]


def v(q, d=3):
    return f"{q['value']:.{d}f} ± {q['se']:.{d}f}"


def iv(q, d=3):
    return f"{q['value']:.{d}f} [{q['p05']:.{d}f}, {q['p95']:.{d}f}]"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--analysis", default=os.path.join(HERE, "results", "analysis.json"))
    ap.add_argument("--other", default=None)
    a = ap.parse_args()
    A = json.load(open(a.analysis))["arms"]
    arms = [x for x in ARMS if x in A]
    print(f"job {json.load(open(a.analysis))['job']}\n")
    print("| policy | " + " | ".join(f"arm {x}" for x in arms) + " |")
    print("|---|" + "---|" * len(arms))
    for b, name in POL:
        cells = []
        for x in arms:
            T = A[x]["table"]
            cells.append("1" if b == "O" else "0" if b == "K" else (v(T[b]["oes_pooled"]) if b in T else "-"))
        if any(c != "-" for c in cells):
            print(f"| {name} | " + " | ".join(cells) + " |")
    print()
    rows = [("hidden worlds (training worlds of P0)", lambda R: f"{R['n_hidden']} ({', '.join(str(n) for n in R['train_worlds'])})"),
            ("ceiling C is", lambda R: R["ceiling_is"]),
            ("share of C's skill with no hypothesis and no experiment", lambda R: iv(R["acceptance"]["share_noexp"])),
            ("  median over hidden worlds", lambda R: f"{R['acceptance']['share_noexp']['median_world']:.3f}"),
            ("  verdict (criterion 2)", lambda R: R["acceptance"]["trivial_verdict"]),
            ("sigma with no Lab", lambda R: iv(R["acceptance"]["sigma_no_lab"])),
            ("sigma at 8 Lab episodes", lambda R: iv(R["acceptance"]["sigma_by_budget"]["8"])),
            ("sigma at 32", lambda R: iv(R["acceptance"]["sigma_by_budget"]["32"])),
            ("sigma at 128", lambda R: iv(R["acceptance"]["sigma_by_budget"]["128"])),
            ("sigma at 512 (the declared null)", lambda R: iv(R["acceptance"]["sigma"])),
            ("  null policy; verdict against 0.15", lambda R: f"{R['acceptance']['null_is']}; {R['acceptance']['sigma_verdict']}"),
            ("rho of amortised S at 8 / 512", lambda R: f"{v(R['acceptance']['rho']['8'], 2)} / {v(R['acceptance']['rho']['512'], 2)}"),
            ("share of the P0-to-C gap closed by FT at 8 / 32 / 128 / 512",
             lambda R: " / ".join(f"{R['acceptance']['rho_finetune'][n]['value']:.2f}" for n in ("8", "32", "128", "512"))),
            ("C - P0 (pooled skill)", lambda R: v(R["gaps_oes"]["C - P0"])),
            ("P0 - P0s (reading the world off the history)", lambda R: v(R["gaps_oes"]["P0 - P0s"])),
            ("O - C (out of reach of a history-only net)", lambda R: v(R["gaps_oes"]["O - C"])),
            ("C - Csm (convergence of C in data)", lambda R: v(R["gaps_oes"]["C - Csm"]) if "C - Csm" in R["gaps_oes"] else
             (v(R["gaps_oes"]["Cscratch - Csm"]) + " (scratch)" if "Cscratch - Csm" in R["gaps_oes"] else "-")),
            ("data-only (better of D, Dr): Lab episodes for 90% of C", lambda R: _n(R["budgets"].get("N90_data_only"))),
            ("data-only: Lab episodes to match P0", lambda R: _n(R["budgets"].get("N_P0_data_only"))),
            ("state-given loss, weights from the prior (median world)",
             lambda R: f"{iv(R['state_given_loss']['plugPrior'], 2)} ({R['state_given_loss']['plugPrior']['median_world']:.2f})"),
            ("state-given loss, weights off by eps 0.03 / 0.1 / 0.3",
             lambda R: " / ".join(f"{R['state_given_loss'][k]['value']:.2f}" for k in ("plug03", "plug10", "plug30"))),
            ("input-blind oracle loss, items with a program", lambda R: iv(R["actions"]["classes_bcd"])),
            ("  by class: blind / aimed / regional", lambda R: " / ".join(f"{R['actions']['class_' + c]['value']:.3f}" for c in "bcd")),
            ("  verdict (criterion 4); worlds at 0.10 or more", lambda R: f"{R['actions']['verdict']}; {R['actions']['worlds_at_least_0p10']} of {R['n_hidden']}"),
            ("tick-alone share of variance, largest world", lambda R: f"{R['stationarity']['all33_max']:.1e}")]
    print("| quantity | " + " | ".join(f"arm {x}" for x in arms) + " |")
    print("|---|" + "---|" * len(arms))
    for name, f in rows:
        cells = []
        for x in arms:
            try:
                cells.append(f(A[x]))
            except (KeyError, TypeError):
                cells.append("-")
        print(f"| {name} | " + " | ".join(cells) + " |")
    print()
    print("| kind of net | " + " | ".join(f"arm {x}: converged / nets (largest late share), median best step / steps" for x in arms) + " |")
    print("|---|" + "---|" * len(arms))
    kinds = ["P0", "A", "P0s", "C", "Cft", "Csm", "D@512 s0", "FT@512 s0", "D@128 s0", "FT@128 s0", "D@32 s0", "FT@32 s0", "D@8 s0", "FT@8 s0"]
    for k in kinds:
        cells = []
        for x in arms:
            cv = A[x]["convergence"]
            e = cv.get(k) or cv.get(f"{x} {k}")
            cells.append("-" if e is None else f"{e['ok']} / {e['nets']} ({e['late_share_max']:.3f}), {e['best_step_median']:.0f} / {e['steps']}")
        print(f"| {k.replace(' s0', '')} | " + " | ".join(cells) + " |")
    if a.other:
        B = json.load(open(a.other))["arms"]
        print(f"\nbetween jobs, arm P (this job, other job {json.load(open(a.other))['job']}):\n")
        print("| policy | this job | other job | difference |")
        print("|---|---|---|---|")
        for b, name in POL:
            if b in A["P"]["table"] and b in B["P"]["table"]:
                x, y = A["P"]["table"][b]["oes_pooled"], B["P"]["table"][b]["oes_pooled"]
                print(f"| {b} | {v(x)} | {v(y)} | {x['value'] - y['value']:+.3f} |")
        for nm in ("share_noexp", "sigma", "sigma_no_lab"):
            x, y = A["P"]["acceptance"][nm], B["P"]["acceptance"][nm]
            print(f"| {nm} | {v(x)} | {v(y)} | {x['value'] - y['value']:+.3f} |")


def _n(x):
    return "-" if x is None else (x if isinstance(x, str) else f"{x:.0f}")


if __name__ == "__main__":
    main()
