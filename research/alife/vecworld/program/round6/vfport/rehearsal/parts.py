"""parts -- the commands of the round-3 RUNBOOK_MAC.md, each written ONCE.

Several pieces of text stand in more than one command of the runbook (the guard, the process listing, the list
of the pilot's programs in the status and in the stop command, the disk check). Here each piece is one Python
string and every command is put together from them, so that repeated text is identical by construction.
rehearsal/make_runbook.py writes RUNBOOK_MAC.md from this file and its own prose. Neither is executed by the
pilot, and neither is listed in PIN.sha256; tools/check_runbook.py checks the result as text.
"""
P = "/ABSOLUTE/PATH/TO/vfport"
G = f'cd "{P}" && test -f RUNBOOK_MAC.md && test -f physim2_env/taskset.py && '
H = '"$HOME/physim2-pilot-20261110'
PY = f'"{P}/.venv/bin/python"'
ENVRE = "^(PHYSIM2_|UV_|VIRTUAL_ENV|PYTHON(PATH|HOME)|DOCKER_|BUILDX_|VF_|MCP_HOST|MCP_PORT|PRIME_RUNS_MODE)"
DISKGATE = ("df -Pk \"$HOME\" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) exit 0 ; "
            "print \"refused: under 8 GiB free on the file system of the home folder\" ; exit 1 }' && ")
TOOLS = ('index(r, "-B tools/prove.py ") == 1 || index(r, "-B tools/check_probe.py ") == 1 || index(r, "-B tools/vfrun.py ") == 1')
VFE = 'index(r, "-B " p "/tools/vfeval.py @ ") == 1'
LAB = 'index(r, "-m physim2_env.lab_tools") == 1'
HELP = ('index(r, "-B " p "/tools/make_instances.py ") == 1 || index(r, "-B tools/make_instances.py ") == 1 || '
        'index(r, "-B " p "/tools/build_reference.py ") == 1')
AWKPS = (f"awk -v p=\"{P}\" 'BEGIN {{ py = p \"/.venv/bin/python \" }} {{ line = $0 ; sub(/^ *[0-9]+ /, \"\", line) ; "
         f"if (index(line, py) != 1) next ; r = substr(line, length(py) + 1) ; k = \"OTHER\" ; "
         f"if ({TOOLS}) k = \"TOOL\" ; else if ({VFE}) k = \"VF-EVAL\" ; else if ({LAB}) k = \"LAB\" ; "
         f"else if ({HELP}) k = \"HELPER\" ; else if (index(r, \"-c\") == 1) k = \"PROBE\" ; print k \" \" substr($0, 1, 160) }}'")
AWKSTOP = (f"awk -v p=\"{P}\" 'BEGIN {{ py = p \"/.venv/bin/python \" }} {{ r = (index($0, py) == 1) ? substr($0, length(py) + 1) : \"\" ; "
           f"if ({TOOLS} || {VFE} || {LAB} || {HELP}) {{ ok = 1 ; print substr($0, 1, 160) }} }} END {{ exit !ok }}'")
PS = f"ps axww -o pid= -o command= | {AWKPS}"
DOCKPS = "docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}'"
FREE = "df -Pk \"$HOME\" | awk 'NR == 2 { print int($4 / 1048576) \" GiB\" }'"
DET_A = "docker info --format '{{.ServerVersion}}' && { ( "
def det(inner, log):
    return (f"{DET_A}{inner} > {H}/scratch/{log}\" 2>&1 < /dev/null ; echo \"EXIT $?\" >> {H}/scratch/{log}\" ) > /dev/null 2>&1 < /dev/null & }}")
NOLINK = f'test ! -L {H}" && test ! -L {H}/store" && test ! -L {H}/scratch" && '

C = {}
C["0a"] = G + f'git rev-parse HEAD && pwd -P | grep -Fx "{P}" && git status --porcelain -- . ../../round5/agentenv ../../../vw1 && echo "TREE-LISTED"'
C["0b"] = G + 'shasum -a 256 PIN.sha256 && shasum -a 256 -c PIN.sha256 > /dev/null && echo PIN-OK'
C["0c"] = G + (f"env | cut -d= -f1 | awk '/{ENVRE}/ {{ bad++ ; print \"FOUND \" $0 }} END {{ print NR \" names, \" bad + 0 \" refused\" }}' && "
               "docker context show && docker context inspect --format '{{.Endpoints.docker.Host}}'")
C["0d"] = G + ("docker info --format '{{.ServerVersion}}' && docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}}' && "
               "echo \"CONTAINERS-LISTED\" && docker images -q physim2-ring:1 && echo \"IMAGES-LISTED\" && "
               f'test ! -e {H}" && test ! -L {H}" && test ! -e {H}-results" && test ! -L {H}-results" && test ! -e .venv && test ! -L .venv && echo "NO-PILOT-FOLDERS"')
