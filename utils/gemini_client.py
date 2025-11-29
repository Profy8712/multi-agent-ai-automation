import os
from typing import Any, Dict, Tuple

from dotenv import load_dotenv
import google.generativeai as genai


class GeminiAPIError(Exception):
    """Raised when Google Gemini API call fails."""


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("Missing GEMINI_API_KEY in .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("GEMINI_MODEL_NAME", "models/gemini-2.5-flash")

model = genai.GenerativeModel(MODEL_NAME)


def generate_text(prompt: str) -> Tuple[str, Dict[str, Any], Any]:
    try:
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1024,
                "temperature": 0.2,
            }
        )
    except Exception as exc:
        raise GeminiAPIError(f"Gemini API request failed: {exc}")

    # ---- SAFETY FALLBACK ----
    try:
        text = (response.text or "").strip()
    except Exception:
        text = ""

        try:
            if response.candidates:
                parts = response.candidates[0].content.parts
                if parts:
                    text = parts[0].text or ""
        except:
            text = ""

    # ---- USAGE METADATA ----
    usage = {}
    try:
        usage = response.usage_metadata.to_dict()
    except:
        pass

    return text.strip(), usage, response
