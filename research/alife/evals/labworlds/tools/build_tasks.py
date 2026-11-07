"""Build the PhySim tasks from each rollout config, without a model: R6Taskset(R6Config(env.taskset)).load().

    python build_tasks.py CONFIG_DIR OUT_JSON PROMPT_DIR

Per config: task count, bundle id, world name, protocol, timeouts (setup, agent, finalize, derived scoring),
resources, and checks that the rendered agent prompt states the configured predictor limits and budgets.
The rendered prompts of the fed-vortex configs are saved to PROMPT_DIR.
"""
import json
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, "/home/user/swpo/residency-environments/environments/physim")
from physim import taskset as TS  # noqa: E402


def main(cfg_dir: Path, out: Path, prompt_dir: Path):
    rows = {}
    prompt_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(cfg_dir.glob("*.toml")):
        raw = tomllib.loads(path.read_text())
        ts = dict(raw["env"]["taskset"])
        assert ts.pop("id") == "physim"
        config = TS.R6Config(**ts)
        tasks = list(TS.R6Taskset(config).load())
        assert len(tasks) == 1
        task = tasks[0]
        d = task.data
        lim = config.task.tools.predictor_limits
        prompt = d.system_prompt
        expect = [f"{lim.cpus}", f"{lim.cpu_seconds}", f"{lim.wall_seconds}", f"{lim.memory_gib}",
                  f"{config.task.tools.max_total_tu:g}", f"{config.task.tools.max_experiments}"]
        rows[path.stem] = dict(
            bundle=str(d.bundle), bundle_id=d.bundle_id, world_name=d.world_name, protocol=d.protocol,
            timeouts=d.timeout.model_dump(), resources=d.resources.model_dump(), image=d.image,
            network_allow=d.network_allow, prompt_chars=len(prompt), user_prompt=d.prompt,
            prompt_states_limits=all(e in prompt for e in expect), harness=raw["env"]["agent"]["harness"]["id"],
            agent_rollout_timeout=raw["env"]["agent"]["timeout"]["rollout"])
        if path.stem.startswith("fedvortex."):
            (prompt_dir / f"agent_prompt_{path.stem}.md").write_text(
                f"<!-- system prompt of the PhySim task built from {path} (R6Taskset.load(), no model); "
                f"user prompt: {d.prompt!r} -->\n\n" + prompt)
        print(path.stem, d.bundle_id[:30], d.world_name, d.timeout.model_dump(), rows[path.stem]["prompt_states_limits"])
    out.write_text(json.dumps(rows, indent=1) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