C["0e"] = G + ("df -Pk \"$HOME\" | awk 'NR == 2 { free = $4 } END { if (free >= 8388608) print \"DISK-OK \" int(free / 1048576) \" GiB free\" ; "
               "else print \"refused: \" int(free / 1048576) \" GiB free on the file system of the home folder, the floor is 8 GiB\" }'")
UV = f'uv sync --project "{P}" --locked --python 3.12 --managed-python'
C["1a"] = G + f'test -f pyproject.toml && test -f uv.lock && {DISKGATE}cd / && {UV} --dry-run 2>&1 | grep -E "^Using CPython|project environment|Would (download|install)|error"'
C["1b"] = G + (f'mkdir -m 700 {H}" && mkdir {H}/scratch" && test ! -L docker/extra-ca.crt && (test -e docker/extra-ca.crt || : > docker/extra-ca.crt) && wc -c docker/extra-ca.crt')
C["1c"] = G + f'test -f pyproject.toml && test -f uv.lock && {DISKGATE}' + det(f"nohup {UV}", "sync.log")
C["1c-status"] = G + f'tail -n 3 {H}/scratch/sync.log"'
C["1d"] = G + (f'{PY} -B -c "import physim2_env, physim2_script, verifiers, numpy, scipy, jax; print(verifiers.__version__, numpy.__version__, '
               'scipy.__version__, jax.__version__, physim2_env.__file__, physim2_env._nokey.state())"')
C["1e"] = G + (f'{PY} -B -c "import os, subprocess; line = subprocess.run([\'ps\', \'-ww\', \'-p\', str(os.getpid()), \'-o\', \'command=\'], '
               f'capture_output=True, text=True).stdout.strip(); print(line[:160]); print(\'INTERPRETER-OK\' if line.startswith(\'{P}/.venv/bin/python -B -c \') '
               'else \'INTERPRETER-DIFFERS\')"')
C["1f"] = G + DISKGATE + det("nohup docker build -f docker/Dockerfile.ring -t physim2-ring:1 docker/", "build.log")
C["1f-status"] = G + f'tail -n 2 {H}/scratch/build.log"'
C["1g"] = G + ('docker run --rm --network none --label verifiers.run=physim2-pilot-20261110 physim2-ring:1 python -c '
               '"import numpy, scipy, jax; print(numpy.__version__, scipy.__version__, jax.__version__)"')
C["1h"] = G + f'{PY} -B tools/make_instances.py --store {H}/store" --world ring --config smoke_ring --n 1 --prefix mac-ring'
C["2-quiet"] = G + "docker ps --format '{{.Names}} {{.Image}}' && echo \"RUNNING-LISTED\""
C["2-status"] = G + (f'{{ tail -n 4 {H}/scratch/prove.log" {H}/scratch/probe.log" {H}/scratch/single.log" 2>/dev/null | cut -c 1-200 ; '
                     f'echo "containers:" ; {DOCKPS} ; echo "processes:" ; {PS} ; echo "free:" ; {FREE} ; echo "status done" ; }}')
C["2a"] = G + det(f'VF_RUN_ID=physim2-pilot-20261110 nohup {PY} -B tools/prove.py --store {H}/store" --scratch {H}/scratch/proof" --worlds 1 --prefix mac-ring '
                  f'--policies D,P0,C --box-check C --no-cross-check --disk-floor-gib 8 --out {H}/scratch/proof_mac.json"', "prove.log")
C["2a-check"] = G + f'''{PY} -B -c "
import json
p = json.load(open('$HOME/physim2-pilot-20261110/scratch/proof_mac.json'))
r = p['per_world'][0]['rollouts']; b = p['one_box_per_item_check_world_0']['C']
print('all_graded', p['all_graded'], 'all_ok', p['all_ok'], 'failed_items', p['n_failed_items_total'])
print('ticks', {{k: r[k]['lab_ticks_used'] for k in r}})
print('layers', {{k: r[k]['grade']['layers'] for k in r}})
print('box', b['identical_per_item_scores'], b['grade']['item_boxes'], b['grade']['infrastructure_failed_items'], round(b['grade']['item_box_wall_s_mean'], 2))
print('table', {{k: round(v['vs_C'], 3) for k, v in p['pooled']['policies'].items() if v['vs_C'] is not None}})
"'''
C["2b"] = G + det(f'VF_RUN_ID=physim2-pilot-20261110 nohup {PY} -B tools/check_probe.py --store {H}/store" --scratch {H}/scratch/probe" --disk-floor-gib 8 '
                  f'--out {H}/scratch/probe_mac.json"', "probe.log")
