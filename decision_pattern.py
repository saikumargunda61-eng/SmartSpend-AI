"""Reusable Strands Decider 2B tool-selection recipe.

Calls the official strands-decider HTTP API and applies a confidence threshold.
This module is intentionally separable so other agents can reuse the pattern.
"""
import os
import requests

DECIDER_URL = os.getenv("STRANDS_DECIDER_URL", "http://127.0.0.1:8099")
DECIDER_MODEL = os.getenv(
    "STRANDS_DECIDER_MODEL",
    "StrandsAgents/strands-decider-2B-qwen3.5-v1-2610",
)
OPTIONS = ["CHECK_BUDGET", "CHECK_UPCOMING_EXPENSES", "GIVE_SAVING_ADVICE"]

def choose_action(state: str) -> dict:
    """Return {'choice': str, 'confidence': float, 'model': str}."""
    payload = {
        "state": state,
        "questions": {
            "next_action": {
                "type": "choice",
                "instructions": (
                    "Choose the single best next tool for a student spending assistant. "
                    "CHECK_BUDGET means calculate money remaining after essential expenses "
                    "and compare it with a planned purchase. CHECK_UPCOMING_EXPENSES means "
                    "focus on future bills or essential expenses. GIVE_SAVING_ADVICE means "
                    "the user mainly asks for general ways to save or reduce spending."
                ),
                "options": OPTIONS,
            }
        },
    }
    response = requests.post(
        f"{DECIDER_URL.rstrip('/')}/v1/systemone",
        json=payload,
        timeout=90,
    )
    response.raise_for_status()
    body = response.json()
    answer = body["answers"]["next_action"]
    choice = answer.get("choice")
    confidence = float(answer.get("confidence", 0.0))
    if choice not in OPTIONS:
        raise ValueError(f"Decider returned unsupported choice: {choice!r}")
    return {"choice": choice, "confidence": confidence, "model": body.get("model", DECIDER_MODEL)}
