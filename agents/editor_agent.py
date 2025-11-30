# agents/editor_agent.py
import json
from typing import Dict, Any

from utils.gemini_client import generate_text, GeminiAPIError


EDITOR_SYSTEM_PROMPT = """
You are a strict editor. You hate generic buzzwords.

You will receive a LinkedIn post draft.
Your tasks:
1) Briefly critique the draft (maximum 3 sentences).
2) Rewrite it to be sharper, more concrete, and more impactful.

RESPONSE FORMAT (IMPORTANT):
- Respond ONLY in valid JSON.
- No additional text, no markdown, no explanations.
- Use exactly these keys: "critique" and "final_post".

Example:
{
  "critique": "The draft is too vague and uses generic language...",
  "final_post": "Here is the revised, punchier version..."
}
""".strip()


def _extract_json_block(text: str) -> str:
    """
    Extracts the JSON block from a string by taking everything
    between the first '{' and the last '}'.

    This helps when the model returns extra text around the JSON.
    """
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        return text[start : end + 1]
    return text


def edit_linkedin_post(draft: str) -> Dict[str, Any]:
    """
    Sends the writer's draft to Gemini (Editor persona) and returns
    a structured result with critique and final post.

    Returns:
        {
            "critique": str,
            "final_post": str,
            "usage": dict,
        }

    Raises:
        GeminiAPIError: if Gemini API call fails at HTTP/API level.
    """
    prompt = (
        f"{EDITOR_SYSTEM_PROMPT}\n\n"
        "DRAFT:\n"
        f"\"\"\"{draft}\"\"\""
    )

    raw_text, usage, _ = generate_text(prompt)

    cleaned = raw_text.strip()

    # If the model returned an empty response, keep the original draft
    if not cleaned:
        return {
            "critique": "Editor model returned an empty response. Keeping original draft.",
            "final_post": draft,
            "usage": usage or {},
        }

    # Remove Markdown fences if the model returns ```json ... ```
    if cleaned.startswith("```"):
        first_newline = cleaned.find("\n")
        if first_newline != -1:
            cleaned = cleaned[first_newline + 1:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

    # Try to isolate a pure JSON block
    json_candidate = _extract_json_block(cleaned)

    critique = ""
    final_post = draft

    try:
        payload = json.loads(json_candidate)
        critique = (payload.get("critique") or "").strip()
        final_post = (payload.get("final_post") or draft).strip()
    except Exception:
        # If JSON parsing fails, we still return something useful.
        critique = f"Failed to parse JSON from editor. Raw response: {cleaned}"

    return {
        "critique": critique,
            "final_post": final_post,
            "usage": usage or {},
    }
