"""Configuration helpers for the content generator."""

import os


def get_gemini_api_key() -> str:
    """Return a validated key, accepting values copied from a .env file."""
    value = os.getenv("GEMINI_API_KEY", "").strip()

    for prefix in ("export GEMINI_API_KEY=", "GEMINI_API_KEY="):
        if value.startswith(prefix):
            value = value.removeprefix(prefix).strip()
            break

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        value = value[1:-1].strip()

    if not value or value in {"your_api_key_here", "YOUR_GEMINI_API_KEY_HERE"}:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Set it as a GitHub Actions repository secret."
        )
    if "\n" in value or "\r" in value:
        raise RuntimeError("GEMINI_API_KEY must be a single-line value.")

    return value
