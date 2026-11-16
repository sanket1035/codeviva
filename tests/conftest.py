from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def sample():
    def _read(name: str) -> str:
        return (ROOT / "samples" / f"{name}.py").read_text(encoding="utf-8")
    return _read
