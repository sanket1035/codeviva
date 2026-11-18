"""LLM wrapper: model default and graceful fallback when the API call fails."""
import json

import pytest

from codeviva import llm
from codeviva.analyzer import analyze

SRC = "def a():\n    pass\n"


class _Boom:
    class chat:
        class completions:
            @staticmethod
            def create(**kw):
                raise RuntimeError("model_not_found")


def _fake_client(content):
    class Msg:
        pass

    class C:
        class chat:
            class completions:
                @staticmethod
                def create(**kw):
                    m = Msg()
                    m.message = Msg()
                    m.message.content = content
                    r = Msg()
                    r.choices = [m]
                    return r
    return C


def test_default_model_is_not_the_retired_one():
    assert llm.DEFAULT_MODEL != "llama-3.3-70b-versatile"


def test_no_key_uses_offline(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    res = llm.explain_and_quiz(analyze(SRC))
    assert "Offline mode" in res["summary"]


def test_api_error_falls_back_to_offline_with_message(monkeypatch):
    monkeypatch.setattr(llm, "_client", lambda: _Boom)
    res = llm.explain_and_quiz(analyze(SRC))
    assert "RuntimeError" in res["summary"] and "GROQ_MODEL" in res["summary"]
    assert "a" in res["functions"]


def test_invalid_json_falls_back(monkeypatch):
    monkeypatch.setattr(llm, "_client", lambda: _fake_client("not json"))
    res = llm.explain_and_quiz(analyze(SRC))
    assert "JSONDecodeError" in res["summary"]


def test_valid_json_is_returned(monkeypatch):
    payload = {"summary": "s", "functions": {"a": "x"}, "viva": []}
    monkeypatch.setattr(llm, "_client", lambda: _fake_client(json.dumps(payload)))
    assert llm.explain_and_quiz(analyze(SRC)) == payload
