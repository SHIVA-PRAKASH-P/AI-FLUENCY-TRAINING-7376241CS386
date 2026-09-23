"""ReAct: run the tool-needing scenario question through the agent and
print its Thought/Action/Observation-style trace."""

from agent import agent

QUESTION = (
    "Based on my current internship at TechNova, how much total net stipend "
    "will I receive by the time it ends, how much have I already been paid, "
    "and which of the three available offers would give me the highest "
    "total net stipend overall?"
)

print("QUESTION:", QUESTION, "\n")
print("--- agent's actions and observations ---")
answer = agent(QUESTION, max_steps=14)
print("\nFINAL ANSWER:", answer)
