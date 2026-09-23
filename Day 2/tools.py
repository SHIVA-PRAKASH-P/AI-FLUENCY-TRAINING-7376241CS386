"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator

from config import INTERN_PROFILE, OFFERS_BY_COMPANY, PAYMENT_HISTORY


def get_intern_profile() -> str:
    """Return the intern's name, current company, role, and start month."""
    return (
        f"{INTERN_PROFILE['intern_name']} is currently a {INTERN_PROFILE['role']} "
        f"at {INTERN_PROFILE['current_company']}, started {INTERN_PROFILE['start_month']}."
    )


def list_offers() -> str:
    """List every internship offer's company name."""
    return ", ".join(OFFERS_BY_COMPANY.keys())


def get_offer_details(company: str) -> str:
    """Get an offer's monthly stipend, tax deduction percent, and duration, by exact company name."""
    offer = OFFERS_BY_COMPANY.get(company)
    if offer is None:
        return f"Unknown company: {company}"
    return (
        f"{company} ({offer['role']}): Rs. {offer['monthly_stipend']}/month stipend, "
        f"{offer['tax_deduction_percent']}% tax deduction, {offer['duration_months']} month duration"
    )


def get_payment_history() -> str:
    """Get every recorded payment so far: month, company, amount paid, tax deducted."""
    lines = [
        f"{p['month']} ({p['company']}): paid Rs. {p['amount_paid']}, "
        f"tax deducted Rs. {p['tax_deducted']}"
        for p in PAYMENT_HISTORY
    ]
    return "; ".join(lines)


# A safe calculator: only numbers and + - * / ( ) are allowed. Never use eval().
_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.left), _evaluate(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        return _OPS[type(node.op)](_evaluate(node.operand))
    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression such as (15000 * 0.9 * 6)."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "get_intern_profile": get_intern_profile,
    "list_offers": list_offers,
    "get_offer_details": get_offer_details,
    "get_payment_history": get_payment_history,
    "calculator": calculator,
}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "get_intern_profile",
        "description": "Get the intern's name, current company, role, and start month.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "list_offers",
        "description": "List every internship offer's company name.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_offer_details",
        "description": "Get an offer's monthly stipend, tax deduction percent, and duration, by exact company name.",
        "parameters": {"type": "object",
                        "properties": {"company": {"type": "string"}},
                        "required": ["company"]}}},
    {"type": "function", "function": {
        "name": "get_payment_history",
        "description": "Get every recorded payment so far: month, company, amount paid, tax deducted.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("get_intern_profile() ->", get_intern_profile())
    print("list_offers() ->", list_offers())
    print("get_offer_details('TechNova') ->", get_offer_details("TechNova"))
    print("get_offer_details('DataForge') ->", get_offer_details("DataForge"))
    print("get_payment_history() ->", get_payment_history())
    print("calculator('15000 * 0.9 * 6') ->", calculator("15000 * 0.9 * 6"))
