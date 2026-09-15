"""Build the static public documentation using only the Python standard library.

Sources live in docs_source/. Existing media and historical pages are retained.
No model, simulator, package manager, network access, or publishing is invoked.
"""

import json
import os
import re
import shutil
from html import escape, unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE, DOCS = ROOT / "docs_source", ROOT / "docs"
PAGES = {
    "index": ("Overview", "Learning physical systems through experiments", "Overview"),
    "worlds": ("Worlds", "Blob-field worlds", "Worlds"),
    "experiment": ("Experiment & predict", "Experiments become predictions", "Experiment & predict"),
    "scoring": ("Evaluation", "Evaluating a prediction function", "Evaluation"),
    "try": ("Try it", "Try the prediction interface", "Try it"),
    "results": ("Results", "Evidence and current results", "Results"),
    "fields": ("Field dynamics", "Structures made of fields", "Reference"),
    "generation": ("World generation", "Generating worlds", "Reference"),
    "simulator": ("Simulator & numerics", "Simulator and numerics", "Reference"),
    "api": ("Prediction API", "Prediction API", "Reference"),
    "registry": ("World registry", "A registry of reproducible worlds", "Reference"),
    "contribute": ("Contribute", "Contributing to Physim", "Contribute"),
}
MAIN = ("index", "worlds", "experiment", "scoring", "try", "results")
DETAIL_PARENTS = {
    "fields": "worlds",
    "generation": "worlds",
    "simulator": "worlds",
    "registry": "worlds",
    "contribute": "worlds",
    "api": "experiment",
}
DESCRIPTIONS = {
    "index": "Learn physical systems through experiments in blob-field worlds, then evaluate an executable prediction function.",
    "worlds": "Blob-field dynamics, the prepared p4g2_044 instance, its instruments, and current evaluation coverage.",
    "experiment": "Explore a physical system, validate a predictor, freeze the artifact, and forecast new experimental programs.",
    "scoring": "Joint energy scoring, independent truth realizations, fixed coordinate scales, marginal diagnostics, and limitations.",
    "try": "Run a minimal Python predictor to understand the sensor-array interface without a simulation or model API.",
    "results": "Saved control scores and model attempts, with resource profiles, failures, and the limits of current evidence.",
    "fields": "Activator fields, coupled channels, localized structures, and the physical background of blob-field worlds.",
    "generation": "Generate field equations, characterize their behavior, and design physically grounded prediction suites.",
    "simulator": "The numerical profile, preparation, noise policy, and event timing of the current native simulation.",
    "api": "Exact action, query, timing, sample-shape, and resource rules for the prediction function.",
    "registry": "Verified local world, preparation, suite, and run artifacts, with reference release status.",
    "contribute": "Requirements for contributing reproducible worlds, evaluation suites, predictors, and documentation.",
}
CONTROL_NAMES = {
    "zero": "Always zero",
    "initial_persistence": "Persist initial readings",
    "frozen_initial_field": "Frozen fields, correct probe movement",
    "physics_25pct": "25% native physics + 75% frozen fields",
    "physics_50pct": "50% native physics + 50% frozen fields",
    "physics_75pct": "75% native physics + 25% frozen fields",
    "native_physics": "Native physics, independent noise",
    "ignore_later_pulses": "Native physics, omit later pulses",
    "ignore_probe_moves": "Native physics, ignore probe movement",
    "five_unit_time_grid": "Native physics, five-unit time grid",
    "spatially_flat": "Native physics, flatten spatial readings",
    "ensemble_mean": "Native ensemble mean, repeated",
    "spread_x100": "Native mean with 100-fold spread",
}
MODEL_NAMES = {
    "deepseek/deepseek-v4-pro": "DeepSeek V4 Pro",
    "openai/gpt-5.6-sol": "GPT-5.6 Sol",
    "openai/gpt-5.6-terra": "GPT-5.6 Terra",
    "Qwen/Qwen3.5-122B-A10B": "Qwen3.5 122B",
    "qwen/qwen3.5-397b-a17b": "Qwen3.5 397B",
    "anthropic/claude-sonnet-5": "Claude Sonnet 5",
}
STOP_NAMES = {
    "submitted": "Submitted",
    "max_output_tokens": "Output-token limit",
    "agent_completed": "Agent ended",
    "error": "Runtime error",
    "dollar_budget": "Dollar stop",
}


def nav(keys, active, prefix=""):
    return "".join(
        f'<a href="{prefix}{key}.html"'
        + (
            ' aria-current="page"'
            if key == active
            else ' class="section-active"'
            if key == DETAIL_PARENTS.get(active)
            else ""
        )
        + f">{escape(PAGES[key][0])}</a>"
        for key in keys
    )


def page_context(key, section, prefix=""):
    parent = DETAIL_PARENTS.get(key)
    if parent:
        return (
            f'<p class="breadcrumb"><a href="{prefix}{parent}.html">'
            f'{escape(PAGES[parent][0])}</a><span aria-hidden="true"> / </span>'
            f"<span>{escape(PAGES[key][0])}</span></p>"
        )
    return f'<p class="eyebrow">{escape(section)}</p>'


