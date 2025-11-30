# agents/writer_agent.py
from utils.gemini_client import generate_text, GeminiAPIError


def generate_linkedin_draft(topic: str) -> dict:
    """
    Agent A — Writer.
    Generates a LinkedIn post draft based on the given topic.
    """
    prompt = f"""
You are a professional LinkedIn copywriter.

Write a short LinkedIn post based on the topic below.

Requirements:
- maximum 5 sentences
- no emojis
- no hashtags
- avoid generic buzzwords
- be specific and concrete
- write in a natural, conversational tone

Topic: "{topic}"
""".strip()

    last_error = None

    # Try up to 3 attempts in case of transient API errors
    for attempt in range(3):
        try:
            text, usage, _ = generate_text(prompt)
            cleaned = text.strip()
            if cleaned:
                return {
                    "topic": topic,
                    "draft": cleaned,
                    "usage": usage or {},
                }
            else:
                print(f"[Writer] Empty text from Gemini on attempt {attempt + 1}")
        except GeminiAPIError as exc:
            last_error = exc
            print(f"[Writer] Gemini error on attempt {attempt + 1}: {exc}")

    # All attempts failed or returned empty text: return a safe fallback
    fallback_text = (
        "AI Writer failed to generate a draft for this topic. "
        "Please try again later or adjust the prompt."
    )

    if last_error:
        print(f"[Writer] Giving up after errors: {last_error}")

    return {
        "topic": topic,
        "draft": fallback_text,
        "usage": {},
    }
