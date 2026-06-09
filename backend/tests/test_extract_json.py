"""Unit tests for BaseAgent.extract_json — pure, no network or DB needed."""

import pytest

from agents.base import BaseAgent


def test_clean_json_object():
    assert BaseAgent.extract_json('{"a": 1}') == {"a": 1}


def test_clean_json_array():
    assert BaseAgent.extract_json("[1, 2, 3]") == [1, 2, 3]


def test_fenced_json():
    text = "```json\n{\"a\": 1}\n```"
    assert BaseAgent.extract_json(text) == {"a": 1}


def test_plain_fence():
    text = "```\n{\"a\": 1}\n```"
    assert BaseAgent.extract_json(text) == {"a": 1}


def test_json_embedded_in_prose():
    text = 'Sure! Here is the result: {"a": 1, "b": [2, 3]} Hope that helps.'
    assert BaseAgent.extract_json(text) == {"a": 1, "b": [2, 3]}


def test_brace_inside_string_does_not_break_balance():
    text = 'prefix {"note": "a } here", "ok": true} suffix'
    assert BaseAgent.extract_json(text) == {"note": "a } here", "ok": True}


def test_unparseable_raises():
    with pytest.raises(ValueError):
        BaseAgent.extract_json("no json at all")
