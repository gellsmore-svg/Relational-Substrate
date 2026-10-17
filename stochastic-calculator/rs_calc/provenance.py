"""Run manifests and source provenance outside the arithmetic mechanism."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import platform
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[1]


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def manifest(config: dict) -> dict:
    files = sorted((ROOT / "rs_calc").glob("*.py"))
    files.extend(sorted((ROOT / "configs").glob("*.json")))
    sources = {str(p.relative_to(ROOT)): sha256(p.read_bytes()).hexdigest() for p in files}
    revision = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True)
    dirty = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT, capture_output=True, text=True)
    return {"timestamp": timestamp(), "config": config,
            "config_sha256": sha256(json.dumps(config, sort_keys=True).encode()).hexdigest(),
            "git_revision": revision.stdout.strip() or "unknown", "dirty": bool(dirty.stdout),
            "source_sha256": sha256(json.dumps(sources, sort_keys=True).encode()).hexdigest(),
            "source_files": sources, "python": platform.python_version(),
            "platform": platform.platform(), "rng": "random.Random / MT19937",
            "seed_policy": "base_seed plus trial ordinal; independent PRNG per trial"}


def write_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def archive_sources(output: Path):
    with tarfile.open(output / "source.tar.gz", "w:gz") as archive:
        for directory in ["rs_calc", "configs", "tests"]:
            for path in sorted((ROOT / directory).glob("*")):
                if path.is_file() and path.suffix in {".py", ".json"}:
                    archive.add(path, arcname=str(path.relative_to(ROOT)))
        archive.add(ROOT / "pyproject.toml", arcname="pyproject.toml")
