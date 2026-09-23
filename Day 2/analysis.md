# Analysis: Direct Prompting vs Chain-of-Thought vs ReAct
### Scenario: Internship Stipend Assistant

**Setup used for these runs:** provider `groq`, model `openai/gpt-oss-120b`.
**Intern:** Saran, AI/ML Intern at TechNova since 2026-06, with 3
offers on the table (TechNova, CloudSprint, DataForge) and 3 months of
real payment history already on record.

---

## 3.1 Explanation of each approach

### Direct prompting
Direct prompting answers immediately from the model's own knowledge,
with no visible reasoning and no tool access.

- **Can answer:** self-contained questions where every number needed
  is already stated in the prompt and the model's arithmetic is
  reliable enough to combine them correctly in one pass.
- **Cannot answer:** anything needing this intern's actual, private
  data — the current payment history or which company he's really
  interning at — since none of that is in its training data.
- **How it arrives at an answer:** one forward pass, question straight
  to answer, no visible working.
- **On this scenario:** direct prompting got **all three**
  reasoning-only questions exactly right (see 3.2) — correct totals,
  correct comparison, correct ranking, correct tax-rate identification.
  Its limitation only shows up on the tool-needing question, where it
  would have no way to know Saran has already been paid Rs. 40,500, or
  even which company he currently works for.

### Chain-of-Thought (CoT)
CoT makes the model show numbered, worked steps before answering. It
still can't fetch a fact it doesn't have — it can only reason more
carefully over what's already in the prompt.

- **Can answer:** the same self-contained questions as direct
  prompting, with visible, checkable working.
- **Cannot answer:** the tool-needing question — no amount of careful
  reasoning substitutes for actually knowing Saran's real payment
  history.
- **How it arrives at an answer:** the prompt instructs numbered
  steps, a shown calculation per step, and a final `Final Answer:`
  line; still one model pass, just a longer and more structured one.
- **On this scenario:** CoT matched direct prompting on all three
  questions — same correct totals (57,000 / 7,320 difference /
  DataForge > TechNova > CloudSprint), just with the full working
  shown. As in the vehicle-maintenance scenario, `gpt-oss-120b` is
  strong enough at this scale of arithmetic that CoT didn't need to
  *fix* anything here — its value would show up more clearly on a
  smaller model, where direct prompting is more likely to slip on a
  three-way percentage-and-duration calculation like this.

### ReAct
ReAct interleaves Thought, Action, and Observation — reasoning about
what it needs, calling a tool, reading the result, and repeating.

- **Can answer:** questions needing Saran's real, private data — the
  tool-needing question in this scenario is exactly that case.
- **How it arrives at an answer:** `agent.py`'s loop lets the model
  call `get_offer_details`, `get_payment_history`, `list_offers`, and
  `calculator`, feeding each result back until it can produce a final
  answer or it runs out of steps.
- **On this scenario (`react_trace.py` output):** this is where the
  real result got interesting. The agent's *reasoning was entirely
  correct* — it looked up TechNova's offer, pulled the full payment
  history, listed and looked up the other two offers, then ran five
  separate calculator calls to get:
  - TechNova total: 15,000 × 0.9 × 6 = **81,000**
  - CloudSprint total: 20,000 × 0.95 × 3 = **57,000**
  - DataForge total: 12,000 × 0.92 × 8 = **88,320** (highest)
  - Already paid: 13,500 × 3 = **40,500**
  - Remaining to be paid: 81,000 − 40,500 = **40,500**

  Every one of these matches the hand-worked values. But the agent
  used one tool call per step and needed 10 steps just to gather and
  compute everything — with `max_steps=10`, it hit the limit *before*
  it had a turn left to write the final sentence, and the run ended
  with `"Stopped: maximum steps reached without a final answer."`
  The reasoning was flawless; the failure was purely a **step-budget
  problem** in how the loop was configured, not a reasoning or
  tool-use error. `max_steps` has been raised to 14 for the next run.

## 3.2 Comparison table

