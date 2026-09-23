"""Direct prompting vs Chain-of-Thought on three reasoning-only questions.
No tools involved here - every number needed is inside the question."""

from config import client, MODEL, banner

QUESTIONS = [
    # 1. Multi-step arithmetic (tax deduction over the full duration)
    "CloudSprint offers a monthly stipend of Rs. 20,000 with a 5% tax "
    "deduction, for 3 months. What is the total net stipend you would "
    "receive over the full internship?",
    # 2. Multi-step comparison (two offers' total net stipend)
    "DataForge pays Rs. 12,000/month with an 8% tax deduction over 8 "
    "months. TechNova pays Rs. 15,000/month with a 10% tax deduction "
    "over 6 months. Which offer gives a higher total net stipend, and "
    "by how much?",
    # 3. Ordering / logic (rank three offers)
    "Rank these three internship offers by total net stipend, from "
    "highest to lowest, and state which one has the lowest monthly tax "
    "deduction rate: TechNova (Rs. 15,000/month, 10% tax, 6 months), "
    "CloudSprint (Rs. 20,000/month, 5% tax, 3 months), DataForge "
    "(Rs. 12,000/month, 8% tax, 8 months).",
]

DIRECT_PROMPT = "You are a helpful assistant. Give only the final answer. Do not explain."
COT_PROMPT = (
    "You are a helpful assistant. Solve the problem step by step. "
    "Number each step and show the calculation in that step. "
    "After the steps, write the last line exactly as: Final Answer: <answer>"
)


def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        temperature=0,
    )
    return response.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("CHAIN-OF-THOUGHT COMPARISON")
    for number, question in enumerate(QUESTIONS, start=1):
        print("=" * 72)
        print(f"QUESTION {number}: {question}\n")
        print("--- WITHOUT CoT ---")
        print(ask(DIRECT_PROMPT, question), "\n")
        print("--- WITH CoT ---")
        print(ask(COT_PROMPT, question), "\n")