def continuation(key, prefix=""):
    if key in MAIN:
        index = MAIN.index(key)
        links = []
        if index:
            previous = MAIN[index - 1]
            links.append(
                f'<a class="previous" rel="prev" href="{prefix}{previous}.html">'
                f"<span>Previous</span>← {escape(PAGES[previous][0])}</a>"
            )
        if index + 1 < len(MAIN):
            following = MAIN[index + 1]
            links.append(
                f'<a class="following" rel="next" href="{prefix}{following}.html">'
                f"<span>Next</span>{escape(PAGES[following][0])} →</a>"
            )
        return '<div class="page-continuation">' + "".join(links) + "</div>"
    if key in DETAIL_PARENTS:
        parent = DETAIL_PARENTS[key]
        return f'<p class="return-link"><a href="{prefix}{parent}.html">← Back to {escape(PAGES[parent][0])}</a></p>'
    return ""


def table(headers, rows, caption, numeric=True):
    return (
        '<div class="table-scroll"><table><caption>'
        + escape(caption)
        + "</caption><thead><tr>"
        + "".join('<th scope="col">' + escape(h) + "</th>" for h in headers)
        + "</tr></thead><tbody>"
        + "".join(
            "<tr>"
            + "".join(
                "<td" + (' class="numeric"' if i and numeric else "") + ">" + str(c) + "</td>"
                for i, c in enumerate(row)
            )
            + "</tr>"
            for row in rows
        )
        + "</tbody></table></div>"
    )


def registry_content():
    catalog = json.loads((SOURCE / "registry.json").read_text())
    worlds = catalog["worlds"]
    counts = catalog["availability"]["counts"]
    heading = (
        f"<p><strong>{len(worlds)} world records · "
        f"{len({w['genome'] for w in worlds})} distinct genomes · "
        f"{counts.get('eval-ready', 0)} eval-ready.</strong> "
        "Separate harvests can refer to the same genome.</p>"
    )
    rows = []
    for status, label in (("eval-ready", "Eval-ready"), ("preserved", "Preserved")):
        selected = [w for w in worlds if w["status"] == status]
        names = ", ".join(f"<code>{escape(n)}</code>" for n in sorted({w["name"] for w in selected}))
        rows.append([label, len(selected), names])
    return heading + table(["Status", "Records", "Names"], rows, "Current registry contents", numeric=False)


def displayed_results(rows):
    """Show one result per model; a scored attempt supersedes missing artifacts.

    Snapshot order is retained. When several attempts have scores, use the last
    recorded one, regardless of whether its score improves. Full history stays
    in the downloadable snapshot.
    """
    selected = {}
    for row in rows:
        previous = selected.get(row["model"])
        if previous is None or row["score_kind"] != "nan" or previous["score_kind"] == "nan":
            selected[row["model"]] = row
    return list(selected.values())


def generated_content():
    world = json.loads((SOURCE / "worlds.json").read_text())["worlds"][0]
    evidence = json.loads((SOURCE / "results.json").read_text())
    bundle = world.get("reference_bundle")
    release_status = (
        "Standalone preparation/suite bundle verified locally; publication pending."
        if bundle and not bundle["public_release_available"]
        else "See the registry for release availability."
    )
    bundle_size = (
        f"<dt>Reference bundle</dt><dd>{bundle['profiles']['evaluation']:,} payload bytes; "
        f"{bundle['case_count']} cases; exact field and truth hashes</dd>"
        if bundle
        else ""
    )
    card = f'''<article class="world" id="{escape(world["id"])}"><span class="badge">Prepared development example</span>
<h2>{escape(world["id"])}</h2><p>{escape(world["description"])}</p><dl>
<dt>Fields</dt><dd>{world["activators"]} activators + {world["channels"]} channels</dd>
<dt>Numerics</dt><dd>{world["grid"][0]} × {world["grid"][1]} periodic grid; {world["dtype"]}; step {world["dt"]}</dd>
<dt>Measurements</dt><dd>{world["ports"]} ports; probe arrays of {world["device_slots"][0]} and {world["device_slots"][1]} slots; global mean and variance</dd>
<dt>Evaluation</dt><dd>{world["evaluation_cases"]} programs; horizon {world["horizon"]} time units; one prepared instance</dd>
<dt>Sampling</dt><dd>{world["model_forecast_members"]} forecast members per model prediction; {world["truths_per_case"]} independent truth realizations per program</dd>
<dt>Release status</dt><dd>Genome available. {escape(release_status)}</dd>{bundle_size}</dl>
<p><a href="{escape(world["genome"]["file"])}" download>Download genome JSON</a> · <a href="simulator.html">Numerical profile</a></p></article>'''
    controls = table(
        ("Predictor", "Joint energy", "Marginal CRPS"),
        [
            (escape(CONTROL_NAMES[k]), f"{v['joint_energy']:.6f}", f"{v['marginal_crps_all_coordinates']:.6f}")
            for k, v in evidence["controls"]["aggregate"].items()
        ],
        "Hand-written controls · 4 forecast members · 2 truths per case",
    )
    profiles = []
    for profile in evidence["profiles"]:
        rows = []
        for row in displayed_results(profile["rows"]):
            name = MODEL_NAMES.get(row["model"], row["model"])
            score = (
                f"{row['primary_joint_energy']:.6f}"
                if row["score_kind"] == "finite"
                else "Invalid (∞)"
                if row["score_kind"] == "infinity"
                else "No score"
            )
            rows.append(
                (
                    escape(name),
                    score,
                    str(row["experiments"]),
                    escape(STOP_NAMES.get(row["stop"], row["stop"])),
                    f"${row['provider_reported_cost_usd']:.4f}",
                )
            )
        profiles.append(
            table(("Model", "Joint energy", "Experiments", "Run ended", "Run cost"), rows, profile["label"])
        )
    predictor = (SOURCE / "examples/predictor.py").read_text()
    sample_code = predictor[predictor.index("SLOTS =") : predictor.index("\n\nif __name__")].strip()
    registry_counts = registry_content()
    return {
        "world_card": card,
        "control_table": controls,
        "model_tables": "\n".join(profiles),
        "predictor_code": escape(sample_code),
        "registry_counts": registry_counts,
    }


