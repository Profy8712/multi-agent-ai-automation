from utils.gemini_client import generate_text


def generate_linkedin_draft(topic: str) -> dict:
    """
    Agent A — Writer.
    Generates a LinkedIn post draft based on the given topic.

    Returns:
        dict: {
            "topic": str,
            "draft": str,
            "usage": dict
        }
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
"""

    text, usage, _ = generate_text(prompt)

    return {
        "topic": topic,
        "draft": text.strip(),
        "usage": usage,
    }
