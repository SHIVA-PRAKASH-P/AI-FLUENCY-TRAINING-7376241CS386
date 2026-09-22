# Internship Stipend Calculator — Chatbot vs Workflow vs Agent

> Fill this in after actually running chatbot.py, workflow.py, agent.py,
> and challenge.py, and looking at your real output. Write full paragraphs
> — this file is graded on its own, without your code.

## 1. Scenario

Describe the scenario in your own words: three internship offers
(TechNova, CloudSprint, DataForge) with different monthly stipends,
durations, and tax deduction rates, plus a payment history for an ongoing
internship — private data no public LLM has seen.

## 2. Explanation of each approach

### 2.1 Plain chatbot
- What data can it access? What happened when you ran chatbot.py on the
  net-stipend and total-received questions — did it guess, or ask for
  the numbers, or something else?
- Why did Q4 (thank-you message) come out fine regardless?

### 2.2 Rule-based workflow
- What exactly did each of the three rules in workflow.py check for?
- Why were its answers instant and exact for the questions it was built
  for, and why did it fail the thank-you-message question?

### 2.3 AI agent
- Walk through the printed steps for at least two questions — which
  tools did it call, in what order, and were the numbers correct?
- For the challenge question, how many of the three offers did the agent
  actually check with `get_offer_details`/`calculate_total_payout` before
  answering? If it skipped any, does its answer still happen to be
  correct, or is it wrong because it didn't check enough?
- Note down any place the agent's final sentence didn't match what its
  own tool calls returned — that's a genuine finding, not something to
  hide.

## 3. Comparison table

| Basis for comparison   | Plain chatbot | Rule-based workflow | AI agent |
|-------------------------|---------------|----------------------|----------|
| Flexibility              |               |                      |          |
| Decision-making          |               |                      |          |
| Tool usage                |               |                      |          |
| Private-data access      |               |                      |          |
| Multi-step task handling |               |                      |          |
| Automation                |               |                      |          |
| Reliability               |               |                      |          |

## 4. Suitability analysis

For an internship stipend calculator, is exact reliability (workflow) or
flexible reasoning (agent) more important? Consider: would you rather a
tool refuse to answer a question it wasn't built for, or attempt an
answer that might be subtly wrong (like checking only 1 of 3 offers)?

## 5. Conclusion

In general — when is a chatbot enough? When does a workflow beat an
agent? When is an agent worth the unpredictability? 2–3 sentences each.
