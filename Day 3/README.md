# Day 3 — LLM with a Single Tool

Scenario: **Internship Stipend Assistant** for Saran , comparing a plain
LLM prompt against an LLM that can call one tool to look up private
internship data (profile, offers, payment history).

## Files

- `tool.py` — the one tool, `get_internship_info(section)`, plus its
  JSON Schema description.
- `no_tool.py` — Run A: plain LLM, no tool access.
- `with_tool.py` — Run B: LLM with the tool available. Makes at most one
  tool call per question, then gives a final answer. No loop.
- `config.py` — provider switch (ollama / groq / huggingface), shared
  question list.
- `data/` — `intern_profile.json`, `offers.json`, `payment_history.json`.
- `analysis.md` — write-up: concepts, comparison table, observations.
- `screenshots/` — put your terminal screenshots of both runs here.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# edit .env: set PROVIDER and, if using groq/huggingface, the API key
```

## Run

```bash
python no_tool.py
python with_tool.py
```

Both print each question, (for Run B) the tool call made, and the
answer. Neither script writes any output file — copy the terminal
output and take screenshots for `screenshots/`.

## Questions used

1. How much total net stipend will Saran receive by the end of the
   TechNova internship? *(needs tool: offers)*
2. Which internship offer gives the highest total net stipend overall?
   *(needs tool: offers)*
3. How much net stipend has Saran already been paid so far? *(needs
   tool: payments)*
4. Why do companies deduct tax from a stipend before paying it out?
   *(general knowledge, no tool)*
5. What's a sensible way to budget a monthly stipend as a student?
   *(general knowledge, no tool)*
