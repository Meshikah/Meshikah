"""Dogfooding: this repository's own files must satisfy the kernel schemas."""

import hashlib
import json
from pathlib import Path

import pytest
import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]
SCHEMAS = ROOT / "kernel" / "schemas"


def validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(json.loads((SCHEMAS / name).read_text(encoding="utf-8")))


@pytest.mark.parametrize("path", sorted(ROOT.glob("**/work/*/context.json")), ids=str)
def test_context_files_match_schema(path):
    errors = list(validator("context.schema.json").iter_errors(json.loads(path.read_text(encoding="utf-8"))))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("path", sorted(ROOT.glob("**/meshikah.yaml")), ids=str)
def test_meshikah_yaml_match_schema(path):
    errors = list(validator("meshikah.schema.json").iter_errors(yaml.safe_load(path.read_text(encoding="utf-8"))))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("path", sorted((ROOT / "packs").glob("*/pack.yaml")), ids=str)
def test_packs_match_schema(path):
    errors = list(validator("pack.schema.json").iter_errors(yaml.safe_load(path.read_text(encoding="utf-8"))))
    assert not errors, [e.message for e in errors]


@pytest.mark.parametrize("path", sorted(ROOT.glob("**/work/*/record.jsonl")), ids=str)
def test_records_are_valid_and_chained(path):
    v = validator("record-event.schema.json")
    prev = None
    for raw in path.read_bytes().splitlines():
        event = json.loads(raw)
        errors = list(v.iter_errors(event))
        assert not errors, [e.message for e in errors]
        assert event["prev"] == prev, "hash chain broken"
        prev = "sha256:" + hashlib.sha256(raw).hexdigest()
