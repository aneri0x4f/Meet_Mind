"""BaseAgent — shared LLM plumbing for all agents.

Uses the OpenAI SDK against an OpenAI-compatible gateway. The gateway does NOT
support `response_format={"type": "json_object"}`, so `call_json()` asks for JSON
in the prompt and recovers it from the text with `extract_json()`.
"""

from __future__ import annotations

import json
import re
from typing import Any

from config import get_client, get_settings


class BaseAgent:
    """Base class for all agents.

    Subclasses typically set `system` and implement a `run(transcript)` method
    that calls `self.call_json(...)`.
    """

    #: Default system prompt; override in subclasses.
    system: str = "You are a careful, precise assistant."

    #: Sampling temperature; override per agent if needed.
    temperature: float = 0.2

    def __init__(self) -> None:
        self._client = get_client()
        self._model = get_settings().model_name

    def call(self, prompt: str, *, system: str | None = None) -> str:
        """Send a single-turn chat completion and return the text content."""
        response = self._client.chat.completions.create(
            model=self._model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system or self.system},
                {"role": "user", "content": prompt},
            ],
        )
        return response.choices[0].message.content or ""

    def call_json(self, prompt: str, *, system: str | None = None) -> Any:
        """Call the model and parse a JSON object/array out of the response.

        We append an explicit JSON-only instruction rather than using the
        unsupported `response_format` json mode.
        """
        json_prompt = (
            f"{prompt}\n\n"
            "Respond with ONLY valid JSON. Do not include any prose, explanation, "
            "or markdown fences outside the JSON."
        )
        text = self.call(json_prompt, system=system)
        return self.extract_json(text)

    @staticmethod
    def extract_json(text: str) -> Any:
        """Best-effort extraction of a JSON value from model text.

        Handles: clean JSON, ```json fenced blocks, and JSON embedded in prose.
        Raises ValueError if nothing parseable is found.
        """
        if text is None:
            raise ValueError("Empty model response")

        candidate = text.strip()

        # 1) Strip a ```json ... ``` (or plain ```) fence if present.
        fence = re.search(r"```(?:json)?\s*(.*?)```", candidate, re.DOTALL)
        if fence:
            candidate = fence.group(1).strip()

        # 2) Try parsing the whole thing.
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

        # 3) Fall back to the first balanced {...} or [...] span.
        span = BaseAgent._first_json_span(candidate)
        if span is not None:
            try:
                return json.loads(span)
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not extract JSON from model response: {text[:200]!r}")

    @staticmethod
    def _first_json_span(text: str) -> str | None:
        """Return the first balanced JSON object/array substring, or None."""
        start = None
        opener = None
        depth = 0
        in_str = False
        escape = False

        pairs = {"{": "}", "[": "]"}
        for i, ch in enumerate(text):
            if start is None:
                if ch in pairs:
                    start = i
                    opener = ch
                    depth = 1
                continue

            if in_str:
                if escape:
                    escape = False
                elif ch == "\\":
                    escape = True
                elif ch == '"':
                    in_str = False
                continue

            if ch == '"':
                in_str = True
            elif ch == opener:
                depth += 1
            elif ch == pairs[opener]:
                depth -= 1
                if depth == 0:
                    return text[start : i + 1]
        return None
