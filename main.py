import os

from dotenv import load_dotenv

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
    Supports both old and new Gemini usage formats.
    """

    def _extract_total(usage: dict) -> int:
        if not isinstance(usage, dict):
            return 0
        # New SDK: total_token_count
        if usage.get("total_token_count") is not None:
            return int(usage.get("total_token_count") or 0)
        # Old naming: totalTokens / total_tokens
        if usage.get("totalTokens") is not None:
            return int(usage.get("totalTokens") or 0)
        if usage.get("total_tokens") is not None:
            return int(usage.get("total_tokens") or 0)
        return 0

    writer_tokens = _extract_total(writer_usage)
    editor_tokens = _extract_total(editor_usage)

    return writer_tokens + editor_tokens


def main() -> None:
    """
    Main workflow:
      1. Writer Agent generates a draft.
      2. Editor Agent critiques and rewrites it.
      3. Token usage is combined.
      4. Cost is calculated.
      5. Everything is saved into Google Sheets.

    Basic error handling is applied around Gemini and Google Sheets calls.
    """
    topic = "The future of AI Agents in Business"

    try:
        # --- Step 1: Writer Agent ---
        writer_result = generate_linkedin_draft(topic)

        # --- Step 2: Editor Agent ---
        editor_result = edit_linkedin_post(writer_result["draft"])

    except GeminiAPIError as exc:
        print("\n[ERROR] Gemini API failed during content generation.")
        print(f"Details: {exc}")
        return

    # --- Step 3: Token calculation ---
    total_tokens = _safe_total_tokens(writer_result["usage"], editor_result["usage"])

    # --- Step 4: Cost calculation ---
    cost = total_tokens * TOKEN_PRICE

    # --- Print results ---
    print("TOPIC:", writer_result["topic"])

    print("\n--- DRAFT (Agent A) ---\n")
    print(writer_result["draft"])

    print("\n--- EDITOR CRITIQUE (Agent B) ---\n")
    print(editor_result["critique"])

    print("\n--- FINAL POST (Agent B) ---\n")
    print(editor_result["final_post"])

    print("\n--- TOKEN USAGE ---")
    print("Writer usage:", writer_result["usage"])
    print("Editor usage:", editor_result["usage"])
    print("Total tokens:", total_tokens)
    print("Estimated cost:", cost)

    # --- Step 5: Save to Google Sheets ---
    try:
        append_post_row(
            topic=topic,
            draft=writer_result["draft"],
            final_post=editor_result["final_post"],
            total_tokens=total_tokens,
            cost=cost,
        )
        print("\nRow successfully appended to Google Sheets.")
    except GoogleSheetsError as exc:
        print("\n[WARNING] Failed to write data to Google Sheets.")
        print(f"Details: {exc}")
        print("The workflow finished, but the result was not logged to the sheet.")


if __name__ == "__main__":
    main()
