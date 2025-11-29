from agents.writer_agent import generate_linkedin_draft
from agents.editor_agent import edit_linkedin_post
from utils.google_sheets import append_post_row


def _safe_total_tokens(writer_usage, editor_usage) -> int:
    """
    Safely sums total tokens from writer and editor usage dicts.
    """
    writer_tokens = 0
    editor_tokens = 0

    if isinstance(writer_usage, dict):
        writer_tokens = writer_usage.get("total_tokens", 0) or 0

    if isinstance(editor_usage, dict):
        editor_tokens = editor_usage.get("total_tokens", 0) or 0

    return int(writer_tokens) + int(editor_tokens)


def main():
    topic = "The future of AI Agents in Business"

    # Agent A — Writer
    writer_result = generate_linkedin_draft(topic)

    # Agent B — Editor
    editor_result = edit_linkedin_post(writer_result["draft"])

    total_tokens = _safe_total_tokens(writer_result["usage"], editor_result["usage"])

    # Print results to console
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

    # Save to Google Sheets
    append_post_row(
        topic=topic,
        draft=writer_result["draft"],
        final_post=editor_result["final_post"],
        total_tokens=total_tokens,
    )

    print("\nRow successfully appended to Google Sheets.")


if __name__ == "__main__":
    main()
