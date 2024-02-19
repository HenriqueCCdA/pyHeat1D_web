from pathlib import Path

CASE_FILE = {
    "length": 100.0,
    "ndiv": 10_000,
    "dt": 1.0,
    "nstep": 100,
    "initialt": 50.0,
    "lbc": {"type": 1, "params": {"value": 0.0}},
    "rbc": {"type": 1, "params": {"value": 100.0}},
    "prop": {"k": 1.0, "ro": 1.0, "cp": 1.0},
    "write_every_steps": 100,
}

EDIT_CASE_FILE = {
    "length": 512.0,
    "ndiv": 11_234,
    "dt": 1.1,
    "nstep": 112,
    "initialt": 51.2,
    "lbc": {"type": 1, "params": {"value": 0.2}},
    "rbc": {"type": 1, "params": {"value": 221.0}},
    "prop": {"k": 1.0, "ro": 1.0, "cp": 1.0},
    "write_every_steps": 100,
}

INPUT_CASE_FILE = Path.cwd() / "pyheat1d_web/core/tests/assets/case.json"
