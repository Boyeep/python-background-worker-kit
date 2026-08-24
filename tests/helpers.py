import json
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"
SNAPSHOT_DIR = Path(__file__).parent / "snapshots"


def fixture_path(name: str) -> Path:
    return FIXTURE_DIR / name


def fixture_bytes(name: str) -> bytes:
    return fixture_path(name).read_bytes()


def snapshot_json(name: str) -> dict:
    return json.loads((SNAPSHOT_DIR / name).read_text(encoding="utf-8"))


def normalize_analysis_payload(payload: dict) -> dict:
    normalized = json.loads(json.dumps(payload))
    normalized["analysis_id"] = "<analysis-id>"
    normalized["generated_at"] = "<generated-at>"
    return normalized