C["2b-report"] = G + f'''{PY} -B -c "
import json
p = json.load(open('$HOME/physim2-pilot-20261110/scratch/probe_mac.json'))
e = p['evidence']
print('round5', p['n_reproduced'], 'of', p['n_checks_round5'], p['failed_round5'], 'new', p['n_passed_new'], 'of', p['n_checks_new'], p['failed_new'])
print('staging', {{k: e['verifier_box_staging'][k] for k in ('container_evidence', 'world_writable_paths_fixed', 'box_limits', 'predictor_uid')}})
print('control', e['c_control'], e['c_listener_hits'])
print('agent box net', e['c_agent_box_net'])
print('item box net', e['c_verifier_box_net_all_items'])
print('lab env', {{k: e['b_lab_process'][k] for k in ('token_values_left_in_environ', 'token_like_names_left_in_os_environ')}})
c = e['a2_channels_one_box_per_item']
print('channels', c['mark_was_read'], c['dirs_touched_after_staging'], c['lo_rx_packets'], c['pid_step'])
print('kill in box', e['h_harness_dies']['killall']['first'], 'wall_s', round(p['wall_s']))
"'''
C["2c"] = G + det(f'VF_RUN_ID=physim2-pilot-20261110 nohup {PY} -B tools/vfrun.py --config configs/scripted_ring.toml --run-name single-d '
                  f'--out-dir {H}/scratch/single" --store {H}/store" --disk-floor-gib 8', "single.log")
C["2c-report"] = G + f'{PY} -B tools/run_report.py --store {H}/store" --run-dir {H}/scratch/single/single-d"'
C["I2"] = G + f"ps -ww -p PID_FROM_THE_STATUS_LINE -o command= | {AWKSTOP} && kill -TERM PID_FROM_THE_STATUS_LINE"
C["I3"] = G + ("docker inspect --format '{{index .Config.Labels \"verifiers.run\"}}' NAME_FROM_THE_STATUS_LINE | grep -Fx physim2-pilot-20261110 && "
               "docker rm -f NAME_FROM_THE_STATUS_LINE")
C["I6"] = G + NOLINK + (f'test -f {H}/store/index.json" && test -d {H}/scratch" && rm -rf {H}/store" {H}/scratch" && mkdir {H}/scratch" && echo "pilot folders reset"')
C["3-dry"] = G + (f'test -f {H}/scratch/LEAD-GO-STEP3" && VF_RUN_ID=physim2-pilot-20261110 {PY} -B tools/vfrun.py --config configs/qwen_ring_bash.toml --run-name qwen-dry '
                  f'--out-dir {H}/scratch/qwen-dry" --store {H}/store" --dry-run > {H}/scratch/qwen-dry.log" 2>&1 && echo "DRY-RUN-OK"')
C["3-paid"] = G + f'test -f {H}/scratch/LEAD-GO-STEP3" && ' + det(
    f'VF_RUN_ID=physim2-pilot-20261110 nohup {PY} -B tools/vfrun.py --config configs/qwen_ring_bash.toml --run-name qwen --out-dir {H}/scratch/qwen" '
    f'--store {H}/store" --disk-floor-gib 8 --model-credentials prime', "qwen.log")
C["3-status"] = G + (f'{{ tail -n 1 {H}/scratch/qwen.log" | cut -c 1-12 ; echo "containers:" ; {DOCKPS} ; echo "processes:" ; {PS} ; echo "free:" ; {FREE} ; echo "status done" ; }}')
C["3-report"] = G + f'{PY} -B tools/run_report.py --store {H}/store" --run-dir {H}/scratch/qwen/qwen"'
C["3-settle"] = G + f'{PY} -B tools/settle.py --store {H}/store" --run-dir {H}/scratch/qwen/qwen"'
C["3-trace"] = G + (f'{PY} -B tools/run_report.py --store {H}/store" --run-dir {H}/scratch/qwen/qwen" | grep -c \'"total_hits": 0\' && mkdir {H}-trace" && '
                    f'cp -R {H}/scratch/qwen/qwen" {H}-trace/" && ls {H}-trace"')
C["4a"] = G + NOLINK + (f'test -f {H}/store/index.json" && test -d {H}/scratch" && test -f {H}/scratch/proof_mac.json" && test -f {H}/scratch/probe_mac.json" && '
                        f'mkdir {H}-results" && cp {H}/scratch/proof_mac.json" {H}/scratch/proof_mac_items.npz" {H}/scratch/probe_mac.json" {H}/scratch/prove.log" '
                        f'{H}/scratch/probe.log" {H}-results/" && test -s {H}-results/proof_mac.json" && test -s {H}-results/probe_mac.json" && '
                        f'rm -rf {H}/store" {H}/scratch" && rmdir {H}" && ls {H}-results"')
C["4b"] = G + ("docker ps -a --filter label=verifiers.run=physim2-pilot-20261110 --format '{{.Names}} {{.Status}}' && echo \"CONTAINERS-LISTED\" && "
               "docker images --format '{{.Repository}}:{{.Tag}} {{.Size}}' && docker system df")
