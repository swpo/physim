"""Render a scientific cost/reward figure from audited, completed campaign rows.

This writes review artifacts only. It never launches evaluations or publishes.
Run campaign_results.py first to refresh the verified input snapshot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, LogLocator

WORLDS = ("bf", "xv", "p4g2_044")
NAMES = {
    "z-ai/glm-5.3-flash": "GLM 5.3 Flash",
    "qwen/qwen3.5-35b-a3b": "Qwen 3.5 35B A3B",
    "qwen/qwen3.5-397b-a17b": "Qwen 3.5 397B A17B",
    "openai/gpt-5.6-luna": "GPT 5.6 Luna",
    "openai/gpt-5.6-terra": "GPT 5.6 Terra",
    "anthropic/claude-sonnet-5": "Claude Sonnet 5",
    "google/gemini-3.8-flash": "Gemini 3.8 Flash",
    "x-ai/grok-4.6": "Grok 4.6",
    "deepseek/deepseek-v4.1-flash": "DeepSeek V4.1 Flash",
    "moonshotai/kimi-k2.6": "Kimi K2.6",
}
STYLES = {
    "z-ai": ("#7551a8", "o"),
    "qwen": ("#2563a6", "s"),
    "deepseek": ("#16817d", "D"),
    "moonshotai": ("#b57713", "^"),
    "openai": ("#21834d", "P"),
    "anthropic": ("#a3633d", "h"),
    "google": ("#cb543d", "v"),
    "x-ai": ("#4c5461", "X"),
}
BASELINES = {
    "initial_persistence": "Persist initial readings",
    "ignore_actions": "Native dynamics, no interventions",
    "independent_native": "Native dynamics, correct interventions",
    "remove_feedback": "Native dynamics, shared feedback removed",
    "wrong_probe_geometry": "Native dynamics, incorrect sensor geometry",
}


def review_data(campaign: Path, selected_baselines: list[str]):
    if (campaign / "HOLD.json").exists():
        raise ValueError("Campaign results are held; review HOLD.json before rendering scores")
    paths = [campaign / name for name in ("results.json", "baselines.json")]
    result, controls = [json.loads(path.read_text()) for path in paths]
    if not result["models"]:
        raise ValueError("No model has completed all three worlds; no aggregate figure can be drawn")
    references = {row["world"]: row["references"] for row in controls["worlds"]}
    for row in result["rows"]:
        if row["bundle_references"] != references[row["world"]]:
            raise ValueError("Model and baseline bundle identities differ")
    for model in result["models"]:
        if set(model["worlds"]) != set(WORLDS) or model["mean_cost_usd"] <= 0:
            raise ValueError("Plot requires all three worlds and a positive measured inference cost")
    lines = [
        {"id": name, "label": BASELINES[name], "reward": controls["mean_rewards"][name]} for name in selected_baselines
    ]
    return {
        "models": result["models"],
        "baselines": lines,
        "rows": result["rows"],
        "incomplete_models": result["incomplete_models"],
        "pending_cost_models": result.get("pending_cost_models", []),
        "excluded_attempts": result["excluded_attempts"],
        "sources": [{"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()} for path in paths],
        "aggregation": result["aggregation"],
        "cost": result["cost"],
        "baseline_forecast_members": controls["stochastic_forecast_members"],
        "truth_members": controls["truth_members"],
    }


def frontier(models):
    """Keep nondominated cost/reward points; ties at a cost keep the best reward."""
    kept, best = [], float("-inf")
    for model in sorted(models, key=lambda m: (m["mean_cost_usd"], -m["mean_reward"])):
        if model["mean_reward"] > best:
            kept.append(model)
            best = model["mean_reward"]
    return kept


def draw(data, output: Path, narrow=False):
    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 11,
            "svg.fonttype": "none",
            "axes.labelcolor": "#192833",
            "text.color": "#192833",
            "axes.edgecolor": "#81909a",
        }
    )
    fig, ax = plt.subplots(figsize=(6.0, 5.5) if narrow else (10.0, 5.5))
    fig.subplots_adjust(left=0.14 if narrow else 0.09, right=0.96, bottom=0.16, top=0.96)
    models = data["models"]
    families = defaultdict(list)
    for model in models:
        families[model["model"].split("/")[0]].append(model)
    xs = [m["mean_cost_usd"] for m in models]
    ys = [m["mean_reward"] for m in models] + [b["reward"] for b in data["baselines"]]
    ax.set_xscale("log")
    ax.set_xlim(min(xs) / 1.7, max(xs) * (2.3 if narrow else 1.9))
    ax.set_ylim(max(0, min(ys) - 0.08), min(1, max(ys) + 0.10))
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#e5e9ed", linewidth=0.7)
    for index, baseline in enumerate(data["baselines"]):
        ax.axhline(
            baseline["reward"],
            color="#69767e",
            linewidth=1,
            linestyle=(0, (5, 3) if index % 2 == 0 else (2, 3)),
            zorder=1,
        )
        label = baseline["label"]
        if narrow and len(label) > 30:
            label = label.replace(", ", ",\n")
        ax.annotate(
            label,
            (0.02, baseline["reward"]),
            xycoords=("axes fraction", "data"),
            xytext=(0, 6),
            textcoords="offset points",
            fontsize=9,
            color="#59666e",
        )
    efficient = frontier(models)
    if len(efficient) > 1:
        ax.plot(
            [m["mean_cost_usd"] for m in efficient],
            [m["mean_reward"] for m in efficient],
            color="#a6afb5",
            linestyle=":",
            linewidth=1.2,
            zorder=2,
        )
    for family, members in families.items():
        color, marker = STYLES.get(family, ("#475569", "o"))
        members.sort(key=lambda m: m["mean_cost_usd"])
        ax.plot(
            [m["mean_cost_usd"] for m in members],
            [m["mean_reward"] for m in members],
            color=color,
            marker=marker,
            markersize=8,
            linewidth=1.5,
            zorder=3,
        )
    # Label placement is checked against the rendered evidence for each release.
    # Alternating offsets provide a starting point; do not shrink labels to fit.
    for index, model in enumerate(sorted(models, key=lambda m: m["mean_cost_usd"])):
        label = NAMES.get(model["model"], model["model"].split("/")[-1])
        if narrow:
            label = label.replace(" 35B", "\n35B").replace("V4.1 Flash", "V4.1\nFlash")
        ax.annotate(
            label,
            (model["mean_cost_usd"], model["mean_reward"]),
            xytext=(8, 12 if index % 2 == 0 else -24),
            textcoords="offset points",
            fontsize=10,
            ha="left",
            va="center",
        )
    ax.xaxis.set_major_locator(LogLocator(base=10, subs=(1, 2, 5)))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _: f"${value:g}"))
    ax.set_xlabel("Mean inference cost per rollout (USD, log scale)", labelpad=12)
    ax.set_ylabel("Mean reward across three worlds ↑", labelpad=10)
    name = "reward-cost-mobile" if narrow else "reward-cost"
    for suffix in ("svg", "png"):
        fig.savefig(output / f"{name}.{suffix}", dpi=180, facecolor="white")
    plt.close(fig)


def report(data):
    lines = [
        "# Evaluation campaign results",
        "",
        data["aggregation"],
        "",
        "| Model | Mean reward | Mean cost | BF | XV | p4g2_044 | Repetitions per world |",
        "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for model in sorted(data["models"], key=lambda m: m["mean_cost_usd"]):
        worlds = model["worlds"]
        values = [
            NAMES.get(model["model"], model["model"]),
            f"{model['mean_reward']:.3f}",
            f"${model['mean_cost_usd']:.3f}",
        ]
        values += [f"{worlds[w]['reward']:.3f}" for w in WORLDS]
        values += [" / ".join(str(worlds[w]["repetitions"]) for w in WORLDS)]
        lines.append("| " + " | ".join(values) + " |")
    lines += [
        "",
        "Costs are reported provider inference charges. Failed-provider-attempt costs remain "
        "in the campaign ledger and are excluded from these model points. Completed attempts "
        "without valid predictors retain zero reward. One rollout per world does not estimate "
        "run-to-run uncertainty.",
        "",
        "The persistence baseline repeats initial sensor readings. Native controls use the "
        "true equations and prepared state, which the agents cannot access. Stochastic native "
        "controls use four forecast members; model predictions use 64. All use the same two "
        "grading truths per case. Persistence is deterministic and member-count invariant.",
        "",
        "Colored segments connect models within a family when more than one is present; the "
        "gray dotted line connects nondominated measured points, when there are at least two.",
        "",
    ]
    for model in data.get("pending_cost_models", []):
        name = NAMES.get(model["model"], model["model"])
        lines.append(
            f"{name} completed all three worlds (mean reward {model['mean_reward']:.3f}), "
            "but is omitted from the cost plot pending missing provider cost receipts."
        )
    if data.get("pending_cost_models"):
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, default=Path("outputs/evaluation-campaign-20260916"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--baselines", default="initial_persistence,ignore_actions")
    args = parser.parse_args()
    data = review_data(args.campaign, args.baselines.split(","))
    output = args.output or args.campaign / "figures"
    output.mkdir(parents=True, exist_ok=True)
    (output / "figure-data.json").write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")
    (output / "report.md").write_text(report(data))
    draw(data, output)
    draw(data, output, narrow=True)
    print(f"Rendered {len(data['models'])} complete model aggregates to {output}")


if __name__ == "__main__":
    main()