| Basis for comparison | Direct prompting | Chain-of-Thought | ReAct agent |
|---|---|---|---|
| Reasoning depth | None visible — single-shot answer | Explicit, numbered steps with shown calculations | Same depth of reasoning as CoT, but interleaved with real tool calls and their raw results |
| Tool usage | None | None | 10 tool calls across 4 tools in this run (`get_offer_details` ×3, `get_payment_history`, `list_offers`, `calculator` ×5) |
| Reliability on multi-step questions | High on this model (3/3 correct) with no way to verify *why* | High — all reasoning shown and correct on all 3 questions | Every individual computation was correct, but the run **failed to complete** because it ran out of steps — reliability depends on both reasoning *and* correctly sizing `max_steps` |
| Transparency (can you see how it got the answer?) | No — black box | Yes — full worked steps shown | Yes, and more so than CoT — every tool call and its exact raw output is printed, which is exactly how this step-budget issue was caught |
| Speed / cost | Fastest, cheapest — one short completion | Slower/costlier — longer completion with full working | Slowest/costliest by far — 10 sequential LLM calls plus tool execution, and this run didn't even finish |
| Consistency across repeated runs | Not tested directly here | Tested via self-consistency: 5/5 runs on Q1 gave the same number (57,000) at `temperature=0.8`, though the majority-vote count read "2 of 5" due to formatting differences | Not repeated in this run; deterministic tool outputs mean the underlying facts wouldn't change between runs, but a tight `max_steps` could cause the *same* run to fail again |

## 3.3 Self-consistency observation

Ran Question 1 ("CloudSprint's total net stipend over 3 months") 5
times at `temperature=0.8`:

```
run 1: 57,000 Rs.
run 2: Rs. 57,000
run 3: 57,000
run 4: Rs. 57,000
run 5: Rs 57,000
```

Every run reached the same correct number, **57,000**. The script
reported the majority as **2 of 5**, because only runs 2 and 4 matched
character-for-character ("Rs. 57,000"); the other three used slightly
different wording or punctuation ("57,000 Rs.", "57,000" with no
currency mark, "Rs 57,000" with no period). This is the same
formatting-artifact issue seen in the vehicle-maintenance scenario:
the model's *reasoning* agreed 5/5 times, but a plain string-equality
vote undercounts that agreement whenever the surface wording varies.
It's a reminder that self-consistency's usefulness depends on
normalizing answers (stripping currency symbols/punctuation, or
extracting just the numeric value) before voting — otherwise it can
report disagreement that isn't really there.

At `temperature=0` (as used in `cot_compare.py`), the single
deterministic run also gave 57,000, consistent with what all 5
higher-temperature runs converged to.

## 3.4 Suitability analysis

**ReAct is still the right approach for this scenario in principle**
— the tool-needing question depends on Saran's real payment history
and his actual current employer, neither of which any LLM could know
without being told. Direct prompting and CoT can only work with
numbers already present in the prompt; they have no way to answer
"how much have I already been paid?" without that data being handed
to them inline.

But this run is also a useful cautionary example: **correct tool use
does not guarantee a correct final answer if the step budget is too
tight.** This scenario needed more tool calls than the vehicle one
(5 lookups + 5 calculations vs. 6 lookups + 1 total there), because
each fact and each calculation consumed its own step one at a time.
Practically, that means sizing `max_steps` to the scenario — a rule of
thumb is (number of facts to look up) + (number of calculations) + 1
turn to compose the final answer — rather than reusing a fixed number
across different scenarios.

For the self-contained reasoning questions, direct prompting and CoT
were both fully correct and dramatically cheaper/faster than ReAct, so
a well-designed real assistant would still route only the
data-dependent question to the ReAct path and answer the rest directly
or with CoT.

## 3.5 Conclusion

In general:

- **Direct prompting** suits simple questions where all the needed
  information is already given and the model is strong enough for the
  arithmetic involved — cheapest and fastest, but no transparency and
  no protection against silent errors.
- **Chain-of-Thought** suits questions needing several dependent
  reasoning steps where you want to see and trust the working,
  especially valuable on smaller or weaker models — slower than direct
  prompting but still self-contained.
- **ReAct** suits questions that depend on information the model
  cannot be expected to know in advance — private records, live data,
  anything that changes over time. It is the only approach of the
  three that can go get that information before answering, but it is
  also the most fragile operationally: this run shows that even
  perfect step-by-step tool use can still fail to produce an answer if
  the surrounding loop (here, `max_steps`) isn't sized generously
  enough for how many tool calls the question actually needs.
