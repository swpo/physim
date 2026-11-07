"""Collect build, verification, proof, limit and native-band records into reports/summary.json and a Markdown table."""
import json
from pathlib import Path

B = Path("/home/user/evalwork/bundles")
ORDER = ["fedvortex", "vortex_main", "vortex_formation", "pm_main", "pm_formation", "cips_main", "cips_formation",
         "rods_main", "rods_formation"]
LABEL = {"fedvortex": ("fed vortices (c53)", "fed-vortex bundle"), "vortex_main": ("fed vortices + selection", "main"),
         "vortex_formation": ("fed vortices + selection", "formation"), "pm_main": ("phase_membrane", "main (iter2)"),
         "pm_formation": ("phase_membrane", "formation"), "cips_main": ("CIPS-iso", "main (iter2)"),
         "cips_formation": ("CIPS-iso", "formation"), "rods_main": ("Marangoni rods", "main (iter2)"),
         "rods_formation": ("Marangoni rods", "formation")}


def load(p):
    p = Path(p)
    return json.loads(p.read_text()) if p.exists() else None


def size(path):
    return sum(f.stat().st_size for f in Path(path).rglob("*") if f.is_file())


def main():
    limits = load(B / "configs" / "limits.json")
    band = load(B / "reports" / "native_band.json")
    reseal = load(B / "reports" / "fedvortex_reseal.json")
    rows = {}
    for k in ORDER:
        lim = limits[k]
        bundle = Path(lim["bundle"])
        manifest = load(bundle / "manifest.json")
        local = load(B / "work" / "prove" / k / "local.json")
        orc = load(B / "work" / "prove" / k / "oracle_m2.json")
        deb = load(B / "work" / "prove" / k / "debias_m2.json")
        ver = reseal["truth_member_check"] if k == "fedvortex" else load(B / "reports" / f"verify_{k}.json")
        rows[k] = dict(
            world=LABEL[k][0], suite=LABEL[k][1], bundle=str(bundle), bundle_id=manifest["bundle_id"],
            cases=lim["cases"], n_ports=local["n_ports"] if local else None, bytes=size(bundle),
            cpu_s_per_tu=lim["cpu_s_per_member_tu"], predictor=lim["predictor"],
            scoring_timeout=lim["derived_scoring_timeout"], agent_timeout=lim["agent_timeout"],
            max_total_tu=lim["max_total_tu"],
            truth_member=dict(case=ver["case"], bit_identical=ver["bit_identical"], cpu_s=ver["cpu_s"]) if ver else None,
            validation=local and local["validation"], experiment=local and dict(
                charged_tu=local["experiment"]["charged_tu"], charge_ok=local["experiment"]["charge_ok"],
                rejected=local["experiment"]["rejected"]["error"], cpu_s=local["experiment"]["cpu_s"]),
            naive=local and dict(energy=local["naive"]["primary_joint_energy"], reward=local["naive"]["reward_K2"]),
            oracle=orc and dict(members=orc["members"], status=orc["status"], energy=orc["primary_joint_energy"],
                                reward=orc["reward_K2"], sim_cpu_s=orc["simulation_cpu_s"]),
            debias=deb and dict(e2=deb["aggregate"]["e2"], e4=deb["aggregate"]["e4"], e64=deb["aggregate"]["e64"],
                                reward64=deb["reward_K2"]["e64"], matches=deb["recomputed_matches_grade"]),
            native=band.get(k),
        )
    (B / "reports" / "summary.json").write_text(json.dumps(rows, indent=1) + "\n")
    head = ("| bundle | world | suite | cases | ports | bundle id | size | CPU-s per tu | predictor limits (CPU-s / wall-s / cpus / GiB) "
            "| scoring timeout (derived) | naive: energy, reward | true simulator M=2: energy, reward | true simulator, 64-member equivalent: energy, reward | native 4-member reference | truth member bit for bit |")
    lines = [head, "|" + "---|" * head.count("|")[:-1] if False else "|" + "|".join(["---"] * (head.count("|") - 1)) + "|"]
    for k, r in rows.items():
        p = r["predictor"]
        o, d, n = r["oracle"], r["debias"], r["native"]
        nat = (f"{n['native4']:.4f} (band x{n['band_ratio']:.2f})" if n and "band_ratio" in n else
               f"{n['native4']:.4f} (64: {n['native64']:.4f})" if n else "-")
        lines.append("| " + " | ".join([
            k, r["world"], r["suite"], str(r["cases"]), str(r["n_ports"]), r["bundle_id"].split(":")[-1][:12],
            f"{r['bytes'] / 1e6:.1f} MB", f"{r['cpu_s_per_tu']:.2f}",
            f"{p['cpu_seconds']} / {p['wall_seconds']} / {p['cpus']} / {p['memory_gib']}",
            f"{r['scoring_timeout']:.0f} s ({r['scoring_timeout'] / 3600:.1f} h)",
            f"{r['naive']['energy']:.3f}, {r['naive']['reward']:.3f}" if r["naive"] else "-",
            f"{o['energy']:.4f}, {o['reward']:.3f}" if o else "pending",
            f"{d['e64']:.4f}, {d['reward64']:.3f}" if d else "pending",
            nat,
            f"{r['truth_member']['case']}: {'yes' if r['truth_member']['bit_identical'] else 'NO'}" if r["truth_member"] else "-",
        ]) + " |")
    (B / "reports" / "table.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
