from collections import defaultdict
from deepagents import create_deep_agent
from langchain_core.tools import tool


# ---------------------------
# Tools
# ---------------------------
@tool
def classify_transactions(raw_transactions: str) -> str:
    """
    Classify each transaction into one category:
    food, transport, shopping, subscription, etc.
    Input must be a plain text list of transactions.
    Return a clean categorized summary.
    """
    lines = [line.strip() for line in raw_transactions.split("\n") if line.strip()]
    result = []

    for line in lines:
        if "스타벅스" in line or "배달의민족" in line:
            category = "food"
        elif "지하철" in line or "버스" in line:
            category = "transport"
        elif "쿠팡" in line:
            category = "shopping"
        else:
            category = "other"

        result.append(f"{line} -> {category}")

    return "\n".join(result)


@tool
def calculate_category_totals(raw_transactions: str) -> str:
    """
    Calculate simple totals by category from a plain text list of transactions.
    Return category totals.
    """
    totals = defaultdict(int)
    lines = [line.strip() for line in raw_transactions.split("\n") if line.strip()]

    for line in lines:
        amount = 0
        digits = "".join(ch for ch in line if ch.isdigit())
        if digits:
            amount = int(digits)

        if "스타벅스" in line or "배달의민족" in line:
            totals["food"] += amount
        elif "지하철" in line or "버스" in line:
            totals["transport"] += amount
        elif "쿠팡" in line:
            totals["shopping"] += amount
        else:
            totals["other"] += amount

    return "\n".join(f"{k}: {v}원" for k, v in totals.items())


@tool
def compare_to_budget(category_totals: str) -> str:
    """
    Compare category totals to a simple monthly budget.
    Input example:
    food: 23000원
    transport: 1250원
    shopping: 32000원
    """
    budgets = {
        "food": 150000,
        "transport": 60000,
        "shopping": 120000,
        "other": 50000,
    }

    lines = [line.strip() for line in category_totals.split("\n") if line.strip()]
    output = []

    for line in lines:
        if ":" not in line:
            continue

        category, amount_text = line.split(":", 1)
        category = category.strip()
        digits = "".join(ch for ch in amount_text if ch.isdigit())
        amount = int(digits) if digits else 0
        budget = budgets.get(category, 50000)

        status = "within budget" if amount <= budget else "over budget"
        output.append(f"{category}: {amount}원 / budget {budget}원 -> {status}")

    return "\n".join(output)


# ---------------------------
# Subagents
# ---------------------------
subagents = [
    {
        "name": "classifier",
        "description": "Classifies transactions into spending categories.",
        "system_prompt": """
You are a transaction classification specialist.
Your only job is to classify transactions into categories.
Use the provided tools when helpful.
Return concise categorized results only.
""",
        "tools": [classify_transactions],
        "model": "openai:gpt-4o-mini",
    },
    {
        "name": "analyst",
        "description": "Analyzes spending patterns and category totals.",
        "system_prompt": """
You are a spending analysis specialist.
Your job is to analyze the transaction data and identify patterns,
major spending categories, and possible overspending.
Use the provided tools when helpful.
Return concise insights only.
""",
        "tools": [calculate_category_totals],
        "model": "openai:gpt-4o-mini",
    },
    {
        "name": "budget-planner",
        "description": "Checks spending against budget and suggests savings strategies.",
        "system_prompt": """
You are a budget planning specialist.
Your job is to compare spending totals against a budget
and suggest realistic saving strategies.
Use the provided tools when helpful.
Return concise action-oriented advice.
""",
        "tools": [compare_to_budget],
        "model": "openai:gpt-4o-mini",
    },
    {
        "name": "report-writer",
        "description": "Writes the final finance report for the user.",
        "system_prompt": """
You are a financial report writer.
Combine the delegated subagent outputs into one final report.

Your report must include:
1. transaction categories
2. spending pattern summary
3. budget status
4. savings suggestions

Keep it clear and easy to read.
""",
        "tools": [],
        "model": "openai:gpt-4o-mini",
    },
]

# ---------------------------
# Supervisor
# ---------------------------
supervisor = create_deep_agent(
    model="openai:gpt-4o-mini",
    system_prompt="""
You are the supervisor of a smart finance agent team.

For this task, delegate work to the specialized subagents.
Use:
- classifier for categorization
- analyst for spending analysis
- budget-planner for budget checking
- report-writer for the final answer

Do not do everything yourself.
Delegate first, then combine the results into one final answer.
""",
    subagents=subagents,
)

# ---------------------------
# Data
# ---------------------------
transactions = [
    {"text": "스타벅스 5000원"},
    {"text": "지하철 1250원"},
    {"text": "쿠팡 쇼핑 32000원"},
    {"text": "배달의민족 18000원"},
]

raw_text = "\n".join(item["text"] for item in transactions)

# ---------------------------
# Run
# ---------------------------
result = supervisor.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": f"""
Analyze the following transactions and produce a smart finance report.

Transactions:
{raw_text}
""",
            }
        ]
    }
)

print(result)