"""The ONE tool for Day 3: get_internship_info(section).

Day 2 (agent.py/tools.py) had five separate tools. Day 3 only needs a
single tool call, so this collapses them into one function with a
'section' argument. It reads the three private JSON files and returns a
plain-text string — including on failure, which is what the Day 3 task
means by "the tool should return an error as text, not raise an
exception." A raised exception would crash the whole script; returned
text lets the LLM read the problem and tell the user, and lets the
program keep running.
"""
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"

with open(DATA_DIR / "intern_profile.json") as f:
    INTERN_PROFILE = json.load(f)
with open(DATA_DIR / "offers.json") as f:
    OFFERS = json.load(f)
with open(DATA_DIR / "payment_history.json") as f:
    PAYMENT_HISTORY = json.load(f)

VALID_SECTIONS = ("profile", "offers", "payments")


def get_internship_info(section: str) -> str:
    """Get one section of Saran's private internship data.

    section must be 'profile', 'offers', or 'payments'.
    """
    section = (section or "").strip().lower()

    if section == "profile":
        p = INTERN_PROFILE
        return (
            f"{p['intern_name']} is a {p['role']} at {p['current_company']}, "
            f"started {p['start_month']}."
        )

    if section == "offers":
        lines = [
            f"{o['company']} ({o['role']}): Rs. {o['monthly_stipend']}/month, "
            f"{o['tax_deduction_percent']}% tax deducted, {o['duration_months']} months duration"
            for o in OFFERS
        ]
        return "; ".join(lines)

    if section == "payments":
        lines = [
            f"{p['month']} ({p['company']}): paid Rs. {p['amount_paid']}, "
            f"tax deducted Rs. {p['tax_deducted']}"
            for p in PAYMENT_HISTORY
        ]
        return "; ".join(lines)

    return f"Unknown section: '{section}'. Valid sections are: {', '.join(VALID_SECTIONS)}"


# JSON Schema the LLM reads to decide whether/how to call the tool.
TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_internship_info",
        "description": (
            "Get Saran's private internship data. section must be one of: "
            "'profile' (name, current company, role, start month), "
            "'offers' (all three internship offers: monthly stipend, tax %, "
            "duration), or 'payments' (every payment made so far, with tax "
            "deducted)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "section": {
                    "type": "string",
                    "enum": list(VALID_SECTIONS),
                }
            },
            "required": ["section"],
        },
    },
}

if __name__ == "__main__":
    print("get_internship_info('profile')  ->", get_internship_info("profile"))
    print("get_internship_info('offers')   ->", get_internship_info("offers"))
    print("get_internship_info('payments') ->", get_internship_info("payments"))
    print("get_internship_info('bogus')    ->", get_internship_info("bogus"))
