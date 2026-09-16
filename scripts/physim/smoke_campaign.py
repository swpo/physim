"""No-charge stock-harness smoke: local scripted responses, real Docker and grading."""

import argparse
import json
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from physim.bundles import Bundle
from run_campaign import configuration, dump

PREDICTOR = """from pathlib import Path
import json
import numpy as np
def predict(actions, queries, n_samples=64, seed=0):
    with np.load(next(Path('/observations').glob('*.npz'))) as data:
        request=json.loads(data['request'].item())
        initial={q['sensor']: data[f'query{i}'][0,0].copy() for i,q in enumerate(request['queries'])}
    return {'samples':[np.broadcast_to(initial[q['sensor']],(n_samples,len(q['t']),*initial[q['sensor']].shape)).copy() for q in queries]}
"""


def main(args):
    root = args.output.resolve()
    root.mkdir(parents=True, exist_ok=False)
    bundle = Bundle(args.bundle)
    calls = []
    steps = [
        (
            "laboratory_experiment",
            {"actions": [], "queries": [{"sensor": s, "t": [0]} for s in ["device0", "device1", "global"]]},
        ),
        ("bash", {"command": "cat > /workspace/predictor.py <<'PY'\n" + PREDICTOR + "PY\n"}),
        ("laboratory_validate", {}),
        ("laboratory_submit", {}),
    ]

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def do_POST(self):
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            index = len(calls)
            tools = [t["function"]["name"] for t in body.get("tools", [])]
            calls.append(dict(index=index, model=body["model"], tool_names=tools))
            if index < len(steps):
                name, arguments = steps[index]
                assert name in tools, (name, tools)
                message = dict(
                    role="assistant",
                    content=None,
                    tool_calls=[
                        dict(
                            id=f"call_{index}",
                            type="function",
                            function=dict(name=name, arguments=json.dumps(arguments)),
                        )
                    ],
                )
                reason = "tool_calls"
            else:
                message, reason = dict(role="assistant", content="Submitted."), "stop"
            response = dict(
                id=f"offline-{index}",
                object="chat.completion",
                created=0,
                model=body["model"],
                choices=[dict(index=0, message=message, finish_reason=reason)],
                usage=dict(prompt_tokens=10, completion_tokens=10, total_tokens=20, cost=0.0),
            )
            encoded = json.dumps(response).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    model = dict(
        id="offline/scripted",
        specs=dict(context_window=10000, max_output_tokens=128),
        pricing=dict(input_usd_per_mtok=0, output_usd_per_mtok=0),
    )
    config = configuration(root, root, model, args.bundle.resolve(), 1)
    config["client"] = dict(
        type="eval",
        base_url=f"http://127.0.0.1:{server.server_port}/v1",
        api_key_var="PHYSIM_OFFLINE_SMOKE_KEY",
        headers={},
    )
    dump(root / "eval.json", config)
    try:
        with (root / "eval.log").open("w") as log:
            result = subprocess.run(
                [str(Path(sys.executable).with_name("eval")), "@", str(root / "eval.json")],
                stdout=log,
                stderr=subprocess.STDOUT,
            )
    finally:
        server.shutdown()
        server.server_close()
    dump(root / "scripted_calls.json", calls)
    if result.returncode:
        raise RuntimeError(f"Offline smoke failed; inspect {root / 'eval.log'}")
    paths = list((root / "runs").glob("*/traces.jsonl"))
    episode = json.loads(paths[0].read_text().splitlines()[-1])
    assert episode.get("traces"), episode.get("errors")
    trace = episode["traces"][-1]
    info = trace["info"]["r6"]
    assert trace["ok"], trace.get("errors")
    assert info["spend_final"]["accounted_cost_usd"] == 0
    assert not info["limit_audit"]["truncated"]
    assert info["grade"]["status"] == "COMPLETE"
    expected = json.loads(bundle.verified_path("checks.json").read_text())["reference"]["primary_joint_energy"]
    assert abs(info["primary_joint_energy"] - expected) < 1e-10
    report = dict(
        ok=True,
        references=bundle.references(),
        model_calls=len(calls),
        cost_usd=0,
        energy=info["primary_joint_energy"],
        stop_condition=trace["stop_condition"],
        audit=info["limit_audit"],
    )
    dump(root / "report.json", report)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bundle", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    main(parser.parse_args())
