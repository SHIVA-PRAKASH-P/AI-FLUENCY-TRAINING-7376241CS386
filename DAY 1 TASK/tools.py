"""Tools the agent is allowed to use, plus their JSON Schema descriptions."""
import ast
import operator

from config import OFFERS, OFFERS_BY_COMPANY, PAYMENT_HISTORY


def list_offers() -> str:
    """List every internship offer's company name."""
    return ", ".join(OFFERS_BY_COMPANY.keys())


def get_offer_details(company: str) -> str:
    """Get the monthly stipend, duration, and tax deduction percent for one company's offer."""
    offer = OFFERS_BY_COMPANY.get(company)
    if offer is None:
        return f"Unknown company: {company}"
    return (
        f"{company}: monthly_stipend={offer['monthly_stipend']}, "
        f"duration_months={offer['duration_months']}, "
        f"tax_deduction_percent={offer['tax_deduction_percent']}"
    )


def calculate_net_monthly_stipend(company: str) -> str:
    """Calculate the take-home (after-tax) monthly stipend for one company's offer."""
    offer = OFFERS_BY_COMPANY.get(company)
    if offer is None:
        return f"Unknown company: {company}"
    net = offer["monthly_stipend"] * (1 - offer["tax_deduction_percent"] / 100)
    return str(net)


def calculate_total_payout(company: str) -> str:
    """Calculate the total take-home payout over the full duration of one offer."""
    offer = OFFERS_BY_COMPANY.get(company)
    if offer is None:
        return f"Unknown company: {company}"
    net_monthly = offer["monthly_stipend"] * (1 - offer["tax_deduction_percent"] / 100)
    total = net_monthly * offer["duration_months"]
    return str(total)


def get_total_received() -> str:
    """Sum the amount actually paid out so far across all past payments."""
    return str(sum(record["amount_paid"] for record in PAYMENT_HISTORY))


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
    """Evaluate a basic arithmetic expression such as (15000 * 0.9)."""
    try:
        return str(_evaluate(ast.parse(expression, mode="eval").body))
    except Exception as error:
        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "list_offers": list_offers,
    "get_offer_details": get_offer_details,
    "calculate_net_monthly_stipend": calculate_net_monthly_stipend,
    "calculate_total_payout": calculate_total_payout,
    "get_total_received": get_total_received,
    "calculator": calculator,
}

# These descriptions are what the LLM reads when deciding which tool to call
TOOLS = [
    {"type": "function", "function": {
        "name": "list_offers",
        "description": "List every internship offer's company name.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_offer_details",
        "description": "Get monthly stipend, duration, and tax deduction percent for one company's offer.",
        "parameters": {"type": "object",
                        "properties": {"company": {"type": "string"}},
                        "required": ["company"]}}},
    {"type": "function", "function": {
        "name": "calculate_net_monthly_stipend",
        "description": "Calculate the take-home (after-tax) monthly stipend for one company.",
        "parameters": {"type": "object",
                        "properties": {"company": {"type": "string"}},
                        "required": ["company"]}}},
    {"type": "function", "function": {
        "name": "calculate_total_payout",
        "description": "Calculate the total take-home payout over an offer's full duration.",
        "parameters": {"type": "object",
                        "properties": {"company": {"type": "string"}},
                        "required": ["company"]}}},
    {"type": "function", "function": {
        "name": "get_total_received",
        "description": "Get the total amount actually paid out so far across all past payments.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "calculator",
        "description": "Evaluate an arithmetic expression using + - * / and brackets.",
        "parameters": {"type": "object",
                        "properties": {"expression": {"type": "string"}},
                        "required": ["expression"]}}},
]

if __name__ == "__main__":
    print("list_offers() ->", list_offers())
    print("get_offer_details('TechNova') ->", get_offer_details("TechNova"))
    print("calculate_net_monthly_stipend('TechNova') ->", calculate_net_monthly_stipend("TechNova"))
    print("calculate_total_payout('DataForge') ->", calculate_total_payout("DataForge"))
    print("get_total_received() ->", get_total_received())
    print("calculator('(15000 * 0.9)') ->", calculator("(15000 * 0.9)"))
