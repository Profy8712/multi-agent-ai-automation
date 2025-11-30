# utils/gemini_client.py
import os
from typing import Any, Dict, Tuple

from dotenv import load_dotenv
import google.generativeai as genai


class GeminiAPIError(Exception):
    """Raised when Google Gemini API call fails at transport or API level."""


# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

# Configure Gemini client
genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")
model = genai.GenerativeModel(MODEL_NAME)


def _extract_usage(response: Any) -> Dict[str, Any]:
    """
    Safely extracts usage metadata from a Gemini response.

    Tries to handle different SDK versions and object shapes.
    """
    usage_obj = getattr(response, "usage_metadata", None)
    if not usage_obj:
        return {}

    raw: Dict[str, Any] = {}

    # If already a dict
    if isinstance(usage_obj, dict):
        raw = dict(usage_obj)
    # If object has to_dict()
    elif hasattr(usage_obj, "to_dict"):
        try:
            raw = usage_obj.to_dict()  # type: ignore[attr-defined]
        except Exception:
            raw = {}
    else:
        # Fallback: collect numeric attributes that look like token counts
        raw = {}
        for attr in dir(usage_obj):
            if attr.startswith("_"):
                continue
            value = getattr(usage_obj, attr, None)
            if isinstance(value, (int, float)):
                raw[attr] = int(value)

    usage: Dict[str, Any] = {}

    # Keep only fields related to tokens
    for key, value in raw.items():
        if not isinstance(value, (int, float)):
            continue
        if "token" in key.lower():
            usage[key] = int(value)

    # If total_token_count is missing, try to compute it
    if "total_token_count" not in usage:
        total = 0
        for key, value in usage.items():
            if isinstance(value, int):
                total += value
        if total:
            usage["total_token_count"] = total

    return usage


def _extract_text_from_response(response: Any) -> str:
    """
    Collects all text parts from response candidates.

    Supports both object-like and dict-like structures.
    """
    text_parts = []

    try:
        candidates = getattr(response, "candidates", None)
        if candidates is None and isinstance(response, dict):
            candidates = response.get("candidates", [])
        candidates = candidates or []
    except Exception:
        candidates = []

    for cand in candidates:
        # Try to get content as attribute or dict key
        content = getattr(cand, "content", None)
        if content is None and isinstance(cand, dict):
            content = cand.get("content")
        if not content:
            continue

        # Try to get parts from attribute or dict key
        parts = getattr(content, "parts", None)
        if parts is None and isinstance(content, dict):
            parts = content.get("parts", [])
        parts = parts or []

        for part in parts:
            text_val = None

            # Object-like part
            if hasattr(part, "text"):
                text_val = getattr(part, "text", None)

            # Dict-like part
            if text_val is None and isinstance(part, dict):
                text_val = part.get("text")

            if text_val:
                text_parts.append(str(text_val))

    return "\n".join(text_parts).strip()


def generate_text(prompt: str) -> Tuple[str, Dict[str, Any], Any]:
    """
    Generates text with Gemini and returns (text, usage, raw_response).

    Raises:
        GeminiAPIError: only if the HTTP/API call itself fails.
        (Empty responses are returned as empty text.)
    """
    try:
        response = model.generate_content(
            prompt,
            generation_config={"max_output_tokens": 1024},
        )
    except Exception as exc:
        # Network/auth/model errors end up here
        raise GeminiAPIError(f"Gemini API request failed: {exc}") from exc

    text = _extract_text_from_response(response)
    usage = _extract_usage(response)

    if not text:
        # Debug log for inspection if needed
        print("[Gemini DEBUG] Empty text extracted from response. Raw response object:")
        print(repr(response))
        # Return empty text and usage (if any). Caller will decide how to fallback.
        return "", usage, response

    # If API did not return usage, estimate it roughly based on word counts
    if not usage:
        prompt_tokens = len(prompt.split())
        completion_tokens = len(text.split())
        total_tokens = prompt_tokens + completion_tokens
        usage = {
            "prompt_token_count": prompt_tokens,
            "candidates_token_count": completion_tokens,
            "total_token_count": total_tokens,
            "estimated": True,
        }

    return text, usage, response
