from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from .models import State


DATA_PATH = Path(__file__).parent / "data"
STATE_FILE = DATA_PATH / "state.json"


def _ensure_data_dir() -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)


def save_state(state: State) -> dict:
    """Persist the in-memory state to disk with JSON-compatible payloads."""

    _ensure_data_dir()
    payload = state.model_dump(mode="json")
    STATE_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    return {"path": str(STATE_FILE), "updated_at": datetime.utcnow().isoformat()}


def load_state() -> State:
    """Load the state from disk if present, otherwise return an empty State."""

    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        try:
            return State.model_validate(data)
        except Exception:
            # If the file is corrupted, start fresh but keep a backup
            backup = STATE_FILE.with_suffix(".corrupted.json")
            STATE_FILE.rename(backup)
    return State()


def storage_info() -> dict:
    _ensure_data_dir()
    info = {"path": str(STATE_FILE), "exists": STATE_FILE.exists()}
    if STATE_FILE.exists():
        info["updated_at"] = datetime.utcfromtimestamp(STATE_FILE.stat().st_mtime).isoformat()
        info["size"] = STATE_FILE.stat().st_size
    return info
