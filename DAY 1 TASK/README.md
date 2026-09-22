# Day 1 — Internship Stipend Calculator (Chatbot vs Workflow vs Agent)

## Setup

1. Open this `stipend_lab` folder in VS Code (File > Open Folder).
2. Create and select a virtual environment:
   - `Ctrl+Shift+P` → `Python: Create Environment` → `Venv` → pick your Python 3.11+.
3. Open a terminal and install packages:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env`:
   ```
   copy .env.example .env
   ```
   This defaults to `PROVIDER=ollama`, `MODEL=qwen2.5:1.5b` — pull it first if you
   don't have it: `ollama pull qwen2.5:1.5b`. (Do not use `qwen2.5:3b` — it has a
   research licence, not Apache 2.0.) You can also point `MODEL` at `qwen3:4b`
   if that's already on your machine and supports tool calling.

## Run, in this order

```
python check_setup.py
python chatbot.py
python workflow.py
python tools.py
python agent.py
python challenge.py
```

Screenshot each run's terminal output for the `Output` folder.

## What to expect

- **chatbot.py**: has no access to the offers or payment history, so it will
  either ask you for numbers or answer generically. Only the thank-you
  message (Q4) needs no private data.
- **workflow.py**: exact, instant answers for TechNova's net stipend, the
  total received so far, and the TechNova-vs-CloudSprint tax comparison —
  but refuses the thank-you message question (no rule for it).
- **agent.py**: should call `calculate_net_monthly_stipend`,
  `get_total_received`, and `get_offer_details` as needed, then answer all
  four correctly.
- **challenge.py**: asks which offer has the highest total payout across
  all three companies — something no rule was written for. Watch the
  agent's printed steps carefully: does it check **all three** offers
  (TechNova, CloudSprint, DataForge) before answering, or does it stop
  early and guess? That's exactly the kind of reliability gap worth
  writing up in your analysis, the same way the vehicle-tracker agent
  answered a similar comparison question by checking only one of five
  tasks.

## Next steps for submission

1. Fill in `analysis_template.md` with your actual observations, then
   rename it `analysis.md`.
2. Push this to your GitHub repo (a new folder, e.g. `Day1-Stipend`, or
   wherever your instructor wants it) alongside your other Day 1 work.
3. Add an `Output` folder with your screenshots.
4. Update the submission Excel sheet with the link, if this is a separate
   submission from your vehicle-tracker one.
