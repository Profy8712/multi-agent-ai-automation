from agents.writer_agent import generate_linkedin_draft
from agents.editor_agent import edit_linkedin_post


def main():
    topic = "The future of AI Agents in Business"

    # Agent A — Writer
    writer_result = generate_linkedin_draft(topic)

    # Agent B — Editor
    editor_result = edit_linkedin_post(writer_result["draft"])

    # Print results
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


if __name__ == "__main__":
    main()
