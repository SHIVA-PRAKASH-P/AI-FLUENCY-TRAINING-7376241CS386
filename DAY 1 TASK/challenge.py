"""A question none of the three systems was designed for."""
from agent import agent
from workflow import workflow

QUESTION = "Which internship offer gives the highest total payout over its full duration, and what is that amount?"

print("Q:", QUESTION)
print("\nWorkflow :", workflow(QUESTION))
print("\nAgent    :", agent(QUESTION))
