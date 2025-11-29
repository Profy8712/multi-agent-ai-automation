import json
from typing import Dict, Any

from utils.gemini_client import generate_text


def _clean_json_raw(text: str) -> str:
    """
    Cleans the raw model output to extract a valid JSON string.
    Handles cases with Markdown code fences like ```json ... ```.
    """
    text = text.strip()

    # Remove markdown code fences if present
    if text.startswith("```"):
        # Remove starting fence with optional language (e.g. ```json)
        first_newline = text.find("\n")
        if first_newline != -1:
            text = text[first_newline + 1 :]
        # Remove ending fence
        if text.endswith("```"):
            text = text[:-3]

    return text.strip()


def edit_linkedin_post(draft: str) -> Dict[str, Any]:
    """
    Agent B — Editor.
    Takes a LinkedIn post draft, critiques it, and returns a revised version.

    The model is instructed to respond strictly in JSON format:
    {
      "critique": "...",
      "final_post": "..."
    }
    """
    prompt = f"""
You are a strict editor. You hate generic buzzwords.

You will receive a LinkedIn post draft.
Your tasks:
1) Briefly critique the draft (maximum 3 sentences).
2) Rewrite it to be sharper, more concrete, and more impactful.

RESPONSE FORMAT (IMPORTANT):
- Respond ONLY in valid JSON.
- No additional text, no markdown, no explanations.
- Use exactly these keys: "critique" and "final_post".

Example of the expected response:
{{
  "critique": "The draft is too vague and uses generic language...",
  "final_post": "Here is the revised, punchier version..."
}}

Now edit this draft:

DRAFT:
\"\"\"{draft}\"\"\" 
"""

    text, usage, _ = generate_text(prompt)

    raw = text or ""
    cleaned = _clean_json_raw(raw)

    try:
        data = json.loads(cleaned)
    except json.JSONDecodeError as e:
        # Basic error handling: return a fallback structure
        return {
            "critique": f"Failed to parse JSON from model output. Error: {e}. Raw output: {raw}",
            "final_post": draft,
            "usage": usage,
            "raw_output": raw,
        }

    # Ensure keys exist
    critique = data.get("critique", "").strip()
    final_post = data.get("final_post", "").strip()

    return {
        "critique": critique,
        "final_post": final_post,
        "usage": usage,
        "raw_output": raw,
    }
