"""LLM agents. Each subclasses BaseAgent and does one focused job."""

from agents.action_extractor import ActionExtractorAgent
from agents.base import BaseAgent
from agents.nugget_finder import NuggetFinderAgent
from agents.person_extractor import PersonExtractorAgent
from agents.summarizer import SummarizerAgent

__all__ = [
    "BaseAgent",
    "SummarizerAgent",
    "ActionExtractorAgent",
    "NuggetFinderAgent",
    "PersonExtractorAgent",
]