def render(key, heading, section, body, title=None, description=None, prefix=""):
    values = {
        "root": prefix,
        "title": escape(title or PAGES[key][0]),
        "description": escape(description or DESCRIPTIONS[key], quote=True),
        "heading": escape(heading),
        "context": page_context(key, section, prefix),
        "body": body,
        "navigation": nav(MAIN, key, prefix),
        "continuation": continuation(key, prefix),
    }
    source = (SOURCE / "template.html").read_text()
    return re.sub(r"\{\{(\w+)\}\}", lambda m: values[m[1]], source)


def redirect(old, target):
    prefix = os.path.relpath(DOCS, (DOCS / old).parent) + "/"
    relative = os.path.relpath(DOCS / target, (DOCS / old).parent)
    # JavaScript retains a deep-link fragment; the plain link works without JS.
    js_target = json.dumps(relative).replace("<", "\\u003c")
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex"><title>Page moved · Physim</title>
<link rel="stylesheet" href="{prefix}site.css"></head><body>
<main style="margin:3rem auto;padding:1rem"><h1>Page moved</h1>
<p><a href="{relative}">Continue to this page</a>.</p>
<p><a href="{prefix}index.html">Current Physim documentation</a></p></main>
<script>window.location.replace({js_target} + window.location.hash);</script>
</body></html>'''


def build():
    DOCS.mkdir(exist_ok=True)
    blocks = generated_content()
    for key, (_, heading, section) in PAGES.items():
        body = (SOURCE / "pages" / f"{key}.html").read_text()
        body = re.sub(r"\{\{(\w+)\}\}", lambda m: blocks[m[1]], body)
        (DOCS / f"{key}.html").write_text(render(key, heading, section, body))
    shutil.copyfile(SOURCE / "site.css", DOCS / "site.css")
    for filename in ("worlds.json", "results.json", "registry.json"):
        (DOCS / "data").mkdir(exist_ok=True)
        shutil.copyfile(SOURCE / filename, DOCS / "data" / filename)
    (DOCS / "examples").mkdir(exist_ok=True)
    for path in (SOURCE / "examples").iterdir():
        if path.is_file():
            shutil.copyfile(path, DOCS / "examples" / path.name)
    # Only explicitly mapped old URLs are rewritten. Archive pages/media are inputs.
    records = json.loads((SOURCE / "archive-map.json").read_text())
    aliases = {"blobs.html": "worlds.html", "rollouts.html": "results.html"}
    for record in records:
        if record["old"] in {f"{key}.html" for key in PAGES}:
            continue
        target = aliases.get(record["old"], record["archive"])
        path = DOCS / record["old"]
        path.parent.mkdir(exist_ok=True, parents=True)
        path.write_text(redirect(record["old"], target))
    body = '<p class="lead">Earlier studies, preserved with their original scope and claims.</p><p>The current program uses blob-field worlds and prediction-function evaluation. Historical scoring rules and model comparisons below apply only to the studies that reported them.</p>'
    for title, group in [
        ("Earlier benchmark", [r for r in records if not r["old"].startswith("blobs")]),
        ("Blob-field research", [r for r in records if r["old"].startswith("blobs")]),
    ]:
        body += f"<h2>{title}</h2><ul>"
        for record in group:
            link = record["archive"].removeprefix("archive/")
            body += f'<li><a href="{escape(link)}">{escape(unescape(record["title"]))}</a></li>'
        body += "</ul>"
    (DOCS / "archive" / "index.html").write_text(
        render(
            "archive",
            "Research archive",
            "Archive",
            body,
            title="Research archive",
            description="Historical Physim benchmarks and blob-field research.",
            prefix="../",
        )
    )
    print(f"Built {len(PAGES)} current pages, an archive index, and compatibility redirects.")


if __name__ == "__main__":
    build()
