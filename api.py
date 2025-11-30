import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from agents.writer_agent import generate_linkedin_draft
from agents.editor_agent import edit_linkedin_post
from utils.google_sheets import append_post_row, GoogleSheetsError
from utils.gemini_client import GeminiAPIError


# Load environment variables from .env
load_dotenv()

# Load token price for cost calculation
TOKEN_PRICE = float(os.getenv("TOKEN_PRICE", 0.000002))


def _safe_total_tokens(writer_usage, editor_usage) -> int:
    """
    Safely sums total tokens from writer and editor usage dicts.
    Supports multiple possible usage formats.
    """

    def _extract_total(usage: dict) -> int:
        if not isinstance(usage, dict):
            return 0
        # New SDK field
        if usage.get("total_token_count") is not None:
            return int(usage.get("total_token_count") or 0)
        # Possible legacy fields
        if usage.get("totalTokens") is not None:
            return int(usage.get("totalTokens") or 0)
        if usage.get("total_tokens") is not None:
            return int(usage.get("total_tokens") or 0)
        return 0

    writer_tokens = _extract_total(writer_usage)
    editor_tokens = _extract_total(editor_usage)

    return writer_tokens + editor_tokens


class TopicRequest(BaseModel):
    """Incoming payload with a single topic field."""
    topic: str


class PostResponse(BaseModel):
    """Structured response for the generated and edited post."""
    topic: str
    draft: str
    critique: str
    final_post: str
    total_tokens: int
    cost: float


app = FastAPI(title="Multi-Agent LinkedIn Post API")


@app.post("/generate-post", response_model=PostResponse)
async def generate_post(payload: TopicRequest) -> PostResponse:
    """
    REST endpoint that runs the full workflow:

    1. Writer agent generates a draft.
    2. Editor agent critiques and refines the draft.
    3. Token usage is combined and cost is calculated.
    4. The result is appended to Google Sheets.
    5. The final structured result is returned as JSON.
    """
    topic = payload.topic

    try:
        # Step 1: Writer agent
        writer_result = generate_linkedin_draft(topic)

        # Step 2: Editor agent
        editor_result = edit_linkedin_post(writer_result["draft"])

    except GeminiAPIError as exc:
        # Upstream LLM error: return 502 to indicate bad gateway from model
        raise HTTPException(
            status_code=502,
            detail=f"Gemini API failed during content generation: {exc}",
        )

    # Step 3: Token calculation
    total_tokens = _safe_total_tokens(writer_result["usage"], editor_result["usage"])

    # Step 4: Cost calculation
    cost = total_tokens * TOKEN_PRICE

    # Step 5: Log to Google Sheets (non-fatal if it fails)
    try:
        append_post_row(
            topic=topic,
            draft=writer_result["draft"],
            final_post=editor_result["final_post"],
            total_tokens=total_tokens,
            cost=cost,
        )
    except GoogleSheetsError as exc:
        # Log the error to console, but do not break the API response
        print("[WARNING] Failed to append row to Google Sheets:", exc)

    return PostResponse(
        topic=topic,
        draft=writer_result["draft"],
        critique=editor_result["critique"],
        final_post=editor_result["final_post"],
        total_tokens=total_tokens,
        cost=cost,
    )
