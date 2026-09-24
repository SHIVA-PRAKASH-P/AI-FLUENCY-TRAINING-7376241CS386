"""Run A: plain LLM prompt, no tool access at all."""
from config import MODEL, QUESTIONS, banner, client

SYSTEM_PROMPT = (
    "You are a helpful assistant. Answer using only your own knowledge and "
    "reasoning. You have no access to any private data or tools, so if a "
    "question needs private information you don't have, say so."
)


def ask_plain(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("RUN A: PLAIN LLM (NO TOOL)")
    for number, question in enumerate(QUESTIONS, 1):
        answer = ask_plain(question)
        print(f"Q{number}: {question}\nA{number}: {answer}\n" + "-" * 70)
