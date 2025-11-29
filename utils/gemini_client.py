import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY is missing in .env")

# Configure Gemini API
genai.configure(api_key=API_KEY)


def generate_text(prompt: str):
    """
    Wrapper for Gemini API.

    Returns:
        text (str): Generated text output.
        usage (dict): Token usage information.
        response (object): Raw Gemini response object.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)

    text = response.text or ""

    usage = None
    if getattr(response, "usage_metadata", None):
        usage = {
            "prompt_tokens": response.usage_metadata.prompt_token_count,
            "candidates_tokens": response.usage_metadata.candidates_token_count,
            "total_tokens": response.usage_metadata.total_token_count,
        }

    return text, usage, response
