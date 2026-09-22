"""System 2: a rule-based workflow. Fixed if/else rules, no LLM at all."""
from config import OFFERS_BY_COMPANY, PAYMENT_HISTORY, QUESTIONS


def _net_monthly(company):
    offer = OFFERS_BY_COMPANY[company]
    return offer["monthly_stipend"] * (1 - offer["tax_deduction_percent"] / 100)


def workflow(question):
    text = question.lower()

    # Rule 1: total received so far, across all past payments
    if "total" in text and "received" in text:
        total = sum(record["amount_paid"] for record in PAYMENT_HISTORY)
        return f"Total stipend received so far: Rs. {total:,.0f}"

    # Rule 2: hard-coded rule, only knows about TechNova's net stipend
    if "net" in text and "technova" in text:
        net = _net_monthly("TechNova")
        return f"Net monthly stipend for TechNova: Rs. {net:,.0f}"

    # Rule 3: hard-coded comparison, only knows TechNova vs CloudSprint tax rates
    if "tax" in text and "technova" in text and "cloudsprint" in text:
        tn_tax = OFFERS_BY_COMPANY["TechNova"]["tax_deduction_percent"]
        cs_tax = OFFERS_BY_COMPANY["CloudSprint"]["tax_deduction_percent"]
        if tn_tax > cs_tax:
            return f"Yes, TechNova's tax deduction ({tn_tax}%) is higher than CloudSprint's ({cs_tax}%) by {tn_tax - cs_tax} percentage points."
        return f"No, TechNova's tax deduction ({tn_tax}%) is not higher than CloudSprint's ({cs_tax}%)."

    return "Sorry, I do not have a rule for this type of question."


if __name__ == "__main__":
    print("\n=== SYSTEM 2: RULE-BASED WORKFLOW (no LLM) ===\n")
    for question in QUESTIONS:
        print("Q:", question)
        print("A:", workflow(question))
        print("-" * 70)
