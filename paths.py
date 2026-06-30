"""Paths for local dev vs Vercel serverless (/tmp for writes)."""
import os
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
VERCEL = bool(os.environ.get("VERCEL"))


def _ensure_vercel_seed_data(runtime_root: str) -> None:
    bundled = os.path.join(ROOT, "data_set", "data.csv")
    dest_dir = os.path.join(runtime_root, "data_set")
    dest = os.path.join(dest_dir, "data.csv")
    if os.path.isfile(bundled) and not os.path.isfile(dest):
        os.makedirs(dest_dir, exist_ok=True)
        shutil.copy2(bundled, dest)


def _runtime_root() -> str:
    if VERCEL:
        base = "/tmp/ims"
        os.makedirs(os.path.join(base, "data_set"), exist_ok=True)
        _ensure_vercel_seed_data(base)
        return base
    return ROOT


RUNTIME_ROOT = _runtime_root()
DATA_SET_DIR = os.path.join(RUNTIME_ROOT, "data_set")
DATA_PATH = os.path.join(DATA_SET_DIR, "data.csv")
MODEL_PATH = os.path.join(RUNTIME_ROOT, "trained_model.pkl")
STATIC_DIR = os.path.join(ROOT, "public", "static")
PLOT_DIR = os.path.join(RUNTIME_ROOT, "plots")
os.makedirs(DATA_SET_DIR, exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)
