# Internship Stipend Assistant — Direct vs CoT vs ReAct

Same structure as the vehicle-maintenance-agent project, applied to a
new scenario: comparing internship offers by total net (after-tax)
stipend.

## Scenario

**Intern:** Saran, currently an AI/ML Intern at TechNova since 2026-06.

- `data/intern_profile.json` — current company, role, start month
- `data/offers.json` — 3 offers (TechNova, CloudSprint, DataForge),
  each with monthly stipend, duration, and tax deduction %
- `data/payment_history.json` — 3 months of actual payments already
  received from TechNova

**Tool-needing question** (needs live data — can't be answered from
parametric knowledge alone):
> "Based on my current internship at TechNova, how much total net
> stipend will I receive by the time it ends, how much have I already
> been paid, and which of the three available offers would give me the
> highest total net stipend overall?"

**Reasoning-only questions** (all data is inside the question itself —
no tool required, but every number comes from the actual offers):
1. Arithmetic: total net stipend for CloudSprint over its full 3-month duration
2. Multi-step comparison: DataForge vs. TechNova total net stipend
3. Ordering/logic: rank all three offers by total net stipend, and identify the lowest tax rate

## Files

| File | Role |
|---|---|
| `config.py` | Picks the LLM provider (Ollama/Groq/Hugging Face via `.env`), loads the three JSON files from `data/`, defines `client`, `MODEL`, `banner` |
| `tools.py` | `get_intern_profile`, `list_offers`, `get_offer_details(company)`, `get_payment_history`, `calculator` (safe AST-based, no `eval`) |
| `agent.py` | ReAct loop: reasons, calls tools, feeds results back, repeats until a final answer or `max_steps` |
| `data/` | `intern_profile.json`, `offers.json`, `payment_history.json` |
| `react_trace.py` | **Approach 3 (ReAct):** runs the tool-needing question through `agent()`, printing every step |
| `cot_compare.py` | **Approaches 1 & 2 (Direct vs CoT):** asks all three reasoning-only questions both ways, `temperature=0` |
| `self_consistency.py` | Runs the first CoT question 5× at `temperature=0.8` and takes the majority answer |

## Setup

```bash
pip install openai python-dotenv
```

Create a `.env` file and add api key or local AI

## How to run

```bash
python react_trace.py        # Approach 3: ReAct on the tool-needing question
python cot_compare.py        # Approaches 1 & 2: direct vs CoT on 3 reasoning questions
python self_consistency.py   # Self-consistency: 5 CoT runs + majority vote
```

## Expected results (to check your actual run against)

Worked by hand from the raw data, so you can verify the agent got it right:

| Offer | Net monthly (after tax) | Duration | Total net stipend |
|---|---|---|---|
| TechNova | 15,000 × 0.90 = 13,500 | 6 months | **81,000** |
| CloudSprint | 20,000 × 0.95 = 19,000 | 3 months | **57,000** |
| DataForge | 12,000 × 0.92 = 11,040 | 8 months | **88,320** |

- **`react_trace.py`** should find: TechNova will pay **81,000** total,
  Saran has already been paid **40,500** (3 × 13,500, matching
  `payment_history.json` exactly), and **DataForge** gives the highest
  total net stipend overall (88,320) — despite having the *lowest*
  monthly amount, because its 8-month duration outweighs the smaller
  monthly figure. This is a good case for checking the agent isn't
  just picking the highest monthly stipend without doing the full
  calculation.
- **`cot_compare.py`**: Q1 = **57,000**, Q2 = **DataForge higher by
  7,320** (88,320 − 81,000), Q3 = **DataForge (88,320) > TechNova
  (81,000) > CloudSprint (57,000); CloudSprint has the lowest tax rate
  (5%)**.
- **`self_consistency.py`**: expect the 5 runs on Q1 to converge on
  57,000; watch for the same formatting-artifact issue seen in the
  vehicle project, where slightly different wording of the same number
  can undercount the "majority" even when every run agrees.

