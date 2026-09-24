"""Run B: LLM with ONE tool available. Single call, no loop."""
import json

from config import MODEL, QUESTIONS, banner, client
from tool import TOOL_SCHEMA, get_internship_info

SYSTEM_PROMPT = (
    "You are Saran's internship stipend assistant. Never guess a private "
    "figure: call get_internship_info to look up profile, offers, or "
    "payment data, then do any arithmetic yourself using the numbers it "
    "returns. If the question doesn't need private data, answer directly "
    "without calling the tool."
)


def ask_with_tool(question):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]
    calls_made = []

    # 1. Ask the model what to do (it may or may not request the tool)
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=[TOOL_SCHEMA], temperature=0,
    )
    message = response.choices[0].message

    if not message.tool_calls:
        return calls_made, message.content.strip()

    messages.append({
        "role": "assistant", "content": message.content or "",
        "tool_calls": [{"id": c.id, "type": "function",
                         "function": {"name": c.function.name,
                                      "arguments": c.function.arguments}}
                        for c in message.tool_calls]})

    # 2. Run the tool call(s) it asked for and feed the result back
    for call in message.tool_calls:
        arguments = json.loads(call.function.arguments or "{}")
        section = arguments.get("section", "")
        result = get_internship_info(section)
        calls_made.append(f"get_internship_info(section='{section}') -> {result}")
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

    # 3. One more call to get the final answer (no further tool calls allowed)
    final = client.chat.completions.create(model=MODEL, messages=messages, temperature=0)
    return calls_made, final.choices[0].message.content.strip()


if __name__ == "__main__":
    banner("RUN B: LLM WITH TOOL")
    for number, question in enumerate(QUESTIONS, 1):
        calls, answer = ask_with_tool(question)
        shown = "\n".join(f"  TOOL CALL: {c}" for c in calls) or "  TOOL CALL: (none)"
        print(f"Q{number}: {question}\n{shown}\nA{number}: {answer}\n" + "-" * 70)
