"""worlds.py — ground-truth world builders for the complexity metric validation.
Seven worlds spanning the known complexity range (see VALIDATION.md)."""
import copy, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L0 = os.path.dirname(HERE)
BLOBS = os.path.dirname(L0)
sys.path.insert(0, os.path.join(L0, "stage2", "lib"))
import genome as G

ENC = os.path.join(L0, "stage3", "jobs_encounter.json")


def _enc_genome(cand):
    for j in json.load(open(ENC)):
        if j["cand"] == cand:
            return copy.deepcopy(j["genome"])
    raise KeyError(cand)


def gt_m0():
    g = G.ref_M0(); g["id"] = "gt_m0"; return g            # static gas (boring)

def gt_m4():
    g = G.ref_M4(tau=6.0); g["id"] = "gt_m4"; return g     # traveling bonds

def gt_xv():
    g = G.ref_XV(); g["id"] = "gt_xv"; return g            # heterodimer rotor

def gt_bf():
    g = G.ref_BFIELD(); g["id"] = "gt_bf"; return g        # autophoresis + trails

def gt_pred():
    g = _enc_genome("enc_s2_101_58_jit"); g["id"] = "gt_pred"; return g   # ecology

def gt_coex():
    g = _enc_genome("enc_s2_116_46_jit"); g["id"] = "gt_coex"; return g   # 3-sp coexist

def gt_mv3():
    sys.path.insert(0, os.path.join(BLOBS, "machinev3"))
    import lib as mv3
    g = mv3.build_world("mimic", 0.6); g["id"] = "gt_mv3"; return g       # engine+cargo


WORLDS = dict(m0=gt_m0, m4=gt_m4, xv=gt_xv, bf=gt_bf,
              pred=gt_pred, coex=gt_coex, mv3=gt_mv3)

# Documented protocol deviation: mv3 engine blobs are operated kicked (their
# certified launch convention). kick_px per act; all other worlds: no kick.
KICKS = {"gt_mv3": {0: 0.5}}
