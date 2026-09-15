"""Private prepared-state binding for the local R6 worked example.

This file, the state cache, and its metadata belong to the evaluator. The
agent receives only the anonymous specification and experimental readings.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / 'environments/physim'))
from physim import blobround6 as R6

STUDY = ROOT / 'probes/blobs/agentenv/round6/physics/p4g2_044/sensor_study'
CACHE = ROOT / 'probes/blobs/agentenv/cache/p4g2_044_s928.npz'


def file_digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def make_origin():
    """Own the exact float32 prepared fields; future noise always starts fresh.

    Native dynamics are autonomous: t_step is an event counter, not a forcing
    phase. Rebasing 85000 to zero changes labels only. Apparatus starts in the
    previously demonstrated close/wide configuration, with the emitter fixed.
    """
    original = R6._native_oracle('p4g2_044', 928, workers=1)
    template = R6._clone_sim(original._template)
    with np.load(CACHE, allow_pickle=False) as archive:
        fields = archive['snapF_1700'].copy()
    if fields.dtype != np.float32 or fields.shape != (12, 256, 256):
        raise ValueError('Prepared origin must be the exact full-precision snapshot')
    field_digest = hashlib.sha256(fields.tobytes()).hexdigest()
    prior = json.loads((STUDY / 'noise_study/manifest.json').read_text())
    expected = {row['initial_field_sha256'] for row in prior['completed']}
    if expected != {field_digest}:
        raise ValueError('Prepared state differs from the demonstrated state')
    template['F'] = fields
    template['t_step'] = 0
    poses = json.loads((STUDY / 'early_observations.json').read_text())['context']['poses'][0]['devices']
    devices = original._devices
    for device, pose in zip(devices, poses):
        device.center = np.array(pose['center'], float)
        device.dilation = float(pose['dilation'])
        np.testing.assert_allclose(device.node_positions()[device.node_perm],
                                   pose['stream_positions'], rtol=0, atol=1e-10)
    oracle = R6.OracleRunner(_template=template, _devices=devices,
                            _port_perm=original._perm, _adjust_mix=original._mix,
                            _emitter_yx=original._emitter, _stepper=original._stepper)
    metadata = dict(world='p4g2_044', preparation_seed=928,
                    prepared_cache_member='snapF_1700', original_time=1700., public_time=0.,
                    initial_field_sha256=field_digest, field_dtype=str(fields.dtype),
                    field_shape=list(fields.shape), noise_policy=R6.NOISE_POLICY,
                    native_noise_coefficient=float(template['noise']),
                    ports=12, slots={'device0':13, 'device1':19, 'global':2},
                    source_sha256={str(p.relative_to(ROOT)):file_digest(p) for p in (
                        Path(__file__), ROOT/'environments/physim/physim/blobround6.py',
                        ROOT/'probes/blobs/agentenv/device.py',
                        ROOT/'probes/blobs/blobkit/blobkit/soup/sim_cpu.py',
                        ROOT/'environments/physim/physim/blobdata/p4g2_044.json')})
    return oracle, metadata
