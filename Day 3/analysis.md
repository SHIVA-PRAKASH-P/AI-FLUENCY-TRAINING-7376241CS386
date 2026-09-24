# Day 3 Analysis: LLM with a Single Tool

**Scenario:** Internship Stipend Assistant for Saran
**Model used:** *(fill in — copy the exact provider/model from your terminal's banner line, e.g. "ollama | qwen3:4b")*

## 1. Concepts

### 1.1 What is an LLM, in this context?

A large language model is a next-token predictor trained on huge amounts
of text. On its own it can only answer from patterns it learned during
training — it has never seen Saran's offers, payments, or profile, so
any specific figure it gives for those is either a refusal to answer, a
request for the missing numbers, or a guess. It has no memory of this
conversation's private data beyond what's placed in its prompt.

### 1.2 What is a tool, and what does the schema do?

A tool is a plain Python function the LLM cannot call directly — it can
only ask for it. The JSON Schema attached to a tool (name, description,
parameter types) is the only thing the model sees when deciding whether
to call it and what arguments to pass. Here, `get_internship_info` has a
single `section` argument restricted to an enum of `profile`, `offers`,
`payments`, so the model can't pass an arbitrary string — it's nudged
toward a valid call. This is a smaller version of the multi-tool
registry used in the Day 2 agent (`tools.py`), where five separate
functions did what this one function now does with a parameter.

### 1.3 The tool-call flow

1. The user's question and the tool schema are sent to the model.
2. The model either answers directly, or returns a `tool_calls` entry
   naming the function and its arguments (here, always
   `get_internship_info` with a `section` value).
3. The Python code runs the real function and sends its return value
   back to the model as a `role: tool` message.
4. The model reads that result and writes the final answer. No further
   tool call is made — Day 3 only requires one round trip, unlike Day
   2's `agent.py`, which loops until the model stops requesting tools.

### 1.4 Why the tool returns errors as plain text, not an exception

If `get_internship_info("bogus")` raised an exception, the whole script
would crash before the model ever saw a response, and the user would
get a traceback instead of an answer. Returning
`"Unknown section: 'bogus'. Valid sections are: ..."` as a normal string
lets that message flow back through the same `role: tool` channel as a
successful result — the model can read it, explain the problem in plain
language, and the conversation continues.

### 1.5 Why a single tool call is enough here

Every private-data question in this scenario (total stipend, best
offer, amount paid so far) can be answered from one section of data —
`offers` or `payments` — with the arithmetic done by the model itself
in its final answer. None of the questions require chaining the result
of one tool call into the input of another, which is the case that
would need the loop from Day 2's `agent.py` instead.

## 2. Design

| | |
|---|---|
| Tool | `get_internship_info(section)` — one function, one enum parameter |
| Data sources | `intern_profile.json`, `offers.json`, `payment_history.json` |
| Questions needing the tool | Q1–Q3 (total stipend, best offer, amount paid) |
| Questions not needing the tool | Q4–Q5 (tax deduction reasoning, budgeting advice) |
| Loop | None — at most one tool call, then a final answer |

## 3. Comparison Table

| Criterion | Plain LLM (no tool) | LLM + tool |
|---|---|---|
| Source of answer | Model's training data only | Model's training data + Saran's real JSON files |
| Reliability on private questions | *(fill in from Run A)* | *(fill in from Run B)* |
| Transparency | No way to check where a number came from | Tool call is logged — you can see exactly which section was read and what it returned |
| Speed / cost | One API call per question | Up to two API calls per question (one to request the tool, one for the final answer), plus the tool schema adds tokens to every request |

## 4. Observations

*(Fill in after running `no_tool.py` and `with_tool.py`. For each
question: Run A's answer, Run B's tool call + answer, and whether Run A
guessed, refused, or was correct/incorrect by coincidence.)*

**Q1 — total TechNova stipend**
- Run A:
- Run B:

**Q2 — best offer overall**
- Run A:
- Run B:

**Q3 — amount paid so far**
- Run A:
- Run B:

**Q4 — why tax is deducted (general)**
- Run A:
- Run B: *(should show no tool call)*

**Q5 — budgeting advice (general)**
- Run A:
- Run B: *(should show no tool call)*

## 5. Suitability and Conclusion

*(Fill in once Section 4 is complete: when a plain LLM prompt is enough
vs. when a single tool call is worth the extra round trip, and whether
this scenario ever needed more than one tool call.)*
