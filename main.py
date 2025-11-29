from agents.writer_agent import generate_linkedin_draft


def main():
    topic = "The future of AI Agents in Business"
    result = generate_linkedin_draft(topic)

    print("TOPIC:", result["topic"])
    print("\nDRAFT:\n", result["draft"])
    print("\nUSAGE:", result["usage"])


if __name__ == "__main__":
    main()
